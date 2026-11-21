#===============================================================================
# Prismfall EBDX Bridge - trainer battle start, modelled frame by frame on the creator's reference
# video (2026-11-21): Pokemon Black 2/White 2, Elite Four Shauntal.
#
# VS screen (replaces EBDX's Poke Ball + split transition for named cast trainers):
#   0.00  two white flash pulses on the overworld, then a full white-out
#   1.15  white clears to a darkened overworld; two lightning bolts streak across
#         (top one from the right, bottom one from the left) and crackle
#   2.05  the opponent's bust slides in top-right, the player's bottom-left
#   2.40  "S" drops from above and "V" rises from below; they lock into "VS."
#   2.80  white flash: the final screen - radial warp tunnel behind, opponent band on top
#         (name top-left), player band below (name bottom-right), a faint Poke Ball emblem
#         across both, sparks off the VS
#   5.20  bands split up/down, V and S part left/right, the tunnel collapses into black
# Battle start (also from the video):
#   the camera opens close on the trainer's black silhouette and sweeps back to the field as the
#   colour comes in; the party bar fills; "You are challenged by ...!" shows WHILE the trainer's
#   Graphics/Trainers strip plays its one-shot pose (it holds the last frame afterwards).
#
# Who gets it: a single opposing trainer whose cast ID has a bust. Cast ID = the trainer's name
# in capitals ("Juno" -> JUNO), or VS_IDS[trainer type]. Bust = Graphics/EBDX/VS/<ID>.png (dedicated
# 256x136 VS art) or, until that exists, the 96x96 dialogue portrait at 1.5x.
# Generic trainers keep EBDX's normal transition. UI art: tools/vs/make_vs_assets.py.
#===============================================================================
module PrismfallVS
  ENABLED    = true
  OFF_SWITCH = nil                 # a game switch that turns the VS screen off (e.g. for a cutscene battle)
  VS_IDS     = {}                  # trainer type => cast ID when the name doesn't match (e.g. :HOLLOW_SABLE => "KROLL")
  THEMES     = {                   # colour per cast ID (graphics/EBDX/VS/{tunnel,bandfoe,bandplayer}_<theme>.png)
    "PLAYER_A" => :teal, "PLAYER_B" => :green,
    "JUNO" => :rose, "KESTREL" => :blue, "DORIAN" => :violet, "TAMSIN" => :gold,
    "LARCH" => :grey, "MARISOL" => :blue, "BRANN" => :red, "CELESTINE" => :violet,
    "VOSS" => :grey, "MARCHETTI" => :red, "KROLL" => :red, "ROWAN" => :green
  }
  DEFAULT_THEME_FOE    = :violet
  DEFAULT_THEME_PLAYER = :teal
  # Layout (512x384), measured off the reference
  TOP_Y = 40; BOT_Y = 208; BAND_H = 136
  BOLT_TOP_Y = 108; BOLT_BOT_Y = 276
  VS_CX = 256; VS_CY = 192; VS_SPLIT = 56             # EBDX's "VS." art: V is columns 0..55, S the rest
  FOE_BUST_CX = 392; PLAYER_BUST_CX = 120
  EMBLEM_CX = 240; EMBLEM_CY = 192
  PORTRAIT_ZOOM = 1.5             # 96x96 portrait (48 native px doubled) -> 144px = 3 screen px per art px
  HOLD_END = 5.2                  # seconds: when the finished screen starts to leave
  POSE_SECONDS = 1.6              # the trainer's one-shot pose, played during the challenge line
  INTRO_ZOOM = 3.0                # how close the battle opens on the trainer's silhouette

  @hold_pose = false
  @input_block_until = 0
  class << self; attr_accessor :hold_pose, :input_block_until; end

  def self.dir; return "Graphics/EBDX/VS"; end

  def self.cast_id(trainer)
    return nil if !trainer
    id = VS_IDS[trainer.trainer_type]
    id ||= trainer.name.to_s.upcase.gsub(/[^A-Z0-9_]/, "")
    return (id.nil? || id.empty?) ? nil : id
  end

  def self.player_id
    tt = ($player ? $player.trainer_type.to_s : "")
    return "PLAYER_B" if tt.end_with?("PLAYER_B")
    return "PLAYER_B" if !tt.include?("PLAYER") && ($player.female? rescue false)
    return "PLAYER_A"
  end

  # [file, zoom] of the bust for a cast ID, or nil
  def self.bust(id)
    return nil if !id
    return ["#{dir}/#{id}", 1.0] if pbResolveBitmap("#{dir}/#{id}")
    return ["Graphics/Portraits/#{id}", PORTRAIT_ZOOM] if pbResolveBitmap("Graphics/Portraits/#{id}")
    return nil
  end

  def self.applies?(battle_type, foe)
    return false if !ENABLED || !foe || foe.length != 1 || battle_type.even?
    return false if OFF_SWITCH && $game_switches[OFF_SWITCH]
    return false if !pbResolveBitmap("#{dir}/bolt0") || !pbResolveBitmap("Graphics/EBDX/Transitions/Common/vs")
    return !bust(cast_id(foe[0])).nil?
  end

  def self.themed(kind, theme)
    f = "#{dir}/#{kind}_#{theme}"
    f = "#{dir}/#{kind}_violet" if !pbResolveBitmap(f)
    return RPG::Cache.load_bitmap("", f)
  end

  def self.ease_out(t); t = t.clamp(0.0, 1.0); return 1 - (1 - t)**3; end
  def self.ease_in(t);  t = t.clamp(0.0, 1.0); return t * t * t; end
  def self.prog(t, a, b); return ((t - a) / (b - a)).clamp(0.0, 1.0); end
  def self.pulse(t, a, peak, b, top = 255)            # 0 -> top (a..peak) -> 0 (peak..b)
    return 0 if t < a || t > b
    return top * prog(t, a, peak) if t < peak
    return top * (1 - prog(t, peak, b))
  end

  #=============================================================================
  class Sequence
    def initialize(viewport, trainer)
      @vp = viewport
      @trainer = trainer
      @s = {}
      @home = {}
      @foe_id = PrismfallVS.cast_id(trainer)
      @pl_id = PrismfallVS.player_id
      @foe_theme = THEMES[@foe_id] || DEFAULT_THEME_FOE
      @pl_theme = THEMES[@pl_id] || DEFAULT_THEME_PLAYER
      w = Graphics.width; h = Graphics.height
      base_z = @vp.z
      # --- the overworld, darkened
      @s["world"] = Sprite.new(@vp); @s["world"].snap_screen; @s["world"].z = 1
      @s["dim"] = Sprite.new(@vp); @s["dim"].bitmap = Bitmap.new(w, h)
      @s["dim"].bitmap.fill_rect(0, 0, w, h, Color.new(2, 2, 8)); @s["dim"].opacity = 0; @s["dim"].z = 2
      # --- the warp tunnel (the final screen's background), two layers turning opposite ways
      %w[tunnel tunnel2].each_with_index do |k, i|
        t = Sprite.new(@vp)
        t.bitmap = PrismfallVS.themed("tunnel", @foe_theme)
        t.ox = t.bitmap.width / 2; t.oy = t.bitmap.height / 2
        t.x = VS_CX; t.y = VS_CY; t.z = 3 + i
        t.mirror = (i == 1); t.opacity = (i == 1) ? 110 : 255
        @s[k] = t
      end
      @s["hole"] = Sprite.new(@vp)
      @s["hole"].bitmap = hole_bitmap(160)
      @s["hole"].ox = 80; @s["hole"].oy = 80; @s["hole"].x = VS_CX; @s["hole"].y = VS_CY
      @s["hole"].zoom_x = @s["hole"].zoom_y = 0; @s["hole"].z = 6
      # --- lightning (before the final screen)
      @bolts = [0, 1, 2].map { |i| RPG::Cache.load_bitmap("", "#{PrismfallVS.dir}/bolt#{i}") }
      @s["boltT"] = Sprite.new(@vp); @s["boltB"] = Sprite.new(@vp)
      [["boltT", BOLT_TOP_Y], ["boltB", BOLT_BOT_Y]].each do |k, y|
        @s[k].bitmap = @bolts[0]; @s[k].y = y - @bolts[0].height / 2; @s[k].z = 8
        @s[k].src_rect = Rect.new(0, 0, 0, @bolts[0].height)
      end
      # --- the two bands: own viewports so busts, emblem and names are clipped to them
      @top = Viewport.new(0, TOP_Y, w, BAND_H); @top.z = base_z + 1
      @bot = Viewport.new(0, BOT_Y, w, BAND_H); @bot.z = base_z + 1
      @s["bgT"] = Sprite.new(@top); @s["bgT"].bitmap = PrismfallVS.themed("bandfoe", @foe_theme)
      @s["bgB"] = Sprite.new(@bot); @s["bgB"].bitmap = PrismfallVS.themed("bandplayer", @pl_theme)
      emb = RPG::Cache.load_bitmap("", "#{PrismfallVS.dir}/emblem")
      [["embT", @top, TOP_Y], ["embB", @bot, BOT_Y]].each do |k, v, by|
        @s[k] = Sprite.new(v); @s[k].bitmap = emb; @s[k].z = 2
        @s[k].x = EMBLEM_CX - emb.width / 2; @s[k].y = EMBLEM_CY - emb.height / 2 - by
      end
      @s["bustT"] = make_bust(@top, @foe_id, FOE_BUST_CX)
      @s["bustB"] = make_bust(@bot, @pl_id, PLAYER_BUST_CX)
      @s["nameT"] = name_sprite(@top, @trainer.name.to_s, 14, 6, :left)
      @s["nameB"] = name_sprite(@bot, ($player ? $player.name : ""), w - 14, BAND_H - 40, :right)
      @final = %w[bgT bgB embT embB nameT nameB tunnel tunnel2]
      @final.each { |k| @s[k].visible = false }
      # --- over everything: VS halves, sparks, white, black
      @over = Viewport.new(0, 0, w, h); @over.z = base_z + 2
      vsb = RPG::Cache.load_bitmap("", "Graphics/EBDX/Transitions/Common/vs")
      @vs_w = vsb.width; @vs_h = vsb.height
      @s["V"] = Sprite.new(@over); @s["V"].bitmap = vsb; @s["V"].src_rect = Rect.new(0, 0, VS_SPLIT, vsb.height)
      @s["S"] = Sprite.new(@over); @s["S"].bitmap = vsb; @s["S"].src_rect = Rect.new(VS_SPLIT, 0, vsb.width - VS_SPLIT, vsb.height)
      @v_home = [VS_CX - @vs_w / 2, VS_CY - @vs_h / 2]
      @s_home = [VS_CX - @vs_w / 2 + VS_SPLIT, VS_CY - @vs_h / 2]
      %w[V S].each { |k| @s[k].z = 20; @s[k].visible = false }
      spk = RPG::Cache.load_bitmap("", "#{PrismfallVS.dir}/spark")
      @sparks = (0...14).map do |i|
        sp = Sprite.new(@over); sp.bitmap = spk; sp.ox = spk.width / 2; sp.oy = spk.height / 2; sp.z = 25
        sp.visible = false
        a = (i * 360.0 / 14 + rand(18)) * Math::PI / 180
        [sp, Math.cos(a), Math.sin(a), 70 + rand(80)]
      end
      @s["white"] = Sprite.new(@over); @s["white"].bitmap = Bitmap.new(w, h)
      @s["white"].bitmap.fill_rect(0, 0, w, h, Color.new(255, 255, 255)); @s["white"].opacity = 0; @s["white"].z = 50
      @s["black"] = Sprite.new(@over); @s["black"].bitmap = Bitmap.new(w, h)
      @s["black"].bitmap.fill_rect(0, 0, w, h, Color.new(0, 0, 0)); @s["black"].opacity = 0; @s["black"].z = 60
    end

    def hole_bitmap(d)
      b = Bitmap.new(d, d); r = d / 2
      (0...d).each do |y|
        dy = y - r + 0.5
        next if dy.abs >= r
        hw = Math.sqrt(r * r - dy * dy)
        b.fill_rect((r - hw).floor, y, (hw * 2).ceil, 1, Color.new(0, 0, 0))
      end
      return b
    end

    def make_bust(vp, id, cx)
      file, zoom = PrismfallVS.bust(id)
      s = Sprite.new(vp); s.z = 5
      return s if !file
      s.bitmap = RPG::Cache.load_bitmap("", file)
      s.zoom_x = s.zoom_y = zoom
      bw = (s.bitmap.width * zoom).round; bh = (s.bitmap.height * zoom).round
      s.x = (cx - bw / 2).round
      s.y = BAND_H - bh                        # bottom flush with the band, top cropped by it
      s.visible = false
      @home[s] = s.x
      return s
    end

    def name_sprite(vp, text, x, y, align)
      s = Sprite.new(vp); s.bitmap = Bitmap.new(Graphics.width, 40); s.z = 8
      pbSetSystemFont(s.bitmap)
      pbDrawTextPositions(s.bitmap, [[text, x, 6, align, Color.new(248, 248, 248), Color.new(40, 40, 48), :outline]])
      s.y = y
      return s
    end

    def play
      t0 = System.uptime
      cues = { 0.12 => "Vs flash", 1.3 => "Vs sword", 2.8 => "Vs flash" }
      loop do
        t = System.uptime - t0
        cues.keys.each { |k| next if t < k; (pbSEPlay(cues.delete(k)) rescue nil) }
        frame(t)
        Graphics.update
        break if t >= HOLD_END + 0.75
      end
      @vp.color = Color.new(0, 0, 0, 255)
      dispose
      Graphics.update
    end

    def frame(t)
      e = PrismfallVS
      # 0.00-1.32: flash, flash, white-out, clears to a darkened overworld (+ the reveal flash at 2.8)
      @s["white"].opacity = [e.pulse(t, 0.10, 0.22, 0.36, 225), e.pulse(t, 0.42, 0.54, 0.68, 225),
                             (t >= 0.72 && t < 1.15) ? 255 * e.prog(t, 0.72, 0.82) : 0,
                             (t >= 1.15 && t < 1.4) ? 255 * (1 - e.prog(t, 1.15, 1.32)) : 0,
                             e.pulse(t, 2.76, 2.80, 3.05, 255)].max
      @s["dim"].opacity = 228 * e.prog(t, 0.72, 0.9)
      # 1.30-2.80: lightning streaks in and crackles
      if t < 2.8
        grow = e.ease_out(e.prog(t, 1.3, 1.52))
        bw = @bolts[0].width; bh = @bolts[0].height
        vis = (bw * grow).round
        idx = ((t * 20).to_i % 3)
        jit = (t > 1.52) ? ((t * 30).to_i.even? ? 1 : -1) : 0
        @s["boltT"].bitmap = @bolts[idx]; @s["boltB"].bitmap = @bolts[(idx + 1) % 3]
        @s["boltT"].src_rect = Rect.new(bw - vis, 0, vis, bh); @s["boltT"].x = bw - vis
        @s["boltB"].src_rect = Rect.new(0, 0, vis, bh); @s["boltB"].x = 0
        @s["boltT"].y = BOLT_TOP_Y - bh / 2 + jit
        @s["boltB"].y = BOLT_BOT_Y - bh / 2 - jit
      else
        @s["boltT"].visible = @s["boltB"].visible = false
      end
      # 2.05: busts slide in (foe from the right, player from the left)
      b = e.ease_out(e.prog(t, 2.05, 2.28))
      [["bustT", 1], ["bustB", -1]].each do |k, dir|
        sp = @s[k]; next if !@home[sp]
        sp.visible = t >= 2.05
        sp.x = (@home[sp] + dir * 280 * (1 - b)).round
      end
      # 2.40: S drops, V rises, both shrinking into place
      if t >= 2.4 && t < HOLD_END
        @s["V"].visible = @s["S"].visible = true
        v = e.ease_out(e.prog(t, 2.4, 2.72))
        z = 3.4 - 2.4 * v
        j = (t >= 2.8 && (t * 12).to_i.odd?) ? 1 : 0      # a one-pixel shimmy once it's locked
        @s["S"].zoom_x = @s["S"].zoom_y = z
        @s["V"].zoom_x = @s["V"].zoom_y = z
        @s["S"].x = @s_home[0] - ((z - 1) * 40).round + j
        @s["S"].y = (@s_home[1] - 260 * (1 - v)).round
        @s["V"].x = @v_home[0] - ((z - 1) * 60).round + j
        @s["V"].y = (@v_home[1] + 260 * (1 - v)).round
      end
      # 2.80: the final screen
      if t >= 2.8
        @final.each { |k| @s[k].visible = true }
        @s["world"].visible = @s["dim"].visible = false
        spin = t * 26.0
        pz = 1.0 + 0.03 * Math.sin(t * 6)
        @s["tunnel"].angle = spin
        @s["tunnel2"].angle = -spin * 0.7
        @s["tunnel"].zoom_x = @s["tunnel"].zoom_y = pz
        @s["tunnel2"].zoom_x = @s["tunnel2"].zoom_y = pz * 1.1
        @sparks.each do |sp, dx, dy, dist|
          u = e.prog(t, 2.82, 3.5)
          sp.visible = u > 0 && u < 1
          d = dist * e.ease_out(u)
          sp.x = VS_CX + (dx * d).round; sp.y = VS_CY + (dy * d * 0.7).round
          sp.opacity = 255 * (1 - u)
        end
      end
      # 5.20: bands part, VS parts, the tunnel collapses into black
      if t >= HOLD_END
        x = e.ease_in(e.prog(t, HOLD_END, HOLD_END + 0.22))
        @top.rect.y = (TOP_Y - (TOP_Y + BAND_H) * x).round
        @bot.rect.y = (BOT_Y + (Graphics.height - BOT_Y) * x).round
        @s["V"].x = @v_home[0] - (200 * x).round
        @s["S"].x = @s_home[0] + (200 * x).round
        k = e.ease_in(e.prog(t, HOLD_END + 0.15, HOLD_END + 0.45))
        @s["hole"].zoom_x = @s["hole"].zoom_y = 5.0 * k
        pz = 1.0 + 0.8 * k
        %w[tunnel tunnel2].each { |n| @s[n].zoom_x = @s[n].zoom_y = pz; @s[n].angle += 40 * k }
        @s["V"].opacity = @s["S"].opacity = 255 * (1 - k)
        @s["black"].opacity = 255 * e.prog(t, HOLD_END + 0.42, HOLD_END + 0.5)
      end
    end

    def dispose
      @s.each_value { |sp| sp.dispose if !sp.disposed? }
      @sparks.each { |sp, *_| sp.dispose if !sp.disposed? }
      [@top, @bot, @over].each { |v| v.dispose if !v.disposed? }
    end
  end
