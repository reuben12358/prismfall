#===============================================================================
# Prismfall Core - 015 Choice-driven Festival draw (SPINE Revision 3)
#-------------------------------------------------------------------------------
# DRAWS[stage_id] is an ordered candidate list; the first candidate whose
# condition holds is the player's opponent for that stage. The stage's default
# (PLAYER_PATH[round], or the stage's :opponent) is always appended as the final
# fallback. Candidate keys:
#   :opponent   entrant ID (ENTRANTS; variants are separate entrants with the
#               same :person, e.g. :KESTREL_FALLEN)
#   :condition  Prismfall::Conditions string (nil = always)
#   :version    trainer version override for this draw (optional)
# Bracket stages (R16-Final) are drawn when Festival.start runs: the drawn
# opponent is seated in the player's path (swapping seats with it if it's
# already seeded, or replacing the default occupant if not). Non-bracket stages
# (Hijack) are drawn live and fixed when their battle starts.
# Validation (at load + Festival.validate): every candidate exists, every
# condition parses, and no person is a candidate in two different stages, so a
# run can never draw the same character twice.
#===============================================================================
module Prismfall
  module Festival
    # Variant / draw-only entrants (SAMPLE until NARRATIVE_KEYS.md).
    ENTRANTS.merge!({
      :KESTREL_FALLEN => { :display => "Kestrel", :person => :KESTREL, :trainer_type => :RIVAL_KESTREL,
                           :name => "Kestrel", :rival_battle => 9, :rating => 94, :level_hint => 94 },   # versions 90-92
      :ROWAN          => { :display => "Rowan", :trainer_type => :LEADER_ROWAN, :name => "Rowan",
                           :version => 50, :rating => 89, :level_hint => 90 },
      :SUCCESSOR      => { :display => "The Successor", :trainer_type => :CHAMPION_SUCCESSOR,
                           :name => "Successor", :version => 0, :rating => 97, :level_hint => 96 },
      :MOURNER        => { :display => "The Mourner", :trainer_type => :HOLLOW_MOURNER, :name => "Mourner",
                           :version => 0, :rating => 98, :level_hint => 98 }
    })

    DRAWS = {
      :R16 => [
        { :opponent => :ROWAN,  :condition => "choice(:rowan_exile) == :exiled && bond(:ROWAN) <= -3" },
        { :opponent => :MELIA,  :condition => "bond(:JUNO) >= 6 && resonance >= 4", :version => 1 }
      ],
      :QF => [
        { :opponent => :NOVA,   :condition => "ruin_route && resonance_band == :ruin", :version => 2 }
      ],
      :SF => [
        { :opponent => :KESTREL_FALLEN, :condition => "bond(:KESTREL) <= -4 || choice(:kestrel_truth) == :betrayed" },
        { :opponent => :TITANIA, :condition => "choice(:kestrel_truth) == :told && bond(:KESTREL) >= 6", :version => 3 }
      ],
      :FINAL => [
        { :opponent => :SUCCESSOR, :condition => "choice(:valen_secret) == :exposed" }
      ],
      :HIJACK => [
        { :opponent => :MOURNER, :condition => "choice(:exposed) == :meridian" }
      ]
    }

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

    # First matching candidate not already used by an earlier stage.
    def self.resolve_draw(stage, used_persons = [])
      stage_candidates(stage).each do |c|
        next if used_persons.include?(person_of(c[:opponent]))
        next if c[:condition] && !Prismfall::Conditions.evaluate(c[:condition])
        return c
      end
      return nil
    end

    # Seats drawn opponent `opp` in the player's round-r block of `br`.
    def self.seat_opponent(br, r, opp)
      p = br.index(:PLAYER)
      block = (p >> r) ^ 1
      cur = br.index(opp)
      return if cur && (cur >> r) == block   # already where it needs to be
      target = BRACKET.index(PLAYER_PATH[r])
      target = (block << r) if !target || (target >> r) != block
      if cur
        br[cur], br[target] = br[target], br[cur]
        return
      end
      same = br.index { |e| e != :PLAYER && person_of(e) == person_of(opp) }
      if same && same != target
        br[same] = br[target]   # the default occupant takes the variant's twin seat
      end
      br[target] = opp
    end

    # Called by Festival.start: draws R16-Final and builds this run's bracket.
    def self.draw_bracket_stages!
      br   = BRACKET.clone
      pth  = PLAYER_PATH.clone
      used = []
      state[:draws] = {}
      state[:draw_versions] = {}
      STAGES.each do |st|
        next if !st[:round]
        c = resolve_draw(st, used) || { :opponent => default_opponent(st) }
        opp = c[:opponent]
        used.push(person_of(opp))
        pth[st[:round]] = opp
        seat_opponent(br, st[:round], opp)
        state[:draws][st[:id]] = opp
        state[:draw_versions][st[:id]] = c[:version] if c[:version]
      end
      state[:bracket] = br
      state[:path]    = pth
      EventHandlers.trigger(:prismfall_festival_drawn, pth.clone)
    end

    # Opponent of a non-bracket stage (live until its battle starts).
    def self.drawn_opponent(stage)
      locked = (started? && state[:draws]) ? state[:draws][stage[:id]] : nil
      return locked if locked
      used = (started?) ? path.map { |id| person_of(id) } : []
      c = resolve_draw(stage, used)
      return (c) ? c[:opponent] : stage[:opponent]
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
      return nil if state[:draws].nil? || state[:draws][stage[:id]] != opp
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
      return errors
    end
  end
end

# Load-time check (console only; Festival.start raises in debug mode).
Prismfall::Festival.validate.each { |msg| Prismfall::Narrative.warn("Festival: #{msg}") }
