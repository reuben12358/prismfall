#===============================================================================
# Prismfall Maps - 021 the Quiet Ward (mapgen/ruby/021_QuietWard.rb, copied by build.py)
#-------------------------------------------------------------------------------
# Chapter 7 (story/26_SCRIPT_CH7.md; the events are mapgen/layouts/story_ch7.py). Stage directions with no tile art:
#   pfm_veil(x, y, w, h = 1, dur = 30)  "a shimmer like heat over a road" across tiles x..x+w-1, y..y+h-1 of this
#                                       map: a grey-violet band that wavers, drawn in code over the map (waits for
#                                       the fade in)
#   pfm_veil_off(dur = 50)              it "thins, wavers, and sinks back into the beds like mist" (waits)
#   pfm_screens(n = 3)                  every lamp-screen in Mirefen flickers at once: n pale pulses and a buzz
#   pfm_sweetrot(taken = 1)             the Sweetrot: peach-pink warmth floods the screen, holds, and drains away
#                                       a little greyer than before (the "want another one" after)
#   pfm_approach(name, dist = 3, stop = 1)  an event "walks up to you": it appears dist tiles from the player on the
#                                       first clear straight line, fades in and walks until stop tiles away
#   pfm_dreaming_eyes(secs = 3.2)       Ward Night, key event 2: a framed close-up drawn in code: a small face under
#                                       a crust of clear salt, the eyes moving side to side, fast (019's pane)
# All of them halve themselves when Prismfall::Cutscene.photosensitive? (no bright pulses).
#===============================================================================
module PrismfallVeil
  module_function

  def safe?; return defined?(PrismfallStaging) && PrismfallStaging.safe?; end

  def show(x, y, w, h, dur)
    dispose
    @rect = [x, y, w, h]
    @map = $game_map.map_id
    @alpha = 0.0
    @target = (safe?) ? 110.0 : 170.0
    @rate = @target / [dur, 1].max
    wait_settle
  end

  def hide(dur)
    return if !@rect
    @target = 0.0
    @rate = [@alpha, 1.0].max / [dur, 1].max
    wait_settle
    dispose
  end

  def wait_settle
    120.times do
      break if (@alpha - @target).abs < 1
      Graphics.update
      Input.update
      pbUpdateSceneMap
    end
  end

  def build(w, h)
    pw = w * 32
    ph = (h * 32) + 24
    bmp = Bitmap.new(pw, ph)
    pw.times do |x|
      k = (Math.sin(x / 5.0) * 0.5) + 0.5
      ph.times do |y|
        edge = [y, ph - 1 - y].min / 12.0
        a = (([edge, 1.0].min) * (110 + (k * 90))).round
        next if a <= 0
        g = 150 + (((x * 7) + (y * 3)) % 40)
        bmp.set_pixel(x, y, Color.new(g - 10, g - 20, g + 30, a)) if (x + y).even? || y % 3 == 0
      end
    end
    return bmp
  end

  def update
    return if !@rect
    if !$game_map || $game_map.map_id != @map || !$scene.is_a?(Scene_Map)
      dispose
      return
    end
    if !@spr || @spr.disposed?
      @spr = Sprite.new(Spriteset_Map.viewport)
      @spr.bitmap = build(@rect[2], @rect[3])
      @spr.z = 8500
      @spr.blend_type = 1
    end
    if @alpha < @target
      @alpha = [@alpha + @rate, @target].min
    elsif @alpha > @target
      @alpha = [@alpha - @rate, @target].max
    end
    t = System.uptime
    x, y, = @rect
    sx = ((x * Game_Map::REAL_RES_X) - $game_map.display_x) / Game_Map::X_SUBPIXELS
    sy = ((y * Game_Map::REAL_RES_Y) - $game_map.display_y) / Game_Map::Y_SUBPIXELS
    @spr.x = sx + (Math.sin(t * 3.1) * 2).round
    @spr.y = sy - 12 + (Math.sin(t * 1.7) * 3).round
    @spr.zoom_x = 1.0 + (Math.sin(t * 2.3) * 0.02)
    @spr.opacity = (@alpha * (0.8 + (Math.sin(t * 4.0) * 0.2))).round
  end

  def dispose
    if @spr && !@spr.disposed?
      @spr.bitmap.dispose if @spr.bitmap && !@spr.bitmap.disposed?
      @spr.dispose
    end
    @spr = nil
    @rect = nil if @target == 0.0
  end
end

EventHandlers.add(:on_frame_update, :prismfall_quiet_ward_veil,
  proc { PrismfallVeil.update }
)

def pfm_veil(x, y, w, h = 1, dur = 30); PrismfallVeil.show(x, y, w, h, dur); return true; end
def pfm_veil_off(dur = 50);             PrismfallVeil.hide(dur);             return true; end

def pfm_screens(n = 3)
  safe = PrismfallVeil.safe?
  n.times do |i|
    pbSEPlay("Glitch Tear Static", (safe) ? 40 : 70, 100 + (i * 10)) rescue nil
    if safe
      $game_screen.start_tone_change(Tone.new(10, 14, 24, 40), 3)
    else
      $game_screen.start_flash(Color.new(180, 200, 230, 110), 6)
    end
    pbWait(0.25)
  end
  return true
