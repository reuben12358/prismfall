#===============================================================================
# Prismfall Cutscenes - 008 Beams and the beam clash
#-------------------------------------------------------------------------------
# Everything is drawn with Bitmap#fill_rect on the half-resolution FX layers:
# hard-edged segments in a 4-colour palette (edge, outer glow, inner, core),
# widths that ripple along the beam, bright slugs travelling away from the
# source, and FX frames at FX_FPS - so it reads as animated pixel art.
#
#   charge_up at: :mon, color: :fire, duration: 1.0, size: 7
#   beam from: :mon, to: :foe, color: :fire, width: 8, duration: 1.2
#   beam_clash a: { from: :reshiram, color: :fire }, b: { from: :kyogre, color: :water },
#              duration: 7, winner: :a | :b | :both | :fizzle | :mash,
#              curve: :a_rallies | [[0, 0.5], [0.5, 0.3], [1, 0.6]], mash: true
#   clash position: 0 = at a's mouth, 1 = at b's mouth (high = a is winning).
#===============================================================================
module Prismfall
  module Cutscene
    module BeamDraw
      WAVE = [-1, 0, 1, 0]

      module_function

      # Beam from (x0, y0) to (x1, y1) in art pixels. frame animates it.
      def beam(b, x0, y0, x1, y1, pal, width, frame, seed = 0, nozzle = true)
        dx = x1 - x0
        dy = y1 - y0
        len = Math.sqrt((dx * dx) + (dy * dy))
        return if len < 1 || width < 0.5
        horiz = dx.abs >= dy.abs
        major = (horiz) ? dx.abs : dy.abs
        return if major < 1
        sgn = (horiz) ? (dx <=> 0) : (dy <=> 0)
        thick = width * len / major          # keep the visual width on slanted beams
        n = (major / BEAM_CHUNK.to_f).ceil
        cols = [pal.edge, pal.outer, pal.inner, pal.core]
        fracs = [1.0, 1.0, 0.58, 0.26]
        4.times do |pass|
          n.times do |i|
            next if pass == 0 && ((i + frame) % 2) == 1       # ragged outer glow
            a0 = i * BEAM_CHUNK
            a1 = [a0 + BEAM_CHUNK, major].min
            w = thick * fracs[pass]
            w += 2 if pass == 0
            if pass <= 1
              w += WAVE[(i - frame) % 4]                       # ripple flowing away from the source
              w += 1 if Util.hash01(i, frame, seed) > 0.82     # flicker
            end
            slug = ((i - (frame * 2)) % 9) == 0                # bright slug racing down the core
            w += 2 if slug && pass == 2
            w += 1 if slug && pass == 3
            w *= 0.45 + (0.275 * i) if nozzle && i < 2
            w = [w.round, 1].max
            t = (a0 + a1) / 2.0 / major
            if horiz
              xa = x0 + (sgn * a0)
              xb = x0 + (sgn * a1)
              Pix.rect(b, [xa, xb].min, (y0 + (dy * t) - (w / 2.0)).round, a1 - a0, w, cols[pass])
            else
              ya = y0 + (sgn * a0)
              yb = y0 + (sgn * a1)
              Pix.rect(b, (x0 + (dx * t) - (w / 2.0)).round, [ya, yb].min, w, a1 - a0, cols[pass])
            end
          end
        end
      end

      def orb(b, x, y, r, pal, frame)
        r = r.round
        return if r < 1
        Pix.disc(b, x, y, r + 1, pal.edge) if frame.even?
        Pix.disc(b, x, y, r, pal.outer)
        Pix.disc(b, x, y, (r * 0.66).round, pal.inner)
        Pix.disc(b, x, y, (r * 0.36).round, pal.core)
      end

      def star(b, x, y, len, col, frame)
        len = len.round
        Pix.rect(b, x - len, y, (len * 2) + 1, 1, col)
        Pix.rect(b, x, y - len, 1, (len * 2) + 1, col)
        return if frame.even?
        d = len / 2
        Pix.line(b, x - d, y - d, x + d, y + d, col)
        Pix.line(b, x - d, y + d, x + d, y - d, col)
      end

      def half_disc(b, cx, cy, r, col, right)
        (-r..r).each do |dy|
          w = Math.sqrt((r * r) - (dy * dy)).round
          if right then Pix.rect(b, cx, cy + dy, w + 1, 1, col)
          else Pix.rect(b, cx - w, cy + dy, w + 1, 1, col)
          end
        end
      end

      # The clash point: two-coloured pulsing ball, white core, star, crackle.
      def clash_ball(b, cx, cy, r, pal_l, pal_r, frame)
        r = (r + [0, 1, 2, 1][frame % 4]).round
        return if r < 1
        Pix.disc(b, cx, cy, r + 2, (frame.even?) ? pal_l.edge : pal_r.edge)
        half_disc(b, cx, cy, r, pal_l.outer, false)
        half_disc(b, cx, cy, r, pal_r.outer, true)
        Pix.disc(b, cx, cy, (r * 0.7).round, (frame % 4 < 2) ? pal_l.inner : pal_r.inner)
        Pix.disc(b, cx, cy, (r * 0.42).round, pal_l.core)
        star(b, cx, cy, r + 3 + ((frame % 3) * 2), pal_r.core, frame)
        4.times do |i|                       # crackling arcs
          ang = Util.hash01(frame, i, 7) * Math::PI * 2
          l0 = r + 1
          l1 = r + 4 + (Util.hash01(frame, i, 8) * 7)
          col = (i.even?) ? pal_l.inner : pal_r.inner
          mx = cx + (Math.cos(ang) * l0)
          my = cy + (Math.sin(ang) * l0)
          kx = cx + (Math.cos(ang + 0.5) * ((l0 + l1) / 2))
          ky = cy + (Math.sin(ang + 0.5) * ((l0 + l1) / 2))
          Pix.line(b, mx, my, kx, ky, col)
          Pix.line(b, kx, ky, cx + (Math.cos(ang) * l1), cy + (Math.sin(ang) * l1), col)
        end
      end
    end

    #---------------------------------------------------------------------------
    class ChargeUp < Effect
      def initialize(scene, a, dur)
        @at = scene.anchor(a[:at] || a[:from])
        @pal = Util.palette(a[:color] || :light)
        @size = a[:size] || 7
        @dur = dur
        @k = 0.0
        Sound.play(:se, a[:se] || :beam_charge) if a[:se] != false
      end

      def draws?; return true; end

      def update(scene, lt, dt)
        @k = Util.clamp(lt / @dur, 0.0, 1.0)
        return lt >= @dur
      end

      def draw(scene, back, front)
        cx, cy = scene.to_fx(@at.call)
        f = scene.fx_frame
        z = scene.camera.zoom
        r = ([@size * @k, 1].max + (f % 2)) * z
        if @k > 0.15                              # scanline halo behind the actor
          hr = (r * 2.4).round
          (-hr..hr).step(2) do |dy|
            w = Math.sqrt((hr * hr) - (dy * dy)).round
            Pix.rect(back, cx - w, cy + dy, (w * 2) + 1, 1, @pal.edge)
          end
        end
        12.times do |i|                           # motes pulled inward
          ph = ((@k * 3) + (i / 12.0)) % 1.0
          dist = (1 - ph) * (18 + (@size * 2)) * z
          ang = (i * 2.399) + (@k * 1.5)
          x = cx + (Math.cos(ang) * dist)
          y = cy + (Math.sin(ang) * dist * 0.8)
          s = (ph > 0.75) ? 2 : 1
          Pix.rect(front, x + (Math.cos(ang) * 2), y + (Math.sin(ang) * 2), 1, 1, @pal.outer)
          Pix.rect(front, x, y, s, s, (ph > 0.6) ? @pal.core : @pal.inner)
        end
        BeamDraw.orb(front, cx, cy, r, @pal, f)
        BeamDraw.star(front, cx, cy, r + 3 + (f % 3), @pal.core, f) if @k > 0.5
      end
    end

    class ShockRing < Effect
      def initialize(pt, pal, max_r, dur, squash = 0.5, back = true, min_r = 6)
        @pt = pt
        @pal = pal
        @max = max_r
        @min = min_r
        @dur = dur
        @squash = squash
        @back = back
        @k = 0.0
      end

      def draws?; return true; end

      def update(scene, lt, dt)
        @k = Util.clamp(lt / @dur, 0.0, 1.0)
        return lt >= @dur
      end

      def draw(scene, back, front)
        cx, cy = scene.to_fx(@pt)
        r = ((@min + ((@max - @min) * Ease.apply(:out, @k))) * scene.camera.zoom).round
        col = @pal[(@k * 3.99).to_i]
        Pix.ring((@back) ? back : front, cx, cy, r, col, (@k < 0.45) ? 2 : 1, [(r * @squash).round, 1].max)
      end
    end

    class ImpactBurst < Effect
      def initialize(scene, pt, pal, size, dur)
        @pt = pt
        @pal = pal
        @size = size
        @dur = dur
        @k = 0.0
      end

      def draws?; return true; end

      def update(scene, lt, dt)
        @k = Util.clamp(lt / @dur, 0.0, 1.0)
        return lt >= @dur
      end

      def draw(scene, back, front)
        cx, cy = scene.to_fx(@pt)
        z = scene.camera.zoom
        f = scene.fx_frame
        if @k < 0.35
          r = (@size * (0.5 + (@k * 2.2)) * z).round
          Pix.disc(front, cx, cy, r, @pal.outer)
          Pix.disc(front, cx, cy, (r * 0.7).round, @pal.inner)
          Pix.disc(front, cx, cy, (r * 0.45).round, @pal.core)
          BeamDraw.star(front, cx, cy, r + 4, @pal.core, f)
        end
        r = (@size * (0.7 + (1.5 * Ease.apply(:out, @k))) * z).round
        Pix.ring(front, cx, cy, r, @pal[(@k * 3.99).to_i], (@k < 0.5) ? 2 : 1)
        return if @k < 0.2
        r2 = (@size * (0.4 + (1.2 * Ease.apply(:out, @k - 0.2))) * z).round
        Pix.ring(front, cx, cy, r2, @pal[1 + (@k * 2.99).to_i], 1)
      end
    end

    class BeamShot < Effect
      def initialize(scene, a, dur)
        @a = a
        @from = scene.anchor(a[:from])
        @to = scene.anchor(a[:to])
        @pal = Util.palette(a[:color] || :light)
        @width = a[:width] || 8
        @dur = dur
        @travel = a[:travel] || [0.3, dur * 0.35].min
        @fade = [0.25, dur * 0.25].min
        @lt = 0.0
        @acc = 0.0
        Sound.play(:se, a[:se] || :beam_fire) if a[:se] != false
      end

      def draws?; return true; end

      def update(scene, lt, dt)
        @lt = lt
        if lt >= @travel && !@landed
          @landed = true
          tgt = @to.call
          if @a[:impact] != false
            scene.run_effect(ImpactBurst.new(scene, tgt, @pal, @width * 2.0, 0.45), scene.time)
            scene.burst_at(:sparks, tgt, 16, @pal)
            scene.add_shake(@a[:shake] || 6, 0.35)
            Sound.play(:se, @a[:hit_se] || :impact) if @a[:hit_se] != false
          end
          if @a[:to].is_a?(Symbol) && scene.actors[@a[:to]] && @a[:hit] != false
            src = @from.call
            scene.hit_actor(@a[:to], (tgt[0] - src[0]) <=> 0, 12, 0.4)
          end
        end
        if @landed && lt < @dur - @fade
          @acc += 40 * dt
          while @acc >= 1
            @acc -= 1
            src = @from.call
            tgt = @to.call
            back = Math.atan2(src[1] - tgt[1], src[0] - tgt[0]) * 180 / Math::PI
            scene.particles.spawn(:sparks, tgt[0], tgt[1], { :color => @pal, :angle => back, :spread => 75 })
          end
        end
        return lt >= @dur
      end

      def draw(scene, back, front)
        x0, y0 = scene.to_fx(@from.call)
        x1, y1 = scene.to_fx(@to.call)
        f = scene.fx_frame
        z = scene.camera.zoom
        k = Util.clamp(@lt / @travel, 0.0, 1.0)
        w = @width * z * Util.clamp(@lt / 0.08, 0.3, 1.0)
        w *= Util.clamp((@dur - @lt) / @fade, 0.0, 1.0) if @lt > @dur - @fade
        return if w < 0.5
        hx = (x0 + ((x1 - x0) * k)).round
        hy = (y0 + ((y1 - y0) * k)).round
        BeamDraw.beam(front, x0, y0, hx, hy, @pal, w, f)
        BeamDraw.orb(front, x0, y0, (w * 0.7) + (f % 2), @pal, f)
        BeamDraw.orb(front, hx, hy, (w * 0.9) + ((@landed) ? (f % 3) : 0), @pal, f)
        BeamDraw.star(front, hx, hy, w + 3 + (f % 3), @pal.core, f) if @landed
      end
    end

    #---------------------------------------------------------------------------
    # The beam clash
    #---------------------------------------------------------------------------
    class BeamClash < Effect
      Side = Struct.new(:from, :pal, :width, :actor)
      CURVES = {
        :even        => [[0, 0.5], [0.2, 0.44], [0.4, 0.57], [0.6, 0.45], [0.8, 0.55], [1, 0.5]],
        :a_rallies   => [[0, 0.5], [0.2, 0.42], [0.45, 0.6], [0.7, 0.3], [0.88, 0.42], [1, 0.56]],
        :b_rallies   => [[0, 0.5], [0.2, 0.58], [0.45, 0.4], [0.7, 0.7], [0.88, 0.58], [1, 0.44]],
        :a_dominates => [[0, 0.5], [0.3, 0.58], [0.6, 0.66], [1, 0.74]],
        :b_dominates => [[0, 0.5], [0.3, 0.42], [0.6, 0.34], [1, 0.26]],
        :left_right_hold => [[0, 0.5], [0.25, 0.34], [0.55, 0.66], [0.8, 0.5], [1, 0.5]]
      }

      attr_accessor :white, :shake, :strobe, :intensity
      attr_reader :pos

      def initialize(scene, a, dur)
        @a = side(scene, a[:a])
        @b = side(scene, a[:b])
        @dur = dur
        @winner = a[:winner] || :both
        @launch = a[:launch] || [0.45, dur * 0.15].min
        @resolve = a[:resolve] || Util.clamp(dur * 0.25, 0.6, 1.6)
        curve = a[:curve] || { :a => :a_rallies, :b => :b_rallies }[@winner] || :even
        @curve = (curve.is_a?(Array)) ? curve : (CURVES[curve] || CURVES[:even])
        @mash = a[:mash] || @winner == :mash
        @player = a[:player] || :a
        @push = 0.0
        @pos = @curve[0][1].to_f
        @ball = a[:ball] || 9
        @ball_scale = 1.0
        @shake = a[:shake] || 4
        @strobe = a[:strobe] != false
        @white = 0.0
        @intensity = 1.0
        @rings = 0
        @next_ring = @launch
        @acc = 0.0
        @lt = 0.0
        @wf = [1.0, 1.0]       # width factors for a, b
        @se = a[:se] != false
        @mote = nil
        Sound.play(:se, :beam_fire) if @se
      end

      def side(scene, s)
        actor = (s[:from].is_a?(Symbol) && scene.actors[s[:from]]) ? s[:from] : nil
        return Side.new(scene.anchor(s[:from]), Util.palette(s[:color] || :light), s[:width] || 9, actor)
      end

      def draws?; return true; end

      def curve_at(u)
        prev = @curve[0]
        @curve.each do |pt|
          if u <= pt[0]
            span = pt[0] - prev[0]
            return pt[1].to_f if span <= 0
            return Util.lerp(prev[1], pt[1], Ease.apply(:sine, (u - prev[0]) / span))
          end
          prev = pt
        end
        return @curve[-1][1].to_f
      end

      def clash_point
        pa = @a.from.call
        pb = @b.from.call
        return [Util.lerp(pa[0], pb[0], @pos), Util.lerp(pa[1], pb[1], @pos)], pa, pb
      end

      def update(scene, lt, dt)
        @lt = lt
        hold_end = @dur - @resolve
        if lt < @launch
          return false
        elsif lt < hold_end
          struggle(scene, (lt - @launch) / [hold_end - @launch, 0.001].max, dt)
        else
          resolve(scene, (lt - hold_end) / @resolve, dt)
        end
        return lt >= @dur
      end

      def struggle(scene, u, dt)
        if !@locked
          @locked = true
          Sound.play(:se, :beam_clash) if @se
          scene.add_flash([255, 255, 255], 0.15, 160)
        end
        if @mash
          btn = Input.const_get(MASH_BUTTON)
          @push += ((@player == :a) ? 0.035 : -0.035) if Input.trigger?(btn)
          @push -= @push * 0.6 * dt
        end
        jitter = (Util.hash01(scene.fx_frame, 5) - 0.5) * 0.014
        @pos = Util.clamp(curve_at(u) + @push + jitter, 0.08, 0.92)
        c, pa, pb = clash_point
        if @lt >= @next_ring                      # shockwave rings on a quickening beat
          @next_ring = @lt + Util.lerp(0.6, 0.28, u)
          @rings += 1
          pal = [@a.pal, @b.pal, Util.palette(:white)][@rings % 3].whitened(@white)
          scene.run_effect(ShockRing.new(c, pal, 52 + (16 * u), 0.55, 0.45, true, @ball), scene.time)
          scene.add_flash([255, 255, 255], 0.09, 60 * @intensity) if @strobe && @rings.even?
        end
        @acc += 45 * @intensity * dt
        ang = Math.atan2(pb[1] - pa[1], pb[0] - pa[0]) * 180 / Math::PI
        while @acc >= 1                           # sparks thrown out sideways
          @acc -= 1
          up = (scene.rng.rand < 0.5) ? 90 : -90
          pal = ((scene.rng.rand < 0.5) ? @a.pal : @b.pal).whitened(@white)
          scene.particles.spawn(:sparks, c[0], c[1], { :color => pal, :angle => ang + up, :spread => 55 })
        end
        amp = @shake * @intensity * (0.5 + (0.5 * u))
        f = scene.fx_frame
        scene.camera.sx += Util.snap(((Util.hash01(f, 11) * 2) - 1) * amp)
        scene.camera.sy += Util.snap(((Util.hash01(f, 12) * 2) - 1) * amp)
        dir = (pb[0] - pa[0]) <=> 0
        trem = (f.even?) ? PX : 0
        if @a.actor && scene.actors[@a.actor]      # the losing side digs in and is pushed back
          scene.actors[@a.actor].off_x -= dir * (([0.5 - @pos, 0].max * 30) + trem)
        end
        if @b.actor && scene.actors[@b.actor]
          scene.actors[@b.actor].off_x += dir * (([@pos - 0.5, 0].max * 30) + trem)
        end
      end

      def resolve(scene, r, dt)
        if !@resolving
          @resolving = true
          @winner = ((@pos >= 0.5) ? :a : :b) if @winner == :mash
          scene.results[:clash_winner] = @winner
          @pos0 = @pos
        end
        c, pa, pb = clash_point
        dir = (pb[0] - pa[0]) <=> 0
        case @winner
        when :a, :b
          r1 = 0.45
          target = (@winner == :a) ? 1.0 : 0.0
          @pos = Util.lerp(@pos0, target, Ease.apply(:in_cubic, r / r1)) if r < r1
          if r >= r1 && !@done
            @done = true
            @pos = target
            loser = (@winner == :a) ? @b : @a
            win = (@winner == :a) ? @a : @b
            pt = loser.from.call
            scene.run_effect(ImpactBurst.new(scene, pt, win.pal, 26, 0.6), scene.time)
            3.times { |i| scene.run_effect(ShockRing.new(pt, win.pal, 70 + (i * 30), 0.6 + (i * 0.15), 0.45), scene.time) }
            scene.burst_at(:sparks, pt, 40, win.pal)
            scene.burst_at(:debris, pt, 14)
            scene.add_flash([255, 255, 255], 0.5, 230)
            scene.add_shake(12, 0.7)
            scene.hit_actor(loser.actor, (@winner == :a) ? dir : -dir, 22, 0.6) if loser.actor
            Sound.play(:se, :beam_break) if @se
          end
          if @done
            k = Util.clamp(1 - ((r - r1) / (1 - r1)), 0.0, 1.0)
            @wf = (@winner == :a) ? [k, 0.0] : [0.0, k]
            @ball_scale = 0.0
          else
            @ball_scale = 1.0 + (r / r1 * 0.4)
          end
        when :both
          r1 = 0.5
          @ball_scale = 1.0 + (2.4 * Ease.apply(:in, r / r1)) if r < r1
          scene.camera.sx += Util.snap(((Util.hash01(scene.fx_frame, 11) * 2) - 1) * @shake * 2) if r < r1
          if r >= r1 && !@done
            @done = true
            @wf = [0.0, 0.0]
            @ball_scale = 0.0
            white = Util.palette(:white)
            4.times { |i| scene.run_effect(ShockRing.new(c, [@a.pal, white, @b.pal, white][i], 90 + (i * 45), 0.7 + (i * 0.2), 0.5), scene.time) }
            scene.run_effect(ImpactBurst.new(scene, c, white, 34, 0.7), scene.time)
            scene.burst_at(:sparks, c, 36, @a.pal)
            scene.burst_at(:sparks, c, 36, @b.pal)
            scene.burst_at(:debris, c, 20)
            scene.add_flash([255, 255, 255], 1.0, 255)
            scene.add_shake(14, 0.9)
            scene.hit_actor(@a.actor, -dir, 24, 0.7) if @a.actor
            scene.hit_actor(@b.actor, dir, 24, 0.7) if @b.actor
            Sound.play(:se, :beam_break) if @se
          end
        when :fizzle
          r1 = 0.6
          if r < r1
            k = 1 - (r / r1)
            @ball_scale = [k, 0.15].max
            @wf = [k, k]
          elsif !@done
            @done = true
            @wf = [0.0, 0.0]
            @ball_scale = 0.0
            @mote = [c[0], c[1], 0.0]
            Sound.play(:se, :chime) if @se
          end
          if @mote                                   # one falling mote of light
            @mote[2] += 160 * dt
            @mote[1] += @mote[2] * dt
          end
        end
      end

      def draw(scene, back, front)
        c, pa, pb = clash_point
        ax, ay = scene.to_fx(pa)
        bx, by = scene.to_fx(pb)
        cx, cy = scene.to_fx(c)
        f = scene.fx_frame
        z = scene.camera.zoom
        pal_a = @a.pal.whitened(@white)
        pal_b = @b.pal.whitened(@white)
        if @lt < @launch                            # both beams race to the meeting point
          k = Ease.apply(:in, @lt / @launch)
          hax = (ax + ((cx - ax) * k)).round
          hay = (ay + ((cy - ay) * k)).round
          hbx = (bx + ((cx - bx) * k)).round
          hby = (by + ((cy - by) * k)).round
          BeamDraw.beam(front, ax, ay, hax, hay, pal_a, @a.width * z, f, 1)
          BeamDraw.beam(front, bx, by, hbx, hby, pal_b, @b.width * z, f, 2)
          BeamDraw.orb(front, hax, hay, @a.width * z * 0.9, pal_a, f)
          BeamDraw.orb(front, hbx, hby, @b.width * z * 0.9, pal_b, f)
        else
          gutter = @winner == :fizzle && @resolving && f.odd?   # guttering flicker
          wa = @a.width * z * @wf[0]
          wb = @b.width * z * @wf[1]
          BeamDraw.beam(front, ax, ay, cx, cy, pal_a, wa, f, 1) if wa >= 0.5 && !gutter
          BeamDraw.beam(front, bx, by, cx, cy, pal_b, wb, f, 2) if wb >= 0.5 && !gutter
          if @ball_scale > 0
            left, right = (ax <= bx) ? [pal_a, pal_b] : [pal_b, pal_a]
            BeamDraw.clash_ball(front, cx, cy, @ball * z * @ball_scale, left, right, f)
          end
        end
        BeamDraw.orb(front, ax, ay, (@a.width * z * 0.6 * @wf[0]) + (f % 2), pal_a, f) if @wf[0] > 0.05
        BeamDraw.orb(front, bx, by, (@b.width * z * 0.6 * @wf[1]) + (f % 2), pal_b, f) if @wf[1] > 0.05
        if @mote
          mx, my = scene.to_fx([@mote[0], @mote[1]])
          Pix.rect(front, mx, my - 3, 1, 3, Util.palette(:white).outer)
          Pix.rect(front, mx, my, 2, 2, Util.palette(:white).core)
        end
      end
    end

    class Scene
      def op_charge_up(a, dur); return ChargeUp.new(self, a, dur); end
      def op_beam(a, dur);      return BeamShot.new(self, a, dur); end

      def op_impact(a, dur)
        pt = point(a[:at])
        pal = Util.palette(a[:color] || :light)
        burst_at(:sparks, pt, a[:sparks] || 16, pal)
        add_shake(a[:shake], 0.3) if a[:shake]
        return ImpactBurst.new(self, pt, pal, a[:size] || 16, dur)
      end

      def op_ring(a, dur)
        return ShockRing.new(point(a[:at]), Util.palette(a[:color] || :white), a[:radius] || 80, dur,
                             a[:squash] || 0.5, a[:layer] != :front)
      end

      def op_beam_clash(a, dur); return BeamClash.new(self, a, dur); end

      # clash_mod :id, white: 0..1, intensity: 0..1, shake:, strobe:
      def op_clash_mod(a, dur)
        clash = @effects.find { |e| e.is_a?(BeamClash) && (a[:id].nil? || e.id == a[:id]) }
        return nil if !clash
        clash.shake = a[:shake] if a[:shake]
        clash.strobe = a[:strobe] if a.has_key?(:strobe)
        w0 = clash.white
        i0 = clash.intensity
        w1 = (a[:white] || w0).to_f
        i1 = (a[:intensity] || i0).to_f
        tween(dur, :linear) do |k, _|
          clash.white = Util.lerp(w0, w1, k)
          clash.intensity = Util.lerp(i0, i1, k)
        end
      end
    end
  end
end
