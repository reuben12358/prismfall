#===============================================================================
# Prismfall Cutscenes - 013 The war climax (story/13_CUTSCENES.md, WAR-1)
#-------------------------------------------------------------------------------
# :WAR_CLIMAX  "The Beam Clash on the Shattered Ice" - 15 shots, about 63 s.
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
      water_pal = :seaclash
      fire_pal  = :fireclash
      who = WAR_SPEAKERS
      clash_pt = [256, 214]
      overpower = var(:overpower, false) && [:B, :C].include?(variant)
      clash_end = :fizzle
      clash_end = :both if variant == :A2
      clash_end = ((variant == :B) ? :b : :a) if overpower

      #--- the stage -----------------------------------------------------------
      background :sky, palette: :dawn, sun: [256, 150]
      background :mountains, color: [72, 72, 120], y: 204, height: 60, snow: true
      background :fortress, x: -420, y: 214, width: 260, height: 130, color: [56, 72, 112], glow: [176, 224, 255]
      background :fortress, x: 680, y: 214, width: 260, height: 140, color: [64, 32, 40], glow: [255, 160, 64]
      background :fleet, x: -330, y: 232, width: 300, count: 5, color: [48, 64, 104]
      background :ice, palette: :dawn, plates: true, cracks: 10
      letterbox true, duration: 0
      camera at: [-40, 192]
      bgm :bgm_war_field
      bgs :bgs_war, volume: 70
      army :isenmar, icons: [:WALREIN, :MAMOSWINE], count: 18, rows: 3, area: [-260, 268, 300, 70], facing: :right
      army :ashkaar, charset: :ASHKAAR_SOLDIER, color: [200, 72, 48], count: 16, rows: 3, area: [470, 268, 300, 70], facing: :left
      army :riders, icons: [:SALAMENCE, :CHARIZARD], count: 8, rows: 2, area: [500, 96, 230, 50], facing: :left
      actor :ship, prop: :ship, color: [72, 96, 144], at: [-150, 262], scale: 2
      actor :eirik, charset: :ISENMAR_OFFICER, color: [96, 160, 224], at: [-150, 236], dir: :right
      actor :hrothgar, charset: :ASHKAAR_OFFICER, color: [224, 96, 56], at: [640, 208], dir: :left

      #--- 1: wide pan across both hosts ---------------------------------------
      emit :snow, area: [-320, -20, 520, 20], rate: 26, id: :snow_left
      emit :embers, area: [330, 250, 420, 80], rate: 22, id: :embers_right
      pan to: [552, 192], duration: 4.6, ease: :in_out
      wait 4.8

      #--- 2: the water bulges; the sea-beast rises ----------------------------
      cut at: [84, 236], zoom: 1.25
      actor :water, species: water, at: [84, 500], flip: true, mouth: (legends) ? [-56, -100] : nil
      se :rumble
      shake power: 5, duration: 1.6, decay: false
      emit :steam, at: [84, 316], rate: 30, duration: 1.6, id: :bulge
      wait 0.5
      move :water, to: [84, 316], duration: 1.3, ease: :out
      wait 0.7
      burst :ice_shards, at: [84, 310], count: 26
      burst :debris, at: [84, 310], count: 10, color: :ice
      ring at: [84, 312], color: :water, radius: 150, duration: 0.8
      cry water
      emit :rain, rate: 70, id: :rain
      bgs :bgs_rain, volume: 60
      tone to: [-24, -12, 28, 0], duration: 1.0
      wait 0.6
      say who[:eirik], "Isenmar! The sea remembers it's a sea!"

      #--- 3: the Warfort wall; the fire answers --------------------------------
      cut at: [600, 176], zoom: 1.25
      if legends
        actor :stone, prop: :stone, color: [240, 240, 255], at: [640, 196], scale: 1
        move :stone, by: [0, -40], duration: 0.8, ease: :out
        hop :hrothgar, height: 6, duration: 0.4
        wait 0.9
        flash duration: 0.7
        se :beam_break
        burst :sparks, at: [640, 150], count: 30, color: :white
        remove :stone
      else
        wait 0.5
      end
      actor :fire, species: fire, at: [566, 150], opacity: 0, scale: 0.5, mouth: (legends) ? [-30, -192] : nil
      fade :fire, to: 255, duration: 0.4
      scale :fire, to: 1.0, duration: 0.6, ease: :out_back
      move :fire, to: [566, 262], duration: 0.9, ease: :out
      cry fire
      tone to: [16, -4, 4, 0], duration: 0.8
      wait 1.0
      say who[:hrothgar], "Then let it remember fire."

      #--- 4: both gather their power (seam at mid-screen) ----------------------
      move :fire, to: [430, 286], duration: 0.7, ease: :in_out
      cut at: [256, 200], zoom: 1.0
      bgm_fade 0.5
      together do
        charge_up at: :water, color: water_pal, duration: 2.0, size: 16
        charge_up at: :fire, color: fire_pal, duration: 2.0, size: 16
        tremble :water, duration: 2.0
        tremble :fire, duration: 2.0
        tone to: [-8, -8, 8, 0], duration: 1.5
      end

      #--- 5-11: the clash runs under seven shots -------------------------------
      s5, s6, s7, s8, s9, s10, s11 = 1.5, 3.2, 3.6, 3.0, 4.6, 3.2, 3.2
      total = s5 + s6 + s7 + s8 + s9 + s10 + s11
      bgm :bgm_war_clash
      beam_clash a: { from: :water, color: water_pal, width: 32 }, b: { from: :fire, color: fire_pal, width: 32 },
                 id: :clash, duration: total, launch: 1.2, resolve: s11, winner: clash_end,
                 curve: [[0, 0.5], [0.08, 0.36], [0.16, 0.64], [0.24, 0.5], [0.5, 0.47], [0.75, 0.53], [1, 0.5]],
                 ball: 26, shake: 3, ground: 306, wait: false
      wait s5
      # 6: hard zoom on the meeting point
      pan to: clash_pt, zoom: 1.5, duration: 0.35, ease: :out
      clash_mod :clash, shake: 6
      3.times do |i|
        at(now + 0.5 + (i * 0.8)) do
          ring at: [256, 300], color: :ice, radius: 200 + (i * 40), duration: 0.9, squash: 0.3
          burst :ice_shards, at: [200 + (i * 56), 300], count: 10
        end
      end
      wait s6
      # 7: the ice turns to steam-glass
      cut at: [256, 200], zoom: 1.0
      clash_mod :clash, shake: 3, intensity: 0.7, duration: 0.5
      army_fall :isenmar, fraction: 0.45, duration: 0.6
      army_fall :ashkaar, fraction: 0.45, duration: 0.6
      army_fall :riders, fraction: 0.4, duration: 0.8
      emit :steam, area: [140, 290, 240, 40], rate: 46, id: :steamline
      ring at: [256, 304], color: :steam, radius: 300, duration: 1.6, squash: 0.25
      se :crowd_gasp
      wait 0.9
      say who[:soldier], "The Steamline! It's coming this way!", duration: s7 - 0.9
      # 8: the dome of Bleed light
      dome at: [256, 280], radius: 250, duration: s8 - 0.4, squash: 0.55
      army_tint :isenmar, color: :bleed, amount: 120, duration: s8
      army_tint :ashkaar, color: :bleed, amount: 120, duration: s8
      stop_emit :embers_right
      wait s8
      # 9: the PC goes in
      case variant
      when :B
        actor :mount, species: :SALAMENCE, at: [620, 190], scale: 0.5
        actor :pc, player: true, at: [620, 150], dir: :left, z: 900
        cut at: [470, 200], zoom: 1.25
        pan to: [330, 220], duration: s9 - 0.3
        move :mount, to: [330, 300], duration: s9 - 0.4, ease: :out
        move :pc, to: [330, 258], duration: s9 - 0.4, ease: :out
        dome hole_at: :pc, hole: 54, duration: 2.0
        wait 0.8
        say who[:sigrun], "Hold on!", duration: 2.0
        wait s9 - 2.8
      when :C
        actor :prow, prop: :ship, color: [72, 96, 144], at: [-120, 330], scale: 2, flip: true
        actor :pc, player: true, at: [-100, 300], dir: :right, z: 900
        cut at: [40, 220], zoom: 1.25
        pan to: [190, 230], duration: s9 - 0.3
        move :prow, to: [190, 330], duration: s9 - 0.4, ease: :out
        move :pc, to: [210, 300], duration: s9 - 0.4, ease: :out
        dome hole_at: :pc, hole: 54, duration: 2.0
        wait 0.8
        say who[:marisol], "Tides take it, kid, now!", duration: 2.4
        wait s9 - 3.2
      else
        actor :pc, player: true, at: [40, 326], dir: :right
        actor :starter, charset: var(:starter_charset, "Followers/EEVEE"), color: [176, 136, 96], at: [14, 328], dir: :right
        cut at: [90, 250], zoom: 1.5
        pan to: [200, 250], duration: s9 - 0.3, ease: :linear
        move :pc, to: [214, 326], duration: s9 - 0.4, walk: true, ease: :linear
        move :starter, to: [188, 328], duration: s9 - 0.4, walk: true, ease: :linear
        dome hole_at: :pc, hole: 54, duration: 2.5
        tint :pc, color: [255, 255, 255], amount: 70, duration: 2.5
        wait s9
      end
      # 10: the hand goes up; the beams go white
      cut at: { actor: :pc, part: :center, offset: [10, -40] }, zoom: 2.0
      hop :pc, height: 4, duration: 0.3
      tint :pc, color: [255, 255, 255], amount: 150, duration: 1.0
      emit :motes, from: { actor: :pc, part: :top }, rate: 30, color: :white, angle: -90, spread: 20, speed: 4, id: :shard
      ring at: { actor: :pc, part: :center }, color: :white, radius: 320, duration: 2.2, squash: 0.8, layer: :front
      clash_mod :clash, white: (overpower) ? 0.0 : 1.0, intensity: (overpower) ? 1.0 : 0.4, shake: (overpower) ? 5 : 2, strobe: overpower, duration: 2.4
      wait s10
      # 11: silence (A/B/C) or the white-out (A2)
      cut at: clash_pt, zoom: 1.25
      stop_emit :shard
      stop_emit :rain
      bgs_fade 1.0
      bgm_fade 0.4
      if variant == :A2
        wait s11 * 0.5
        dome radius: 420, duration: 0.6
        fade :water, to: 0, duration: 1.2
        fade :fire, to: 0, duration: 1.2
        wait s11 * 0.5
        flash duration: 2.4
        dome off: true
        stop_emit :steamline
        rout :isenmar, by: [0, 0], duration: 0.1
        rout :ashkaar, by: [0, 0], duration: 0.1
        rout :riders, by: [0, 0], duration: 0.1
        remove :pc
        camera at: [256, 200], zoom: 1.0
        tone to: [8, 8, 16, 60], duration: 0
        background :ice, palette: :glass, cracks: 4
        emit :snow, rate: 26
        wait 1.6
      else
        emit :snow, rate: 30
        wait s11
        tone to: [0, 0, 8, 20], duration: 1.5

        #--- 12: the two legends look down, and leave --------------------------
        cut at: [256, 206], zoom: 1.0
        dome radius: 120, duration: 2.0
        hop :water, height: 4, duration: 0.5
        hop :fire, height: 4, duration: 0.5
        wait 1.2
        move :water, by: [0, 260], duration: 2.2, ease: :in
        fade :water, to: 0, duration: 2.2
        ring at: [96, 316], color: :water, radius: 120, duration: 1.2, squash: 0.3
        flip :fire
        move :fire, to: [760, 30], duration: 2.2, ease: :in
        text "It looked at me as if I were very small and very familiar. Again.", position: :top, duration: 3.6
        dome off: true
      end
      bgm :bgm_war_after

      #--- 13: what is left ------------------------------------------------------
      case variant
      when :A
        cut at: [236, 230], zoom: 1.25
        actor :sigrun, charset: :LEADER_SIGRUN, color: [216, 88, 56], at: [300, 60], dir: :left
        actor :anja, charset: :LEADER_ANJA, color: [112, 168, 224], at: [20, 330], dir: :right
        move :sigrun, to: [272, 326], duration: 0.7, ease: :in
        move :anja, to: [156, 326], duration: 1.6, walk: true
        wait 0.7
        burst :smoke, at: [272, 326], count: 8
        shake power: 3, duration: 0.2
        wait 1.0
        face :sigrun, :right
        face :anja, :left
        say who[:sigrun], "Father. Enough."
        say who[:anja], "Eirik. Enough."
        say "#{who[:sigrun]} & #{who[:anja]}", "The Boon will settle it.", duration: 2.6
      when :A2
        actor :eirik2, charset: :ISENMAR_OFFICER, color: [96, 160, 224], at: [-30, 326], dir: :right
        actor :hrothgar2, charset: :ASHKAAR_OFFICER, color: [224, 96, 56], at: [540, 326], dir: :left
        move :eirik2, to: [150, 326], duration: 3.0, walk: true, ease: :linear
        move :hrothgar2, to: [360, 326], duration: 3.0, walk: true, ease: :linear
        wait 3.2
        text "Both lines were gone. Two rulers stood alone on the glass.", duration: 3.6
      else
        winner_army, loser_army = (variant == :B) ? [:ashkaar, :isenmar] : [:isenmar, :ashkaar]
        loser_x = (variant == :B) ? -300 : 800
        col = (variant == :B) ? [224, 72, 40] : [72, 136, 224]
        cut at: [256, 200], zoom: 1.0
        rout loser_army, duration: 2.6
        emit :smoke, area: [(variant == :B) ? -80 : 380, 280, 220, 40], rate: 18, id: :rout_smoke
        march winner_army, by: [(variant == :B) ? -70 : 70, 0], duration: 2.6
        pan to: [(variant == :B) ? 40 : 472, 190], duration: 2.6
        wait 2.6
        3.times do |i|
          actor :"banner#{i}", prop: :banner, color: col, at: [loser_x + 40 + (i * 70), 150 - (i.odd? ? 16 : 0)], scale: 2, opacity: 0
          fade :"banner#{i}", to: 255, duration: 0.5
          move :"banner#{i}", by: [0, -26], duration: 0.6, ease: :out
        end
        pan to: [(variant == :B) ? -170 : 690, 180], duration: 1.4
        wait 1.6
        say (variant == :B) ? who[:hrothgar] : who[:eirik], "It's done."
        say (variant == :B) ? who[:anja] : who[:sigrun], "I'll remember which side you stood on.", duration: 3.2
      end

      #--- 14: the observers on the ridge ---------------------------------------
      fade_out duration: 0.5
      stop_emit
      camera at: [1600, 170], zoom: 1.25
      tone to: [0, 0, 0, 0], duration: 0
      actor :tripod, prop: :tripod, color: [208, 168, 72], at: [1570, 300], scale: 2
      actor :quent, charset: :MERIDIAN_QUENT, color: [240, 240, 244], at: [1620, 304], dir: :left
      actor :obs1, charset: :MERIDIAN_AGENT, color: [224, 224, 232], at: [1528, 306], dir: :right
      actor :obs2, charset: :MERIDIAN_AGENT, color: [224, 224, 232], at: [1668, 308], dir: :left
      fade_in duration: 0.5
      fade :tripod, to: 0, duration: 1.6
      hop :quent, height: 3, times: 3, duration: 1.5
      burst :motes, at: [1570, 262], count: 10, color: :electric
      say who[:quent], "Lovely reading. Simply lovely.", duration: 3.2

      #--- 15: the steam-glass plain at sunrise ---------------------------------
      fade_out duration: 0.6
      camera at: [96, 200], zoom: 1.0
      clear_actors
      background :ice, palette: :glass, cracks: 4 if variant != :A2
      army_tint :isenmar, color: [232, 240, 255], amount: 235, duration: 0
      army_tint :ashkaar, color: [232, 240, 255], amount: 235, duration: 0
      tone to: [24, 8, -8, 30], duration: 0
      emit :motes, area: [0, 200, 512, 140], rate: 12, color: :bleed
      fade_in duration: 0.9
      pan by: [330, 0], duration: 5.0, ease: :linear
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
