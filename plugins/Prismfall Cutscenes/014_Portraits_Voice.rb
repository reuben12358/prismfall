#===============================================================================
# Prismfall Cutscenes - 014 Portraits: voice blips (Audio v4.3 VoiceTicker)
#-------------------------------------------------------------------------------
# While a named character's line types out, a short blip in that character's
# voice ticks along with the letters (Audio/SE/"Voice - <Name>", one file per
# speaker; audio/manifest.tsv installs them).
#
# Who is speaking: the \pf[...] / [portrait: ...] tag of the line, the face a
# cast member carried from an earlier line, or the plain "Name: " label. A line
# with no speaker (narration, signs, system text) never blips.
#
# It is deliberately hard to break:
#   - no file for the speaker         -> silent (nothing is played or logged)
#   - a message window that cannot report its typing position (the selftest
#     stub, other plugins' windows)   -> silent
#   - text shown instantly (text speed "Inst", a skipped line) -> silent
#   - Options > Voice Blips: Off, or VoiceTicker::ENABLED = false -> silent
#   - any error inside the ticker     -> that line goes silent, the message
#     itself is never affected
# Loads after 014_Portraits.rb and wraps its message hook, so the face / bubble
# code is untouched.
#===============================================================================
module Prismfall
  module Portrait
    module VoiceTicker
      ENABLED        = true
      FILE_PREFIX    = "Voice - "
      STRIDE         = 3        # one blip per this many letters
      COOLDOWN       = 0.068    # seconds: never closer together than this
      BURST          = 8        # more letters than this in one frame = shown at once, not typed
      VOLUME         = 70
      PITCH_VARIANCE = 3        # each blip is pitched 100 +/- this
      # Speakers whose blip is another character's file (ids as in Portrait::CAST, values = the name in the file).
      # nil = no voice. Anyone not listed uses their own name: :JUNO -> "Voice - Juno".
      ALIASES = {
        :PLAYER_A => "Player", :PLAYER_B => "Player",
        :ROWAN    => "Mourner"       # the Mourner unmasked keeps the Mourner's voice (cue sheet #11)
      }

      Session = Struct.new(:file, :pos, :count, :time, :dead)

      module_function

      # 0 = on (default), 1 = off: Options > Voice Blips.
      def muted?
        return true if !ENABLED
        return false if !defined?($PokemonSystem) || !$PokemonSystem || !$PokemonSystem.respond_to?(:pf_voice_blips)
        return $PokemonSystem.pf_voice_blips == 1
      rescue StandardError
        return true
      end

      def file?(name)
        return false if name.nil? || name.empty?
        return false if !FileTest.respond_to?(:audio_exist?)
        return FileTest.audio_exist?("Audio/SE/#{FILE_PREFIX}#{name}")
      rescue StandardError
        return false
      end

      # Names to try for a speaker id (:PLAYER_A, :KESTREL) or a "Name: " label ("dr. quent").
      def candidates(who)
        return [] if who.nil?
        if who.is_a?(Symbol)
          return [ALIASES[who]].compact if ALIASES.key?(who)
          base = who.to_s.sub(/_[AB]\z/, "")
          names = [base.split("_").map(&:capitalize).join(" "), base.split("_").last.capitalize]
          shown = (Portrait.display_name(who) rescue nil)
          names += shown.to_s.split(/\s+/).reverse if shown
          return names.uniq
        end
        words = who.to_s.split(/\s+/).map { |w| w.gsub(/[^[:alnum:]'-]/, "") }.reject(&:empty?)
        return [] if words.empty?
        return ([words.map(&:capitalize).join(" "), words.first.capitalize, words.last.capitalize]).uniq
      end

      # "Voice - Juno" for this speaker, or nil. Looked up once per speaker.
      def file_for(who)
        @files ||= {}
        return @files[who] if @files.key?(who)
        name = candidates(who).find { |n| file?(n) }
        return @files[who] = (name) ? "#{FILE_PREFIX}#{name}" : nil
      end

      def forget_files; @files = nil; end   # after installing audio in a running game (debug)

      # The speaker of a raw message (tags still in it): an id Symbol, a label String or nil.
      def speaker_of(message)
        text, spec = Portrait.extract(message)
        spec ||= Portrait.carry(text)
        return spec[:id] if spec && spec[:id]
        return Portrait.label_of(text)
      rescue StandardError
        return nil
      end

      # -> a Session when this line should blip, else nil.
      def start(msgwindow, message)
        return nil if muted?
        return nil if !msgwindow || !msgwindow.respond_to?(:position) || !msgwindow.respond_to?(:busy?)
        return nil if !defined?(pbSEPlay)
        who = speaker_of(message)
        file = file_for(who)
        file ||= file_for(Portrait.label_of(Portrait.extract(message)[0])) if who.is_a?(Symbol)
        return nil if !file
        return Session.new(file, 0, 0, -1.0, false)
      rescue StandardError
        return nil
      end

      # Once a frame while the line is on screen.
      def tick(session, msgwindow)
        return if !session || session.dead
        pos = msgwindow.position.to_i
        delta = pos - session.pos
        session.pos = pos
        return if delta <= 0                       # waiting, paused, or a new page started
        if delta > BURST                           # the rest of the page appeared at once
          session.count = 0
          return
        end
        session.count += delta
        return if session.count < STRIDE
        now = Prismfall::Cutscene::Util.now
        return if now - session.time < COOLDOWN
        session.count = 0
        session.time = now
        pbSEPlay(session.file, VOLUME, 100 + rand(PITCH_VARIANCE * 2 + 1) - PITCH_VARIANCE)
      rescue StandardError => e
        session.dead = true
        Prismfall::Cutscene::Util.log("voice ticker off for this line: #{e.class}: #{e.message}") rescue nil
      end
    end
  end
end

#-------------------------------------------------------------------------------
# Message hook (outside the portrait hook of 014_Portraits.rb).
#-------------------------------------------------------------------------------
if defined?(pbMessageDisplay) && defined?(prismfall_portrait_pbMessageDisplay) && !defined?(prismfall_voice_pbMessageDisplay)
  alias prismfall_voice_pbMessageDisplay pbMessageDisplay

  def pbMessageDisplay(msgwindow, message, letterbyletter = true, commandProc = nil, &block)
    vt = Prismfall::Portrait::VoiceTicker
    voice = (letterbyletter) ? vt.start(msgwindow, message) : nil
    return prismfall_voice_pbMessageDisplay(msgwindow, message, letterbyletter, commandProc, &block) if !voice
    return prismfall_voice_pbMessageDisplay(msgwindow, message, letterbyletter, commandProc) do
      vt.tick(voice, msgwindow)
      block&.call
    end
  end
end

#-------------------------------------------------------------------------------
# Options > Voice Blips (saved with the other options).
#-------------------------------------------------------------------------------
if defined?(PokemonSystem)
  class PokemonSystem
    attr_writer :pf_voice_blips
    def pf_voice_blips; return @pf_voice_blips || 0; end   # 0 = on, 1 = off
  end
end

if defined?(MenuHandlers) && defined?(EnumOption) && defined?(PokemonSystem)
  MenuHandlers.add(:options_menu, :pf_voice_blips, {
    "name"        => _INTL("Voice Blips"),
    "order"       => 35,
    "type"        => EnumOption,
    "parameters"  => [_INTL("On"), _INTL("Off")],
    "description" => _INTL("Choose whether story characters make a short voice sound as they talk."),
    "get_proc"    => proc { next $PokemonSystem.pf_voice_blips },
    "set_proc"    => proc { |value, _scene| $PokemonSystem.pf_voice_blips = value }
  })
end
