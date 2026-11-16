#===============================================================================
# Scripted probes: short real battles in which the player's moves are scripted
# (the foe only uses Splash), forcing each field's signature interactions.
# Probe plans are DERIVED from the field definitions, so every transition rule,
# seed rule and end-of-round rule of every field gets its own mini battle.
#===============================================================================
module Harness
  class BattleLog
    def hits; @hits ||= []; end   # [battler index, damage] for every move hit
  end

  class LogScene
    alias __probe_hit pbHitAndHPLossAnimation
    def pbHitAndHPLossAnimation(targets)
      targets.each { |t| @log.hits << [t[0].index, t[1] - t[0].hp] }
      __probe_hit(targets)
    end
  end

  module Probes
    TYPE_MOVES = { :NORMAL => :SWIFT, :FIRE => :FLAMETHROWER, :WATER => :WATERPULSE, :GRASS => :ENERGYBALL,
                   :ELECTRIC => :THUNDERBOLT, :ICE => :ICEBEAM, :FIGHTING => :AURASPHERE, :POISON => :SLUDGEBOMB,
                   :GROUND => :EARTHPOWER, :FLYING => :AIRSLASH, :PSYCHIC => :PSYCHIC, :BUG => :BUGBUZZ,
                   :ROCK => :POWERGEM, :GHOST => :SHADOWBALL, :DRAGON => :DRAGONPULSE, :DARK => :DARKPULSE,
                   :STEEL => :FLASHCANNON, :FAIRY => :MOONBLAST }.freeze
    TYPE_SPECIES = { :NORMAL => :SNORLAX, :FIRE => :ARCANINE, :WATER => :MILOTIC, :GRASS => :TANGROWTH,
                     :ELECTRIC => :AMPHAROS, :ICE => :GLALIE, :FIGHTING => :MACHAMP, :POISON => :MUK,
                     :GROUND => :HIPPOWDON, :FLYING => :TORNADUS, :PSYCHIC => :ALAKAZAM, :BUG => :PINSIR,
                     :ROCK => :GIGALITH, :GHOST => :DUSKNOIR, :DRAGON => :HAXORUS, :DARK => :UMBREON,
                     :STEEL => :KLINKLANG, :FAIRY => :FLORGES }.freeze
    WEATHER_MOVES = { :Rain => :RAINDANCE, :Sun => :SUNNYDAY, :Sandstorm => :SANDSTORM, :Hail => :HAIL }.freeze
    WEATHER_ABILITIES = { :HeavyRain => :PRIMORDIALSEA, :HarshSun => :DESOLATELAND, :StrongWinds => :DELTASTREAM }.freeze
    TERRAIN_MOVES = { :Electric => :ELECTRICTERRAIN, :Grassy => :GRASSYTERRAIN, :Misty => :MISTYTERRAIN,
                      :Psychic => :PSYCHICTERRAIN }.freeze
    FALLBACK_MOVES = [:FLAMETHROWER, :EARTHQUAKE, :SURF, :THUNDERBOLT, :HYPERVOICE, :ICEBEAM, :BULLDOZE,
                      :ROCKSLIDE, :HURRICANE, :GIGAIMPACT, :STOMPINGTANTRUM, :FIREBLAST, :MAGNITUDE,
                      :HEAVYSLAM, :BODYSLAM, :EXPLOSION].freeze

    # A fully deterministic Pokemon (fixed IVs/nature) so paired runs are comparable.
    def self.mk(species, level = 100, moves: [:SPLASH], ability: nil, item: nil, status: nil, hp_frac: nil)
      p = Pokemon.new(species, level)
      GameData::Stat.each_main { |s| p.iv[s.id] = 31; p.ev[s.id] = 0 }
      p.nature = :HARDY
      p.ability = ability if ability
      p.item = item
      p.forget_all_moves
      moves.first(4).each { |m| p.learn_move(m) }
      p.calc_stats
      p.hp = [(p.totalhp * hp_frac).floor, 1].max if hp_frac
      if status == :TOXIC
        p.status = :POISON; p.statusCount = 1
      elsif status && status != :NONE
        p.status = status
        p.statusCount = 3 if status == :SLEEP
      end
      p
    end

    # Runs one scripted wild battle. script: Array of move IDs (or procs returning one);
    # when it runs out the battle is ended. rng: nil (seeded random), :mid or :zero (fixed rolls).
    def self.mini(title, field:, user:, foe:, script:, rng: nil, stage: nil, seed: 4242)
      $player.party = [user]
      info = { :snaps => [], :used => [], :refused => [] }
      setup = lambda do |battle|
        info[:battle] = battle
        battle.define_singleton_method(:pbRandom) { |x| (rng == :mid) ? x / 2 : 0 } if rng
        queue = script.dup
        battle.instance_variable_get(:@battleAI).define_singleton_method(:pbDefaultChooseEnemyCommand) do |idx|
          b = @battle.battlers[idx]
          if !@battle.pbOwnedByPlayer?(idx)
            @battle.pbRegisterMove(idx, 0, false)
          else
            foe_b = @battle.battlers[1]
            info[:snaps] << { :hp => b.hp, :item => b.item_id, :status => b.status, :stages => b.stages.dup,
                              :types => b.pbTypes(true), :foe_hp => foe_b&.hp, :field => @battle.field_effect,
                              :stage => @battle.field_stage, :weather => @battle.field.weather,
                              :borrowed => FieldEffects.borrowed_fields(@battle).dup }
            step = queue.shift
            step = step.call(@battle, b) if step.is_a?(Proc)
            if step.nil?
              @battle.decision = 3
            else
              i = b.moves.index { |m| m.id == step }
              if !i
                b.moves[0] = Battle::Move.from_pokemon_move(@battle, Pokemon::Move.new(step))
                i = 0
              end
              info[:used] << step
              info[:refused] << step if !@battle.pbRegisterMove(idx, i, false)
            end
          end
        end
      end
      log = Harness.run_battle(title, :seed => seed, :setup => setup) do
        setBattleRule("field", (field == :NONE) ? "none" : field)
        setBattleRule("fieldStage", stage) if stage && field != :NONE
        setBattleRule("canLose")
        setBattleRule("cannotRun")
        WildBattle.start(foe)
      end
      [log, info]
    end

    def self.neutral_foe(move_id)
      type = GameData::Move.get(move_id).type
      sp = [:SNORLAX, :MILOTIC, :UMBREON, :ALAKAZAM].find do |s|
        Effectiveness.normal?(Effectiveness.calculate(type, *GameData::Species.get(s).types))
      end
      mk(sp || :SNORLAX)
    end

    #---------------------------------------------------------------------------
    # Probe 1: a field-boosted move. Same move, same rolls, with and without the field.
    #---------------------------------------------------------------------------
    def self.boost_candidates(field)
      d = FieldEffects.get(field)
      list = []
      (d[:type_mods] || {}).each { |t, m| list << [TYPE_MOVES[t], "#{t}-type moves x#{m}"] if m > 1 && TYPE_MOVES[t] }
      (d[:move_mods] || {}).each { |mv, m| list << [mv, "#{GameData::Move.get(mv).name} x#{m}"] if m > 1 }
      (d[:damage_mods] || []).each do |r|
        m = r[:mult] || r[:final_mult]
        next if !m || m <= 1
        (r[:moves] || []).first(2).each { |mv| list << [mv, "#{GameData::Move.get(mv).name} x#{m} (damage rule)"] }
      end
      list
    end

    def self.probe_boost(field, out)
      cands = boost_candidates(field)
      borrowing = FieldEffects.get(field)[:borrow]
      if cands.empty? && borrowing
        # Borrowing fields (BLEED, PRISM_ARENA): wait for an overlay, then use a move it boosts.
        picked = nil
        chooser = lambda do |battle, _b|
          bid = FieldEffects.borrowed_fields(battle).find { |f| !boost_candidates(f).empty? }
          next :SPLASH if !bid
          picked ||= [boost_candidates(bid).first[0], bid]
          picked[0]
        end
        script = Array.new(12) { lambda { |battle, b| picked ? nil : chooser.call(battle, b) } }
        log, = mini("#{field} probe: boosted move through a borrowed field", :field => field, :user => mk(:MEW),
                    :foe => mk(:MILOTIC), :script => script, :rng => :mid)
        out << log
        return { :ok => false, :detail => "no overlay with a boost appeared in 12 rounds" } if !picked
        with = log.hits.find { |h| h[0] == 1 }&.[](1)
        base_log, = mini("#{field} probe: baseline (no field) for #{picked[0]}", :field => :NONE, :user => mk(:MEW),
                         :foe => mk(:MILOTIC), :script => [picked[0]], :rng => :mid)
        out << base_log
        base = base_log.hits.find { |h| h[0] == 1 }&.[](1)
        ok = with && base && with > base * 1.03
        return { :ok => ok ? true : false, :move => picked[0], :with => with, :without => base,
                 :detail => "#{GameData::Move.get(picked[0]).name} while borrowing #{picked[1]}: #{with} dmg vs #{base} with no field" }
      end
      last = { :ok => false, :detail => "field defines no flat damage boost" }
      cands.first(4).each do |move, why|
        runs = [field, :NONE].map do |f|
          log, = mini("#{field} probe: boosted move #{move} (#{f == :NONE ? 'baseline, no field' : 'on field'})",
                      :field => f, :user => mk(:MEW, :moves => [move]), :foe => neutral_foe(move),
                      :script => [move], :rng => :mid)
          [log, log.hits.find { |h| h[0] == 1 }&.[](1)]
        end
        with, base = runs[0][1], runs[1][1]
        ok = with && base && base > 0 && with > base * 1.03
        last = { :ok => ok ? true : false, :move => move, :with => with, :without => base,
                 :ratio => (with && base && base > 0) ? (with.to_f / base).round(2) : nil,
                 :detail => "#{GameData::Move.get(move).name}: #{with.inspect} dmg on field vs #{base.inspect} without (#{why})" }
        out << runs[0][0] << runs[1][0] if ok || move == cands.first(4).last[0]
        break if ok
      end
      last
    end

    #---------------------------------------------------------------------------
    # Probe 2: every transition rule.
    #---------------------------------------------------------------------------
    def self.move_matches?(m, rule)
      return false if rule[:not_moves]&.include?(m.id)
      return false if rule[:types] && !rule[:types].include?(m.type)
      return false if rule[:not_types]&.include?(m.type)
      return false if rule[:flags] && !rule[:flags].any? { |f| m.flags.any? { |mf| mf.casecmp?(f) } }
      return false if rule[:function_codes] && !rule[:function_codes].include?(m.function_code)
      if rule[:category]
        cats = Array(rule[:category])
        ok = cats.any? do |c|
          case c
          when :physical then m.category == 0
          when :special  then m.category == 1
          when :status   then m.category == 2
          when :damaging then m.category != 2
          end
        end
        return false if !ok
      end
      true
    end

    def self.moves_for_rule(rule)
      if rule[:moves]
        return rule[:moves].select { |m| GameData::Move.exists?(m) }.first(5)
      end
      if (rule.keys & [:types, :flags, :category, :function_codes]).empty?
        return FALLBACK_MOVES.dup   # pure :condition rule: try a spread of moves
      end
      picks = []
      Array(rule[:types]).each { |t| picks << TYPE_MOVES[t] if TYPE_MOVES[t] }
      GameData::Move.each do |m|
        next if m.power < 40 || m.power > 100 || m.accuracy != 100 || m.function_code != "None"
        picks << m.id
      end
      GameData::Move.each { |m| picks << m.id }
      picks.uniq.select { |id| move_matches?(GameData::Move.get(id), rule) }.first(4)
    end

    def self.describe_rule(rule)
      trig = if rule[:weather] then "weather #{rule[:weather].join('/')}"
             elsif rule[:terrain] then "terrain #{rule[:terrain].join('/')}"
             elsif rule[:turns] then "after #{rule[:turns]} rounds"
             elsif rule[:check] then "check proc"
             elsif rule[:moves] then "moves #{rule[:moves].first(3).join('/')}#{rule[:moves].size > 3 ? '...' : ''}"
             else (rule.keys & [:types, :flags, :category, :function_codes, :condition]).map { |k|
               k == :condition ? "condition proc" : "#{k} #{Array(rule[k]).join('/')}" }.join(", ")
             end
      dest = if rule[:to] then "-> #{rule[:to].is_a?(Proc) ? '(proc)' : rule[:to]}"
             elsif rule[:stage] then "-> stage #{rule[:stage]}"
             elsif rule[:stage_delta] then "-> stage #{format('%+d', rule[:stage_delta])}"
             else "rewinds #{rule[:rewind].inspect}"
             end
      "#{trig}#{rule[:uses] ? " x#{rule[:uses]}" : ''} #{dest}"
    end

    def self.transition_fired?(log, info, field, rule, start_stage)
      if rule[:to]
        return log.field_changes.any? { |o, n, _| o == field && n != field && (rule[:to].is_a?(Proc) || n == rule[:to]) } ||
               (rule[:to] == :NONE && info[:snaps].any? { |s| s[:field] == :NONE })
      elsif rule[:stage] || rule[:stage_delta]
        return log.field_changes.any? { |o, n, st| o == field && n == field && st != start_stage }
      elsif rule[:message]
        return log.include?(Harness.message_regexp(rule[:message]))
      end
      false
    end

    def self.probe_transitions(field, out)
      results = []
      seen = {}
      stages = [1] + (FieldEffects.get(field)[:stages] || {}).keys.sort
      max_stage = stages.max
      stages.each do |st|
        rules = FieldEffects.definition_for(field, st)[:transitions] || []
        rules.each do |rule|
          key = rule.inspect
          next if seen[key]
          seen[key] = true
          start = st
          start = [st, 2].max if rule[:stage_delta] && rule[:stage_delta] < 0 && max_stage > 1
          start = (rule[:stage] == 1) ? 2 : 1 if rule[:stage] && rule[:stage] == start
          desc = "stage #{st}: " + describe_rule(rule)
          uses = rule[:uses] || 1
          scripts = []
          weather_ability = nil
          if rule[:weather]
            mv = rule[:weather].map { |w| WEATHER_MOVES[w] }.compact.first
            scripts << [mv] * uses if mv
            if !mv && (weather_ability = rule[:weather].map { |w| WEATHER_ABILITIES[w] }.compact.first)
              scripts << [:SPLASH]
            end
          elsif rule[:terrain]
            mv = rule[:terrain].map { |t| TERRAIN_MOVES[t] }.compact.first
            scripts << [mv] * uses if mv
          elsif rule[:turns]
            scripts << [:SPLASH] * (rule[:turns] + 1)
          elsif rule[:check]
            scripts = []
          else
            prefix = []
            if !rule[:to] && !rule[:stage] && !rule[:stage_delta] && rule[:rewind]
              # Rewind-only rule: first make progress on the rule it rewinds.
              rid = rule[:rewind].is_a?(Hash) ? rule[:rewind].keys.first : Array(rule[:rewind]).first
              tgt = rules.find { |r| r[:id] == rid }
              pm = tgt && (results.find { |r| r[:rule_id] == rid && r[:ok] }&.[](:move) || moves_for_rule(tgt).first)
              prefix = [pm] if pm
            end
            moves_for_rule(rule).each { |mv| scripts << prefix + ([mv] * uses) }
          end
          if scripts.empty?
            results << { :desc => desc, :ok => false, :forced => false,
                         :detail => "not forced (trigger is a #{rule[:check] ? 'check proc' : 'weather/terrain no move sets'})" }
            next
          end
          res = nil
          # Status moves that need a stat change on the target (Topsy-Turvy) get a Growl first.
          scripts += scripts.select { |sc| GameData::Move.get(sc.last).category == 2 }.map { |sc| [:GROWL] + sc }
          um = rule[:user] || {}
          user_species = (um[:types] && TYPE_SPECIES[um[:types].first]) || :MEW
          scripts.each do |script|
            mv = script.last
            foe = neutral_foe(mv)
            foe = mk(TYPE_SPECIES[rule[:target][:types].first]) if rule[:target] && rule[:target][:types]
            log, info = mini("#{field} probe: transition [#{desc}] using #{script.join(', ')}", :field => field,
                             :stage => start,
                             :user => mk(user_species, :moves => script.uniq, :ability => weather_ability || um[:abilities]&.first,
                                         :item => um[:items]&.first),
                             :foe => foe, :script => script + [:SPLASH])
            ok = transition_fired?(log, info, field, rule, start)
            res = { :desc => desc, :ok => ok, :forced => true, :move => mv, :rule_id => rule[:id], :log => log,
                    :detail => ok ? "fired with #{script.map { |m| GameData::Move.get(m).name }.join(', ')}" :
                                    "did NOT fire with #{script.join(', ')}" }
            break if ok
          end
          out << res.delete(:log)
          results << res
        end
      end
      results
    end

    #---------------------------------------------------------------------------
    # Probe 3: seeds.
    #---------------------------------------------------------------------------
    def self.probe_seeds(field, out)
      Array(FieldEffects.get(field)[:seed]).compact.map do |rule|
        item = rule[:item]
        log, info = mini("#{field} probe: #{GameData::Item.get(item).name} held on entry", :field => field,
                         :user => mk(:MEW, :item => item, :hp_frac => 0.5), :foe => mk(:SNORLAX),
                         :script => [:SPLASH])
        out << log
        consumed = info[:snaps].any? { |s| s[:item].nil? }
        msg = rule[:message] ? log.find(Harness.message_regexp(rule[:message])) : log.find("reacted to the field")
        { :desc => item.to_s, :ok => (consumed && !msg.nil?), :detail => consumed ?
          "consumed; \"#{msg.to_s.strip}\"" : "seed was NOT consumed" }
      end
    end

    #---------------------------------------------------------------------------
    # Probe 4: end-of-round rules (and :end_of_round hooks).
    #---------------------------------------------------------------------------
    def self.eor_subjects(matcher, default_status = nil)
      m = matcher || {}
      species = m[:types] ? m[:types].map { |t| TYPE_SPECIES[t] }.compact : TYPE_SPECIES.values
      species = species.reject { |s| (GameData::Species.get(s).types & Array(m[:not_types])).any? }
      species = species.sort_by { |s| (m[:grounded] == false) == GameData::Species.get(s).types.include?(:FLYING) ? 0 : 1 }
      species.first(8).map do |s|
        mk(s, :ability => m[:abilities]&.first, :item => m[:items]&.first, :hp_frac => 0.5,
              :status => m[:status]&.first || default_status)
      end
    end

    def self.eor_lines(log)
      lines = []
      on = false
      log.lines.each do |l|
        if l.include?("(end of round)") then on = true; next end
        on = false if l.start_with?("--- ")
        lines << l.strip if on && !l.strip.empty?
      end
      lines
    end

    def self.probe_eor(field, out)
      d = FieldEffects.get(field)
      results = []
      (d[:end_of_round] || []).each_with_index do |rule, i|
        effect = (rule.keys & [:damage, :heal, :status, :confuse, :cure_status, :stats, :effects, :proc]).join("+")
        desc = "rule #{i + 1}: #{effect} on #{(rule[:battlers] || {}).reject { |_, v| v.is_a?(Proc) }.inspect}" \
               "#{rule[:battlers]&.values&.any? { |v| v.is_a?(Proc) } ? ' +condition' : ''}"
        res = nil
        conditional = rule[:battlers]&.values&.any? { |v| v.is_a?(Proc) }
        # Rules gated by a condition proc are also tried under each weather.
        preludes = conditional ? [[], [:RAINDANCE], [:SUNNYDAY], [:SANDSTORM], [:HAIL]] : [[]]
        frozen = Array(rule[:battlers] && rule[:battlers][:status]).include?(:FROZEN)   # fixed rolls: no random thaw
        preludes.each do |prelude|
          subjects = eor_subjects(rule[:battlers], rule[:cure_status] ? :BURN : nil)
          # PRISM_ARENA's Plate rule needs the holder of the ascendant Plate (Flame Plate once VOLCANIC turns up).
          if field == :PRISM_ARENA
            subjects = [mk(:SNORLAX, :item => :FLAMEPLATE, :hp_frac => 0.5)]
            prelude = [:SPLASH] * 4
          end
          subjects.each do |subject|
            log, = mini("#{field} probe: end-of-round #{desc} [subject #{subject.speciesName}" \
                        "#{prelude.empty? ? '' : ", after #{prelude.first}"}]", :field => field,
                        :user => subject, :foe => mk(:SNORLAX, :hp_frac => 0.5),
                        :script => prelude + [:SPLASH, :SPLASH],
                        :rng => rule[:chance] ? :zero : (frozen ? :mid : nil))
            lines = eor_lines(log)
            hit = rule[:message] ? lines.find { |l| l =~ Harness.message_regexp(rule[:message]) } :
                                   lines.find { |l| l !~ /^\(anim/ && l !~ /rain|sunlight|sandstorm|hail|snow/i }
            res = { :desc => desc, :ok => !hit.nil?, :log => log,
                    :detail => hit ? "#{subject.speciesName}#{prelude.empty? ? '' : " (#{prelude.first})"}: \"#{hit}\"" :
                                     "no end-of-round effect seen (tried #{subject.speciesName})" }
            break if hit
          end
          break if res && res[:ok]
        end
        res ||= { :desc => desc, :ok => false, :detail => "no candidate subject" }
        out << res.delete(:log) if res[:log]
        results << res
      end
      if d[:hooks] && d[:hooks][:end_of_round]
        log, = mini("#{field} probe: :end_of_round hook over 7 rounds", :field => field,
                    :user => mk(:MEW, :hp_frac => 0.5), :foe => mk(:SNORLAX, :hp_frac => 0.5),
                    :script => [:SPLASH] * 7)
        out << log
        lines = eor_lines(log).reject { |l| l =~ /^\(anim/ }
        results << { :desc => "end_of_round hook", :ok => !lines.empty?,
                     :detail => lines.empty? ? "hook ran for 7 rounds without visible output" : "\"#{lines.uniq.first(2).join(' / ')}\"" }
      end
      results
    end

    def self.run_field(field)
      logs = []
      summary = { :boost => probe_boost(field, logs), :transitions => probe_transitions(field, logs),
                  :seeds => probe_seeds(field, logs), :eor => probe_eor(field, logs) }
      banner = "LOGIC-TEST OUTPUT (headless harness). Scripted probes for #{field}: the player's moves are scripted,\n" \
               "the foe only uses Splash. Not a game screenshot.\n\n"
      { :summary => summary, :text => banner + logs.map(&:text).join("\n\n"),
        :errors => logs.flat_map { |l| l.errors.map { |e| e.merge(:title => l.title) } } }
    end

    #---------------------------------------------------------------------------
    # Bosses + PRISM_ARENA rotation
    #---------------------------------------------------------------------------
    def self.strong_party(level)
      Harness.challenger_party([level, 48].max)   # the final-evolution team, at the given level
          .each { |p| p.level = level; p.calc_stats; p.heal }
    end

    def self.boss_run(name, file, party)
      breaks = []
      EventHandlers.add(:prismfall_boss_bar_broken, :harness_boss,
        proc { |battle, battler, id, n, left|
          breaks << [id, n, left]
          Harness.log&.add("## BOSS BAR BROKEN: #{id} bar #{n} depleted, #{left} bar(s) left " \
                           "(#{battler.name} HP #{battler.hp}/#{battler.totalhp}, field #{battle.field_effect})", "")
        })
      $player.party = party
      log = Harness.run_battle(name, :seed => 77) { yield }
      EventHandlers.remove(:prismfall_boss_bar_broken, :harness_boss)
      { :file => file, :log => log,
        :summary => { :name => name, :outcome => log.outcome, :outcome_text => Harness::OUTCOMES[log.outcome] || "CRASHED",
                      :turns => log.turns, :bar_breaks => breaks, :field_changes => log.field_changes,
                      :result => (Prismfall::Bosses.last_result rescue nil).inspect, :log => "logs/#{file}.txt" } }
    end

    def self.run_bosses
      runs = []
      Harness.set_badges(18)
      runs << boss_run("BOSS Zekrom (ZEKROM_ENGINE, 3 bars, FACTORY -> SCRAPYARD) vs over-levelled Lv.100 party", "boss_zekrom",
                       strong_party(100)) { Prismfall::Bosses.wild_battle(:ZEKROM_ENGINE, :can_lose => true) }
      runs << boss_run("BOSS Kyogre (KYOGRE_ISENMAR, 3 bars, FROZEN_LAKE -> WATER_SURFACE) vs over-levelled Lv.100 party",
                       "boss_kyogre", strong_party(100)) { Prismfall::Bosses.wild_battle(:KYOGRE_ISENMAR, :can_lose => true) }
      runs << boss_run("BOSS Arceus (ARCEUS_FINALE on PRISM_ARENA) vs Lv.100 party", "boss_arceus",
                       strong_party(100)) { Prismfall::Bosses.wild_battle(:ARCEUS_FINALE, :can_lose => true) }
      old = Prismfall::Difficulty.current rescue nil
      runs << boss_run("BOSS Hard-mode Warden Ilsa (ace is a 2-bar boss) on MINDSCAPE vs over-levelled Lv.100 party",
                       "boss_hard_warden_ilsa", strong_party(100)) do
        Harness.set_badges(11)
        Prismfall::Bosses.trainer_battle(:LEADER_ILSA, "Ilsa", 100, :boss => :WARDEN_ACE_2BAR, :can_lose => true,
                                         :field => :MINDSCAPE)
      end
      Harness.set_badges(18)
      runs << prism_rotation
      runs
    end

    # PRISM_ARENA: 20 quiet rounds (Arceus with Multitype vs a Splash wall), logging every Plate turn.
    def self.prism_rotation
      rot = []
      EventHandlers.add(:prismfall_field_overlay_changed, :harness_prism,
        proc { |battle, _field, _old, new_ids| rot << [battle.turnCount + 1, new_ids.dup] })
      script = []
      20.times { |i| script << ((i % 3 == 2) ? :JUDGMENT : :SPLASH) }
      log, info = mini("PRISM_ARENA rotation: Lv.25 Arceus (Multitype) for 20 rounds, Judgment every 3rd round",
                       :field => :PRISM_ARENA, :user => mk(:ARCEUS, 25, :moves => [:SPLASH, :JUDGMENT]),
                       :foe => mk(:CRESSELIA), :script => script)
      EventHandlers.remove(:prismfall_field_overlay_changed, :harness_prism)
      types = info[:snaps].map { |s| s[:types].join("/") }.chunk_while { |a, b| a == b }.map(&:first)
      { :file => "prism_arena_rotation", :log => log,
        :summary => { :name => log.title, :outcome => log.outcome, :outcome_text => Harness::OUTCOMES[log.outcome] || "CRASHED",
                      :turns => log.turns, :bar_breaks => [], :field_changes => log.field_changes,
                      :rotations => rot, :arceus_types => types, :log => "logs/prism_arena_rotation.txt" } }
    end
  end
end

EventHandlers.add(:prismfall_field_overlay_changed, :harness_log,
  proc { |battle, field_id, old_ids, new_ids|
    Harness.log&.add("## FIELD OVERLAY: #{field_id} now borrows #{new_ids.inspect} (was #{old_ids.inspect})", "")
  }
)
