#===============================================================================
# Prismfall Z-Power - 001 Config (SPINE Revision 19: the Eevee Octave)
#-------------------------------------------------------------------------------
# A small Z-move system for Essentials v21.1 + Elite Battle DX, scoped to what
# the Eevee Octave needs (design/EEVEE_OCTAVE.md section 5):
#   * type Z-crystals turn a damaging move of their type into that type's
#     Z-move (power from the base move, Gen 7 table; physical/special from the
#     base move; hits through Protect for 1/4 damage; never misses)
#   * Eevium Z turns Eevee's Last Resort into Extreme Evoboost (+2 Atk, Def,
#     Sp. Atk, Sp. Def and Speed)
#   * once per trainer per battle; the crystal is never used up and cannot be
#     knocked off, stolen, swapped or flung
#   * the player needs the Z-Power Ring (key item); NPC trainers only need the
#     crystal on their Pokemon. Wild Pokemon never use Z-Power.
# Data: pbs/moves_zpower.txt (the Z-moves) and pbs/items_zpower.txt (crystals,
# ring). Add a crystal by adding its item and one line below; nothing else.
# Why not the Deluxe Battle Kit's Z-Power add-on: it is built on the Deluxe
# Battle Kit, a battle-UI framework of its own, and this game's battle UI is
# Elite Battle DX (see design/EEVEE_OCTAVE.md section 5.1).
#===============================================================================
module PrismfallZ
  RING = :ZPOWERRING

  # Type crystal => the type it powers. Its Z-move is TYPE_ZMOVES[type].
  CRYSTALS = {
    :WATERIUMZ   => :WATER,
    :ELECTRIUMZ  => :ELECTRIC,
    :FIRIUMZ     => :FIRE,
    :ICIUMZ      => :ICE,
    :GRASSIUMZ   => :GRASS,
    :PSYCHIUMZ   => :PSYCHIC,
    :DARKINIUMZ  => :DARK,
    :FAIRIUMZ    => :FAIRY
  }.freeze

  TYPE_ZMOVES = {
    :WATER    => :HYDROVORTEX,
    :ELECTRIC => :GIGAVOLTHAVOC,
    :FIRE     => :INFERNOOVERDRIVE,
    :ICE      => :SUBZEROSLAMMER,
    :GRASS    => :BLOOMDOOM,
    :PSYCHIC  => :SHATTEREDPSYCHE,
    :DARK     => :BLACKHOLEECLIPSE,
    :FAIRY    => :TWINKLETACKLE
  }.freeze

  # Species-exclusive crystals: one species, one base move, one Z-move.
  EXCLUSIVE = {
    :EEVIUMZ => { :species => :EEVEE, :move => :LASTRESORT, :zmove => :EXTREMEEVOBOOST }
  }.freeze

  # The animation each status Z-move shows (damaging Z-moves show their base move's).
  STATUS_ANIMS = { :EXTREMEEVOBOOST => :WORKUP }.freeze

  # Gen 7 Z-move power from the base move's power.
  POWER_TABLE = [[55, 100], [65, 120], [75, 140], [85, 160], [95, 175],
                 [100, 180], [110, 185], [125, 190], [130, 195]].freeze
  POWER_MAX = 200

  # Damage multiplier when a Z-move breaks through a protecting move.
  PROTECT_PIERCE = 0.25

  # AI: how much more it likes a move whose Z-move it could unleash this turn.
  AI_DAMAGING_MULT = 1.6
  AI_EVOBOOST_SCORE = 260   # Last Resort -> Extreme Evoboost while the user is fresh

  def self.all_crystals
    return CRYSTALS.keys + EXCLUSIVE.keys
  end

  # A Z-crystal: listed above, or any item with the ZCrystal flag in its PBS entry.
  def self.crystal?(item)
    return false if !item
    item = item.id if item.respond_to?(:id)
    item = item.to_sym
    return true if CRYSTALS.key?(item) || EXCLUSIVE.key?(item)
    return GameData::Item.exists?(item) && GameData::Item.get(item).has_flag?("ZCrystal")
  end

  def self.zmove_ids
    return TYPE_ZMOVES.values + EXCLUSIVE.values.map { |e| e[:zmove] }
  end

  def self.power_for(base_power)
    p = base_power.to_i
    POWER_TABLE.each { |limit, pw| return pw if p <= limit }
    return POWER_MAX
  end
end
