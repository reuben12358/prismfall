#===============================================================================
# Prismfall Cutscenes - 007 Particles, burning/freezing overlays, the dome
#-------------------------------------------------------------------------------
# emit :embers / :snow / :rain / :debris / :sparks / :smoke / :steam /
#      :ice_shards / :petals / :motes
#   at: point, area: [x, y, w, h], from: actor  (none = the whole screen, as weather)
#   rate: per second, duration: seconds (none = until stop_emit / scene end),
#   color: palette, id: name for stop_emit, layer: :back / :front
# burst kind, at:, count:, color:   - one-off puff
#===============================================================================
module Prismfall
  module Cutscene
    class Particles
      P = Struct.new(:x, :y, :vx, :vy, :age, :life, :ramp, :size, :grav, :back, :screen, :streak, :sway, :seed, :shape)

      # kind => [speed range, angle centre (deg, 0 = right, 90 = down), spread,
      #          life range, gravity, size, streak, sway, default palette, weather?]
      PRESETS = {
        :embers     => { :speed => [14, 44],  :angle => -90, :spread => 35,  :life => [1.4, 3.0], :grav => -6,  :size => 1, :sway => 10, :pal => :fire,  :weather => :bottom },
        :snow       => { :speed => [14, 30],  :angle => 100, :spread => 20,  :life => [5.0, 8.0], :grav => 0,   :size => 1, :sway => 12, :pal => :white, :weather => :top },
        :rain       => { :speed => [260, 320], :angle => 105, :spread => 3,  :life => [0.9, 1.2], :grav => 0,   :size => 1, :streak => 4, :pal => :water, :weather => :top },
        :debris     => { :speed => [40, 130], :angle => -90, :spread => 60,  :life => [0.6, 1.2], :grav => 260, :size => 2, :pal => :rock, :shape => :shard },
        :ice_shards => { :speed => [50, 150], :angle => -90, :spread => 70,  :life => [0.6, 1.1], :grav => 240, :size => 2, :pal => :ice, :shape => :shard },
        :sparks     => { :speed => [60, 190], :angle => 0,   :spread => 180, :life => [0.2, 0.55], :grav => 60, :size => 1, :streak => 2, :pal => :electric },
        :smoke      => { :speed => [8, 22],   :angle => -90, :spread => 25,  :life => [1.6, 2.8], :grav => -4,  :size => 3, :sway => 6, :pal => :smoke, :shape => :puff },
        :steam      => { :speed => [12, 30],  :angle => -90, :spread => 40,  :life => [1.2, 2.4], :grav => -8,  :size => 3, :sway => 8, :pal => :steam, :shape => :puff },
        :petals     => { :speed => [20, 50],  :angle => 70,  :spread => 50,  :life => [2.0, 3.5], :grav => 8,   :size => 2, :sway => 18, :pal => :fairy },
        :lift       => { :speed => [14, 46],  :angle => -90, :spread => 22,  :life => [0.9, 2.0], :grav => -30, :size => 3, :sway => 5, :pal => :ice, :shape => :shard },
        :motes      => { :speed => [4, 14],   :angle => -90, :spread => 180, :life => [1.5, 3.0], :grav => 0,   :size => 1, :sway => 4, :pal => :light }
      }

      attr_reader :count

      def initialize(scene)
        @scene = scene
        @list = []
        @count = 0
      end

      def spawn(kind, wx, wy, o = {})
        return if @list.length >= MAX_PARTICLES
        pr = PRESETS[kind] || PRESETS[:sparks]
        rng = @scene.rng
        sp = Util.lerp(pr[:speed][0], pr[:speed][1], rng.rand) * (o[:speed] || 1.0)
        ang = ((o[:angle] || pr[:angle]) + ((rng.rand - 0.5) * 2 * (o[:spread] || pr[:spread]))) * Math::PI / 180
        life = Util.lerp(pr[:life][0], pr[:life][1], rng.rand) * (o[:life] || 1.0)
        pal = Util.palette(o[:color] || pr[:pal])
        @list.push(P.new(wx, wy, Math.cos(ang) * sp, Math.sin(ang) * sp, 0.0, life, pal, o[:size] || pr[:size],
                         pr[:grav], o[:layer] == :back, o[:screen] || false, pr[:streak], pr[:sway] || 0, rng.rand * 6.28, pr[:shape]))
        @count = @list.length
      end

      def update(dt)
        @list.reject! do |p|
          p.age += dt
          p.vy += p.grav * dt
          p.x += (p.vx + (Math.sin((p.age * 2.2) + p.seed) * p.sway)) * dt
          p.y += p.vy * dt
          p.age >= p.life
        end
        @count = @list.length
      end

      def draw(back, front)
        cam = @scene.camera
        @list.each do |p|
          if p.screen then sx, sy = p.x, p.y
          else sx, sy = cam.to_screen(p.x, p.y, 1.0)
          end
          k = p.age / p.life
          c = p.ramp[(k * 3.99).to_i]
          size = (p.size > 1 && k > 0.6) ? p.size - 1 : p.size
          b = (p.back) ? back : front
          x = (sx / PX).round
          y = (sy / PX).round
          if p.streak
            # a short tail against the direction of travel
            tx = (p.vx.abs > p.vy.abs) ? -(p.vx <=> 0) : 0
            ty = (p.vx.abs > p.vy.abs) ? 0 : -(p.vy <=> 0)
            p.streak.times { |i| Pix.rect(b, x + (tx * i), y + (ty * i), 1, 1, (i == 0) ? p.ramp.core : c) }
          elsif p.shape == :shard               # jagged chips, four variants, tumbling
            v = ((p.seed * 10) + (p.age * 6)).to_i % 4
            hi = p.ramp.core
            case v
            when 0 then Pix.rect(b, x, y, size, 1, c); Pix.rect(b, x + 1, y + 1, size, 1, c); Pix.rect(b, x, y, 1, 1, hi)
            when 1 then Pix.rect(b, x, y, 1, size + 1, c); Pix.rect(b, x + 1, y, 1, size - 1, c); Pix.rect(b, x, y, 1, 1, hi)
            when 2 then Pix.rect(b, x, y, size, size, c); Pix.rect(b, x + size, y - 1, 1, 1, c); Pix.rect(b, x, y, 1, 1, hi)
            else        Pix.rect(b, x, y + 1, size + 1, 1, c); Pix.rect(b, x + 1, y, size - 1, 1, hi)
            end
          elsif p.shape == :puff                # soft-edged puffs that thin out as they age
            r = p.size + ((k < 0.5) ? 1 : 0)
            Dither.disc(b, x, y, r, r, p.ramp.rgb[1 + (k * 2.99).to_i], (k > 0.6) ? 4 : 2)     # see-through wisps
            Pix.disc(b, x, y, [r - 2, 1].max, c) if k < 0.35
          else
            Pix.rect(b, x, y, size, size, c)
          end
        end
      end
    end

    class Emitter < Effect
      def initialize(scene, kind, a, dur)
        @kind = kind
        @a = a
        @dur = dur
        @rate = (a[:rate] || 20).to_f
        @acc = 0.0
        @stopped = false
        pr = Particles::PRESETS[kind] || {}
        spec = a[:at] || a[:from] || a[:area]
        if spec
          @src = (spec.is_a?(Symbol) && scene.armies[spec]) ? proc { scene.point(spec) } : scene.anchor(spec)
          @area = a[:area]
          @screen = false
        else   # weather: whole screen, in screen space
          @screen = true
          @edge = pr[:weather] || :all
        end
        @opts = { :color => a[:color], :layer => a[:layer], :speed => a[:speed], :angle => a[:angle],
                  :spread => a[:spread], :life => a[:life], :size => a[:size], :screen => @screen }
      end

      def stop; @stopped = true; end

      def update(scene, lt, dt)
        return true if @stopped || (@dur && @dur > 0 && lt >= @dur)
        @acc += @rate * dt
        while @acc >= 1
          @acc -= 1
          if @screen
            x = (scene.rng.rand * (scene.w + 120)) - 60
            y = case @edge
                when :top    then -6
                when :bottom then scene.h - (scene.rng.rand * scene.h * 0.35)
                else scene.rng.rand * scene.h
                end
            scene.particles.spawn(@kind, x, y, @opts)
          else
            x, y = (@area) ? scene.point(@area) : @src.call
            scene.particles.spawn(@kind, x, y, @opts)
          end
        end
        return false
      end
    end

    # A dome of light swelling from a point (the Bleed dome of the war climax).
    # Scanline-dithered so the scene stays visible inside it.
    class Dome < Effect
      attr_accessor :radius, :hole

      def initialize(scene, a)
        @at = scene.anchor(a[:at] || [scene.w / 2, scene.h / 2])
        @pal = Util.palette(a[:color] || :bleed)
        @squash = a[:squash] || 0.6
        @radius = 0.0
        @hole = 0.0                   # radius of a clear circle around hole_at (e.g. the PC)
        @hole_at = nil
      end

      def set_hole(anchor); @hole_at = anchor; end
      def draws?; return true; end
      def update(scene, lt, dt); return false; end   # lives until `dome off: true`

      # A flat translucent disc (no stripes) with a chunky dithered rim and
      # glints; the hole is cut row by row.
      def draw(scene, back, front)
        cx, cy = scene.to_fx(@at.call)
        z = scene.camera.zoom
        rx = (@radius * z / PX).round
        ry = (rx * @squash).round
        return if rx < 2 || ry < 2
        f = scene.fx_frame
        @fill ||= @pal.rgb[1..3].map { |c| Color.new(c[0], c[1], c[2], 84) }
        fill = @fill[(f / 8) % 3]
        hx = hy = hr = nil
        if @hole_at && @hole > 1
          hx, hy = scene.to_fx(@hole_at.call)
          hr = (@hole * z / PX).round
        end
        run_w = nil
        run_y = 0
        (-ry..ry + 1).each do |dy|
          y = cy + dy
          in_hole = hr && dy <= ry && (y - hy).abs < hr * @squash
          w = (dy > ry) ? nil : (rx * Math.sqrt(1.0 - ((dy.to_f / ry)**2))).round
          key = (in_hole) ? [:hole, dy] : w
          next if key == run_w
          Pix.rect(back, cx - run_w, cy + run_y, (run_w * 2) + 1, dy - run_y, fill) if run_w.is_a?(Integer)
          run_w = key
          run_y = dy
          next if !in_hole
          hw = (hr * Math.sqrt(1.0 - (((y - hy) / (hr * @squash))**2))).round
          Pix.rect(back, cx - w, y, (hx - hw) - (cx - w), 1, fill)
          Pix.rect(back, hx + hw, y, (cx + w) - (hx + hw), 1, fill)
        end
        Pix.ring(front, cx, cy, rx, @pal.core, 2, ry)
        Pix.ring(front, cx, cy, rx + 3, @pal[1 + ((f / 4) % 3)], 1, ry + 2)
        14.times do |i|                                   # glints drifting inside
          ang = (i * 2.399) + (f * 0.02)
          d = 0.25 + (Util.hash01(i, f / 6, 9) * 0.7)
          Pix.rect(back, cx + (Math.cos(ang) * rx * d), cy + (Math.sin(ang) * ry * d), 2, 2, @pal.core)
        end
      end
    end

    class Scene
      def burst_at(kind, pt, count = 12, color = nil, o = {})
        opts = { :color => color }.merge(o)
        count.times { @particles.spawn(kind, pt[0], pt[1], opts) }
      end

      def op_emit(a, dur)
        e = Emitter.new(self, a[:kind], a, a[:duration])
        @emitters[a[:id] || a[:kind]] = e
        return e
      end

      def op_stop_emit(a, _dur)
        if a[:id]
          e = @emitters.delete(a[:id])
          e.stop if e
        else
          @emitters.each_value(&:stop)
          @emitters.clear
        end
        nil
      end

      def op_burst(a, _dur)
        burst_at(a[:kind], point(a[:at] || [@w / 2, @h / 2]), a[:count] || 14, a[:color],
                 { :speed => a[:speed], :layer => a[:layer], :angle => a[:angle], :spread => a[:spread] })
        nil
      end

      # dome at:, radius:, duration:  - grow (or resize) the dome
      # dome hole_at: :actor, hole: px   - open a clear circle around someone
      # dome off: true                   - remove it
      def op_dome(a, dur)
        dome = @effects.find { |e| e.is_a?(Dome) }
        if a[:off]
          @effects.delete(dome) if dome
          return nil
        end
        dome ||= run_effect(Dome.new(self, a), @time)
        dome.set_hole(anchor(a[:hole_at])) if a[:hole_at]
        r0 = dome.radius
        h0 = dome.hole
        r1 = (a[:radius] || r0).to_f
        h1 = (a[:hole] || h0).to_f
        tween(dur, a[:ease] || :out) do |k, _|
          dome.radius = Util.lerp(r0, r1, k)
          dome.hole = Util.lerp(h0, h1, k)
        end
      end

      # overlay :burning / :freezing, level: 0..1 - creeping screen overlays.
      def op_overlay(a, dur)
        kind = a[:kind]
        raise ArgumentError, "overlay is :burning or :freezing" if !@overlay.has_key?(kind)
        from = @overlay[kind]
        to = Util.clamp((a[:level] || 0).to_f, 0.0, 1.0)
        tween(dur, :linear) { |k, _| @overlay[kind] = Util.lerp(from, to, k) }
      end

      # Flames licking up from the bottom edge: 4px columns, 4 colours.
      def draw_burning(b)
        level = @overlay[:burning]
        pal = Util.palette(:fire)
        f = @fx_frame / 2
        cols = @vw / 4
        base = @vh - (@bar / PX).round
        cols.times do |i|
          n = (Util.hash01(i, f, 3) * 0.5) + (Util.hash01(i / 3, f / 2, 4) * 0.5)
          h = (level * @vh * 0.42 * (0.45 + (0.55 * n))).round
          next if h <= 0
          x = i * 4
          Pix.rect(b, x, base - h, 4, h, pal.edge)
          Pix.rect(b, x + ((i + f) % 2), base - h - 2, 2, 2, pal.edge)
          Pix.rect(b, x, base - (h * 0.7).round, 4, (h * 0.7).round, pal.outer)
          Pix.rect(b, x, base - (h * 0.42).round, 4, (h * 0.42).round, pal.inner)
          Pix.rect(b, x + 1, base - (h * 0.16).round, 2, (h * 0.16).round, pal.core)
        end
      end

      # Frost creeping in from the screen edges. Drawn incrementally: only
      # newly frozen cells are painted as the level rises.
      def update_frost
        level = (@overlay[:freezing] * 24).round
        return if level == (@frost_level || 0)
        if !@frost_sprite
          @frost_bmp = Bitmap.new(@vw, @vh)
          @frost_sprite = fx_sprite(@frost_bmp, Z_FROST)
          @frost_cells = {}
        end
        if level < (@frost_level || 0)
          @frost_bmp.clear
          @frost_cells.clear
        end
        @frost_level = level
        return if level <= 0
        lv = level / 24.0
        cw = @vw / 2
        ch = @vh / 2
        white = Color.new(255, 255, 255)
        pale = Color.new(200, 236, 255)
        blue = Color.new(120, 184, 240)
        depth = lv * 0.42 * [cw, ch].min          # how far the frost reaches in, in cells
        bar = (@bar / (PX * 2)).floor
        ch.times do |cy|
          dyy = [cy, ch - 1 - cy].min - bar
          next if dyy < 0
          cw.times do |cx|
            d = [cx, cw - 1 - cx, dyy].min
            next if d > depth * 1.7
            key = (cy * cw) + cx
            next if @frost_cells[key]
            lump = Util.hash01(cx / 4, cy / 4, 6)   # lumpy border
            n = Util.hash01(cx, cy, 5)
            vein = ((cx + cy) % 9) == 0 || ((cx - cy) % 11) == 0
            solid = d < depth * (0.3 + (0.6 * lump)) && n > 0.12
            crystal = vein && d < depth * (1.0 + (0.7 * lump))
            next if !solid && !crystal
            @frost_cells[key] = true
            c = (crystal && !solid) ? pale : ((d < depth * 0.25 || n > 0.85) ? white : ((n > 0.45) ? pale : blue))
            @frost_bmp.fill_rect(cx * 2, cy * 2, 2, 2, c)
          end
        end
      end
    end
  end
end
