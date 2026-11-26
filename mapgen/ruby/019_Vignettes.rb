#===============================================================================
# Prismfall Maps - 019 drawn vignettes for things a map can't show at tile size (mapgen/ruby/019_Vignettes.rb)
#-------------------------------------------------------------------------------
# A framed pane over the map, drawn in code (no art file), faded in and out; the caller's next message box shows
# over it. Photosensitive mode needs nothing here (no flashes).
#   pfm_arena_model   185, the Spire lobby: the Prism Arena model under glass. A white bowl in a ring of mountains,
#                     a brass ring round its rim, eighteen slim pylons (09 #15 counts them: keep it at 18).
#===============================================================================
module PrismfallVignette
  module_function

  def pane(w, h)
    vp = Viewport.new((Graphics.width - w) / 2, 34, w, h)
    vp.z = 99990
    return vp
  end

  def fade(sprites, from, to, secs)
    t0 = System.uptime
    loop do
      k = [(System.uptime - t0) / secs, 1.0].min
      sprites.each { |s| s.opacity = (from + ((to - from) * k)).round }
      break if k >= 1.0
      Graphics.update
      Input.update
      pbUpdateSceneMap
    end
  end

  def hold(secs)
    t0 = System.uptime
    until System.uptime - t0 >= secs
      Graphics.update
      Input.update
      pbUpdateSceneMap
      break if Input.trigger?(Input::USE) && System.uptime - t0 > 0.6
    end
  end

  def ellipse(bmp, cx, cy, rx, ry, color, step = 1)
    (-ry..ry).step(step) do |dy|
      half = (rx * Math.sqrt([1.0 - ((dy.to_f / ry)**2), 0].max)).round
      bmp.fill_rect(cx - half, cy + dy, half * 2, step, color)
    end
  end

  def arena_model
    w = 352
    h = 196
    vp = pane(w, h)
    spr = Sprite.new(vp)
    spr.bitmap = Bitmap.new(w, h)
    b = spr.bitmap
    b.fill_rect(0, 0, w, h, Color.new(36, 30, 24))                    # the plinth's mahogany frame
    b.fill_rect(4, 4, w - 8, h - 8, Color.new(176, 150, 96))           # brass bezel
    b.fill_rect(7, 7, w - 14, h - 14, Color.new(26, 30, 44))           # the case, dark behind the model
    cx = w / 2
    cy = 112
    # the ring of mountains
    16.times do |i|
      a = (Math::PI * 2 * i / 16.0) + 0.2
      mx = cx + (Math.cos(a) * 150).round
      my = cy + (Math.sin(a) * 58).round
      hgt = 34 + ((i * 7) % 18)
      wid = 34 + ((i * 5) % 14)
      shade = (my < cy) ? 92 : 120
      wid.times do |dx|
        hh = (hgt * (1.0 - ((dx - (wid / 2.0)).abs / (wid / 2.0)))).round
        b.fill_rect(mx - (wid / 2) + dx, my - hh, 1, hh, Color.new(shade, shade - 6, shade - 18))
      end
      b.fill_rect(mx - 3, my - hgt, 6, 5, Color.new(236, 236, 240)) if hgt > 44   # snow
    end
    # the white bowl and its terraces
    ellipse(b, cx, cy, 104, 40, Color.new(214, 214, 220))
    ellipse(b, cx, cy + 2, 92, 34, Color.new(240, 240, 244))
    ellipse(b, cx, cy + 4, 70, 25, Color.new(226, 228, 234))
    ellipse(b, cx, cy + 6, 46, 15, Color.new(196, 186, 150))          # the stage floor
    # the brass ring round the rim
    360.times do |deg|
      a = Math::PI * deg / 180.0
      b.fill_rect(cx + (Math.cos(a) * 106).round, cy + (Math.sin(a) * 41).round, 2, 2, Color.new(214, 170, 74))
    end
    # eighteen slim pylons on the ring, back ones first
    pylons = (0...18).map { |i| Math::PI * 2 * i / 18.0 }.sort_by { |a| Math.sin(a) }
    pylons.each do |a|
      px = cx + (Math.cos(a) * 106).round
      py = cy + (Math.sin(a) * 41).round
      ph = 30 + (Math.sin(a) * 6).round
      b.fill_rect(px - 1, py - ph, 3, ph, Color.new(232, 226, 210))
      b.fill_rect(px - 2, py - ph - 3, 5, 3, Color.new(214, 170, 74))
    end
    # the glass: a pale sheen across the case
    gl = Sprite.new(vp)
    gl.bitmap = Bitmap.new(w, h)
    (0...w).step(2) do |x|
      a = (28 * Math.sin(Math::PI * ((x - 40).clamp(0, 140) / 140.0))).round
      gl.bitmap.fill_rect(x, 7, 2, h - 14, Color.new(255, 255, 255, a)) if a > 0
    end
    sprites = [spr, gl]
    sprites.each { |s| s.opacity = 0 }
    pbSEPlay("GUI menu open", 60, 80) rescue nil
    fade(sprites, 0, 255, 0.4)
    hold(3.2)
    fade(sprites, 255, 0, 0.4)
    sprites.each { |s| s.bitmap.dispose; s.dispose }
    vp.dispose
    return true
  end
end

def pfm_arena_model; return PrismfallVignette.arena_model; end
