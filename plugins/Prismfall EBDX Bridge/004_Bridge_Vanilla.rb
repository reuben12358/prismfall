#===============================================================================
# Prismfall EBDX Bridge - vanilla Essentials fallback (no EBDX)
#-------------------------------------------------------------------------------
# Field Effects' apply_battle_rule already sets battle.backdrop to the field's
# :backdrop when Graphics/Battlebacks/<backdrop>_bg exists. This file:
#   * remembers the pre-field backdrop/base (to restore on change to :NONE),
#   * makes a field backdrop use its own <backdrop>_base0/_base1 instead of the
#     map environment's base (e.g. "grass"), and
#   * swaps bg/bases/message bar live on :prismfall_field_changed with a fade.
# Uses only Essentials v21.1 Battle::Scene members (verified in
# 011_Battle/004_Scene/002_Scene_Initialize.rb#pbCreateBackdropSprites).
# Note: meta.txt Requires EBDX (SPINE). To run without EBDX, replace the line
# "Requires = Elite Battle: DX,1.4.7" with "Optional = Elite Battle: DX,1.4.7".
#===============================================================================
module PrismfallEBDX
  module Vanilla
    module_function

    def remember_default(battle)
      return if !battle.respond_to?(:backdrop)
      return if battle.instance_variable_defined?(:@prismfall_default_backdrop)
      battle.instance_variable_set(:@prismfall_default_backdrop, [battle.backdrop, battle.backdropBase])
    end

    def default_for(battle)
      d = battle.instance_variable_get(:@prismfall_default_backdrop)
      return d if d.is_a?(Array)
      return ["indoor1", nil]
    end

    def resolve(path)
      return pbResolveBitmap(path) ? true : false
    end

    # [backdrop, base] to use for the battle's current field (nil = no art).
    def field_pair(battle)
      id = PrismfallEBDX.current_field(battle)
      return default_for(battle) if id == :NONE
      bd = PrismfallEBDX.backdrop_name(id, PrismfallEBDX.current_stage(battle))
      return nil if !resolve(VANILLA_DIR + bd + "_bg")
      base = resolve(VANILLA_DIR + bd + "_base0") ? nil : battle.backdropBase
      return [bd, base]
    end

    # Same filename rules as Battle::Scene#pbCreateBackdropSprites.
    def filenames(backdrop, base_name, time_id)
      time = { 1 => "eve", 2 => "night" }[time_id]
      bg_file = backdrop
      base_file = base_name ? sprintf("%s_%s", backdrop, base_name) : backdrop
      msg_file = backdrop
      if time
        try = sprintf("%s_%s", bg_file, time)
        bg_file = try if resolve(VANILLA_DIR + try + "_bg")
        try = sprintf("%s_%s", base_file, time)
        base_file = try if resolve(VANILLA_DIR + try + "_base0")
        try = sprintf("%s_%s", msg_file, time)
        msg_file = try if resolve(VANILLA_DIR + try + "_message")
      end
      if !resolve(VANILLA_DIR + base_file + "_base0") && base_name
        base_file = base_name
        try = time ? sprintf("%s_%s", base_file, time) : nil
        base_file = try if try && resolve(VANILLA_DIR + try + "_base0")
      end
      return [VANILLA_DIR + bg_file + "_bg", VANILLA_DIR + base_file + "_base0",
              VANILLA_DIR + base_file + "_base1", VANILLA_DIR + msg_file + "_message"]
    end

    def swap(scene, battle, old_id, new_id)
      sig = PrismfallEBDX.signature(battle)
      return if scene.instance_variable_get(:@prismfall_signature) == sig
      pair = field_pair(battle)
      return if !pair
      files = filenames(pair[0], pair[1], battle.time)
      return if !resolve(files[0])
      sprites = scene.sprites
      fade = nil
      trans = LIVE_TRANSITIONS ? PrismfallEBDX.transition_for(old_id, PrismfallEBDX.current_field(battle)) : nil
      trans = [255, 255, 255] if trans.is_a?(Symbol)   # EBDX animations don't exist here
      if trans.is_a?(Array) && scene.respond_to?(:viewport) && scene.viewport
        fade = Sprite.new(scene.viewport)
        fade.bitmap = Bitmap.new(Graphics.width, Graphics.height)
        fade.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, PrismfallEBDX.to_color(trans))
        fade.z = 2          # above bg (0) and bases (1), below trainers/Pokémon
        fade.opacity = 0
        fade_step(scene, fade, 0, 255)
      end
      battle.backdrop = pair[0]
      battle.backdropBase = pair[1]
      ["battle_bg", "battle_bg2"].each { |k| sprites[k]&.setBitmap(files[0]) }
      2.times do |side|
        base = sprites["base_#{side}"]
        next if !base
        if resolve(files[1 + side])
          base.setBitmap(files[1 + side])
          base.visible = true
          if base.bitmap
            base.ox = base.bitmap.width / 2
            base.oy = (side == 0) ? base.bitmap.height : base.bitmap.height / 2
          end
        else
          base.visible = false
        end
      end
      sprites["cmdBar_bg"]&.setBitmap(files[3]) if resolve(files[3])
      scene.instance_variable_set(:@prismfall_signature, sig)
      if fade
        fade_step(scene, fade, 255, 0)
        fade.bitmap.dispose
        fade.dispose
      end
      PrismfallEBDX.log("Vanilla backdrop swapped to #{pair.inspect}")
    end

    def fade_step(scene, sprite, from, to)
      duration = VANILLA_FADE_TIME.to_f
      start = System.uptime
      loop do
        t = [(System.uptime - start) / duration, 1.0].min
        sprite.opacity = from + ((to - from) * t)
        if scene.respond_to?(:pbGraphicsUpdate)
          scene.pbGraphicsUpdate
          scene.pbFrameUpdate if scene.respond_to?(:pbFrameUpdate)
        else
          Graphics.update
        end
        break if t >= 1.0
      end
    end
  end
end

#===============================================================================
# Hooks
#===============================================================================
if defined?(FieldEffects) && FieldEffects.respond_to?(:apply_battle_rule)
  module FieldEffects
    class << self
      alias prismfall_ebdx_apply_battle_rule apply_battle_rule unless method_defined?(:prismfall_ebdx_apply_battle_rule)
      def apply_battle_rule(battle)
        PrismfallEBDX::Vanilla.remember_default(battle) rescue nil
        prismfall_ebdx_apply_battle_rule(battle)
      end
    end
  end
end

if Battle::Scene.method_defined?(:pbCreateBackdropSprites)
  class Battle::Scene
    alias prismfall_ebdx_pbCreateBackdropSprites pbCreateBackdropSprites unless method_defined?(:prismfall_ebdx_pbCreateBackdropSprites)
    def pbCreateBackdropSprites
      if PrismfallEBDX::ENABLED && @battle
        begin
          pair = (PrismfallEBDX.current_field(@battle) == :NONE) ? nil : PrismfallEBDX::Vanilla.field_pair(@battle)
          if pair
            @battle.backdrop = pair[0]
            @battle.backdropBase = pair[1]
          end
        rescue StandardError => e
          PrismfallEBDX.log_error("pbCreateBackdropSprites", e)
        end
      end
      prismfall_ebdx_pbCreateBackdropSprites
      @prismfall_signature = PrismfallEBDX.signature(@battle) if @battle
    end
  end
end
