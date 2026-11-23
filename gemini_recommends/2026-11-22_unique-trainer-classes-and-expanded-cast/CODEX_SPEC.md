# Pokémon Prismfall — Character Codex & Repeatable Cast Systems Spec

**Target Date:** Wednesday Sprint Implementation Spec  
**Author:** Character Codex & Repeatable Cast Systems Architect  
**Scope:** In-game Character Codex (`Prismfall::Codex`), Unified Prism Notebook (`:FIELDNOTES`), Auto-Discovery Hooks + Non-Blocking Toast, and Repeatable Cast & Tag-Partner Rematch System (`Prismfall::Rematches`).  
**Compatibility:** Pokémon Essentials v21.1 · Ruby 3.1 · Elite Battle: DX (optional) · Headless Harness (`tools/harness/`)

---

## 0. Executive Summary & Architectural Fit

Prismfall currently ships four distinct progression/reference systems — **Narrative State** (`012_Narrative_Data.rb`, `013_Narrative_State.rb`), **The Ledger** (`016_Ledger.rb`, `019_LedgerScene.rb`), **Trials Quest Log** (`009_Trials_QuestLog.rb`), and **Field Notes** (`009_FieldEffects_FieldNotes.rb`) — plus a planned **Ties page** (`story/10_CHOICES_ENDINGS.md` §1.4, `020_Passwords.rb` `:OPEN_BOOK`) that does not exist in code yet. However, Prismfall has **no in-game Character Codex / People Directory** and **no mid-to-late-game Repeatable Cast / Tag-Partner Rematch Hub**.

This spec delivers a clean, zero-mandatory-art, save-safe architecture that slots directly after `026_PlayerLooks.rb` inside `plugins/Prismfall Core/`:

| Deliverable | Path | Responsibility |
|---|---|---|
| **Codex Data, DSL & Auto-Discovery** | `plugins/Prismfall Core/027_Codex_Data.rb` | Save state extension (`Prismfall.state.codex`), `Prismfall::Codex.register` DSL, single-source-of-truth `GameData::TrainerType` class resolution, identity-reveal masking, progressive spoiler-free bios, auto-discovery hooks (Portraits + Battle Start), non-blocking toast HUD, `Prismfall::Conditions` extensions, and `NarrativeCheck` validation. |
| **Codex UI & Unified Notebook Hub** | `plugins/Prismfall Core/028_Codex_Scene.rb` | Pixel-exact `512×384` `PrismfallCodexScene`, Pause Menu entry (`:prismfall_codex`), Ties/Bond lantern integration (honoring `:OPEN_BOOK`), and `:FIELDNOTES` Key Item 4-module switcher (`Fields \| People \| Quests \| Ledger`). |
| **Repeatable Cast & Rematch Hub** | `plugins/Prismfall Core/029_Rematches.rb` | `Prismfall::Rematches` — **World Hangout Spots** (`pf_hangout(:ID)`) + **Lumen Battle Pavilion** (Ch5+) & **Festival Training Court** (Ch20+/Post-Game) central rematch & tag-battle hub, LevelCap-aware dynamic party scaling, Left-Hand Back-Throw Ally Sprite support, anti-exploit Bond guard, and scaled rewards. |
| **Small Targeted Hooks** | `002_SaveState.rb`, `014_Portraits.rb`, `024_NarrativeCheck.rb`, `pbs/items_fields.txt` (→ `items_prismfall.txt`) | Minimal 2–6 line additions documented explicitly in §1.5, §5.2, and §6. |
| **Headless Verification** | `tools/harness/run_codex.rb` | Automated selftest verifying registry integrity, bespoke trainer-class sync, auto-discovery, identity masking, Marshal save migration, dynamic LevelCap scaling, and partner cleanup. |

### Key Design Guarantees
1. **Single Source of Truth for Bespoke Trainer Classes:** `Prismfall::Codex` **never** hardcodes `"Warden"`, `"Rival"`, or `"Hollow Keeper"`. Every entry resolves its class dynamically from `GameData::TrainerType.try_get(active_tt)&.name` (supporting conditional act-progression swaps such as `RIVAL_JUNO` → `LEADER_JUNO` or `HOLLOW_SABLE` → `MERIDIAN_KROLL`), falling back to `:class_fallback` only for non-battler NPCs.
2. **Zero Spoilers Across Acts I–V & Ruin Route:** Progressive bios, dynamic display names, faction pills, and `"Where Now"` trackers evaluate safe `Prismfall::Conditions` strings (or Procs) at render time. Masked identities (`:MOURNER` → `:ROWAN` on `S124`; `:SABLE` → `:KROLL` on `S136`) stay completely hidden until their story reveal.
3. **Zero Cutscene-Void Characters:** Every Leader, Ally, Rival, Evil-Org Defector, Eevee Octave Chorister, Sister-Game Cameo, and newly added Reborn/Rejuvenation-style recurring side character registers with a `:repeatable` block and immediately gains both a **World Hangout Spot** and **Central Hub Opponent + Tag-Battle Partner** support.
4. **Load-Order Safe & Headless Safe:** `Prismfall Core` loads alphabetically **before** `Prismfall Cutscenes`, `Prismfall Field Effects`, and `Prismfall Trials`. All cross-plugin hooks use `EventHandlers`, `defined?` guards, or `alias ... unless method_defined?`, and skip all `Viewport`/`Sprite` allocations when headless (`tools/harness/`).

---

## 1. `Prismfall::Codex` Architecture (`027_Codex_Data.rb`)

### 1.1 Categories / Tabs

Four fixed top-level tabs matching the game's narrative pillars:

| Tab Index | Key | Tab Label | Scope & Ordering |
|---|---|---|---|
| `0` | `:ALLIES` | `Allies` | Core companions, mentors, rivals, and Sovereign-side allies (`:JUNO`, `:KESTREL`, `:LARCH`, `:EDDA`, `:VALEN`, `:HESPER`, `:CALLA` post-defection, `:PIP`, `:WENLOW`, `:MAUD`). |
| `1` | `:LEADERS` | `18 Leaders` | Strictly ordered `01`–`18` matching `Prismfall::GYMS` (`001_Config.rb`). Displays badge number, Type pip, **bespoke `GameData::TrainerType` class**, institutional Kingdom + City, Signature Field, and badge-earned check. Seat `#09` shows **Rowan Ashby** in Acts I–II (`!switch(125)`) and **Juno Hale** from Ch10 onward (`switch(125)`). |
| `2` | `:FACTIONS` | `Factions` | Grouped by sub-faction pill with optional Faction Standing summary in the header: **The Hollow / Lantern Hollow** (`:MOURNER` / `:ROWAN`, `:WICK`, `:THISTLE`, `:TEO`, + new Hollow personalities), **Meridian Concord** (`:VOSS`, `:QUENT`, `:MARCHETTI`, `:KROLL`, `:CALLA`, `:HOLLIS`, + new Meridian personalities), **The Eevee Octave** (`:VESPER`, `:LYRA`, `:ARIA`, `:CADENCE`, `:SONA`, `:NOCT`, `:FORTE`, `:LENTO`, `:CAROL`), and **Kingdoms & Wildcards** (`:MAELIS`, `:CAEDMON`, `:DASK`, `:EIRIK`, `:HROTHGAR`, `:KASSAN`, `:SALLOW`, `:GUTTER`, `:OKORO`, `:MORWEN`, `:THEODRIC`). |
| `3` | `:WANDERERS` | `Wanderers` | All **recurring side characters & repeatable rivals** (all new Sandy / Novae / Rorim B.-style recurring personalities from the Expanded Cast pass, Trial keepers like Six-Fingers Ottoline & Clerk Fenwright, Dex, recurring trainers, plus the 10 **Sister-Game Cameos** synced with `Prismfall::Ledger.cameo_beaten?`). |

> **Cross-Tab Promotion (`:also_in`):** Characters who change roles mid-story can appear in two tabs cleanly without duplicating save records. Example: `:JUNO` lives in `:ALLIES` from Ch1 and carries `:also_in => [["switch(125)", :LEADERS]]` (taking Leader slot `#09` once confirmed in Verdance); `:CALLA` starts in `:FACTIONS` (Meridian) and dynamically shifts `:faction` to `:ALLIES` once `chose(:ch20_calla, :shelter)` holds.

### 1.2 Per-Character Entry Schema & Ruby DSL (`Prismfall::Codex.register`)

Every entry is registered via `Prismfall::Codex.register(:ID, ...)` using a validated schema (modeled directly on `Prismfall::Trials::QUEST_KEYS` in `003_Trials_Registry.rb`).

#### Conditional Value Helper (`resolve_value`)
To keep entries spoiler-free **and** statically validatable by `024_NarrativeCheck.rb`, fields marked **Dynamic** accept either:
- A static value (`String`, `Symbol`, `nil`), **OR**
- An ordered `Array` of `[condition, value]` pairs where `condition` is a `Prismfall::Conditions` string (preferred — validated at load!), a `Proc`, or `nil` (fallback). The **first matching pair** wins.

#### Full Schema Table

