#===============================================================================
# Prismfall Maps - 009 the Velmora town map (mapgen/ruby/009_TownMap.rb, copied by build.py)
#-------------------------------------------------------------------------------
# Velmora must be region 0 (WORLD.md section 1), but the stock PBS/town_map.txt already defines region 0 (Essen), and
# Essentials refuses a section name used twice. When the kit's PBS/town_map_prismfall.txt is present, compile only that
# file: Velmora replaces the sample regions (the stock file is left untouched on disk).
# Source: tools/worldmap/gen_docs.py writes pbs/town_map.txt (packaged as PBS/town_map_prismfall.txt); the graphic is
# Graphics/UI/Town Map/prismfall_velmora.png (tools/worldmap/gen_world_map.py). Owner: world cartographer.
#===============================================================================
module Compiler
  class << self
    if method_defined?(:compile_town_map) && !method_defined?(:prismfall_compile_town_map)
      alias_method :prismfall_compile_town_map, :compile_town_map

      def compile_town_map(*paths)
        ours = paths.select { |p| File.basename(p.to_s) == "town_map_prismfall.txt" }
        prismfall_compile_town_map(*(ours.empty? ? paths : ours))
      end
    end
  end
end

#-------------------------------------------------------------------------------
# Fly follows the town's live HealingSpot. A Point's fly coordinates are copied from the PC's HealingSpot when
# tools/worldmap/gen_docs.py runs; when a map rebuild moves the PC door, the town map would send Fly to the old
# tile until gen_docs is re-run. Here the spot comes from map metadata (the PC map whose HealingSpot names the same
# town) and the PBS coordinates are only the fallback. Nothing changes for towns whose spot is already right.
#-------------------------------------------------------------------------------
module Prismfall
  module TownMapFly
    module_function

    def live_spot(map_id)
      @spots ||= {}
      return @spots[map_id] if @spots.key?(map_id)
      found = nil
      GameData::MapMetadata.each do |md|
        dest = md.teleport_destination
        next if !dest || dest[0] != map_id
        found = [dest[0], dest[1], dest[2]]
        break
      end
      @spots[map_id] = found
    end
  end
end

class PokemonRegionMap_Scene
  if method_defined?(:pbGetHealingSpot) && !method_defined?(:prismfall_pbGetHealingSpot)
    alias_method :prismfall_pbGetHealingSpot, :pbGetHealingSpot

    def pbGetHealingSpot(x, y)
      spot = prismfall_pbGetHealingSpot(x, y)
      return spot if !spot || @editor
      Prismfall::TownMapFly.live_spot(spot[0]) || spot
    end
  end
end
