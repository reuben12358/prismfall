#===============================================================================
# Prismfall Core - 031 Audio cues (Audio v4.3 wiring)
#-------------------------------------------------------------------------------
# One place for the named jingles / sound effects the plugins play, and the
# safety net for music that is not installed yet.
#
#   Prismfall::AudioCue.me(:badge_get)        # first existing file of the cue
#   Prismfall::AudioCue.se(:boss_shield)
#   Prismfall::AudioCue.bgm_name("Battle - Boss")   # -> the name, a stock
#                                                   #    stand-in, or nil
#
# Tracks come from audio/manifest.tsv (python3 audio/install_audio.py <game>).
# A project without them keeps working: a cue with no file is silent, and a
# trainer type whose BattleBGM / VictoryBGM file is missing gets the stock
# track it used before (BGM_FALLBACK), never silence.
# Docs: design/AUDIO.md, design/AUDIO_SOUNDTRACK_PLAN.md, design/MAP_AUDIO.yaml.
#===============================================================================
module Prismfall
  module AudioCue
    # Jingles (Audio/ME). First file that exists wins; none = silent.
    ME = {
      :badge_get   => ["Warden Badge Get", "Badge get"],
      :trial_rank  => ["Trial Rank Up", "Badge get"],
      :game_over   => ["Prismfall game over"]
    }
    # Sound effects (Audio/SE).
    SE = {
      :boss_shield   => ["Boss Shield Break", "Battle damage super"],
      :field_shatter => ["Field Shatter"],
      :glass_quench  => ["Glass Quench"],
      :prism_swell   => ["Prism Arena Swell"],
      :vs_lightning  => ["VS Cutin Lightning", "Vs sword"]
    }
    # Music (Audio/BGM).
    BGM = {
      :title          => ["Title - Prismfall"],
      :boss           => ["Battle - Boss"],
      :boss_legendary => ["Battle - Legendary", "Battle - Boss"],
      :boss_arceus    => ["Battle - Arceus", "Battle - Boss"],
      :boss_final_bar => ["Battle - Boss Final Bar"]
    }
    # Prismfall track -> the stock base-project track played while it is not
    # installed (what pbs/trainer_types.txt named before Audio v4.3).
    BGM_FALLBACK = {
      "Battle - Warden"         => "Battle Gym Leader",
      "Battle - Juno"           => "Battle Elite",
      "Battle - Kestrel"        => "Battle Elite",
      "Battle - Valen"          => "Battle Champion",
      "Battle - Hollow"         => "Battle trainer",
      "Battle - Hollow Admin"   => "Battle Elite",
      "Battle - Mourner"        => "Battle Elite",
      "Battle - Meridian"       => "Battle trainer",
      "Battle - Meridian Admin" => "Battle Elite",
      "Battle - Voss"           => "Battle Champion",
      "Battle - Cameo"          => "Battle Champion",
      "Battle - Ruin"           => "Battle Champion",
      "War - Battlefield"       => "Battle trainer",
      "Battle - Boss"           => "Battle Elite",
      "Battle - Legendary"      => "Battle Elite",
      "Battle - Trainer"        => "Battle trainer",
      "Battle - Wild"           => "Battle wild",
      "Victory - Sovereign"     => "Battle victory leader",
      "Victory - Festival"      => "Battle victory leader"
    }
    BGM_PATH_PREFIX = "../../Audio/BGM/"   # how the victory getters hand their file to the ME channel
    SE_VOLUME = 90

    module_function

    def exists?(folder, name)
      return false if name.nil? || name.to_s.empty?
      return true if !FileTest.respond_to?(:audio_exist?)
      return FileTest.audio_exist?("Audio/#{folder}/#{name}")
    rescue StandardError
      return false
    end

    # cue: a key of the table, a file name, or a list of file names.
    def resolve(folder, table, cue)
      list = (cue.is_a?(Symbol)) ? (table[cue] || []) : Array(cue)
      return list.find { |n| exists?(folder, n) }
    end

    def me(cue, volume = nil, pitch = nil)
      file = resolve("ME", ME, cue)
      return false if !file || !defined?(pbMEPlay)
      pbMEPlay(file, volume, pitch)
      return true
    rescue StandardError
      return false
    end

    def se(cue, volume = SE_VOLUME, pitch = nil)
      file = resolve("SE", SE, cue)
      return false if !file || !defined?(pbSEPlay)
      pbSEPlay(file, volume, pitch)
      return true
    rescue StandardError
      return false
    end

    # The file a `\me[...]` message tag should name for this cue ("" = none).
    def me_name(cue)
      return resolve("ME", ME, cue) || ""
    end

    # An installed BGM for this cue / name: the first that exists, else the
    # stock stand-in of the first name, else nil.
    def bgm_name(cue)
      list = (cue.is_a?(Symbol)) ? (BGM[cue] || []) : Array(cue)
      hit = list.find { |n| exists?("BGM", n) }
      return hit if hit
      fb = BGM_FALLBACK[list.first]
      return (fb && exists?("BGM", fb)) ? fb : nil
    end

    # audio: a String or RPG::AudioFile from one of the battle BGM getters.
    # Returns it untouched when its file exists; otherwise the stock stand-in
    # (same volume / pitch), or the original if there is no stand-in.
    def installed(audio)
      return audio if audio.nil?
      name = (audio.is_a?(String)) ? audio : audio.name
      return audio if name.nil? || name.empty?
      prefix = (name.start_with?(BGM_PATH_PREFIX)) ? BGM_PATH_PREFIX : ""
      base = name[prefix.length..]
      return audio if exists?("BGM", base)
      fb = BGM_FALLBACK[base]
      return audio if !fb || !exists?("BGM", fb)
      return prefix + fb if audio.is_a?(String)
      ret = audio.clone
      ret.name = prefix + fb
      return ret
    rescue StandardError
      return audio
    end
  end