| Field | Type | Required | Description |
|---|---|---|---|
| `:id` | `Symbol` | Yes | Canonical uppercase cast ID (`:MARISOL`, `:ROOK`, `:THISTLE`, `:KESTREL`). |
| `:name` | `String` or Dynamic Array | Yes | Display name. Supports identity updates, e.g. `[["switch(136)", "Sabine Kroll"], [nil, "Sable"]]`. |
| `:category` | `Symbol` | Yes | Primary tab: `:ALLIES`, `:LEADERS`, `:FACTIONS`, or `:WANDERERS`. |
| `:also_in` | `Array` of `[cond, :TAB]` | No | Optional secondary tab placement (e.g., Juno entering `:LEADERS` at Ch10). |
| `:sort_order` | `Integer` | No | Explicit list ordering within tab (defaults to registration order; `1..18` for `:LEADERS`). |
| `:gym_index` | `Integer (1..18)` | No | Links to `Prismfall::GYMS[gym_index - 1]` and `WARDEN_CONSENT[gym_index - 1]`. Auto-populates default `:trainer_type`, `:signature_field`, and badge check if omitted. |
| `:trainer_type` | `Symbol` or Dynamic Array | No | **Single source of truth for Trainer Class.** `Codex.trainer_class(id)` queries `GameData::TrainerType.try_get(tt)&.name`. Example: `[["switch(125)", :LEADER_JUNO], [nil, :RIVAL_JUNO]]`. |
| `:trainer_types_all` | `Array<Symbol>` | No | All `TrainerType` IDs that map to this Codex entry for battle auto-discovery (auto-derived from `:trainer_type` + `:repeatable[:rematch_trainer]` if omitted). |
| `:class_fallback` | `String` | No | Fallback class title **only** when `:trainer_type` is `nil` or absent from compiled PBS (e.g., `"Professor"` for Larch, `"Ferry Captain"` for Edda before any trainer PBS entry exists). |
| `:faction` | `Symbol` or Dynamic Array | Yes | Controls Faction Pill label + accent color (`:ALLIES`, `:ACCORD`, `:HOLLOW`, `:LANTERN_HOLLOW`, `:MERIDIAN`, `:OCTAVE`, `:ELOWEN`, `:ISENMAR`, `:ZENITH`, `:NADIR`, `:ASHKAAR`, `:OSSARIA`, `:ANTUMBRA`, `:ROGUE`, `:CAMEO`). |
| `:region` | `String` or Dynamic Array | Yes | Institutional region & home city, e.g., `"Isenmar · Ebbmouth"`, `"Zenith · Lumen City"`, `"Antumbra · Gravenmoor"`. |
| `:portrait` | `String` | No | Explicit portrait path override. Defaults to `"Graphics/Portraits/#{id}"` (with fallback chain: `_neutral` → base → VS bust crop → trainer front head crop → tinted initial crest). |
| `:portrait_ids` | `Array<Symbol>` | No | `Prismfall::Portrait` speaker IDs that unlock this card (defaults to `[id]`). |
| `:vs_bust` | `String` | No | Optional header banner override. Default fallback chain: `"Graphics/EBDX/VS/#{id}"` (already exists for 28+ characters!) → `"Graphics/EBDX/Battlers/Trainers/#{trainer_type}"` → themed gradient bar. |
| `:theme` | `Symbol` | No | Accent palette (`:rose`, `:blue`, `:gold`, `:violet`, `:red`, `:teal`, `:green`, `:grey`). Defaults to `PrismfallVS::THEMES[id.to_s]` if EBDX Bridge is loaded. |
| `:ace_species` | `Symbol` or Dynamic Array | No | Signature ace Pokémon (`:GYARADOS`, `:AEGISLASH`, `[["badges >= 5", :LEAVANNY], [nil, :SWADLOON]]`). Renders mini icon via `GameData::Species.icon_filename`. |
| `:signature_field` | `Symbol` | No | Signature `FieldEffects` ID (`:WATER_SURFACE`, `:NEON_GRID`, etc.). Displays live name via `FieldEffects.name_of(field)`. |
| `:bond_key` | `Symbol` | No | Key in `Prismfall::Narrative::BONDS` (`:JUNO`, `:KESTREL`, `:ROWAN`, `:VOSS`, `:VALEN`, `:ILSA`, `:SIGRUN`, `:NYX`, `:MARISOL`, `:YSOLDE`). Auto-reads `Prismfall::Bonds.get` & `Prismfall::Bonds.tier` (and shows exact score when `:OPEN_BOOK` password is active). |
| `:favorite_gifts` | `Array<Symbol>` | No | Item IDs that give bonus Rapport / Bond when gifted at Hangout Spots (e.g., `[:FRESHWATER, :ELEMENTALSEED, :SITRUSBERRY]`). |
| `:unlock_condition` | `String` / `Proc` / `nil` | No | Passive unlock condition (in addition to portrait & battle auto-discovery), e.g., `"has_badge(3)"`, `"switch(101)"`, `"octave_has(:LYRA)"`, `"cameo_beaten(:FESTIVAL_SHELLY)"`. |
| `:hide_when` | `String` / `Proc` / `nil` | No | Optional condition hiding a superseded masked alias card (e.g., `:MOURNER` has `:hide_when => "switch(124)"` once unmasked and merged into `:ROWAN`!). |
| `:merged_from` | `Symbol` | No | Copies unlock/battle history from a retired alias entry (e.g., `:ROWAN` specifies `:merged_from => :MOURNER`). |
| `:progressive_bios` | `Array` | Yes | Ordered array of `[condition_or_proc, text]` or `{ :if => cond, :tag => "Act I", :text => "...", :replace => false }`. Evaluates every matching stage in order without spoilers. |
| `:where_now` | `Array` of `[cond, String]` | Yes | Ordered latest-first list of `[condition_or_proc, "Location hint"]`. First match wins, giving players an always-accurate world tracker. |
| `:repeatable` | `Hash` or `nil` | No | Full repeatability configuration (schema in §1.3 & §3). `nil` only for strictly non-battling/deceased NPCs with no Echo/Reflection. |

#### DSL Example (`027_Codex_Data.rb`)

```ruby
Prismfall::Codex.register(:MARISOL,
  :name            => "Marisol Reyes",
  :category        => :LEADERS,
  :gym_index       => 3,
  :sort_order      => 3,
  :trainer_type    => :LEADER_MARISOL,       # Class read live from GameData::TrainerType.get(:LEADER_MARISOL).name
  :faction         => :ISENMAR,
  :region          => "Isenmar · Ebbmouth",
  :theme           => :blue,
  :ace_species     => :GYARADOS,
  :signature_field => :WATER_SURFACE,
  :bond_key        => :MARISOL,              # Auto-reads Prismfall::Bonds.get(:MARISOL) & tier
  :favorite_gifts  => [:MYSTICWATER, :ELEMENTALSEED, :FRESHWATER, :HEARTSCALE],
  :unlock_condition => "var(124) >= 2 || has_badge(3)",
  :progressive_bios => [
    { :if => nil, :tag => "Act I",
      :text => "Elected by the Ebb Guild rather than appointed by the crown. Broad-shouldered, foghorn-voiced, and fiercely protective of Ebbmouth's dockworkers." },
    { :if => "switch(112)", :tag => "Act I",
      :text => "Her nineteen-year-old brother Teo leads Ebbmouth's Hollow cell. She has been walking a razor's edge between the river and Meridian's paychecks." },
    { :if => "switch(123) && flag(:TEO_SAVED)", :tag => "Act II",
      :text => "Never forgot who pulled Teo out of Ironreach's shafts. Stands solidly behind the docks—and behind you." },
    { :if => "switch(123) && !flag(:TEO_SAVED)", :tag => "Act II",
      :text => "Carries Teo's death like iron ballast. Her fury at Meridian—and anyone who let him fall—runs deeper than the Ebb." },
    { :if => "switch(130)", :tag => "Act III",
      :text => "Led the Ebbmouth Strike and severed the tidal Lattice, forcing the river to run both ways again." },
    { :if => "flag(:WAR_STOPPED)", :tag => "Act V",
      :text => "Brought her siege-runners and fishing fleet south to defend Crownhaven's lower city during the Festival." }
  ],
  :where_now => [
    ["switch(160)",                    "Crownhaven — Festival Training Court & Ebbmouth Mill Quay"],
    ["var(102) >= 20",                 "Crownhaven — Court of Eight Pavilions (Isenmar Pavilion)"],
    ["var(122) >= 3 && var(122) <= 4", "Skaldfast — Siege Lines (Steamline Convoy)"],
    ["switch(130)",                    "Ebbmouth — Mill Quay (Docks Restored)"],
    [nil,                              "Ebbmouth — Tidelock Gym & Mill Quay"]
  ],
  :repeatable => {
    :unlock           => "has_badge(3)",
    :unavailable_when => "var(122) == 3 && var(102) < 19",
    :unavailable_msg  => "Marisol is pinned down running siege convoys into Skaldfast.",
    :rematch_trainer  => [:LEADER_MARISOL, "Marisol"],
    :tier_versions    => { 0 => 0, 50 => 0, 85 => 90 },  # Picks closest PBS template, then scales to LevelCap!
    :partner_trainer  => [:LEADER_MARISOL, "Marisol", 1],
    :rematch_map      => 160,                             # Ebbmouth Mill Quay
    :rematch_map_name => "Ebbmouth — Mill Quay",
    :hangout_schedule => :always,
    :rematch_rules    => { :format => :single, :double_ok => true, :field => :WATER_SURFACE, :can_lose => true },
    :cooldown         => :daily,                          # Bonus rewards once/day; hub sparring always_available: true
    :always_available => true,
    :reward_pool      => { :first_win => [:MYSTICWATER, 1], :first_tag => [:DIVEBALL, 5], :seed => :ELEMENTALSEED },
    :dialogue_pool    => {
      :hangout_greet => "Tides take it, look who washed up on my quay. Got time for a bout, kid?",
      :banter => [
        "Gyarados still remembers being a Magikarp everyone laughed at. Funny how nobody laughs now.",
        "Eel-stall owner's still keeping a tab for 'The Boy.' Four eels a day. Don't tell Kestrel I told you.",
        "The Ebb runs both ways. Took a strike to remind Zenith of that."
      ],
      :gift_love => "Hah! Now that's a proper gift for a dockworker. You've got good instincts, kid.",
      :gift_like => "Appreciate it. I'll put it to good use down at the Guild.",
      :pre_battle => "No holding back just because we're off the clock. Show me your best wave!",
      :win => "Tides take it—you hit like a spring surge! Good scrap.",
      :lose => "Harbor's still mine today, kid. Catch your breath and try me again!",
      :tag_invite => "Watch my flank and I'll watch yours. Ready to flood the floor?",
      :tag_victory => "Now THAT'S how you run a crew! Same time next tide?"
    }
  }
)
```