end

SpecialBattleIntroAnimations.register("prismfall_vs_screen", 90,
  proc { |battle_type, foe, location| next PrismfallVS.applies?(battle_type, foe) },
  proc { |viewport, battle_type, foe, location|
    begin
      PrismfallVS::Sequence.new(viewport, foe[0]).play
    rescue StandardError => e
      echoln("[Prismfall VS] #{e.class}: #{e.message}")
      viewport.color = Color.new(0, 0, 0, 255)
    end
  }
)

#===============================================================================
# Battle start: hold the trainer's pose strip on frame 0 through EBDX's intro sweep,
# then play it once (time-based) during "You are challenged by ...!".
#===============================================================================
class DynamicTrainerSprite
  alias pf_vs_play play unless method_defined?(:pf_vs_play)
  def play
    return if PrismfallVS.hold_pose          # the pose waits for the challenge line
    pf_vs_play
  end

  alias pf_vs_totalFrames totalFrames unless method_defined?(:pf_vs_totalFrames)
  def totalFrames
    return 24 if PrismfallVS.hold_pose        # EBDX's intro loop: long enough for the ~1 s sweep, not the strip
    return pf_vs_totalFrames
  end

  def pf_strip_frames
    return (@bitmap && @bitmap.respond_to?(:totalFrames)) ? @bitmap.totalFrames : 1
  end
