#===============================================================================
# Prismfall Cutscenes - 011 Festival match highlights
#-------------------------------------------------------------------------------
# Prismfall::Cutscene.match_highlight(a, b, winner, moments)
#   This is the call Prismfall Core makes (015_Festival_Draw.rb play_highlight):
#   a, b, winner are { :id, :name, :trainer_type } hashes and moments is a
#   MATCH_RULES list of [actor_id, species, event, caption] rows, where event is
#   :send_out :attack :beam :beam_clash :dodge :faint :switch :field_shift
#   :taunt :forfeit :finish.
# Also accepted (keywords win over positionals):
#   match_highlight(a, b, winner: :a, moments: [:opening, :beam_clash, :final_blow])
#   a / b : hash as above (optional :team => [species], :version), a Festival
#           entrant id, or [trainer_type, name, version]
#   winner: :a, :b, an id, or one of the hashes
#   moments: rows as above, or template names (:opening, :super_effective,
#           :clutch, :beam_clash, :final_blow, :walk_off); nil = picked for you
#   tint: floor tint (palette or [r, g, b]), play: false returns the Definition.
# The result is a 15-30 second scene: VS card, 2-4 key moments, result card.
# Teams come from trainers PBS (through Core's Festival entrants when present).
#===============================================================================
module Prismfall
  module Cutscene
    module Highlight
      POS = { :a => [152, 318], :b => [360, 318] }
      TRAINER_POS = { :a => [44, 312], :b => [468, 312] }
      TEMPLATES = [:opening, :super_effective, :clutch, :beam_clash, :final_blow, :walk_off]
      EVENTS = [:send_out, :attack, :beam, :beam_clash, :dodge, :faint, :switch, :field_shift, :taunt,
                :forfeit, :finish, :clutch, :exchange, :walk_off]

      module_function

      #-------------------------------------------------------------------------
      # Input normalisation
      #-------------------------------------------------------------------------
      def trainer_info(spec)
        info = { :id => nil, :name => "???", :type => nil, :team => nil, :version => nil }
        case spec
        when Hash
          info[:id] = spec[:id]
          info[:name] = (spec[:name] || spec[:display] || spec[:id]).to_s
          info[:type] = spec[:trainer_type] || spec[:type]
          info[:team] = spec[:team]
          info[:version] = spec[:version]
          info[:pbs_name] = spec[:pbs_name]
        when Array
          info[:type], info[:name], info[:version] = spec
          info[:id] = info[:type]
        when Symbol
          info[:id] = spec
          info[:name] = spec.to_s.capitalize
          if defined?(Prismfall::Festival) && Prismfall::Festival.respond_to?(:entrant) && Prismfall::Festival.entrant(spec)
            info[:name] = Prismfall::Festival.display_name(spec)
            info[:type] = Array(Prismfall::Festival.entrant(spec)[:trainer_type]).first
          else
            info[:type] = spec
          end
        end
        info[:team] ||= pbs_team(info)
        return info
      end

      # Species list from trainers PBS; [] when the trainer cannot be found.
      def pbs_team(info)
        return [] if !defined?(GameData::Trainer)
        type = info[:type]
        name = info[:pbs_name] || info[:name]
        versions = [info[:version]].compact
        if defined?(Prismfall::Festival) && Prismfall::Festival.respond_to?(:entrant) && info[:id]
          e = Prismfall::Festival.entrant(info[:id])
          if e
            v = info[:version] || e[:version] || 0
            if e[:rival_battle] && defined?(Prismfall::Rival) && Prismfall::Rival.respond_to?(:version_for)
              v = Prismfall::Rival.version_for(e[:rival_battle])
            end
            type, name = Prismfall::Festival.resolve_trainer(e, v)
            versions.unshift(v)
          end
        end
        (versions + [0, 50, 3, 2, 1, 40, 80]).uniq.each do |v|
          tr = GameData::Trainer.try_get(type, name, v)
          next if !tr || !tr.pokemon
          return tr.pokemon.map { |p| p[:species] }.compact
        end
        return []
      rescue StandardError => e
        Util.log("highlight team lookup failed for #{info[:name]}: #{e.message}")
        return []
      end

      def winner_side(winner, a, b)
        return :a if winner == :a
        return :b if winner == :b
        id = (winner.is_a?(Hash)) ? (winner[:id] || winner[:name]) : winner
        return :b if id && (id == b[:id] || id.to_s == b[:name])
        return :a
      end

      def side_of(actor, a, b)
        return :b if actor == :b || (actor && (actor == b[:id] || actor.to_s == b[:name]))
        return :a
      end

      def super_effective?(attacker, defender)
        return false if !defined?(Effectiveness) || !Effectiveness.respond_to?(:super_effective_type?)
        at = Util.species_types(attacker)[0]
        dt = Util.species_types(defender)
        return false if !at || dt.empty?
        return Effectiveness.super_effective_type?(at, *dt)
      rescue StandardError
        return false
      end

      # -> [{ :side, :species, :event, :caption }]
      def normalise_moments(moments, a, b, win, seed)
        lose = (win == :a) ? :b : :a
        team = { :a => a[:team], :b => b[:team] }
        ace = { :a => team[:a].last || :PIKACHU, :b => team[:b].last || :EEVEE }
        lead = { :a => team[:a].first || ace[:a], :b => team[:b].first || ace[:b] }
        name = { :a => a[:name], :b => b[:name] }
        if moments.nil? || moments.empty?
          mid = [:super_effective, :clutch, :beam_clash]
          moments = [:opening, mid[seed % 3], :final_blow, :walk_off]
        end
        rows = []
        moments.each do |m|
          if m.is_a?(Array)
            side = side_of(m[0], a, b)
            ev = (EVENTS.include?(m[2])) ? m[2] : :attack
            rows.push({ :side => side, :species => m[1] || ace[side], :event => ev, :caption => m[3].to_s })
            next
          end
          case m
          when :opening
            rows.push({ :side => :a, :species => lead[:a], :other => lead[:b], :event => :exchange,
                        :caption => Util.tr("{1} leads with {2}. {3} answers with {4}!", name[:a],
                                            Util.species_name(lead[:a]), name[:b], Util.species_name(lead[:b])) })
          when :super_effective
            atk = team[win].find { |s| team[lose].any? { |d| super_effective?(s, d) } } || ace[win]
            dfn = team[lose].find { |d| super_effective?(atk, d) } || lead[lose]
            rows.push({ :side => win, :species => atk, :other => dfn, :event => :beam, :strong => true,
                        :caption => Util.tr("{1} finds the weak point. It's super effective!", Util.species_name(atk)) })
          when :clutch
            rows.push({ :side => win, :species => ace[win], :other => ace[lose], :event => :clutch,
                        :caption => Util.tr("{1} hangs on by a thread, and hits back!", Util.species_name(ace[win])) })
          when :beam_clash
            rows.push({ :side => win, :species => ace[win], :other => ace[lose], :event => :beam_clash,
                        :caption => Util.tr("{1} and {2} lock beams in the middle of the arena!",
                                            Util.species_name(ace[win]), Util.species_name(ace[lose])) })
          when :final_blow
            rows.push({ :side => win, :species => ace[win], :other => ace[lose], :event => :finish,
                        :caption => Util.tr("{1} lands the final blow!", Util.species_name(ace[win])) })
          when :walk_off
            rows.push({ :side => win, :species => nil, :event => :walk_off,
                        :caption => Util.tr("{1} and {2} meet in the middle. A good match.", name[:a], name[:b]) })
          end
        end
        rows = rows[0, 3] + [rows[-1]] if rows.length > 4            # 2-4 key moments
        if rows.length < 2
          rows.push({ :side => win, :species => ace[win], :other => ace[lose], :event => :finish,
                      :caption => Util.tr("{1} lands the final blow!", Util.species_name(ace[win])) })
        end
        return rows
      end

      #-------------------------------------------------------------------------
      # Building
      #-------------------------------------------------------------------------
      class Director
        def initialize(b, a, bb, win, tint)
          @b = b
          @info = { :a => a, :b => bb }
          @win = win
          @mon = { :a => nil, :b => nil }
          @hp = { :a => 1.0, :b => 1.0 }
          @tint = tint
        end

        def other(side); return (side == :a) ? :b : :a; end
        def id(side);    return (side == :a) ? :hl_a : :hl_b; end
        def tid(side);   return (side == :a) ? :hl_ta : :hl_tb; end
        def pal(side);   return Util.type_palette(@mon[side], :light); end

        def put(side, species, pop = true)
          return if species.nil? || @mon[side] == species
          @mon[side] = species
          @hp[side] = 1.0
          @b.actor id(side), species: species, at: POS[side], flip: (side == :a), opacity: (pop) ? 0 : 255
          @b.hp_bar id(side), value: 1.0, duration: 0
          return if !pop
          @b.fade id(side), to: 255, duration: 0.25
          @b.tint id(side), color: [255, 255, 255], amount: 255, duration: 0
          @b.tint id(side), color: [255, 255, 255], amount: 0, duration: 0.35
          @b.burst :motes, at: id(side), count: 14, color: pal(side)
          @b.cry species
        end

        def default_mon(side)
          t = @info[side][:team]
          return t.first || ((side == :a) ? :PIKACHU : :EEVEE)
        end

        def ensure_mons(row)
          put(row[:side], row[:species])
          o = other(row[:side])
          put(o, row[:other]) if row[:other]
          put(o, default_mon(o)) if !@mon[o]
          put(row[:side], default_mon(row[:side])) if !@mon[row[:side]]
        end

        def damage(side, amount, dur = 0.5)
          @hp[side] = [@hp[side] - amount, 0.0].max
          @b.hp_bar id(side), value: @hp[side], duration: dur
        end

        def moment(row)
          b = @b
          s = row[:side]
          o = other(s)
          cap = row[:caption]
          dur = send("len_#{row[:event]}")
          dur = [dur, [Builder.read_time(cap), 5.0].min].max if cap && !cap.empty?
          this = self
          b.together do
            b.text cap, duration: dur - 0.1 if cap && !cap.empty?
            b.sequence { this.send("do_#{row[:event]}", row, s, o) }
          end
          b.wait 0.1
        end

        def len_send_out; 2.6; end
        def do_send_out(row, s, o)
          @mon[s] = nil if @mon[s] == row[:species]     # replay the entrance
          put(s, row[:species])
          put(o, default_mon(o)) if !@mon[o]
          @b.wait 0.5
          @b.hop tid(s), height: 8, duration: 0.3
          @b.wait 0.6
        end

        def len_attack; 2.8; end
        def do_attack(row, s, o)
          ensure_mons(row)
          @b.wait 0.4
          @b.lunge id(s), toward: id(o), color: pal(s), duration: 0.45
          damage(o, 0.45)
          @b.wait 0.8
        end

        def len_exchange; 3.6; end
        def do_exchange(row, s, o)
          ensure_mons(row)
          @b.wait 0.6
          @b.lunge id(s), toward: id(o), color: pal(s), duration: 0.45
          damage(o, 0.3)
          @b.wait 0.4
          @b.charge_up at: id(o), color: pal(o), duration: 0.5
          @b.beam from: id(o), to: id(s), color: pal(o), duration: 0.9
          damage(s, 0.35)
          @b.wait 0.3
        end

        def len_beam; 3.2; end
        def do_beam(row, s, o)
          ensure_mons(row)
          @b.wait 0.3
          @b.charge_up at: id(s), color: pal(s), duration: 0.6
          @b.beam from: id(s), to: id(o), color: pal(s), duration: 1.1, width: (row[:strong]) ? 18 : 13,
                  hit_se: (row[:strong]) ? :impact_super : :impact
          damage(o, (row[:strong]) ? 0.7 : 0.5)
          @b.flash duration: 0.25, power: 140 if row[:strong]
          @b.wait 0.6
        end

        def len_beam_clash; 5.6; end
        def do_beam_clash(row, s, o)
          ensure_mons(row)
          b = @b
          a_id = id(:a)
          b_id = id(:b)
          pa = pal(:a)
          pb = pal(:b)
          b.together do
            b.charge_up at: a_id, color: pa, duration: 0.6
            b.charge_up at: b_id, color: pb, duration: 0.6
          end
          b.zoom to: 1.25, duration: 0.5
          b.beam_clash a: { from: a_id, color: pa, width: 18 }, b: { from: b_id, color: pb, width: 18 },
                       duration: 3.8, winner: s, ball: 15, shake: 3, ground: 322
          b.zoom to: 1.0, duration: 0.4
          b.emit :steam, at: [256, 280], rate: 30, duration: 0.8, id: :hl_steam
          damage(o, 0.6)
          b.wait 0.6
        end

        def len_dodge; 2.8; end
        def do_dodge(row, s, o)
          ensure_mons(row)
          dx = (s == :a) ? -36 : 36
          @b.wait 0.4
          @b.lunge id(o), toward: id(s), hit: false, duration: 0.5, wait: false
          @b.wait 0.12
          @b.move id(s), by: [dx, 0], arc: 14, duration: 0.25, ease: :out
          @b.wait 0.7
          @b.tremble id(s), duration: 0.5
          @b.move id(s), by: [-dx, 0], duration: 0.3
          @b.wait 0.6
        end

        def len_faint; 3.0; end
        def do_faint(row, s, o)
          ensure_mons(row)
          @b.wait 0.4
          @b.lunge id(o), toward: id(s), color: pal(o), duration: 0.45, se: :impact_super
          damage(s, 1.0, 0.6)
          @b.wait 0.5
          @b.me :me_hl_hit
          @b.faint id(s)
          @b.hp_bar id(s), show: false
          @mon[s] = nil
          @b.wait 0.4
        end

        def len_switch; 2.6; end
        def do_switch(row, s, o)
          put(o, default_mon(o)) if !@mon[o]
          if @mon[s] && @mon[s] != row[:species]
            @b.fade id(s), to: 0, duration: 0.3
            @b.wait 0.4
          end
          @mon[s] = nil if @mon[s] == row[:species]
          put(s, row[:species])
          @b.wait 1.2
        end

        def len_field_shift; 3.0; end
        def do_field_shift(row, s, o)
          ensure_mons(row)
          col = Util.palette(pal(s)).rgb[2]
          @b.wait 0.3
          @b.ring at: { actor: id(s), part: :feet }, color: pal(s), radius: 260, duration: 0.9
          @b.ring at: { actor: id(s), part: :feet }, color: pal(s), radius: 180, duration: 1.1
          @b.tone to: [col[0] / 6 - 16, col[1] / 6 - 16, col[2] / 6 - 16, 0], duration: 0.8
          @b.emit :motes, area: [0, 200, 512, 150], rate: 40, color: pal(s), duration: 2.0, id: :hl_field
          @b.tremble id(o), duration: 0.6
          @b.wait 1.6
        end

        def len_taunt; 2.6; end
        def do_taunt(row, s, o)
          ensure_mons(row)
          @b.wait 0.4
          @b.hop tid(s), height: 10, times: 2, duration: 0.6
          @b.wait 0.5
          @b.tremble id(o), duration: 0.7
          @b.wait 0.8
        end

        def len_forfeit; 3.0; end
        def do_forfeit(row, s, o)
          ensure_mons(row)
          @b.wait 0.5
          @b.hop tid(s), height: 8, duration: 0.35
          @b.wait 0.4
          @b.tint id(s), color: [255, 255, 255], amount: 255, duration: 0.3
          @b.fade id(s), to: 0, duration: 0.5
          @b.hp_bar id(s), show: false
          @mon[s] = nil
          @b.wait 1.2
        end

        def len_finish; 3.8; end
        def do_finish(row, s, o)
          ensure_mons(row)
          @b.wait 0.3
          @b.charge_up at: id(s), color: pal(s), duration: 0.7, size: 9
          @b.beam from: id(s), to: id(o), color: pal(s), duration: 1.2, width: 18, shake: 9, hit_se: :impact_super
          damage(o, 1.0, 0.5)
          @b.flash duration: 0.4, power: 200
          @b.me :me_hl_hit
          @b.faint id(o)
          @b.hp_bar id(o), show: false
          @mon[o] = nil
          @b.wait 0.3
        end

        def len_clutch; 4.2; end
        def do_clutch(row, s, o)
          ensure_mons(row)
          @b.wait 0.3
          @b.charge_up at: id(o), color: pal(o), duration: 0.5
          @b.beam from: id(o), to: id(s), color: pal(o), duration: 1.0, width: 15
          @hp[s] = 0.04
          @b.hp_bar id(s), value: 0.04, duration: 0.7
          @b.tremble id(s), duration: 0.7
          @b.wait 0.8
          @b.lunge id(s), toward: id(o), color: pal(s), duration: 0.45, se: :impact_super
          damage(o, 0.6)
          @b.wait 0.5
        end

        def len_walk_off; 3.6; end
        def do_walk_off(row, s, o)
          b = @b
          [:a, :b].each do |side|
            next if !@mon[side]
            b.fade id(side), to: 0, duration: 0.3
            b.hp_bar id(side), show: false
            @mon[side] = nil
          end
          b.wait 0.3
          b.move tid(:a), to: [226, 316], duration: 1.0, ease: :in_out
          b.move tid(:b), to: [286, 316], duration: 1.0, ease: :in_out
          b.wait 1.1
          b.hop tid(:a), height: 6, duration: 0.3
          b.hop tid(:b), height: 6, duration: 0.3
          b.wait 0.7
          lose = other(@win)
          b.flip tid(lose)
          b.move tid(lose), by: [(lose == :a) ? -260 : 260, 0], duration: 1.4, ease: :in
          b.wait 1.4
        end
      end

      def build(a, b, win, rows, tint: nil)
        name = :"HIGHLIGHT_#{a[:id] || a[:name]}_#{b[:id] || b[:name]}"
        pal = { :a => Util.type_palette(a[:team].last, :water), :b => Util.type_palette(b[:team].last, :fire) }
        pal[:b] = :dragon if pal[:b] == pal[:a] && pal[:a] != :dragon
        col = pal.transform_values { |p| Util.palette(p).rgb[2] }
        defn = Cutscene.build(name) do |s|
          s.background :arena, colors: [col[:a], col[:b]], tint: tint
          s.letterbox true, duration: 0
          s.bgm :bgm_highlight, volume: HIGHLIGHT_BGM_VOLUME
          s.actor :hl_ta, trainer: a[:type] || a[:id], at: TRAINER_POS[:a], flip: true, scale: 0.5, z: 480
          s.actor :hl_tb, trainer: b[:type] || b[:id], at: TRAINER_POS[:b], scale: 0.5, z: 480
          s.me :me_hl_start
          s.vs_card a: { name: a[:name], trainer: a[:type] || a[:id], color: pal[:a], team: a[:team] },
                    b: { name: b[:name], trainer: b[:type] || b[:id], color: pal[:b], team: b[:team] },
                    duration: 3.6
          d = Director.new(s, a, b, win, tint)
          rows.each_with_index do |row, i|
            d.moment(row)
            s.flash duration: 0.2, power: 120 if i < rows.length - 1      # cut between moments
          end
          winner = (win == :a) ? a : b
          result = 2.6
          total = s.now + result
          result += HIGHLIGHT_MIN_SECONDS - total if total < HIGHLIGHT_MIN_SECONDS
          s.me :me_hl_result
          s.se :crowd_cheer
          s.title Util.tr("{1} wins!", winner[:name]), sub: Util.tr("{1} vs {2}", a[:name], b[:name]),
                  color: pal[win], duration: result
        end
        return defn
      end
    end

    class << self
      # See the header of this file. Returns true when the highlight played to
      # the end, false when skipped/failed; with play: false, the Definition.
      def match_highlight(a, b, winner = nil, moments = nil, **kw)
        winner = kw[:winner] if kw.has_key?(:winner)
        moments = kw[:moments] if kw.has_key?(:moments)
        ia = Highlight.trainer_info(a)
        ib = Highlight.trainer_info(b)
        win = Highlight.winner_side(winner, ia, ib)
        seed = kw[:seed] || (ia[:name].to_s + ib[:name].to_s).sum
        rows = Highlight.normalise_moments(moments, ia, ib, win, seed)
        # Species named in the moments join the VS-card teams.
        rows.each do |r|
          t = ((r[:side] == :a) ? ia : ib)[:team]
          t.push(r[:species]) if r[:species] && !t.include?(r[:species])
        end
        defn = Highlight.build(ia, ib, win, rows, tint: kw[:tint])
        if defn.length > HIGHLIGHT_MAX_SECONDS + 0.01 && rows.length > 2
          rows.delete_at(1)                                          # keep it inside 30 s
          defn = Highlight.build(ia, ib, win, rows, tint: kw[:tint])
        end
        return defn if kw[:play] == false
        return play(defn)
      rescue StandardError => e
        Util.log("match_highlight failed: #{e.class}: #{e.message}\n#{(e.backtrace || [])[0, 5].join("\n")}")
        raise if @raise_errors
        return false
      end

      # Optional convenience for events: asks first. (Core's Festival already
      # asks "Watch the highlights?" itself and then calls match_highlight.)
      def offer_festival_highlight(a, b, winner = nil, moments = nil, **kw)
        return false if defined?(pbConfirmMessage) && !pbConfirmMessage(Util.tr("Watch the highlights?"))
        return match_highlight(a, b, winner, moments, **kw)
      end

      # The sample shipped for the Debug menu: Anja vs Brann, the Truce Match.
      def play_sample_highlight(play: true)
        return match_highlight(
          { :id => :ANJA, :name => "Anja", :trainer_type => :LEADER_ANJA },
          { :id => :BRANN, :name => "Brann", :trainer_type => :LEADER_BRANN },
          { :id => :ANJA, :name => "Anja", :trainer_type => :LEADER_ANJA },
          [[:BRANN, :COALOSSAL, :send_out, "Two Wardens who were on opposite shores a season ago."],
           [:ANJA, :MAMOSWINE, :beam_clash, "Blizzard meets Flamethrower: the war's beam clash, in miniature, and this time nobody dies."],
           [:BRANN, :COALOSSAL, :faint, "Brann laughs until he coughs. \"Aye. Ice remembers.\""]],
          tint: :ice, play: play
        )
      end
    end
  end
end
