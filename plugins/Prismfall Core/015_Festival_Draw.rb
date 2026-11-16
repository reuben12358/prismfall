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
# Also here: Festival days (exhibitions), drawn(:STAGE), ARCEUS_VARIANTS.
#===============================================================================
module Prismfall
  module Festival
    DRAWS = {
      :R16 => [   # default :JUNO (J4)
        { :opponent => :MARISOL, :condition => "!ruin_route && !flag(:TEO_SAVED) && bond(:MARISOL) <= 2" },
        { :opponent => :ANJA,    :condition => "!ruin_route && flag(:ANJA_EXPOSED)" },
        { :opponent => :ROWAN,   :condition => "!ruin_route && flag(:ROWAN_ALIVE) && choice(:ch13_rowan_testimony) == :mercy && standing(:HOLLOW) >= 4" }
      ],
      :QF => [    # default :ISAURA (v2)
        { :opponent => :DASK,      :condition => "ruin_route" },
        { :opponent => :CELESTINE, :condition => "resonance <= -3",                         :version => 92 },
        { :opponent => :KAITO,     :condition => "choice(:ch19_oath) == :keep",             :version => 92 },
        { :opponent => :YSOLDE,    :condition => "flag(:KESTREL_FALLEN)" },
        { :opponent => :MIREILLE,  :condition => "tally(:WARM_BONDS) >= 5 && resonance >= 2" }
      ],
      :SF => [    # default :KESTREL (K8); the Ruin Route uses the same team with Ruin dialogue
        { :opponent => :KESTREL_FALLEN, :condition => "!ruin_route && flag(:KESTREL_FALLEN)" }
      ],
      :FINAL => [ # default :VALEN; stage is :live (drawn on Day 7)
        { :opponent => :VALEN_RUIN, :condition => "ruin_route" },
        { :opponent => :SIGRUN,     :condition => "flag(:VALEN_COLLAPSED) && bond(:SIGRUN) >= 5", :version => 96 },
        { :opponent => :BRANN,      :condition => "flag(:VALEN_COLLAPSED)" }
      ],
      :HIJACK => [ # default :VOSS (drawn live)
        { :opponent => :THEODRIC, :condition => "ruin_route" },
        { :opponent => :QUENT,    :condition => "flag(:VOSS_DISCREDITED)" }
      ]
    }

    # Offered in addition to knocked-out :exhibition entrants (NARRATIVE_KEYS 6.5).
    EXHIBITION_EXTRAS = [
      { :entrant => :PAGEANT_BOUT, :condition => "!ruin_route", :from_day => 3 },
      { :entrant => :BASTIAN,      :condition => "!ruin_route", :from_day => 5 },
      { :entrant => :JUNO,         :condition => "!ruin_route && drawn(:R16) != :JUNO", :from_day => 3 },
      { :entrant => :MARISOL,      :condition => "!ruin_route && drawn(:R16) != :MARISOL && flag(:TEO_SAVED) && bond(:MARISOL) >= 5", :from_day => 3 },
      { :entrant => :ISAURA,       :condition => "!ruin_route && drawn(:QF) != :ISAURA", :from_day => 5 },
      { :entrant => :MIREILLE,     :condition => "!ruin_route && drawn(:QF) != :MIREILLE", :from_day => 3 },
      { :entrant => :MORWEN,       :condition => "!ruin_route && flag(:KESTREL_YSOLDE_RECONCILED) && choice(:ch15_kestrel) == :resolve", :from_day => 5 }
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
      target = BRACKET.index(PLAYER_PATH[r])
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
      br   = BRACKET.clone
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
      EXHIBITION_EXTRAS.each do |x|
        errors.push("EXHIBITION_EXTRAS: unknown entrant #{x[:entrant].inspect}") if !ENTRANTS[x[:entrant]]
      end
      ENTRANTS.each do |id, e|
        next if !e[:trainer_type]
        types = Array(e[:trainer_type])
        if Prismfall::Narrative::CAMEOS.keys.any? { |t| types.include?(t) }
          errors.push("#{id}: sister-game cameos aren't Festival entrants (SPINE Revision 4)")
        end
      end
      return errors
    end
  end
end

# Load-time check (console only; Festival.start raises in debug mode).
Prismfall::Festival.validate.each { |msg| Prismfall::Narrative.warn("Festival: #{msg}") }
