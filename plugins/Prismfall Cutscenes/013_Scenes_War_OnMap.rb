#===============================================================================
# Prismfall Cutscenes - 013 The war climax, staged the Rejuvenation/Reborn way
#-------------------------------------------------------------------------------
# :WAR_CLIMAX  "The Beam Clash on the Glass Dunes" (story/13_CUTSCENES.md WAR-1, SPINE Rev 18)
#
# The war is fought on land, on the Glass Dunes in Ossaria's western desert (map 926):
# Isenmar's host from Skaldfast in the west (left), Ashkaar's legions from the Siege
# Camp in the east (right), the Northern Sea along the top. Staged like those games'
# map set pieces (design/CUTSCENE_RESEARCH.md):
# * the stage is a tile map shown 1:1 (map pixels are world pixels). Until map 926
#   exists it is a picture composed from Reborn's and Rejuvenation's desert tiles:
#   Graphics/Pictures/pfw_glass_dunes.png (tools/build_desert.py). When map 926 is
#   built, export its render to the same file (mapgen/render.py) and keep the
#   coordinates below, or change them.
# * legendaries and armies are overworld-scale charsets / acting sheets whose
#   frames are stepped like move routes; never battle sprites;
# * Kyogre's flood-sea is a 6-frame sheet that rolls in over the sand and drains
#   back out; Blue Flare leaves a trail of glass patches; the clash glasses the
#   wet sand in a ring; a breaking wave sets into glass;
# * the beams are segment cells (Rejuvenation's anim_beam), the clash point and
#   impacts are animation cells; flashes ramp up, the camera follows, cuts and zooms.
# Variables are unchanged (variant:, legends:, overpower:, ...). If the art
# overlay is missing, the procedural version (:WAR_CLIMAX_PROCEDURAL) plays.
#===============================================================================
module Prismfall
  module Cutscene
    WAR_STAGE = "Graphics/Pictures/pfw_glass_dunes"

    WAR_CLIMAX_BLOCK = proc do
      if !Gfx.resolve(WAR_STAGE)
        include_scene(:WAR_CLIMAX_PROCEDURAL, **@vars)
        next
      end
      variant = var(:variant, :A)
      legends = var(:legends, true)
      overpower = var(:overpower, false) && [:B, :C].include?(variant)
      clash_end = :fizzle
      clash_end = :both if variant == :A2
      clash_end = ((variant == :B) ? :b : :a) if overpower
      who = WAR_SPEAKERS
      ch = "Graphics/Characters/"
      an = "Graphics/Animations/"
      # The Wardens' aces stand in when :war_legend kept the legendaries away:
      # Marisol's Gyarados out of the trench-lines' meltwater, Sigrun's Salamence.
      water_cs = (legends) ? var(:water_charset, "pfw_kyogre") : var(:water_charset, "pfw_gyarados")
      fire_cs  = (legends) ? var(:fire_charset, "pfw_reshiram") : var(:fire_charset, "pfw_salamence")
      water_cry = (legends) ? var(:water_legend, :KYOGRE) : var(:water_mon, :GYARADOS)
      fire_cry  = (legends) ? var(:fire_legend, :RESHIRAM) : var(:fire_mon, :SALAMENCE)

      # Stage coordinates (map pixels; 32 px tiles; the stage is 64 x 24 tiles).
      water_at = [700, 418]          # Kyogre, in the hollow the flood fills
      fire_at  = [1060, 372]         # Reshiram, hovering over the dunes
      clash_c  = [864, 334]          # the meeting point, over the flood's waterline
      ground   = 420
      two_shot = [870, 318]
      gate     = [1505, 324]         # the Siege Camp's gate, on the earthwork
      crest    = [1000, 262]         # the bone-carters' banner
      mesa     = [1830, 196]         # Meridian's ledge on the sandstone mesa
      flood_at = [768, 576]          # bottom centre of the flood sheet's cells (768 x 576)
      flames = { sheet: an + "pfw_fx_sky_burn", grid: [5, 5], frames: 5..9, hold: 0.09, loops: :forever, scale: 0.5 }
      steam = { sheet: an + "pfw_fx_steam", grid: [5, 4], frames: 5..8, hold: 0.12, loops: :forever, scale: 0.7 }

      #--- the stage -----------------------------------------------------------
      background image: WAR_STAGE, parallax: 1.0
      letterbox true, duration: 0
      camera at: [256, 318]
      tone to: [-26, -30, -10, 24], duration: 0                # low dawn over bone sand
      bgm :bgm_war_field
      bgs :bgs_war, volume: 70
      # Two drilled blocks a side under their banners, the Wardens' Pokemon as a front line, the rulers out ahead.
      army :isenmar, charsets: ["pfw_soldier_isenmar"], count: 16, rows: 2, blocks: 2, gap: 56,
           area: [60, 396, 320, 40], facing: :right
      army :ice_mons, charsets: ["pfw_walrein", "pfw_beartic", "pfw_sealeo", "pfw_walrein"], count: 4, rows: 2,
           area: [408, 388, 76, 52], facing: :right
      army :ashkaar, charsets: ["pfw_soldier_ashkaar"], count: 16, rows: 2, blocks: 2, gap: 56,
           area: [1390, 396, 320, 40], facing: :left
      army :fire_mons, charsets: ["pfw_houndoom", "pfw_camerupt", "pfw_camerupt", "pfw_houndoom"], count: 4, rows: 2,
           area: [1290, 384, 76, 56], facing: :left
      army :riders, charsets: ["pfw_charizard", "pfw_salamence"], count: 4, rows: 2,
           area: [1420, 236, 250, 44], facing: :left, walk: true
      [[52, 380], [240, 380], [420, 372]].each_with_index do |pt, i|
        actor :"ban_i#{i}", sheet: ch + "pfw_banner_isenmar", grid: [1, 1], at: pt
      end
      [[1340, 372], [1570, 380], [1730, 380]].each_with_index do |pt, i|
        actor :"ban_a#{i}", sheet: ch + "pfw_banner_ashkaar", grid: [1, 1], at: pt
      end
      # Eirik on the lead ice-sledge; the Dominar on the Siege Camp's earthwork.
      actor :sled, sheet: ch + "pfw_sled", grid: [1, 1], at: [500, 458]
      actor :sled2, sheet: ch + "pfw_sled", grid: [1, 1], at: [318, 470]
      actor :eirik, charset: "pfw_eirik", at: [496, 446], dir: :right, z: 970
      actor :hrothgar, charset: "pfw_hrothgar", at: gate, dir: :down
      # The bone-carters' white banner on a dune crest between the hosts, the carters stopped dead beside it.
      actor :carter_banner, sheet: ch + "pfw_banner_carters", grid: [1, 1], at: crest
      actor :carter1, charset: "pfw_bone_carter", at: [crest[0] - 30, crest[1] + 6], dir: :down
      actor :carter2, charset: "pfw_bone_carter", at: [crest[0] + 32, crest[1] + 8], dir: :left
      [[1290, 486], [1470, 478], [1650, 490], [1800, 446]].each_with_index do |pt, i|
        fx_sheet flames[:sheet], **flames, at: pt, z: 400 + pt[1], id: :"camp#{i}"
      end
      [[930, 92], [1060, 84], [1190, 96]].each_with_index do |pt, i|      # the Steamline's wall of steam
        fx_sheet steam[:sheet], **steam, at: pt, z: 300, id: :"steamline#{i}"
      end
      emit :snow, area: [0, 0, 600, 30], rate: 22, id: :snow
      emit :embers, area: [1200, 380, 760, 160], rate: 22, id: :embers
      emit :sand, area: [700, 160, 500, 360], rate: 14, id: :sand
      emit :smoke, area: [1280, 200, 480, 30], rate: 5, layer: :back, id: :camp_smoke

      #--- 1: establishing pan across both hosts --------------------------------
      pan to: [1792, 318], duration: 6.0, ease: :in_out
      wait 6.2

      #--- 2: the sea stands up and pours in over the dunes; the sea-beast rises -
      cut at: [760, 196], zoom: 1.0
      se :rumble
      shake power: 3, duration: 3.6, decay: false
      if legends
        actor :flood, sheet: an + "pfw_fx_flood", grid: [3, 2], frame: 0, at: flood_at, z: 455
        actor :water, sheet: ch + "pfw_kyogre_primal", grid: [4, 4], frame: 0, at: water_at, opacity: 0, mouth: [14, -58]
        actor :water_rise, sheet: ch + "pfw_kyogre_rise", grid: [4, 4], frame: 12, at: water_at, opacity: 0
        fx_sheet an + "pfw_fx_origin_pulse", grid: [5, 3], frames: 5..9, hold: 0.1, at: [820, 70], scale: 1.6, z: 900
        wait 0.5
        flipbook :flood, frames: 0..5, holds: [0.5, 0.42, 0.42, 0.42, 0.42, 0.5]
        move :carter1, by: [140, -60], duration: 2.4, walk: true
        move :carter2, by: [150, -50], duration: 2.4, walk: true
        pan to: [730, 330], duration: 2.7, ease: :in_out
        emit :steam, area: [560, 170, 360, 60], rate: 18, duration: 2.6, id: :surf
        wait 2.8
        remove :carter1
        remove :carter2
        fade :water_rise, to: 255, duration: 0
      else
        actor :water, charset: water_cs, at: water_at, dir: :right
        submerge :water, to: 64, duration: 0
        wait 0.9
      end
      fx_sheet ch + "pfw_kyogre_rise", grid: [4, 4], frames: [12, 13, 14, 15], hold: 0.1, loops: :forever,
               at: [water_at[0], water_at[1] - 40], z: 900, id: :ripples
      fx_sheet an + "pfw_fx_steam", grid: [5, 4], frames: 15..19, hold: 0.1, at: [water_at[0], water_at[1] - 30], scale: 1.5, z: 980
      wait 0.6
      if legends
        flipbook :water_rise, frames: [0, 1, 2, 3, 4], holds: [0.25, 0.22, 0.22, 0.25, 0.45], wait: true
        remove :water_rise
        fade :water, to: 255, duration: 0
        idle :water, frames: 0..3, hold: 0.16
      else
        submerge :water, to: 12, duration: 1.4, ease: :out, wait: true
      end
      fx_sheet an + "pfw_fx_origin_pulse", grid: [5, 3], frames: 5..8, hold: 0.08, at: [water_at[0] - 70, water_at[1] - 30], blend: :add, z: 960
      fx_sheet an + "pfw_fx_origin_pulse", grid: [5, 3], frames: 5..8, hold: 0.08, at: [water_at[0] + 74, water_at[1] - 34], blend: :add, z: 960
      stop_fx :ripples
      burst :lift, at: [water_at[0], water_at[1] - 10], count: 24, color: :water
      emit :rain, rate: 70, id: :rain
      bgs :bgs_rain, volume: 60
      # close: the markings light up
      cut at: { actor: :water, part: :center, offset: [0, -14] }, zoom: 2.0
      impact_frames count: 2
      flash duration: 0.3, color: [200, 240, 255], power: 160
      fx_sheet ch + "pfw_kyogre_primal", grid: [4, 4], frames: [12, 15, 12, 15, 12], hold: 0.1, at: { actor: :water, part: :center },
               blend: :add, z: 1150 if legends
      rim :water, color: [176, 248, 255], side: :left
      cry water_cry
      shake power: 4, duration: 0.5
      fx_sheet an + "pfw_fx_origin_pulse", grid: [5, 3], frames: 0..3, hold: 0.07, loops: 4,
               at: { actor: :water, part: :mouth }, blend: :add, scale: 0.6, z: 1200
      pan by: [6, -4], duration: 2.8, ease: :out
      wait 0.4
      say who[:eirik], "Isenmar! The sea has come to the sand!", duration: 2.6

      #--- 3: Ashkaar answers from the Siege Camp's earthwork ---------------------
      cut at: [gate[0], gate[1] - 20], zoom: 2.0
      if legends
        actor :stone, prop: :stone, color: [240, 240, 255], at: [gate[0], gate[1] - 30], z: 1100
        move :stone, by: [0, -24], duration: 0.6, ease: :out
        hop :hrothgar, height: 4, duration: 0.4
        wait 0.7
        impact_frames count: 2
        flash duration: 0.7, power: 220
        se :beam_break
        fx_sheet an + "pfw_fx_explosions", grid: [4, 3], frames: 0..3, hold: 0.06, at: [gate[0], gate[1] - 60], blend: :add, z: 1200
        remove :stone
        emit :steam, area: [1260, 180, 500, 80], rate: 16, duration: 3.0, id: :hiss     # the rain hisses to steam over the camp
      else
        wait 0.4
      end
      if legends                                 # off screen, the sea-beast turns to face its enemy
        actor :water, sheet: ch + "pfw_kyogre_side", grid: [4, 2], frame: 0, at: [water_at[0], water_at[1] + 4], mouth: [80, -46]
        submerge :water, to: 14, duration: 0
        idle :water, frames: 0..3, hold: 0.16
        fx_sheet ch + "pfw_kyogre_rise", grid: [4, 4], frames: [12, 13, 14, 15], hold: 0.12, loops: :forever,
                 at: [water_at[0], water_at[1] - 44], z: 500 + water_at[1] + 6, id: :wake_ripples
      end
      cut at: [fire_at[0] - 40, 300], zoom: 1.0
      actor :fire, charset: fire_cs, at: [fire_at[0] + 30, fire_at[1] - 330], dir: :left, walk: true,
            mouth: (legends) ? [-46, -64] : nil
      shadow :fire, size: 34, ground: 40
      move :fire, to: fire_at, duration: 1.5, ease: :out
      fx_sheet an + "pfw_fx_fusion_flare", grid: [5, 5], frames: 1..8, hold: 0.07, loops: 2,
               at: { actor: :fire, part: :center }, blend: :add, z: 1150
      emit :embers, from: { actor: :fire, part: :center }, rate: 60, duration: 1.8, id: :wake
      wait 1.5
      shake power: 5, duration: 0.4
      burst :debris, at: [fire_at[0], ground], count: 12
      cut at: { actor: :fire, part: :center, offset: [0, -10] }, zoom: 2.0
      impact_frames count: 2
      flash duration: 0.3, color: [255, 224, 176], power: 160
      rim :fire, color: [255, 200, 56], side: :right
      cry fire_cry
      pan by: [-6, -4], duration: 2.8, ease: :out
      wait 0.4
      say who[:hrothgar], "Then let it remember fire.", duration: 2.4

      #--- 4: anticipation - the flood rises behind Kyogre, the sand glows under Reshiram
      bgm_fade 0.6
      bgs_fade 0.8
      stop_emit :rain
      tone to: [-80, -84, -60, 70], duration: 0.6
      cut at: { actor: :water, part: :mouth, offset: [-10, 0] }, zoom: (legends) ? 1.5 : 2.0
      idle :water, frames: 4..7, hold: 0.12 if legends          # markings lit
      fx_sheet an + "pfw_fx_origin_pulse", grid: [5, 3], frames: 0..3, hold: 0.06, loops: 6,
               at: { actor: :water, part: :mouth }, blend: :add, scale: 0.8, z: 1200
      if legends
        fx_sheet an + "pfw_fx_glass_wave", grid: [6, 1], frames: [0, 1, 2, 1], hold: 0.3, loops: 2,
                 at: [water_at[0] - 96, water_at[1] - 14], scale: 1.4, z: 500 + water_at[1] - 30
      end
      pan by: [8, 0], duration: 1.3, ease: :linear
      wait 1.3
      cut at: { actor: :fire, part: :mouth, offset: [-16, 10] }, zoom: 2.0
      fx_sheet an + "pfw_fx_fusion_flare", grid: [5, 5], frames: [11, 12, 11, 2], hold: 0.08, loops: 4,
               at: { actor: :fire, part: :mouth }, blend: :add, scale: 0.7, z: 1200
      fx_sheet an + "pfw_fx_glass_patch", grid: [4, 1], frames: [0, 1, 0, 1], hold: 0.16, loops: 2,
               at: [fire_at[0] - 6, ground + 18], scale: 1.6, squash: 0.8, blend: :add, z: 470
      pan by: [-8, 0], duration: 1.3, ease: :linear
      wait 1.3
      cut at: two_shot, zoom: 1.0                    # one held breath, wide
      wait 0.8

      #--- 5-11: the clash runs under seven shots -------------------------------
      s5, s6, s7, s8, s9, s10, s11 = 1.0, 3.4, 4.6, 2.8, 4.6, 3.2, 3.4
      total = s5 + s6 + s7 + s8 + s9 + s10 + s11
      impact_frames count: 2
      tone to: [-56, -60, -40, 56], duration: 0.2
      bgm :bgm_war_clash
      shake power: 6, duration: 0.5
      beam_clash style: :sheet, id: :clash, duration: total, launch: s5, resolve: s11, winner: clash_end,
                 a: { from: :water, color: :seaclash, width: 20, sheet: ch + "pfw_beam_sea",
                      flare: { sheet: an + "pfw_fx_origin_pulse", grid: [5, 3], frames: 0..3, scale: 0.55 } },
                 b: { from: :fire, color: :fireclash, width: 20, sheet: ch + "pfw_beam_fire",
                      flare: { sheet: an + "pfw_fx_fusion_flare", grid: [5, 5], frames: [11, 11, 12], scale: 0.45 } },
                 core: [{ sheet: an + "pfw_fx_steam", grid: [5, 4], frames: [9], scale: 0.8, spin: 50, blend: :normal },
                        { sheet: an + "pfw_fx_clash_core", grid: [4, 1], frames: 0..3, scale: 0.46, blend: :normal }],
                 spray: { every: 0.28, chunks: { sheet: an + "pfw_fx_ice_chunks", grid: [4, 1], frames: 1..3, scale: 0.2 },
                          steam: { sheet: an + "pfw_fx_steam", grid: [5, 4], frames: 5..8, hold: 0.09, scale: 0.5 } },
                 burst: { sheet: an + "pfw_fx_explosions", grid: [4, 3], frames: 0..3, hold: 0.06, blend: :normal },
                 steam: { sheet: an + "pfw_fx_steam", grid: [5, 4], frames: 5..8, hold: 0.1, blend: :normal },
                 curve: [[0, 0.5], [0.06, 0.37], [0.12, 0.63], [0.18, 0.41], [0.25, 0.57], [0.5, 0.45], [0.63, 0.56], [0.76, 0.46], [1, 0.5]],
                 ball: 14, shake: 3, ground: ground, wait: false
      # 5: Blue Flare glasses the wet sand under it, patch by patch, as the beam runs out
      7.times do |i|
        at(now + 0.1 + (i * 0.12)) do
          fx_sheet an + "pfw_fx_glass_patch", grid: [4, 1], frames: 0..3, holds: [0.14, 0.24, 0.7, 0.1], stay: :forever,
                   at: [1030 - (i * 26), 430 + ((i.odd?) ? 4 : -2)], scale: 1.1 - (i * 0.03), z: 470
        end
      end
      wait s5
      # 6: impact - white frame, a slow-motion beat, push in on the meeting point; flashes ramp; the sand glasses in a ring
      impact_frames count: 2
      slowmo 0.2, duration: 0.3
      fx_sheet an + "pfw_fx_glass_ring", grid: [4, 1], frames: 0..3, hold: 0.32, stay: :forever, at: [clash_c[0], ground - 2],
               scale: 0.8, z: 468, id: :glass_ring
      pan to: clash_c, zoom: 2.0, duration: 0.9, ease: :out
      clash_mod :clash, shake: 6
      [[0.6, 20], [1.2, 50], [1.8, 130], [2.4, 220]].each do |t, p|
        at(now + t) { flash duration: 0.12, power: p }
      end
      2.times do |i|
        at(now + 1.1 + (i * 0.9)) do
          burst :ice_shards, at: [clash_c[0] - 60 + (i * 120), ground], count: 14, speed: 1.3, color: :white
          burst :lift, at: [clash_c[0], ground], count: 8, color: :steam
        end
      end
      wait s6
      # 7: the dune surface - a breaking wave sets into glass mid-curl; the ranks go down; the player
      clash_mod :clash, shake: 3, intensity: 0.8, duration: 0.3
      cut at: [660, 470], zoom: 2.0
      if legends
        actor :wave, sheet: an + "pfw_fx_glass_wave", grid: [6, 1], frame: 0, at: [650, 520]
        flipbook :wave, frames: 0..5, holds: [0.14, 0.14, 0.16, 0.18, 0.2, 0.3]
      else
        fx_sheet an + "pfw_fx_glass_patch", grid: [4, 1], frames: 0..3, hold: 0.2, stay: :forever, at: [660, 500], scale: 2, z: 470
      end
      se :crowd_gasp
      emit :steam, area: [clash_c[0] - 120, ground - 20, 240, 30], rate: 16, size: 2, id: :steamline
      wait 1.2
      cut at: [380, 410], zoom: 2.0
      army_fall :isenmar, fraction: 0.4, duration: 0.8
      tremble :eirik, duration: 1.6
      face :eirik, :left
      say who[:soldier], "The Steamline! It's coming this way!", duration: 2.4
      actor :pc, player: true, at: [800, 560], dir: :up
      actor :starter, charset: var(:starter_charset, "Followers/EEVEE"), color: [176, 136, 96], at: [776, 568], dir: :up
      cut at: [790, 520], zoom: 2.0
      tremble :starter, duration: 1.0
      rim :pc, color: [255, 255, 255], side: :right
      pan by: [0, -6], duration: 1.0, ease: :linear
      wait s7 - 3.6
      # 8: the dome of Bleed light; on its crest the bone-carters' banner glasses where it stands
      cut at: two_shot, zoom: 1.0
      army_fall :ashkaar, fraction: 0.4, duration: 0.8
      army_fall :fire_mons, fraction: 0.5, duration: 0.8
      fx_sheet an + "pfw_fx_dome", grid: [4, 1], frames: 0..3, hold: 0.14, loops: :forever, origin: [240, 236],
               at: [clash_c[0], ground + 34], scale: 0.92, grow: [0.12, 1.0, 0.7], opacity: 225, z: 1240, id: :dome
      tint :carter_banner, color: [206, 240, 252], amount: 170, duration: 1.6
      army_tint :isenmar, color: :bleed, amount: 110, duration: s8
      army_tint :ashkaar, color: :bleed, amount: 110, duration: s8
      stop_emit :embers
      stop_emit :sand
      wait s8
      # 9: the PC goes in
      case variant
      when :B
        remove :starter
        actor :mount, charset: "pfw_salamence", at: [1300, 300], dir: :left, walk: true, z: 870
        shadow :mount, size: 26, ground: 30
        cut at: [1100, 420], zoom: 1.0
        pan to: [900, 440], duration: s9 - 0.3
        move :mount, to: [930, 470], duration: s9 - 0.4, ease: :out
        move :pc, to: [930, 440], duration: 0
        fade :pc, to: 0, duration: 0
        wait 0.8
        say who[:sigrun], "Hold on!", duration: 2.0
        wait s9 - 2.8
      when :C
        remove :starter
        # Marisol's sled-boat riding the flood in, the PC on its prow
        actor :mount, sheet: ch + "pfw_sled", grid: [1, 1], px: 2, at: [440, 500], z: 960
        move :pc, to: [470, 470], duration: 0
        face :pc, :right
        cut at: [560, 460], zoom: 1.0
        pan to: [760, 440], duration: s9 - 0.3
        move :mount, to: [790, 480], duration: s9 - 0.4, ease: :out
        move :pc, to: [820, 450], duration: s9 - 0.4, ease: :out
        emit :steam, from: { actor: :mount, part: :center }, rate: 20, duration: s9 - 0.4, id: :wake2
        wait 0.8
        say who[:marisol], "Tides take it, kid, now!", duration: 2.4
        wait s9 - 3.2
      else
        cut at: [820, 440], zoom: 1.0
        follow :pc, smooth: 0.08, offset: [0, -80]
        move :pc, to: [870, 430], duration: s9 - 0.4, walk: true, ease: :linear
        move :starter, to: [846, 440], duration: s9 - 0.4, walk: true, ease: :linear
        tint :pc, color: [255, 255, 255], amount: 70, duration: 2.5
        wait s9
      end
      # 10: the hand goes up; the beams go white
      hero = (variant == :B) ? :mount : :pc
      cut at: { actor: hero, part: :top, offset: [0, -40] }, zoom: 2.0
      hop hero, height: 4, duration: 0.3
      tint hero, color: [255, 255, 255], amount: 150, duration: 1.0
      emit :motes, from: { actor: hero, part: :top }, rate: 30, color: :white, angle: -90, spread: 20, speed: 4, id: :shard
      fx_sheet an + "pfw_fx_steam", grid: [5, 4], frames: 15..19, hold: 0.12, loops: 2, at: { actor: hero, part: :center }, scale: 2, z: 1400
      clash_mod :clash, white: (overpower) ? 0.0 : 1.0, intensity: (overpower) ? 1.0 : 0.4,
                        shake: (overpower) ? 5 : 2, strobe: overpower, duration: 2.4
      wait s10
      # 11: silence (A/B/C), the white-out (A2) or the overpower; the rain turns to snow and falls on glass
      cut at: clash_c, zoom: 1.0
      stop_emit :shard
      bgm_fade 0.4
      if variant == :A2
        wait s11 * 0.5
        impact_frames count: 2
        stop_fx :dome
        fx_sheet an + "pfw_fx_dome", grid: [4, 1], frames: 0..3, hold: 0.1, loops: 3, origin: [240, 236],
                 at: [clash_c[0], ground + 34], scale: 0.92, grow: [1.0, 2.4, 0.6], opacity: 225, z: 1240, id: :dome
        fade :water, to: 0, duration: 1.2
        fade :fire, to: 0, duration: 1.2
        wait (s11 * 0.5) - 0.14
        flash duration: 2.4, hold: 0.6
        stop_fx :dome
        stop_emit :steamline
        [:isenmar, :ashkaar, :ice_mons, :fire_mons, :riders].each { |a| rout a, by: [0, 0], duration: 0.1 }
        4.times { |i| stop_fx :"camp#{i}" }
        3.times { |i| remove :"ban_i#{i}"; remove :"ban_a#{i}" }
        stop_fx :wake_ripples if legends
        remove :flood if legends
        remove :pc
        remove :starter
        camera at: two_shot, zoom: 1.0
        tone to: [16, 12, 24, 110], duration: 0
        emit :snow, rate: 26
        wait 1.8
      else
        emit :snow, rate: 30
        wait s11
        tone to: [-10, -16, 0, 50], duration: 1.5

        #--- 12: the two legends look down, and leave; the flood goes out with Kyogre
        cut at: two_shot, zoom: 1.0
        stop_fx :dome
        fx_sheet an + "pfw_fx_dome", grid: [4, 1], frames: 0..3, hold: 0.14, loops: 4, origin: [240, 236], fade: 1.0,
                 at: [clash_c[0], ground + 34], scale: 0.92, grow: [1.0, 0.45, 2.0], opacity: 225, z: 1240
        hop :water, height: 3, duration: 0.5
        wait 1.0
        if legends
          stop_fx :wake_ripples
          fx_sheet an + "pfw_fx_origin_pulse", grid: [5, 3], frames: 5..8, hold: 0.08, at: [water_at[0], water_at[1] - 30], z: 1100
          actor :water_sink, sheet: ch + "pfw_kyogre_rise", grid: [4, 4], frame: 5, at: water_at
          fade :water, to: 0, duration: 0
          flipbook :water_sink, frames: [5, 6, 7, 8, 9, 10, 11], hold: 0.24
          at(now + 1.0) { flipbook :flood, frames: [5, 4, 3, 2, 1, 0], hold: 0.34 }
          at(now + 3.1) { fade :flood, to: 0, duration: 0.4 }
        else
          submerge :water, to: 64, duration: 2.0, ease: :in
        end
        face :fire, :up
        move :fire, to: [fire_at[0] + 60, -200], duration: 2.4, ease: :in
        text "It looked at me as if I were very small and very familiar. Again.", position: :top, duration: 3.6
      end
      bgm :bgm_war_after

      #--- 13: what is left ------------------------------------------------------
      case variant
      when :A
        cut at: [872, 400], zoom: 2.0
        actor :sigrun, charset: :LEADER_SIGRUN, color: [216, 88, 56], at: [960, 240], dir: :left
        actor :anja, charset: :LEADER_ANJA, color: [112, 168, 224], at: [720, 432], dir: :right
        move :sigrun, to: [912, 430], duration: 0.6, ease: :in
        move :anja, to: [834, 432], duration: 1.6, walk: true
        wait 0.6
        burst :smoke, at: [912, 430], count: 8
        shake power: 3, duration: 0.2
        wait 1.1
        face :sigrun, :left
        face :anja, :right
        say who[:sigrun], "Father. Enough."
        say who[:anja], "Eirik. Enough."
        say "#{who[:sigrun]} & #{who[:anja]}", "The Boon will settle it.", duration: 2.6
      when :A2
        actor :eirik2, charset: "pfw_eirik", at: [560, 470], dir: :right
        actor :hrothgar2, charset: "pfw_hrothgar", at: [1180, 470], dir: :left
        move :eirik2, to: [800, 470], duration: 3.0, walk: true, ease: :linear
        move :hrothgar2, to: [944, 470], duration: 3.0, walk: true, ease: :linear
        wait 3.2
        text "Both lines were gone. Two rulers stood alone on the glass.", duration: 3.6
      else
        # B: Isenmar breaks back behind Skaldfast's walls and Ashkaar's banners go up over them.
        # C: Ashkaar breaks back over the Siege Camp's earthwork and Isenmar's banners go up over the camp.
        winner_army, loser_army = (variant == :B) ? [:ashkaar, :isenmar] : [:isenmar, :ashkaar]
        cut at: two_shot, zoom: 1.0
        rout loser_army, duration: 2.6
        loser_mons = (variant == :B) ? :ice_mons : :fire_mons
        rout loser_mons, duration: 2.6
        emit :smoke, area: [(variant == :B) ? 40 : 1260, 280, 460, 60], rate: 18, id: :rout_smoke
        march winner_army, by: [(variant == :B) ? -120 : 120, 0], duration: 2.6
        pan to: [(variant == :B) ? 300 : 1480, 280], duration: 2.6
        wait 2.6
        sheet_name = (variant == :B) ? "pfw_banner_ashkaar" : "pfw_banner_isenmar"
        spots = (variant == :B) ? [[110, 300], [256, 290], [420, 300]] : [[1330, 318], [1505, 312], [1680, 318]]
        spots.each_with_index do |pt, i|
          actor :"win#{i}", sheet: ch + sheet_name, grid: [1, 1], at: [pt[0], pt[1] + 20], opacity: 0, z: 980
          fade :"win#{i}", to: 255, duration: 0.5
          move :"win#{i}", by: [0, -20], duration: 0.6, ease: :out
        end
        wait 0.8
        say (variant == :B) ? who[:hrothgar] : who[:eirik], "It's done."
        say (variant == :B) ? who[:anja] : who[:sigrun], "I'll remember which side you stood on.", duration: 3.2
      end

      #--- 14: the observers on the sandstone mesa behind the lines ---------------
      fade_out duration: 0.5, steps: 5
      stop_emit
      camera at: [mesa[0] + 10, mesa[1] - 30], zoom: 2.0
      tone to: [-6, -12, -6, 30], duration: 0
      actor :tripod, prop: :tripod, color: [208, 168, 72], at: [mesa[0] - 24, mesa[1] - 2]
      actor :quent, charset: :MERIDIAN_QUENT, color: [240, 240, 244], at: [mesa[0] + 12, mesa[1]], dir: :down
      actor :obs1, charset: :MERIDIAN_AGENT, color: [224, 224, 232], at: [mesa[0] - 56, mesa[1] - 4], dir: :right
      actor :obs2, charset: :MERIDIAN_AGENT, color: [224, 224, 232], at: [mesa[0] + 48, mesa[1] - 2], dir: :left
      emit :snow, rate: 10
      fade_in duration: 0.5, steps: 5
      fade :tripod, to: 0, duration: 1.6, steps: 4
      hop :quent, height: 3, times: 3, duration: 1.5
      burst :motes, at: [mesa[0] - 24, mesa[1] - 30], count: 10, color: :electric
      pan by: [6, 0], duration: 3.4, ease: :linear
      say who[:quent], "Lovely reading. Simply lovely.", duration: 3.2

      #--- 15: the Glass Dunes at sunrise; the bone-carters raise a new banner ----
      fade_out duration: 0.6, steps: 5
      stop_emit
      remove :quent
      remove :obs1
      remove :obs2
      remove :carter_banner
      camera at: [400, 330], zoom: 1.0
      army_tint :isenmar, color: [232, 240, 255], amount: 235, duration: 0
      army_tint :ashkaar, color: [232, 240, 255], amount: 235, duration: 0
      tone to: [36, 14, -10, 40], duration: 0
      actor :carter1, charset: "pfw_bone_carter", at: [1250, 300], dir: :left
      actor :carter2, charset: "pfw_bone_carter", at: [1290, 306], dir: :left
      actor :new_banner, sheet: ch + "pfw_banner_carters", grid: [1, 1], at: [crest[0] + 20, crest[1] + 40], opacity: 0, z: 760
      emit :motes, area: [200, 260, 1200, 260], rate: 14, color: :bleed
      fade_in duration: 0.9, steps: 5
      pan by: [900, 0], duration: 5.2, ease: :linear
      at(now + 1.2) do
        move :carter1, to: [crest[0] + 2, crest[1] + 22], duration: 2.4, walk: true, ease: :linear
        move :carter2, to: [crest[0] + 50, crest[1] + 26], duration: 2.4, walk: true, ease: :linear
      end
      at(now + 3.7) do
        fade :new_banner, to: 255, duration: 0.3
        move :new_banner, by: [0, -18], duration: 0.6, ease: :out
      end
      say who[:larch], "That wasn't a battle to them. That was a reading.", duration: 4.2
      fade_out duration: 1.2, steps: 6
    end

    define(:WAR_CLIMAX, vars: proc { Cutscene.war_vars }, &WAR_CLIMAX_BLOCK)
    [:A2, :B, :C].each { |v| build(:WAR_CLIMAX, variant: v) }              # author-time check of every variant
    build(:WAR_CLIMAX, legends: false)
    build(:WAR_CLIMAX, variant: :C, overpower: true)
    define(:WAR_CLIMAX_DEMO) { include_scene(:WAR_CLIMAX, variant: var(:variant, :A2)) }
  end
end
