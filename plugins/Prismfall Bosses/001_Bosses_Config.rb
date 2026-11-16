#===============================================================================
# Prismfall Bosses - 001 Config
# Rejuvenation-style multi-bar ("shield") boss battles. See design/BOSSES.md.
#===============================================================================
module Prismfall
  module Bosses
    VERSION = "1.0.0"

    # Core's Festival stages run by this plugin: Festival stage id => boss id.
    # A stage can also name its boss itself with :prismfall_boss => :ID
    # (or :prismfall_boss => false to keep Core's own boss battle).
    FESTIVAL_BOSSES  = { :ARCEUS => :ARCEUS_FINALE }
    USE_FOR_FESTIVAL = true

    # Statuses blocked while bars remain when a definition says
    # :status_immunity => true (the default). Valid entries: :SLEEP :POISON
    # :BURN :PARALYSIS :FROZEN :CONFUSION :ATTRACT :YAWN (:TOXIC = :POISON).
    DEFAULT_IMMUNITIES = [:SLEEP, :POISON, :BURN, :PARALYSIS, :FROZEN, :YAWN]
    ALL_IMMUNITIES     = [:SLEEP, :POISON, :BURN, :PARALYSIS, :FROZEN, :YAWN, :CONFUSION, :ATTRACT]
    DEFAULT_BARS       = 2
    DEFAULT_AI_SKILL   = 100     # wild bosses use the best-skill AI

    # Messages ({1} = the boss, e.g. "The wild Kyogre"). Plain strings; formatted with _INTL at display time.
    BREAK_MESSAGE  = "{1}'s shield shattered!"
    IMMUNE_MESSAGE = "{1}'s shield repelled the effect!"
    BALL_MESSAGE   = "The shield around {1} deflected the Poké Ball!"

    # Databox pips. Optional graphic: 2 frames side by side (full, empty).
    PIP_GRAPHIC          = "Graphics/UI/Prismfall/boss_pips"
    PIP_SIZE             = [10, 6]
    PIP_GAP              = 2
    PIP_COLORS           = { :full => [248, 200, 72], :empty => [64, 64, 80], :border => [24, 24, 32] }
    PIPS_INCLUDE_CURRENT = true     # true: one pip per bar left (incl. the current one)
    EBDX_PIP_OFFSET      = [0, -9]  # EBDX: relative to the databox's HP bar sprite
    VANILLA_PIP_POS      = [102, 32] # vanilla: on the databox bitmap (+ @spriteBaseX)
    EBDX_BOSS_DATABOX    = true     # wild bosses use EBDX's boss databox + Renovation's :setBoss styling

    DEBUG_MENU = true
  end
end
