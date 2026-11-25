#===============================================================================
# Prismfall Cutscenes — Wave-3 Rejuvenation V14 Rethink Choreography Module
#-------------------------------------------------------------------------------
# Drop-in companion to Plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb
# (paste directly into 017_AdvancedAnimations.rb OR require right after it once
# Wave 2 finishes recording in /home/antigravity/pf_engine_run/game/!).
#
# DEMOLISHES ALL RETIRED MS-PAINT WAVE-3 VFX SHEETS:
#   - ZERO pf_vfx_origin_beam / pf_vfx_blue_flare_beam / pf_vfx_beam_clash_core
#   - ZERO pf_vfx_trinitite_glass_wave / pf_vfx_glassfall_curtain / pf_vfx_sky_fracture
#   - ZERO pf_vfx_arceus_18locks / pf_vfx_prism_helix_18 / pf_vfx_legend_plate_burst
#   - 100% replaced by pure-pixel 2x pf_vfx_w3_*.png + bespoke 4x4 B2W2 acting
#     sheets (act_ch19_valen_command, act_ch19_kestrel_shield,
#     act_ch15_glassfall_brace, act_ch21_valen_kneel) + live 512x384 90-degree
#     Banquet-style apex plates!
#
# REUBEN'S DIRECTOR'S NOTE & SIX PERMANENT LAWS COMPLIANCE:
#   - Ch15 CE-1 AF 290 historical vision has ZERO Protagonist inside the vision
#     (frames grounded present-day Protagonist calmly before & after only!).
#   - Ch19 WAR-1 & Ch21 Finale keep the Protagonist's staging completely calm,
#     grounded, and natural — ZERO jerky fidgeting or unnatural darting!
#   - Heavy physical acting spotlights Valen, Kestrel, and Juno's 4x4 sheets.
#   - Strictly <= 3 restrained emote balloons per scene (2 per scene here).
#   - 0px static portraits during speech + multi-box dramatic dialogue with
#     silent breathing pauses + >= 3.0s text-free contemplation on 90° plates.
#   - Razor-sharp bgm_cut dead-silence audio vacuums (0.38s - 0.45s) at apex!
#
# Scenes included:
#   1. pf_play_ch19_war1_rethink      (~42s, Map 926 The Glass Dunes)
#   2. pf_play_ch15_glassfall_rethink (~36s, Map 295 -> AF 290 Vision -> Map 295)
#   3. pf_play_ch21_arceus_rethink    (~44s, Map 285 Briar Hall Summit Terrace)
#===============================================================================

