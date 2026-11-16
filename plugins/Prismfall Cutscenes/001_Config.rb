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
    VIEWPORT_Z     = 99_990
    SKIP_BUTTONS   = [:BACK]  # Input constants; hold one to skip
    SKIP_HOLD      = 0.7      # seconds
    MASH_BUTTON    = :USE
    FADE_TIME      = 0.4      # automatic fade in/out of every scene
    MAX_PARTICLES  = 260
    BEAM_CHUNK     = 3        # art pixels per beam segment
    POKEMON_ANIM_FPS = 20     # EBDX sprite strips
    # Sprites up to this height are native-resolution art and are shown at 2x
    # (EBDX battlers/trainers); taller ones are already doubled.
    NATIVE_SPRITE_MAX_HEIGHT = 128
    TEXT_COLOR     = [248, 248, 248]
    TEXT_SHADOW    = [24, 24, 32]

    # Effect palettes: [core, inner, outer, edge] (4 colours per effect).
    PALETTES = {
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
      :me_hl_result    => ["Festival highlight result", "Slots win"]
    }
    HIGHLIGHT_BGM_VOLUME = 70
    HIGHLIGHT_MIN_SECONDS = 15.0
    HIGHLIGHT_MAX_SECONDS = 30.0
  end
end
