#===============================================================================
# Prismfall Core - 023 Sidequest cameo fights + trainer HP boosts
#-------------------------------------------------------------------------------
# SPINE Revision 4: the Reborn/Rejuvenation/Desolation cameos are optional
# sidequest fights, not Festival entrants.
#   Prismfall.cameo_battle(:FESTIVAL_LIN, "Lin", 9)
# This is a normal trainer battle (difficulty variant via pbLoadTrainer, canLose,
# so no blackout). The first win against each cameo trainer type is written to
# the Ledger (Cameos tab). Returns true on a win.
#
# HP_BOOSTS gives specific trainer Pokémon a max-HP multiplier (BALANCE.md:
# Shiv's Ambipom "absurd HP" = x2), independent of EBDX's :bossboost.
#===============================================================================
module Prismfall
  HP_BOOSTS = [
    { :trainer_type => :FESTIVAL_SHIV, :species => :AMBIPOM, :multiplier => 2.0 }
  ]

  def self.cameo_battle(trainer_type, trainer_name, version = 0, lose_text: nil, double: false,
                        field: nil, outcome_var: nil)
    setBattleRule("canLose")
    setBattleRule("double") if double
    setBattleRule("outcomeVar", outcome_var) if outcome_var
    set_field_rule(field) if field
    won = TrainerBattle.start([trainer_type, trainer_name, version, lose_text]) ? true : false
    if won
      first = Ledger.record_cameo(trainer_type)
      EventHandlers.trigger(:prismfall_cameo_beaten, trainer_type, first)
      if first && Narrative::CAMEOS.has_key?(trainer_type)
        pbMessage(_INTL("\\se[]A new name was written in the Ledger: {1}.", _INTL(Narrative::CAMEOS[trainer_type])))
      end
    end
    return won
  end

  def self.apply_hp_boosts(trainer)
    return if !trainer.respond_to?(:trainer_type) || !trainer.respond_to?(:party)
    HP_BOOSTS.each do |b|
      next if b[:trainer_type] != trainer.trainer_type
      trainer.party.each_with_index do |pkmn, i|
        next if !pkmn
        next if b[:species] && !pkmn.isSpecies?(b[:species])
        next if b[:slot] && b[:slot] != i
        pkmn.prismfall_hp_multiplier = b[:multiplier]
        pkmn.calc_stats
        pkmn.hp = pkmn.totalhp
      end
    end
  end
end

EventHandlers.add(:on_trainer_load, :prismfall_hp_boosts,
  proc { |trainer| Prismfall.apply_hp_boosts(trainer) if trainer }
)

class Pokemon
  attr_accessor :prismfall_hp_multiplier

  alias __prismfall_core_calc_stats calc_stats unless method_defined?(:__prismfall_core_calc_stats)

  # *args keeps EBDX's calc_stats(basestat, boss) signature working.
  def calc_stats(*args)
    ret = __prismfall_core_calc_stats(*args)
    m = @prismfall_hp_multiplier
    if m && m != 1 && @totalhp.to_i > 1
      base = @totalhp
      @totalhp = (base * m).floor
      @hp = [@hp + (@totalhp - base), @totalhp].min if @hp > 0
    end
    return ret
  end
end
