#===============================================================================
# Prismfall Base Fixes - 002 glyph fallback for the stock fonts
#-------------------------------------------------------------------------------
# No font the base projects ship (Power Green / Small / Narrow, Power Clear,
# EBDX's "Truth And Ideals") has the em dash, en dash or ₽, and the Power Green
# family has no arrows, so those characters draw as boxes. Our script uses the
# em dash a lot (event text, quest log). Every text path in Essentials and EBDX
# ends in Bitmap#draw_text, and every layout measures with Bitmap#text_size,
# so both swap the missing characters for look-alikes the fonts do have. The
# text itself (maps, PBS, saves) is not changed. Characters the fonts have,
# such as … “ ” ‘ ’ é ♂ ♀, are left alone.
#===============================================================================
module PrismfallGlyphs
  MAP = {
    "—" => "--",   # — em dash
    "―" => "--",   # ― horizontal bar
    "–" => "-",    # – en dash
    "‒" => "-",    # ‒ figure dash
    "−" => "-",    # − minus sign
    "₽" => "$",    # ₽ (Essentials shows money with $)
    "→" => "->",   # →
    "←" => "<-",   # ←
    "↑" => "^",    # ↑
    "↓" => "v",    # ↓
    "„" => "\"",   # „
    "€" => "EUR",  # €
    " " => " ",    # thin space
    " " => " ",    # hair space
    " " => " ",    # narrow no-break space
    "​" => ""      # zero-width space
  }.freeze
  PATTERN = Regexp.union(MAP.keys)

  def self.fix(text)
    return text if !text.is_a?(String) || !text.match?(PATTERN)
    return text.gsub(PATTERN, MAP)
  rescue StandardError   # e.g. a binary string: draw it as it is
    return text
  end
end

class Bitmap
  alias prismfall_glyphs_draw_text draw_text unless method_defined?(:prismfall_glyphs_draw_text)
  alias prismfall_glyphs_text_size text_size unless method_defined?(:prismfall_glyphs_text_size)

  # draw_text(x, y, width, height, text, align) or draw_text(rect, text, align)
  def draw_text(*args)
    i = (args[0].is_a?(Rect)) ? 1 : 4
    args[i] = PrismfallGlyphs.fix(args[i]) if args.length > i
    return prismfall_glyphs_draw_text(*args)
  end

  def text_size(text)
    return prismfall_glyphs_text_size(PrismfallGlyphs.fix(text))
  end
end
