#===============================================================================
# Prismfall Core - 019 Ledger viewer (code-drawn; no art needed)
#-------------------------------------------------------------------------------
# Event usage: Script: Prismfall::Ledger.show
# Also in the pause menu once the Ledger has any entry (LEDGER_IN_PAUSE_MENU).
# LEFT/RIGHT switch tabs, UP/DOWN select, BACK closes. Unfound entries are "???".
#===============================================================================
module Prismfall
  module Ledger
    LEDGER_IN_PAUSE_MENU = true

    def self.any?
      return !data[:game_overs].empty? || !data[:endings].empty?
    end

    def self.show
      pbFadeOutIn do
        scene = PrismfallLedgerScene.new
        scene.main
      end
    end
  end
end

class PrismfallLedgerScene
  ROWS       = 7
  ROW_H      = 30
  LIST_TOP   = 62
  BG         = Color.new(18, 14, 24)
  PANEL      = Color.new(40, 32, 52)
  SELECT     = Color.new(92, 56, 72)
  GOLD       = Color.new(232, 196, 120)
  TEXT       = Color.new(232, 228, 240)
  DIM        = Color.new(120, 112, 136)
  SHADOW     = Color.new(0, 0, 0)

  def initialize
    @tab = 0
    @index = [0, 0]
    @top = [0, 0]
  end

  def entries(tab)
    if tab == 0
      reg = Prismfall::Narrative::GAME_OVERS
      return reg.keys.map do |id|
        d = reg[id]
        [id, Prismfall::Ledger.game_over_found?(id), d[:title], d[:epitaph], d[:hint]]
      end
    end
    reg = Prismfall::Narrative::ENDINGS
    return reg.keys.map do |id|
      d = reg[id]
      [id, Prismfall::Ledger.ending_seen?(id), d[:name], _INTL("Kind: {1}", d[:kind].to_s.capitalize), nil]
    end
  end

  def refresh
    bmp = @overlay.bitmap
    bmp.clear
    w = Graphics.width
    list = entries(@tab)
    found = list.count { |e| e[1] }
    # Header + tabs
    pbSetSystemFont(bmp)
    pbDrawTextPositions(bmp, [[_INTL("THE LEDGER"), w / 2, 4, :center, GOLD, SHADOW]])
    pbSetSmallFont(bmp)
    tabs = [_INTL("Game Overs"), _INTL("Endings")]
    tabs.each_with_index do |t, i|
      x = (i == 0) ? 16 : w / 2 + 8
      bmp.fill_rect(x, 34, (w / 2) - 24, 24, (i == @tab) ? SELECT : PANEL)
      pbDrawTextPositions(bmp, [[t, x + ((w / 2) - 24) / 2, 36, :center, (i == @tab) ? TEXT : DIM, SHADOW]])
    end
    # Rows
    bmp.fill_rect(16, LIST_TOP, w - 32, ROWS * ROW_H, PANEL)
    texts = []
    top = @top[@tab]
    list[top, ROWS].to_a.each_with_index do |e, i|
      idx = top + i
      y = LIST_TOP + (i * ROW_H)
      bmp.fill_rect(16, y, w - 32, ROW_H, SELECT) if idx == @index[@tab]
      label = (e[1]) ? _INTL(e[2].to_s) : "???"
      texts.push([sprintf("%02d", idx + 1), 28, y + 6, :left, DIM, SHADOW])
      texts.push([label, 64, y + 6, :left, (e[1]) ? TEXT : DIM, SHADOW])
    end
    pbDrawTextPositions(bmp, texts)
    # Detail box
    sel = list[@index[@tab]]
    box_y = LIST_TOP + (ROWS * ROW_H) + 6
    bmp.fill_rect(16, box_y, w - 32, 72, PANEL)
    if sel
      detail = if sel[1]
                 _INTL(sel[3].to_s)
               elsif sel[4] && Prismfall::Narrative::LEDGER_SHOW_HINTS
                 _INTL("Not yet found. ({1})", _INTL(sel[4].to_s))
               else
                 _INTL("Not yet found.")
               end
      drawFormattedTextEx(bmp, 24, box_y + 4, w - 48, detail, TEXT, SHADOW, 26)
    end
    # Footer
    pbSetSmallFont(bmp)
    ruin = (Prismfall::Ledger.ruin_unlocked?) ? _INTL("Ruin Route: unlocked") : _INTL("Ruin Route: locked")
    pbDrawTextPositions(bmp, [
      [_INTL("Found {1}/{2}", found, list.length), 20, Graphics.height - 26, :left, TEXT, SHADOW],
      [ruin, w - 20, Graphics.height - 26, :right, (Prismfall::Ledger.ruin_unlocked?) ? GOLD : DIM, SHADOW]
    ])
  end

  def main
    @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
    @viewport.z = 99999
    @bg = ColoredPlane.new(BG, @viewport)
    @overlay = BitmapSprite.new(Graphics.width, Graphics.height, @viewport)
    refresh
    loop do
      Graphics.update
      Input.update
      count = entries(@tab).length
      if Input.trigger?(Input::BACK)
        pbPlayCloseMenuSE
        break
      elsif Input.trigger?(Input::LEFT) || Input.trigger?(Input::RIGHT)
        @tab = 1 - @tab
        pbPlayCursorSE
        refresh
      elsif (Input.repeat?(Input::UP) || Input.repeat?(Input::DOWN)) && count > 0
        @index[@tab] = (@index[@tab] + ((Input.repeat?(Input::UP)) ? -1 : 1)) % count
        @top[@tab] = @index[@tab] if @index[@tab] < @top[@tab]
        @top[@tab] = @index[@tab] - ROWS + 1 if @index[@tab] >= @top[@tab] + ROWS
        pbPlayCursorSE
        refresh
      end
    end
    @overlay.dispose
    @bg.dispose
    @viewport.dispose
  end
end

MenuHandlers.add(:pause_menu, :prismfall_ledger, {
  "name"      => _INTL("Ledger"),
  "order"     => 45,
  "condition" => proc { next Prismfall::Ledger::LEDGER_IN_PAUSE_MENU && Prismfall::Ledger.any? },
  "effect"    => proc { |menu|
    pbPlayDecisionSE
    pbFadeOutIn do
      PrismfallLedgerScene.new.main
      menu.pbRefresh
    end
    next false
  }
})
