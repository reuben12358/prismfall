#===============================================================================
# Prismfall Cutscenes - 012 Techniques borrowed from Rejuvenation / Reborn
#-------------------------------------------------------------------------------
# See design/CUTSCENE_RESEARCH.md for where each one comes from.
#
#   actor :portal, sheet: "Graphics/Characters/DimensionPortal", grid: [4, 4], frame: 0
#   pose :portal, frame: 5          (or row:, col:)  - show one cell
#   flipbook :portal, frames: 0..7, hold: 0.1, loops: 1, se: { 4 => "Anim/Explosion" }
#                                    - step through hand-drawn cells (charset-format
#                                      pose sheets and effect sheets, Rejuvenation style)
#   still "Graphics/Pictures/Storyboard_1", duration: 3, fade: 0.4, steps: 5, dim: 120
#                                    - a full-screen illustration over the scene
#   pulse tone: [-68, -102, -102, 120], duration: 0.15, times: 2
#                                    - a short tone heartbeat (Reborn's impact beat)
#   anim 16, at: :kyogre             - an RMXP/Essentials database animation (Animations.rxdata)
#   fade_in steps: 5 / fade_out steps: 5 / fade :id, to: 0, steps: 5   - stepped fades
#   define(:ID, on_map: true) { actor :mark, image: "...", event: 12, offset: [0, -40] }
#                                    - play over the live map; actors can follow events
#   Prismfall::Cutscene.photosensitive = true   - weak flashes, no impact frames, little shake
#   actor ..., blend: :add / :sub    - additive glow cells / subtractive darkness (Reborn's anim cells)
#   play_sheet "Graphics/Animations/x", grid: [5, 2], frames: 0..4, at: [x, y], hold: 0.05, blend: :add
#                                    - a one-shot effect sheet that removes itself (chain several
#                                      along a path with at() for Reborn-style travelling bursts)
#   follow :kyogre, smooth: 0.15     - camera keeps tracking an actor (follow off: true to stop)
#===============================================================================
module Prismfall
  module Cutscene
    @photosensitive = nil

    class << self
      attr_writer :photosensitive

      # Explicit setting first, then a game option if one exists.
      def photosensitive?
        return @photosensitive if !@photosensitive.nil?
        if defined?($PokemonSystem) && $PokemonSystem.respond_to?(:photosensitive)
          return [1, true].include?($PokemonSystem.photosensitive)
        end
        return false
      end
    end

    module Gfx
      module_function

      # Any grid sheet: cols x rows equal cells (charset format = 4 x 4).
      def sheet(path, grid = [4, 4], px = 1)
        bmp = load_bitmap(path)
        if !bmp
          Util.log("sheet #{path.inspect} not found; using a placeholder")
          return placeholder_charset([200, 200, 208])
        end
        cols, rows = grid
        return Data.new(bmp, bmp.width / cols, bmp.height / rows, cols * rows, :grid, px, nil, false)
      end
    end

    class Actor
      attr_accessor :cell
      attr_reader :follow

      alias prismfall_tech_initialize initialize
      def initialize(scene, id, o)
        if o[:sheet]
          @sheet_opts = o
        end
        @follow = o[:event]
        @blend = { :add => 1, :sub => 2, :normal => 0 }[o[:blend]] || o[:blend]
        @follow_off = o[:offset] || [0, 0]
        @grid_cols = (o[:grid] || [4, 4])[0]
        prismfall_tech_initialize(scene, id, o)
        set_frame(o[:frame]) if o[:frame]
      end

      # Cell index -> [row, col].
      def set_frame(f)
        @cell = (f.is_a?(Array)) ? f : [f / @grid_cols, f % @grid_cols]
      end

      alias prismfall_tech_update update
      def update(scene, dt)
        if @follow
          ch = Actor.character(@follow)
          if ch && ch.respond_to?(:screen_x)
            @x = ch.screen_x + @follow_off[0]
            @y = ch.screen_y + @follow_off[1]
          end
        end
        prismfall_tech_update(scene, dt)
        @sprite.blend_type = @blend if @blend
        if @cell && [:grid, :charset, :icon].include?(@gfx.mode)
          @sprite.src_rect.set(@cell[1] * @gfx.fw, @cell[0] * @gfx.fh, @gfx.fw, @gfx.fh - (@submerge || 0))
        elsif @gfx.mode == :grid
          @sprite.src_rect.set(0, 0, @gfx.fw, @gfx.fh - (@submerge || 0))
        end
      end

      def self.character(ref)
        return $game_player if ref == :player || ref == 0
        return nil if !defined?($game_map) || !$game_map || !$game_map.respond_to?(:events)
        return $game_map.events[ref] if ref.is_a?(Integer)
        return $game_map.events.values.find { |e| e.respond_to?(:name) && e.name.to_s == ref.to_s }
      end
    end

    module Gfx
      class << self
        alias prismfall_tech_for_actor for_actor
        def for_actor(o)
          return sheet(o[:sheet], o[:grid] || [4, 4], o[:px] || 1) if o[:sheet]
          return prismfall_tech_for_actor(o)
        end
      end
    end

    # A full-screen picture faded in over the world, held, faded out.
    class Still < Effect
      def initialize(scene, a, dur)
        @dur = dur
        @fade = [a[:fade] || 0.3, dur / 2.0].min
        @ease = (a[:steps]) ? :"step#{a[:steps]}" : :linear
        @sprites = []
        if a[:dim]
          d = scene.solid([0, 0, 0], 140)
          d.opacity = 0
          @sprites.push([d, a[:dim].to_f])
        end
        bmp = Gfx.load_bitmap(a[:image])
        if bmp
          s = Sprite.new(scene.ui)
          s.bitmap = bmp
          s.z = 150
          s.x = (scene.w - bmp.width) / 2
          s.y = (scene.h - bmp.height) / 2
          s.opacity = 0
          @sprites.push([s, (a[:opacity] || 255).to_f])
          @own = s
        else
          Util.log("still #{a[:image].inspect} not found")
        end
      end

      def update(scene, lt, dt)
        k_in = Ease.apply(@ease, lt / [@fade, 0.001].max)
        k_out = Ease.apply(@ease, (@dur - lt) / [@fade, 0.001].max)
        k = [k_in, k_out, 1.0].min
        @sprites.each { |s, full| s.opacity = (full * k).round }
        return lt >= @dur
      end

      def dispose
        @sprites.each { |s, _| s.visible = false if !s.disposed? }
        return if !@own || @own.disposed?
        @own.bitmap.dispose if @own.bitmap && !@own.bitmap.disposed?
        @own.dispose
      end
    end

    # A database animation (Animations.rxdata) played at a world point.
    class DbAnim < Effect
      def initialize(scene, a)
        @at = scene.anchor(a[:at] || [scene.w / 2, scene.h / 2])
        @sprite = RPG::Sprite.new(scene.viewport)
        @sprite.bitmap = Bitmap.new(1, 1)
        @sprite.z = a[:z] || 1200
        place(scene)
        @sprite.animation($data_animations[a[:anim_id]], true, a[:height] || 3)
        @t = 0.0
      end

      def place(scene)
        sx, sy = scene.camera.to_screen(*@at.call, 1.0)
        @sprite.x = sx.round
        @sprite.y = sy.round
      end

      def update(scene, lt, dt)
        place(scene)
        @sprite.update
        @t += dt
        return !@sprite.effect? || @t > 20
      end

      def dispose
        return if @sprite.disposed?
        @sprite.bitmap.dispose if @sprite.bitmap && !@sprite.bitmap.disposed?
        @sprite.dispose
      end
    end

    class Scene
      def on_map?; return @definition.options[:on_map] == true; end

      def op_pose(a, _dur)
        act = actor!(a[:id])
        if a[:frame] then act.set_frame(a[:frame])
        elsif a[:row] || a[:col] then act.cell = [a[:row] || 0, a[:col] || 0]
        else act.cell = nil
        end
        nil
      end

      def op_flipbook(a, dur)
        act = actor!(a[:id])
        frames = a[:frames].to_a
        holds = (a[:holds] || [a[:hold] || 0.1] * frames.length).map(&:to_f)
        total = holds.sum
        return nil if frames.empty? || total <= 0
        loops = a[:loops] || 1
        se = a[:se] || {}
        last = -1
        tween(dur, :linear) do |_, raw|
          t = (raw >= 1) ? (total * loops) - 0.0001 : raw * total * loops
          t %= total
          i = 0
          acc = 0.0
          i += 1 while i < frames.length - 1 && t >= (acc += holds[i])
          if i != last
            last = i
            act.set_frame(frames[i])
            Sound.play(:se, se[i]) if se[i] && raw < 1
          end
          act.set_frame(a[:end_frame]) if raw >= 1 && a[:end_frame]
        end
      end

      def op_still(a, dur); return Still.new(self, a, dur); end

      def op_pulse(a, dur)
        from = @tone.dup
        to = (a[:tone] || Util.rgb(a[:color] || [255, 255, 255])[0, 3].map { |v| v - 128 } + [0]).map(&:to_f)
        to.push(0.0) while to.length < 4
        n = a[:times] || 1
        tween(dur * n, :linear) do |_, raw|
          ph = (raw * n) % 1.0
          k = (raw >= 1) ? 0.0 : 1.0 - ((ph * 2) - 1).abs           # up and back each time
          @tone = [0, 1, 2, 3].map { |i| Util.lerp(from[i], to[i], k) }
        end
      end

      # Camera tracks an actor with exponential smoothing (Rejuvenation's camera follow).
      def op_follow(a, _dur)
        @effects.reject! { |e| e.id == :__follow }
        stop_camera_moves
        return nil if a[:off]
        act = actor!(a[:id])
        smooth = (a[:smooth] || 0.15).to_f
        off = a[:offset] || [0, 0]
        eff = Class.new(Effect) {
          define_method(:update) do |scene, _lt, dt|
            return true if !scene.actors.value?(act)
            tx, ty = act.center
            k = 1 - ((1 - smooth)**(dt * 60))          # frame-rate independent smoothing
            scene.camera.x += (tx + off[0] - scene.camera.x) * k
            scene.camera.y += (ty + off[1] - scene.camera.y) * k
            false
          end
        }.new
        run_effect(eff, @time, :__follow)
        nil
      end

      def op_anim(a, _dur)
        if !defined?(RPG::Sprite) || !defined?($data_animations) || !$data_animations || !$data_animations[a[:anim_id]]
          Util.log("anim #{a[:anim_id]}: no database animation available here")
          return nil
        end
        return DbAnim.new(self, a)
      end
    end

    class Builder
      def pose(id, **o); add(:pose, o.merge(:id => ref(id))); end

      def flipbook(id, **o)
        n = o[:frames].to_a.length
        holds = o[:holds] || [o[:hold] || 0.1] * n
        add(:flipbook, o.merge(:id => ref(id)), o[:duration] || (holds.sum * (o[:loops] || 1)))
      end

      def still(image, **o)
        add(:still, o.merge(:image => image), o[:duration] || 3.0, true)
      end

      def pulse(**o); add(:pulse, o, (o[:duration] || 0.15) * (o[:times] || 1)); end
      def follow(id = nil, **o); add(:follow, (o[:off]) ? o : o.merge(:id => ref(id))); end

      # One-shot effect sheet: declares a temporary actor, plays it once, removes it.
      def play_sheet(path, at:, frames: nil, grid: [5, 1], hold: 0.05, holds: nil, blend: :add, scale: 1, px: 1, z: nil, wait: false, **o)
        @auto_fx = (@auto_fx || 0) + 1
        id = :"__fx#{@auto_fx}"
        frames ||= (0...(grid[0] * grid[1]))
        list = frames.to_a
        holds ||= [hold] * list.length
        start = now
        actor id, sheet: path, grid: grid, at: at, frame: list.first, blend: blend, scale: scale, px: px, z: z, **o
        flipbook id, frames: list, holds: holds
        at(start + holds.sum) { remove id }
        wait(holds.sum) if wait
        return id
      end
      def anim(id, **o); add(:anim, check_points(o).merge(:anim_id => id)); end
    end
  end
end
