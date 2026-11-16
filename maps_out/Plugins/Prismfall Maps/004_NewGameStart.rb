#===============================================================================
# Prismfall Maps - new-game start position (no RPG Maker XP edit needed)
# Game.start_new (003_Game processing/001_StartGame.rb) places the player at
# $data_system.start_map_id / start_x / start_y. This overrides those values
# in memory for the new game so it begins on the Dovetail's deck (map 109),
# whose prologue event handles appearance, name, running shoes and difficulty
# (the jobs of the stock intro map). Set PRISMFALL_START to nil to use RMXP's
# own "Player's Starting Position" instead.
#===============================================================================
module PrismfallMaps
  PRISMFALL_START = [109, 8, 6]   # [map_id, x, y] or nil

  def self.apply_start_position
    st = PRISMFALL_START
    return false if !st
    return false if !pbRgssExists?(sprintf("Data/Map%03d.rxdata", st[0]))
    $data_system.start_map_id = st[0]
    $data_system.start_x      = st[1]
    $data_system.start_y      = st[2]
    return true
  end
end

module Game
  class << self
    alias prismfall_maps_start_new start_new unless method_defined?(:prismfall_maps_start_new)

    def start_new
      PrismfallMaps.apply_start_position
      prismfall_maps_start_new
    end
  end
end
