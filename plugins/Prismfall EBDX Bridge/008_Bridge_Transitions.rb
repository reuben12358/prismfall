#===============================================================================
# Prismfall EBDX Bridge - staged in-room transitions (STAGED_TRANSITIONS, 001)
#-------------------------------------------------------------------------------
# EBDX's live swap (BattleSceneRoom#reconfigure with a Color) fades a flat,
# screen-sized colour card over the whole room for 8 frames, rebuilds the room
# under it and fades the card out: for a moment the battlers float on nothing,
# then everything of the new room (glints, plumes, glow layers) pops in at once.
# A staged transition plays the change inside the room instead, as room layers
# (so EBDX's camera moves it with the room and the battlers stay on top):
#
#   0.00 s  impact      white-hot glow and a perspective heat ring at the base
#                       opposite the last move's user (the foe's base if no move)
#   0.2 s   front       the new room is revealed band by band (STAGED_ART bands,
#                       cut from an arrival-time map: fastest along water, then
#                       sand, rock; the sky last, as rising haze). Each band:
#                       a shimmer just ahead (preheat), then the glass under a
#                       white-hot leading edge and an amber body (ground only:
#                       the sky just turns), cooling through orange; steam puffs
#                       rise where the front crosses water. The old room's own
#                       animated layers and particles fade out as it is covered.
#   1.5 s   swap        the room is rebuilt under the finished reveal (identical
#                       pixels, so nothing pops); the new room's layers and
#                       particles fade in while the reveal layer fades away
#   0.5-1.8 s crackle   light runs out through the new glass, band by band
#   ~2.2 s  done        (the field's own message follows, as before)
#
# Times are at 60 fps and scale with Graphics.frame_rate. Any error falls back to
# an instant rebuild (logged), so a bad asset can never stall a battle.
#===============================================================================
module PrismfallEBDX
  STAGED_TIMING = {
    :band0      => 12,    # first band starts revealing (after the impact reads)
    :step       => 5.0,   # frames between bands
    :band_in    => 6,     # a band's fade-in
    :preheat    => 9,     # shimmer ahead of the band
    :cool       => 20,    # white-hot -> orange -> gone
    :crack_lag  => 16,    # crackle after the band
    :crack_life => 20,
    :glow       => 34,    # impact glow life
    :ring       => 30,    # heat ring life
    :old_out    => [10, 80],
    :swap_after => 7,     # frames after the last band starts
    :new_in     => [6, 40],   # after the swap
    :acc_out    => [12, 38],  # after the swap: the reveal layer fades, the new room's own layers show
    :puff_life  => 56,
    :max        => 150
  }
  WHITE_HOT = [255, 252, 236]
  COOL_MID  = [255, 140, 50]
  COOL_END  = [180, 60, 20]

  module_function

  def staged?(trans)
    return trans.is_a?(Symbol) && defined?(STAGED_TRANSITIONS) && STAGED_TRANSITIONS.key?(trans)
  end

  def staged_fallback(trans)
    return trans if !staged?(trans)
    return STAGED_TRANSITIONS[trans][:fallback] || [255, 255, 255]
  end

  # :foe = the impact is on the foe's base (the player's side used the move), :player = on the player's.
  def impact_side(battle)
    u = battle.respond_to?(:lastMoveUser) ? battle.lastMoveUser : -1
    return :foe if !u.is_a?(Integer) || u < 0
    return u.even? ? :foe : :player
  rescue StandardError
    return :foe
  end
end

