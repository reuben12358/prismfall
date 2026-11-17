#===============================================================================
# Prismfall EBDX Bridge - EBDX battle room integration
#-------------------------------------------------------------------------------
# Verified against Manurocker95's EBDX v1.4.7.1 (E21):
#   Battle::Scene#loadBackdrop builds @sprites["battlebg"] = BattleSceneRoom
#   BattleSceneRoom#reconfigure(data, transition) rebuilds the room; transition
#     is a Color (fade the backdrop through it), nil (instant) or a common
#     animation Symbol (the animation calls room.configure itself)
#   BattleSceneRoom#refresh(Hash) disposes and redraws every room sprite and
#     ignores keys it doesn't know, so "prismfall_*" keys ride along in @data
#   BattleSceneRoom#position places every @sprites entry from .ex/.ey/.param
#     (room-image coordinates) using the camera vector, and defocus/focus
#     shift all of them by -/+100 z during move animations.
#===============================================================================
module PrismfallEBDX
  module EBDX
    module_function

    # Called right after EBDX built the default room for this battle.
    def apply_initial(scene, battle)
      room = PrismfallEBDX.ebdx_room(scene)
      return if !room
      sig = PrismfallEBDX.signature(battle)
      id = PrismfallEBDX.current_field(battle)
      if id == :NONE || (RESPECT_SCRIPTED_BACKDROP && !EliteBattle.get(:nextBattleBack).nil?)
        room.prismfall_signature = sig   # so the battle-start event doesn't swap it
        return
      end
      data = PrismfallEBDX.room_data(id, PrismfallEBDX.current_stage(battle))
      return if !data
      room.reconfigure(data, nil)       # instant; room's @backup keeps the map default
      room.prismfall_signature = sig
    rescue StandardError => e
      PrismfallEBDX.log_error("EBDX.apply_initial", e)
    end

    # Live change (also stage changes, where old_id == new_id).
    def swap(scene, battle, old_id, new_id)
      room = PrismfallEBDX.ebdx_room(scene)
      return if !room
      sig = PrismfallEBDX.signature(battle)
      return if room.prismfall_signature == sig
      id = PrismfallEBDX.current_field(battle)
      if id == :NONE
        data = PrismfallEBDX.deep_dup(room.prismfall_default_data || {})
        data = PrismfallEBDX.fallback_room(nil) if data.empty?
      else
        data = PrismfallEBDX.room_data(id, PrismfallEBDX.current_stage(battle))
      end
      return if !data
      room.prismfall_overlay_specs = nil   # a new field restarts any borrowing overlay
      trans = LIVE_TRANSITIONS ? PrismfallEBDX.transition_for(old_id, id) : nil
      if trans.is_a?(Symbol)
        room.reconfigure(data, trans)
        room.configure                      # no-op if the animation already applied it
      elsif trans.is_a?(Array)
        room.reconfigure(data, PrismfallEBDX.to_color(trans))
      else
        room.reconfigure(data, nil)
      end
      room.prismfall_signature = sig
      PrismfallEBDX.log("Room swapped to #{sig.inspect}")
    end
  end
end

