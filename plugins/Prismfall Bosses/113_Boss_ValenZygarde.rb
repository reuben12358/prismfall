#===============================================================================
# Valen's Zygarde "Order" - the Final (Festival stage :FINAL, Chapter 21
# "Sovereign"; story/40_SCRIPT_CH21.md "The Final", story/08_ACT_V.md "The Final:
# Valen Corrigan"). A trainer boss on his ace: "Zygarde on its last bar
# (Complete Forme): 'Order, not justice. I chose order.'"
#   * Bars: Casual 2, Standard 2, Hard 3. The 50% Forme holds every bar but the
#     last; when the last bar starts, the Cells gather and it becomes the
#     Complete Forme (at full HP: Complete's own, about twice the 50% Forme's).
#   * Power Construct is held back until then: with bars, "half HP" would come
#     in the middle of bar 1, and the script puts the change on the last bar.
#   * Nothing else changes: his PBS set, level (96; Casual 89) and item stay.
#     Standard and Hard get no stat multipliers (the bars are the boss); Casual's
#     bars are x0.55 HP each.
#   * The Final only (CHAMPION_VALEN v0 / 100 / 200). The Ruin Route's Last
#     Tuning (v1 / 101 / 201) keeps its Zygarde Complete from the start, no bars.
# Also from the script, Valen only: each time the arena's Plates turn, "The
# crystal climbs Valen's throat..." (the sprite overlay is the map/EBDX side).
# Harness: tools/harness/winrates_r4.rb cell VALEN (design/BALANCE.md section 9b).
#===============================================================================
module Prismfall
  module Bosses
    VALEN_FINAL_VERSIONS  = [0, 100, 200].freeze
    # Bosses whose Zygarde keeps Power Construct for its last bar.
    CONSTRUCT_ON_LAST_BAR = [:VALEN_ZYGARDE_ORDER].freeze
    VALEN_CRYSTAL_LINE    = "The crystal climbs Valen's throat..."
    # The Complete Forme's bar, as a fraction of its own (about twice the 50% Forme's) max HP (2026-11-26, Reuben:
    # prepared teams must be able to win; at full Complete HP Hard prepared fell 35% -> 0%). Casual keeps it full.
    VALEN_COMPLETE_HP     = { :CASUAL => 1.0, :STANDARD => 0.6, :HARD => 0.5 }

    # True while a bar-boss Zygarde still has bars to lose (its Power Construct waits).
    def self.construct_held?(battler)
      return false if !battler || !battler.isSpecies?(:ZYGARDE) || battler.form >= 2
      st = state_for(battler)
      return st && CONSTRUCT_ON_LAST_BAR.include?(st.id) && !st.last_bar? ? true : false
    end

    # The last bar: the Cells gather (Power Construct's own lines), then Valen's.
    ZYGARDE_COMPLETE_PROC = proc { |battle, b, _st|
      if b.form < 2 && !b.fainted?
        battle.pbDisplay(Prismfall::Bosses.text("You sense the presence of many!"))
        if b.hasActiveAbility?(:POWERCONSTRUCT)
          battle.pbShowAbilitySplash(b, true)
          battle.pbHideAbilitySplash(b)
        end
        b.pbChangeForm(b.form + 2, Prismfall::Bosses.text("{1} transformed into its Complete Forme!", b.pbThis))
        frac = Prismfall::Bosses.resolve(VALEN_COMPLETE_HP) || 1.0
        if frac < 1.0
          b.hp = [[(b.totalhp * frac).round, 1].max, b.hp].min
          battle.scene.pbRefreshOne(b.index) if battle.scene.respond_to?(:pbRefreshOne)
        end
      end
      battle.pbDisplay(Prismfall::Bosses.text("Valen: \"Order, not justice. I chose order.\""))
    }

    def self.valen_final?(battle)
      return false if !battle || !battle.opponent
      return battle.opponent.any? do |t|
        t && t.trainer_type == :CHAMPION_VALEN &&
          VALEN_FINAL_VERSIONS.include?(t.respond_to?(:version) ? t.version.to_i : 0)
      end
    end
  end
end

class Battle::Battler
  alias prismfall_valen_pbCheckForm pbCheckForm unless method_defined?(:prismfall_valen_pbCheckForm)
  def pbCheckForm(endOfRound = false)
    return if endOfRound && Prismfall::Bosses.construct_held?(self)   # Zygarde has no other form check
    return prismfall_valen_pbCheckForm(endOfRound)
  end
end

Prismfall::Bosses.register(:VALEN_ZYGARDE_ORDER, {
  :bars       => { :CASUAL => 2, :STANDARD => 2, :HARD => 3 },
  # Hard's three bars are x0.5 HP each (2026-11-26: at full HP Hard prepared teams never got through them).
  :stat_mults => { :CASUAL => { :HP => 0.55 }, :HARD => { :HP => 0.7 } },
  :catch      => false,
  :intro      => ["Order rises out of the arena floor, cell by cell."],
  :on_break   => [
    { :cure_status => true, :reset_stats => :negative },
    { :condition => proc { |_battle, _b, st| !st.last_bar? },
      :messages  => ["More Cells pour up through the cracks in the floor. {1} holds its shape!"] },   # (no +1 Defense since 2026-11-26)
    { :condition => proc { |_battle, _b, st| st.last_bar? },
      :proc      => Prismfall::Bosses::ZYGARDE_COMPLETE_PROC }
  ],
  :description => "Ch21 the Final: Valen's Zygarde \"Order\" (trainer boss); Complete Forme on its last bar"
})

Prismfall::Bosses.register_trainer_boss(:VALEN_FINAL_ZYGARDE, {
  :trainer_type => :CHAMPION_VALEN, :name => "Valen",
  :versions     => Prismfall::Bosses::VALEN_FINAL_VERSIONS,   # never the Last Tuning (v1 / 101 / 201)
  :species      => :ZYGARDE,
  :boss         => :VALEN_ZYGARDE_ORDER
})

# "Each time the field cycles (a battle hook, Valen only): his crystal visibly spreads."
EventHandlers.add(:prismfall_field_overlay_changed, :prismfall_valen_crystal,
  proc { |battle, field_id, old_ids, new_ids|
    next if field_id != :PRISM_ARENA || old_ids == new_ids || battle.decision != 0
    next if !Prismfall::Bosses.valen_final?(battle)
    battle.pbDisplay(Prismfall::Bosses.text(Prismfall::Bosses::VALEN_CRYSTAL_LINE))
  }
)
