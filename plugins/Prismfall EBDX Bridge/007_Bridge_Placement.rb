#===============================================================================
# Prismfall EBDX Bridge - battler placement (feet on the base).
#-------------------------------------------------------------------------------
# EBDX anchors every battler at a fixed room point (PBS/EBDX/metrics.txt
# BATTLERPOS: foe 234,152 / player 116,252, room px), and every Prismfall room
# paints its bases centred on those points. EBDX then hangs the sprite from that
# point by its bitmap bottom, shifted by the per-species BattlerEnemyY /
# BattlerPlayerY / BattlerAltitude of the base project's PBS/EBDX/pokemon.txt
# (plus EliteBattle::PLAYER_BACKSPRITE_Y_OFFSET). Those numbers do not describe
# the bundled sprites: for 90% of the 1020 front sprites the lowest opaque row
# lands between 2 px above and 26 px below the anchor (median 14 px below), so
# Pokemon stand in front of, or off, their base; back sprites end 20 px above
# to 8 px below; and "floating" species hover at random heights
# (Bronzong's lowest row is 9 px BELOW the base centre, Golbat's 18 px above).
#
# The project's metric source is now this file: the sprite's own pixels. When
# EBDX loads a battler bitmap, the lowest opaque row of each animation frame is
# measured once (cached per file); the median of those rows is put exactly
# FOOT_LINE px from the anchor. Floating species are lifted a constant HOVER px
# above that line; EBDX's ground shadow (squashed silhouette, 1/8 height) stays
# at the base, so they read as hovering over it. Only the vertical origin
# changes: EBDX's X metric and every animation that saves/restores the origin
# (send-out, recall, legacy animations) keep working.
#
#   FOOT_LINE  bitmap px, + = below the anchor (sprite zoom applies: the foe is
#              drawn at 1x and the player at 2x at the battle camera). Foe +16:
#              its feet a little in front of the base centre (the foe base is
#              25 px deep each way at the battle camera), as a creature standing
#              on a disc seen from above shows its front feet. Player +2: just
#              in front of its (1.5x) base's centre.
#   HOVER      bitmap px above the foot line for floating species
#   FLOATING   species => true/false, wins over the automatic rule
#              (EBDX BattlerAltitude > 0, or Levitate for species EBDX has no
#              metrics for, e.g. the Gen 9 pack's statics)
#   FOOT_TWEAK species => [front_dy, back_dy], extra hand tweak in bitmap px
#
# The ally's spot. EBDX stands the single-battle player Pokemon at room
# (116,252), 33 px below the bottom of the screen at the battle camera; with
# its feet on that point a small ally (Joltik, Bidoof, the starters) showed only
# 69-79% of itself. In Prismfall rooms (whose bases art/battlebacks paints
# around bblib.PLAYER) the point is raised PLAYER_RAISE room px: 18 px at the
# battle camera (84-94% shown), and at the send-out pull-back the ally stands a
# little further into the scene. EBDX's stock rooms keep their own point.
#===============================================================================
module PrismfallEBDX
  GROUND_SPRITES = true
  FOOT_LINE      = { :front => 16, :back => 2 }
  HOVER          = 20
  PLAYER_RAISE   = 8          # room px (EBDX's player point 116,252 -> 116,244 in Prismfall rooms)
  # EBDX gives these an altitude for their animation (a hop, a bounce), but they stand.
  FLOATING = {
    :SKITTY => false, :POLITOED => false, :GROVYLE => false, :KABUTO => false, :FERROTHORN => false,
    :ESCAVALIER => false, :SHELMET => false, :SUNKERN => false, :VICTREEBEL => false, :TIRTOUGA => false,
    :REGICE => false, :PROBOPASS => false
  }
  FOOT_TWEAK = {}

  @ground_cache = {}

  module_function

  # Median over the animation frames of the lowest opaque row, +1 (= the feet line), in bitmap px.
  def sprite_feet(anim)
    return nil if !anim
    file = anim.instance_variable_get(:@bitmapFile)
    frames = anim.instance_variable_get(:@bitmaps) || []
    frames = [anim.bitmap] if frames.empty? && anim.respond_to?(:bitmap) && anim.bitmap
    return nil if frames.empty?
    scale = (anim.respond_to?(:scale) ? anim.scale : 1).to_f
    key = file.is_a?(String) ? [file, scale, frames.length, frames[0].width, frames[0].height] : nil
    return @ground_cache[key] if key && @ground_cache.key?(key)
    step = (scale >= 2 && scale == scale.floor) ? scale.to_i : 1
    picks = frames.length <= 12 ? (0...frames.length).to_a : (0...12).map { |i| (i * (frames.length - 1) / 11.0).round }
    rows = picks.map { |i| lowest_row(frames[i], step) }.compact.sort
    feet = rows.empty? ? nil : rows[rows.length / 2] + 1
    @ground_cache[key] = feet if key
    return feet
  end

  def lowest_row(bmp, step)
    return nil if !bmp || bmp.disposed?
    w, h = bmp.width, bmp.height
    y = h - 1
    while y >= 0
      x = 0
      while x < w
        return y if bmp.get_pixel(x, y).alpha > 40
        x += step
      end
      y -= step
    end
    return nil
  end

  def floating?(species, form = 0)
    return false if species.nil?
    sp = species.to_s.upcase.to_sym
    return FLOATING[sp] if FLOATING.key?(sp)
    alt = (EliteBattle.get_data(species, :Species, :ALTITUDE, form) rescue nil)
    return alt > 0 if alt.is_a?(Numeric)
    data = (GameData::Species.get_species_form(species, form) rescue nil)
    return false if !data
    return (data.abilities + data.hidden_abilities).include?(:LEVITATE)
  end

  # New vertical origin for a DynamicPokemonSprite (nil = leave EBDX's).
  def grounded_oy(anim, species, form, back)
    feet = sprite_feet(anim)
    return nil if !feet
    t = FOOT_LINE[back ? :back : :front]
    t -= HOVER if floating?(species, form)
    tw = FOOT_TWEAK[species.to_s.upcase.to_sym]
    t += (back ? tw[1] : tw[0]) if tw
    return feet - t
  end
