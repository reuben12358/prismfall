#===============================================================================
# Prismfall Bosses - 006 Starting boss battles (events), trainer bosses,
# EBDX intro styling and the Festival switch.
#===============================================================================
module Prismfall
  module Bosses
    #---------------------------------------------------------------------------
    # Wild boss.  Event: Conditional Branch > Script: Prismfall::Bosses.wild_battle(:KYOGRE_ISENMAR)
    # Options: field: (nil = definition's, :NONE = none), can_lose:, size: ("2v1"),
    #          level:, music:, outcome_var:. Returns true on a win/capture/scripted end.
    #---------------------------------------------------------------------------
    def self.wild_battle(id, **opts)
      raise ArgumentError, "Unknown boss #{id.inspect}" if !exists?(id)
      pkmn = create_pokemon(id, opts[:level])
      return start_wild(pkmn, id, **opts)
    end

    def self.start_wild(pkmn, id, **opts)
      data = get(id)
      prepare_rules(data, opts, true)
      setup_ebdx(data, true)
      music = opts[:music] || resolve(data[:music])
      @default_music_for = nil
      if !music && ($PokemonGlobal.nil? || !$PokemonGlobal.nextBattleBGM)
        music = default_music(id, data)
        @default_music_for = id if music
      end
      $PokemonGlobal.nextBattleBGM = music if music && $PokemonGlobal
      @last_result = nil
      EventHandlers.trigger(:prismfall_boss_starting, id, pkmn)
      ret = WildBattle.start(pkmn, can_override: false)
      return (ret) ? true : false
    end

    # Music for a wild boss that names none (design/AUDIO.md 5.C2): the Arceus theme, the legendary theme for a
    # boss that can be caught, else the boss theme. Only installed files; nil = the map's usual wild battle music.
    def self.default_music(id, data)
      return nil if !defined?(Prismfall::AudioCue)
      cue = :boss
      cue = :boss_legendary if (resolve(data[:catch]) rescue false)
      cue = :boss_arceus if id.to_s.start_with?("ARCEUS")
      return Prismfall::AudioCue.resolve("BGM", Prismfall::AudioCue::BGM, cue)
    rescue StandardError
      return nil
    end

    # The boss id whose battle is playing the default music (so the last bar may swap to the final-bar track).
    def self.default_music_for; return @default_music_for; end

    def self.rule_set?(*keys)
      rules = ($game_temp) ? $game_temp.battle_rules : {}
      return keys.any? { |k| rules.key?(k) }
    end

    def self.prepare_rules(data, opts, wild)
      if wild
        setBattleRule((resolve(data[:can_run])) ? "canRun" : "cannotRun") if !rule_set?("canRun")
        size = opts[:size] || resolve(data[:size])
        setBattleRule(size) if size && !rule_set?("size")
      end
      setBattleRule("canLose") if (opts[:can_lose] || resolve(data[:can_lose])) && !rule_set?("canLose")
      setBattleRule("outcomeVar", opts[:outcome_var]) if opts[:outcome_var]
      field = opts.key?(:field) ? opts[:field] : resolve(data[:field])
      if field && defined?(FieldEffects) && !rule_set?("field")
        setBattleRule("field", (field == :NONE) ? "none" : field)
      end
      w = resolve(data[:weather])
      setBattleRule("weather", w) if w && !rule_set?("weather")
      t = resolve(data[:terrain])
      setBattleRule("terrain", t) if t && !rule_set?("terrain")
    end

    # EBDX: boss databox/intro for wild bosses; this plugin owns the HP
    # thresholds, so Renovation's :damageCap is cleared.
    def self.setup_ebdx(data, wild)
      return if !defined?(EliteBattle)
      eb = resolve(data[:ebdx]) || {}
      if wild && eb.fetch(:databox, EBDX_BOSS_DATABOX)
        ui = (EliteBattle.get_data(:BOSSDATABOX, :Metrics, :METRICS) rescue nil)
        EliteBattle.set(:nextUI, ui || { :ENEMYDATABOX => { :BITMAP => "dataBoxBoss", :CONTAINER => "containersBoss" } })
        EliteBattle.set(:setBoss, true) rescue nil
      end
      EliteBattle.set(:damageCap, []) rescue nil
      EliteBattle.set(:nextBattleScript, eb[:script]) if eb[:script]
    end

    #---------------------------------------------------------------------------
    # Trainer bosses (a trainer whose ace is a boss)
    #   Script: Prismfall::Bosses.trainer_battle(:LEADER_ILSA, "Ilsa", 0, boss: :WARDEN_ACE_2BAR)
    #   Before another helper (e.g. Prismfall.gym_battle(12)):
    #   Script: Prismfall::Bosses.mark_next_trainer(:WARDEN_ACE_2BAR)
    # slot: :ace (last Pokémon, default), :lead, or a party index; species: picks by species.
    #---------------------------------------------------------------------------
    def self.mark_next_trainer(boss, slot: :ace, species: nil, trainer_type: nil)
      raise ArgumentError, "Unknown boss #{boss.inspect}" if !exists?(boss)
      @pending_trainer = { :boss => boss, :slot => slot, :species => species, :trainer_type => trainer_type }
    end

    def self.trainer_battle(tr_type, tr_name, version = 0, boss:, slot: :ace, species: nil, lose_text: nil, **opts)
      mark_next_trainer(boss, slot: slot, species: species, trainer_type: tr_type)
      prepare_rules(get(boss), opts, false)
      setup_ebdx(get(boss), false)
      @last_result = nil
      begin
        return TrainerBattle.start([tr_type, tr_name, version, lose_text])
      ensure
        @pending_trainer = nil
      end
    end

    # Standing rules, checked on every trainer load:
    #   register_trainer_boss(:KEY, { :trainer_type => :LEADER_ILSA, :name => "Ilsa", :versions => [0, 100],
    #                                 :condition => proc { |trainer| Prismfall::Difficulty.hard? },
    #                                 :slot => :ace, :boss => :WARDEN_ACE_2BAR })
    def self.register_trainer_boss(key, rule)
      @trainer_rules[key] = rule
    end

    def self.trainer_rules; return @trainer_rules; end

    def self.rule_matches?(rule, trainer)
      return false if rule[:trainer_type] && !Array(rule[:trainer_type]).include?(trainer.trainer_type)
      return false if rule[:name] && !Array(rule[:name]).include?(trainer.name)
      v = rule[:versions]
      if v
        ver = (trainer.respond_to?(:version)) ? trainer.version.to_i : 0
        return false if !(v.is_a?(Range) || v.is_a?(Array) ? v.include?(ver) : v == ver)
      end
      return false if rule[:condition] && !rule[:condition].call(trainer)
      return exists?(rule[:boss])
    end

    def self.pick_party_member(party, slot, species)
      list = party.select { |p| p && !p.egg? }
      return list.find { |p| p.isSpecies?(species) } if species
      case slot
      when :lead    then return list.first
      when Integer  then return party[slot]
      end
      return list.last
    end

    def self.apply_trainer_rules(trainer)
      return if !trainer || !trainer.respond_to?(:party)
      pt = @pending_trainer
      if pt && (!pt[:trainer_type] || pt[:trainer_type] == trainer.trainer_type)
        @pending_trainer = nil
        make_boss(pick_party_member(trainer.party, pt[:slot], pt[:species]), pt[:boss])
      end
      @trainer_rules.each_value do |rule|
        next if !rule_matches?(rule, trainer)
        pkmn = pick_party_member(trainer.party, rule[:slot] || :ace, rule[:species])
        make_boss(pkmn, rule[:boss]) if pkmn && !pkmn.prismfall_boss_id
      end
    end

    #---------------------------------------------------------------------------
    # Festival (Core 009_Festival.rb boss_battle) - clean switch
    #---------------------------------------------------------------------------
    def self.festival_boss_for(stage)
      return nil if !festival_enabled? || !stage.is_a?(Hash)
      id = (stage.key?(:prismfall_boss)) ? stage[:prismfall_boss] : FESTIVAL_BOSSES[stage[:id]]
      return (id && exists?(id)) ? id : nil
    end

    # next_match has already applied the stage's rule set, field and extra rules.
    def self.festival_battle(id, stage)
      pkmn = create_pokemon(id, stage[:level])
      EventHandlers.trigger(:prismfall_festival_boss, pkmn, stage[:id])
      return start_wild(pkmn, id)
    end
  end
end

EventHandlers.add(:on_trainer_load, :prismfall_bosses_trainer_rules,
  proc { |trainer| Prismfall::Bosses.apply_trainer_rules(trainer) }
)

if defined?(Prismfall::Festival) && Prismfall::Festival.respond_to?(:boss_battle)
  module Prismfall
    module Festival
      class << self
        alias_method :prismfall_bosses_boss_battle, :boss_battle unless method_defined?(:prismfall_bosses_boss_battle)

        def boss_battle(stage)
          id = Prismfall::Bosses.festival_boss_for(stage)
          return Prismfall::Bosses.festival_battle(id, stage) if id
          return prismfall_bosses_boss_battle(stage)
        end
      end
    end
  end
end
