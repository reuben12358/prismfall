#===============================================================================
# Prismfall Cutscenes - 009 Armies: crowds, marching, clashing, volleys
#-------------------------------------------------------------------------------
#   army :ashkaar, icons: [:CHARIZARD, :SALAMENCE], count: 18, area: [x, y, w, h],
#        facing: :right, rows: 3
#   army :isenmar, charset: :ISENMAR_SOLDIER (trainer type or file name) / color: [r, g, b]
#   march :ashkaar, by: [120, 0], duration: 3
#   clash_armies :ashkaar, :isenmar, duration: 4, casualties: 0.3
#   volley from: :ashkaar, to: :isenmar, kind: :fire, count: 14, duration: 1.6
#   rout :isenmar, by: [200, 0]      army_fall :isenmar, fraction: 0.5
#   army_tint :isenmar, color: :bleed, amount: 200   (glassing)
#===============================================================================
module Prismfall
  module Cutscene
    class Army
      Unit = Struct.new(:x, :y, :sprite, :gfx, :phase, :alive, :ox, :oy, :flash, :fall)

      attr_accessor :off_x, :off_y, :walking, :facing, :tint, :opacity
      attr_reader :id, :units

      def initialize(scene, id, o)
        @id = id
        @facing = o[:facing] || :right
        @off_x = @off_y = 0.0
        @walking = o[:walk] || false
        @opacity = 255.0
        @tint = [0.0, 0.0, 0.0, 0.0]
        @time = 0.0
        @scale = o[:scale] || 1
        @gfx = []
        if o[:icons] || o[:icon]
          @gfx = Array(o[:icons] || o[:icon]).map { |s| Gfx.icon(s) }
        elsif o[:charsets] || o[:charset]
          @gfx = Array(o[:charsets] || o[:charset]).map { |c| Gfx.charset(c, o[:color]) }
        else
          @gfx = [Gfx.placeholder_charset(o[:color] || [160, 160, 176])]
        end
        ax, ay, aw, ah = o[:area] || [0, 240, 200, 80]
        count = o[:count] || 12
        rows = [o[:rows] || 3, count].min
        cols = (count / rows.to_f).ceil
        seed = id.to_s.sum
        @units = []
        count.times do |i|
          r = i % rows
          c = i / rows
          x = ax + (aw * (c + 0.5 + ((r.odd?) ? 0.35 : 0)) / cols) + ((Util.hash01(i, seed, 1) - 0.5) * 10)
          y = ay + ((rows > 1) ? ah * r / (rows - 1.0) : ah / 2.0) + ((Util.hash01(i, seed, 2) - 0.5) * 6)
          g = @gfx[i % @gfx.length]
          s = Sprite.new(scene.viewport)
          s.bitmap = g.bitmap
          s.ox = g.fw / 2
          s.oy = g.fh
          s.color = Color.new(0, 0, 0, 0)
          @units.push(Unit.new(x, y, s, g, Util.hash01(i, seed, 3) * 4, true, 0.0, 0.0, 0.0, 0.0))
        end
        update(scene, 0)
      end

      def alive; return @units.select(&:alive); end

      def center
        list = alive
        list = @units if list.empty?
        return [(list.sum(&:x) / list.length) + @off_x, (list.sum(&:y) / list.length) + @off_y]
      end

      def random_point(rng)
        list = alive
        list = @units if list.empty?
        u = list[rng.rand(list.length)]
        return [u.x + @off_x, u.y + @off_y - (u.gfx.fh * u.gfx.px * @scale * 0.5)]
      end

      # x of the rank nearest the enemy.
      def front_x
        xs = alive.map(&:x)
        xs = @units.map(&:x) if xs.empty?
        return ((@facing == :right) ? xs.max : xs.min) + @off_x
      end

      def update(scene, dt)
        @time += dt
        cam = scene.camera
        row = Gfx::DIR_ROWS[@facing] || 0
        @units.each do |u|
          s = u.sprite
          g = u.gfx
          if u.fall > 0 && u.fall < 1
            u.fall = [u.fall + (dt * 2.2), 1.0].min
          end
          u.flash = [u.flash - (dt * 4), 0.0].max
          hop = 0.0
          if g.mode == :charset
            col = (@walking && u.alive) ? ((@time * 6) + u.phase).to_i % 4 : 0
            s.src_rect.set(col * g.fw, row * g.fh, g.fw, g.fh)
          else
            col = ((@time * 4) + u.phase).to_i % g.frames
            s.src_rect.set(col * g.fw, 0, g.fw, g.fh)
            s.mirror = (@facing == :right)
            hop = (@walking && u.alive) ? -(Math.sin(((@time * 6) + u.phase) * Math::PI).abs * 4) : 0.0
          end
          sx, sy = cam.to_screen(u.x + @off_x + u.ox, u.y + @off_y + u.oy + hop + (u.fall * 4), 1.0)
          if cam.zoom == 1.0
            sx = Util.snap(sx)
            sy = Util.snap(sy)
          end
          s.x = sx.round
          s.y = sy.round
          s.zoom_x = s.zoom_y = g.px * @scale * cam.zoom
          s.z = 500 + (u.y + @off_y).round
          s.angle = 0                                   # fallen units fade where they stand (no rotated pixels)
          s.opacity = (@opacity * ((u.fall > 0) ? 1 - (u.fall * 0.8) : 1)).round
          sil = scene.silhouette_rgb
          if sil then s.color.set(sil[0], sil[1], sil[2], 255)
          elsif u.flash > 0 then s.color.set(255, 255, 255, 255 * u.flash)
          else s.color.set(@tint[0], @tint[1], @tint[2], @tint[3])
          end
        end
      end

      def fell(unit)
        return if !unit || !unit.alive
        unit.alive = false
        unit.flash = 1.0
        unit.fall = 0.01
      end

      def fell_random(rng, near = nil)
        list = alive
        return nil if list.empty?
        u = (near) ? list.min_by { |v| ((v.x + @off_x - near[0])**2) + ((v.y + @off_y - near[1])**2) } : list[rng.rand(list.length)]
        fell(u)
        return u
      end

      def dispose
        @units.each { |u| u.sprite.dispose if !u.sprite.disposed? }
        @gfx.each { |g| Gfx.dispose(g) }
      end
    end

    # Both hosts surge together; soldiers lunge, sparks fly, some fall.
    class ArmyClash < Effect
      def initialize(scene, a, dur)
        @a = scene.army!(a[:a])
        @b = scene.army!(a[:b])
        @dur = dur
        @cas = a[:casualties] || 0.3
        gap = (@b.front_x - @a.front_x).abs - (a[:gap] || 26)
        dir = (@b.front_x >= @a.front_x) ? 1 : -1
        @close = [gap / 2.0, 0].max * dir
        @a0 = @a.off_x
        @b0 = @b.off_x
        @kills = [(@a.units.length * @cas).round, (@b.units.length * @cas).round]
        @done_kills = [0, 0]
        @acc = 0.0
        @se_t = 0.0
      end

      def update(scene, lt, dt)
        raw = Util.clamp(lt / @dur, 0.0, 1.0)
        k = Ease.apply(:in_out, Util.clamp(raw / 0.3, 0.0, 1.0))
        @a.off_x = @a0 + (@close * k)
        @b.off_x = @b0 - (@close * k)
        @a.walking = @b.walking = raw < 0.3
        return true if raw >= 1.0
        return false if raw < 0.3
        t = scene.time
        [@a, @b].each_with_index do |army, n|
          dir = ((army.facing == :right) ? 1 : -1)
          army.units.each_with_index do |u, i|
            next if !u.alive
            w = ((t * 1.6) + u.phase + (i * 0.37)) % 1.0
            u.ox = dir * 9 * ((w < 0.25) ? Math.sin(w * 4 * Math::PI) : 0)
          end
          want = (@kills[n] * (raw - 0.3) / 0.7).floor
          while @done_kills[n] < want
            @done_kills[n] += 1
            front = [(@a.front_x + @b.front_x) / 2.0, army.center[1] + ((scene.rng.rand - 0.5) * 80)]
            army.fell_random(scene.rng, front)
          end
        end
        @acc += 14 * dt
        mid = (@a.front_x + @b.front_x) / 2.0
        cy = (@a.center[1] + @b.center[1]) / 2.0
        while @acc >= 1
          @acc -= 1
          y = cy + ((scene.rng.rand - 0.5) * 90)
          scene.burst_at(:sparks, [mid + ((scene.rng.rand - 0.5) * 30), y - 16], 3, :light, { :speed => 0.5 })
          scene.particles.spawn(:smoke, mid + ((scene.rng.rand - 0.5) * 40), y, { :layer => :back, :size => 2 })
        end
        scene.camera.sy += (scene.fx_frame % 4 == 0) ? PX : 0
        return false
      end

      def dispose
        (@a.units + @b.units).each { |u| u.ox = 0.0 }
      end
    end

    # A flight of projectiles on arcs, drawn as 2px heads with fading tails.
    class Volley < Effect
      Shot = Struct.new(:x0, :y0, :x1, :y1, :t0, :flight, :arc, :landed)
      KINDS = { :fire => :fire, :ice => :ice, :water => :water, :arrow => :steel, :rock => :rock,
                :dragon => :dragon, :electric => :electric }

      def initialize(scene, a, dur)
        @a = a
        @pal = Util.palette(a[:color] || KINDS[a[:kind] || :fire] || :fire)
        @dur = dur
        @kind = a[:kind] || :fire
        n = a[:count] || 12
        flight = a[:flight] || [dur * 0.6, 0.25].max
        spread = [dur - flight, 0].max
        arc = a[:arc] || 70
        @shots = Array.new(n) do |i|
          x0, y0 = scene.point(a[:from])
          x1, y1 = scene.point(a[:to])
          Shot.new(x0, y0, x1, y1, spread * i / [n - 1, 1].max.to_f, flight * (0.85 + (scene.rng.rand * 0.3)),
                   arc * (0.7 + (scene.rng.rand * 0.6)), false)
        end
        @target = (a[:to].is_a?(Symbol) && scene.armies[a[:to]]) ? scene.armies[a[:to]] : nil
        @kills = ((a[:casualties] || 0) * n).round
        @lt = 0.0
      end

      def draws?; return true; end

      def pos(s, u)
        return Util.lerp(s.x0, s.x1, u), Util.lerp(s.y0, s.y1, u) - (s.arc * 4 * u * (1 - u))
      end

      def update(scene, lt, dt)
        @lt = lt
        @shots.each do |s|
          next if s.landed || lt < s.t0 + s.flight
          s.landed = true
          pt = [s.x1, s.y1]
          scene.burst_at((@kind == :ice) ? :ice_shards : :sparks, pt, 6, @pal, { :speed => 0.6 })
          scene.particles.spawn((@kind == :fire) ? :smoke : :steam, pt[0], pt[1], { :size => 2 })
          if @target && @kills > 0
            @kills -= 1
            @target.fell_random(scene.rng, pt)
          end
        end
        scene.camera.sy += PX if @a[:shake] && @shots.any? { |s| s.landed && lt - (s.t0 + s.flight) < 0.08 }
        return lt >= @dur && @shots.all?(&:landed)
      end

      def draw(scene, back, front)
        @shots.each do |s|
          u = (@lt - s.t0) / s.flight
          next if u < 0 || u > 1
          3.downto(0) do |i|
            uu = u - (i * 0.035)
            next if uu < 0
            x, y = scene.to_fx(pos(s, uu))
            size = (i == 0) ? 2 : 1
            Pix.rect(front, x, y, size, size, @pal[i])
          end
        end
      end
    end

    class Scene
      def op_army(a, _dur)
        @armies[a[:id]].dispose if @armies[a[:id]]
        @armies[a[:id]] = Army.new(self, a[:id], a)
        nil
      end

      def op_march(a, dur)
        army = army!(a[:id])
        x0, y0 = army.off_x, army.off_y
        by = a[:by] || [0, 0]
        army.walking = true
        tween(dur, a[:ease] || :linear) do |k, raw|
          army.off_x = x0 + (by[0] * k)
          army.off_y = y0 + (by[1] * k)
          army.walking = false if raw >= 1
        end
      end

      # The host turns and runs, fading out.
      def op_rout(a, dur)
        army = army!(a[:id])
        x0 = army.off_x
        by = a[:by] || [(army.facing == :right) ? -220 : 220, 0]
        army.facing = (army.facing == :right) ? :left : :right
        army.walking = true
        o0 = army.opacity
        tween(dur, :in) do |k, raw|
          army.off_x = x0 + (by[0] * k)
          army.opacity = o0 * (1 - ((a[:fade] == false) ? 0 : k))
          army.walking = false if raw >= 1
        end
      end

      def op_army_tint(a, dur)
        army = army!(a[:id])
        from = army.tint.dup
        c = Util.rgb(a[:color] || [255, 255, 255])
        to = [c[0].to_f, c[1].to_f, c[2].to_f, (a[:amount] || 160).to_f]
        from[0, 3] = to[0, 3] if from[3] <= 0
        tween(dur, :linear) { |k, _| army.tint = [0, 1, 2, 3].map { |i| Util.lerp(from[i], to[i], k) } }
      end

      # A share of the host is thrown flat over the duration.
      def op_army_fall(a, dur)
        army = army!(a[:id])
        total = (army.alive.length * (a[:fraction] || 0.5)).round
        done = 0
        tween(dur, :linear) do |k, _|
          want = (total * k).round
          while done < want
            done += 1
            army.fell_random(@rng)
          end
        end
      end

      def op_clash_armies(a, dur); return ArmyClash.new(self, a, dur); end
      def op_volley(a, dur);       return Volley.new(self, a, dur); end
    end
  end
end
