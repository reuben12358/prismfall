#===============================================================================
# Prismfall Cutscenes - 012 Sheet effects: hand-drawn effect cells as sprites
#-------------------------------------------------------------------------------
# How Rejuvenation / Reborn sell their set pieces (design/CUTSCENE_RESEARCH.md):
# small hand-drawn cells (192 px animation cells, or charset-format sheets)
# played at points, chained along paths, often with additive blending.
#
#   fx_sheet "Graphics/Animations/pfw_fx_explosions", grid: [4, 3], frames: 0..3,
#            at: point, hold: 0.06, blend: :add, scale: 1, loops: 1 (or :forever), id: :boom
#   stop_fx :boom
#   submerge :kyogre, to: 0, duration: 1.5      - reveal a sprite rising out of water
#   beam_clash style: :sheet, a: { from:, sheet: "Graphics/Characters/pfw_beam_sea",
#                                  flare: { sheet:, grid:, frames: } }, b: {...},
#              core: [{ sheet:, grid:, frames: }, ...], burst: { sheet:, grid:, frames: }, ...
#     - the beams are tiled segment cells (4x4 sheet, cells head-right), the
#       clash point is drawn from effect cells; struggle, rings, sparks,
#       flashes and outcomes are the normal beam_clash ones.
#===============================================================================
module Prismfall
  module Cutscene
    BLENDS = { :add => 1, :sub => 2, :normal => 0, nil => 0 }

    class Scene
      # One Bitmap per sheet per scene (many effects share it).
      def sheet_bitmap(path)
        @sheet_cache ||= {}
        bmp = @sheet_cache[path]
        return bmp if bmp && !bmp.disposed?
        bmp = Gfx.load_bitmap(path)
        @sheet_cache[path] = bmp
        return bmp
      end

      alias prismfall_sheets_dispose dispose
      def dispose
        prismfall_sheets_dispose
        (@sheet_cache || {}).each_value { |b| b.dispose if b && !b.disposed? }
        @sheet_cache = {}
      end
    end

    # A sprite stepping through cells of a sheet at a world point.
    class SheetFx < Effect
      def initialize(scene, a)
        @bmp = scene.sheet_bitmap(a[:sheet])
        @at = (a[:at].is_a?(Proc)) ? a[:at] : scene.anchor(a[:at] || [scene.w / 2, scene.h / 2])
        @cols, @rows = a[:grid] || [5, 1]
        @frames = (a[:frames] || (0...(@cols * @rows))).to_a
        @holds = (a[:holds] || [a[:hold] || 0.06] * @frames.length).map(&:to_f)
        @loops = a[:loops] || 1
        @scale = (a[:scale] || 1).to_f
        @offset = a[:offset] || [0, 0]
        @spin = (a[:spin] || 0).to_f
        @angle = (a[:angle] || 0).to_f
        @opacity = a[:opacity] || 255
        return if !@bmp
        @cw = @bmp.width / @cols
        @ch = @bmp.height / @rows
        @sprite = Sprite.new(scene.viewport)
        @sprite.bitmap = @bmp
        @sprite.ox = @cw / 2
        @sprite.oy = @ch / 2
        @sprite.z = a[:z] || 1100
        @sprite.blend_type = BLENDS[a[:blend]] || 0
        @sprite.mirror = a[:mirror] || false
        @sprite.opacity = @opacity
        @sprite.visible = false
        @total = @holds.sum
      end

      def stop; @stopped = true; end

      def update(scene, lt, dt)
        return true if !@bmp || @stopped
        return true if @loops != :forever && lt >= @total * @loops
        t = lt % @total
        i = 0
        acc = 0.0
        i += 1 while i < @frames.length - 1 && t >= (acc += @holds[i])
        cell = @frames[i]
        @sprite.src_rect.set((cell % @cols) * @cw, (cell / @cols) * @ch, @cw, @ch)
        pt = @at.call
        sx, sy = scene.camera.to_screen(pt[0] + @offset[0], pt[1] + @offset[1], 1.0)
        @sprite.x = sx.round
        @sprite.y = sy.round
        @sprite.zoom_x = @sprite.zoom_y = @scale * scene.camera.zoom
        @sprite.angle = @angle + (@spin * lt)
        @sprite.visible = scene.silhouette.nil?
        return false
      end

      def dispose
        @sprite.dispose if @sprite && !@sprite.disposed?
      end
    end

    class Actor
      def submerge; return @submerge || 0; end
      def submerge=(v); @submerge = v.round; end

      alias prismfall_sheets_update update
      def update(scene, dt)
        prismfall_sheets_update(scene, dt)
        if [:charset, :grid].include?(@gfx.mode) && @sprite
          vis = [@gfx.fh - (@submerge || 0), 0].max
          @sprite.oy = vis
          r = @sprite.src_rect
          @sprite.src_rect.set(r.x, r.y, r.width, vis)
        end
      end
    end

    #---------------------------------------------------------------------------
    # The beam clash, drawn from sheets
    #---------------------------------------------------------------------------
    class SheetBeamClash < BeamClash
      STEP = 32           # segment spacing along the beam (cells are 64 long, so they overlap by half)

      def initialize(scene, a, dur)
        super
        @scene = scene
        @spec = a
        @no_rings = a[:rings] != true
        @sides = [[@a, a[:a]], [@b, a[:b]]].map do |side, o|
          bmp = scene.sheet_bitmap(o[:sheet])
          { :side => side, :bmp => bmp, :sprites => [], :flare => o[:flare] }
        end
        @cores = (a[:core] || []).map do |c|
          s = Sprite.new(scene.viewport)
          s.bitmap = scene.sheet_bitmap(c[:sheet])
          s.blend_type = BLENDS[c.fetch(:blend, :add)] || 1
          s.z = 1300
          s.visible = false
          { :sprite => s, :spec => c }
        end
        @flares = @sides.map do |sd|
          f = sd[:flare]
          next nil if !f
          s = Sprite.new(scene.viewport)
          s.bitmap = scene.sheet_bitmap(f[:sheet])
          s.blend_type = BLENDS[f.fetch(:blend, :add)] || 1
          s.z = 1250
          s.visible = false
          { :sprite => s, :spec => f }
        end
        @burst = a[:burst]
      end

      def cell_rect(sprite, spec, index)
        cols, rows = spec[:grid] || [5, 1]
        b = sprite.bitmap
        return [0, 0] if !b
        cw = b.width / cols
        ch = b.height / rows
        frames = (spec[:frames] || (0...(cols * rows))).to_a
        cell = frames[index % frames.length]
        sprite.src_rect.set((cell % cols) * cw, (cell / cols) * ch, cw, ch)
        sprite.ox = cw / 2
        sprite.oy = ch / 2
        return [cw, ch]
      end

      def burst_at(scene, pt, spec, scale = 1.0, z = 1350)
        return if !spec
        scene.run_effect(SheetFx.new(scene, spec.merge(:at => pt, :scale => scale * (spec[:scale] || 1), :z => z,
                                                       :blend => spec.fetch(:blend, :add))), scene.time)
      end

      # Like the base surge, without the code-drawn rings: flash, shake, sprays, effect cells.
      def surge(scene, c, pa, pb, power = 1.0)
        pal_a, pal_b = palettes
        scene.add_flash([255, 255, 255], 0.14, [110 * @intensity * power, 130].min)
        scene.add_shake((@shake + 4) * @intensity * power, 0.35)
        ang = Math.atan2(pb[1] - pa[1], pb[0] - pa[0]) * 180 / Math::PI
        [90, -90].each do |up|
          scene.burst_at(:sparks, c, 10, pal_a, { :angle => ang + up - 25, :spread => 40, :speed => 1.4 })
          scene.burst_at(:sparks, c, 10, pal_b, { :angle => ang + up + 25, :spread => 40, :speed => 1.4 })
        end
        scene.burst_at(:ice_shards, [c[0], ground_y(c)], 10, nil, { :speed => 1.2 })
        burst_at(scene, c, @burst, 0.9 + (0.4 * power))
        burst_at(scene, [c[0], ground_y(c)], @spec[:steam], 1.0, 900) if @spec[:steam]
      end

      def update(scene, lt, dt)
        done = super
        @lt_now = lt
        if @done && !@sheet_done
          @sheet_done = true
          c, pa, pb = clash_point
          case @winner
          when :a then burst_at(scene, pb, @burst, 2.0)
          when :b then burst_at(scene, pa, @burst, 2.0)
          when :both then burst_at(scene, c, @burst, 2.6)
          end
        end
        layout(scene, lt)
        return done
      end

      def layout(scene, lt)
        c, pa, pb = clash_point
        f = (lt * 12).to_i
        zoom = scene.camera.zoom
        launching = lt < @launch
        k = (launching) ? Util.clamp(lt / @launch, 0.0, 1.0) : 1.0
        gutter = @winner == :fizzle && @resolving && f.odd?
        whiten = @white
        @sides.each_with_index do |sd, n|
          side = sd[:side]
          src = (n == 0) ? pa : pb
          head = [src[0] + ((c[0] - src[0]) * k), src[1] + ((c[1] - src[1]) * k)]
          wf = @wf[n]
          dx = head[0] - src[0]
          dy = head[1] - src[1]
          len = Math.sqrt((dx * dx) + (dy * dy))
          sprites = sd[:sprites]
          if !sd[:bmp] || len < 8 || wf < 0.03 || gutter
            sprites.each { |s| s.visible = false }
          else
            ux = dx / len
            uy = dy / len
            ang = (n == 0) ? Math.atan2(-uy, ux) : Math.atan2(uy, -ux)
            deg = ang * 180 / Math::PI
            count = [((len - STEP) / STEP).ceil + 1, 1].max
            while sprites.length < count
              s = Sprite.new(scene.viewport)
              s.bitmap = sd[:bmp]
              s.ox = sd[:bmp].width / 8
              s.oy = sd[:bmp].height / 8
              s.mirror = (n == 1)
              sprites.push(s)
            end
            cw = sd[:bmp].width / 4
            ch = sd[:bmp].height / 4
            sprites.each_with_index do |s, i|
              if i >= count
                s.visible = false
                next
              end
              back = (cw / 2) + ((count - 1 - i) * STEP)
              wx = head[0] - (ux * back)
              wy = head[1] - (uy * back)
              sx, sy = scene.camera.to_screen(wx, wy, 1.0)
              s.src_rect.set(((f + i) % 4) * cw, (((f / 2) + i) % 4) * ch, cw, ch)
              s.x = sx.round
              s.y = sy.round
              s.zoom_x = zoom
              s.zoom_y = zoom * [wf, 1.6].min
              s.angle = deg
              s.z = 1000 + i + (n * 2)
              s.visible = scene.silhouette.nil?
              s.color.set(255, 255, 255, (whiten * 230).round)
            end
          end
          fl = @flares[n]
          next if !fl
          if wf < 0.05
            fl[:sprite].visible = false
            next
          end
          cell_rect(fl[:sprite], fl[:spec], f)
          sx, sy = scene.camera.to_screen(src[0], src[1], 1.0)
          fl[:sprite].x = sx.round
          fl[:sprite].y = sy.round
          fl[:sprite].zoom_x = fl[:sprite].zoom_y = zoom * (fl[:spec][:scale] || 1.0) * [wf, 1.4].min
          fl[:sprite].visible = scene.silhouette.nil?
        end
        @cores.each_with_index do |co, i|
          s = co[:sprite]
          if launching || @ball_scale <= 0.02 || @mote
            s.visible = false
            next
          end
          cell_rect(s, co[:spec], f + (i * 2))
          sx, sy = scene.camera.to_screen(c[0], c[1], 1.0)
          pulse = 1.0 + (0.12 * [0, 1, 2, 1][f % 4])
          s.x = sx.round
          s.y = sy.round
          s.zoom_x = s.zoom_y = zoom * (co[:spec][:scale] || 1.0) * @ball_scale * pulse
          s.angle = (co[:spec][:spin] || 0) * lt
          s.visible = scene.silhouette.nil?
        end
      end

      # Ground light, actor lighting and the falling mote stay; beams and the
      # clash ball are sprites (layout above).
      def draw(scene, back, front)
        @scene_ref = scene
        c, pa, pb = clash_point
        ax, = scene.to_fx(pa)
        bx, = scene.to_fx(pb)
        cx, cy = scene.to_fx(c)
        f = scene.fx_frame
        @dir_x = ((bx - ax) <=> 0)
        @dir_x = 1 if @dir_x == 0
        pal_a, pal_b = palettes
        z = scene.camera.zoom
        _gx, gy = scene.to_fx([c[0], ground_y(c)])
        light_actors(scene, @lt >= @launch && @wf[0] + @wf[1] > 0.2 && !@mote)
        ground_light(back, ax, cx, gy, @a.width * z * @wf[0], pal_a, f) if @lt >= @launch
        ground_light(back, bx, cx, gy, @b.width * z * @wf[1], pal_b, f) if @lt >= @launch
        if @mote
          mx, my = scene.to_fx([@mote[0], @mote[1]])
          Pix.rect(front, mx, my - 4, 2, 4, Util.palette(:white).outer)
          Pix.rect(front, mx - 1, my, 4, 4, Util.palette(:white).core)
        end
      end

      def dispose
        super
        @sides.each { |sd| sd[:sprites].each { |s| s.dispose if !s.disposed? } }
        @cores.each { |co| co[:sprite].dispose if !co[:sprite].disposed? }
        @flares.compact.each { |fl| fl[:sprite].dispose if !fl[:sprite].disposed? }
      end
    end

    class Scene
      alias prismfall_sheets_op_beam_clash op_beam_clash
      def op_beam_clash(a, dur)
        return SheetBeamClash.new(self, a, dur) if a[:style] == :sheet
        return prismfall_sheets_op_beam_clash(a, dur)
      end

      def op_fx_sheet(a, _dur)
        return SheetFx.new(self, a)
      end

      def op_stop_fx(a, _dur)
        e = @effects.find { |x| x.is_a?(SheetFx) && x.id == a[:id] }
        e.stop if e
        nil
      end

      def op_submerge(a, dur)
        act = actor!(a[:id])
        from = act.submerge
        to = (a[:to] || 0).to_f
        tween(dur, a[:ease] || :out) { |k, _| act.submerge = Util.lerp(from, to, k) }
      end
    end

    # A soft dithered shadow under an actor (flyers: ground: pixels below the feet).
    class GroundShadow < Effect
      def initialize(scene, a)
        @act = scene.actor!(a[:id])
        @rx = a[:size] || 28
        @ground = a[:ground] || 0
        @rgb = a[:color] || [16, 24, 48]
      end

      def draws?; return true; end
      def update(scene, lt, dt); return !scene.actors.value?(@act); end

      def draw(scene, back, front)
        return if @act.opacity < 32
        x, y = scene.to_fx([@act.x + @act.off_x, @act.y + @ground])
        r = (@rx * scene.camera.zoom / PX).round
        Dither.disc(back, x, y, r, [(r * 0.35).round, 1].max, @rgb, 2)
      end
    end

    class Scene
      def op_shadow(a, _dur); return GroundShadow.new(self, a); end
    end

    class Builder
      def shadow(id, **o); add(:shadow, o.merge(:id => ref(id))); end
    end

    class Builder
      def fx_sheet(path, **o)
        add(:fx_sheet, check_points(o).merge(:sheet => path), 0.0)
      end

      def stop_fx(id); add(:stop_fx, { :id => id }); end
      def submerge(id, **o); add(:submerge, o.merge(:id => ref(id)), o[:duration] || 1.0); end
    end
  end
end
