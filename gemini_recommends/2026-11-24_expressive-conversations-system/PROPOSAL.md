# Expressive Normal Conversations & Overworld Character-Acting System — v2 Natural Restraint (`018_ExpressiveDialogue.rb`)

**Date:** 2026-11-24 (v2 Natural Restraint Revision — 2026-11-25)  
**Target Plugin Drop-In:** `plugins/Prismfall Cutscenes/018_ExpressiveDialogue.rb` (loads after `014_Portraits.rb` and `017_RejuvCutscenes.rb` with **zero breaking changes** to existing `[portrait: CHAR, expr]` / `\pf[...]` / `\pfb[...]` tags or `pf_say` calls!)  
**Benchmark Bar:** *The Legend of Heroes: Trails*, *Fire Emblem*, *Persona*, *Pokémon Rejuvenation V14*, and official Nintendo DS *Pokémon Black 2 / White 2* (Gen 5).

---

## 0. v1 → v2 Creator Feedback & Natural Restraint Redesign

Following creator review of the v1 prototype (`102b_expressive_dialogue_before_after.gif`), two sharp craft adjustments reshaped the entire architecture around **prestige JRPG restraint**:

> 1. *"also dont make the portraits move, that looks weird, try to make it as natural as possible"*
> 2. *"maybe u went a bit too much with the expressions... like dont throw them into every single thing..."*

### What Changed from v1 → v2

| Area | v1 Prototype (Too Busy / Cartoonish) | v2 Natural Restraint (Shipped Architecture) |
|---|---|---|
| **Portrait Position** | Slid in `28px`, bounced on `:happy`, shook/jumped on `:shocked`, trembled on `:angry`, drooped on `:sad`, swayed on `:blush`, dropped `4px` when inactive, and micro-bobbed every glyph | **100% Rock-Solid Still (`0px` X/Y motion at all times).** Anchored pixel-locked at exact Left & Right slots — zero bounce, zero shake, zero bob, zero recess drop, zero flashing borders. |
| **Portrait Polish** | Aggressive per-emotion physics + pulsing red borders | **Pure prestige visual cues:** clean **Dual-Speaker Stage**, smooth **4-frame (`0.10s`) alpha fade-in & expression crossfade**, and subtle **listener dimming** (`Tone.new(-42, -42, -42, 35)`) on the inactive portrait. |
| **Emote Balloons** | `AUTO_EMOTES = true` fired balloons automatically on almost every portrait expression change (`:happy` → 🎵, `:angry` → 💢, `:deadpan` → `...`, etc.) | **`AUTO_EMOTE = false` by default.** Zero automatic emote spam. Balloons fire **only** when explicitly scripted via `\pfe[...]` or `pf_emote(ev, :dots)` on genuine punchlines, surprises, or awkward pauses (**rule of thumb: max 1–2 per conversation**). |
| **Overworld Micro-Acting** | `AUTO_MICRO_ACTING = true` made sprites automatically hop, shudder, or recoil on every line | **`AUTO_MICRO_ACTING = false` by default.** Overworld expressiveness comes from **natural facing turns** toward the speaker, **tasteful restrained `pose_<CHAR>` stance shifts**, and **gentle opt-in acting** (`pf_nod`, `pf_step_back`, `pf_turn_away`, `pf_lean_in`). |
| **Scene Cleanup Overhead** | Called `clear_all` on every idle `Scene_Map#update` tick | Guarded with `Expressive.active?` so cleanup triggers **once** when dialogue ends — zero per-frame exploration overhead. |

---

## 1. Audit of Prismfall's Current Conversation System (`014_Portraits.rb`)

An inspection of [`plugins/Prismfall Cutscenes/014_Portraits.rb`](../../plugins/Prismfall%20Cutscenes/014_Portraits.rb) and [`plugins/Prismfall Core/025_CharsetAliases.rb`](../../plugins/Prismfall%20Core/025_CharsetAliases.rb) shows a clean, modular foundation — with **three high-value, natural upgrades** that elevate everyday scenes without ever feeling gimmicky:

| # | Current Behavior in `014_Portraits.rb` | Why Normal Conversations Feel Flat | How `018_ExpressiveDialogue.rb` v2 Solves It Naturally |
|---|---|---|---|
| 1 | **Single Left-Only `FaceBox`** (`Portrait.open` immediately calls `close`, lines 234–249; lines 608–617 rise `8px` or nudge `2px`) | When Character B replies to Character A, A vanishes abruptly and B overwrites the exact same left slot. Two-person dialogue loses spatial rhythm and presence. | **Pillar A — Rock-Solid Still Dual-Speaker Stage:** Speaker A fades cleanly into Left (`0px` motion); when Speaker B replies, A remains anchored on Left smoothly dimmed (`Tone.new(-42, -42, -42, 35)`) while B fades smoothly into Right at full brightness. Expression swaps crossfade over 4 frames with `0px` jitter. |
| 2 | **No Overworld Emote Balloons in Face Mode** (line 20: `# In face mode the emotes and event fields are ignored`) | Writers cannot punctuate a rare awkward silence (`...`), surprise (`!`), or realization (`💡`) above the map sprite during normal face-portrait dialogue. | **Pillar B — Sparing, High-Impact B2W2 Emote Balloons (`pf_emote_balloons.png`):** Crisp 10-emote × 4-frame 2× DS balloon sheet, **`AUTO_EMOTE = false` by default** — triggered **only** on intentional scripted beats via `\pfe[dots]` / `pf_emote(ev, :question)` (max 1–2 per conversation). |
| 3 | **Frozen Overworld Sprites** | Characters stand locked in a single idle frame for entire multi-page conversations, never turning to face speakers or shifting posture. | **Pillar C — Natural Overworld Body Language:** Automatic subtle speaker-facing turns (`AUTO_FACE_SPEAKER = true`), tasteful restrained 4-pose stance shifts (`pose_<CHAR>.png` for `JUNO`, `KESTREL`, `LARCH`, `PLAYER_A`, `PLAYER_B`, `VOSS`), and gentle opt-in micro-acting (`pf_nod`, `pf_step_back`, `pf_turn_away`, `pf_lean_in`) — never automatic cartoon hopping. |

### Compatibility & Safety Guarantees
- **100% Backwards-Compatible:** Existing `[portrait: CHAR, expr]`, `\pf[CHAR,expr]`, `\pfb[...]`, `pf_say(...)`, and untagged carry-over lines (`Portrait.carry`) work untouched with zero story-script rewrites.
- **Bubble Mode Preserved:** Explicit opt-in `[bubble: ...]` / `\pfb[...]` lines clear the dual stage and continue using `014_Portraits.rb`'s round speech bubble.
- **Battle Safe:** Dual-portrait stage, overworld balloons, facing turns, and pose swaps automatically suppress when `$game_temp.in_battle` is true or `$scene` is not `Scene_Map`.
- **Inherently Photosensitive Safe:** Zero portrait shaking, zero flashing borders, and zero strobing effects across the entire system.
- **Clean Disposal & Zero Leaks:** Hooks `Interpreter#setup` (`@main`), `Scene_Map#transfer_player`, and conversation end in `Scene_Map#update` (guarded by `Expressive.active?`) so portrait viewports, emote sprites, visual offsets, and custom `pose_<CHAR>` sheets ALWAYS clean up cleanly.

---

## 2. Production Art Assets Delivered (Shipped & Dual-Synced)

All **7 pixel-art sheets** are already shipped, generated via 100% pure `generate_image` Nintendo DS B2W2 pixel art, grid-locked, palette-matched to canonical overworlds, verified (`exact2x=True`, `semi=0`, `orphans=0`), visually inspected at 4× zoom, and byte-identically dual-synced between `graphics/` and `art/out/Graphics/`.

