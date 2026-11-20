#===============================================================================
# DEV-ONLY: Z-Power and Eevee Octave sessions for the playtest bot (run_zpower.sh; never ship).
# Real mkxp-z + Elite Battle DX. The bot only presses buttons; the battles are started from Scene_Map#update,
# the way a map event starts them, so the bot's input keeps working inside them.
#   PLAYBOT_SESSION=zpower     the PLAYER's Fight menu (controlPlayer off): a Timid Vaporeon with the Waterium Z and the
#                              ring vs Lento (OCTAVE_SINGER v60) on the Frozen Lake. The bot presses Use: Fight -> Scald ->
#                              the "Unleash ... Z-Power?" box -> Yes -> Hydro Vortex. Lento's Glaceon answers with Subzero
#                              Slammer (AI). (Forte's Flareon on Volcanic one-shots a Lv 95 Vaporeon through the resist:
#                              Flash Fire + Volcanic + STAB on Inferno Overdrive; see mapgen/REQUESTS.md.)
#   PLAYBOT_SESSION=zgauntlet  the whole gauntlet through Vesper's map event script (pf_trial_talk(:VESPER_GARDEN)):
#                              eight singers in a set help order, then Vesper; the AI plays the player's side.
#                              PLAYBOT_ZP_TEAM=legends gives an overwhelming team, to see the reward path end to end.
#   PLAYBOT_SESSION=zevo       the Eevium Z under the shipped Gen 9 Pack's CHAMPIONS_MECHANICS (Last Resort locked until
#                              the other moves are used): the player's Eevee picks Last Resort in the Fight menu -> Yes ->
#                              Extreme Evoboost, against Vesper's Amen (AI), who opens with it too.
#===============================================================================
module PlayBot
  ZP_SESSIONS = ["zpower", "zgauntlet", "zevo"].freeze
  ZP_HELP_ORDER = [:NOCT, :LYRA, :SONA, :ARIA, :LENTO, :CADENCE, :FORTE, :CAROL].freeze   # deliberately not gym order
  ZP_QUEUE = []
  @zp_control = true
  @zp_shoot = []      # [frame, name]
  @zp_prompt = nil    # frame the Z-Power box opened
  class << self
    attr_accessor :zp_control, :zp_prompt
    def zp_shot_in(frames, name); @zp_shoot << [@frame + frames, name]; end
    def zp_due
      due = @zp_shoot.select { |f, _n| @frame >= f }
      @zp_shoot -= due
      due.each { |_f, n| shot(n) }
    end
    def zp_frame; return @frame; end

    alias zp_plan plan unless method_defined?(:zp_plan)
    def plan
      return [[:zp_run], [:done]] if ZP_SESSIONS.include?(SESSION)
      return zp_plan
    end

    alias zp_drive_plan drive_plan unless method_defined?(:zp_drive_plan)
    def drive_plan
      step = plan[@step]
      return zp_drive_plan if !step || step[0] != :zp_run
      @step_start = @frame if @step_start == 0
      if !@zp_queued
        return if @idle < 30
        shot("zp_00_start")
        ZP_QUEUE.push(SESSION.to_sym)
        @zp_queued = true
        log("ZP: queued #{SESSION}")
        return
      end
      return if !ZP_QUEUE.empty? || @idle < 40
      next_step
    end

    # Battles: Use every 20 frames, except while the Z-Power box is up (hold it 40 frames for a screenshot).
    alias zp_drive_battle drive_battle unless method_defined?(:zp_drive_battle)
    def drive_battle
      zp_due
      if @zp_prompt
        age = @frame - @zp_prompt
        shot("zp_prompt_unleash_z_power") if age == 30
        if age >= 40
          press(B::USE)
          log("ZP: pressed Use on the Z-Power box (cursor on Yes)")
          @zp_prompt = nil
        end
        return
      end
      zp_drive_battle
    end
  end

  # PLAYBOT_ZP_TEAM=legends: an overwhelming team, to see the reward path end to end (the default team can lose).
  def self.zp_setup_party(strong)
    if strong && ENV["PLAYBOT_ZP_TEAM"] == "legends"
      mons = [[:ARCEUS, [:EXTREMESPEED, :JUDGMENT, :EARTHQUAKE, :RECOVER], :LEFTOVERS],
              [:MEWTWO, [:PSYSTRIKE, :AURASPHERE, :ICEBEAM, :FLAMETHROWER], :LIFEORB],
              [:KYOGRE, [:WATERSPOUT, :ICEBEAM, :THUNDER, :CALMMIND], :LEFTOVERS],
              [:GROUDON, [:PRECIPICEBLADES, :STONEEDGE, :FIREPUNCH, :SWORDSDANCE], :LEFTOVERS],
              [:RAYQUAZA, [:DRAGONASCENT, :EXTREMESPEED, :EARTHQUAKE, :VCREATE], :LIFEORB],
              [:LUGIA, [:AEROBLAST, :PSYCHIC, :ROOST, :ICEBEAM], :LEFTOVERS]]
    elsif strong
      mons = [[:SNORLAX, [:BODYSLAM, :HEAVYSLAM, :CRUNCH, :EARTHQUAKE], :LEFTOVERS],
              [:GARCHOMP, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :FIREFANG], :LIFEORB],
              [:METAGROSS, [:METEORMASH, :ZENHEADBUTT, :EARTHQUAKE, :BULLETPUNCH], :LEFTOVERS],
              [:TYRANITAR, [:STONEEDGE, :CRUNCH, :EARTHQUAKE, :ICEPUNCH], :LEFTOVERS],
              [:VOLCARONA, [:FIERYDANCE, :BUGBUZZ, :QUIVERDANCE, :GIGADRAIN], :LEFTOVERS],
              [:TOGEKISS, [:AIRSLASH, :DAZZLINGGLEAM, :AURASPHERE, :ROOST], :LEFTOVERS]]
    else
      mons = [[:VAPOREON, [:SCALD, :ICEBEAM, :PROTECT, :WISH], :WATERIUMZ]]   # Timid, below
    end
    $player.party = mons.map do |sp, mv, it|
      pk = Pokemon.new(sp, 100)
      pk.nature = :TIMID if !strong
      GameData::Stat.each_main { |s| pk.iv[s.id] = 31 }
      pk.forget_all_moves
      mv.each { |m| pk.learn_move(m) }
      pk.item = it
      GameData::Stat.each_main { |st| pk.ev[st.id] = 84 } if strong   # 504 EVs spread evenly
      pk.calc_stats
      pk
    end
  end

  def self.zp_run(kind)
    case kind
    when :zpower
      zp_setup_party(false)
      @zp_control = false
      log("ZP: player's Fight menu vs Lento (v60) on the Frozen Lake; party #{party_text}; ring #{$bag.has?(:ZPOWERRING)}")
      won = Prismfall::Trials.trainer_battle([:OCTAVE_SINGER, "Lento", 60], field: :FROZEN_LAKE)
      log("ZP: battle vs Lento #{won ? 'won' : 'lost'}; Z used #{PrismfallZ.log($zp_last_battle).inspect rescue '?'}")
      @zp_control = true
    when :zevo
      ev = Pokemon.new(:EEVEE, 100)
      GameData::Stat.each_main { |st| ev.iv[st.id] = 31 }
      ev.forget_all_moves
      [:LASTRESORT, :STOREDPOWER, :SHADOWBALL, :QUICKATTACK].each { |m| ev.learn_move(m) }
      ev.item = :EEVIUMZ
      ev.calc_stats
      zp_setup_party(true)
      $player.party = [ev] + $player.party.first(2)
      $bag.add(:ZPOWERRING) if !$bag.has?(:ZPOWERRING)
      @zp_control = false
      log("ZP: Eevium Z vs Vesper (v60); CHAMPIONS_MECHANICS #{defined?(Settings::CHAMPIONS_MECHANICS) ? Settings::CHAMPIONS_MECHANICS : 'n/a'}; party #{party_text}")
      won = Prismfall::Trials.trainer_battle([:OCTAVE_VESPER, "Vesper", 60], field: :GRAND_STAGE)
      log("ZP: battle vs Vesper #{won ? 'won' : 'lost'}; Z used #{PrismfallZ.log($zp_last_battle).inspect rescue '?'}")
      @zp_control = true
    when :zgauntlet
      zp_setup_party(true)
      oc = Prismfall::Trials::Octave
      oc.reset
      Prismfall::Trials.start(:CR_OCTAVE, false) if !Prismfall::Trials.active?(:CR_OCTAVE)
      ZP_HELP_ORDER.each { |id| oc.help(id) }
      log("ZP: help order #{oc.order.inspect}; ready #{oc.ready?}; Vesper's row ready #{pf_trial_ready?(:VESPER_GARDEN)}")
      pf_trial_talk(:VESPER_GARDEN)
      ev = $player.party.find { |p| p.isSpecies?(:EEVEE) } ||
           ($PokemonStorage.boxes.flat_map { |b| b.pokemon.compact }.find { |p| p.isSpecies?(:EEVEE) } rescue nil)
      log("ZP: gauntlet over: CR_OCTAVE #{Prismfall::Trials.state(:CR_OCTAVE)}; S177 #{$game_switches[177]}; " \
          "Eevee #{ev ? "Lv #{ev.level} #{ev.moves.map(&:id).inspect}" : 'none'}; Eevium Z #{$bag.has?(:EEVIUMZ)}; ring #{$bag.has?(:ZPOWERRING)}")
    end
  end
end

# Battles start here, from the map scene, like a map event's script.
class Scene_Map
  alias zp_update update unless method_defined?(:zp_update)
  def update
    zp_update
    return if PlayBot::ZP_QUEUE.empty? || !PlayBot.map_ready?
    kind = PlayBot::ZP_QUEUE.first
    begin
      PlayBot.zp_run(kind)
    rescue StandardError => e
      PlayBot.fatal("ZP #{kind}: #{e.class}: #{e.message}\n  " + (e.backtrace || [])[0, 20].join("\n  "))
    ensure
      PlayBot::ZP_QUEUE.shift
    end
  end
end

module BattleCreationHelperMethods
  class << self
    alias zp_prepare_battle prepare_battle unless method_defined?(:zp_prepare_battle)
    def prepare_battle(battle)
      zp_prepare_battle(battle)
      battle.controlPlayer = PlayBot.zp_control
      $zp_last_battle = battle
      PlayBot.log("ZP: controlPlayer #{battle.controlPlayer}") if PlayBot::ZP_SESSIONS.include?(PlayBot::SESSION)
    end
  end
end

# The Z-Power box is the scene's Yes/No command list: note when it opens so the bot can photograph it.
class Battle::Scene
  alias zp_pbShowCommands pbShowCommands unless method_defined?(:zp_pbShowCommands)
  def pbShowCommands(msg, commands, *args, &block)
    if msg.to_s.include?("Z-Power")
      PlayBot.zp_prompt = PlayBot.zp_frame
      PlayBot.log("ZP: box '#{msg}' #{commands.inspect}")
    end
    return zp_pbShowCommands(msg, commands, *args, &block)
  end
end

EventHandlers.add(:prismfall_zmove_chosen, :zp_bot, proc { |battle, idx, z|
  PlayBot.log("ZP: chosen #{z.id} by #{battle.battlers[idx].name} (side #{idx & 1})")
})
EventHandlers.add(:prismfall_zmove_unleashed, :zp_bot, proc { |battle, user, z|
  PlayBot.log("ZP: UNLEASHED #{z.id} (#{z.name}) by #{user.name} (side #{user.index & 1}), power #{z.power}, field #{battle.field_effect rescue '?'}")
  PlayBot.zp_shot_in(8, "zp_z_power_#{user.name}_#{z.id}")
  PlayBot.zp_shot_in(70, "zp_z_move_#{user.name}_#{z.id}")
  # The bot only ever presses Use (first move): once the player's Z-move is spent, let the AI finish the battle
  # (under CHAMPIONS_MECHANICS the first move, Last Resort, is locked again and the menu would refuse it forever).
  if (user.index & 1) == 0 && !battle.controlPlayer
    battle.controlPlayer = true
    PlayBot.log("ZP: the player's Z-move is spent; the AI plays the rest")
  end
})

module Game
  class << self
    alias zpbot_start_new start_new unless method_defined?(:zpbot_start_new)
    def start_new
      return zpbot_start_new if !PlayBot::ZP_SESSIONS.include?(PlayBot::SESSION)
      door = PlayBot.find_door(load_data(sprintf("Data/Map%03d.rxdata", 147)).events.values, 150)
      st = door ? [147, door[0], door[1] + 1] : nil
      if st
        PrismfallMaps.define_singleton_method(:apply_start_position) do
          $data_system.start_map_id, $data_system.start_x, $data_system.start_y = *st
          true
        end
      end
      zpbot_start_new
      $player.name = PlayBot::NAME
      $player.has_running_shoes = true
      $player.badges = Array.new(18) { true }
      (101..110).each { |i| $game_switches[i] = true }
      $game_switches[155] = true
      Prismfall::LevelCap.disable! if Prismfall::LevelCap.respond_to?(:disable!)
      $bag.add(:ZPOWERRING) if PlayBot::SESSION == "zpower"
      PlayBot.zp_setup_party(PlayBot::SESSION == "zgauntlet")
      $game_map.need_refresh = true
      PlayBot.recording = true
      PlayBot.log("ZP session #{PlayBot::SESSION}: start #{st.inspect}; Z-Power plugin #{defined?(PrismfallZ) ? 'loaded' : 'MISSING'}; " \
                  "plugins #{PluginManager.plugins.inspect}")
    end
  end
end
