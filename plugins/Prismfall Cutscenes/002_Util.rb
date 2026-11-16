#===============================================================================
# Prismfall Cutscenes - 002 Utilities: easing, colours, pixel drawing, audio
#===============================================================================
module Prismfall
  module Cutscene
    module Ease
      FUNCS = {
        :linear    => proc { |k| k },
        :in        => proc { |k| k * k },
        :out       => proc { |k| 1 - ((1 - k) * (1 - k)) },
        :in_out    => proc { |k| (k < 0.5) ? 2 * k * k : 1 - (2 * (1 - k) * (1 - k)) },
        :in_cubic  => proc { |k| k * k * k },
        :out_cubic => proc { |k| 1 - ((1 - k)**3) },
        :sine      => proc { |k| 0.5 - (0.5 * Math.cos(Math::PI * k)) },
        :out_back  => proc { |k| 1 + (2.70158 * ((k - 1)**3)) + (1.70158 * ((k - 1)**2)) },
        :out_bounce => proc { |k|
          if k < 1 / 2.75 then 7.5625 * k * k
          elsif k < 2 / 2.75 then (7.5625 * (k - (1.5 / 2.75))**2) + 0.75
          elsif k < 2.5 / 2.75 then (7.5625 * (k - (2.25 / 2.75))**2) + 0.9375
          else (7.5625 * (k - (2.625 / 2.75))**2) + 0.984375
          end
        },
        :steps     => proc { |k| (k * 6).floor / 6.0 }   # deliberately choppy
      }

      def self.apply(name, k)
        k = 0.0 if k < 0
        k = 1.0 if k > 1
        f = FUNCS[name] || FUNCS[:linear]
        return f.call(k)
      end
    end

    # Four ready-made Color objects for one effect.
    class Palette
      attr_reader :core, :inner, :outer, :edge, :rgb

      def initialize(rgb)
        @rgb = rgb
        @core, @inner, @outer, @edge = rgb.map { |c| Color.new(c[0], c[1], c[2]) }
      end

      def [](i); return [@core, @inner, @outer, @edge][i % 4]; end
      def to_a;  return [@core, @inner, @outer, @edge]; end

      # A copy shifted towards white (k = 0..1), in 4 steps so it stays a palette.
      def whitened(k)
        step = (k * 4).round
        return self if step <= 0
        @white ||= {}
        @white[step] ||= Palette.new(@rgb.map { |c| c.map { |v| (v + ((255 - v) * step / 4.0)).round } })
        return @white[step]
      end
    end

    module Util
      module_function

      def now
        return System.uptime if defined?(System) && System.respond_to?(:uptime)
        return Process.clock_gettime(Process::CLOCK_MONOTONIC)
      end

      def clamp(v, a, b)
        return a if v < a
        return b if v > b
        return v
      end

      def lerp(a, b, k); return a + ((b - a) * k); end

      # Nearest position on the art-pixel grid.
      def snap(v); return (v.to_f / PX).round * PX; end

      # Deterministic noise 0...1 (same picture every run, no flicker by accident).
      def hash01(a, b = 0, c = 0)
        n = ((a.to_i * 374_761_393) + (b.to_i * 668_265_263) + (c.to_i * 2_246_822_519)) & 0xFFFFFFFF
        n = ((n ^ (n >> 13)) * 1_274_126_177) & 0xFFFFFFFF
        n ^= (n >> 16)
        return n / 4_294_967_296.0
      end

      # [r, g, b(, a)] from an array, Color or palette name (its "inner" colour).
      def rgb(spec)
        case spec
        when Array  then return spec
        when Symbol then return (PALETTES[spec] || PALETTES[:light])[1]
        when nil    then return [255, 255, 255]
        else
          return [spec.red, spec.green, spec.blue, spec.alpha] if spec.respond_to?(:red)
        end
        return [255, 255, 255]
      end

      def color(spec, alpha = nil)
        c = rgb(spec)
        return Color.new(c[0], c[1], c[2], alpha || c[3] || 255)
      end

      def mix(c1, c2, k)
        return [0, 1, 2].map { |i| (c1[i] + ((c2[i] - c1[i]) * k)).round }
      end

      # Palette from a name, a Palette or one [r, g, b] (a ramp is derived).
      def palette(spec)
        return spec if spec.is_a?(Palette)
        @palettes ||= {}
        key = spec
        return @palettes[key] if @palettes[key]
        if spec.is_a?(Array)
          base = spec[0, 3]
          rgb4 = [mix(base, [255, 255, 255], 0.85), mix(base, [255, 255, 255], 0.4), base, mix(base, [0, 0, 0], 0.45)]
        else
          rgb4 = PALETTES[spec] || PALETTES[:light]
        end
        @palettes[key] = Palette.new(rgb4)
        return @palettes[key]
      end

      def species_types(species)
        return [] if !defined?(GameData::Species) || species.nil?
        data = GameData::Species.try_get(species)
        return (data) ? data.types : []
      rescue StandardError
        return []
      end

      def type_palette(species, fallback = :light)
        t = species_types(species)[0]
        return TYPE_PALETTES[t] || fallback
      end

      def species_name(species)
        if defined?(GameData::Species)
          data = (GameData::Species.try_get(species) rescue nil)
          return data.name if data
        end
        return species.to_s.capitalize
      end

      def tr(text, *args)
        return _INTL(text, *args) if defined?(_INTL)
        args.each_with_index { |a, i| text = text.gsub("{#{i + 1}}", a.to_s) }
        return text
      end

      def log(msg)
        if defined?(echoln) then echoln("[Prismfall Cutscenes] #{msg}")
        else $stderr.puts("[Prismfall Cutscenes] #{msg}")
        end
      end
    end

    #---------------------------------------------------------------------------
    # Pixel drawing. Only Bitmap#fill_rect is used, with integer coordinates, so
    # every shape lands on the art-pixel grid with hard edges.
    #---------------------------------------------------------------------------
    module Pix
      module_function

      def rect(b, x, y, w, h, c)
        x = x.round; y = y.round; w = w.round; h = h.round
        if x < 0 then w += x; x = 0 end
        if y < 0 then h += y; y = 0 end
        w = b.width - x if x + w > b.width
        h = b.height - y if y + h > b.height
        return if w <= 0 || h <= 0
        b.fill_rect(x, y, w, h, c)
      end

      # Filled ellipse (disc when ry is nil); equal rows are merged into one rect.
      def disc(b, cx, cy, rx, c, ry = nil)
        rx = rx.round
        ry = (ry || rx).round
        return rect(b, cx, cy, 1, 1, c) if rx <= 0 || ry <= 0
        run_w = nil
        run_y = 0
        (-ry..ry + 1).each do |dy|
          w = (dy > ry) ? nil : (rx * Math.sqrt(1.0 - ((dy.to_f / ry)**2))).round
          next if w == run_w
          rect(b, cx - run_w, cy + run_y, (run_w * 2) + 1, dy - run_y, c) if run_w
          run_w = w
          run_y = dy
        end
      end

      # Ellipse outline, th art pixels thick.
      def ring(b, cx, cy, rx, c, th = 1, ry = nil)
        rx = rx.round
        ry = (ry || rx).round
        return if rx <= 0 || ry <= 0
        ix = rx - th
        iy = ry - th
        (-ry..ry).each do |dy|
          w = (rx * Math.sqrt(1.0 - ((dy.to_f / ry)**2))).round
          if ix > 0 && iy > 0 && dy.abs < iy
            wi = (ix * Math.sqrt(1.0 - ((dy.to_f / iy)**2))).round
            seg = [w - wi, 1].max
            rect(b, cx - w, cy + dy, seg, 1, c)
            rect(b, cx + w - seg + 1, cy + dy, seg, 1, c)
          else
            rect(b, cx - w, cy + dy, (w * 2) + 1, 1, c)
          end
        end
      end

      # Line with merged runs (few rects for near-horizontal/vertical lines).
      def line(b, x0, y0, x1, y1, c, th = 1)
        x0 = x0.round; y0 = y0.round; x1 = x1.round; y1 = y1.round
        dx = x1 - x0
        dy = y1 - y0
        n = [dx.abs, dy.abs].max
        return rect(b, x0, y0, th, th, c) if n == 0
        horiz = dx.abs >= dy.abs
        start = 0
        last = nil
        (0..n + 1).each do |i|
          minor = nil
          if i <= n
            minor = (horiz) ? (y0 + (dy * i / n.to_f)).round : (x0 + (dx * i / n.to_f)).round
          end
          next if minor == last
          if last
            a0 = ((horiz) ? x0 : y0) + (((horiz) ? dx : dy) <=> 0) * start
            a1 = ((horiz) ? x0 : y0) + (((horiz) ? dx : dy) <=> 0) * (i - 1)
            lo = [a0, a1].min
            len = (a0 - a1).abs + 1
            if horiz then rect(b, lo, last, len, th, c)
            else rect(b, last, lo, th, len, c)
            end
          end
          last = minor
          start = i
        end
      end

      # One row of 50% dither.
      def dither_row(b, x, y, w, c, phase = 0, step = 2)
        xx = x + (phase % step)
        while xx < x + w
          rect(b, xx, y, 1, 1, c)
          xx += step
        end
      end

      # Vertical banded gradient with dithered joins (pixel-art sky style).
      def gradient(b, x, y, w, h, colors, dither = true)
        n = colors.length
        cols = colors.map { |c| Util.color(c) }
        n.times do |i|
          y0 = y + (h * i / n)
          y1 = y + (h * (i + 1) / n)
          rect(b, x, y0, w, y1 - y0, cols[i])
          next if !dither || i == 0
          dither_row(b, x, y0 - 2, w, cols[i], 0, 4)
          dither_row(b, x, y0 - 1, w, cols[i], 1, 2)
          dither_row(b, x, y0, w, cols[i - 1], 0, 2)
          dither_row(b, x, y0 + 1, w, cols[i - 1], 2, 4)
        end
      end
    end

    #---------------------------------------------------------------------------
    # Audio (never raises; a missing file is silence)
    #---------------------------------------------------------------------------
    module Sound
      module_function

      def exists?(folder, name)
        return false if name.nil? || name == ""
        path = "Audio/#{folder}/#{name}"
        return FileTest.audio_exist?(path) if FileTest.respond_to?(:audio_exist?)
        return true
      rescue StandardError
        return false
      end

      # name: a file name, or a key of AUDIO (first existing candidate wins).
      def resolve(folder, name)
        list = (name.is_a?(Symbol)) ? (AUDIO[name] || [name.to_s]) : [name.to_s]
        return list.find { |n| exists?(folder, n) }
      end

      def play(kind, name, volume = nil, pitch = nil)
        folder = { :bgm => "BGM", :se => "SE", :me => "ME", :bgs => "BGS" }[kind]
        file = resolve(folder, name)
        return false if !file
        case kind
        when :bgm then pbBGMPlay(file, volume, pitch) if defined?(pbBGMPlay)
        when :se  then pbSEPlay(file, volume, pitch) if defined?(pbSEPlay)
        when :me  then pbMEPlay(file, volume, pitch) if defined?(pbMEPlay)
        when :bgs then pbBGSPlay(file, volume, pitch) if defined?(pbBGSPlay)
        end
        return true
      rescue StandardError => e
        Util.log("audio #{kind} #{name.inspect}: #{e.message}")
        return false
      end

      def fade(kind, seconds)
        if kind == :bgs then pbBGSFade(seconds) if defined?(pbBGSFade)
        elsif defined?(pbBGMFade) then pbBGMFade(seconds)
        end
      rescue StandardError
        nil
      end

      def cry(species, volume = 90, pitch = 100)
        return if !defined?(GameData::Species) || !GameData::Species.respond_to?(:play_cry_from_species)
        GameData::Species.play_cry_from_species(species, 0, volume, pitch)
      rescue StandardError
        nil
      end
    end
  end
end