#===============================================================================
# Hooks (only when EBDX is loaded)
#===============================================================================
if defined?(BattleSceneRoom) && defined?(EliteBattle)

  class Battle::Scene
    alias prismfall_ebdx_loadBackdrop loadBackdrop unless method_defined?(:prismfall_ebdx_loadBackdrop)
    def loadBackdrop
      prismfall_ebdx_loadBackdrop
      PrismfallEBDX::EBDX.apply_initial(self, @battle) if PrismfallEBDX::ENABLED
    end
  end

  class BattleSceneRoom
    attr_accessor :prismfall_signature
    attr_accessor :prismfall_overlay_specs

    # Room data EBDX built before any field was applied (map/trainer default).
    def prismfall_default_data
      return @backup
    end

    #---------------------------------------------------------------------------
    # Redraw: after EBDX rebuilt the room, apply our tone and particle layers.
    #---------------------------------------------------------------------------
    alias prismfall_ebdx_refresh refresh unless method_defined?(:prismfall_ebdx_refresh)
    def refresh(*args)
      prismfall_ebdx_refresh(*args)
      return if !args[0].is_a?(Hash)
      begin
        prismfall_apply_tone
        @pf_particles = []
        @pf_flash = nil
        # Created at base z like EBDX's own sprites; reconfigure's defocus/focus
        # then shifts them together with the rest of the room.
        prismfall_spawn_art_layers(@data["prismfall_layers"]) if PrismfallEBDX::AMBIENT_LAYERS
        prismfall_spawn_layer(@data["prismfall_fx"], "pfx", false) if PrismfallEBDX::AMBIENT_FX
        prismfall_spawn_layer(@prismfall_overlay_specs, "pfo", false) if PrismfallEBDX::AMBIENT_FX
      rescue StandardError => e
        @pf_particles = nil
        PrismfallEBDX.log_error("BattleSceneRoom#refresh", e)
      end
    end

    alias prismfall_ebdx_update update unless method_defined?(:prismfall_ebdx_update)
    def update
      if @pf_particles && !self.disposed?
        begin
          prismfall_update_fx
        rescue StandardError => e
          @pf_particles = nil   # disable FX for this room rather than spam errors
          PrismfallEBDX.log_error("BattleSceneRoom#update", e)
        end
      end
      prismfall_ebdx_update
    end

    #---------------------------------------------------------------------------
    # Public: replace the borrowed-field particle layer without a rebuild.
    #---------------------------------------------------------------------------
    def prismfall_set_overlay_fx(specs)
      return if self.disposed?
      @prismfall_overlay_specs = specs
      @pf_particles ||= []
      @pf_particles.reject! { |p| p[:key].start_with?("pfo") }
      @sprites.keys.select { |k| k.start_with?("pfo") }.each do |k|
        @sprites[k].dispose if !@sprites[k].disposed?
        @sprites.delete(k)
      end
      prismfall_spawn_layer(specs, "pfo", true) if PrismfallEBDX::AMBIENT_FX
    end

    # Public: brief colour flash of the backdrop image.
    def prismfall_flash(rgb, alpha = 150, decay = 16)
      @pf_flash_now = { :rgb => rgb, :alpha => alpha.to_f, :decay => decay.to_f }
    end

    #---------------------------------------------------------------------------
    # Internals
    #---------------------------------------------------------------------------
    def prismfall_apply_tone
      t = @data["prismfall_tone"]
      return if !t.is_a?(Array)
      @sprites.each do |key, spr|
        next if key.start_with?("pf") || !spr || spr.disposed?
        old = spr.tone
        spr.tone = Tone.new(old.red + (t[0] || 0), old.green + (t[1] || 0),
                            old.blue + (t[2] || 0), old.gray + (t[3] || 0))
      end
    end

    def prismfall_area(spec)
      a = spec[:area]
      return a if a.is_a?(Array) && a.length == 4
      bmp = @sprites["bg"]&.bitmap
      return [0, 0, (bmp ? bmp.width : 384), (bmp ? bmp.height : 308)]
    end

    def prismfall_rand(range, default)
      r = range || default
      return r.to_f if r.is_a?(Numeric)
      return r[0] + (rand * (r[1] - r[0]))
    end

    def prismfall_spawn_layer(specs, prefix, focus_offset)
      return if !specs.is_a?(Array) || !@sprites["bg"] || !@sprites["bg"].bitmap
      @pf_particles ||= []
      budget = PrismfallEBDX::MAX_PARTICLES - @pf_particles.length
      specs.each_with_index do |spec, si|
        next if !spec.is_a?(Hash)
        if spec[:type] == :flash
          @pf_flash = spec.merge(:timer => prismfall_rand(spec[:interval], [120, 240]))
          next
        end
        count = ((spec[:count] || 12) * PrismfallEBDX::FX_DENSITY).round
        count.times do |i|
          break if budget <= 0
          key = "#{prefix}#{si}_#{i}"
          spr = Sprite.new(@viewport)
          spr.default!
          spr.bitmap = PrismfallEBDX.particle_bitmap(spec)
          spr.ox = spr.bitmap.width / 2
          spr.oy = spr.bitmap.height / 2
          spr.blend_type = spec[:blend] || 0
          if spec[:colors].is_a?(Array) && !spec[:colors].empty?
            spr.color = PrismfallEBDX.to_color(spec[:colors][rand(spec[:colors].length)], 255)
          end
          @sprites[key] = spr
          p = { :key => key, :spec => spec }
          prismfall_respawn(p, true, focus_offset)
          @pf_particles.push(p)
          budget -= 1
        end
      end
    end

    def prismfall_respawn(p, initial, focus_offset = true)
      spec = p[:spec]
      spr = @sprites[p[:key]]
      x1, y1, x2, y2 = prismfall_area(spec)
      zr = spec[:zoom] || [0.5, 1.0]
      spr.param = prismfall_rand(zr, [0.5, 1.0])
      p[:param0] = spr.param
      layers = spec[:layers] || [:mid]
      lz = PrismfallEBDX::LAYER_Z[layers[rand(layers.length)]] || [12, 19]
      spr.z = lz[0] + rand(lz[1] - lz[0] + 1) - ((focus_offset && !@focused) ? 100 : 0)
      p[:speed] = prismfall_rand(spec[:speed], [0.5, 1.5])
      p[:phase] = rand * 2 * Math::PI
      p[:peak]  = prismfall_rand(spec[:opacity], [200, 255])
      p[:spin]  = spec[:spin] ? (rand * spec[:spin] * 2) - spec[:spin] : 0
      w = x2 - x1
      h = y2 - y1
      case spec[:type]
      when :rise
        spr.ex = x1 + rand * w
        spr.ey = initial ? y1 + rand * h : y2 + rand(16)
      when :fall
        spr.ex = x1 + rand * w
        spr.ey = initial ? y1 + rand * h : y1 - rand(24)
      when :drift
        p[:dir] = spec[:dir] || (rand(2) == 0 ? 1 : -1)
        spr.ex = initial ? x1 + rand * w : (p[:dir] > 0 ? x1 - rand(24) : x2 + rand(24))
        spr.ey = y1 + rand * h
      when :twinkle
        spr.ex = x1 + rand * w
        spr.ey = y1 + rand * h
        p[:toggle] = 1
        spr.opacity = initial ? rand(p[:peak].to_i + 1) : 0
      when :streak
        ang = (spec[:angle] || 100) * Math::PI / 180.0
        p[:vx] = Math.cos(ang)
        p[:vy] = Math.sin(ang)
        spr.angle = -(spec[:angle] || 100)
        if initial
          spr.ex = x1 + rand * w
          spr.ey = y1 + rand * h
        elsif p[:vy].abs > 0.3   # mostly vertical: enter from the top/bottom edge
          spr.ex = x1 - 60 + rand * (w + 120)
          spr.ey = p[:vy] > 0 ? y1 - rand(40) : y2 + rand(40)
        else                     # mostly horizontal: enter from the side
          spr.ex = p[:vx] > 0 ? x1 - rand(60) : x2 + rand(60)
          spr.ey = y1 + rand * h
        end
      end
      p[:base_x] = spr.ex
      p[:base_y] = spr.ey
      spr.opacity = 0 if !initial && spec[:type] != :twinkle
    end

    # Opacity envelope: fade in over the first 15% of the path, out over the last 30%.
    def prismfall_envelope(progress, peak)
      return 0 if progress <= 0 || progress >= 1
      return peak * progress / 0.15 if progress < 0.15
      return peak * (1 - progress) / 0.3 if progress > 0.7
      return peak
    end

    #---------------------------------------------------------------------------
    # Animated art layers (profile :layers, see 001_Bridge_Config.rb). One sprite
    # each in the room's own hash, so EBDX's camera/zoom/focus code moves them.
    #---------------------------------------------------------------------------
    def prismfall_spawn_art_layers(specs)
      @pf_layers = []
      return if !specs.is_a?(Array)
      inv = 1.0 / PrismfallEBDX.room_scale
      specs.each_with_index do |spec, i|
        next if !spec.is_a?(Hash) || !spec[:bitmap]
        key = "pfl#{i}"
        spr = Sprite.new(@viewport)
        spr.default!
        bmp = pbBitmap(PrismfallEBDX::EBDX_ELEMENTS + spec[:bitmap].to_s)
        spr.bitmap = bmp
        frames = [(spec[:frames] || 1).to_i, 1].max
        fw = bmp.width / frames
        spr.src_rect.set(0, 0, fw, bmp.height) if frames > 1
        spr.ox = spec[:ox] || (fw / 2)
        spr.oy = spec[:oy] || (bmp.height / 2)
        spr.ex = spec[:x] || 0
        spr.ey = spec[:y] || 0
        spr.z = spec[:z] || 1
        spr.param = (spec[:hd] ? inv : 1.0) * (spec[:zoom] || 1.0)
        spr.blend_type = spec[:blend] || 0
        spr.opacity = spec[:opacity] || 255
        spr.mirror = true if spec[:mirror]
        spr.angle = spec[:angle] if spec[:angle]
        @sprites[key] = spr
        @pf_layers.push({ :key => key, :spec => spec, :t => (spec[:phase_frames] || rand(1000)).to_f,
                          :frames => frames, :fw => fw, :base_x => spr.ex, :base_y => spr.ey, :fl => 0 })
      end
    end

    def prismfall_update_art_layers(d)
      return if !@pf_layers
      @pf_layers.each do |l|
        spr = @sprites[l[:key]]
        next if !spr || spr.disposed?
        s = l[:spec]
        l[:t] += 1.0 / d
        t = l[:t]
        per = (s[:period] || 120).to_f
        w = t * 2 * Math::PI / per + (s[:phase] || 0)
        base_o = (s[:opacity] || 255).to_f
        o = base_o
        anims = s[:anim].is_a?(Array) ? s[:anim] : [s[:anim]]
        anims.each do |a|
          case a
          when :pulse    # smooth glow breathing between :min and :max opacity
            lo = (s[:min] || (base_o * 0.5)).to_f
            hi = (s[:max] || base_o).to_f
            o = lo + ((hi - lo) * (0.5 + (0.5 * Math.sin(w))))
          when :flicker  # random dropouts (broken lamps, buzzing neon)
            if l[:fl] > 0
              l[:fl] -= 1.0 / d
              o = (s[:min] || 0).to_f
            elsif rand < (s[:chance] || 0.02) / d
              l[:fl] = 1 + rand((s[:dropout] || 6).to_i)
              o = (s[:min] || 0).to_f
            end
          when :sway     # pendulum around the anchor (chains, banners, lamps)
            spr.angle = (s[:angle] || 0) + ((s[:amp] || 4) * Math.sin(w))
          when :rotate   # continuous spin (gears, rings)
            spr.angle += (s[:speed] || 0.5) / d
          when :bob      # vertical float
            spr.ey = l[:base_y] + ((s[:amp] || 2) * Math.sin(w))
          when :drift    # horizontal float
            spr.ex = l[:base_x] + ((s[:amp] || 6) * Math.sin(w))
          end
        end
        spr.opacity = o
        if l[:frames] > 1
          f = (t / (s[:frame_time] || 8).to_f).to_i % l[:frames]
          spr.src_rect.x = f * l[:fw]
        end
      end
    end

    def prismfall_update_fx
      d = self.delta
      d = 1.0 if d <= 0
      prismfall_update_art_layers(d)
      @pf_particles.each do |p|
        spr = @sprites[p[:key]]
        next if !spr || spr.disposed?
        spec = p[:spec]
        x1, y1, x2, y2 = prismfall_area(spec)
        sway = spec[:sway] || 0
        case spec[:type]
        when :rise
          spr.ey -= p[:speed] / d
          spr.ex = p[:base_x] + (sway * Math.sin(p[:phase] + (spr.ey * 0.05)))
          spr.opacity = prismfall_envelope((y2 - spr.ey) / (y2 - y1).to_f, p[:peak])
          prismfall_respawn(p, false) if spr.ey < y1
        when :fall
          spr.ey += p[:speed] / d
          spr.ex = p[:base_x] + (sway * Math.sin(p[:phase] + (spr.ey * 0.05)))
          spr.opacity = prismfall_envelope((spr.ey - y1) / (y2 - y1).to_f, p[:peak])
          prismfall_respawn(p, false) if spr.ey > y2
        when :drift
          spr.ex += p[:dir] * p[:speed] / d
          spr.ey = p[:base_y] + (sway * Math.sin(p[:phase] + (spr.ex * 0.04)))
          prog = (spr.ex - x1) / (x2 - x1).to_f
          prog = 1 - prog if p[:dir] < 0
          spr.opacity = prismfall_envelope(prog, p[:peak])
          prismfall_respawn(p, false) if spr.ex < x1 - 30 || spr.ex > x2 + 30
        when :twinkle
          spr.opacity += p[:toggle] * p[:speed] / d
          p[:toggle] = -1 if spr.opacity >= p[:peak]
          if spr.opacity <= 0 && p[:toggle] < 0
            p[:toggle] = 1
            prismfall_respawn(p, false) if rand(3) == 0
          end
        when :streak
          spr.ex += p[:vx] * p[:speed] / d
          spr.ey += p[:vy] * p[:speed] / d
          spr.opacity = p[:peak]
          prismfall_respawn(p, false) if spr.ey > y2 + 40 || spr.ey < y1 - 50 ||
                                         spr.ex > x2 + 70 || spr.ex < x1 - 70
        end
        spr.angle += p[:spin] / d if p[:spin] != 0 && spec[:type] != :streak
        if spec[:grow] && [:rise, :fall].include?(spec[:type])   # puffs swell as they rise
          prog = spec[:type] == :rise ? (y2 - spr.ey) / (y2 - y1).to_f : (spr.ey - y1) / (y2 - y1).to_f
          spr.param = p[:param0] * (1 + (spec[:grow] * [[prog, 0].max, 1].min)) if p[:param0]
        end
      end
      prismfall_update_flash(d)
    end

    def prismfall_update_flash(d)
      bg = @sprites["bg"]
      return if !bg || bg.disposed?
      if @pf_flash
        @pf_flash[:timer] -= 1.0 / d
        if @pf_flash[:timer] <= 0
          @pf_flash[:timer] = prismfall_rand(@pf_flash[:interval], [120, 240])
          @pf_flash_now = { :rgb => @pf_flash[:color] || [255, 255, 255], :alpha => (@pf_flash[:alpha] || 120).to_f,
                            :decay => (@pf_flash[:decay] || 12).to_f, :echo => @pf_flash[:double] }
        end
      end
      return if !@pf_flash_now
      f = @pf_flash_now
      bg.color = PrismfallEBDX.to_color(f[:rgb], [[f[:alpha], 0].max, 255].min.to_i)
      f[:alpha] -= f[:decay] / d
      if f[:echo] && f[:alpha] < 40
        f[:alpha] = 140
        f[:echo] = false
      end
      return if f[:alpha] > 0
      bg.color = Color.new(0, 0, 0, 0)
      @pf_flash_now = nil
    end
  end

end
