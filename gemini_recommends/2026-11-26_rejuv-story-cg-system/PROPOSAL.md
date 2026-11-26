# Proposal: Pokémon Rejuvenation-Style Single-Frame Story CG System (`021_StoryCG.rb`) + CG Wave 1 Delivery (6 Scenes / 11 PNGs — Pass 2 Certified)

- **Date:** 2026-11-26 (Pass 2 Revision)
- **From:** Gemini — Rejuv Single-Frame Illustrated CG Art Squad (CG Wave 1)
- **For:** Claude — Drop-in integration into `plugins/Prismfall Cutscenes/021_StoryCG.rb` (and optional `017_AdvancedAnimations.rb` kwarg)
- **Art Status:** **CG Wave 1 Pass 2 Complete & Dual-Synced** — 11 PNGs (22 byte-identical files across `graphics/Pictures/cg_*.png` and `art/out/Graphics/Pictures/cg_*.png`), 100% verified (`512×384`, `exact2x == True`, `colors <= 64`, `semi_alpha == 0`, `y=0..280` hero safe-zone / `y=288..384` dark dialogue bed, `0.00%` static background drift on locked-camera swaps `ch09` & `ch05`).

---

## 1. Design Goal (Pokémon Rejuvenation Single-Frame Story CGs)

Reuben loves *Pokémon Rejuvenation*'s unforgettable single-frame illustrated story CGs (such as Keta holding back Shadow Mewtwo while live conversational dialogue textboxes appear seamlessly across the lower edge of the painting, with locked-camera emotional beat-swaps mid-conversation).

Unlike `017_AdvancedAnimations.rb`'s `show_cut_plate` (which takes over the render loop with pans/zooms for short ~4s action apex plates like `cut_ch2_pageant_tear_90deg.png` and `cut_ch17_voss_breach_90deg.png`), **Story CGs** stay **static, crisp, 1:1 native `512×384`** while normal Essentials `Show Text` / `pbMessage` / `pf_say` / `Show Choices` commands run interactively on top of them!

### Visual & Safe-Zone Contract (Guaranteed on All Wave 1–3 CGs)
- **Native resolution:** Painted at `256×192`, upscaled `2×` `NEAREST` to **`512×384`** (`exact2x == True`), opaque RGBA (`semi_alpha == 0`), crisp `<= 64`-color pixel-art palette matching our Critic-certified **9.6 PASS** `cut_ch2_pageant_tear_90deg.png` and `cut_ch17_voss_breach_90deg.png`.
- **Dialogue Safe-Zone (`y=0..280` hero / `y=288..384` dark bed):** 100% of faces, eyes, focal hands, and key emotional props sit cleanly inside `y=0..280`. The bottom `96px` (`y=288..384`) is organically painted dark, moody foreground so Essentials' `512×96` message box sits cleanly over it with **ZERO face/hand/prop occlusion** (verified visually on `159_rejuv_cg_wave1_with_dialogue_overlay.png` and zoomed detail sheet `159b_rejuv_cg_wave1_pass2_fixes.png`).
- **Locked-Camera Beat-Swaps (`_a` → `_b`):** Non-relight `_b` variants are mask-composited directly onto `_a` using `_a`'s exact 64-color palette (`shift=(0,0)`, **`0.00%` static background pixel drift** on `ch09` and `ch05`, `0.0%` wall drift on `ch20`), so `pf_cg_swap` crossfades effortlessly in `8–14` frames with zero background shimmer.

---

## 2. Architecture & Drop-In Spec: `plugins/Prismfall Cutscenes/021_StoryCG.rb`

### 2.1 Public Event Script API

| Helper | Signature | Purpose |
|---|---|---|
| Show CG | `pf_cg_show(name, fade: 20, tone: nil, dim_bottom: false, suppress_portraits: true)` | Opens dedicated CG viewport (`z = 99_800`), loads `Graphics/Pictures/<name>`, fades in over `fade` frames (`0` = hard cut). Optional `Tone`, optional subtle bottom-96px scrim (`dim_bottom: true` for extra high-key scenes; default `false` since all CGs have dark beds), and suppresses redundant dialogue faceboxes by default (`suppress_portraits: true`). |
| Beat-Swap CG | `pf_cg_swap(name, flash: nil, shake: nil, fade: 8, tone: nil)` | Locked-camera crossfade to `_b` (or next plate) over `fade` frames. Optional viewport-scoped `flash:` (`Color` or `[r, g, b, a, dur]`) and viewport-scoped `shake:` (`power` or `[power, frames]`), both clamped when `Prismfall::Cutscene.photosensitive?` is true. Loop always runs for `[fade_frames, sh_dur, f_dur].max` frames so flashes never freeze mid-decay. |
| Instant Blackout | `pf_cg_blackout(hold_frames: 0)` | **0-frame hard cut to absolute black** without exposing the lit map underneath! Hides `@main_sp`/`@swap_sp`/`@dim_sp` while keeping `@bg_sp` opaque `#000000` at `z = 99_800` through gunshot SE & silence holds (e.g., Wenlow Ch16 L358–359). Call `pf_cg_hide(fade: 0)` only after `$game_screen.tone` is black (or map transfer begins) for **ZERO 1-frame lit-map flash**. |
| Hide CG | `pf_cg_hide(fade: 20)` | Fades out over `fade` frames (`0` = immediate teardown) and disposes all bitmaps/sprites/viewport cleanly. |

Query & lifecycle helpers on `Prismfall::StoryCG`:
- `Prismfall::StoryCG.active?` — `true` while a Story CG viewport is displayed.
- `Prismfall::StoryCG.suppress_portraits?` — `true` when `active? && @suppress_portraits`.
- `Prismfall::StoryCG.current_name` — current picture basename (or `nil`).
- `Prismfall::StoryCG.update` — ticks `@viewport.update` every frame from `Scene_Map#update` while active.
- `Prismfall::StoryCG.force_clear` — immediate leak-proof 0-frame teardown (used by cleanup hooks).

