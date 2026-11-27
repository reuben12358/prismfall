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
# arena's own announced :turn (Multitype re-types), to the trio's field best
# against the player's active Pokemon (:prism_best_field; the cycle goes on from
# there in gym order); Arceus then takes that type's form and Plate moveset. The
# arena's regular turns inside a bar are followed the same way (:follow_prism),
# telegraphed 2 rounds ahead on Casual, 1 elsewhere (:prism_telegraph).
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
#   Events, for the pylon staging (Bosses 116 plays the 36 release / refusal
#   lines of story/11_FINALE_LINES.md on them):
#     :prismfall_arceus_locks        (battle, bar, gyms, forced)  a bar starts:
#        its Wardens kneel and release or refuse (before the forced-lock boost)
#     :prismfall_arceus_locks_broken (battle, bar, gyms, forced, final)  the bar
#        breaks: the refused locks tear free by force
#   Gilded (ENGINE_CALIBRATED): "the last bar can't be broken". It refills three
#     times, then the Gilded Chain closes (the last bar is one bar's HP in four
#     pieces: 0.4, then 3 x 0.2; 2026-11-26): the battle ends, result
#     :gilded_chain (the event then runs END_GILDED_CHAIN). Elsewhere the last
#     bar's fall ends the battle as a win, result :freed (Arceus never faints).
#   Judgment (Ruin Route R7): Giratina-Origin fights at the PC's side (:partner,
#     PARTNER_GIRATINA "Depths", a 2v1) and "no Warden releases anything; all
#     eighteen locks hold": every lock forced, capped like War.
#   Standard: Recover at most twice a bar (BALANCE.md section 7, :move_limits).
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
    # When nobody is asked (every lock forced), the forced stages a bar are capped (BALANCE.md section 7: +2 on
    # Casual / Standard).
    ARCEUS_WAR_STAGE_CAP   = { :CASUAL => 2, :STANDARD => 2, :HARD => 3 }
    # Casual only: a forced lock hardens Arceus (Defense, Sp. Def) but doesn't sharpen it; at most two stages a bar.
    ARCEUS_FORCED_STAGES   = { :CASUAL => [:DEFENSE, :SPECIAL_DEFENSE], :default => ARCEUS_STAT_STAGES }
    # Standard / Hard (2026-11-26, a refusal is a consequence, not a dead end): a refusing Warden's lock raises the one
    # stat its Plate stands for, +1 each (two refusals on one stat stack), instead of +1 to every stat (a refusal in
    # every bar was 0% for prepared teams). :all restores the old rule. Casual keeps ARCEUS_FORCED_STAGES above.
    ARCEUS_REFUSAL_SCOPE   = :plate
    ARCEUS_PLATE_STATS = {
      :NORMAL => :SPEED,           :BUG => :SPEED,              :FLYING => :SPEED,
      :ELECTRIC => :SPECIAL_ATTACK, :FIRE => :SPECIAL_ATTACK,   :PSYCHIC => :SPECIAL_ATTACK, :GHOST => :SPECIAL_ATTACK,
      :FIGHTING => :ATTACK,        :DARK => :ATTACK,            :DRAGON => :ATTACK,
      :GROUND => :DEFENSE,         :ICE => :DEFENSE,            :ROCK => :DEFENSE,           :STEEL => :DEFENSE,
      :WATER => :SPECIAL_DEFENSE,  :POISON => :SPECIAL_DEFENSE, :GRASS => :SPECIAL_DEFENSE,  :FAIRY => :SPECIAL_DEFENSE
    }.freeze
    ARCEUS_FORCED_CAP      = { :CASUAL => 2, :default => 3 }
    # When nobody is asked (War, Judgment) every lock is forced every bar, so the forced stages harden Arceus (Defense,
    # Sp. Def) without sharpening it, on every difficulty (2026-11-26: with offence too the harness lost one Pokemon a
    # bar and never won, at any bar HP).
    ARCEUS_UNASKED_FORCED_STAGES = [:DEFENSE, :SPECIAL_DEFENSE].freeze

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

    # War: the shard eats the types; Judgment: no Warden releases anything. Nobody is asked, every lock is forced.
    ARCEUS_NOBODY_ASKED = [:ARCEUS_WAR, :ARCEUS_JUDGMENT].freeze
    ARCEUS_GILDED_REFILLS = 3
    # Gilded's last bar is one bar's HP cut into four (2026-11-26): it starts at 0.4 of a bar and refills 3x at 0.2, so
    # the Gilded Chain costs what the last bar costs on Bound (with full refills a prepared team never reached it).
    # Bar HP and stats by difficulty (2026-11-26, Reuben: "use best judgement" -> a team built for the fight must be able
    # to win; BALANCE.md section 9b has the before / after). Was Standard x1.0 HP, x1.25 Atk / Def / SpA / SpD, x1.1 Spe;
    # Hard x1.25 HP, x1.3, x1.15 Spe: Arceus one-shot every prepared Pokemon after its turn-1 Calm Mind, 0% at 3 or 6 bars.
    ARCEUS_MULTS = {
      :CASUAL   => { :HP => 0.5, :ATTACK => 0.6, :SPECIAL_ATTACK => 0.6 },
      :STANDARD => { :HP => 0.32, :ATTACK => 0.8, :DEFENSE => 1.0, :SPECIAL_ATTACK => 0.8, :SPECIAL_DEFENSE => 1.0, :SPEED => 1.1 },
      :HARD     => { :HP => 0.32, :ATTACK => 0.8, :DEFENSE => 1.0, :SPECIAL_ATTACK => 0.8, :SPECIAL_DEFENSE => 1.0, :SPEED => 1.15 }
    }.freeze
    # The variants' structure differs (Gilded's four-piece last bar, Judgment's partner, War's forced locks), so each
    # scales its bar HP to land near Bound's difficulty (harness-tuned 2026-11-26; Casual only where it fell short).
    ARCEUS_VARIANT_HP = {
      :ARCEUS_GILDED        => { :CASUAL => 1.0, :STANDARD => 0.8,  :HARD => 0.8 },
      :ARCEUS_JUDGMENT      => { :CASUAL => 1.0, :STANDARD => 1.45, :HARD => 1.3 },
      :ARCEUS_WAR           => { :CASUAL => 0.4, :STANDARD => 0.4,  :HARD => 0.4 },
      :ARCEUS_MISCALIBRATED => { :CASUAL => 1.0, :STANDARD => 1.15, :HARD => 1.15 }
    }.freeze

    def self.arceus_stat_mults
      m = (resolve(ARCEUS_MULTS) || {}).dup
      f = resolve(ARCEUS_VARIANT_HP[arceus_variant[:id]])
      m[:HP] = ((m[:HP] || 1.0) * f).round(3) if f.is_a?(Numeric) && f != 1.0
      return m
    end

    ARCEUS_GILDED_LAST_BAR = 0.4
    ARCEUS_GILDED_REFILL   = 0.2

    def self.arceus_nobody_asked?
      return ARCEUS_NOBODY_ASKED.include?(arceus_variant[:id])
    end

    def self.arceus_gilded?
      return arceus_variant[:id] == :ARCEUS_GILDED
    end

    # Gym numbers of the given bar whose lock is forced.
    def self.arceus_forced_locks(bar)
      gyms = arceus_bar_gyms[bar - 1]
      return [] if !gyms
      return gyms.dup if arceus_nobody_asked?
      return gyms.reject { |n| arceus_consents?(n) }
    end

    # A Gilded refill: the Casual bar's HP, as a fraction of this difficulty's bar. Casual only (eased 2026-11-26:
    # 13% for the harness with full refills): half its own bar.
    def self.arceus_gilded_refill
      return ARCEUS_GILDED_REFILL
    end

    # A bar has just been broken (or, final = true, the last one fell): its refused locks tear free.
    def self.arceus_end_bar(battle, bar, final = false)
      gyms   = arceus_bar_gyms[bar - 1]
      return if !gyms
      forced = battle.instance_variable_get(:@prismfall_arceus_forced_list) || []
      EventHandlers.trigger(:prismfall_arceus_locks_broken, battle, bar, gyms, forced, final)
    end

    # A bar starts: forced locks (+1 to every stat stage per refusing Warden, for this bar only).
    # { stat => stages } the bar's forced locks give Arceus.
    def self.arceus_forced_boosts(forced)
      return {} if forced.empty?
      if arceus_nobody_asked? || difficulty == :CASUAL || ARCEUS_REFUSAL_SCOPE != :plate
        stats = (arceus_nobody_asked?) ? ARCEUS_UNASKED_FORCED_STAGES : (resolve(ARCEUS_FORCED_STAGES) || ARCEUS_STAT_STAGES)
        n = [forced.length, resolve(ARCEUS_FORCED_CAP) || 3].min
        n = [n, resolve(ARCEUS_WAR_STAGE_CAP) || 2].min if arceus_nobody_asked?
        return stats.map { |s| [s, n] }.to_h
      end
      ret = Hash.new(0)
      forced.each do |g|
        gym = Prismfall.gym(g)
        ret[ARCEUS_PLATE_STATS[gym[:type]] || :SPECIAL_DEFENSE] += 1 if gym
      end
      return ret
    end

    # A bar starts: the last bar's forced stages are spent, the Wardens kneel (Core 033 / Bosses 116), then this bar's
    # refused locks hold and their stages are added (for this bar only).
    def self.arceus_start_bar(battle, b, st)
      bar    = st.phase
      forced = arceus_forced_locks(bar)
      (battle.instance_variable_get(:@prismfall_arceus_boosts) || {}).each do |s, k|
        b.stages[s] = [b.stages[s] - k, 0].max if b.stages[s] > 0
      end
      boosts = arceus_forced_boosts(forced)
      battle.instance_variable_set(:@prismfall_arceus_boosts, boosts)
      battle.instance_variable_set(:@prismfall_arceus_forced, boosts.values.max.to_i)
      battle.instance_variable_set(:@prismfall_arceus_forced_list, forced.dup)
      EventHandlers.trigger(:prismfall_arceus_locks, battle, bar, arceus_bar_gyms[bar - 1] || [], forced)
      return if boosts.empty?
      n = forced.length
      battle.pbDisplay(text((n == 1) ? "One lock holds fast!" : "{2} locks hold fast!", b.pbThis, n))
      boosts.each { |s, k| b.stages[s] = [b.stages[s] + k, 6].min }
      battle.pbCommonAnimation("StatUp", b) rescue nil
      if boosts.length == ARCEUS_STAT_STAGES.length
        battle.pbDisplay(text("{1}'s power surged!", b.pbThis))
      elsif boosts.keys.all? { |s| [:DEFENSE, :SPECIAL_DEFENSE].include?(s) } && boosts.length == 2
        battle.pbDisplay(text("{1}'s defenses hardened!", b.pbThis))
      else
        boosts.each do |s, k|
          battle.pbDisplay(text((k > 1) ? "{1}'s {2} rose sharply!" : "{1}'s {2} rose!", b.pbThis, GameData::Stat.get(s).name))
        end
      end
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
  # BALANCE.md section 7: at every break the Plates skip to the new bar's field best against the player's active
  # Pokemon (every difficulty; bar 1 still opens on Gym 1's field), and each turn is telegraphed 2 rounds ahead on
  # Casual, 1 on Standard and Hard (2026-11-27).
  :prism_best_field  => true,
  :prism_telegraph   => { :CASUAL => 2, :default => 1 },
  :partner           => proc {
    v = Prismfall::Bosses.arceus_variant
    (v[:player_side].to_i >= 2) ? [:PARTNER_GIRATINA, "Depths", 0] : nil
  },
  :move_limits       => { :STANDARD => { :RECOVER => 2 }, :default => nil },   # Casual has no Recover; Hard has no limit
  :stat_mults        => proc { Prismfall::Bosses.arceus_stat_mults },
  :field             => :PRISM_ARENA,
  :catch             => false,
  :status_immunity   => true,
  :immunity_last_bar => true,
  :intro             => ["The eighteen Plates blaze as one... Arceus descends upon Crownhaven!"],
  :break_message     => "The Plates around {1} crack and reform!",
  :on_break          => [
    # The bar just broken: its refused locks tear free (Bosses 116), before the Plates turn to the next bar.
    { :proc => proc { |battle, _b, st| Prismfall::Bosses.arceus_end_bar(battle, st.breaks_done) } },
    # Gilded: the last bar starts at 0.4 (then refills 3x at 0.2: on_defeat below).
    { :condition => proc { |_battle, _b, st| st.last_bar? && Prismfall::Bosses.arceus_gilded? },
      :refill => Prismfall::Bosses::ARCEUS_GILDED_LAST_BAR },
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
  :on_defeat         => [
    # Gilded: the last bar can't be broken. The Engine binds it shut again, three times...
    { :condition => proc { |_battle, _b, st|
        Prismfall::Bosses.arceus_gilded? && st.revives < Prismfall::Bosses::ARCEUS_GILDED_REFILLS },
      :messages  => ["The last lock cracks... and gold pours into the break!",
                     "The Engine binds the chain shut again!"],
      :reset_stats => :negative, :cure_status => true,
      :revive    => proc { |_battle, _b, _st| Prismfall::Bosses.arceus_gilded_refill }, :carry => true },
    # ...and then the Gilded Chain closes (END_GILDED_CHAIN).
    { :condition => proc { |_battle, _b, st|
        Prismfall::Bosses.arceus_gilded? && st.revives >= Prismfall::Bosses::ARCEUS_GILDED_REFILLS },
      :messages  => ["The last lock will not break.",
                     "Gold runs down every chain at once. The Gilded Chain closes around {1}.",
                     "Inside the Ring, Valen kneels, crystal to the jaw, as the chain closes."],
      :end_battle => 1, :result => :gilded_chain },
    # Everywhere else the last bar's fall frees the god (it never faints).
    { :condition => proc { |_battle, _b, _st| !Prismfall::Bosses.arceus_gilded? },
      :proc      => proc { |battle, b, st|
        Prismfall::Bosses.arceus_end_bar(battle, st.bars, true)
        battle.pbDisplay(Prismfall::Bosses.text("The last chain falls away from {1}.", b.pbThis))
      },
      :end_battle => 1, :result => :freed }
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
