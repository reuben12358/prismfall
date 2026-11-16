#===============================================================================
# Prismfall Bosses - 007 Databox bar pips (EBDX databox or vanilla databox)
#===============================================================================
module Prismfall
  module Bosses
    module UI
      # [filled, total] for a boss battler, or nil.
      def self.pip_info(battler)
        st = Bosses.state_for(battler)
        return nil if !st
        total  = st.bars
        filled = st.bars_left
        filled -= 1 if st.pending == :break
        filled = 0 if st.defeated
        if !PIPS_INCLUDE_CURRENT
          total -= 1
          filled -= 1
        end
        return nil if total <= 1 && PIPS_INCLUDE_CURRENT
        return nil if total <= 0
        return [[filled, 0].max, total]
      end

      def self.graphic
        if @graphic.nil? || (@graphic && @graphic.disposed?)
          @graphic = (defined?(pbResolveBitmap) && pbResolveBitmap(PIP_GRAPHIC)) ? Bitmap.new(PIP_GRAPHIC) : false
        end
        return @graphic || nil
      end

      def self.pip_size
        g = graphic
        return (g) ? [g.width / 2, g.height] : PIP_SIZE
      end

      def self.strip_size(total)
        w, h = pip_size
        return [[total * (w + PIP_GAP) - PIP_GAP, 1].max, h]
      end

      def self.draw_pips(bitmap, x, y, filled, total)
        w, h = pip_size
        g = graphic
        total.times do |i|
          px = x + i * (w + PIP_GAP)
          full = i < filled
          if g
            bitmap.blt(px, y, g, Rect.new((full) ? 0 : w, 0, w, h))
          else
            bitmap.fill_rect(px, y, w, h, Color.new(*PIP_COLORS[:border]))
            bitmap.fill_rect(px + 1, y + 1, w - 2, h - 2, Color.new(*PIP_COLORS[(full) ? :full : :empty]))
          end
        end
      end
    end
  end
end

#-------------------------------------------------------------------------------
# EBDX: an extra sprite in the databox's @sprites hash (so EBDX's own x=/y=/
# opacity=/visible=/dispose loops move, fade and free it), positioned with
# ex/ey relative to the HP bar. Built lazily, so trainer aces sent out later work.
#-------------------------------------------------------------------------------
if defined?(DataBoxEBDX)
  class DataBoxEBDX
    alias prismfall_bosses_refresh refresh unless method_defined?(:prismfall_bosses_refresh)
    def refresh(*args)
      ret = prismfall_bosses_refresh(*args)
      prismfall_bosses_pips(true)
      return ret
    end

    alias prismfall_bosses_update update unless method_defined?(:prismfall_bosses_update)
    def update(*args)
      ret = prismfall_bosses_update(*args)
      prismfall_bosses_pips(false)
      return ret
    end

    def prismfall_bosses_pips(force)
      return if self.disposed? || !@loaded || !@sprites || !@sprites["base"]
      ui   = Prismfall::Bosses::UI
      info = ui.pip_info(@battler)
      return if !force && info == @prismfall_pips_key
      @prismfall_pips_key = info
      spr = @sprites["prismfall_pips"]
      if !info
        spr.bitmap.clear if spr && !spr.disposed? && spr.bitmap
        return
      end
      w, h = ui.strip_size(info[1])
      if !spr || spr.disposed? || !spr.bitmap || spr.bitmap.width < w
        if spr && !spr.disposed?
          spr.bitmap.dispose if spr.bitmap
          spr.dispose
        end
        base = @sprites["base"]
        hp   = @sprites["hp"]
        spr  = Sprite.new(@viewport)
        spr.bitmap = Bitmap.new(w, h)
        ox, oy = Prismfall::Bosses::EBDX_PIP_OFFSET
        if spr.respond_to?(:ex=)
          spr.ex = ((hp && hp.ex) || 0) + ox
          spr.ey = ((hp && hp.ey) || 0) + oy
        end
        spr.x = base.x + ((spr.respond_to?(:ex)) ? spr.ex.to_i : ox)
        spr.y = base.y + ((spr.respond_to?(:ey)) ? spr.ey.to_i : oy)
        spr.z = ((hp) ? hp.z : base.z) + 1
        spr.opacity = base.opacity
        spr.visible = base.visible
        @sprites["prismfall_pips"] = spr
      end
      spr.bitmap.clear
      ui.draw_pips(spr.bitmap, 0, 0, *info)
    end
  end
end

#-------------------------------------------------------------------------------
# Vanilla databox: drawn onto the databox bitmap.
#-------------------------------------------------------------------------------
class Battle::Scene::PokemonDataBox
  alias prismfall_bosses_refresh refresh unless method_defined?(:prismfall_bosses_refresh)
  def refresh
    prismfall_bosses_refresh
    @prismfall_pips_key = Prismfall::Bosses::UI.pip_info(@battler)
    return if !@prismfall_pips_key || !self.bitmap || self.bitmap.disposed?
    x, y = Prismfall::Bosses::VANILLA_PIP_POS
    Prismfall::Bosses::UI.draw_pips(self.bitmap, (@spriteBaseX || 0) + x, y, *@prismfall_pips_key)
  end

  alias prismfall_bosses_update update unless method_defined?(:prismfall_bosses_update)
  def update(*args)
    prismfall_bosses_update(*args)
    refresh if Prismfall::Bosses::UI.pip_info(@battler) != @prismfall_pips_key
  end
end
