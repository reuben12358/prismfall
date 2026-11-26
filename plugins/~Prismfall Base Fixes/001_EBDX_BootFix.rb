#===============================================================================
# Prismfall Base Fixes - 001 EBDX boot fix (base-project bug, not a Prismfall one)
#-------------------------------------------------------------------------------
# Elite Battle: DX's "[000] Scripts/Battle UI/UI Fixes.rb" line 4 reopens
#   class PokemonSprite < SpriteWrapper
# but Essentials v21.1 defines PokemonSprite < Sprite, and EBDX's own
# SpriteWrapper is an unrelated class. Ruby stops the boot with "superclass
# mismatch for class PokemonSprite". The untouched EBDX Renovation fork (and
# Manurocker95's port) fail the same way with no Prismfall file installed.
#
# PluginManager.runPlugins runs every plugin file through
# eval(code, TOPLEVEL_BINDING, fname). This plugin loads before every other one:
# PluginManager loads plugins in reverse folder-name order, the "~" makes this
# folder sort last, and it has no dependencies, so the sort never moves it. It
# drops the superclass from that one line in memory (no file is changed). If the
# line was already fixed by hand (docs/SETUP.md §6), it does nothing.
#===============================================================================
module PluginManager
  PRISMFALL_EBDX_SPRITE_LINE = /^class PokemonSprite\s*<\s*SpriteWrapper\s*$/
  # In-memory line patches for base-project plugin files, applied as each file is evaluated (no file is changed):
  # key => { :file => file name suffix, :line => Regexp, :with => replacement, :note => log text }. A patch whose line
  # is not found (already fixed by hand, or a newer base project) does nothing. Later Base Fixes files add their own
  # rows (003_Gen9_PsychoShift.rb).
  PRISMFALL_SOURCE_PATCHES = {} if !const_defined?(:PRISMFALL_SOURCE_PATCHES)
  PRISMFALL_SOURCE_PATCHES[:ebdx_pokemon_sprite] = {
    :file => "UI Fixes.rb", :line => PRISMFALL_EBDX_SPRITE_LINE,
    :with => "class PokemonSprite   # superclass dropped by Prismfall Base Fixes",
    :note => "dropped the PokemonSprite superclass (EBDX boot fix)"
  }

  def self.eval(code, *args)
    if args[1].is_a?(String) && code.is_a?(String)
      PRISMFALL_SOURCE_PATCHES.each_value do |pt|
        next if !args[1].end_with?(pt[:file]) || !code.match?(pt[:line])
        code = (pt[:all]) ? code.gsub(pt[:line], pt[:with]) : code.sub(pt[:line], pt[:with])   # :all => every match
        echoln("[Prismfall Base Fixes] #{args[1]}: #{pt[:note]}")
      end
    end
    return super(code, *args)
  end
end
