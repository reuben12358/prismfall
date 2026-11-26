#===============================================================================
# Prismfall Maps - 018 Crownhaven's Prism Arena: the procession, the Concordance Ring's 18 pylons, the white
# vision (mapgen/ruby/018_Crownhaven.rb, copied by build.py)
#-------------------------------------------------------------------------------
# story/39_SCRIPT_CH20.md "Day 1: The Opening Ceremony" and story/40_SCRIPT_CH21.md "The Hijack" / "Six bars,
# three locks each". The data (who carries which Plate, in what order, what colour it burns) is Core
# 030_Ceremony_Ladder.rb; the finale's release / refusal record is Core 033_Finale.rb. This file moves the events.
#
# WHAT THE ARENA MAP NEEDS (names are the contract; positions are the builder's):
#   "Pylon 1" .. "Pylon 18"   the Ring's pylons, in gym order. Pages by self switch:
#        A = its Plate is set and burning    B = a golden lock is on it (Ch21)
#        C = released (lock open, Plate risen)   D = refused / torn free by force (dark)
#   "Stand 1" .. "Stand 18"   (optional, no graphic) where each bearer stops; default: the tile south of the pylon
#   "Stair 1", "Stair 2" ...  (optional, no graphic) waypoints down the Sovereign's Stair, walked in name order
#   one event per bearer, named as Prismfall::Ceremony.procession gives it: "Dorian" ... "Sigrun", plus
#   "Meridian officer", "Choir porter", "Pip", "Magnus guard 1", "Magnus guard 2" (whoever the flags call for)
#
# CEREMONY (Ch20)
#   pf_ceremony_step(gym)        that Warden's bearer walks the stair to their pylon and sets the Plate (it lights)
#   pf_ceremony_procession       all eighteen, in gym order ("to the Choir's counting rhyme"); pause: seconds between
#   pf_pylon_light(gym)          one pylon lights in its Plate's colour;  pf_ring_light = "The Ring lights in
#                                eighteen colours" (all of them, a ripple round the Ring)
#   pf_ceremony_vision           "[anim: the PC's sprite glows; screen to white over 60 frames; hold]"
#   pf_ceremony_vision_end       "[anim: white to black]" - transfer to the stands, then pfm_fade_in
# FINALE (Ch21)
#   pf_pylon_lock                "The Ring's pylons sprout golden locks. Eighteen."   pf_pylon_lock(gym) for one
#   pf_pylon_release(gym) / pf_pylon_refuse(gym) / pf_pylon_force(gym)   one lock's end, with its light
#   pf_pylons_sync               after the Arceus battle: every pylon shows what its Warden did (Core 033's record)
#   pf_warden_kneel(gym)         the Warden's event goes to their pylon and kneels (charset "kneel_NAME" if drawn)
#   pf_ring_dark                 all pylons out (the Ring goes quiet)
# A missing event is skipped, so a half-built arena still plays the rest.
#===============================================================================
module PrismfallCrownhaven
  PYLON_SE     = "Mining reveal"
  LOCK_SE      = "Door enter"
  STATES       = ["A", "B", "C", "D"]
  WALK_LIMIT   = 120          # steps per leg before the walker is simply placed (a route that was never possible)

  module_function

  def event(name)
    return nil if !$game_map
    return $game_map.events.values.find { |e| e.name == name.to_s }
  end

  def pylon(gym);   return event("Pylon #{gym}"); end
  def safe?
    return defined?(Prismfall::Cutscene) && Prismfall::Cutscene.respond_to?(:photosensitive?) &&
           Prismfall::Cutscene.photosensitive?
  end

  def row(gym)
    return nil if !defined?(Prismfall::Ceremony)
    return Prismfall::Ceremony.row(gym)
  end

  def set_switch(ev, ch, value)
    return if !ev || !$game_self_switches
    $game_self_switches[[$game_map.map_id, ev.id, ch]] = value
    $game_map.need_refresh = true
  end

  # One-hot pylon state: nil = bare, or "A".."D" (A can stay under B: a locked pylon still holds its Plate).
  def set_pylon(gym, on: [], off: [])
    ev = pylon(gym)
    return false if !ev
    off.each { |ch| set_switch(ev, ch, false) }
    on.each { |ch| set_switch(ev, ch, true) }
    return true
  end

  def wait(seconds)
    pbWait(seconds) if seconds > 0 && defined?(pbWait)
  end

  def flash(color, dur = 8, alpha = 150)
    return if !$game_screen
    if defined?(pfm_flash)
      pfm_flash(color[0], color[1], color[2], dur, alpha)
    elsif !safe?
      $game_screen.start_flash(Color.new(color[0], color[1], color[2], alpha), dur)
    end
  end

  def tone(r, g, b, gray, dur)
    return if !$game_screen
    $game_screen.start_tone_change(Tone.new(r, g, b, gray), dur)
    wait(dur / 20.0)
  end

  def se(name, pitch = 100)
    pbSEPlay(name, 80, pitch)
  rescue StandardError
    nil
  end

  #-----------------------------------------------------------------------------
  # Walking
  #-----------------------------------------------------------------------------
  def wait_move(ev)
    80.times do
      break if !ev.moving?
      Graphics.update
      Input.update
      pbUpdateSceneMap
    end
  end

  def step(ev, dir)
    was = ev.through
    ev.through = true
    case dir
    when 2 then ev.move_down(false)
    when 4 then ev.move_left(false)
    when 6 then ev.move_right(false)
    when 8 then ev.move_up(false)
    end
    ev.through = was
    ev.instance_variable_set(:@direction, dir)
    wait_move(ev)
  end

  # Straight legs: the longer axis first. Places the walker if the walk runs away.
  def walk_to(ev, x, y)
    n = 0
    while (ev.x != x || ev.y != y) && n < WALK_LIMIT
      dx = x - ev.x
      dy = y - ev.y
      dir = (dx.abs >= dy.abs && dx != 0) ? ((dx > 0) ? 6 : 4) : ((dy > 0) ? 2 : 8)
      before = [ev.x, ev.y]
      step(ev, dir)
      break if [ev.x, ev.y] == before
      n += 1
    end
    ev.moveto(x, y) if ev.x != x || ev.y != y
  end

  def stair
    return [] if !$game_map
    pts = $game_map.events.values.select { |e| e.name =~ /\AStair \d+\z/ }
    return pts.sort_by { |e| e.name[/\d+/].to_i }.map { |e| [e.x, e.y] }
  end

  def stand_tile(gym)
    st = event("Stand #{gym}")
    return [st.x, st.y] if st
    py = pylon(gym)
    return (py) ? [py.x, py.y + 1] : nil
  end

  def face(ev, target)
    return if !ev || !target
    dx = target.x - ev.x
    dy = target.y - ev.y
    dir = (dx.abs > dy.abs) ? ((dx > 0) ? 6 : 4) : ((dy > 0) ? 2 : 8)
    ev.instance_variable_set(:@direction, dir)
  end

  #-----------------------------------------------------------------------------
  # The ceremony
  #-----------------------------------------------------------------------------
  def light(gym, quiet: false)
    r = row(gym)
    return false if !set_pylon(gym, :on => ["A"])
    return true if quiet
    se(PYLON_SE, 80 + (gym * 4))                 # the eighteen notes climb
    flash(r ? r[:color] : [255, 255, 255], 8, 130)
    return true
  end

  def ceremony_step(gym, pause: 0.3)
    r = row(gym)
    return false if !r
    bearer = event(r[:bearer])
    dest = stand_tile(gym)
    if bearer && dest
      bearer.opacity = 255 if bearer.respond_to?(:opacity=)
      stair.each { |x, y| walk_to(bearer, x, y) }
      walk_to(bearer, dest[0], dest[1])
      face(bearer, pylon(gym))
      r[:with].each_with_index do |name, i|        # Pip at Bastian's elbow; Magnus's guards a step behind
        ev = event(name)
        next if !ev
        ev.moveto(dest[0] + ((i.even?) ? 1 : -1), dest[1] + ((r[:with].length > 1) ? 1 : 0))
        face(ev, pylon(gym))
      end
    end
    wait(pause)
    light(gym)
    wait(pause)
    return true
  end

  def procession(from: 1, to: 18, pause: 0.3)
    done = 0
    (from..to).each { |gym| done += 1 if ceremony_step(gym, pause: pause) }
    return done
  end

  # "The Ring lights in eighteen colours."
  def ring_light(pause: 0.08)
    (1..18).each do |gym|
      light(gym, quiet: true)
      se(PYLON_SE, 80 + (gym * 4))
      wait(pause)
    end
    flash([255, 255, 255], 12, 110)
    return true
  end

  def ring_dark
    (1..18).each { |gym| set_pylon(gym, :off => STATES) }
    return true
  end

  # The PC glows and the world goes white (a softer, slower white when photosensitive). Holds white.
  def vision(hold: 1.0)
    3.times do |i|
      flash([255, 255, 255], 6, 60 + (i * 30))
      wait(0.25)
    end
    v = safe? ? 150 : 255
    tone(v, v, v, 0, safe? ? 45 : 30)            # "over 60 frames"
    wait(hold)
    return true
  end

  def vision_end(dur = 20)
    tone(-255, -255, -255, 0, dur)               # white to black; the caller moves the PC to the stands
    PrismfallStaging.black = true if defined?(PrismfallStaging) && PrismfallStaging.respond_to?(:black=)
    return true
  end

  #-----------------------------------------------------------------------------
  # The finale's locks
  #-----------------------------------------------------------------------------
  def each_gym(gym)
    list = (gym.nil? || gym == :all) ? (1..18).to_a : Array(gym)
    list.each { |g| yield g }
  end

  def lock(gym = :all, pause: 0.06)
    each_gym(gym) do |g|
      next if !set_pylon(g, :on => ["B"], :off => ["C", "D"])
      se(LOCK_SE, 140)
      wait(pause)
    end
    flash([255, 208, 64], 10, 120)               # gold
    return true
  end

  def release(gym)
    r = row(gym)
    return false if !set_pylon(gym, :on => ["C"], :off => ["B", "D"])
    se(PYLON_SE, 120)
    flash(r ? r[:color] : [255, 255, 255], 10, 140)
    return true
  end

  def refuse(gym)
    return false if !set_pylon(gym, :on => ["B", "D"], :off => ["C"])
    se(LOCK_SE, 70)
    return true
  end

  # "The Warden is thrown back from the pylon and the Plate tears free with a crack of Bleed light."
  def force(gym)
    return false if !set_pylon(gym, :on => ["D"], :off => ["B", "C"])
    flash([168, 88, 232], 8, 160)                # Bleed violet
    $game_screen.start_shake(safe? ? 2 : 5, 14, 8) if $game_screen
    r = row(gym)
    w = r && event(r[:name])
    if w                                         # thrown a tile back from the pylon
      py = pylon(gym)
      back = (py) ? [w.x + (w.x <=> py.x), w.y + (w.y <=> py.y)] : nil
      w.moveto(back[0], back[1]) if back && back != [w.x, w.y]
    end
    return true
  end

  # After the battle: every pylon shows what happened to its lock (Core 033_Finale.rb's record).
  def sync
    return false if !defined?(Prismfall::Finale)
    (1..18).each do |gym|
      case Prismfall::Finale.lock_state(gym)
      when :released then set_pylon(gym, :on => ["C"], :off => ["B", "D"])
      when :refused, :forced then set_pylon(gym, :on => ["D"], :off => ["B", "C"])
      end
    end
    return true
  end

  def kneel(gym)
    r = row(gym)
    return false if !r
    w = event(r[:name]) || event(r[:bearer])
    return false if !w
    dest = stand_tile(gym)
    w.moveto(dest[0], dest[1]) if dest && [w.x, w.y] != dest
    face(w, pylon(gym))
    sheet = "kneel_#{r[:warden]}"
    if pbResolveBitmap("Graphics/Characters/#{sheet}")
      w.instance_variable_set(:@character_name, sheet)
      w.instance_variable_set(:@walk_anime, false)
      w.instance_variable_set(:@step_anime, false)
    end
    w.instance_variable_set(:@direction_fix, true)
    return true
  end
