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
  VS_IDS     = {                   # trainer type => cast ID (ensures prefixed display names like "Prof. Larch" resolve)
    :RIVAL_JUNO     => "JUNO",
    :LEADER_JUNO    => "JUNO",
    :RIVAL_KESTREL  => "KESTREL",
    :LARCH          => "LARCH",
    :LEADER_DORIAN  => "DORIAN",
    :LEADER_TAMSIN  => "TAMSIN",
    :LEADER_MARISOL => "MARISOL",
    :HOLLOW_SABLE   => "SABLE",      # her undercover Hollow-cloak bust: no Meridian-suit spoiler before Ch13
    :MERIDIAN_KROLL => "KROLL",      # PBS name "Sabine"
    :MERIDIAN_MARCHETTI => "MARCHETTI",  # PBS name "Helene"
    :MERIDIAN_QUENT => "QUENT",      # PBS name "Percival"
    :HOLLOW_THISTLE => "THISTLE",
    :OCTAVE_VESPER  => "VESPER",
    :MERIDIAN_VOSS  => "VOSS",       # PBS name "Aurelian"
    :CHAMPION_VALEN => "VALEN",
    :HOLLOW_MOURNER => "MOURNER",
    :LEADER_ROOK    => "ROOK",
    :LEADER_SAHAR   => "SAHAR"
  }
  THEMES     = {                   # colour per cast ID (graphics/EBDX/VS/{tunnel,bandfoe,bandplayer}_<theme>.png)
    "PLAYER_A" => :teal, "PLAYER_B" => :green,
    "JUNO" => :rose, "KESTREL" => :blue, "DORIAN" => :violet, "TAMSIN" => :gold,
    "LARCH" => :grey, "MARISOL" => :blue, "BRANN" => :red, "CELESTINE" => :violet,
    "VOSS" => :grey, "MARCHETTI" => :red, "KROLL" => :red, "ROWAN" => :green,
    "VALEN" => :gold, "MOURNER" => :green, "ROOK" => :blue, "SAHAR" => :gold,
    # Art Drops 11-12 (Gemini wiring proposal 2026-11-22)
    "CORVIN" => :violet, "KAITO" => :red, "ANJA" => :teal,
    "ODESSA" => :blue, "ILSA" => :rose, "BASTIAN" => :gold, "YSOLDE" => :violet, "MAGNUS" => :grey,
    "NYX" => :violet, "SIGRUN" => :red,
    # Art Drop 13
    "VESPER" => :gold, "THISTLE" => :green, "QUENT" => :teal, "SABLE" => :teal
  }
  DEFAULT_THEME_FOE    = :violet
  DEFAULT_THEME_PLAYER = :teal
  # Layout (512x384), measured off the B2W2 reference
  TOP_Y = 40; BOT_Y = 208; BAND_H = 136
  BOLT_TOP_Y = 108; BOLT_BOT_Y = 276
  VS_CX = 256; VS_CY = 192; VS_SPLIT = 56             # EBDX's "VS." art: V is columns 0..55, S the rest
  FOE_BUST_CX = 392; PLAYER_BUST_CX = 120
  EMBLEM_CX = 240; EMBLEM_CY = 192
  PORTRAIT_ZOOM = 1.5             # 96x96 portrait fallback -> 144px; dedicated 256x136 VS busts render at 1.0
  HOLD_END = 5.2                  # seconds: when the finished screen starts to leave
  POSE_SECONDS = 1.6              # the trainer's one-shot pose, played during the challenge line
  INTRO_ZOOM = 2.4                # how close the battle opens on the trainer's silhouette (3.0 cropped heads; Gemini QA 2026-11-22)

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
      @owned_bmps = []
      @home = {}
      @foe_id = PrismfallVS.cast_id(trainer)
      @pl_id = PrismfallVS.player_id
      @foe_theme = THEMES[@foe_id] || DEFAULT_THEME_FOE
      @pl_theme = THEMES[@pl_id] || DEFAULT_THEME_PLAYER
      w = Graphics.width; h = Graphics.height
      base_z = @vp.z
      # --- the overworld, darkened
      @s["world"] = Sprite.new(@vp); @s["world"].snap_screen; @s["world"].z = 1
      @s["dim"] = Sprite.new(@vp); @s["dim"].bitmap = make_bmp(w, h)
      @s["dim"].bitmap.fill_rect(0, 0, w, h, Color.new(2, 2, 8)); @s["dim"].opacity = 0; @s["dim"].z = 2
      # --- 3-layer perspective-rushing warp tunnel (emulates B2W2's 3D cone fly-through)
      tbmp = PrismfallVS.themed("tunnel", @foe_theme)
      3.times do |i|
        k = "tunnel#{i}"
        t = Sprite.new(@vp)
        t.bitmap = tbmp
        t.ox = tbmp.width / 2; t.oy = tbmp.height / 2
        t.x = VS_CX; t.y = VS_CY; t.z = 3 + i
        t.mirror = i.odd?
        t.blend_type = (i == 0) ? 0 : 1
        @s[k] = t
      end
      @s["hole"] = Sprite.new(@vp)
      @s["hole"].bitmap = hole_bitmap(180)
      @s["hole"].ox = 90; @s["hole"].oy = 90; @s["hole"].x = VS_CX; @s["hole"].y = VS_CY
      @s["hole"].zoom_x = @s["hole"].zoom_y = 0; @s["hole"].z = 7
      # --- lightning (doubled horizontally for seamless high-speed UV scroll + additive glow)
      @bolts = [0, 1, 2].map do |i|
        src = RPG::Cache.load_bitmap("", "#{PrismfallVS.dir}/bolt#{i}")
        dbl = make_bmp(src.width * 2, src.height)
        dbl.blt(0, 0, src, src.rect)
        dbl.blt(src.width, 0, src, src.rect)
        [dbl, src.width, src.height]
      end
      @s["boltT"] = Sprite.new(@vp); @s["boltB"] = Sprite.new(@vp)
      [["boltT", BOLT_TOP_Y], ["boltB", BOLT_BOT_Y]].each do |k, y|
        bmp, bw, bh = @bolts[0]
        @s[k].bitmap = bmp; @s[k].y = y - bh / 2; @s[k].z = 9
        @s[k].blend_type = 1
        @s[k].src_rect = Rect.new(0, 0, 0, bh)
      end
      # --- the two bands: own viewports so busts, ghost echo, sheen, emblem and names clip cleanly
      @top = Viewport.new(0, TOP_Y, w, BAND_H); @top.z = base_z + 1
      @bot = Viewport.new(0, BOT_Y, w, BAND_H); @bot.z = base_z + 1
      @s["bgT"] = Sprite.new(@top); @s["bgT"].bitmap = PrismfallVS.themed("bandfoe", @foe_theme); @s["bgT"].z = 0
      @s["bgB"] = Sprite.new(@bot); @s["bgB"].bitmap = PrismfallVS.themed("bandplayer", @pl_theme); @s["bgB"].z = 0
      # subtle scrolling diagonal anime speed sheen across each band
      sheen_bmp = make_sheen_bitmap(w, BAND_H)
      [["sheenT", @top], ["sheenB", @bot]].each do |k, vp|
        sh = Sprite.new(vp); sh.bitmap = sheen_bmp; sh.z = 1; sh.blend_type = 1; sh.opacity = 52
        sh.src_rect = Rect.new(0, 0, w, BAND_H)
        @s[k] = sh
      end
      emb = RPG::Cache.load_bitmap("", "#{PrismfallVS.dir}/emblem")
      [["embT", @top, TOP_Y], ["embB", @bot, BOT_Y]].each do |k, v, by|
        @s[k] = Sprite.new(v); @s[k].bitmap = emb; @s[k].z = 2; @s[k].opacity = 185
        @s[k].x = EMBLEM_CX - emb.width / 2; @s[k].y = EMBLEM_CY - emb.height / 2 - by
      end
      # enlarged translucent ghost echo behind the foe bust (signature B2W2 Panel 5 look!)
      @s["ghostT"] = make_ghost_bust(@top, @foe_id, FOE_BUST_CX - 64)
      @s["bustT"]  = make_bust(@top, @foe_id, FOE_BUST_CX)
      @s["bustB"]  = make_bust(@bot, @pl_id, PLAYER_BUST_CX)
      # Reborn-style two-line plate: the bespoke class small above the name ("PAGEANT MASTER" / "Dorian")
      cls = (@trainer.trainer_type_name rescue "").to_s
      cls = "" if cls == @trainer.name.to_s || cls.end_with?(@trainer.name.to_s)
      @s["nameT"]  = name_sprite(@top, @trainer.name.to_s, 18, (cls.empty? ? 8 : 18), :left, cls.upcase)
      @s["nameB"]  = name_sprite(@bot, ($player ? $player.name : ""), w - 18, BAND_H - 42, :right)
      @final = %w[bgT bgB sheenT sheenB embT embB ghostT nameT nameB tunnel0 tunnel1 tunnel2]
      @final.concat(@s.keys.grep(/_class_/))   # the class line shows with the names
      @final.each { |k| @s[k].visible = false }
      # --- over everything: centered-pivot VS halves, sparks, white, black
      @over = Viewport.new(0, 0, w, h); @over.z = base_z + 2
      vsb = RPG::Cache.load_bitmap("", "Graphics/EBDX/Transitions/Common/vs")
      @vs_w = vsb.width; @vs_h = vsb.height
      v_w = VS_SPLIT; s_w = vsb.width - VS_SPLIT
      @s["V"] = Sprite.new(@over); @s["V"].bitmap = vsb; @s["V"].src_rect = Rect.new(0, 0, v_w, vsb.height)
      @s["S"] = Sprite.new(@over); @s["S"].bitmap = vsb; @s["S"].src_rect = Rect.new(VS_SPLIT, 0, s_w, vsb.height)
      @s["V"].ox = v_w / 2; @s["V"].oy = @vs_h / 2
      @s["S"].ox = s_w / 2; @s["S"].oy = @vs_h / 2
      @v_home = [VS_CX - @vs_w / 2 + v_w / 2, VS_CY]
      @s_home = [VS_CX - @vs_w / 2 + VS_SPLIT + s_w / 2, VS_CY]
      %w[V S].each { |k| @s[k].z = 20; @s[k].visible = false }
      spk = RPG::Cache.load_bitmap("", "#{PrismfallVS.dir}/spark")
      @sparks = (0...18).map do |i|
        sp = Sprite.new(@over); sp.bitmap = spk; sp.ox = spk.width / 2; sp.oy = spk.height / 2
        sp.z = 25; sp.blend_type = 1; sp.visible = false
        a = (i * 360.0 / 18 + rand(16)) * Math::PI / 180
        [sp, Math.cos(a), Math.sin(a), 80 + rand(110), 0.7 + rand * 0.8]
      end
      @s["white"] = Sprite.new(@over); @s["white"].bitmap = make_bmp(w, h)
      @s["white"].bitmap.fill_rect(0, 0, w, h, Color.new(255, 255, 255)); @s["white"].opacity = 0; @s["white"].z = 50
      @s["black"] = Sprite.new(@over); @s["black"].bitmap = make_bmp(w, h)
      @s["black"].bitmap.fill_rect(0, 0, w, h, Color.new(0, 0, 0)); @s["black"].opacity = 0; @s["black"].z = 60
    end

    def make_bmp(w, h)
      b = Bitmap.new(w, h)
      @owned_bmps.push(b)
      return b
    end

    def hole_bitmap(d)
      # soft-feathered radial black core so the vortex collapse blends cleanly into darkness
      b = make_bmp(d, d); r = d / 2.0
      (0...d).each do |y|
        dy = y - r + 0.5
        next if dy.abs >= r
        hw = Math.sqrt(r * r - dy * dy)
        x0 = (r - hw).floor; x1 = (r + hw).ceil
        # solid inner 72%, soft feathered outer rim
        inner_r = r * 0.72
        if dy.abs < inner_r
          ihw = Math.sqrt(inner_r * inner_r - dy * dy)
          ix0 = (r - ihw).floor; ix1 = (r + ihw).ceil
          b.fill_rect(x0, y, [ix0 - x0, 0].max, 1, Color.new(0, 0, 0, 145))
          b.fill_rect(ix0, y, [ix1 - ix0, 0].max, 1, Color.new(0, 0, 0, 255))
          b.fill_rect(ix1, y, [x1 - ix1, 0].max, 1, Color.new(0, 0, 0, 145))
        else
          b.fill_rect(x0, y, [x1 - x0, 0].max, 1, Color.new(0, 0, 0, 130))
        end
      end
      return b
    end

    def make_sheen_bitmap(w, h)
      # doubled 2*w strip of subtle diagonal white energy streaks that scrolls smoothly
      b = make_bmp(w * 2, h)
      stripes = [[40, 28, 120], [150, 10, 180], [270, 44, 95], [410, 16, 150]]
      stripes.each do |sx, sw, alpha|
        col = Color.new(255, 255, 255, alpha)
        h.times do |y|
          dx = -(y * 0.55).round
          [0, w].each do |rep|
            x = (sx + dx + rep) % (w * 2)
            b.fill_rect(x, y, sw, 1, col)
          end
        end
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
      s.y = BAND_H - bh                        # bottom flush with the band
      s.visible = false
      @home[s] = s.x
      return s
    end

    def make_ghost_bust(vp, id, cx)
      file, zoom = PrismfallVS.bust(id)
      s = Sprite.new(vp); s.z = 3
      return s if !file
      gz = zoom * 1.48
      s.bitmap = RPG::Cache.load_bitmap("", file)
      s.zoom_x = s.zoom_y = gz
      s.blend_type = 1
      s.opacity = 58
      bw = (s.bitmap.width * gz).round; bh = (s.bitmap.height * gz).round
      s.x = (cx - bw / 2).round
      s.y = BAND_H - bh + 18
      s.visible = false
      @home[s] = s.x
      return s
    end

    def name_sprite(vp, text, x, y, align, sub = "")
      s = Sprite.new(vp); s.bitmap = make_bmp(Graphics.width, 44); s.z = 8
      if !sub.empty?
        cl = Sprite.new(vp); cl.bitmap = make_bmp(Graphics.width, 24); cl.z = 8
        pbSetSmallFont(cl.bitmap)
        pbDrawTextPositions(cl.bitmap, [
          [sub, x + 1, 3, align, Color.new(10, 10, 18, 170), Color.new(10, 10, 18, 170)],
          [sub, x,     2, align, Color.new(255, 236, 170), Color.new(24, 24, 38), :outline]
        ])
        cl.y = y - 14
        @s["#{text}_class_#{x}"] = cl
      end
      pbSetSystemFont(s.bitmap)
      s.bitmap.font.size += 6
      s.bitmap.font.bold = true
      # bold double-drop shadow + crisp white face (matches B2W2's dramatic high-contrast nameplate)
      pbDrawTextPositions(s.bitmap, [
        [text, x + 2, 8, align, Color.new(10, 10, 18, 190), Color.new(10, 10, 18, 190)],
        [text, x,     6, align, Color.new(252, 252, 255), Color.new(24, 24, 38), :outline]
      ])
      s.y = y
      return s
    end

    def play
      t0 = System.uptime
      cues = { 0.12 => "Vs flash", 1.3 => "Vs sword", 2.8 => "Vs flash" }
      begin
        loop do
          t = System.uptime - t0
          cues.keys.each { |k| next if t < k; (pbSEPlay(cues.delete(k)) rescue nil) }
          frame(t)
          Graphics.update
          break if t >= HOLD_END + 0.75
        end
        @vp.color = Color.new(0, 0, 0, 255)
      ensure
        dispose        # also on an exception mid-sequence, so nothing leaks onto the battle
      end
      Graphics.update
    end

    def frame(t)
      e = PrismfallVS
      # 0.00-1.32: flash, flash, white-out, clears to a darkened overworld (+ reveal flash at 2.78)
      @s["white"].opacity = [e.pulse(t, 0.10, 0.22, 0.36, 225), e.pulse(t, 0.42, 0.54, 0.68, 225),
                             (t >= 0.72 && t < 1.15) ? 255 * e.prog(t, 0.72, 0.82) : 0,
                             (t >= 1.15 && t < 1.4) ? 255 * (1 - e.prog(t, 1.15, 1.32)) : 0,
                             e.pulse(t, 2.76, 2.80, 3.06, 255)].max
      @s["dim"].opacity = 228 * e.prog(t, 0.72, 0.9)

      # 1.30-2.80: organic lightning streaks in, then tears horizontally across screen with additive blaze
      if t < 2.8
        grow = e.ease_out(e.prog(t, 1.3, 1.50))
        idx = ((t * 24).to_i % 3)
        bmpT, bw, bh = @bolts[idx]
        bmpB, _,  _  = @bolts[(idx + 1) % 3]
        vis = (bw * grow).round
        scroll = (t > 1.48) ? (((t - 1.48) * 680).to_i % bw) : 0
        jit = (t > 1.50) ? ((t * 36).to_i.even? ? 1 : -1) : 0
        @s["boltT"].bitmap = bmpT; @s["boltB"].bitmap = bmpB
        @s["boltT"].src_rect = Rect.new(bw - vis + scroll, 0, vis, bh); @s["boltT"].x = bw - vis
        @s["boltB"].src_rect = Rect.new(bw - scroll, 0, vis, bh);       @s["boltB"].x = 0
        @s["boltT"].y = BOLT_TOP_Y - bh / 2 + jit
        @s["boltB"].y = BOLT_BOT_Y - bh / 2 - jit
        @s["boltT"].visible = @s["boltB"].visible = (t >= 1.3)
      else
        @s["boltT"].visible = @s["boltB"].visible = false
      end

      # 2.05: busts rocket in (foe from right, player from left), then subtle cinematic drift on hold
      b = e.ease_out(e.prog(t, 2.05, 2.28))
      drift = (t >= 2.8 && t < HOLD_END) ? ((t - 2.8) * 5.5) : 0.0
      [["bustT", 1, -drift], ["bustB", -1, drift]].each do |k, dir, dx|
        sp = @s[k]; next if !@home[sp]
        sp.visible = t >= 2.05
        sp.x = (@home[sp] + dir * 290 * (1 - b) + dx).round
      end
      if @s["ghostT"] && @home[@s["ghostT"]] && t >= 2.8
        @s["ghostT"].x = (@home[@s["ghostT"]] + drift * 1.4).round
      end

      # 2.40: S drops huge from above, V rises huge from below (centered pivot!), slamming into "VS."
      if t >= 2.4 && t < HOLD_END
        @s["V"].visible = @s["S"].visible = true
        raw = e.prog(t, 2.4, 2.74)
        v = e.ease_in(raw)
        # 4.6x -> 1.0x slam + crisp 1.08 -> 1.0 impact settle bounce
        z = (t < 2.74) ? (4.6 - 3.6 * v) : (1.0 + 0.12 * (1 - e.ease_out(e.prog(t, 2.74, 2.90))))
        j = (t >= 2.82 && (t * 14).to_i.odd?) ? 1 : 0
        @s["S"].zoom_x = @s["S"].zoom_y = z
        @s["V"].zoom_x = @s["V"].zoom_y = z
        @s["S"].x = @s_home[0] + j
        @s["S"].y = (@s_home[1] - 250 * (1 - v)).round
        @s["V"].x = @v_home[0] + j
        @s["V"].y = (@v_home[1] + 250 * (1 - v)).round
      end

      # impact screen punch shake right when V & S lock (t = 2.76..2.98)
      if t >= 2.76 && t < 2.98
        amp = (6 * (1 - e.prog(t, 2.76, 2.98))).round
        shx = ((t * 60).to_i.even? ? amp : -amp)
        shy = ((t * 48).to_i.odd?  ? (amp / 2) : -(amp / 2))
        @top.ox = @bot.ox = @over.ox = shx
        @top.oy = @bot.oy = @over.oy = shy
      else
        @top.ox = @bot.ox = @over.ox = 0
        @top.oy = @bot.oy = @over.oy = 0
      end

      # 2.80: final screen (3-layer 3D rushing vortex tunnel + scrolling diagonal sheen + spark burst)
      if t >= 2.8
        @final.each { |k| @s[k].visible = true }
        @s["world"].visible = false
        @s["dim"].opacity = 255            # dark backing: the cycling tunnel layers shrink to 0.6x and would show the map at the corners
        # scrolling diagonal speed sheen across both bands
        sw = Graphics.width
        sp_off = ((t - 2.8) * 340).to_i % sw
        @s["sheenT"].src_rect.x = sp_off
        @s["sheenB"].src_rect.x = sw - sp_off
        # 3 staggered perspective-rushing vortex layers (emulates flying through B2W2's 3D cone!)
        accel = (t >= HOLD_END) ? (1.0 + 2.4 * e.prog(t, HOLD_END, HOLD_END + 0.45)) : 1.0
        3.times do |i|
          tn = @s["tunnel#{i}"]
          phase = ((t * 0.65 * accel + i / 3.0) % 1.0)
          z = 0.60 + 1.85 * (phase ** 1.5)
          tn.zoom_x = tn.zoom_y = z
          tn.angle = (i.even? ? 1 : -1) * (t * (38.0 + i * 16.0) * accel)
          tn.opacity = (i == 0) ? 255 : (175 * Math.sin(phase * Math::PI)).round
        end
        @sparks.each do |sp, dx, dy, dist, sz|
          u = e.prog(t, 2.80, 3.45)
          sp.visible = u > 0 && u < 1
          d = dist * e.ease_out(u)
          sp.x = VS_CX + (dx * d).round; sp.y = VS_CY + (dy * d * 0.72).round
          sp.zoom_x = sp.zoom_y = sz * (1.1 - 0.5 * u)
          sp.opacity = (255 * (1 - u)).round
        end
      end

      # 5.20: bands split cleanly up/down, V & S shoot outward, 3D vortex swallows screen into black
      if t >= HOLD_END
        x = e.ease_in(e.prog(t, HOLD_END, HOLD_END + 0.22))
        @top.rect.y = (TOP_Y - (TOP_Y + BAND_H) * x).round
        @bot.rect.y = (BOT_Y + (Graphics.height - BOT_Y) * x).round
        # creator-caught: at 220 px the letters stopped inside the frame at ~94% opacity for 0.24 s.
        # They now travel 360 px (clear of 512) and fade with their own travel, not the vortex's.
        @s["V"].x = @v_home[0] - (360 * x).round
        @s["S"].x = @s_home[0] + (360 * x).round
        k = e.ease_in(e.prog(t, HOLD_END + 0.14, HOLD_END + 0.46))
        @s["hole"].zoom_x = @s["hole"].zoom_y = 5.4 * k
        @s["V"].opacity = @s["S"].opacity = (255 * (1 - x)).round
        @s["black"].opacity = (255 * e.prog(t, HOLD_END + 0.42, HOLD_END + 0.52)).round
      end
    end

    def dispose
      return if @disposed
      @disposed = true
      w = @s["world"]
      w.bitmap.dispose if w && !w.disposed? && w.bitmap && !w.bitmap.disposed?   # snap_screen's 512x384 copy
      @s.each_value { |sp| sp.dispose if sp && !sp.disposed? }
      @sparks.each { |sp, *_| sp.dispose if sp && !sp.disposed? }
      @owned_bmps.each { |b| b.dispose if b && !b.disposed? }
      [@top, @bot, @over].each { |v| v.dispose if v && !v.disposed? }
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
# Battle start: hold the trainer's pose strip on frame 0 through EBDX's intro sweep
# under dramatic B2W2 spotlight dimming, then brighten and play the one-shot pose
# during "You are challenged by ...!" (holding the final Hero frame afterwards).
#===============================================================================
# Everything below hooks EBDX classes; without EBDX the VS screen simply never applies.
if defined?(EliteBattle) && defined?(DynamicTrainerSprite)

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
      @pf_intro_dim_t0 = System.uptime
      # Dramatic B2W2 spotlight dim while the camera sweeps back from the trainer silhouette
      @viewport.tone = Tone.new(-72, -72, -56, 0) rescue nil
      v = EliteBattle.get_vector(:ENEMY).dup    # dup: never write into EBDX's shared vector table
      v[4] = PrismfallVS::INTRO_ZOOM if v[4]
      @vector = Vector.new(*v[0, 6]); @vector.battle = @battle
    end
    pf_vs_startSceneAnimation
  end

  alias pf_vs_animateScene animateScene unless method_defined?(:pf_vs_animateScene)
  def animateScene(align = false, smanim = false, &block)
    pf_vs_animateScene(align, smanim, &block)
    pf_vs_update_intro_tone
    pf_vs_update_pose
  end

  def pf_vs_update_intro_tone
    return if !@pf_intro_dim_t0 || !@viewport
    elapsed = System.uptime - @pf_intro_dim_t0
    if !PrismfallVS.hold_pose
      @viewport.tone = Tone.new(0, 0, 0, 0) rescue nil
      @pf_intro_dim_t0 = nil
      return
    end
    # Hold dark silhouette drama for ~0.55s, then smoothly illuminate over 0.45s as trainer colour returns
    k = PrismfallVS.prog(elapsed, 0.55, 1.0)
    @viewport.tone = Tone.new((-72 * (1 - k)).round, (-72 * (1 - k)).round, (-56 * (1 - k)).round, 0) rescue nil
  end

  def pf_vs_start_pose
    return if @pf_pose_t0 || !@battle.opponent
    PrismfallVS.hold_pose = false
    @viewport.tone = Tone.new(0, 0, 0, 0) rescue nil
    @pf_intro_dim_t0 = nil
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

end   # defined?(EliteBattle)

# A battle that ends (or crashes) mid-intro must not leave the pose hold or the input block behind.
EventHandlers.add(:on_end_battle, :prismfall_vs_reset,
  proc { |*_args|
    PrismfallVS.hold_pose = false
    PrismfallVS.input_block_until = 0
  }
)
