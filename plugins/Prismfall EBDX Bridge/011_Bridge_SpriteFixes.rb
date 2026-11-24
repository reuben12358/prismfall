#===============================================================================
# Prismfall EBDX Bridge - 011 sprite fixes (Gemini sprite audit 2026-11-23, Part A.3 bugs 1-3 + altitude)
#-------------------------------------------------------------------------------
# Version-proof guards, so the same kit works on either EBDX build in use
# (ours already uses "Front shiny"; the pf_engine_run base still asks for
# "FrontShiny") and on case-sensitive file systems:
#  1. Shiny static fallback: a lookup under Graphics/Pokemon/FrontShiny or
#     BackShiny that misses retries the v21.1 folders "Front shiny" / "Back shiny".
#  2. Upper-case extensions: a bitmap lookup that misses retries <name>.PNG
#     (29+ Hisuian / Legends statics ship as .PNG; Linux and mkxp-z are
#     case-sensitive). tools/normalize_png_ext.py renames them for good.
#  3. Oversized statics: a single-frame static sprite 160 px or taller (the Gen 9
#     DLC statics are 192 front / 288 back) gets EBDX scale 1 instead of 2 when
#     its species has no SpriteScale of its own, so it isn't drawn at 384-576 px.
#  4. Floaters: Gen 6-9 species EBDX gives BattlerAltitude 0 that hover (no
#     Levitate to catch them) are added to PrismfallEBDX::FLOATING.
#===============================================================================
module PrismfallEBDX
  SPRITE_FIX_SHINY_DIRS = { "Graphics/Pokemon/FrontShiny" => "Graphics/Pokemon/Front shiny",
                            "Graphics/Pokemon/BackShiny"  => "Graphics/Pokemon/Back shiny" }
  OVERSIZED_STATIC_PX = 160

  # Hover over their shadows (EBDX metrics say altitude 0; none has Levitate).
  FLOATING_GEN7_9 = %i[
    PECHARUNT FLUTTERMANE IRONMOTH IRONJUGULIS GHOLDENGO DREEPY DRAKLOAK DRAGAPULT NOIBAT NOIVERN MINIOR
    TAPUKOKO TAPULELE TAPUBULU TAPUFINI COSMOG COSMOEM LUNALA NECROZMA NIHILEGO KARTANA CHIYU
  ]
  FLOATING_GEN7_9.each { |sp| FLOATING[sp] = true if !FLOATING.key?(sp) }

  @png_size_cache = {}

  module_function

  # [width, height] from a PNG header, or nil.
  def png_size(path)
    return nil if !path
    return @png_size_cache[path] if @png_size_cache.key?(path)
    size = nil
    begin
      file = path
      file += ".png" if !File.exist?(file) && File.exist?(file + ".png")
      file += ".PNG" if !File.exist?(file) && File.exist?(path + ".PNG")
      head = File.binread(file, 24) if File.exist?(file)
      size = head[16, 8].unpack("NN") if head && head.length >= 24 && head[1, 3] == "PNG"
    rescue StandardError
      size = nil
    end
    @png_size_cache[path] = size
    return size
  end

  # Scale 1 for an oversized single-frame static sprite (nil = leave EBDX's own value).
  def oversized_static_scale(species, back, form)
    @oversized_cache ||= {}
    key = [species, back, form]
    return @oversized_cache[key] if @oversized_cache.key?(key)
    return (@oversized_cache[key] = oversized_static_scale_uncached(species, back, form))
  end

  def oversized_static_scale_uncached(species, back, form)
    return nil if !defined?(GameData::Species)
    data = (GameData::Species.get_species_form(species, form || 0) rescue nil)
    return nil if !data
    file = (back ? GameData::Species.back_sprite_filename(data.species, data.form)
                 : GameData::Species.front_sprite_filename(data.species, data.form)) rescue nil
    w, h = png_size(file)
    return nil if !w || !h
    return nil if w > h            # a horizontal strip = animated: EBDX's scale is right
    return (h >= OVERSIZED_STATIC_PX) ? 1 : nil
  end
end

# 1 + 2: bitmap lookups.
alias prismfall_spritefix_pbResolveBitmap pbResolveBitmap unless defined?(prismfall_spritefix_pbResolveBitmap)
def pbResolveBitmap(x)
  ret = prismfall_spritefix_pbResolveBitmap(x)
  return ret if ret || !x.is_a?(String)
  PrismfallEBDX::SPRITE_FIX_SHINY_DIRS.each do |bad, good|
    next if !x.start_with?(bad)
    ret = prismfall_spritefix_pbResolveBitmap(good + x[bad.length..-1])
    return ret if ret
  end
  noext = x.sub(/\.(png|PNG)\z/, "")
  upper = noext + ".PNG"
  return upper if !x.end_with?(".png") && File.exist?(upper)
  PrismfallEBDX::SPRITE_FIX_SHINY_DIRS.each do |bad, good|
    next if !noext.start_with?(bad)
    alt = good + noext[bad.length..-1] + ".PNG"
    return alt if File.exist?(alt)
  end
  return nil
end

# 3: EBDX's per-species scale.
if defined?(EliteBattle) && EliteBattle.respond_to?(:get_data)
  module EliteBattle
    class << self
      alias prismfall_spritefix_get_data get_data unless method_defined?(:prismfall_spritefix_get_data)
      def get_data(const, mod, key = nil, variant = 0, ext = 0)
        ret = prismfall_spritefix_get_data(const, mod, key, variant, ext)
        if ret.nil? && mod == :Species && (key == :SCALE || key == :BACKSCALE) && const.is_a?(Symbol)
          ret = PrismfallEBDX.oversized_static_scale(const, key == :BACKSCALE, variant)
        end
        return ret
      end
    end
  end
end
