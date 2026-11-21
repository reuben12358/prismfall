#===============================================================================
# Prismfall Z-Power - 002 The Z-move classes
#-------------------------------------------------------------------------------
# A Z-move is a Battle::Move built for one use from its PBS entry
# (pbs/moves_zpower.txt) and "attached" to the base move it came from:
#   * power from the base move (Gen 7 table), category from the base move,
#     contact if the base move makes contact
#   * pp -1, so the engine never spends its PP; the base move loses 1 PP when
#     the Z-move is unleashed instead
#   * accuracy 0 in PBS (never misses); no CanProtect flag, so Protect-style
#     moves don't stop it, and it deals 1/4 damage to a protecting target
#   * shows the base move's animation (Elite Battle DX has those)
# Bookkeeping after use (Encore, Disable, Choice lock, Copycat, Last Resort)
# points at the base move, as in Gen 7.
#===============================================================================
class Battle::Move
  def prism_zmove?; return false; end
end

module PrismfallZ
  module MoveMixin
    attr_reader :prism_base, :prism_executed

    def prism_zmove?; return true; end

    # Called once, right after the move object is created for a turn.
    def prism_attach(base_move)
      @prism_base = base_move
      @pp = -1
      @prism_executed = false
      if damagingMove? && base_move
        # A species crystal's Z-move keeps its own power (PBS); a type Z-move's comes from the base move.
        exclusive = PrismfallZ::EXCLUSIVE.values.any? { |e| e[:zmove] == @id }
        @power    = (exclusive && @power.to_i > 1) ? @power : PrismfallZ.power_for(base_move.power)
        @category = base_move.category
        @flags.push("Contact") if base_move.contactMove? && !@flags.include?("Contact")
      end
      return self
    end

    # Status-move Z-moves can't be snatched or bounced.
    def canSnatch?;      return false; end
    def canMagicCoat?;   return false; end

    # Runs after the user has passed every "can it move?" check: the Z-Power is spent here.
    def pbDisplayUseMessage(user)
      PrismfallZ.on_unleash(@battle, user, self) if !@prism_executed
      @prism_executed = true
      super
    end

    def pbShowAnimation(id, user, targets, hitNum = 0, showAnimation = true)
      if id == @id
        id = (@prism_base && damagingMove?) ? @prism_base.id : (PrismfallZ::STATUS_ANIMS[@id] || id)
      end
      super(id, user, targets, hitNum, showAnimation)
    end

    def pbModifyDamage(damageMult, user, target)
      damageMult = super
      if damagingMove? && PrismfallZ.protecting?(target)
        @battle.pbDisplay(_INTL("{1} couldn't fully protect itself and got hurt!", target.pbThis))
        damageMult *= PrismfallZ::PROTECT_PIERCE
      end
      return damageMult
    end
  end
end

#-------------------------------------------------------------------------------
# Type Z-moves (Hydro Vortex, Gigavolt Havoc...): FunctionCode PrismfallZMove.
# Used without a base move (a debug call, say), it hits at 100 power.
#-------------------------------------------------------------------------------
class Battle::Move::PrismfallZMove < Battle::Move
  include PrismfallZ::MoveMixin

  def initialize(battle, move)
    super
    @power = 100 if @power.to_i <= 1
  end
end

#-------------------------------------------------------------------------------
# Extreme Evoboost (Eevium Z + Last Resort): +2 Atk, Def, Sp. Atk, Sp. Def, Speed.
#-------------------------------------------------------------------------------
class Battle::Move::PrismfallExtremeEvoboost < Battle::Move::MultiStatUpMove
  include PrismfallZ::MoveMixin

  def initialize(battle, move)
    super
    @statUp = [:ATTACK, 2, :DEFENSE, 2, :SPECIAL_ATTACK, 2, :SPECIAL_DEFENSE, 2, :SPEED, 2]
  end
end

#-------------------------------------------------------------------------------
# Z-crystals stay put: no Knock Off, Thief, Covet, Trick, Switcheroo, Bestow.
#-------------------------------------------------------------------------------
class Battle::Battler
  alias prismfall_z_unlosableItem? unlosableItem? unless method_defined?(:prismfall_z_unlosableItem?)
  def unlosableItem?(check_item)
    return true if PrismfallZ.crystal?(check_item)
    return prismfall_z_unlosableItem?(check_item)
  end
end
