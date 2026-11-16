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
      # band widths as a share of the full beam: outline, edge, body, inner, core
      BANDS = [1.0, 0.9, 0.74, 0.5, 0.24]

      module_function

      # Thick beam from (x0, y0) to (x1, y1) in art pixels: dark pixel outline,
      # coloured edge and body, hot inner band and white core, with dithered
      # fringes between the bands, a ripple flowing away from the source and
      # bright slugs racing down the core. width = full thickness.
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
        cols = [pal.outline, pal.edge, pal.outer, pal.inner, pal.core]
        thin = thick < 6
        dither = BEAM_DITHER && !thin
        5.times do |pass|
          next if thin && pass == 1
          n.times do |i|
            a0 = i * BEAM_CHUNK
            a1 = [a0 + BEAM_CHUNK, major].min
            w = thick * BANDS[pass]
            w = [w, thick - 2].min if pass == 1 && thick >= 6        # outline is one pixel each side
            if pass <= 2
              w += WAVE[(i - frame) % 4] * ((thick >= 16) ? 2 : 1)   # ripple
              w += 2 if Util.hash01(i, frame, seed) > 0.85           # flicker
            end
            slug = ((i - (frame * 2)) % 9) < 2                       # bright slugs
            w += thick * 0.12 if slug && pass >= 3
            w *= 0.4 + (0.2 * i) if nozzle && i < 3
            w = [w.round, 1].max
            t = (a0 + a1) / 2.0 / major
            la = (horiz ? x0 : y0) + (sgn * a0)
            lb = (horiz ? x0 : y0) + (sgn * a1)
            lo = [la, lb].min
            mid = (horiz) ? y0 + (dy * t) : x0 + (dx * t)
            top = (mid - (w / 2.0)).round
            if horiz then Pix.rect(b, lo, top, a1 - a0, w, cols[pass])
            else Pix.rect(b, top, lo, w, a1 - a0, cols[pass])
            end
            next if !dither || pass < 2 || w < 3
            # dithered fringe: this band's colour stippled one pixel into its neighbour
            ph = (i + frame + pass) % 2
            (a1 - a0).times do |k|
              next if ((k + ph) % 2) != 0
              if horiz
                Pix.rect(b, lo + k, top - 1, 1, 1, cols[pass])
                Pix.rect(b, lo + k, top + w, 1, 1, cols[pass])
              else
                Pix.rect(b, top - 1, lo + k, 1, 1, cols[pass])
                Pix.rect(b, top + w, lo + k, 1, 1, cols[pass])
              end
            end
          end
        end
        return if thin
        # streaks of turbulence sliding along the body
        n.times do |i|
          next if ((i + (frame * 3) + seed) % 7) != 0
          a0 = i * BEAM_CHUNK
          t = a0.to_f / major
          off = ((Util.hash01(i, seed, 4) > 0.5) ? 1 : -1) * thick * 0.31
          la = (horiz ? x0 : y0) + (sgn * a0)
          mid = ((horiz) ? y0 + (dy * t) : x0 + (dx * t)) + off
          if horiz then Pix.rect(b, [la, la + (sgn * 6)].min, mid, 6, 1, pal.inner)
          else Pix.rect(b, mid, [la, la + (sgn * 6)].min, 1, 6, pal.inner)
          end
        end
      end

      def orb(b, x, y, r, pal, frame)
        r = r.round
        return if r < 1
        Pix.disc(b, x, y, r + 1, pal.outline) if r >= 3
        Pix.disc(b, x, y, r, (frame.even?) ? pal.edge : pal.outer)
        Pix.disc(b, x, y, (r * 0.8).round, pal.outer)
        Pix.disc(b, x, y, (r * 0.58).round, pal.inner)
        Pix.disc(b, x, y, (r * 0.34).round, pal.core)
      end

      # Chunky four-point star: tapered bars, diagonals on odd frames.
      def star(b, x, y, len, col, frame, th = 1)
        len = len.round
        [[1.0, th], [0.6, th + 2]].each do |frac, t|
          l = (len * frac).round
          Pix.rect(b, x - l, y - (t / 2), (l * 2) + 1, t, col)
          Pix.rect(b, x - (t / 2), y - l, t, (l * 2) + 1, col)
        end
        return if frame.even?
        d = len / 2
        Pix.line(b, x - d, y - d, x + d, y + d, col, th)
        Pix.line(b, x - d, y + d, x + d, y - d, col, th)
      end

      # The clash sphere: dark outline, the two beams' colours swirling round
      # each other in a two-armed spiral, a scalloped white-hot core and a star.
      def clash_ball(b, cx, cy, r, pal_l, pal_r, frame)
        r = (r + ([0, 1, 3, 1][frame % 4] * ((r >= 14) ? 1 : 0.5))).round
        return if r < 1
        Pix.disc(b, cx, cy, r + 2, (frame.even?) ? pal_l.outline : pal_r.outline)
        Pix.disc(b, cx, cy, r + 1, (frame.even?) ? pal_r.edge : pal_l.edge)
        phase = frame * 0.5
        step = (r >= 12) ? 2 : 1
        (-r..r).step(step) do |dy|
          half = Math.sqrt((r * r) - (dy * dy)).round
          cur = nil
          start = -half
          x = -half
          while x <= half + step
            col = nil
            if x <= half
              d = Math.sqrt((x * x) + (dy * dy))
              k = Math.sin((Math.atan2(dy, x) * 2) + (d * 0.24) - phase)
              side = (k > 0) ? pal_l : pal_r
              col = (k.abs < 0.3) ? side.inner : side.outer
            end
            if col != cur
              Pix.rect(b, cx + start, cy + dy, x - start, step, cur) if cur
              cur = col
              start = x
            end
            x += step
          end
        end
        core = (r * 0.5).round
        8.times do |i|                                   # scalloped edge of the core, counter-rotating
          ang = (i * Math::PI / 4) - (frame * 0.3)
          Pix.disc(b, cx + (Math.cos(ang) * core), cy + (Math.sin(ang) * core), [(r * 0.16).round, 1].max, pal_l.core)
        end
        Pix.disc(b, cx, cy, core, pal_l.core)
        star(b, cx, cy, (r * 1.45) + ((frame % 3) * 3), pal_r.core, frame, (r >= 14) ? 3 : 1)
      end

      # Energy thrown out sideways from the clash point: tapered tongues that
      # lean back towards each beam's own side. (ux, uy) = beam direction.
      def splash(b, cx, cy, ux, uy, r, pal_a, pal_b, frame)
        px = -uy
        py = ux
        6.times do |i|
          side = (i.even?) ? 1 : -1                       # above / below the beam line
          own = (i < 3) ? -1 : 1                          # a's side / b's side
          pal = (own < 0) ? pal_a : pal_b
          len = r * (0.7 + (Util.hash01(i, frame / 2, 21) * 1.5))
          lean = 0.35 + (Util.hash01(i, frame / 2, 22) * 0.5)
          base = r * 0.25 * (1 + (i % 3))
          segs = [(len / 2).ceil, 1].max
          segs.times do |sgi|
            f = sgi / segs.to_f
            d = (r * 0.8) + (len * f)
            w = [(r * 0.5 * (1 - f) * (1 - f)).round, 1].max
            wob = Math.sin((f * 5) + (frame * 0.9) + i) * r * 0.1
            x = cx + (px * side * d) + (ux * (own * (base + (len * f * lean)) + wob))
            y = cy + (py * side * d) + (uy * (own * (base + (len * f * lean)) + wob))
            col = (f < 0.25) ? pal.core : ((f < 0.5) ? pal.inner : ((f < 0.8) ? pal.outer : pal.edge))
            Pix.rect(b, x - (w / 2) - 1, y - 1, w + 2, 4, pal.outline) if w > 3 && sgi.even?
            Pix.rect(b, x - (w / 2), y, w, 2, col)
          end
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
        if @k > 0.15                              # flat glow behind the actor
          @halo ||= Color.new(@pal.rgb[2][0], @pal.rgb[2][1], @pal.rgb[2][2], 96)
          Pix.disc(back, cx, cy, (r * 2.2).round + ((f.even?) ? 2 : 0), @halo)
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
        BeamDraw.star(front, cx, cy, (r * 1.5) + 3 + (f % 3), @pal.core, f, (r >= 8) ? 3 : 1) if @k > 0.5
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
        ry = [(r * @squash).round, 1].max
        b = (@back) ? back : front
        th = (@k < 0.3) ? 4 : ((@k < 0.65) ? 3 : 2)
        Pix.ring(b, cx, cy, r + 1, @pal.outline, th + 2, ry + 1) if @k < 0.65
        Pix.ring(b, cx, cy, r, @pal[(@k * 3.99).to_i], th, ry)
        Pix.ring(b, cx, cy, r - 1, @pal.core, 1, [ry - 1, 1].max) if @k < 0.4
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
        @width = a[:width] || 14
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
            scene.run_effect(ImpactBurst.new(scene, tgt, @pal, @width * 1.3, 0.45), scene.time)
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
        BeamDraw.orb(front, x0, y0, (w * 0.6) + (f % 2), @pal, f)
        BeamDraw.orb(front, hx, hy, (w * 0.75) + ((@landed) ? (f % 3) : 0), @pal, f)
        BeamDraw.star(front, hx, hy, w + 3 + (f % 3), @pal.core, f, (w >= 10) ? 3 : 1) if @landed
      end
    end

    #---------------------------------------------------------------------------
    # The beam clash
    #---------------------------------------------------------------------------
    class BeamClash < Effect
      Side = Struct.new(:from, :pal, :width, :actor)
      CURVES = {
        :even        => [[0, 0.5], [0.2, 0.42], [0.4, 0.58], [0.6, 0.44], [0.8, 0.56], [1, 0.5]],
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
        @launch = a[:launch] || [0.6, dur * 0.15].min
        @resolve = a[:resolve] || Util.clamp(dur * 0.28, 0.8, 2.2)
        curve = a[:curve] || { :a => :a_rallies, :b => :b_rallies }[@winner] || :even
        @curve = (curve.is_a?(Array)) ? curve : (CURVES[curve] || CURVES[:even])
        @mash = a[:mash] || @winner == :mash
        @player = a[:player] || :a
        @push = 0.0
        @pos = @curve[0][1].to_f
        @ball = a[:ball] || ((@a.width + @b.width) * 0.45)
        @ball_scale = 1.0
        @shake = a[:shake] || 4
        @strobe = a[:strobe] != false
        @ground = a[:ground]            # y of the ground under the clash (debris lifts from here)
        @white = 0.0
        @intensity = 1.0
        @rings = 0
        @next_ring = @launch
        @key = 1                        # next curve keyframe (a surge happens at each)
        @acc = 0.0
        @lift = 0.0
        @lt = 0.0
        @wf = [1.0, 1.0]                # width factors for a, b
        @se = a[:se] != false
        @mote = nil
        Sound.play(:se, :beam_fire) if @se
      end

      def side(scene, s)
        actor = (s[:from].is_a?(Symbol) && scene.actors[s[:from]]) ? s[:from] : nil
        return Side.new(scene.anchor(s[:from]), Util.palette(s[:color] || :light), s[:width] || 22, actor)
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

      def ground_y(c); return @ground || (c[1] + 70); end

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

      def palettes; return @a.pal.whitened(@white), @b.pal.whitened(@white); end

      # One push in the struggle: flash, kick, rings, a spray of energy and ice.
      def surge(scene, c, pa, pb, power = 1.0)
        pal_a, pal_b = palettes
        white = Util.palette(:white)
        scene.add_flash([255, 255, 255], 0.14, [110 * @intensity * power, 130].min)
        scene.add_shake((@shake + 4) * @intensity * power, 0.35)
        scene.run_effect(ShockRing.new(c, white, 120, 0.5, 0.5, true, @ball), scene.time)
        scene.run_effect(ShockRing.new([c[0], ground_y(c)], (@pos >= 0.5) ? pal_a : pal_b, 170, 0.8, 0.22, true, 20), scene.time)
        ang = Math.atan2(pb[1] - pa[1], pb[0] - pa[0]) * 180 / Math::PI
        [90, -90].each do |up|
          scene.burst_at(:sparks, c, 12, pal_a, { :angle => ang + up - 25, :spread => 40, :speed => 1.5 })
          scene.burst_at(:sparks, c, 12, pal_b, { :angle => ang + up + 25, :spread => 40, :speed => 1.5 })
        end
        g = [c[0], ground_y(c)]
        scene.burst_at(:ice_shards, g, 10, nil, { :speed => 1.2 })
        scene.burst_at(:debris, g, 6)
      end

      def struggle(scene, u, dt)
        c, pa, pb = clash_point
        if !@locked
          @locked = true
          Sound.play(:se, :beam_clash) if @se
          surge(scene, c, pa, pb, 1.4)
        end
        if @mash
          btn = Input.const_get(MASH_BUTTON)
          @push += ((@player == :a) ? 0.035 : -0.035) if Input.trigger?(btn)
          @push -= @push * 0.6 * dt
        end
        jitter = (Util.hash01(scene.fx_frame, 5) - 0.5) * 0.012
        @pos = Util.clamp(curve_at(u) + @push + jitter, 0.08, 0.92)
        c, pa, pb = clash_point
        while @key < @curve.length - 1 && u >= @curve[@key][0]      # the tide turns: surge
          @key += 1
          surge(scene, c, pa, pb)
        end
        pal_a, pal_b = palettes
        if @lt >= @next_ring                                         # shockwave rings on a quickening beat
          @next_ring = @lt + Util.lerp(0.55, 0.26, u)
          @rings += 1
          pal = [pal_a, pal_b, Util.palette(:white)][@rings % 3]
          scene.run_effect(ShockRing.new(c, pal, 70 + (@ball * 2) + (20 * u), 0.55, 0.5, true, @ball), scene.time)
          scene.add_flash([255, 255, 255], 0.08, 50 * @intensity) if @strobe && @rings.even?
        end
        @acc += 60 * @intensity * dt
        ang = Math.atan2(pb[1] - pa[1], pb[0] - pa[0]) * 180 / Math::PI
        while @acc >= 1                                              # energy sprayed out sideways
          @acc -= 1
          up = (scene.rng.rand < 0.5) ? 90 : -90
          pal = (scene.rng.rand < 0.5) ? pal_a : pal_b
          lean = (pal.equal?(pal_a)) ? -30 : 30
          scene.particles.spawn(:sparks, c[0], c[1] + ((up > 0) ? @ball : -@ball),
                                { :color => pal, :angle => ang + up + (lean * ((up > 0) ? -1 : 1)), :spread => 40, :speed => 1.3, :size => 2 })
        end
        @lift += 16 * @intensity * dt
        while @lift >= 1                                             # ice and rubble lifting off the ground
          @lift -= 1
          x = c[0] + ((scene.rng.rand - 0.5) * 240)
          scene.particles.spawn(:lift, x, ground_y(c) + (scene.rng.rand * 20),
                                { :color => (scene.rng.rand < 0.7) ? :ice : :rock, :size => (scene.rng.rand < 0.4) ? 3 : 2 })
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
        f = scene.fx_frame
        case @winner
        when :a, :b
          # the winning beam swells, swallows the other and washes the screen white
          r1 = 0.5
          target = (@winner == :a) ? 0.97 : 0.03
          if r < r1
            k = Ease.apply(:in_cubic, r / r1)
            @pos = Util.lerp(@pos0, target, k)
            grow = 1.0 + (0.5 * k)
            shrink = 1.0 - (0.5 * k)
            @wf = (@winner == :a) ? [grow, shrink] : [shrink, grow]
            @ball_scale = 1.0 + (0.5 * k)
            scene.camera.sx += Util.snap(((Util.hash01(f, 11) * 2) - 1) * @shake * (1 + (2 * k)))
            scene.camera.sy += Util.snap(((Util.hash01(f, 12) * 2) - 1) * @shake * (1 + k))
          elsif !@done
            @done = true
            @pos = target
            loser = (@winner == :a) ? @b : @a
            win = (@winner == :a) ? @a : @b
            pt = loser.from.call
            scene.run_effect(ImpactBurst.new(scene, pt, win.pal, win.width * 1.6, 0.8), scene.time)
            4.times { |i| scene.run_effect(ShockRing.new(pt, (i.odd?) ? Util.palette(:white) : win.pal, 110 + (i * 50), 0.7 + (i * 0.18), 0.5), scene.time) }
            scene.burst_at(:sparks, pt, 50, win.pal, { :speed => 1.6, :size => 2 })
            scene.burst_at(:debris, pt, 18)
            scene.burst_at(:ice_shards, [pt[0], ground_y(c)], 18)
            wash = [@resolve * (1 - r1), 0.6].max
            scene.add_flash([255, 255, 255], wash, 255, nil, wash * 0.35)
            scene.add_shake(16, 0.9)
            scene.hit_actor(loser.actor, (@winner == :a) ? dir : -dir, 26, 0.7) if loser.actor
            Sound.play(:se, :beam_break) if @se
          end
          if @done
            k = Util.clamp(1 - ((r - r1) / (1 - r1)), 0.0, 1.0)
            @wf = (@winner == :a) ? [1.5 * k, 0.0] : [0.0, 1.5 * k]
            @ball_scale = 0.0
          end
        when :both
          r1 = 0.5
          @ball_scale = 1.0 + (1.8 * Ease.apply(:in, r / r1)) if r < r1
          scene.camera.sx += Util.snap(((Util.hash01(f, 11) * 2) - 1) * @shake * 2) if r < r1
          if r >= r1 && !@done
            @done = true
            @wf = [0.0, 0.0]
            @ball_scale = 0.0
            white = Util.palette(:white)
            4.times { |i| scene.run_effect(ShockRing.new(c, [@a.pal, white, @b.pal, white][i], 120 + (i * 55), 0.7 + (i * 0.2), 0.5), scene.time) }
            scene.run_effect(ImpactBurst.new(scene, c, white, @ball * 1.8, 0.8), scene.time)
            scene.burst_at(:sparks, c, 40, @a.pal, { :speed => 1.6, :size => 2 })
            scene.burst_at(:sparks, c, 40, @b.pal, { :speed => 1.6, :size => 2 })
            scene.burst_at(:debris, c, 20)
            scene.burst_at(:ice_shards, [c[0], ground_y(c)], 24)
            wash = [@resolve * (1 - r1), 0.8].max
            scene.add_flash([255, 255, 255], wash, 255, nil, wash * 0.3)
            scene.add_shake(16, 1.0)
            scene.hit_actor(@a.actor, -dir, 24, 0.7) if @a.actor
            scene.hit_actor(@b.actor, dir, 24, 0.7) if @b.actor
            Sound.play(:se, :beam_break) if @se
          end
        when :fizzle
          r1 = 0.6
          if r < r1
            k = 1 - (r / r1)
            @ball_scale = [k, 0.2].max
            @wf = [[k, 0.3].max, [k, 0.3].max]      # stays a chunky beam until it cuts out
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
        pal_a, pal_b = palettes
        wa = @a.width * z * @wf[0]
        wb = @b.width * z * @wf[1]
        if @lt < @launch                            # both beams race to the meeting point
          k = Util.clamp(@lt / @launch, 0.0, 1.0)
          hax = (ax + ((cx - ax) * k)).round
          hay = (ay + ((cy - ay) * k)).round
          hbx = (bx + ((cx - bx) * k)).round
          hby = (by + ((cy - by) * k)).round
          BeamDraw.beam(front, ax, ay, hax, hay, pal_a, wa, f, 1)
          BeamDraw.beam(front, bx, by, hbx, hby, pal_b, wb, f, 2)
          BeamDraw.orb(front, hax, hay, wa * 0.62, pal_a, f)
          BeamDraw.orb(front, hbx, hby, wb * 0.62, pal_b, f)
        else
          gutter = @winner == :fizzle && @resolving && f.odd?   # guttering flicker
          # the stronger beam is drawn last so it overlaps the weaker one
          order = (wa >= wb) ? [[bx, by, pal_b, wb, 2], [ax, ay, pal_a, wa, 1]] : [[ax, ay, pal_a, wa, 1], [bx, by, pal_b, wb, 2]]
          order.each { |x, y, pal, w, seed| BeamDraw.beam(front, x, y, cx, cy, pal, w, f, seed) if w >= 0.5 && !gutter }
          if @ball_scale > 0
            r = @ball * z * @ball_scale
            len = Math.sqrt(((bx - ax)**2) + ((by - ay)**2))
            len = 1.0 if len < 1
            ux = (bx - ax) / len
            uy = (by - ay) / len
            BeamDraw.splash(front, cx, cy, ux, uy, r, pal_a, pal_b, f) if @ball_scale > 0.5 && !@mote
            left, right = (ax <= bx) ? [pal_a, pal_b] : [pal_b, pal_a]
            BeamDraw.clash_ball(front, cx, cy, r, left, right, f)
          end
        end
        BeamDraw.orb(front, ax, ay, (wa * 0.5) + (f % 2), pal_a, f) if wa > 1
        BeamDraw.orb(front, bx, by, (wb * 0.5) + (f % 2), pal_b, f) if wb > 1
        if @mote
          mx, my = scene.to_fx([@mote[0], @mote[1]])
          Pix.rect(front, mx, my - 4, 2, 4, Util.palette(:white).outer)
          Pix.rect(front, mx - 1, my, 4, 4, Util.palette(:white).core)
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
