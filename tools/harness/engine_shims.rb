#===============================================================================
# Overworld-side shims. Only things OUTSIDE the battle system are replaced here:
# the battle intro transition, the map the player "stands on", and the post-
# battle evolution/blackout screens. Battle, Battler, Move, AI, abilities, items
# and all plugin code run unmodified.
#===============================================================================
module Harness
  # A map stand-in: just enough for pbGetEnvironment / prepare_battle.
  class FakeMap
    attr_accessor :map_id, :need_refresh
    def initialize(id); @map_id = id; end
    def metadata; nil; end
    def name; "Harness Arena"; end
    def events; {}; end
    def update; end
  end

  class FakePlayerChar
    def terrain_tag; GameData::TerrainTag.get(:None); end
    def pbFacingTerrainTag; terrain_tag; end
    def straighten; end
    def map_id; $game_map.map_id; end
    def x; 0; end
    def y; 0; end
    def direction; 2; end
    def move_route_forcing; false; end
    def refresh_charset; end
    def set_movement_type(*_args); end   # pbUpdateVehicle (reached by some wild-battle paths)
  end

  def self.new_game_state
    $game_temp = Game_Temp.new
    SaveData.initialize_bootup_values
    SaveData.load_new_game_values       # real path: also builds $prismfall / field notes
    $game_map    = FakeMap.new(990)     # 990 = the kit's Test Arena map id
    $game_player = FakePlayerChar.new
    $player.name = "Tester"
    $player.character_ID = 1 if $player.respond_to?(:character_ID=)
  end
end

# Battle intro transition (screen wipe + BGM): visuals only.
def pbBattleAnimation(_bgm = nil, _battletype = 0, _foe = nil)
  $game_temp.in_battle = true
  yield if block_given?
  $game_temp.in_battle = false
end

def pbSceneStandby
  yield if block_given?
end

# Post-battle overworld handlers that open full-screen UI (evolution scene, blackout warp).
EventHandlers.remove(:on_end_battle, :evolve_and_black_out)

# Overworld message boxes (used by plugins around battles) go to the battle log.
def pbMessage(message, commands = nil, _cmd_if_cancel = 0, _skin = nil, default_cmd = 0, &_block)
  Harness.log&.add("(overworld message) #{Harness.clean(message)}")
  return default_cmd if commands
  return 0
end
