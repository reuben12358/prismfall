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
  PRISMFALL_START = [109, 7, 6]   # [map_id, x, y] or nil; must be a walkable tile (8,6 is under the deck barrels)

  def self.apply_start_position
    st = PRISMFALL_START
    return false if !st
    return false if !pbRgssExists?(sprintf("Data/Map%03d.rxdata", st[0]))
    if !start_tileset_installed?(st[0])
      # Without our tilesets Game_Map#setup crashes (tileset_name for nil). In Debug mode, offer the installer
      # (same as Debug > Files > Install Prismfall maps); otherwise start on RMXP's own starting position.
      if $DEBUG && defined?(PrismfallMapInstaller) &&
         pbConfirmMessage(_INTL("The Prismfall tilesets and maps aren't installed in this project yet. Install them now?"))
        PrismfallMapInstaller.install(new_game: true)
      end
      if !start_tileset_installed?(st[0])
        echoln("[Prismfall Maps] The start map's tileset is not installed: run Debug > Files > Install Prismfall maps.")
        return false
      end
    end
    $data_system.start_map_id = st[0]
    $data_system.start_x      = st[1]
    $data_system.start_y      = st[2]
    return true
  end

  def self.start_tileset_installed?(map_id)
    map = load_data(sprintf("Data/Map%03d.rxdata", map_id))
    ts = $data_tilesets && $data_tilesets[map.tileset_id]
    return !ts.nil? && !ts.tileset_name.to_s.empty?
  rescue StandardError
    return true   # let the normal start report any other problem
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