module Prismfall
  module AdvancedAnimations
    # Guarded CutPlateExtension: only defines if 017_AdvancedAnimations.rb hasn't
    # already loaded the dedicated @plate_vp z=390 version from Wave 2!
    unless defined?(Prismfall::AdvancedAnimations::CutPlateExtension)
      module CutPlateExtension
        def show_cut_plate(path_or_name, fade_in: 0.20, hold: 4.0, fade_out: 0.30,
                           pan: nil, zoom: [1.0, 1.06], shake: 0, &block)
          path = path_or_name.start_with?("Graphics/") ? path_or_name : "Graphics/Pictures/#{path_or_name}"
          file_p = path.end_with?(".png") ? path : "#{path}.png"
          return false unless File.exist?(file_p)

          ensure_cut_plate_sprite
          bmp = cached_bitmap(path)
          @cut_plate_sp.bitmap  = bmp
          @cut_plate_sp.ox      = bmp.width / 2
          @cut_plate_sp.oy      = bmp.height / 2
          @cut_plate_sp.z       = 1000
          @cut_plate_sp.visible = true
          @cut_plate_bg.visible = true if @cut_plate_bg && !@cut_plate_bg.disposed?

          @cut_plate_saved_zoom = [@zoom, @zoom_focus, @zoom_task]
          @zoom = 1.0
          @zoom_task = nil
          @zoom_sp.visible = false if @zoom_sp && !@zoom_sp.disposed?

          p0, p1 = parse_pan_spec(pan)
          z0, z1 = Array(zoom).length >= 2 ? [zoom[0].to_f, zoom[1].to_f] : [1.0, 1.05]
          sh = photosensitive? ? (shake.to_f * 0.2) : shake.to_f

          hw = [bmp.width / 2.0, 1.0].max
          hh = [bmp.height / 2.0, 1.0].max
          req_z0 = [1.0, 1.0 + (p0[0].abs + sh + 1.0) / hw, 1.0 + (p0[1].abs + sh + 1.0) / hh].max
          req_z1 = [1.0, 1.0 + (p1[0].abs + sh + 1.0) / hw, 1.0 + (p1[1].abs + sh + 1.0) / hh].max
          z0 = [z0, req_z0].max
          z1 = [z1, req_z1, z0 + 0.04].max

          total_motion = [fade_in.to_f + hold.to_f + fade_out.to_f, 0.5].max
          @cut_plate_task = {
            :t => 0.0, :dur => total_motion,
            :p0 => p0, :p1 => p1, :z0 => z0, :z1 => z1, :shake => sh
          }
          apply_cut_plate_transform(0.0)

          if fade_in.to_f > 0.001
            t_start = @time
            while (@time - t_start) < fade_in.to_f
              u = [(@time - t_start) / fade_in.to_f, 1.0].min
              op = (255.0 * Ease.apply(:out, u)).round
              @cut_plate_sp.opacity = op
              @cut_plate_bg.opacity = op if @cut_plate_bg && !@cut_plate_bg.disposed?
              step_frame
            end
          end
          @cut_plate_sp.opacity = 255
          @cut_plate_bg.opacity = 255 if @cut_plate_bg && !@cut_plate_bg.disposed?

          if block_given?
            block.call(self)
          else
            wait(hold.to_f)
          end

          if fade_out.to_f > 0.001
            t_start = @time
            while (@time - t_start) < fade_out.to_f
              u = [(@time - t_start) / fade_out.to_f, 1.0].min
              op = (255.0 * (1.0 - Ease.apply(:in, u))).round
              @cut_plate_sp.opacity = op
              @cut_plate_bg.opacity = op if @cut_plate_bg && !@cut_plate_bg.disposed?
              step_frame
            end
          end

          clear_cut_plate
          true
        end

        def clear_cut_plate
          @cut_plate_task = nil
          if @cut_plate_sp && !@cut_plate_sp.disposed?
            @cut_plate_sp.visible = false
            @cut_plate_sp.opacity = 0
            @cut_plate_sp.bitmap  = nil
          end
          if @cut_plate_bg && !@cut_plate_bg.disposed?
            @cut_plate_bg.visible = false
            @cut_plate_bg.opacity = 0
          end
          if @cut_plate_saved_zoom
            @zoom, @zoom_focus, @zoom_task = @cut_plate_saved_zoom
            @cut_plate_saved_zoom = nil
          end
        end

        def step_frame(ignore_hitstop = false)
          if @cut_plate_task && @cut_plate_sp && !@cut_plate_sp.disposed? && @cut_plate_sp.visible
            dt = @fixed_dt || 0.0333
            @cut_plate_task[:t] += dt
            u = [@cut_plate_task[:t] / @cut_plate_task[:dur], 1.0].min
            apply_cut_plate_transform(u)
          end
          super(ignore_hitstop)
        end

        def dispose
          clear_cut_plate
          @cut_plate_sp.dispose if @cut_plate_sp && !@cut_plate_sp.disposed?
          @cut_plate_bg.dispose if @cut_plate_bg && !@cut_plate_bg.disposed?
          @plate_vp.dispose     if @plate_vp     && !@plate_vp.disposed?
          @cut_plate_sp = nil
          @cut_plate_bg = nil
          @plate_vp     = nil
          super
        end

        private

        def ensure_cut_plate_sprite
          return if @cut_plate_sp && !@cut_plate_sp.disposed?
          @plate_vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
          @plate_vp.z = 390
          @cut_plate_bg = Sprite.new(@plate_vp)
          @cut_plate_bg.bitmap = Bitmap.new(Graphics.width, Graphics.height)
          @cut_plate_bg.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(8, 10, 18, 255))
          @cut_plate_bg.z = 990
          @cut_plate_bg.visible = false
          @cut_plate_bg.opacity = 0
          @cut_plate_sp = Sprite.new(@plate_vp)
          @cut_plate_sp.z = 1000
          @cut_plate_sp.visible = false
          @cut_plate_sp.opacity = 0
        end

        def parse_pan_spec(pan)
          if pan.is_a?(Hash) && !pan.empty?
            k, v = pan.first
            return [k[0].to_f, k[1].to_f], [v[0].to_f, v[1].to_f]
          elsif pan.is_a?(Array) && pan.length == 2 && pan[0].is_a?(Array)
            return [pan[0][0].to_f, pan[0][1].to_f], [pan[1][0].to_f, pan[1][1].to_f]
          end
          return [0.0, 0.0], [0.0, 0.0]
        end

        def apply_cut_plate_transform(u)
          task = @cut_plate_task
          return unless task && @cut_plate_sp && !@cut_plate_sp.disposed?
          k = Ease.apply(:in_out, u)
          px = task[:p0][0] + (task[:p1][0] - task[:p0][0]) * k
          py = task[:p0][1] + (task[:p1][1] - task[:p0][1]) * k
          sc = task[:z0] + (task[:z1] - task[:z0]) * k
          sh_x = task[:shake] > 0.0 ? Math.sin(task[:t] * 48.0) * task[:shake] : 0.0
          sh_y = task[:shake] > 0.0 ? Math.cos(task[:t] * 61.0) * (task[:shake] * 0.65) : 0.0
          @cut_plate_sp.x = (Graphics.width / 2.0 + px + sh_x).round
          @cut_plate_sp.y = (Graphics.height / 2.0 + py + sh_y).round
          @cut_plate_sp.zoom_x = sc
          @cut_plate_sp.zoom_y = sc
        end
      end
    end

    if defined?(Engine) && !Engine.ancestors.include?(CutPlateExtension)
      Engine.prepend(CutPlateExtension)
    end

    class << self
      #=========================================================================
      # WAVE-3 SCENE 1 — Ch19 WAR-1 Rethink (~42s, Live Map 926 The Glass Dunes)
      # "Origin Pulse vs Blue Flare — Valen's Command, Kestrel's Intercept &
      #  The 90° Panoramic Glass Dunes Apex Plate"
      #-------------------------------------------------------------------------
      # Emote Count: STRICTLY 2 (:exclaim on Kestrel spotting blast, :ellipsis
      #              on Anja surveying the vitrified desert).
      # Protagonist: Grounded & natural (calm observational footing -> single
      #              steady defensive step back behind Kestrel's shield cover).
      # Pure-Pixel VFX: pf_vfx_w3_origin_beam, pf_vfx_w3_blue_flare,
      #                 pf_vfx_w3_clash_core, pf_vfx_w3_glass_curtain.
      # Acting Sheets:  act_ch19_valen_command, act_ch19_kestrel_shield,
      #                 act_war1_primal_kyogre, act_war1_reshiram.
      # 90° Apex Plate: cut_ch19_war1_90deg.png (3.1s silent text-free hold!).
      #=========================================================================
      def pf_play_ch19_war1_rethink(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Dawn Frontline, Primal Kyogre & Reshiram Summons, Valen's Vigil
          # (~0.0s .. 11.2s)
          #---------------------------------------------------------------------
          eng.transfer_map(926, 25.8, 8.6, hide_player: true)
          (3..10).each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(12, 2, -10, 8, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch19_dynast", volume: 82, tag: "ch19_dynast")

          # Isenmar Host (West / Left)
          eng.spawn_actor(:eirik, sheet: "EIRIK", tx: 23.5, ty: 11.3, dir: :right, is_charset: true)
          eng.spawn_actor(:is_s1, sheet: "pfw_soldier_isenmar", tx: 22.4, ty: 9.8,  dir: :right, is_charset: true)
          eng.spawn_actor(:is_s2, sheet: "pfw_soldier_isenmar", tx: 22.4, ty: 11.8, dir: :right, is_charset: true)
          eng.spawn_actor(:is_s3, sheet: "pfw_soldier_isenmar", tx: 23.9, ty: 12.4, dir: :right, is_charset: true)
          eng.spawn_actor(:is_b1, sheet: "pfw_banner_isenmar",  tx: 21.8, ty: 8.6,  grid: [1, 1], is_charset: false)
          eng.spawn_actor(:is_b2, sheet: "pfw_banner_isenmar",  tx: 21.7, ty: 12.1, grid: [1, 1], is_charset: false)

          # Ashkaar Host (East / Right)
          eng.spawn_actor(:hrothgar, sheet: "HROTHGAR", tx: 36.5, ty: 11.3, dir: :left, is_charset: true)
          eng.spawn_actor(:as_s1, sheet: "pfw_soldier_ashkaar", tx: 37.6, ty: 9.8,  dir: :left, is_charset: true)
          eng.spawn_actor(:as_s2, sheet: "pfw_soldier_ashkaar", tx: 37.6, ty: 11.8, dir: :left, is_charset: true)
          eng.spawn_actor(:as_s3, sheet: "pfw_soldier_ashkaar", tx: 36.1, ty: 12.4, dir: :left, is_charset: true)
          eng.spawn_actor(:as_b1, sheet: "pfw_banner_ashkaar",  tx: 38.2, ty: 8.6,  grid: [1, 1], is_charset: false)
          eng.spawn_actor(:as_b2, sheet: "pfw_banner_ashkaar",  tx: 38.3, ty: 12.1, grid: [1, 1], is_charset: false)

          # Southern Dune Ridge — Valen commanding forward; Kestrel, grounded PC, Anja & Sigrun below
          eng.spawn_actor(:valen,   sheet: "act_ch19_valen_command",  tx: 30.0, ty: 11.3, grid: [4, 4], is_charset: false, z_bias: 4)
          eng.spawn_actor(:kestrel, sheet: "act_ch19_kestrel_shield", tx: 28.1, ty: 12.5, grid: [4, 4], is_charset: false, z_bias: 4)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A",                tx: 30.0, ty: 12.6, dir: :up, is_charset: true)
          eng.spawn_actor(:anja,    sheet: "ANJA",                    tx: 26.8, ty: 12.7, dir: :up, is_charset: true)
          eng.spawn_actor(:sigrun,  sheet: "SIGRUN",                  tx: 32.2, ty: 12.7, dir: :up, is_charset: true)
          eng.actor(:valen).set_cell(0)
          eng.actor(:kestrel).set_cell(14)

          # Beat 1: Primal Kyogre breaches on Isenmar flank inside pure-pixel hydro vortex!
          eng.play_se("Anim/Water5", volume: 95)
          eng.shake(power: 4, duration: 0.45)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_origin_beam", tx: 25.3, ty: 9.8,
                        grid: [4, 2], frames: 4..7, ticks: [3, 4, 4, 5],
                        blend: :add, scale: 1.18, z_layer: :above, origin: :foot)
          eng.spawn_actor(:kyogre, sheet: "act_war1_primal_kyogre", tx: 25.3, ty: 9.8,
                          grid: [4, 2], is_charset: false, z_bias: 20)
          eng.actor(:kyogre).play_clip(
            sheet: "act_war1_primal_kyogre", grid: [4, 2], frames: [0, 1, 2, 3],
            ticks: [4, 4, 5, 14], stay: true
          )
          eng.play_cry(:KYOGRE_1, volume: 100)
          eng.wait(1.35)
          eng.say(:EIRIK, :angry, "Isenmar! Look to the crest!", hold: 0.95, name: "Thane Eirik")
          eng.wait(0.28)
          eng.say(:EIRIK, :angry, "The sea has come to the sand!", hold: 1.10, name: "Thane Eirik")

          # Beat 2: Wide pan east to Ashkaar flank -> Reshiram unfolds in cobalt turbine inferno!
          eng.pan_camera_to(34.2, 8.6, duration: 1.00, ease: :in_out)
          eng.wait(1.05)
          eng.flash(color: [255, 226, 178], power: 195, duration: 0.28)
          eng.play_se("Anim/Fire4", volume: 95)
          eng.shake(power: 4, duration: 0.45)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_blue_flare", tx: 34.7, ty: 9.8,
                        grid: [4, 2], frames: 4..7, ticks: [3, 3, 4, 4],
                        blend: :add, scale: 1.15, z_layer: :above, origin: :foot)
          eng.spawn_actor(:reshiram, sheet: "act_war1_reshiram", tx: 34.7, ty: 9.8,
                          grid: [4, 2], is_charset: false, z_bias: 20)
          eng.actor(:reshiram).play_clip(
            sheet: "act_war1_reshiram", grid: [4, 2], frames: [0, 1, 2, 3],
            ticks: [5, 4, 5, 14], stay: true
          )
          eng.play_cry(:RESHIRAM, volume: 100)
          eng.wait(1.15)
          eng.say(:HROTHGAR, :angry, "Then let it remember fire.", hold: 1.25, name: "Dominar Hrothgar")

          #---------------------------------------------------------------------
          # ACT II — Valen's Command, Pure-Pixel Beam Launch & Tug-of-War
          # (~11.8s .. 22.8s)
          #---------------------------------------------------------------------
          eng.pan_camera_to(30.0, 8.8, duration: 0.85, ease: :in_out)
          eng.set_tone(-72, -74, -52, 62, duration: 0.85)
          eng.play_bgm("ch19_war_clash", volume: 90, tag: "ch19_war_clash")

          # Valen braces into rising dune gale and raises gauntleted command hand!
          eng.actor(:valen).play_clip(
            sheet: "act_ch19_valen_command", grid: [4, 4],
            frames: [1, 2, 4, 5, 6, 7], ticks: [6, 6, 5, 5, 10, 8], stay: true
          )
          eng.wait(1.05)
          eng.say(:VALEN, :angry, "Hold the southern ridge!", hold: 0.85)
          eng.wait(0.24)
          eng.say(:VALEN, :shocked, "Nobody crosses that seam— BRACE!!", hold: 0.95)

          # Both titans enter charge poses (frame 4) with pure-pixel swirling muzzle vortices!
          eng.actor(:valen).play_clip(
            sheet: "act_ch19_valen_command", grid: [4, 4], frames: [8, 9], ticks: [8, 12], stay: true
          )
          eng.actor(:kyogre).set_cell(4)
          eng.actor(:reshiram).set_cell(4)
          eng.play_se("Anim/Charge_Beam", volume: 95)
          eng.play_se("Anim/Fire5", volume: 82)
          eng.spawn_vfx(:muzzle_l, sheet: "pf_vfx_w3_origin_beam", tx: 26.75, ty: 9.8,
                        grid: [4, 2], frames: 4..7, ticks: [3, 3, 3, 3], loops: :forever,
                        blend: :add, scale: 0.78, offset: [0, -47], z_layer: :above)
          eng.spawn_vfx(:muzzle_r, sheet: "pf_vfx_w3_blue_flare", tx: 33.45, ty: 9.8,
                        grid: [4, 2], frames: [4, 5, 6, 5], ticks: [3, 3, 3, 3], loops: :forever,
                        blend: :add, scale: 0.78, offset: [0, -47], z_layer: :above)
          eng.zoom_map(1.18, duration: 0.95, focus: [30.0, 8.6], ease: :in_out)
          eng.wait(1.05)

          # ORIGIN PULSE vs BLUE FLARE LAUNCH!
          eng.actor(:kyogre).set_cell(5)
          eng.actor(:reshiram).set_cell(5)
          eng.actor(:valen).set_cell(10)
          eng.play_se("Anim/HyperBeam", volume: 100)
          eng.play_se("Anim/Fire6", volume: 95)
          eng.impact_beat(hitstop_sec: 0.12)

          mouth_l = 26.75
          mouth_r = 33.45
          # Center-anchored pure-pixel beams (invariant under mirror: true!) bridging mouth -> clash point!
          beam_l = eng.spawn_vfx(:beam_l, sheet: "pf_vfx_w3_origin_beam", tx: mouth_l + 0.3, ty: 9.8,
                                 grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: :forever,
                                 blend: :add, origin: :center, offset: [0, -47], z_layer: :above)
          beam_r = eng.spawn_vfx(:beam_r, sheet: "pf_vfx_w3_blue_flare", tx: mouth_r - 0.3, ty: 9.8,
                                 grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: :forever,
                                 blend: :add, mirror: true, origin: :center, offset: [0, -47], z_layer: :above)

          # 10-frame (0.33s) crisp beam extension to dead-center tx = 30.0!
          10.times do |fi|
            u = (fi + 1) / 10.0
            tip_l = mouth_l + (30.0 - mouth_l) * u
            tip_r = mouth_r - (mouth_r - 30.0) * u
            beam_l.set_tile((mouth_l + tip_l) * 0.5, 9.8)
            beam_r.set_tile((mouth_r + tip_r) * 0.5, 9.8)
            beam_l.set_scale([((tip_l - mouth_l) * 32.0) / 118.0, 0.12].max, 0.88)
            beam_r.set_scale([((mouth_r - tip_r) * 32.0) / 118.0, 0.12].max, 0.88)
            eng.step_frame
          end

          # DEAD-CENTER PURE-PIXEL CLASH COLLISION!
          eng.play_se("Anim/Explosion7", volume: 100)
          eng.play_se("Anim/Ice8", volume: 88)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash_ramp(color: [224, 248, 255], steps: [51, 136, 221, 255],
                         step_dur: 0.025, hold_dur: 0.08, fade_dur: 0.25)
          core = eng.spawn_vfx(:clash_core, sheet: "pf_vfx_w3_clash_core", tx: 30.0, ty: 9.8,
                               grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: :forever,
                               blend: :add, scale: 1.28, offset: [0, -47], z_layer: :above)

          # Sustained 3.0s (90 frames) live beam tug-of-war as emerald Trinitite heat builds beneath!
          eng.shake(power: 6, duration: 3.05, decay: false)
          eng.zoom_map(1.32, duration: 0.85, focus: [30.0, 8.6], ease: :in_out)

          90.times do |fi|
            u = fi / 90.0
            cx = 30.0 + Math.sin(u * 13.0) * 0.86 * (1.0 - 0.28 * u)
            core.set_tile(cx, 9.8)
            pulse_y = 0.88 + 0.14 * Math.sin(fi * 0.85).abs
            beam_l.set_tile((mouth_l + cx) * 0.5, 9.8)
            beam_r.set_tile((mouth_r + cx) * 0.5, 9.8)
            beam_l.set_scale(((cx - mouth_l) * 32.0) / 116.0, pulse_y)
            beam_r.set_scale(((mouth_r - cx) * 32.0) / 116.0, pulse_y)

            if fi == 26
              eng.zoom_map(1.10, duration: 0.90, focus: [30.0, 8.6], ease: :in_out)
              eng.flash(color: [215, 246, 255], power: 135, duration: 0.12)
              eng.play_se("Anim/Ice2", volume: 82)
              eng.actor(:valen).set_cell(11)
              eng.spawn_vfx(nil, sheet: "pf_vfx_w3_glass_curtain", tx: 30.0, ty: 9.4,
                            grid: [4, 2], frames: [4, 5], ticks: [5, 14], stay: :forever,
                            blend: :normal, untoned: false, opacity: 155, scale: 0.52, z_layer: :floor)
            elsif fi == 56
              eng.flash(color: [255, 234, 200], power: 145, duration: 0.12)
              eng.play_se("Anim/Fire5", volume: 85)
            elsif fi == 78
              eng.flash(color: [216, 255, 236], power: 175, duration: 0.14)
              eng.play_se("Anim/Saint7", volume: 88, pitch: 112)
            end
            eng.step_frame
          end

          #---------------------------------------------------------------------
          # ACT III — 90° BANQUET-STYLE APEX PLATE (cut_ch19_war1_90deg.png)
          # (~22.8s .. 30.4s | 3.6s Pure Silent Text-Free Panoramic Hold!)
          #---------------------------------------------------------------------
          eng.flash(color: [232, 252, 255], power: 220, duration: 0.24)
          eng.show_cut_plate(
            "cut_ch19_war1_90deg",
            fade_in: 0.22, hold: 7.2, fade_out: 0.28,
            pan: { [-10, 4] => [10, -4] }, zoom: [1.02, 1.09], shake: 1.5
          ) do |e|
            # Subtle live pure-pixel spark shimmer along the clash seam without washing out the 90° art!
            e.spawn_vfx(:p19_sparks, sheet: "pf_vfx_w3_clash_core", tx: 30.0, ty: 8.6,
                        grid: [4, 2], frames: [2, 3, 2, 3], ticks: [4, 4, 4, 4], loops: :forever,
                        blend: :add, opacity: 52, scale: 0.55, z_layer: :above)
            # 3.6s PURE SILENT TEXT-FREE CONTEMPLATION of Kyogre vs Reshiram side-view!
            e.wait(3.60)
            e.say(:VALEN, :shocked, "Sea and fire... the sand is melting straight to glass!", hold: 1.25)
            e.wait(0.28)
            e.say(:KESTREL, :angry, "Look out— the seam's about to blow!!", hold: 1.05)
            e.stop_vfx(:p19_sparks)
          end

          #---------------------------------------------------------------------
          # ACT IV — 0.42s DEAD-SILENCE bgm_cut -> TRINITITE SHOCKWAVE &
          #          KESTREL'S AIRBORNE SHIELD INTERCEPT! (~30.4s .. 35.4s)
          #---------------------------------------------------------------------
          eng.stop_vfx(:beam_l)
          eng.stop_vfx(:beam_r)
          eng.stop_vfx(:muzzle_l)
          eng.stop_vfx(:muzzle_r)
          eng.stop_vfx(:clash_core)

          # LAW 2: 0.42s DIGITAL-ZERO AUDIO VACUUM + SINGLE CHILLING BELL!
          eng.bgm_cut
          eng.play_se("Anim/HealBell", volume: 96, pitch: 118)
          eng.wait(0.42)

          # MASSIVE EMERALD TRINITITE ERUPTION ACROSS MAP 926!
          eng.play_se("Anim/Ice8", volume: 100, pitch: 78)
          eng.play_se("Anim/Explosion7", volume: 96)
          eng.play_se("Anim/Saint7", volume: 88, pitch: 90)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash_ramp(color: [188, 255, 224], steps: [64, 152, 232, 255],
                         step_dur: 0.025, hold_dur: 0.12, fade_dur: 0.45)
          eng.shake(power: 7, duration: 0.72, decay: true)
          eng.zoom_map(1.0, duration: 0.65, ease: :out_cubic)
          eng.pan_camera_to(30.0, 9.6, duration: 0.55, ease: :out_cubic)

          # Single heroic central emerald Trinitite spire between the two titans (clean desert breathing room!)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_clash_core", tx: 30.0, ty: 9.4,
                        grid: [4, 2], frames: 4..7, ticks: [3, 4, 5, 16], stay: :forever,
                        blend: :normal, untoned: false, scale: 0.72, z_layer: :mid, origin: :foot)

          # Valen recoils backward shielding brow with sand kick!
          eng.actor(:valen).play_clip(
            sheet: "act_ch19_valen_command", grid: [4, 4],
            frames: [12, 13], ticks: [6, 16], stay: true
          )
          eng.actor(:valen).move_to(30.0, 11.75, duration: 0.34, walk: false, ease: :out)

          # EMOTE #1 (Earned!): Kestrel spots the emerald shockwave racing south -> SPRINT & AIRBORNE LEAP!
          eng.actor(:kestrel).show_emote(:exclaim, duration: 0.55)
          eng.play_se("Exclaim", volume: 92)
          eng.actor(:kestrel).play_clip(
            sheet: "act_ch19_kestrel_shield", grid: [4, 4],
            frames: [1, 2, 3], ticks: [3, 3, 4], stay: true
          )
          eng.actor(:kestrel).move_to(29.0, 12.25, duration: 0.28, walk: false, ease: :out)

          # Crisp, well-spaced perimeter vitrified glass shards so the Glass Dunes floor stays open & readable!
          [
            [[27.2, 9.2], [32.8, 9.2]],
            [[25.2, 10.9], [34.8, 10.9]],
            []
          ].each_with_index do |pair, pi|
            pair.each do |gx, gy|
              eng.spawn_vfx(nil, sheet: "pf_vfx_w3_glass_curtain", tx: gx, ty: gy,
                            grid: [4, 2], frames: 4..7, ticks: [3, 4, 5, 14], stay: :forever,
                            blend: :normal, untoned: false, opacity: 178, scale: 0.36, z_layer: :floor)
            end
            eng.play_se("Anim/Ice2", volume: 74, pitch: 88 + pi * 10)
            if pi == 1
              # Kestrel launches sideways airborne dive-leap directly in front of grounded PC!
              eng.play_se("Player jump", volume: 90)
              eng.actor(:kestrel).play_clip(
                sheet: "act_ch19_kestrel_shield", grid: [4, 4],
                frames: [4, 5, 6, 7], ticks: [4, 5, 4, 12], stay: true
              )
              eng.actor(:kestrel).move_to(30.0, 12.15, duration: 0.36, walk: false, arc_h: 22.0, ease: :out_cubic)
              # Grounded, natural Protagonist takes ONE calm steady defensive step back (ZERO jerky fidgeting!)
              eng.actor(:pc).move_to(30.0, 13.05, duration: 0.32, walk: true, dir: :up)
            end
            eng.wait(0.28)
          end

          # Kestrel absorbs shockwave crouch with emerald rim flash -> eases upright!
          eng.play_se("Player bump", volume: 76, pitch: 90)
          eng.actor(:kestrel).play_clip(
            sheet: "act_ch19_kestrel_shield", grid: [4, 4],
            frames: [8, 9, 10, 11], ticks: [5, 6, 7, 8], stay: true
          )
          eng.actor(:kyogre).play_clip(
            sheet: "act_war1_primal_kyogre", grid: [4, 2], frames: [6, 7], ticks: [12, 24], stay: true
          )
          eng.actor(:reshiram).play_clip(
            sheet: "act_war1_reshiram", grid: [4, 2], frames: [6, 7], ticks: [12, 24], stay: true
          )
          eng.wait(1.15)

          #---------------------------------------------------------------------
          # ACT V — Vitrified Silence, Truce & Larch's Radio Verdict (~35.4s .. 42.3s)
          #---------------------------------------------------------------------
          eng.set_tone(-16, 6, -4, 62, duration: 1.35)
          eng.play_bgm("ch19_aftermath", volume: 78, tag: "ch19_aftermath")

          # Valen recovers composed; Kestrel checks calmly on PC; Anja & Sigrun step onto vitrified glass
          eng.actor(:valen).play_clip(
            sheet: "act_ch19_valen_command", grid: [4, 4], frames: [14, 15], ticks: [10, 16], stay: true
          )
          eng.actor(:kestrel).play_clip(
            sheet: "act_ch19_kestrel_shield", grid: [4, 4], frames: [12, 13, 14, 15], ticks: [8, 10, 8, 16], stay: true
          )
          eng.actor(:anja).move_to(28.4, 11.5, duration: 0.95, walk: true, dir: :up)
          eng.actor(:sigrun).move_to(31.6, 11.5, duration: 0.95, walk: true, dir: :up)
          eng.wait(1.10)

          # EMOTE #2 (Restrained quiet grief!): Anja gazes across the glassed desert
          eng.actor(:anja).show_emote(:ellipsis, duration: 0.85)
          eng.wait(0.55)

          eng.say(:SIGRUN, :neutral, "Father. Enough.", hold: 0.78)
          eng.wait(0.24)
          eng.say(:SIGRUN, :sad, "Nobody won this morning that the dead would agree with.", hold: 1.15)
          eng.wait(0.26)
          eng.say(:ANJA, :sad, "Eirik... the glass stops here. The Boon will settle it.", hold: 1.15)
          eng.wait(0.30)
          eng.say(:LARCH, :neutral, "That wasn't a battle to them.", hold: 0.82, name: "Larch (Radio)")
          eng.wait(0.28)
          eng.say(:LARCH, :deadpan, "That was a reading.", hold: 1.15, name: "Larch (Radio)")

          eng.wait(0.85)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.55)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # WAVE-3 SCENE 2 — Ch15 CE-1 Glassfall Rethink (~36s, Map 295 -> AF 290 -> 295)
      # "Through Her Eyes — AF 290 Sanctuary Fracture & 90° Cathedral Apex Plate"
      #-------------------------------------------------------------------------
      # DIRECTOR'S NOTE STRICTLY ENFORCED:
      #   - ZERO Protagonist inside the AF 290 historical flashback!
      #   - Grounded, calm Protagonist appears ONLY in present-day framing
      #     before and after the historical vision.
      # Emote Count: STRICTLY 2 (:exclaim on Young Voss when sky cracks,
      #              :ellipsis on present-day Kestrel when Echo Morwen turns).
      # Pure-Pixel VFX: pf_vfx_w3_glass_curtain, pf_vfx_w3_prism_light.
      # Acting Sheet:   act_ch15_glassfall_brace (JUNO.png anchored).
      # 90° Apex Plate: cut_ch15_glassfall_90deg.png (3.8s silent text-free hold!).
      #=========================================================================
      def pf_play_ch15_glassfall_rethink(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Present-Day Hollow Cathedral Framing (~0.0s .. 6.8s)
          #---------------------------------------------------------------------
          eng.transfer_map(295, 15.0, 14.0, hide_player: true)
          ev_prior = $game_map.events[2]
          ev_prior.transparent = true if ev_prior

          eng.set_tone(-46, -42, -18, 38, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch15_ominous", volume: 80, tag: "ch15_ominous")

          # Present-day party standing calmly and naturally (ZERO jerky movement!)
          eng.spawn_actor(:kestrel, sheet: "KESTREL",                 tx: 15.0, ty: 11.4, dir: :down, is_charset: true)
          eng.spawn_actor(:ysolde,  sheet: "YSOLDE",                  tx: 12.8, ty: 14.4, dir: :up,   is_charset: true)
          eng.spawn_actor(:juno,    sheet: "act_ch15_glassfall_brace", tx: 17.2, ty: 14.4, grid: [4, 4], is_charset: false)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A",                tx: 15.0, ty: 15.8, dir: :up,   is_charset: true)
          eng.actor(:juno).set_cell(15)

          eng.wait(1.05)
          eng.play_se("Anim/HealBell", volume: 90, pitch: 112)
          eng.play_se("Anim/Saint7", volume: 84)
          eng.flash(color: [228, 244, 255], power: 175, duration: 0.25)
          eng.shake(power: 3, duration: 0.30)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_prism_light", tx: 15.0, ty: 11.4,
                        grid: [4, 2], frames: [4, 5, 4, 5], ticks: [4, 4, 4, 4],
                        blend: :add, scale: 0.95, z_layer: :above)
          eng.wait(0.85)

          eng.say(:KESTREL, :angry, "Ten years, Ysolde. 'When he's ready.'", hold: 0.95)
          eng.wait(0.28)
          eng.say(:KESTREL, :angry, "I'm ready. Watch what really happened.", hold: 1.15)
          eng.wait(0.35)

          #---------------------------------------------------------------------
          # ACT II — AF 290 HISTORICAL VISION (STRICTLY ZERO PROTAGONIST!!)
          # (~6.8s .. 21.0s)
          #---------------------------------------------------------------------
          eng.flash_ramp(color: [255, 240, 206], steps: [44, 128, 214, 255],
                         step_dur: 0.03, hold_dur: 0.12, fade_dur: 0.40)
          eng.wait(0.45)
          eng.clear_actors
          eng.clear_vfxs
          # Iconic warm AF 290 sepia memory tone
          eng.set_tone(28, 12, -26, 95, duration: 0.0)

          # Historical AF 290 Sanctuary Cast — ZERO PLAYER_A ANYWHERE IN THIS VISION!
          eng.spawn_actor(:valen,   sheet: "VALEN",                   tx: 15.0, ty: 10.6, dir: :down, is_charset: true)
          eng.spawn_actor(:ines,    sheet: "trainer_LADY",            tx: 13.6, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:ch1,     sheet: "trainer_LASS",            tx: 12.2, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:ch2,     sheet: "NPC 04",                  tx: 16.4, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:ch3,     sheet: "NPC 11",                  tx: 17.8, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:voss,    sheet: "VOSS",                    tx: 19.4, ty: 11.1, dir: :left, is_charset: true)
          eng.spawn_actor(:obs,     sheet: "trainer_SCIENTIST",       tx: 20.6, ty: 11.3, dir: :left, is_charset: true)
          eng.spawn_actor(:child,   sheet: "NPC 02",                  tx: 15.0, ty: 14.5, dir: :up,   is_charset: true)
          eng.spawn_actor(:morwen,  sheet: "MORWEN",                  tx: 10.8, ty: 14.9, dir: :right, is_charset: true)
          # Archivist Witness bracing across the nave using our bespoke 4x4 brace sheet!
          eng.spawn_actor(:witness, sheet: "act_ch15_glassfall_brace", tx: 18.2, ty: 14.6, grid: [4, 4], is_charset: false)
          eng.actor(:witness).set_cell(0)

          # Soft luminous memory motes drifting slowly through the AF 290 nave
          [[11.5, 12.2], [15.0, 12.6], [18.5, 12.2]].each_with_index do |(mx, my), mi|
            eng.spawn_vfx(:"mote_#{mi}", sheet: "pf_vfx_w3_prism_light", tx: mx, ty: my,
                          grid: [4, 2], frames: [4, 5], ticks: [10, 10], loops: :forever,
                          blend: :add, opacity: 125, scale: 0.72, z_layer: :above)
          end

          eng.zoom_map(1.22, duration: 1.35, focus: [17.4, 11.4], ease: :in_out)
          eng.wait(1.55)
          eng.say(:VOSS, :neutral, "The Choir's note is climbing.", hold: 0.90, name: "Young Voss")
          eng.wait(0.28)
          eng.say(:VOSS, :neutral, "Hold the Crown steady— eighteen Plates, one reading.", hold: 1.15, name: "Young Voss")

          # Pressure drops -> witness's veil lifts -> sky cracks cleanly overhead!
          eng.zoom_map(1.26, duration: 0.90, focus: [15.0, 12.2], ease: :in_out)
          eng.actor(:witness).play_clip(
            sheet: "act_ch15_glassfall_brace", grid: [4, 4],
            frames: [1, 2, 3], ticks: [7, 8, 8], stay: true
          )
          # EMOTE #1 (Earned!): Young Voss snaps up as the harmonic overloads!
          eng.actor(:voss).show_emote(:exclaim, duration: 0.65)
          eng.play_se("Anim/Saint7", volume: 88, pitch: 118)
          eng.play_se("Anim/Ice5", volume: 84)
          eng.spawn_vfx(:fracture_hi, sheet: "pf_vfx_w3_glass_curtain", tx: 15.0, ty: 9.2,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [4, 4, 8], stay: 0.65,
                        blend: :add, opacity: 195, scale: 0.85, z_layer: :above)
          eng.wait(1.05)

          # LAW 2: 0.40s DIGITAL-ZERO DEAD-SILENCE VACUUM + CRACKING BELL!
          eng.bgm_cut
          eng.play_se("Anim/HealBell", volume: 100, pitch: 70)
          eng.play_se("Anim/Ice8", volume: 92, pitch: 112)
          eng.wait(0.40)

          # THE GLASSFALL SHARD CURTAIN DROPS!!
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash(color: [224, 255, 240], power: 235, duration: 0.28)
          eng.shake(power: 6, duration: 0.70)
          eng.play_bgm("ch15_decretum", volume: 88, tag: "ch15_decretum")
          eng.zoom_map(1.0, duration: 0.55, ease: :out_cubic)

          # Witness drops into crisp high-contrast eye-shield forearm crouch (frames 4..7)!
          eng.actor(:witness).play_clip(
            sheet: "act_ch15_glassfall_brace", grid: [4, 4],
            frames: [4, 5, 6, 7, 9, 10], ticks: [6, 7, 7, 8, 8, 8], stay: true
          )
          # Morwen dashes to shield the 5-year-old child!
          eng.actor(:morwen).move_to(14.3, 14.6, duration: 0.60, walk: true, dir: :right)

          # Pure-pixel diagonal emerald shard curtain raining across pews & creeping vitrified floor cracks!
          [[11.0, 11.4], [15.0, 11.6], [19.0, 11.4], [12.8, 15.0], [17.4, 15.0]].each_with_index do |(rx, ry), ri|
            eng.spawn_vfx(nil, sheet: "pf_vfx_w3_glass_curtain", tx: rx, ty: ry,
                          grid: [4, 2], frames: 0..3, ticks: [3, 3, 4, 4], loops: 2,
                          blend: :add, scale: 1.15, z_layer: :above)
            eng.wait(0.14) if ri.even?
          end
          eng.play_se("Anim/Ice8", volume: 94, pitch: 86)

          [[10.4, 13.6], [19.6, 13.6], [10.6, 16.2], [19.4, 16.2]].each_with_index do |(cx, cy), ci|
            eng.spawn_vfx(:"gspire_#{ci}", sheet: "pf_vfx_w3_glass_curtain", tx: cx, ty: cy,
                          grid: [4, 2], frames: 4..7, ticks: [4, 4, 5, 14], stay: :forever,
                          blend: :normal, untoned: false, scale: 0.90, z_layer: :mid, origin: :foot)
            eng.play_se("Anim/Ice2", volume: 72, pitch: 92 + ci * 8) if ci.even?
            eng.wait(0.28)
          end

          # Morwen's Mismagius rises calmly over the shielded child
          eng.spawn_actor(:mismagius, sheet: "Followers/MISMAGIUS", tx: 15.9, ty: 14.4,
                          dir: :left, grid: [4, 4], is_charset: true)
          eng.actor(:mismagius).opacity = 225
          eng.play_cry(:MISMAGIUS, volume: 82)
          eng.wait(1.35)

          #---------------------------------------------------------------------
          # ACT III — 90° BANQUET-STYLE APEX PLATE (cut_ch15_glassfall_90deg.png)
          # (~21.0s .. 30.2s | 3.8s Pure Silent Text-Free Contemplation!)
          #---------------------------------------------------------------------
          eng.show_cut_plate(
            "cut_ch15_glassfall_90deg",
            fade_in: 0.25, hold: 9.0, fade_out: 0.30,
            pan: { [0, 6] => [0, -6] }, zoom: [1.02, 1.08], shake: 0
          ) do |e|
            # Live pure-pixel falling prism motes drifting gently over the cathedral arches!
            e.spawn_vfx(:p15_motes, sheet: "pf_vfx_w3_prism_light", tx: 15.0, ty: 12.8,
                        grid: [4, 2], frames: [4, 5, 4, 5], ticks: [8, 8, 8, 8], loops: :forever,
                        blend: :add, opacity: 120, scale: 1.05, z_layer: :above)
            # 3.8s PURE SILENT TEXT-FREE HOLD letting Decretum & Morwen's embrace breathe!
            e.wait(3.80)
            e.say(:VALEN, :angry, "Find the child. Whatever it costs.", hold: 1.15)
            e.wait(0.32)
            e.say(:MORWEN, :sad, "Take them to Edda's boat at midnight.", hold: 1.05)
            e.wait(0.28)
            e.say(:MORWEN, :crying, "I'll carry the name... Kestrel, I'm sorry.", hold: 1.30)
            e.wait(0.40)
            e.stop_vfx(:p15_motes)
          end

          #---------------------------------------------------------------------
          # ACT IV — RETURN TO PRESENT-DAY CATHEDRAL (Grounded PC & Echo Morwen)
          # (~30.2s .. 36.2s)
          #---------------------------------------------------------------------
          eng.flash(color: [192, 224, 255], power: 185, duration: 0.42)
          eng.clear_actors
          eng.clear_vfxs
          eng.set_tone(-38, -28, 4, 62, duration: 0.90)
          eng.pan_camera_to(15.0, 14.8, duration: 0.65, ease: :in_out)

          # Present-day Protagonist stands calmly and naturally beside Kestrel, Ysolde & grieving Juno!
          eng.spawn_actor(:pc,          sheet: "PLAYER_A",                 tx: 15.0, ty: 16.4, dir: :up,   is_charset: true)
          eng.spawn_actor(:kestrel,     sheet: "KESTREL",                  tx: 12.6, ty: 13.0, dir: :down, is_charset: true)
          eng.spawn_actor(:ysolde,      sheet: "YSOLDE",                   tx: 17.4, ty: 13.0, dir: :down, is_charset: true)
          eng.spawn_actor(:juno,        sheet: "act_ch15_glassfall_brace", tx: 17.2, ty: 15.8, grid: [4, 4], is_charset: false)
          eng.spawn_actor(:echo_morwen, sheet: "trainer_ECHO_MORWEN",      tx: 15.0, ty: 13.8, dir: :up,   is_charset: true)
          eng.actor(:juno).play_clip(
            sheet: "act_ch15_glassfall_brace", grid: [4, 4], frames: [15, 14, 15], ticks: [10, 12, 20], stay: true
          )
          eng.actor(:echo_morwen).opacity = 205
          # Render spectral halo BEHIND Echo Morwen (:floor) so her face & 10-year turn read razor clear!
          eng.spawn_vfx(:echo_halo, sheet: "pf_vfx_w3_prism_light", tx: 15.0, ty: 13.8,
                        grid: [4, 2], frames: [4, 5], ticks: [8, 8], loops: :forever,
                        blend: :add, opacity: 145, scale: 0.66, z_layer: :floor)
          eng.wait(1.25)

          # Impossibly across ten years, Echo Morwen turns straight :down at the Protagonist!
          eng.actor(:echo_morwen).set_dir(:down)
          # EMOTE #2 (Quiet stunned hush!): Kestrel freezes witnessing the impossible turn
          eng.actor(:kestrel).show_emote(:ellipsis, duration: 0.90)
          eng.play_se("Anim/HealBell", volume: 84, pitch: 105)
          eng.zoom_map(1.26, duration: 0.95, focus: :echo_morwen, ease: :in_out)
          eng.wait(1.10)

          eng.say(:MORWEN, :neutral, "Little one. You came back.", hold: 1.05, name: "Echo Morwen")
          eng.wait(0.32)
          eng.say(:MORWEN, :sad, "I told her not to let you.", hold: 1.35, name: "Echo Morwen")

          # Echo Morwen dissolves softly into pure-pixel golden-silver motes
          eng.stop_vfx(:echo_halo)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_prism_light", tx: 15.0, ty: 13.8,
                        grid: [4, 2], frames: [5, 4, 5], ticks: [6, 6, 8], fade: 0.45,
                        blend: :add, scale: 0.85, z_layer: :above)
          24.times do |fi|
            eng.actor(:echo_morwen).opacity = (205 * (1.0 - (fi + 1) / 24.0)).round
            eng.step_frame
          end
          eng.remove_actor(:echo_morwen)
          eng.actor(:juno).set_cell(15)
          eng.zoom_map(1.0, duration: 0.70, ease: :out)
          eng.wait(0.55)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.55)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # WAVE-3 SCENE 3 — Ch21 Arceus Finale Rethink (~44s, Map 285 Summit Terrace)
      # "The Ring, The Kneel & The Dawn — 18 Golden Astral Locks, Valen's
      #  Sacrifice & 90° Crownhaven Apex Plate"
      #-------------------------------------------------------------------------
      # Emote Count: STRICTLY 2 (:exclaim on Voss when Lock #18 shatters,
      #              :ellipsis on Ilsa gazing at Valen's empty cracked Crown).
      # Protagonist: Completely grounded & natural (steady observational stance,
      #              single calm purposeful step forward when Lock #18 opens).
      # Pure-Pixel VFX: pf_vfx_w3_arceus_locks, pf_vfx_w3_prism_light.
      # Acting Sheets:  act_ch21_valen_kneel, act_ch21_arceus_bound.
      # 90° Apex Plate: cut_ch21_valen_90deg.png (4.2s silent text-free hold!).
      #=========================================================================
      def pf_play_ch21_arceus_rethink(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Bound Creator & Ornate Golden Astral Locks (~0.0s .. 8.8s)
          #---------------------------------------------------------------------
          eng.transfer_map(285, 48.5, 22.8, hide_player: true)
          [1, 2].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(-48, -64, -18, 46, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch21_arceus_bound", volume: 84, tag: "ch21_arceus_bound")

          # Cast staged cleanly on Map 285 white-stone summit terrace (PC balanced right, clear view of Valen & Crown!)
          eng.spawn_actor(:valen,     sheet: "act_ch21_valen_kneel", tx: 48.5, ty: 24.4, grid: [4, 4], is_charset: false, z_bias: 6)
          eng.spawn_actor(:ilsa,      sheet: "ILSA",                 tx: 47.1, ty: 24.8, dir: :up, is_charset: true)
          eng.spawn_actor(:voss,      sheet: "VOSS",                 tx: 51.8, ty: 23.8, dir: :up, is_charset: true)
          eng.spawn_actor(:pc,        sheet: "PLAYER_A",             tx: 49.5, ty: 26.2, dir: :up, is_charset: true)
          eng.spawn_actor(:celestine, sheet: "CELESTINE",            tx: 44.6, ty: 25.4, dir: :up, is_charset: true)
          eng.spawn_actor(:kestrel,   sheet: "KESTREL",              tx: 52.4, ty: 25.4, dir: :up, is_charset: true)
          eng.actor(:valen).set_cell(0)

          # Bound Arceus suspended high above terrace framed by pure-pixel Golden Astral Rune Seals!
          eng.spawn_actor(:arceus, sheet: "act_ch21_arceus_bound", tx: 48.5, ty: 21.0,
                          grid: [4, 2], is_charset: false, z_bias: 35)
          eng.actor(:arceus).play_clip(
            sheet: "act_ch21_arceus_bound", grid: [4, 2], frames: [0, 1, 0, 1],
            ticks: [10, 10, 10, 10], loops: :forever
          )
          eng.spawn_vfx(:locks_main, sheet: "pf_vfx_w3_arceus_locks", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [0, 1], ticks: [9, 9], loops: :forever,
                        blend: :add, scale: 1.04, z_layer: :above)
          eng.spawn_vfx(:lock_l, sheet: "pf_vfx_w3_arceus_locks", tx: 46.2, ty: 20.4,
                        grid: [4, 2], frames: [0, 1], ticks: [11, 11], loops: :forever,
                        blend: :add, opacity: 175, scale: 0.56, z_layer: :above)
          eng.spawn_vfx(:lock_r, sheet: "pf_vfx_w3_arceus_locks", tx: 50.8, ty: 20.4,
                        grid: [4, 2], frames: [1, 0], ticks: [11, 11], loops: :forever,
                        blend: :add, opacity: 175, scale: 0.56, z_layer: :above)

          eng.play_cry(:ARCEUS, volume: 100)
          eng.shake(power: 4, duration: 0.55)
          eng.zoom_map(1.24, duration: 1.25, focus: [48.5, 20.5], ease: :in_out)
          eng.wait(1.85)
          eng.zoom_map(1.0, duration: 0.55, ease: :out)
          eng.pan_camera_to(48.5, 22.9, duration: 0.55, ease: :in_out)
          eng.wait(0.75)

          eng.say(:VOSS, :shocked, "Eighteen Plates. Eighteen golden locks.", hold: 1.05)
          eng.wait(0.32)
          eng.say(:VOSS, :happy, "Look at it— it's magnificent!", hold: 1.15)

          #---------------------------------------------------------------------
          # ACT II — Holding the Door & Pure-Pixel Dawn Pillar Shattering Lock #18
          # (~8.8s .. 20.2s)
          #---------------------------------------------------------------------
          eng.zoom_map(1.16, duration: 0.80, focus: [48.5, 23.8], ease: :in_out)
          eng.play_se("Anim/Saint7", volume: 84)
          # Valen spreads both hands wide gripping the Concordance Ring pylons!
          eng.actor(:valen).play_clip(
            sheet: "act_ch21_valen_kneel", grid: [4, 4],
            frames: [1, 2, 3, 2], ticks: [8, 8, 8, 8], loops: :forever
          )
          eng.wait(1.05)

          eng.say(:ILSA, :neutral, "I've got you, Father. Little owl's got you.", hold: 1.25)
          eng.wait(0.34)
          eng.say(:VALEN, :neutral, "Go. Free it.", hold: 0.85)
          eng.wait(0.28)
          eng.say(:VALEN, :neutral, "I'll hold the door. I've had thirty years of practice.", hold: 1.35)
          eng.wait(0.40)

          # Grounded, calm Protagonist takes ONE steady purposeful step forward (unobstructed center view!)
          eng.actor(:pc).move_to(49.5, 25.5, duration: 0.65, walk: true, dir: :up)
          eng.pan_camera_to(48.5, 22.4, duration: 0.60, ease: :in_out)
          eng.zoom_map(1.0, duration: 0.55, ease: :out)
          eng.set_tone(-74, -76, -44, 62, duration: 0.65)

          # Lock #18 overheats white-gold as pure-pixel divine prism pillar ascends!
          eng.stop_vfx(:locks_main)
          eng.stop_vfx(:lock_l)
          eng.stop_vfx(:lock_r)
          eng.spawn_vfx(:lock_overheat, sheet: "pf_vfx_w3_arceus_locks", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [2, 3], ticks: [10, 12], stay: :forever,
                        blend: :add, scale: 1.12, z_layer: :above)
          eng.actor(:arceus).play_clip(
            sheet: "act_ch21_arceus_bound", grid: [4, 2], frames: [2, 3], ticks: [14, 16], stay: true
          )

          # Continuous spiraling pure-pixel divine light pillar (ZERO flat pink rectangle!)
          eng.play_se("Anim/Charge_Beam", volume: 95)
          eng.play_se("Anim/HyperBeam", volume: 88, pitch: 112)
          eng.shake(power: 5, duration: 1.65, decay: false)
          eng.spawn_vfx(:pillar_bot, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 23.6,
                        grid: [4, 2], frames: 0..3, ticks: [3, 3, 3, 3], loops: :forever,
                        blend: :add, scale: 1.05, z_layer: :above)
          eng.spawn_vfx(:pillar_top, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 20.2,
                        grid: [4, 2], frames: [2, 3, 0, 1], ticks: [3, 3, 3, 3], loops: :forever,
                        blend: :add, scale: 1.05, z_layer: :above)
          eng.zoom_map(1.22, duration: 1.35, focus: [48.5, 20.8], ease: :in_out)
          eng.wait(1.75)

          # LOCK #18 SHATTERS!! Chain explosion + flying golden lock fragments + radiant starburst!
          eng.stop_vfx(:lock_overheat)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_arceus_locks", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [4, 5, 6, 7], ticks: [4, 5, 5, 6],
                        blend: :add, scale: 1.35, z_layer: :above)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [6, 7], ticks: [5, 7],
                        blend: :add, scale: 1.0, grow: [0.85, 2.35, 0.55], fade: 0.25, z_layer: :above)
          # EMOTE #1 (Earned!): Voss reels in shock as all eighteen golden locks burst!
          eng.actor(:voss).show_emote(:exclaim, duration: 0.65)
          eng.play_se("Anim/Explosion7", volume: 96)
          eng.play_se("Anim/Ice8", volume: 94, pitch: 115)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash_ramp(color: [255, 248, 224], steps: [64, 152, 232, 255],
                         step_dur: 0.025, hold_dur: 0.10, fade_dur: 0.35)
          eng.wait(0.65)

          #---------------------------------------------------------------------
          # ACT III — 0.45s DEAD-SILENCE VACUUM -> VALEN DROPS TO ONE KNEE!
          # (~20.2s .. 28.4s)
          #---------------------------------------------------------------------
          eng.stop_vfx(:pillar_bot)
          eng.stop_vfx(:pillar_top)

          # LAW 2: 0.45s DIGITAL-ZERO AUDIO VACUUM + SOLITARY CHIME!
          eng.bgm_cut
          eng.play_se("Anim/HealBell", volume: 98, pitch: 100)
          eng.wait(0.45)

          # T-KT enters warmly as dawn tone washes across Briar Hall summit!
          eng.play_bgm("ch21_tkt", volume: 88, tag: "ch21_tkt")
          eng.set_tone(12, 8, -4, 16, duration: 1.25)
          eng.zoom_map(1.14, duration: 1.05, focus: [48.5, 23.4], ease: :in_out)

          # Valen recoils -> Crown slips off brow -> drops to ONE KNEE -> Crown clatters on marble -> looks UP in peace!
          eng.actor(:valen).play_clip(
            sheet: "act_ch21_valen_kneel", grid: [4, 4],
            frames: [4, 5, 6, 7, 8, 9, 10],
            ticks: [5, 7, 6, 8, 12, 12, 18],
            se: { 3 => "Anim/HealBell" },
            stay: true
          )
          eng.spawn_vfx(:valen_motes, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 24.2,
                        grid: [4, 2], frames: [4, 5], ticks: [9, 9], loops: :forever,
                        blend: :add, opacity: 145, scale: 0.78, z_layer: :floor)
          eng.wait(3.15)

          eng.say(:VALEN, :happy, "Little owl...", hold: 0.95)
          eng.wait(0.38)
          eng.say(:VALEN, :happy, "Velmora is free.", hold: 1.25)
          eng.wait(0.40)

          #---------------------------------------------------------------------
          # ACT IV — 90° BANQUET-STYLE APEX PLATE (cut_ch21_valen_90deg.png)
          # (~28.4s .. 35.8s | 4.2s Pure Silent Text-Free Emotional Peak!)
          #---------------------------------------------------------------------
          eng.show_cut_plate(
            "cut_ch21_valen_90deg",
            fade_in: 0.28, hold: 7.4, fade_out: 0.35,
            pan: { [-8, 4] => [8, -4] }, zoom: [1.02, 1.08], shake: 0
          ) do |e|
            # Live falling golden dawn motes floating over Ilsa, Valen, cracked Crown & Arceus!
            e.spawn_vfx(:p21_motes, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 22.8,
                        grid: [4, 2], frames: [4, 5, 4, 5], ticks: [9, 9, 9, 9], loops: :forever,
                        blend: :add, opacity: 120, scale: 0.96, z_layer: :above)
            # 4.2s COMPLETELY SILENT, TEXT-FREE CONTEMPLATION at T-KT's soaring peak!
            e.wait(4.20)
            e.say(:ILSA, :crying, "...Father.", hold: 1.55)
            e.wait(0.55)
            e.stop_vfx(:p21_motes)
          end

          #---------------------------------------------------------------------
          # ACT V — EMPTY CRACKED CROWN, FREED ARCEUS & GOLDEN DAWN (~35.8s .. 44.3s)
          #---------------------------------------------------------------------
          eng.set_tone(24, 18, 4, 6, duration: 1.25)
          eng.zoom_map(1.0, duration: 0.85, ease: :out_cubic)
          eng.pan_camera_to(48.5, 22.9, duration: 0.85, ease: :in_out)

          # Valen ascends gently into sunlit golden motes -> ONLY the empty cracked Crown stays on the stone (frame 15)!
          eng.actor(:valen).play_clip(
            sheet: "act_ch21_valen_kneel", grid: [4, 4],
            frames: [11, 12, 13, 14, 15],
            ticks: [8, 9, 9, 10, 24],
            se: { 4 => "Anim/HealBell" },
            stay: true
          )
          eng.actor(:ilsa).move_to(47.4, 24.9, duration: 0.70, walk: true, dir: :right)
          eng.wait(1.95)
          eng.stop_vfx(:valen_motes)

          # EMOTE #2 (Quiet reverent grief!): Ilsa pauses beside the empty cracked Sovereign Crown
          eng.actor(:ilsa).show_emote(:ellipsis, duration: 0.95)
          eng.wait(0.85)

          # Freed Radiant Arceus descends serenely IN FRONT OF pure-pixel golden starburst (:floor z=5 BEHIND Arceus!)
          eng.actor(:arceus).play_clip(
            sheet: "act_ch21_arceus_bound", grid: [4, 2], frames: [4, 5, 6, 7],
            ticks: [7, 8, 10, 24], stay: true
          )
          eng.actor(:arceus).move_to(48.5, 21.8, duration: 1.40, walk: false, ease: :out_cubic)
          eng.spawn_vfx(:arceus_dawn, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 20.6,
                        grid: [4, 2], frames: [6, 7], ticks: [10, 10], loops: :forever,
                        blend: :add, opacity: 150, scale: 1.18, spin: 12.0, z_layer: :floor)
          eng.wait(1.45)

          eng.play_cry(:ARCEUS, volume: 95)
          eng.play_se("Anim/Saint7", volume: 90, pitch: 108)
          eng.flash(color: [255, 248, 214], power: 185, duration: 0.36)
          eng.spawn_vfx(:dawn_spark_l, sheet: "pf_vfx_w3_prism_light", tx: 46.6, ty: 23.0,
                        grid: [4, 2], frames: [4, 5], ticks: [9, 9], loops: :forever,
                        blend: :add, opacity: 145, scale: 0.72, z_layer: :above)
          eng.spawn_vfx(:dawn_spark_r, sheet: "pf_vfx_w3_prism_light", tx: 50.4, ty: 23.0,
                        grid: [4, 2], frames: [5, 4], ticks: [9, 9], loops: :forever,
                        blend: :add, opacity: 145, scale: 0.72, z_layer: :above)
          eng.wait(1.10)

          eng.say(:ILSA, :crying, "Little light. You have carried me far.", hold: 1.25, name: "Arceus (via Ilsa)")
          eng.wait(0.36)
          eng.say(:ILSA, :happy, "I will not take what is not given.", hold: 1.45, name: "Arceus (via Ilsa)")

          eng.wait(1.15)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.65)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end
    end
  end
end

# Global convenience dispatcher for Wave-3 Rethink scenes
def pbRejuvCutsceneWave3(id, **opts)
  case id.to_sym
  when :ch19_war1_rethink, :ch19_rethink, :war1
    Prismfall::AdvancedAnimations.pf_play_ch19_war1_rethink(**opts)
  when :ch15_glassfall_rethink, :ch15_rethink, :ce1
    Prismfall::AdvancedAnimations.pf_play_ch15_glassfall_rethink(**opts)
  when :ch21_arceus_rethink, :ch21_rethink, :arceus
    Prismfall::AdvancedAnimations.pf_play_ch21_arceus_rethink(**opts)
  else
    raise ArgumentError, "Unknown Wave-3 Rejuv cutscene id: #{id.inspect}"
  end
end
