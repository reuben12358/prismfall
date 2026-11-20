#===============================================================================
# Prismfall Z-Power - 004 Z-moves on Prismfall fields
#-------------------------------------------------------------------------------
# How a field treats a Z-move (Prismfall Field Effects needs no change for it):
#   1. A Z-move IS its type. Every type rule applies to it: type boosts and
#      cuts (Water Surface's Water x1.5 powers Hydro Vortex, Volcanic halves
#      Subzero Slammer), type-counted transitions (Bloom Doom grows a Flower
#      Garden like any Grass attack; Inferno Overdrive counts toward Silkwood's
#      Wildfire), and transform strikes x1.3.
#   2. Rules that name a base move do not follow it into its Z-move (Volcanic's
#      Lava Plume eruptions, Water Surface's Dive, Fairy Tale's Draining Kiss):
#      the Z-move is a different move. A field that wants a Z-move rule names
#      it in :moves, or matches every Z-move with :flags => ["ZMove"]
#      (pbs/moves_zpower.txt gives each one that flag).
#   3. Showpieces, below: a Z-move is the biggest flourish there is.
#        Grand Stage: one step up the applause ladder after a Z-move resolves.
#===============================================================================
module PrismfallZ
  FIELD_SHOWPIECES = {
    :GRAND_STAGE => { 2 => "A Z-Move! The audience leaps to its feet!",
                      3 => "The Z-Move brings the house down! Standing ovation!" }
  }.freeze

  def self.field_showpiece(battle, user, z)
    return if !defined?(FieldEffects) || !battle.respond_to?(:set_field_stage)
    msgs = FIELD_SHOWPIECES[FieldEffects.current(battle)]
    return if !msgs
    st = FieldEffects.stage(battle)
    nxt = st + 1
    return if !msgs[nxt] || nxt > FieldEffects.max_stage(FieldEffects.current(battle))
    battle.set_field_stage(nxt, msgs[nxt])
  end
end

EventHandlers.add(:prismfall_zmove_done, :prismfall_z_field_showpieces,
  proc { |battle, user, z|
    PBDebug.logonerr { PrismfallZ.field_showpiece(battle, user, z) }
  }
)
