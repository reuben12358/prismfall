#===============================================================================
# Prismfall Core - 007 Trainer Card: 18 badges in 2 rows of 9
#-------------------------------------------------------------------------------
# The vanilla card draws 8 badges per region at y=310. We keep the vanilla
# text drawing (alias-chained), suppress only its badge row, then draw all 18
# badges using Prismfall::TrainerCardLayout (001_Config.rb).
#
# Art (see design/SYSTEMS.md):
#   Graphics/UI/Trainer Card/icon_badges_18.png  288x64 (9 cols x 2 rows, 32x32)
#   Graphics/UI/Trainer Card/icon_badge_slot.png 32x32 (optional empty slot)
#   Graphics/UI/Trainer Card/card.png / card_f.png 512x384 with a badge strip
#     at x 56-456, y 286-372 (optional; layout works on the vanilla card too)
#===============================================================================
module Prismfall
  module TrainerCard
    module_function

    # Source rect [file, src_x, src_y] for badge index i (0-17), or nil.
    def badge_source(i)
      layout = Prismfall::TrainerCardLayout
      size = layout::ICON_SIZE
      if pbResolveBitmap(layout::SHEET)
        return [layout::SHEET, (i % layout::COLS) * size, (i / layout::COLS) * size]
      elsif pbResolveBitmap(layout::SHEET_FALLBACK)
        return [layout::SHEET_FALLBACK, (i % 8) * size, (i / 8) * size]
      end
      return nil
    end

    def slot_position(i)
      layout = Prismfall::TrainerCardLayout
      col = i % layout::COLS
      row = i / layout::COLS
      return [layout::ORIGIN_X + (col * layout::SPACING_X), layout::ORIGIN_Y + (row * layout::SPACING_Y)]
    end

    def draw_badges(bitmap)
      return if !bitmap || !$player
      layout = Prismfall::TrainerCardLayout
      size = layout::ICON_SIZE
      frame_exists = pbResolveBitmap(layout::SLOT_FRAME) ? true : false
      empty_color = Color.new(*layout::EMPTY_SLOT_COLOR)
      images = []
      Prismfall::BADGE_COUNT.times do |i|
        x, y = slot_position(i)
        owned = $player.badges[i] == true
        if layout::DRAW_EMPTY_SLOTS
          if frame_exists
            images.push([layout::SLOT_FRAME, x, y, 0, 0, size, size])
          elsif !owned
            bitmap.fill_rect(x + 2, y + 2, size - 4, size - 4, empty_color)
          end
        end
        next if !owned
        src = badge_source(i)
        next if !src
        images.push([src[0], x, y, src[1], src[2], size, size])
      end
      pbDrawImagePositions(bitmap, images)
    end
  end
end

class PokemonTrainerCard_Scene
  alias __prismfall_core_pbDrawTrainerCardFront pbDrawTrainerCardFront unless method_defined?(:__prismfall_core_pbDrawTrainerCardFront)

  def pbDrawTrainerCardFront
    @prismfall_hide_vanilla_badges = true
    begin
      __prismfall_core_pbDrawTrainerCardFront
    ensure
      @prismfall_hide_vanilla_badges = false
    end
    Prismfall::TrainerCard.draw_badges(@sprites["overlay"].bitmap)
  end

  # The vanilla method reads badges at index i + (region * 8). While it runs,
  # report a region far beyond the badge array so it draws none; everything
  # else (text, sprites) is untouched. Outside that call this defers to the
  # global pbGetCurrentRegion.
  def pbGetCurrentRegion(default = -1)
    return 1_000_000 if @prismfall_hide_vanilla_badges
    return super
  end
  private :pbGetCurrentRegion
end
