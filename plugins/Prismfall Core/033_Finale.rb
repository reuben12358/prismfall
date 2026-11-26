#===============================================================================
# Prismfall Core - 033 Chapter 21 "Sovereign": the finale's rules and records
#-------------------------------------------------------------------------------
# story/40_SCRIPT_CH21.md (the Hijack, his hand, the allies' montage and Larch's
# eleven lamps, the tag battle, the eighteen locks, the endings table) and
# story/11_FINALE_LINES.md (the 18 release and 18 refusal lines, the Last Shatter
# slides). Data and rules live here; the pictures are Prismfall Cutscenes
# 019_Scenes_Finale.rb (pfm_cutscene ids) and the pylons mapgen/ruby/018_Crownhaven.rb.
#
# THE HIJACK
#   Prismfall::Finale.hijacker        :VOSS, :QUENT (VOSS_DISCREDITED) or :AURELIUS (Ruin Route)
#   Prismfall::Finale.his_hand        the "> Take it. / > Refuse." prompt and what follows:
#       :concord   (VOSS_ACCEPTED and taken: :ch21_hand = :take, END_CONCORD_DAWN has been triggered)
#       :refused   (:ch21_hand = :refuse when VOSS_ACCEPTED; plain "Don't." otherwise)
#       :game_over (taken without VOSS_ACCEPTED: GO_HIS_HAND)   :none (it isn't Voss in the harness)
#   Prismfall::Finale.refresh_weakpoints   V117 ENGINE_WEAKPOINTS (0-6), the story mirror
# THE ALLIES MOVE
#   Prismfall::Finale.lamps           11 booleans, Larch's board (TALLIES[:ENGINE_BREAKS] in order)
#   Prismfall::Finale.montage         the beats that fire, in the script's order: { :id, :who, :lines,
#                                     :lamps => [indices this beat lights] }
#   Prismfall::Finale.play_montage    plays them: a 2-second cut each (pfm_cutscene(:MONTAGE_<ID>) when that
#                                     shot is registered), the line, the lamp board lighting. pf_finale_montage
# THE TAG BATTLE
#   Prismfall::Finale.partner         [type, name, version]: the Redeemed Kestrel, or Juno (J7) if he Fell
#   Prismfall::Finale.tag_foes        the two of Marchetti / Quent / Kroll who aren't turned or hijacking (v21)
#   Prismfall::Finale.tag_battle      registers the partner and fights them on :PRISM_ARENA -> true on a win
# THE EIGHTEEN LOCKS (during the Arceus battle; Prismfall Bosses 103 fires :prismfall_arceus_locks per bar)
#   each Warden of the bar kneels and releases (their line; V118 WARDENS_RELEASED + 1) or refuses (their line;
#   the boss plugin makes the lock forced). Prismfall::Finale.lock_state(gym) -> :released / :refused / :forced / nil
#   afterwards (pf_pylons_sync shows it on the map; the Gauntlet's empty pedestals read it in the post-game).
# THE ENDINGS
#   Prismfall::Finale.vignettes(id)   the ending's scenes in order: [{ :key, :map, :tone, :weather, :if }]
#   Prismfall::Finale.shatter_slides  [[city, line], ...] for each refusing Warden (Homecoming, Unfinished)
#   pf_vignette?(:bride_tree)         page condition for the reused maps' ending autoruns
#===============================================================================
module Prismfall
  module Finale
    VAR_WEAKPOINTS = 117   # V117 ENGINE_WEAKPOINTS
    VAR_RELEASED   = 118   # V118 WARDENS_RELEASED

    # story/11_FINALE_LINES.md sections 1-3, gym order (index = gym - 1). Stage directions are in the comments.
    RELEASE_LINES = [
      "Three hundred years of pageants, and this is the only true scene I ever staged. Exit, pursued by nothing. Lights down.",   # 1 Dorian
      "Granny wove a whole village around this. I think she'd want me to finish the pattern. Cut the thread.",   # 2 Tamsin
      "The Ebb ran both ways because of this. It'll run one way now, like any honest river. Go on, tides take you.",   # 3 Marisol
      "First time I've ever held it. Kinda thought it'd be heavier. ...Stay charged, wherever you're going.",   # 4 Rook
      "The desert keeps everything. I'm asking it, just this once, to give something back.",   # 5 Sahar
      "Dose makes the cure. Three hundred years is rather over the dose. Off you go, dear.",   # 6 Corvin
      "Forge it to break right, lad. Forge it to break right.",   # 7 Brann (He's weeping.)
      "A fist is a promise. So is an open hand.",   # 8 Kaito (He opens it.)
      "Verdance has never had an autumn. I'd like to see one.",   # 9 Juno (She is always the first to let go in her bar.)
      "We'll move south. We've hauled heavier things than a city. Take it before I count my grandchildren's toes again.",   # 10 Anja
      "The wind doesn't care who owns it. Never did. Fly home.",   # 11 Odessa
      "I've heard everyone's thoughts but yours. I'd like the quiet. Go.",   # 12 Ilsa (If reconciled, she says it with one hand still on her father's shoulder.)
      "First time in three hundred years a Warden's had nothing in his keeping. Feels like setting down a sack of stone. Go on, then.",   # 13 Bastian
      "Go home. All of you. Go home.",   # 14 Ysolde (The echoes in the stands fade as she says it. If Kestrel is beside her, he puts his hand over hers on the pylon.)
      "Tolerances exceeded. I'm releasing the part. That was a joke. I'm told I should make them.",   # 15 Magnus (A beat.)
      "My family kept one secret for three hundred years. I'm keeping none. It's yours, sweetheart. Take the dark with you.",   # 16 Nyx
      "Not chained, not broken, not bought, not crowned: given back, as a gift is found.",   # 17 Celestine (sung)
      "Dragons don't let anything through they haven't weighed. I've weighed this. It's too heavy for anyone. Go.",   # 18 Sigrun
    ].freeze
    REFUSAL_LINES = [
      "You told them the pageant version, darling. So did I, for thirty years. I find I can't stop on cue.",   # 1 Dorian
      "I can't. I can't. The contract's still running and there's nothing left in the village but this. I'm sorry — sorry —",   # 2 Tamsin
      "My brother's in the river mud because of what this thing started. It owes Ebbmouth. It stays.",   # 3 Marisol
      "It's not mine to give! It never was! It's in their cradle, I can't even — chat, I can't reach it.",   # 4 Rook
      "I buried the truth once because someone with a badge asked me to. You stood with the badge. I'll keep what the sand gave me.",   # 5 Sahar
      "I — I'm not him. I don't know how. Nobody told me how.",   # 6 Corvin [spoken by the Porter]
      "You gave my guild's Light away to a king, and now you'd have me give the fire too? No, lad. Not for you.",   # 7 Brann
      "I never said it out loud. Marrowgate. A man who can't open his mouth can't open his hand.",   # 8 Kaito
      "I let go of him. I let go of the dock we started on. I'm not letting go of the last thing that's mine because you asked.",   # 9 Juno
      "Rimeholt drowns without it. You threw me to the court for less. Ice remembers.",   # 10 Anja
      "Dead letters are the last thing some people ever said. You burned one. I don't hand things to people who burn them.",   # 11 Odessa
      "He's dying on that Ring for a country that never thanked him. Someone in this family is going to keep something.",   # 12 Ilsa
      "You walked a Meridian beacon into my seams, child, and they came for my people by it. I'll keep my stone.",   # 13 Bastian
      "She asked me to keep one boy safe and I couldn't. I won't lose the only place I can still hear them both.",   # 14 Ysolde
      "I won't hand my city's future to a god. Gods have had three hundred years. Engineers have had ten.",   # 15 Magnus
      "Everything has a price, sweetheart, and you never paid mine. The dark stays where it's useful.",   # 16 Nyx
      "I cannot lie, so hear it plainly: you're singing in the wrong key, and I won't give the dusk to that song.",   # 17 Celestine
      "You swore over my fire you'd keep them, or end them. I believed you. So I'm keeping mine from you.",   # 18 Sigrun
    ].freeze
    SHATTER_SLIDES = [
      ["Saltmere", "The one city the Bleed never touched has a glass promenade. The Lantern Theatre plays to it."],
      ["Briarwick", "The looms went still in one night. Tamsin weaves by hand now."],
      ["Ebbmouth", "The Ebb stopped, then ran out to sea and didn't come back. The mills are museums."],
      ["Lumen City", "The Lowlight's glass took three more streets before the dark came. Rook reads the names on air every year."],
      ["Duneholt", "The well never refilled. The caravans left by the east gate, in order of age."],
      ["Mirefen", "The mire went clear and killed everything that had learned to live in it. Corvin's Ward was empty by then."],
      ["Cindervault", "The Cinderhorn went cold with its forges full. Brann's last blade is still in the stone."],
      ["Ironreach", "The shafts fell in on the Pit. Kaito dug for nine days."],
      ["Verdance", "Autumn came all at once, and winter the same week. Juno planted anyway."],
      ["Rimeholt", "The lake let go. The Holdfast is an island now, and Anja lights its beacon for nobody."],
      ["Skyreach", "The Stormfront fell on the masts. The Gale Post flies from Ebbmouth, when it flies."],
      ["Lucent", "The city in the sky came down on the city below. The Athenaeum's books were found as far as Gloaming."],
      ["Cragholm", "The crystal halls went dark and brittle. Pip carried her grandfather's lamp out."],
      ["Gravenmoor", "Every echo spoke at once, and then none ever did again. Ysolde keeps the candles lit out of habit."],
      ["Cogsworth", "The foundries seized mid-shift. The clock-towers stopped at eleven-forty, all of them."],
      ["Underveil", "The long night ended at noon, and the towers couldn't bear the light. Nadir moved up the lifts, uninvited."],
      ["Gloaming", "Dusk became midnight and stayed. The lantern-moths are the only stars."],
      ["Wyrmrest", "The dragons left the Rift in one flight and didn't choose a new one."],
    ].freeze

    #---------------------------------------------------------------------------
    # The Hijack
    #---------------------------------------------------------------------------
    HIJACK_BEATS = [:HJ_RINGS, :HJ_CRADLE, :HJ_LOCKS, :HJ_CROWN, :HJ_DESCENT].freeze   # pfm_cutscene ids, in order

    @answers = []
    class << self
      attr_accessor :answers   # scripted answers for his_hand / play_montage (headless tests)
    end

    def self.flag(name)
      return (Prismfall::Narrative.flag(name) rescue false) ? true : false
    end

    def self.hijacker
      return :AURELIUS if Prismfall.ruin_route?
      return :QUENT if flag(:VOSS_DISCREDITED)
      return :VOSS
    end

    def self.pick(prompt, labels)
      if @answers && !@answers.empty?
        ans = @answers.shift
        return ans.is_a?(Integer) ? ans : labels.index(ans.to_s)
      end
      return pbMessage(prompt, labels, 0)
    end

    def self.his_hand
      return :none if hijacker != :VOSS
      if flag(:VOSS_ACCEPTED)
        idx = pick(_INTL("He holds out his hand."), [_INTL("Take it."), _INTL("Refuse.")])
        if idx == 0
          Prismfall::Choices.make(:ch21_hand, :take)
          pbMessage(_INTL("You take it. He helps you up. Behind him, the Engine's light steadies, and turns warm."))
          Prismfall.trigger_ending(:END_CONCORD_DAWN)
          return :concord
        end
        Prismfall::Choices.make(:ch21_hand, :refuse)
        return :refused
      end
      idx = pick(_INTL("He holds out his hand."), [_INTL("Take it."), _INTL("Don't.")])
      if idx == 0
        Prismfall.game_over(:GO_HIS_HAND)
        return :game_over
      end
      return :refused
    end

    # telemetry sabotaged, Zekrom freed, the governor, the grid cut, comms, schematics
    WEAKPOINTS = ["flag(:TELEMETRY_SABOTAGED)", "flag(:ZEKROM_FREED)", "flag(:MAGNUS_KEPT_FAITH)", "flag(:ROOK_CUTS_GRID)",
                  "flag(:NYX_PRECISE)", "chose(:ch20_calla, :shelter) || chose(:ch20_calla, :send_back)"].freeze

    def self.refresh_weakpoints
      n = WEAKPOINTS.count { |c| (Prismfall::Conditions.evaluate(c) rescue false) }
      $game_variables[VAR_WEAKPOINTS] = n if $game_variables
      return n
    end

    #---------------------------------------------------------------------------
    # Larch's eleven lamps and the allies' montage
    #---------------------------------------------------------------------------
    LAMP_COUNT = 11

    def self.lamps
      list = Prismfall::Narrative::TALLIES[:ENGINE_BREAKS]
      return list.map { |c| (Prismfall::Conditions.evaluate(c) rescue false) ? true : false }
    end

    def self.lamp_total
      return lamps.count(true)
    end

    # The script's table, in order. :if nil = always. :lamps = ENGINE_BREAKS rows this beat lights on the board
    # (only those that are true light). :lines may hold [:SPEAKER, :expression, "text"] or narration Strings.
    MONTAGE = [
      { :id => :ROOK, :who => "Rook", :if => "flag(:ROOK_CUTS_GRID)", :lamps => [4],
        :lines => ["Rook, in the broadcast gantry.",
                   [:ROOK, :smug, "First time Lumen's been dark in ten years. Kinda pretty."],
                   "The Engine flickers."] },
      { :id => :NYX, :who => "Nyx", :if => "flag(:NYX_PRECISE)", :lamps => [5],
        :lines => ["Nyx: a single switch, and Meridian's comms go dead, surgically."] },
      { :id => :NYX_KNIVES, :who => "Nyx", :if => "!flag(:NYX_PRECISE)", :lamps => [],
        :lines => ["Nyx goes in with knives and her people. It works, and it's bloody, and she's hurt."] },
      { :id => :MAGNUS, :who => "Magnus", :if => "flag(:MAGNUS_KEPT_FAITH)", :lamps => [3],
        :lines => ["Magnus in the machine-gallery, a spanner in his steel hand.",
                   [:MAGNUS, :neutral, "No machine I have built will kill a child. Governor's off. Go."]] },
      { :id => :MARCHETTI, :who => "Marchetti", :if => "flag(:MARCHETTI_TURNED)", :lamps => [8],
        :lines => ["Marchetti, on the Directorate channel.",
                   [:MARCHETTI, :neutral, "All units, stand down. Not for this. Never for this."]] },
      { :id => :LARCH, :who => "Larch", :if => "flag(:TELEMETRY_SABOTAGED)", :lamps => [0, 1],
        :lines => [[:LARCH, :happy, "It's miscalibrated! It's reaching for a shard that isn't where it thinks!"]] },
      { :id => :CALLA, :who => "Calla", :if => "chose(:ch20_calla, :shelter)", :lamps => [6],
        :lines => ["Calla's schematics, pinned to Larch's board. One lamp."] },
      { :id => :CALLA_BACK, :who => "Calla", :if => "chose(:ch20_calla, :send_back)", :lamps => [6, 7],
        :lines => ["Calla's schematics, the full set. Two lamps.", "Larch touches the second lamp and says nothing."] },
      { :id => :SIGRUN, :who => "Sigrun", :if => nil, :lamps => [],
        :lines => ["Sigrun and her dragons hold the sky against Meridian's Gilded Hours airships, with Reshiram beside her."],
        :extra => [["flag(:DOMINAR_SWAYED)", "The Ashkaar legions fly with her."]] },
      { :id => :MARISOL, :who => "Marisol", :if => nil, :lamps => [],
        :lines => ["Marisol's fleet evacuates Lower Crownhaven across the caldera lake. Edda pilots the lead boat."] },
      { :id => :TAMSIN, :who => "Tamsin", :if => nil, :lamps => [],
        :lines => ["Tamsin's silk nets catch falling debris over the stands."] },
      { :id => :HOLLOW, :who => "The Lantern Hollow", :if => "flag(:LANTERN_HOLDS)", :lamps => [9],
        :lines => [] },   # the line names who leads them (below)
      { :id => :KAITO, :who => "Kaito", :if => nil, :lamps => [],
        :lines => ["Kaito holds the arena gate."] },
      { :id => :WAR, :who => "The war", :if => "flag(:WAR_STOPPED)", :lamps => [],
        :lines => ["Ashkaar's riders hold the sky and Isenmar's ice-riders hold the lake shore. Together."] }
    ].freeze

    def self.hollow_leader
      return _INTL("Rowan") if flag(:ROWAN_ALIVE)
      return _INTL("Teo") if flag(:TEO_SAVED)
      return _INTL("Thistle and Wick")
    end

    # The beats that fire, with the lamps each one really lights.
    def self.montage
      lit = lamps
      out = []
      MONTAGE.each do |b|
        next if b[:if] && !(Prismfall::Conditions.evaluate(b[:if]) rescue false)
        lines = b[:lines].dup
        if b[:id] == :HOLLOW
          lines = [_INTL("The Lantern Hollow guard the pylons against Directorate techs, led by {1}.", hollow_leader)]
        end
        (b[:extra] || []).each { |cond, text| lines.push(text) if (Prismfall::Conditions.evaluate(cond) rescue false) }
        out.push({ :id => b[:id], :who => b[:who], :lines => lines, :lamps => b[:lamps].select { |i| lit[i] } })
      end
      return out
    end

    # Lamps no montage beat lights: they are already burning when Larch sets the board down
    # (the telemetry destroyed, Zekrom freed, Kestrel not lost).
    def self.lamps_before_montage
      lit = lamps
      later = montage.flat_map { |b| b[:lamps] }
      return (0...lit.length).select { |i| lit[i] && !later.include?(i) }
    end

    def self.say(line)
      if line.is_a?(Array)
        spk, expr, text = line
        if defined?(pf_say) && defined?(Prismfall::Portrait)
          pf_say(spk, expr || :neutral, _INTL(text)) rescue pbMessage("#{spk.to_s.capitalize}: #{_INTL(text)}")
        else
          pbMessage("#{spk.to_s.capitalize}: #{_INTL(text)}")
        end
      else
        pbMessage(_INTL(line))
      end
    end

    def self.board(lit_indices, flash = [])
      return if !defined?(Prismfall::Cutscene) || !Prismfall::Cutscene.respond_to?(:lamp_board)
      Prismfall::Cutscene.lamp_board(lit_indices, flash)
    rescue StandardError => e
      PBDebug.log("[Prismfall Finale] lamp board: #{e.class}: #{e.message}") if defined?(PBDebug)
    end

    def self.board_off
      Prismfall::Cutscene.lamp_board_off if defined?(Prismfall::Cutscene) && Prismfall::Cutscene.respond_to?(:lamp_board_off)
    rescue StandardError
      nil
    end

    # Returns the number of lamps lit at the end (== tally(:ENGINE_BREAKS)).
    def self.play_montage(cut: 2.0)
      refresh_weakpoints
      lit = lamps_before_montage
      board(lit)
      montage.each do |b|
        shot = :"MONTAGE_#{b[:id]}"
        played = false
        if defined?(pfm_cutscene) && defined?(Prismfall::Cutscene::CUTSCENE_SCENES) &&
           Prismfall::Cutscene::CUTSCENE_SCENES[shot]
          played = pfm_cutscene(shot)
        end
        b[:lines].each { |l| say(l) }
        if !b[:lamps].empty?
          lit |= b[:lamps]
          pbSEPlay("Mining reveal") rescue nil
          board(lit, b[:lamps])
        end
        pbWait(cut) if !played && cut > 0 && defined?(pbWait) && !defined?(Harness)
      end
      board_off
      return lit.length
    end

    #---------------------------------------------------------------------------
    # The tag battle
    #---------------------------------------------------------------------------
    TAG_VERSION    = 21
    KESTREL_PARTNER_DECADE = 9   # Redeemed Kestrel: Prismfall::Rival.partner_version(9) = 93 / 94 / 95 by starter slot
    TAG_FOES = [
      [:MERIDIAN_MARCHETTI, "Helene", "!flag(:MARCHETTI_TURNED)"],
      [:MERIDIAN_QUENT, "Percival", "!flag(:VOSS_DISCREDITED)"],     # Quent is in the harness when Voss fell
      [:MERIDIAN_KROLL, "Sabine", nil]
    ].freeze

    # [type, name, version]. The Redeemed team is a rival PARTNER team (Core 006): one block per starter slot, 93 / 94 /
    # 95, so his starter follows the player's (the script's "version 21" was his K2 number). If that block is missing,
    # he brings his semifinal team.
    def self.partner
      if flag(:KESTREL_FALLEN)
        return [:RIVAL_JUNO, "Juno", Prismfall::Rival.version_for(7)]
      end
      version = Prismfall::Rival.partner_version(KESTREL_PARTNER_DECADE)
      return [:RIVAL_KESTREL, "Kestrel", version] if GameData::Trainer.exists?(:RIVAL_KESTREL, "Kestrel", version)
      return [:RIVAL_KESTREL, "Kestrel", Prismfall::Rival.version_for(8)]
    end

    def self.tag_foes
      list = TAG_FOES.select { |_t, _n, cond| cond.nil? || (Prismfall::Conditions.evaluate(cond) rescue true) }
      list = list.select { |t, n, _c| GameData::Trainer.exists?(t, n, TAG_VERSION) }
      return list.first(2).map { |t, n, _c| [t, n, TAG_VERSION] }
    end

    def self.register_partner
      type, name, version = partner
      return false if !GameData::Trainer.exists?(type, name, version)
      pbRegisterPartner(type, name, version)
      return true
    end

    # true on a win. "(LOSE: retry from the montage.)" is the caller's loop.
    def self.tag_battle
      foes = tag_foes
      return true if foes.empty?
      register_partner
      setBattleRule("canLose")
      setBattleRule("field", :PRISM_ARENA) if defined?(FieldEffects)
      setBattleRule("double") if foes.length == 1
      won = TrainerBattle.start(*foes) ? true : false
      pbDeregisterPartner if defined?(pbDeregisterPartner)
      $player.heal_party if !won && $player
      return won
    end

    #---------------------------------------------------------------------------
    # The eighteen locks
    #---------------------------------------------------------------------------
    CHOIR_LINE = "The Gloaming choir in the stands picks it up. Then the Prism Choir in the loft. Then the crowd. " \
                 "Forty thousand people singing a song most of them only learned this week."

    def self.locks
      c = Prismfall.state.custom
      c[:finale_locks] = {} if !c[:finale_locks].is_a?(Hash)
      return c[:finale_locks]
    end

    def self.lock_state(gym); return locks[gym]; end
    def self.released_count;  return locks.values.count(:released); end
    def self.refusers;        return (1..18).select { |g| [:refused, :forced].include?(locks[g]) }; end

    def self.reset_locks
      Prismfall.state.custom[:finale_locks] = {}
      $game_variables[VAR_RELEASED] = 0 if $game_variables
    end

    def self.consents?(gym)
      if defined?(Prismfall::Bosses) && Prismfall::Bosses.respond_to?(:arceus_consents?)
        return Prismfall::Bosses.arceus_consents?(gym)      # the boss's own reading (and its test override)
      end
      return Prismfall::Ceremony.consent?(gym)
    end

    def self.warden(gym)
      return Prismfall::GYMS[gym - 1][:trainer_name]
    end

    # Who speaks a Warden's line: Corvin's refusal is the Choir porter in his mask.
    def self.speaker(gym, released)
      return _INTL("Porter") if gym == 6 && !released
      return _INTL(warden(gym))
    end

    def self.line_for(gym, released)
      return _INTL((released) ? RELEASE_LINES[gym - 1] : REFUSAL_LINES[gym - 1])
    end

    # A bar begins: its Wardens kneel. forced = the gyms whose lock the boss treats as forced.
    def self.kneel_bar(battle, bar, gyms, forced)
      reset_locks if bar == 1
      # yesterday's refusals were broken by force when their bar fell
      locks.each { |g, st| locks[g] = :forced if st == :refused && !gyms.include?(g) }
      order = gyms.sort_by { |g| (g == 9 && !forced.include?(g)) ? 0 : 1 }   # Juno is always the first to let go in her bar
      order.each do |gym|
        consent = consents?(gym)
        if forced.include?(gym) && consent        # the War variant: nobody is asked
          locks[gym] = :forced
          next
        end
        released = !forced.include?(gym)
        locks[gym] = (released) ? :released : :refused
        show(battle, _INTL("{1} kneels at the {2} pylon.", _INTL(warden(gym)), Prismfall::Ceremony::PLATES[gym - 1][1]))
        show(battle, "#{speaker(gym, released)}: #{line_for(gym, released)}", true)
        show(battle, _INTL(CHOIR_LINE)) if gym == 17 && released
      end
      $game_variables[VAR_RELEASED] = released_count if $game_variables
      EventHandlers.trigger(:prismfall_finale_kneels, bar, gyms, forced)
    end

    def self.show(battle, text, paused = false)
      if battle
        (paused) ? battle.pbDisplayPaused(text) : battle.pbDisplay(text)
      else
        pbMessage(text)
      end
    end

    # [[city, line], ...] for each Warden whose lock didn't open (Homecoming, Unfinished; the Gauntlet's empty pedestals).
    def self.shatter_slides
      return refusers.map { |g| SHATTER_SLIDES[g - 1] }
    end

    def self.pedestal_line(gym)
      return nil if !refusers.include?(gym)
      return _INTL(SHATTER_SLIDES[gym - 1][1])
    end

    #---------------------------------------------------------------------------
    # The endings: which scenes play, in order (the scene text is story/08_ACT_V.md)
    #---------------------------------------------------------------------------
    # :map is the maps.json id of the reused map (nil = the arena, or a still); :if is a Conditions string.
    WAKINGS = [
      { :key => :bride_tree,   :map => 708, :weather => :Rain,  :note => "Verdance and the Bride Tree: Elin wakes" },
      { :key => :lowlight,     :map => 608, :weather => nil,    :note => "the Lowlight: Dex" },
      { :key => :quiet_ward,   :map => 223, :weather => nil,    :note => "Mirefen's Quiet Ward" },
      { :key => :scar_forty,   :map => 888, :weather => nil,    :note => "the Glassfall Scar's forty" },
      { :key => :marrowgate,   :map => nil, :weather => nil,    :note => "Marrowgate's gate: Kaito" },
      { :key => :arena_floor,  :map => 491, :weather => :Rain,  :note => "the PC alone on the arena floor; the scanner reads a faint ordinary colour" }
    ].freeze
    VOSS_SUNRISE = { :key => :voss_sunrise, :map => nil, :if => "flag(:PC_SPARED_VOSS)",
                     :note => "Voss in a wheeled chair on the Basilica roof, facing east" }.freeze
    FERRY_RAIL = { :key => :ferry_rail, :map => 100, :note => "the Ferrow's Landing rail, the first ferry (Edda)" }.freeze

    VIGNETTES = {
      :END_HOMECOMING       => WAKINGS + [VOSS_SUNRISE, { :key => :one_year_later, :map => nil, :note => "the epilogue slides, 08 order" }, FERRY_RAIL],
      :END_UNFINISHED       => WAKINGS + [{ :key => :last_shatter, :map => nil, :note => "one Last Shatter slide per refusing Warden (shatter_slides)" },
                                          VOSS_SUNRISE, FERRY_RAIL],
      :END_EMPTY_LIGHTHOUSE => WAKINGS + [{ :key => :hesper_lamp, :map => 105, :note => "Hesper's lamp each night" },
                                          { :key => :kestrel_grave, :map => 384, :note => "the Gravenmoor barrows: the letter read at Kestrel's grave" },
                                          FERRY_RAIL],
      :END_LONG_VIGIL       => [{ :key => :crown_worn, :map => 491, :note => "the PC wears the Crown; Arceus leaves" },
                                { :key => :ten_years, :map => nil, :note => "ten years later: the first crystal on the PC's hand" }],
      :END_BORROWED_CROWN   => [{ :key => :bearer, :map => 491, :note => "the bearer crystallizing" }, FERRY_RAIL,
                                { :key => :kestrel_rail, :map => 100, :if => "flag(:KESTREL_BEARS)", :note => "Kestrel's hand on the rail, turning to glass" },
                                { :key => :sigrun_roof, :map => nil, :if => "flag(:SIGRUN_BEARS)", :note => "Sigrun on the Basilica roof: \"Ten years. Maybe twelve.\"" }],
      :END_CONCORD_DAWN     => [{ :key => :half_bound, :map => 491, :note => "Arceus half-bound by Magnus's governor" },
                                { :key => :council, :map => nil, :note => "the PC on the Zenith Council; Celestine's voice" }],
      :END_HOLLOW_SPRING    => [{ :key => :fire_and_glass, :map => 491, :note => "one night of fire and glass" },
                                { :key => :first_seed, :map => nil, :note => "Rowan (or Thistle) plants the first seed in plain soil" }],
      :END_GILDED_CHAIN     => [{ :key => :second_sun, :map => 491, :note => "Arceus bound in gold above Crownhaven" },
                                { :key => :sleeper, :map => 491, :note => "the Sovereign Who Sleeps; the linesman's mug" }]
    }.freeze

    def self.ending_id
      id = (Prismfall.state.narrative[:postgame] rescue nil)     # set by Endings.trigger
      return id if id.is_a?(Symbol)
      return (Prismfall::Endings.determine rescue nil)
    end

    def self.vignettes(id = nil)
      id ||= ending_id
      list = VIGNETTES[id] || []
      return list.select { |v| v[:if].nil? || (Prismfall::Conditions.evaluate(v[:if]) rescue false) }
    end

    def self.vignette?(key, id = nil)
      return vignettes(id).any? { |v| v[:key] == key.to_sym }
    end
  end
end

# The locks open (or don't) bar by bar while Arceus is fought.
EventHandlers.add(:prismfall_arceus_locks, :prismfall_finale_kneels,
  proc { |battle, bar, gyms, forced|
    Prismfall::Finale.kneel_bar(battle, bar, gyms || [], forced || [])
  }
)

def pf_finale_hand;           return Prismfall::Finale.his_hand;           end
def pf_finale_montage(**o);   return Prismfall::Finale.play_montage(**o);  end
def pf_finale_tag_battle;     return Prismfall::Finale.tag_battle;         end
def pf_lock_state(gym);       return Prismfall::Finale.lock_state(gym);    end
def pf_vignette?(key);        return Prismfall::Finale.vignette?(key);     end