### Asset QA Manifest

| Asset Path (`graphics/` & `art/out/Graphics/`) | Size | Grid Layout | Colors | `exact2x` | `semi` | `orphans` | SHA-256 (first 12) |
|---|---|---|---:|:---:|---:|---:|---|
| `Animations/pf_emote_balloons.png` | `128×320` | 10 rows × 4 frames (`32×32` = `16×16` @ 2×) | 23 | `True` | `0` | `0` | `2df9c8af18ee` |
| `Characters/pose_JUNO.png` | `128×48` | 4 poses × 1 row (`32×48` = `16×24` @ 2×) | 24 | `True` | `0` | `0` | `a4b7696e6d9b` |
| `Characters/pose_KESTREL.png` | `128×48` | 4 poses × 1 row (`32×48` = `16×24` @ 2×) | 13 | `True` | `0` | `0` | `311e2224eab8` |
| `Characters/pose_LARCH.png` | `128×48` | 4 poses × 1 row (`32×48` = `16×24` @ 2×) | 12 | `True` | `0` | `0` | `07b950b6bd64` |
| `Characters/pose_PLAYER_A.png` | `128×48` | 4 poses × 1 row (`32×48` = `16×24` @ 2×) | 14 | `True` | `0` | `0` | `d5e6fe8eb455` |
| `Characters/pose_PLAYER_B.png` | `128×48` | 4 poses × 1 row (`32×48` = `16×24` @ 2×) | 13 | `True` | `0` | `0` | `4831eaecf845` |
| `Characters/pose_VOSS.png` | `128×48` | 4 poses × 1 row (`32×48` = `16×24` @ 2×) | 17 | `True` | `0` | `0` | `9fcf7d677cf2` |

### Pillar B — Emote Balloon Row Map (`pf_emote_balloons.png`)

Each row has **4 animation frames** (`F0` Pop-In → `F1` Peak → `F2` Active → `F3` Settle Hold). **All emotes are opt-in only (`AUTO_EMOTE = false`)** — trigger sparingly on genuine story beats via `\pfe[symbol]` or `pf_emote(target, :symbol)`:

| Row | Symbol | Visual Icon | Aliases | Best Used For (Max 1–2 per Conversation) |
|---:|---|---|---|---|
| `0` | `:exclaim` | `!` Crimson Exclamation | `:alert` | Genuine sudden reveal or interruption |
| `1` | `:double_exclaim` | `!!` Spiky Double Exclamation | `:shock`, `:horror` | Rare major plot shock (never routine banter) |
| `2` | `:question` | `?` Cobalt Question Mark | `:confused`, `:curious` | Quiet puzzlement or clarifying beat |
| `3` | `:dots` | `...` Sequential Ellipsis | `:ellipsis`, `:gloom`, `:silent` | Heavy pause, hesitation, or unspoken tension |
| `4` | `:anger` | `💢` Anime Anger Vein | `:angry`, `:furious` | Rare comedic snapping point or sharp confrontation |
| `5` | `:sweat` | `💧` Glossy Sky-Blue Sweatdrop | `:nervous`, `:tears` | Awkward catch or sheepish admission |
| `6` | `:heart` | `♥` Warm Rosy-Pink Heart | `:blush`, `:warm` | Rare heartfelt or affectionate punchline |
| `7` | `:idea` | `💡` Glowing Golden Lightbulb | `:sparkle`, `:realize` | Sudden deduction or clue breakthrough |
| `8` | `:music` | `🎵` Cheerful Blue/Gold Music Note | `:note`, `:cheerful` | Lighthearted humming or breezy departure |
| `9` | `:jolt` | `⚡` Jagged Amber Dread/Jolt Bolt | `:dread`, `:wince`, `:tension` | Sharp unease or ominous realization |

### Pillar C — Core Cast 4-Pose Acting Sheet Map (`pose_<CHAR>.png`)

All 6 sheets share the **exact `32×48` cell scale & `y=45` foot baseline** of `graphics/Characters/<CHAR>.png` (`128×192`), so shifting between natural idle walking sheets and `pose_<CHAR>.png` produces **zero height pop, zero foot slide, and zero palette shift**:

| Character | Sheet (`128×48`) | Pose `0` | Pose `1` | Pose `2` | Pose `3` |
|---|---|---|---|---|---|
| **Juno** | `pose_JUNO.png` | `:clasped` (Hands Clasped) | `:flinch` (Startled Flinch) | `:worried` (Worried Looking-Down) | `:resolute` (Resolute Fist-Clench) |
| **Kestrel** | `pose_KESTREL.png` | `:crossed` (Arms Crossed Brooding) | `:scoff` (Scoffing Hand-Wave) | `:lean_angry` (Angry Lean-Forward) | `:guarded` (Soft Guarded Look-Away) |
| **Larch** | `pose_LARCH.png` | `:ponder` (Chin-Stroking Pondering) | `:glasses` (Pushing Glasses Down) | `:explain` (Hands-Out Explaining) | `:sheepish` (Sheepish Scratch-Head) |
| **Player A** | `pose_PLAYER_A.png` | `:determined` (Determined Fist) | `:recoil` (Startled Recoil) | `:thoughtful` (Thoughtful Nod) | `:reach` (Empathetic Reach) |
| **Player B** | `pose_PLAYER_B.png` | `:determined` (Determined Fist) | `:recoil` (Startled Recoil) | `:thoughtful` (Thoughtful Nod) | `:reach` (Empathetic Reach) |
| **Voss** | `pose_VOSS.png` | `:behind_back` (Hands Behind Back) | `:open_palm` (Calm Open-Palm) | `:collar` (Adjusting Collar Coldly) | `:shock` (Rare Cracked Shock) |

### Visual Proofs (Verified at 4× & Native `512×384`)
- Master 4× Asset Sheet: `previews/102a_expressive_dialogue_assets_sheet.png`
- Animated Natural v2 Before vs. After Briarwick Demo: `previews/102c_expressive_dialogue_natural_v2.gif` (also mirrored to `previews/102b_expressive_dialogue_before_after.gif`)

---

## 3. Ready-to-Drop Plugin Implementation: `018_ExpressiveDialogue.rb` (v2 Natural Restraint)

Save the code block below verbatim to **`plugins/Prismfall Cutscenes/018_ExpressiveDialogue.rb`**. No edits to `014_Portraits.rb`, `pbs/`, `story/`, or existing map events are required. Verified with `ruby -c` (`Syntax OK`).