> **Note on `Prismfall::Narrative.bond`:** In existing `013_Narrative_State.rb`, Bonds are exposed via `Prismfall::Bonds.get(id)` / `Prismfall::Bonds.tier(id)` (which alias `Prismfall::Narrative::Bonds`). `027_Codex_Data.rb` calls `Prismfall::Bonds.get(bond_key)` directly and optionally defines a 2-line convenience alias `Prismfall::Narrative.bond(id)` / `Prismfall::Narrative.bond_tier(id)` so both call signatures work seamlessly.

### 1.3 Handling Identity Reveals & Bespoke Class Evolution

Prismfall has three high-impact identity/title shifts that must **never** leak early in the Codex:

1. **The Mourner (`:MOURNER`) → Rowan Ashby (`:ROWAN`):**
   - Acts I–II (`!switch(124)`):
     - `:ROWAN` appears in `:LEADERS` (Seat `#09`, class from `LEADER_ROWAN`, region `"Elowen · Verdance"`). Bio only discusses Uncle Rowan, the Bride Tree, and Verdance's endless bloom.
     - `:MOURNER` appears separately in `:FACTIONS` (Hollow, class from `HOLLOW_MOURNER`, portrait `MOURNER.png`, VS bust `Graphics/EBDX/VS/MOURNER.png`).
   - Once `S124` (`CH9_MOURNER_UNMASKED`) turns ON:
     - `:MOURNER` sets `:hide_when => "switch(124)"`, removing the duplicate masked card.
     - `:ROWAN` shifts from `:LEADERS` to `:FACTIONS` (`:HOLLOW` → `:LANTERN_HOLLOW` after Ch13 Fault if `flag(:ROWAN_ALIVE)`), updates `:name` to `"Rowan Ashby (The Mourner)"`, unlocks his post-unmasking bio entries, and merges any battle/discovery timestamps via `:merged_from => :MOURNER`.
     - If `choice(:ch13_fault) == :marchetti` (`!flag(:ROWAN_ALIVE)`), `:ROWAN`'s bio appends his memorial epitaph and marks `:repeatable` unavailable (`"Lost in the Lucent Fault."` — except in the post-game **Hall of Reflections**!).
2. **Sable (`HOLLOW_SABLE`) → Sabine Kroll (`MERIDIAN_KROLL`):**
   - Single Codex entry `:KROLL` with dynamic fields:
     - `:name => [["switch(136) || flag(:KROLL_EXPOSED_CH13)", "Sabine Kroll"], [nil, "Sable"]]`
     - `:trainer_type => [["switch(136) || flag(:KROLL_EXPOSED_CH13)", :MERIDIAN_KROLL], [nil, :HOLLOW_SABLE]]`
     - `:faction => [["switch(136) || flag(:KROLL_EXPOSED_CH13)", :MERIDIAN], [nil, :HOLLOW]]`
     - `:portrait_ids => [:SABLE, :KROLL]` and `:trainer_types_all => [:HOLLOW_SABLE, :MERIDIAN_KROLL]`.
     - Portrait/VS art resolves `"KROLL"` after `S136` and `"SABLE"` before `S136` (both `graphics/EBDX/VS/SABLE.png` and `KROLL.png` already exist!).
3. **Juno Hale (`RIVAL_JUNO` → `LEADER_JUNO`):**
   - `:trainer_type => [["switch(125)", :LEADER_JUNO], [nil, :RIVAL_JUNO]]`
   - Automatically switches her displayed class from her bespoke Rival class to her bespoke Grass Leader class the instant Verdance confirms her, and promotes her into `:LEADERS` Seat `#09` via `:also_in => [["switch(125)", :LEADERS]]`!

### 1.4 Single-Source-of-Truth Trainer Class Resolver

```ruby
module Prismfall
  module Codex
    def self.active_trainer_type(id)
      entry = get(id)
      return nil if !entry
      tt = resolve_value(entry[:trainer_type])
      if tt.nil? && entry[:gym_index]
        g = Prismfall.gym(entry[:gym_index])
        tt = g[:trainer_type] if g
      end
      return tt
    end

    # Single source of truth: always pulls compiled PBS Name from GameData::TrainerType.
    def self.trainer_class(id)
      entry = get(id)
      return "" if !entry
      tt = active_trainer_type(id)
      if tt && defined?(GameData::TrainerType) && GameData::TrainerType.exists?(tt)
        return GameData::TrainerType.get(tt).name
      end
      return _INTL(entry[:class_fallback].to_s) if entry[:class_fallback]
      return ""
    end

    # Mirrors 025_CharsetAliases.rb Trainer#full_name deduplication ("The Mourner", not "The Mourner Mourner").
    def self.titled_name(id)
      nm = display_name(id)
      kl = trainer_class(id)
      return nm if kl.empty?
      return kl if !nm.empty? && kl.downcase.end_with?(nm.downcase)
      return "#{kl} #{nm}"
    end
  end
end
```

### 1.5 Auto-Discovery Hooks & Non-Blocking Toast HUD