end

def pfm_sweetrot(taken = 1)
  pbSEPlay("Sweet Scent", 85, 100) rescue nil
  base = (defined?(PrismfallStaging)) ? PrismfallStaging.map_tone : Tone.new(0, 0, 0, 0)
  warm = (PrismfallVeil.safe?) ? Tone.new(40, 10, 20, 0) : Tone.new(90, 30, 50, 0)
  $game_screen.start_tone_change(warm, 20)
  pbWait(1.6)
  grey = Tone.new(base.red, base.green, base.blue, [base.gray + (taken * 30), 255].min)
  $game_screen.start_tone_change(grey, 30)
  pbWait(1.2)
  $game_screen.start_tone_change(base, 40)
  return true
end

DIR_OF = { [0, 1] => 2, [0, -1] => 8, [1, 0] => 6, [-1, 0] => 4 }

def pfm_approach(name, dist = 3, stop = 1)
  ev = PrismfallStaging.char(name)
  return false if !ev
  was_through = ev.through
  ev.through = false                                  # an actor page is Through: walk it like a person
  px = $game_player.x
  py = $game_player.y
  spot = nil
  [[0, 1], [0, -1], [1, 0], [-1, 0]].each do |dx, dy|
    sx = px + (dx * dist)
    sy = py + (dy * dist)
    next if !$game_map.valid?(sx, sy)
    toward = DIR_OF[[-(dx <=> 0), -(dy <=> 0)]]
    next if !toward
    clear = (stop...dist).all? do |k|
      x = px + (dx * (k + 1))
      y = py + (dy * (k + 1))
      ev.passable?(x, y, toward) && $game_map.events.values.none? { |o| o != ev && o.x == x && o.y == y && !o.through && o.character_name != "" }
    end
    next if !clear
    spot = [sx, sy]
    break
  end
  spot ||= [px, py + 1]
  ev.moveto(*spot)
  ev.opacity = 0
  ev.turn_toward_player
  PrismfallStaging.fade(ev, 0, 255, 12)
  (dist - stop).times do
    ev.move_toward_player
    40.times do
      break if !ev.moving?
      Graphics.update
      Input.update
      pbUpdateSceneMap
    end
  end
  ev.turn_toward_player
  ev.through = was_through
  return true
end

def pfm_dreaming_eyes(secs = 3.2)
  return false if !defined?(PrismfallVignette)
  w = 240
  h = 140
  vp = PrismfallVignette.pane(w, h)
  bg = Sprite.new(vp)
  bg.bitmap = Bitmap.new(w, h)
  b = bg.bitmap
  b.fill_rect(0, 0, w, h, Color.new(20, 22, 30))
  b.fill_rect(3, 3, w - 6, h - 6, Color.new(120, 124, 140))
  b.fill_rect(6, 6, w - 12, h - 12, Color.new(34, 36, 48))
  PrismfallVignette.ellipse(b, w / 2, 86, 70, 64, Color.new(214, 196, 184))          # her face, cheek to brow
  PrismfallVignette.ellipse(b, w / 2, 30, 96, 30, Color.new(236, 240, 248))          # salt hair over the pillow
  60.times do |i|                                                                     # crystal glints in the salt
    x = 20 + ((i * 37) % (w - 40))
    y = 8 + ((i * 23) % 50)
    b.fill_rect(x, y, 2, 2, Color.new(255, 255, 255))
  end
  [[w / 2 - 34, 78], [w / 2 + 34, 78]].each do |ex, ey|                              # closed lids
    PrismfallVignette.ellipse(b, ex, ey, 18, 8, Color.new(196, 176, 166))
    b.fill_rect(ex - 18, ey + 6, 36, 2, Color.new(120, 96, 90))
  end
  eyes = Sprite.new(vp)                                                              # the eyes under the lids
  eyes.bitmap = Bitmap.new(w, h)
  salt = Sprite.new(vp)                                                              # the clear salt over them
  salt.bitmap = Bitmap.new(w, h)
  sb = salt.bitmap
  (40..118).step(2) do |y|
    (24..(w - 24)).step(2) do |x|
      a = 40 + (((x * 13) + (y * 7)) % 50)
      sb.set_pixel(x, y, Color.new(230, 244, 255, a)) if (x + y) % 4 == 0
    end
  end
  all = [bg, eyes, salt]
  all.each { |s| s.opacity = 0 }
  draw = proc do |off|
    eyes.bitmap.clear
    [[w / 2 - 34, 78], [w / 2 + 34, 78]].each do |ex, ey|
      PrismfallVignette.ellipse(eyes.bitmap, ex + off, ey + 1, 6, 4, Color.new(120, 100, 104, 150))
    end
  end
  draw.call(0)
  PrismfallVignette.fade(all, 0, 255, 0.5)
  t0 = System.uptime
  until System.uptime - t0 >= secs
    t = System.uptime - t0
    draw.call((Math.sin(t * 9.0) * 10).round)                                         # side to side, fast
    Graphics.update
    Input.update
    pbUpdateSceneMap
  end
  PrismfallVignette.fade(all, 255, 0, 0.5)
  all.each { |s| s.bitmap.dispose; s.dispose }
  vp.dispose
  return true
end
