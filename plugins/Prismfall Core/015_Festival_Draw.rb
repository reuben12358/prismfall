#===============================================================================
# Prismfall Core - 015 Choice-driven Festival draw (NARRATIVE_KEYS section 6)
#-------------------------------------------------------------------------------
# DRAWS[stage_id] is an ordered candidate list; the first candidate whose
# condition holds (and whose person isn't already used by an earlier stage) is
# the player's opponent. The stage default (PLAYER_PATH[round] or the stage's
# :opponent) is always appended as the final fallback. Candidate keys:
#   :opponent   entrant ID (variants share a :person, e.g. :KESTREL_FALLEN)
#   :condition  Prismfall::Conditions string (nil = always)
#   :version    trainer version override for this draw (optional)
# Timing:
#   bracket stages   drawn at Festival.start. A drawn opponent seeded elsewhere
#                    swaps seats with the default; an unseeded one (Rowan, Dask)
#                    replaces the default, who withdraws (counts as out).
#   :live stages     (the Final) seeded with the default at start and drawn
#                    when the battle starts (Day 7); a stand-in fights in the
#                    default's slot without reseating anyone.
#   other stages     (the Hijack) drawn live, fixed when their battle starts.
# Validation (load + Festival.validate): candidates exist, conditions parse,
# every stage has a fallback, no person is a candidate in two stages.
# Also here: delegation seating + seated?(), MATCH_RULES and match highlights,
# Festival days (exhibitions), drawn(:STAGE), ARCEUS_VARIANTS.
#===============================================================================
module Prismfall
  module Festival
    DRAWS = {
      :R16 => [   # default :JUNO (J4)
        { :opponent => :MARISOL, :condition => "!ruin_route && seated(:MARISOL) && !flag(:TEO_SAVED) && bond(:MARISOL) <= 2" },
        { :opponent => :ANJA,    :condition => "!ruin_route && seated(:ANJA) && flag(:ANJA_EXPOSED)" },
        { :opponent => :ROWAN,   :condition => "!ruin_route && flag(:ROWAN_ALIVE) && choice(:ch13_rowan_testimony) == :mercy && standing(:HOLLOW) >= 4" }
      ],
      :QF => [    # default :CELESTINE (v92)
        { :opponent => :DASK,   :condition => "ruin_route" },
        { :opponent => :SIGRUN, :condition => "resonance <= -3 || flag(:WAR_ISENMAR_WON)",       :version => 92 },   # she weighs you again, or comes for the one who broke her father's legions
        { :opponent => :KAITO,  :condition => "choice(:ch19_oath) == :keep",                     :version => 92 },
        { :opponent => :YSOLDE, :condition => "flag(:KESTREL_FALLEN)" },
        { :opponent => :ODESSA, :condition => "seated(:ODESSA) && tally(:WARM_BONDS) >= 5 && resonance >= 2", :version => 92 }
      ],
      :SF => [    # default :KESTREL (K8, 80-82); Ruin Route: same team, Ruin dialogue
        { :opponent => :KESTREL_FALLEN, :condition => "!ruin_route && flag(:KESTREL_FALLEN)" }
      ],
      :FINAL => [ # default :VALEN. :live => true [CORE+]: drawn when the Final starts (Day 7)
        { :opponent => :VALEN_RUIN, :condition => "ruin_route" },
        { :opponent => :BRANN,      :condition => "flag(:VALEN_COLLAPSED)" }
      ],
      :HIJACK => [ # default :VOSS (drawn live)
        { :opponent => :THEODRIC, :condition => "ruin_route" },
        { :opponent => :QUENT,    :condition => "flag(:VOSS_DISCREDITED)" }
      ]
    }

    # Offered in addition to knocked-out :exhibition entrants (NARRATIVE_KEYS 6.6).
    EXHIBITION_EXTRAS = [
      { :entrant => :PAGEANT_BOUT, :condition => "!ruin_route", :from_day => 3 },                                    # Dorian & Rook double
      { :entrant => :JUNO,         :condition => "!ruin_route && drawn(:R16) != :JUNO", :from_day => 3 },            # Garden Match (J4 team)
      { :entrant => :MARISOL,      :condition => "!ruin_route && drawn(:R16) != :MARISOL && flag(:TEO_SAVED) && bond(:MARISOL) >= 5", :from_day => 3 },
      { :entrant => :MORWEN,       :condition => "!ruin_route && flag(:KESTREL_YSOLDE_RECONCILED) && choice(:ch15_kestrel) == :resolve", :from_day => 5 }
    ]

    # Companion matches (NARRATIVE_KEYS 6.5): winner rules + highlight moments
    # [actor, pokemon, event, caption] for Prismfall Cutscenes. First row for
    # the pair whose condition holds decides an NPC-vs-NPC match.
    MATCH_RULES = [
      { :pair => [:KESTREL, :KAITO], :winner => :KESTREL, :condition => nil, :moments => [
          [:KAITO,   :LUCARIO,   :send_out,   "Kaito: \"Stand up. Again.\""],
          [:KESTREL, :AEGISLASH, :attack,     "The Gauntlet flares; the arena's field surges on its own."],
          [:KAITO,   :LUCARIO,   :dodge,      "Lucario flinches from something that isn't the blade."],
          [:KESTREL, :AEGISLASH, :finish,     "Kaito, after: \"Lucario felt it. That isn't him fighting.\""] ] },
      { :pair => [:KESTREL, :ROOK], :winner => :KESTREL, :condition => nil, :moments => [
          [:ROOK,    :ROTOM,     :send_out,   "Rook: \"Chat says you're gonna lose.\""],
          [:KESTREL, :STARAPTOR, :attack,     "Brave Bird through a Thunderbolt, live on every screen in Zenith."],
          [:ROOK,    :TOXTRICITY,:faint,      "Rook, off-mic: \"...Chat's wrong a lot.\""] ] },
      { :pair => [:KESTREL, :ODESSA], :winner => :KESTREL, :condition => nil, :moments => [
          [:ODESSA,  :CORVIKNIGHT, :send_out, "Odessa: \"Hold onto something.\""],
          [:KESTREL, :AEGISLASH,   :attack,   "King's Shield, then the counter."],
          [:ODESSA,  :CORVIKNIGHT, :forfeit,  "She salutes and loses with style."] ] },
      { :pair => [:ANJA, :BRANN], :winner => :ANJA, :condition => "flag(:WAR_ISENMAR_WON) || (flag(:WAR_STOPPED) && choice(:war_prisoner) == :free)", :moments => [
          [:BRANN, :COALOSSAL, :send_out,     "Two Wardens who were on opposite shores a season ago."],
          [:ANJA,  :MAMOSWINE, :beam_clash,   "Blizzard meets Flamethrower: the war's beam clash, in miniature, and this time nobody dies."],
          [:BRANN, :COALOSSAL, :faint,        "Brann laughs until he coughs. \"Aye. Ice remembers.\""] ] },
      { :pair => [:ANJA, :BRANN], :winner => :BRANN, :condition => nil, :moments => [
          [:ANJA,  :MAMOSWINE, :send_out,     "Anja doesn't bow."],
          [:BRANN, :COALOSSAL, :beam_clash,   "Flamethrower against Blizzard; steam hides the whole arena."],
          [:ANJA,  :MAMOSWINE, :faint,        "Brann offers a hand. Whether she takes it depends on the armistice (ISENMAR_EMBITTERED)."] ] },
      { :pair => [:MARISOL, :BRANN], :winner => :MARISOL, :condition => "!flag(:WAR_ASHKAAR_WON)", :moments => [
          [:MARISOL, :GYARADOS, :send_out,    "\"Tides take it. Let's go, old man.\""],
          [:MARISOL, :GYARADOS, :beam,        "Hydro Pump douses the forge-field: :VOLCANIC cools to :ASHEN_WASTE."],
          [:BRANN,   :ARCANINE, :faint,       "Brann: \"Forged to break right.\""] ] },
      { :pair => [:YSOLDE, :SIGRUN], :winner => :SIGRUN, :condition => nil, :moments => [
          [:YSOLDE, :CHANDELURE, :field_shift, "The Cathedral's candles follow her in."],
          [:SIGRUN, :SALAMENCE,  :attack,      "Salamence dives through the dark."],
          [:YSOLDE, :CHANDELURE, :faint,       "Ysolde: \"The dead say you fight like someone with nothing to bury.\""] ] },
      { :pair => [:JUNO, :SIGRUN], :winner => :SIGRUN, :condition => nil, :moments => [
          [:JUNO,   :TSAREENA,  :send_out,     "Juno, displaced by a Grievance, fights anyway."],
          [:JUNO,   :TSAREENA,  :field_shift,  "The Flower Garden reaches stage five for the first time in her life."],
          [:SIGRUN, :HAXORUS,   :finish,       "Sigrun kneels to her afterward. Nobody has seen her do that."] ] },
      { :pair => [:JUNO, :YSOLDE], :winner => :JUNO, :condition => "bond(:JUNO) >= 5", :moments => [
          [:YSOLDE, :GENGAR,    :taunt,        "\"Your aunt is listening, you know.\""],
          [:JUNO,   :WHIMSICOTT,:attack,       "Juno, crying, doesn't miss."],
          [:YSOLDE, :GENGAR,    :faint,        "Ysolde smiles. It was a kindness, and it worked."] ] },
      { :pair => [:CELESTINE, :MARISOL], :winner => :CELESTINE, :condition => nil, :moments => [
          [:CELESTINE, :TOGEKISS, :send_out,   "\"Once upon a time, a dockworker fought a fairy tale.\""],
          [:MARISOL,   :GYARADOS, :attack,     "\"I don't do stories. Waterfall.\""],
          [:CELESTINE, :TOGEKISS, :finish,     "The story wins. Marisol swears for a full caption box."] ] },
      { :pair => [:VALEN, :SIGRUN], :winner => :VALEN, :condition => nil, :moments => [
          [:SIGRUN, :SALAMENCE, :send_out,     "She entered to take the Blessing so the child wouldn't have to."],
          [:VALEN,  :ZYGARDE,   :attack,       "His crystal arm spreads to the collarbone with the order."],
          [:SIGRUN, :SALAMENCE, :faint,        "\"He beat me with an arm made of glass.\""] ] },
      { :pair => [:VALEN, :KAITO], :winner => :VALEN, :condition => nil, :moments => [
          [:KAITO, :LUCARIO, :send_out,        "The man who sealed Marrowgate, and the man who ordered it."],
          [:KAITO, :LUCARIO, :attack,          "Kaito's first Aura Sphere is aimed a hand's width wide. On purpose."],
          [:VALEN, :ZYGARDE, :finish,          "If KAITO_TESTIFIED: Valen bows first."] ] }
    ]

    # True Finale variants (read by the Prismfall Bosses plugin; Core doesn't
    # change the :ARCEUS stage). First match wins.
    ARCEUS_VARIANTS = [
      { :id => :ARCEUS_JUDGMENT,      :condition => "ruin_route",                 :bars => 7, :player_side => 2 },
      { :id => :ARCEUS_GILDED,        :condition => "flag(:ENGINE_CALIBRATED)",   :bars => 6 },
      { :id => :ARCEUS_WAR,           :condition => "resonance <= -6",            :bars => 7 },
      { :id => :ARCEUS_MISCALIBRATED, :condition => "flag(:TELEMETRY_SABOTAGED)", :bars => 5 },
      { :id => :ARCEUS_BOUND,         :condition => nil,                          :bars => 6 }
    ]

    def self.arceus_variant
      ARCEUS_VARIANTS.each { |v| return v if v[:condition].nil? || Prismfall::Conditions.evaluate(v[:condition]) }
      return ARCEUS_VARIANTS.last
    end

    #---------------------------------------------------------------------------
    # Festival days (events set them: Prismfall::Festival.set_day(3))
    #---------------------------------------------------------------------------
    def self.day
      return (started? && state[:day]) ? state[:day] : 1
    end

    def self.set_day(n)
      return if !started?
      state[:day] = n.to_i
    end

    def self.next_day!
      set_day(day + 1)
      return day
    end

    # Entrant knocked out (or withdrawn) on the current day.
    def self.mark_out(id)
      return if !started? || id.nil? || id == :PLAYER
      state[:out_day] ||= {}
      state[:out_day][id] ||= day
    end

    def self.out?(id)
      return false if !started? || !state[:out_day]
      return state[:out_day].has_key?(id)
    end

    # Entrant locked for a stage (nil if not drawn yet).
    def self.drawn(stage_id)
      return nil if !started? || !state[:draws]
      return state[:draws][stage_id]
    end

    #---------------------------------------------------------------------------
    # Delegations -> seats
    #---------------------------------------------------------------------------
    # { seat => entrant } for the current narrative state.
    def self.resolve_delegations
      seats = {}
      taken = []
      forfeits = []
      DELEGATIONS.each do |seat, cands|
        cands.each do |id, cond|
          next if id != :FORFEIT && taken.include?(id)
          next if cond && !Prismfall::Conditions.evaluate(cond)
          if id == :FORFEIT
            forfeits.push(seat)
          else
            seats[seat] = id
            taken.push(id)
          end
          break
        end
        forfeits.push(seat) if !seats[seat] && !forfeits.include?(seat)   # safety net
      end
      forfeits.each do |seat|
        id = FORFEIT_POOL.find { |f| !taken.include?(f) }
        seats[seat] = id
        taken.push(id)
      end
      return seats
    end

    def self.seated_bracket(seats)
      return BRACKET_SEATS.map { |seat| (seat == :PLAYER) ? :PLAYER : seats[seat] }
    end

    # True if the entrant holds a delegation seat this run (live preview before
    # the Festival starts).
    def self.seated?(id)
      list = (started? && state[:seated]) ? state[:seated] : resolve_delegations.values
      return list.include?(id)
    end

    #---------------------------------------------------------------------------
    # Companion matches and highlights
    #---------------------------------------------------------------------------
    def self.match_rule(a, b)
      return MATCH_RULES.find do |rule|
        next false if !(rule[:pair].include?(a) && rule[:pair].include?(b)) || a == b
        rule[:condition].nil? || Prismfall::Conditions.evaluate(rule[:condition])
      end
    end

    def self.highlight_info(id)
      e = ENTRANTS[id] || {}
      return { :id => id, :name => display_name(id), :trainer_type => Array(e[:trainer_type]).first }
    end

    # Plays the key moments of an NPC match: Prismfall::Cutscene.match_highlight
    # if the Cutscenes plugin provides it, else a text summary.
    def self.play_highlight(a, b, winner, moments)
      if defined?(Prismfall::Cutscene) && Prismfall::Cutscene.respond_to?(:match_highlight)
        begin
          Prismfall::Cutscene.match_highlight(highlight_info(a), highlight_info(b), highlight_info(winner), moments)
          return true
        rescue ArgumentError => e
          Prismfall::Narrative.warn("match_highlight signature mismatch: #{e.message}")
        end
      end
      moments.each { |m| pbMessage(_INTL(m[3].to_s)) }
      return false
    end

    # Announces the NPC results of round r; matches with highlight data offer
    # "Watch the highlights?". Called by next_match after a win (if
    # AUTO_ROUND_RESULTS) or by an event: Prismfall::Festival.show_round_results
    AUTO_ROUND_RESULTS = true

    def self.show_round_results(r = nil)
      return if !started?
      r ||= (state[:last_round] || 0)
      return if r >= ROUNDS
      matches_in_round(r).times do |m|
        a, b = participants(r, m)
        w = winner(r, m)
        next if !a || !b || !w || a == :PLAYER || b == :PLAYER
        loser = (w == a) ? b : a
        pbMessage(_INTL("{1}: {2} defeated {3}.", _INTL(ROUND_NAMES[r]), display_name(w), display_name(loser)))
        rule = (state[:match_rules] || {})[[r, m]]
        rule = MATCH_RULES[rule] if rule
        next if !rule || !rule[:moments] || rule[:moments].empty?
        next if !pbConfirmMessage(_INTL("Watch the highlights?"))
        play_highlight(a, b, w, rule[:moments])
      end
    end

    #---------------------------------------------------------------------------
    # Draw resolution
    #---------------------------------------------------------------------------
    def self.person_of(id)
      e = ENTRANTS[id]
      return (e && e[:person]) ? e[:person] : id
    end

    def self.default_opponent(stage)
      return (stage[:round]) ? PLAYER_PATH[stage[:round]] : stage[:opponent]
    end

    def self.stage_candidates(stage)
      list = (DRAWS[stage[:id]] || []).clone
      default = default_opponent(stage)
      list.push({ :opponent => default, :condition => nil, :fallback => true }) if default
      return list
    end

    def self.resolve_draw(stage, used_persons = [])
      stage_candidates(stage).each do |c|
        next if used_persons.include?(person_of(c[:opponent]))
        next if c[:condition] && !Prismfall::Conditions.evaluate(c[:condition])
        return c
      end
      return nil
    end

    # Seats drawn opponent `opp` in the player's round-r block of `br`.
    # Returns the withdrawn entrant (if the default had to leave), else nil.
    def self.seat_opponent(br, r, opp)
      p = br.index(:PLAYER)
      block = (p >> r) ^ 1
      cur = br.index(opp)
      return nil if cur && (cur >> r) == block
      target = br.index(PLAYER_PATH[r])
      target = (block << r) if !target || (target >> r) != block
      if cur
        br[cur], br[target] = br[target], br[cur]
        return nil
      end
      same = br.index { |e| e != :PLAYER && person_of(e) == person_of(opp) }
      if same && same != target
        br[same] = br[target]   # variant: the default takes its twin's seat
        br[target] = opp
        return nil
      end
      gone = br[target]
      br[target] = opp
      return (gone && person_of(gone) != person_of(opp)) ? gone : nil
    end

    # Called by Festival.start: draws R16-SF (and seeds the :live Final with
    # its default) and builds this run's bracket.
    def self.draw_bracket_stages!
      seats = resolve_delegations
      state[:seats]  = seats
      state[:seated] = seats.values
      br   = seated_bracket(seats)
      pth  = PLAYER_PATH.clone
      used = []
      state[:draws] = {}
      state[:draw_versions] = {}
      withdrawn = []
      STAGES.each do |st|
        next if !st[:round]
        if st[:live]
          used.push(person_of(default_opponent(st)))
          next
        end
        c = resolve_draw(st, used) || { :opponent => default_opponent(st) }
        opp = c[:opponent]
        used.push(person_of(opp))
        pth[st[:round]] = opp
        gone = seat_opponent(br, st[:round], opp)
        withdrawn.push(gone) if gone
        state[:draws][st[:id]] = opp
        state[:draw_versions][st[:id]] = c[:version] if c[:version]
      end
      state[:bracket] = br
      state[:path]    = pth
      withdrawn.each { |id| mark_out(id) }
      EventHandlers.trigger(:prismfall_festival_drawn, pth.clone)
    end

    # Opponent of a live/non-bracket stage (resolved live until its battle starts).
    def self.drawn_opponent(stage)
      locked = drawn(stage[:id])
      return locked if locked
      used = []
      if started?
        path.each_with_index do |id, i|
          next if stage[:round] && i == stage[:round]
          used.push(person_of(id))
        end
      end
      c = resolve_draw(stage, used)
      return (c) ? c[:opponent] : default_opponent(stage)
    end

    def self.lock_draw(stage, opp)
      return if !started?
      state[:draws] ||= {}
      state[:draw_versions] ||= {}
      return if state[:draws][stage[:id]]
      state[:draws][stage[:id]] = opp
      c = stage_candidates(stage).find { |cand| cand[:opponent] == opp }
      state[:draw_versions][stage[:id]] = c[:version] if c && c[:version]
    end

    def self.draw_version(stage, opp)
      return nil if !started? || !state[:draw_versions]
      return nil if drawn(stage[:id]) != opp
      return state[:draw_versions][stage[:id]]
    end

    def self.validate_draws
      errors = []
      owner = {}   # person => stage id
      DRAWS.each_key do |sid|
        errors.push("DRAWS has unknown stage #{sid.inspect}") if !STAGES.any? { |s| s[:id] == sid }
      end
      STAGES.each do |st|
        next if st[:wild]
        cands = stage_candidates(st)
        errors.push("Stage #{st[:id]} has no fallback opponent") if !cands.any? { |c| c[:condition].nil? }
        cands.each do |c|
          id = c[:opponent]
          if !ENTRANTS[id] || id == :PLAYER
            errors.push("Stage #{st[:id]}: unknown opponent #{id.inspect}")
            next
          end
          ok, msg = Prismfall::Conditions.check(c[:condition])
          errors.push("Stage #{st[:id]} #{id}: #{msg}") if !ok
          person = person_of(id)
          if owner[person] && owner[person] != st[:id]
            errors.push("#{person.inspect} is a candidate in both #{owner[person]} and #{st[:id]}")
          end
          owner[person] ||= st[:id]
        end
      end
      DELEGATIONS.each do |seat, cands|
        errors.push("Seat #{seat} isn't in BRACKET_SEATS") if !BRACKET_SEATS.include?(seat)
        errors.push("Seat #{seat} has no unconditional last candidate") if cands.empty? || !cands.last[1].nil?
        cands.each do |id, cond|
          errors.push("Seat #{seat}: unknown entrant #{id.inspect}") if id != :FORFEIT && !ENTRANTS[id]
          ok, msg = Prismfall::Conditions.check(cond)
          errors.push("Seat #{seat} #{id}: #{msg}") if !ok
        end
      end
      errors.push("BRACKET_SEATS must be :PLAYER + the 15 seats") if BRACKET_SEATS.sort_by(&:to_s) != ([:PLAYER] + DELEGATIONS.keys).sort_by(&:to_s)
      FORFEIT_POOL.each { |id| errors.push("FORFEIT_POOL: unknown entrant #{id.inspect}") if !ENTRANTS[id] }
      MATCH_RULES.each_with_index do |rule, i|
        rule[:pair].each { |id| errors.push("MATCH_RULES[#{i}]: unknown entrant #{id.inspect}") if !ENTRANTS[id] }
        errors.push("MATCH_RULES[#{i}]: winner not in pair") if !rule[:pair].include?(rule[:winner])
        ok, msg = Prismfall::Conditions.check(rule[:condition])
        errors.push("MATCH_RULES[#{i}]: #{msg}") if !ok
      end
      begin
        seats = resolve_delegations
        errors.push("Default delegations leave a seat empty or doubled") if seats.values.compact.uniq.length != DELEGATIONS.length
      rescue StandardError => e
        errors.push("Delegations failed to resolve: #{e.message}")
      end
      EXHIBITION_EXTRAS.each do |x|
        errors.push("EXHIBITION_EXTRAS: unknown entrant #{x[:entrant].inspect}") if !ENTRANTS[x[:entrant]]
      end
      ENTRANTS.each do |id, e|
        next if !e[:trainer_type]
        types = Array(e[:trainer_type])
        if Prismfall::Narrative::CAMEOS.keys.any? { |t| types.include?(t) }
          errors.push("#{id}: sister-game cameos aren't Festival entrants (SPINE Revision 4)")
        end
        if types.any? { |t| [:FESTIVAL_ISAURA, :FESTIVAL_DREY, :FESTIVAL_MIREILLE, :FESTIVAL_THORNE].include?(t) }
          errors.push("#{id}: Rev-4 outsiders are retired (SPINE Revision 5)")
        end
      end
      return errors
    end
  end
end

# Load-time check (console only; Festival.start raises in debug mode).
Prismfall::Festival.validate.each { |msg| Prismfall::Narrative.warn("Festival: #{msg}") }
