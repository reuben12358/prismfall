#===============================================================================
# Prismfall Cutscenes — Final Pair Completing the 12/12 Rejuvenation V14 Slate
#-------------------------------------------------------------------------------
# Scene H (#7):  Ch13 Glass Court — Sable Unmasked, Voss's Broadcast & The Fault
#                (:CH13_FAULT, ~39s, Live Map 287 -> 90° Broadcast -> Map 287 ->
#                 90° Fault Plate -> Live Map 174 Flooded Undercroft!)
# Scene I (#10): Ch17 Drowned Aurelia Sun Court — The Missing Piece & Voss's
#                Torch Breach (:CH17_SUN_COURT, ~38s, Live Map 186 -> 90° Voss
#                Torch Breach Plate -> Live Map 186 Breached Vault!)
#
# SIX PERMANENT LAWS COMPLIANCE:
#   - 100% Pure-Pixel 2x DS assets (ZERO MS-Paint geometry!):
#       pf_vfx_ch13_fault_vfx.png, pf_vfx_ch17_sun_court.png,
#       pf_vfx_ch17_golden_hand.png, act_ch13_kroll_vault.png,
#       act_ch17_voss_palm.png, cut_ch13_voss_broadcast_90deg.png,
#       cut_ch13_fault_90deg.png, cut_ch17_voss_breach_90deg.png.
#   - Strictly <= 3 restrained earned emote balloons per scene (2-3 max).
#   - Calm, grounded Protagonist (ZERO jerky fidgeting; ZERO PC inside pure
#     Voss Broadcast cut!).
#   - 0px static portraits + multi-box dramatic pacing + >= 3.4s text-free
#     contemplation on 90° apex plates + razor 0.42s bgm_cut audio vacuums!
#===============================================================================

