#===============================================================================
# Prismfall Maps - 016 staging helpers for map events (mapgen/ruby/016_Staging.rb, copied by build.py)
#-------------------------------------------------------------------------------
# The scripts' bracketed narration is stage direction (design/MAPGEN.md "Stage directions"): events play it with
# move routes, emotes, tones, SEs and these calls instead of printing it. Durations are in 1/20 s, like the event
# commands. Everything here softens itself when Prismfall::Cutscene.photosensitive? (no white frames, half shake).
#
#   pfm_flash(r, g, b, dur = 8, alpha = 200)   a screen flash; a dim pulse of the same colour when photosensitive
#   pfm_shake(power = 4, speed = 12, dur = 10) screen shake (halved when photosensitive)
#   pfm_tone(r, g, b, gray = 0, dur = 20)      tone change, waits for it
#   pfm_fade_out(dur = 20) / pfm_fade_in(dur = 20)   to black / back to the map's own tone, waits. The black holds
#                                              across a transfer until pfm_fade_in (or any pfm_tone).
#   pfm_glow(r, g, b, dur = 30, hold = 20)     the room fills with a colour and lets go again (steam, ash, a gauge)
#   pfm_emote(who, id)                         an emote bubble on an event name / id / :player (3 "!", 4 "?", ...)
#   pfm_face(who, target)                      who turns toward target (event name / id / :player)
#   pfm_event(name)                            the Game_Event called name on this map (nil if none)
#   pfm_vanish(name, dur = 16)                 fades an event out and erases it
#   pfm_appear(name, dur = 16)                 fades an event in from opacity 0
#   pfm_step(who, dx, dy)                      teleports who by a tile offset with no walk (staging under a fade)
#   pfm_needle(key, from, to, dur)             three SE ticks falling or rising in pitch: a gauge needle moving
#   pfm_pan_home(dur = 20)                     the camera glides back onto the player after a pan (clamped to the map)
#   pfm_shadow_pass(dur = 60, dark = 70)       a long soft shadow slides across the screen, left to right (an airship
#                                              overhead); waits. Over the map, under the message box.
#===============================================================================
module PrismfallStaging
  module_function

  def safe?
    return defined?(Prismfall::Cutscene) && Prismfall::Cutscene.respond_to?(:photosensitive?) &&
           Prismfall::Cutscene.photosensitive?
  end

  def secs(dur); return dur / 20.0; end

  # A scene's own standing tone for the map (night in the lighthouse during Interlude I): the first rule that
  # answers wins over the spec's tone. PrismfallStaging.tone_rule { Tone or nil }
  def tone_rule(&block); (@tone_rules ||= []) << block; end

  def rule_tone
    (@tone_rules || []).each do |r|
      t = (r.call rescue nil)
      return t if t
    end
    return nil
  end

  def map_tone
    t = rule_tone
    return t if t
    t = (defined?(PrismfallMaps::MAP_TONES) && $game_map && PrismfallMaps::MAP_TONES[$game_map.map_id]) || [0, 0, 0, 0]
    return Tone.new(*t)
  end

  # pfm_fade_out holds the screen black across a transfer (entering a map resets the tone to the map's own)
  def black?;      return @black ? true : false; end
  def black=(v);   @black = v;                   end

  def enter_map
    return if !$game_screen
    if black?
      $game_screen.start_tone_change(Tone.new(-255, -255, -255, 0), 0)
    elsif (t = rule_tone)
      $game_screen.start_tone_change(t, 0)
    end
  end

  def char(who)
    return $game_player if who.nil? || who == :player || who.to_s.downcase == "player" || who == -1
    return who if who.is_a?(Game_Character)
    return nil if !$game_map
    return $game_map.events[who] if who.is_a?(Integer)
    return $game_map.events.values.find { |e| e.name == who.to_s }
  end

  def flash(r, g, b, dur, alpha)
    if safe?
      $game_screen.start_tone_change(Tone.new(r / 6, g / 6, b / 6, 0), 6)
      pbWait(0.3)
      $game_screen.start_tone_change(map_tone, [dur, 12].max)
    else
      $game_screen.start_flash(Color.new(r, g, b, alpha), dur)
    end
  end

  def shake(power, speed, dur)
    power = [power / 2, 1].max if safe?
    $game_screen.start_shake(power, speed, dur)
  end

  def fade(ev, from, to, dur)
    return if !ev
    t0 = System.uptime
    len = [secs(dur), 0.05].max
    loop do
      k = [(System.uptime - t0) / len, 1.0].min
      ev.opacity = (from + ((to - from) * k)).round
      break if k >= 1.0
      pbWait(0.02)
    end
  end
end

EventHandlers.add(:on_enter_map, :prismfall_staging_tone,
  proc { |_old_map_id| PrismfallStaging.enter_map }
)

def pfm_flash(r = 255, g = 255, b = 255, dur = 8, alpha = 200); PrismfallStaging.flash(r, g, b, dur, alpha); return true; end
def pfm_shake(power = 4, speed = 12, dur = 10);                  PrismfallStaging.shake(power, speed, dur);   return true; end

