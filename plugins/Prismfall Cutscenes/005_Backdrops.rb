#===============================================================================
# Prismfall Cutscenes - 005 Backgrounds
#-------------------------------------------------------------------------------
# background :sky / :sea / :ice / :battlefield / :mountains / :arena / :fleet /
# :fortress / :gradient / :color are drawn by code (no art needed);
# background image: "Graphics/..." uses a picture. Each call adds one or more
# layers, back to front. parallax: 0 = fixed to the screen, 1 = moves fully
# with the camera. Positions are in screen pixels.
#===============================================================================
module Prismfall
  module Cutscene
    module Backdrop
      SKIES = {
        :day     => [[88, 152, 232], [120, 176, 240], [160, 200, 248], [200, 224, 248]],
        :dawn    => [[56, 64, 120], [120, 96, 152], [208, 136, 144], [248, 192, 144], [255, 224, 176]],
        :dusk    => [[40, 32, 88], [96, 48, 112], [176, 72, 96], [232, 120, 72], [248, 176, 96]],
        :night   => [[8, 8, 32], [16, 16, 56], [24, 32, 80], [40, 48, 104]],
        :burning => [[40, 8, 16], [96, 16, 16], [168, 40, 16], [224, 88, 24], [248, 152, 48]],
        :storm   => [[32, 40, 56], [48, 56, 80], [72, 80, 104], [96, 104, 128]],
        :snow    => [[136, 152, 184], [168, 184, 208], [200, 212, 228], [224, 232, 240]]
      }
      CLOUDS = {   # [body, highlight]
        :day => [[232, 240, 255], [255, 255, 255]], :dawn => [[232, 168, 168], [255, 216, 192]],
        :dusk => [[120, 64, 104], [216, 112, 96]], :night => [[32, 40, 80], [56, 64, 112]],
        :burning => [[56, 16, 24], [136, 40, 24]], :storm => [[40, 48, 64], [80, 88, 112]],
        :snow => [[208, 216, 232], [240, 244, 250]]
      }
      SEAS = {
        :day     => [[96, 168, 232], [64, 136, 216], [40, 104, 192], [24, 72, 160]],
        :night   => [[24, 40, 96], [16, 32, 80], [8, 24, 64], [8, 16, 48]],
        :burning => [[200, 96, 56], [136, 56, 64], [80, 40, 72], [40, 24, 56]],
        :storm   => [[72, 88, 112], [56, 72, 96], [40, 56, 80], [24, 40, 64]],
        :black   => [[40, 48, 80], [24, 32, 56], [16, 24, 40], [8, 12, 28]]
      }
      ICES = {
        :day   => [[232, 244, 255], [208, 228, 248], [176, 208, 240], [144, 184, 224]],
        :dawn  => [[255, 236, 224], [232, 216, 232], [196, 200, 236], [160, 176, 224]],
        :ember => [[255, 216, 192], [240, 192, 192], [208, 168, 192], [160, 136, 184]],
        :night => [[136, 160, 208], [104, 128, 184], [80, 104, 160], [56, 80, 136]],
        :glass => [[255, 255, 255], [240, 232, 248], [216, 232, 240], [200, 208, 232]]
      }
      GROUNDS = {
        :grass    => [[120, 176, 88], [96, 152, 72], [72, 128, 64], [56, 104, 56]],
        :scorched => [[104, 80, 72], [80, 56, 56], [56, 40, 48], [40, 24, 32]],
        :snow     => [[240, 244, 250], [216, 228, 244], [192, 208, 232], [168, 184, 216]],
        :sand     => [[240, 216, 160], [224, 192, 136], [200, 168, 112], [176, 144, 96]],
        :stone    => [[176, 176, 192], [152, 152, 172], [128, 128, 152], [104, 104, 132]]
      }

      module_function

      def v(n); return (n.to_f / PX).round; end

      def spec(bitmap, o, defaults = {})
        return { :bitmap => bitmap, :px => PX,
                 :parallax => o[:parallax] || defaults[:parallax] || 0.0,
                 :scroll => o[:scroll] || defaults[:scroll] || 0,
                 :x => o[:x] || defaults[:x] || 0, :y => defaults[:y] || 0,
                 :tile => (o.has_key?(:tile)) ? o[:tile] : defaults.fetch(:tile, true),
                 :opacity => o[:opacity] || 255, :front => o[:front] || false }
      end

      # Returns an array of layer specs.
      def build(kind, o, scene)
        vw = scene.vw
        vh = scene.vh
        seed = o[:seed] || kind.to_s.sum
        case kind
        when :color
          b = Bitmap.new(vw, vh)
          b.fill_rect(0, 0, vw, vh, Util.color(o[:color] || [0, 0, 0]))
          return [spec(b, o)]
        when :image
          b = Gfx.load_bitmap(o[:image])
          if !b
            Util.log("background image #{o[:image].inspect} not found; using a flat colour")
            return build(:color, { :color => [24, 24, 40] }, scene)
          end
          s = spec(b, o, { :tile => false, :y => o[:y] || 0 })
          s[:px] = o[:px] || 1
          return [s]
        when :gradient
          y = v(o[:y] || 0)
          h = (o[:height]) ? v(o[:height]) : vh - y
          b = Bitmap.new(vw, h + 8)
          Pix.gradient(b, 0, 0, vw, h + 8, o[:colors] || SKIES[:day], o[:dither] != false)
          return [spec(b, o, { :y => y * PX })]
        when :sky       then return sky(o, vw, vh, seed)
        when :sea       then return sea(o, vw, vh, seed)
        when :ice       then return ice(o, vw, vh, seed)
        when :battlefield then return battlefield(o, vw, vh, seed)
        when :mountains then return mountains(o, vw, vh, seed)
        when :arena     then return arena(o, vw, vh, seed)
        when :fleet     then return fleet(o, vw, vh, seed)
        when :fortress  then return fortress(o, vw, vh, seed)
        end
        return send(kind, o, vw, vh, seed) if respond_to?(kind)      # kinds added by other files
        raise ArgumentError, "Unknown background kind #{kind.inspect}"
      end

      def sky(o, vw, vh, seed)
        pal = o[:palette] || :day
        cols = o[:colors] || SKIES[pal] || SKIES[:day]
        b = Bitmap.new(vw, vh)
        Pix.gradient(b, 0, 0, vw, v(o[:height] || (vh * PX * 0.62)), cols)
        b.fill_rect(0, v(o[:height] || (vh * PX * 0.62)), vw, vh, Util.color(cols[-1]))
        if pal == :night || o[:stars]
          90.times do |i|
            c = (Util.hash01(i, seed, 3) > 0.8) ? Color.new(255, 255, 255) : Color.new(168, 176, 216)
            Pix.rect(b, Util.hash01(i, seed, 1) * vw, Util.hash01(i, seed, 2) * vh * 0.55, 1, 1, c)
          end
        end
        if o[:sun]
          sx, sy = o[:sun]
          sc = SKIES[pal][-1]
          Pix.disc(b, v(sx), v(sy), 12, Util.color(Util.mix(sc, [255, 255, 255], 0.4)))
          Pix.disc(b, v(sx), v(sy), 9, Util.color(Util.mix(sc, [255, 255, 255], 0.8)))
        end
        layers = [spec(b, o, { :parallax => 0.0, :tile => true })]
        return layers if o[:clouds] == false
        body, light = (CLOUDS[pal] || CLOUDS[:day]).map { |c| Util.color(c) }
        cb = Bitmap.new(vw, v(vh * PX * 0.5))
        n = o[:clouds].is_a?(Integer) ? o[:clouds] : 6
        n.times do |i|
          cx = (Util.hash01(i, seed, 11) * vw).round
          cy = 10 + (Util.hash01(i, seed, 12) * (cb.height - 24)).round
          w = 14 + (Util.hash01(i, seed, 13) * 22).round
          [-vw, 0, vw].each do |wrap|   # seamless when tiled
            x = cx + wrap
            Pix.disc(cb, x, cy, w, light, 3)
            Pix.disc(cb, x - (w / 3), cy - 2, w / 2, light, 4)
            Pix.disc(cb, x + (w / 4), cy - 3, w / 3, light, 4)
            Pix.disc(cb, x, cy + 1, w, body, 3)
            Pix.disc(cb, x - (w / 3), cy, w / 2, body, 3)
            Pix.disc(cb, x + (w / 4), cy - 1, w / 3, body, 3)
          end
        end
        layers.push(spec(cb, {}, { :parallax => 0.08, :scroll => o[:cloud_scroll] || -5, :tile => true }))
        return layers
      end

      def ground_bitmap(vw, vh, horizon, cols)
        top = v(horizon)
        b = Bitmap.new(vw, vh - top + 16)
        # Bands get taller towards the viewer (cheap perspective).
        n = cols.length
        y = 0
        n.times do |i|
          h = ((b.height - y) * ((i == n - 1) ? 1.0 : (0.16 + (0.1 * i)))).round
          Pix.rect(b, 0, y, vw, h, Util.color(cols[i]))
          if i > 0
            Pix.dither_row(b, 0, y, vw, Util.color(cols[i - 1]), 0, 2)
            Pix.dither_row(b, 0, y + 1, vw, Util.color(cols[i - 1]), 1, 4)
          end
          y += h
        end
        return b, top
      end

      def sea(o, vw, vh, seed)
        cols = o[:colors] || SEAS[o[:palette] || :day] || SEAS[:day]
        b, top = ground_bitmap(vw, vh, o[:horizon] || 200, cols)
        Pix.rect(b, 0, 0, vw, 1, Util.color(Util.mix(cols[0], [255, 255, 255], 0.5)))
        layers = [spec(b, o, { :parallax => 1.0, :y => top * PX })]
        light = Util.color(Util.mix(cols[0], [255, 255, 255], 0.6))
        2.times do |k|
          g = Bitmap.new(vw, b.height)
          70.times do |i|
            fy = Util.hash01(i, seed + k, 1)**1.6
            y = 2 + (fy * (g.height - 4)).round
            w = 2 + (fy * 6).round + (Util.hash01(i, seed + k, 3) * 3).round
            Pix.rect(g, Util.hash01(i, seed + k, 2) * vw, y, w, 1, light)
          end
          layers.push(spec(g, {}, { :parallax => 1.0, :y => top * PX, :scroll => (k == 0) ? 7 : -4 }))
        end
        return layers
      end

      # Frozen sea. plates: true cuts black-water channels between ice plates.
      def ice(o, vw, vh, seed)
        cols = o[:colors] || ICES[o[:palette] || :day] || ICES[:day]
        b, top = ground_bitmap(vw, vh, o[:horizon] || 200, cols)
        white = Color.new(255, 255, 255)
        crack = Util.color(Util.mix(cols[-1], [16, 32, 80], 0.6))
        water = Util.color(o[:water] || [12, 16, 36])
        rim   = Util.color(Util.mix(cols[0], [255, 255, 255], 0.6))
        n = o[:cracks] || 9
        n.times do |i|
          y = 6 + ((Util.hash01(i, seed, 1)**1.3) * (b.height - 24)).round
          x = -8
          th = (o[:plates]) ? 1 + (y * 4 / b.height) : 1
          while x < vw + 8
            len = 8 + (Util.hash01(i, x, seed) * 22).round
            ny = y + ((Util.hash01(i, x, seed + 5) * 7) - 3).round
            if o[:plates]
              Pix.line(b, x, y - 1, x + len, ny - 1, rim, 1)
              Pix.line(b, x, y, x + len, ny, water, th)
            else
              Pix.line(b, x, y, x + len, ny, crack, 1)
            end
            if Util.hash01(i, x, seed + 9) > 0.7   # side crack
              Pix.line(b, x + len, ny, x + len + 5, ny + 6 + th, (o[:plates]) ? water : crack, (o[:plates]) ? 2 : 1)
            end
            x += len
            y = ny
          end
        end
        60.times do |i|
          Pix.rect(b, Util.hash01(i, seed, 21) * vw, 2 + (Util.hash01(i, seed, 22) * (b.height - 4)), 1 + (i % 2), 1, white)
        end
        return [spec(b, o, { :parallax => 1.0, :y => top * PX })]
      end

      def battlefield(o, vw, vh, seed)
        cols = o[:colors] || GROUNDS[o[:palette] || :grass] || GROUNDS[:grass]
        b, top = ground_bitmap(vw, vh, o[:horizon] || 200, cols)
        dark = Util.color(Util.mix(cols[-1], [0, 0, 0], 0.4))
        light = Util.color(Util.mix(cols[0], [255, 255, 255], 0.3))
        120.times do |i|
          fy = Util.hash01(i, seed, 1)
          Pix.rect(b, Util.hash01(i, seed, 2) * vw, 2 + (fy * (b.height - 4)), 1 + (fy * 2).round, 1, (i.odd?) ? dark : light)
        end
        (o[:craters] || 5).times do |i|
          fy = 0.2 + (Util.hash01(i, seed, 31) * 0.7)
          r = 4 + (fy * 10).round
          cx = Util.hash01(i, seed, 32) * vw
          cy = fy * (b.height - 16)
          Pix.disc(b, cx, cy, r, dark, [r / 3, 1].max)
          Pix.disc(b, cx, cy + 1, r - 2, Util.color(cols[-1]), [(r / 3) - 1, 1].max)
        end
        return [spec(b, o, { :parallax => 1.0, :y => top * PX })]
      end

      def mountains(o, vw, vh, seed)
        base = v(o[:y] || 200)
        height = v(o[:height] || 90)
        col = o[:color] || [56, 64, 96]
        b = Bitmap.new(vw, base + 8)
        c = Util.color(col)
        snow = (o[:snow]) ? Util.color(Util.mix(col, [255, 255, 255], 0.75)) : nil
        shade = Util.color(Util.mix(col, [0, 0, 0], 0.25))
        tau = Math::PI * 2
        p1 = Util.hash01(seed, 1) * tau
        p2 = Util.hash01(seed, 2) * tau
        p3 = Util.hash01(seed, 3) * tau
        (vw / 2).times do |i|
          a = i * 2.0 / vw * tau
          k = 0.5 + (0.28 * Math.sin((a * 2) + p1)) + (0.14 * Math.sin((a * 5) + p2)) + (0.08 * Math.sin((a * 11) + p3))
          h = (height * Util.clamp(k, 0.08, 1.0)).round
          h -= h % 2
          Pix.rect(b, i * 2, base - h, 2, h + 8, c)
          Pix.rect(b, i * 2, base - h, 2, [h / 5, 2].max, snow) if snow && h > height * 0.55
          Pix.rect(b, i * 2, base - h + (h / 2), 2, 2, shade) if (i % 5) == 0
        end
        return [spec(b, o, { :parallax => 0.3 })]
      end

      # Temple-arena: stands with a crowd, a wall, and a marked floor.
      # colors: [left, right] tints the two halves of the crowd; tint: colours the floor.
      def arena(o, vw, vh, seed)
        b = Bitmap.new(vw, vh + 16)
        wall_y = v(o[:horizon] || 190)
        Pix.gradient(b, 0, 0, vw, wall_y - 10, [[32, 28, 48], [48, 40, 64], [64, 52, 80]], false)
        sides = o[:colors] || [[96, 168, 104], [200, 160, 88]]
        common = [[232, 216, 200], [176, 136, 112], [88, 72, 96], [208, 208, 224]]
        row = 0
        y = 6
        while y < wall_y - 12
          Pix.rect(b, 0, y + 4, vw, 1, Color.new(24, 20, 36))
          (vw / 4).times do |i|
            next if Util.hash01(i, row, seed) < 0.12
            x = (i * 4) + ((row.odd?) ? 2 : 0)
            side = sides[(x < vw / 2) ? 0 : 1]
            pick = Util.hash01(i, row, seed + 1)
            col = (pick < 0.45) ? side : common[(pick * 97).to_i % 4]
            Pix.rect(b, x, y + 1, 2, 3, Util.color(Util.mix(col, [0, 0, 0], 0.25)))
            Pix.rect(b, x, y, 2, 2, Util.color(common[(pick * 31).to_i % 2]))
          end
          y += 7
          row += 1
        end
        Pix.rect(b, 0, wall_y - 12, vw, 12, Color.new(88, 80, 112))
        Pix.rect(b, 0, wall_y - 12, vw, 2, Color.new(144, 136, 168))
        Pix.rect(b, 0, wall_y - 2, vw, 2, Color.new(40, 36, 60))
        (vw / 32).times { |i| Pix.rect(b, (i * 32) + 14, wall_y - 10, 4, 8, Util.color(sides[(i * 32 < vw / 2) ? 0 : 1])) }
        floor = GROUNDS[o[:palette] || :stone] || GROUNDS[:stone]
        floor = floor.map { |c| Util.mix(c, Util.rgb(o[:tint]), 0.35) } if o[:tint]
        fh = b.height - wall_y
        4.times do |i|
          Pix.rect(b, 0, wall_y + (fh * i / 4), vw, (fh / 4) + 1, Util.color(floor[i]))
        end
        line = Util.color(Util.mix(floor[0], [255, 255, 255], 0.6))
        cy = wall_y + (fh * 0.52).round
        Pix.ring(b, vw / 2, cy, 34, line, 1, 12)
        Pix.rect(b, vw / 2, wall_y + 6, 1, fh - 28, line)
        Pix.ring(b, vw / 2, cy, 8, line, 1, 3)
        Pix.rect(b, 12, wall_y + 6, vw - 24, 1, line)
        return [spec(b, o, { :parallax => 1.0 })]
      end

      # A row of sled-ship silhouettes. x/width place the row (screen px).
      def fleet(o, vw, vh, seed)
        w = v(o[:width] || 256)
        col = o[:color] || [40, 56, 96]
        b = Bitmap.new(w, 44)
        c = Util.color(col)
        sail = Util.color(Util.mix(col, [255, 255, 255], 0.35))
        n = o[:count] || 5
        n.times do |i|
          x = ((i + 0.5) * w / n).round + ((Util.hash01(i, seed) * 8) - 4).round
          s = 0.7 + (Util.hash01(i, seed, 4) * 0.5)
          hull = (22 * s).round
          mast = (26 * s).round
          Pix.rect(b, x, 40 - mast, 1, mast, c)
          (mast / 2).times { |r| Pix.rect(b, x + 1, 40 - mast + 2 + r, [(hull / 2) - r, 1].max, 1, sail) }
          4.times { |r| Pix.rect(b, x - (hull / 2) + r, 38 + r, hull - (r * 2), 1, c) }
          Pix.rect(b, x - (hull / 2) - 2, 37, 3, 1, c)
        end
        return [spec(b, o, { :parallax => 0.8, :tile => false, :y => (o[:y] || 200) - (42 * PX), :x => o[:x] || 0 })]
      end

      # A crenellated wall with towers. y = ground line (screen px).
      def fortress(o, vw, vh, seed)
        w = v(o[:width] || 220)
        h = v(o[:height] || 120)
        col = o[:color] || [48, 40, 64]
        b = Bitmap.new(w, h)
        c = Util.color(col)
        light = Util.color(Util.mix(col, [255, 255, 255], 0.2))
        glow = (o[:glow]) ? Util.color(o[:glow]) : nil
        wall = (h * 0.55).round
        Pix.rect(b, 0, h - wall, w, wall, c)
        (w / 6).times { |i| Pix.rect(b, i * 6, h - wall - 3, 3, 3, c) }
        Pix.rect(b, 0, h - wall, w, 1, light)
        towers = o[:towers] || 3
        towers.times do |i|
          tx = (((i + 0.5) * w / towers) - 9).round
          th = (h * (0.78 + (Util.hash01(i, seed) * 0.22))).round
          Pix.rect(b, tx, h - th, 18, th, c)
          Pix.rect(b, tx - 2, h - th, 22, 4, c)
          4.times { |k| Pix.rect(b, tx - 2 + (k * 6), h - th - 3, 3, 3, c) }
          Pix.rect(b, tx, h - th + 4, 1, th - 4, light)
          Pix.rect(b, tx + 7, h - th + 12, 3, 5, glow) if glow
        end
        (w / 14).times { |i| Pix.rect(b, (i * 14) + 5, h - wall + 8, 2, 4, glow) } if glow
        return [spec(b, o, { :parallax => 0.7, :tile => false, :y => (o[:y] || 200) - (h * PX), :x => o[:x] || 0 })]
      end
    end
  end
end
