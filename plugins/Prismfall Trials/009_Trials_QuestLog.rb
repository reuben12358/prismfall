#===============================================================================
# Prismfall Trials - 009 Quest log (pause menu "Quests")
#-------------------------------------------------------------------------------
# Code-drawn like the Ledger (no art needed). Tabs: Active / Done / Rumours.
# Lists Trial quests (with Trial, rank stars and the current step) and the map
# builder's story quests (pfm_quest in Prismfall Maps' 006_MapStory.rb, stored
# in $PokemonGlobal.pf_quests) so there is one quest log.
# Event usage: Script: Prismfall::Trials.show_log
#===============================================================================
module Prismfall
  module Trials
    # [title, detail, tag] rows for a tab (0 active, 1 done, 2 rumours).
    def self.log_rows(tab)
      rows = []
      story = ($PokemonGlobal && $PokemonGlobal.respond_to?(:pf_quests)) ? $PokemonGlobal.pf_quests : {}
      case tab
      when 0
        active_ids.each do |id|
          q = get(id)
          rows.push([_INTL(q[:title]), step_text(id, step(id)) || _INTL(q[:summary].to_s),
                     "#{trial_name(q[:trial])} #{'*' * (q[:rank] || 1)}"])
        end
        story.each { |_k, v| rows.push([_INTL(v[:title].to_s), _INTL(v[:text].to_s), _INTL("Story")]) if !v[:done] }
      when 1
        done_ids.each do |id|
          q = get(id)
          o = outcome(id)
          rows.push([_INTL(q[:title]), _INTL(q[:summary].to_s) + ((o) ? _INTL(" (Outcome: {1})", o.to_s.tr("_", " ")) : ""),
                     trial_name(q[:trial])])
        end
        failed_ids.each { |id| rows.push([_INTL(get(id)[:title]), _INTL("Failed."), trial_name(get(id)[:trial])]) }
        story.each { |_k, v| rows.push([_INTL(v[:title].to_s), _INTL(v[:text].to_s), _INTL("Story")]) if v[:done] }
      else
        BadgeTiers.rumours.reverse.each do |m, b|
          rows.push([BadgeTiers.map_name(m), BadgeTiers.rumour_text(m, b), _INTL("Badge {1}", b)])
        end
        TRIALS.each_key do |t|
          next if points(t) <= 0
          rows.push([trial_name(t), _INTL("Rank: {1} ({2} points).", rank_name(t), points(t)), _INTL("Trial")])
        end
      end
      return rows
    end

    def self.log_any?
      return !store[:quests].empty? || !store[:rumours].empty? ||
             ($PokemonGlobal && $PokemonGlobal.respond_to?(:pf_quests) && !$PokemonGlobal.pf_quests.empty?)
    end

    def self.show_log
      pbFadeOutIn { PrismfallQuestLogScene.new.main }
    end
  end
end

class PrismfallQuestLogScene
  ROWS     = 7
  ROW_H    = 30
  LIST_TOP = 62
  BG       = Color.new(14, 20, 22)
  PANEL    = Color.new(30, 44, 46)
  SELECT   = Color.new(52, 92, 84)
  GOLD     = Color.new(226, 204, 132)
  TEXT     = Color.new(232, 236, 230)
  DIM      = Color.new(120, 140, 136)
  SHADOW   = Color.new(0, 0, 0)
  TABS     = ["Active", "Done", "Rumours"].freeze

  def initialize
    @tab = 0
    @index = [0, 0, 0]
    @top = [0, 0, 0]
  end

  def refresh
    bmp = @overlay.bitmap
    bmp.clear
    w = Graphics.width
    rows = Prismfall::Trials.log_rows(@tab)
    pbSetSystemFont(bmp)
    pbDrawTextPositions(bmp, [[_INTL("QUESTS"), w / 2, 4, :center, GOLD, SHADOW]])
    pbSetSmallFont(bmp)
    tab_w = (w - 32 - 16) / 3
    TABS.each_with_index do |t, i|
      x = 16 + (i * (tab_w + 8))
      bmp.fill_rect(x, 34, tab_w, 24, (i == @tab) ? SELECT : PANEL)
      pbDrawTextPositions(bmp, [[_INTL(t), x + (tab_w / 2), 36, :center, (i == @tab) ? TEXT : DIM, SHADOW]])
    end
    bmp.fill_rect(16, LIST_TOP, w - 32, ROWS * ROW_H, PANEL)
    texts = []
    top = @top[@tab]
    rows[top, ROWS].to_a.each_with_index do |r, i|
      idx = top + i
      y = LIST_TOP + (i * ROW_H)
      bmp.fill_rect(16, y, w - 32, ROW_H, SELECT) if idx == @index[@tab]
      texts.push([r[0], 28, y + 6, :left, TEXT, SHADOW])
      texts.push([r[2].to_s, w - 28, y + 6, :right, DIM, SHADOW])
    end
    texts.push([_INTL("Nothing here yet."), w / 2, LIST_TOP + 6, :center, DIM, SHADOW]) if rows.empty?
    pbDrawTextPositions(bmp, texts)
    box_y = LIST_TOP + (ROWS * ROW_H) + 6
    bmp.fill_rect(16, box_y, w - 32, 72, PANEL)
    sel = rows[@index[@tab]]
    drawFormattedTextEx(bmp, 24, box_y + 4, w - 48, sel[1].to_s, TEXT, SHADOW, 26) if sel
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
      count = Prismfall::Trials.log_rows(@tab).length
      if Input.trigger?(Input::BACK)
        pbPlayCloseMenuSE
        break
      elsif Input.trigger?(Input::LEFT) || Input.trigger?(Input::RIGHT)
        @tab = (@tab + ((Input.trigger?(Input::LEFT)) ? 2 : 1)) % 3
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

MenuHandlers.add(:pause_menu, :prismfall_quests, {
  "name"      => _INTL("Quests"),
  "order"     => 44,
  "condition" => proc { next Prismfall::Trials::QUEST_LOG_IN_PAUSE_MENU && Prismfall::Trials.log_any? },
  "effect"    => proc { |menu|
    pbPlayDecisionSE
    pbFadeOutIn do
      PrismfallQuestLogScene.new.main
      menu.pbRefresh
    end
    next false
  }
})