### 2.2 Viewport Z-Stacking & Shake-Safe Backing

| Layer | Z | Owner | Notes |
|---|---|---|---|
| Map tileset, events, weather, `017` `@plate_vp` (`390`) | `0 .. 500` | Essentials / `017` | Hidden completely underneath Story CG |
| **`Prismfall::StoryCG` `@viewport`** | **`99_800`** | **`021_StoryCG.rb`** | Contains `#000000` shake-safe backing (`z=0`), primary CG (`z=10`), crossfade CG (`z=20`), optional bottom scrim (`z=30`) |
| Finale letterbox bars (`BARS_Z`) | `99_900` | `019_Scenes_Finale.rb` L43 | Stays strictly ABOVE Story CG |
| Cutscene canvas / Lamp (`VIEWPORT_Z` / `LAMP_Z`) | `99_990` | `001_Config.rb` L14 / `019` L35 | Stays strictly ABOVE Story CG |
| Essentials `pbMessageDisplay` / `014_Portraits.rb` | `99_999` | Essentials / `014` L42 | Interactive dialogue & choices sit cleanly on top of Story CG |

### 2.3 Clean Integration Hooks (Verified Against Current Plugin Files & Pass 1 Audit Fixes)

1. **`014_Portraits.rb` — `Prismfall::Portrait.mode_for(spec)` (L171):**
   - Alias `prismfall_story_cg_mode_for`:
     ```ruby
     def mode_for(spec)
       if Prismfall::StoryCG.suppress_portraits?
         # Preserve cast carry-over so subsequent plain "[name: The Mourner]" lines
         # still resolve to :MOURNER for VoiceTicker blips!
         remember(spec, "") if spec && !spec[:carried] && cast?(spec[:id])
         return :plain
       end
       return prismfall_story_cg_mode_for(spec)
     end
     ```
   - **Why this works cleanly:**
     - `014_Portraits.rb` L822 (`pf.extract(message)`) **still strips `\pf[VALEN,neutral]` / `[portrait: ...]` tags cleanly** and **preserves the `"Valen: "` name label**.
     - `014_Portraits_Voice.rb` wraps `pbMessageDisplay` *outside* `014_Portraits.rb` and reads `VoiceTicker.speaker_of(message)` (L88–106) *before* `mode_for` runs — so **Audio v4.3 voice blips continue playing identically** (including carried aliases like `"The Mourner:"`!) while **zero duplicate portrait faceboxes overlap the illustrated CG**.
     - Passing `suppress_portraits: false` restores faceboxes transparently if any future scene requests them.

2. **`018_ExpressiveDialogue.rb` — `Prismfall::Expressive.trigger_acting` (L260) & `clear_all` (L421):**
   - Alias `prismfall_story_cg_trigger_acting`: early-return when `Prismfall::StoryCG.active?` so hidden overworld events don't spawn emotes, swap poses, or turn behind the fullscreen CG.
   - Alias `prismfall_story_cg_clear_all`: defense-in-depth cleanup hook when an expressive conversation clears.