end

class Battle::Scene
  alias pf_vs_startSceneAnimation startSceneAnimation unless method_defined?(:pf_vs_startSceneAnimation)
  def startSceneAnimation
    if @battle.trainerBattle? && @battle.opponent && @vector
      PrismfallVS.hold_pose = true
      # open closer on the silhouette than EBDX's default; EBDX then sweeps back to the field
      v = EliteBattle.get_vector(:ENEMY)
      v[4] = PrismfallVS::INTRO_ZOOM if v[4]
      @vector = Vector.new(*v[0, 6]); @vector.battle = @battle
    end
    pf_vs_startSceneAnimation
  end

  alias pf_vs_animateScene animateScene unless method_defined?(:pf_vs_animateScene)
  def animateScene(align = false, smanim = false, &block)
    pf_vs_animateScene(align, smanim, &block)
    pf_vs_update_pose
  end

  def pf_vs_start_pose
    return if @pf_pose_t0 || !@battle.opponent
    PrismfallVS.hold_pose = false
    @pf_pose_t0 = System.uptime
    @pf_pose_last = {}
  end

  def pf_vs_update_pose
    return if !@pf_pose_t0 || @pf_pose_done
    u = (System.uptime - @pf_pose_t0) / PrismfallVS::POSE_SECONDS
    @battle.opponent.each_index do |i|
      sp = @sprites["trainer_#{i}"]
      next if !sp || sp.disposed? || !sp.respond_to?(:pf_strip_frames)
      n = sp.pf_strip_frames
      f = [(u * n).floor, n - 1].min
      next if @pf_pose_last[i] == f
      @pf_pose_last[i] = f
      sp.setFrame(f)
    end
    @pf_pose_done = true if u >= 1
  end

  # "You are challenged by ...!": the pose plays while it shows, and the line can't be
  # dismissed before the pose has finished (as in B2W2).
  alias pf_vs_pbDisplayPausedMessage pbDisplayPausedMessage unless method_defined?(:pf_vs_pbDisplayPausedMessage)
  def pbDisplayPausedMessage(msg)
    if @battle.trainerBattle? && @battle.opponent && !@pf_pose_t0
      pf_vs_start_pose
      PrismfallVS.input_block_until = @pf_pose_t0 + PrismfallVS::POSE_SECONDS
    end
    pf_vs_pbDisplayPausedMessage(msg)
  end
end

module Input
  class << self
    alias pf_vs_trigger? trigger? unless method_defined?(:pf_vs_trigger?)
    def trigger?(button)
      if (button == Input::USE || button == Input::BACK) && System.uptime < PrismfallVS.input_block_until
        return false
      end
      return pf_vs_trigger?(button)
    end
  end
end

# The opening camera sweep runs slower than EBDX's default (~1 s back from the silhouette,
# like the reference) while the pose is being held.
class Vector
  alias pf_vs_set_inc inc= unless method_defined?(:pf_vs_set_inc)
  def inc=(val)
    val = [val, 0.028].min if PrismfallVS.hold_pose
    pf_vs_set_inc(val)
  end
end
