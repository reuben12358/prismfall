#===============================================================================
# Prismfall Cutscenes - 013 The war climax (story/13_CUTSCENES.md, WAR-1)
#-------------------------------------------------------------------------------
# :WAR_CLIMAX  "The Beam Clash on the Shattered Ice" - 15 shots, about 75 s.
# Isenmar and Kyogre hold the left of the strait, Ashkaar and Reshiram the right.
#
# Variables (Prismfall::Cutscene.play(:WAR_CLIMAX, variant: :B) overrides them;
# otherwise they are read from Prismfall Core's war outcome flags):
#   variant: :A  = WAR_STOPPED       the PC walks in, the clash falls silent
#            :A2 = WAR_BOTH_BROKEN   as A to shot 10, then a white-out; both lines gone
#            :B  = WAR_ASHKAAR_WON   the PC rides in on Sigrun's Salamence
#            :C  = WAR_ISENMAR_WON   the PC rides in on Marisol's prow
#   legends: false = :war_legend kept the legendaries away; the Wardens' aces
#            fight instead (fire_mon: / water_mon:, default Salamence / Mamoswine)
#   fire_legend: / water_legend: placeholder species the story team can swap.
#   overpower: true (B/C only, not in the storyboard) = instead of falling silent,
#            the winning kingdom's beam swallows the other and washes the screen white.
# :WAR_CLIMAX_DEMO is the same scene with fixed variables (variant :A2), for
# testing without a save file.
#===============================================================================
module Prismfall
  module Cutscene
    WAR_SPEAKERS = {
      :eirik => "Thane Eirik", :hrothgar => "Dominar Hrothgar", :sigrun => "Sigrun", :anja => "Anja",
      :marisol => "Marisol", :quent => "Dr. Quent", :larch => "Larch (radio)", :soldier => "Soldier"
    }

    # Variables from Core's narrative state (all guarded; defaults = variant A).
    def self.war_vars
      vars = {}
      return vars if !defined?(Prismfall::Narrative) || !Prismfall::Narrative.respond_to?(:flag)
      begin
        if Prismfall::Narrative.flag(:WAR_BOTH_BROKEN)    then vars[:variant] = :A2
        elsif Prismfall::Narrative.flag(:WAR_ASHKAAR_WON) then vars[:variant] = :B
        elsif Prismfall::Narrative.flag(:WAR_ISENMAR_WON) then vars[:variant] = :C
        elsif Prismfall::Narrative.flag(:WAR_STOPPED)     then vars[:variant] = :A
        end
        if defined?(Prismfall::Conditions) && Prismfall::Conditions.evaluate("choice(:war_legend) == :neither")
          vars[:legends] = false
        end
      rescue StandardError => e
        Util.log("war_vars: #{e.message} (using defaults)")
      end
      return vars
    end

    WAR_CLIMAX_BLOCK = proc do
      variant = var(:variant, :A)
      legends = var(:legends, true)
      water   = (legends) ? var(:water_legend, :KYOGRE)   : var(:water_mon, :MAMOSWINE)
      fire    = (legends) ? var(:fire_legend, :RESHIRAM)  : var(:fire_mon, :SALAMENCE)
      # Optional overworld-scale acting sheets (see design/CUTSCENE_RESEARCH.md): used when the file exists.
      water_sheet = var(:water_sheet, "Graphics/Characters/pkmn_#{water.to_s.downcase}_war")
      fire_sheet  = var(:fire_sheet, "Graphics/Characters/pkmn_#{fire.to_s.downcase}_war")
      water_src = (Gfx.resolve(water_sheet)) ? { sheet: water_sheet, grid: [4, 4], frame: 0, px: 2 } : { species: water }
      fire_src  = (Gfx.resolve(fire_sheet)) ? { sheet: fire_sheet, grid: [4, 4], frame: 0, px: 2 } : { species: fire }
      water_pal = :seaclash
      fire_pal  = :fireclash
      who = WAR_SPEAKERS
      wide = [232, 192]                 # the wide two-shot
      ground = 318                      # the ice between the two hosts
      water_at = [40, 300]
      fire_at  = [404, 300]
      overpower = var(:overpower, false) && [:B, :C].include?(variant)
      clash_end = :fizzle
      clash_end = :both if variant == :A2
      clash_end = ((variant == :B) ? :b : :a) if overpower

      # The Shattered Ice before dawn: aurora over Isenmar (left), smoke over
      # Ashkaar (right), two mountain ranges, both fortresses, pack ice, and
      # the two hosts as ranks of tiny figures in front of everything behind y 312.
      stage = lambda do |ice, hosts|
        background :sky, palette: :dawn, stars: true, clouds: 5, height: 392,
                   colors: [[12, 10, 40], [24, 18, 66], [52, 30, 98], [98, 46, 110], [164, 72, 106], [226, 122, 96], [250, 190, 126]]
        background :aurora, x: -300, y: 2, width: 600, height: 160
        background :smoke_bank, x: 330, y: 216, width: 640, height: 200
        background :mountains, color: [52, 44, 104], y: 200, height: 56, snow: true, parallax: 0.15, seed: 3
        background :mountains, color: [30, 26, 70], y: 206, height: 34, parallax: 0.3, seed: 8
        background :fortress, x: -190, y: 210, width: 300, height: 96, color: [22, 26, 60], glow: [150, 224, 255]
        background :fortress, x: 400, y: 210, width: 320, height: 110, color: [36, 16, 30], glow: [255, 168, 64], seed: 4
        background :fleet, x: -400, y: 226, width: 300, count: 5, color: [26, 34, 72]
        background :floes, x: -512, width: 1536, palette: ice, pools: (hosts) ? [[water_at[0], 302, 124, 20]] : nil
        next if !hosts
        background :host, x: -400, width: 510, y: 330, rows: 6, color: [80, 128, 208], banner: [208, 240, 255],
                   facing: :right, frost: 7, haze: [60, 70, 130], front: true
        background :host, x: 330, width: 560, y: 330, rows: 6, color: [204, 64, 40], banner: [255, 184, 56],
                   facing: :left, fires: 7, haze: [110, 60, 90], front: true, seed: 77
      end

      #--- the stage -----------------------------------------------------------
      stage.call(:dawn, true)
      letterbox true, duration: 0
      camera at: [-170, 192]
      bgm :bgm_war_field
      bgs :bgs_war, volume: 70
      army :isenmar, charset: :ISENMAR_SOLDIER, color: [80, 128, 208], count: 6, rows: 1, area: [-260, 344, 330, 6], facing: :right
      army :ashkaar, charset: :ASHKAAR_SOLDIER, color: [204, 64, 40], count: 6, rows: 1, area: [370, 344, 360, 6], facing: :left
      army :riders, icons: [:SALAMENCE, :CHARIZARD], count: 8, rows: 2, area: [520, 70, 260, 44], facing: :left, scale: 0.5
      actor :eirik, charset: :ISENMAR_OFFICER, color: [96, 160, 224], at: [-96, 340], dir: :right
      actor :hrothgar, charset: :ASHKAAR_OFFICER, color: [224, 96, 56], at: [520, 340], dir: :left
      glow side: :left, color: [72, 200, 232], level: 0.5, duration: 0
      glow side: :right, color: [240, 112, 40], level: 0.5, duration: 0
      emit :snow, area: [-420, -20, 560, 20], rate: 30, id: :snow_left
      emit :embers, area: [340, 260, 480, 70], rate: 26, id: :embers_right
      emit :smoke, area: [380, 300, 420, 20], rate: 6, layer: :back, id: :camp_smoke

      #--- 1: establishing pan across both hosts --------------------------------
      pan to: [640, 192], duration: 5.4, ease: :in_out
      wait 5.6

      #--- 2: the water bulges; a shape rises behind Isenmar's ranks -------------
      cut at: [70, 226], zoom: 1.0
      actor :water, **water_src, at: [water_at[0], water_at[1] + 240], flip: water_src[:species] ? true : false, silhouette: [8, 14, 44],
            submerge: (legends) ? 26 : 0, mouth: (legends) ? [-56, -48] : nil
      se :rumble
      shake power: 4, duration: 2.0, decay: false
      emit :steam, area: [-40, 296, 170, 12], rate: 34, duration: 2.2, id: :bulge
      ring at: [water_at[0], 302], color: :seaclash, radius: 150, duration: 1.4, squash: 0.2
      wait 0.6
      move :water, to: water_at, duration: 1.5, ease: :out
      flipbook :water, frames: 0..3, hold: 0.1 if water_src[:sheet]
      wait 0.9
      burst :ice_shards, at: [water_at[0], 300], count: 30, speed: 1.3
      burst :lift, at: [water_at[0], 300], count: 12
      ring at: [water_at[0], 302], color: :seaclash, radius: 220, duration: 0.9, squash: 0.2
      emit :rain, rate: 80, id: :rain
      bgs :bgs_rain, volume: 60
      tone to: [-28, -14, 24, 0], duration: 1.0
      glow side: :left, level: 0.8, duration: 1.0
      wait 0.9
      # low-angle close shot: the markings light up
      cut at: { actor: :water, part: :center, offset: [20, -6] }, zoom: 2.0
      impact_frames count: 2
      flash duration: 0.35, color: [200, 240, 255]
      tint :water, color: [8, 14, 44], amount: 0, duration: 0.5
      rim :water, color: [176, 248, 255], side: :right
      cry water
      shake power: 5, duration: 0.6
      pan by: [10, -8], duration: 2.8, ease: :out
      wait 0.5
      say who[:eirik], "Isenmar! The sea remembers it's a sea!", duration: 2.6

      #--- 3: Ashkaar answers ----------------------------------------------------
      cut at: [520, 300], zoom: 2.0
      if legends
        actor :stone, prop: :stone, color: [240, 240, 255], at: [520, 296], scale: 1, z: 900
        move :stone, by: [0, -30], duration: 0.7, ease: :out
        hop :hrothgar, height: 5, duration: 0.4
        wait 0.8
        impact_frames count: 2
        flash duration: 0.8
        se :beam_break
        burst :sparks, at: [520, 262], count: 34, color: :white
        remove :stone
      else
        wait 0.4
      end
      cut at: [430, 200], zoom: 1.0
      actor :fire, **fire_src, at: [fire_at[0] + 40, fire_at[1] - 300], silhouette: [255, 255, 255],
            mouth: (legends) ? [-30, -192] : nil
      move :fire, to: fire_at, duration: 1.3, ease: :out
      emit :embers, from: { actor: :fire, part: :center }, rate: 60, duration: 1.6, id: :wake
      wait 1.3
      shake power: 6, duration: 0.5
      burst :debris, at: [fire_at[0], 318], count: 14
      ring at: [fire_at[0], 318], color: :fireclash, radius: 200, duration: 0.8, squash: 0.2
      cut at: { actor: :fire, part: :top, offset: [-20, 50] }, zoom: 2.0
      impact_frames count: 2
      flash duration: 0.35, color: [255, 224, 176]
      tint :fire, color: [255, 255, 255], amount: 0, duration: 0.5
      rim :fire, color: [255, 200, 56], side: :left
      cry fire
      glow side: :right, level: 0.8, duration: 1.0
      tone to: [8, -8, 0, 0], duration: 0.8
      pan by: [-10, -8], duration: 2.8, ease: :out
      wait 0.5
      say who[:hrothgar], "Then let it remember fire.", duration: 2.4

      #--- 4: anticipation - the world dims, both draw breath --------------------
      bgm_fade 0.6
      bgs_fade 0.8
      stop_emit :rain
      tone to: [-72, -72, -52, 40], duration: 0.6
      glow side: :left, level: 0.2, duration: 0.6
      glow side: :right, level: 0.2, duration: 0.6
      flipbook :water, frames: 4..7, holds: [0.3, 0.1, 0.1, 2.0] if water_src[:sheet]
      flipbook :fire, frames: 4..7, holds: [0.3, 0.1, 0.1, 2.0] if fire_src[:sheet]
      charge_up at: :water, color: water_pal, duration: 3.5, size: 15, wait: false
      charge_up at: :fire, color: fire_pal, duration: 3.5, size: 15, wait: false
      tremble :water, duration: 3.5
      tremble :fire, duration: 3.5
      cut at: { actor: :water, part: :mouth, offset: [-10, 0] }, zoom: 2.0
      pan by: [8, 0], duration: 1.3, ease: :linear
      wait 1.3
      cut at: { actor: :fire, part: :mouth, offset: [10, 20] }, zoom: 2.0
      pan by: [-8, 0], duration: 1.3, ease: :linear
      wait 1.3
      cut at: wide, zoom: 1.0                      # one held breath, wide
      wait 0.9

      #--- 5-11: the clash runs under seven shots -------------------------------
      s5, s6, s7, s8, s9, s10, s11 = 1.0, 3.4, 4.6, 2.8, 4.6, 3.2, 3.4
      total = s5 + s6 + s7 + s8 + s9 + s10 + s11
      impact_frames count: 2
      tone to: [0, 0, 0, 0], duration: 0.2
      bgm :bgm_war_clash
      glow side: :left, level: 0.7, duration: 0.3
      glow side: :right, level: 0.7, duration: 0.3
      shake power: 6, duration: 0.5
      beam_clash a: { from: :water, color: water_pal, width: 30 }, b: { from: :fire, color: fire_pal, width: 30 },
                 id: :clash, duration: total, launch: s5, resolve: s11, winner: clash_end,
                 curve: [[0, 0.5], [0.07, 0.38], [0.14, 0.62], [0.22, 0.5], [0.5, 0.46], [0.75, 0.54], [1, 0.5]],
                 ball: 24, shake: 3, ground: ground, wait: false
      wait s5
      # 6: impact - a white frame, a slow-motion beat, then the push in
      impact_frames count: 2
      slowmo 0.2, duration: 0.3
      fracture at: [236, ground], radius: 250, duration: 1.6, arms: 11
      pan to: [236, 196], zoom: 1.5, duration: 0.9, ease: :out
      clash_mod :clash, shake: 6
      2.times do |i|
        at(now + 1.1 + (i * 0.9)) do
          burst :ice_shards, at: [176 + (i * 120), ground], count: 14, speed: 1.3
          burst :lift, at: [236, ground], count: 8
        end
      end
      wait s6
      # 7: reaction cuts - the ranks, then the player
      clash_mod :clash, shake: 3, intensity: 0.8, duration: 0.3
      cut at: [-110, 318], zoom: 2.0
      glow side: :right, color: [255, 255, 255], level: 0.6, duration: 0.2
      army_fall :isenmar, fraction: 0.45, duration: 0.8
      tremble :eirik, duration: 1.6
      face :eirik, :left
      se :crowd_gasp
      emit :steam, area: [140, 300, 200, 30], rate: 16, size: 2, id: :steamline
      say who[:soldier], "The Steamline! It's coming this way!", duration: 2.4
      actor :pc, player: true, at: [150, 340], dir: :right
      actor :starter, charset: var(:starter_charset, "Followers/EEVEE"), color: [176, 136, 96], at: [128, 342], dir: :right
      cut at: [156, 318], zoom: 2.0
      glow side: :left, color: [72, 200, 232], level: 0.3, duration: 0.2
      tremble :starter, duration: 1.0
      rim :pc, color: [255, 255, 255], side: :right
      pan by: [6, 0], duration: 2.0, ease: :linear
      wait s7 - 2.4
      # 8: the dome of Bleed light
      cut at: wide, zoom: 1.0
      glow side: :right, color: [240, 112, 40], level: 0.6, duration: 0.3
      glow side: :left, level: 0.6, duration: 0.3
      army_fall :ashkaar, fraction: 0.45, duration: 0.8
      dome at: [236, ground - 10], radius: 240, duration: s8 - 0.4, squash: 0.5
      army_tint :isenmar, color: :bleed, amount: 110, duration: s8
      army_tint :ashkaar, color: :bleed, amount: 110, duration: s8
      stop_emit :embers_right
      wait s8
      # 9: the PC goes in
      case variant
      when :B
        remove :starter
        actor :mount, species: :SALAMENCE, at: [560, 240], scale: 0.5, z: 870
        actor :pc, player: true, at: [560, 204], dir: :left, z: 880
        cut at: [470, 230], zoom: 1.5
        pan to: [320, 250], duration: s9 - 0.3
        move :mount, to: [310, 320], duration: s9 - 0.4, ease: :out
        move :pc, to: [310, 284], duration: s9 - 0.4, ease: :out
        dome hole_at: :pc, hole: 54, duration: 2.0
        wait 0.8
        say who[:sigrun], "Hold on!", duration: 2.0
        wait s9 - 2.8
      when :C
        remove :starter
        actor :prow, prop: :ship, color: [72, 96, 144], at: [-40, 344], scale: 2, flip: true, z: 870
        actor :pc, player: true, at: [-20, 316], dir: :right, z: 880
        cut at: [40, 250], zoom: 1.5
        pan to: [170, 250], duration: s9 - 0.3
        move :prow, to: [160, 344], duration: s9 - 0.4, ease: :out
        move :pc, to: [180, 316], duration: s9 - 0.4, ease: :out
        dome hole_at: :pc, hole: 54, duration: 2.0
        wait 0.8
        say who[:marisol], "Tides take it, kid, now!", duration: 2.4
        wait s9 - 3.2
      else
        cut at: [160, 280], zoom: 1.5
        pan to: [216, 270], duration: s9 - 0.3, ease: :linear
        move :pc, to: [226, 336], duration: s9 - 0.4, walk: true, ease: :linear
        move :starter, to: [200, 338], duration: s9 - 0.4, walk: true, ease: :linear
        dome hole_at: :pc, hole: 54, duration: 2.5
        tint :pc, color: [255, 255, 255], amount: 70, duration: 2.5
        wait s9
      end
      # 10: the hand goes up; the beams go white
      cut at: { actor: :pc, part: :center, offset: [6, -36] }, zoom: 2.0
      hop :pc, height: 4, duration: 0.3
      tint :pc, color: [255, 255, 255], amount: 150, duration: 1.0
      emit :motes, from: { actor: :pc, part: :top }, rate: 30, color: :white, angle: -90, spread: 20, speed: 4, id: :shard
      ring at: { actor: :pc, part: :center }, color: :white, radius: 320, duration: 2.2, squash: 0.8, layer: :front
      clash_mod :clash, white: (overpower) ? 0.0 : 1.0, intensity: (overpower) ? 1.0 : 0.4, shake: (overpower) ? 5 : 2, strobe: overpower, duration: 2.4
      wait s10
      # 11: silence (A/B/C), the white-out (A2) or the overpower
      cut at: [236, 196], zoom: 1.25
      stop_emit :shard
      bgm_fade 0.4
      glow side: :left, level: 0.25, duration: 1.5
      glow side: :right, level: 0.25, duration: 1.5
      if variant == :A2
        wait s11 * 0.5
        impact_frames count: 2
        dome radius: 420, duration: 0.6
        fade :water, to: 0, duration: 1.2
        fade :fire, to: 0, duration: 1.2
        wait (s11 * 0.5) - 0.14
        flash duration: 2.4, hold: 0.6
        dome off: true
        stop_emit :steamline
        rout :isenmar, by: [0, 0], duration: 0.1
        rout :ashkaar, by: [0, 0], duration: 0.1
        rout :riders, by: [0, 0], duration: 0.1
        clear_actors
        clear_backgrounds
        stage.call(:glass, false)
        camera at: wide, zoom: 1.0
        tone to: [8, 8, 16, 60], duration: 0
        emit :snow, rate: 26
        wait 1.8
      else
        emit :snow, rate: 30
        wait s11
        tone to: [0, 0, 8, 20], duration: 1.5

        #--- 12: the two legends look down, and leave --------------------------
        cut at: wide, zoom: 1.0
        dome radius: 120, duration: 2.0
        hop :water, height: 4, duration: 0.5
        hop :fire, height: 4, duration: 0.5
        wait 1.2
        move :water, by: [0, 240], duration: 2.2, ease: :in
        fade :water, to: 0, duration: 2.2
        ring at: [water_at[0], 302], color: :seaclash, radius: 150, duration: 1.4, squash: 0.2
        flip :fire
        move :fire, to: [780, 10], duration: 2.2, ease: :in
        text "It looked at me as if I were very small and very familiar. Again.", position: :top, duration: 3.6
        dome off: true
      end
      bgm :bgm_war_after

      #--- 13: what is left ------------------------------------------------------
      case variant
      when :A
        cut at: [230, 300], zoom: 2.0
        actor :sigrun, charset: :LEADER_SIGRUN, color: [216, 88, 56], at: [296, 120], dir: :left
        actor :anja, charset: :LEADER_ANJA, color: [112, 168, 224], at: [110, 338], dir: :right
        move :sigrun, to: [278, 336], duration: 0.6, ease: :in
        move :anja, to: [178, 338], duration: 1.6, walk: true
        wait 0.6
        burst :smoke, at: [278, 336], count: 8
        shake power: 3, duration: 0.2
        wait 1.1
        face :sigrun, :right
        face :anja, :left
        say who[:sigrun], "Father. Enough."
        say who[:anja], "Eirik. Enough."
        say "#{who[:sigrun]} & #{who[:anja]}", "The Boon will settle it.", duration: 2.6
      when :A2
        actor :eirik2, charset: :ISENMAR_OFFICER, color: [96, 160, 224], at: [-20, 336], dir: :right
        actor :hrothgar2, charset: :ASHKAAR_OFFICER, color: [224, 96, 56], at: [500, 336], dir: :left
        move :eirik2, to: [170, 336], duration: 3.0, walk: true, ease: :linear
        move :hrothgar2, to: [300, 336], duration: 3.0, walk: true, ease: :linear
        wait 3.2
        text "Both lines were gone. Two rulers stood alone on the glass.", duration: 3.6
      else
        winner_army, loser_army = (variant == :B) ? [:ashkaar, :isenmar] : [:isenmar, :ashkaar]
        loser_x = (variant == :B) ? -330 : 620
        col = (variant == :B) ? [224, 72, 40] : [72, 136, 224]
        cut at: wide, zoom: 1.0
        rout loser_army, duration: 2.6
        emit :smoke, area: [(variant == :B) ? -120 : 380, 300, 240, 30], rate: 18, id: :rout_smoke
        march winner_army, by: [(variant == :B) ? -70 : 70, 0], duration: 2.6
        pan to: [(variant == :B) ? 60 : 420, 192], duration: 2.6
        wait 2.6
        3.times do |i|
          actor :"banner#{i}", prop: :banner, color: col, at: [loser_x + 40 + (i * 70), 300 - (i.odd? ? 16 : 0)], scale: 2, opacity: 0, z: 860
          fade :"banner#{i}", to: 255, duration: 0.5
          move :"banner#{i}", by: [0, -26], duration: 0.6, ease: :out
        end
        pan to: [(variant == :B) ? -170 : 650, 192], duration: 1.4
        wait 1.6
        say (variant == :B) ? who[:hrothgar] : who[:eirik], "It's done."
        say (variant == :B) ? who[:anja] : who[:sigrun], "I'll remember which side you stood on.", duration: 3.2
      end

      #--- 14: the observers on the ridge ---------------------------------------
      fade_out duration: 0.5
      stop_emit
      clear_actors
      clear_backgrounds
      glow side: :left, level: 0, duration: 0
      glow side: :right, level: 0, duration: 0
      background :sky, palette: :dawn, clouds: 4, sun: [150, 150]
      background :mountains, color: [72, 72, 120], y: 210, height: 70, snow: true
      background :battlefield, palette: :snow, horizon: 250
      camera at: [256, 230], zoom: 2.0
      tone to: [0, 0, 0, 0], duration: 0
      actor :tripod, prop: :tripod, color: [208, 168, 72], at: [226, 300], scale: 2
      actor :quent, charset: :MERIDIAN_QUENT, color: [240, 240, 244], at: [270, 304], dir: :left
      actor :obs1, charset: :MERIDIAN_AGENT, color: [224, 224, 232], at: [190, 306], dir: :right
      actor :obs2, charset: :MERIDIAN_AGENT, color: [224, 224, 232], at: [316, 308], dir: :left
      emit :snow, rate: 14
      fade_in duration: 0.5
      fade :tripod, to: 0, duration: 1.6
      hop :quent, height: 3, times: 3, duration: 1.5
      burst :motes, at: [226, 262], count: 10, color: :electric
      pan by: [8, 0], duration: 3.4, ease: :linear
      say who[:quent], "Lovely reading. Simply lovely.", duration: 3.2

      #--- 15: the steam-glass plain at sunrise ---------------------------------
      fade_out duration: 0.6
      stop_emit
      clear_actors
      clear_backgrounds
      stage.call(:glass, true)
      camera at: [60, 192], zoom: 1.0
      tone to: [30, 12, -8, 36], duration: 0
      emit :motes, area: [-100, 200, 720, 140], rate: 14, color: :bleed
      fade_in duration: 0.9
      pan by: [340, 0], duration: 5.2, ease: :linear
      say who[:larch], "That wasn't a battle to them. That was a reading.", duration: 4.2
      fade_out duration: 1.2
    end

    define(:WAR_CLIMAX, vars: proc { Cutscene.war_vars }, &WAR_CLIMAX_BLOCK)
    [:A2, :B, :C].each { |v| build(:WAR_CLIMAX, variant: v) }              # author-time check of every variant
    build(:WAR_CLIMAX, legends: false)
    build(:WAR_CLIMAX, variant: :C, overpower: true)
    define(:WAR_CLIMAX_DEMO) { include_scene(:WAR_CLIMAX, variant: var(:variant, :A2)) }
  end
end