def pfm_tone(r, g, b, gray = 0, dur = 20)
  PrismfallStaging.black = (r <= -255 && g <= -255 && b <= -255)
  $game_screen.start_tone_change(Tone.new(r, g, b, gray), dur)
  pbWait(PrismfallStaging.secs(dur)) if dur > 0
  return true
end

def pfm_fade_out(dur = 20); return pfm_tone(-255, -255, -255, 0, dur); end

def pfm_fade_in(dur = 20)
  PrismfallStaging.black = false
  $game_screen.start_tone_change(PrismfallStaging.map_tone, dur)
  pbWait(PrismfallStaging.secs(dur)) if dur > 0
  return true
end

def pfm_glow(r, g, b, dur = 30, hold = 20)
  k = (PrismfallStaging.safe?) ? 0.5 : 1.0
  $game_screen.start_tone_change(Tone.new((r * k).round, (g * k).round, (b * k).round, 0), dur)
  pbWait(PrismfallStaging.secs(dur + hold))
  $game_screen.start_tone_change(PrismfallStaging.map_tone, dur)
  pbWait(PrismfallStaging.secs(dur))
  return true
end

def pfm_event(name); return PrismfallStaging.char(name); end

def pfm_emote(who, id = 3)
  ch = PrismfallStaging.char(who)
  return false if !ch
  ch.animation_id = id
  pbWait(0.6)
  return true
end

def pfm_face(who, target)
  a = PrismfallStaging.char(who)
  b = PrismfallStaging.char(target)
  return false if !a || !b
  dx = b.x - a.x
  dy = b.y - a.y
  dir = (dx.abs > dy.abs) ? ((dx > 0) ? 6 : 4) : ((dy > 0) ? 2 : 8)
  a.instance_variable_set(:@direction, dir)       # also turns a direction-fixed actor
  return true
end

def pfm_vanish(name, dur = 16)
  ev = PrismfallStaging.char(name)
  return false if !ev
  PrismfallStaging.fade(ev, ev.opacity, 0, dur)
  ev.erase if ev.respond_to?(:erase)
  return true
end

def pfm_appear(name, dur = 16)
  ev = PrismfallStaging.char(name)
  return false if !ev
  PrismfallStaging.fade(ev, 0, 255, dur)
  return true
end

def pfm_step(who, dx, dy)
  ch = PrismfallStaging.char(who)
  return false if !ch
  ch.moveto(ch.x + dx, ch.y + dy)
  return true
end

def pfm_needle(se = "Voltorb Flip mark", from = 120, to = 70, dur = 24)
  3.times do |i|
    pitch = (from + ((to - from) * i / 2.0)).round
    pbSEPlay(se, 80, pitch) rescue nil
    pbWait(PrismfallStaging.secs(dur) / 3.0)
  end
  return true
end

def pfm_shadow_pass(dur = 60, dark = 70)
  w = Graphics.width
  h = Graphics.height
  bw = (w * 0.9).round
  bh = (h * 0.55).round
  spr = Sprite.new(Spriteset_Map.viewport)
  spr.bitmap = Bitmap.new(bw, bh)
  bh.times do |y|
    ky = Math.sin(Math::PI * y / bh.to_f)
    (0...bw).step(4) do |x|
      kx = Math.sin(Math::PI * x / bw.to_f)
      a = (dark * ky * kx).round
      spr.bitmap.fill_rect(x, y, 4, 1, Color.new(60, 60, 50, a)) if a > 0
    end
  end
  spr.blend_type = 2
  spr.z = 8999
  y0 = (h * 0.15).round
  pbSEPlay("Anim/Wind1", 50, 50) rescue nil
  t0 = System.uptime
  len = [dur / 20.0, 0.2].max
  loop do
    k = [(System.uptime - t0) / len, 1.0].min
    spr.x = (-bw + ((w + bw) * k)).round
    spr.y = (y0 + (h * 0.12 * k)).round
    break if k >= 1.0
    pbWait(0.02)
  end
  spr.bitmap.dispose
  spr.dispose
  return true
end

def pfm_pan_home(dur = 20)
  return false if !$game_map || !$game_player
  x0 = $game_map.display_x
  y0 = $game_map.display_y
  $game_player.center($game_player.x, $game_player.y)      # where the camera belongs (Game_Player clamps it)
  x1 = $game_map.display_x
  y1 = $game_map.display_y
  $game_map.display_x = x0
  $game_map.display_y = y0
  t0 = System.uptime
  len = [dur / 20.0, 0.05].max
  loop do
    k = [(System.uptime - t0) / len, 1.0].min
    e = 0.5 - (0.5 * Math.cos(Math::PI * k))
    $game_map.display_x = (x0 + ((x1 - x0) * e)).round
    $game_map.display_y = (y0 + ((y1 - y0) * e)).round
    break if k >= 1.0
    pbWait(0.02)
  end
  return true
end
