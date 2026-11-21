#===============================================================================
# Prismfall EBDX Bridge - configuration and per-field visual profiles
#-------------------------------------------------------------------------------
# What this plugin does
#   * Battle start: if battle.field_effect != :NONE, the EBDX battle room
#     (BattleSceneRoom) is rebuilt from the field's :backdrop graphic.
#   * :prismfall_field_changed: swaps the room live with a short transition
#     (EBDX's own BattleSceneRoom#reconfigure, the same call EBDX's sample
#     battle scripts use), including FLOWER_GARDEN-style stage changes.
#   * :prismfall_field_overlay_changed (BLEED / PRISM_ARENA borrowing): swaps
#     the ambient particle layer to the borrowed fields and flashes the room.
#   * Ambient FX (embers, snow, spores, rain, stars...) are injected into the
#     EBDX room's own sprite hash, so EBDX's camera/zoom/focus code moves them.
#   * Without EBDX (Battle::Scene is vanilla) it swaps the vanilla battlebacks
#     Graphics/Battlebacks/<backdrop>_bg / _base0 / _base1 / _message instead.
#
# Art lookup (EBDX), for a field whose definition has :backdrop => "field_x":
#   Graphics/EBDX/Battlebacks/battlebg/field_x.png        room image, 384x308
#   Graphics/EBDX/Battlebacks/battlebg/field_x_night.png  optional (outdoor fields)
#   Graphics/EBDX/Battlebacks/base/field_x.png            optional ground overlay, 384x182
#   Graphics/EBDX/Battlebacks/elements/field_x_fog.png    optional scrolling front layer
# If the room image is missing, the profile's :fallback (a stock EBDX
# environment) is used with :tone applied, so every field is playable before
# its art exists. See docs/ART_ASSETS.md.
#
# Colours are [r, g, b]; tones are [r, g, b, gray] (plain arrays so this file
# has no RGSS dependency).
#===============================================================================
module PrismfallEBDX
  VERSION = "1.0.0"

  # Master switch for everything in this plugin.
  ENABLED = true
  # Ambient particle FX on/off, and a density multiplier (0.5 = half the particles).
  AMBIENT_FX      = true
  FX_DENSITY      = 1.0
  MAX_PARTICLES   = 90     # hard cap per room (main + overlay layers)
  # Field art: use battlebg/<bd>_hd.png (864x693, drawn 1:1 at the default camera) when present.
  HD_ART          = true
  # Animated art layers (:layers in the profiles: pulsing glows, flickering lamps, swaying chains...).
  AMBIENT_LAYERS  = true
  # If a script set EliteBattle.set(:nextBattleBack, ...) for this battle, keep
  # that backdrop at battle start (live field changes still swap it).
  RESPECT_SCRIPTED_BACKDROP = true
  # Live swaps: fade the background through the transition colour (frames are
  # EBDX's: 8 in + 8 out). false = instant swap.
  LIVE_TRANSITIONS = true
  # Vanilla fallback fade time per half, in seconds.
  VANILLA_FADE_TIME = 0.2

  # Transition presets. A profile/override may also give [r, g, b] or an EBDX
  # common animation Symbol (e.g. :DISTORTION).
  TRANSITIONS = {
    :black      => [0, 0, 0],
    :white      => [255, 255, 255],
    :distortion => :DISTORTION
  }
  DEFAULT_TRANSITION = :black

  # Specific old -> new transitions (:ANY matches any field). Checked first.
  TRANSITION_OVERRIDES = {
    [:VOLCANIC, :ASHEN_WASTE]         => [200, 200, 200],   # steam
    [:FROZEN_LAKE, :WATER_SURFACE]    => :white,            # thaw glare
    [:WATER_SURFACE, :UNDERWATER]     => [0, 48, 110],      # dive
    [:UNDERWATER, :WATER_SURFACE]     => [150, 210, 255],   # surface
    [:CRYSTAL_CAVERN, :DARK_CRYSTAL]  => :black,
    [:FACTORY, :SCRAPYARD]            => [255, 150, 40],    # explosion flash
    [:SILKWOOD, :WILDFIRE]            => [255, 120, 30],    # the forest catches
    [:FLOWER_GARDEN, :WILDFIRE]       => [255, 120, 30],
    # Revision 10 field web (design/FIELD_BACKDROPS_NEEDED.md)
    [:DESERT, :FLOODED_DUNES]         => [150, 210, 255],   # the flood-sea pours in
    [:DESERT, :GLASS_DUNES]           => :glass_quench_sand, # white fire glasses the sand (staged, below)
    [:FLOODED_DUNES, :GLASS_DUNES]    => :glass_quench,      # the flood flash-boils and freezes into glass
    [:GLASS_DUNES, :FLOODED_DUNES]    => [150, 210, 255],
    [:GLASS_DUNES, :DESERT]           => [230, 220, 190],   # the glass shatters into glittering sand
    [:FLOODED_DUNES, :DESERT]         => [200, 255, 170],   # the tide drains, the wet sand blooms
    [:FLOODED_DUNES, :FROZEN_LAKE]    => :white,
    [:ASHEN_WASTE, :VOLCANIC]         => [255, 90, 20],
    [:ASHEN_WASTE, :WATER_SURFACE]    => [200, 220, 235],
    [:WILDFIRE, :MEADOW]              => [200, 255, 170],
    [:CORROSIVE_MIRE, :WATER_SURFACE] => [180, 230, 255],
    [:CORROSIVE_MIRE, :WASTELAND]     => [255, 140, 40],
    [:WATER_SURFACE, :FROZEN_LAKE]    => :white,
    [:WATER_SURFACE, :CORROSIVE_MIRE] => [120, 40, 140],
    [:UNDERWATER, :CORROSIVE_MIRE]    => [120, 40, 140],
    [:STORMFRONT, :RAINBOW]           => [255, 245, 200],
    [:RAINBOW, :ANY]                  => :white,
    [:MINDSCAPE, :INVERSE]            => :distortion,
    [:HOLLOW_CATHEDRAL, :INVERSE]     => :distortion,
    [:INVERSE, :ANY]                  => :distortion,
    [:SCRAPYARD, :FACTORY]            => [255, 240, 120],
    [:SCRAPYARD, :WASTELAND]          => [120, 40, 140],
    [:FAIRY_TALE, :DRAGONS_DEN]       => [255, 110, 40],
    [:DRAGONS_DEN, :CAVE]             => [200, 220, 235],
    [:DRAGONS_DEN, :FAIRY_TALE]       => [255, 210, 240],
    [:CAVE, :CRYSTAL_CAVERN]          => [200, 240, 255],
    [:CAVE, :VOLCANIC]                => [255, 90, 20],
    [:MOUNTAIN, :VOLCANIC]            => [255, 90, 20],
    [:SNOWY_MOUNTAIN, :VOLCANIC]      => [255, 90, 20],
    [:CAVE, :DRAGONS_DEN]             => [255, 110, 40],
    [:COLOSSEUM, :CAVE]               => [150, 120, 90],
    [:CRYSTAL_CAVERN, :CAVE]          => [150, 120, 90],
    [:DARK_CRYSTAL, :CAVE]            => [150, 120, 90],
    [:DARK_CRYSTAL, :CRYSTAL_CAVERN]  => :white,
    [:MOUNTAIN, :SNOWY_MOUNTAIN]      => :white,
    [:SNOWY_MOUNTAIN, :MOUNTAIN]      => :white,
    [:BEACH, :WATER_SURFACE]          => [150, 210, 255],
    [:WASTELAND, :MEADOW]             => [200, 255, 170],
    [:WASTELAND, :FLOWER_GARDEN]      => [200, 255, 170],
    [:MEADOW, :WILDFIRE]              => [255, 120, 30],
    [:MEADOW, :FLOWER_GARDEN]         => [255, 230, 240],
    [:ANY, :BLEED]                    => :distortion,
    [:BLEED, :ANY]                    => :white
  }

  # Staged transitions: played IN the room (008_Bridge_Transitions.rb) instead of EBDX's flat colour fade.
  # The new room is revealed band by band from where the move hit (the base opposite the last move's user;
  # the foe's base when no move caused the change), under a white-hot front that cools, with steam where the
  # front crosses water and a crackle of light through the new glass; the battlers stay on top throughout.
  #   :art       band set in STAGED_ART (009_Bridge_Transition_Art.rb, generated by art/battlebacks/transitions.py);
  #              used only when the new room is the art the bands were cut from, else :fallback
  #   :fallback  colour fade for the vanilla scene, missing art or a night room
  #   :steam     steam puffs per band point (0 = none)
  #   :preheat   colour of the shimmer running just ahead of the front
  STAGED_TRANSITIONS = {
    :glass_quench      => { :art => :glass_quench, :fallback => [235, 255, 240], :steam => 1.3,
                            :preheat => [255, 250, 230] },
    :glass_quench_sand => { :art => :glass_quench, :fallback => [235, 255, 240], :steam => 0.3,
                            :preheat => [255, 180, 100] }
  }

  # Room-space z layers for particles (EBDX battler z: foe ~11, player ~21).
  LAYER_Z = { :back => [1, 9], :mid => [12, 19], :front => [24, 34] }

  #-----------------------------------------------------------------------------
  # Particle spec keys (Hash per emitter):
  #   :type    :rise / :fall / :drift / :twinkle / :streak, or :flash (room flash timer)
  #   :count   particles (scaled by FX_DENSITY)
  #   :shape   :dot / :glow / :spark / :rect / :puff (generated, white, tinted by :colors;
  #            :puff = soft round cloud for steam/smoke)
  #   :size    shape size in px; :w/:h for :rect
  #   :bitmap  alternative to :shape: file in Graphics/EBDX/Battlebacks/elements/
  #   :colors  [[r,g,b], ...] random tint per particle
  #   :speed   [min, max] room px per 40fps-frame (EBDX convention)
  #   :sway    sideways wobble amplitude (px)
  #   :zoom    [min, max] size multiplier (room zoom is applied on top)
  #   :opacity [min, max] peak opacity
  #   :layers  any of :back / :mid / :front
  #   :area    [x1, y1, x2, y2] in room-image pixels (default: whole 384x308 room)
  #   :blend   0 normal, 1 additive (glows), 2 subtractive
  #   :angle   :streak motion direction in degrees (0 = right, 90 = down)
  #   :spin    max degrees per frame (petals, confetti)
  #   :dir     :drift direction 1 (right) / -1 (left); random if omitted
  #   :grow    :rise/:fall only: size grows by this factor over the path (puffs swell)
  #-----------------------------------------------------------------------------
  # Art layers (:layers, written by art/battlebacks/build_backdrops.py into
  # 006_Bridge_Art.rb). One sprite each, in room coordinates like EBDX elements:
  #   :bitmap  file in elements/      :x, :y  room-image anchor   :ox, :oy  pivot in bitmap px
  #   :hd      true = painted at ROOM_SCALE resolution (drawn 1:1 at the default camera)
  #   :zoom    extra size factor      :z  room z (foe ~11, player ~21)   :blend  0/1/2
  #   :opacity base opacity           :angle  base angle   :mirror  true/false
  #   :frames, :frame_time            horizontal sprite-sheet animation
  #   :anim    :pulse / :flicker / :sway / :rotate / :bob / :drift, or an Array of them
  #   :period  frames per cycle (40 fps frames); :phase radians
  #   :min/:max opacity range (:pulse, :flicker)  :amp sway degrees / bob / drift px
  #   :speed   :rotate degrees per frame          :chance/:dropout  :flicker odds / length
  #   flash:   :color, :alpha, :interval [min, max] frames, :decay, :double
  #-----------------------------------------------------------------------------
  EMBER  = [[255, 150, 50], [255, 100, 30], [255, 210, 90]]
  ASH    = [[110, 110, 110], [150, 140, 130], [80, 80, 85]]
  SNOW   = [[255, 255, 255], [225, 240, 255]]
  SPORE  = [[200, 255, 160], [240, 255, 200], [170, 230, 120]]
  TOXIC  = [[190, 90, 230], [140, 220, 90], [220, 120, 255]]
  GOLD   = [[255, 230, 120], [255, 250, 200]]
  PRISM  = [[255, 90, 90], [255, 200, 80], [120, 255, 120], [90, 200, 255], [190, 120, 255]]
  PSY    = [[255, 120, 220], [190, 130, 255], [255, 200, 255]]
  WISP   = [[150, 220, 255], [200, 160, 255], [230, 255, 255]]
  NEON   = [[80, 240, 255], [255, 80, 220], [255, 255, 120]]
  DUST   = [[230, 220, 190], [255, 245, 220]]
  STEAM  = [[220, 220, 220], [190, 195, 200]]
  GLITCH = [[255, 40, 70], [40, 255, 230], [255, 255, 255]]

  #-----------------------------------------------------------------------------
  # Per-field profiles. Keys:
  #   :fallback    EBDX environment (EnvironmentEBDX constant Symbol, or a Hash)
  #                used when the field's own room image is missing
  #   :tone        tone applied to the fallback room
  #   :art_tone    tone applied even when the field's own art exists (rarely needed)
  #   :art_extras  EBDX room keys merged over the field's own art ("water", "lightsC"...).
  #                An "imgNNN" entry may add :parallax => [px, py] (far layers such
  #                as sky clouds follow the camera by that fraction); with the
  #                *_night room, an element with its own <bitmap>_night uses it.
  #   :fallback_extras  EBDX room keys merged over the fallback room
  #   :outdoor     true = EBDX day/night tint + *_night art variant apply
  #   :transition  transition INTO this field (see TRANSITIONS)
  #   :flash       [r, g, b] colour of the overlay-change flash (borrowing fields)
  #   :fx          particle emitters (see above)
  #   :stages      { n => { profile overrides } } (shallow merge, like FIELD_API §7)
  #-----------------------------------------------------------------------------
  PROFILES = {
    #--- Gym fields -------------------------------------------------------------
    :SILKWOOD => {
      :fallback => :FOREST, :tone => [-10, 5, -25, 40], :transition => :black,
      :art_extras => { "lightsC" => true },
      :fx => [
        { :type => :drift, :count => 10, :shape => :rect, :w => 6, :h => 1, :colors => [[255, 255, 245]],
          :speed => [0.3, 0.7], :sway => 8, :zoom => [0.6, 1.0], :opacity => [90, 160], :layers => [:back, :mid, :front] },
        { :type => :rise, :count => 12, :shape => :dot, :size => 3, :colors => SPORE,
          :speed => [0.3, 0.7], :sway => 10, :zoom => [0.4, 0.8], :opacity => [120, 200], :layers => [:back, :mid] }
      ]
    },
    :GRAND_STAGE => {
      :fallback => :STAGE, :tone => [10, 0, -10, 0], :transition => :white,
      :art_extras => { "lightsA" => true, "spinLights" => true },
      :fx => [
        { :type => :fall, :count => 24, :shape => :rect, :w => 3, :h => 2, :colors => PRISM,
          :speed => [0.6, 1.2], :sway => 12, :zoom => [0.6, 1.0], :opacity => [200, 255], :spin => 8,
          :layers => [:back, :mid, :front] }
      ]
    },
    :WATER_SURFACE => {
      :fallback => :WATER, :outdoor => true, :transition => [150, 210, 255],
      :art_extras => { "water" => true },
      :fx => [
        { :type => :twinkle, :count => 14, :shape => :spark, :size => 5, :colors => [[255, 255, 255]],
          :area => [0, 160, 384, 300], :speed => [2, 5], :zoom => [0.5, 0.9], :opacity => [160, 255],
          :layers => [:back, :mid], :blend => 1 }
      ]
    },
    :NEON_GRID => {
      :fallback => :NET, :tone => [-30, -10, 40, 0], :transition => [80, 240, 255],
      :art_extras => { "spinLights" => true },
      :fx => [
        { :type => :rise, :count => 16, :shape => :rect, :w => 2, :h => 2, :colors => NEON,
          :speed => [0.8, 1.8], :sway => 2, :zoom => [0.6, 1.0], :opacity => [200, 255], :layers => [:back, :mid, :front], :blend => 1 },
        { :type => :twinkle, :count => 10, :shape => :spark, :size => 5, :colors => NEON,
          :speed => [4, 8], :zoom => [0.5, 0.9], :opacity => [180, 255], :layers => [:back], :blend => 1 },
        { :type => :flash, :color => [120, 230, 255], :alpha => 70, :interval => [160, 320], :decay => 10 }
      ]
    },
    :DESERT => {
      :fallback => { "backdrop" => "Sand", "sky" => true }, :outdoor => true, :tone => [25, 10, -25, 0],
      :transition => [255, 220, 150],
      :fx => [
        { :type => :drift, :count => 26, :shape => :dot, :size => 2, :colors => DUST, :dir => 1,
          :speed => [1.5, 3.0], :sway => 4, :zoom => [0.5, 0.9], :opacity => [120, 200], :layers => [:back, :mid, :front] }
      ]
    },
    :CORROSIVE_MIRE => {
      :fallback => :FOREST, :tone => [-25, -20, 15, 60], :transition => [120, 60, 150],
      :fallback_extras => { "bubbles" => "bubbleDark" },
      :fx => [
        { :type => :rise, :count => 18, :shape => :glow, :size => 5, :colors => TOXIC,
          :area => [0, 120, 384, 308], :speed => [0.3, 0.8], :sway => 6, :zoom => [0.4, 0.9], :opacity => [140, 220],
          :layers => [:back, :mid, :front], :blend => 1 }
      ]
    },
    :VOLCANIC => {
      :fallback => :MAGMA, :tone => [40, -10, -40, 0], :transition => [255, 96, 0],
      :fx => [
        { :type => :rise, :count => 24, :shape => :glow, :size => 5, :colors => EMBER,
          :speed => [0.8, 2.0], :sway => 10, :zoom => [0.3, 0.7], :opacity => [180, 255],
          :layers => [:back, :mid, :front], :blend => 1 },
        { :type => :fall, :count => 10, :shape => :dot, :size => 3, :colors => ASH,
          :speed => [0.3, 0.8], :sway => 14, :zoom => [0.4, 0.7], :opacity => [110, 180], :layers => [:back, :mid] }
      ]
    },
    :COLOSSEUM => {
      :fallback => :NET, :tone => [20, 5, -20, 0], :transition => :black,
      :fx => [
        { :type => :drift, :count => 14, :shape => :dot, :size => 2, :colors => DUST,
          :speed => [0.2, 0.5], :sway => 6, :zoom => [0.5, 0.9], :opacity => [80, 150], :layers => [:back, :mid, :front] }
      ]
    },
    :FLOWER_GARDEN => {
      :fallback => :OUTDOOR, :outdoor => true, :tone => [5, 10, 0, 0], :transition => [255, 230, 240],
      :fallback_extras => { "tallGrass" => { :elements => 7, :x => [124, 274, 204, 62, 248, 275, 182],
        :y => [160, 140, 140, 185, 246, 174, 170], :z => [2, 1, 2, 17, 27, 17, 17],
        :zoom => [0.7, 0.35, 0.5, 1, 1.5, 0.7, 1], :mirror => [false, true, false, true, false, true, false] } },
      :fx => [
        { :type => :fall, :count => 6, :shape => :dot, :size => 3, :colors => [[255, 190, 220], [255, 255, 255]],
          :speed => [0.4, 0.8], :sway => 16, :zoom => [0.6, 1.0], :opacity => [200, 255], :spin => 6, :layers => [:back, :mid, :front] }
      ],
      :stages => {
        2 => { :fx => [
          { :type => :fall, :count => 12, :shape => :dot, :size => 3, :colors => [[255, 190, 220], [255, 255, 255], [255, 240, 140]],
            :speed => [0.4, 0.8], :sway => 16, :zoom => [0.6, 1.0], :opacity => [200, 255], :spin => 6, :layers => [:back, :mid, :front] }
        ] },
        3 => { :fx => [
          { :type => :fall, :count => 18, :shape => :dot, :size => 3, :colors => [[255, 170, 210], [255, 255, 255], [255, 240, 140]],
            :speed => [0.4, 0.9], :sway => 16, :zoom => [0.6, 1.1], :opacity => [200, 255], :spin => 6, :layers => [:back, :mid, :front] },
          { :type => :rise, :count => 8, :shape => :dot, :size => 2, :colors => GOLD,
            :speed => [0.2, 0.5], :sway => 8, :zoom => [0.5, 0.8], :opacity => [120, 200], :layers => [:back, :mid], :blend => 1 }
        ] },
        4 => { :fx => [
          { :type => :fall, :count => 26, :shape => :dot, :size => 3, :colors => [[255, 150, 200], [255, 255, 255], [255, 230, 120], [200, 160, 255]],
            :speed => [0.4, 1.0], :sway => 18, :zoom => [0.6, 1.2], :opacity => [210, 255], :spin => 8, :layers => [:back, :mid, :front] },
          { :type => :rise, :count => 12, :shape => :dot, :size => 2, :colors => GOLD,
            :speed => [0.2, 0.5], :sway => 8, :zoom => [0.5, 0.9], :opacity => [140, 220], :layers => [:back, :mid, :front], :blend => 1 }
        ] },
        5 => { :fx => [
          { :type => :fall, :count => 34, :shape => :dot, :size => 3, :colors => [[255, 120, 190], [255, 255, 255], [255, 220, 100], [190, 140, 255]],
            :speed => [0.5, 1.1], :sway => 20, :zoom => [0.7, 1.3], :opacity => [220, 255], :spin => 10, :layers => [:back, :mid, :front] },
          { :type => :rise, :count => 18, :shape => :glow, :size => 4, :colors => GOLD,
            :speed => [0.2, 0.6], :sway => 10, :zoom => [0.4, 0.8], :opacity => [160, 240], :layers => [:back, :mid, :front], :blend => 1 }
        ] }
      }
    },
    :FROZEN_LAKE => {
      :fallback => :SNOW, :outdoor => true, :tone => [-10, 0, 25, 0], :transition => :white,
      :fx => [
        { :type => :fall, :count => 30, :bitmap => "snow", :speed => [0.6, 1.4], :sway => 12,
          :zoom => [0.2, 0.45], :opacity => [200, 255], :layers => [:back, :mid, :front] },
        { :type => :twinkle, :count => 10, :shape => :spark, :size => 5, :colors => [[220, 245, 255]],
          :area => [0, 170, 384, 300], :speed => [3, 6], :zoom => [0.5, 0.9], :opacity => [160, 255], :layers => [:back, :mid], :blend => 1 }
      ]
    },
    :STORMFRONT => {
      :fallback => :SKY, :outdoor => true, :tone => [-40, -35, -20, 80], :transition => [200, 210, 230],
      :fx => [
        { :type => :streak, :count => 34, :shape => :rect, :w => 14, :h => 1, :colors => [[210, 220, 240]],
          :angle => 105, :speed => [7, 11], :zoom => [0.6, 1.0], :opacity => [120, 200], :layers => [:back, :mid, :front] },
        { :type => :streak, :count => 8, :shape => :rect, :w => 26, :h => 1, :colors => [[255, 255, 255]],
          :angle => 175, :speed => [5, 8], :zoom => [0.6, 1.0], :opacity => [60, 120], :layers => [:back, :front] },
        { :type => :flash, :color => [255, 255, 255], :alpha => 170, :interval => [140, 300], :decay => 14, :double => true }
      ]
    },
    :MINDSCAPE => {
      :fallback => :DIMENSION, :tone => [30, -10, 40, 0], :transition => :white,
      :art_extras => { "vacuum" => "dark006" },
      :fx => [
        { :type => :twinkle, :count => 16, :shape => :glow, :size => 5, :colors => PSY,
          :speed => [2, 4], :zoom => [0.4, 0.9], :opacity => [140, 230], :layers => [:back, :mid, :front], :blend => 1 },
        { :type => :rise, :count => 10, :shape => :spark, :size => 5, :colors => PSY,
          :speed => [0.3, 0.6], :sway => 14, :zoom => [0.5, 0.9], :opacity => [150, 230], :layers => [:back, :mid], :blend => 1 }
      ]
    },
    :CRYSTAL_CAVERN => {
      :fallback => :CAVE, :tone => [-5, 15, 35, 0], :transition => [180, 255, 255],
      :fx => [
        { :type => :twinkle, :count => 18, :shape => :spark, :size => 7, :colors => [[200, 255, 255], [255, 255, 255], [180, 210, 255]],
          :speed => [3, 7], :zoom => [0.5, 1.0], :opacity => [170, 255], :layers => [:back, :mid], :blend => 1 },
        { :type => :drift, :count => 8, :shape => :dot, :size => 2, :colors => [[200, 255, 255]],
          :speed => [0.2, 0.4], :sway => 6, :zoom => [0.5, 0.8], :opacity => [80, 140], :layers => [:mid, :front] }
      ]
    },
    :HOLLOW_CATHEDRAL => {
      :fallback => :CHAMPION, :tone => [-70, -70, -25, 60], :transition => [60, 40, 90],
      :art_extras => { "lightsC" => true },
      :fx => [
        { :type => :rise, :count => 10, :shape => :glow, :size => 7, :colors => WISP,
          :speed => [0.2, 0.5], :sway => 18, :zoom => [0.5, 0.9], :opacity => [120, 210], :layers => [:back, :mid, :front], :blend => 1 },
        { :type => :drift, :count => 12, :shape => :dot, :size => 2, :colors => DUST,
          :speed => [0.1, 0.3], :sway => 4, :zoom => [0.5, 0.8], :opacity => [60, 120], :layers => [:back, :mid] }
      ]
    },
    :FACTORY => {
      :fallback => :INDOOR, :tone => [-15, -10, 0, 50], :transition => [255, 190, 90],
      :fx => [
        { :type => :rise, :count => 8, :shape => :glow, :size => 9, :colors => STEAM,
          :area => [0, 60, 384, 308], :speed => [0.3, 0.6], :sway => 10, :zoom => [1.0, 1.8], :opacity => [50, 100], :layers => [:back, :front] },
        { :type => :fall, :count => 12, :shape => :dot, :size => 2, :colors => EMBER,
          :area => [40, 0, 344, 240], :speed => [2.0, 3.5], :sway => 3, :zoom => [0.5, 0.8], :opacity => [200, 255],
          :layers => [:back, :mid], :blend => 1 }
      ]
    },
    :NEW_MOON => {
      :fallback => :DARKNESS, :tone => [-40, -40, -10, 40], :transition => :black,
      :fx => [
        { :type => :twinkle, :count => 26, :bitmap => "star", :area => [0, 0, 384, 140],
          :speed => [1, 3], :zoom => [0.6, 1.2], :opacity => [140, 255], :layers => [:back] },
        { :type => :rise, :count => 8, :shape => :glow, :size => 5, :colors => [[150, 110, 220], [90, 70, 160]],
          :speed => [0.2, 0.4], :sway => 10, :zoom => [0.5, 0.9], :opacity => [90, 160], :layers => [:back, :mid, :front], :blend => 1 }
      ]
    },
    :FAIRY_TALE => {
      :fallback => :FOREST, :tone => [30, 5, 30, 0], :transition => [255, 200, 240],
      :fx => [
        { :type => :rise, :count => 16, :shape => :spark, :size => 5, :colors => [[255, 180, 230], [255, 240, 160], [255, 255, 255]],
          :speed => [0.3, 0.7], :sway => 12, :zoom => [0.5, 1.0], :opacity => [170, 255], :layers => [:back, :mid, :front], :blend => 1 },
        { :type => :twinkle, :count => 10, :shape => :glow, :size => 4, :colors => GOLD,
          :speed => [2, 5], :zoom => [0.4, 0.8], :opacity => [140, 230], :layers => [:back, :mid], :blend => 1 }
      ]
    },
    :DRAGONS_DEN => {
      :fallback => :MAGMA, :tone => [25, -20, 20, 0], :transition => [180, 60, 255],
      :fx => [
        { :type => :rise, :count => 20, :shape => :glow, :size => 5, :colors => [[255, 140, 50], [200, 90, 255], [255, 210, 90]],
          :speed => [0.6, 1.6], :sway => 10, :zoom => [0.3, 0.7], :opacity => [170, 255], :layers => [:back, :mid, :front], :blend => 1 },
        { :type => :twinkle, :count => 10, :shape => :spark, :size => 5, :colors => GOLD,
          :area => [0, 200, 384, 308], :speed => [3, 6], :zoom => [0.5, 0.9], :opacity => [160, 255], :layers => [:back, :mid], :blend => 1 }
      ]
    },
    #--- Story / route fields ---------------------------------------------------
    :CAVE => {
      :fallback => :CAVE, :transition => :black,
      :fx => [
        { :type => :drift, :count => 8, :shape => :dot, :size => 2, :colors => DUST,
          :speed => [0.1, 0.3], :sway => 5, :zoom => [0.5, 0.8], :opacity => [60, 120], :layers => [:back, :mid] }
      ]
    },
    :MOUNTAIN => {
      :fallback => :MOUNTAIN, :outdoor => true, :transition => :black,
      :fx => [
        { :type => :streak, :count => 6, :shape => :rect, :w => 22, :h => 1, :colors => [[255, 255, 255]],
          :angle => 178, :speed => [4, 7], :zoom => [0.6, 1.0], :opacity => [50, 100], :layers => [:back, :front] }
      ]
    },
    :SNOWY_MOUNTAIN => {
      :fallback => :SNOW, :outdoor => true, :tone => [-5, 0, 15, 0], :transition => :white,
      :fx => [
        { :type => :fall, :count => 44, :bitmap => "snow", :speed => [0.8, 1.8], :sway => 16,
          :zoom => [0.2, 0.5], :opacity => [200, 255], :layers => [:back, :mid, :front] }
      ]
    },
    :BEACH => {
      :fallback => { "backdrop" => "Sand", "sky" => true, "water" => true }, :outdoor => true, :transition => :white,
      :fx => [
        { :type => :twinkle, :count => 10, :shape => :spark, :size => 5, :colors => [[255, 255, 255]],
          :area => [0, 150, 384, 230], :speed => [2, 5], :zoom => [0.5, 0.8], :opacity => [150, 255], :layers => [:back], :blend => 1 }
      ]
    },
    :UNDERWATER => {
      :fallback => :UNDERWATER, :transition => [0, 48, 110],
      :art_extras => { "bubbles" => true, "lightsC" => true },
      :fx => [
        { :type => :drift, :count => 14, :shape => :dot, :size => 2, :colors => [[200, 240, 255], [160, 220, 200]],
          :speed => [0.1, 0.3], :sway => 8, :zoom => [0.5, 0.9], :opacity => [80, 150], :layers => [:back, :mid, :front] }
      ]
    },
    :RAINBOW => {
      :fallback => :SKY, :outdoor => true, :tone => [15, 10, 25, 0], :transition => :white,
      :fx => [
        { :type => :twinkle, :count => 18, :shape => :spark, :size => 5, :colors => PRISM,
          :speed => [2, 5], :zoom => [0.5, 1.0], :opacity => [170, 255], :layers => [:back, :mid, :front], :blend => 1 },
        { :type => :fall, :count => 12, :shape => :rect, :w => 2, :h => 2, :colors => PRISM,
          :speed => [0.3, 0.7], :sway => 12, :zoom => [0.5, 0.9], :opacity => [180, 255], :spin => 6, :layers => [:back, :mid] }
      ]
    },
    :WASTELAND => {
      :fallback => { "backdrop" => "Sand", "sky" => true }, :outdoor => true, :tone => [-15, -25, -35, 90],
      :transition => [140, 120, 60],
      :fx => [
        { :type => :rise, :count => 14, :shape => :glow, :size => 5, :colors => TOXIC,
          :area => [0, 150, 384, 308], :speed => [0.3, 0.7], :sway => 6, :zoom => [0.4, 0.8], :opacity => [120, 200], :layers => [:back, :mid, :front] },
        { :type => :drift, :count => 10, :shape => :dot, :size => 2, :colors => ASH,
          :speed => [0.6, 1.2], :sway => 4, :zoom => [0.5, 0.8], :opacity => [90, 150], :layers => [:back, :mid] }
      ]
    },
    :ASHEN_WASTE => {
      :fallback => :CAVE, :tone => [-20, -25, -25, 140], :transition => [200, 200, 200],
      :fx => [
        { :type => :fall, :count => 34, :shape => :dot, :size => 3, :colors => ASH,
          :speed => [0.3, 0.8], :sway => 16, :zoom => [0.4, 0.8], :opacity => [140, 220], :layers => [:back, :mid, :front] },
        { :type => :rise, :count => 6, :shape => :glow, :size => 9, :colors => STEAM,
          :speed => [0.2, 0.4], :sway => 10, :zoom => [1.0, 1.8], :opacity => [40, 80], :layers => [:back, :front] }
      ]
    },
    :DARK_CRYSTAL => {
      :fallback => :DARKCAVE, :tone => [-30, -40, 10, 0], :transition => :black,
      :art_extras => { "vacuum" => "dark006" },
      :fx => [
        { :type => :twinkle, :count => 16, :shape => :spark, :size => 7, :colors => [[170, 90, 255], [110, 60, 200], [230, 200, 255]],
          :speed => [2, 5], :zoom => [0.5, 1.0], :opacity => [150, 240], :layers => [:back, :mid], :blend => 1 }
      ]
    },
    :SCRAPYARD => {
      :fallback => :INDOOR, :tone => [-10, -20, -35, 90], :transition => [255, 150, 40],
      :fx => [
        { :type => :rise, :count => 8, :shape => :glow, :size => 9, :colors => [[120, 115, 110], [90, 90, 95]],
          :speed => [0.2, 0.5], :sway => 12, :zoom => [1.0, 1.8], :opacity => [50, 100], :layers => [:back, :front] },
        { :type => :fall, :count => 6, :shape => :dot, :size => 2, :colors => EMBER,
          :area => [60, 0, 324, 220], :speed => [2.0, 3.5], :sway => 3, :zoom => [0.5, 0.8], :opacity => [200, 255],
          :layers => [:back, :mid], :blend => 1 }
      ]
    },
    # Ch19 war fields: the DESERT room flooded, then glassed (art: art/battlebacks/fields_g.py)
    :FLOODED_DUNES => {
      :fallback => { "backdrop" => "Sand", "sky" => true }, :outdoor => true, :tone => [-20, 0, 25, 20],
      :fallback_extras => { "water" => true }, :transition => [150, 210, 255],
      :fx => [
        { :type => :drift, :count => 14, :shape => :dot, :size => 2, :colors => [[255, 255, 255], [210, 235, 250]],
          :dir => 1, :speed => [1.0, 2.0], :sway => 10, :zoom => [0.5, 0.9], :opacity => [150, 230], :layers => [:back, :mid, :front] },
        { :type => :twinkle, :count => 14, :shape => :spark, :size => 5, :colors => [[255, 255, 255]],
          :area => [0, 150, 384, 300], :speed => [2, 5], :zoom => [0.5, 0.9], :opacity => [160, 255], :layers => [:back, :mid], :blend => 1 }
      ]
    },
    :GLASS_DUNES => {
      :fallback => { "backdrop" => "Sand", "sky" => true }, :outdoor => true, :tone => [-35, 0, -20, 40],
      :transition => [235, 255, 240],
      :fx => [
        { :type => :rise, :count => 8, :shape => :puff, :size => 18, :colors => STEAM, :speed => [0.25, 0.5],
          :sway => 6, :zoom => [0.5, 0.8], :grow => 1.6, :opacity => [50, 95], :layers => [:back, :mid] },
        { :type => :twinkle, :count => 18, :shape => :spark, :size => 7, :colors => [[255, 255, 255], [200, 255, 220]],
          :speed => [4, 8], :zoom => [0.4, 0.9], :opacity => [170, 255], :layers => [:back, :mid], :blend => 1 }
      ]
    },
    :MEADOW => {
      :fallback => :OUTDOOR, :outdoor => true, :tone => [5, 10, -5, 0], :transition => [220, 255, 200],
      :fallback_extras => { "tallGrass" => { :elements => 7, :x => [124, 274, 204, 62, 248, 275, 182],
        :y => [160, 140, 140, 185, 246, 174, 170], :z => [2, 1, 2, 17, 27, 17, 17],
        :zoom => [0.7, 0.35, 0.5, 1, 1.5, 0.7, 1], :mirror => [false, true, false, true, false, true, false] } },
      :fx => [
        { :type => :drift, :count => 14, :shape => :dot, :size => 2, :colors => [[255, 255, 240], [250, 240, 200]],
          :dir => 1, :speed => [0.8, 1.6], :sway => 12, :zoom => [0.5, 0.9], :opacity => [160, 230], :layers => [:back, :mid, :front] }
      ]
    },
    :WILDFIRE => {
      :fallback => :FOREST, :tone => [60, -10, -50, 20], :transition => [255, 120, 30],
      :fx => [
        { :type => :rise, :count => 30, :shape => :glow, :size => 5, :colors => EMBER,
          :speed => [1.0, 2.4], :sway => 12, :zoom => [0.3, 0.7], :opacity => [180, 255],
          :layers => [:back, :mid, :front], :blend => 1 }
      ],
      :stages => { 2 => { :tone => [-20, -25, -25, 120], :fx => [
        { :type => :fall, :count => 30, :shape => :dot, :size => 3, :colors => ASH,
          :speed => [0.3, 0.7], :sway => 16, :zoom => [0.4, 0.8], :opacity => [130, 210], :layers => [:back, :mid, :front] }
      ] } }
    },
    :INVERSE => {
      :fallback => :DIMENSION, :tone => [0, 0, 0, 255], :transition => :white,
      :fx => [
        # "Snow" that falls upward: the world's rules are reversed here.
        { :type => :rise, :count => 14, :shape => :rect, :w => 2, :h => 2, :colors => [[255, 255, 255], [20, 20, 20]],
          :speed => [0.3, 0.6], :sway => 8, :zoom => [0.5, 0.9], :opacity => [150, 230], :layers => [:back, :mid, :front] }
      ]
    },
    :BLEED => {
      :fallback => :DARKNESS, :tone => [35, -45, -25, 30], :transition => :distortion, :flash => [255, 40, 70],
      :fx => [
        { :type => :rise, :count => 18, :shape => :rect, :w => 3, :h => 2, :colors => GLITCH,
          :speed => [0.4, 1.4], :sway => 2, :zoom => [0.6, 1.2], :opacity => [160, 255], :layers => [:back, :mid, :front], :blend => 1 },
        { :type => :streak, :count => 6, :shape => :rect, :w => 40, :h => 1, :colors => GLITCH,
          :angle => 0, :speed => [9, 14], :zoom => [0.8, 1.2], :opacity => [90, 160], :layers => [:back, :front], :blend => 1 },
        { :type => :flash, :color => [255, 40, 70], :alpha => 90, :interval => [90, 220], :decay => 18 }
      ]
    },
    :PRISM_ARENA => {
      :fallback => :CHAMPION, :tone => [10, 10, 25, 0], :transition => :white, :flash => [255, 255, 255],
      :fx => [
        { :type => :twinkle, :count => 18, :shape => :spark, :size => 7, :colors => PRISM,
          :speed => [2, 5], :zoom => [0.5, 1.0], :opacity => [170, 255], :layers => [:back, :mid], :blend => 1 },
        { :type => :rise, :count => 12, :shape => :glow, :size => 4, :colors => PRISM,
          :speed => [0.3, 0.7], :sway => 10, :zoom => [0.4, 0.8], :opacity => [150, 230], :layers => [:back, :mid, :front], :blend => 1 }
      ]
    }
  }

  # Profile used for field IDs that have no entry above (custom fields).
  DEFAULT_PROFILE = { :fallback => nil, :transition => :black, :fx => [] }

  # When a :borrow field (BLEED, PRISM_ARENA) borrows other fields, each
  # borrowed field's particle emitters are added at this fraction of their count.
  OVERLAY_FX_SCALE = 0.5
  OVERLAY_MAX_FIELDS = 2
end
