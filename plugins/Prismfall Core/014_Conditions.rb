#===============================================================================
# Prismfall Core - 014 Safe condition evaluator
#-------------------------------------------------------------------------------
# Evaluates data-table strings such as
#   "bond(:JUNO) >= 3 && choice(:mourner_fate) == :spare"
# with a small parser. It never calls eval: only the whitelisted functions below
# can run.
# Grammar:
#   expr  := or ;  or := and (('||'|'or') and)* ;  and := not (('&&'|'and') not)*
#   not   := ('!'|'not') not | cmp ;  cmp := sum (('=='|'!='|'>='|'<='|'>'|'<') sum)?
#   sum   := unary (('+'|'-') unary)* ;  unary := '-' unary | atom
#   atom  := '(' expr ')' | INT | :SYMBOL | "string" | 'string' | true | false | nil
#          | NAME | NAME '(' [expr (',' expr)*] ')'      (NAME = whitelisted function)
# nil counts as 0 in arithmetic and < > comparisons. An empty condition is true.
#===============================================================================
module Prismfall
  module Conditions
    class Error < StandardError; end

    # name => [arity, proc]; arity -1 = any.
    FUNCTIONS = {
      "bond"           => [1, proc { |id| Prismfall::Bonds.get(id) }],
      "bond_tier"      => [1, proc { |id| Prismfall::Bonds.tier(id) }],
      "standing"       => [1, proc { |f| Prismfall::Standing.get(f) }],
      "standing_tier"  => [1, proc { |f| Prismfall::Standing.tier(f) }],
      "resonance"      => [0, proc { Prismfall::Resonance.value }],
      "resonance_band" => [0, proc { Prismfall::Resonance.band }],
      "choice"         => [1, proc { |k| Prismfall::Choices.get(k) }],
      "made"           => [1, proc { |k| Prismfall::Choices.made?(k) }],
      "chose"          => [2, proc { |k, v| Prismfall::Choices.get(k) == v }],
      "badges"         => [0, proc { Prismfall.badge_count }],
      "has_badge"      => [1, proc { |n| Prismfall.has_badge?(n) }],
      "difficulty"     => [0, proc { Prismfall::Difficulty.current }],
      "level_cap"      => [0, proc { Prismfall::LevelCap.current }],
      "starter_slot"   => [0, proc { Prismfall::Rival.starter_slot }],
      "starter_gen"    => [0, proc { Prismfall::Rival.starter_gen }],
      "password"       => [1, proc { |id| Prismfall::Passwords.active?(id) }],
      "gameover_found" => [1, proc { |id| Prismfall::Ledger.game_over_found?(id) }],
      "gameovers_found" => [0, proc { Prismfall::Ledger.game_overs_found.length }],
      "ending_seen"    => [1, proc { |id| Prismfall::Ledger.ending_seen?(id) }],
      "ruin_unlocked"  => [0, proc { Prismfall::Ledger.ruin_unlocked? }],
      "ruin_route"     => [0, proc { Prismfall.ruin_route? }],
      "festival_stage" => [0, proc { Prismfall::Festival.stage_id }],
      "eliminated"     => [1, proc { |id| Prismfall::Festival.out?(id) }],
      "drawn"          => [1, proc { |stage| Prismfall::Festival.drawn(stage) }],
      "festival_day"   => [0, proc { Prismfall::Festival.day }],
      "flag"           => [1, proc { |n| Prismfall::Narrative.flag(n) }],
      "tally"          => [1, proc { |n| Prismfall::Narrative.tally(n) }],
      "cameo_beaten"   => [1, proc { |t| Prismfall::Ledger.cameo_beaten?(t) }],
      "met"            => [1, proc { |id| Prismfall::Ledger.met?(id) }],
      "switch"         => [1, proc { |n| $game_switches ? $game_switches[n] : false }],   # read-only
      "var"            => [1, proc { |n| $game_variables ? $game_variables[n] : 0 }]     # read-only
    }

    TOKEN_RE = /\s*(?:(\d+)|(:[A-Za-z_][A-Za-z0-9_]*[?!]?)|"([^"]*)"|'([^']*)'|([A-Za-z_][A-Za-z0-9_]*\??)|(&&|\|\||==|!=|>=|<=|[><!()+\-,]))/

    @cache = {}

    def self.tokenize(text)
      tokens = []
      pos = 0
      text = text.to_s
      while pos < text.length
        break if text[pos..-1].strip.empty?
        m = TOKEN_RE.match(text, pos)
        raise Error, "Unexpected character at #{pos} in #{text.inspect}" if !m || m.begin(0) != pos
        if m[1]    then tokens.push([:lit, m[1].to_i])
        elsif m[2] then tokens.push([:lit, m[2][1..-1].to_sym])
        elsif m[3] then tokens.push([:lit, m[3]])
        elsif m[4] then tokens.push([:lit, m[4]])
        elsif m[5]
          case m[5]
          when "true"  then tokens.push([:lit, true])
          when "false" then tokens.push([:lit, false])
          when "nil"   then tokens.push([:lit, nil])
          when "and"   then tokens.push([:op, "&&"])
          when "or"    then tokens.push([:op, "||"])
          when "not"   then tokens.push([:op, "!"])
          else              tokens.push([:name, m[5]])
          end
        else
          tokens.push([:op, m[6]])
        end
        pos = m.end(0)
      end
      return tokens
    end

    class Parser
      def initialize(tokens, text)
        @t = tokens
        @i = 0
        @text = text
      end

      def parse
        node = parse_or
        raise Error, "Unexpected #{peek.inspect} in #{@text.inspect}" if peek
        return node
      end

      private

      def peek;     return @t[@i];                  end
      def op?(s);   return peek && peek[0] == :op && peek[1] == s; end
      def advance;  @i += 1; return @t[@i - 1];      end

      def expect(s)
        raise Error, "Expected '#{s}' in #{@text.inspect}" if !op?(s)
        advance
      end

      def parse_or
        node = parse_and
        while op?("||")
          advance
          node = [:or, node, parse_and]
        end
        return node
      end

      def parse_and
        node = parse_not
        while op?("&&")
          advance
          node = [:and, node, parse_not]
        end
        return node
      end

      def parse_not
        if op?("!")
          advance
          return [:not, parse_not]
        end
        return parse_cmp
      end

      def parse_cmp
        node = parse_sum
        ["==", "!=", ">=", "<=", ">", "<"].each do |o|
          next if !op?(o)
          advance
          return [:cmp, o, node, parse_sum]
        end
        return node
      end

      def parse_sum
        node = parse_unary
        while op?("+") || op?("-")
          o = advance[1]
          node = [:arith, o, node, parse_unary]
        end
        return node
      end

      def parse_unary
        if op?("-")
          advance
          return [:arith, "-", [:lit, 0], parse_unary]
        end
        return parse_atom
      end

      def parse_atom
        tok = peek
        raise Error, "Unexpected end of #{@text.inspect}" if !tok
        if op?("(")
          advance
          node = parse_or
          expect(")")
          return node
        end
        case tok[0]
        when :lit
          advance
          return [:lit, tok[1]]
        when :name
          advance
          name = tok[1]
          fn = FUNCTIONS[name]
          raise Error, "Unknown function '#{name}' in #{@text.inspect}" if !fn
          args = []
          if op?("(")
            advance
            if !op?(")")
              args.push(parse_or)
              while op?(",")
                advance
                args.push(parse_or)
              end
            end
            expect(")")
          end
          if fn[0] >= 0 && args.length != fn[0]
            raise Error, "'#{name}' takes #{fn[0]} argument(s), got #{args.length} in #{@text.inspect}"
          end
          return [:call, name, args]
        end
        raise Error, "Unexpected #{tok[1].inspect} in #{@text.inspect}"
      end
    end

    def self.parse(text)
      key = text.to_s
      return @cache[key] if @cache.has_key?(key)
      ast = (key.strip.empty?) ? [:lit, true] : Parser.new(tokenize(key), key).parse
      @cache[key] = ast
      return ast
    end

    # [true, nil] or [false, "error message"] - parses only, doesn't evaluate.
    def self.check(text)
      parse(text)
      return [true, nil]
    rescue Error => e
      return [false, e.message]
    end

    def self.valid?(text)
      return check(text)[0]
    end

    def self.num(v)
      return 0 if v.nil?
      return v if v.is_a?(Numeric)
      return (v == true) ? 1 : 0 if v == true || v == false
      raise Error, "Not a number: #{v.inspect}"
    end

    def self.run(node)
      case node[0]
      when :lit   then return node[1]
      when :not   then return !run(node[1])
      when :and   then return (run(node[1]) && run(node[2])) ? true : false
      when :or    then return (run(node[1]) || run(node[2])) ? true : false
      when :arith
        a = num(run(node[2]))
        b = num(run(node[3]))
        return (node[1] == "+") ? a + b : a - b
      when :cmp
        a = run(node[2])
        b = run(node[3])
        case node[1]
        when "==" then return a == b
        when "!=" then return a != b
        end
        return false if !(a.nil? || a.is_a?(Numeric)) || !(b.nil? || b.is_a?(Numeric))
        a = num(a)
        b = num(b)
        case node[1]
        when ">=" then return a >= b
        when "<=" then return a <= b
        when ">"  then return a > b
        when "<"  then return a < b
        end
      when :call
        args = node[2].map { |arg| run(arg) }
        return FUNCTIONS[node[1]][1].call(*args)
      end
      raise Error, "Bad node #{node.inspect}"
    end

    # Truthiness of the condition. Raises Conditions::Error on bad syntax.
    def self.evaluate(text)
      return true if text.nil?
      return (run(parse(text))) ? true : false
    end

    # Raw value of an expression (e.g. "bond(:JUNO) + standing(:ACCORD)").
    def self.value(text)
      return run(parse(text))
    end
  end

  def self.cond(text)
    return Conditions.evaluate(text)
  end
end
