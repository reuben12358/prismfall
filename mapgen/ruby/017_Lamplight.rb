#===============================================================================
# Prismfall Maps - 017 Interlude I "Lamplight" (mapgen/ruby/017_Lamplight.rb, copied by build.py)
#-------------------------------------------------------------------------------
# story/24_SCRIPT_CH5.md "Maps 105/106 - Ferrow Lighthouse: INTERLUDE I". The events are written by
# mapgen/layouts/story_interlude1.py; the party / charset swap is Core 028 (Prismfall::Interlude, loadout 1).
#
#   pfm_il1_start      on a black screen: Kestrel's three (Honedge "Morwen" in front, Staravia, his starter,
#                      K2's levels + 2), his sprite and name, V119 = 1; Juno stops following; the BGM stops and
#                      the lighthouse maps stay quiet while it runs.
#   pfm_il1_end        the PC's party, look and name back; V119 = 0; Juno's leg restored.
#   pfm_il1_memory     the memory flash (no control): a crowd seen from a small boy's height, a veiled woman
#                      running away toward a light, a kid made of light. A slow soft version when photosensitive.
#   pfm_il1_haunter    the Bleed-touched Haunter (K2's level + 3; no capture, no running, a loss doesn't black
#                      out): true on a win. Kestrel's "Hold. Hold it." plays when Honedge is out.
#   pfm_il1_boat       Edda's boat slipping the harbour chain, seen from the gallery (a drawn vignette).
#   The great lamp's sweep is automatic on 105 / 106 while V119 == 1 (pfm_il1_lamp(false) holds it).
#===============================================================================
module PrismfallLamplight
  MAPS = [105, 106]
  VAR  = 119
  module_function

  def running?
    return $game_variables && $game_variables[VAR] == 1
  end

  def safe?
    return defined?(Prismfall::Cutscene) && Prismfall::Cutscene.respond_to?(:photosensitive?) &&
           Prismfall::Cutscene.photosensitive?
  end

  #-----------------------------------------------------------------------------
  # The swap
  #-----------------------------------------------------------------------------
  def starter_line
    r = Prismfall::Rival
    return (Array(r.line(r.starter_gen, r.kestrel_slot)) + Array(r.line(r::RIVAL_SOURCE_GEN, r.kestrel_slot))).uniq
  rescue StandardError
    return []
  end

  # The PBS party carries the source generation's starter line (the rival hook swaps it when a battle loads the
  # trainer); the borrowed team gets the same swap, so Kestrel holds the starter he really picked.
  def match_starter(party)
    r = Prismfall::Rival
    gen = r.starter_gen
    return if gen == r::RIVAL_SOURCE_GEN
    party.each do |pk|
      info = r.lookup(pk.species)
      next if !info || info[:gen] != r::RIVAL_SOURCE_GEN
      line = r.line(gen, info[:slot])
      sp = line && (line[info[:stage]] || line.last)
      next if !sp || !GameData::Species.exists?(sp)
      r.swap_species(pk, sp)
      pk.calc_stats
      pk.heal
    end
  rescue StandardError => e
    PBDebug.log("[Lamplight] match_starter: #{e.class}: #{e.message}") if defined?(PBDebug)
  end

  def start
    return false if !defined?(Prismfall::Interlude)
    leg = (pfm_get(:juno_leg) rescue nil)
    if leg
      pfm_set(:il1_juno_leg, leg)
      pfm_juno_part rescue nil
    end
    ok = Prismfall::Interlude.start(1, :drop => nil, :only => [:HONEDGE, :STARAVIA] + starter_line)
    return false if !ok
    party = $player.party
    match_starter(party)
    morwen = party.find { |pk| pk.isSpecies?(:HONEDGE) }
    if morwen                                   # "Morwen. Up.": she leads
      party.delete(morwen)
      party.unshift(morwen)
      morwen.name = "Morwen" if !morwen.nicknamed?
    end
    @lamp_hold = false
    pbBGMStop(0.5) rescue nil
    return true
  end

  def finish
    @line = nil
    ok = (defined?(Prismfall::Interlude)) ? Prismfall::Interlude.finish : false
    leg = (pfm_get(:il1_juno_leg) rescue nil)
    if leg
      pfm_set(:juno_leg, leg)                   # she falls in again on the next map entry (juno_sync)
      pfm_set(:il1_juno_leg, nil)
    end
    dispose_beam
    return ok
  end

  # K2's level for his Honedge (the script's "K2"), from PBS; 21 if the trainer isn't compiled.
  def k2_level
    ver = (Prismfall::Rival.version_for(2) rescue 20)
    data = (GameData::Trainer.try_get(:RIVAL_KESTREL, "Kestrel", ver) rescue nil)
    row = data&.pokemon&.find { |p| p[:species] == :HONEDGE }
    return (row) ? row[:level] : 21
  end

  #-----------------------------------------------------------------------------
  # The Haunter on the stair
  #-----------------------------------------------------------------------------
  def haunter
    lv = k2_level + 3
    pk = Pokemon.new(:HAUNTER, lv)
    moves = [:SHADOWPUNCH, :HYPNOSIS, :NIGHTSHADE, :SUCKERPUNCH].select { |m| GameData::Move.exists?(m) }
    if moves.length == 4
      pk.forget_all_moves
      moves.each { |m| pk.learn_move(m) }
    end
    pk.calc_stats
    @line = { :species => :HONEDGE,
              :text => _INTL("Kestrel: Hold. Hold it. She held a line for a whole city once, everyone says. You can hold a staircase.") }
    setBattleRule("cannotRun")
    setBattleRule("disablePokeBalls")
    setBattleRule("canLose")
    won = WildBattle.start(pk)
    @line = nil
    $player.party.each { |p| p&.heal } if !won      # "the interlude restarts at the stair"
    return (won) ? true : false
  end

  # Battle#pbCommandPhase calls this: the pending line, once, when its species is the active battler.
  def say_line(battle)
    bl = @line
    return false if !bl || !battle
    b = battle.battlers.compact.find { |x| !x.opposes? && !x.fainted? && x.isSpecies?(bl[:species]) }
    return false if !b
    @line = nil
    battle.pbDisplayPaused(bl[:text])
    return true
  end

  #-----------------------------------------------------------------------------
  # Screen-space scenes: shared pieces
  #-----------------------------------------------------------------------------
  def tick
    Graphics.update
    Input.update
    pbUpdateSceneMap
  end

  # runs the block every frame for `seconds`, with k = 0..1
  def over(seconds)
    t0 = System.uptime
    loop do
      k = [(System.uptime - t0) / seconds, 1.0].min
      yield k
      tick
      break if k >= 1.0
    end
  end

  def ease(k); return 0.5 - (0.5 * Math.cos(Math::PI * k)); end

  def charset_bitmap(*names)
    names.flatten.compact.each do |n|
      next if !pbResolveBitmap("Graphics/Characters/#{n}")
      return RPG::Cache.load_bitmap("Graphics/Characters/", n)
    end
    return nil
  end

  # a soft round light, white in the middle
  def radial(radius, color)
    bmp = Bitmap.new(radius * 2, radius * 2)
    steps = 24
    steps.times do |i|
      r = radius - (i * radius / steps)
      a = ((i + 1) * 255 / steps)
      a = (a * a) / 255
      c = Color.new(color.red, color.green, color.blue, a)
      y0 = radius - r
      (0...(r * 2)).step(2) do |dy|
        yy = dy - r
        half = Math.sqrt([(r * r) - (yy * yy), 0].max).floor
        bmp.fill_rect(radius - half, y0 + dy, half * 2, 2, c)
      end
    end
    return bmp
  end

  def figure(vp, bmp, row, zoom, x, y, z, tint)
    s = Sprite.new(vp)
    s.bitmap = bmp
    cw = bmp.width / 4
    ch = bmp.height / 4
    s.src_rect = Rect.new(0, row * ch, cw, ch)
    s.ox = cw / 2
    s.oy = ch
    s.zoom_x = s.zoom_y = zoom
    s.x = x
    s.y = y
    s.z = z
    s.color = tint if tint
    return s
  end

  def step_frame(s, pattern)
    cw = s.bitmap.width / 4
    r = s.src_rect
    s.src_rect = Rect.new((pattern % 4) * cw, r.y, r.width, r.height)       # keeps a cropped (legs only) row
  end

  #-----------------------------------------------------------------------------
  # MEMORY: a crowd, enormous, and lights. A small boy's height: everything is legs and coats. A woman in a
  # veil running, away from him, toward something so bright you can't look at it. A kid. A kid made of light-
  #-----------------------------------------------------------------------------
  CROWD = ["NPC 03", "NPC 08", "NPC 12", "NPC 13", "NPC 17", "NPC 19", "NPC 21", "NPC 26", "NPC 11", "NPC 14"]

  def memory
    soft = safe?
    w = Graphics.width
    h = Graphics.height
    vp = Viewport.new(0, 0, w, h)
    vp.z = 99990
    made = []
    wash = Sprite.new(vp)
    wash.bitmap = Bitmap.new(w, h)
    wash.bitmap.fill_rect(0, 0, w, h, Color.new(198, 200, 208))
    wash.opacity = 0
    made << wash.bitmap
    glow_bmp = radial(96, Color.new(255, 240, 196))
    made << glow_bmp
    glow = Sprite.new(vp)
    glow.bitmap = glow_bmp
    glow.ox = glow.oy = 96
    glow.x = w / 2
    glow.y = (h * 0.34).round
    glow.z = 5
    glow.blend_type = 1
    glow.zoom_x = glow.zoom_y = 0.4
    glow.opacity = 0
    # the crowd: three depths, a lane left open up the middle. Backs to us: they are all looking at the lights.
    crowd = []
    # depth 0: right beside him, hems and legs only, half off the screen. 1: a row of backs. 2, 3: the crowd beyond.
    lanes = [[0.02, 0], [0.98, 0], [0.19, 1], [0.81, 1], [0.31, 2], [0.69, 2], [0.10, 2], [0.90, 2],
             [0.38, 3], [0.62, 3], [0.24, 3], [0.76, 3], [0.05, 3], [0.95, 3]]
    lanes.each_with_index do |(fx, depth), i|
      bmp = charset_bitmap(CROWD[i % CROWD.length], "NPC 01")
      next if !bmp
      zoom, foot, z, dark, tone = [[8.0, h + 24, 30, 240, 26], [5.0, h + 2, 20, 215, 44], [3.2, h - 58, 12, 190, 70],
                                   [2.2, h - 104, 10, 170, 104]][depth]
      s = figure(vp, bmp, (i % 5 == 3) ? 2 : 3, zoom, (w * fx).round, foot, z, Color.new(tone, tone + 2, tone + 12, dark))
      if depth == 0                                # a small boy's height: coats and legs, no faces
        ch = bmp.height / 4
        s.src_rect = Rect.new(s.src_rect.x, s.src_rect.y + (ch * 2 / 5), s.src_rect.width, ch - (ch * 2 / 5))
        s.oy = s.src_rect.height
      end
      s.opacity = 0
      crowd << [s, s.x, i * 1.7, (depth == 0) ? 7.0 : 3.0]
    end
    # the woman in the veil, running away up the lane
    veil_bmp = charset_bitmap("MORWEN", "trainer_CHANNELER", "NPC 19")
    woman = (veil_bmp) ? figure(vp, veil_bmp, 3, 4.2, w / 2, h + 30, 15, Color.new(10, 10, 20, 150)) : nil
    woman.opacity = 0 if woman
    # the kid made of light: the shape is the one the PC walks in
    look = (GameData::PlayerMetadata.get($player.character_ID || 1).pf_interlude_walk_charset rescue nil)
    look ||= (GameData::PlayerMetadata.get($player.character_ID || 1).walk_charset rescue nil)
    kid_bmp = charset_bitmap(look, "trainer_PLAYER_A", "NPC 01")
    kid = []
    if kid_bmp
      [[-2, 0], [2, 0], [0, -2], [0, 2]].each do |dx, dy|
        k = figure(vp, kid_bmp, 0, 2.0, (w / 2) + dx, glow.y + 44 + dy, 40, Color.new(255, 206, 110, 255))
        k.opacity = 0
        kid << k
      end
      k = figure(vp, kid_bmp, 0, 2.0, w / 2, glow.y + 44, 41, Color.new(255, 255, 255, 255))
      k.opacity = 0
      kid << k
    end
    pbSEPlay("Anim/Saint7", 70, 70) rescue nil
    # 1. the room goes white-grey; the crowd comes up out of it
    over((soft) ? 1.4 : 0.8) do |k|
      wash.opacity = (255 * k).round
      crowd.each { |c| c[0].opacity = (255 * ease(k)).round }
    end
    pbSEPlay("Anim/Wind8", 60, 60) rescue nil
    # 2. she runs; the light opens ahead of her
    t0 = System.uptime
    run = (soft) ? 4.6 : 3.8
    over(run) do |k|
      t = System.uptime - t0
      crowd.each do |s, x0, ph, amp|
        s.x = (x0 + (Math.sin((t * 1.6) + ph) * amp)).round
        step_frame(s, ((t * 2.0) + ph).floor) if amp > 5
      end
      e = ease(k)
      if woman
        woman.opacity = [(k * 900).round, 255].min
        woman.zoom_x = woman.zoom_y = 4.2 - (3.1 * e)
        woman.y = (h + 30 - ((h + 30 - (glow.y + 52)) * e)).round
        woman.x = ((w / 2) + (Math.sin(t * 9.0) * 3 * (1.0 - e))).round
        step_frame(woman, (t * 9.0).floor)
        woman.color = Color.new(10, 10, 20, 150 + (70 * e).round)
      end
      glow.opacity = [((soft) ? 150 : 255) * e * 1.3, (soft) ? 150 : 255].min.round
      glow.zoom_x = glow.zoom_y = 0.4 + (((soft) ? 1.6 : 2.6) * e)
    end
    # 3. a kid. a kid made of light-
    pbSEPlay("Anim/Saint9", 80, 120) rescue nil
    over((soft) ? 1.6 : 1.1) do |k|
      kid.each { |s| s.opacity = (255 * ease(k)).round }
      woman.opacity = (255 * (1.0 - k)).round if woman
      glow.zoom_x = glow.zoom_y = glow.zoom_x + 0.01
    end
    over(0.5) { |_k| }
    # 4. it stops
    if soft
      over(0.9) do |k|
        a = (255 * (1.0 - k)).round
        ([wash, glow] + kid + crowd.map { |c| c[0] }).each { |s| s.opacity = [s.opacity, a].min }
      end
    else
      wash.bitmap.fill_rect(0, 0, w, h, Color.new(255, 255, 255))
      wash.z = 90
      3.times { tick }
    end
    pbSEStop rescue nil
    vp.dispose
    made.each { |b| b.dispose if !b.disposed? }
    return true
  end

  #-----------------------------------------------------------------------------
  # From the gallery: a small boat with no lights slips out under the harbour chain, past the Concert's cutters.
  # A stocky shape at the tiller. A glint of gold tooth.
  #-----------------------------------------------------------------------------
  def boat
    soft = safe?
    w = Graphics.width
    h = Graphics.height
    vp = Viewport.new(0, 0, w, h)
    vp.z = 99990
    pw = w - 96
    ph = 150
    px = 48
    py = 40
    frame = Sprite.new(vp)
    frame.bitmap = Bitmap.new(pw + 8, ph + 8)
    frame.bitmap.fill_rect(0, 0, pw + 8, ph + 8, Color.new(16, 14, 20))
    frame.bitmap.fill_rect(2, 2, pw + 4, ph + 4, Color.new(92, 74, 52))        # the gallery window's timber
    frame.bitmap.fill_rect(4, 4, pw, ph, Color.new(8, 12, 26))
    frame.x = px - 4
    frame.y = py - 4
    pvp = Viewport.new(px, py, pw, ph)                                         # the pane: everything in it is clipped
    pvp.z = 99991
    sea = Sprite.new(pvp)
    sea.bitmap = Bitmap.new(pw, ph)
    b = sea.bitmap
    horizon = 52
    horizon.times { |y| b.fill_rect(0, y, pw, 1, Color.new(10 + (y / 6), 14 + (y / 5), 34 + (y / 3))) }           # night sky
    (ph - horizon).times { |y| b.fill_rect(0, horizon + y, pw, 1, Color.new(14 + (y / 10), 30 + (y / 6), 52 + (y / 4))) }
    [[30, 10], [88, 22], [150, 8], [214, 30], [270, 14], [330, 24], [372, 9]].each { |sx, sy| b.fill_rect(sx % pw, sy, 2, 2, Color.new(200, 206, 230)) }
    b.fill_rect(0, horizon - 12, 70, 12, Color.new(4, 6, 12))                  # the harbour mole, left
    b.fill_rect(pw - 54, horizon - 9, 54, 9, Color.new(4, 6, 12))              # and right
    (70...(pw - 54)).step(9) { |x| b.fill_rect(x, horizon + 6 + ((x / 9) % 2), 5, 2, Color.new(70, 64, 60)) }     # the chain
    # the Concert's cutters, lanterns lit
    [[pw * 0.26, horizon + 26], [pw * 0.78, horizon + 40]].each do |cx, cy|
      cx = cx.round
      b.fill_rect(cx - 22, cy, 44, 7, Color.new(70, 74, 92))
      b.fill_rect(cx - 16, cy + 7, 32, 3, Color.new(46, 50, 66))
      b.fill_rect(cx - 1, cy - 30, 2, 30, Color.new(70, 74, 92))
      b.fill_rect(cx + 1, cy - 28, 14, 18, Color.new(190, 190, 200, 120))
      b.fill_rect(cx - 20, cy - 5, 4, 4, Color.new(255, 214, 120))
      b.fill_rect(cx - 21, cy + 9, 6, 1, Color.new(255, 214, 120, 110))
    end
    sea.z = 1
    lights = Sprite.new(pvp)                                                   # the lamp's sweep on the water
    lights.bitmap = Bitmap.new(90, ph - horizon)
    90.times { |x| a = (60 * Math.sin(Math::PI * x / 90.0)).round; lights.bitmap.fill_rect(x, 0, 1, ph - horizon, Color.new(255, 236, 170, a)) }
    lights.y = horizon
    lights.z = 2
    lights.blend_type = 1
    boatspr = Sprite.new(pvp)
    boatspr.bitmap = Bitmap.new(30, 18)
    bb = boatspr.bitmap
    bb.fill_rect(2, 11, 26, 5, Color.new(2, 3, 6))                             # hull, no lights
    bb.fill_rect(5, 16, 20, 2, Color.new(2, 3, 6))
    bb.fill_rect(20, 3, 6, 8, Color.new(2, 3, 6))                              # a stocky shape at the tiller
    bb.fill_rect(21, 0, 4, 4, Color.new(2, 3, 6))
    boatspr.z = 3
    tooth = Sprite.new(pvp)
    tooth.bitmap = Bitmap.new(2, 2)
    tooth.bitmap.fill_rect(0, 0, 2, 2, Color.new(255, 214, 90))
    tooth.z = 4
    tooth.opacity = 0
    all = [frame, sea, lights, boatspr, tooth]
    all.each { |s| s.opacity = 0 if s != tooth }
    over(0.5) { |k| all.each { |s| s.opacity = (255 * k).round if s != tooth } }
    glint_at = 0.62
    over((soft) ? 7.0 : 6.0) do |k|
      bx = 96 + ((pw - 190) * k)
      by = horizon + 30 - (26 * k) + (Math.sin(k * 26) * 1.5)                  # out, under the chain
      boatspr.x = bx.round
      boatspr.y = by.round
      lights.x = ((((k * 1.7) % 1.0) * (pw + 90)) - 90).round
      g = (k - glint_at).abs
      tooth.x = boatspr.x + 22
      tooth.y = boatspr.y + 2
      tooth.opacity = (g < 0.035) ? ((1.0 - (g / 0.035)) * 255).round : 0
      pbSEPlay("Mining ping", 60, 150) if !@glinted && k >= glint_at
      @glinted = true if k >= glint_at
    end
    @glinted = false
    over(0.5) { |k| all.each { |s| s.opacity = (255 * (1.0 - k)).round if s != tooth } }
    all.each { |s| s.bitmap.dispose; s.dispose }
    pvp.dispose
    vp.dispose
    return true
  end

  #-----------------------------------------------------------------------------
  # The great lamp turns: a warm band of light crosses the room every few seconds (inside the map viewport, so
  # screen tones and fades take it with them). Fainter one floor down.
  #-----------------------------------------------------------------------------
  def lamp(on); @lamp_hold = !on; dispose_beam if !on; return true; end

  def dispose_beam
    if @beam && !@beam.disposed?
      @beam.bitmap.dispose if @beam.bitmap && !@beam.bitmap.disposed?
      @beam.dispose
    end
    @beam = nil
  end

  ROOM = { 106 => [1, 2, 12, 11], 105 => [3, 3, 17, 13] }       # x0, y0, x1, y1 in tiles: where the band shows

  def beam_update
    on = running? && !@lamp_hold && $game_map && MAPS.include?($game_map.map_id) && $scene.is_a?(Scene_Map)
    if !on
      dispose_beam if @beam
      return
    end
    if !@beam || @beam.disposed?
      bw = 190
      @beam = Sprite.new(Spriteset_Map.viewport)
      @beam.bitmap = Bitmap.new(bw, Graphics.height)
      bw.times do |x|
        a = (Math.sin(Math::PI * x / bw.to_f)**2 * 255).round
        @beam.bitmap.fill_rect(x, 0, 1, Graphics.height, Color.new(255, 232, 160, a))
      end
      @beam.z = 9000
      @beam.blend_type = 1
    end
    top = ($game_map.map_id == 106)
    period = (top) ? 5.0 : 6.5
    peak = (top) ? 120 : 46
    peak /= 2 if safe?
    k = (System.uptime % period) / period
    sweep = 0.42
    if k > sweep
      @beam.opacity = 0
    else
      p = k / sweep
      x0, y0, x1, y1 = ROOM[$game_map.map_id]
      left = ((x0 * Game_Map::REAL_RES_X) - $game_map.display_x) / Game_Map::X_SUBPIXELS
      right = ((x1 * Game_Map::REAL_RES_X) - $game_map.display_x) / Game_Map::X_SUBPIXELS
      top = ((y0 * Game_Map::REAL_RES_Y) - $game_map.display_y) / Game_Map::Y_SUBPIXELS
      bottom = ((y1 * Game_Map::REAL_RES_Y) - $game_map.display_y) / Game_Map::Y_SUBPIXELS
      bx = (left - 190 + ((right - left + 190) * p)).round
      a = [bx, left].max
      b = [bx + 190, right].min
      if b <= a
        @beam.opacity = 0
      else
        @beam.src_rect = Rect.new(a - bx, 0, b - a, [bottom - top, Graphics.height].min)
        @beam.x = a
        @beam.y = top
        @beam.opacity = (peak * Math.sin(Math::PI * p)).round
      end
    end
  end