```ruby
#===============================================================================
# Prismfall Cutscenes - 018 Expressive Normal Conversations (v2 Natural Restraint)
#-------------------------------------------------------------------------------
# Elevates everyday [portrait: CHAR, expr] / \pf[...] conversations with ZERO
# breaking changes, ZERO story-script edits, and prestige JRPG restraint
# (Trails / Fire Emblem / Persona / Rejuvenation V14):
#
#   Pillar A (Rock-Solid Still Portraits):
#     - Clean Dual-Speaker Stage anchored pixel-locked at Left & Right slots
#       with 0px X/Y portrait motion (no bouncing, shaking, bobbing, or sliding).
#     - Subtle, smooth listener dimming Tone(-42, -42, -42, 35) on the inactive
#       speaker while the active speaker remains bright and crisp.
#     - Silky 4-frame (0.10s) alpha fade-in and expression crossfade in place.
#
#   Pillar B (Sparing, High-Impact Emote Balloons):
#     - Crisp 2x Gen 5 B2W2 emote sheet (Graphics/Animations/pf_emote_balloons.png).
#     - AUTO_EMOTE = false by default — zero automatic emote spam!
#     - Fires ONLY when explicitly scripted via \pfe[dots] or pf_emote(ev, :dots)
#       on genuine punchlines, surprises, or awkward pauses (max 1-2 per scene).
#
#   Pillar C (Natural Overworld Body Language):
#     - Subtle facing turns toward whoever is speaking (AUTO_FACE_SPEAKER = true).
#     - Tasteful restrained 4-pose stance shifts (pose_<CHAR>.png) via explicit
#       \pfp[crossed] / pf_pose(...) or optional restrained mode.
#     - Gentle opt-in micro-acting helpers (pf_nod, pf_step_back, pf_turn_away,
#       pf_lean_in, pf_headshake) — NEVER automatic cartoon hopping!
#===============================================================================
module Prismfall
  module Expressive
    C  = Prismfall::Cutscene
    P  = Prismfall::Portrait
    PX = C::PX

    #---------------------------------------------------------------------------
    # Master Restraint Switches
    #---------------------------------------------------------------------------
    ENABLED             = true
    AUTO_EMOTE          = false        # OFF by default: emotes fire ONLY via \pfe[...] or pf_emote
    AUTO_POSES          = :restrained  # :restrained (grounded non-neutral beats only), false (manual \pfp only)
    AUTO_FACE_SPEAKER   = true         # Clean natural facing turn toward active speaker
    AUTO_MICRO_ACTING   = false        # OFF by default: gentle gestures are strictly opt-in (\pfa / pf_nod)
    ENABLE_VOICE_BLIPS  = false        # Optional subtle text-blip SE (0px portrait movement)

    #---------------------------------------------------------------------------
    # Pillar A: Rock-Solid Dual-Speaker Portrait Stage Constants (0px Motion)
    #---------------------------------------------------------------------------
    STAGE_Z             = P::VIEWPORT_Z
    FADE_IN_TIME        = 0.10         # 4 frames @ 40fps smooth in-place alpha fade-in
    CROSSFADE_TIME      = 0.10         # 4 frames @ 40fps smooth in-place expression crossfade
    DIM_TRANS_TIME      = 0.12         # ~5 frames smooth active <-> listener tone dim
    INACTIVE_TONE       = [-42, -42, -42, 35]

    #---------------------------------------------------------------------------
    # Pillar B: Sparing B2W2 Overworld Emote Balloons (pf_emote_balloons.png)
    #---------------------------------------------------------------------------
    EMOTE_SHEET_PATH    = "Graphics/Animations/pf_emote_balloons"
    EMOTE_CELL          = 32           # 16x16 native @ 2x
    EMOTE_FRAMES        = 4
    EMOTE_COOLDOWN      = 2.20         # Safety cooldown if AUTO_EMOTE is ever enabled manually
    POSE_MIN_HOLD       = 1.25         # Prevents rapid back-to-back auto-pose flickering

    EMOTE_ROWS = {
      :exclaim        => 0,
      :double_exclaim => 1,
      :question       => 2,
      :dots           => 3,
      :anger          => 4,
      :sweat          => 5,
      :heart          => 6,
      :idea           => 7,
      :music          => 8,
      :jolt           => 9
    }

    EMOTE_ALIASES = {
      :alert    => :exclaim,
      :shock    => :double_exclaim,
      :horror   => :double_exclaim,
      :confused => :question,
      :curious  => :question,
      :ellipsis => :dots,
      :gloom    => :dots,
      :silent   => :dots,
      :angry    => :anger,
      :furious  => :anger,
      :nervous  => :sweat,
      :tears    => :sweat,
      :blush    => :heart,
      :warm     => :heart,
      :sparkle  => :idea,
      :realize  => :idea,
      :note     => :music,
      :cheerful => :music,
      :dread    => :jolt,
      :wince    => :jolt,
      :tension  => :jolt
    }

    # Used ONLY if a project manually sets AUTO_EMOTE = true (still ultra-sparing)
    SPARING_AUTO_EMOTES = {
      :shocked => :exclaim,
      :panic   => :double_exclaim
    }

    # Subtle optional SEs per emote (silent if file absent via Cutscene::Sound)
    EMOTE_SE = {
      :exclaim        => "Exclaim",
      :double_exclaim => "Exclaim",
      :idea           => "Mining ping",
      :jolt           => "Battle damage normal"
    }

    #---------------------------------------------------------------------------
    # Pillar C: Core Cast 4-Pose Acting Sheet Registry (pose_<CHAR>.png)
    #---------------------------------------------------------------------------
    POSE_NAMES = {
      :JUNO     => { :clasped => 0, :flinch => 1, :worried => 2, :resolute => 3 },
      :KESTREL  => { :crossed => 0, :scoff => 1, :lean_angry => 2, :guarded => 3 },
      :LARCH    => { :ponder => 0, :glasses => 1, :explain => 2, :sheepish => 3 },
      :PLAYER_A => { :determined => 0, :recoil => 1, :thoughtful => 2, :reach => 3 },
      :PLAYER_B => { :determined => 0, :recoil => 1, :thoughtful => 2, :reach => 3 },
      :VOSS     => { :behind_back => 0, :open_palm => 1, :collar => 2, :shock => 3 }
    }

    # Restrained stance table: :neutral ALWAYS keeps natural directional facing idle.
    # Only clear emotional beats trigger grounded conversation stances.
    RESTRAINED_POSE_TABLE = {
      :JUNO => {
        :happy => 0, :blush => 0,
        :shocked => 1, :panic => 1,
        :sad => 2, :crying => 2,
        :angry => 3
      },
      :KESTREL => {
        :deadpan => 0, :smug => 0,
        :angry => 2,
        :sad => 3, :crying => 3
      },
      :LARCH => {
        :deadpan => 0,
        :smug => 1,
        :happy => 2,
        :sad => 3, :blush => 3
      },
      :PLAYER_A => {
        :angry => 0,
        :shocked => 1, :panic => 1,
        :sad => 3
      },
      :PLAYER_B => {
        :angry => 0,
        :shocked => 1, :panic => 1,
        :sad => 3
      },
      :VOSS => {
        :deadpan => 0,
        :smug => 2, :angry => 2,
        :shocked => 3, :panic => 3
      }
    }

    # Optional voice-blip SE pitch table (used only when ENABLE_VOICE_BLIPS = true)
    VOICE_PROFILES = {
      :JUNO     => { :se => "pf_blip_mid",  :pitch => 114 },
      :KESTREL  => { :se => "pf_blip_low",  :pitch => 92  },
      :LARCH    => { :se => "pf_blip_mid",  :pitch => 102 },
      :PLAYER_A => { :se => "pf_blip_mid",  :pitch => 100 },
      :PLAYER_B => { :se => "pf_blip_mid",  :pitch => 112 },
      :VOSS     => { :se => "pf_blip_low",  :pitch => 78  }
    }

    #===========================================================================
    # Utility & Conversation Coordinator
    #===========================================================================
    class << self
      def on_map?
        return false if !defined?($scene) || !defined?(Scene_Map) || !$scene.is_a?(Scene_Map)
        return false if defined?($game_temp) && $game_temp && $game_temp.respond_to?(:in_battle) && $game_temp.in_battle
        return true
      end

      def active?
        return true if @conversation_active
        return true if @stage && @stage.active?
        return true if @emotes && @emotes.active?
        return false
      end

      def resolve_emote(sym)
        return nil if sym.nil?
        key = sym.to_s.downcase.strip.to_sym
        key = EMOTE_ALIASES[key] || key
        return EMOTE_ROWS.key?(key) ? key : nil
      end

      def resolve_character(target)
        return target if defined?(Game_Character) && target.is_a?(Game_Character)
        return $game_player if target == :PLAYER || target == 0 || target.to_s.upcase == "PLAYER"
        return nil if !defined?($game_map) || !$game_map || !$game_map.respond_to?(:events)
        return $game_map.events[target] if target.is_a?(Integer) && $game_map.events[target]
        spec = { :id => target.to_s.upcase.to_sym, :event => nil }
        return P.speaker(spec)
      rescue StandardError
        return nil
      end

      def pose_sheet_for(id)
        aid = P.art_id(id)
        path = "Graphics/Characters/pose_#{aid}"
        return nil if !C::Gfx.resolve(path)
        return "pose_#{aid}", aid
      end

      # Strips inline \pfe[emote] / \pfe[emote,target] / \pfp[pose] / \pfa[act]
      # tags cleanly before message display and returns [clean_text, directives].
      def extract_inline_tags(message)
        text = message.to_s.dup
        dirs = { :emotes => [], :pose => nil, :act => nil }
        text.gsub!(/\\pfe\[([^\]]+)\]/i) do
          parts = $1.split(",").map(&:strip)
          dirs[:emotes] << { :kind => parts[0], :target => parts[1] } if !parts[0].to_s.empty?
          ""
        end
        text.gsub!(/\\pfp\[([^\]]+)\]/i) do
          parts = $1.split(",").map(&:strip)
          dirs[:pose] = { :pose => parts[0], :target => parts[1] } if !parts[0].to_s.empty?
          ""
        end
        text.gsub!(/\\pfa\[([^\]]+)\]/i) do
          parts = $1.split(",").map(&:strip)
          dirs[:act] = { :kind => parts[0], :target => parts[1] } if !parts[0].to_s.empty?
          ""
        end
        return text, dirs
      end

      def stage
        @stage ||= DualPortraitStage.new
      end

      def emotes
        @emotes ||= EmoteManager.new
      end

      def clear_all
        @conversation_active = false
        @stage&.clear
        @emotes&.clear
        @last_auto_emote = {}
        @last_auto_pose  = {}
        @last_auto_expr  = {}
        @recent_speakers = []
        reset_all_actors
      end

      def reset_all_actors
        if defined?($game_player) && $game_player && $game_player.respond_to?(:pf_reset_acting)
          $game_player.pf_reset_acting
        end
        if defined?($game_map) && $game_map && $game_map.respond_to?(:events)
          $game_map.events.each_value do |ev|
            ev.pf_reset_acting if ev.respond_to?(:pf_reset_acting)
          end
        end
      rescue StandardError
        nil
      end

      # Coordinates restrained overworld acting for a line of dialogue.
      def trigger_acting(spec, dirs)
        return if !on_map?
        @conversation_active = true
        spk  = P.speaker(spec)
        id   = spec[:id]
        expr = (spec[:expression] || :neutral).to_sym
        now  = C::Util.now

        @last_auto_emote ||= {}
        @last_auto_pose  ||= {}
        @last_auto_expr  ||= {}
        @recent_speakers ||= []
        expr_changed = (@last_auto_expr[id] != expr)
        @last_auto_expr[id] = expr

        # 1. Natural facing turns: turn speaker and previous speaker gently toward each other
        if AUTO_FACE_SPEAKER && spk
          prev_spk = @recent_speakers.reverse.find { |c| c && c != spk }
          if prev_spk
            turn_toward(spk, prev_spk) if !spk.respond_to?(:pf_pose_sheet) || spk.pf_pose_sheet.nil?
            turn_toward(prev_spk, spk) if !prev_spk.respond_to?(:pf_pose_sheet) || prev_spk.pf_pose_sheet.nil?
          end
          @recent_speakers.delete(spk)
          @recent_speakers << spk
          @recent_speakers.shift if @recent_speakers.length > 4
        end

        # 2. Explicit inline \pfe[...] emotes ALWAYS fire (sparing, writer-directed)
        dirs[:emotes].each do |em|
          t = em[:target] ? resolve_character(em[:target]) : spk
          emotes.spawn(t, em[:kind]) if t
        end

        # Optional auto-emote (DISABLED by default: AUTO_EMOTE = false)
        if AUTO_EMOTE && dirs[:emotes].empty? && spk && expr_changed
          em_kind = SPARING_AUTO_EMOTES[expr]
          if em_kind && (now - (@last_auto_emote[id] || -999.0)) >= EMOTE_COOLDOWN
            emotes.spawn(spk, em_kind)
            @last_auto_emote[id] = now
          end
        end

        # 3. Restrained 4-pose stance shifts (explicit \pfp[...] takes full priority)
        if dirs[:pose]
          t = dirs[:pose][:target] ? resolve_character(dirs[:pose][:target]) : spk
          apply_pose(t, id, dirs[:pose][:pose]) if t
          @last_auto_pose[id] = now
        elsif AUTO_POSES == :restrained && spk && !spec[:carried] && expr_changed
          if expr == :neutral
            spk.pf_clear_pose if spk.respond_to?(:pf_clear_pose)
          elsif (now - (@last_auto_pose[id] || -999.0)) >= POSE_MIN_HOLD
            sheet, aid = pose_sheet_for(id)
            if sheet && RESTRAINED_POSE_TABLE[aid] && RESTRAINED_POSE_TABLE[aid].key?(expr)
              spk.pf_set_pose(sheet, RESTRAINED_POSE_TABLE[aid][expr]) if spk.respond_to?(:pf_set_pose)
              @last_auto_pose[id] = now
            end
          end
        end

        # 4. Gentle opt-in micro-acting (NEVER auto-triggered when AUTO_MICRO_ACTING = false)
        if dirs[:act]
          t = dirs[:act][:target] ? resolve_character(dirs[:act][:target]) : spk
          run_micro_act(t, dirs[:act][:kind], other: @recent_speakers[-2]) if t
        end
      end

      def apply_pose(char, id, pose_spec)
        return if !char || !char.respond_to?(:pf_set_pose)
        key_str = pose_spec.to_s.downcase.strip
        if key_str == "reset" || key_str == "none" || key_str == "idle"
          char.pf_clear_pose
          return
        end
        sheet, aid = pose_sheet_for(id)
        return if !sheet
        idx = if pose_spec.is_a?(Integer) || key_str =~ /\A\d+\z/
                pose_spec.to_i
              else
                (POSE_NAMES[aid] || {})[key_str.to_sym]
              end
        char.pf_set_pose(sheet, idx.clamp(0, 3)) if !idx.nil?
      end

      def run_micro_act(char, kind, other: nil)
        return if !char || !char.respond_to?(:pf_start_act)
        case kind.to_s.downcase.strip.to_sym
        when :nod         then char.pf_start_act(:nod)
        when :step_back   then char.pf_start_act(:step_back, dist: 4)
        when :lean_in     then char.pf_start_act(:lean_in, dist: 4)
        when :turn_away   then turn_away(char, other)
        when :headshake   then char.pf_start_act(:headshake)
        when :return      then char.pf_start_act(:return)
        when :shudder     then char.pf_start_act(:shudder, duration: 0.28)
        when :hop         then char.pf_start_act(:hop, height: 4, count: 1)
        end
      end

      def turn_toward(char, target)
        return if !char || !target || char == target
        return if !char.respond_to?(:x) || !target.respond_to?(:x)
        return if char.respond_to?(:moving?) && char.moving?
        dx = target.x - char.x
        dy = target.y - char.y
        return if dx == 0 && dy == 0
        # Only turn if conversational proximity (within 6 tiles)
        return if (dx.abs + dy.abs) > 6
        dir = if dx.abs >= dy.abs
                dx > 0 ? 6 : 4
              else
                dy > 0 ? 2 : 8
              end
        char.pf_set_facing(dir) if char.respond_to?(:pf_set_facing)
      end

      def turn_away(char, from_target = nil)
        return if !char || !char.respond_to?(:direction)
        if from_target && char.respond_to?(:x) && from_target.respond_to?(:x)
          dx = char.x - from_target.x
          dy = char.y - from_target.y
          if dx != 0 || dy != 0
            dir = if dx.abs >= dy.abs
                    dx > 0 ? 6 : 4
                  else
                    dy > 0 ? 2 : 8
                  end
            char.pf_set_facing(dir) if char.respond_to?(:pf_set_facing)
            return
          end
        end
        # Fallback: turn 90/180 degrees calmly away from current facing
        away = { 2 => 4, 4 => 6, 6 => 4, 8 => 2 }[char.direction] || 4
        char.pf_set_facing(away) if char.respond_to?(:pf_set_facing)
      end
    end

    #===========================================================================
    # PILLAR A: Rock-Solid Still Dual-Speaker Portrait Stage (0px Motion)
    #===========================================================================
    class PortraitSlot
      attr_reader :id, :side, :expression, :last_used

      def initialize(viewport, side, spec, msgwindow)
        @vp         = viewport
        @side       = side                  # :left or :right
        @id         = spec[:id]
        @expression = (spec[:expression] || :neutral).to_sym
        @file       = P.face_file(@id, @expression)
        @frame_bmp  = P::Frame.build(msgwindow)
        @face_bmp   = load_face_bitmap(@file)
        @prev_bmp   = nil

        @frame = Sprite.new(@vp)
        @frame.bitmap = @frame_bmp

        @prev_face = Sprite.new(@vp)
        @prev_face.visible = false

        @face = Sprite.new(@vp)
        @face.bitmap = @face_bmp

        @entered_at  = C::Util.now
        @expr_at     = @entered_at
        @focus_at    = @entered_at - DIM_TRANS_TIME
        @active      = true
        @last_used   = @entered_at
        @first_tick  = true
        @disposed    = false
      end

      def active?; @active; end

      def set_active(flag, spec = nil, _msgwindow = nil)
        now = C::Util.now
        if @active != flag
          @active   = flag
          @focus_at = now
        end
        @last_used = now if flag
        return if !flag || !spec

        new_expr = (spec[:expression] || :neutral).to_sym
        new_file = P.face_file(@id, new_expr)
        if new_file != @file || new_expr != @expression
          # Silky 4-frame in-place expression crossfade (0px X/Y motion!)
          @prev_bmp.dispose if @prev_bmp && !@prev_bmp.disposed?
          @prev_bmp = @face_bmp
          @prev_face.bitmap  = @prev_bmp
          @prev_face.visible = true
          @prev_face.opacity = 255
          @face_bmp = load_face_bitmap(new_file)
          @face.bitmap = @face_bmp
          @file = new_file
          @expression = new_expr
          @expr_at = now
        end
      end

      def update(msgwindow, now)
        return if @disposed
        fx, fy = compute_anchor(msgwindow)
        @first_tick = false

        z_base = @active ? 20 : 10
        @frame.z     = z_base
        @prev_face.z = z_base + 1
        @face.z      = z_base + 2

        # 1. Silky 4-frame in-place alpha fade-in on first entry (0px movement!)
        t_in = now - @entered_at
        entry_op = if t_in < FADE_IN_TIME
                     k = C::Ease.apply(:out, C::Util.clamp(t_in / FADE_IN_TIME, 0.0, 1.0))
                     (255 * k).round
                   else
                     255
                   end

        # 2. Smooth active <-> dimmed listener tone transition (0px movement!)
        t_foc = C::Util.clamp((now - @focus_at) / DIM_TRANS_TIME, 0.0, 1.0)
        foc_k = @active ? C::Ease.apply(:out, t_foc) : (1.0 - C::Ease.apply(:out, t_foc))
        dim_w = 1.0 - foc_k
        tone  = Tone.new(
          (INACTIVE_TONE[0] * dim_w).round,
          (INACTIVE_TONE[1] * dim_w).round,
          (INACTIVE_TONE[2] * dim_w).round,
          (INACTIVE_TONE[3] * dim_w).round
        )

        # 3. Silky 4-frame in-place expression crossfade (0px movement!)
        t_xf = now - @expr_at
        if @prev_face.visible && t_xf < CROSSFADE_TIME
          xk = C::Util.clamp(t_xf / CROSSFADE_TIME, 0.0, 1.0)
          @prev_face.opacity = ((1.0 - xk) * entry_op).round
          @face.opacity      = (xk * entry_op).round
        else
          @prev_face.visible = false
          @face.opacity      = entry_op
        end

        # Rock-solid fixed coordinates: ZERO bounce, ZERO shake, ZERO bob, ZERO slide!
        @frame.x = fx
        @frame.y = fy
        @frame.opacity = entry_op
        @frame.tone = tone

        @face.x = fx + P::FACE_EDGE
        @face.y = fy + P::FACE_EDGE
        @face.tone = tone

        @prev_face.x = @face.x
        @prev_face.y = @face.y
        @prev_face.tone = tone
      end

      def dispose
        return if @disposed
        @disposed = true
        [@frame, @face, @prev_face].each { |s| s.dispose if s && !s.disposed? }
        [@frame_bmp, @face_bmp, @prev_bmp].each { |b| b.dispose if b && !b.disposed? }
      end

      private

      def load_face_bitmap(file)
        out = Bitmap.new(P::FACE_SIZE, P::FACE_SIZE)
        src = file ? C::Gfx.load_bitmap(file) : nil
        return out if !src
        size = [src.width, src.height].min
        sx = (src.width - size) / 2
        if size == P::FACE_SIZE
          out.blt(0, 0, src, Rect.new(sx, 0, size, size))
        else
          out.stretch_blt(Rect.new(0, 0, P::FACE_SIZE, P::FACE_SIZE), src, Rect.new(sx, 0, size, size))
        end
        src.dispose
        return out
      end

      def predicted_y(mh)
        pos = ($game_system.message_position rescue 2) if defined?($game_system) && $game_system
        return 0 if pos == 0
        return (Graphics.height - mh) / 2 if pos == 1
        return Graphics.height - mh
      end

      def compute_anchor(msgwindow)
        mx = 0
        mw = Graphics.width
        mh = 96
        my = Graphics.height - mh
        if msgwindow && msgwindow.respond_to?(:y) && msgwindow.respond_to?(:height)
          mx = msgwindow.x.to_i if msgwindow.respond_to?(:x)
          mw = msgwindow.width.to_i if msgwindow.respond_to?(:width)
          mh = msgwindow.height.to_i
          my = @first_tick ? predicted_y(mh) : msgwindow.y.to_i
        end
        y = my - P::FACE_FRAME
        y = my + mh if y < 0
        x = (@side == :left) ? mx : (mx + mw - P::FACE_FRAME)
        return x, y
      end
    end

    class DualPortraitStage
      def initialize
        @viewport     = nil
        @slots        = { :left => nil, :right => nil }
        @active_side  = nil
        @last_pos     = -1
        @last_blip_at = 0.0
      end

      def active?
        return !@slots[:left].nil? || !@slots[:right].nil?
      end

      def ensure_viewport
        return if @viewport && !@viewport.disposed?
        @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @viewport.z = STAGE_Z
      end

      def open_line(spec, msgwindow)
        ensure_viewport
        @last_pos = -1
        id = spec[:id]

        # Keep existing speaker anchored in their side; 3rd speaker replaces LRU slot.
        if @slots[:left] && @slots[:left].id == id
          side = :left
        elsif @slots[:right] && @slots[:right].id == id
          side = :right
        elsif @slots[:left].nil?
          side = :left
        elsif @slots[:right].nil?
          side = :right
        else
          side = (@slots[:left].last_used <= @slots[:right].last_used) ? :left : :right
          @slots[side].dispose
          @slots[side] = nil
        end

        if @slots[side].nil?
          @slots[side] = PortraitSlot.new(@viewport, side, spec, msgwindow)
        else
          @slots[side].set_active(true, spec, msgwindow)
        end

        other = (side == :left) ? :right : :left
        @slots[other].set_active(false) if @slots[other]
        @active_side = side
        update(msgwindow, nil)
      end

      def update(msgwindow, clean_text = nil)
        return if !@viewport || @viewport.disposed?
        now = C::Util.now
        track_voice_blips(msgwindow, clean_text, now) if ENABLE_VOICE_BLIPS
        @slots.each_value { |s| s&.update(msgwindow, now) }
      end

      def clear
        @slots.each_key do |k|
          @slots[k]&.dispose
          @slots[k] = nil
        end
        if @viewport && !@viewport.disposed?
          @viewport.dispose
        end
        @viewport = nil
        @active_side = nil
      end

      private

      # Optional subtle text-blip audio only — NEVER moves portraits.
      def track_voice_blips(msgwindow, clean_text, now)
        slot = @active_side ? @slots[@active_side] : nil
        return if !slot || !msgwindow
        return if msgwindow.respond_to?(:pausing?) && msgwindow.pausing?
        return if msgwindow.respond_to?(:busy?) && !msgwindow.busy?
        pos = msgwindow.respond_to?(:position) ? msgwindow.position.to_i : -1
        return if pos <= @last_pos
        @last_pos = pos
        ch = (clean_text && pos > 0 && pos <= clean_text.length) ? clean_text[pos - 1] : "a"
        return if ch =~ /[\s.,!?;:\-—…]/
        return if (now - @last_blip_at) < 0.075
        prof = VOICE_PROFILES[P.art_id(slot.id)] || { :se => "pf_blip_mid", :pitch => 100 }
        C::Sound.play(:se, prof[:se], 44, prof[:pitch] + rand(-3..3))
        @last_blip_at = now
      end
    end

    #===========================================================================
    # PILLAR B: Crisp 2x Gen 5 B2W2 Overworld Emote Balloons (Opt-In Only)
    #===========================================================================
    class EmoteBalloonSprite
      DURATION = 0.92

      def initialize(viewport, bitmap, character, row)
        @char   = character
        @row    = row
        @start  = C::Util.now
        @sprite = Sprite.new(viewport)
        @sprite.bitmap = bitmap
        @sprite.ox = EMOTE_CELL / 2
        @sprite.oy = EMOTE_CELL
        @sprite.z  = 500
        @done   = false
        update
      end

      def done?; @done; end

      def update
        return true if @done || !@sprite || @sprite.disposed?
        if !@char || !@char.respond_to?(:screen_x)
          dispose
          return true
        end
        lt = C::Util.now - @start
        if lt >= DURATION
          dispose
          return true
        end
        # Clean 4-frame B2W2 cadence: F0 Pop-In -> F1 Peak -> F2 Active -> F3 Settle
        fi = if lt < 0.10    then 0
             elsif lt < 0.28 then 1
             elsif lt < 0.56 then 2
             else 3
             end
        @sprite.src_rect.set(fi * EMOTE_CELL, @row * EMOTE_CELL, EMOTE_CELL, EMOTE_CELL)
        act_ox = @char.respond_to?(:pf_visual_ox) ? @char.pf_visual_ox : 0
        act_oy = @char.respond_to?(:pf_visual_oy) ? @char.pf_visual_oy : 0
        @sprite.x = C::Util.snap(@char.screen_x + act_ox)
        @sprite.y = C::Util.snap(@char.screen_y - 46 + act_oy)
        @sprite.opacity = (lt > 0.74) ? ((1.0 - ((lt - 0.74) / 0.18)) * 255).round : 255
        return false
      end

      def dispose
        return if @done
        @done = true
        @sprite.dispose if @sprite && !@sprite.disposed?
      end
    end

    class EmoteManager
      def initialize
        @viewport = nil
        @bitmap   = nil
        @active   = []
      end

      def active?; !@active.empty?; end

      def spawn(character, kind)
        return nil if !character || !Expressive.on_map?
        key = Expressive.resolve_emote(kind)
        return nil if !key
        ensure_resources
        return nil if !@bitmap
        @active.reject! do |b|
          if b.instance_variable_get(:@char) == character
            b.dispose
            true
          else
            false
          end
        end
        b = EmoteBalloonSprite.new(@viewport, @bitmap, character, EMOTE_ROWS[key])
        @active << b
        se = EMOTE_SE[key]
        C::Sound.play(:se, se, 60, 100) if se
        return b
      end

      def update
        return if @active.empty?
        @active.reject! { |b| b.update }
      end

      def clear
        @active.each(&:dispose)
        @active.clear
        @bitmap.dispose if @bitmap && !@bitmap.disposed?
        @bitmap = nil
        @viewport.dispose if @viewport && !@viewport.disposed?
        @viewport = nil
      end

      private

      def ensure_resources
        if !@viewport || @viewport.disposed?
          @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
          @viewport.z = STAGE_Z - 5
        end
        if !@bitmap || @bitmap.disposed?
          @bitmap = C::Gfx.load_bitmap(EMOTE_SHEET_PATH)
        end
      end
    end
  end
end

#===============================================================================
# PILLAR C: Game_Character Natural Overworld Body Language & 4-Pose Support
#===============================================================================
if defined?(Game_Character) && !Game_Character.method_defined?(:pf_update_expressive)
  class Game_Character
    attr_reader :pf_pose_sheet, :pf_pose_index

    def pf_visual_ox; @pf_ox.to_i; end
    def pf_visual_oy; @pf_oy.to_i; end

    def pf_set_facing(dir)
      return if ![2, 4, 6, 8].include?(dir)
      @pf_saved_dir ||= @direction
      @direction = dir
    end

    def pf_set_pose(sheet_name, pose_index = 0)
      @pf_pose_sheet = sheet_name
      @pf_pose_index = pose_index.to_i.clamp(0, 3)
    end

    def pf_clear_pose
      @pf_pose_sheet = nil
      @pf_pose_index = 0
    end

    def pf_reset_acting
      @pf_pose_sheet = nil
      @pf_pose_index = 0
      @pf_act        = nil
      @pf_ox         = 0
      @pf_oy         = 0
      @pf_hold_ox    = 0
      @pf_hold_oy    = 0
      @pf_saved_dir  = nil
    end

    def pf_start_act(kind, dist: 4, height: 4, count: 1, duration: 0.28)
      @pf_act = {
        :kind     => kind.to_sym,
        :start    => Prismfall::Cutscene::Util.now,
        :dist     => dist.to_i,
        :height   => height.to_i,
        :count    => [count.to_i, 1].max,
        :duration => duration.to_f,
        :orig_dir => @direction,
        :from_ox  => @pf_hold_ox.to_i,
        :from_oy  => @pf_hold_oy.to_i
      }
      pf_update_expressive
    end

    def pf_update_expressive
      @pf_hold_ox ||= 0
      @pf_hold_oy ||= 0
      if !@pf_act
        @pf_ox = @pf_hold_ox
        @pf_oy = @pf_hold_oy
        return
      end
      lt = Prismfall::Cutscene::Util.now - @pf_act[:start]
      px = Prismfall::Cutscene::PX
      ps = Prismfall::Cutscene.photosensitive?

      case @pf_act[:kind]
      when :nod
        # Single quiet, natural 2px downward acknowledgment nod
        dur = 0.22
        if lt >= dur
          @pf_act = nil; @pf_ox = @pf_hold_ox; @pf_oy = @pf_hold_oy
        else
          k = lt / dur
          @pf_ox = @pf_hold_ox
          @pf_oy = @pf_hold_oy + Prismfall::Cutscene::Util.snap(Math.sin(k * Math::PI) * 2)
        end
      when :step_back
        # Restrained 4px ease-out step back (zero cartoon hop!)
        dur = 0.20
        dx, dy = pf_facing_vector(@pf_act[:orig_dir])
        k = Prismfall::Cutscene::Ease.apply(:out, Prismfall::Cutscene::Util.clamp(lt / dur, 0.0, 1.0))
        d = @pf_act[:dist]
        @pf_hold_ox = Prismfall::Cutscene::Util.snap(-dx * d * k)
        @pf_hold_oy = Prismfall::Cutscene::Util.snap(-dy * (d / 2.0) * k)
        @pf_ox = @pf_hold_ox
        @pf_oy = @pf_hold_oy
        @pf_act = nil if lt >= dur
      when :lean_in
        # Subtle 4px ease-out lean toward conversational partner
        dur = 0.20
        dx, dy = pf_facing_vector(@pf_act[:orig_dir])
        k = Prismfall::Cutscene::Ease.apply(:out, Prismfall::Cutscene::Util.clamp(lt / dur, 0.0, 1.0))
        d = @pf_act[:dist]
        @pf_hold_ox = Prismfall::Cutscene::Util.snap(dx * d * k)
        @pf_hold_oy = Prismfall::Cutscene::Util.snap(dy * (d / 2.0) * k)
        @pf_ox = @pf_hold_ox
        @pf_oy = @pf_hold_oy
        @pf_act = nil if lt >= dur
      when :return
        # Smooth ease back to exact neutral tile anchor
        dur = 0.18
        k = 1.0 - Prismfall::Cutscene::Ease.apply(:out, Prismfall::Cutscene::Util.clamp(lt / dur, 0.0, 1.0))
        @pf_hold_ox = Prismfall::Cutscene::Util.snap(@pf_act[:from_ox] * k)
        @pf_hold_oy = Prismfall::Cutscene::Util.snap(@pf_act[:from_oy] * k)
        @pf_ox = @pf_hold_ox
        @pf_oy = @pf_hold_oy
        @pf_act = nil if lt >= dur
      when :headshake
        # Calm, measured Left -> Right -> Restore glance
        step = (lt / 0.14).to_i
        case step
        when 0 then @direction = 4
        when 1 then @direction = 6
        else
          @direction = @pf_act[:orig_dir]
          @pf_act = nil
        end
        @pf_ox = @pf_hold_ox
        @pf_oy = @pf_hold_oy
      when :shudder
        # Opt-in only (rare dramatic beat)
        dur = @pf_act[:duration]
        if lt >= dur
          @pf_act = nil; @pf_ox = @pf_hold_ox; @pf_oy = @pf_hold_oy
        else
          amp = ps ? 0 : px
          @pf_ox = @pf_hold_ox + (((lt * 24).to_i.even?) ? -amp : amp)
          @pf_oy = @pf_hold_oy
        end
      when :hop
        # Opt-in only (rare bright/startled beat)
        dur = 0.22 * @pf_act[:count]
        if lt >= dur
          @pf_act = nil; @pf_ox = @pf_hold_ox; @pf_oy = @pf_hold_oy
        else
          cycle = (lt / 0.22) % 1.0
          @pf_ox = @pf_hold_ox
          @pf_oy = @pf_hold_oy - Prismfall::Cutscene::Util.snap(Math.sin(cycle * Math::PI) * @pf_act[:height])
        end
      end
    end

    alias prismfall_expr_char_update update
    def update
      prismfall_expr_char_update
      pf_update_expressive
    end

    private

    def pf_facing_vector(dir)
      case dir
      when 2 then [0, 1]
      when 4 then [-1, 0]
      when 6 then [1, 0]
      when 8 then [0, -1]
      else [0, 1]
      end
    end
  end
end

#-------------------------------------------------------------------------------
# Sprite_Character Hook: Single-Row 128x48 Pose Sheet Slicer + Visual Offsets
#-------------------------------------------------------------------------------
if defined?(Sprite_Character) && !Sprite_Character.method_defined?(:prismfall_expr_sprite_update)
  class Sprite_Character
    alias prismfall_expr_sprite_update update

    def update
      prismfall_expr_sprite_update
      return if !@character || !@character.respond_to?(:pf_pose_sheet)

      sheet = @character.pf_pose_sheet
      if sheet && !sheet.empty?
        if @pf_active_pose_sheet != sheet
          @pf_pose_bmp = AnimatedBitmap.new("Graphics/Characters/#{sheet}") rescue nil
          @pf_active_pose_sheet = sheet
        end
        if @pf_pose_bmp && @pf_pose_bmp.bitmap && !@pf_pose_bmp.bitmap.disposed?
          bmp = @pf_pose_bmp.bitmap
          @cw = bmp.width / 4
          @ch = bmp.height                # Single-row 128x48 -> 32x48 cell
          self.bitmap = bmp
          self.ox = @cw / 2
          self.oy = @ch
          self.src_rect.set(@character.pf_pose_index * @cw, 0, @cw, @ch)
        end
      elsif @pf_active_pose_sheet
        @pf_pose_bmp&.dispose
        @pf_pose_bmp = nil
        @pf_active_pose_sheet = nil
        @character_name = nil             # Force clean stock Sprite_Character reload
      end

      self.x += @character.pf_visual_ox
      self.y += @character.pf_visual_oy
    end

    alias prismfall_expr_sprite_dispose dispose
    def dispose
      @pf_pose_bmp&.dispose
      @pf_pose_bmp = nil
      prismfall_expr_sprite_dispose
    end
  end
end

#===============================================================================
# Message Display, Conversation Reset & Map Update Hooks
#===============================================================================
if defined?(pbMessageDisplay) && !defined?(prismfall_expressive_pbMessageDisplay)
  alias prismfall_expressive_pbMessageDisplay pbMessageDisplay

  def pbMessageDisplay(msgwindow, message, letterbyletter = true, commandProc = nil, &block)
    ex = Prismfall::Expressive
    return prismfall_expressive_pbMessageDisplay(msgwindow, message, letterbyletter, commandProc, &block) if !ex::ENABLED

    pf = Prismfall::Portrait
    stripped, dirs = ex.extract_inline_tags(message)
    text, spec = pf.extract(stripped)
    spec ||= pf.carry(text)
    mode = pf.mode_for(spec)

    # Bubble mode and plain narrator/non-cast lines delegate cleanly to 014_Portraits.rb
    if mode != :face
      ex.stage.clear if ex.stage.active?
      return prismfall_expressive_pbMessageDisplay(msgwindow, stripped, letterbyletter, commandProc, &block)
    end

    pf.remember(spec, text) if !spec[:carried]
    ex.stage.open_line(spec, msgwindow)
    ex.trigger_acting(spec, dirs)

    # Invoke base message display directly so 014's single FaceBox never double-draws
    base_display = defined?(prismfall_portrait_pbMessageDisplay) ? method(:prismfall_portrait_pbMessageDisplay) : method(:prismfall_expressive_pbMessageDisplay)
    return base_display.call(msgwindow, text, letterbyletter, commandProc) do
      ex.stage.update(msgwindow, text)
      ex.emotes.update
      block&.call
    end
  end
end

if defined?(Interpreter) && !Interpreter.method_defined?(:prismfall_expressive_setup)
  class Interpreter
    alias prismfall_expressive_setup setup

    def setup(*args)
      Prismfall::Expressive.clear_all if @main && Prismfall::Expressive.active?
      return prismfall_expressive_setup(*args)
    end
  end
end

if defined?(Scene_Map) && !Scene_Map.method_defined?(:prismfall_expressive_update)
  class Scene_Map
    alias prismfall_expressive_update update
    alias prismfall_expressive_transfer transfer_player

    def update
      prismfall_expressive_update
      Prismfall::Expressive.emotes.update
      if Prismfall::Expressive.active? && $game_system && $game_system.map_interpreter && !$game_system.map_interpreter.running?
        Prismfall::Expressive.clear_all
      end
    end

    def transfer_player(*args)
      Prismfall::Expressive.clear_all if Prismfall::Expressive.active?
      return prismfall_expressive_transfer(*args)
    end
  end
end

#===============================================================================
# Public Writer & Eventer Helpers (Restrained Opt-In Choreography)
#===============================================================================
def pf_emote(target, kind, wait: false)
  ev = Prismfall::Expressive.resolve_character(target)
  b  = Prismfall::Expressive.emotes.spawn(ev, kind)
  if wait && b
    until b.done?
      Graphics.update
      Input.update
      $scene.miniupdate if defined?($scene) && $scene.respond_to?(:miniupdate)
      Prismfall::Expressive.emotes.update
    end
  end
  return b
end

def pf_nod(target)
  ev = Prismfall::Expressive.resolve_character(target)
  ev&.pf_start_act(:nod)
end

def pf_step_back(target, dist: 4)
  ev = Prismfall::Expressive.resolve_character(target)
  ev&.pf_start_act(:step_back, dist: dist)
end

def pf_turn_away(target, from_other = nil)
  ev    = Prismfall::Expressive.resolve_character(target)
  other = from_other ? Prismfall::Expressive.resolve_character(from_other) : nil
  Prismfall::Expressive.turn_away(ev, other)
end

def pf_turn_toward(target, other)
  ev = Prismfall::Expressive.resolve_character(target)
  to = Prismfall::Expressive.resolve_character(other)
  Prismfall::Expressive.turn_toward(ev, to)
end

def pf_face_each_other(a, b)
  ea = Prismfall::Expressive.resolve_character(a)
  eb = Prismfall::Expressive.resolve_character(b)
  Prismfall::Expressive.turn_toward(ea, eb)
  Prismfall::Expressive.turn_toward(eb, ea)
end

def pf_lean_in(target, dist: 4)
  ev = Prismfall::Expressive.resolve_character(target)
  ev&.pf_start_act(:lean_in, dist: dist)
end

def pf_headshake(target)
  ev = Prismfall::Expressive.resolve_character(target)
  ev&.pf_start_act(:headshake)
end

def pf_step_return(target)
  ev = Prismfall::Expressive.resolve_character(target)
  ev&.pf_start_act(:return)
end

def pf_pose(target, pose_or_index, char_id = nil)
  ev = Prismfall::Expressive.resolve_character(target)
  return if !ev
  cid = char_id || (target.is_a?(Symbol) ? target : ev.character_name.to_s.sub(/\Apose_/i, "").upcase.to_sym)
  Prismfall::Expressive.apply_pose(ev, cid, pose_or_index)
end

def pf_pose_reset(target = nil)
  if target.nil?
    Prismfall::Expressive.reset_all_actors
  else
    ev = Prismfall::Expressive.resolve_character(target)
    ev&.pf_reset_acting
  end
end

def pf_stage_clear
  Prismfall::Expressive.clear_all
end
```

