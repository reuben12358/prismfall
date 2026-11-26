#===============================================================================
# Arceus - the True Finale (Festival stage :ARCEUS, design/BALANCE.md §7).
# Core's Prismfall::Festival.boss_battle runs this automatically when this
# plugin is installed (FESTIVAL_BOSSES / stage :prismfall_boss). Battle field:
# :PRISM_ARENA.
# Bars = locks (NARRATIVE_KEYS 6.7, story/40_SCRIPT_CH21.md "Six bars, three
# locks each, in gym order"): the bar count comes from the STORY VARIANT
# (Prismfall::Festival.arceus_variant: Bound 6, Gilded 6, Miscalibrated 5,
# War 7, Judgment 7), never from the difficulty. Bar k holds the Plates of gyms
# 3k-2..3k, so within a bar the arena cycles only that trio's gym fields, in gym
# order (:prism_order -> the arena's :set_order; bar 1 Grand Stage / Silkwood /
# Water Surface ... bar 6 New Moon / Fairy Tale / Dragon's Den). Every bar break
# moves the arena to the next trio and turns the Plates at once through the
# arena's own announced :turn (Multitype re-types); Arceus then takes that
# type's form and Plate moveset. The arena's regular turns inside a bar are
# followed the same way (:follow_prism).
#   Miscalibrated: bar 5 cycles all six fields of gyms 13-18 (bar HP x0.85).
#   War / Judgment: bar 7 is the Legend Plate phase (??? type; War settles the
#     arena by Resonance, Judgment turns it to :INVERSE).
#   Forced locks: each Warden of the coming bar who refuses (WARDEN_CONSENT
#     false) gives Arceus +1 to every stat stage for that bar; on War every lock
#     is forced (capped at +2 on Casual / Standard, BALANCE.md section 7).
#     Casual only: a forced lock raises Defense and Sp. Def alone, at most +2.
#   Casual is the only eased mode (bar HP x0.6, offence x0.6, Safeguard for
#   Recover / Calm Mind); Standard and Hard are the BALANCE.md numbers.
#   HARMONY_BUFF (Resonance >= 6): at every break the PC's active Pokemon
#     recover 25% HP and lose their stat drops.
#   Event :prismfall_arceus_locks (battle, bar, gym numbers, refusing gym numbers)
#     fires as each bar starts, for the pylon / release staging.
# Not built here (TODO_QUOTA): Gilded's bar-6 refills and scripted binding, the
# Judgment variant's Giratina partner, the 36 release / refusal lines.
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

    # Casual: no Recover and no Calm Mind (Safeguard in slot 4). Hard: Mind Plate sets Trick Room.
    def self.arceus_movesets
      sets = ARCEUS_MOVESETS.transform_values(&:dup)
      case difficulty
      when :CASUAL then sets.each_value { |m| m[3] = :SAFEGUARD }      # no Recover and no setup (was Calm Mind: it snowballed)
      when :HARD   then sets[:PSYCHIC][3] = :TRICKROOM
      end
      return sets
    end

    def self.ruin_lean?
      return false if !defined?(Prismfall::Resonance)
      return [:ruin_leaning, :ruin].include?(Prismfall::Resonance.band) if Prismfall::Resonance.respond_to?(:band)
      return Prismfall::Resonance.value.to_i < 0
    end

    #---------------------------------------------------------------------------
    # The story variant (Core 015_Festival_Draw.rb ARCEUS_VARIANTS; first match wins).
    #---------------------------------------------------------------------------
    ARCEUS_DEFAULT_VARIANT = { :id => :ARCEUS_BOUND, :bars => 6 }.freeze
    ARCEUS_STAT_STAGES     = [:ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED].freeze
    ARCEUS_WAR_STAGE_CAP   = { :CASUAL => 2, :STANDARD => 2, :HARD => 3 }
    # Casual only: a forced lock hardens Arceus (Defense, Sp. Def) but doesn't sharpen it; at most two stages a bar.
    ARCEUS_FORCED_STAGES   = { :CASUAL => [:DEFENSE, :SPECIAL_DEFENSE], :default => ARCEUS_STAT_STAGES }
    ARCEUS_FORCED_CAP      = { :CASUAL => 2, :default => 3 }

    class << self
      # Tests / debug: a variant id (:ARCEUS_WAR ...) or Hash to force, and a proc { |gym| true/false } for consent.
      attr_accessor :arceus_variant_override, :arceus_consent_override
    end

    def self.arceus_variant
      ov = @arceus_variant_override
      return ov if ov.is_a?(Hash)
      draw = (defined?(Prismfall::Festival)) ? Prismfall::Festival : nil
      if ov && draw && draw.const_defined?(:ARCEUS_VARIANTS)
        v = draw::ARCEUS_VARIANTS.find { |x| x[:id] == ov }
        return v if v
      end
      v = (draw && draw.respond_to?(:arceus_variant)) ? (draw.arceus_variant rescue nil) : nil
      return (v.is_a?(Hash) && v[:bars].is_a?(Integer)) ? v : ARCEUS_DEFAULT_VARIANT
    end

    def self.arceus_bars
      return [arceus_variant[:bars].to_i, 1].max
    end

    # Gym numbers (1-18) locked into each bar.
    def self.arceus_bar_gyms
      trios = (1..18).each_slice(3).to_a
      return trios[0, 4] + [(13..18).to_a] if arceus_variant[:id] == :ARCEUS_MISCALIBRATED
      return trios
    end

    def self.arceus_gym_field(n)
      g = (Prismfall.respond_to?(:gym)) ? (Prismfall.gym(n) rescue nil) : nil
      return g ? g[:field] : nil
    end

    # :prism_order - one list of gym fields per bar (a 7th bar is the Legend Plate phase and never reads it).
    def self.arceus_prism_order
      return arceus_bar_gyms.map { |gyms| gyms.map { |n| arceus_gym_field(n) }.compact }
    end

    def self.arceus_consents?(gym)
      ov = @arceus_consent_override
      return (ov.call(gym) ? true : false) if ov.respond_to?(:call)
      list = (defined?(Prismfall::Narrative) && Prismfall::Narrative.const_defined?(:WARDEN_CONSENT)) ? Prismfall::Narrative::WARDEN_CONSENT : nil
      cond = list && list[gym - 1]
      return true if !cond
      return (Prismfall::Conditions.evaluate(cond) ? true : false) rescue true
    end

    # Gym numbers of the given bar whose lock is forced.
    def self.arceus_forced_locks(bar)
      gyms = arceus_bar_gyms[bar - 1]
      return [] if !gyms
      return gyms.dup if arceus_variant[:id] == :ARCEUS_WAR      # the shard eats the types: nobody is asked
      return gyms.reject { |n| arceus_consents?(n) }
    end

    # A bar starts: forced locks (+1 to every stat stage per refusing Warden, for this bar only).
    def self.arceus_start_bar(battle, b, st)
      bar    = st.phase
      forced = arceus_forced_locks(bar)
      prev   = battle.instance_variable_get(:@prismfall_arceus_forced).to_i
      stats = resolve(ARCEUS_FORCED_STAGES) || ARCEUS_STAT_STAGES
      if prev > 0     # last bar's forced locks are spent
        stats.each { |s| b.stages[s] = [b.stages[s] - prev, 0].max if b.stages[s] > 0 }
      end
      n = [forced.length, resolve(ARCEUS_FORCED_CAP) || 3].min
      n = [n, resolve(ARCEUS_WAR_STAGE_CAP) || 2].min if arceus_variant[:id] == :ARCEUS_WAR
      battle.instance_variable_set(:@prismfall_arceus_forced, n)
      if n > 0
        battle.pbDisplay(text((n == 1) ? "A lock holds! Its Plate is torn free by force!" : "{2} locks hold! Their Plates are torn free by force!", b.pbThis, n))
        stats.each { |s| b.stages[s] = [b.stages[s] + n, 6].min }
        battle.pbCommonAnimation("StatUp", b) rescue nil
        battle.pbDisplay(text((stats.length < ARCEUS_STAT_STAGES.length) ? "{1}'s defenses hardened!" : "{1}'s power surged!", b.pbThis))
      end
      EventHandlers.trigger(:prismfall_arceus_locks, battle, bar, arceus_bar_gyms[bar - 1] || [], forced)
    end

    def self.arceus_harmony_buff(battle, boss)
      return if !defined?(Prismfall::Narrative) || !(Prismfall::Narrative.flag(:HARMONY_BUFF) rescue false)
      shown = false
      battle.allOtherSideBattlers(boss.index).each do |a|
        next if a.fainted?
        battle.pbDisplay(text("The shard in your chest hums, and your Pokémon steady!")) if !shown
        shown = true
        a.pbRecoverHP((a.totalhp / 4.0).round) if a.hp < a.totalhp
        a.stages.each_key { |s| a.stages[s] = 0 if a.stages[s] < 0 }
      end
    end

    # The seventh bar (War, Judgment) is the Legend Plate phase; ARCEUS_LEGEND_PHASE forces it on any last bar.
    def self.arceus_legend_final?(st)
      return false if !st.last_bar?
      return ARCEUS_LEGEND_PHASE || st.bars >= 7
    end

    ARCEUS_LEGEND_PROC = proc { |battle, b, _st|
      field = (Prismfall::Bosses.harmony_lean?) ? :RAINBOW : (Prismfall::Bosses.ruin_lean?) ? :BLEED : :NONE
      field = :INVERSE if Prismfall::Bosses.arceus_variant[:id] == :ARCEUS_JUDGMENT   # Giratina turns the arena inside out
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
  # Bars by story variant, not by difficulty (was 3 / 3 / 4 until 2026-11-25). Bar HP by difficulty (BALANCE.md
  # section 7's "bar HP" row): Casual x0.6, Standard x1.0, Hard x1.25 of Arceus's max HP a bar.
  :bars              => proc { Prismfall::Bosses.arceus_bars },
  :prism_order       => proc { Prismfall::Bosses.arceus_prism_order },
  :stat_mults        => {
    :CASUAL   => { :HP => 0.5, :ATTACK => 0.6, :SPECIAL_ATTACK => 0.6 },
    :STANDARD => { :ATTACK => 1.25, :DEFENSE => 1.25, :SPECIAL_ATTACK => 1.25, :SPECIAL_DEFENSE => 1.25, :SPEED => 1.1 },
    :HARD     => { :HP => 1.25, :ATTACK => 1.3, :DEFENSE => 1.3, :SPECIAL_ATTACK => 1.3, :SPECIAL_DEFENSE => 1.3, :SPEED => 1.15 }
  },
  :field             => :PRISM_ARENA,
  :catch             => false,
  :status_immunity   => true,
  :immunity_last_bar => true,
  :intro             => ["The eighteen Plates blaze as one... Arceus descends upon Crownhaven!"],
  :break_message     => "The Plates around {1} crack and reform!",
  :on_break          => [
    # Miscalibrated: the last bar holds six Plates; BALANCE.md section 7 keeps it fair with bar HP x0.85.
    { :condition => proc { |_battle, _b, st| st.last_bar? && Prismfall::Bosses.arceus_variant[:id] == :ARCEUS_MISCALIBRATED },
      :refill => 0.85 },
    { :condition => proc { |_battle, _b, st| !Prismfall::Bosses.arceus_legend_final?(st) },
      :messages => ["The Plates answer their god!"], :prism_turn => true,
      :reset_stats => :negative, :cure_status => true,
      :proc => proc { |battle, b, st| Prismfall::Bosses.arceus_start_bar(battle, b, st) } },
    { :condition => proc { |_battle, _b, st| Prismfall::Bosses.arceus_legend_final?(st) },
      :messages => ["Your Legend Plate fragment resonates with Arceus!"],
      :reset_stats => :negative, :cure_status => true,
      :proc => proc { |battle, b, st|
        Prismfall::Bosses::ARCEUS_LEGEND_PROC.call(battle, b, st)
        Prismfall::Bosses.arceus_start_bar(battle, b, st)
      } },
    { :proc => proc { |battle, b, _st| Prismfall::Bosses.arceus_harmony_buff(battle, b) } }
  ],
  :follow_prism      => { :form => true, :form_message => "{1} took on the {2} type!",
                          :movesets => proc { Prismfall::Bosses.arceus_movesets } },
  :ai_script         => { 1 => [:CALMMIND] },
  :ebdx              => { :databox => true }
})

# Bar 1's locks: forced before the first blow if its Wardens refuse (the later bars are handled at each break).
EventHandlers.add(:prismfall_boss_entered, :prismfall_arceus_first_bar,
  proc { |battle, battler, id|
    next if id != :ARCEUS_FINALE
    st = Prismfall::Bosses.state_for(battler)
    Prismfall::Bosses.arceus_start_bar(battle, battler, st) if st && st.breaks_done == 0
  }
)
