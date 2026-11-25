#===============================================================================
# Silvally "NULL" (Project NULL) - the Hijack (Festival stage :HIJACK, Chapter 21
# "Sovereign"; story/40_SCRIPT_CH21.md "The hijacker", story/08_ACT_V.md "Voss",
# design/NARRATIVE_KEYS.md section 8, design/BALANCE.md section 6). A trainer
# boss on the hijacker's ace: Voss (MERIDIAN_VOSS v0 / 100 / 200) or, when Voss
# is discredited, Quent with Voss's team (MERIDIAN_QUENT v99 / 199 / 299).
#   * Three bars on every difficulty (the script's beat sits "between bars 2
#     and 3"). Standard and Hard get no stat multipliers; Casual's bars are
#     x0.55 HP each.
#   * "Its type follows the active field": whenever :PRISM_ARENA turns, NULL
#     swaps to that Plate's type Memory (item + form; RKS System and
#     Multi-Attack follow), "NULL re-indexes to the X Memory!". The Grand
#     Stage's turn (Normal) = no Memory. It keeps its Steel Memory through the
#     arena's opening rounds. (:follow_prism with :items.)
#   * The conduit bar (bar 3). If KESTREL_FALLEN, Kestrel is harnessed into the
#     Engine as its conduit, and when bar 2 breaks the player answers
#     :ch21_reach_kestrel inside the battle (Reach only with CAN_REACH_KESTREL):
#       :reach / :burn -> the conduit is broken: no bar-3 regeneration
#       :let_go        -> KESTREL_LOST; the Engine fires through him, and NULL
#                         regenerates every round of bar 3 (Casual 1/16,
#                         Standard 1/8, Hard 1/6 of its max HP)
#     If the choice is already made (a retry after a loss), it isn't asked again.
#     If Kestrel isn't fallen there is no conduit and no regeneration.
#   * VOSS_FEIGNED: NULL enters at -1 to every stat for 3 rounds ("You were
#     close. You let me get close.").
#   * Voss's two mid-battle lines play at the first two breaks (Voss only).
# Bosses.last_result[:result]: :conduit_broken, :conduit_fired or nil.
# Harness: tools/harness/winrates_r4.rb cells VOSS, QH and VOSSC (conduit live).
#===============================================================================
module Prismfall
  module Bosses
    NULL_MEMORIES = {
      :FIGHTING => :FIGHTINGMEMORY, :FLYING => :FLYINGMEMORY, :POISON => :POISONMEMORY, :GROUND => :GROUNDMEMORY,
      :ROCK => :ROCKMEMORY, :BUG => :BUGMEMORY, :GHOST => :GHOSTMEMORY, :STEEL => :STEELMEMORY, :FIRE => :FIREMEMORY,
      :WATER => :WATERMEMORY, :GRASS => :GRASSMEMORY, :ELECTRIC => :ELECTRICMEMORY, :PSYCHIC => :PSYCHICMEMORY,
      :ICE => :ICEMEMORY, :DRAGON => :DRAGONMEMORY, :DARK => :DARKMEMORY, :FAIRY => :FAIRYMEMORY,
      :NORMAL => nil, :default => nil
    }.freeze
    NULL_REGEN        = { :CASUAL => 1 / 16.0, :STANDARD => 1 / 8.0, :HARD => 1 / 6.0 }
    NULL_BOSSES       = [:VOSS_SILVALLY_NULL, :QUENT_SILVALLY_NULL].freeze
    NULL_FEIGN_ROUNDS = 3
    NULL_STAT_STAGES  = [:ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED].freeze
    HIJACKER_NAMES    = { :MERIDIAN_VOSS => "Voss", :MERIDIAN_QUENT => "Quent" }.freeze

    def self.narrative_flag?(name)
      return false if !defined?(Prismfall::Narrative)
      return (Prismfall::Narrative.flag(name) ? true : false) rescue false
    end

    def self.narrative_choice(key)
      return nil if !defined?(Prismfall::Choices)
      return (Prismfall::Choices.get(key) rescue nil)
    end

    # Per-battle scratch for the hijack: { :conduit => live?, :feigned => rounds left }.
    def self.null_state(battle)
      h = battle.instance_variable_get(:@prismfall_null)
      battle.instance_variable_set(:@prismfall_null, h = { :conduit => false, :feigned => 0 }) if !h
      return h
    end

    def self.hijacker_name(battle)
      t = (battle.opponent || []).find { |tr| tr && HIJACKER_NAMES[tr.trainer_type] }
      return (t) ? HIJACKER_NAMES[t.trainer_type] : "the hijacker"
    end

    # Asks :ch21_reach_kestrel in the battle (the scene's command window); returns the value.
    def self.ask_reach_kestrel(battle)
      cmds = []
      vals = []
      if narrative_flag?(:CAN_REACH_KESTREL)
        cmds.push(_INTL("Reach him."))
        vals.push(:reach)
      end
      cmds.push(_INTL("Burn it off."))
      vals.push(:burn)
      cmds.push(_INTL("Let go."))
      vals.push(:let_go)
      idx = battle.pbShowCommands(_INTL("Kestrel..."), cmds, -1)
      val = vals[idx.to_i] || vals[0]
      Prismfall::Choices.make(:ch21_reach_kestrel, val, false) if defined?(Prismfall::Choices)
      return val
    end

    # Bar 2 has just broken: the floor opens behind the hijacker.
    NULL_CONDUIT_PROC = proc { |battle, b, st|
      bs = Prismfall::Bosses
      next if !bs.narrative_flag?(:KESTREL_FALLEN)      # he fought beside you: the Engine has no conduit
      info = bs.null_state(battle)
      who  = bs.hijacker_name(battle)
      say  = proc { |msg, *args| battle.pbDisplay(bs.text(msg, *args)) }
      say.call("The arena floor opens behind {1}. Harnessed into the Engine under it, Gauntlet fused to the cradle's wrist and burning: Kestrel.", who)
      say.call("His eyes are open. He isn't in them.")
      choice = bs.narrative_choice(:ch21_reach_kestrel)
      choice = bs.ask_reach_kestrel(battle) if choice.nil?
      case choice
      when :reach
        if [:keep, :send].include?(bs.narrative_choice(:ch12_letter))
          say.call("\"Keep them small and safe and far. I'll carry the name.\"")
          say.call("\"She carried yours. Put it down.\"")
        else
          say.call("You hold up her ring. You say his name. Just his name.")
        end
        say.call("He comes back. You see it happen: he's in his eyes again. The Gauntlet goes dark. He tears himself loose.")
      when :burn
        say.call("Your shard tears the Gauntlet off him by force. He screams. He lives.")
      else
        say.call("You turn back to {1}. Behind you the Engine fires through its conduit, and the conduit burns out.", who)
      end
      if choice == :let_go
        info[:conduit] = true
        st.result = :conduit_fired
        say.call("The Engine's fire pours into {1}!", b.pbThis)
      else
        info[:conduit] = false
        st.result = :conduit_broken
        say.call("The Engine has lost its conduit! {1} is cut off from it!", b.pbThis)
      end
    }

    # After every round NULL spends on the field.
    NULL_END_OF_ROUND = proc { |battle, b, st|
      bs   = Prismfall::Bosses
      info = bs.null_state(battle)
      if info[:feigned] > 0
        info[:feigned] -= 1
        if info[:feigned] == 0
          NULL_STAT_STAGES.each { |s| b.stages[s] += 1 if b.stages[s] < 6 }
          battle.pbDisplay(bs.text("{1} shook off the feint! Its stats returned to normal!", b.pbThis))
        end
      end
      if info[:conduit] && st.last_bar? && !b.fainted? && b.hp < b.totalhp && b.canHeal?
        frac = bs.resolve(NULL_REGEN) || (1 / 8.0)
        battle.pbDisplay(bs.text("The Engine pours through its conduit!"))
        b.pbRecoverHP([(b.totalhp * frac).round, 1].max)
        battle.pbDisplay(bs.text("{1} regenerated!", b.pbThis))
      end
    }

    NULL_FORM_MESSAGE = proc { |type|
      (type == :NORMAL) ? "{1} ejects its Memory and reverts to the Normal type!" : "{1} re-indexes to the {2} Memory!"
    }

    def self.null_boss(voss)
      breaks = { 2 => [{ :proc => NULL_CONDUIT_PROC }] }
      if voss
        breaks[1] = [{ :messages => ["Voss: \"Your mother wilted for ten years because a god dropped its furniture on her.\""] }]
        breaks[2].unshift({ :messages => ["Voss: \"I'm not your enemy. I'm the only adult in this arena who'll say the true thing out loud: we don't need it.\""] })
      end
      return {
        :bars         => 3,
        :stat_mults   => { :CASUAL => { :HP => 0.55 } },
        :catch        => false,
        :intro        => ["Project NULL lowers its head. The Memory disc behind its crest spins up."],
        :on_break     => { :cure_status => true, :reset_stats => :negative },
        :breaks       => breaks,
        :follow_prism => { :form => true, :form_message => NULL_FORM_MESSAGE, :items => NULL_MEMORIES },
        :end_of_round => NULL_END_OF_ROUND,
        :description  => "Ch21 the Hijack: #{voss ? "Voss's" : "Quent's (Voss's team)"} Silvally \"NULL\" (trainer boss, 3 bars); " \
                         "type follows the Prism Arena; bar 3 regenerates while Fallen Kestrel is the Engine's conduit"
      }
    end
  end
end

Prismfall::Bosses.register(:VOSS_SILVALLY_NULL, Prismfall::Bosses.null_boss(true))
Prismfall::Bosses.register(:QUENT_SILVALLY_NULL, Prismfall::Bosses.null_boss(false))

Prismfall::Bosses.register_trainer_boss(:VOSS_HIJACK_NULL, {
  :trainer_type => :MERIDIAN_VOSS, :name => "Aurelian",
  :versions     => [0, 100, 200],
  :species      => :SILVALLY,
  :boss         => :VOSS_SILVALLY_NULL
})

Prismfall::Bosses.register_trainer_boss(:QUENT_HIJACK_NULL, {
  :trainer_type => :MERIDIAN_QUENT, :name => "Percival",
  :versions     => [99, 199, 299],     # the Hijack only: never his Ch8 / Ch17 / tag-battle teams
  :species      => :SILVALLY,
  :boss         => :QUENT_SILVALLY_NULL
})

# NULL enters: VOSS_FEIGNED's opening penalty (once), and re-index to the Plate that is already ascendant.
EventHandlers.add(:prismfall_boss_entered, :prismfall_null_enters,
  proc { |battle, battler, id|
    bs = Prismfall::Bosses
    next if !bs::NULL_BOSSES.include?(id)
    info = bs.null_state(battle)
    if !info[:entered]
      info[:entered] = true
      if id == :VOSS_SILVALLY_NULL && bs.narrative_flag?(:VOSS_FEIGNED)     # his line, his feint: not Quent's
        battle.pbDisplay(bs.text("Voss: \"You were close. You let me get close.\""))
        bs::NULL_STAT_STAGES.each { |s| battler.stages[s] -= 1 if battler.stages[s] > -6 }
        battle.pbCommonAnimation("StatDown", battler) rescue nil
        battle.pbDisplay(bs.text("{1} hesitates! All its stats fell!", battler.pbThis))
        info[:feigned] = bs::NULL_FEIGN_ROUNDS
      end
    end
    bs.sync_prism_followers(battle)
  }
)
