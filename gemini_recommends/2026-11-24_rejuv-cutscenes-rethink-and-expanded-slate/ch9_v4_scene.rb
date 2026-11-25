module Prismfall
  module AdvancedAnimations
    class << self
      #-------------------------------------------------------------------------
      # SCENE 2 — Ch9 Peak #2 (DIRECTOR'S CUT v4 — TRUE 10/10 CINEMA):
      # "Trevenant's Ingrain, The 3-Wave Breach, 90° Unmasking & Arrival Epilogue"
      # Live Map 295 (Gen 5 B2W2 Crimson Emergency Reliquary; Wednesday swaps
      # map_id: 295 -> 264) + 90-degree Banquet-style Side-View Cathedral Cut!
      # ZERO Protagonist during Acts I-VI (pure 4-cast cinema: Mourner, Trevenant,
      # Juno, Nell); Protagonist walks naturally in from the south entrance ONLY
      # in Act VII after the unmasking reveal!
      #-------------------------------------------------------------------------
      def play_ch9_trevenant_unmasking(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # Helper lambdas for exact pixel staging during the 90-degree side-view cut
          s2t_foot = proc { |sx, sy| eng.screen_to_tile(sx, sy) }
          s2t_ctr  = proc { |sx, sy| eng.screen_to_tile(sx, sy + 16) }

          #=====================================================================
          # ACT I — Reliquary Sabotage & Juno's Heroic Leap to Shield Nell!
          #         (ZERO Protagonist! $game_player.transparent = true)
          #=====================================================================
          eng.transfer_map(295, 15.0, 11.4, hide_player: true)
          eng.set_tone(-28, -86, -78, 42, duration: 0.0)
          eng.set_emergency_vignette([216, 28, 38], max_alpha: 74, pulse_hz: 1.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch9_tension", volume: 80, tag: "ch9_tension")

          # Tactical vertical aisle layout (NORTH -> SOUTH, 100% spatial continuity):
          #   Reliquary Plinth (15.0, 10.4) — fires crimson crystal spears SOUTHWARD
          #   5-Tile Ingrain Root Wall (y = 14.65) — erupts NORTH of Trevenant!
          #   Trevenant (15.0, 16.35) — 100% Row 3 UP-facing (NORTH) back view on all 16 frames!
          #   Mourner (15.0, 18.02) — dives in front of Juno & Nell, spins NORTH, throws UPWARD!
          #   Nell starts exposed in center aisle (15.0, 19.55); Juno leaps from (13.5, 19.80)
          #   right in front of Nell (15.0, 19.12) to shield her with her body!
          eng.spawn_vfx(:reliquary, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [0, 1], ticks: [10, 10], loops: :forever,
                        blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          eng.spawn_actor(:mourner, sheet: "act_ch9_mourner_throw_up", tx: 15.0, ty: 11.7,
                          grid: [4, 4], is_charset: false)
          eng.spawn_actor(:juno, sheet: "JUNO",   tx: 13.5, ty: 19.80, dir: :up, is_charset: true)
          eng.spawn_actor(:nell, sheet: "NPC 02", tx: 15.0, ty: 19.55, dir: :up, is_charset: true)

          # Mourner frantically pulling Splitter wires off the Fist Plate Reliquary!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [0, 1, 0, 1],
            ticks: [7, 7, 6, 6], loops: 1, stay: true
          )
          eng.zoom_map(1.44, duration: 1.0, focus: [15.0, 10.9], ease: :in_out)
          eng.wait(1.08)

          # Audio Vacuum #1: dry CLICK on the last Splitter -> Emote #1 (!) on Mourner ONLY!
          eng.bgm_cut
          eng.stop_vfx(:reliquary)
          eng.spawn_vfx(:reliquary_arm, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [2], hold: 0.65, stay: :forever,
                        blend: :normal, untoned: true, z_layer: :mid, origin: :foot)
          eng.play_se("Battle catch click", volume: 100, pitch: 130)
          eng.actor(:mourner).show_emote(:exclaim, duration: 0.55)
          eng.wait(0.42)

          # Partial Fist Plate Shatter! Bell chime + crimson shockwave ring!
          eng.stop_vfx(:reliquary_arm)
          eng.spawn_vfx(:reliquary_crack, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [3, 4, 5, 6, 7], ticks: [4, 6, 6, 6, 6],
                        loops: :forever, blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          eng.play_se("Anim/HealBell", volume: 95, pitch: 72)
          eng.play_se("Anim/Ice8", volume: 95)
          eng.play_bgm("ch9_tension", volume: 86, tag: "ch9_tension")
          eng.flash_ramp(color: [255, 196, 208], steps: [51, 136, 221, 255], step_dur: 0.03, hold_dur: 0.10, fade_dur: 0.35)
          eng.shake(power: 5, duration: 0.45)
          eng.spawn_vfx(nil, sheet: "pf_vfx_shockwave_ring", tx: 15.0, ty: 10.6,
                        grid: [4, 2], frames: 4..7, ticks: [3, 3, 4, 4],
                        blend: :add, scale: 1.0, grow: [0.6, 3.2, 0.7], fade: 0.25, z_layer: :above)
          eng.zoom_map(1.0, duration: 0.42, ease: :out)
          eng.wait(0.42)

          # Crimson glass frost races SOUTH down the central carpet toward exposed Nell!
          eng.pan_camera_to(15.0, 15.9, duration: 1.05, ease: :in_out)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [2, 3], ticks: [4, 6]
          )
          [11.9, 13.0, 14.1, 15.2, 16.3].each_with_index do |gy, gi|
            [-1.1, 0.0, 1.1].each do |gx|
              eng.spawn_vfx(nil, sheet: "pf_vfx_glass_frost", tx: 15.0 + gx, ty: gy,
                            grid: [4, 2], frames: 4..7, ticks: [2, 2, 3, 3],
                            stay: :forever, blend: :normal, opacity: 140, scale: 0.88, z_layer: :floor)
            end
            if gi == 3
              # Exposed Nell freezes trembling in the center aisle!
              eng.actor(:nell).tremble(duration: 1.35, amp: 2.0, freq: 48.0)
            end
            eng.play_se("Anim/Ice2", volume: 70, pitch: 95 + gi * 6) if gi.even?
            eng.wait(0.15)
          end

          # Multi-Box Sabotage & Shielding Beat:
          # Box 1 (Juno, shocked): "Wait—the glass—"
          eng.say(:JUNO, :shocked, "Wait—the glass—", hold: 0.58)
          eng.wait(0.14)

          # Juno spots Nell exposed in the center aisle (Emote #2 !!), sprints & LEAPS right in front of Nell!
          eng.actor(:juno).show_emote(:double_exclaim, duration: 0.75)
          eng.play_se("Exclaim", volume: 95)
          eng.actor(:juno).set_dir(:right)
          eng.wait(0.14)
          eng.actor(:juno).move_to(14.15, 19.55, duration: 0.16, walk: true, dir: :right)
          eng.wait_for_move(:juno)

          # HEROIC JUMP ARC: Juno physically leaps across flagstones directly in front of Nell!
          eng.play_se("Player jump", volume: 92)
          eng.actor(:juno).move_to(15.0, 19.12, duration: 0.34, walk: false, dir: :right, arc_h: 24.0, ease: :out_cubic)
          eng.actor(:nell).move_to(14.85, 19.82, duration: 0.24, walk: true, dir: :up)
          eng.actor(:nell).crouch_to(3, duration: 0.20)
          eng.actor(:nell).tremble(duration: 0.90, amp: 2.0, freq: 46.0)
          eng.wait_for_move(:juno)

          # Juno lands shielding Nell with her body (pose_JUNO :flinch + protective crouch)!
          eng.play_se("Player bump", volume: 78, pitch: 90)
          eng.shake(power: 2, duration: 0.12)
          eng.actor(:juno).set_pose("pose_JUNO", 1)
          eng.actor(:juno).crouch_to(4, duration: 0.12)

          # Box 2 (Juno, panic): "NELL!!"
          eng.say(:JUNO, :panic, "NELL!!", hold: 0.45)
          eng.wait(0.12)
          # Box 3 (Juno, panic): "Get down—!!"
          eng.say(:JUNO, :panic, "Get down—!!", hold: 0.58)

          #=====================================================================
          # ACT II — Mourner's Dive South, Spin-Turn NORTH & UPWARD Dusk Ball Throw!
          #=====================================================================
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [3, 4, 4, 5],
            ticks: [3, 4, 4, 5], se: { 1 => "Fly" }
          )
          eng.actor(:mourner).move_to(15.0, 18.02, duration: 0.56, walk: false, arc_h: 24.0, ease: :out_cubic)
          eng.wait_for_move(:mourner)
          eng.shake(power: 3, duration: 0.18)
          eng.actor(:juno).restore_charset("JUNO", dir: :up)
          eng.wait(0.16)

          # Mourner faces UP (NORTH) & whips arm UPWARD launching Dusk Ball NORTHWARD!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [6, 7, 8, 9],
            ticks: [5, 7, 3, 7],
            se: { 2 => "Battle throw" }
          )
          eng.wait(0.60) # Launch ball right on frame 8 upward whip smear!
          eng.spawn_vfx(nil, sheet: "pf_vfx_duskball_release", tx: 15.0, ty: 17.9,
                        grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: 3,
                        blend: :normal, untoned: true, move_to: [15.0, 16.35, 0.42],
                        arc_h: 36.0, z_layer: :above)
          eng.wait(0.42)

          # Dusk Ball pops open at vanguard tile (15.0, 16.35) -> UP-FACING TREVENANT MATERIALIZES!
          eng.play_se("Battle ball drop", volume: 90)
          eng.play_se("Anim/Darkness6", volume: 88, pitch: 115)
          eng.spawn_vfx(nil, sheet: "pf_vfx_duskball_release", tx: 15.0, ty: 16.35,
                        grid: [4, 2], frames: 4..7, ticks: [2, 3, 3, 3],
                        blend: :add, scale: 1.4, z_layer: :above)
          eng.spawn_actor(:trevenant, sheet: "act_ch9_trevenant_ingrain_up", tx: 15.0, ty: 16.35,
                          grid: [4, 4], is_charset: false, z_bias: 8)
          eng.play_cry(:TREVENANT, volume: 100)

          #=====================================================================
          # ACT III — UP-FACING TREVENANT INGRAIN SLAM & 5-TILE NORTH ROOT WALL!
          #=====================================================================
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: 0..8,
            ticks: [4, 4, 5, 7, 10, 2, 6, 6, 6],
            se: { 6 => "Anim/Earth4", 7 => "Anim/LeechSeedPlanted" },
            shake: { 6 => [6, 0.45] },
            flash: { 6 => [[168, 255, 176], 125, 0.22] },
            on_frame: {
              6 => proc do |e, _a, _fi|
                # 5-tile gnarled emerald Ingrain Root Wall erupts NORTH of Trevenant (y = 14.65)!
                [15.0, 14.0, 16.0, 13.0, 17.0].each_with_index do |rx, ri|
                  e.spawn_vfx(:"root_#{ri}", sheet: "pf_vfx_ingrain_roots", tx: rx, ty: 14.65,
                              grid: [4, 2], frames: [0, 1, 2, 3, 4],
                              ticks: [2 + ri, 3, 3, 4, 8], stay: :forever,
                              blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
                end
              end
            }
          )
          # Mourner spreads both arms wide facing NORTH shielding Juno & Nell behind him!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [10], ticks: [20], stay: true
          )
          eng.wait_for_clip(:trevenant)
          eng.wait(0.24)

          #=====================================================================
          # ACT IV — 3 ESCALATING BARRAGE WAVES (TIGHT 4-CAST DRAMA, ZERO SPAM!)
          #=====================================================================

          # --- WAVE 1: HOLD! (Two-volley 6 crimson spears -> emerald deflects) ---
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [8, 9, 8, 9, 8, 9, 8],
            ticks: [7, 6, 7, 6, 7, 6, 14], stay: true
          )
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [10, 11, 10, 11],
            ticks: [10, 12, 10, 20], stay: true
          )
          w1_pairs = [
            [13.0, 3], [17.0, 4], [15.0, 0],
            [14.0, 1], [16.0, 2], [15.0, 0]
          ]
          w1_pairs.each_with_index do |(sx, ri), si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: sx, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.15, move_to: [sx, 14.15, 0.28], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 78, pitch: 106 + si * 4) if si.even?
            eng.wait(0.22)
            eng.stop_vfx(:"root_#{ri}")
            eng.stop_vfx(:"root_w1_#{ri}")
            eng.spawn_vfx(:"root_w1_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: sx, ty: 14.65,
                          grid: [4, 2], frames: [0], hold: 0.45, stay: :forever,
                          blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: sx, ty: 14.05,
                          grid: [4, 2], frames: [7], hold: 0.14, blend: :add, scale: 0.72, z_layer: :above)
            if si == 2 || si == 5
              eng.shake(power: 4, duration: 0.28)
              eng.play_se("Anim/hit", volume: 88, pitch: 112 + si * 2)
              eng.flash(color: [164, 255, 184], power: 82, duration: 0.16)
              eng.actor(:nell).tremble(duration: 0.35, amp: 2.0)
            end
            eng.wait(0.12) if si == 2
          end
          eng.play_se("Anim/Ice8", volume: 76, pitch: 120)
          eng.zoom_map(1.15, duration: 0.75, focus: [15.0, 15.7], ease: :in_out)
          eng.wait(0.80)

          # --- WAVE 2: OVERWHELMING! (Cracks spread -> splinters -> Multi-Box!) ---
          eng.set_tone(-42, -96, -84, 52, duration: 0.85)
          eng.set_emergency_vignette([232, 24, 38], max_alpha: 92, pulse_hz: 2.0)
          eng.play_se("Anim/Earth1", volume: 84, pitch: 88)
          eng.wait(0.24)

          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [10, 11, 10, 11, 10, 11, 10, 11],
            ticks: [6, 6, 6, 6, 6, 6, 6, 10], stay: true
          )
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [11, 12, 11, 12, 11, 12],
            ticks: [7, 7, 7, 7, 7, 14], stay: true
          )

          w2_specs_a = [
            [14.8, 13.0], [15.2, 17.0], [14.6, 14.0], [15.4, 16.0],
            [15.0, 15.0], [14.2, 13.4], [15.8, 16.6], [15.0, 15.0]
          ]
          w2_specs_a.each_with_index do |(x0, x1), si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: x0, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.24, move_to: [x1, 14.15, 0.24], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 84, pitch: 102 + si * 4) if si.even?
            if si == 3
              # Glowing crimson stress cracks spread across the emerald barrier!
              5.times { |ri| eng.stop_vfx(:"root_w1_#{ri}"); eng.stop_vfx(:"root_#{ri}") }
              [15.0, 14.0, 16.0, 13.0, 17.0].each_with_index do |rx, ri|
                eng.spawn_vfx(:"root_w2_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.65,
                              grid: [4, 2], frames: [1], hold: 0.4, stay: :forever,
                              blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
              end
              eng.shake(power: 5, duration: 0.34)
              eng.play_se("Anim/Ice8", volume: 82, pitch: 106)
              eng.actor(:trevenant).flash_color(255, 110, 140, 170, duration: 0.20)
            elsif si == 7
              # Center tiles crack deep crimson + emerald bark splinters shower south!
              [0, 1, 2].each { |ri| eng.stop_vfx(:"root_w2_#{ri}") }
              [15.0, 14.0, 16.0].each_with_index do |rx, ri|
                eng.spawn_vfx(:"root_w2b_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.65,
                              grid: [4, 2], frames: [2], hold: 0.4, stay: :forever,
                              blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
                eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.8,
                              grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                              scale: 0.56, drift: [(ri - 1) * 34, 68], gravity: 110, z_layer: :above)
              end
              eng.play_se("Anim/Ice8", volume: 92, pitch: 90)
              eng.play_cry(:TREVENANT, volume: 84)
              eng.shake(power: 6, duration: 0.42)
              eng.actor(:trevenant).flash_color(255, 180, 200, 200, duration: 0.24)
              # Juno ducks tighter shielding Nell (pose_JUNO :flinch + crouch):
              eng.actor(:juno).set_pose("pose_JUNO", 1)
              eng.actor(:juno).crouch_to(5, duration: 0.12)
            end
            eng.wait(0.17)
          end
          eng.wait(0.24)

          # Wave 2 Multi-Box Dialogue Beat:
          # Box 4 (Juno, panic): "The roots—they're splintering!!"
          eng.say(:JUNO, :panic, "The roots—they're splintering!!", hold: 0.72)

          # Wave 2 SLAMS HARDER between boxes!
          [[14.0, 14.0], [16.0, 16.0], [14.8, 14.8], [15.2, 15.2]].each_with_index do |(x0, x1), si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: x0, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.32, move_to: [x1, 14.15, 0.21], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 88, pitch: 112 + si * 6) if si.even?
            if si == 2
              eng.play_se("Anim/Ice8", volume: 92, pitch: 86)
              eng.shake(power: 6, duration: 0.36)
              eng.actor(:trevenant).flash_color(255, 196, 210, 210, duration: 0.22)
              eng.actor(:nell).tremble(duration: 0.65, amp: 2.0)
            end
            eng.wait(0.14)
          end
          eng.actor(:juno).restore_charset("JUNO", dir: :up)
          eng.wait(0.14)

          # Box 5 (Juno, shocked): "Hold on! Please, hold on—"
          eng.say(:JUNO, :shocked, "Hold on! Please, hold on—", hold: 0.72)

          # --- WAVE 3: PENETRATION!! Center root wall BLOWS OPEN! ---
          eng.zoom_map(1.28, duration: 0.70, focus: [15.0, 15.9], ease: :in_out)
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [11, 10, 12, 13],
            ticks: [6, 6, 10, 18], stay: true
          )
          w3_xs = [14.0, 16.0, 14.6, 15.4, 15.0, 14.8, 15.2, 15.0]
          w3_xs.each_with_index do |sx, si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: sx, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.32, move_to: [sx, 14.2, 0.21], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 88, pitch: 116 + si * 4) if si.even?
            if si == 4
              eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: 15.0, ty: 14.7,
                            grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                            scale: 0.62, drift: [10, 75], gravity: 115, z_layer: :above)
              eng.shake(power: 5, duration: 0.25)
            end
            eng.wait(0.13)
          end
          eng.wait(0.12)

          # BLOWN-OPEN JAGGED BREACH GAP IN CENTER ROOT WALL (x = 15.0)!!
          eng.stop_vfx(:root_w2b_0)
          eng.spawn_vfx(:root_breach_center, sheet: "pf_vfx_ingrain_roots_breach", tx: 15.0, ty: 14.65,
                        grid: [4, 2], frames: [3], hold: 1.0, stay: :forever,
                        blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
          3.times do |bi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: 14.6 + bi * 0.4, ty: 14.8,
                          grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                          scale: 0.70, drift: [(bi - 1) * 48, 88], gravity: 130, z_layer: :above)
          end
          eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: 15.0, ty: 14.4,
                        grid: [4, 2], frames: [7], hold: 0.22, blend: :add, scale: 0.95, z_layer: :above)
          eng.play_se("Anim/Explosion2", volume: 96)
          eng.play_se("Anim/Ice8", volume: 98, pitch: 84)
          eng.play_cry(:TREVENANT, volume: 92)
          eng.flash(color: [255, 196, 212], power: 190, duration: 0.22)
          eng.shake(power: 7, duration: 0.48)
          eng.actor(:trevenant).flash_color(255, 220, 232, 220, duration: 0.24)
          eng.wait(0.42) # Horror beat letting the smoking breached center gap register!

          # Stray spear + FATAL JAGGED SPEAR punching STRAIGHT THROUGH THE BREACH toward Juno & Nell!
          eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: 14.7, ty: 13.8,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                        blend: :add, scale: 1.25, move_to: [14.2, 18.4, 0.28], z_layer: :above)
          eng.play_se("Anim/Slash9", volume: 86, pitch: 115)
          eng.wait(0.18)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [12, 14, 15],
            ticks: [3, 3, 4], stay: true
          )
          # Juno throws arms over Nell!
          eng.actor(:juno).set_pose("pose_JUNO", 1)
          eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: 15.0, ty: 13.6,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 4,
                        blend: :add, scale: 1.45, move_to: [15.0, 18.6, 0.36], z_layer: :above)
          eng.play_se("Anim/Ice2", volume: 96, pitch: 132)
          eng.wait(0.28)

          #=====================================================================
          # ACT V — 90-DEGREE BANQUET SIDE-VIEW CATHEDRAL CUT!
          #   - PURE 4-CAST CINEMA (ZERO Protagonist!):
          #       LEFT:  Vertical Ingrain Wall (sx=78) + LEFT-facing Trevenant (sx=152)
          #       MID:   Diving Mourner (sx=356 -> 274 -> 302)
          #       RIGHT: Shielding Juno (sx=388) + clearly visible trembling Nell (sx=444)
          #   - ZERO emote balloon clutter — pure physical acting & cinema!
          #   - ZERO DOUBLE-MASK: ONLY the single mask on Mourner's own face
          #     shatters at 1.55x pbZoomMap with crisp face-matched shards!
          #=====================================================================
          eng.flash(color: [255, 224, 236], power: 195, duration: 0.12)
          eng.clear_actors
          eng.clear_vfxs
          eng.zoom_map(1.0, duration: 0.0)
          eng.set_tone(0, 0, 0, 0, duration: 0.0)
          eng.set_backdrop("pf_vfx_ch9_sideview_hall", z: 1)

          # LEFT (sx = 78): Vertical side-profile Ingrain Root Wall cracking -> blowing open!
          wx, wy = s2t_foot.call(78, 318)
          eng.spawn_vfx(:side_wall, sheet: "pf_vfx_ingrain_wall_side", tx: wx, ty: wy,
                        grid: [4, 1], frames: [1, 2], ticks: [10, 10], stay: :forever,
                        blend: :normal, untoned: false, scale: 1.15, z_layer: :mid, origin: :foot)

          # LEFT-MID (sx = 152): Side-profile Trevenant (Row 1 LEFT) bracing against the storm!
          ttx, tty = s2t_foot.call(152, 312)
          eng.spawn_actor(:side_trev, sheet: "Followers/TREVENANT", tx: ttx, ty: tty,
                          dir: :left, grid: [4, 4], is_charset: true, scale: 2.0, z_bias: 20)

          # RIGHT-MID (sx = 388): Juno crouched physically shielding right in front of Nell!
          jtx, jty = s2t_foot.call(388, 314)
          eng.spawn_actor(:side_juno, sheet: "JUNO", tx: jtx, ty: jty,
                          dir: :left, grid: [4, 4], is_charset: true, scale: 2.0, z_bias: 26)
          eng.actor(:side_juno).off_y = 6.0

          # RIGHT (sx = 444): Nell clearly visible crouched & trembling right behind Juno!
          ntx, nty = s2t_foot.call(444, 310)
          eng.spawn_actor(:side_nell, sheet: "NPC 02", tx: ntx, ty: nty,
                          dir: :left, grid: [4, 4], is_charset: true, scale: 2.0, z_bias: 18)
          eng.actor(:side_nell).off_y = 6.0
          eng.actor(:side_nell).tremble(duration: 2.2, amp: 2.0, freq: 44.0)

          # Establish clean 4-character 90-deg cathedral as 3 horizontal spears hammer left wall!
          [[14, 206, 78, 212, 0.24], [8, 256, 80, 254, 0.24], [10, 238, 86, 240, 0.23]].each_with_index do |(x0, y0, x1, y1, dur), si|
            stx0, sty0 = s2t_ctr.call(x0, y0)
            stx1, sty1 = s2t_ctr.call(x1, y1)
            eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: stx0, ty: sty0,
                          grid: [4, 2], frames: [6], hold: dur, blend: :add, scale: 1.08,
                          move_to: [stx1, sty1, dur], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 88, pitch: 114 + si * 8)
            eng.shake(power: 4, duration: 0.18) if si == 1
            eng.wait(0.26)
          end

          # Side-profile vertical root wall BLOWS OPEN into Frame 3 jagged chest-height breach gap!
          eng.stop_vfx(:side_wall)
          eng.spawn_vfx(:side_wall_breach, sheet: "pf_vfx_ingrain_wall_side", tx: wx, ty: wy,
                        grid: [4, 1], frames: [3], hold: 1.0, stay: :forever,
                        blend: :normal, untoned: false, scale: 1.15, z_layer: :mid, origin: :foot)
          sp_x, sp_y = s2t_ctr.call(110, 240)
          eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: sp_x, ty: sp_y,
                        grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                        scale: 0.85, drift: [95, -18], gravity: 110, z_layer: :above)
          eng.play_se("Anim/Ice8", volume: 96, pitch: 88)
          eng.shake(power: 6, duration: 0.30)
          eng.actor(:side_trev).flash_color(255, 190, 210, 200, duration: 0.22)
          eng.actor(:side_trev).tremble(duration: 0.28, amp: 2.0, freq: 42.0)
          eng.wait(0.26)

          # ====================================================================
          # DEAD SILENCE (bgm_cut!) + FATAL SPEAR + SAKUGA SLOW-MO DIVE!!
          # ====================================================================
          eng.bgm_cut
          eng.play_se("Fly", volume: 90, pitch: 82)

          # Fatal horizontal blazing crimson spear rockets straight out of the breach!
          fsx0, fsy0 = s2t_ctr.call(90, 250)
          fsx1, fsy1 = s2t_ctr.call(264, 250)
          eng.spawn_vfx(:fatal_spear, sheet: "pf_vfx_ingrain_roots_breach", tx: fsx0, ty: fsy0,
                        grid: [4, 2], frames: [6], hold: 0.78, blend: :add, scale: 1.28,
                        move_to: [fsx1, fsy1, 0.74], z_layer: :above)

          # MOURNER LEAPS HORIZONTALLY INTO FRAME shielding BOTH Juno and Nell!
          mtx0, mty0 = s2t_foot.call(356, 312)
          mtx1, mty1 = s2t_foot.call(274, 312)
          eng.spawn_actor(:side_mourner, sheet: "act_ch9_mourner_dive_side", tx: mtx0, ty: mty0,
                          grid: [4, 2], is_charset: false, scale: 1.0, z_bias: 45)
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [0, 1, 2],
            ticks: [4, 6, 10], stay: true
          )
          eng.actor(:side_mourner).move_to(mtx1, mty1, duration: 0.76, walk: false, arc_h: 38.0, ease: :out_cubic)
          # Smooth 1.55x pbZoomMap centered directly onto Mourner's face for single-mask impact!
          eng.zoom_map(1.55, duration: 0.74, focus: :side_mourner, ease: :out_cubic)
          eng.wait(0.74)

          # 2-FRAME HIGH-CONTRAST B&W SILHOUETTE IMPACT + 0.25s HITSTOP FREEZE RIGHT ON HIS FACE!!
          eng.stop_vfx(:fatal_spear)
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [3], ticks: [20], stay: true
          )
          ix, iy = s2t_ctr.call(262, 254)
          eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: ix, ty: iy,
                        grid: [4, 2], frames: [7], hold: 0.24, blend: :add, scale: 1.05, z_layer: :above)
          eng.play_se("Cut", volume: 100, pitch: 78)
          eng.play_se("Anim/Ice8", volume: 96, pitch: 118)
          eng.impact_beat(hitstop_sec: 0.25)
          eng.flash(color: [255, 242, 248], power: 235, duration: 0.22)
          eng.shake(power: 7, duration: 0.34)

          # SINGLE-MASK SLOW-MO SHATTER DIRECTLY OFF MOURNER'S FACE (ZERO DUPLICATE GIANT MASK!)
          eng.clear_vignette
          eng.set_tone(-44, -52, -40, 88, duration: 0.75)

          # Frame 4: Spiderweb crack right across the ONE mask on Mourner's own face!
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [4], ticks: [20], stay: true
          )
          mtx_c, mty_c = s2t_foot.call(282, 312)
          eng.actor(:side_mourner).move_to(mtx_c, mty_c, duration: 0.65, walk: false, ease: :out)
          eng.wait(0.32)
          eng.play_se("Anim/Ice2", volume: 84, pitch: 140) # Crisp porcelain crack in dead silence!
          gx, gy = s2t_ctr.call(266, 254)
          eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: gx, ty: gy,
                        grid: [4, 2], frames: [7], hold: 0.16, blend: :add, scale: 0.45, z_layer: :above)
          eng.wait(0.33)

          # Frame 5: Mask shears directly off Mourner's face exposing Rowan's bare eyes!
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [5], ticks: [16], stay: true
          )
          mtx_s, mty_s = s2t_foot.call(290, 312)
          eng.actor(:side_mourner).move_to(mtx_s, mty_s, duration: 0.55, walk: false, ease: :out)
          eng.wait(0.55)

          # Frame 6 -> Frame 7: Unmasked Rowan tumbles & drops to one knee!
          # Spawn ONLY crisp face-matched (scale 0.26) porcelain halves & lily petals flying OFF his face!
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [6, 7],
            ticks: [12, 40], stay: true
          )
          mtx2, mty2 = s2t_foot.call(302, 312)
          eng.actor(:side_mourner).move_to(mtx2, mty2, duration: 0.95, walk: false, ease: :out)

          # Spawn mask halves directly from Frame 5's sheared mask position (left of Rowan's bare face!)
          shx_l, shy_l = s2t_ctr.call(248, 254)
          shx_r, shy_r = s2t_ctr.call(262, 252)
          eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: shx_l, ty: shy_l,
                        grid: [4, 2], frames: [4], hold: 1.55, blend: :normal, untoned: true,
                        scale: 0.26, drift: [-58, -18], gravity: 58, spin: -115, fade: 0.28, z_layer: :above)
          eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: shx_r, ty: shy_r,
                        grid: [4, 2], frames: [5], hold: 1.55, blend: :normal, untoned: true,
                        scale: 0.26, drift: [26, -38], gravity: 54, spin: 96, fade: 0.28, z_layer: :above)
          [[244, 244, 6, -24, -12], [268, 240, 7, 22, -16], [254, 258, 6, -12, -4]].each_with_index do |(px, py, fr, vx, vy), pi|
            ptx, pty = s2t_ctr.call(px, py)
            eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: ptx, ty: pty,
                          grid: [4, 2], frames: [fr], hold: 1.75, blend: :normal, untoned: true,
                          scale: 0.28 + (pi % 2) * 0.04, drift: [vx, vy], gravity: 14,
                          spin: (pi.even? ? 28 : -24), fade: 0.35, z_layer: :above)
          end
          # Smoothly ease zoom back 1.55x -> 1.12x framing LEFT-facing Trevenant, kneeling Rowan, Juno & Nell!
          eng.zoom_map(1.12, duration: 1.15, focus: :side_mourner, ease: :out)
          eng.wait(1.40)

          #=====================================================================
          # ACT VI — Cut Back to Top-Down Map 295 & Intimate Unmasking Reveal!
          #          (STILL ZERO Protagonist — strictly Juno, Nell, Rowan & Trevenant!)
          #=====================================================================
          eng.clear_backdrop
          eng.clear_actors
          eng.clear_vfxs
          eng.set_camera_tile(15.0, 16.5)
          eng.set_tone(-34, -56, -48, 86, duration: 0.0) # Dying crimson fading to cool twilight!
          eng.zoom_map(1.34, duration: 0.0, focus: [15.0, 18.2])

          # Restore live scarred Map 295 aftermath: cracked Reliquary, floor frost, breached root wall!
          eng.spawn_vfx(:reliquary_after, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [5, 6, 7], ticks: [10, 10, 10], loops: :forever,
                        blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          [11.9, 13.0, 14.1, 15.2, 16.3].each do |gy|
            [-1.1, 0.0, 1.1].each do |gx|
              eng.spawn_vfx(nil, sheet: "pf_vfx_glass_frost", tx: 15.0 + gx, ty: gy,
                            grid: [4, 2], frames: [7], hold: 1.0, stay: :forever,
                            blend: :normal, opacity: 120, scale: 0.88, z_layer: :floor)
            end
          end
          [[13.0, 1], [14.0, 2], [15.0, 3], [16.0, 2], [17.0, 1]].each_with_index do |(rx, fr), ri|
            eng.spawn_vfx(:"root_after_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.65,
                          grid: [4, 2], frames: [fr], hold: 1.0, stay: :forever,
                          blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
          end

          # Scarred Trevenant remaining rooted facing NORTH toward the breached wall (100% Row 3 back view!)
          eng.spawn_actor(:trevenant, sheet: "act_ch9_trevenant_ingrain_up", tx: 15.0, ty: 16.35,
                          grid: [4, 4], is_charset: false, z_bias: 6)
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [14, 14, 15],
            ticks: [18, 18, 80], stay: true
          )

          # Juno & Nell matching exact side-view continuity (ZERO Protagonist!)
          eng.spawn_actor(:juno, sheet: "JUNO",   tx: 15.0,  ty: 19.35, dir: :up, is_charset: true)
          eng.actor(:juno).off_y = 4.0
          eng.spawn_actor(:nell, sheet: "NPC 02", tx: 14.55, ty: 19.85, dir: :up, is_charset: true)
          eng.actor(:nell).off_y = 3.0

          # Unmasked Rowan collapsing to his knees with head bowed deep (Frame 13)!
          eng.spawn_actor(:mourner, sheet: "act_ch9_mourner_unmask", tx: 15.0, ty: 18.0,
                          grid: [4, 4], is_charset: false, z_bias: 10)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [9, 10, 13],
            ticks: [10, 12, 90], stay: true
          )

          # Broken porcelain mask half tumbles & CLATTERS clearly beside Rowan at (15.75, 18.42)!
          eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: 15.10, ty: 17.85,
                        grid: [4, 2], frames: [4], hold: 0.36, blend: :normal, untoned: true,
                        scale: 0.30, move_to: [15.75, 18.42, 0.36], arc_h: 18.0, spin: 180, z_layer: :above)
          eng.set_tone(-26, -30, -14, 112, duration: 2.1)
          eng.wait(0.36)

          # Dry ceramic clink as broken mask hits stone -> unobstructed split mask & white lily!
          eng.play_se("Anim/Ice8", volume: 74, pitch: 134)
          eng.spawn_vfx(:mask_floor, sheet: "pf_vfx_smoke_and_motes", tx: 15.75, ty: 18.42,
                        grid: [4, 2], frames: [6], hold: 1.0, stay: :forever,
                        blend: :normal, untoned: false, z_layer: :mid)

          # Subtle perimeter motes & drifting white lily petals (Rowan & lily 100% unobstructed!)
          6.times do |mi|
            mx = mi < 3 ? (12.2 + mi * 0.7) : (16.4 + (mi - 3) * 0.7)
            eng.spawn_vfx(nil, sheet: "pf_vfx_smoke_and_motes", tx: mx, ty: 19.2 - (mi % 3) * 0.9,
                          grid: [4, 2], frames: [7], hold: 16.0, blend: :add,
                          drift: [3 - (mi % 3) * 3, -10 - (mi % 4) * 2], fade: 1.4, z_layer: :above)
          end
          [[12.6, 16.5, 6], [16.9, 16.8, 7], [17.4, 18.4, 6]].each_with_index do |(px, py, fr), pi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: px, ty: py,
                          grid: [4, 2], frames: [fr], hold: 16.0, blend: :normal, untoned: true,
                          scale: 0.28, drift: [4 - pi * 3, 7], gravity: 1.2,
                          spin: (pi.even? ? 16 : -14), fade: 1.4, z_layer: :above)
          end

          # Nell uncrouches and peeks out trembling beside Juno in stunned silence!
          eng.wait(0.45)
          eng.actor(:nell).crouch_to(0, duration: 0.35)
          eng.actor(:nell).move_to(14.20, 19.65, duration: 0.42, walk: true, dir: :up)
          eng.actor(:nell).tremble(duration: 0.75, amp: 2.0, freq: 38.0)

          # Complete the 1.45s pure dead-silence hold after mask clatter!
          eng.wait(1.00)

          # Juno slowly rises from her crouch with Emote #3 (ONE quiet '...' balloon)!
          eng.actor(:juno).crouch_to(0, duration: 0.42)
          eng.actor(:juno).move_to(15.0, 19.18, duration: 0.42, walk: true, dir: :up)
          eng.actor(:juno).show_emote(:dots, duration: 0.95)
          eng.wait(0.45)

          # === INTIMATE 6-BOX EMOTIONAL REVEAL (Juno, Nell & Uncle Rowan) ===
          # Box 6 (Juno, shocked): "...Wait." (0.75s silent beat!)
          eng.say(:JUNO, :shocked, "...Wait.", hold: 0.80)
          eng.wait(0.75)

          # Box 7 (Juno, crying): "...That voice..."
          eng.say(:JUNO, :crying, "...That voice...", hold: 0.90)

          # Rowan slowly lifts his bare face; Never Meant to Belong solo violin softly enters!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [13, 14, 15, 12],
            ticks: [5, 9, 10, 140], stay: true
          )
          eng.play_bgm("ch9_never_meant", volume: 82, tag: "ch9_never_meant")
          eng.wait(0.55)

          # Box 8 (Juno, crying): "...Uncle Rowan?"
          eng.say(:JUNO, :crying, "...Uncle Rowan?", hold: 1.05)

          # Quiet violin pause — Nell shifts softly in disbelief (zero balloons, zero alert ping!)
          eng.actor(:nell).hop(height: 5, duration: 0.18)
          eng.wait(0.75)

          # Box 9 (Rowan, sad): "Juno..." (0.55s pause)
          eng.say(:ROWAN, :sad, "Juno...", hold: 0.75)
          eng.wait(0.55)

          # Box 10 (Rowan, sad): "Don't look at me like that."
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [15], ticks: [80], stay: true
          )
          eng.say(:ROWAN, :sad, "Don't look at me like that.", hold: 1.02)

          # Fresh delicate white lily petals drift across the twilight hall
          [[13.4, 16.8, 6], [16.5, 17.2, 7], [15.9, 18.2, 6]].each_with_index do |(px, py, fr), pi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: px, ty: py,
                          grid: [4, 2], frames: [fr], hold: 10.0, blend: :normal, untoned: true,
                          scale: 0.28, drift: [3 - pi * 2, 7], gravity: 1.0,
                          spin: (pi.even? ? 14 : -12), fade: 1.2, z_layer: :above)
          end
          eng.wait(0.55)

          # Box 11 (Rowan, neutral): "Look at the flowers."
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [12], ticks: [200], stay: true
          )
          eng.say(:ROWAN, :neutral, "Look at the flowers.", hold: 1.25)

          #=====================================================================
          # ACT VII — POST-UNMASKING ARRIVAL EPILOGUE!
          #           Camera pulls back to reveal the south entrance;
          #           Protagonist walks naturally into the shattered clearing
          #           AFTER the event, teeing up post-cutscene gameplay!
          #=====================================================================
          eng.zoom_map(1.0, duration: 1.05, focus: [15.0, 18.5], ease: :in_out)
          eng.pan_camera_to(15.0, 19.2, duration: 1.05, ease: :in_out)
          eng.wait(1.35)

          # Protagonist enters naturally from offscreen south entrance (crisp B2W2 walk stride!)
          eng.spawn_actor(:pc, sheet: "PLAYER_A", tx: 15.35, ty: 25.0, dir: :up, is_charset: true)
          eng.actor(:pc).move_to(15.35, 20.65, duration: 2.05, walk: true, dir: :up, ease: :linear)
          eng.wait(1.15)
          # Hearing footsteps, Juno turns south (keeping close to Nell), then Nell turns too!
          eng.actor(:juno).set_dir(:down)
          eng.wait(0.18)
          eng.actor(:nell).set_dir(:down)
          eng.wait_for_move(:pc)
          eng.wait(0.35)

          # Box 12 (Juno, crying): "...You made it."
          eng.say(:JUNO, :crying, "...You made it.", hold: 0.95)
          eng.actor(:juno).set_dir(:up)
          eng.wait(0.24)
          eng.actor(:nell).set_dir(:up)
          eng.wait(0.12)

          # Box 13 (Juno, sad): "Look — his mask... it broke."
          eng.say(:JUNO, :sad, "Look — his mask... it broke.", hold: 1.15)

          # Quiet resignation hold — Rowan meets your eyes beside the broken mask & white lily
          eng.bgm_fade(1.4)
          eng.wait(1.35)
          eng.letterbox(false, duration: 0.50)
          eng.wait(0.45)
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