end

EventHandlers.add(:on_frame_update, :prismfall_lamplight_beam,
  proc { PrismfallLamplight.beam_update if $game_variables && $game_variables[PrismfallLamplight::VAR] == 1 || PrismfallLamplight.instance_variable_get(:@beam) }
)

# The lighthouse is quiet for the interlude: its maps don't start their daytime BGM.
class Game_Map
  alias pf_lamplight_autoplay autoplay unless method_defined?(:pf_lamplight_autoplay)
  def autoplay
    return if PrismfallLamplight.running? && PrismfallLamplight::MAPS.include?(@map_id)
    pf_lamplight_autoplay
  end

  alias pf_lamplight_autoplayAsCue autoplayAsCue unless method_defined?(:pf_lamplight_autoplayAsCue)
  def autoplayAsCue
    return if PrismfallLamplight.running? && PrismfallLamplight::MAPS.include?(@map_id)
    pf_lamplight_autoplayAsCue
  end
end

class Battle
  alias pf_lamplight_pbCommandPhase pbCommandPhase unless method_defined?(:pf_lamplight_pbCommandPhase)
  def pbCommandPhase
    PrismfallLamplight.say_line(self) rescue nil
    pf_lamplight_pbCommandPhase
  end
end

# Night in the lighthouse while it runs (the maps' own tones are daylight).
if defined?(PrismfallStaging)
  PrismfallStaging.tone_rule do
    night = PrismfallLamplight.running? && $game_map && PrismfallLamplight::MAPS.include?($game_map.map_id)
    (night) ? Tone.new(-72, -64, -22, 44) : nil
  end
end

def pfm_il1_start;        return PrismfallLamplight.start;    end
def pfm_il1_end;          return PrismfallLamplight.finish;   end
def pfm_il1_memory;       return PrismfallLamplight.memory;   end
def pfm_il1_haunter;      return PrismfallLamplight.haunter;  end
def pfm_il1_boat;         return PrismfallLamplight.boat;     end
def pfm_il1_lamp(on = true); return PrismfallLamplight.lamp(on); end

# Title cards (the Cutscenes plugin draws them; pfm_card falls back to message boxes without it)
if defined?(Prismfall::Cutscene) && Prismfall::Cutscene.respond_to?(:define)
  Prismfall::Cutscene.define(:PF_IL1_CARD) do
    background :color, color: [0, 0, 0]
    text "The same night. Ferrow's Landing."
  end
  Prismfall::Cutscene.define(:PF_ACT1_END) do
    background :color, color: [0, 0, 0]
    title "END OF ACT I"
  end
  Prismfall::Cutscene.define(:PF_ACT2_TITLE) do
    background :color, color: [0, 0, 0]
    title "II — IMPRINTS"
  end
end
