#===============================================================================
# Prismfall EBDX Bridge - Rejuvenation-style trainer VS screen (creator's direction 2026-11-21:
# "player vs Eizen" in Rejuvenation). Replaces EBDX's Poke Ball + split-screen transition for
# named cast trainers:
#   the overworld dims -> a band opens across the middle -> the player's half (left) and the
#   opponent's half (right) slide in with their busts over speed-line panels -> the VS slams in
#   over the bottom edge -> names under each half -> hold -> flash -> battle.
# The battle scene then opens on the trainer's one-shot intro pose (EBDX plays the
# Graphics/Trainers/<TYPE>.png strip once; no in-battle VS overlay).
#
# Who gets it: a single opposing trainer whose cast ID has a bust. Cast ID = the trainer's name
# in capitals ("Juno" -> JUNO), or VS_IDS[trainer type]. Bust = Graphics/EBDX/VS/<ID>.png (dedicated
# VS art, drawn at final size) or, until that exists, the 96x96 dialogue portrait at 1.5x.
# Generic trainers (no bust) keep EBDX's normal transition.
# UI art: Graphics/EBDX/VS/{panel_<theme>,vs_logo,band_edge}.png (tools/vs/make_vs_assets.py).
#===============================================================================
module PrismfallVS
  ENABLED   = true
  OFF_SWITCH = nil                 # a game switch that turns the VS screen off (e.g. for a cutscene battle)
  VS_IDS    = {}                   # trainer type => cast ID when the name doesn't match (e.g. :HOLLOW_SABLE => "KROLL")
  THEMES    = {                    # panel colour per cast ID (graphics/EBDX/VS/panel_<theme>.png)
    "PLAYER_A" => :green, "PLAYER_B" => :teal,
    "JUNO" => :rose, "KESTREL" => :blue, "DORIAN" => :violet, "TAMSIN" => :gold,
    "LARCH" => :grey, "MARISOL" => :blue, "BRANN" => :red, "CELESTINE" => :violet,
    "VOSS" => :grey, "MARCHETTI" => :red, "KROLL" => :red, "ROWAN" => :green
  }
  DEFAULT_THEME_FOE = :red
  DEFAULT_THEME_PLAYER = :green
  # Layout (512x384 screen)
  BAND_Y = 112; BAND_H = 136; EDGE_H = 8
  VS_X = 256; VS_Y = 250
  NAME_Y = 280
  PORTRAIT_ZOOM = 1.5              # 96x96 portrait (48 native px doubled) -> 144px = 3 screen px per art px
  HOLD = 1.9                       # seconds the finished screen holds

  def self.dir; return "Graphics/EBDX/VS"; end

  def self.cast_id(trainer)
    return nil if !trainer
    id = VS_IDS[trainer.trainer_type]
    id ||= trainer.name.to_s.upcase.gsub(/[^A-Z0-9_]/, "")
    return (id.nil? || id.empty?) ? nil : id
  end

  def self.player_id
    return "PLAYER_B" if $player && $player.trainer_type.to_s.end_with?("PLAYER_B")
    return "PLAYER_B" if $player && !$player.trainer_type.to_s.include?("PLAYER") && ($player.female? rescue false)
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
    return false if !pbResolveBitmap("#{dir}/vs_logo")
    return !bust(cast_id(foe[0])).nil?
  end

  def self.theme_bitmap(theme)
    f = "#{dir}/panel_#{theme}"
    f = "#{dir}/panel_red" if !pbResolveBitmap(f)
    src = RPG::Cache.load_bitmap("", f)
    bmp = Bitmap.new(src.width * 2, src.height)          # doubled so a scrolling window never runs off the end
    bmp.blt(0, 0, src, src.rect); bmp.blt(src.width, 0, src, src.rect)
    return bmp
  end

  def self.ease_out(t); t = t.clamp(0.0, 1.0); return 1 - (1 - t)**3; end
  def self.prog(t, a, b); return ((t - a) / (b - a)).clamp(0.0, 1.0); end

  #=============================================================================
  class Sequence
    def initialize(viewport, trainer)
      @vp = viewport
      @trainer = trainer
      @sprites = {}
      @foe_id = PrismfallVS.cast_id(trainer)
      @pl_id = PrismfallVS.player_id
      w = Graphics.width
      # dimmed overworld
      @sprites["bg"] = Sprite.new(@vp)
      @sprites["bg"].snap_screen
      @sprites["bg"].z = 1
      @sprites["dim"] = Sprite.new(@vp)
      @sprites["dim"].bitmap = Bitmap.new(w, Graphics.height)
      @sprites["dim"].bitmap.fill_rect(0, 0, w, Graphics.height, Color.new(4, 4, 10))
      @sprites["dim"].opacity = 0
      @sprites["dim"].z = 2
      # the band: its own viewport, so panels and busts are clipped to it
      @band = Viewport.new(0, BAND_Y + BAND_H / 2, w, 1)
      @band.z = @vp.z + 1
      @half = w / 2
      @pl_theme = THEMES[@pl_id] || DEFAULT_THEME_PLAYER
      @foe_theme = THEMES[@foe_id] || DEFAULT_THEME_FOE
      @sprites["panelL"] = Sprite.new(@band)
      @sprites["panelL"].bitmap = PrismfallVS.theme_bitmap(@pl_theme)
      @sprites["panelL"].src_rect = Rect.new(0, 0, @half, BAND_H)
      @sprites["panelR"] = Sprite.new(@band)
      @sprites["panelR"].bitmap = PrismfallVS.theme_bitmap(@foe_theme)
      @sprites["panelR"].src_rect = Rect.new(0, 0, @half, BAND_H)
      @sprites["bustL"] = make_bust(@pl_id, false)
      @sprites["bustR"] = make_bust(@foe_id, true)
      @sprites["seam"] = Sprite.new(@band)
      @sprites["seam"].bitmap = Bitmap.new(6, BAND_H)
      @sprites["seam"].bitmap.fill_rect(0, 0, 6, BAND_H, Color.new(255, 255, 255, 90))
      @sprites["seam"].bitmap.fill_rect(2, 0, 2, BAND_H, Color.new(255, 255, 255))
      @sprites["seam"].ox = 3; @sprites["seam"].x = @half; @sprites["seam"].z = 20
      @sprites["seam"].opacity = 0
      # metal trim above and below the band
      @over = Viewport.new(0, 0, w, Graphics.height)
      @over.z = @vp.z + 2
      %w[edgeT edgeB].each do |k|
        @sprites[k] = Sprite.new(@over)
        @sprites[k].bitmap = RPG::Cache.load_bitmap("", "#{PrismfallVS.dir}/band_edge")
        @sprites[k].y = BAND_Y + BAND_H / 2 - EDGE_H / 2
      end
      # VS logo, names, flash
      @sprites["vs"] = Sprite.new(@over)
      @sprites["vs"].bitmap = RPG::Cache.load_bitmap("", "#{PrismfallVS.dir}/vs_logo")
      @sprites["vs"].ox = @sprites["vs"].bitmap.width / 2
      @sprites["vs"].oy = @sprites["vs"].bitmap.height / 2
      @sprites["vs"].x = VS_X; @sprites["vs"].y = VS_Y
      @sprites["vs"].opacity = 0; @sprites["vs"].z = 30
      @sprites["names"] = Sprite.new(@over)
      @sprites["names"].bitmap = Bitmap.new(w, 56)
      pbSetSystemFont(@sprites["names"].bitmap)
      @sprites["names"].bitmap.font.size += 8
      white = Color.new(248, 248, 248); shadow = Color.new(24, 24, 32)
      pbDrawTextPositions(@sprites["names"].bitmap, [
        [$player ? $player.name : "", @half / 2, 8, :center, white, shadow, :outline],
        [@trainer.name.to_s, @half + @half / 2, 8, :center, white, shadow, :outline]])
      @sprites["names"].y = NAME_Y + 12; @sprites["names"].opacity = 0; @sprites["names"].z = 25
      @sprites["flash"] = Sprite.new(@over)
      @sprites["flash"].bitmap = Bitmap.new(w, Graphics.height)
      @sprites["flash"].bitmap.fill_rect(0, 0, w, Graphics.height, Color.new(255, 255, 255))
      @sprites["flash"].opacity = 0; @sprites["flash"].z = 40
    end

    def make_bust(id, foe)
      file, zoom = PrismfallVS.bust(id)
      s = Sprite.new(@band)
      return s if !file
      s.bitmap = RPG::Cache.load_bitmap("", file)
      s.zoom_x = s.zoom_y = zoom
      s.mirror = false
      bw = (s.bitmap.width * zoom).round; bh = (s.bitmap.height * zoom).round
      # each bust sits toward the seam (as in Rejuvenation), bottom flush with the band
      @bust_home ||= {}
      cx = foe ? @half + @half * 0.42 : @half * 0.58
      s.x = (cx - bw / 2).round
      s.y = [BAND_H - bh, (BAND_H - bh) / 2].max
      s.z = 10
      @bust_home[foe ? :R : :L] = s.x
      return s
    end

    def play
      pbSEPlay("Vs flash") rescue nil
      t0 = System.uptime
      slammed = false; swooshed = false
      total = 0.95 + HOLD
      loop do
        t = System.uptime - t0
        layout(t)
        if !swooshed && t >= 0.25
          swooshed = true; pbSEPlay("Vs sword") rescue nil
        end
        if !slammed && t >= 0.78
          slammed = true; pbSEPlay("Vs flash") rescue nil
        end
        Graphics.update
        break if t >= total
      end
      # exit: white flash, then black
      t1 = System.uptime
      loop do
        u = System.uptime - t1
        scroll(System.uptime - t0)
        @sprites["flash"].opacity = 255 * PrismfallVS.prog(u, 0, 0.18)
        Graphics.update
        break if u >= 0.2
      end
      @vp.color = Color.new(0, 0, 0, 255)
      dispose
      Graphics.update
    end

    def scroll(t)
      sp = (t * 420).to_i
      @sprites["panelL"].src_rect.x = sp % (@sprites["panelL"].bitmap.width / 2)
      w2 = @sprites["panelR"].bitmap.width / 2
      @sprites["panelR"].src_rect.x = (w2 - (sp % w2)) % w2
    end

    def layout(t)
      e = PrismfallVS
      @sprites["dim"].opacity = 205 * e.prog(t, 0, 0.2)
      # band opens from its centre line
      o = e.ease_out(e.prog(t, 0.12, 0.38))
      h = (BAND_H * o).round
      @band.rect.y = BAND_Y + (BAND_H - h) / 2
      @band.rect.height = h
      @band.oy = (BAND_H - h) / 2
      @sprites["edgeT"].y = @band.rect.y - EDGE_H
      @sprites["edgeB"].y = @band.rect.y + h
      # panels slide in from their sides
      p = e.ease_out(e.prog(t, 0.22, 0.52))
      @sprites["panelL"].x = (-@half * (1 - p)).round
      @sprites["panelR"].x = (@half + @half * (1 - p)).round
      scroll(t)
      # busts arrive a beat later, from further out
      b = e.ease_out(e.prog(t, 0.36, 0.7))
      @sprites["bustL"].x = (@bust_home[:L] - 200 * (1 - b)).round if @bust_home[:L]
      @sprites["bustR"].x = (@bust_home[:R] + 200 * (1 - b)).round if @bust_home[:R]
      @sprites["seam"].opacity = 255 * e.prog(t, 0.45, 0.6)
      # VS slams in, with a flash and a short shake
      v = e.prog(t, 0.78, 0.9)
      @sprites["vs"].opacity = 255 * v
      @sprites["vs"].zoom_x = @sprites["vs"].zoom_y = 2.6 - 1.6 * e.ease_out(v)
      f = e.prog(t, 0.9, 1.2)
      @sprites["flash"].opacity = (t >= 0.9) ? 200 * (1 - f) : 0
      shake = (t >= 0.9 && t < 1.12) ? ((t * 60).to_i.even? ? 3 : -3) : 0
      @band.ox = shake
      @sprites["vs"].x = VS_X + shake
      # names
      n = e.ease_out(e.prog(t, 0.95, 1.2))
      @sprites["names"].opacity = 255 * n
      @sprites["names"].y = NAME_Y + (12 * (1 - n)).round
    end

    def dispose
      @sprites.each_value do |s|
        next if s.disposed?
        s.bitmap.dispose if s.bitmap && !s.bitmap.disposed? && !%w[edgeT edgeB vs bustL bustR].any? { |k| @sprites[k].equal?(s) }
        s.dispose
      end
      @band.dispose; @over.dispose
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
# B2W2 PWT-style trainer intro: after the VS screen the camera pushes in on the opposing trainer
# while their Graphics/Trainers strip plays its one-shot pose (EBDX plays the strip once and holds
# the last frame) and through "You are challenged by ...!", then pulls back for the send-out.
#===============================================================================
module PrismfallVS
  POSE_CAMERA = true
end

class Battle::Scene
  alias pf_vs_pbShowPartyLineup pbShowPartyLineup unless method_defined?(:pf_vs_pbShowPartyLineup)
  def pbShowPartyLineup(side, fullAnim = false)
    ret = pf_vs_pbShowPartyLineup(side, fullAnim)
    if side == 1 && !@pf_pose_cam && PrismfallVS::POSE_CAMERA && @battle.trainerBattle? &&
       @battle.opponent && @battle.opponent.length == 1 && @vector
      @pf_pose_cam = true
      @vector.set(EliteBattle.get_vector(:ENEMY))
    end
    return ret
  end

  alias pf_vs_pbSendOutBattlers pbSendOutBattlers unless method_defined?(:pf_vs_pbSendOutBattlers)
  def pbSendOutBattlers(sendOuts, startBattle = false)
    if @pf_pose_cam && !@pf_pose_cam_back
      @pf_pose_cam_back = true
      @vector.set(EliteBattle.get_vector(:MAIN, @battle))
      @vector.inc = 0.2
      16.times { self.wait(1, true) }
    end
    return pf_vs_pbSendOutBattlers(sendOuts, startBattle)
  end
end
