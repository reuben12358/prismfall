#===============================================================================
# Prismfall Core - 024 Narrative data validation (NARRATIVE_KEYS section 15)
#-------------------------------------------------------------------------------
# Prismfall::NarrativeCheck.run -> array of error strings (empty = OK).
# Runs at load (console warnings in debug) and from Debug > Prismfall Core >
# Show Core status. Walks every condition string in the data tables.
#===============================================================================
module Prismfall
  module NarrativeCheck
    module_function

    # [label, condition] for every condition string Core knows about.
    def all_conditions
      n = Prismfall::Narrative
      list = []
      n::DERIVED_FLAGS.each { |k, c| list.push(["flag #{k}", c]) }
      n::TALLIES.each { |k, arr| arr.each_with_index { |c, i| list.push(["tally #{k}[#{i}]", c]) } }
      n::ENDING_RULES.each { |id, c| list.push(["ending #{id}", c]) }
      n::MIRROR_SWITCHES.each { |sw, c| list.push(["mirror S#{sw}", c]) }
      fe = Prismfall::Festival
      fe::DRAWS.each { |st, cands| cands.each { |c| list.push(["draw #{st} #{c[:opponent]}", c[:condition]]) if c[:condition] } }
      fe::DELEGATIONS.each { |seat, cands| cands.each { |id, c| list.push(["seat #{seat} #{id}", c]) if c } }
      fe::MATCH_RULES.each_with_index { |r, i| list.push(["match rule #{i}", r[:condition]]) if r[:condition] }
      if fe.const_defined?(:EXHIBITION_EXTRAS)
        fe::EXHIBITION_EXTRAS.each { |x| list.push(["exhibition #{x[:entrant]}", x[:condition]]) if x[:condition] }
      end
      if fe.const_defined?(:ARCEUS_VARIANTS)
        fe::ARCEUS_VARIANTS.each { |v| list.push(["arceus #{v[:id]}", v[:condition]]) if v[:condition] }
      end
      return list
    end

    def walk(node, &block)
      return if !node.is_a?(Array)
      yield node
      node.each { |child| walk(child, &block) if child.is_a?(Array) }
    end

    def lit(node)
      return (node.is_a?(Array) && node[0] == :lit) ? node[1] : :__dynamic__
    end

    def check_choice(errors, label, key, value = :__none__)
      return if key == :__dynamic__
      ch = Prismfall::Narrative::CHOICES[key]
      if !ch
        errors.push("#{label}: unknown choice #{key.inspect}")
        return
      end
      return if value == :__none__ || value == :__dynamic__ || value.nil? || ch[:values].nil?
      errors.push("#{label}: #{value.inspect} isn't a value of #{key.inspect}") if !ch[:values].include?(value)
    end

    def flag_refs(cond)
      refs = []
      ast = Prismfall::Conditions.parse(cond)
      walk(ast) { |nd| refs.push(lit(nd[2][0])) if nd[0] == :call && nd[1] == "flag" }
      return refs
    rescue Prismfall::Conditions::Error
      return []
    end

    def run
      n = Prismfall::Narrative
      errors = []
      all_conditions.each do |label, cond|
        ok, msg = Prismfall::Conditions.check(cond)
        if !ok
          errors.push("#{label}: #{msg}")
          next
        end
        walk(Prismfall::Conditions.parse(cond)) do |nd|
          case nd[0]
          when :call
            args = nd[2].map { |a| lit(a) }
            case nd[1]
            when "choice", "made" then check_choice(errors, label, args[0])
            when "chose"          then check_choice(errors, label, args[0], args[1])
            when "flag"
              errors.push("#{label}: unknown flag #{args[0].inspect}") if args[0] != :__dynamic__ && !n::DERIVED_FLAGS.has_key?(args[0])
            when "tally"
              errors.push("#{label}: unknown tally #{args[0].inspect}") if args[0] != :__dynamic__ && !n::TALLIES.has_key?(args[0])
            when "bond", "bond_tier"
              errors.push("#{label}: unknown bond #{args[0].inspect}") if args[0] != :__dynamic__ && !n::BONDS.has_key?(args[0])
            when "standing", "standing_tier"
              errors.push("#{label}: unknown faction #{args[0].inspect}") if args[0] != :__dynamic__ && !n::FACTIONS.has_key?(args[0])
            end
          when :cmp
            [[nd[2], nd[3]], [nd[3], nd[2]]].each do |a, b|
              next if !a.is_a?(Array) || a[0] != :call || a[1] != "choice"
              check_choice(errors, label, lit(a[2][0]), lit(b))
            end
          end
        end
      end
      # Flag cycles (depth-first search over flag -> flag references)
      state = {}
      visit = lambda do |f, path|
        return if state[f] == :done
        if state[f] == :active
          errors.push("flag cycle: #{(path + [f]).join(' -> ')}")
          return
        end
        state[f] = :active
        flag_refs(n::DERIVED_FLAGS[f].to_s).each { |g| visit.call(g, path + [f]) if n::DERIVED_FLAGS.has_key?(g) }
        state[f] = :done
      end
      n::DERIVED_FLAGS.each_key { |f| visit.call(f, []) }
      # Choice effects
      n::CHOICE_EFFECTS.each do |key, vals|
        check_choice(errors, "effects", key)
        vals.each do |v, text|
          check_choice(errors, "effects #{key}", key, v)
          text.to_s.split(/\s+/).each do |tok|
            m = /\A([A-Za-z_]+)[+-]\d+\z/.match(tok)
            if !m
              errors.push("effects #{key}.#{v}: bad token #{tok.inspect}")
              next
            end
            id = m[1].upcase.to_sym
            next if id == :RES || n::BONDS.has_key?(id) || n::FACTIONS.has_key?(id)
            errors.push("effects #{key}.#{v}: #{id} is not a Bond or faction")
          end
        end
      end
      # Aliases
      n::CHOICE_ALIASES.each { |a, c| errors.push("choice alias #{a} -> unknown #{c}") if !n::CHOICES.has_key?(c) }
      n::GAME_OVER_ALIASES.each { |a, c| errors.push("game over alias #{a} -> unknown #{c}") if !n::GAME_OVERS.has_key?(c) }
      # Endings
      n::ENDING_RULES.each { |id, _c| errors.push("ENDING_RULES names unknown ending #{id}") if !n::ENDINGS.has_key?(id) }
      errors.push("DEFAULT_ENDING is not registered") if !n::ENDINGS.has_key?(n::DEFAULT_ENDING)
      final = n::CHOICES[:ch21_final]
      if final && final[:values]
        rules_text = n::ENDING_RULES.map { |r| r[1].to_s }.join(" ")
        final[:values].each do |v|
          next if rules_text.include?("choice(:ch21_final) == :#{v}")
          errors.push("ENDING_RULES never handles :ch21_final #{v.inspect}")
        end
      end
      errors.push("WARDEN_CONSENT must have 18 entries (has #{n::WARDEN_CONSENT.size})") if n::WARDEN_CONSENT.size != 18
      # Festival
      errors.concat(Prismfall::Festival.validate.map { |e| "Festival: #{e}" })
      return errors
    end
  end
end

Prismfall::NarrativeCheck.run.each { |msg| Prismfall::Narrative.warn(msg) }