module Prismfall
  module AdvancedAnimations
    class << self
      #=========================================================================
      # SCENE H (#7) — Ch13 Glass Court: Sable Unmasked, Voss's Broadcast &
      #                The Fault (:CH13_FAULT, ~39s)
      # Live Maps: Map 287 (Glass Court Tribunal) -> cut_ch13_voss_broadcast_90deg
      #            -> Map 287 (Evening Fault) -> cut_ch13_fault_90deg
      #            -> Map 174 (Flooded Undercroft Pool)
      # Emote Count: STRICTLY 3 (:exclaim Juno, :exclaim Valen, :ellipsis PC)
      #=========================================================================
      def pf_play_ch13_glass_court_fault(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Glass Court Tribunal & Sable Unmasked (Map 287, ~0.0s..14.0s)
          #---------------------------------------------------------------------
          eng.transfer_map(287, 13.0, 14.5, hide_player: true)
          $game_map.events.each_value { |ev| ev.transparent = true }

          eng.set_tone(-6, -4, 6, 10, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch13_predators", volume: 82, tag: "ch13_predators")

          # North Dais: Sovereign Valen at white chair, Provost Ilsa beside him, chained Rowan in left dock
          eng.spawn_actor(:valen,     sheet: "VALEN",                  tx: 13.0, ty: 10.1, dir: :down,  is_charset: true)
          eng.spawn_actor(:ilsa,      sheet: "ILSA",                   tx: 15.0, ty: 10.7, dir: :down,  is_charset: true)
          eng.spawn_actor(:rowan,     sheet: "ROWAN",                  tx: 10.6, ty: 11.4, dir: :right, is_charset: true)

          # Accord Court Guards flanking the glass well
          eng.spawn_actor(:guard_l,   sheet: "trainer_THORNGUARD",     tx: 10.6, ty: 13.8, dir: :right, is_charset: true)
          eng.spawn_actor(:guard_r,   sheet: "trainer_THORNGUARD",     tx: 15.6, ty: 13.8, dir: :left,  is_charset: true)

          # Left Wardens' Row (benches): Juno, Kaito, Celestine
          eng.spawn_actor(:juno,      sheet: "JUNO",                   tx: 8.4,  ty: 14.4, dir: :right, is_charset: true)
          eng.spawn_actor(:kaito,     sheet: "KAITO",                  tx: 8.4,  ty: 16.4, dir: :right, is_charset: true)
          eng.spawn_actor(:celestine, sheet: "CELESTINE",              tx: 8.4,  ty: 18.4, dir: :right, is_charset: true)

          # Right Public Gallery: civilians + 3rd row Sabine Kroll disguised in her grey hat!
          eng.spawn_actor(:spec1,     sheet: "NPC 04",                 tx: 17.6, ty: 14.4, dir: :left,  is_charset: true)
          eng.spawn_actor(:spec2,     sheet: "NPC 11",                 tx: 17.6, ty: 18.4, dir: :left,  is_charset: true)
          eng.spawn_actor(:kroll,     sheet: "act_ch13_kroll_vault",   tx: 17.6, ty: 16.4, grid: [4, 4], is_charset: false, z_bias: 8)
          eng.actor(:kroll).set_cell(0)

          # Calm, grounded Protagonist standing steadily at the central witness rail
          eng.spawn_actor(:pc,        sheet: "PLAYER_A",               tx: 13.0, ty: 16.4, dir: :up,    is_charset: true)

          eng.wait(0.85)
          eng.zoom_map(1.16, duration: 0.90, focus: [14.0, 12.6], ease: :in_out)
          eng.play_se("Anim/HealBell", volume: 72, pitch: 118)
          eng.wait(0.65)

          eng.say(:ILSA, :neutral, "Someone in this room recognises that Meridian box.", hold: 0.95)
          eng.wait(0.24)
          eng.say(:ILSA, :angry, "Public gallery. Third row. Grey hat. Sabine Kroll.", hold: 1.05)

          # EMOTE #1 (Earned!): Juno recoils in the Wardens' row as Kroll stands, tosses her grey hat & vaults!
          eng.actor(:juno).show_emote(:exclaim, duration: 0.60)
          eng.play_se("Exclaim", volume: 88)
          eng.zoom_map(1.18, duration: 0.65, focus: [15.4, 15.6], ease: :in_out)
          eng.actor(:kroll).play_clip(
            sheet: "act_ch13_kroll_vault", grid: [4, 4],
            frames: [1, 2, 3], ticks: [7, 8, 7], stay: true
          )
          eng.wait(0.80)

          eng.say(:KROLL, :happy, "Light for everyone, right? ...You're no fun any more, Provost.", hold: 1.00)

          # Fluid athletic vault over the gallery rail into the courtroom well + Sharpedo release!
          eng.play_se("Player jump", volume: 92)
          eng.actor(:kroll).play_clip(
            sheet: "act_ch13_kroll_vault", grid: [4, 4],
            frames: [4, 5, 6, 7], ticks: [4, 5, 4, 8], stay: true
          )
          eng.actor(:kroll).move_to(14.6, 15.1, duration: 0.42, walk: false, arc_h: 24.0, ease: :out_cubic)
          eng.wait(0.55)

          eng.play_se("Battle throw", volume: 92)
          eng.actor(:kroll).play_clip(
            sheet: "act_ch13_kroll_vault", grid: [4, 4],
            frames: [8, 9], ticks: [6, 14], stay: true
          )
          eng.wait(0.22)
          eng.flash(color: [220, 245, 255], power: 165, duration: 0.20)
          eng.spawn_actor(:sharpedo, sheet: "Followers/SHARPEDO", tx: 14.0, ty: 13.6, dir: :up, grid: [4, 4], is_charset: true, z_bias: 6)
          eng.play_cry(:SHARPEDO, volume: 96)
          eng.shake(power: 3, duration: 0.30)
          eng.wait(0.85)

          eng.say(:KROLL, :smug, "Inquiry. There'll be an inquiry. You'll see.", hold: 0.90)

          # Smoke pellet drop -> vanishes leaving ONLY her discarded grey hat on the glass well floor!
          eng.actor(:kroll).play_clip(
            sheet: "act_ch13_kroll_vault", grid: [4, 4],
            frames: [10, 11, 12, 13, 14, 15], ticks: [4, 4, 5, 5, 6, 18],
            se: { 1 => "Anim/fog2" }, stay: true
          )
          eng.wait(0.45)
          eng.remove_actor(:sharpedo)
          eng.wait(0.95)

          #---------------------------------------------------------------------
          # ACT II — Voss On Every Screen (cut_ch13_voss_broadcast_90deg.png)
          # (~14.2s .. 22.0s | ZERO Protagonist! Ice-cold Meridian Spin!)
          #---------------------------------------------------------------------
          eng.flash(color: [168, 232, 255], power: 210, duration: 0.22)
          eng.play_bgm("ch13_voss_spin", volume: 82, tag: "ch13_voss_spin")
          eng.play_se("Anim/Thunder4", volume: 68, pitch: 130)
          eng.show_cut_plate(
            "cut_ch13_voss_broadcast_90deg",
            fade_in: 0.18, hold: 7.5, fade_out: 0.26,
            pan: { [0, 6] => [0, -6] }, zoom: [1.02, 1.07], shake: 0
          ) do |e|
            e.wait(1.65)
            e.say(:VOSS, :sad, "If any Meridian contractor acted outside the law, they acted alone.", hold: 1.00)
            e.wait(0.24)
            e.say(:VOSS, :sad, "I am appalled. I've ordered a full inquiry.", hold: 0.95)
            e.wait(0.26)
            e.say(:VOSS, :deadpan, "MERIDIAN APPROVAL +4  —  'DIRECTOR'S CANDOUR PRAISED'", hold: 1.15, name: "Lucent Broadcast")
          end

          #---------------------------------------------------------------------
          # ACT III — Evening Session Fault Tremor, 0.42s bgm_cut &
          #           90° Collapsing Dome Fault Apex Plate (~22.0s .. 32.8s)
          #---------------------------------------------------------------------
          # Return to dusk/evening Glass Court on Map 287 (hat & Kroll gone; tension heavy!)
          eng.remove_actor(:kroll)
          eng.zoom_map(1.0, duration: 0.0)
          eng.pan_camera_to(13.0, 14.5, duration: 0.0)
          eng.set_tone(-48, -42, -16, 44, duration: 0.0)
          eng.wait(0.65)

          # Deep bedrock Arbiter Engine test-fire tremor! Floor splits with glowing cyan fissures!
          eng.play_se("Anim/Earth4", volume: 96)
          eng.shake(power: 5, duration: 1.35, decay: false)
          eng.spawn_vfx(:fiss1, sheet: "pf_vfx_ch13_fault_vfx", tx: 13.0, ty: 14.8,
                        grid: [4, 2], frames: [4, 5], ticks: [7, 16], stay: :forever,
                        blend: :normal, untoned: false, scale: 0.92, z_layer: :floor)
          eng.spawn_vfx(:fiss2, sheet: "pf_vfx_ch13_fault_vfx", tx: 13.0, ty: 12.6,
                        grid: [4, 2], frames: [4, 5], ticks: [8, 16], stay: :forever,
                        blend: :normal, untoned: false, scale: 0.84, z_layer: :floor)
          # EMOTE #2 (Earned!): Valen snaps upright as the stained-glass dome splits!
          eng.actor(:valen).show_emote(:exclaim, duration: 0.60)
          eng.play_se("Anim/Ice5", volume: 88)
          eng.spawn_vfx(:shards_top, sheet: "pf_vfx_ch13_fault_vfx", tx: 13.0, ty: 13.6,
                        grid: [4, 2], frames: 0..3, ticks: [4, 4, 4, 5], loops: 2,
                        blend: :add, scale: 1.18, z_layer: :above)
          eng.wait(1.05)

          # LAW 2: 0.42s DIGITAL-ZERO AUDIO VACUUM + SHATTERING GLASS DOME CRACK!
          eng.bgm_cut
          eng.play_se("Anim/Ice8", volume: 100, pitch: 86)
          eng.play_se("Anim/Crash", volume: 92)
          eng.wait(0.42)

          # 90° BANQUET-STYLE APEX PLATE: Collapsing Dome, Chained Rowan vs Pinned Marchetti!
          eng.impact_beat(hitstop_sec: 0.12)
          eng.flash(color: [198, 244, 255], power: 220, duration: 0.25)
          eng.play_bgm("ch13_fault_dread", volume: 88, tag: "ch13_fault_dread")
          eng.play_se("Anim/Water5", volume: 96)
          eng.play_cry(:MANECTRIC, volume: 90)
          eng.show_cut_plate(
            "cut_ch13_fault_90deg",
            fade_in: 0.20, hold: 8.6, fade_out: 0.30,
            pan: { [-8, 5] => [8, -4] }, zoom: [1.02, 1.08], shake: 1.8
          ) do |e|
            # Live glittering stained-glass shards drifting cleanly over the 90° collapse plate!
            e.spawn_vfx(:p13_shards, sheet: "pf_vfx_ch13_fault_vfx", tx: 13.0, ty: 13.6,
                        grid: [4, 2], frames: [2, 3, 2, 3], ticks: [6, 6, 6, 6], loops: :forever,
                        blend: :add, opacity: 120, scale: 0.88, z_layer: :above)
            # 3.6s PURE SILENT TEXT-FREE CONTEMPLATION letting the vertical horror land!
            e.wait(3.60)
            e.say(:ROWAN, :angry, "Forget the chain— the water's coming up from the undercroft!!", hold: 1.10)
            e.wait(0.28)
            e.say(:MARCHETTI, :panic, "The orrery ring— it's pinned my waist—!", hold: 1.05)
            e.stop_vfx(:p13_shards)
          end

          #---------------------------------------------------------------------
          # ACT IV — Flooded Undercroft Pool Moral Choice (Map 174, ~32.8s..40.0s)
          #---------------------------------------------------------------------
          eng.transfer_map(174, 10.0, 11.4, hide_player: true)
          $game_map.events.each_value { |ev| ev.transparent = true }
          eng.set_tone(-44, -38, -14, 42, duration: 0.0)

          # Left half-submerged stone island: Rowan chained cleanly beside rope coil; Wick on far left pier!
          eng.spawn_actor(:rowan_u,   sheet: "ROWAN",               tx: 5.5,  ty: 10.8, dir: :right, is_charset: true, z_bias: 6)
          eng.spawn_actor(:wick_u,    sheet: "WICK",                tx: 3.1,  ty: 10.4, dir: :right, is_charset: true, z_bias: 6)
          # Right stone dock pier (100% clear of the white rowboat!): Marchetti pinned with barking Manectric!
          eng.spawn_actor(:march_u,   sheet: "MARCHETTI",           tx: 15.2, ty: 14.0, dir: :left,  is_charset: true, z_bias: 6)
          eng.spawn_actor(:manectric, sheet: "Followers/MANECTRIC", tx: 14.1, ty: 14.0, dir: :left,  grid: [4, 4], is_charset: true, z_bias: 6)
          # Center stone stair: Calm grounded Protagonist forced to choose!
          eng.spawn_actor(:pc_u,      sheet: "PLAYER_A",            tx: 10.0, ty: 11.5, dir: :left,  is_charset: true, z_bias: 6)

          # Surging dark floodwater splash crests placed cleanly in OPEN water channels (ZERO actor overlap!)
          eng.spawn_vfx(:wave_l, sheet: "pf_vfx_ch13_fault_vfx", tx: 7.4, ty: 11.0,
                        grid: [4, 2], frames: [6, 7], ticks: [9, 9], loops: :forever,
                        blend: :normal, untoned: false, opacity: 155, scale: 0.44, z_layer: :floor)
          eng.spawn_vfx(:wave_r, sheet: "pf_vfx_ch13_fault_vfx", tx: 15.8, ty: 11.4,
                        grid: [4, 2], frames: [7, 6], ticks: [9, 9], loops: :forever,
                        blend: :normal, untoned: false, opacity: 155, scale: 0.44, z_layer: :floor)

          eng.play_se("Anim/Water2", volume: 86, pitch: 82)
          eng.play_se("Anim/metal", volume: 84, pitch: 90)
          eng.shake(power: 3, duration: 0.45)
          eng.wait(0.85)

          eng.say(:WICK, :panic, "The dock's going under! Break Rowan's chain— please!", hold: 1.05, name: "Brother Wick")
          eng.actor(:pc_u).set_dir(:right)
          eng.play_cry(:MANECTRIC, volume: 88)
          eng.wait(0.32)
          eng.say(:MARCHETTI, :sad, "I can't lift this brass... you can only reach one of us.", hold: 1.15)

          # EMOTE #3 (Restrained heavy choice silence!): Calm Protagonist turns north-center facing the rising flood
          eng.actor(:pc_u).set_dir(:down)
          eng.actor(:pc_u).show_emote(:ellipsis, duration: 0.95)
          eng.wait(1.05)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.50)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE I (#10) — Ch17 Drowned Aurelia Sun Court: The Missing Piece &
      #                 Voss's Torch Breach (:CH17_SUN_COURT, ~38s)
      # Live Map: Map 186 (Gilded Sun Court Vault) -> cut_ch17_voss_breach_90deg
      #           -> Map 186 (Breached Vault & Voss's Open Palm Offer)
      # Emote Count: STRICTLY 3 (:exclaim Nyx, :exclaim Sahar, :ellipsis PC)
      #=========================================================================
      def pf_play_ch17_sun_court_breach(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Sunken Sun Court & Eighteen Awakening Colors (Map 186, ~0.0s..11.8s)
          #---------------------------------------------------------------------
          eng.transfer_map(186, 13.5, 13.2, hide_player: true)
          $game_map.events.each_value { |ev| ev.transparent = true }

          # Deep 300-year-old sunken lapis-and-gold vault gloom so prismatic light shafts, 18 colors & torch breach POP!
          eng.set_tone(-44, -48, -16, 26, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch17_murals", volume: 82, tag: "ch17_murals")

          # Door-sized Broken Golden Hand Keystone Cradle resting squarely on the circular sun medallion!
          eng.spawn_vfx(:golden_hand, sheet: "pf_vfx_ch17_golden_hand", tx: 13.5, ty: 12.8,
                        grid: [4, 2], frames: [0], ticks: [30], loops: :forever,
                        blend: :normal, untoned: false, scale: 0.82, z_layer: :mid)

          # Ethereal slanting golden-prismatic sunken temple light shafts cutting through the gloom
          eng.spawn_vfx(:shaft_l, sheet: "pf_vfx_ch17_sun_court", tx: 10.4, ty: 11.4,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 165, scale: 1.05, z_layer: :above)
          eng.spawn_vfx(:shaft_r, sheet: "pf_vfx_ch17_sun_court", tx: 16.6, ty: 11.4,
                        grid: [4, 2], frames: [2, 3, 0, 1], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 165, scale: 1.05, z_layer: :above)

          # Cast: Sahar studying inscription beside cradle, Nyx descending marble stair, calm PC approaching!
          eng.spawn_actor(:sahar, sheet: "SAHAR",    tx: 11.3, ty: 13.4, dir: :right, is_charset: true)
          eng.spawn_actor(:nyx,   sheet: "NYX",      tx: 15.6, ty: 10.8, dir: :down,  is_charset: true)
          eng.spawn_actor(:pc,    sheet: "PLAYER_A", tx: 13.5, ty: 16.4, dir: :up,    is_charset: true)

          # Calm, natural walk up to the giant broken golden hand (clean breathing room below plinth!)
          eng.wait(0.65)
          eng.actor(:pc).move_to(13.5, 15.0, duration: 1.25, walk: true, dir: :up)
          eng.wait(1.35)

          # THE EIGHTEEN COLORS KINDLE ONE BY ONE AROUND THE GOLDEN MEDALLION!!
          eng.play_se("Anim/Shiny sparkle", volume: 90, pitch: 96)
          eng.play_se("Anim/Saint7", volume: 86, pitch: 108)
          eng.flash(color: [255, 250, 224], power: 165, duration: 0.30)

          # Broken Golden Hand awakens through frames 1 -> 2 -> 3 (colorless fingertips -> radiant prismatic halo!)
          eng.stop_vfx(:golden_hand)
          eng.spawn_vfx(:golden_hand, sheet: "pf_vfx_ch17_golden_hand", tx: 13.5, ty: 12.8,
                        grid: [4, 2], frames: [1, 2, 3], ticks: [10, 12, 30], stay: :forever,
                        blend: :normal, untoned: true, scale: 0.82, z_layer: :mid)

          # Staggered 18-color prismatic sanctuary rings kindling vividly around the circular sun court!
          [
            [11.0, 11.6], [16.0, 11.6], [11.0, 14.9], [16.0, 14.9]
          ].each_with_index do |(mx, my), mi|
            eng.spawn_vfx(:"prism_#{mi}", sheet: "pf_vfx_ch17_golden_hand", tx: mx, ty: my,
                          grid: [4, 2], frames: [4, 5, 6, 7], ticks: [8, 8, 8, 8], loops: :forever,
                          blend: :add, opacity: 225, scale: 0.84, z_layer: :floor)
            eng.play_se("Anim/HealBell", volume: 68, pitch: 96 + mi * 8) if mi.even?
            eng.wait(0.32)
          end

          #---------------------------------------------------------------------
          # ACT II — "You're The Missing Piece" & PC's 4th Authored Line (~11.8s..20.4s)
          #---------------------------------------------------------------------
          eng.zoom_map(1.18, duration: 0.90, focus: [13.5, 13.4], ease: :in_out)
          # EMOTE #1 (Earned!): Nyx gasps stepping softly down beside the glowing medallion
          eng.actor(:nyx).show_emote(:exclaim, duration: 0.65)
          eng.actor(:nyx).move_to(15.5, 12.6, duration: 0.70, walk: true, dir: :left)
          eng.wait(0.80)

          eng.say(:NYX, :shocked, "Oh...", hold: 0.65)
          eng.wait(0.22)
          eng.say(:NYX, :sad, "Oh, darling. You're the missing piece.", hold: 1.05)
          eng.wait(0.28)
          eng.say(:SAHAR, :neutral, "'Here rests the One that is every color and none.'", hold: 1.05)
          eng.wait(0.26)
          eng.say(:SAHAR, :sad, "It's the Legend Plate. You're carrying what was torn from this hand.", hold: 1.10)
          eng.wait(0.36)
          # Protagonist's canonical fourth authored line!
          eng.say(:PLAYER_A, :neutral, "...I know. I think I always knew. I just didn't have the word.", hold: 1.25, name: "Avery")
          eng.wait(0.35)

          #---------------------------------------------------------------------
          # ACT III — 0.42s bgm_cut -> PLASMA TORCH BREACH -> 90° VOSS BREACH PLATE!
          # (~20.4s .. 31.6s | 3.6s Pure Silent Text-Free Contemplation!)
          #---------------------------------------------------------------------
          eng.zoom_map(1.0, duration: 0.40, ease: :out)
          # LAW 2: 0.42s DIGITAL-ZERO AUDIO VACUUM + RAZOR PLASMA TORCH IGNITION!
          eng.bgm_cut
          eng.play_se("Anim/Slash1", volume: 96, pitch: 125)
          eng.play_se("Anim/Fire6", volume: 94, pitch: 112)
          eng.wait(0.42)

          # Blinding white-hot plasma cutting-torch arc slices through the dark eastern golden wall!
          eng.impact_beat(hitstop_sec: 0.12)
          eng.flash(color: [255, 224, 148], power: 215, duration: 0.24)
          eng.shake(power: 5, duration: 0.65)
          eng.play_se("Anim/Explosion7", volume: 90, pitch: 108)
          eng.play_se("Anim/Fire4", volume: 88)
          eng.spawn_vfx(:torch_arc, sheet: "pf_vfx_ch17_sun_court", tx: 18.2, ty: 12.6,
                        grid: [4, 2], frames: [4, 5, 4, 5], ticks: [5, 6, 5, 6],
                        blend: :add, scale: 1.25, z_layer: :above)
          eng.spawn_vfx(:breach_sparks, sheet: "pf_vfx_ch17_sun_court", tx: 18.2, ty: 13.0,
                        grid: [4, 2], frames: [6, 7], ticks: [5, 5], loops: :forever,
                        blend: :add, opacity: 235, scale: 1.02, z_layer: :above)

          # EMOTE #2 (Earned!): Sahar & PC spin right toward the blazing molten wall breach!
          eng.actor(:sahar).show_emote(:exclaim, duration: 0.60)
          eng.actor(:pc).set_dir(:right)
          eng.actor(:nyx).set_dir(:right)
          eng.wait(1.05)

          # Clear all untoned @vfx_vp map VFX before cutting to 90° plate so ZERO top-down sprites bleed onto plate!
          eng.stop_vfx(:golden_hand)
          eng.stop_vfx(:shaft_l)
          eng.stop_vfx(:shaft_r)
          eng.stop_vfx(:breach_sparks)

          # 90° BANQUET-STYLE APEX PLATE: Voss stepping through molten breach extending bare open palm!
          eng.play_bgm("ch17_voss_treachery", volume: 84, tag: "ch17_voss_treachery")
          eng.show_cut_plate(
            "cut_ch17_voss_breach_90deg",
            fade_in: 0.22, hold: 8.8, fade_out: 0.30,
            pan: { [8, 4] => [-8, -3] }, zoom: [1.02, 1.08], shake: 0.6
          ) do |e|
            # Subtle molten spark shower drifting cleanly on the far right breach edge without blocking Voss or Hand!
            e.spawn_vfx(:p17_sparks, sheet: "pf_vfx_ch17_sun_court", tx: 18.8, ty: 12.6,
                        grid: [4, 2], frames: [6, 7], ticks: [6, 6], loops: :forever,
                        blend: :add, opacity: 80, scale: 0.66, z_layer: :above)
            # 3.6s PURE SILENT TEXT-FREE HOLD letting the double-open-palm visual rhyme land!
            e.wait(3.60)
            e.say(:VOSS, :happy, "Oh, look at that. Ten years of telemetry... nothing compares to seeing it live.", hold: 1.15)
            e.wait(0.28)
            e.say(:VOSS, :neutral, "Gods are absentee landlords. I'm making sure we never need one again.", hold: 1.15)
            e.stop_vfx(:p17_sparks)
          end

          #---------------------------------------------------------------------
          # ACT IV — Breached Sun Court & Voss's Open Palm Offer (~31.6s..39.0s)
          #---------------------------------------------------------------------
          eng.set_tone(-38, -42, -14, 24, duration: 0.65)
          # Cleanly restore the awakened Broken Golden Hand, sunken light shafts & molten breach embers!
          eng.spawn_vfx(:golden_hand, sheet: "pf_vfx_ch17_golden_hand", tx: 13.5, ty: 12.8,
                        grid: [4, 2], frames: [3], ticks: [30], loops: :forever,
                        blend: :normal, untoned: true, scale: 0.82, z_layer: :mid)
          eng.spawn_vfx(:shaft_l, sheet: "pf_vfx_ch17_sun_court", tx: 10.4, ty: 11.4,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 145, scale: 1.05, z_layer: :above)
          eng.spawn_vfx(:shaft_r, sheet: "pf_vfx_ch17_sun_court", tx: 16.6, ty: 11.4,
                        grid: [4, 2], frames: [2, 3, 0, 1], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 145, scale: 1.05, z_layer: :above)
          eng.spawn_vfx(:breach_embers, sheet: "pf_vfx_ch17_sun_court", tx: 18.2, ty: 12.8,
                        grid: [4, 2], frames: [6, 7], ticks: [7, 7], loops: :forever,
                        blend: :add, opacity: 185, scale: 0.85, z_layer: :above)

          # Voss steps smoothly into the Sun Court flanked by two Meridian salvage divers!
          eng.spawn_actor(:voss,   sheet: "act_ch17_voss_palm",           tx: 17.2, ty: 14.4, grid: [4, 4], is_charset: false, z_bias: 8)
          eng.spawn_actor(:crew_1, sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 18.2, ty: 12.6, dir: :left, is_charset: true)
          eng.spawn_actor(:crew_2, sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 18.2, ty: 15.0, dir: :left, is_charset: true)
          eng.actor(:voss).set_cell(3)

          eng.actor(:voss).play_clip(
            sheet: "act_ch17_voss_palm", grid: [4, 4],
            frames: [3, 4, 5, 7], ticks: [7, 7, 7, 8], stay: true
          )
          eng.actor(:voss).move_to(15.6, 14.7, duration: 0.95, walk: false, ease: :out_cubic)
          eng.actor(:nyx).move_to(15.2, 11.4, duration: 0.65, walk: true, dir: :down)
          eng.zoom_map(1.14, duration: 0.90, focus: [14.5, 13.8], ease: :in_out)
          eng.wait(1.05)

          # Voss smoothly extends his bare right palm open — echoing the Broken Golden Hand directly beside him!
          eng.play_se("Anim/HealBell", volume: 74, pitch: 90)
          eng.actor(:voss).play_clip(
            sheet: "act_ch17_voss_palm", grid: [4, 4],
            frames: [8, 9, 10, 11, 12], ticks: [6, 7, 8, 12, 24], stay: true
          )
          eng.wait(0.85)

          eng.say(:VOSS, :neutral, "Stand with me at the Festival. No child in Velmora will ever be Fixed again.", hold: 1.15)
          eng.wait(0.30)
          eng.say(:VOSS, :sad, "Your mother wilted in exile because of a broken god. I can fix the god.", hold: 1.30)

          # EMOTE #3 (Quiet stunned weight!): Calm Protagonist stares at Voss's open palm
          eng.actor(:pc).show_emote(:ellipsis, duration: 0.95)
          eng.wait(1.10)
          eng.zoom_map(1.0, duration: 0.65, ease: :out)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.55)
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

# Global convenience dispatcher for Final Pair (Scenes #7 & #10 -> 12/12 Complete!)
def pbRejuvCutsceneFinalPair(id, **opts)
  case id.to_sym
  when :ch13_fault, :ch13_glass_court_fault, :ch13
    Prismfall::AdvancedAnimations.pf_play_ch13_glass_court_fault(**opts)
  when :ch17_sun_court, :ch17_sun_court_breach, :ch17
    Prismfall::AdvancedAnimations.pf_play_ch17_sun_court_breach(**opts)
  else
    raise ArgumentError, "Unknown Final Pair Rejuv cutscene id: #{id.inspect}"
  end
end
