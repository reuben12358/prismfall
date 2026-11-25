#===============================================================================
# Prismfall Core - 017 Story game overs + checkpoints
#-------------------------------------------------------------------------------
#   Prismfall.game_over(:GO_LAST_FERRY)   - call from a map/common event
#   Prismfall.checkpoint                  - autosave before a risky scene
# The game over screen is drawn in code (dark fade, title, epitaph, Ledger
# note), records the ID in the Ledger, then returns to the title screen or
# reloads the last save. Uses the vanilla "Return to Title" flag, so the map
# scene shuts down cleanly. Don't call it from inside a battle: use
# setBattleRule("canLose") and call it after the battle returns false.
#===============================================================================
module Prismfall
  module GameOver
    GAME_OVER_ME   = "Prismfall game over"   # Audio/ME; nil = silence (a missing file is silent too)
    FADE_SECONDS   = 1.2
    TITLE_COLOR    = Color.new(200, 56, 64)
    TEXT_COLOR     = Color.new(224, 220, 232)
    DIM_COLOR      = Color.new(140, 136, 156)
    SHADOW_COLOR   = Color.new(0, 0, 0)

    class << self
      attr_accessor :pending_reload
    end

    def self.data_for(id)
      d = Prismfall::Narrative::GAME_OVERS[id]
      Prismfall::Narrative.warn("Unregistered game over #{id.inspect}") if !d
      return d || { :title => id.to_s, :epitaph => "" }
    end

    # Returns only if the player is sent back (always true); the map scene then
    # closes on the next frame.
    def self.trigger(id, can_reload = true)
      id = Prismfall::Ledger.canonical_game_over(id)
      data = data_for(id)
      first = Prismfall::Ledger.record_game_over(id)
      EventHandlers.trigger(:prismfall_game_over, id, first)
      pbBGMFade(1.0)
      pbBGSFade(1.0)
      me = data[:me] || GAME_OVER_ME
      pbMEPlay(me) if me
      reload = can_reload && SaveData.exists?
      choice = PrismfallGameOverScene.new(id, data, first, reload).main
      self.pending_reload = (choice == :reload)
      pbMapInterpreter.command_end if pbMapInterpreterRunning?
      $game_temp.title_screen_calling = true
      return true
    end
  end

  def self.game_over(id, can_reload = true)
    return GameOver.trigger(id, can_reload)
  end

  # Saves the game (like the Save menu) so a game over can reload right here.
  # Event usage: Script: Prismfall.checkpoint   (place it before the risky
  # scene's trigger, not inside an autorun event that would re-run on load)
  def self.checkpoint(show_message = true)
    return false if $game_temp.in_battle || !$game_system
    return false if defined?(Prismfall::Passwords) && Prismfall::Passwords.active?(:NO_MERCY)   # 'nomercy'

    ok = Game.save
    if show_message
      pbMessage((ok) ? _INTL("\\se[]Progress saved.") : _INTL("\\se[GUI save choice]Save failed."))
    end
    return ok
  end
end

#===============================================================================
# The code-drawn screen
#===============================================================================
class PrismfallGameOverScene
  def initialize(id, data, first_time, can_reload)
    @id = id
    @data = data
    @first_time = first_time
    @can_reload = can_reload
  end

  def wait_fade(sprites, from, to, seconds)
    start = System.uptime
    loop do
      t = [(System.uptime - start) / seconds, 1.0].min
      sprites.each { |s| s.opacity = from + ((to - from) * t) }
      Graphics.update
      Input.update
      break if t >= 1.0
    end
  end

  def draw_text(bmp)
    w = Graphics.width
    gm = Prismfall::GameOver
    pbSetSmallFont(bmp)
    pbDrawTextPositions(bmp, [[_INTL("GAME OVER"), w / 2, 70, :center, gm::DIM_COLOR, gm::SHADOW_COLOR]])
    pbSetSystemFont(bmp)
    bmp.font.size = 40
    pbDrawTextPositions(bmp, [[_INTL(@data[:title].to_s), w / 2, 96, :center, gm::TITLE_COLOR, gm::SHADOW_COLOR]])
    pbSetSystemFont(bmp)
    epitaph = _INTL(@data[:epitaph].to_s)
    drawFormattedTextEx(bmp, 48, 160, w - 96, "<ac>" + epitaph + "</ac>", gm::TEXT_COLOR, gm::SHADOW_COLOR) if !epitaph.empty?
    pbSetSmallFont(bmp)
    found, total = Prismfall::Ledger.ruin_progress
    note = (@first_time) ? _INTL("A new entry was written in the Ledger. ({1}/{2})", found, total) :
                           _INTL("Ledger: {1}/{2}", found, total)
    pbDrawTextPositions(bmp, [[note, w / 2, 262, :center, gm::DIM_COLOR, gm::SHADOW_COLOR]])
  end

  def draw_options(bmp, index, options)
    gm = Prismfall::GameOver
    bmp.fill_rect(0, 296, Graphics.width, 80, Color.new(0, 0, 0))
    pbSetSystemFont(bmp)
    texts = []
    options.each_with_index do |opt, i|
      label = (i == index) ? "> " + opt[1] + " <" : opt[1]
      texts.push([label, Graphics.width / 2, 300 + (i * 34), :center,
                  (i == index) ? gm::TEXT_COLOR : gm::DIM_COLOR, gm::SHADOW_COLOR])
    end
    pbDrawTextPositions(bmp, texts)
  end

  # Returns :reload or :title.
  def main
    viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
    viewport.z = 999_999
    bg = ColoredPlane.new(Color.new(0, 0, 0), viewport)
    bg.opacity = 0
    text = BitmapSprite.new(Graphics.width, Graphics.height, viewport)
    text.opacity = 0
    draw_text(text.bitmap)
    wait_fade([bg], 0, 255, Prismfall::GameOver::FADE_SECONDS)
    wait_fade([text], 0, 255, Prismfall::GameOver::FADE_SECONDS)
    options = []
    options.push([:reload, _INTL("Load last save")]) if @can_reload
    options.push([:title, _INTL("Return to title")])
    index = 0
    draw_options(text.bitmap, index, options)
    loop do
      Graphics.update
      Input.update
      if Input.trigger?(Input::UP) || Input.trigger?(Input::DOWN)
        index = (index + ((Input.trigger?(Input::UP)) ? -1 : 1)) % options.length
        pbPlayCursorSE
        draw_options(text.bitmap, index, options)
      elsif Input.trigger?(Input::USE)
        pbPlayDecisionSE
        break
      end
    end
    Graphics.freeze   # keep the black screen until the next scene transitions in
    text.dispose
    bg.dispose
    viewport.dispose
    return options[index][0]
  end
end

#===============================================================================
# "Load last save" after a game over: the title call is redirected once.
#===============================================================================
class PrismfallReloadScene
  def main
    save_data = {}
    begin
      save_data = SaveData.read_from_file(SaveData::FILE_PATH) if SaveData.exists?
    rescue StandardError
      save_data = {}
    end
    if save_data.is_a?(Hash) && !save_data.empty? && SaveData.valid?(save_data)
      Game.load(save_data)
    else
      $scene = __prismfall_core_pbCallTitle
    end
  end
end

alias __prismfall_core_pbCallTitle pbCallTitle unless defined?(__prismfall_core_pbCallTitle)
def pbCallTitle
  if Prismfall::GameOver.pending_reload
    Prismfall::GameOver.pending_reload = false
    return PrismfallReloadScene.new
  end
  return __prismfall_core_pbCallTitle
end
