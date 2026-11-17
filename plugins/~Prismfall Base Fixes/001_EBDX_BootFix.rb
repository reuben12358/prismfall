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

  def self.eval(code, *args)
    if args[1].is_a?(String) && args[1].end_with?("UI Fixes.rb") &&
       code.is_a?(String) && code.match?(PRISMFALL_EBDX_SPRITE_LINE)
      code = code.sub(PRISMFALL_EBDX_SPRITE_LINE, "class PokemonSprite   # superclass dropped by Prismfall Base Fixes")
      echoln("[Prismfall Base Fixes] #{args[1]}: dropped the PokemonSprite superclass (EBDX boot fix)")
    end
    return super(code, *args)
  end
end
