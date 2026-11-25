#===============================================================================
# Prismfall Mega - 002 Battle rules: one Mega per trainer, Z-crystals, the event
#-------------------------------------------------------------------------------
# Battle#pbCanMegaEvolve? is the one question every Mega choice asks: Essentials'
# Fight menu, Elite Battle DX's Mega button (UI Fight.rb), the AI
# (Battle::AI#pbEnemyShouldMegaEvolve?) and the AI playing the player's side.
# Battle#pbMegaEvolve does the change; after it this plugin fires
# :prismfall_mega_evolved and runs the field interactions (003).
# Essentials keeps @megaEvolution[side][owner]: -1 = not chosen, idx = chosen this
# turn, -2 = used. LIMIT == :trainer (the rule since 2026-11-25) is exactly that:
# each trainer once, so both foes of a tag pair, and the player and a partner,
# can each Mega Evolve. With LIMIT == :side, a trainer may not Mega Evolve while
# another trainer on the same side has chosen or used theirs.
# Partners: Essentials forgets a registered partner's Items, so its Mega Ring
# never reached the battle. pbRegisterPartner now keeps the ring(s) (only those:
# a partner still brings no medicine), and the battle hands them to the ally.
#===============================================================================
module PrismfallMega
  # [battler index, species, mega form name, field] for each Mega Evolution (tests read it).
  def self.log(battle)
    battle.instance_variable_set(:@prism_mega_log, []) if !battle.instance_variable_get(:@prism_mega_log)
    return battle.instance_variable_get(:@prism_mega_log)
  end

  # True if another trainer on idxBattler's side has chosen or used its Mega this battle.
  def self.side_taken?(battle, idx)
    return false if LIMIT != :side
    b = battle.battlers[idx]
    return false if !b
    side  = b.idxOwnSide
    owner = battle.pbGetOwnerIndexFromBattlerIndex(idx)
    row = battle.megaEvolution[side] || []
    row.each_with_index do |v, i|
      next if i == owner
      return true if v != -1
    end
    return false
  end

  def self.holds_z_crystal?(battler)
    return false if !Z_CRYSTAL_BLOCKS_MEGA || !defined?(PrismfallZ) || !battler
    return PrismfallZ.crystal?(battler.item_id)
  end

  def self.ring?
    return $bag && $bag.has?(RING)
  end

  def self.on_mega(battle, battler, old_ability)
    log(battle).push([battler.index, battler.species, battler.pokemon.megaName.to_s,
                      (battle.respond_to?(:field_effect) ? battle.field_effect : nil)])
    EventHandlers.trigger(:prismfall_mega_evolved, battle, battler, old_ability)
  end
end

class Battle
  alias prismfall_mega_pbCanMegaEvolve? pbCanMegaEvolve? unless method_defined?(:prismfall_mega_pbCanMegaEvolve?)
  def pbCanMegaEvolve?(idxBattler)
    return false if !prismfall_mega_pbCanMegaEvolve?(idxBattler)
    b = @battlers[idxBattler]
    return false if PrismfallMega.holds_z_crystal?(b)
    return false if PrismfallMega.side_taken?(self, idxBattler)
    return true
  end

  alias prismfall_mega_pbMegaEvolve pbMegaEvolve unless method_defined?(:prismfall_mega_pbMegaEvolve)
  def pbMegaEvolve(idxBattler)
    b = @battlers[idxBattler]
    was_mega = (b && b.pokemon) ? b.mega? : true
    old_ability = (b) ? b.ability_id : nil
    prismfall_mega_pbMegaEvolve(idxBattler)
    return if was_mega || !b || !b.pokemon || !b.mega?
    PBDebug.logonerr { PrismfallMega.on_mega(self, b, old_ability) }
  end
end

#-------------------------------------------------------------------------------
# A registered partner keeps its Mega Ring ($PokemonGlobal.partner[4]).
#-------------------------------------------------------------------------------
module PrismfallMega
  class << self
    attr_accessor :last_loaded_trainer
  end

  # The Mega Rings among a trainer's Items (item flag "MegaRing").
  def self.rings_of(items)
    return Array(items).select { |i| GameData::Item.exists?(i) && GameData::Item.get(i).has_flag?("MegaRing") }.uniq
  end
end

EventHandlers.add(:on_trainer_load, :prismfall_mega_last_loaded,
  proc { |trainer| PrismfallMega.last_loaded_trainer = trainer }
)

alias prismfall_mega_pbRegisterPartner pbRegisterPartner unless defined?(prismfall_mega_pbRegisterPartner)
def pbRegisterPartner(tr_type, tr_name, tr_id = 0)
  PrismfallMega.last_loaded_trainer = nil
  ret = prismfall_mega_pbRegisterPartner(tr_type, tr_name, tr_id)
  trainer = PrismfallMega.last_loaded_trainer     # the object Essentials loaded (after every :on_trainer_load handler)
  PrismfallMega.last_loaded_trainer = nil
  if $PokemonGlobal && $PokemonGlobal.partner && trainer && trainer.respond_to?(:items)
    $PokemonGlobal.partner[4] = PrismfallMega.rings_of(trainer.items)
  end
  return ret
end

module BattleCreationHelperMethods
  class << self
    alias prismfall_mega_set_up_player_trainers set_up_player_trainers unless method_defined?(:prismfall_mega_set_up_player_trainers)
    def set_up_player_trainers(foe_party)
      ret = prismfall_mega_set_up_player_trainers(foe_party)
      rings = ($PokemonGlobal && $PokemonGlobal.partner) ? $PokemonGlobal.partner[4] : nil
      if rings.is_a?(Array) && !rings.empty? && ret[0].length > 1 && ret[1].is_a?(Array)
        ret[1][1] = (Array(ret[1][1]) + rings).uniq
      end
      return ret
    end
  end
end

#-------------------------------------------------------------------------------
# Z-moves: one per SIDE (SPINE Rev 20; unchanged by the per-trainer Mega rule). Prismfall Z-Power keys its
# "used" record and its partner check on owner_key; with Z_LIMIT == :side the key
# is the side alone, so a side gets one Z-move however many trainers it has.
#-------------------------------------------------------------------------------
if defined?(PrismfallZ) && PrismfallZ.respond_to?(:owner_key)
  module PrismfallZ
    class << self
      alias prismfall_mega_owner_key owner_key unless method_defined?(:prismfall_mega_owner_key)
      def owner_key(battle, idx)
        return [idx & 1] if PrismfallMega::Z_LIMIT == :side
        return prismfall_mega_owner_key(battle, idx)
      end
    end
  end
end
