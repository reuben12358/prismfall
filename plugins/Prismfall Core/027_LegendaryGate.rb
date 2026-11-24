#===============================================================================
# Prismfall Core - 027 Legendary catch gate (Reuben's rule: no legendary is
# caught or gifted in the main story; design/POKEMON_AVAILABILITY.md §4).
#-------------------------------------------------------------------------------
# A safety net under every boss's own :catch => false (Gemini proposal
# 2026-11-23 gen6-9-sprites-postgame-legendaries-dorian-meloetta, Part B.2):
# before the post-game (S160 POSTGAME or Prismfall::Endings.postgame?), a Poké
# Ball thrown at any wild Legendary, Mythical, Ultra Beast or Paradox Pokémon,
# or at one of EXTRA_LOCKED_SPECIES, is deflected (Prismfall Bosses
# 004_Bosses_Battle.rb pbThrowPokeBall). The post-game Legends board (S270+)
# hands them out.
#   Prismfall.legendary_catch_allowed?(pkmn)  -> false while the gate holds
#   Prismfall.story_legendary_locked?(pkmn)   -> the inverse
#   Prismfall.postgame_unlocked?
# Exempt one species for testing: Prismfall::LEGENDARY_CATCH_EXEMPT << :MEW
#===============================================================================
module Prismfall
  LEGENDARY_FLAGS       = %w[Legendary Mythical SubLegendary UltraBeast Paradox].freeze
  EXTRA_LOCKED_SPECIES  = [:TYPENULL, :SILVALLY, :KUBFU, :URSHIFU].freeze
  LEGENDARY_CATCH_EXEMPT = []
  LEGENDARY_GATE_SWITCH = 160   # S160 POSTGAME (design/FLAGS.md)
  LEGENDARY_GATE_MESSAGE = "Its power refuses to be bound while Velmora's Plates remain unsettled!"

  def self.postgame_unlocked?
    return true if defined?(Prismfall::Endings) && (Prismfall::Endings.postgame? rescue false)
    return ($game_switches && $game_switches[LEGENDARY_GATE_SWITCH]) ? true : false
  end

  def self.legendary_species?(species)
    data = GameData::Species.try_get(species)
    return false if !data
    return true if EXTRA_LOCKED_SPECIES.include?(data.species)
    flags = data.flags || []
    return LEGENDARY_FLAGS.any? { |f| flags.include?(f) }
  end

  def self.story_legendary_locked?(pkmn)
    return false if !pkmn || postgame_unlocked?
    species = (pkmn.respond_to?(:species)) ? pkmn.species : pkmn
    return false if LEGENDARY_CATCH_EXEMPT.include?(species)
    return legendary_species?(species)
  end

  def self.legendary_catch_allowed?(pkmn)
    return !story_legendary_locked?(pkmn)
  end
end
