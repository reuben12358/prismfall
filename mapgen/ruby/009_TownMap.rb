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
