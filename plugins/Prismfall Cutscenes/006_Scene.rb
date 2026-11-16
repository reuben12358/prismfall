#===============================================================================
# Prismfall Cutscenes - 006 The player: scene, camera, layers, timeline
#-------------------------------------------------------------------------------
# Timing is frame-rate independent: the scene clock advances by real elapsed
# time (System.uptime, as core v21.1 animations do) and every effect is a
# function of its own local time, so 30, 60 or 144 FPS show the same scene.
#===============================================================================
module Prismfall
  module Cutscene
    class Camera
      attr_accessor :x, :y, :zoom, :sx, :sy

      def initialize(w, h)
        @hx = w / 2.0
        @hy = h / 2.0
        @x = @hx
        @y = @hy
        @zoom = 1.0
        @sx = @sy = 0.0
      end

      def zoom_for(parallax); return 1.0 + ((@zoom - 1.0) * parallax); end

      # World -> screen for a layer of the given parallax (floats).
      def to_screen(wx, wy, parallax = 1.0)
        z = zoom_for(parallax)
        cx = @hx + ((@x - @hx) * parallax)
        cy = @hy + ((@y - @hy) * parallax)
        return ((wx - cx) * z) + @hx + (@sx * parallax), ((wy - cy) * z) + @hy + (@sy * parallax)
      end
    end

    class Layer
      attr_accessor :opacity

      def initialize(scene, spec, z)
        @bitmap   = spec[:bitmap]
        @px       = spec[:px]
        @parallax = spec[:parallax]
        @scroll   = spec[:scroll].to_f
        @x        = spec[:x].to_f
        @y        = spec[:y].to_f
        @tile     = spec[:tile]
        @opacity  = spec[:opacity]
        @off      = 0.0
        @sprites  = Array.new((@tile) ? 3 : 1) do
          s = Sprite.new(scene.viewport)
          s.bitmap = @bitmap
          s.z = z
          s
        end
      end

      def update(scene, dt)
        @off += @scroll * dt
        cam = scene.camera
        z = cam.zoom_for(@parallax)
        sx, sy = cam.to_screen(@x + @off, @y, @parallax)
        zoom = @px * z
        tw = @bitmap.width * zoom
        sx = (sx % tw) - tw if @tile
        if z == 1.0
          sx = Util.snap(sx)
          sy = Util.snap(sy)
        end
        @sprites.each_with_index do |s, i|
          s.x = (sx + (i * tw)).round
          s.y = sy.round
          s.zoom_x = s.zoom_y = zoom
          s.opacity = @opacity
        end
      end

      def dispose
        @sprites.each { |s| s.dispose if !s.disposed? }
        @bitmap.dispose if !@bitmap.disposed?
      end
    end

    #---------------------------------------------------------------------------
    # Effects: anything that lives for a while on the timeline.
    #---------------------------------------------------------------------------
    class Effect
      attr_accessor :t0, :id

      def update(scene, lt, dt); return true; end   # true = finished
      def draws?; return false; end
      def draw(scene, back, front); end
      def dispose; end
    end

    class Tween < Effect
      def initialize(dur, ease, &block)
        @dur = dur
        @ease = ease || :in_out
        @block = block
      end

      def update(scene, lt, dt)
        raw = (@dur <= 0) ? 1.0 : Util.clamp(lt / @dur, 0.0, 1.0)
        @block.call(Ease.apply(@ease, raw), raw)
        return raw >= 1.0
      end
    end

    class Scene
      Z_FX_BACK = 400
      Z_FX_FRONT = 2000
      Z_FROST = 2100
      Z_BARS = 100
      Z_TEXT = 200
      Z_CARD = 300
      Z_FLASH = 500
      Z_CURTAIN = 600
      Z_SKIP = 700

      attr_reader :viewport, :ui, :w, :h, :vw, :vh, :camera, :actors, :armies, :particles,
                  :results, :time, :fx_frame, :rng, :definition, :effects
      attr_accessor :curtain

      def initialize(definition)
        @definition = definition
        @w  = Graphics.width
        @h  = Graphics.height
        @vw = @w / PX
        @vh = @h / PX
        @results = {}
        @rng = Random.new(definition.id.to_s.sum + 7)
      end

      #-------------------------------------------------------------------------
      # Main loop
      #-------------------------------------------------------------------------
      def play
        setup
        last = Util.now
        until @finished
          Graphics.update
          Input.update
          now = Util.now
          update(Util.clamp(now - last, 0.0, MAX_DT))
          last = now
        end
        return (@skipped) ? :skipped : :done
      ensure
        dispose
      end

      def setup
        @viewport = Viewport.new(0, 0, @w, @h)
        @viewport.z = VIEWPORT_Z
        @ui = Viewport.new(0, 0, @w, @h)
        @ui.z = VIEWPORT_Z + 1
        @camera  = Camera.new(@w, @h)
        @layers  = []
        @actors  = {}
        @armies  = {}
        @effects = []
        @emitters = {}
        @attached = {}
        @owned   = []     # extra sprites/bitmaps to dispose
        @particles = Particles.new(self)
        @time    = 0.0
        @next    = 0
        @fx_acc  = 0.0
        @fx_frame = 0
        @fx_dirty = false
        @tone    = [0.0, 0.0, 0.0, 0.0]
        @tone_obj = Tone.new(0, 0, 0, 0)
        @overlay = { :burning => 0.0, :freezing => 0.0 }
        @bar     = 0.0
        @curtain = 255.0
        @cut_blink = 0.0
        @skip_hold = 0.0
        @fx_back_bmp  = Bitmap.new(@vw, @vh)
        @fx_front_bmp = Bitmap.new(@vw, @vh)
        @fx_back  = fx_sprite(@fx_back_bmp, Z_FX_BACK)
        @fx_front = fx_sprite(@fx_front_bmp, Z_FX_FRONT)
        @bars = [solid([0, 0, 0], Z_BARS), solid([0, 0, 0], Z_BARS)]
        @flash_sprite = solid([255, 255, 255], Z_FLASH)
        @flash_sprite.opacity = 0
        @curtain_sprite = solid([0, 0, 0], Z_CURTAIN)
        @memo_bgm = @definition.uses?(:bgm) && @definition.options[:restore_bgm] != false
        $game_system.bgm_memorize if @memo_bgm && $game_system && $game_system.respond_to?(:bgm_memorize)
        run_effect(Tween.new(FADE_TIME, :linear) { |k, _| @curtain = 255.0 * (1 - k) }, 0.0)
      end

      def update(dt)
        @time += dt
        check_skip(dt)
        @camera.sx = @camera.sy = 0.0
        @actors.each_value { |a| a.off_x = a.off_y = 0.0 }
        events = @definition.events
        while !@ending && @next < events.length && events[@next].t <= @time
          ev = events[@next]
          @next += 1
          start_event(ev)
        end
        @effects.reject! do |e|
          done = e.update(self, @time - e.t0, dt)
          e.dispose if done
          done
        end
        @particles.update(dt)
        @layers.each { |l| l.update(self, dt) }
        @actors.each_value { |a| a.update(self, dt) }
        @armies.each_value { |a| a.update(self, dt) }
        @attached.each_value { |a| a.update(self, dt) }
        @fx_acc += dt
        if @fx_acc >= 1.0 / FX_FPS
          @fx_acc = (@fx_acc >= 2.0 / FX_FPS) ? 0.0 : @fx_acc - (1.0 / FX_FPS)
          @fx_frame += 1
          redraw_fx
        end
        update_screen(dt)
        if !@ending && @time >= @definition.length
          begin_ending(FADE_TIME)
        elsif @ending && @time >= @end_at
          @finished = true
        end
      end

      def begin_ending(fade)
        @ending = true
        from = @curtain
        @end_at = @time + ((from >= 255) ? 0.0 : fade)
        run_effect(Tween.new(fade, :linear) { |k, _| @curtain = from + ((255.0 - from) * k) }, @time)
      end

      def start_event(ev)
        eff = send("op_#{ev.op}", ev.args, ev.dur)
        run_effect(eff, ev.t, ev.args[:id]) if eff.is_a?(Effect)
      end

      def run_effect(eff, t0, id = nil)
        eff.t0 = t0
        eff.id = id
        @effects.push(eff)
        return eff
      end

      def tween(dur, ease = nil, &block)
        if dur <= 0
          block.call(1.0, 1.0)
          return nil
        end
        return Tween.new(dur, ease, &block)
      end

      #-------------------------------------------------------------------------
      # Skipping (hold a button)
      #-------------------------------------------------------------------------
      def check_skip(dt)
        return if @ending || @definition.options[:skippable] == false
        held = SKIP_BUTTONS.any? { |b| Input.press?(Input.const_get(b)) }
        if !held
          @skip_hold = 0.0
          @skip_sprite.visible = false if @skip_sprite
          return
        end
        @skip_hold += dt
        show_skip_hint
        return if @skip_hold < SKIP_HOLD
        @skipped = true
        Sound.fade(:bgm, 0.3) if @definition.uses?(:bgm)
        @definition.events[@next..-1].each do |ev|
          ev.args[:proc].call(self) if ev.op == :call && ev.args[:always]
        end
        begin_ending(0.3)
      end

      def show_skip_hint
        if !@skip_sprite
          bmp = Bitmap.new(160, 28)
          TextDraw.font(bmp)
          TextDraw.outline(bmp, 0, 0, 160, 24, Util.tr("Skipping..."), Util.color(TEXT_COLOR), Util.color(TEXT_SHADOW), 2)
          @skip_sprite = Sprite.new(@ui)
          @skip_sprite.bitmap = bmp
          @skip_sprite.x = @w - 168
          @skip_sprite.y = 4
          @skip_sprite.z = Z_SKIP
          @owned.push(@skip_sprite)
        end
        @skip_sprite.visible = true
        @skip_sprite.opacity = 96 + (159 * Util.clamp(@skip_hold / SKIP_HOLD, 0, 1)).round
      end

      #-------------------------------------------------------------------------
      # Screen-level state
      #-------------------------------------------------------------------------
      def fx_sprite(bmp, z)
        s = Sprite.new(@viewport)
        s.bitmap = bmp
        s.zoom_x = s.zoom_y = PX
        s.z = z
        return s
      end

      def solid(rgb, z, viewport = nil)
        bmp = Bitmap.new(4, 4)
        bmp.fill_rect(0, 0, 4, 4, Util.color(rgb))
        s = Sprite.new(viewport || @ui)
        s.bitmap = bmp
        s.zoom_x = @w / 4.0
        s.zoom_y = @h / 4.0
        s.z = z
        @owned.push(s)
        return s
      end

      def update_screen(dt)
        @cut_blink -= dt if @cut_blink > 0
        @curtain_sprite.opacity = (@cut_blink > 0) ? 255 : @curtain.round
        bar = Util.snap(@bar)
        @bars[0].zoom_y = bar / 4.0
        @bars[1].zoom_y = bar / 4.0
        @bars[1].y = @h - bar
        @bars.each { |b| b.visible = bar > 0 }
        burn = @overlay[:burning]
        cold = @overlay[:freezing]
        @tone_obj.set(Util.clamp(@tone[0] + (burn * 40) - (cold * 16), -255, 255),
                      Util.clamp(@tone[1] + (burn * 6), -255, 255),
                      Util.clamp(@tone[2] - (burn * 24) + (cold * 36), -255, 255),
                      Util.clamp(@tone[3] + (cold * 40), 0, 255))
        @viewport.tone = @tone_obj
      end

      def bar_height; return @bar; end

      def redraw_fx
        drawers = @effects.select(&:draws?)
        active = !drawers.empty? || @particles.count > 0 || @overlay[:burning] > 0
        if @fx_dirty
          @fx_back_bmp.clear
          @fx_front_bmp.clear
          @fx_dirty = false
        end
        update_frost
        return if !active
        drawers.each { |e| e.draw(self, @fx_back_bmp, @fx_front_bmp) }
        @particles.draw(@fx_back_bmp, @fx_front_bmp)
        draw_burning(@fx_front_bmp) if @overlay[:burning] > 0
        @fx_dirty = true
      end

      #-------------------------------------------------------------------------
      # Lookups
      #-------------------------------------------------------------------------
      def actor!(id)
        a = @actors[id]
        raise ArgumentError, "Cutscene #{@definition.id}: actor #{id.inspect} is not on stage" if !a
        return a
      end

      def army!(id)
        a = @armies[id]
        raise ArgumentError, "Cutscene #{@definition.id}: army #{id.inspect} is not on stage" if !a
        return a
      end

      # World point from [x, y], [x, y, w, h] (random inside), an actor id
      # (mouth), an army id (random soldier) or { actor:, part:, offset: }.
      def point(spec)
        case spec
        when Array
          return [spec[0] + (@rng.rand * spec[2]), spec[1] + (@rng.rand * spec[3])] if spec.length >= 4
          return [spec[0].to_f, spec[1].to_f]
        when Symbol
          return @actors[spec].mouth_point if @actors[spec]
          return @armies[spec].random_point(@rng) if @armies[spec]
          raise ArgumentError, "Cutscene #{@definition.id}: nothing called #{spec.inspect} is on stage"
        when Hash
          a = actor!(spec[:actor])
          base = case spec[:part]
                 when :feet   then a.pos
                 when :top    then a.top
                 when :center then a.center
                 else a.mouth_point
                 end
          off = spec[:offset] || [0, 0]
          return [base[0] + off[0], base[1] + off[1]]
        end
        return [@w / 2.0, @h / 2.0]
      end

      # A proc returning a world point; follows actors, fixed otherwise.
      def anchor(spec)
        return proc { point(spec) } if (spec.is_a?(Symbol) && @actors[spec]) || spec.is_a?(Hash)
        fixed = point(spec)
        return proc { fixed }
      end

      # World -> FX bitmap (art pixel) coordinates.
      def to_fx(pt)
        sx, sy = @camera.to_screen(pt[0], pt[1], 1.0)
        return (sx / PX).round, (sy / PX).round
      end

      def add_shake(power, dur, t0 = nil)
        run_effect(ShakeEffect.new(power, dur), t0 || @time)
      end

      def add_flash(color, dur, power = 255, t0 = nil)
        @flash_sprite.bitmap.fill_rect(0, 0, 4, 4, Util.color(color || [255, 255, 255]))
        run_effect(Tween.new(dur, :out) { |k, _| @flash_sprite.opacity = (power * (1 - k)).round }, t0 || @time)
      end

      # White flash + knock-back on an actor (dir: -1 left, 1 right).
      def hit_actor(id, dir = 0, power = 10, dur = 0.35, t0 = nil)
        a = @actors[id]
        return if !a
        base = a.tint.dup
        run_effect(Tween.new(dur, :out) { |k, raw|
          a.tint = (raw >= 1) ? base : [255.0, 255.0, 255.0, 255.0 * (1 - k)]
          a.off_x += dir * power * Math.sin(Math::PI * raw)
        }, t0 || @time)
      end

      #-------------------------------------------------------------------------
      # Ops: stage
      #-------------------------------------------------------------------------
      def op_background(a, _dur)
        Backdrop.build(a[:kind], a, self).each do |spec|
          @layers.push(Layer.new(self, spec, @layers.length))
        end
        nil
      end

      def op_clear_backgrounds(_a, _dur)
        @layers.each(&:dispose)
        @layers.clear
        nil
      end

      def op_actor(a, _dur)
        @actors[a[:id]].dispose if @actors[a[:id]]
        old_bar = @attached.delete(a[:id])
        old_bar.dispose if old_bar
        @actors[a[:id]] = Actor.new(self, a[:id], a)
        nil
      end

      def op_remove(a, _dur)
        act = @actors.delete(a[:id])
        act.dispose if act
        att = @attached.delete(a[:id])
        att.dispose if att
        nil
      end

      def target_pos(spec)
        return @actors[spec].pos if spec.is_a?(Symbol) && @actors[spec]
        return point(spec)
      end

      def op_move(a, dur)
        act = actor!(a[:id])
        x0, y0 = act.x, act.y
        x1, y1 = (a[:to]) ? target_pos(a[:to]) : [x0 + (a[:by] || [0, 0])[0], y0 + (a[:by] || [0, 0])[1]]
        arc = a[:arc] || 0
        act.walking = true if a[:walk]
        tween(dur, a[:ease]) do |k, raw|
          act.x = Util.lerp(x0, x1, k)
          act.y = Util.lerp(y0, y1, k)
          act.off_y -= arc * 4 * raw * (1 - raw)
          act.walking = false if a[:walk] && raw >= 1
        end
      end

      def op_scale(a, dur)
        act = actor!(a[:id])
        s0 = act.scale
        tween(dur, a[:ease]) { |k, _| act.scale = Util.lerp(s0, a[:to].to_f, k) }
      end

      def op_rotate(a, dur)
        act = actor!(a[:id])
        r0 = act.angle
        r1 = (a[:by]) ? r0 + a[:by] : a[:to].to_f
        tween(dur, a[:ease]) { |k, _| act.angle = Util.lerp(r0, r1, k) }
      end

      def op_fade(a, dur)
        act = actor!(a[:id])
        o0 = act.opacity
        tween(dur, a[:ease] || :linear) { |k, _| act.opacity = Util.lerp(o0, (a[:to] || 0).to_f, k) }
      end

      # tint :id, color: [r, g, b] or palette, amount: 0..255 (255 = silhouette)
      def op_tint(a, dur)
        act = actor!(a[:id])
        from = act.tint.dup
        c = Util.rgb(a[:color] || [255, 255, 255])
        to = [c[0].to_f, c[1].to_f, c[2].to_f, (a[:amount] || c[3] || 128).to_f]
        from[0, 3] = to[0, 3] if from[3] <= 0
        tween(dur, a[:ease] || :linear) { |k, _| act.tint = [0, 1, 2, 3].map { |i| Util.lerp(from[i], to[i], k) } }
      end

      def op_flip(a, _dur)
        act = actor!(a[:id])
        act.flip = (a[:value].nil?) ? !act.flip : a[:value]
        nil
      end

      def op_face(a, _dur)
        actor!(a[:id]).dir = a[:dir]
        nil
      end

      def op_hop(a, dur)
        act = actor!(a[:id])
        h = a[:height] || 12
        n = a[:times] || 1
        tween(dur, :linear) { |_, raw| act.off_y -= h * Math.sin(Math::PI * ((raw * n) % 1.0)).abs }
      end

      def op_tremble(a, dur)
        act = actor!(a[:id])
        p = a[:power] || PX
        tween(dur, :linear) { |_, _raw| act.off_x += (@fx_frame.even?) ? p : -p }
      end

      # lunge :id, toward: target, distance: px - dart forward and back.
      def op_lunge(a, dur)
        act = actor!(a[:id])
        tx, ty = (a[:toward]) ? target_pos(a[:toward]) : [act.x + ((act.flip) ? 60 : -60), act.y]
        dx = tx - act.x
        dy = ty - act.y
        len = Math.sqrt((dx * dx) + (dy * dy))
        len = 1.0 if len < 1
        dist = a[:distance] || [len - 40, 24].max
        hit_done = false
        tween(dur, :linear) do |_, raw|
          k = (raw < 0.4) ? Ease.apply(:in, raw / 0.4) : 1.0 - Ease.apply(:out, (raw - 0.4) / 0.6)
          act.off_x += dx / len * dist * k
          act.off_y += dy / len * dist * k
          if raw >= 0.4 && !hit_done
            hit_done = true
            if a[:toward].is_a?(Symbol) && @actors[a[:toward]] && a[:hit] != false
              hit_actor(a[:toward], (dx <=> 0), 10)
              burst_at(:sparks, @actors[a[:toward]].center, 10, a[:color] || :light)
              add_shake(a[:shake] || 4, 0.25)
              Sound.play(:se, a[:se] || :impact)
            end
          end
        end
      end

      def op_hit(a, dur)
        hit_actor(a[:id], a[:dir] || 0, a[:power] || 10, dur)
        nil
      end

      def op_faint(a, dur)
        act = actor!(a[:id])
        o0 = act.opacity
        y0 = act.y
        Sound.play(:se, :faint) if a[:se] != false
        tween(dur, :in) do |k, _|
          act.y = y0 + (act.height * 0.35 * k)
          act.opacity = o0 * (1 - k)
        end
      end

      #-------------------------------------------------------------------------
      # Ops: camera and screen
      #-------------------------------------------------------------------------
      def camera_target(a)
        if a[:to] || a[:at]
          spec = a[:to] || a[:at]
          return @actors[spec].center if spec.is_a?(Symbol) && @actors[spec]
          return point(spec)
        end
        by = a[:by] || [0, 0]
        return [@camera.x + by[0], @camera.y + by[1]]
      end

      def op_camera(a, _dur)
        @camera.x, @camera.y = camera_target(a) if a[:at] || a[:to] || a[:by]
        @camera.zoom = quantize_zoom(a[:zoom]) if a[:zoom]
        nil
      end

      # Hard cut: instant camera move behind a two-frame black blink.
      def op_cut(a, _dur)
        op_camera(a, 0)
        @cut_blink = a[:blink] || 0.07
        nil
      end

      def op_pan(a, dur)
        x0, y0 = @camera.x, @camera.y
        x1, y1 = camera_target(a)
        z0 = @camera.zoom
        z1 = a[:zoom] || z0
        tween(dur, a[:ease] || :in_out) do |k, _|
          @camera.x = Util.lerp(x0, x1, k)
          @camera.y = Util.lerp(y0, y1, k)
          @camera.zoom = quantize_zoom(Util.lerp(z0, z1, k))
        end
      end

      def op_zoom(a, dur)
        z0 = @camera.zoom
        z1 = (a[:to] || 1.0).to_f
        tween(dur, a[:ease] || :in_out) { |k, _| @camera.zoom = quantize_zoom(Util.lerp(z0, z1, k)) }
      end

      # Zoom moves in 1/16 steps so sprites land on whole pixels more often.
      def quantize_zoom(z); return (z * 16).round / 16.0; end

      def op_shake(a, dur)
        return ShakeEffect.new(a[:power] || 6, dur, a[:decay] != false)
      end

      def op_flash(a, dur)
        add_flash(a[:color], dur, a[:power] || 255)
        nil
      end

      # tone to: [r, g, b, gray] - tints the world (not text or bars).
      def op_tone(a, dur)
        from = @tone.dup
        to = (a[:to] || [0, 0, 0, 0]).map(&:to_f)
        to.push(0.0) while to.length < 4
        tween(dur, a[:ease] || :linear) { |k, _| @tone = [0, 1, 2, 3].map { |i| Util.lerp(from[i], to[i], k) } }
      end

      def op_fade_out(a, dur)
        from = @curtain
        tween(dur, :linear) { |k, _| @curtain = Util.lerp(from, 255.0, k) }
      end

      def op_fade_in(a, dur)
        from = @curtain
        tween(dur, :linear) { |k, _| @curtain = Util.lerp(from, 0.0, k) }
      end

      def op_letterbox(a, dur)
        from = @bar
        to = (a[:on]) ? (a[:height] || 32).to_f : 0.0
        tween(dur, :out) { |k, _| @bar = Util.lerp(from, to, k) }
      end

      #-------------------------------------------------------------------------
      # Ops: audio and control
      #-------------------------------------------------------------------------
      def op_bgm(a, _dur); Sound.play(:bgm, a[:name], a[:volume], a[:pitch]); nil; end
      def op_bgs(a, _dur); @used_bgs = true; Sound.play(:bgs, a[:name], a[:volume], a[:pitch]); nil; end
      def op_se(a, _dur);  Sound.play(:se, a[:name], a[:volume], a[:pitch]); nil; end
      def op_me(a, _dur);  Sound.play(:me, a[:name], a[:volume], a[:pitch]); nil; end
      def op_cry(a, _dur); Sound.cry(a[:species], a[:volume] || 90, a[:pitch] || 100); nil; end
      def op_bgm_fade(a, _dur); Sound.fade(:bgm, a[:seconds]); nil; end
      def op_bgs_fade(a, _dur); Sound.fade(:bgs, a[:seconds]); nil; end

      def op_call(a, _dur)
        a[:proc].call(self)
        nil
      end

      #-------------------------------------------------------------------------
      # Teardown
      #-------------------------------------------------------------------------
      def dispose
        return if @disposed || !@viewport
        @disposed = true
        (@effects || []).each { |e| e.dispose rescue nil }
        (@attached || {}).each_value(&:dispose)
        (@actors || {}).each_value(&:dispose)
        (@armies || {}).each_value(&:dispose)
        (@layers || []).each(&:dispose)
        (@owned || []).each do |o|
          next if o.disposed?
          o.bitmap.dispose if o.respond_to?(:bitmap) && o.bitmap && !o.bitmap.disposed?
          o.dispose
        end
        [@fx_back, @fx_front, @frost_sprite].compact.each { |s| s.dispose if !s.disposed? }
        [@fx_back_bmp, @fx_front_bmp, @frost_bmp].compact.each { |b| b.dispose if !b.disposed? }
        @viewport.dispose
        @ui.dispose
        Sound.fade(:bgs, 0.5) if @used_bgs
        if @memo_bgm && $game_system && $game_system.respond_to?(:bgm_restore)
          $game_system.bgm_restore
        end
      end

      # Fades the map back in after a scene (the scene itself ends on black).
      def self.fade_back(duration = 0.3)
        vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
        vp.z = VIEWPORT_Z + 2
        col = Color.new(0, 0, 0, 255)
        vp.color = col
        start = Util.now
        loop do
          k = Util.clamp((Util.now - start) / duration, 0.0, 1.0)
          col.set(0, 0, 0, 255 * (1 - k))
          vp.color = col
          Graphics.update
          Input.update
          pbUpdateSceneMap if defined?(pbUpdateSceneMap)
          break if k >= 1.0
        end
        vp.dispose
      end
    end

    class ShakeEffect < Effect
      def initialize(power, dur, decay = true)
        @power = power
        @dur = dur
        @decay = decay
      end

      def update(scene, lt, dt)
        raw = (@dur <= 0) ? 1.0 : Util.clamp(lt / @dur, 0.0, 1.0)
        amp = (@decay) ? @power * (1 - raw) : @power
        f = scene.fx_frame
        scene.camera.sx += Util.snap(((Util.hash01(f, 1) * 2) - 1) * amp)
        scene.camera.sy += Util.snap(((Util.hash01(f, 2) * 2) - 1) * amp)
        return raw >= 1.0
      end
    end
  end
end
