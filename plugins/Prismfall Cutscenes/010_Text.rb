#===============================================================================
# Prismfall Cutscenes - 010 Captions, speaker lines, title and VS cards, HP bars
#-------------------------------------------------------------------------------
#   text "Caption."                     (position: :bottom / :top / :center)
#   say "Sigrun", "Father. Enough."     (name tag + line, typed out)
#   title "THE GLASS DUNES", sub: "Chapter 19"
#   hp_bar :mon, value: 0.1, duration: 0.6      hp_bar :mon, show: false
# Text is timed (it never waits for a button), so scenes keep their length.
#===============================================================================
module Prismfall
  module Cutscene
    module TextDraw
      LINE_H = 30

      module_function

      def font(bmp, size = nil)
        pbSetSystemFont(bmp) if defined?(pbSetSystemFont)
        bmp.font.size = size if size
      end

      def outline(bmp, x, y, w, h, str, base, shadow, align = 0)
        bmp.font.color = shadow
        [[-2, 0], [2, 0], [0, -2], [0, 2], [2, 2]].each { |dx, dy| bmp.draw_text(x + dx, y + dy, w, h, str, align) }
        bmp.font.color = base
        bmp.draw_text(x, y, w, h, str, align)
      end

      def wrap(bmp, str, max_w)
        lines = []
        str.to_s.split("\n").each do |para|
          line = ""
          para.split(" ").each do |word|
            try = (line.empty?) ? word : "#{line} #{word}"
            if !line.empty? && bmp.text_size(try).width > max_w
              lines.push(line)
              line = word
            else
              line = try
            end
          end
          lines.push(line)
        end
        return lines
      end
    end

    class Caption < Effect
      def initialize(scene, a, dur)
        @dur = dur
        @str = a[:text].to_s
        @speaker = a[:speaker]
        @type = (a.has_key?(:type)) ? a[:type] : !@speaker.nil?
        w = scene.w
        probe = Bitmap.new(8, 8)
        TextDraw.font(probe)
        @lines = TextDraw.wrap(probe, @str, w - 64)
        probe.dispose
        rows = @lines.length + ((@speaker) ? 1 : 0)
        @h = (rows * TextDraw::LINE_H) + 12
        @bmp = Bitmap.new(w, @h)
        TextDraw.font(@bmp)
        @sprite = Sprite.new(scene.ui)
        @sprite.bitmap = @bmp
        @sprite.z = Scene::Z_TEXT
        bar = (scene.respond_to?(:bar_height) ? scene.bar_height.to_f.round : 0)   # keep clear of the letterbox
        @sprite.y = case a[:position]
                    when :top    then 8 + bar
                    when :center then (scene.h - @h) / 2
                    else scene.h - @h - 8 - bar
                    end
        @base = Util.color(a[:color] || TEXT_COLOR)
        @shadow = Util.color(TEXT_SHADOW)
        @name_col = Util.color(a[:name_color] || [255, 216, 96])
        @band = a[:band] != false
        @shown = -1
        @total = @str.length
        redraw((@type) ? 0 : @total)
      end

      def redraw(count)
        return if count == @shown
        @shown = count
        @bmp.clear
        @bmp.fill_rect(0, 0, @bmp.width, @h, Color.new(0, 0, 0, 150)) if @band
        @bmp.fill_rect(0, 0, @bmp.width, 2, Color.new(0, 0, 0, 220)) if @band
        y = 6
        if @speaker
          TextDraw.outline(@bmp, 32, y, @bmp.width - 64, TextDraw::LINE_H, @speaker.to_s, @name_col, @shadow, 0)
          y += TextDraw::LINE_H
        end
        left = count
        @lines.each do |line|
          part = line[0, [left, 0].max]
          left -= line.length + 1
          TextDraw.outline(@bmp, 32, y, @bmp.width - 64, TextDraw::LINE_H, part, @base, @shadow, (@speaker) ? 0 : 1) if !part.empty?
          y += TextDraw::LINE_H
        end
      end

      def update(scene, lt, dt)
        redraw([(lt * 45).to_i, @total].min) if @type
        fade = 0.18
        k = [lt / fade, (@dur - lt) / fade, 1.0].min
        @sprite.opacity = (255 * Util.clamp(k, 0.0, 1.0)).round
        return lt >= @dur
      end

      def dispose
        @sprite.dispose if !@sprite.disposed?
        @bmp.dispose if !@bmp.disposed?
      end
    end

    # Big centred card: a dark band, chunky 2x title, optional subtitle.
    class TitleCard < Effect
      def initialize(scene, a, dur)
        @dur = dur
        w = scene.w
        @bmp = Bitmap.new(w / 2, 56)
        TextDraw.font(@bmp)
        pal = Util.palette(a[:color] || :light)
        @bmp.fill_rect(0, 8, w / 2, 40, Color.new(0, 0, 0, 190))
        @bmp.fill_rect(0, 8, w / 2, 1, pal.inner)
        @bmp.fill_rect(0, 47, w / 2, 1, pal.outer)
        TextDraw.outline(@bmp, 0, 12, w / 2, 30, a[:text].to_s, pal.core, Util.color(TEXT_SHADOW), 1)
        @sprite = Sprite.new(scene.ui)
        @sprite.bitmap = @bmp
        @sprite.zoom_x = @sprite.zoom_y = 2
        @sprite.z = Scene::Z_CARD
        @y = (a[:y] || ((scene.h / 2) - 56 - ((a[:sub]) ? 12 : 0)))
        @sprite.y = @y
        @w = w
        if a[:sub]
          @sub_bmp = Bitmap.new(w, 34)
          TextDraw.font(@sub_bmp)
          TextDraw.outline(@sub_bmp, 0, 2, w, 30, a[:sub].to_s, Util.color(TEXT_COLOR), Util.color(TEXT_SHADOW), 1)
          @sub = Sprite.new(scene.ui)
          @sub.bitmap = @sub_bmp
          @sub.y = @y + 108
          @sub.z = Scene::Z_CARD
        end
      end

      def update(scene, lt, dt)
        k_in = Ease.apply(:out_cubic, lt / 0.3)
        k_out = Util.clamp((@dur - lt) / 0.25, 0.0, 1.0)
        @sprite.x = Util.snap(-@w * (1 - k_in))
        @sprite.opacity = (255 * k_out).round
        if @sub
          @sub.x = Util.snap(@w * (1 - k_in))
          @sub.opacity = (255 * k_out).round
        end
        return lt >= @dur
      end

      def dispose
        [@sprite, @sub].compact.each { |s| s.dispose if !s.disposed? }
        [@bmp, @sub_bmp].compact.each { |b| b.dispose if !b.disposed? }
      end
    end

    # "A vs B" intro: two colour panels slam in with trainer sprites, names and
    # team icons; VS stamps in the middle.
    #   vs_card a: { name:, trainer:, color:, team: [species...] }, b: { ... }
    class VsCard < Effect
      def initialize(scene, a, dur)
        @dur = dur
        @w = scene.w
        @h = scene.h
        @sides = [a[:a] || {}, a[:b] || {}].each_with_index.map { |s, i| build_side(scene, s, i) }
        @vs_bmp = Bitmap.new(64, 36)
        TextDraw.font(@vs_bmp)
        TextDraw.outline(@vs_bmp, 0, 2, 64, 30, "VS", Color.new(255, 255, 255), Color.new(16, 16, 24), 1)
        @vs = Sprite.new(scene.ui)
        @vs.bitmap = @vs_bmp
        @vs.ox = 32
        @vs.oy = 18
        @vs.x = @w / 2
        @vs.y = @h / 2
        @vs.z = Scene::Z_CARD + 20
        @vs.visible = false
        @stamped = false
        Sound.play(:se, :card)
      end

      def build_side(scene, s, i)
        half = @w / 2
        pal = Util.palette(s[:color] || ((i == 0) ? :water : :fire))
        panel_bmp = Bitmap.new(half / 2, @h / 2)
        Pix.gradient(panel_bmp, 0, 0, half / 2, @h / 2, [pal.rgb[3], Util.mix(pal.rgb[3], pal.rgb[2], 0.5), pal.rgb[2]], true)
        12.times { |k| Pix.rect(panel_bmp, 0, (k * 16) + ((i == 0) ? 0 : 8), half / 2, 1, pal.outer) }
        edge_x = (i == 0) ? (half / 2) - 2 : 0
        Pix.rect(panel_bmp, edge_x, 0, 2, @h / 2, pal.core)
        panel = Sprite.new(scene.ui)
        panel.bitmap = panel_bmp
        panel.zoom_x = panel.zoom_y = 2
        panel.z = Scene::Z_CARD
        gfx = Gfx.trainer(s[:trainer])
        tr = Sprite.new(scene.ui)
        tr.bitmap = gfx.bitmap
        tr.ox = gfx.fw / 2
        tr.oy = gfx.fh
        tr.zoom_x = tr.zoom_y = gfx.px
        tr.mirror = (i == 0)
        tr.z = Scene::Z_CARD + 5
        name_bmp = Bitmap.new(half, 36)
        TextDraw.font(name_bmp)
        name_bmp.fill_rect(0, 2, half, 32, Color.new(0, 0, 0, 170))
        TextDraw.outline(name_bmp, 8, 4, half - 16, 28, s[:name].to_s, pal.core, Color.new(16, 16, 24), 1)
        name = Sprite.new(scene.ui)
        name.bitmap = name_bmp
        name.z = Scene::Z_CARD + 10
        icons = (s[:team] || [])[0, 6].each_with_index.map do |sp, k|
          g = Gfx.icon(sp)
          ic = Sprite.new(scene.ui)
          ic.bitmap = g.bitmap
          ic.src_rect.set(0, 0, g.fw, g.fh)
          ic.zoom_x = ic.zoom_y = g.px
          ic.z = Scene::Z_CARD + 11 + k
          [ic, g]
        end
        return { :panel => panel, :panel_bmp => panel_bmp, :trainer => tr, :gfx => gfx, :name => name,
                 :name_bmp => name_bmp, :icons => icons, :dir => (i == 0) ? -1 : 1 }
      end

      def update(scene, lt, dt)
        half = @w / 2
        out = Util.clamp((@dur - lt) / 0.3, 0.0, 1.0)
        @sides.each_with_index do |s, i|
          base = (i == 0) ? 0 : half
          k = Ease.apply(:out_cubic, lt / 0.35)
          k2 = Ease.apply(:out_cubic, (lt - 0.15) / 0.4)
          off = s[:dir] * half * (1 - k)
          off2 = s[:dir] * half * (1 - k2)
          exit_off = s[:dir] * half * (1 - Ease.apply(:out, out))
          s[:panel].x = Util.snap(base + off + exit_off)
          s[:trainer].x = Util.snap(base + (half / 2) + off2 + exit_off)
          s[:trainer].y = @h - 64
          s[:name].x = Util.snap(base + off2 + exit_off)
          s[:name].y = 20
          s[:icons].each_with_index do |(ic, g), n|
            ic.x = Util.snap(base + 6 + (n * 36) + off2 + exit_off)
            ic.y = @h - 66
            ic.visible = lt > 0.5 + (n * 0.07)
          end
        end
        if lt >= 0.6
          if !@stamped
            @stamped = true
            @vs.visible = true
            scene.add_flash([255, 255, 255], 0.25, 200)
            scene.add_shake(4, 0.2)
          end
          z = 2 + (2 * (1 - Ease.apply(:out, (lt - 0.6) / 0.18))).round
          @vs.zoom_x = @vs.zoom_y = z
          @vs.opacity = (255 * out).round
        end
        return lt >= @dur
      end

      def dispose
        @sides.each do |s|
          [s[:panel], s[:trainer], s[:name]].each { |sp| sp.dispose if !sp.disposed? }
          [s[:panel_bmp], s[:name_bmp]].each { |b| b.dispose if !b.disposed? }
          Gfx.dispose(s[:gfx])
          s[:icons].each do |ic, g|
            ic.dispose if !ic.disposed?
            Gfx.dispose(g)
          end
        end
        @vs.dispose if !@vs.disposed?
        @vs_bmp.dispose if !@vs_bmp.disposed?
      end
    end

    # Small HP bar floating over an actor.
    class HpBar
      attr_accessor :value, :visible

      def initialize(scene, actor)
        @actor = actor
        @value = 1.0
        @visible = true
        @drawn = nil
        @bmp = Bitmap.new(30, 5)
        @sprite = Sprite.new(scene.viewport)
        @sprite.bitmap = @bmp
        @sprite.ox = 15
        @sprite.zoom_x = @sprite.zoom_y = PX
        @sprite.z = Scene::Z_FX_FRONT + 50
      end

      def update(scene, dt)
        fill = (@value * 26).ceil
        fill = 1 if @value > 0 && fill < 1
        if fill != @drawn
          @drawn = fill
          @bmp.fill_rect(0, 0, 30, 5, Color.new(24, 24, 32))
          @bmp.fill_rect(1, 1, 28, 3, Color.new(72, 72, 88))
          col = if @value > 0.5 then Color.new(88, 216, 104)
                elsif @value > 0.2 then Color.new(248, 208, 56)
                else Color.new(240, 72, 56)
                end
          @bmp.fill_rect(2, 1, fill, 3, col) if fill > 0
        end
        top = @actor.top
        sx, sy = scene.camera.to_screen(top[0] + @actor.off_x, top[1] - 14, 1.0)
        @sprite.x = Util.snap(sx)
        @sprite.y = Util.snap(sy)
        @sprite.visible = @visible && @actor.opacity > 8
      end

      def dispose
        @sprite.dispose if !@sprite.disposed?
        @bmp.dispose if !@bmp.disposed?
      end
    end

    class Scene
      def op_text(a, dur);    return Caption.new(self, a, dur); end
      def op_title(a, dur);   return TitleCard.new(self, a, dur); end
      def op_vs_card(a, dur); return VsCard.new(self, a, dur); end

      def op_hp_bar(a, dur)
        act = actor!(a[:id])
        bar = (@attached[a[:id]] ||= HpBar.new(self, act))
        bar.visible = a[:show] if a.has_key?(:show)
        return nil if !a[:value]
        from = (a[:from] || bar.value).to_f
        to = a[:value].to_f
        tween(dur, :out) { |k, _| bar.value = Util.lerp(from, to, k) }
      end
    end
  end
end