end

#-------------------------------------------------------------------------------
# Trainer music: a trainer type's Prismfall track when it is installed, else the
# stock track. An IntroBGM whose file is missing is skipped (as before v4.3).
#-------------------------------------------------------------------------------
if defined?(pbGetTrainerBattleBGM) && !defined?(prismfall_audio_pbGetTrainerBattleBGM)
  alias prismfall_audio_pbGetTrainerBattleBGM pbGetTrainerBattleBGM
  def pbGetTrainerBattleBGM(trainer)
    return Prismfall::AudioCue.installed(prismfall_audio_pbGetTrainerBattleBGM(trainer))
  end

  alias prismfall_audio_pbGetTrainerBattleBGMFromType pbGetTrainerBattleBGMFromType
  def pbGetTrainerBattleBGMFromType(trainertype)
    return Prismfall::AudioCue.installed(prismfall_audio_pbGetTrainerBattleBGMFromType(trainertype))
  end

  alias prismfall_audio_pbGetTrainerVictoryBGM pbGetTrainerVictoryBGM
  def pbGetTrainerVictoryBGM(trainer)
    return Prismfall::AudioCue.installed(prismfall_audio_pbGetTrainerVictoryBGM(trainer))
  end

  alias prismfall_audio_pbGetWildBattleBGM pbGetWildBattleBGM
  def pbGetWildBattleBGM(wild_party)
    return Prismfall::AudioCue.installed(prismfall_audio_pbGetWildBattleBGM(wild_party))
  end

  alias prismfall_audio_pbPlayTrainerIntroBGM pbPlayTrainerIntroBGM
  def pbPlayTrainerIntroBGM(trainer_type)
    data = GameData::TrainerType.try_get(trainer_type)
    return if data && !nil_or_empty?(data.intro_BGM) && !Prismfall::AudioCue.exists?("BGM", data.intro_BGM)
    return prismfall_audio_pbPlayTrainerIntroBGM(trainer_type)
  end
end

#-------------------------------------------------------------------------------
# Title screen: "Title - Prismfall" when installed (stock Title.ogg otherwise).
#-------------------------------------------------------------------------------
if defined?(IntroEventScene) && !IntroEventScene.method_defined?(:prismfall_audio_open_title_screen)
  class IntroEventScene
    alias prismfall_audio_open_title_screen open_title_screen
    def open_title_screen(*args)
      name = Prismfall::AudioCue.resolve("BGM", Prismfall::AudioCue::BGM, :title)
      if name && $data_system && (!$data_system.title_bgm || $data_system.title_bgm.name != name)
        $data_system.title_bgm = RPG::AudioFile.new(name, 100, 100)
      end
      return prismfall_audio_open_title_screen(*args)
    end
  end
end

#-------------------------------------------------------------------------------
# Battle cues on the events the other Prismfall plugins already raise.
#-------------------------------------------------------------------------------
if defined?(EventHandlers)
  # A boss HP bar breaks: the shield-break hit; on the last bar of a wild boss
  # that plays the generic boss music, the final-bar track.
  EventHandlers.add(:prismfall_boss_bar_broken, :prismfall_audio_cue,
    proc { |battle, _battler, id, n, bars_left|
      Prismfall::AudioCue.se(:boss_shield)
      next if bars_left != 1 || !battle.wildBattle?
      next if !defined?(Prismfall::Bosses) || !Prismfall::Bosses.respond_to?(:default_music_for)
      next if Prismfall::Bosses.default_music_for != id
      data = (Prismfall::Bosses.get(id) rescue nil) || {}
      effects = [data[:on_break], (data[:breaks] || {})[n]].flatten.compact
      next if effects.any? { |e| e.is_a?(Hash) && e[:music] }
      file = Prismfall::AudioCue.resolve("BGM", Prismfall::AudioCue::BGM, :boss_final_bar)
      pbBGMPlay(file) if file
    }
  )

  # The battlefield changes mid-battle. The quench transitions (flood or fire
  # flashing to glass) hiss; every other change gets the shatter.
  EventHandlers.add(:prismfall_field_changed, :prismfall_audio_cue,
    proc { |_battle, old_id, new_id|
      next if old_id == new_id
      trans = nil
      if defined?(PrismfallEBDX) && PrismfallEBDX.respond_to?(:transition_for)
        trans = (PrismfallEBDX.transition_for(old_id, new_id) rescue nil)
      end
      if trans.is_a?(Symbol) && trans.to_s.start_with?("glass_quench")
        Prismfall::AudioCue.se(:glass_quench) || Prismfall::AudioCue.se(:field_shatter)
      else
        Prismfall::AudioCue.se(:field_shatter)
      end
    }
  )

  # The Prism Arena turns to its next borrowed field.
  EventHandlers.add(:prismfall_field_overlay_changed, :prismfall_audio_cue,
    proc { |_battle, field_id, old_ids, new_ids|
      next if field_id != :PRISM_ARENA
      next if old_ids.nil? || old_ids.empty? || old_ids == new_ids
      Prismfall::AudioCue.se(:prism_swell)
    }
  )
end