if defined?(BattleSceneRoom) && defined?(EliteBattle)
  class BattleSceneRoom
    # Plays a staged transition into `data`. Returns false (nothing done) when the
    # transition's art doesn't fit the new room; the caller then uses the fallback fade.
    def prismfall_staged(data, name, impact = :foe)
      tr = PrismfallEBDX::STAGED_TRANSITIONS[name]
      set = tr && defined?(PrismfallEBDX::STAGED_ART) ? PrismfallEBDX::STAGED_ART[tr[:art]] : nil
      return false if !set || data["backdrop"].to_s != set[:art].to_s
      imp = set[:impacts][impact] || set[:impacts][:foe]
      impact = set[:impacts][impact] ? impact : :foe
      dir = set[:dir] + impact.to_s + "/"
      return false if !imp || !pbResolveBitmap(dir + "rv00") || !pbResolveBitmap(set[:dir] + "puff")
      @pftr = { :tr => tr, :set => set, :imp => imp, :dir => dir, :data => data, :swapped => false }
      begin
        prismfall_staged_run
      rescue StandardError => e
        PrismfallEBDX.log_error("BattleSceneRoom#prismfall_staged(#{name})", e)
        prismfall_staged_swap if !@pftr[:swapped]
      ensure
        prismfall_staged_cleanup
      end
      return true
    end

    #---------------------------------------------------------------------------
    def prismfall_staged_run
      t_ = PrismfallEBDX::STAGED_TIMING
      k = Graphics.frame_rate / 60.0
      f = ->(v) { (v * k).round }
      n = @pftr[:set][:bands]
      starts = (0...n).map { |i| f.call(t_[:band0] + i * t_[:step]) }
      swap_at = starts[-1] + f.call(t_[:swap_after])
      inv = 1.0 / PrismfallEBDX.room_scale
      @pftr_zoff = (@sprites["bg"] && @sprites["bg"].z < 0) ? -100 : 0
      @pftr_keys = []
      # the reveal layer: finished bands are blitted into one HD-canvas bitmap
      acc = prismfall_tr_canvas("pfimg_trA", Bitmap.new(864, 693), 5, inv)
      bands = Array.new(n)          # { :bmp, :rv, :glow, :lt, :done... }
      puffs = []
      tr = @pftr[:tr]
      imp = @pftr[:imp]
      steam = (tr[:steam] || 0).to_f
      # impact glow and heat ring (room-space, uniform zoom)
      glow = prismfall_tr_sprite("pftr_glow", @pftr[:set][:dir] + "glow", 6, imp[:point], 1)
      ring = prismfall_tr_sprite("pftr_ring", @pftr[:set][:dir] + "ring", 6, imp[:point], 1)
      puffbmp = pbBitmap(@pftr[:set][:dir] + "puff")
      old_fx = prismfall_tr_fx_keys
      old_imgs = prismfall_tr_img_levels
      new_fx = nil
      new_imgs = nil
      frame = 0
      last = f.call(t_[:max])
      loop do
        # ---- impact
        g = frame / f.call(t_[:glow]).to_f
        if g <= 1
          glow.param = inv * (0.3 + 1.2 * Math.sqrt(g))
          glow.opacity = g < 0.25 ? 255 : 255 * (1 - (g - 0.25) / 0.75)
        else
          glow.visible = false
        end
        r = frame / f.call(t_[:ring]).to_f
        if r <= 1
          ring.param = inv * (0.25 + 2.5 * (1 - (1 - r)**2))
          ring.opacity = 230 * (1 - r)
        else
          ring.visible = false
        end
        # ---- bands
        n.times do |i|
          s = frame - starts[i]
          b = bands[i]
          if !b && s >= -f.call(t_[:preheat]) - 2
            bmp = Bitmap.new(pbResolveBitmap(@pftr[:dir] + format("rv%02d", i)))
            b = bands[i] = { :bmp => bmp, :done => false }
            b[:rv] = prismfall_tr_canvas(format("pfimg_trR%02d", i), bmp, 5, inv)
            b[:rv].opacity = 0
            hk = Bitmap.new(pbResolveBitmap(@pftr[:dir] + format("hk%02d", i)))
            b[:glow] = prismfall_tr_canvas(format("pfimg_trG%02d", i), hk, 6, inv)
            b[:glow].blend_type = 1
            b[:glow].opacity = 0
          end
          next if !b
          pre = f.call(t_[:preheat])
          bin = f.call(t_[:band_in])
          cool = f.call(t_[:cool])
          if s < 0                                   # preheat: the ground just ahead of the front shimmers
            p = (s + pre) / pre.to_f
            if p > 0
              b[:glow].color = PrismfallEBDX.to_color(tr[:preheat] || PrismfallEBDX::WHITE_HOT, 255)
              b[:glow].opacity = 70 * p
              b[:glow].ex = (rand(3) - 1) * 0.45       # heat shimmer
            end
          elsif s < bin                              # the band turns to glass under its white-hot leading edge
            b[:glow].ex = 0
            b[:rv].opacity = 255 * (s + 1) / bin.to_f
            b[:glow].color = Color.new(0, 0, 0, 0)    # the heat image's own colours: white rim, amber body
            b[:glow].opacity = 255 * (s + 1) / bin.to_f
            if s == 0 && steam > 0
              (imp[:steam][i] || []).each do |pt|
                c = (steam * (1 + rand(2))).round
                c = 1 if c == 0 && rand < steam
                c.times { puffs.push(prismfall_tr_puff(puffbmp, pt, inv, frame + rand(4), puffs.length)) }
              end
            end
          elsif s < bin + cool                       # cooling: white -> orange -> dark glass
            if !b[:done]
              acc.bitmap.blt(0, 0, b[:bmp], b[:bmp].rect)
              b[:rv].visible = false
              b[:done] = true
            end
            c = (s - bin) / cool.to_f                # cooling: white-hot -> orange -> dull red -> gone
            col = c < 0.45 ? PrismfallEBDX::COOL_MID
                           : prismfall_tr_mix(PrismfallEBDX::COOL_MID, PrismfallEBDX::COOL_END, (c - 0.45) / 0.55)
            b[:glow].color = PrismfallEBDX.to_color(col, (255 * [c / 0.45, 1].min).to_i)
            b[:glow].opacity = 255 * (1 - c)**1.4
          elsif b[:glow].visible
            b[:glow].visible = false
          end
          # crackle of light through the new glass
          cs = s - f.call(t_[:crack_lag])
          if cs >= 0 && !b[:lt]
            lbmp = Bitmap.new(pbResolveBitmap(@pftr[:dir] + format("lt%02d", i)))
            b[:lt] = prismfall_tr_canvas(format("pfimg_trL%02d", i), lbmp, 7, inv)
            b[:lt].blend_type = 1
          end
          if b[:lt] && b[:lt].visible
            life = f.call(t_[:crack_life])
            if cs >= life
              b[:lt].visible = false
            else
              q = cs / life.to_f
              b[:lt].opacity = (q < 0.15 ? 255 : 255 * (1 - q)**1.3) * (0.75 + rand * 0.25)
            end
          end
        end
        # ---- steam puffs
        puffs.each { |p| prismfall_tr_update_puff(p, frame, inv, f.call(t_[:puff_life])) }
        # ---- the old room's own animated layers and particles fade as it is covered
        o0, o1 = t_[:old_out].map { |v| f.call(v) }
        if !@pftr[:swapped] && frame >= o0
          v = 1 - [(frame - o0) / (o1 - o0).to_f, 1].min
          prismfall_tr_fade(v, old_fx, old_imgs)
        end
        # ---- swap under the finished reveal
        if frame == swap_at && !@pftr[:swapped]
          bands.each { |b| next if !b || b[:done]; acc.bitmap.blt(0, 0, b[:bmp], b[:bmp].rect); b[:rv].visible = false; b[:done] = true }
          prismfall_staged_swap
          new_fx = prismfall_tr_fx_keys
          new_imgs = prismfall_tr_img_levels
          prismfall_tr_fade(0, new_fx, new_imgs)
        end
        if @pftr[:swapped]
          a = frame - swap_at
          n0, n1 = t_[:new_in].map { |v| f.call(v) }
          prismfall_tr_fade([[(a - n0) / (n1 - n0).to_f, 0].max, 1].min, new_fx, new_imgs) if a >= n0
          a0, a1 = t_[:acc_out].map { |v| f.call(v) }
          acc.opacity = 255 * (1 - [[(a - a0) / (a1 - a0).to_f, 0].max, 1].min)
        end
        frame += 1
        busy = !@pftr[:swapped] || acc.opacity > 0 || puffs.any? { |p| p[:spr].visible } ||
               bands.any? { |b| b && ((b[:glow] && b[:glow].visible) || !b[:lt] || b[:lt].visible) }
        break if !busy || frame > last
        @scene.wait
      end
      prismfall_tr_fade(1, new_fx, new_imgs) if new_fx
    end

    # Rebuild the room for the new field without disposing the transition's own sprites.
    def prismfall_staged_swap
      mine = {}
      @sprites.keys.each { |k| mine[k] = @sprites.delete(k) if k.start_with?("pfimg_tr", "pftr_") }
      data = @pftr[:data]
      @data = data.clone
      self.refresh(data)
      mine.each do |k, s|
        @sprites[k] = s
        @data[k] = { :flat => true } if k.include?("img")
      end
      @pftr[:swapped] = true
    end

    def prismfall_staged_cleanup
      (@sprites.keys.select { |k| k.start_with?("pfimg_tr", "pftr_") }).each do |k|
        s = @sprites.delete(k)
        @data.delete(k) if @data
        next if !s || s.disposed?
        s.bitmap.dispose if s.bitmap && !s.bitmap.disposed? && !k.start_with?("pftr_p")   # puffs share one bitmap
        s.dispose
      end
      @pf_fade = nil
      @pftr = nil
    end

    #---------------------------------------------------------------------------
    # helpers
    #---------------------------------------------------------------------------
    # HD-canvas layer drawn exactly over the room (a flat "img" key: EBDX zooms it with the room on both axes).
    def prismfall_tr_canvas(key, bmp, z, inv)
      spr = Sprite.new(@viewport)
      spr.default!
      spr.bitmap = bmp
      spr.ox = 0; spr.oy = 0; spr.ex = 0; spr.ey = 0
      spr.zx = inv; spr.zy = inv
      spr.z = z + @pftr_zoff
      @sprites[key] = spr
      @data[key] = { :flat => true }
      return spr
    end

    def prismfall_tr_sprite(key, path, z, pt, blend)
      spr = Sprite.new(@viewport)
      spr.default!
      spr.bitmap = Bitmap.new(pbResolveBitmap(path))
      spr.ox = spr.bitmap.width / 2
      spr.oy = spr.bitmap.height / 2
      spr.ex = pt[0]; spr.ey = pt[1]
      spr.z = z + @pftr_zoff
      spr.blend_type = blend
      spr.opacity = 0
      @sprites[key] = spr
      return spr
    end

    def prismfall_tr_puff(bmp, pt, inv, born, i)
      spr = Sprite.new(@viewport)
      spr.default!
      spr.bitmap = bmp
      cw = bmp.width / 3
      spr.src_rect.set(cw * rand(3), 0, cw, bmp.height)
      spr.ox = cw / 2
      spr.oy = bmp.height - 4
      spr.ex = pt[0] + rand(15) - 7
      spr.ey = pt[1] + rand(5) - 2
      front = spr.ey > 250                       # nearer than the player's base: in front of the player, fainter
      spr.z = (front ? 24 : 8) + @pftr_zoff
      spr.opacity = 0
      spr.mirror = rand(2) == 0
      @sprites["pftr_p#{i}"] = spr
      return { :spr => spr, :born => born, :y0 => spr.ey, :vy => 0.22 + rand * 0.25,
               :peak => front ? 95 : 150, :s0 => 1.0 + rand * 0.6 }
    end

    def prismfall_tr_update_puff(p, frame, inv, life)
      spr = p[:spr]
      return if !spr.visible
      a = frame - p[:born]
      return if a < 0
      if a >= life
        spr.visible = false
        return
      end
      q = a / life.to_f
      spr.ey = p[:y0] - p[:vy] * a
      spr.param = inv * p[:s0] * (1 + 1.3 * q)
      spr.opacity = q < 0.15 ? p[:peak] * q / 0.15 : p[:peak] * [(1 - q) / 0.6, 1].min
    end

    def prismfall_tr_mix(a, b, t)
      t = [[t, 0].max, 1].min
      return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]
    end

    # particle keys, each with a random threshold: a fade level v shows the particles with threshold < v
    def prismfall_tr_fx_keys
      return (@pf_particles || []).map { |p| [p[:key], rand * 0.98 + 0.01] }
    end

    # EBDX image layers drawn above the reveal layer (z > 5): their own opacity, to fade
    def prismfall_tr_img_levels
      out = {}
      @sprites.each do |k, s|
        next if k == "img000" || k.start_with?("pfimg_tr", "pftr_") || !k.include?("img") || !s || s.disposed?
        next if s.z - @pftr_zoff <= 5
        out[k] = s.opacity
      end
      return out
    end

    def prismfall_tr_fade(v, fx, imgs)
      @pf_fade = v
      (fx || []).each do |key, th|
        s = @sprites[key]
        s.visible = v > th if s && !s.disposed?
      end
      (imgs || {}).each do |key, o|
        s = @sprites[key]
        s.opacity = o * v if s && !s.disposed?
      end
    end
  end
end