#### Important Load-Order Guard (`Prismfall Core` vs `Prismfall Cutscenes`)
`PluginManager` loads `Prismfall Core` **before** `Prismfall Cutscenes`. Therefore `027_Codex_Data.rb` must **never** assume `Prismfall::Portrait` is already defined at load time. Instead, we use `EventHandlers` (Prismfall Core's standard decoupled bus, `design/SYSTEMS.md` §0):

1. **Hook A — Dialogue / Portrait Discovery (`plugins/Prismfall Cutscenes/014_Portraits.rb`):**
   Add two guarded lines inside `014_Portraits.rb`:
   - In `pbMessageDisplay` (right after `text, spec = pf.extract(message)` and `spec ||= pf.carry(text)`):
     ```ruby
     if spec && spec[:id]
       spec[:_codex_emitted] = true
       EventHandlers.trigger(:prismfall_portrait_opened, spec[:id], spec[:expression], mode)
     end
     ```
     *Why here in addition to `Portrait.open`?* Because characters whose portrait art isn't installed yet fall into `mode == :plain` and skip `Portrait.open`! Triggering right after `extract` guarantees that **every** `\pf[ID,...]` / `pf_say(:ID, ...)` line unlocks the speaker's Codex card even before their PNG exists.
   - Inside `Prismfall::Portrait.open(spec, msgwindow = nil, mode = nil)` (for direct `Portrait.open` calls outside `pbMessageDisplay`):
     ```ruby
     EventHandlers.trigger(:prismfall_portrait_opened, spec[:id], spec[:expression], mode) if spec && spec[:id] && !spec[:_codex_emitted]
     ```
   - `027_Codex_Data.rb` registers a listener:
     ```ruby
     EventHandlers.add(:prismfall_portrait_opened, :prismfall_codex_unlock,
       proc { |portrait_id, _expr, _mode|
         next if !$player || portrait_id.nil?
         Prismfall::Codex.discover_by_portrait(portrait_id)
       }
     )
     ```

2. **Hook B — Battle Start Discovery (`Battle#pbStartBattleCore` in `027_Codex_Data.rb`):**
   Alias-chained with `unless method_defined?` (F12 soft-reset safe) and checks **both** opposing trainers (`@opponent`) and tag-battle allies (`@player[1..]`)!
   ```ruby
   class Battle
     alias __prismfall_codex_pbStartBattleCore pbStartBattleCore unless method_defined?(:__prismfall_codex_pbStartBattleCore)

     def pbStartBattleCore
       if @internalBattle || (@rules.is_a?(Hash) && @rules["prismfall_codex_record"])
         (@opponent || []).each do |tr|
           Prismfall::Codex.discover_from_trainer(tr, via: :battle, defer_toast: true) if tr
         end
         (@player || [])[1..-1]&.each do |ally|
           Prismfall::Codex.discover_from_trainer(ally, via: :partner, defer_toast: true) if ally
         end
       end
       return __prismfall_codex_pbStartBattleCore
     end
   end
   ```
   - **Why `defer_toast: true` in battle?** So a HUD toast never collides with the B2W2 VS intro (`010_Bridge_VersusIntro.rb`) or EBDX camera sweep. Queued toasts flush cleanly on the first frame back on `Scene_Map`!
   - Also hook `:prismfall_narrative_changed` and `:prismfall_badge_awarded` so when a major act choice unlocks a **new progressive bio stage** on an already-known character, the Codex subtly queues `"Codex Updated: [Class] [Name]"` (rate-limited to once per character per chapter transition so it feels exciting, never spammy!).

3. **Non-Blocking Toast HUD (`Prismfall::Codex::Toast`):**
   - Renders in a dedicated top-right `Viewport` (`z = 99_990`, below `99_999` message boxes; `x = 276..504, y = 10..54`, dimensions `228×44` — opposite `FaceBox` at bottom-left, zero overlap!).
   - **Never blocks input or freezes dialogue.** Driven by `System.uptime` inside `Scene_Map#update` (aliased with `unless method_defined?(:__prismfall_codex_toast_update)`) and also ticks cleanly inside `pbMessageDisplay`'s frame yield if triggered mid-dialogue.
   - **Slide animation:** `0.22s` cubic ease-out slide-in from `x = 516 → 276`, `2.20s` hold, `0.28s` ease-in slide-out → `516`, soft SE (`"GUI party switch"` at volume 60, pitch 115).
   - **Coalescing:** If a group cutscene introduces > 2 new characters simultaneously, shows the first 2 individually and folds the rest into a single compact toast: `"Codex Updated: +N new entries"`.
   - **Headless Guard:** Instantly no-ops (`return`) if `!defined?(Scene_Map) || !$scene.is_a?(Scene_Map) || Graphics.width <= 0`, ensuring zero noise/errors in `tools/harness/run_all.rb` and `run_trials.rb`.

### 1.6 `Prismfall::Conditions` Extensions

Added to `Prismfall::Conditions::FUNCTIONS` (`014_Conditions.rb`) at load time by `027_Codex_Data.rb` (matching `012_Trials_Octave.rb`'s pattern):

```ruby
Prismfall::Conditions::FUNCTIONS.merge!({
  "codex_unlocked"     => [1, proc { |id| Prismfall::Codex.unlocked?(id) }],
  "codex_count"        => [0, proc { Prismfall::Codex.unlocked_count }],
  "codex_rematches"    => [1, proc { |id| Prismfall::Codex.rematch_wins(id) }],
  "codex_tag_wins"     => [1, proc { |id| Prismfall::Codex.tag_wins(id) }],
  "codex_rapport"      => [1, proc { |id| Prismfall::Codex.rapport_stars(id) }],
  "codex_hangout_here" => [1, proc { |id| Prismfall::Rematches.hangout_visible?(id) }]
})
```
> Because `010_Trials_PageConditions.rb` evaluates `Comment: Condition: ...` on map event pages using `Prismfall::Conditions`, every World Hangout NPC can simply place `Comment: Condition: codex_hangout_here(:MARISOL)` on its event page — **consuming zero RMXP Game Switches!**

---

## 2. `512×384` UI Wireframe & Menu Integration (`028_Codex_Scene.rb`)

### 2.1 Pixel-Exact `512×384` Layout Specification

Designed to match `019_LedgerScene.rb` and `010_Festival_BracketScene.rb` (code-drawn with crisp 1px borders, optional background skin `Graphics/UI/Prismfall/codex_bg.png`, zero mandatory external UI sprites).

```text
+======================================================================+ y=0
| CHARACTER CODEX  [L] Fields | *People* | Quests | Ledger [R]  18/64  | y=0..31 (32px)
+----------------------------------------------------------------------+ y=32
| [  Allies  ]  [=18 Leaders=]  [ Factions ]  [ Wanderers ]            | y=32..57 (26px)
+========================+=============================================+ y=62
| Roster (170x294)       | Dossier Header Banner (320x108)             | y=62..170
| x=8..177               | x=184..503  (optional VS bust @ 35% scrim)  |
| +--------------------+ | +----------+  Tidelock Union Captain (Gold) | y=68
| | ■ 01 Dorian      ★ | | |          |  Marisol Reyes          (Sys)  | y=85
| | ■ 02 Tamsin      ★ | | |  96x96   |  [ ISENMAR ]  Isenmar·Ebbmouth | y=109..142
| |▶■ 03 Marisol     ★ | | | Portrait |  Lantern: ◆◆◆◇◇ Friendly (+3)  | y=147..165
| | ■ 04 Rook        ★ | | +----------+                                |
| | ■ 05 Sahar         | +---------------------------------------------+ y=172..204 (32px)
| | ■ 06 Corvin        | [32px] Ace: Gyarados  |  Field: Water Surface |
| | ■ 07 ???           | +---------------------------------------------+ y=208..355 (148px)
| | ■ 08 ???           |  [MODE 0: PROGRESSIVE BIO (7 lines @ 18px)]   |
| | ■ 09 Rowan         |  [Act I] Elected by the Ebb Guild rather than |
| | ■ 10 ???        ██ |  appointed by the crown. Fiercely protective  |
| +--------------------+ |  of Ebbmouth's dockworkers.                 |
|                        |  [Act III] Led the Ebbmouth Strike and cut  |
|                        |  the tidal Lattice so the river runs again. |
|                        |                              1/2 [Shift] >> | y=339
+========================+=============================================+ y=360
| [←/→] Tabs  [↑/↓] Pick            [C] Rematch / Location Info [X]End | y=360..383 (24px)
+======================================================================+ y=384
```

#### Exact Coordinate Budget (Zero Overlap / Zero Clipping Proof)

| Region | X Range (Width) | Y Range (Height) | Font / Rendering Notes |
|---|---|---|---|
| **Header Bar** | `0..511` (`512px`) | `0..31` (`32px`) | Title `"CHARACTER CODEX"` (`pbSetSystemFont`, Gold) at `x=12, y=4`; or Hub bar when launched via `:FIELDNOTES`. Count `"Met 18/64"` (`pbSetSmallFont`, right-aligned) at `x=500, y=7`. |
| **4 Category Tabs** | `8..503` (`496px`) | `32..57` (`26px`) | 4 tabs × `121px` + 3 gaps × `4px` (`x = 8, 133, 258, 383`). Active tab: `SELECT` fill + `2px` Gold bottom bar + white text. |
| **Left Roster Panel** | `8..177` (`170px`) | `62..355` (`294px`) | **10 visible rows × `28px`** (`y = 66..345`) + `4px` scrollbar at `x = 171..174`. Per row: `3px` type/faction bar (`x=10`), index/status (`x=16`), `fit_text` name (`x=36`, max `118px`), rematch/badge star pip (`x=158`). |
| **Right Header Banner** | `184..503` (`320px`) | `62..170` (`108px`) | Optional `vs_bust` (`Graphics/EBDX/VS/<ID>.png`) blitted right-aligned inside clip rect under a dark `rgba(18,20,34,155)` readability scrim, else themed gradient. |
| **96×96 Portrait Frame** | `190..289` (`100px`) | `68..167` (`100px`) | `2px` border (`BORDER`/`GOLD`), soft slate-parchment backing `Color.new(44, 42, 58)` (so pale hair/veils read clearly per `REVIEW.md`), native `1:1` `96×96` portrait at `x=192, y=70`. |
| **Identity Column** | `296..498` (`202px`) | `68..166` (`98px`) | `y=68` Class (`SmallFont`, Gold, max `198px`) · `y=85` Full Name (`SystemFont`, White, max `198px`) · `y=111` Faction Pill (`h=17px`) · `y=130` Region (`SmallFont`, Subtext, max `198px`) · `y=148` Bond Lantern / Rapport Stars (`h=17px`). |
| **Ace & Field Strip** | `184..503` (`320px`) | `172..204` (`32px`) | Left (`x=188..346`): `28×28` Ace icon + `"Ace: Gyarados"` (`SmallFont`, max `124px`). Right (`x=350..498`): colored dot + `"Water Surface"` (`SmallFont`, max `136px`). |
| **Lower Detail Card** | `184..503` (`320px`) | `208..355` (`148px`) | Inner text width `304px` (`x=192..496`). **Mode 0 (Bio):** 7 wrapped lines × `18px` (`y=214..338`) + page indicator at `y=339`. **Mode 1 (`[C]` Rematch & Location):** Where Now (`y=214..248`), Hub/Hangout availability (`y=252..282`), Win/Tag/Gift record (`y=286`), Scaled Rewards (`y=306`), Hub Quick-Challenge action (`y=330`). |
| **Footer Strip** | `0..511` (`512px`) | `360..383` (`24px`) | `1px` top divider at `y=359`. Left (`x=10, y=363`): `"[←/→] Tabs  [↑/↓] Pick"`. Right (`x=502, y=363`): `"[C] Rematch / Location Info  [X] Back"`. |

#### Bond Lantern & `openbook` Password Rendering
- If `entry[:bond_key]` is present (one of `Prismfall::Narrative::BONDS`):
  - Maps `Prismfall::Bonds.tier(key)` to the exact 6-level Ties lantern metaphor from `story/10_CHOICES_ENDINGS.md` §1.4:
    - `:hostile` (`-10..-5`) → Cracked (crimson) · `:wary` (`-4..-2`) → Guttering (amber-grey) · `:neutral` (`-1..1`) → Lit (soft ivory) · `:friendly` (`2..4`) → Bright (warm gold) · `:close` (`5..7`) → Blazing (bright gold) · `:devoted` (`8..10`) → Starred (prism white-gold).
  - When `Prismfall::Passwords.active?(:OPEN_BOOK)` is `true`, appends `" (+#{val})"` right next to the tier label (`"Friendly (+3)"`), fulfilling the `openbook` password natively!
- If `entry[:bond_key]` is `nil`: displays **Rapport Stars** (`★☆☆☆☆`..`★★★★★`, earned via Hangouts, Rematches, and Tag Battles) + `"Repeatable"` pill when `repeatable` is active.
- On the **Factions** tab (`@tab == 2`), clicking/pressing `ACTION` or glancing at the compact header strip can show the 3 `Narrative::FACTIONS` Standing tiers (`Hollow`, `Meridian`, `Accord` — also honoring `:OPEN_BOOK`!).

#### Locked Entry Treatment
- Unmet entries in `:LEADERS` show `"07 ???"` with their Gym badge number and `"Not yet encountered."` (preserving anticipation for all 18 seats).
- Unmet entries in `:ALLIES`, `:FACTIONS`, and `:WANDERERS` show `"???"` with a locked silhouette and optional spoiler-free region whisper (e.g., `"Someone waiting in Mirefen..."` or `"???"` for secret/Ruin characters so plot twists like `:THEODRIC` or `:DASK` never leak on the roster before their route!). Secret entries set `:secret => true` and are **completely omitted from the list** until unlocked!

### 2.2 Dual Menu Integration & `:FIELDNOTES` Unified Notebook Hub

#### A. Pause Menu Integration (Clean Non-Colliding Orders)
Currently `009_FieldEffects_FieldNotes.rb` and `019_LedgerScene.rb` both register at `order => 45`. Standardize the reference block cleanly:

| Pause Menu Entry | Handler ID | Order | Condition |
|---|---|---|---|
| `Codex` | `:prismfall_codex` | `43` | `Prismfall::Codex.unlocked_count > 0` |
| `Quests` | `:prismfall_quests` | `44` | `Prismfall::Trials.log_any?` (existing) |
| `Field Notes` | `:prismfall_field_notes` | `45` | `FieldEffects::FieldNotes.seen_count > 0` (existing) |
| `Ledger` | `:prismfall_ledger` | `46` | `Prismfall::Ledger.any?` (bump from `45` → `46`) |

#### B. Key Item `:FIELDNOTES` — Tabbed Prism Notebook (`Fields | People | Quests | Ledger`)
Add `[FIELDNOTES]` to `pbs/items_fields.txt` (which `tools/package.sh` maps to `PBS/items_prismfall.txt`):

```ini
#-------------------------------
[FIELDNOTES]
Name = Field Notebook
NamePlural = Field Notebooks
Pocket = 8
Price = 0
FieldUse = Direct
Flags = KeyItem
Description = Professor Larch's field folio. Tracks Battle Fields, People met across Velmora, Trial Quests, and the Ledger.
```

- Given to the player by Professor Larch in Ch1 (and auto-granted silently on map load if `badges >= 1 && !$bag.has?(:FIELDNOTES)` so existing playtest saves receive it automatically!).
- Register BOTH `ItemHandlers::UseFromBag.add(:FIELDNOTES, ...)` and `ItemHandlers::UseInField.add(:FIELDNOTES, ...)` (so players can bind it to Quick-Register `F5`!):
  ```ruby
  module Prismfall
    module Notebook
      TABS = [
        { :id => :fields, :label => "Fields", :available => proc { defined?(FieldEffects::FieldNotes) } },
        { :id => :people, :label => "People", :available => proc { defined?(Prismfall::Codex) } },
        { :id => :quests, :label => "Quests", :available => proc { defined?(Prismfall::Trials) } },
        { :id => :ledger, :label => "Ledger", :available => proc { defined?(Prismfall::Ledger) } }
      ].freeze

      # Cycles seamlessly with Q/W (Input::AUX1 / Input::AUX2) across all 4 scenes without
      # rewriting the inner logic of FieldNotes, QuestLog, or Ledger.
      def self.open(start_tab = nil)
        tabs = TABS.select { |t| t[:available].call }
        return if tabs.empty?
        idx = start_tab ? (tabs.index { |t| t[:id] == start_tab } || 0) : Prismfall::Codex.store[:ui_prefs][:last_notebook_tab].to_i
        idx = idx.clamp(0, tabs.length - 1)
        @active = true
        @tabs = tabs
        pbFadeOutIn do
          loop do
            @current_idx = idx
            Prismfall::Codex.store[:ui_prefs][:last_notebook_tab] = idx
            nav = run_tab(tabs[idx][:id])
            break if nav.nil? || nav == :close
            idx = (idx + ((nav == :prev) ? -1 : 1)) % tabs.length
            pbPlayCursorSE
          end
        end
      ensure
        @active = false
      end
    end
  end
  ```
- **Zero-rewrite adapter for existing scenes:** Each of `PrismfallFieldNotes_Scene`, `PrismfallQuestLogScene`, and `PrismfallLedgerScene` checks `if Prismfall::Notebook.active?` on `Input::AUX1` (`Q`/`L`) / `Input::AUX2` (`W`/`R`) and returns `:prev` / `:next` cleanly, plus draws a subtle `"[L/R] Fields|People|Quests|Ledger"` strip in the header! When opened directly from the Pause Menu, each scene behaves 100% identically to before.

---

## 3. Repeatable Cast & Rematch System (`029_Rematches.rb`)

To ensure **no character ever vanishes into the void after a single cutscene** — including all 18 Leaders, Rivals, Allies, Hollow/Meridian Defectors, Eevee Octave Choristers, Sister-Game Cameos, and every new Expanded Cast recurring character — `Prismfall::Rematches` provides **two interconnected gameplay loops** powered by the exact same `Codex` `:repeatable` metadata.

### 3.1 Pillar 1: World Hangout Spots (`pf_hangout(:ID)`)

Every unlocked cast member stands at a lore-accurate overworld hangout when not occupied by an active story crisis.

#### Map Event Wiring (Zero Switches Consumed!)
Each hangout NPC on a map needs only a **single 2-line event** using `010_Trials_PageConditions.rb`:
- **Page 1 Comment:** `Condition: codex_hangout_here(:MARISOL)`
- **Page 1 Script:** `pf_hangout(:MARISOL)`
- **Character graphic:** Automatically resolved by `025_CharsetAliases.rb` (or the character's `<ID>.png` sheet in `Graphics/Characters/`).

`Prismfall::Rematches.hangout_visible?(id)` returns `true` when:
1. `Codex.unlocked?(id)` is `true`
2. `repeatable[:unlock]` evaluates `true`
3. `repeatable[:unavailable_when]` evaluates `false` (respects story crises like Corvin's arrest, Marisol's Skaldfast siege, or Rowan's Fault outcome!)
4. `repeatable[:hangout_schedule]` matches current time (`:always`, `:day` via `!PBDayNight.isNight?`, `:night` via `PBDayNight.isNight?`, `:dusk`, or a custom `Prismfall::Conditions` string).

#### Hangout Interaction Menu (`pf_hangout(id)`)
When the player speaks to a Hangout NPC:
1. Plays their portrait-tagged greeting (`pf_say(id, :happy, greet)`).
2. Presents a concise contextual menu:
   - **`★ Quiet Hour`** *(shown ONLY if a Quiet Hours bond scene from `story/10_CHOICES_ENDINGS.md` §7.1 is ready for this character!)*
   - **`Chat`** — Plays the next line from `dialogue_pool[:banter]` (rotating cursor stored in `codex[:banter_idx][id]`, never repeating back-to-back, interleaved with chapter-reactive lines) and grants `+5` Rapport once per real day.
   - **`Give a Gift`** — Opens a filtered Bag pocket (Berries, Field Seeds, Drinks/Snacks, Held Items, Heart Scales). Once per real day per character:
     - Favorite item (`favorite_gifts`): `+20` Rapport + `:gift_love` portrait line.
     - Ordinary item: `+8` Rapport + `:gift_like` portrait line.
   - **`Spar / Rematch`** — Challenges them right there on their `signature_field`, scaled cleanly to your current `Prismfall::LevelCap.current`!
   - **`Leave`**

#### Anti-Trivialization Guard for Narrative Bonds (`NARRATIVE_KEYS.md` Safety)
In `NARRATIVE_KEYS.md`, the 10 Narrative Bonds span `-10..+10` and strictly gate major story branches (e.g., `KESTREL_BEARS >= 8`, `MARISOL >= 3`, `ILSA >= 4`). Infinite gift-spamming must **never** short-circuit story choices. Therefore:
- Hangout chats, gifts, rematches, and tag wins grow **Codex Rapport (`0..100`, displayed as 1–5 Stars `★☆☆☆☆` → `★★★★★`)**.
- For characters with a `:bond_key`, hitting Rapport milestones **Lv. 2 (`25 pts`)**, **Lv. 4 (`70 pts`)**, and **Lv. 5 (`100 pts`)** each grant **`+1` Narrative Bond**, capped at **at most `+1` per Story Act (`V101`) and `+3` lifetime per character** (`codex[:gifts][id][:bond_gained] < 3`).
- Non-Bond characters still get full 1–5 Star Rapport progression, unlocking special Lv. 3 / Lv. 5 hangout banter lines and a Lv. 5 signature keepsake!

---

### 3.2 Pillar 2: Central Repeatable Hub — Lumen Battle Pavilion & Festival Training Court

Inspired by Pokémon Reborn's Grand Hall trainers and Rejuvenation's Gearen Lab / Nightclub Battle Facility, Velmora provides **two linked entry points** to the same `Prismfall::Rematches.open_hub(venue)` engine:

| Venue | Location & Map ID | Unlocks | Purpose & Atmosphere |
|---|---|---|---|
| **Lumen Battle Pavilion** | **Lumen City** — Pavilion wing / reception desk off `180: Concourse` or `184: Arcade Dept. Store 2F` (or dedicated interior map when added; works immediately via an NPC receptionist on `180`/`184`!) | **Ch5 (after Badge 4 — Rook)** | Mid-to-late-game training & rematch hub. Rook & Meridian originally built it as a "Broadcast Sparring Floor"; after Ch5 it becomes Velmora's independent training pavilion. Supports **On-Demand Singles, Doubles, and 2v2 Tag Battles** with any unlocked repeatable cast member! |
| **Festival Training Court** | **Crownhaven** — `499: Festival Grounds - Court of Eight Pavilions` (reception pavilion) and post-game `493: Concordance Spire - Lobby` | **Ch20 (Festival Week) & Post-Game (`S160`)** | Late/post-game master court. Unlocks **Lv. 90–100 Master Ruleset**, **Random Cast Gauntlet (3-wave)**, and connects seamlessly with `910: Antumbra - Distortion Core`'s **Hall of Reflections** for alternate-timeline/Fallen/Ruin variants recorded in `Prismfall::Ledger.met_list`! |

> **Direct Codex Shortcut:** When the player opens the Character Codex (`028_Codex_Scene.rb`) while standing inside a Hub map (`Prismfall::Rematches::HUB_MAPS.include?($game_map.map_id)`), pressing `[C]` on any eligible character's Rematch Card offers immediate **`Challenge Here`** or **`Invite as Tag Partner`** without even walking back to the reception desk!

#### Hub Menu Options (`pf_rematch_hub(:LUMEN_PAVILION)` / `pf_rematch_hub(:FESTIVAL_COURT)`)
1. **`Spar with an Opponent (1v1 / 2v2)`**
   - Pick any unlocked Codex character whose `:repeatable` unlock is met (grouped by tab: Allies / Leaders / Factions / Wanderers, with `(★ Today's Bonus)` badge if their daily seed bonus hasn't been claimed yet!).
   - Choose format (`Single` / `Double`, respecting `:double_ok`).
   - Choose field: **Signature Field** (default), **Standard Arena (`:NONE`)**, or **Pick from Field Notes** (any field seen in `FieldEffects::FieldNotes`!).
2. **`Tag-Battle Practice (2v2 Multi-Battle — Left-Hand Ally Showcase!)`**
   - **Step 1:** Choose ANY unlocked eligible Codex character as your **Tag Partner** (Juno, Kestrel, Marisol, Rook, Sigrun, Thistle, Teo, Vesper, any Expanded Cast rival/side character, etc.).
   - **Step 2:** Choose opposing duo:
     - **Curated Iconic Duos** (unlocked once both foes are in the Codex!):
       - *Stage & Stream:* Dorian & Rook (`:GRAND_STAGE` / `:NEON_GRID`)
       - *Tide & Frost:* Marisol & Anja (`:WATER_SURFACE` / `:FROZEN_LAKE`)
       - *Forge & Flame:* Brann & Sigrun (`:VOLCANIC` / `:DRAGONS_DEN`)
       - *Quiet Ward & Underveil:* Corvin & Nyx (`:CORROSIVE_MIRE` / `:NEW_MOON`)
       - *Special Projects:* Dr. Quent & Sabine Kroll (`:FACTORY` / `:SCRAPYARD`)
       - *Lantern Front:* Thistle & Teo (`:SILKWOOD` / `:BLEED`)
       - *Octave Duet:* Vesper & any helped Chorister (`:GRAND_STAGE`)
     - **Custom Pair:** Pick any two unlocked opponents!
     - **Random Unlocked Pair:** Instant surprise matchup for +1 extra Heart Scale!
3. **`Daily Featured Matchup`** *(3 deterministic daily opponents seeded by `pbGetTimeNow.strftime("%Y%m%d").to_i` — Reborn Grand Hall style! Gives 2× Exp Candy bonus on first clear of the day!)*
4. **`View Hub Record & Codex`** — Opens `PrismfallCodexScene` directly.

---

### 3.3 Dynamic LevelCap Scaling Engine (Zero PBS Bloat!)

A major engineering risk of 40–60+ repeatable characters across an 18-badge game is PBS bloat (writing 18 versions × 3 difficulties × 50 characters = 2,700 trainer blocks — unacceptable!). Instead, `029_Rematches.rb` solves this with **Two-Layer Hybrid Scaling**:

#### Layer 1: Compact Tiered PBS Templates (1–3 templates per character)
Each repeatable character uses their **existing** PBS teams plus at most 1–2 high-level versions:
- `tier_versions => { 0 => 0, 50 => 0, 85 => 90 }` (picks the highest threshold `<= target_level` whose `[type, name, ver]` actually exists in `GameData::Trainer`!).
- `004_Difficulty.rb`'s existing `pbLoadTrainer` hook (`+100` Hard / `+200` Casual, fallback to base) runs **first** automatically — preserving Casual/Standard/Hard movesets, items, and AI skill floors!
- `006_RivalStarters.rb`'s `:on_trainer_load` hook runs automatically for Juno & Kestrel — keeping their starter matched to the player's chosen Gen 1–9 starter!

#### Layer 2: Scoped `:on_trainer_load` Level & Evolution Scaler
When `Prismfall::Rematches.with_scaling(target_level, role: :opponent)` wraps a rematch or `pbRegisterPartner`:

```ruby
module Prismfall
  module Rematches
    @scale_ctx = nil

    def self.target_level_for(venue = :LUMEN_PAVILION)
      cap = Prismfall::LevelCap.current
      cap = 100 if venue == :FESTIVAL_COURT && Prismfall.all_badges? && Prismfall::LevelCap.finale_unlocked?
      diff_adj = Prismfall::Difficulty.casual? ? -2 : 0
      return (cap + diff_adj).clamp(10, 100)
    end

    def self.with_scaling(target_level, role: :opponent, max_party: 6)
      prev = @scale_ctx
      @scale_ctx = { :target => target_level.clamp(5, 100), :role => role, :max_party => max_party }
      yield
    ensure
      @scale_ctx = prev
    end

    def self.scale_trainer!(trainer)
      ctx = @scale_ctx
      return if !ctx || !trainer || !trainer.respond_to?(:party) || trainer.party.empty?
      target = ctx[:target]
      # Trim partner party to 3 Pokemon in 2v2 Multi-Battles (standard Essentials partner balance)
      if ctx[:role] == :partner && trainer.party.length > ctx[:max_party]
        # Keep ace (last slot) + first (max_party - 1) members
        ace = trainer.party.last
        rest = trainer.party[0, ctx[:max_party] - 1]
        trainer.party = rest + [ace]
      end
      base_ace = trainer.party.map(&:level).max || target
      trainer.party.each do |pkmn|
        next if !pkmn || pkmn.egg?
        offset = base_ace - pkmn.level                       # Preserve relative spread (e.g., ace at cap, team at cap - 2)
        new_lv = (target - offset.clamp(0, 4)).clamp(5, 100)
        next if new_lv == pkmn.level
        evolved = maybe_promote_evolution!(pkmn, new_lv) if new_lv > pkmn.level + 10
        pkmn.level = new_lv
        # Only reset moves if we promoted an early-game unevolved template upward significantly
        pkmn.reset_moves if evolved
        pkmn.calc_stats
        pkmn.heal
      end
    end

    # Promotes early templates (e.g., Gym 2 Lv.19 Swadloon fought at Cap 59) along natural level evolutions.
    def self.maybe_promote_evolution!(pkmn, new_lv)
      changed = false
      2.times do
        evos = pkmn.species_data.get_evolutions(true)
        break if !evos || evos.empty?
        # Pick deterministic level-up or happiness/stone evolution once well above threshold
        cand = evos.find { |sp, method, param|
          (method == :Level && param.is_a?(Integer) && new_lv >= param) ||
          (new_lv >= 36 && [:Happiness, :HappinessDay, :HappinessNight, :Item].include?(method))
        }
        break if !cand || !GameData::Species.exists?(cand[0])
        pkmn.species = cand[0]
        changed = true
      end
      return changed
    end
  end
end

EventHandlers.add(:on_trainer_load, :prismfall_rematch_scaler,
  proc { |trainer| Prismfall::Rematches.scale_trainer!(trainer) }
)
```

> **Why this is rock-solid:**
> - If a high-tier template exists (e.g., Marisol `v90` at Cap 90), `new_lv == pkmn.level` and curated movesets/EVs/items are untouched!
> - If a newly added side character only has a single Ch3 Lv.18 PBS team (`v0`), you can STILL rematch them or tag-partner with them at Cap 47, 67, or 100 — their party smoothly evolves and scales to match your exact LevelCap!
> - On **Hard Mode**, `004_Difficulty.rb` still enforces Set style, no Bag items, and AI skill floor ≥ 48 unless explicitly overridden by battle rules.

---

### 3.4 Tag-Battle Partner Showcase & Left-Hand Back-Throw Ally Sprites

When inviting ANY unlocked Codex character as a **Tag-Battle Partner**:

```ruby
def self.run_tag_battle(partner_id, foe_a_id, foe_b_id, field: nil, venue: :LUMEN_PAVILION)
  target = target_level_for(venue)
  p_spec = resolve_partner_spec(partner_id, target)
  a_spec = resolve_opponent_spec(foe_a_id, target)
  b_spec = resolve_opponent_spec(foe_b_id, target)
  return false if !p_spec || !a_spec || !b_spec

  $player.heal_party
  with_scaling(target, role: :partner, max_party: 3) do
    pbRegisterPartner(p_spec[0], p_spec[1], p_spec[2])
  end
  begin
    setBattleRule("canLose")
    setBattleRule("noMoney")
    Prismfall.set_field_rule(field) if field && field != :NONE
    $game_temp.battle_rules["prismfall_codex_record"] = true
    won = with_scaling(target, role: :opponent, max_party: 3) do
      TrainerBattle.start(a_spec[0], a_spec[1], a_spec[2], b_spec[0], b_spec[1], b_spec[2])
    end
  ensure
    pbDeregisterPartner rescue nil
    $player.heal_party
  end
  record_tag_result(partner_id, foe_a_id, foe_b_id, won ? true : false)
  return won ? true : false
end
```

#### Left-Hand Back-Throw Ally Sprite Contract & Safe Fallback
To let Prismfall's new **LEFT-HAND back-throw ally sprites** shine in every Hub & Story Tag Battle without crashing on characters still awaiting custom back sprites:
1. **Primary Asset Path:** `Graphics/Trainers/<TRAINER_TYPE>_back.png` — 5-frame horizontal `800×160` strip (`160×160` per frame, left-hand side stance facing up-right, matching `graphics/Trainers/PLAYER_A_back.png` and `PLAYER_B_back.png` verified in `REVIEW.md`!).
2. **Secondary EBDX Path:** `Graphics/EBDX/Battlers/Trainers/<TRAINER_TYPE>_back.png` (supported automatically if placed under EBDX's battler tree).
3. **Alias-Chained Fallback in `029_Rematches.rb`:**
   Wrap `GameData::TrainerType.back_sprite_filename(tr_type)` (with `unless method_defined?`):
   - Step 1: Check standard Essentials path (`Graphics/Trainers/<TYPE>_back.png`).
   - Step 2: Check `Graphics/EBDX/Battlers/Trainers/<TYPE>_back.png`.
   - Step 3: Check canonical cast ID alias (e.g., if `LEADER_JUNO_back.png` is absent, reuse `RIVAL_JUNO_back.png`!).
   - Step 4: Graceful gender-matched fallback (`PLAYER_A_back.png` / `PLAYER_B_back.png`) so tagging with **any** of the 50+ Codex characters works **on Day 1** and upgrades automatically the instant their bespoke `_back.png` is dropped into `Graphics/Trainers/`!

---

### 3.5 Rematch Reward Table (`reward_pool`)

Rewards scale cleanly to `Prismfall::LevelCap.current`, giving players a fun, lore-rich anti-grind loop (Exp Candies, Heart Scales, Field Seeds) without breaking the level cap:

| Current `LevelCap` | Guaranteed Candy per Win | Heart Scales | Daily First-Win Field Seed (per character) |
|---|---|---|---|
| `≤ 23` (Gyms 1–3) | `:EXPCANDYXS × 3` | `:HEARTSCALE × 1` | Signature Field Family Seed × 1 |
| `24–39` (Gyms 4–7) | `:EXPCANDYS × 3` | `:HEARTSCALE × 1` | Signature Field Family Seed × 1 |
| `40–59` (Gyms 8–12) | `:EXPCANDYM × 3` | `:HEARTSCALE × 1` | Signature Field Family Seed × 1 |
| `60–80` (Gyms 13–17) | `:EXPCANDYL × 2` | `:HEARTSCALE × 2` | Signature Field Family Seed × 1 |
| `81–100` (Gym 18 / Festival / Post-Game) | `:EXPCANDYXL × 2` | `:HEARTSCALE × 2` | Signature Field Family Seed × 1 |

- **Field Seed Resolution:** Automatically reads `FieldEffects::FAMILY_SEEDS[FieldEffects.get(sig_field)[:family]]` → `:ELEMENTALSEED`, `:MAGICALSEED`, `:TELLURICSEED`, or `:SYNTHETICSEED` (all four already defined in `pbs/items_fields.txt`!), or uses `reward_pool[:seed]` if explicitly specified.
- **Bonus Modifiers:**
  - **Hard Mode** or **Tag-Battle Win:** `+1` extra Heart Scale (`+1` Exp Candy on Daily Featured Matchup!).
  - **First Rematch Win (`first_win_rewarded == false`):** Character-specific signature reward from `reward_pool[:first_win]` (held item, TM, or regional keepsake).
  - **First Tag Partner Win (`first_tag_rewarded == false`):** Partner keepsake from `reward_pool[:first_tag]` (specialty Poké Balls, Mint, or Field Seed ×2).

---

## 4. Repeatable Cast Onboarding Contract (For Expanded Cast & Bespoke Classes)

To guarantee that **every new recurring side character & villain-org personality** introduced alongside the bespoke Trainer Classes pass is immediately inside the Codex and repeatable, each new character requires **only**:

1. **PBS Trainer Type (`pbs/trainer_types.txt`):** Unique `[TYPE_ID]` with bespoke `Name = <Unique Class>` (e.g., `[WANDERER_...]`, `[HOLLOW_...]`, `[MERIDIAN_...]`).
2. **At least 1 PBS Trainer Team (`pbs/trainers.txt`):** Their first encounter `v0` (and optional mid/late `v50`/`v90` if they evolve a signature team). Layer 2 scaling automatically covers every other LevelCap!
3. **1 `Prismfall::Codex.register(:ID, ...)` block in `027_Codex_Data.rb`** specifying:
   - `:category => :WANDERERS` (for recurring rivals/side characters) or `:FACTIONS` (for expanded Hollow/Meridian/Octave personalities)
   - `:trainer_type => :THEIR_TYPE`
   - `:progressive_bios` (minimum 2 entries: intro + post-arc)
   - `:where_now` (at least 1 active location + post-game hub line)
   - `:repeatable` block (`rematch_trainer`, `rematch_map`, `dialogue_pool`, `reward_pool`)
4. **1 World Hangout Event (optional, 2 lines):** `Condition: codex_hangout_here(:ID)` + `Script: pf_hangout(:ID)`. Even before the map event is placed, the character is **already fightable & tag-partnerable** in the Lumen Battle Pavilion / Festival Training Court the moment they unlock in the Codex!

### Complete Initial Codex Roster Coverage Checklist

| Tab | Baseline Entries to Seed in `027_Codex_Data.rb` | Repeatable? |
|---|---|---|
| **Allies & Rivals** | Juno Hale, Kestrel Vane, Prof. Imelda Larch, Capt. Edda Morrow, Sovereign Valen Corrigan, Hesper Vane, Pip Ore, Wenlow *(memorial post-Ch16)*, Hierophant Maud Ellery | Juno, Kestrel, Valen *(post-game / reflections)*, Larch *(optional spar!)*, Edda *(optional spar!)* |
| **18 League Leaders** | All 18 Wardens in exact `Prismfall::GYMS` order (`01` Dorian → `18` Sigrun), pulling live bespoke classes from `GameData::TrainerType` | **All 18** (Opponent + Tag Partner + World Hangout!) |
| **Factions & Adversaries** | **Hollow:** Rowan Ashby / The Mourner, Brother Wick, Mara "Thistle" Thistlewood, Teo Reyes · **Meridian:** Aurelian Voss, Dr. Percival Quent, Director Helene Marchetti, Sabine Kroll ("Sable"), Calla Wren, Chancellor Hollis · **Octave:** Vesper Lindqvist + all 8 Choristers (Lyra, Aria, Cadence, Sona, Noct, Forte, Lento, Carol) · **Kingdoms/Ruin:** Queen Maelis, Prince Caedmon, Archseer Dask, Thane Eirik, Dominar Hrothgar, Elector Kassan, Councillor Sallow, Mother Gutter, Envoy Okoro, Echo Morwen *(secret)*, King Theodric *(secret, Ruin)* · **+ Expanded Hollow/Meridian Personalities** | Wick, Thistle, Teo *(if alive)*, Marchetti *(if turned/post)*, Kroll *(hub/reflections)*, Quent *(hub/reflections)*, Voss *(reflections)*, Vesper + all 8 Octave Choristers, Dask *(Ruin/reflections)*, Morwen *(exhibition/reflections)*, + all new Villain-Org personalities |
| **Wanderers & Side Cast** | **All new Reborn/Rejuv-style recurring side characters & repeatable rivals** + Dex, Six-Fingers Ottoline, Clerk Fenwright + **10 Sister-Game Cameos** (Lin, Amaria, Shelly, Alexandra, Venam, Shiv, Garret, Melia, Titania, Nova *[Ruin secret]*) | **All recurring side rivals & cameos** (Opponent + Tag Partner + Hangouts!) |

---

## 5. Save-Safe Persistence & Migration (`002_SaveState.rb`)

### 5.1 Marshal-Safe Schema (`Prismfall.state.codex`)

Follows the exact pattern of `013_Narrative_State.rb` (`@narrative`) and `002_Trials_State.rb` (`@trials`): plain Ruby primitives only (`Symbol`, `Integer`, `String`, `Boolean`, `Hash`, `Array`) — **zero Procs, zero custom structs**, guaranteeing `Marshal.dump`/`Marshal.load` never breaks across updates.

```ruby
# In 002_SaveState.rb (minimal diff: add :codex accessor + migrate! guard)
class Prismfall::SaveState
  attr_accessor :codex   # Hash (see 027_Codex_Data.rb)
  # Inside initialize: @codex = {}
  # Inside migrate!:   @codex = {} if !@codex.is_a?(Hash)
end
```

```ruby
# In 027_Codex_Data.rb (lazy-normalizing getter — safe even on pre-Codex saves!)
class Prismfall::SaveState
  def codex
    @codex = {} if !@codex.is_a?(Hash)
    c = @codex
    c[:version]    ||= 1
    c[:unlocked]   ||= {}   # id => { :at => play_time_i, :via => :portrait/:battle/:partner/:sync, :bio_ver => Integer }
    c[:rematches]  ||= {}   # id => { :wins => 0, :losses => 0, :tag_wins => 0, :last_day => nil, :first_win => false, :first_tag => false }
    c[:rapport]    ||= {}   # id => Integer (0..100)
    c[:gifts]      ||= {}   # id => { :count => 0, :last_day => nil, :bond_gained => 0, :last_bond_act => -1 }
    c[:banter_idx] ||= {}   # id => Integer
    c[:hub_stats]  ||= { :total_wins => 0, :total_tag_wins => 0, :daily_date => nil, :daily_cleared => [] }
    c[:ui_prefs]   ||= { :last_tab => 0, :last_notebook_tab => 1 }
    return c
  end
end
```

### 5.2 Backwards-Compatible Save Load & Silent Backfill

Inside `SaveData.register(:prismfall_core)` (`002_SaveState.rb`, `load_value` block):

```ruby
load_value do |value|
  $prismfall = (value.is_a?(Prismfall::SaveState)) ? value : Prismfall::SaveState.new
  $prismfall.migrate!
  Prismfall.ensure_badge_array if Prismfall.respond_to?(:ensure_badge_array)
  Prismfall::Codex.sync_from_progress!(silent: true) if defined?(Prismfall::Codex)
end
```

`Prismfall::Codex.sync_from_progress!(silent: true)` inspects:
1. All registered entries whose `:unlock_condition` already evaluates `true` (switches, vars, choices, flags).
2. All 18 Leaders whose badge is already owned (`Prismfall.has_badge?(g[:gym_index])`).
3. All Eevee Octave Choristers in `Prismfall::Trials::Octave.order` (if Trials is loaded).
4. All Festival opponents in `Prismfall::Ledger.met_list` and cameos in `Prismfall::Ledger.cameos_beaten`.

Existing saves mid-way through Acts I–V load with **zero errors**, **zero toast spam**, and an immediately populated Codex matching everything the player has already experienced!

---

## 6. Validation & Headless Selftest Harness

### 6.1 `024_NarrativeCheck.rb` Integration

Append one line inside `Prismfall::NarrativeCheck.run`:
```ruby
errors.concat(Prismfall::Codex.validate.map { |e| "Codex: #{e}" }) if defined?(Prismfall::Codex)
```

`Prismfall::Codex.validate` checks at boot (debug) and via **Debug → Prismfall Core → Show Core status**:
- Every condition string inside `:unlock_condition`, `:hide_when`, `:name`, `:trainer_type`, `:faction`, `:region`, `:ace_species`, `:also_in`, `:progressive_bios`, `:where_now`, `:repeatable[:unlock]`, and `:repeatable[:unavailable_when]` passes `Prismfall::Conditions.check` and references only registered choices/flags/bonds/tallies.
- Every `:bond_key` exists in `Prismfall::Narrative::BONDS`.
- Every `:signature_field` exists in `FieldEffects` (when loaded).
- Every `:ace_species` exists in `GameData::Species` (when compiled).
- Every `:trainer_type` exists in `GameData::TrainerType` (warns cleanly if a pending PBS drop hasn't landed yet).
- `:LEADERS` covers `gym_index` `1..18` cleanly with zero gaps or duplicates.
- Every character in `Prismfall::Trials::Octave::SINGERS` and `Prismfall::Narrative::CAMEOS` has a Codex entry.

### 6.2 Debug Menu Tools (`027_Codex_Data.rb` / `011_Debug.rb`)

Add `"Codex & Rematches..."` under `:prismfall_core_menu`:
- `Open Codex` · `Unlock All Codex Entries` · `Reset Codex State` · `Test Toast Notification` · `Open Lumen Battle Pavilion (Remote)` · `Open Festival Training Court (Remote)`.

### 6.3 Headless Harness Suite (`tools/harness/run_codex.rb`)

Modeled directly on `tools/harness/run_trials.rb` (runs via `PRISM_RUN_DIR=<copy> PRISM_COMPILE=1 ruby tools/harness/run_codex.rb`, exits `1` on any failure):

| # | Test Suite | Assertions |
|---|---|---|
| **1** | **Schema & Static Data Check** | `Prismfall::Codex.validate` returns `[]`; all 18 Leaders map 1:1 to `Prismfall::GYMS`; `Codex.trainer_class(:MARISOL) == GameData::TrainerType.get(:LEADER_MARISOL).name` (single source of truth verified!). |
| **2** | **Auto-Discovery & Toast Queue** | Emitting `:prismfall_portrait_opened` unlocks `:JUNO` once (`via: :portrait`) and queues 1 toast; re-emitting does not duplicate; running a headless `TrainerBattle` against `:LEADER_DORIAN` unlocks `:DORIAN` (`via: :battle`); tag partner battle unlocks partner (`via: :partner`); 5 simultaneous unlocks coalesce cleanly; headless mode allocates zero Sprites/Viewports. |
| **3** | **Identity Masking & Spoiler-Free Bios** | Before `S124`: `:MOURNER` visible in `:FACTIONS`, `:ROWAN` in `:LEADERS` with Act I bio only; after `S124 = true`: `:MOURNER` hidden, `:ROWAN` moves to `:FACTIONS`, inherits battle count, updates title/bio. Before `S136`: `:KROLL` displays `"Sable"` + `:HOLLOW_SABLE` class; after `S136 = true`: displays `"Sabine Kroll"` + `:MERIDIAN_KROLL` class. Before `S125`: `:JUNO` uses `:RIVAL_JUNO`; after `S125 = true`: `:LEADER_JUNO` + Leader Seat `#09`. |
| **4** | **Save Round-Trip & Legacy Migration** | `SaveState` with `@codex = nil` runs `migrate!` cleanly; `Marshal.load(Marshal.dump($prismfall))` preserves all unlocked cards, rematch wins, rapport, and banter cursors; `sync_from_progress!(silent: true)` backfills Leaders 1–6 when 6 badges are set with zero queued toasts. |
| **5** | **Dynamic LevelCap Scaling & Tag Partner Battles** | At 3 badges (`LevelCap = 27`), rematching `:LEADER_DORIAN` scales his team cleanly to Lv. 27; at 10 badges (`LevelCap = 55`), rematching `:LEADER_TAMSIN` promotes Swadloon → Leavanny and scales to Lv. 55; Casual/Standard/Hard offsets apply cleanly; running `run_tag_battle(:JUNO, :DORIAN, :ROOK)` registers Juno with 3 scaled Pokémon, runs a real headless Essentials v21.1 2v2 battle, cleans up `$PokemonGlobal.partner == nil` even on forced loss, and increments `tag_wins` + grants scaled Exp Candy, Heart Scale, and Field Seed. |
| **6** | **Bond Cap & `:OPEN_BOOK` Integration** | Gifting Marisol 10 times in Act I grants at most `+1` Narrative Bond in Act I (never breaks `NARRATIVE_KEYS` math) while advancing Rapport Stars; enabling `:OPEN_BOOK` surfaces numeric Bond readout in `Codex.bond_label(:MARISOL)`. |

---

## 7. Wednesday Implementation Order for Claude

1. **Step 1 (Save & PBS Prep — ~10 min):** Add `@codex` to `002_SaveState.rb`, add `[FIELDNOTES]` to `pbs/items_fields.txt`, and add the 2-line `EventHandlers.trigger(:prismfall_portrait_opened, ...)` hook to `014_Portraits.rb`.
2. **Step 2 (`027_Codex_Data.rb` — ~45 min):** Implement `Prismfall::Codex` core module, dynamic resolver, `Battle#pbStartBattleCore` hook, `Toast` HUD, condition functions, `validate`, and seed the complete baseline cast + drop-in entries from the bespoke classes / expanded cast specs.
3. **Step 3 (`028_Codex_Scene.rb` — ~45 min):** Build the `512×384` `PrismfallCodexScene`, `PrismfallNotebookHub` (`:FIELDNOTES` `Fields | People | Quests | Ledger` switcher), and Pause Menu ordering (`43/44/45/46`).
4. **Step 4 (`029_Rematches.rb` — ~45 min):** Implement `Prismfall::Rematches` (Hangout engine, Lumen Battle Pavilion & Festival Training Court menus, two-layer `LevelCap` scaler, Tag Partner `pbRegisterPartner` + left-hand `_back.png` fallback resolver, and reward tables).
5. **Step 5 (Verification — ~20 min):** Wire `Prismfall::Codex.validate` into `024_NarrativeCheck.rb`, run `tools/harness/run_codex.rb`, plus regression check `run_all.rb` and `run_trials.rb` (0 errors).
