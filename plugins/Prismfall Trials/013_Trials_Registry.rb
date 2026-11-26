#===============================================================================
# Prismfall Trials - 013 Larch's Postgame Registry: the :POSTGAME category's tiers,
# clear switches and board
#-------------------------------------------------------------------------------
# story/41_SCRIPT_POSTGAME.md P1 "Larch's Postgame Registry" (and P6.1, the black card);
# gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta
# Part B.3 (the tiers and the switch allocation, design/FLAGS.md S270-S294).
# The cards are ordinary Trials quests on the :POSTGAME board (115_Quests_Postgame.rb);
# this file knows which tier each is in, which switch its clear writes, and when a tier opens.
#
#   Script: pf_registry_larch     Larch in the Spire lobby (493). Before S160: false (her map lines
#                                 play instead). First post-game talk: the P1 scene (S270 on, V143 = 1).
#                                 After that: the black card once it appears (S267; S269 on, V143 = 5),
#                                 a finished roamers card, then the board.
#   Script: pf_registry_board     the board itself (the easel event): Tier 1 cards first, then Tier 2
#                                 and Tier 3, each sealed until it opens, with how to open it.
#   pf_registry_open?             S270          pf_registry_clears(1)   cleared cards in a tier
#   pf_registry_tier_open?(2)     S279 / S285   pf_registry_roamer(:HEATRAN)  one Warden's rumour (T1-8)
#
# Tiers (the script): Tier 1 opens at once. Tier 2 opens at TIER2_NEEDS Tier 1 clears plus S268 (the
# Distortion Core). Tier 3 opens at TIER3_KEYSTONES Tier 2 clears plus S267 (the Gauntlet). Endings
# (NARRATIVE_KEYS 6.5): Hollow Spring and Concord Dawn get Tier 1 only; the Ruin endings get every
# tier but the Convergence (Arceus doesn't return); the Gilded Chain has no post-game at all.
# A card's clear switch is written when its quest completes; S279 / S285 are written here, never by events.
#===============================================================================
module Prismfall
  module Trials
    module Registry
      SWITCH_POSTGAME     = 160
      SWITCH_RUIN_WORLD   = 265
      SWITCH_GAUNTLET     = 267
      SWITCH_DISTORTION   = 268
      SWITCH_CONCORD_ZERO = 269
      SWITCH_OPEN         = 270
      SWITCH_TIER         = { 2 => 279, 3 => 285 }
      VAR_STEP            = 143      # V143 PG_STEP
      TIER2_NEEDS         = 4        # Tier 1 clears
      TIER3_KEYSTONES     = 3        # Tier 2 clears (the "keystones")
      ROAMERS_NEEDED      = 8        # rumours settled to clear T1-8 (one per kingdom's worth)
      PARTIAL_ENDINGS     = [:END_HOLLOW_SPRING, :END_CONCORD_DAWN]
      RUIN_ENDINGS        = [:END_UNMAKING, :END_REFLECTION]

      # quest id => { :no, :tier, :switch (or :switches) }. Order = the order on the board.
      CARDS = {
        :PG_MELOETTA     => { :no => "T1-1", :tier => 1, :switch => 271 },
        :PG_OGERPON      => { :no => "T1-2", :tier => 1, :switch => 272 },
        :PG_PECHARUNT    => { :no => "T1-3", :tier => 1, :switch => 273 },
        :PG_REGIS        => { :no => "T1-4", :tier => 1, :switch => 274 },
        :PG_LAKES        => { :no => "T1-5", :tier => 1, :switch => 275 },
        :PG_TYPENULL     => { :no => "T1-6", :tier => 1, :switch => 276 },
        :PG_KUBFU        => { :no => "T1-7", :tier => 1, :switch => 277 },
        :PG_ROAMERS      => { :no => "T1-8", :tier => 1, :switch => 278 },
        :PG_UBS          => { :no => "T2-1", :tier => 2, :switch => 280 },
        :PG_TAPUS        => { :no => "T2-2", :tier => 2, :switch => 281 },
        :PG_RUIN_QUARTET => { :no => "T2-3", :tier => 2, :switch => 282 },
        :PG_PARADOX      => { :no => "T2-4", :tier => 2, :switch => 283 },
        :PG_CALYREX      => { :no => "T2-5", :tier => 2, :switch => 284 },
        :PG_WEATHER_TRIO => { :no => "T3-1", :tier => 3, :switch => 286 },
        :PG_TAO_TRIO     => { :no => "T3-2", :tier => 3, :switch => 287 },
        :PG_GIRATINA     => { :no => "T3-3", :tier => 3, :switch => 288 },
        :PG_ZYGARDE      => { :no => "T3-4", :tier => 3, :switch => 289 },
        :PG_BOX_LEGENDS  => { :no => "T3-5", :tier => 3, :switches => [290, 291, 292] },
        :PG_ARCEUS       => { :no => "T3-6", :tier => 3, :switch => 294 }
      }.freeze

      TIER_NAMES = { 1 => "Regional Trials and Mythical Encores", 2 => "Bleed Rifts and Ruin Anomalies",
                     3 => "Apex Rematches and the Convergence" }.freeze

      class << self
        def sw(n);        return ($game_switches) ? ($game_switches[n] ? true : false) : false; end
        def set_sw(n, v = true)
          return if !$game_switches || $game_switches[n] == v
          $game_switches[n] = v
          $game_map.need_refresh = true if $game_map && $game_map.respond_to?(:need_refresh=)
        end

        def postgame?
          return true if sw(SWITCH_POSTGAME)
          return (Prismfall.respond_to?(:postgame_unlocked?) && Prismfall.postgame_unlocked?) ? true : false
        end

        def open?;  return postgame? && sw(SWITCH_OPEN); end

        # :none / :partial (Tier 1 only) / :ruin (no Convergence) / :full
        def scope
          return :none if !postgame?
          id = (Prismfall.state.narrative[:postgame] rescue nil)
          return :partial if PARTIAL_ENDINGS.include?(id)
          return :ruin if RUIN_ENDINGS.include?(id) || sw(SWITCH_RUIN_WORLD)
          return :full
        end

        def tr; return Prismfall::Trials; end

        def cards(tier = nil)
          ids = CARDS.keys.select { |id| tr.exists?(id) }
          return (tier) ? ids.select { |id| CARDS[id][:tier] == tier } : ids
        end

        def card_switches(id)
          c = CARDS[id]
          return [] if !c
          return c[:switches] || [c[:switch]]
        end

        def cleared?(id)
          sws = card_switches(id)
          return !sws.empty? && sws.all? { |n| sw(n) }
        end

        def clears(tier)
          return CARDS.keys.count { |id| CARDS[id][:tier] == tier && cleared?(id) }
        end

        def tier_open?(tier)
          return open? if tier == 1
          return open? && sw(SWITCH_TIER[tier])
        end

        def tier_hint(tier)
          case tier
          when 2
            return _INTL("Larch hasn't pinned these yet. Some endings leave the old ones be.") if scope == :partial
            return _INTL("Sealed: {1} of {2} Tier 1 cards, and the Distortion Core must be open.", [clears(1), TIER2_NEEDS].min, TIER2_NEEDS)
          when 3
            return _INTL("Larch hasn't pinned these yet. Some endings leave the old ones be.") if scope == :partial
            return _INTL("Sealed: {1} of {2} Tier 2 cards, and the Warden's Gauntlet must be open.", [clears(2), TIER3_KEYSTONES].min, TIER3_KEYSTONES)
          end
          return ""
        end

        # Writes S279 / S285 when their conditions hold. Returns the tiers that just opened.
        def refresh_tiers(announce = true)
          opened = []
          return opened if !open? || ![:full, :ruin].include?(scope)
          if !sw(SWITCH_TIER[2]) && clears(1) >= TIER2_NEEDS && sw(SWITCH_DISTORTION)
            set_sw(SWITCH_TIER[2])
            opened.push(2)
          end
          if sw(SWITCH_TIER[2]) && !sw(SWITCH_TIER[3]) && clears(2) >= TIER3_KEYSTONES && sw(SWITCH_GAUNTLET)
            set_sw(SWITCH_TIER[3])
            opened.push(3)
          end
          if announce
            opened.each do |t|
              pbMessage("\\se[GUI save choice]" + _INTL("REGISTRY: new cards are pinned to Larch's board. Tier {1}: {2}.", t, _INTL(TIER_NAMES[t])))
            end
          end
          return opened
        end

        # A card's quest finished: write its clear switch(es) and see whether a tier opens.
        def on_quest_done(id)
          return if !CARDS[id]
          card_switches(id).each { |n| set_sw(n) }
          refresh_tiers
        end

        #-----------------------------------------------------------------------
        # T1-8: each Warden's rumour is its own encounter; the card clears at ROAMERS_NEEDED settled.
        #-----------------------------------------------------------------------
        def roamer_id(species); return :"PG_ROAM_#{species}"; end

        def roamers_settled
          return Prismfall::EventMons.ids.count do |id|
            next false if !id.to_s.start_with?("PG_ROAM_")
            [:caught, :joined, :won].include?(Prismfall::EventMons.status(id))
          end
        end

        # Map events: Script: pf_registry_roamer(:HEATRAN). Returns the battle result, or nil if it isn't due.
        def roamer(species)
          id = roamer_id(species)
          return nil if !Prismfall::EventMons.exists?(id) || !tr.active?(:PG_ROAMERS)
          return nil if [:caught, :joined].include?(Prismfall::EventMons.status(id))
          res = Prismfall::EventMons.battle(id)
          n = roamers_settled
          if tr.step(:PG_ROAMERS) == :rumours && n >= ROAMERS_NEEDED
            tr.set_step(:PG_ROAMERS, :report)
          end
          return res
        end

        #-----------------------------------------------------------------------
        # Larch
        #-----------------------------------------------------------------------
        def larch_say(expr, text)
          tr.say(:LARCH, expr, text)
        end

        # P1: "There you are. Sit. No, don't sit, look."
        def open_scene
          pbMessage(_INTL("The Concordance Spire's lobby, finished at last. A board on an easel, covered in pinned notes: eighteen columns, one per kingdom."))
          larch_say(:happy, "There you are. Sit. No, don't sit, look. Every Warden sent me something. Rumours. Sightings. Things that woke up when the sky closed and didn't go back to sleep.")
          larch_say(:neutral, "The old ones. The legends. They're not bound any more. They're not anyone's. Some of them want to be found. Some want to be fought. One or two want to be left alone, and I've marked those in red. Respect the red.")
          larch_say(:smug, "I'm calling it the Registry. Dorian wanted \"The Grand Tour\". We compromised: I won.")
          set_sw(SWITCH_OPEN)
          $game_variables[VAR_STEP] = 1 if $game_variables && $game_variables[VAR_STEP].to_i < 1
          refresh_tiers
          return true
        end

        def black_card_due?
          return open? && sw(SWITCH_GAUNTLET) && !sw(SWITCH_CONCORD_ZERO) && scope != :partial
        end

        # P6.1: the black card.
        def black_card_scene
          pbMessage(_INTL("A black card on the Registry board. No Warden's name on it. Larch takes it down and turns it over."))
          pbMessage(_INTL("On the back, in Quent's neat hand: \"Your readings were the most beautiful thing I've ever seen. I kept them. — P.Q.\""))
          larch_say(:angry, "He kept them.")
          set_sw(SWITCH_CONCORD_ZERO)
          $game_variables[VAR_STEP] = 5 if $game_variables
          return true
        end

        # Larch herself. false = it isn't the post-game: the map's own Larch lines play.
        def larch
          return false if !postgame?
          return open_scene && board if !sw(SWITCH_OPEN)
          if tr.exists?(:PG_ROAMERS) && tr.at?(:PG_ROAMERS, :report)
            larch_say(:happy, "That's the column filled in. I'll stop pretending I'm not impressed.")
            tr.complete(:PG_ROAMERS)
          end
          black_card_scene if black_card_due?
          return board
        end

        #-----------------------------------------------------------------------
        # The board
        #-----------------------------------------------------------------------
        def card_label(id)
          q = tr.get(id)
          c = CARDS[id]
          label = "#{c[:no]}  #{_INTL(q[:title])}"
          if cleared?(id) || tr.done?(id) then label += _INTL(" (cleared)")
          elsif tr.active?(id) then label += _INTL(" (taken)")
          elsif q[:rec_level] then label += _INTL(" | Rec. Lv. {1}", q[:rec_level])
          end
          return label
        end

        # [[label, quest id or nil], ...]: Tier 1 cards first, then Tier 2, then Tier 3.
        def board_rows
          rows = []
          [1, 2, 3].each do |tier|
            ids = cards(tier)
            if !tier_open?(tier)
              rows.push([_INTL("Tier {1}: {2}", tier, tier_hint(tier)), nil])
              next
            end
            ids.each do |id|
              q = tr.get(id)
              next if q[:hidden]
              st = tr.state(id)
              next if st == :expired
              next if id == :PG_ARCEUS && scope == :ruin        # Arceus doesn't return on the Ruin Route
              rows.push([card_label(id), id])
            end
          end
          return rows
        end

        def header
          return _INTL("The Registry. Tier 1: {1}/{2}   Tier 2: {3}/{4}   Tier 3: {5}/{6}",
                       clears(1), cards(1).length, clears(2), cards(2).length, clears(3), cards(3).length)
        end

        def show_card(id)
          q = tr.get(id)
          if cleared?(id) || (tr.done?(id) && !q[:repeatable])
            pbMessage(_INTL("\"{1}\". The card is pinned face down, with a small star on it.", _INTL(q[:title])))
            return
          end
          if tr.active?(id)
            pbMessage(_INTL("\"{1}\" - {2}", _INTL(q[:title]), tr.step_text(id, tr.step(id)) || _INTL(q[:summary].to_s)))
            return
          end
          where = (q[:where]) ? _INTL("\nAsk {1} at {2}.", _INTL(q[:giver].to_s), _INTL(q[:where])) : ""
          pbMessage(_INTL("{1}{2}", _INTL(q[:summary].to_s), where))
          if q[:stub]
            pbMessage(_INTL("Larch has written \"NOT YET\" across the corner. She's still tracing this one."))
            return
          end
          if tr.state(id) == :locked
            pbMessage(_INTL("The pin won't come out. Something has to happen first."))
            return
          end
          return if tr.pick(_INTL("Take this card?"), [_INTL("Yes"), _INTL("No")], 1) != 0
          t = TRIALS[:POSTGAME]
          pbMessage(_INTL(t[:accept])) if t && t[:accept]
          tr.start(id)
          tr.set_flag(id, :from_board, true) if q[:scenes] && q[:scenes][:offer]
        end

        def board
          return false if !postgame?
          if !sw(SWITCH_OPEN)
            pbMessage(_INTL("An easel, a board, and a great many pins. Larch isn't done arranging it."))
            return false
          end
          refresh_tiers
          60.times do      # bounded, like the Trial boards: a headless run can't spin forever
            rows = board_rows
            cmds = rows.map { |r| r[0] } + [_INTL("Leave")]
            choice = tr.pick(header, cmds, cmds.length - 1)
            break if choice.nil? || choice < 0 || choice >= rows.length
            label, id = rows[choice]
            if id.nil?
              pbMessage(label)
              next
            end
            show_card(id)
          end
          return true
        end
      end
    end
  end
end

EventHandlers.add(:prismfall_quest_changed, :prismfall_registry_clears,
  proc { |id, change|
    Prismfall::Trials::Registry.on_quest_done(id) if change == :done
  }
)

def pf_registry_larch;             return Prismfall::Trials::Registry.larch;             end
def pf_registry_board;             return Prismfall::Trials::Registry.board;             end
def pf_registry_open?;             return Prismfall::Trials::Registry.open?;             end
def pf_registry_clears(tier);      return Prismfall::Trials::Registry.clears(tier);      end
def pf_registry_tier_open?(tier);  return Prismfall::Trials::Registry.tier_open?(tier);  end
def pf_registry_roamer(species);   return Prismfall::Trials::Registry.roamer(species);   end
