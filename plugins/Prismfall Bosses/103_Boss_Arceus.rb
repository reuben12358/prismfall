#===============================================================================
# Arceus - the True Finale (Festival stage :ARCEUS, design/BALANCE.md §7).
# Core's Prismfall::Festival.boss_battle runs this automatically when this
# plugin is installed (FESTIVAL_BOSSES / stage :prismfall_boss). Battle field:
# :PRISM_ARENA. Every bar break turns the Plates through the arena's own
# announced :turn (the next gym field is borrowed and Multitype re-types);
# Arceus then takes that type's form and Plate moveset. The arena's regular
# turns are followed the same way (:follow_prism).
#===============================================================================
module Prismfall
  module Bosses
    # BALANCE.md's optional final phase: on the last bar the Legend Plate wakes,
    # Arceus becomes ??? and the arena settles by Resonance (Harmony :RAINBOW,
    # Ruin :BLEED, otherwise no field). Off by default: every break turns the Plates.
    ARCEUS_LEGEND_PHASE = false

    # Slot 1 Judgment; coverage hits what resists that Plate (BALANCE.md §7).
    ARCEUS_MOVESETS = {
      :NORMAL   => [:JUDGMENT, :SHADOWBALL, :FOCUSBLAST, :CALMMIND],
      :BUG      => [:JUDGMENT, :EARTHPOWER, :SHADOWBALL, :RECOVER],
      :WATER    => [:JUDGMENT, :ICEBEAM, :THUNDERBOLT, :RECOVER],
      :ELECTRIC => [:JUDGMENT, :FLASHCANNON, :ICEBEAM, :RECOVER],
      :GROUND   => [:JUDGMENT, :FIREBLAST, :SHADOWBALL, :RECOVER],
      :POISON   => [:JUDGMENT, :EARTHPOWER, :SHADOWBALL, :RECOVER],
      :FIRE     => [:JUDGMENT, :EARTHPOWER, :WILLOWISP, :RECOVER],
      :FIGHTING => [:JUDGMENT, :SHADOWBALL, :PSYCHIC, :RECOVER],
      :GRASS    => [:JUDGMENT, :EARTHPOWER, :SLUDGEBOMB, :RECOVER],
      :ICE      => [:JUDGMENT, :THUNDERBOLT, :EARTHPOWER, :RECOVER],
      :FLYING   => [:JUDGMENT, :THUNDERBOLT, :FOCUSBLAST, :RECOVER],
      :PSYCHIC  => [:JUDGMENT, :FOCUSBLAST, :SHADOWBALL, :CALMMIND],
      :ROCK     => [:JUDGMENT, :EARTHPOWER, :FIREBLAST, :RECOVER],
      :GHOST    => [:JUDGMENT, :FOCUSBLAST, :WILLOWISP, :RECOVER],
      :STEEL    => [:JUDGMENT, :EARTHPOWER, :THUNDERBOLT, :RECOVER],
      :DARK     => [:JUDGMENT, :FOCUSBLAST, :FLAMETHROWER, :CALMMIND],
      :FAIRY    => [:JUDGMENT, :FLAMETHROWER, :EARTHPOWER, :RECOVER],
      :DRAGON   => [:JUDGMENT, :FIREBLAST, :EARTHPOWER, :RECOVER]
    }.freeze
    ARCEUS_LEGEND_MOVES = [:JUDGMENT, :EXTREMESPEED, :CALMMIND, :RECOVER]

    # Casual: no Recover. Hard: Mind Plate sets Trick Room.
    def self.arceus_movesets
      sets = ARCEUS_MOVESETS.transform_values(&:dup)
      case difficulty
      when :CASUAL then sets.each_value { |m| m[3] = :CALMMIND if m[3] == :RECOVER }
      when :HARD   then sets[:PSYCHIC][3] = :TRICKROOM
      end
      return sets
    end

    def self.ruin_lean?
      return false if !defined?(Prismfall::Resonance)
      return [:ruin_leaning, :ruin].include?(Prismfall::Resonance.band) if Prismfall::Resonance.respond_to?(:band)
      return Prismfall::Resonance.value.to_i < 0
    end

    def self.arceus_legend_final?(st)
      return ARCEUS_LEGEND_PHASE && st.last_bar?
    end

    ARCEUS_LEGEND_PROC = proc { |battle, b, _st|
      field = (Prismfall::Bosses.harmony_lean?) ? :RAINBOW : (Prismfall::Bosses.ruin_lean?) ? :BLEED : :NONE
      battle.change_field(field, (field == :NONE) ? "The Plates fall silent." : nil) if battle.respond_to?(:change_field)
      f = Prismfall::Bosses.form_for_type(:ARCEUS, :QMARKS)
      b.pbChangeForm(f, Prismfall::Bosses.text("{1} became the ??? type!", b.pbThis)) if f
      Prismfall::Bosses.set_moves(battle, b, ARCEUS_LEGEND_MOVES)
    }
  end
end

Prismfall::Bosses.register(:ARCEUS_FINALE, {
  :species           => :ARCEUS,
  :level             => 100,
  :ability           => :MULTITYPE,
  :nature            => :TIMID,
  :ivs               => 31,
  :evs               => { :HP => 4, :SPECIAL_ATTACK => 252, :SPEED => 252 },
  :moves             => Prismfall::Bosses::ARCEUS_MOVESETS[:NORMAL],
  :bars              => { :CASUAL => 3, :STANDARD => 3, :HARD => 4 },
  :stat_mults        => {
    :CASUAL   => { :ATTACK => 1.1, :DEFENSE => 1.1, :SPECIAL_ATTACK => 1.1, :SPECIAL_DEFENSE => 1.1, :SPEED => 1.1 },
    :STANDARD => { :ATTACK => 1.25, :DEFENSE => 1.25, :SPECIAL_ATTACK => 1.25, :SPECIAL_DEFENSE => 1.25, :SPEED => 1.1 },
    :HARD     => { :ATTACK => 1.3, :DEFENSE => 1.3, :SPECIAL_ATTACK => 1.3, :SPECIAL_DEFENSE => 1.3, :SPEED => 1.15 }
  },
  :field             => :PRISM_ARENA,
  :catch             => false,
  :status_immunity   => true,
  :immunity_last_bar => true,
  :intro             => ["The eighteen Plates blaze as one... Arceus descends upon Crownhaven!"],
  :break_message     => "The Plates around {1} crack and reform!",
  :on_break          => [
    { :condition => proc { |_battle, _b, st| !Prismfall::Bosses.arceus_legend_final?(st) },
      :messages => ["The Plates answer their god!"], :prism_turn => true,
      :reset_stats => :negative, :cure_status => true },
    { :condition => proc { |_battle, _b, st| Prismfall::Bosses.arceus_legend_final?(st) },
      :messages => ["Your Legend Plate fragment resonates with Arceus!"], :proc => Prismfall::Bosses::ARCEUS_LEGEND_PROC,
      :reset_stats => :negative, :cure_status => true }
  ],
  :follow_prism      => { :form => true, :form_message => "{1} took on the {2} type!",
                          :movesets => proc { Prismfall::Bosses.arceus_movesets } },
  :ai_script         => { 1 => [:CALMMIND] },
  :ebdx              => { :databox => true }
})
