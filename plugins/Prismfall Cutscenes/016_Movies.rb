#===============================================================================
# Prismfall Cutscenes - 016 movies (Pillar 2 sakuga) and live-map acting sheets (Pillar 1)
#-------------------------------------------------------------------------------
# Gemini cinematics spec (gemini_recommends/2026-11-22_rejuv-v14-cutscene-cinematics-spec §2.A / §3.2.1).
#
#   Prismfall::Cutscene.movie("pf_ch5_spire_shatter")
#       Movies/<name>.ogv through mkxp-z's Graphics.play_movie (Ogg Theora), or
#       Movies/<name>_safe.ogv when Cutscene.photosensitive? (no strobes). The BGM is
#       stopped first and the screen held black for 2 frames on each side (the spec's
#       hard cut). Returns false (and plays nothing) when the engine has no
#       play_movie or the file is missing, so the caller can fall back.
#
#   Prismfall::Cutscene.act("Mourner", "act_ch5_mourner_reach", frames: 0..11, hold: 0.12)
#       steps a map event through cells of a 4x4 acting sheet in Graphics/Characters
#       (cell n = row n / 4 (down, left, right, up), column n % 4). hold: seconds per
#       frame, or an Array (one per frame, the last repeats). The event keeps the last
#       frame. Event: id, name, or a Game_Event.
#
#   pfm_cutscene(:SH1)   named live-map scenes (CUTSCENE_SCENES below); the map scripts
#                        call these, and unknown ids are a logged no-op.
#===============================================================================
module Prismfall
  module Cutscene
    MOVIE_DIR = "Movies/"

    class << self
      def movie_file(name)
        base = name.to_s.sub(/\.ogv\z/, "")
        base = MOVIE_DIR + base if !base.include?("/")
        candidates = []
        candidates << base + "_safe.ogv" if photosensitive?
        candidates << base + ".ogv"
        candidates << base + "_safe.ogv"
        return candidates.find { |f| File.exist?(f) }
      end

      def movie(name, volume: 100, skippable: true)
        file = movie_file(name)
        return false if !file || !Graphics.respond_to?(:play_movie)
        pbBGMStop(0.0) rescue nil
        pbBGSStop(0.0) rescue nil
        2.times { Graphics.update }
        begin
          Graphics.play_movie(file, volume, skippable)
        rescue ArgumentError
          Graphics.play_movie(file, volume)      # older mkxp-z: no skippable argument
        end
        2.times { Graphics.update }
        return true
      rescue StandardError => e
        PBDebug.log("[Prismfall movie] #{e.class}: #{e.message}") if defined?(PBDebug)
        return false
      end

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

      # A soft stand-in when a scene's movie can't play: a flash (a dim pulse when photosensitive).
      def fallback_flash(color = [255, 220, 255])
        if photosensitive?
          $game_screen.start_tone_change(Tone.new(60, 50, 60, 0), 8) rescue nil
          pbWait(0.2)
        else
          $game_screen.start_tone_change(Tone.new(*color, 0), 4) rescue nil
          pbSEPlay("Anim/Explosion7") rescue nil
          pbWait(0.5)
        end
        $game_screen.start_tone_change(Tone.new(0, 0, 0, 0), 30) rescue nil
      end
    end

    # Live-map scenes the generated maps call by id (mapgen layouts: pfm_cutscene(:ID)).
    CUTSCENE_SCENES = {
      # Ch5 Peak #1, the Spire Shatter (952): the Mourner reaches gently, lunges as the Splitter fires (sheet cells
      # 12..15), the sakuga movie, then (SH1_BURN) he clutches his smoking hand and leaves through the service door.
      :SH1 => proc {
        Cutscene.act("Mourner", "act_ch5_mourner_reach", frames: 0..11, hold: [0.35, 0.2, 0.2, 0.25, 0.12])
        Cutscene.act("Mourner", "act_ch5_mourner_reach", frames: 12..15, hold: 0.06)
        Cutscene.fallback_flash if !Cutscene.movie("pf_ch5_spire_shatter")
      },
      :SH1_BURN => proc {
        Cutscene.act("Mourner", "act_ch5_mourner_burn", frames: 0..15, hold: [0.3, 0.14, 0.14, 0.14, 0.2])
      },
      :SH1_EXIT => proc {
        ev = Cutscene.find_event("Mourner")
        ev&.erase
      }
    }
  end
end

def pfm_cutscene(id)
  scene = Prismfall::Cutscene::CUTSCENE_SCENES[id.to_s.upcase.to_sym]
  if !scene
    PBDebug.log("[Prismfall] pfm_cutscene(#{id.inspect}): no such scene") if defined?(PBDebug)
    return false
  end
  scene.call
  return true
end
