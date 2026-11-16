#===============================================================================
# Prismfall Core - 009 Festival of Champions: tournament manager
#-------------------------------------------------------------------------------
# Story-locked 16-entrant bracket with persistent state in $prismfall.festival.
# (PWT, shipped with the base project, is a random 8-trainer map-event
# tournament with no persistence, so it isn't used here; it stays available for
# post-game facilities and composes with Core's hooks.)
#
# State hash (Marshal-safe: Symbols, Integers, Arrays, Hashes only):
#   :active      true between start and finish
#   :stage       index into STAGES of the player's next battle
#   :results     { [round, match] => winner_id }
#   :seed        RNG seed for simulated NPC matches (stable per save)
#   :exhibitions { entrant_id => :won / :lost }
#   :losses      number of lost (retried) player matches
#   :finished    true after the final stage
#   :champion    bracket winner (entrant id) once the Final is decided
#===============================================================================
module Prismfall
  module Festival
    BRACKET_SIZE = 16
    ROUNDS = 4

    #---------------------------------------------------------------------------
    # State
    #---------------------------------------------------------------------------
    def self.state
      return Prismfall.state.festival
    end

    def self.new_state
      return {
        :active => true, :stage => 0, :results => {}, :seed => rand(1 << 30),
        :exhibitions => {}, :losses => 0, :finished => false, :champion => nil
      }
    end

    def self.started?;  return state.is_a?(Hash);                 end
    def self.active?;   return started? && state[:active] == true; end
    def self.finished?; return started? && state[:finished] == true; end
    def self.results;   return (started?) ? state[:results] : {};  end
    def self.champion;  return (started?) ? state[:champion] : nil; end

    # Event usage: Script: Prismfall::Festival.start
    # Returns false if the player doesn't hold all 18 badges (unless force).
    def self.start(force: false)
      if !force && !Prismfall.all_badges?
        pbMessage(_INTL("You need all {1} badges to enter the Festival of Champions.", Prismfall::BADGE_COUNT))
        return false
      end
      if $DEBUG
        errors = validate
        raise "Festival data invalid:\n" + errors.join("\n") if !errors.empty?
      end
      if !active? || finished?
        old = state
        Prismfall.state.festival = new_state
        state[:exhibitions] = old[:exhibitions] if old.is_a?(Hash) && old[:exhibitions]
        draw_bracket_stages!
      end
      EventHandlers.trigger(:prismfall_festival_started)
      return true
    end

    def self.reset!
      Prismfall.state.festival = nil
    end

    #---------------------------------------------------------------------------
    # Entrants
    #---------------------------------------------------------------------------
    def self.entrant(id)
      return ENTRANTS[id]
    end

    def self.display_name(id)
      return "???" if id.nil?
      return ($player) ? $player.name : _INTL("You") if id == :PLAYER
      e = entrant(id)
      return id.to_s if !e
      return _INTL(e[:display]) if e[:display]
      return Array(e[:name]).first.to_s
    end

    # [trainer_type, name] that exists for `version` (or the first candidates).
    def self.resolve_trainer(e, version)
      types = Array(e[:trainer_type])
      names = Array(e[:name])
      types.each do |tt|
        next if !GameData::TrainerType.exists?(tt)
        names.each do |nm|
          return [tt, nm] if GameData::Trainer.exists?(tt, nm, version)
        end
      end
      return [types.first, names.first]
    end

    def self.rating(id)
      e = entrant(id)
      return (e && e[:rating]) ? e[:rating].to_f : 50.0
    end

    #---------------------------------------------------------------------------
    # Bracket structure
    #---------------------------------------------------------------------------
    # Seeding / player path for this run (set by the draw at start), falling
    # back to the default BRACKET / PLAYER_PATH constants.
    def self.bracket
      return (started? && state[:bracket].is_a?(Array)) ? state[:bracket] : BRACKET
    end

    def self.path
      return (started? && state[:path].is_a?(Array)) ? state[:path] : PLAYER_PATH
    end

    def self.player_slot
      return bracket.index(:PLAYER)
    end

    def self.matches_in_round(r)
      return BRACKET_SIZE >> (r + 1)
    end

    def self.player_match_index(r)
      return player_slot >> (r + 1)
    end

    # The two entrants of match m in round r (nil while still undecided).
    def self.participants(r, m)
      return [bracket[2 * m], bracket[(2 * m) + 1]] if r == 0
      return [results[[r - 1, 2 * m]], results[[r - 1, (2 * m) + 1]]]
    end

    def self.winner(r, m)
      return results[[r, m]]
    end

    # Round in which entrant id was knocked out (nil = still in / champion).
    def self.eliminated_in(id)
      ROUNDS.times do |r|
        matches_in_round(r).times do |m|
          a, b = participants(r, m)
          next if a != id && b != id
          w = winner(r, m)
          return r if w && w != id
        end
      end
      return nil
    end

    # Checks seeding against PLAYER_PATH. Returns an array of error strings.
    def self.validate
      errors = []
      errors.push("BRACKET must have #{BRACKET_SIZE} entries") if BRACKET.length != BRACKET_SIZE
      errors.push("BRACKET has duplicate entrants") if BRACKET.uniq.length != BRACKET.length
      BRACKET.each { |id| errors.push("Unknown entrant #{id.inspect}") if !ENTRANTS[id] }
      p = player_slot
      if !p
        errors.push("BRACKET has no :PLAYER")
        return errors
      end
      PLAYER_PATH.each_with_index do |opp, r|
        s = BRACKET.index(opp)
        if !s
          errors.push("PLAYER_PATH entrant #{opp.inspect} is not in BRACKET")
        elsif (s >> r) != ((p >> r) ^ 1)
          errors.push("#{opp.inspect} can't meet the player in #{ROUND_NAMES[r]} with this seeding")
        end
      end
      STAGES.each do |st|
        errors.push("Stage #{st[:id]} uses unknown ruleset #{st[:ruleset].inspect}") if !RULESETS[st[:ruleset]]
      end
      errors.concat(validate_draws) if respond_to?(:validate_draws)
      return errors
    end

    #---------------------------------------------------------------------------
    # NPC-vs-NPC results
    #---------------------------------------------------------------------------
    def self.npc_winner(a, b, r, m)
      # Player-path entrants always advance until they meet the player.
      ka = path.index(a)
      kb = path.index(b)
      return a if ka && ka > r
      return b if kb && kb > r
      scripted = SCRIPTED_WINNERS[[r, m]]
      return scripted if scripted && [a, b].include?(scripted)
      ra = rating(a)
      rb = rating(b)
      if SIMULATE_UNSCRIPTED
        wa = ra**SIMULATION_SHARPNESS
        wb = rb**SIMULATION_SHARPNESS
        rng = Random.new(state[:seed] + (r * 101) + m)
        return (rng.rand < wa / (wa + wb)) ? a : b
      end
      return (ra >= rb) ? a : b
    end

    # Decides every undecided NPC match of round r whose entrants are known.
    def self.resolve_round(r)
      return if !started?
      matches_in_round(r).times do |m|
        next if results[[r, m]]
        a, b = participants(r, m)
        next if !a || !b
        next if a == :PLAYER || b == :PLAYER   # the player's matches are played
        w = npc_winner(a, b, r, m)
        results[[r, m]] = w
        mark_out((w == a) ? b : a)
      end
      state[:champion] = results[[ROUNDS - 1, 0]] if results[[ROUNDS - 1, 0]]
    end

    #---------------------------------------------------------------------------
    # Stages
    #---------------------------------------------------------------------------
    def self.stage_index
      return (started?) ? state[:stage] : 0
    end

    def self.current_stage
      return nil if !active? || finished?
      return STAGES[stage_index]
    end

    def self.stage_id
      st = current_stage
      return (st) ? st[:id] : nil
    end

    def self.current_stage_name
      st = current_stage
      return (st) ? _INTL(st[:name]) : ""
    end

    def self.opponent_id(stage = nil)
      stage ||= current_stage
      return nil if !stage
      return drawn_opponent(stage) if !stage[:round] || stage[:live]
      r = stage[:round]
      a, b = participants(r, player_match_index(r))
      opp = (a == :PLAYER) ? b : a
      return opp || path[r]
    end

    def self.current_opponent_name
      st = current_stage
      return "" if !st
      return GameData::Species.get(st[:wild]).name if st[:wild]
      return display_name(opponent_id(st))
    end

    def self.ruleset(key)
      return RULESETS[key] || RULESETS[:bracket]
    end

    #---------------------------------------------------------------------------
    # Rules / eligibility / healing
    #---------------------------------------------------------------------------
    def self.heal
      $player.heal_party
    end

    # Party Pokémon above the rule set's level limit.
    def self.over_limit(rules)
      return [] if !rules[:enforce_level] || !rules[:level_cap]
      return $player.party.select { |pkmn| pkmn && !pkmn.egg? && pkmn.level > rules[:level_cap] }
    end

    def self.party_eligible?(rules, show_message = true)
      offenders = over_limit(rules)
      return true if offenders.empty?
      if show_message
        names = offenders.map { |pkmn| pkmn.name }.join(", ")
        pbMessage(_INTL("Festival rules: Pokémon above Lv. {1} can't take part. ({2})", rules[:level_cap], names))
      end
      return false
    end

    def self.apply_battle_rules(rules, field = nil, extra_rules = nil)
      setBattleRule("canLose")    if rules[:can_lose]
      setBattleRule("noBagItems") if rules[:bag_items] == false
      setBattleRule("noExp")      if rules[:exp] == false
      setBattleRule("noMoney")    if rules[:money] == false
      Prismfall.set_field_rule(field) if field
      (extra_rules || []).each { |r| setBattleRule(r) }
    end

    # Raises the level cap for a Festival stage (never lowers it). Caps between
    # FESTIVAL_CAP and FESTIVAL_FINALE_CAP use the story override; the finale cap
    # clears that override and unlocks FESTIVAL_FINALE_CAP.
    def self.unlock_cap_for(rules)
      cap = rules[:level_cap]
      return if !cap.is_a?(Integer)
      state = Prismfall.state
      if cap >= FESTIVAL_FINALE_CAP
        state.level_cap_override = nil if state.level_cap_override.is_a?(Integer) &&
                                          state.level_cap_override < FESTIVAL_FINALE_CAP
        Prismfall::LevelCap.unlock_finale!
      elsif cap > FESTIVAL_CAP
        cur = state.level_cap_override
        state.level_cap_override = cap if !cur.is_a?(Integer) || cur < cap
      end
    end

    #---------------------------------------------------------------------------
    # Battles
    #---------------------------------------------------------------------------
    # version: explicit trainer version (e.g. from a draw candidate).
    def self.battle_entrant(id, exhibition: false, lose_text: nil, version: nil)
      e = entrant(id)
      raise ArgumentError, "Unknown Festival entrant #{id.inspect}" if !e || id == :PLAYER
      if e[:rival_battle] && version.nil?
        return Prismfall::Rival.battle(Array(e[:trainer_type]).first, Array(e[:name]).first,
                                       e[:rival_battle], lose_text: lose_text)
      end
      version ||= ((exhibition) ? e[:exhibition_version] : nil) || e[:version] || 0
      if e[:double]   # two trainers side by side (arrays are trainer pairs, not candidates)
        setBattleRule("double")
        foes = Array(e[:trainer_type]).each_with_index.map { |tt, i| [tt, Array(e[:name])[i], version] }
        foes[-1].push(lose_text) if lose_text
        return TrainerBattle.start(*foes)
      end
      tr_type, tr_name = resolve_trainer(e, version)
      return TrainerBattle.start([tr_type, tr_name, version, lose_text])
    end

    def self.boss_battle(stage)
      species = stage[:wild]
      level   = stage[:level] || 100
      boss    = stage[:boss]
      if boss && defined?(EliteBattle) && EliteBattle.respond_to?(:bossBattle)
        return EliteBattle.bossBattle(species, level, boss[:player_side] || 1,
                                      boss[:can_catch] ? true : false, boss[:options] || {})
      end
      pkmn = Pokemon.new(species, level)
      ARCEUS_SETUP.call(pkmn) if ARCEUS_SETUP && species == :ARCEUS
      EventHandlers.trigger(:prismfall_festival_boss, pkmn, stage[:id])
      return WildBattle.start(pkmn)
    end

    # Plays the player's next Festival battle. Event usage:
    #   Conditional Branch > Script: Prismfall::Festival.next_match
    # Returns true on a win (state advances), false on a loss/refusal (the
    # match can simply be retried).
    def self.next_match(lose_text: nil)
      st = current_stage
      return false if !st
      rules = ruleset(st[:ruleset])
      unlock_cap_for(rules)
      return false if !party_eligible?(rules)
      heal if rules[:heal_before]
      EventHandlers.trigger(:prismfall_festival_before_battle, st[:id], opponent_id(st))
      apply_battle_rules(rules, st[:field], st[:rules])
      if st[:wild]
        won = boss_battle(st)
      else
        opp = opponent_id(st)
        lock_draw(st, opp)   # a live/non-bracket stage's draw is fixed once its battle starts
        Prismfall::Ledger.record_met(opp)
        won = battle_entrant(opp, lose_text: lose_text, version: draw_version(st, opp))
      end
      won = (won) ? true : false
      record_result(won)
      heal if rules[:heal_after]
      return won
    end

    # Records the outcome of the current stage. Use directly if an event runs
    # the battle itself (e.g. a scripted double battle).
    def self.record_result(won)
      st = current_stage
      return false if !st
      if !won
        state[:losses] += 1
        EventHandlers.trigger(:prismfall_festival_result, st[:id], false)
        return false
      end
      if st[:round]
        r = st[:round]
        a, b = participants(r, player_match_index(r))
        results[[r, player_match_index(r)]] = :PLAYER
        mark_out((a == :PLAYER) ? b : a)
        resolve_round(r)
      end
      state[:stage] += 1
      EventHandlers.trigger(:prismfall_festival_result, st[:id], true)
      finish! if state[:stage] >= STAGES.length
      return true
    end

    def self.finish!
      return if !started?
      state[:finished] = true
      state[:active]   = false
      state[:champion] ||= :PLAYER
      Prismfall::LevelCap.unlock_finale!
      EventHandlers.trigger(:prismfall_festival_finished, state[:champion])
    end

    #---------------------------------------------------------------------------
    # Exhibition matches (optional battles during Festival week)
    #---------------------------------------------------------------------------
    # Exhibition opponents (NARRATIVE_KEYS 6.5): entrants flagged :exhibition
    # open from the day after they're knocked out (or withdraw); EXHIBITION_EXTRAS
    # (015) add more. None on the Ruin Route (its Eevee Octave is event-run).
    def self.exhibition_ids
      return [] if Prismfall.ruin_route?
      ids = []
      if started?
        ENTRANTS.each_key do |id|
          next if !ENTRANTS[id][:exhibition]
          d = (state[:out_day] || {})[id]
          ids.push(id) if d && day > d
        end
      end
      EXHIBITION_EXTRAS.each do |x|
        next if ids.include?(x[:entrant])
        next if x[:from_day] && day < x[:from_day]
        next if x[:condition] && !Prismfall::Conditions.evaluate(x[:condition])
        ids.push(x[:entrant])
      end
      return ids
    end

    def self.exhibition_version(id)
      x = EXHIBITION_EXTRAS.find { |e| e[:entrant] == id && e[:version] }
      return (x) ? x[:version] : nil
    end

    def self.exhibition_result(id)
      return (started?) ? state[:exhibitions][id] : nil
    end

    # Event usage: Script: Prismfall::Festival.exhibition(:CAMEO_3)
    def self.exhibition(id, lose_text: nil, force: false)
      raise ArgumentError, "#{id.inspect} has no exhibition match today" if !force && !exhibition_ids.include?(id)
      if !started?   # exhibitions before the bracket opens: keep the Festival inactive
        Prismfall.state.festival = new_state
        state[:active] = false
      end
      rules = ruleset(:exhibition)
      return false if !party_eligible?(rules)
      heal if rules[:heal_before]
      apply_battle_rules(rules)
      setBattleRule("double") if entrant(id)[:exhibition_double]
      Prismfall::Ledger.record_met(id)
      won = battle_entrant(id, exhibition: true, lose_text: lose_text,
                           version: exhibition_version(id)) ? true : false
      state[:exhibitions][id] = :won if won
      state[:exhibitions][id] ||= :lost
      heal if rules[:heal_after]
      return won
    end

    # Choice list of exhibition opponents. Returns the battle result, or nil if
    # cancelled.
    def self.exhibition_menu
      ids = exhibition_ids
      return nil if ids.empty?
      cmds = ids.map do |id|
        res = exhibition_result(id)
        (res == :won) ? _INTL("{1} (won)", display_name(id)) : display_name(id)
      end
      cmds.push(_INTL("Cancel"))
      idx = pbMessage(_INTL("Who will you challenge to an exhibition match?"), cmds, cmds.length)
      return nil if idx < 0 || idx >= ids.length
      return exhibition(ids[idx])
    end

    #---------------------------------------------------------------------------
    # Debug helpers
    #---------------------------------------------------------------------------
    # Marks every stage before `stage_id` as won (bracket gets filled in).
    def self.debug_skip_to(stage_id)
      start(force: true) if !active?
      target = STAGES.index { |s| s[:id] == stage_id }
      return false if !target
      record_result(true) while state[:stage] < target && current_stage
      return true
    end

    def self.summary_lines
      lines = []
      ROUNDS.times do |r|
        matches_in_round(r).times do |m|
          a, b = participants(r, m)
          w = winner(r, m)
          lines.push(sprintf("%s %d: %s vs %s -> %s", ROUND_NAMES[r], m + 1, display_name(a),
                             display_name(b), (w) ? display_name(w) : "-"))
        end
      end
      return lines
    end
  end
end
