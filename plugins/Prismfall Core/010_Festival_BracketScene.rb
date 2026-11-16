#===============================================================================
# Prismfall Core - 010 Festival bracket display (drawn in code, no art needed)
#-------------------------------------------------------------------------------
# Event usage: Script: Prismfall::Festival.show_bracket
# Optional background: Graphics/UI/Prismfall/festival_bracket_bg.png (512x384);
# a flat colour is used if it's missing.
# Layout: R16 names on the left/right edges, connector lines meeting in a
# centre "Final" box. Winning paths are gold, eliminated paths grey, the
# player's live path blue.
#===============================================================================
class PrismfallFestivalBracketScene
  LEAF_W      = 100
  LEAF_H      = 24
  ROW_SPACING = 40
  TOP         = 40
  EDGE        = 4
  COL_STEP    = 22
  LINE_W      = 2
  CENTER_W    = 128
  CENTER_H    = 48
  BG_COLOR      = Color.new(22, 26, 44)
  LEAF_BG       = Color.new(44, 50, 78)
  LEAF_BG_PLAYER = Color.new(36, 72, 120)
  WIN_COLOR     = Color.new(248, 208, 96)
  LOSE_COLOR    = Color.new(72, 76, 96)
  PENDING_COLOR = Color.new(150, 156, 180)
  PLAYER_COLOR  = Color.new(96, 176, 248)
  TEXT_BASE     = Color.new(240, 240, 248)
  TEXT_DIM      = Color.new(128, 130, 150)
  TEXT_SHADOW   = Color.new(16, 16, 28)

  def pbUpdate
    pbUpdateSpriteHash(@sprites)
  end

  def pbStartScene
    @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
    @viewport.z = 99999
    @sprites = {}
    addBackgroundOrColoredPlane(@sprites, "bg", "Prismfall/festival_bracket_bg", BG_COLOR, @viewport)
    @sprites["overlay"] = BitmapSprite.new(Graphics.width, Graphics.height, @viewport)
    draw_bracket
    pbFadeInAndShow(@sprites) { pbUpdate }
  end

  def pbMain
    loop do
      Graphics.update
      Input.update
      pbUpdate
      break if Input.trigger?(Input::BACK) || Input.trigger?(Input::USE)
    end
    pbPlayCloseMenuSE
  end

  def pbEndScene
    pbFadeOutAndHide(@sprites) { pbUpdate }
    pbDisposeSpriteHash(@sprites)
    @viewport.dispose
  end

  #-----------------------------------------------------------------------------
  # Geometry
  #-----------------------------------------------------------------------------
  def width;  return Graphics.width;  end
  def height; return Graphics.height; end

  def leaf_left?(slot); return slot < Prismfall::Festival::BRACKET_SIZE / 2; end

  def leaf_x(slot)
    return (leaf_left?(slot)) ? EDGE : width - EDGE - LEAF_W
  end

  def leaf_top(slot)
    return TOP + ((slot % (Prismfall::Festival::BRACKET_SIZE / 2)) * ROW_SPACING)
  end

  def leaf_anchor(slot)   # where the connector line leaves the name box
    x = (leaf_left?(slot)) ? EDGE + LEAF_W : width - EDGE - LEAF_W
    return [x, leaf_top(slot) + (LEAF_H / 2)]
  end

  def node_left?(r, m)
    return m < Prismfall::Festival.matches_in_round(r) / 2
  end

  def node_x(r, m)
    off = EDGE + LEAF_W + 12 + (r * COL_STEP)
    return (node_left?(r, m)) ? off : width - off
  end

  def node_y(r, m)
    if r == 0
      return (leaf_anchor(2 * m)[1] + leaf_anchor((2 * m) + 1)[1]) / 2
    end
    return (node_y(r - 1, 2 * m) + node_y(r - 1, (2 * m) + 1)) / 2
  end

  def center_rect
    cx = (width - CENTER_W) / 2
    cy = node_y(2, 0) - (CENTER_H / 2)
    return [cx, cy, CENTER_W, CENTER_H]
  end

  #-----------------------------------------------------------------------------
  # Drawing helpers
  #-----------------------------------------------------------------------------
  def hline(bmp, x1, x2, y, color)
    x1, x2 = x2, x1 if x2 < x1
    bmp.fill_rect(x1, y - (LINE_W / 2), x2 - x1 + LINE_W, LINE_W, color)
  end

  def vline(bmp, x, y1, y2, color)
    y1, y2 = y2, y1 if y2 < y1
    bmp.fill_rect(x - (LINE_W / 2), y1, LINE_W, y2 - y1 + LINE_W, color)
  end

  def fit_text(bmp, text, max_w)
    text = text.to_s
    return text if bmp.text_size(text).width <= max_w
    while text.length > 1 && bmp.text_size(text + ".").width > max_w
      text = text[0, text.length - 1]
    end
    return text + "."
  end

  # Colour of the segment that carries `entrant` into match (r, m).
  def segment_color(entrant, r, m)
    w = Prismfall::Festival.winner(r, m)
    return PENDING_COLOR if entrant.nil?
    if w.nil?
      return (entrant == :PLAYER) ? PLAYER_COLOR : PENDING_COLOR
    end
    return LOSE_COLOR if w != entrant
    return (entrant == :PLAYER) ? PLAYER_COLOR : WIN_COLOR
  end

  def draw_bracket
    fe  = Prismfall::Festival
    bmp = @sprites["overlay"].bitmap
    bmp.clear
    # Title
    pbSetSystemFont(bmp)
    pbDrawTextPositions(bmp, [[_INTL("FESTIVAL OF CHAMPIONS"), width / 2, 6, :center, WIN_COLOR, TEXT_SHADOW]])
    pbSetSmallFont(bmp)
    # Connectors: rounds 0-2 (both halves)
    3.times do |r|
      fe.matches_in_round(r).times do |m|
        xn = node_x(r, m)
        yn = node_y(r, m)
        a, b = fe.participants(r, m)
        children = (r == 0) ? [leaf_anchor(2 * m), leaf_anchor((2 * m) + 1)] :
                              [[node_x(r - 1, 2 * m), node_y(r - 1, 2 * m)],
                               [node_x(r - 1, (2 * m) + 1), node_y(r - 1, (2 * m) + 1)]]
        [[a, children[0]], [b, children[1]]].each do |entrant, pos|
          color = segment_color(entrant, r, m)
          hline(bmp, pos[0], xn, pos[1], color)
          vline(bmp, xn, pos[1], yn, color)
        end
      end
    end
    # Final connectors + centre box
    cx, cy, cw, ch = center_rect
    fa, fb = fe.participants(3, 0)
    hline(bmp, node_x(2, 0), cx, node_y(2, 0), segment_color(fa, 3, 0))
    hline(bmp, node_x(2, 1), cx + cw, node_y(2, 1), segment_color(fb, 3, 0))
    champ = fe.winner(3, 0)
    bmp.fill_rect(cx, cy, cw, ch, (champ) ? WIN_COLOR : PENDING_COLOR)
    bmp.fill_rect(cx + 2, cy + 2, cw - 4, ch - 4, LEAF_BG)
    label = (champ) ? _INTL("CHAMPION") : _INTL("FINAL")
    line2 = (champ) ? fe.display_name(champ) :
                      _INTL("{1} vs {2}", (fa) ? fe.display_name(fa) : "?", (fb) ? fe.display_name(fb) : "?")
    pbDrawTextPositions(bmp, [
      [label, cx + (cw / 2), cy + 3, :center, WIN_COLOR, TEXT_SHADOW],
      [fit_text(bmp, line2, cw - 8), cx + (cw / 2), cy + 23, :center, TEXT_BASE, TEXT_SHADOW]
    ])
    # Entrant name boxes
    texts = []
    fe::BRACKET.each_with_index do |id, slot|
      x = leaf_x(slot)
      y = leaf_top(slot)
      out = !fe.eliminated_in(id).nil?
      bg = (id == :PLAYER) ? LEAF_BG_PLAYER : LEAF_BG
      bmp.fill_rect(x, y, LEAF_W, LEAF_H, (out) ? LOSE_COLOR : bg)
      bmp.fill_rect(x + 1, y + 1, LEAF_W - 2, LEAF_H - 2, bg) if !out
      name = fit_text(bmp, fe.display_name(id), LEAF_W - 8)
      texts.push([name, x + 4, y + 3, :left, (out) ? TEXT_DIM : TEXT_BASE, TEXT_SHADOW])
    end
    # Status line
    texts.push([status_text, width / 2, height - 28, :center, TEXT_BASE, TEXT_SHADOW])
    pbDrawTextPositions(bmp, texts)
  end

  def status_text
    fe = Prismfall::Festival
    return _INTL("The Festival hasn't begun.") if !fe.started?
    if fe.finished?
      return _INTL("Festival complete. Sovereign: {1}", fe.display_name(:PLAYER))
    end
    st = fe.current_stage
    return "" if !st
    return _INTL("Next: {1} vs {2}", _INTL(st[:name]), fe.current_opponent_name)
  end
end

module Prismfall
  module Festival
    def self.show_bracket
      pbFadeOutIn do
        scene = PrismfallFestivalBracketScene.new
        scene.pbStartScene
        scene.pbMain
        scene.pbEndScene
      end
    end
  end
end
