#===============================================================================
# Prismfall Cutscenes - 016 the live-map scene registry (was: movies), acting sheets, scene audio tags
#-------------------------------------------------------------------------------
# No movies (creator directive, Gemini 2026-11-24_rejuv-advanced-animations-engine §0): the .ogv path is
# gone. Every scene is in-engine choreography on the real tilemap, played by 017_AdvancedAnimations.rb.
#
#   pfm_cutscene(:ID)      what map events call. Plays the scene if its maps are built, then hands the map,
#                          the player, the screen tone and the BGM back. Returns true if it played. It never
#                          raises: an unknown id, a scene whose map isn't built yet, or a scene that fails
#                          is logged (PBDebug + Cutscene.scene_log) and returns false, so an event can do
#                          `if pfm_cutscene(:SH1) ... else <the lines as text> end`.
#   pfm_cutscene(:ID, preview: true)
#                          also plays a scene that is still staged on a stand-in map (debug / harness).
#   Prismfall::Cutscene.scene_status(:ID)   :ready, :standin (staged on a stand-in; its own map isn't
#                          built), :unbuilt (a map it needs is missing) or nil (unknown id).
#
#   Prismfall::Cutscene.act("Mourner", "act_ch5_mourner_reach", frames: 0..11, hold: 0.12)
#       small inline gesture: steps a map event through cells of a 4x4 acting sheet in Graphics/Characters
#       (cell n = row n / 4 (down, left, right, up), column n % 4). hold: seconds per frame, or an Array
#       (one per frame, the last repeats). The event keeps the last frame. Event: id, name, or a Game_Event.
#
#   Prismfall::Cutscene.scene_bgm("ch9_tension") / scene_se("ch16_gunshot")
#       the scenes' audio tags -> a file that exists in Audio/BGM or Audio/SE (SCENE_BGM / SCENE_SE below),
#       or nil (the scene stays silent there; Cutscene.missing_audio lists what was asked for).
#===============================================================================
module Prismfall
  module Cutscene
    class << self
      def find_event(ref)
        return ref if ref.is_a?(Game_Character)
        return nil if !$game_map
        return $game_map.events[ref] if ref.is_a?(Integer)
        return $game_map.events.values.find { |e| e.name == ref.to_s }
      end

      def act(ref, sheet, frames: 0..15, hold: 0.1)
        ev = find_event(ref)
        return false if !ev
        frames = frames.to_a
        holds = Array(hold)
        ev.instance_variable_set(:@character_name, sheet)
        ev.instance_variable_set(:@walk_anime, false)
        ev.instance_variable_set(:@step_anime, false)
        ev.instance_variable_set(:@direction_fix, true)
        frames.each_with_index do |cell, i|
          ev.instance_variable_set(:@direction, [2, 4, 6, 8][(cell / 4) % 4])
          ev.instance_variable_set(:@pattern, cell % 4)
          ev.instance_variable_set(:@original_pattern, cell % 4)
          secs = holds[[i, holds.length - 1].min].to_f
          pbWait([secs, 0.02].max)
        end
        return true
      end
    end

    #===========================================================================
    # Scene audio tags -> Prismfall's file names (audio/manifest.tsv "final_name"; design/AUDIO.md).
    # Each tag lists candidates in order; the first that exists plays, none = silence. These are the
    # stand-in slots until the soundtrack picks are locked (the anime-OST audition pool is not wired).
    #===========================================================================
    SCENE_BGM = {
      "ch2_dorian_stage"      => ["Gym - Warden Hall"],          # Dorian's spotlight flourish
      "ch2_mourner_sermon"    => ["Theme - Hollow"],             # the Mourner's sermon from the torn canvas
      "ch5_girei_intro"       => ["Theme - Hollow"],
      "ch5_vogel_climax"      => ["Mood - Tension"],
      "ch5_lowlight_grief"    => ["Mood - Farewell"],
      "ch8_caldera_crisis"    => ["Mood - Tension"],
      "ch8_lightstone_burden" => ["Mood - Emotion"],
      "ch9_tension"           => ["Mood - Tension"],
      "ch9_never_meant"       => ["Mood - Farewell"],
      "ch10_veil_hollow"      => ["Route - Elowen Forest"],
      "ch10_bride_tree_grace" => ["Mood - Emotion"],
      "ch11_ominous"          => ["Mood - Mystery"],
      "ch11_kyogre_thaw"      => ["Battle - Legendary", "Mood - Tension"],
      "ch13_predators"        => ["Theme - Meridian"],
      "ch13_voss_spin"        => ["Theme - Meridian"],
      "ch13_fault_dread"      => ["Mood - Tension"],
      "ch15_ominous"          => ["Mood - Mystery"],
      "ch15_decretum"         => ["Mood - Farewell"],
      "ch16_wenlow_warm"      => ["Town - Nadir"],
      "ch16_aftermath_violin" => ["Mood - Farewell"],
      "ch17_murals"           => ["Dungeon - Ruins"],
      "ch17_voss_treachery"   => ["Theme - Meridian"],
      "ch19_dynast"           => ["War - March"],
      "ch19_war_clash"        => ["War - Beam Clash"],
      "ch19_aftermath"        => ["War - Aftermath"],
      "ch21_arceus_bound"     => ["Mood - Mystery"],
      "ch21_tkt"              => ["Mood - Emotion"],
      "ruin_intro_organ"      => ["Dungeon - Ruins"],
      # PROVISIONAL: the Gilded King's theme is on hold (Reuben). Gemini's scene asks for "Cosmic Air";
      # until the pick is made his entrance borrows the Accord's regal theme. Change only this line.
      "ruin_cosmic_air"       => ["Theme - Accord"]
    }
    SCENE_SE = {
      "ch16_gunshot"     => ["Directorate Rifle Crack"],         # audio/gemini_cc0/SE
      "ch8_foundry_bell" => ["Foundry Bell", "Anim/HealBell"]    # no bronze bell SE yet: the stock chime stands in
    }

    @missing_audio = []
    @scene_log = []
    @scene_running = false

    class << self
      attr_reader :missing_audio, :scene_log

      def audio_there?(folder, name)
        path = "Audio/#{folder}/#{name}"
        return FileTest.audio_exist?(path) if FileTest.respond_to?(:audio_exist?)
        return true
      end

      def scene_audio_file(folder, table, tag)
        names = table[tag.to_s] || [tag.to_s]
        found = names.find { |n| audio_there?(folder, n) }
        if !found
          entry = "#{folder}/#{tag}"
          @missing_audio << entry if !@missing_audio.include?(entry)
        end
        return found
      end

      def scene_bgm(tag); return scene_audio_file("BGM", SCENE_BGM, tag); end
      def scene_se(tag);  return scene_audio_file("SE", SCENE_SE, tag);   end
    end

    #===========================================================================
    # The live-map scenes. :play is the AdvancedAnimations method; :staged the maps its choreography was
    # authored on; :canon the maps the story sets it on. Where they differ the scene waits (the tile
    # coordinates belong to the stand-in): when the canon map is built, restage the scene on it in
    # 017_AdvancedAnimations.rb and make :staged match :canon here.
    #===========================================================================
    SCENES = {
      :CH2_PAGEANT      => { :play => :play_ch2_lantern_pageant_dc,    :staged => [145],      :canon => [145],
                             :aliases => [:CH2_PAGEANT_DC, :CH2_DC] },
      :CH5_DC           => { :play => :play_ch5_spire_shatter_dc,      :staged => [952, 608], :canon => [952, 608],
                             :aliases => [:SH1_DC, :CH5_SHATTER_DC, :CH5_SHATTER] },
      :CH8_CALDERA      => { :play => :play_ch8_caldera,               :staged => [255, 928], :canon => [255, 244],
                             :aliases => [:CH8_FIVE_BELLS, :CH8_DC] },
      :CH9_UNMASK       => { :play => :play_ch9_trevenant_unmasking,   :staged => [295],      :canon => [264],
                             :aliases => [:IR1] },
      :CH10_BRIDE_GROVE => { :play => :play_ch10_bride_grove,          :staged => [525],      :canon => [708],
                             :aliases => [:CH10_JUNO, :CH10_DC] },
      :CH11_RETHINK     => { :play => :play_ch11_kyogre_rethink,       :staged => [563],      :canon => [309],
                             :aliases => [:CH11_KYOGRE_RETHINK, :CH11_THAW_DC, :CH11_DC, :CH11_KYOGRE, :CH11_THAW, :KYOGRE] },
      :CH13_FAULT       => { :play => :pf_play_ch13_glass_court_fault, :staged => [287, 174], :canon => [343],
                             :aliases => [:CH13_GLASS_COURT, :CH13_DC] },
      :CH15_GLASSFALL   => { :play => :pf_play_ch15_glassfall_rethink, :staged => [295],      :canon => [391],
                             :aliases => [:CE1, :GLASSFALL] },
      :CH16_WENLOW      => { :play => :play_ch16_wenlow,               :staged => [104, 544], :canon => [223, 363],
                             :aliases => [:CH16_PURGE, :CH16_DC] },
      :CH17_SUN_COURT   => { :play => :pf_play_ch17_sun_court_breach,  :staged => [186],      :canon => [826],
                             :aliases => [:CH17_BREACH, :CH17_DC] },
      # 926's own event still plays the branching Prismfall::Cutscene.play(:WAR_CLIMAX) (013_Scenes_War_OnMap.rb,
      # four outcomes by :war_climax). This is Gemini's single-outcome version; it is not wired to the map.
      :WAR_CLIMAX       => { :play => :pf_play_ch19_war1_rethink,      :staged => [926],      :canon => [926],
                             :aliases => [:WAR1, :CH19_WAR] },
      :CH21_ARCEUS      => { :play => :pf_play_ch21_arceus_rethink,    :staged => [285],      :canon => [491],
                             :aliases => [:CH21_FINALE, :THE_LIGHT] },
      :RUIN_AURELIUS_DC => { :play => :play_ruin_aurelius_dc,          :staged => [186],      :canon => [491],
                             :aliases => [:RUIN_R7_AURELIUS, :RUIN_AURELIUS] }
    }

    # Ch5: story/24_SCRIPT_CH5.md keeps the glass Lowlight for map 608 after the boss (SH-1 beat 4: "no streets
    # shown"; Rook's "Turn it off" is "saved for the Lowlight"). Gemini's Director's Cut cuts to Dex freezing
    # in the middle of the vault scene. false = the vault scene without that cutaway; true = Gemini's full cut
    # (pfm_cutscene(:CH5_DC) always plays the full cut).
    SH1_LOWLIGHT_CUTAWAY = false

    class << self
      def scene_key(id)
        key = id.to_s.upcase.to_sym
        return key if SCENES[key]
        SCENES.each { |k, info| return k if info[:aliases].include?(key) }
        return nil
      end

      def map_built?(map_id)
        file = format("Data/Map%03d.rxdata", map_id)
        return pbRgssExists?(file) if defined?(pbRgssExists?)
        return File.exist?(file)
      end

      def scene_status(id)
        info = SCENES[scene_key(id)]
        return nil if !info
        return :unbuilt if !info[:staged].all? { |m| map_built?(m) }
        return :standin if info[:staged] != info[:canon]
        return :ready
      end

      def scene_note(msg)
        @scene_log << msg
        @scene_log.shift if @scene_log.length > 60
        PBDebug.log("[Prismfall cutscene] #{msg}") if defined?(PBDebug)
        return false
      end

      # Plays a registered scene. true = it ran to the end. Never raises.
      def play_scene(id, preview: false, **opts)
        key = scene_key(id)
        return scene_note("#{id.inspect}: no such scene") if !key
        info = SCENES[key]
        return scene_note("#{key}: the scene engine (017_AdvancedAnimations.rb) is not loaded") if !defined?(Prismfall::AdvancedAnimations)
        return scene_note("#{key}: not on the map (#{$scene.class}); skipped") if !defined?(Scene_Map) || !$scene.is_a?(Scene_Map)
        return scene_note("#{key}: a scene is already playing; skipped") if @scene_running
        case scene_status(key)
        when :unbuilt
          return scene_note("#{key}: waits for map(s) #{info[:staged].reject { |m| map_built?(m) }.join(', ')}; skipped")
        when :standin
          if !preview
            return scene_note("#{key}: staged on stand-in map(s) #{info[:staged].join(', ')}, waits for #{info[:canon].join(', ')}; skipped")
          end
        end
        @scene_running = true
        begin
          Prismfall::AdvancedAnimations.public_send(info[:play], **opts)
        ensure
          @scene_running = false
        end
        scene_note("#{key}: played")
        return true
      rescue StandardError => e
        scene_note("#{key}: #{e.class}: #{e.message} (#{(e.backtrace || []).first})")
        return false
      end

      # 952 after the Shatter scene: the player stands at the foot of the dais stairs (where the event's own
      # walk-in used to leave them), the Mourner is gone and the cradle shows its cracked tile until
      # CH5_STEP 9 turns its page.
      def sh1_aftermath
        cradle = find_event("Cradle")
        if cradle
          $game_player.moveto(cradle.x, cradle.y + 5)
          $game_player.turn_up
          cracked = (cradle.instance_variable_get(:@event).pages[1].graphic.tile_id rescue 0)
          cradle.instance_variable_set(:@tile_id, cracked) if cracked > 0
        end
        find_event("Mourner")&.erase
      end
    end

    # Ids the generated maps call that are not a scene of their own (mapgen layouts: pfm_cutscene(:ID)).
    CUTSCENE_SCENES = {
      # Ch5 Peak #1, the Spire Shatter (952). One call plays the whole beat: the Mourner and Sable at the
      # cradle, the Splitter, the Shatter, the smoking hand, his exit by the service door, the Electivire.
      :SH1 => proc {
        next false if !Cutscene.play_scene(:CH5_DC, lowlight: SH1_LOWLIGHT_CUTAWAY)
        Cutscene.sh1_aftermath
        true
      },
      :SH1_BURN => proc { true },                               # folded into :SH1 (maps built before 2026-11-25 call it)
      :SH1_EXIT => proc { Cutscene.find_event("Mourner")&.erase; true }
    }
  end
end

def pfm_cutscene(id, preview: false, **opts)
  legacy = Prismfall::Cutscene::CUTSCENE_SCENES[id.to_s.upcase.to_sym]
  return (legacy.call ? true : false) if legacy
  return Prismfall::Cutscene.play_scene(id, preview: preview, **opts)
rescue StandardError => e
  Prismfall::Cutscene.scene_note("#{id.inspect}: #{e.class}: #{e.message}")
  return false
end