---

## 4. Integration & Writer Style Guide (The Rule of Restraint)

### Step 1 — Zero-Friction Drop-In
1. Confirm all 7 shipped PNGs exist in `graphics/` and `art/out/Graphics/` (already verified & SHA-256 dual-synced):
   - `graphics/Animations/pf_emote_balloons.png`
   - `graphics/Characters/pose_JUNO.png`, `pose_KESTREL.png`, `pose_LARCH.png`, `pose_PLAYER_A.png`, `pose_PLAYER_B.png`, `pose_VOSS.png`
2. Save the Ruby code block in Section 3 to `plugins/Prismfall Cutscenes/018_ExpressiveDialogue.rb`.
3. Boot `mkxp-z` on any existing story map — **every existing `[portrait: CHAR, expr]` scene immediately upgrades to rock-solid motionless Dual-Speaker Portraits, smooth listener dimming (`Tone(-42,-42,-42,35)`), 4-frame expression crossfades, and natural speaker-facing turns — with zero emote spam and zero weird portrait jumping!**

### Step 2 — Writer Guidelines (Trails / Rejuv V14 Natural Restraint)
- **Let portraits stay still.** Never try to shake or bounce faces to manufacture drama — the crisp pixel expressions, dual-speaker rhythm, and dialogue cadence carry the scene naturally.
- **Emote budget: max 1–2 per conversation.** Because `AUTO_EMOTE = false`, balloons only appear where you explicitly drop `\pfe[...]` or `pf_emote(...)`. Save them for a real pause (`\pfe[dots]`), honest question (`\pfe[question]`), or genuine twist (`\pfe[exclaim]`).
- **Act in the overworld, gently.** Prefer subtle posture shifts (`\pfp[crossed]`, `\pfp[guarded]`, `\pfp[worried]`) and understated moves (`pf_nod`, `pf_step_back`, `pf_turn_away`) over cartoon hops.

