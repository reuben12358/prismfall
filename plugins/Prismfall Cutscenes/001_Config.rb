#===============================================================================
# Prismfall Cutscenes - 001 Config
#-------------------------------------------------------------------------------
# Code-driven pixel cutscenes (SPINE Revision 6). Everything here is tunable.
# Docs: design/CUTSCENES.md
#===============================================================================
module Prismfall
  module Cutscene
    VERSION        = "1.0.0"
    PX             = 2        # one "art pixel" = PX screen pixels (all FX are drawn on this grid)
    FX_FPS         = 30       # FX layers redraw at this rate (animating "on twos" reads as pixel art)
    MAX_DT         = 0.1      # longest time step accepted per frame (lag never skips content)
    TICK           = 0.05     # one RMXP event "Wait 1" in Reborn/Rejuvenation (40 FPS, 2 frames): port event timings as n * TICK
    VIEWPORT_Z     = 99_990
    SKIP_BUTTONS   = [:BACK]  # Input constants; hold one to skip
    SKIP_HOLD      = 0.7      # seconds
    MASH_BUTTON    = :USE
    FADE_TIME      = 0.4      # automatic fade in/out of every scene
    MAX_PARTICLES  = 260
    BEAM_CHUNK     = 4        # art pixels per beam segment
    BEAM_DITHER    = true     # dithered fringes between beam colours (set false on very weak machines)
    POKEMON_ANIM_FPS = 20     # EBDX sprite strips
    # Sprites up to this height are native-resolution art and are shown at 2x
    # (EBDX battlers/trainers); taller ones are already doubled.
    NATIVE_SPRITE_MAX_HEIGHT = 128
    TEXT_COLOR     = [248, 248, 248]
    TEXT_SHADOW    = [24, 24, 32]

    # Effect palettes: [core, inner, outer, edge] (4 colours per effect).
    PALETTES = {
      # the war's two beams: orange-red-violet against cyan-blue-white
      :fireclash => [[255, 255, 224], [255, 200, 56],  [240, 80, 32],   [136, 40, 168]],
      :seaclash  => [[255, 255, 255], [168, 248, 255], [40, 152, 248],  [24, 64, 184]],
      :fire     => [[255, 250, 220], [255, 208, 64],  [240, 112, 24],  [160, 32, 16]],
      :blueflare=> [[255, 255, 255], [200, 236, 255], [96, 168, 255],  [232, 96, 32]],
      :water    => [[236, 252, 255], [120, 208, 255], [40, 120, 232],  [16, 48, 152]],
      :ice      => [[255, 255, 255], [184, 240, 255], [96, 184, 232],  [48, 96, 176]],
      :dragon   => [[240, 224, 255], [168, 120, 255], [96, 56, 216],   [48, 24, 120]],
      :electric => [[255, 255, 232], [255, 240, 96],  [232, 184, 24],  [136, 96, 8]],
      :grass    => [[240, 255, 216], [152, 232, 88],  [56, 168, 56],   [16, 88, 40]],
      :psychic  => [[255, 232, 248], [255, 128, 192], [216, 56, 136],  [112, 16, 88]],
      :dark     => [[200, 184, 216], [112, 88, 136],  [56, 40, 80],    [16, 8, 32]],
      :ghost    => [[224, 208, 255], [144, 112, 216], [80, 56, 152],   [32, 16, 72]],
      :fairy    => [[255, 240, 248], [255, 176, 216], [232, 112, 176], [152, 56, 112]],
      :steel    => [[248, 248, 255], [200, 208, 224], [136, 144, 168], [72, 80, 104]],
      :poison   => [[248, 224, 255], [200, 112, 224], [136, 48, 168],  [72, 16, 96]],
      :ground   => [[255, 240, 208], [224, 184, 112], [168, 120, 56],  [96, 64, 24]],
      :rock     => [[240, 232, 208], [192, 176, 128], [136, 120, 80],  [80, 64, 40]],
      :fighting => [[255, 232, 216], [240, 128, 88],  [192, 56, 40],   [104, 24, 16]],
      :bug      => [[248, 255, 200], [184, 216, 64],  [120, 152, 24],  [64, 88, 8]],
      :flying   => [[248, 252, 255], [184, 208, 255], [120, 152, 232], [64, 88, 160]],
      :light    => [[255, 255, 255], [248, 240, 200], [216, 200, 144], [136, 120, 88]],
      :white    => [[255, 255, 255], [240, 240, 248], [200, 200, 216], [136, 136, 160]],
      :bleed    => [[255, 255, 255], [255, 176, 232], [112, 224, 216], [136, 96, 216]],
      :smoke    => [[200, 200, 200], [136, 136, 144], [88, 88, 96],    [48, 48, 56]],
      :steam    => [[255, 255, 255], [224, 236, 240], [176, 196, 208], [120, 144, 160]]
    }
    TYPE_PALETTES = {
      :NORMAL => :light, :FIRE => :fire, :WATER => :water, :ICE => :ice, :DRAGON => :dragon,
      :ELECTRIC => :electric, :GRASS => :grass, :PSYCHIC => :psychic, :DARK => :dark, :GHOST => :ghost,
      :FAIRY => :fairy, :STEEL => :steel, :POISON => :poison, :GROUND => :ground, :ROCK => :rock,
      :FIGHTING => :fighting, :BUG => :bug, :FLYING => :flying
    }

    # Audio cues (design/AUDIO.md names first, stock/EBDX stand-ins after). The
    # first file that exists is played; a cue with no file is silent.
    AUDIO = {
      :beam_charge  => ["Beam charge", "Anim/Charge_Beam", "Anim/Flash2"],
      :beam_fire    => ["Beam fire", "Anim/HyperBeam"],
      :beam_clash   => ["Beam clash", "Anim/HyperBeam", "Anim/Explosion"],
      :beam_break   => ["Beam break", "Anim/Explosion", "Voltorb Flip explosion"],
      :impact       => ["Battle damage normal"],
      :impact_super => ["Battle damage super"],
      :explosion    => ["Anim/Explosion", "Voltorb Flip explosion"],
      :rumble       => ["Mining collapse", "Anim/Earth1"],
      :crowd_cheer  => ["Crowd cheer", "Anim/Applause"],
      :crowd_gasp   => ["Crowd gasp"],
      :faint        => ["Pkmn faint"],
      :chime        => ["Mining ping", "Pkmn exp full"],
      :card         => ["GUI trainer card open"],
      :bgm_war_field   => ["War - Battlefield", "Battle Elite"],
      :bgm_war_clash   => ["War - Beam Clash", "Battle Champion"],
      :bgm_war_after   => ["War - Aftermath"],
      :bgs_war         => ["War - Distant Battle"],
      :bgs_rain        => ["Rain"],
      :bgm_highlight   => ["Festival - Highlights", "B2W2 212 PWT Final Round!"],
      :me_hl_start     => ["Festival highlight start", "BP Fanfare"],
      :me_hl_hit       => ["Festival highlight hit"],
      :me_hl_result    => ["Festival highlight result", "Slots win"],

      # --- Audio v4.3 / v4.4 cue matrix (gemini_recommends/2026-11-21_audio-mastering-and-soundscape:
      # WIRING_SPEC.md + CUTSCENE_AND_NEW_CAST_AUDIO.md 1B). Every list starts with the slot's own file
      # (audio/manifest.tsv) and ends on a file that exists today, so a cue upgrades by dropping a file in.
      # Battle / Layer 0 hits (CC0 pack)
      :field_shatter   => ["Field Shatter", "Anim/Explosion"],
      :boss_shield     => ["Boss Shield Break", "Battle damage super"],
      :glass_quench    => ["Glass Quench", "Anim/Ice1", "Mining ping"],
      :prism_swell     => ["Prism Arena Swell", "Anim/Flash2"],
      :vs_lightning    => ["VS Cutin Lightning", "Anim/Thunder1", "Vs sword"],
      :glass_shatter   => ["Glass Shatter Burst", "Field Shatter", "Anim/Explosion"],
      :hitstop_boom    => ["Impact Hitstop Boom", "Boss Shield Break", "Battle damage super"],
      :glitch_tear     => ["Glitch Tear Static", "Glass Quench", "Anim/Flash2"],
      :chapter_wipe    => ["Chapter Card Prismatic Wipe", "Prism Arena Swell", "Pkmn exp full"],
      :mirror_crack    => ["Mirror Crack", "Glass Quench", "Field Shatter"],
      :eye_flash       => ["Ace Eye-Flash Zing", "VS Cutin Lightning", "Anim/Flash2"],
      :rifle_crack     => ["Directorate Rifle Crack", "Beam break", "Anim/Explosion"],
      :ring_harmonic   => ["Ring Glass Harmonic", "Glass Quench", "Mining ping"],
      :void_implode    => ["Void Eat Bass Implosion", "Beam break", "Mining collapse"],
      :heartbeat       => ["Heartbeat Sub-Pulse", "Battle damage normal"],
      :ferry_horn      => ["Ferry Foghorn", "Prism Arena Swell"],
      # Named in the Rejuv V14 cinematics spec with no file of their own yet: the nearest CC0 hit stands in
      # (drop "Blade Pierce" / "Mask Crack" / "Bell Break" into Audio/SE to replace it).
      :blade_pierce    => ["Blade Pierce", "Mirror Crack", "Glass Shatter Burst", "Anim/Slash"],     # dry crystalline pierce
      :mask_crack      => ["Mask Crack", "Mirror Crack", "Glass Quench", "Anim/Ice1"],               # one razor-sharp snap
      :bell_break      => ["Bell Break", "Glass Shatter Burst", "Field Shatter", "Anim/Explosion"],  # "every bell breaking at once"
      # Ambience loops (the nine CC0 BGS)
      :bgs_bleed       => ["Glassfall Bleed"],
      :bgs_harbor      => ["Saltmere Harbor"],
      :bgs_isenmar     => ["Wind - Isenmar"],
      :bgs_ashkaar     => ["Lava - Ashkaar"],
      :bgs_machinery   => ["Machinery - Zenith"],
      :bgs_drip        => ["Drip - Nadir"],
      :bgs_deepwood    => ["Gossamer Deepwood"],
      # Jingles
      :me_game_over    => ["Prismfall game over", "Voltorb Flip game over"],
      :me_badge_get    => ["Warden Badge Get", "Badge get"],
      :me_trial_rank   => ["Trial Rank Up", "Item get"],
      # Cutscene music: [Phase-2 soundtrack slot (design/AUDIO_SOUNDTRACK_PLAN.md), today's manifest slot, ...].
      # (The Gilded King has no cue here: his music is on hold.)
      :bgm_last_ferry      => ["Intro - Last Ferry"],
      :bgm_saltmere        => ["Town - Saltmere", "Town - Elowen"],
      :bgm_verdance        => ["Town - Verdance", "Town - Elowen"],
      :bgm_gloaming        => ["Town - Gloaming", "Town - Elowen"],
      :bgm_mirefen         => ["Town - Mirefen", "Town - Nadir"],
      :bgm_bleed_zone      => ["Dungeon - Bleed Zones", "Mood - Mystery", "Route - Antumbra"],
      :bgm_ruins           => ["Dungeon - Ruins"],
      :bgm_sky_tower       => ["Dungeon - Sky Tower", "Route - Zenith", "Dungeon - Deep"],
      :bgm_drowned_aurelia => ["Dungeon - Drowned Aurelia", "Dungeon - Ruins"],
      :bgm_cinderhorn      => ["Dungeon - Cinderhorn", "Route - Ashkaar", "Dungeon - Deep"],
      :bgm_ashkaar_route   => ["Route - Ashkaar"],
      :bgm_ruin_purgatorium => ["Dungeon - Distortion Core", "Route - Antumbra", "Ending - Ruin"],
      :bgm_mood_mystery    => ["Mood - Mystery"],
      :bgm_mood_tension    => ["Mood - Tension"],
      :bgm_mood_farewell   => ["Mood - Farewell"],
      :bgm_mood_hope       => ["Mood - Theme of Hope", "Mood - Emotion"],
      :bgm_theme_hollow    => ["Theme - Hollow"],
      :bgm_theme_meridian  => ["Theme - Meridian"],
      :bgm_theme_accord    => ["Theme - Accord"],
      :bgm_war_march       => ["War - Frontlines", "War - March"],
      :bgm_mourner         => ["Battle - Mourner", "Battle Elite"],
      :bgm_marchetti       => ["Battle - Marchetti", "Battle - Meridian Admin", "Battle Elite"],
      :bgm_tribunal        => ["Battle - Tribunal Ambush", "Battle - Meridian Admin", "Mood - Tension"],
      :bgm_kestrel_k8      => ["Battle - Kestrel K8", "Battle - Kestrel", "Battle Elite"],
      :bgm_voss            => ["Battle - Voss", "Battle Champion"],
      :bgm_valen           => ["Battle - Sovereign Valen", "Battle - Valen", "Battle Champion"],
      :bgm_arceus          => ["Battle - Arceus", "Battle - Boss"],
      :bgm_ruin_arceus     => ["Battle - Arceus Final", "Battle - Arceus", "Battle - Ruin"],
      :bgm_boss_loyal_three => ["Boss - Loyal Three", "Battle - Boss"],
      :bgm_boss_kyogre     => ["Boss - Kyogre", "Battle - Legendary", "Battle - Boss"],
      :bgm_boss_zekrom     => ["Boss - Zekrom", "Battle - Legendary", "Battle - Boss"],
      :bgm_boss_reshiram   => ["Boss - Reshiram", "Battle - Legendary", "Battle - Boss Final Bar"],
      :bgm_mindscape       => ["Boss - Mindscape Nightmare", "Route - Antumbra", "Mood - Mystery"],
      :bgm_echo_morwen     => ["Boss - Echo of Morwen", "Battle - Warden", "Dungeon - Manor"],
      :bgm_ruin_reflection => ["Battle - Ruin Reflection", "Battle - Ruin"],
      :bgm_ruin_dask       => ["Ruin - Archseer Dask", "Battle - Ruin"],
      :bgm_victory_sov     => ["Victory - Sovereign", "B2W2 214 PWT Victor!", "Battle victory leader"],
      :bgm_end_homecoming  => ["Ending - Homecoming"],
      :bgm_end_ruin        => ["Ending - Ruin"]
    }
    # Stock sprites that stand in for Prismfall trainer types until their own
    # art exists (Graphics/Trainers/X.png and Graphics/Characters/trainer_X.png).
    # Own art always wins; with neither, a code-drawn figure is used.
    STAND_INS = {
      :ASHKAAR_SOLDIER => :BLACKBELT,     :ASHKAAR_SOLDIER_M => :BLACKBELT,  :ASHKAAR_SOLDIER_F => :CRUSHGIRL,
      :ASHKAAR_OFFICER => :ELITEFOUR_Lance,
      :ISENMAR_SOLDIER => :SAILOR,        :ISENMAR_SOLDIER_M => :SAILOR,     :ISENMAR_SOLDIER_F => :SWIMMER2_F,
      :ISENMAR_OFFICER => :ELITEFOUR_Bruno,
      :MERIDIAN_QUENT  => :PROFESSOR,     :MERIDIAN_AGENT => :SCIENTIST,     :MERIDIAN_AGENT_M => :SCIENTIST,
      :MERIDIAN_AGENT_F => :SCIENTIST,    :MERIDIAN_ADMIN => :SUPERNERD,     :MERIDIAN_VOSS => :ROCKETBOSS,
      :LEADER_SIGRUN   => :COOLTRAINER_F, :LEADER_ANJA => :ELITEFOUR_Lorelei, :LEADER_BRANN => :HIKER,
      :LEADER_MARISOL  => :SWIMMER2_F,    :LEADER_KAITO => :BLACKBELT,       :LEADER_ROOK => :ROCKER,
      :LEADER_ODESSA   => :BIRDKEEPER,    :LEADER_YSOLDE => :CHANNELER,      :LEADER_CELESTINE => :LADY,
      :LEADER_NYX      => :BEAUTY,        :LEADER_MAGNUS => :ENGINEER,       :LEADER_TAMSIN => :BUGCATCHER,
      :LEADER_DORIAN   => :GENTLEMAN,     :LEADER_JUNO => :PICNICKER,        :RIVAL_JUNO => :PICNICKER,
      :RIVAL_KESTREL   => :RIVAL1,        :CHAMPION_VALEN => :CHAMPION
    }

    HIGHLIGHT_BGM_VOLUME = 70
    HIGHLIGHT_MIN_SECONDS = 15.0
    HIGHLIGHT_MAX_SECONDS = 30.0
  end
end