3. **Independent Leak-Proof `Scene_Map#update` + Teardown Guards (Fixes Pass 1 P0 Leak & Frozen-Flash Bugs!):**
   - `021_StoryCG.rb` hooks **`Scene_Map#update` directly** (never relying on `018_ExpressiveDialogue.rb`'s `ex.active?`, which stays `false` when an event opens with `pf_cg_show` before ordinary dialogue!):
     - If `StoryCG.active? && (!defined?(pbMapInterpreterRunning?) || !pbMapInterpreterRunning?)` → calls `StoryCG.force_clear` immediately!
     - Otherwise while `StoryCG.active?` → calls `StoryCG.update` (`@viewport.update`) every frame so flashes/tones always animate smoothly and never freeze!
   - Also hooks `Interpreter#setup` (`if @main`), `Scene_Map#transfer_player`, and `Scene_Map#disposeSpritesets` so battles, `GO_EARLY_CROWN` game overs, menus, and map transfers can **never** leak a viewport.

4. **Optional `017_AdvancedAnimations.rb` `PortraitBox` Integration (`L661` & `Engine#say` `L1178`):**
   - Adding an optional keyword arg `hide_portrait: nil` to `PortraitBox#initialize` (L661) and `Engine#say` (L1178):
     ```ruby
     # 017_AdvancedAnimations.rb L661:
     def initialize(ui_vp, speaker_sym, expression, text, engine, name: nil, hide_portrait: nil)
       ...
       hide_p = hide_portrait.nil? ? (defined?(Prismfall::StoryCG) && Prismfall::StoryCG.suppress_portraits?) : hide_portrait
       p_bmp = (!hide_p && speaker_sym) ? load_portrait(speaker_sym, expression) : nil
     ```
     and forwarding `hide_portrait: hide_portrait` from `Engine#say` (L1178 → L1186). When `p_bmp` is `nil`, `PortraitBox` (L698) already stretches `msg_x = 12`, `msg_w = Graphics.width - 24` cleanly across the full width while keeping the gold speaker nameplate tab!

5. **Photosensitive Safety (`Prismfall::Cutscene.photosensitive?`):**
   - Matches `019_Scenes_Finale.rb` (L151–157) & `017_AdvancedAnimations.rb` (L1083–1088):
     - When `photosensitive?` is true: `flash` alpha is clamped to `<= 64` (soft wash, zero hard strobe) and `shake` amplitude is scaled `0.25×` (clamped `<= 2px`, min `1px`).

---

### 2.4 Drop-In Reference Implementation (`plugins/Prismfall Cutscenes/021_StoryCG.rb`)

```ruby
#===============================================================================
# Prismfall Cutscenes - 021 Story CG (Pokémon Rejuvenation-Style Illustrated CG)
#-------------------------------------------------------------------------------
# Fullscreen 512x384 single-frame pixel-illustrated story CG layer that stays
# live behind interactive Essentials Show Text / pbMessage / pf_say / choices,
# with locked-camera _a -> _b beat-swaps, 0-frame blackout hold (zero map
# flash), automatic portrait suppression (preserving VoiceTicker blips, carry
# aliases, and "Name: " labels), photosensitive clamps, and independent
# leak-proof Scene_Map / Interpreter auto-cleanup.
#
# Public Event Script API:
#   pf_cg_show(name, fade: 20, tone: nil, dim_bottom: false, suppress_portraits: true)
#   pf_cg_swap(name, flash: nil, shake: nil, fade: 8, tone: nil)
#   pf_cg_blackout(hold_frames: 0)
#   pf_cg_hide(fade: 20)
#===============================================================================
module Prismfall
  module StoryCG
    VIEWPORT_Z    = 99_800   # Strictly below 019 BARS_Z (99_900) & pbMessageDisplay (99_999)
    PICTURES_DIR  = "Graphics/Pictures/"
    SAFE_BOTTOM_H = 96       # Essentials 512x96 dialogue band (y=288..384)

    class << self
      def active?
        return !@viewport.nil? && !@viewport.disposed?
      end

      def suppress_portraits?
        return active? && @suppress_portraits
      end

      def current_name
        return active? ? @current_name : nil
      end

      def update
        @viewport.update if active?
      end

      def photosensitive?
        return Prismfall::Cutscene.photosensitive? if defined?(Prismfall::Cutscene) &&
                                                      Prismfall::Cutscene.respond_to?(:photosensitive?)
        return false
      rescue StandardError
        return false
      end

      def show(name, fade: 20, tone: nil, dim_bottom: false, suppress_portraits: true)
        bmp = load_cg_bitmap(name)
        return false if !bmp

        ensure_viewport
        @suppress_portraits = !!suppress_portraits
        @current_name = name.to_s

        # Close any stale portrait window currently open
        Prismfall::Portrait.close if defined?(Prismfall::Portrait) && Prismfall::Portrait.respond_to?(:close)

        dispose_bitmap_safe(@main_sp.bitmap)
        @main_sp.bitmap  = bmp
        @main_sp.ox      = 0
        @main_sp.oy      = 0
        @main_sp.x       = 0
        @main_sp.y       = 0
        @main_sp.tone    = resolve_tone(tone)
        @main_sp.visible = true

        @swap_sp.visible = false
        dispose_bitmap_safe(@swap_sp.bitmap)
        @swap_sp.bitmap  = nil

        @dim_sp.visible  = !!dim_bottom

        frames = [fade.to_i, 0].max
        if frames <= 0
          @bg_sp.opacity   = 255
          @main_sp.opacity = 255
          @dim_sp.opacity  = dim_bottom ? 255 : 0
          @viewport.update
        else
          @bg_sp.opacity   = 0
          @main_sp.opacity = 0
          @dim_sp.opacity  = 0
          1.upto(frames) do |i|
            op = (255.0 * i / frames).round
            @bg_sp.opacity   = op
            @main_sp.opacity = op
            @dim_sp.opacity  = dim_bottom ? op : 0
            step_cg_frame
          end
        end
        return true
      rescue StandardError => e
        log_err("StoryCG.show(#{name.inspect}) failed: #{e.class}: #{e.message}")
        force_clear
        return false
      end

      def swap(name, flash: nil, shake: nil, fade: 8, tone: nil)
        return show(name, fade: fade, tone: tone) if !active?
        bmp = load_cg_bitmap(name)
        return false if !bmp

        @current_name = name.to_s
        dispose_bitmap_safe(@swap_sp.bitmap)
        @swap_sp.bitmap  = bmp
        @swap_sp.ox      = 0
        @swap_sp.oy      = 0
        @swap_sp.x       = 0
        @swap_sp.y       = 0
        @swap_sp.tone    = tone ? resolve_tone(tone) : @main_sp.tone.clone
        @swap_sp.opacity = 0
        @swap_sp.visible = true

        # Viewport-scoped flash (photosensitive-clamped); f_dur tracked in total_frames so flash never freezes!
        f_dur = 0
        if flash
          f_color, f_dur = parse_flash(flash)
          if f_color
            if photosensitive?
              f_color = Color.new(f_color.red, f_color.green, f_color.blue, [f_color.alpha, 64].min)
            end
            @viewport.flash(f_color, f_dur)
          else
            f_dur = 0
          end
        end

        # Viewport-scoped damped shake (photosensitive-clamped; #000000 backing prevents edge gaps)
        sh_power, sh_dur = parse_shake(shake)
        if sh_power > 0 && photosensitive?
          sh_power = [[(sh_power * 0.25).round, 1].max, 2].min
        end

        fade_frames  = [fade.to_i, 0].max
        total_frames = [fade_frames, sh_dur, f_dur].max
        if total_frames <= 0
          promote_swap_sprite
          @viewport.update
        else
          promoted = false
          1.upto(total_frames) do |i|
            if !promoted
              if fade_frames > 0
                u = [i.to_f / fade_frames, 1.0].min
                @swap_sp.opacity = (255.0 * u).round
                if i >= fade_frames
                  promote_swap_sprite
                  promoted = true
                end
              else
                promote_swap_sprite
                promoted = true
              end
            end
            if sh_power > 0 && i <= sh_dur
              decay = 1.0 - (i.to_f / [sh_dur, 1].max)
              amp = (sh_power * decay).round
              @viewport.ox = (i.odd? ? amp : -amp)
              @viewport.oy = ((i % 3 == 0) ? (amp / 2) : 0)
            else
              @viewport.ox = 0
              @viewport.oy = 0
            end
            step_cg_frame
          end
          @viewport.ox = 0
          @viewport.oy = 0
          promote_swap_sprite if !promoted
        end
        return true
      rescue StandardError => e
        log_err("StoryCG.swap(#{name.inspect}) failed: #{e.class}: #{e.message}")
        return false
      end

      # 0-frame hard cut to solid opaque #000000 at z=99_800 — keeps the lit map
      # completely occluded (ZERO 1-frame lit-map flash!) while SE / silence hold plays.
      # Follow with $game_screen.start_tone_change(...) + pf_cg_hide(fade: 0) or transfer.
      def blackout(hold_frames: 0)
        ensure_viewport
        @current_name    = nil
        @bg_sp.opacity   = 255
        @bg_sp.visible   = true
        @main_sp.visible = false
        @swap_sp.visible = false
        @dim_sp.visible  = false
        @viewport.ox     = 0
        @viewport.oy     = 0
        @viewport.flash(nil, 0)
        @viewport.update
        frames = [hold_frames.to_i, 0].max
        frames.times { step_cg_frame } if frames > 0
        return true
      rescue StandardError => e
        log_err("StoryCG.blackout failed: #{e.class}: #{e.message}")
        return false
      end

      def hide(fade: 20)
        return false if !active?
        frames = [fade.to_i, 0].max
        if frames > 0
          start_bg   = @bg_sp.opacity
          start_main = @main_sp.visible ? @main_sp.opacity : 0
          start_dim  = @dim_sp.visible ? @dim_sp.opacity : 0
          1.upto(frames) do |i|
            k = 1.0 - (i.to_f / frames)
            @bg_sp.opacity   = (start_bg * k).round
            @main_sp.opacity = (start_main * k).round if @main_sp.visible
            @dim_sp.opacity  = (start_dim * k).round  if @dim_sp.visible
            step_cg_frame
          end
        end
        force_clear
        return true
      rescue StandardError => e
        log_err("StoryCG.hide failed: #{e.class}: #{e.message}")
        force_clear
        return false
      end

      def force_clear
        @suppress_portraits = false
        @current_name = nil
        [@dim_sp, @swap_sp, @main_sp, @bg_sp].each do |sp|
          next if !sp
          dispose_bitmap_safe(sp.bitmap) if !sp.disposed?
          sp.dispose if !sp.disposed?
        end
        @dim_sp = @swap_sp = @main_sp = @bg_sp = nil
        @viewport.dispose if @viewport && !@viewport.disposed?
        @viewport = nil
      rescue StandardError
        @dim_sp = @swap_sp = @main_sp = @bg_sp = @viewport = nil
        @suppress_portraits = false
        @current_name = nil
      end

      private

      def ensure_viewport
        return if active?
        w = Graphics.width
        h = Graphics.height
        @viewport = Viewport.new(0, 0, w, h)
        @viewport.z = VIEWPORT_Z

        # Oversized #000000 shake-safe backing prevents map bleed during shake & blackout
        pad = 32
        @bg_sp = Sprite.new(@viewport)
        @bg_sp.z = 0
        @bg_sp.x = -pad
        @bg_sp.y = -pad
        bg_bmp = Bitmap.new(w + pad * 2, h + pad * 2)
        bg_bmp.fill_rect(0, 0, w + pad * 2, h + pad * 2, Color.new(0, 0, 0, 255))
        @bg_sp.bitmap = bg_bmp

        @main_sp = Sprite.new(@viewport)
        @main_sp.z = 10

        @swap_sp = Sprite.new(@viewport)
        @swap_sp.z = 20
        @swap_sp.visible = false

        # Optional subtle bottom-96px gradient scrim (y=288..384) when dim_bottom: true
        @dim_sp = Sprite.new(@viewport)
        @dim_sp.z = 30
        @dim_sp.y = h - SAFE_BOTTOM_H - 16
        dim_bmp = Bitmap.new(w, SAFE_BOTTOM_H + 16)
        (SAFE_BOTTOM_H + 16).times do |row|
          u = [row.to_f / 28.0, 1.0].min
          alpha = (128 * u).round
          dim_bmp.fill_rect(0, row, w, 1, Color.new(8, 10, 18, alpha))
        end
        @dim_sp.bitmap  = dim_bmp
        @dim_sp.visible = false
      end

      def promote_swap_sprite
        dispose_bitmap_safe(@main_sp.bitmap)
        @main_sp.bitmap  = @swap_sp.bitmap
        @main_sp.tone    = @swap_sp.tone.clone
        @main_sp.opacity = 255
        @main_sp.visible = true
        @swap_sp.bitmap  = nil
        @swap_sp.visible = false
      end

      def load_cg_bitmap(name)
        raw = name.to_s.sub(/\.png\z/i, "")
        path = raw.start_with?("Graphics/") ? raw : "#{PICTURES_DIR}#{raw}"
        if defined?(Prismfall::Cutscene::Gfx) && Prismfall::Cutscene::Gfx.respond_to?(:load_bitmap)
          bmp = Prismfall::Cutscene::Gfx.load_bitmap(path)
          return bmp if bmp
        end
        return RPG::Cache.picture(File.basename(raw)).clone if defined?(RPG::Cache)
        return Bitmap.new("#{path}.png") if File.exist?("#{path}.png")
        log_err("StoryCG missing picture: #{path}")
        return nil
      end

      def resolve_tone(tone)
        return Tone.new(0, 0, 0, 0) if !tone
        return tone.clone if tone.is_a?(Tone)
        if tone.is_a?(Array)
          return Tone.new(tone[0].to_f, tone[1].to_f, tone[2].to_f, (tone[3] || 0).to_f)
        end
        return Tone.new(0, 0, 0, 0)
      end

      def parse_flash(flash)
        return [nil, 0] if !flash
        return [Color.new(255, 255, 255, 200), 12] if flash == true
        return [flash, 12] if flash.is_a?(Color)
        if flash.is_a?(Array)
          r, g, b, a, dur = flash
          return [Color.new(r.to_i, g.to_i, b.to_i, (a || 200).to_i), (dur || 12).to_i]
        end
        return [nil, 0]
      end

      def parse_shake(shake)
        return [0, 0] if !shake
        return [4, 12] if shake == true
        return [shake.to_i, 12] if shake.is_a?(Numeric)
        return [shake[0].to_i, (shake[1] || 12).to_i] if shake.is_a?(Array)
        return [0, 0]
      end

      def step_cg_frame
        @viewport.update if @viewport && !@viewport.disposed?
        Graphics.update
        Input.update
      end

      def dispose_bitmap_safe(bmp)
        bmp.dispose if bmp && !bmp.disposed?
      rescue StandardError
        nil
      end

      def log_err(msg)
        if defined?(Prismfall::Cutscene::Util) && Prismfall::Cutscene::Util.respond_to?(:log)
          Prismfall::Cutscene::Util.log(msg)
        end
      end
    end
  end
end

#-------------------------------------------------------------------------------
# Global Event Script Helpers
#-------------------------------------------------------------------------------
def pf_cg_show(name, fade: 20, tone: nil, dim_bottom: false, suppress_portraits: true)
  Prismfall::StoryCG.show(name, fade: fade, tone: tone, dim_bottom: dim_bottom,
                          suppress_portraits: suppress_portraits)
end

def pf_cg_swap(name, flash: nil, shake: nil, fade: 8, tone: nil)
  Prismfall::StoryCG.swap(name, flash: flash, shake: shake, fade: fade, tone: tone)
end

def pf_cg_blackout(hold_frames: 0)
  Prismfall::StoryCG.blackout(hold_frames: hold_frames)
end

def pf_cg_hide(fade: 20)
  Prismfall::StoryCG.hide(fade: fade)
end

#-------------------------------------------------------------------------------
# Hook 1: 014_Portraits.rb — suppress redundant faceboxes while preserving
#         \pf[...] stripping, "Name: " labels, carry aliases, & VoiceTicker blips!
#-------------------------------------------------------------------------------
if defined?(Prismfall::Portrait) && !Prismfall::Portrait.respond_to?(:prismfall_story_cg_mode_for)
  module Prismfall
    module Portrait
      class << self
        alias prismfall_story_cg_mode_for mode_for

        def mode_for(spec)
          if Prismfall::StoryCG.suppress_portraits?
            remember(spec, "") if spec && !spec[:carried] && cast?(spec[:id])
            return :plain
          end
          return prismfall_story_cg_mode_for(spec)
        end
      end
    end
  end
end

#-------------------------------------------------------------------------------
# Hook 2: 018_ExpressiveDialogue.rb — pause hidden map acting & defense-in-depth clear
#-------------------------------------------------------------------------------
if defined?(Prismfall::Expressive) && !Prismfall::Expressive.respond_to?(:prismfall_story_cg_trigger_acting)
  module Prismfall
    module Expressive
      class << self
        alias prismfall_story_cg_trigger_acting trigger_acting
        alias prismfall_story_cg_clear_all      clear_all

        def trigger_acting(spec, dirs, plain = false)
          return if Prismfall::StoryCG.active?
          return prismfall_story_cg_trigger_acting(spec, dirs, plain)
        end

        def clear_all
          Prismfall::StoryCG.force_clear if Prismfall::StoryCG.active? &&
                                            (!defined?(pbMapInterpreterRunning?) || !pbMapInterpreterRunning?)
          return prismfall_story_cg_clear_all
        end
      end
    end
  end
end

#-------------------------------------------------------------------------------
# Hook 3: Independent Scene_Map#update + Leak-Proof Interpreter / Teardown Guards
#         (Runs even if Expressive.active? == false, AND ticks @viewport.update!)
#-------------------------------------------------------------------------------
if defined?(Interpreter) && !Interpreter.method_defined?(:prismfall_story_cg_setup)
  class Interpreter
    alias prismfall_story_cg_setup setup

    def setup(*args)
      Prismfall::StoryCG.force_clear if @main && Prismfall::StoryCG.active?
      return prismfall_story_cg_setup(*args)
    end
  end
end

if defined?(Scene_Map) && !Scene_Map.method_defined?(:prismfall_story_cg_update)
  class Scene_Map
    alias prismfall_story_cg_update             update
    alias prismfall_story_cg_transfer           transfer_player
    alias prismfall_story_cg_dispose_spritesets disposeSpritesets

    def update
      prismfall_story_cg_update
      if Prismfall::StoryCG.active?
        if !defined?(pbMapInterpreterRunning?) || !pbMapInterpreterRunning?
          Prismfall::StoryCG.force_clear
        else
          Prismfall::StoryCG.update
        end
      end
    end

    def transfer_player(*args)
      Prismfall::StoryCG.force_clear if Prismfall::StoryCG.active?
      return prismfall_story_cg_transfer(*args)
    end

    def disposeSpritesets(*args)
      Prismfall::StoryCG.force_clear if Prismfall::StoryCG.active?
      return prismfall_story_cg_dispose_spritesets(*args)
    end
  end
end
```

---

## 3. Complete Wave 1 Asset Inventory (6 Flagship Scenes / 11 PNGs = 22 Dual-Synced Files — Pass 2 Verified)

All **11 PNGs** are dual-synced byte-identically between `graphics/Pictures/` and `art/out/Graphics/Pictures/` (`0` MD5 mismatches), verified `512×384`, `exact2x == True`, `colors == 64` (`<= 64`), `semi_alpha == 0`, and visually proofed with live `512×96` RPG Maker dialogue overlays at `y=288..384`:

| # | Scene & Chapter | Filename (`graphics/Pictures/` & `art/out/Graphics/Pictures/`) | Script Anchor | MD5 (Byte-Identical Dual-Sync) | Bytes |
|---|---|---|---|---|---:|
| 1a | **Ch5 — Shattered Lowlight** (Map 608): Valen peels grey glove (dangling tips clear of `y=288`) & presses crystal left palm to Veil | `cg_ch05_valen_glove_off_a.png` | `story/24_SCRIPT_CH5.md` L887–889 | `305a2ac41076e787863e6a2667078688` | 60,821 |
| 1b | **Ch5 — Shattered Lowlight** (Locked-Palette Swap, `0.00%` street drift): Glove back on, Veil calms, Valen locks eyes on PC | `cg_ch05_valen_glove_off_b.png` | `story/24_SCRIPT_CH5.md` L890–894 | `e1518ed0c73cc491049931c009fbaf46` | 58,710 |
| 2a | **Ch9 — Iron Pit Reliquary** (Map 264): Trevenant root-wall + frost ridge, split lily mask, Rowan unmasked, emerald-eyed Juno cradling warm-skinned Nell buried in blossoms (`Ch10 L46`) | `cg_ch09_rowan_unmasked_a.png` | `story/27_SCRIPT_CH9.md` L601–608 | `6d283c08bd463aab200824a3b3f31ccd` | 94,071 |
| 2b | **Ch9 — Iron Pit Reliquary** (Locked-Palette Swap, `0.00%` bg drift): Crystal climbs shoulder/wrist, Rowan droops, delicate silver tears beneath Juno's emerald eyes | `cg_ch09_rowan_unmasked_b.png` | `story/27_SCRIPT_CH9.md` L609–614 | `cc480796df7f43f6f67790b1e3c17453` | 93,924 |
| 3a | **Ch16 — Mirefen Infirmary** (Map 223): "This Is a Hospital" — 17yo Wenlow blocking glass-bead doorway before Quiet Ward cots facing grey-coat Meridian Lieutenant w/ patrol lantern & Sweetrot list (ZERO rifles → `pf_cg_blackout`!) | `cg_ch16_wenlow_doorway_a.png` | `story/35_SCRIPT_CH16.md` L352–359 | `672ab6db5188e9d821b44512a6bcff65` | 77,011 |
| 4a | **Ch10 — Bride Grove** (Heartgarden, branch-agnostic for `:ogre` & `:hesitate` — no Ogerpon/Valen): Juno presses bare hands to emerald Meadow Plate in cold Bleed haze | `cg_ch10_bride_tree_plate_a.png` | `story/28_SCRIPT_CH10.md` L493–504 | `87dba24dfe738e6b86777031fc43ced1` | 69,173 |
| 4b | **Ch10 — Bride Grove** (Global Relight Swap): Bleed banished in warm golden sunrise, emerald pollen & pink petals rise, parted-lips awe + glistening tears + golden pollen flecks on Juno | `cg_ch10_bride_tree_plate_b.png` | `story/28_SCRIPT_CH10.md` L505–514 | `06b0579c098b302f9639db54e915c9c0` | 73,217 |
| 5a | **Ch20 — Sovereign's Sanctum** *(9.3 Gold Pass)*: Valen's Last Audience (candlelight, crystal left arm on cushion, cracked Crown, emerald Zygarde Cell) | `cg_ch20_valen_audience_a.png` | `story/39_SCRIPT_CH20.md` L390–415 | `16aac7d1606bea214246bc6f12948716` | 59,407 |
| 5b | **Ch20 — Sovereign's Sanctum** *(9.3 Gold Pass)*: Valen lifts eyes to PC with one unhidden tear & faint relieved smile | `cg_ch20_valen_audience_b.png` | `story/39_SCRIPT_CH20.md` L419–425 | `fe33dcef807b32dc01225c39f4bf6b45` | 63,040 |
| 6a | **Ch13 — Mindscape** *(8.8 Pass)* (Lower Crownhaven AF 290): Gender-neutral 15yo PC crouching before 5yo self clutching Choir ribbon | `cg_ch13_five_year_old_self_a.png` | `story/32_SCRIPT_CH13.md` L162–171 | `af28ee7fc3cf9d6efdb1fb4c2dc37843` | 48,482 |
| 6b | **Ch13 — Mindscape** *(8.8 Pass)*: 5yo self takes 15yo PC's hand as pure white star-crack blooms between chests | `cg_ch13_five_year_old_self_b.png` | `story/32_SCRIPT_CH13.md` L172–182 | `18ed98f1ae73f7ab5353ef54822dcfb8` | 51,092 |

### 3.1 Exact Event Choreography Snippets (Ready to Wire)

- **Ch5 (`24_SCRIPT_CH5.md` L887–894):**
  ```ruby
  pf_cg_show("cg_ch05_valen_glove_off_a", fade: 20)
  pbMessage(_INTL("Valen Corrigan pulls off his grey glove..."))
  pf_cg_swap("cg_ch05_valen_glove_off_b", flash: [210, 225, 255, 110, 8], fade: 10)
  pf_say(:VALEN, :shocked, "...")
  pf_say(:VALEN, :neutral, "You were in the Lowlight when it went?")
  pf_say(:VALEN, :neutral, "And you're... standing.")
  pf_cg_hide(fade: 20)
  ```
- **Ch9 (`27_SCRIPT_CH9.md` L601–614):**
  ```ruby
  pf_cg_show("cg_ch09_rowan_unmasked_a", fade: 16)
  pf_say(:JUNO, :shocked, "...")
  pf_say(:JUNO, :shocked, "...Uncle Rowan?")
  pf_cg_swap("cg_ch09_rowan_unmasked_b", fade: 12)
  pf_say(:ROWAN, :sad, "Juno. Don't look at me like that.")
  pf_say(:ROWAN, :sad, "Look at the flowers. Look at what they're standing on.")
  pf_cg_hide(fade: 24)
  ```
- **Ch16 (`35_SCRIPT_CH16.md` L352–359 — 0-frame blackout with ZERO lit-map flash!):**
  ```ruby
  # Framed with grey-coat Meridian Lieutenant holding patrol lamp & Sweetrot list (NO rifles visible!)
  pbBGMStop
  pf_cg_show("cg_ch16_wenlow_doorway_a", fade: 14)
  pf_say(:WENLOW, :neutral, "This is a hospital.")
  pf_say(:WENLOW, :neutral, "You have to —")
  pf_cg_blackout(hold_frames: 0)  # Instant 0-frame opaque #000000 at z=99_800 — ZERO 1-frame map flash!
  pbSEPlay("pf_gunshot")          # Single gunshot SE in total darkness
  pf_cg_blackout(hold_frames: 120)# 120-frame silent hold (swap PC party/charset safely under black!)
  $game_screen.start_tone_change(Tone.new(-255, -255, -255, 0), 0)
  $game_screen.update
  pbUpdateSceneMap if defined?(pbUpdateSceneMap)
  $scene.spriteset.update if $scene.respond_to?(:spriteset) && $scene.spriteset
  pf_cg_hide(fade: 0)             # Seamless release into darkened aftermath transfer!
  ```
- **Ch10 (`28_SCRIPT_CH10.md` L493–514 — 100% branch-agnostic for BOTH `:ogre` & `:hesitate`):**
  ```ruby
  pf_cg_show("cg_ch10_bride_tree_plate_a", fade: 24)
  # ... Juno's hesitation + PC choice ("Just hold it." / "Say what you'd say to a plant." / "...")
  pf_cg_swap("cg_ch10_bride_tree_plate_b", flash: [255, 244, 196, 170, 14], fade: 18)
  pf_say(:JUNO, :crying, "Oh, it's heavy. Nobody said it was heavy.")
  pf_say(:JUNO, :crying, "It's so heavy. It's like holding the whole hill.")
  pf_cg_hide(fade: 24)            # Returns to map right before Valen & Tamsin arrive at L517!
  ```
- **Ch20 (`39_SCRIPT_CH20.md` L390–425):**
  ```ruby
  pf_cg_show("cg_ch20_valen_audience_a", fade: 28)
  # ... Valen's explanation + :ch20_audience choice
  pf_cg_swap("cg_ch20_valen_audience_b", fade: 14) # on :keep weep OR :refuse rare smile!
  # ... concluding beat (before GO_EARLY_CROWN stand-up)
  pf_cg_hide(fade: 24)
  ```
- **Ch13 (`32_SCRIPT_CH13.md` L162–182):**
  ```ruby
  pf_cg_show("cg_ch13_five_year_old_self_a", fade: 24)
  pbMessage(_INTL("Child: Mum's singing. Do you want to see the light?"))
  # ... :ch13_remember choice; on :show or :scared:
  # Note: total_frames = [fade(10), shake(0), f_dur(14)].max = 14 -> flash completes cleanly!
  pf_cg_swap("cg_ch13_five_year_old_self_b", flash: [255, 255, 245, 190, 14], fade: 10)
  pbMessage(_INTL("Child: I know. That's why I waited for you."))
  pf_cg_hide(fade: 20)
  ```

---

## 4. Queued Master Plan: Waves 2 & 3 (14 Additional Flagship Story CGs)

All 14 queued CGs follow the exact same `512×384` (`exact2x == True`, `<= 64` colors, `y=0..280` hero / `y=288..384` dark dialogue bed, locked-palette mask-composite `_b` swaps with `0.00%` static background drift) visual contract:

### Wave 2 — Act I–IV Character & Turning-Point CGs (7 Scenes)

| # | Planned Filenames | Chapter & Scene | Script Anchor | Visual Pitch |
|---|---|---|---|---|
| 7 | `cg_ch00_dovetail_letter_a/b.png` | **Ch0 — The Dovetail Deck**: Reading Mum's final letter at dusk | `story/20_SCRIPT_CH0-2.md` L23–55 | PC hands holding Ines's folded salt-stained letter over the ferry rail (`_a`), glowing faint horizon beacon of Ferrow Lighthouse rising in twilight mist (`_b`). |
| 8 | `cg_ch07_quiet_ward_cots_a/b.png` | **Ch7 — Mirefen Quiet Ward**: Corvin drawing back the glass-bead curtain | `story/26_SCRIPT_CH7.md` L117–148 | Forty dreaming glass-edged patients beneath soft blue lanterns, masked Corvin pausing beside one breathing chest (`_a`), Juno clutching Rowan's ledger in realization (`_b`). |
| 9 | `cg_ch08_hearthguild_chestnuts_a/b.png` | **Ch8 — Hearthguild Hall**: Late-night chestnuts by the forge | `story/29_SCRIPT_CH8.md` L412–440 | Brann Holloway in firelight passing roasted chestnuts & cider to Sigrun and PC (`_a`), Brann's face going quiet and shadowed at his slip about AF 290 (`_b`). |
| 10 | `cg_ch11_kyogre_harbour_a/b.png` | **Ch11 — Rimeholt Harbour**: "The Lake Breathes" | `story/30_SCRIPT_CH11.md` L365–404 | Cracking glacier pier under storm-lit purple clouds as Primal Kyogre's glowing blue markings surface beneath Anja & PC (`_a`), torrential sea wall rising (`_b`). |
| 11 | `cg_ch12_larch_broadcast_a/b.png` | **Ch12 — Stormwatch Spire Roof**: The Midnight Larch Papers | `story/31_SCRIPT_CH12.md` L184–224 | Wind-whipped Professor Larch clutching rain-soaked AF 292 pages before the glowing relay dish (`_a`), dozens of distant Velmora screens lighting up gold behind her (`_b`). |
| 12 | `cg_ch14_badge_case_lining_a/b.png` | **Ch14 — Cragholm Bench**: "Voss Isn't Watching You. He's Tuning You." | `story/33_SCRIPT_CH14.md` L242–295 | Overhead close-up of Larch's tools prying open the PC's leather badge case revealing hidden Lattice-glass wiring (`_a`), transmitter LED pulsing amber-crimson in the dark (`_b`). |
| 13 | `cg_ch15_morwen_nursery_echo_a/b.png` | **Ch15 — Hollow Cathedral**: Morwen's AF 290 Echo | `story/34_SCRIPT_CH15.md` L179–265 | Translucent violet-silver memory of Morwen Vane throwing her Ghost-Warden cloak over the 5-year-old PC as blinding white light breaks across her back (`_a`), Kestrel's shattered expression watching (`_b`). |

### Wave 3 — Act IV–V Climax, Finale & Post-Game CGs (7 Scenes)

| # | Planned Filenames | Chapter & Scene | Script Anchor | Visual Pitch |
|---|---|---|---|---|
| 14 | `cg_ch17_aurelia_sun_court_a/b.png` | **Ch17 — Sunken Aurelia**: "You're the Missing Piece" | `story/36_SCRIPT_CH17.md` L285–345 | Cathedral-vault underwater glass dome framing the ancient golden Sun Court mosaic (`_a`), Aurelian Voss stepping calmly from the breached glowing doorway naming himself (`_b`). |
| 15 | `cg_ch18_hymn_of_return_a/b.png` | **Ch18 — Gloaming Dusk-Chapel**: The Complete Hymn of Return | `story/37_SCRIPT_CH18.md` L284–309 | Celestine unveiling the illuminated ancient score beneath luminous Great Tree roots (`_a`), eighteen faint prismatic notes rising into the dusk vault (`_b`). |
| 16 | `cg_ch19_draco_brazier_oath_a/b.png` | **Ch19 — Wyrmrest Gate**: Sigrun's Trial & The Oath | `story/38_SCRIPT_CH19.md` L90–145 | Roaring blue-white dragonfire brazier lighting Sigrun and the hooded PC (`_a`), sparks rising toward the distant crown-spire horizon as the oath is spoken (`_b`). |
| 17 | `cg_ch20_little_owl_bedside_a/b.png` | **Ch20 — Sanctum After Midnight**: "...Little Owl." | `story/39_SCRIPT_CH20.md` L447–462 | Ilsa standing inside the candlelit Sanctum door holding her earmuffs off (`_a`), sitting quietly beside Valen on the camp bed under his white coat (`_b`). |
| 18 | `cg_ch21_arceus_eighteen_plates_a/b.png` | **Ch21 — Prism Arena True Finale**: Eighteen Wardens Letting Go | `story/40_SCRIPT_CH21.md` L220–275 | Valen holding the fracturing Ring as eighteen luminous Plates orbit high above (`_a`), Arceus descending in calm golden-white radiance as the chains dissolve into stardust (`_b`). |
| 19 | `cg_pg_zygarde_memorial_a/b.png` | **Post-Game — Fallmorn**: Valen's Memorial & Zygarde Chooses | `story/41_SCRIPT_POSTGAME.md` L140–175 | Sunlit Basilica garden stone beside the quiet ocean horizon with a glowing cluster of emerald Zygarde Cells gathering (`_a`), Zygarde's emerald silhouette watching calmly over Crownhaven (`_b`). |
| 20 | `cg_ruin_gilded_king_throne_a/b.png` | **Ruin Route — R7 Hijack**: The Gilded King Unchained | `story/42_SCRIPT_RUIN_KING.md` L105–165 | Inverted crimson-and-gold Prism Arena with shattered golden chains swirling around Gilded King Aurelius (`_a`), the cracked Crown blazing stark inverse violet-black (`_b`). |

---

## 5. Verification & Selftest Checklist for Claude

1. **Zero regressions on existing portraits/voices:** Normal conversation (`StoryCG.active? == false`) -> `FaceBox` & `VoiceTicker` unchanged.
2. **Active Story CG dialogue + carry alias test:** Call `pf_cg_show("cg_ch05_valen_glove_off_a")` then `pf_say(:VALEN, :neutral, "You were in the Lowlight when it went?")` (plus an untagged carried follow-up line like `"The Mourner: ..."`) -> verify `\pf[...]` stripped, `"Name: "` preserved, `VoiceTicker` ticks cleanly on both tagged and carried lines, ZERO facebox overlaps the CG, text sits cleanly in `y=288..384`.
3. **Flash completion when `f_dur > fade` (Pass 1 P0 fix):** Run `pf_cg_swap("cg_ch13_five_year_old_self_b", flash: [255, 255, 245, 190, 14], fade: 10)` -> verify loop steps all `14` frames AND `Scene_Map#update` calls `StoryCG.update`, leaving ZERO frozen white wash; confirm photosensitive clamp caps flash alpha `<= 64` & shake `<= 2px`.
4. **Ch16 0-frame blackout without 1-frame lit-map flash (Pass 1 P1 fix):** Run `pf_cg_show("cg_ch16_wenlow_doorway_a")` -> `pf_cg_blackout(hold_frames: 0)` -> `pbSEPlay("pf_gunshot")` -> `pf_cg_blackout(hold_frames: 120)` -> `$game_screen.start_tone_change(...)` -> `pf_cg_hide(fade: 0)` -> verify ZERO 1-frame lit-Infirmary flash!
5. **Leak-proof event-end cleanup when CG opens first (Pass 1 P0 fix):** Run an event that calls `pf_cg_show(...)` as its very first command (so `Expressive.active? == false`) and ends WITHOUT calling `pf_cg_hide` -> verify `Scene_Map#update` immediately calls `StoryCG.force_clear`, leaving `StoryCG.active? == false` and zero undisposed `Viewport` objects. Also test `transfer_player` and battle entry (`disposeSpritesets`).
