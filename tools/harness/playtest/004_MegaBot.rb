#===============================================================================
# DEV-ONLY: Mega Evolution session for the playtest bot (run_mega.sh; never ship).
# Real mkxp-z + Elite Battle DX. Battles start from Scene_Map#update, like a map event's script.
#   PLAYBOT_SESSION=mega   the PLAYER's Fight menu (controlPlayer off): Charizard @Charizardite X with the Mega Ring vs
#                          "Brann" (a test trainer: Torkoal, then Camerupt @Cameruptite with a Mega Ring) on Volcanic.
#                          The bot presses Use for Fight, then Action (EBDX: toggles the Mega button), photographs the
#                          lit button, presses Use on Flamethrower; the Mega animation plays; the AI's Camerupt Megas
#                          when it comes out. Every 2nd engine frame is saved (PLAYBOT_REC_EVERY=2) for a slow GIF;
#                          bot.log notes the frame numbers of each Mega Evolution ("MG: frames ...").
#===============================================================================
module PlayBot
  MG_SESSIONS = ["mega"].freeze
  MG_QUEUE = []
  @mg_fight = nil     # frame the EBDX Fight menu opened (player's turn)
  @mg_toggled = false
  @mg_marks = []
  class << self
    attr_accessor :mg_fight, :mg_toggled, :mg_marks
    def mg_frame; return @frame; end
    def mg_nframe; return @nframe; end

    alias mg_plan plan unless method_defined?(:mg_plan)
    def plan
      return [[:mg_run], [:done]] if MG_SESSIONS.include?(SESSION)
      return mg_plan
    end

    alias mg_drive_plan drive_plan unless method_defined?(:mg_drive_plan)
    def drive_plan
      step = plan[@step]
      return mg_drive_plan if !step || step[0] != :mg_run
      if !@mg_queued
        return if @idle < 30
        shot("mg_00_start")
        MG_QUEUE.push(:mega)
        @mg_queued = true
        log("MG: queued #{SESSION}")
        return
      end
      return if !MG_QUEUE.empty? || @idle < 40
      next_step
    end

    # In the player's Fight menu: Action toggles the Mega button (EBDX UI Fight.rb), then Use picks the first move.
    alias mg_drive_battle drive_battle unless method_defined?(:mg_drive_battle)
    def drive_battle
      if @mg_fight && !@mg_toggled
        age = @frame - @mg_fight
        shot("mg_01_fight_menu") if age == 20
        press(B::ACTION) if age == 30
        if age == 50
          shot("mg_02_mega_button_on")
        elsif age >= 64
          press(B::USE)
          @mg_toggled = true
          log("MG: toggled the Mega button and chose the first move")
        end
        return
      end
      mg_drive_battle
    end

    def mg_party
      cz = Pokemon.new(:CHARIZARD, 60)
      GameData::Stat.each_main { |s| cz.iv[s.id] = 31 }
      cz.forget_all_moves
      [:FLAMETHROWER, :DRAGONCLAW, :AIRSLASH, :ROOST].each { |m| cz.learn_move(m) }
      cz.item = :CHARIZARDITEX
      cz.calc_stats
      sx = Pokemon.new(:SNORLAX, 60)
      sx.forget_all_moves
      [:BODYSLAM, :REST].each { |m| sx.learn_move(m) }
      sx.calc_stats
      $player.party = [cz, sx]
    end

    def mg_run(_kind)
      mg_party
      $bag.add(:MEGARING) if !$bag.has?(:MEGARING)
      tk = Pokemon.new(:TORKOAL, 55)
      tk.forget_all_moves
      [:FLAMETHROWER, :PROTECT].each { |m| tk.learn_move(m) }
      tk.calc_stats
      cm = Pokemon.new(:CAMERUPT, 56)
      cm.forget_all_moves
      [:EARTHPOWER, :FLAMETHROWER, :ROCKSLIDE, :YAWN].each { |m| cm.learn_move(m) }
      cm.item = :CAMERUPTITE
      cm.calc_stats
      foe = NPCTrainer.new("Brann", :LEADER_BRANN)
      foe.party = [tk, cm]
      foe.items = [:MEGARING]
      log("MG: player's Fight menu vs Brann (test team) on Volcanic; party #{party_text}; ring #{$bag.has?(:MEGARING)}; " \
          "Mega plugin #{defined?(PrismfallMega) ? 'loaded' : 'MISSING'}; LIMIT #{PrismfallMega::LIMIT rescue '?'}")
      setBattleRule("field", :VOLCANIC)
      setBattleRule("canLose")
      won = TrainerBattle.start(foe)
      log("MG: battle #{won ? 'won' : 'lost'}; Megas #{PrismfallMega.log($mg_last_battle).inspect rescue '?'}; marks #{@mg_marks.inspect}; " \
          "one per side: #{(PrismfallMega.log($mg_last_battle).group_by { |m| m[0] & 1 }.values.all? { |v| v.length == 1 }) rescue '?'}")
    end
  end
