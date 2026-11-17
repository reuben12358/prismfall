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
      COL = 2                                   # art pixels per beam column
      BANDS = [1.0, 0.86, 0.66, 0.42, 0.2]      # outline, edge, body, inner, core (share of thickness)

      module_function

      # Smooth pseudo-noise -1..1 that scrolls with the frame (the "flow").
      def flow(i, frame, k)
        return (Math.sin((i * 0.37) - (frame * 0.8) + (k * 1.7)) * 0.55) + (Math.sin((i * 0.13) + (frame * 0.23) + k) * 0.45)
      end

      # A turbulent beam from (x0, y0) to (x1, y1), in art pixels.
      #   nozzle: cone out of the mouth        head: rounded white-hot leading edge
      #   swell:  flares out where it slams into something
      # Each 2px column has its own top and bottom edge (so the silhouette
      # boils), band borders wander with a scrolling flow, and bright and dark
      # streaks run down the body.
      def beam(b, x0, y0, x1, y1, pal, width, frame, seed = 0, nozzle: true, head: false, swell: false)
        dx = x1 - x0
        dy = y1 - y0
        len = Math.sqrt((dx * dx) + (dy * dy))
        return if len < 1 || width < 0.5
        horiz = dx.abs >= dy.abs
        major = (horiz) ? dx.abs : dy.abs
        return if major < 1
        sgn = (horiz) ? (dx <=> 0) : (dy <=> 0)
        thick = width * len / major
        n = (major / COL.to_f).ceil
        cols = [pal.outline, pal.edge, pal.outer, pal.inner, pal.core]
        thin = thick < 6
        cap = thick * 0.75
        cone = thick * 1.3
        n.times do |i|
          a0 = i * COL
          a1 = [a0 + COL, major].min
          t = (a0 + a1) / 2.0 / major
          rest = major - a0
          prof = 1.0
          prof = 0.28 + (0.72 * (a0 / cone)) if nozzle && a0 < cone
          hot = 0.0
          if head && rest < cap                      # rounded leading edge, white-hot
            e = rest / cap
            prof *= 1.22 * Math.sqrt(1 - ((1 - e)**2)) + 0.08
            hot = 1 - e
          elsif swell && rest < cap                  # pressure front
            e = rest / cap
            prof *= 1.0 + (0.55 * (1 - e) * (1 - e))
            hot = (1 - e) * 0.7
          end
          up = (thick / 2.0) * prof * (1 + (0.11 * flow(i, frame, seed)))
          dn = (thick / 2.0) * prof * (1 + (0.11 * flow(i, frame, seed + 3)))
          up += 1 if Util.hash01(i, frame, seed) > 0.88
          dn += 1 if Util.hash01(i, frame, seed + 1) > 0.88
          mid = (horiz) ? y0 + (dy * t) : x0 + (dx * t)
          la = (horiz ? x0 : y0) + (sgn * a0)
          lb = (horiz ? x0 : y0) + (sgn * a1)
          lo = [la, lb].min
          last = 9.0
          5.times do |k|
            next if thin && (k == 1 || k == 3)
            f = BANDS[k]
            if k >= 2
              f *= 1 + (0.17 * flow(i * 1.3, frame * 1.4, seed + (k * 2)))
              f = Util.lerp(f, [0.9, 0.78, 0.62][k - 2], hot) if hot > 0
              f = [f, last - 0.05].min
            end
            last = f
            top = (mid - (up * f)).round
            bot = (mid + (dn * f)).round
            if k == 0
              top -= 1
              bot += 1
            elsif k >= 2 && ((i + k + frame) % 2) == 0       # dither teeth between bands
              top -= 1
              bot += 1
            end
            h = [bot - top, 1].max
            if horiz then Pix.rect(b, lo, top, a1 - a0, h, cols[k])
            else Pix.rect(b, top, lo, h, a1 - a0, cols[k])
            end
          end
        end
        return if thin
        streaks = (major / 6.0).ceil                          # flow streaks racing down the body
        streaks.times do |j|
          speed = 3 + (Util.hash01(j, seed, 31) * 5)
          a0 = ((Util.hash01(j, seed, 32) * major) + (frame * speed)) % major
          l = 4 + (Util.hash01(j, seed, 33) * 9).round
          l = [l, major - a0].min
          next if l < 2 || (nozzle && a0 < cone)
          off = (Util.hash01(j, seed, 34) - 0.5) * thick * 0.74
          tone = [pal.core, pal.inner, pal.edge, pal.inner][j % 4]
          tone = pal.outer if off.abs < thick * 0.12 && j.odd?     # dark thread in the core
          t = (a0 + (l / 2.0)) / major
          mid = ((horiz) ? y0 + (dy * t) : x0 + (dx * t)) + off
          la = (horiz ? x0 : y0) + (sgn * a0)
          lb = la + (sgn * l)
          th = (thick >= 20 && j % 3 == 0) ? 2 : 1
          if horiz then Pix.rect(b, [la, lb].min, mid, l, th, tone)
          else Pix.rect(b, mid, [la, lb].min, th, l, tone)
          end
        end
      end

      # Irregular blob: radius wobbles with the angle (spikes), turning with the
      # frame. The building block for flares and bursts (never a clean circle).
      def blob(b, cx, cy, r, col, frame, seed = 0, spikes = 6, amp = 0.3, spin = 0.25)
        return if r < 1
        reach = (r * (1 + amp)).ceil
        step = (r >= 14) ? 2 : 1
        rot = (frame * spin) + seed
        (-reach..reach).step(step) do |dy|
          start = nil
          x = -reach
          while x <= reach + step
            inside = false
            if x <= reach
              ang = Math.atan2(dy, x)
              lim = r * (1 + (amp * ((Math.sin((ang * spikes) + rot) * 0.6) + (Math.sin((ang * ((spikes * 2) + 1)) - (rot * 1.7)) * 0.4))))
              inside = ((x * x) + (dy * dy)) <= lim * lim
            end
            if inside && !start
              start = x
            elsif !inside && start
              Pix.rect(b, cx + start, cy + dy, x - start, step, col)
              start = nil
            end
            x += step
          end
        end
      end

      # Muzzle flare: a ragged, flickering burst (not concentric rings).
      def flare(b, x, y, r, pal, frame, seed = 0)
        return if r < 1
        r += frame % 2
        blob(b, x, y, r + 1.5, pal.outline, frame, seed, 7, 0.34)
        blob(b, x, y, r, pal.edge, frame, seed, 7, 0.34)
        blob(b, x, y, r * 0.8, pal.outer, frame, seed + 1, 6, 0.4, -0.3)
        blob(b, x, y, r * 0.55, pal.inner, frame, seed + 2, 5, 0.45)
        blob(b, x, y, r * 0.3, pal.core, frame, seed + 3, 4, 0.5, -0.4)
      end

      # Kept for small uses (charge motes, volleys): a soft orb with a ragged edge.
      def orb(b, x, y, r, pal, frame)
        flare(b, x, y, r, pal, frame)
      end

      # Chunky four-point glint.
      def star(b, x, y, len, col, frame, th = 1)
        blob(b, x, y, len * 0.42, col, frame, 0, 4, 1.25, 0.0)
      end

      # Forked pixel lightning between two points.
      def lightning(b, x0, y0, x1, y1, col, core, frame, seed, th = 2)
        segs = 4
        px = x0
        py = y0
        nx = -(y1 - y0)
        ny = (x1 - x0)
        nl = Math.sqrt((nx * nx) + (ny * ny))
        return if nl < 2
        segs.times do |i|
          f = (i + 1) / segs.to_f
          j = (i == segs - 1) ? 0 : (Util.hash01(frame / 2, seed, i) - 0.5) * 0.5
          qx = x0 + ((x1 - x0) * f) + (nx * j)
          qy = y0 + ((y1 - y0) * f) + (ny * j)
          Pix.line(b, px, py, qx, qy, col, th)
          Pix.line(b, px, py, qx, qy, core, 1) if th > 1 && i < 2
          px = qx
          py = qy
        end
      end

      # The clash point: a ragged white-hot burst with both beams' colours
      # boiling round it, a turning four-point glare and forked lightning.
      def clash_burst(b, cx, cy, r, pal_l, pal_r, frame)
        r += [0, 1, 3, 1][frame % 4] * ((r >= 12) ? 1 : 0.4)
        return if r < 1
        off = r * 0.3
        blob(b, cx, cy, r * 1.22, (frame.even?) ? pal_l.outline : pal_r.outline, frame, 5, 9, 0.3)
        blob(b, cx - off, cy, r, pal_l.edge, frame, 1, 7, 0.32, 0.35)
        blob(b, cx + off, cy, r, pal_r.edge, frame, 2, 7, 0.32, -0.35)
        blob(b, cx - off, cy, r * 0.82, pal_l.outer, frame, 3, 6, 0.36, 0.5)
        blob(b, cx + off, cy, r * 0.82, pal_r.outer, frame, 4, 6, 0.36, -0.5)
        blob(b, cx - (off * 0.6), cy, r * 0.6, pal_l.inner, frame, 5, 5, 0.4, -0.6)
        blob(b, cx + (off * 0.6), cy, r * 0.6, pal_r.inner, frame, 6, 5, 0.4, 0.6)
        blob(b, cx, cy, r * 0.44, pal_l.core, frame, 7, 9, 0.38, 0.7)
        blob(b, cx, cy, r * 0.36, pal_l.core, frame, 8, 4, 1.35, 0.12)     # glare
        5.times do |i|
          ang = (Util.hash01(frame / 2, i, 41) * Math::PI * 2)
          l0 = r * 0.9
          l1 = r * (1.5 + (Util.hash01(frame / 2, i, 42) * 0.9))
          pal = (Math.cos(ang) < 0) ? pal_l : pal_r
          lightning(b, cx + (Math.cos(ang) * l0), cy + (Math.sin(ang) * l0), cx + (Math.cos(ang) * l1), cy + (Math.sin(ang) * l1),
                    pal.inner, pal.core, frame, i, (r >= 12) ? 2 : 1)
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
        r = [@size * @k, 1].max * z
        Dither.glow(back, cx, cy, (r * 3.2) + 6, (r * 3.2) + 6, @pal.rgb[2]) if @k > 0.1     # light gathering behind
        18.times do |i|                           # motes and shards pulled inward along curved paths
          ph = ((@k * 3) + (i / 18.0)) % 1.0
          dist = (1 - ph) * (26 + (@size * 2.4)) * z
          ang = (i * 2.399) + (@k * 2.5) + (ph * 1.2)
          x = cx + (Math.cos(ang) * dist)
          y = cy + (Math.sin(ang) * dist * 0.85)
          tx = Math.cos(ang) * (2 + (ph * 4))
          ty = Math.sin(ang) * (2 + (ph * 4))
          Pix.line(front, x + tx, y + ty, x, y, (ph > 0.6) ? @pal.inner : @pal.outer, (ph > 0.8) ? 2 : 1)
          Pix.rect(front, x, y, 1, 1, @pal.core)
        end
        BeamDraw.flare(front, cx, cy, r, @pal, f, 3)
        BeamDraw.blob(front, cx, cy, (r * 0.9) + 2, @pal.core, f, 9, 4, 1.4, 0.2) if @k > 0.6 && f % 3 != 0
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
        if @k < 0.45
          r = (@size * (0.5 + (@k * 2.0)) * z).round
          BeamDraw.blob(front, cx, cy, r * 1.1, @pal.outline, f, 1, 9, 0.4, 0.5)
          BeamDraw.blob(front, cx, cy, r, @pal.outer, f, 1, 9, 0.4, 0.5)
          BeamDraw.blob(front, cx, cy, r * 0.72, @pal.inner, f, 2, 7, 0.45, -0.5)
          BeamDraw.blob(front, cx, cy, r * 0.46, @pal.core, f, 3, 5, 0.9, 0.3)
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
        BeamDraw.beam(front, x0, y0, hx, hy, @pal, w, f, 0, head: !@landed, swell: @landed)
        BeamDraw.flare(front, x0, y0, w * 0.5, @pal, f, 1)
        if @landed
          BeamDraw.blob(front, hx, hy, w * 0.7, @pal.inner, f, 2, 7, 0.45, 0.6)
          BeamDraw.blob(front, hx, hy, w * 0.45, @pal.core, f, 3, 5, 0.9, -0.4)
        end
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
          scene.run_effect(ShockRing.new(c, pal, 70 + (@ball * 2) + (20 * u), 0.55, 0.5, true, @ball), scene.time) if !@no_rings
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
        @steam = (@steam || 0.0) + (22 * @intensity * dt)
        while @steam >= 1                                            # steam where fire meets ice
          @steam -= 1
          scene.particles.spawn(:steam, c[0] + ((scene.rng.rand - 0.5) * @ball * 2), c[1] - (@ball * 0.5), { :size => 3 + scene.rng.rand(2), :speed => 1.6 })
          scene.particles.spawn(:steam, c[0] + ((scene.rng.rand - 0.5) * 200), ground_y(c), { :size => 2 + scene.rng.rand(2), :layer => :back })
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

      # Light on the two Pokemon: a rim on the side facing the clash and a tint
      # towards their own beam, flickering with the struggle.
      def light_actors(scene, on)
        [[@a, 1], [@b, -1]].each do |sd, dir|
          act = sd.actor && scene.actors[sd.actor]
          next if !act
          @base_tint ||= {}
          @base_tint[sd.actor] ||= act.tint.dup
          if on
            c = sd.pal.whitened(@white).rgb[1]
            flick = (scene.fx_frame.even?) ? 78 : 52
            act.tint = [c[0].to_f, c[1].to_f, c[2].to_f, flick * [@intensity, 0.4].max]
            act.set_rim(scene, Util.palette(:white).rgb[0], dir * @dir_x)
          else
            act.tint = @base_tint[sd.actor]
            act.set_rim(scene, nil)
          end
        end
      end

      def dispose
        return if !@scene_ref
        light_actors(@scene_ref, false)
      end

      def draw(scene, back, front)
        @scene_ref = scene
        c, pa, pb = clash_point
        ax, ay = scene.to_fx(pa)
        bx, by = scene.to_fx(pb)
        cx, cy = scene.to_fx(c)
        f = scene.fx_frame
        z = scene.camera.zoom
        @dir_x = ((bx - ax) <=> 0)
        @dir_x = 1 if @dir_x == 0
        pal_a, pal_b = palettes
        wa = @a.width * z * @wf[0]
        wb = @b.width * z * @wf[1]
        _gx, gy = scene.to_fx([c[0], ground_y(c)])
        if @lt < @launch                            # both beams race to the meeting point
          k = Util.clamp(@lt / @launch, 0.0, 1.0)
          hax = (ax + ((cx - ax) * k)).round
          hay = (ay + ((cy - ay) * k)).round
          hbx = (bx + ((cx - bx) * k)).round
          hby = (by + ((cy - by) * k)).round
          ground_light(back, ax, hax, gy, wa, pal_a, f)
          ground_light(back, bx, hbx, gy, wb, pal_b, f)
          BeamDraw.beam(front, ax, ay, hax, hay, pal_a, wa, f, 1, head: true)
          BeamDraw.beam(front, bx, by, hbx, hby, pal_b, wb, f, 2, head: true)
        else
          light_actors(scene, @wf[0] + @wf[1] > 0.2 && !@mote)
          gutter = @winner == :fizzle && @resolving && f.odd?   # guttering flicker
          ground_light(back, ax, cx, gy, wa, pal_a, f) if wa >= 2
          ground_light(back, bx, cx, gy, wb, pal_b, f) if wb >= 2
          if @ball_scale > 0.3                                   # white pool of light under the clash
            r = @ball * z * @ball_scale
            Dither.disc(back, cx, gy, r * 2.4, r * 0.4, Util.palette(:white).rgb[1], 8)
            Dither.disc(back, cx, gy, r * 1.4, r * 0.24, Util.palette(:white).rgb[0], 4)
          end
          # the stronger beam is drawn last so it overlaps the weaker one
          order = (wa >= wb) ? [[bx, by, pal_b, wb, 2], [ax, ay, pal_a, wa, 1]] : [[ax, ay, pal_a, wa, 1], [bx, by, pal_b, wb, 2]]
          order.each { |x, y, pal, w, seed| BeamDraw.beam(front, x, y, cx, cy, pal, w, f, seed, swell: @ball_scale > 0) if w >= 0.5 && !gutter }
          if @ball_scale > 0
            left, right = (ax <= bx) ? [pal_a, pal_b] : [pal_b, pal_a]
            BeamDraw.clash_burst(front, cx, cy, @ball * z * @ball_scale, left, right, f)
          end
        end
        BeamDraw.flare(front, ax, ay, wa * 0.42, pal_a, f, 11) if wa > 1
        BeamDraw.flare(front, bx, by, wb * 0.42, pal_b, f, 12) if wb > 1
        if @mote
          mx, my = scene.to_fx([@mote[0], @mote[1]])
          Pix.rect(front, mx, my - 4, 2, 4, Util.palette(:white).outer)
          Pix.rect(front, mx - 1, my, 4, 4, Util.palette(:white).core)
        end
      end

      # Beam light thrown on the ground along its length (dithered, flickering).
      def ground_light(b, x0, x1, gy, width, pal, f)
        return if width < 2 || (x1 - x0).abs < 4
        lo = [x0, x1].min
        len = (x1 - x0).abs
        h = [(width * 0.2).round, 3].max + (f % 2)
        Dither.fill(b, lo - 4, gy - h, len + 8, h * 2, pal.rgb[2], 8)
        Dither.fill(b, lo, gy - (h / 2), len, h, pal.rgb[2], 4)
        Dither.fill(b, lo + 6, gy - 1, len - 12, 2, pal.rgb[1], 2)
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