end

def pf_ceremony_step(gym, pause: 0.3);    return PrismfallCrownhaven.ceremony_step(gym, pause: pause);  end
def pf_ceremony_procession(**opts);       return PrismfallCrownhaven.procession(**opts);                end
def pf_pylon_light(gym);                  return PrismfallCrownhaven.light(gym);                        end
def pf_ring_light;                        return PrismfallCrownhaven.ring_light;                        end
def pf_ring_dark;                         return PrismfallCrownhaven.ring_dark;                         end
def pf_ceremony_vision(hold: 1.0);        return PrismfallCrownhaven.vision(hold: hold);                end
def pf_ceremony_vision_end(dur = 20);     return PrismfallCrownhaven.vision_end(dur);                   end
def pf_pylon_lock(gym = :all);            return PrismfallCrownhaven.lock(gym);                         end
def pf_pylon_release(gym);                return PrismfallCrownhaven.release(gym);                      end
def pf_pylon_refuse(gym);                 return PrismfallCrownhaven.refuse(gym);                       end
def pf_pylon_force(gym);                  return PrismfallCrownhaven.force(gym);                        end
def pf_pylons_sync;                       return PrismfallCrownhaven.sync;                              end
def pf_warden_kneel(gym);                 return PrismfallCrownhaven.kneel(gym);                        end