end

class Scene_Map
  alias mg_update update unless method_defined?(:mg_update)
  def update
    mg_update
    return if PlayBot::MG_QUEUE.empty? || !PlayBot.map_ready?
    kind = PlayBot::MG_QUEUE.first
    begin
      PlayBot.mg_run(kind)
    rescue StandardError => e
      PlayBot.fatal("MG #{kind}: #{e.class}: #{e.message}\n  " + (e.backtrace || [])[0, 20].join("\n  "))
    ensure
      PlayBot::MG_QUEUE.shift
    end
  end
end

module BattleCreationHelperMethods
  class << self
    alias mg_prepare_battle prepare_battle unless method_defined?(:mg_prepare_battle)
    def prepare_battle(battle)
      mg_prepare_battle(battle)
      return if !PlayBot::MG_SESSIONS.include?(PlayBot::SESSION)
      battle.controlPlayer = false
      $mg_last_battle = battle
      PlayBot.log("MG: controlPlayer #{battle.controlPlayer}")
    end
  end
end

# Note when the player's EBDX Fight menu is open (the bot toggles the Mega button there once).
class Battle::Scene
  alias mg_pbFightMenu pbFightMenu unless method_defined?(:mg_pbFightMenu)
  def pbFightMenu(idxBattler, *args, &block)
    if PlayBot::MG_SESSIONS.include?(PlayBot::SESSION) && !PlayBot.mg_toggled
      PlayBot.mg_fight = PlayBot.mg_frame
      PlayBot.log("MG: Fight menu open for #{@battle.battlers[idxBattler].name}; Mega possible #{@battle.pbCanMegaEvolve?(idxBattler)}")
    end
    return mg_pbFightMenu(idxBattler, *args, &block)
  ensure
    PlayBot.mg_fight = nil
  end

  alias mg_pbCommonAnimation pbCommonAnimation unless method_defined?(:mg_pbCommonAnimation)
  def pbCommonAnimation(animName, user = nil, target = nil)
    if PlayBot::MG_SESSIONS.include?(PlayBot::SESSION) && animName.to_s.start_with?("MegaEvolution")
      PlayBot.mg_marks << [animName.to_s, user ? user.name : nil, PlayBot.mg_nframe]
      PlayBot.log("MG: frames #{animName} start for #{user ? user.name : '?'} at rec frame #{PlayBot.mg_nframe}")
      PlayBot.shot("mg_anim_#{animName}_#{user ? user.name : 'x'}")
    end
    ret = mg_pbCommonAnimation(animName, user, target)
    if PlayBot::MG_SESSIONS.include?(PlayBot::SESSION) && animName.to_s.start_with?("MegaEvolution")
      PlayBot.log("MG: frames #{animName} end at rec frame #{PlayBot.mg_nframe}")
      PlayBot.shot("mg_after_#{animName}_#{user ? user.name : 'x'}")
    end
    return ret
  end
end

EventHandlers.add(:prismfall_mega_evolved, :mg_bot, proc { |battle, b, old|
  PlayBot.log("MG: MEGA #{b.name} (side #{b.index & 1}) #{old} -> #{b.ability_id}, field #{battle.field_effect rescue '?'}, rec frame #{PlayBot.mg_nframe}")
  # The player's Mega is the point of the session: the AI plays the rest of the battle (the bot only knows Use).
  if (b.index & 1) == 0 && !battle.controlPlayer
    battle.controlPlayer = true
    PlayBot.log("MG: the player's Mega is done; the AI plays the rest")
  end
})

module Game
  class << self
    alias mgbot_start_new start_new unless method_defined?(:mgbot_start_new)
    def start_new
      return mgbot_start_new if !PlayBot::MG_SESSIONS.include?(PlayBot::SESSION)
      door = PlayBot.find_door(load_data(sprintf("Data/Map%03d.rxdata", 147)).events.values, 150)
      st = door ? [147, door[0], door[1] + 1] : nil
      if st
        PrismfallMaps.define_singleton_method(:apply_start_position) do
          $data_system.start_map_id, $data_system.start_x, $data_system.start_y = *st
          true
        end
      end
      mgbot_start_new
      $player.name = PlayBot::NAME
      $player.has_running_shoes = true
      $player.badges = Array.new(18) { |i| i < 8 }
      (101..110).each { |i| $game_switches[i] = true }
      Prismfall::LevelCap.disable! if Prismfall::LevelCap.respond_to?(:disable!)
      $bag.add(:MEGARING)
      PlayBot.mg_party
      $game_map.need_refresh = true
      PlayBot.recording = true
      PlayBot.log("MG session #{PlayBot::SESSION}: start #{st.inspect}; plugins #{PluginManager.plugins.inspect}")
    end
  end
end
