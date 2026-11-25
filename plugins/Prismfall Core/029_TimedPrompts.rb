#===============================================================================
# Prismfall Core - 029 Timed prompts, and GO_OVERTIME's countdown
#-------------------------------------------------------------------------------
# story/35_SCRIPT_CH16.md "GO_OVERTIME" (map 406, the Engine Core Chamber):
# three prompts, "Finish copying? (3) / (2) / (1)", Stay or Go. "The prompts time
# out after 3 seconds each as Go (the countdown is real). Rook only warns twice."
# Staying all three times is Prismfall.game_over(:GO_OVERTIME).
#
#   Prismfall.timed_choice("Finish copying?", ["Stay.", "Go."], seconds: 3, default: 1)
#       a normal choice box with a draining bar over it. Returns the index chosen,
#       or `default` when the time runs out (Prismfall::TimedPrompt.timed_out? says
#       which). BACK does nothing: the only way out is to pick, or to wait.
#   pf_timed_choice(...)            the same, for event Script commands
#   pf_overtime_prompt(3)           one of the three prompts -> true if the player STAYED
#   pf_overtime                     the whole scripted sequence (klaxon lines, Rook's
#                                   two warnings, the three prompts) -> :go, or
#                                   :game_over after Prismfall.game_over(:GO_OVERTIME)
#
# Headless tests and the playtest bots answer through
#   Prismfall::TimedPrompt.answers = [0, "Stay.", :timeout]
# (consumed in order; with none left a headless run times out, like a player
# who puts the controller down).
#===============================================================================
module Prismfall
  module TimedPrompt
    DEFAULT_SECONDS = 3.0
    BAR_HEIGHT      = 6
    BAR_COLOR       = [248, 80, 64]
    BAR_BACK        = [40, 40, 48]

    @answers   = []
    @timed_out = false
    @log       = []

    class << self
      attr_accessor :answers
      attr_reader :log

      def timed_out?; return @timed_out; end

      def now
        return System.uptime if defined?(System) && System.respond_to?(:uptime)
        return Process.clock_gettime(Process::CLOCK_MONOTONIC)
      end

      def headless?
        return defined?(Harness) ? true : false
      end

      # Returns the chosen index (default on a timeout).
      def ask(message, commands, seconds: DEFAULT_SECONDS, default: 0)
        labels = commands.map { |c| _INTL(c) }
        default = default.to_i.clamp(0, labels.length - 1)
        @timed_out = false
        ret = nil
        if @answers && !@answers.empty?
          ans = @answers.shift
          if ans == :timeout
            @timed_out = true
            ret = default
          else
            ret = ans.is_a?(Integer) ? ans : labels.index(ans.to_s)
            raise ArgumentError, "Scripted answer #{ans.inspect} not in #{labels.inspect}" if ret.nil? || ret >= labels.length
          end
          pbMessage(message) if headless?   # keep the line in the test transcript
        elsif headless?
          @timed_out = true
          ret = default
        else
          ret = show(message, labels, seconds.to_f, default)
        end
        @log.push([message, labels[ret], @timed_out])
        @log.shift while @log.length > 20
        return ret
      end

      # The real thing: the message box, a command window with nothing preselected to lean on,
      # and a bar that drains over `seconds`.
      def show(message, labels, seconds, default)
        msgwindow = pbCreateMessageWindow
        ret = default
        begin
          ret = pbMessageDisplay(msgwindow, message, true,
                                 proc { |msgwin| next command_loop(msgwin, labels, seconds, default) })
        ensure
          pbDisposeMessageWindow(msgwindow)
          Input.update
        end
        return ret
      end

      def command_loop(msgwindow, labels, seconds, default)
        cmdwindow = Window_CommandPokemonEx.new(labels)
        cmdwindow.z = 99999
        cmdwindow.visible = true
        cmdwindow.resizeToFit(cmdwindow.commands)
        pbPositionNearMsgWindow(cmdwindow, msgwindow, :right)
        cmdwindow.index = 0
        bar = Sprite.new
        bar.z = 99999
        bar.bitmap = Bitmap.new([cmdwindow.width, 16].max, BAR_HEIGHT)
        bar.x = cmdwindow.x
        bar.y = [cmdwindow.y - BAR_HEIGHT - 2, 0].max
        command = default
        start = now
        last_w = nil
        begin
          loop do
            Graphics.update
            Input.update
            cmdwindow.update
            msgwindow&.update
            left = seconds - (now - start)
            if left <= 0
              @timed_out = true
              command = default
              break
            end
            w = ((bar.bitmap.width * left) / seconds).ceil
            if w != last_w
              bar.bitmap.fill_rect(0, 0, bar.bitmap.width, BAR_HEIGHT, Color.new(*BAR_BACK))
              bar.bitmap.fill_rect(0, 0, w, BAR_HEIGHT, Color.new(*BAR_COLOR))
              last_w = w
            end
            if Input.trigger?(Input::USE)
              command = cmdwindow.index
              break
            end
            pbUpdateSceneMap if defined?(pbUpdateSceneMap)
          end
        ensure
          bar.bitmap.dispose
          bar.dispose
          cmdwindow.dispose
        end
        return command
      end
    end
  end

  def self.timed_choice(message, commands, seconds: TimedPrompt::DEFAULT_SECONDS, default: 0)
    return TimedPrompt.ask(message, commands, seconds: seconds, default: default)
  end

  #=============================================================================
  # GO_OVERTIME (Ch16): "We go when the whistle goes, no heroics."
  #=============================================================================
  module Overtime
    SECONDS = 3.0
    STAY = 0
    GO   = 1
    # count => [the speaker line before the prompt, Rook's warning (nil the third time), the page line on Stay]
    BEATS = {
      3 => ["CORE BREACH. CONTAINMENT VENT IN THREE.", "That's the whistle! That's the whistle! No heroics!", "(Page thirty-four.)"],
      2 => ["CONTAINMENT VENT IN TWO.", "I said no heroics! I'm not saying it a third time!", "(Page thirty-eight.)"],
      1 => ["CONTAINMENT VENT IN ONE.", nil, nil]
    }
    OUT_LINE = "You dive through the bulkhead as it slams behind you. Through the porthole: white fire filling " \
               "the chamber, the copier going with it."

    # One prompt. Returns true if the player chose to stay (timeouts go).
    def self.prompt(count)
      idx = Prismfall.timed_choice(_INTL("Finish copying? ({1})", count), [_INTL("Stay."), _INTL("Go.")],
                                   seconds: SECONDS, default: GO)
      return idx == STAY
    end

    def self.say_rook(line)
      if defined?(pf_say) && defined?(Prismfall::Portrait)
        pf_say(:ROOK, :panic, _INTL(line)) rescue pbMessage(_INTL("Rook: {1}", _INTL(line)))
      else
        pbMessage(_INTL("Rook: {1}", _INTL(line)))
      end
    end

    # The whole sequence. Returns :go, or :game_over (after the Game Over screen).
    def self.run
      [3, 2, 1].each do |count|
        speaker, rook, page = BEATS[count]
        pbMessage(_INTL("\"{1}\"", _INTL(speaker)))
        say_rook(rook) if rook
        if !prompt(count)
          pbMessage(_INTL(OUT_LINE))
          return :go
        end
        if count == 1
          Prismfall.game_over(:GO_OVERTIME)
          return :game_over
        end
        pbMessage(_INTL(page)) if page
      end
      return :go
    end
  end
end

def pf_timed_choice(message, commands, seconds: 3.0, default: 0)
  return Prismfall.timed_choice(message, commands, seconds: seconds, default: default)
end
def pf_overtime_prompt(count); return Prismfall::Overtime.prompt(count); end
def pf_overtime;               return Prismfall::Overtime.run;           end