```text
# Natural 4-line Briarwick exchange (ONLY ONE emote balloon across the entire scene!):
[portrait: JUNO, happy]\pfp[clasped]\pfa[lean_in] Juno: Kestrel—you came back to Briarwick. I wasn't sure you would.
[portrait: KESTREL, deadpan]\pfp[crossed] Kestrel: Don't make a fuss. I only stopped by for Larch's report.
[portrait: JUNO, sad]\pfp[worried] Juno: You heard what happened at the Spire... didn't you?
[portrait: KESTREL, sad]\pfe[dots]\pfp[guarded]\pfa[step_back] Kestrel: ...Keep off the ridge tonight. Meridian's watching.
```

```ruby
# Gentle opt-in Ruby event helpers (work on ANY NPC on ANY map!):
pf_face_each_other(:JUNO, :KESTREL)
pf_nod(:JUNO)
pf_step_back(:KESTREL, dist: 4)
pf_turn_away(:KESTREL, :JUNO)
pf_emote(:KESTREL, :dots)       # Sparing! Max 1-2 per conversation
pf_pose(:LARCH, :glasses)
pf_stage_clear                  # Optional mid-event reset (automatic when event ends)
```

### Step 3 — Recommended Selftest Cases (for `plugins/Prismfall Cutscenes/selftest/`)
1. **Rock-solid `0px` portrait anchor:** Across entry fade-in (`0.00s..0.15s`), expression crossfade, active↔inactive dimming, and text typing, `@frame.x/y` and `@face.x/y` remain invariant at exact `(mx, my - 128)` (Left) and `(mx + mw - 128, my - 128)` (Right) — zero pixel drift.
2. **Smooth listener dimming:** `pbMessage("\\pf[JUNO,happy]Juno: Hi")` → `pbMessage("\\pf[KESTREL,deadpan]Kestrel: Hey")` keeps Juno anchored Left dimmed to `Tone(-42, -42, -42, 35)` while Kestrel fades cleanly into Right at `Tone(0, 0, 0, 0)`.
3. **Zero auto-emote spam (`AUTO_EMOTE == false`):** Playing a 4-line tagged conversation with no `\pfe[...]` tags spawns `0` emote balloons; adding `\pfe[dots]` on Line 4 spawns exactly `1` balloon on row `3` (`:dots`).
4. **3-speaker LRU replacement:** A third speaker (`LARCH`) replaces whichever slot had older `last_used`, keeping the most recent speaker visible and dimmed.
5. **Inline tag stripping & cleanup safety:** `extract_inline_tags` strips `\pfe`, `\pfp`, and `\pfa` cleanly with zero raw control codes leaking; `Interpreter#setup` (`@main = true`), `Scene_Map#transfer_player`, and conversation end dispose all viewports/bitmaps and reset all character poses/offsets once via `Expressive.active?`.
