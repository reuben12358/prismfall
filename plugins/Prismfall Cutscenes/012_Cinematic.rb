#===============================================================================
# Prismfall Cutscenes - 012 Cinematic kit
#-------------------------------------------------------------------------------
# Pixel-art dithering, deep scenery layers and direction tools:
#   background :floes / :aurora / :smoke_bank / :host   (front: true = in front of actors)
#   actor ..., submerge: n            sprite sunk n source pixels below its waterline
#   rim :id, color:, side: :left/:right   one-pixel rim light on that side (rim :id, off: true)
#   impact_frames count: 2            white/black silhouette frames
#   slowmo 0.25, duration: 0.5        slow the scene clock (duration in scene seconds)
#   fracture at:, radius:, duration:  cracks spreading through the ground under a point
#   glow side: :left/:right, color:, level: 0..1   dithered light spilling in from a screen edge
#===============================================================================
module Prismfall
  module Cutscene
    # Ordered-dither fills by blitting cached pattern tiles (cheap: one blt per
    # block). density: 2 = 50 %, 4 = 25 %, 8 = 12.5 %.
    module Dither
      TW = 256
      TH = 64
      @strips = {}

      module_function

      def cache_size; return @strips.count { |_, b| !b.disposed? }; end

      def strip(rgb, density)
        key = [rgb[0], rgb[1], rgb[2], density]
        s = @strips[key]
        return s if s && !s.disposed?
        col = Color.new(rgb[0], rgb[1], rgb[2])
        tile = Bitmap.new(8, 8)
        8.times do |y|
          8.times do |x|
            hit = case density
                  when 2 then (x + y).even?
                  when 4 then ((x + (2 * (y % 2))) % 4) == 0                       # 25 %, staggered
                  else        y.even? && ((x + (2 * ((y / 2) % 2))) % 4) == 0     # 12.5 %
                  end
            tile.fill_rect(x, y, 1, 1, col) if hit
          end
        end
        row = Bitmap.new(TW + 8, 8)
        ((TW + 8) / 8).times { |i| row.blt(i * 8, 0, tile, Rect.new(0, 0, 8, 8)) }
        out = Bitmap.new(TW + 8, TH + 8)
        ((TH + 8) / 8).times { |i| out.blt(0, i * 8, row, Rect.new(0, 0, TW + 8, 8)) }
        tile.dispose
        row.dispose
        @strips[key] = out
        return out
      end

      # Dithered rectangle, pattern locked to the bitmap's pixel grid.
      def fill(b, x, y, w, h, rgb, density = 2)
        x = x.round; y = y.round; w = w.round; h = h.round
        if x < 0 then w += x; x = 0 end
        if y < 0 then h += y; y = 0 end
        w = b.width - x if x + w > b.width
        h = b.height - y if y + h > b.height
        return if w <= 0 || h <= 0
        src = strip(rgb, density)
        yy = 0
        while yy < h
          hh = [h - yy, TH].min
          xx = 0
          while xx < w
            ww = [w - xx, TW].min
            b.blt(x + xx, y + yy, src, Rect.new((x + xx) % 8, (y + yy) % 8, ww, hh))
            xx += ww
          end
          yy += hh
        end
      end

      # Dithered ellipse (rows of equal width are merged into one blt).
      def disc(b, cx, cy, rx, ry, rgb, density = 2)
        rx = rx.round
        ry = ry.round
        return if rx <= 0 || ry <= 0
        run_w = nil
        run_y = 0
        (-ry..ry + 1).each do |dy|
          w = (dy > ry) ? nil : (rx * Math.sqrt(1.0 - ((dy.to_f / ry)**2))).round
          w -= w % 2 if w
          next if w == run_w
          fill(b, cx - run_w, cy + run_y, (run_w * 2) + 1, dy - run_y, rgb, density) if run_w
          run_w = w
          run_y = dy
        end
      end

      # A glow that fades outwards in three dither steps.
      def glow(b, cx, cy, rx, ry, rgb)
        disc(b, cx, cy, rx, ry, rgb, 8)
        disc(b, cx, cy, rx * 0.7, ry * 0.7, rgb, 4)
        disc(b, cx, cy, rx * 0.42, ry * 0.42, rgb, 2)
      end
    end

    def self.cached_bitmaps
      return Gfx.placeholder_cache_size + Dither.cache_size
    end

    #---------------------------------------------------------------------------
    # Scenery
    #---------------------------------------------------------------------------
    module Backdrop
      module_function

      # Pack ice in perspective: rows of irregular floes with a lit top face, a
      # shaded side face and black water between; bigger towards the viewer.
      #   pools: [[x, y, rx, ry], ...] open water (screen px), palette: ICES key
      def floes(o, vw, vh, seed)
        cols = o[:colors] || ICES[o[:palette] || :dawn] || ICES[:dawn]
        top = v(o[:horizon] || 200)
        x0 = o[:x] || 0
        vw = v(o[:width]) if o[:width]          # a wide, untiled sheet (needed with pools)
        b = Bitmap.new(vw, vh - top + 16)
        water = o[:water] || [10, 14, 34]
        deep = Util.mix(water, [40, 56, 104], 0.5)
        Pix.gradient(b, 0, 0, vw, b.height, [deep, Util.mix(water, deep, 0.5), water, water], true)
        Pix.rect(b, 0, 0, vw, 1, Util.color(Util.mix(cols[0], [255, 255, 255], 0.4)))
        pools = (o[:pools] || []).map { |p| [v(p[0] - x0), v(p[1]) - top, v(p[2]), v(p[3])] }
        y = 1
        row = 0
        while y < b.height - 2
          h = 3 + (row * row * 0.5).round + row            # rows get deeper towards the viewer
          side = [1 + (row / 2), 5].min                   # thickness of the side face
          band = cols[[row / 2, cols.length - 1].min]
          shade = Util.mix(cols[-1], [24, 40, 96], 0.45 + (row * 0.03))
          x = -((Util.hash01(row, seed, 1) * 30).round)
          i = 0
          while x < vw
            small = Util.hash01(row, i, seed + 6) < 0.22
            w = ((h * (1.5 + (Util.hash01(row, i, seed) * 4.2))) + 4).round
            w = (w * 0.4).round + 3 if small
            gap = 2 + ((row + 1) / 2) + ((Util.hash01(row, i, seed + 2) * (2 + row)).round)
            fh = h - side - ((Util.hash01(row, i, seed + 3) * (1 + (h / 4))).round)
            fh = (fh * 0.6).round if small
            fy = y + ((Util.hash01(row, i, seed + 4) * (1 + (h / 3))).round)
            cx = x + (w / 2)
            in_pool = pools.any? { |p| (((cx - p[0]).to_f / (p[2] + (w / 2)))**2) + (((fy + (fh / 2) - p[1]).to_f / (p[3] + 2))**2) < 1.0 }
            if fh >= 1 && !in_pool
              tint = (Util.hash01(row, i, seed + 9) - 0.5) * 0.14
              face = Util.mix(band, (tint > 0) ? [255, 255, 255] : cols[-1], tint.abs * 2)
              lit = Util.mix(face, [255, 255, 255], 0.5)
              sl = (Util.hash01(row, i, seed + 10) - 0.5) * 1.1      # slant of the left / right edge
              sr = (Util.hash01(row, i, seed + 11) - 0.5) * 1.1
              corner = [fh / 3, 3].min
              run = nil
              ry = 0
              l = r = 0
              (0..fh).each do |j|                                  # irregular outline, row by row
                key = nil
                if j < fh
                  round = [corner - j, corner - (fh - 1 - j), 0].max
                  l = x + round + (sl * j).round + ((Util.hash01(row, i, j + 40) > 0.8) ? 1 : 0)
                  r = x + w - round + (sr * j).round - ((Util.hash01(row, i, j + 80) > 0.8) ? 1 : 0)
                  key = [l, r]
                end
                next if key == run
                Pix.rect(b, run[0], fy + ry, run[1] - run[0], j - ry, Util.color(face)) if run
                run = key
                ry = j
              end
              Pix.rect(b, l + 1, fy + fh, r - l - 2, side, Util.color(shade))                          # side face
              Pix.rect(b, l + 2, fy + fh + side, r - l - 4, 1, Util.color(Util.mix(shade, water, 0.5))) if side > 1
              Pix.rect(b, x + corner + 1, fy, w - (corner * 2) - 2, 1, Util.color(lit))                 # lit far edge
              if fh > 4                                                                               # drifted snow and a hairline crack
                sw = [w / 4, 2].max
                Pix.rect(b, x + 3 + ((Util.hash01(row, i, 7) * [w - sw - 6, 1].max).round), fy + 2, sw, 1, Util.color(lit))
                Pix.rect(b, x + 5 + ((Util.hash01(row, i, 17) * [w - sw - 10, 1].max).round), fy + 3, [sw / 2, 1].max, 1, Util.color(lit))
                if Util.hash01(row, i, 8) > 0.6
                  kx = x + (w / 3) + ((Util.hash01(row, i, 18) * (w / 3)).round)
                  Pix.line(b, kx, fy + 1, kx + (fh / 2), fy + fh - 1, Util.color(Util.mix(face, shade, 0.55)))
                end
              end
            end
            x += w + gap
            i += 1
          end
          y += h + 1 + (row / 2)
          row += 1
        end
        pools.each do |p|                                  # foam rim round open water
          Pix.ring(b, p[0], p[1], p[2], Util.color(Util.mix(cols[0], [255, 255, 255], 0.5)), 1, p[3])
        end
        return [spec(b, o, { :parallax => 1.0, :y => top * PX, :x => x0, :tile => o[:width].nil? && o[:pools].nil? })]
      end

      # Desert dunes in perspective (the Glass Dunes, SPINE Rev 18): the grey
      # Northern Sea along the horizon, then rows of dune ridges with a lit
      # windward face and a shaded lee, bigger towards the viewer.
      #   flood: [[x, y, rx, ry], ...] Kyogre's flood-sea (screen px), grey water with foam
      #   palette: DUNES key (:dawn, :day, :glass)
      DUNES = {
        :dawn  => [[246, 236, 220], [226, 212, 190], [196, 178, 158], [158, 138, 124]],
        :day   => [[252, 246, 232], [236, 226, 206], [212, 198, 174], [176, 158, 136]],
        :glass => [[255, 255, 255], [226, 244, 250], [196, 228, 240], [150, 196, 220]]
      }

      def dunes(o, vw, vh, seed)
        cols = o[:colors] || DUNES[o[:palette] || :dawn] || DUNES[:dawn]
        top = v(o[:horizon] || 200)
        x0 = o[:x] || 0
        vw = v(o[:width]) if o[:width]
        b = Bitmap.new(vw, vh - top + 16)
        sea = o[:sea] || [92, 106, 124]
        sea_h = v(o[:sea_height] || 12)
        Pix.rect(b, 0, 0, vw, sea_h, Util.color(sea))
        Pix.rect(b, 0, 2, vw, 1, Util.color(Util.mix(sea, [255, 255, 255], 0.25)))
        Pix.rect(b, 0, sea_h, vw, 1, Util.color(Util.mix(sea, [255, 255, 255], 0.7)))       # surf
        Pix.rect(b, 0, sea_h + 1, vw, b.height - sea_h - 1, Util.color(cols[1]))            # sand
        Pix.rect(b, 0, sea_h + 1, vw, 1, Util.color(cols[3]))                               # wet sand
        lit = Util.color(cols[0])
        lee = Util.color(cols[2])
        foot = Util.color(cols[3])
        crest = Util.color(Util.mix(cols[0], [255, 255, 255], 0.5))
        y = sea_h + 3
        row = 0
        while y < b.height - 2
          h = 2 + row + (row * row * 0.25).round
          x = -((Util.hash01(row, seed, 1) * 40).round)
          i = 0
          while x < vw
            w = (h * (4.5 + (Util.hash01(row, i, seed) * 6))).round + 6
            if Util.hash01(row, i, seed + 7) > 0.25
              peak = x + (w * (0.3 + (Util.hash01(row, i, seed + 3) * 0.3))).round
              yy = y + ((Util.hash01(row, i, seed + 4) * (1 + (h / 3))).round)
              h.times do |j|
                l = peak - ((peak - x) * (j + 1) / h)
                r = peak + ((x + w - peak) * (j + 1) / h)
                Pix.rect(b, l, yy + j, peak - l, 1, lit)
                Pix.rect(b, peak, yy + j, r - peak, 1, lee)
              end
              Pix.rect(b, x, yy + h, w, 1, foot)
              Pix.rect(b, peak - 1, yy, 2, 1, crest)
            end
            x += w - (h / 2)
            i += 1
          end
          y += h + 1 + (row / 2)
          row += 1
        end
        (o[:flood] || []).each do |p|
          cx, cy, rx, ry = v(p[0] - x0), v(p[1]) - top, v(p[2]), v(p[3])
          Pix.disc(b, cx, cy, rx, Util.color(sea), ry)
          Pix.disc(b, cx, cy - (ry / 3), (rx * 0.7).round, Util.color(Util.mix(sea, [255, 255, 255], 0.12)), (ry * 0.5).round)
          Pix.ring(b, cx, cy, rx, Util.color(Util.mix(sea, [255, 255, 255], 0.75)), 1, ry)
          Pix.rect(b, cx - (rx / 4), 0, rx / 2, cy - ry + 2, Util.color(sea)) if o[:flood_channel]     # the channel from the sea
        end
        return [spec(b, o, { :parallax => 1.0, :y => top * PX, :x => x0, :tile => o[:width].nil? && o[:flood].nil? })]
      end

      # Northern lights: hanging curtains fading upwards in dither steps.
      def aurora(o, vw, vh, seed)
        w = v(o[:width] || 320)
        h = v(o[:height] || 150)
        b = Bitmap.new(w, h)
        cols = o[:colors] || [[112, 255, 184], [72, 216, 208], [96, 136, 232], [136, 96, 208]]
        tau = Math::PI * 2
        (w / 2).times do |i|
          x = i * 2
          fx = i * 2.0 / w
          edge = [fx / 0.12, (1 - fx) / 0.12, 1.0].min                 # fades at both ends
          next if edge <= 0
          base = (h * (0.62 + (0.16 * Math.sin((fx * tau * 1.5) + seed)) + (0.07 * Math.sin((fx * tau * 4.3) + (seed * 2))))).round
          len = (h * edge * (0.34 + (0.2 * Math.sin((fx * tau * 2.7) + 1 + seed)) + (0.14 * Util.hash01(i / 3, seed, 1)))).round
          next if len < 4
          Pix.rect(b, x, base - 2, 2, 2, Util.color(cols[0]))
          Dither.fill(b, x, base - (len * 0.25).round, 2, (len * 0.25).round - 2, cols[0], 2)
          Dither.fill(b, x, base - (len * 0.55).round, 2, (len * 0.30).round, cols[1], 2)
          Dither.fill(b, x, base - (len * 0.8).round, 2, (len * 0.25).round, cols[2], 4)
          Dither.fill(b, x, base - len, 2, (len * 0.2).round, cols[3], 8)
        end
        return [spec(b, o, { :parallax => 0.06, :tile => false, :x => o[:x] || 0, :y => o[:y] || 10 })]
      end

      # A wall of smoke lit from below by fires.
      def smoke_bank(o, vw, vh, seed)
        w = v(o[:width] || 320)
        h = v(o[:height] || 170)
        b = Bitmap.new(w, h)
        dark = o[:color] || [34, 22, 44]
        mid = Util.mix(dark, [150, 64, 56], 0.45)
        soft = Util.mix(dark, [96, 64, 96], 0.5)
        glow = o[:glow] || [248, 136, 48]
        n = o[:plumes] || 5
        band_y = (h * 0.3).round
        n.times do |i|                                   # thin columns climbing from the camp fires
          cx = (((i + 0.5) * w / n) + ((Util.hash01(i, seed, 1) - 0.5) * (w / n) * 0.5)).round
          Dither.glow(b, cx, h - 3, 26, 10, glow)
          steps = ((h - band_y) / 5.0).ceil
          steps.times do |k|
            f = k / (steps - 1.0)
            r = (2 + (f * 7)).round
            x = cx + (Math.sin((k * 0.6) + (i * 2)) * (2 + (f * 5))).round + ((o[:lean] || -30) * f * f).round
            y = h - 6 - ((h - band_y - 6) * f).round
            Dither.disc(b, x, y, r + 2, r + 1, dark, 2) if k.odd?
            Pix.disc(b, x, y, r, Util.color((f < 0.25) ? mid : dark), [(r * 0.85).round, 1].max)
            Pix.disc(b, x + (r / 3), y + (r / 3), [r / 2, 1].max, Util.color((f < 0.4) ? Util.mix(mid, glow, 0.35) : soft), [r / 3, 1].max) if k % 3 == 0
          end
        end
        11.times do |i|                                  # the pall they feed: long flat rolls, ragged underneath
          x = ((i + 0.3) * w / 10.0).round + ((Util.hash01(i, seed, 5) - 0.5) * 20).round
          y = band_y + ((Util.hash01(i, seed, 6) - 0.5) * 22).round
          rx = 28 + (Util.hash01(i, seed, 7) * 22).round
          ry = 6 + (Util.hash01(i, seed, 8) * 5).round
          Dither.disc(b, x, y + 3, rx + 6, ry + 3, dark, 2)
          Pix.disc(b, x, y + 1, rx, Util.color(soft), ry)
          Pix.disc(b, x - 2, y - 1, rx - 2, Util.color(dark), [ry - 1, 1].max)
          Dither.disc(b, x, y - ry, (rx * 0.7).round, 3, dark, 4)
        end
        return [spec(b, o, { :parallax => 0.2, :tile => false, :x => o[:x] || 0, :y => (o[:y] || 210) - (h * PX), :scroll => 0 })]
      end

      # An army as dense ranks of tiny figures with spears, banners and either
      # campfires or frost spikes. y = ground line of the front rank (screen px).
      def host(o, vw, vh, seed)
        w = v(o[:width] || 300)
        rows = o[:rows] || 5
        h = 26 + (rows * 5)
        b = Bitmap.new(w, h)
        col = o[:color] || [200, 72, 48]
        banner = o[:banner] || col
        skin = [232, 192, 152]
        right = (o[:facing] || :right) == :right
        rows.times do |r|
          depth = (rows - 1 - r) / [rows - 1, 1].max.to_f                 # 1 = back rank
          tone = Util.mix(col, o[:haze] || [72, 64, 104], depth * 0.55)
          dark = Util.mix([24, 20, 36], o[:haze] || [72, 64, 104], depth * 0.4)
          fy = h - 1 - ((rows - 1 - r) * 5)
          n = w / 5
          n.times do |i|
            next if Util.hash01(i, r, seed) < 0.08
            x = (i * 5) + ((r.odd?) ? 2 : 0) + ((Util.hash01(i, r, seed + 1) * 2).round)
            Pix.rect(b, x, fy - 3, 1, 3, Util.color(dark))                 # legs
            Pix.rect(b, x + 2, fy - 3, 1, 3, Util.color(dark))
            Pix.rect(b, x, fy - 7, 3, 4, Util.color(tone))                 # body
            Pix.rect(b, (right) ? x : x + 2, fy - 6, 1, 3, Util.color(Util.mix(tone, [0, 0, 0], 0.35)))
            Pix.rect(b, x, fy - 9, 3, 2, Util.color(Util.mix(skin, o[:haze] || [72, 64, 104], depth * 0.4)))
            Pix.rect(b, x, fy - 10, 3, 1, Util.color(dark))                # helm
            if Util.hash01(i, r, seed + 2) > 0.45                          # spear
              sx = (right) ? x + 3 : x - 1
              Pix.rect(b, sx, fy - 15, 1, 12, Util.color(dark))
              Pix.rect(b, sx, fy - 16, 1, 2, Util.color([216, 224, 240]))
            end
          end
        end
        (o[:banners] || (w / 44)).times do |i|                           # banners over the ranks
          x = 12 + (i * (w - 24) / [(o[:banners] || (w / 44)) - 1, 1].max) + ((Util.hash01(i, seed, 9) * 8) - 4).round
          fy = h - 1 - ((i % rows) * 5)
          Pix.rect(b, x, fy - 26, 1, 20, Util.color([24, 20, 36]))
          fx = (right) ? x + 1 : x - 8
          Pix.rect(b, fx, fy - 26, 8, 6, Util.color(banner))
          Pix.rect(b, fx, fy - 26, 8, 1, Util.color(Util.mix(banner, [255, 255, 255], 0.5)))
          Pix.rect(b, fx + ((right) ? 6 : 0), fy - 20, 2, 2, Util.color(banner))
          Pix.rect(b, fx + 3, fy - 24, 2, 2, Util.color(Util.mix(banner, [255, 255, 255], 0.7)))
        end
        (o[:fires] || 0).times do |i|                                    # campfires
          x = 10 + ((Util.hash01(i, seed, 11) * (w - 20)).round)
          fy = h - 1 - ((i % 2) * 3)
          Dither.disc(b, x, fy - 3, 9, 6, [248, 136, 48], 4)
          Pix.rect(b, x - 2, fy - 4, 5, 4, Util.color([240, 112, 24]))
          Pix.rect(b, x - 1, fy - 7, 3, 5, Util.color([255, 208, 64]))
          Pix.rect(b, x, fy - 9, 1, 4, Util.color([255, 250, 220]))
        end
        (o[:frost] || 0).times do |i|                                    # frost spikes
          x = 8 + ((Util.hash01(i, seed, 13) * (w - 16)).round)
          fy = h - 1
          len = 6 + ((Util.hash01(i, seed, 14) * 9).round)
          len.times do |k|
            Pix.rect(b, x - ((len - k) / 5), fy - k, [((len - k) / 2.5).ceil, 1].max, 1, Util.color((k.even?) ? [200, 236, 255] : [120, 184, 240]))
          end
          Pix.rect(b, x, fy - len, 1, 2, Color.new(255, 255, 255))
        end
        s = spec(b, o, { :parallax => 1.0, :tile => false, :x => o[:x] || 0, :y => (o[:y] || 330) - (h * PX) })
        return [s]
      end
    end

    #---------------------------------------------------------------------------
    # Effects
    #---------------------------------------------------------------------------
    # One or two frames of pure silhouette: white field with black figures, then
    # black field with white figures. The classic anime impact frame.
    class ImpactFrames < Effect
      def initialize(scene, count, each)
        @count = count
        @each = each
      end

      def update(scene, lt, dt)
        i = (lt / @each).floor
        if i >= @count
          scene.set_silhouette(nil)
          return true
        end
        scene.set_silhouette((i.even?) ? :white : :black) if !Cutscene.photosensitive?
        return false
      end

      def dispose; end
    end

    # Cracks racing outwards through the ground, drawn once onto a decal layer.
    class Fracture < Effect
      def initialize(scene, a, dur)
        @dur = dur
        cx, cy = scene.point(a[:at])
        radius = (a[:radius] || 160).to_f
        squash = a[:squash] || 0.34
        rng = scene.rng
        @segs = []
        (a[:arms] || 9).times do |i|
          ang = (i * Math::PI * 2 / (a[:arms] || 9)) + ((rng.rand - 0.5) * 0.5)
          grow = lambda do |x, y, ang2, len, from, depth|
            steps = (len / 14).ceil
            steps.times do |k|
              ang2 += (rng.rand - 0.5) * 0.7
              step = len / steps
              nx = x + (Math.cos(ang2) * step)
              ny = y + (Math.sin(ang2) * step * squash)
              d0 = from + (k * step)
              @segs.push([d0 / radius, x, y, nx, ny, (depth == 0 && k < steps / 2) ? 2 : 1])
              grow.call(nx, ny, ang2 + ((rng.rand < 0.5) ? 0.9 : -0.9), len * 0.4, d0 + step, depth + 1) if depth < 1 && rng.rand < 0.3
              x = nx
              y = ny
            end
          end
          grow.call(cx, cy, ang, radius * (0.6 + (rng.rand * 0.4)), 0.0, 0)
        end
        @segs.sort_by! { |s| s[0] }
        @drawn = 0
        @dark = Util.color(a[:color] || [16, 22, 60])
        @light = Util.color(a[:highlight] || [226, 238, 255])
      end

      def update(scene, lt, dt)
        k = (@dur <= 0) ? 1.0 : Util.clamp(lt / @dur, 0.0, 1.0)
        b = scene.decal
        while @drawn < @segs.length && @segs[@drawn][0] <= k
          s = @segs[@drawn]
          @drawn += 1
          x0, y0 = scene.decal_point(s[1], s[2])
          x1, y1 = scene.decal_point(s[3], s[4])
          Pix.line(b, x0, y0 - 1, x1, y1 - 1, @light, 1) if s[5] > 1      # lit lip on the main cracks only
          Pix.line(b, x0, y0, x1, y1, @dark, s[5])
        end
        return k >= 1.0
      end
    end

    class Actor
      attr_reader :rim_color

      # Rim light: a solid-colour copy peeking out one art pixel on one side.
      def set_rim(scene, color, dx = 1, dy = 0)
        if color.nil?
          @rim.dispose if @rim && !@rim.disposed?
          @rim = nil
          return
        end
        if !@rim
          @rim = Sprite.new(scene.viewport)
          @rim.bitmap = @gfx.bitmap
          @rim.ox = @sprite.ox
          @rim.oy = @sprite.oy
        end
        c = Util.rgb(color)
        @rim.color = Color.new(c[0], c[1], c[2], 255)
        @rim_off = [dx, dy]
      end

      def update_rim(scene)
        return if !@rim
        r = @rim
        s = @sprite
        r.src_rect.set(s.src_rect.x, s.src_rect.y, s.src_rect.width, s.src_rect.height)
        step = PX * [scene.camera.zoom.round, 1].max
        r.x = s.x + (@rim_off[0] * step)
        r.y = s.y + (@rim_off[1] * step)
        r.zoom_x = s.zoom_x
        r.zoom_y = s.zoom_y
        r.mirror = s.mirror
        r.angle = s.angle
        r.opacity = s.opacity
        r.z = s.z - 1
        r.visible = scene.silhouette.nil?
      end

      def dispose_rim
        @rim.dispose if @rim && !@rim.disposed?
        @rim = nil
      end
    end

    class Scene
      attr_reader :silhouette, :decal
      DECAL_X = -512     # world x of the decal layer's left edge (it is 1536 px wide)

      def set_silhouette(mode)
        @silhouette = mode
        if !@matte
          @matte = solid([255, 255, 255], 450, @viewport)
          @matte.visible = false
        end
        @matte.visible = !mode.nil?
        return if mode.nil?
        @matte.bitmap.fill_rect(0, 0, 4, 4, (mode == :white) ? Color.new(255, 255, 255) : Color.new(0, 0, 0))
      end

      # [r, g, b] figures take during an impact frame, or nil.
      def silhouette_rgb
        return nil if !@silhouette
        return (@silhouette == :white) ? [0.0, 0.0, 0.0] : [255.0, 255.0, 255.0]
      end

      def ensure_decal
        return @decal if @decal
        @decal = Bitmap.new(768, @vh + 16)
        @decal_sprite = Sprite.new(@viewport)
        @decal_sprite.bitmap = @decal
        @decal_sprite.z = 350
        return @decal
      end

      def decal_point(wx, wy)
        return ((wx - DECAL_X) / PX).round, (wy / PX).round
      end

      def update_decal
        return if !@decal_sprite
        sx, sy = @camera.to_screen(DECAL_X, 0, 1.0)
        @decal_sprite.x = sx.round
        @decal_sprite.y = sy.round
        @decal_sprite.zoom_x = @decal_sprite.zoom_y = PX * @camera.zoom
        @decal_sprite.visible = @silhouette.nil?
      end

      def op_impact_frames(a, dur)
        return ImpactFrames.new(self, a[:count] || 2, dur / (a[:count] || 2).to_f)
      end

      # Slows the scene clock for `dur` scene seconds; at scale <= 0.001 (a hitstop) the scene clock stops, so the
      # duration is counted on the wall clock instead (Gemini cinematics P0: slowmo(0.0) used to freeze forever).
      class SlowmoEffect < Effect
        def initialize(scale, dur, real)
          @scale = scale; @d = dur; @real = real; @rt0 = nil
        end

        def update(scene, lt, _dt)
          @rt0 ||= scene.real_time
          elapsed = (@real) ? scene.real_time - @rt0 : lt
          done = elapsed >= @d
          scene.timescale = (done) ? 1.0 : @scale
          return done
        end

        def dispose; end
      end

      def op_slowmo(a, dur)
        scale = [a[:scale].to_f, 0.0].max
        real = a.key?(:real) ? a[:real] : scale <= 0.001
        return SlowmoEffect.new(scale, dur, real)
      end

      attr_accessor :timescale

      def op_fracture(a, dur)
        ensure_decal
        return Fracture.new(self, a, dur)
      end

      def op_rim(a, _dur)
        act = actor!(a[:id])
        if a[:off] then act.set_rim(self, nil)
        else act.set_rim(self, a[:color] || [255, 255, 255], (a[:side] == :left) ? -1 : 1, a[:dy] || 0)
        end
        nil
      end

      # glow side: :left / :right, color:, level: 0..1 - light spilling in from an edge.
      def op_glow(a, dur)
        @glows ||= {}
        side = a[:side] || :left
        g = (@glows[side] ||= { :rgb => Util.rgb(a[:color] || [255, 255, 255])[0, 3], :level => 0.0 })
        g[:rgb] = Util.rgb(a[:color])[0, 3] if a[:color]
        from = g[:level]
        to = (a[:level] || 0).to_f
        tween(dur, :linear) { |k, _| g[:level] = Util.lerp(from, to, k) }
      end

      def glows_active?; return @glows && @glows.any? { |_, g| g[:level] > 0.01 }; end

      def draw_glows(b)
        return if !@glows
        @glows.each do |side, g|
          lv = g[:level] * (0.9 + (0.1 * Math.sin(@fx_frame * 0.7)))
          next if lv <= 0.01
          [[0.13, 8], [0.045, 4]].each do |frac, density|     # a faint dithered falloff, never a wall
            w = (@vw * frac * lv).round
            w -= w % 2
            next if w <= 0
            x = (side == :left) ? 0 : @vw - w
            Dither.fill(b, x, 0, w, @vh, g[:rgb], density)
          end
        end
      end
    end

    class Builder
      def impact_frames(**o); add(:impact_frames, o, o[:duration] || ((o[:count] || 2) * 0.07), true); end
      def slowmo(scale, **o); add(:slowmo, o.merge(:scale => scale), o[:duration] || 0.5); end
      # A real-clock freeze-frame on impact (Law 3): the scene stops for `duration` wall-clock seconds.
      def hitstop(duration = 0.14, **o); add(:slowmo, o.merge(:scale => 0.0, :real => true), duration); end
      def fracture(**o);      add(:fracture, check_points(o), o[:duration] || 1.0); end
      def rim(id, **o);       add(:rim, o.merge(:id => ref(id))); end
      def glow(**o);          add(:glow, o, o[:duration] || 1.0); end
    end
  end
end
