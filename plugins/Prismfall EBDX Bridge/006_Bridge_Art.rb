#===============================================================================
# Prismfall EBDX Bridge - GENERATED field art profiles. Do not edit by hand:
# rebuild with `python3 -I art/battlebacks/build_backdrops.py [FIELD ...]`.
# Each entry is merged over the hand-written profile in 001_Bridge_Config.rb:
#   :art_extras  EBDX room keys for the field's own art (scrolling HD strips,
#                EBDX stock elements, lights, bubbles...)
#   :layers      Bridge-animated HD layers (pulse / flicker / sway / rotate / bob)
#   :fx          particle emitters tuned to the art (replace the hand-written ones)
#   :stages      per-stage overrides (FLOWER_GARDEN)
#===============================================================================
module PrismfallEBDX
  ART_PROFILES = {
    # >>> ASHEN_WASTE
    :ASHEN_WASTE => {
      :art_extras => {
        "img001" => { :bitmap => "decor006", :scrolling => true, :speed => 2, :direction => -1, :oy => 0, :z => 3, :flat => true, :opacity => 110 },
        "img003" => {
          :bitmap => "pf_ashen_waste_steam",
          :scrolling => true,
          :speed => 0.5,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 88.89,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 4
        }
      },
      :layers => [
        {
          :bitmap => "pf_ashen_waste_embers",
          :hd => true,
          :x => 56.89,
          :y => 19.56,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :opacity => 150,
          :anim => :pulse,
          :min => 40,
          :max => 170,
          :period => 150
        },
        {
          :bitmap => "pf_ashen_waste_banner0",
          :hd => true,
          :x => 171.56,
          :y => 48.0,
          :ox => 19,
          :oy => 3,
          :z => 2,
          :anim => :sway,
          :amp => 1.4,
          :period => 170
        },
        {
          :bitmap => "pf_ashen_waste_banner1",
          :hd => true,
          :x => 284.44,
          :y => 48.0,
          :ox => 19,
          :oy => 3,
          :z => 2,
          :anim => :sway,
          :amp => 1.4,
          :period => 199
        }
      ],
      :fx => [
        {
          :type => :fall,
          :count => 30,
          :shape => :dot,
          :size => 3,
          :colors => [
            [110, 110, 110],
            [150, 140, 130],
            [80, 80, 85]
          ],
          :speed => [0.3, 0.8],
          :sway => 16,
          :zoom => [0.4, 0.8],
          :opacity => [140, 220],
          :layers => [:back, :mid, :front]
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 18,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [141.7, 53.3, 151.7, 133.3],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [50, 95],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 18,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [263.4, 51.6, 273.4, 131.6],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [50, 95],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 18,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [106.1, 122.2, 116.1, 202.2],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [50, 95],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 18,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [306.1, 151.1, 316.1, 231.1],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [50, 95],
          :layers => [:back],
          :blend => 0
        }
      ]
    },
    # <<< ASHEN_WASTE
    # >>> CAVE
    :CAVE => {
      :art_extras => {
        "img001" => { :bitmap => "decor006", :scrolling => true, :speed => 2, :direction => -1, :oy => 0, :z => 3, :flat => true, :opacity => 120 },
        "img002" => { :bitmap => "decor009", :scrolling => true, :speed => 1, :direction => 1, :oy => 0, :z => 3, :flat => true, :opacity => 80 },
        "img003" => { :bitmap => "fog", :scrolling => true, :speed => 0.5, :direction => 1, :oy => 0, :z => 4, :flat => true, :opacity => 160 }
      },
      :layers => [
        { :bitmap => "pf_cave_lantern0", :hd => true, :x => 160.0, :y => 69.33, :ox => 11, :oy => 2, :z => 3, :anim => :sway, :amp => 3, :period => 160 },
        {
          :bitmap => "pf_cave_lanternglow0",
          :hd => true,
          :x => 135.56,
          :y => 60.0,
          :ox => 0,
          :oy => 0,
          :z => 3,
          :blend => 1,
          :anim => [:pulse, :flicker],
          :min => 90,
          :max => 150,
          :period => 50,
          :chance => 0.01,
          :dropout => 3
        },
        { :bitmap => "pf_cave_lantern1", :hd => true, :x => 62.22, :y => 11.56, :ox => 11, :oy => 2, :z => 30, :anim => :sway, :amp => 3, :period => 200 },
        {
          :bitmap => "pf_cave_lanternglow1",
          :hd => true,
          :x => 24.0,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 30,
          :blend => 1,
          :anim => [:pulse, :flicker],
          :min => 90,
          :max => 150,
          :period => 50,
          :chance => 0.01,
          :dropout => 3
        }
      ],
      :fx => [
        {
          :type => :drift,
          :count => 12,
          :shape => :dot,
          :size => 2,
          :colors => [
            [230, 220, 190],
            [255, 245, 220]
          ],
          :speed => [0.1, 0.3],
          :sway => 5,
          :zoom => [0.5, 0.8],
          :opacity => [70, 140],
          :layers => [:back, :mid]
        },
        {
          :type => :fall,
          :count => 4,
          :shape => :rect,
          :w => 1,
          :h => 3,
          :colors => [
            [170, 200, 230]
          ],
          :area => [60, 60, 330, 240],
          :speed => [2.0, 3.0],
          :sway => 0,
          :zoom => [0.6, 0.9],
          :opacity => [120, 200],
          :layers => [:back, :mid]
        }
      ]
    },
    # <<< CAVE
    # >>> COLOSSEUM
    :COLOSSEUM => {
      :layers => [
        { :bitmap => "pf_colosseum_crowd", :hd => true, :x => 0.0, :y => 94.22, :ox => 0, :oy => 0, :z => 1, :frames => 2, :frame_time => 14 },
        { :bitmap => "pf_colosseum_fence", :hd => true, :x => 0.0, :y => 81.78, :ox => 0, :oy => 0, :z => 2 },
        { :bitmap => "pf_colosseum_lamp0", :hd => true, :x => 133.33, :y => 0.0, :ox => 11, :oy => 0, :z => 3, :anim => :sway, :amp => 2.5, :period => 170 },
        {
          :bitmap => "pf_colosseum_cone0",
          :hd => true,
          :x => 99.11,
          :y => 37.78,
          :ox => 0,
          :oy => 0,
          :z => 3,
          :blend => 1,
          :anim => :pulse,
          :min => 60,
          :max => 110,
          :period => 90
        },
        { :bitmap => "pf_colosseum_lamp1", :hd => true, :x => 248.89, :y => 0.0, :ox => 11, :oy => 0, :z => 3, :anim => :sway, :amp => 2.5, :period => 201 },
        {
          :bitmap => "pf_colosseum_cone1",
          :hd => true,
          :x => 214.67,
          :y => 37.78,
          :ox => 0,
          :oy => 0,
          :z => 3,
          :blend => 1,
          :anim => :pulse,
          :min => 60,
          :max => 110,
          :period => 107
        },
        { :bitmap => "pf_colosseum_lamp2", :hd => true, :x => 337.78, :y => 0.0, :ox => 11, :oy => 0, :z => 30, :anim => :sway, :amp => 2.5, :period => 232 },
        {
          :bitmap => "pf_colosseum_cone2",
          :hd => true,
          :x => 303.56,
          :y => 24.44,
          :ox => 0,
          :oy => 0,
          :z => 30,
          :blend => 1,
          :anim => :pulse,
          :min => 60,
          :max => 110,
          :period => 124
        },
        { :bitmap => "pf_colosseum_lamp3", :hd => true, :x => 53.33, :y => 0.0, :ox => 11, :oy => 0, :z => 30, :anim => :sway, :amp => 2.5, :period => 263 },
        {
          :bitmap => "pf_colosseum_cone3",
          :hd => true,
          :x => 19.11,
          :y => 24.44,
          :ox => 0,
          :oy => 0,
          :z => 30,
          :blend => 1,
          :anim => :pulse,
          :min => 60,
          :max => 110,
          :period => 141
        }
      ],
      :fx => [
        {
          :type => :drift,
          :count => 16,
          :shape => :dot,
          :size => 2,
          :colors => [
            [230, 220, 190],
            [255, 245, 220]
          ],
          :speed => [0.2, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.9],
          :opacity => [80, 150],
          :layers => [:back, :mid, :front]
        },
        { :type => :flash, :color => [255, 240, 200], :alpha => 40, :interval => [200, 400], :decay => 8 }
      ]
    },
    # <<< COLOSSEUM
    # >>> CRYSTAL_CAVERN
    :CRYSTAL_CAVERN => {
      :layers => [
        {
          :bitmap => "pf_crystal_cavern_glow",
          :hd => true,
          :x => 0.0,
          :y => 66.67,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 40,
          :max => 140,
          :period => 140
        },
        {
          :bitmap => "pf_crystal_cavern_shine",
          :hd => true,
          :x => 0.0,
          :y => 38.22,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 30,
          :max => 130,
          :period => 90,
          :phase => 2.0
        },
        {
          :bitmap => "pf_crystal_cavern_shaft0",
          :hd => true,
          :x => 117.78,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 90,
          :period => 180,
          :phase => 0.0
        },
        {
          :bitmap => "pf_crystal_cavern_shaft1",
          :hd => true,
          :x => 215.56,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 90,
          :period => 230,
          :phase => 2.0
        },
        {
          :bitmap => "pf_crystal_cavern_shaft2",
          :hd => true,
          :x => 286.67,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 90,
          :period => 280,
          :phase => 4.0
        }
      ],
      :fx => [
        {
          :type => :twinkle,
          :count => 22,
          :shape => :spark,
          :size => 7,
          :colors => [
            [200, 255, 255],
            [255, 255, 255],
            [230, 190, 255]
          ],
          :speed => [3, 7],
          :zoom => [0.5, 1.0],
          :opacity => [170, 255],
          :layers => [:back, :mid],
          :blend => 1
        },
        {
          :type => :drift,
          :count => 10,
          :shape => :dot,
          :size => 2,
          :colors => [
            [200, 255, 255],
            [240, 200, 255]
          ],
          :speed => [0.2, 0.4],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :opacity => [90, 160],
          :layers => [:mid, :front],
          :blend => 1
        }
      ]
    },
    # <<< CRYSTAL_CAVERN
    # >>> DARK_CRYSTAL
    :DARK_CRYSTAL => {
      :art_extras => {
        "vacuum" => "dark006",
        "img003" => {
          :bitmap => "pf_dark_crystal_murk",
          :scrolling => true,
          :speed => 0.5,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 102.22,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 4
        }
      },
      :layers => [
        {
          :bitmap => "pf_dark_crystal_glow",
          :hd => true,
          :x => 0.0,
          :y => 66.67,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 10,
          :max => 80,
          :period => 200
        }
      ]
    },
    # <<< DARK_CRYSTAL
    # >>> DESERT
    :DESERT => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_desert_haze",
          :scrolling => true,
          :speed => 1,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 91.11,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 3
        },
        "img002" => {
          :bitmap => "pf_desert_haze2",
          :scrolling => true,
          :speed => 2,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 177.78,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 24
        }
      },
      :layers => [
        {
          :bitmap => "pf_desert_sun",
          :hd => true,
          :x => 228.89,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 90,
          :max => 170,
          :period => 200
        }
      ]
    },
    # <<< DESERT
    # >>> DRAGONS_DEN
    :DRAGONS_DEN => {
      :art_extras => {
        "img001" => { :bitmap => "decor009", :scrolling => true, :speed => 1, :direction => 1, :oy => 0, :z => 3, :flat => true, :opacity => 90 },
        "img003" => {
          :bitmap => "pf_dragons_den_haze",
          :scrolling => true,
          :speed => 0.5,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 102.22,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 4
        }
      },
      :layers => [
        {
          :bitmap => "pf_dragons_den_magma",
          :hd => true,
          :x => 0.0,
          :y => 66.67,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :opacity => 140,
          :anim => :pulse,
          :min => 50,
          :max => 150,
          :period => 130
        },
        {
          :bitmap => "pf_dragons_den_violet",
          :hd => true,
          :x => 124.44,
          :y => 80.44,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 30,
          :max => 110,
          :period => 190,
          :phase => 1.5
        },
        {
          :bitmap => "pf_dragons_den_goldglint",
          :hd => true,
          :x => 0.0,
          :y => 122.67,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :opacity => 120,
          :anim => :pulse,
          :min => 40,
          :max => 150,
          :period => 70
        }
      ]
    },
    # <<< DRAGONS_DEN
    # >>> FROZEN_LAKE
    :FROZEN_LAKE => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_frozen_lake_mist",
          :scrolling => true,
          :speed => 0.5,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 114.67,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 1
        }
      },
      :fx => [
        {
          :type => :fall,
          :count => 30,
          :bitmap => "snow",
          :speed => [0.6, 1.4],
          :sway => 12,
          :zoom => [0.2, 0.45],
          :opacity => [200, 255],
          :layers => [:back, :mid, :front]
        },
        {
          :type => :twinkle,
          :count => 12,
          :shape => :spark,
          :size => 5,
          :colors => [
            [220, 245, 255]
          ],
          :area => [0, 130, 384, 300],
          :speed => [3, 6],
          :zoom => [0.5, 0.9],
          :opacity => [160, 255],
          :layers => [:back, :mid],
          :blend => 1
        }
      ]
    },
    # <<< FROZEN_LAKE
    # >>> MOUNTAIN
    :MOUNTAIN => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_mountain_clouds",
          :scrolling => true,
          :speed => 0.5,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 31.11,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 1
        },
        "img002" => {
          :bitmap => "pf_mountain_mist",
          :scrolling => true,
          :speed => 1,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 120.0,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 2
        }
      },
      :layers => [
        {
          :bitmap => "pf_mountain_pine0",
          :hd => true,
          :x => 78.22,
          :y => 208.89,
          :ox => 34,
          :oy => 146,
          :z => 22,
          :anim => :sway,
          :amp => 1.5,
          :period => 130,
          :angle => -4
        },
        {
          :bitmap => "pf_mountain_pine1",
          :hd => true,
          :x => 342.22,
          :y => 208.89,
          :ox => 38,
          :oy => 166,
          :z => 22,
          :anim => :sway,
          :amp => 1.5,
          :period => 170,
          :angle => -4
        }
      ],
      :fx => [
        {
          :type => :streak,
          :count => 8,
          :shape => :rect,
          :w => 22,
          :h => 1,
          :colors => [
            [255, 255, 255]
          ],
          :angle => 178,
          :speed => [4, 7],
          :zoom => [0.6, 1.0],
          :opacity => [50, 110],
          :layers => [:back, :front]
        },
        {
          :type => :drift,
          :count => 8,
          :shape => :dot,
          :size => 2,
          :colors => [
            [120, 160, 90],
            [170, 190, 110]
          ],
          :dir => -1,
          :speed => [1.0, 2.0],
          :sway => 10,
          :zoom => [0.6, 1.0],
          :opacity => [140, 220],
          :spin => 8,
          :layers => [:mid, :front]
        }
      ]
    },
    # <<< MOUNTAIN
    # >>> SNOWY_MOUNTAIN
    :SNOWY_MOUNTAIN => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_snowy_mountain_spindrift",
          :scrolling => true,
          :speed => 3,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 102.22,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 3
        },
        "img002" => {
          :bitmap => "pf_snowy_mountain_blizzard",
          :scrolling => true,
          :speed => 4,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 160.0,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 26
        }
      },
      :layers => [
        {
          :bitmap => "pf_snowy_mountain_flags",
          :hd => true,
          :x => 280.0,
          :y => 75.56,
          :ox => 212,
          :oy => 2,
          :z => 2,
          :anim => :sway,
          :amp => 1.2,
          :period => 90
        },
        {
          :bitmap => "pf_snowy_mountain_flags2",
          :hd => true,
          :x => 97.78,
          :y => 53.33,
          :ox => 182,
          :oy => 0,
          :z => 30,
          :anim => :sway,
          :amp => 1.6,
          :period => 110
        }
      ],
      :fx => [
        {
          :type => :fall,
          :count => 44,
          :bitmap => "snow",
          :speed => [0.8, 1.8],
          :sway => 16,
          :zoom => [0.2, 0.5],
          :opacity => [200, 255],
          :layers => [:back, :mid, :front]
        },
        {
          :type => :streak,
          :count => 10,
          :shape => :rect,
          :w => 18,
          :h => 1,
          :colors => [
            [255, 255, 255]
          ],
          :angle => 172,
          :speed => [6, 9],
          :zoom => [0.6, 1.0],
          :opacity => [60, 130],
          :layers => [:back, :front]
        }
      ]
    },
    # <<< SNOWY_MOUNTAIN
    # >>> VOLCANIC
    :VOLCANIC => {
      :art_extras => {
        "img001" => { :bitmap => "decor006", :scrolling => true, :speed => 2, :direction => -1, :oy => 0, :z => 3, :flat => true, :opacity => 155 },
        "img002" => { :bitmap => "decor009", :scrolling => true, :speed => 1, :direction => 1, :oy => 0, :z => 3, :flat => true, :opacity => 96 },
        "img003" => {
          :bitmap => "pf_volcanic_haze",
          :scrolling => true,
          :speed => 0.5,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 111.11,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 4
        },
        "img005" => { :bitmap => "base001", :scrolling => true, :speed => 0.5, :direction => -1, :oy => 0, :y => 122, :z => 1, :flat => true, :opacity => 110 },
        "bubbles" => "bubbleRed"
      },
      :layers => [
        {
          :bitmap => "pf_volcanic_lavaglow",
          :hd => true,
          :x => 48.89,
          :y => 13.78,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :opacity => 150,
          :anim => :pulse,
          :min => 60,
          :max => 170,
          :period => 110
        },
        {
          :bitmap => "pf_volcanic_caldera",
          :hd => true,
          :x => 84.0,
          :y => 249.33,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 40,
          :max => 110,
          :period => 170
        },
        {
          :bitmap => "pf_volcanic_banner0",
          :hd => true,
          :x => 171.56,
          :y => 48.0,
          :ox => 19,
          :oy => 3,
          :z => 2,
          :anim => :sway,
          :amp => 2.2,
          :period => 150
        },
        {
          :bitmap => "pf_volcanic_banner1",
          :hd => true,
          :x => 284.44,
          :y => 48.0,
          :ox => 19,
          :oy => 3,
          :z => 2,
          :anim => :sway,
          :amp => 2.2,
          :period => 187
        }
      ]
    },
    # <<< VOLCANIC
    # >>> WASTELAND
    :WASTELAND => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_wasteland_smog",
          :scrolling => true,
          :speed => 1,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 88.89,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 3
        }
      },
      :layers => [
        {
          :bitmap => "pf_wasteland_pools",
          :hd => true,
          :x => 79.11,
          :y => 130.22,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :opacity => 110,
          :anim => :pulse,
          :min => 40,
          :max => 120,
          :period => 100
        }
      ],
      :fx => [
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 20,
          :colors => [
            [90, 86, 84],
            [70, 68, 70],
            [110, 104, 98]
          ],
          :area => [141.7, 23.3, 151.7, 133.3],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [60, 110],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 20,
          :colors => [
            [90, 86, 84],
            [70, 68, 70],
            [110, 104, 98]
          ],
          :area => [306.1, 21.6, 316.1, 131.6],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [60, 110],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 12,
          :shape => :glow,
          :size => 5,
          :colors => [
            [150, 230, 80],
            [190, 255, 120]
          ],
          :area => [100, 140, 340, 300],
          :speed => [0.3, 0.7],
          :sway => 6,
          :zoom => [0.4, 0.8],
          :opacity => [120, 200],
          :layers => [:back, :mid],
          :blend => 1
        },
        {
          :type => :drift,
          :count => 10,
          :shape => :dot,
          :size => 2,
          :colors => [
            [110, 110, 110],
            [150, 140, 130],
            [80, 80, 85]
          ],
          :speed => [0.6, 1.2],
          :sway => 4,
          :zoom => [0.5, 0.8],
          :opacity => [90, 150],
          :layers => [:back, :mid]
        }
      ]
    },
    # <<< WASTELAND
  }

  ART_PROFILES.each do |id, art|
    base = PROFILES[id] || DEFAULT_PROFILE.dup
    merged = base.merge(art.reject { |k, _| k == :stages })
    if art[:stages] || base[:stages]
      st = (base[:stages] || {}).dup
      (art[:stages] || {}).each { |n, o| st[n] = (st[n] || {}).merge(o) }
      merged[:stages] = st
    end
    PROFILES[id] = merged
  end
end