end

if defined?(DynamicPokemonSprite) && defined?(EliteBattle)
  class DynamicPokemonSprite
    alias prismfall_refreshMetrics refreshMetrics unless method_defined?(:prismfall_refreshMetrics)
    def refreshMetrics(metrics = nil, species = nil)
      prismfall_refreshMetrics(metrics, species)
      return if !PrismfallEBDX::GROUND_SPRITES || !@pokemon || !@bitmap
      begin
        sp = species.nil? ? @pokemon.species : species
        oy = PrismfallEBDX.grounded_oy(@bitmap, sp, (@pokemon.form rescue 0), @index % 2 == 0)
        return if oy.nil?
        @sprite.oy = oy
        @oy = oy
      rescue StandardError => e
        PrismfallEBDX.log_error("DynamicPokemonSprite#refreshMetrics", e)
      end
    end

    # EBDX rebuilds the origin from its own metrics when a Substitute ends; keep ours.
    alias prismfall_removeSubstitute removeSubstitute unless method_defined?(:prismfall_removeSubstitute)
    def removeSubstitute
      prismfall_removeSubstitute
      return if !PrismfallEBDX::GROUND_SPRITES || @oy.nil?
      @sprite.ox = @ox
      @sprite.oy = @oy
      formatShadow
    end
  end

  class BattleSceneRoom
    # Prismfall rooms (art named field_*) paint the player's base at the raised point (see PLAYER_RAISE).
    alias prismfall_place_adjustMetrics adjustMetrics unless method_defined?(:prismfall_place_adjustMetrics)
    def adjustMetrics
      prismfall_place_adjustMetrics
      return if !PrismfallEBDX::GROUND_SPRITES || PrismfallEBDX::PLAYER_RAISE == 0
      return if !@data.is_a?(Hash) || !@data["prismfall_field"] || !@data["backdrop"].to_s.start_with?("field_")
      return if !@battle || @battle.pbMaxSize > 1
      b = @sprites["battler0"]
      b.ey -= PrismfallEBDX::PLAYER_RAISE if b && b.ey
    rescue StandardError => e
      PrismfallEBDX.log_error("BattleSceneRoom#adjustMetrics", e)
    end
  end

  # Send-out landing: a floating Pokemon doesn't shake the screen (EBDX asks for its altitude).
  if defined?(getBattlerAltitude)
    alias prismfall_getBattlerAltitude getBattlerAltitude unless defined?(prismfall_getBattlerAltitude)
    def getBattlerAltitude(battler)
      return prismfall_getBattlerAltitude(battler) if !PrismfallEBDX::GROUND_SPRITES || battler.nil?
      sp = (battler.displaySpecies rescue nil)
      return prismfall_getBattlerAltitude(battler) if sp.nil?
      return PrismfallEBDX.floating?(sp, (battler.displayForm rescue 0)) ? PrismfallEBDX::HOVER : 0
    end
  end
end
