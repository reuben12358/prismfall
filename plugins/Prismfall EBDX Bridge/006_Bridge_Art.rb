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
        "img001" => { :bitmap => "decor006", :scrolling => true, :speed => 2, :direction => -1, :oy => 0, :z => 3, :flat => true, :opacity => 120 },
        "img003" => {
          :bitmap => "pf_ashen_waste_steam",
          :scrolling => true,
          :speed => 0.5,
          :direction => 1,
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
          :bitmap => "pf_ashen_waste_seams",
          :hd => true,
          :x => 53.78,
          :y => 83.56,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 70,
          :max => 200,
          :period => 100
        },
        {
          :bitmap => "pf_ashen_waste_sheen",
          :hd => true,
          :x => 105.33,
          :y => 149.78,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 30,
          :max => 90,
          :period => 180
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
          :amp => 1.8,
          :period => 160
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
          :amp => 1.8,
          :period => 189
        },
        {
          :bitmap => "pf_ashen_waste_plume",
          :hd => true,
          :x => 146.67,
          :y => 135.11,
          :ox => 32,
          :oy => 200,
          :z => 3,
          :frames => 8,
          :frame_time => 9,
          :zoom => 0.8,
          :phase_frames => 0,
          :opacity => 220
        },
        {
          :bitmap => "pf_ashen_waste_vent0",
          :hd => true,
          :x => 136.44,
          :y => 130.67,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 90,
          :max => 230,
          :period => 72
        },
        {
          :bitmap => "pf_ashen_waste_plume",
          :hd => true,
          :x => 272.0,
          :y => 133.33,
          :ox => 32,
          :oy => 200,
          :z => 3,
          :frames => 8,
          :frame_time => 10,
          :zoom => 0.8,
          :phase_frames => 23,
          :opacity => 220
        },
        {
          :bitmap => "pf_ashen_waste_vent1",
          :hd => true,
          :x => 261.78,
          :y => 128.89,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 90,
          :max => 230,
          :period => 80
        },
        {
          :bitmap => "pf_ashen_waste_plume",
          :hd => true,
          :x => 102.22,
          :y => 208.89,
          :ox => 32,
          :oy => 200,
          :z => 23,
          :frames => 8,
          :frame_time => 11,
          :zoom => 1.3,
          :phase_frames => 46,
          :opacity => 220
        },
        {
          :bitmap => "pf_ashen_waste_vent2",
          :hd => true,
          :x => 92.0,
          :y => 204.44,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 90,
          :max => 230,
          :period => 88
        },
        {
          :bitmap => "pf_ashen_waste_plume",
          :hd => true,
          :x => 320.0,
          :y => 231.11,
          :ox => 32,
          :oy => 200,
          :z => 23,
          :frames => 8,
          :frame_time => 12,
          :zoom => 1.3,
          :phase_frames => 69,
          :opacity => 220
        },
        {
          :bitmap => "pf_ashen_waste_vent3",
          :hd => true,
          :x => 309.78,
          :y => 226.67,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 90,
          :max => 230,
          :period => 96
        }
      ],
      :fx => [
        {
          :type => :twinkle,
          :count => 22,
          :shape => :spark,
          :size => 7,
          :colors => [
            [255, 255, 255],
            [200, 180, 255],
            [255, 200, 150]
          ],
          :area => [0, 110, 384, 308],
          :speed => [4, 8],
          :zoom => [0.4, 0.9],
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
            [200, 180, 255],
            [255, 255, 255]
          ],
          :speed => [0.3, 0.7],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :opacity => [110, 190],
          :layers => [:mid, :front],
          :blend => 1
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 20,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [141.7, 25.1, 151.7, 135.1],
          :speed => [0.5, 1.0],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [70, 130],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 20,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [267.0, 23.3, 277.0, 133.3],
          :speed => [0.5, 1.0],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [70, 130],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 20,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [97.2, 98.9, 107.2, 208.9],
          :speed => [0.5, 1.0],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [70, 130],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 20,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [315.0, 121.1, 325.0, 231.1],
          :speed => [0.5, 1.0],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [70, 130],
          :layers => [:back],
          :blend => 0
        }
      ]
    },
    # <<< ASHEN_WASTE
    # >>> BEACH
    :BEACH => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_beach_glints",
          :scrolling => true,
          :speed => 0.5,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 97.78,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 1,
          :opacity => 170
        },
        "img002" => {
          :bitmap => "pf_beach_foam",
          :scrolling => true,
          :speed => 1,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 116.44,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 1
        }
      },
      :layers => [
        {
          :bitmap => "pf_beach_gull0",
          :hd => true,
          :x => 136.89,
          :y => 77.33,
          :ox => 10,
          :oy => 6,
          :z => 1,
          :anim => [:drift, :bob],
          :amp => 30,
          :period => 300,
          :phase => 0
        },
        {
          :bitmap => "pf_beach_gull1",
          :hd => true,
          :x => 279.11,
          :y => 86.22,
          :ox => 10,
          :oy => 6,
          :z => 1,
          :anim => [:drift, :bob],
          :amp => 30,
          :period => 370,
          :phase => 1
        },
        {
          :bitmap => "pf_beach_gull2",
          :hd => true,
          :x => 314.67,
          :y => 72.89,
          :ox => 10,
          :oy => 6,
          :z => 1,
          :anim => [:drift, :bob],
          :amp => 30,
          :period => 440,
          :phase => 2
        }
      ],
      :fx => [
        {
          :type => :twinkle,
          :count => 12,
          :shape => :spark,
          :size => 5,
          :colors => [
            [255, 255, 255]
          ],
          :area => [0, 95, 384, 125],
          :speed => [2, 5],
          :zoom => [0.5, 0.8],
          :opacity => [150, 255],
          :layers => [:back],
          :blend => 1
        }
      ]
    },
    # <<< BEACH
    # >>> BLEED
    :BLEED => {
      :layers => [
        {
          :bitmap => "pf_bleed_slice0",
          :hd => true,
          :x => 4.44,
          :y => 47.11,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :anim => :flicker,
          :opacity => 0,
          :min => 230,
          :chance => 0.04,
          :dropout => 6
        },
        {
          :bitmap => "pf_bleed_slice1",
          :hd => true,
          :x => 8.0,
          :y => 134.22,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :anim => :flicker,
          :opacity => 0,
          :min => 230,
          :chance => 0.04,
          :dropout => 6
        },
        {
          :bitmap => "pf_bleed_slice2",
          :hd => true,
          :x => 1.78,
          :y => 226.22,
          :ox => 0,
          :oy => 0,
          :z => 26,
          :anim => :flicker,
          :opacity => 0,
          :min => 230,
          :chance => 0.04,
          :dropout => 6
        },
        {
          :bitmap => "pf_bleed_slice3",
          :hd => true,
          :x => 0.0,
          :y => 204.44,
          :ox => 0,
          :oy => 0,
          :z => 26,
          :anim => :flicker,
          :opacity => 0,
          :min => 230,
          :chance => 0.04,
          :dropout => 6
        },
        {
          :bitmap => "pf_bleed_tears",
          :hd => true,
          :x => 42.67,
          :y => 44.89,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 60,
          :max => 200,
          :period => 40
        }
      ]
    },
    # <<< BLEED
    # >>> CAVE
    :CAVE => {
      :art_extras => {
        "img001" => { :bitmap => "decor006", :scrolling => true, :speed => 2, :direction => -1, :oy => 0, :z => 3, :flat => true, :opacity => 110 },
        "img003" => { :bitmap => "fog", :scrolling => true, :speed => 0.5, :direction => 1, :oy => 0, :z => 4, :flat => true, :opacity => 150 }
      },
      :layers => [
        { :bitmap => "pf_cave_lantern0", :hd => true, :x => 109.78, :y => 83.56, :ox => 11, :oy => 2, :z => 3, :anim => :sway, :amp => 3, :period => 160 },
        {
          :bitmap => "pf_cave_lanternglow0",
          :hd => true,
          :x => 81.78,
          :y => 71.56,
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
        { :bitmap => "pf_cave_lantern1", :hd => true, :x => 284.44, :y => 66.67, :ox => 11, :oy => 2, :z => 3, :anim => :sway, :amp => 3, :period => 200 },
        {
          :bitmap => "pf_cave_lanternglow1",
          :hd => true,
          :x => 256.44,
          :y => 62.67,
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
      ],
      :stages => {
        2 => {
          :backdrop => "field_cave_cracked",
          :layers => [
            { :bitmap => "pf_cave_lantern0", :hd => true, :x => 109.78, :y => 83.56, :ox => 11, :oy => 2, :z => 3, :anim => :sway, :amp => 3, :period => 160 },
            {
              :bitmap => "pf_cave_lanternglow0",
              :hd => true,
              :x => 81.78,
              :y => 71.56,
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
            { :bitmap => "pf_cave_lantern1", :hd => true, :x => 284.44, :y => 66.67, :ox => 11, :oy => 2, :z => 3, :anim => :sway, :amp => 3, :period => 200 },
            {
              :bitmap => "pf_cave_lanternglow1",
              :hd => true,
              :x => 256.44,
              :y => 62.67,
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
            {
              :bitmap => "pf_cave_cracked_daylight",
              :hd => true,
              :x => 179.56,
              :y => 66.22,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :pulse,
              :min => 60,
              :max => 120,
              :period => 130
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
            },
            {
              :type => :fall,
              :count => 10,
              :shape => :dot,
              :size => 3,
              :colors => [
                [120, 100, 84],
                [80, 64, 54]
              ],
              :area => [60, 60, 330, 250],
              :speed => [2.5, 4.0],
              :sway => 0,
              :zoom => [0.5, 1.0],
              :opacity => [220, 255],
              :layers => [:back, :mid, :front]
            },
            {
              :type => :rise,
              :count => 4,
              :shape => :puff,
              :size => 18,
              :colors => [
                [230, 220, 190],
                [255, 245, 220]
              ],
              :area => [203.9, 91.1, 213.9, 151.1],
              :speed => [0.25, 0.5],
              :sway => 6,
              :zoom => [0.5, 0.8],
              :grow => 1.6,
              :opacity => [40, 80],
              :layers => [:back],
              :blend => 0
            }
          ]
        }
      }
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
      ],
      :stages => {
        2 => {
          :backdrop => "field_colosseum_frenzy",
          :layers => [
            { :bitmap => "pf_colosseum_crowd", :hd => true, :x => 0.0, :y => 94.22, :ox => 0, :oy => 0, :z => 1, :frames => 2, :frame_time => 5 },
            { :bitmap => "pf_colosseum_fence", :hd => true, :x => 0.0, :y => 81.78, :ox => 0, :oy => 0, :z => 2 },
            { :bitmap => "pf_colosseum_lamp0", :hd => true, :x => 133.33, :y => 0.0, :ox => 11, :oy => 0, :z => 3, :anim => :sway, :amp => 7, :period => 70 },
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
              :period => 70,
              :amp => 0
            },
            { :bitmap => "pf_colosseum_lamp1", :hd => true, :x => 248.89, :y => 0.0, :ox => 11, :oy => 0, :z => 3, :anim => :sway, :amp => 7, :period => 70 },
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
              :period => 70,
              :amp => 0
            },
            { :bitmap => "pf_colosseum_lamp2", :hd => true, :x => 337.78, :y => 0.0, :ox => 11, :oy => 0, :z => 30, :anim => :sway, :amp => 7, :period => 70 },
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
              :period => 70,
              :amp => 0
            },
            { :bitmap => "pf_colosseum_lamp3", :hd => true, :x => 53.33, :y => 0.0, :ox => 11, :oy => 0, :z => 30, :anim => :sway, :amp => 7, :period => 70 },
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
              :period => 70,
              :amp => 0
            },
            {
              :bitmap => "pf_colosseum_frenzy_roar",
              :hd => true,
              :x => 71.11,
              :y => 45.78,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 30,
              :max => 120,
              :period => 36
            }
          ],
          :fx => [
            {
              :type => :fall,
              :count => 30,
              :shape => :rect,
              :w => 3,
              :h => 2,
              :colors => [
                [230, 60, 50],
                [250, 210, 80],
                [240, 240, 240]
              ],
              :speed => [0.8, 1.6],
              :sway => 12,
              :zoom => [0.6, 1.0],
              :opacity => [200, 255],
              :spin => 10,
              :layers => [:back, :mid, :front]
            },
            {
              :type => :drift,
              :count => 14,
              :shape => :dot,
              :size => 2,
              :colors => [
                [230, 220, 190],
                [255, 245, 220]
              ],
              :speed => [0.4, 0.9],
              :sway => 6,
              :zoom => [0.5, 0.9],
              :opacity => [100, 170],
              :layers => [:back, :mid, :front]
            },
            { :type => :flash, :color => [255, 230, 180], :alpha => 70, :interval => [60, 140], :decay => 12, :double => true }
          ]
        }
      }
    },
    # <<< COLOSSEUM
    # >>> CORROSIVE_MIRE
    :CORROSIVE_MIRE => {
      :art_extras => {
        "bubbles" => "bubbleDark",
        "img010" => {
          :bitmap => "pf_corrosive_mire_goo",
          :scrolling => true,
          :vertical => true,
          :speed => 2,
          :direction => -1,
          :ox => 7,
          :oy => 0,
          :x => 160.0,
          :y => 104.89,
          :zoom => 0.444444444,
          :z => 2
        },
        "img011" => {
          :bitmap => "pf_corrosive_mire_goo",
          :scrolling => true,
          :vertical => true,
          :speed => 2,
          :direction => -1,
          :ox => 7,
          :oy => 0,
          :x => 288.89,
          :y => 104.89,
          :zoom => 0.444444444,
          :z => 2
        },
        "img012" => {
          :bitmap => "pf_corrosive_mire_goo",
          :scrolling => true,
          :vertical => true,
          :speed => 2,
          :direction => -1,
          :ox => 7,
          :oy => 0,
          :x => 333.33,
          :y => 104.89,
          :zoom => 0.444444444,
          :z => 2
        },
        "img020" => {
          :bitmap => "pf_corrosive_mire_fumes",
          :scrolling => true,
          :speed => 1,
          :direction => 1,
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
          :bitmap => "pf_corrosive_mire_sludgeglow",
          :hd => true,
          :x => 29.33,
          :y => 114.67,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 40,
          :max => 140,
          :period => 110
        },
        {
          :bitmap => "pf_corrosive_mire_lamp",
          :hd => true,
          :x => 208.89,
          :y => 0.0,
          :ox => 11,
          :oy => 0,
          :z => 3,
          :anim => :sway,
          :amp => 3,
          :period => 170
        },
        {
          :bitmap => "pf_corrosive_mire_lampcone",
          :hd => true,
          :x => 169.33,
          :y => 35.11,
          :ox => 0,
          :oy => 0,
          :z => 3,
          :blend => 1,
          :anim => [:pulse, :flicker],
          :min => 40,
          :max => 100,
          :period => 60,
          :chance => 0.02,
          :dropout => 5
        }
      ],
      :fx => [
        {
          :type => :rise,
          :count => 18,
          :shape => :glow,
          :size => 5,
          :colors => [
            [190, 90, 230],
            [140, 220, 90],
            [220, 120, 255]
          ],
          :area => [0, 120, 384, 308],
          :speed => [0.3, 0.8],
          :sway => 6,
          :zoom => [0.4, 0.9],
          :opacity => [140, 220],
          :layers => [:back, :mid, :front],
          :blend => 1
        },
        {
          :type => :fall,
          :count => 6,
          :shape => :rect,
          :w => 2,
          :h => 3,
          :colors => [
            [150, 230, 90]
          ],
          :area => [140, 0, 340, 120],
          :speed => [1.5, 2.5],
          :sway => 0,
          :zoom => [0.6, 1.0],
          :opacity => [180, 240],
          :layers => [:back]
        }
      ]
    },
    # <<< CORROSIVE_MIRE
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
          :y => 57.78,
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
          :y => 102.22,
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
          :y => 186.67,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 24
        }
      },
      :layers => [
        {
          :bitmap => "pf_desert_sun",
          :hd => true,
          :x => 40.44,
          :y => 24.44,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 100,
          :max => 190,
          :period => 200
        },
        {
          :bitmap => "pf_desert_devil",
          :hd => true,
          :x => 277.78,
          :y => 82.22,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :anim => [:drift, :pulse],
          :amp => 40,
          :min => 30,
          :max => 120,
          :period => 260
        }
      ],
      :stages => {
        2 => {
          :layers => [
            {
              :bitmap => "pf_desert_sun",
              :hd => true,
              :x => 40.44,
              :y => 24.44,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 100,
              :max => 190,
              :period => 200
            }
          ],
          :fx => [
            {
              :type => :drift,
              :count => 16,
              :shape => :dot,
              :size => 3,
              :colors => [
                [255, 150, 200],
                [255, 230, 120],
                [210, 160, 255]
              ],
              :dir => 1,
              :speed => [0.6, 1.2],
              :sway => 14,
              :zoom => [0.6, 1.0],
              :opacity => [200, 255],
              :spin => 6,
              :layers => [:back, :mid, :front]
            },
            {
              :type => :rise,
              :count => 10,
              :shape => :dot,
              :size => 2,
              :colors => [
                [255, 230, 120],
                [255, 250, 200]
              ],
              :speed => [0.2, 0.5],
              :sway => 8,
              :zoom => [0.5, 0.8],
              :opacity => [120, 200],
              :layers => [:back, :mid],
              :blend => 1
            },
            {
              :type => :drift,
              :count => 4,
              :shape => :spark,
              :size => 5,
              :colors => [
                [255, 255, 255],
                [255, 200, 240]
              ],
              :speed => [0.4, 0.8],
              :sway => 20,
              :zoom => [0.6, 0.9],
              :opacity => [200, 255],
              :layers => [:mid, :front]
            }
          ],
          :art_extras => {  }
        }
      }
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
          :x => 168.44,
          :y => 107.56,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :opacity => 140,
          :anim => :pulse,
          :min => 50,
          :max => 170,
          :period => 130
        },
        {
          :bitmap => "pf_dragons_den_violet",
          :hd => true,
          :x => 122.67,
          :y => 47.56,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 30,
          :max => 120,
          :period => 190,
          :phase => 1.5
        },
        {
          :bitmap => "pf_dragons_den_goldglint",
          :hd => true,
          :x => 0.0,
          :y => 118.67,
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
      ],
      :stages => {
        2 => {
          :layers => [
            {
              :bitmap => "pf_dragons_den_wyrmfire_magma",
              :hd => true,
              :x => 38.22,
              :y => 70.22,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 110,
              :max => 230,
              :period => 60
            },
            {
              :bitmap => "pf_dragons_den_wyrmfire_eyes",
              :hd => true,
              :x => 145.33,
              :y => 68.44,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 100,
              :max => 255,
              :period => 45
            },
            {
              :bitmap => "pf_dragons_den_wyrmfire_flame",
              :hd => true,
              :x => 133.33,
              :y => 146.67,
              :ox => 13,
              :oy => 44,
              :z => 2,
              :frames => 4,
              :frame_time => 4,
              :zoom => 1.0,
              :blend => 0
            },
            {
              :bitmap => "pf_dragons_den_wyrmfire_flame",
              :hd => true,
              :x => 186.67,
              :y => 141.33,
              :ox => 13,
              :oy => 44,
              :z => 2,
              :frames => 4,
              :frame_time => 5,
              :zoom => 0.8,
              :blend => 0
            },
            {
              :bitmap => "pf_dragons_den_wyrmfire_flame",
              :hd => true,
              :x => 320.0,
              :y => 146.67,
              :ox => 13,
              :oy => 44,
              :z => 2,
              :frames => 4,
              :frame_time => 6,
              :zoom => 1.1,
              :blend => 0
            },
            {
              :bitmap => "pf_dragons_den_wyrmfire_flame",
              :hd => true,
              :x => 80.0,
              :y => 208.89,
              :ox => 13,
              :oy => 44,
              :z => 22,
              :frames => 4,
              :frame_time => 4,
              :zoom => 1.6,
              :blend => 0
            },
            {
              :bitmap => "pf_dragons_den_wyrmfire_flame",
              :hd => true,
              :x => 364.44,
              :y => 222.22,
              :ox => 13,
              :oy => 44,
              :z => 22,
              :frames => 4,
              :frame_time => 5,
              :zoom => 1.8,
              :blend => 0
            },
            {
              :bitmap => "pf_dragons_den_wyrmfire_flame",
              :hd => true,
              :x => 275.56,
              :y => 133.33,
              :ox => 13,
              :oy => 44,
              :z => 1,
              :frames => 4,
              :frame_time => 6,
              :zoom => 0.7,
              :blend => 0
            }
          ],
          :fx => [
            {
              :type => :rise,
              :count => 30,
              :shape => :glow,
              :size => 5,
              :colors => [
                [255, 140, 50],
                [200, 90, 255],
                [255, 210, 90]
              ],
              :speed => [1.0, 2.2],
              :sway => 10,
              :zoom => [0.3, 0.7],
              :opacity => [180, 255],
              :layers => [:back, :mid, :front],
              :blend => 1
            },
            {
              :type => :twinkle,
              :count => 10,
              :shape => :spark,
              :size => 5,
              :colors => [
                [255, 230, 120],
                [255, 250, 200]
              ],
              :area => [0, 120, 384, 308],
              :speed => [3, 6],
              :zoom => [0.5, 0.9],
              :opacity => [160, 255],
              :layers => [:back, :mid],
              :blend => 1
            }
          ],
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
            },
            "bubbles" => "bubbleRed"
          }
        }
      }
    },
    # <<< DRAGONS_DEN
    # >>> FACTORY
    :FACTORY => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_factory_belt",
          :scrolling => true,
          :speed => 2,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 129.78,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 2
        },
        "img010" => {
          :bitmap => "pf_factory_pour2",
          :scrolling => true,
          :vertical => true,
          :speed => 3,
          :direction => -1,
          :ox => 8,
          :oy => 0,
          :x => 267.56,
          :y => 88.89,
          :zoom => 0.444444444,
          :z => 2
        },
        "img002" => {
          :bitmap => "pf_factory_heat",
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
        }
      },
      :layers => [
        { :bitmap => "pf_factory_gear0", :hd => true, :x => 104.89, :y => 80.0, :ox => 109, :oy => 109, :z => 1, :anim => :rotate, :speed => 0.195652174 },
        { :bitmap => "pf_factory_gear1", :hd => true, :x => 158.22, :y => 46.22, :ox => 62, :oy => 62, :z => 1, :anim => :rotate, :speed => -0.346153846 },
        { :bitmap => "pf_factory_gear2", :hd => true, :x => 314.67, :y => 66.67, :ox => 130, :oy => 130, :z => 1, :anim => :rotate, :speed => -0.163636364 },
        { :bitmap => "pf_factory_gear3", :hd => true, :x => 367.11, :y => 120.0, :ox => 72, :oy => 72, :z => 1, :anim => :rotate, :speed => 0.3 },
        { :bitmap => "pf_factory_gear4", :hd => true, :x => 248.89, :y => 42.67, :ox => 48, :oy => 48, :z => 1, :anim => :rotate, :speed => 0.45 },
        {
          :bitmap => "pf_factory_crucible",
          :hd => true,
          :x => 288.44,
          :y => 66.67,
          :ox => 43,
          :oy => -12,
          :z => 2,
          :anim => :sway,
          :amp => 0.6,
          :period => 200
        },
        { :bitmap => "pf_factory_cruchain", :hd => true, :x => 286.22, :y => 0.0, :ox => 0, :oy => 0, :z => 2 },
        {
          :bitmap => "pf_factory_pourglow",
          :hd => true,
          :x => 224.0,
          :y => 106.67,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 110,
          :max => 220,
          :period => 30
        },
        {
          :bitmap => "pf_factory_furnace",
          :hd => true,
          :x => 42.67,
          :y => 239.56,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 60,
          :max => 130,
          :period => 140
        },
        {
          :bitmap => "pf_factory_channel",
          :hd => true,
          :x => 0.0,
          :y => 128.0,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 90,
          :max => 190,
          :period => 80
        },
        { :bitmap => "pf_factory_hook0", :hd => true, :x => 84.44, :y => 112.0, :ox => 11, :oy => 2, :z => 3, :anim => :sway, :amp => 3, :period => 150 },
        { :bitmap => "pf_factory_hook1", :hd => true, :x => 142.22, :y => 112.0, :ox => 11, :oy => 2, :z => 3, :anim => :sway, :amp => 3, :period => 180 },
        { :bitmap => "pf_factory_hook2", :hd => true, :x => 320.0, :y => 112.0, :ox => 11, :oy => 2, :z => 3, :anim => :sway, :amp => 3, :period => 210 }
      ],
      :fx => [
        {
          :type => :fall,
          :count => 14,
          :shape => :dot,
          :size => 2,
          :colors => [
            [255, 150, 50],
            [255, 210, 90],
            [255, 240, 170]
          ],
          :area => [262, 90, 290, 140],
          :speed => [2.0, 3.5],
          :sway => 10,
          :zoom => [0.5, 0.8],
          :opacity => [200, 255],
          :layers => [:back, :mid],
          :blend => 1
        },
        {
          :type => :rise,
          :count => 10,
          :shape => :glow,
          :size => 4,
          :colors => [
            [255, 150, 50],
            [255, 200, 80]
          ],
          :area => [0, 140, 384, 308],
          :speed => [0.5, 1.2],
          :sway => 8,
          :zoom => [0.3, 0.6],
          :opacity => [150, 230],
          :layers => [:back, :mid, :front],
          :blend => 1
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 20,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [61.7, 42.2, 71.7, 142.2],
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
          :size => 20,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [359.4, 51.1, 369.4, 151.1],
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
    # <<< FACTORY
    # >>> FAIRY_TALE
    :FAIRY_TALE => {
      :layers => [
        {
          :bitmap => "pf_fairy_tale_windows",
          :hd => true,
          :x => 179.11,
          :y => 69.33,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 80,
          :max => 220,
          :period => 90
        },
        {
          :bitmap => "pf_fairy_tale_wisp0",
          :hd => true,
          :x => 108.44,
          :y => 104.0,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => [:pulse, :bob],
          :amp => 6,
          :min => 80,
          :max => 220,
          :period => 100,
          :phase => 0
        },
        {
          :bitmap => "pf_fairy_tale_wisp1",
          :hd => true,
          :x => 299.56,
          :y => 95.11,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => [:pulse, :bob],
          :amp => 6,
          :min => 80,
          :max => 220,
          :period => 117,
          :phase => 1
        },
        {
          :bitmap => "pf_fairy_tale_wisp2",
          :hd => true,
          :x => 179.56,
          :y => 86.22,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => [:pulse, :bob],
          :amp => 6,
          :min => 80,
          :max => 220,
          :period => 134,
          :phase => 2
        },
        {
          :bitmap => "pf_fairy_tale_wisp3",
          :hd => true,
          :x => 72.89,
          :y => 179.56,
          :ox => 0,
          :oy => 0,
          :z => 26,
          :blend => 1,
          :anim => [:pulse, :bob],
          :amp => 6,
          :min => 80,
          :max => 220,
          :period => 151,
          :phase => 3
        },
        {
          :bitmap => "pf_fairy_tale_wisp4",
          :hd => true,
          :x => 330.67,
          :y => 179.56,
          :ox => 0,
          :oy => 0,
          :z => 26,
          :blend => 1,
          :anim => [:pulse, :bob],
          :amp => 6,
          :min => 80,
          :max => 220,
          :period => 168,
          :phase => 4
        }
      ],
      :fx => [
        {
          :type => :rise,
          :count => 16,
          :shape => :spark,
          :size => 5,
          :colors => [
            [255, 180, 230],
            [255, 240, 160],
            [255, 255, 255]
          ],
          :speed => [0.3, 0.7],
          :sway => 12,
          :zoom => [0.5, 1.0],
          :opacity => [170, 255],
          :layers => [:back, :mid, :front],
          :blend => 1
        },
        {
          :type => :fall,
          :count => 10,
          :shape => :dot,
          :size => 3,
          :colors => [
            [255, 170, 210],
            [255, 220, 235]
          ],
          :speed => [0.4, 0.8],
          :sway => 16,
          :zoom => [0.6, 1.0],
          :opacity => [200, 255],
          :spin => 6,
          :layers => [:back, :mid, :front]
        }
      ]
    },
    # <<< FAIRY_TALE
    # >>> FLOODED_DUNES
    :FLOODED_DUNES => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_flooded_dunes_wisps",
          :scrolling => true,
          :speed => 1,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 66.67,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 1
        },
        "img002" => {
          :bitmap => "pf_flooded_dunes_spray",
          :scrolling => true,
          :speed => 2,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 89.78,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 2
        }
      },
      :layers => [
        {
          :bitmap => "pf_flooded_dunes_swellA",
          :hd => true,
          :x => 0.44,
          :y => 125.78,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => [:drift, :pulse],
          :amp => 5,
          :min => 60,
          :max => 200,
          :period => 210
        },
        {
          :bitmap => "pf_flooded_dunes_swellB",
          :hd => true,
          :x => 0.44,
          :y => 125.78,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => [:drift, :pulse],
          :amp => 5,
          :min => 40,
          :max => 160,
          :period => 170,
          :phase => 2.4
        },
        {
          :bitmap => "pf_flooded_dunes_tide",
          :hd => true,
          :x => 0.0,
          :y => 123.11,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => [:bob, :pulse],
          :amp => 2.5,
          :min => 90,
          :max => 230,
          :period => 180
        },
        {
          :bitmap => "pf_flooded_dunes_sheen",
          :hd => true,
          :x => 88.44,
          :y => 138.22,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 70,
          :period => 240
        }
      ],
      :fx => [
        {
          :type => :streak,
          :count => 40,
          :shape => :rect,
          :w => 12,
          :h => 1,
          :colors => [
            [210, 225, 240],
            [180, 200, 220]
          ],
          :angle => 102,
          :speed => [7, 10],
          :zoom => [0.6, 1.0],
          :opacity => [110, 190],
          :layers => [:back, :mid, :front]
        },
        {
          :type => :drift,
          :count => 14,
          :shape => :dot,
          :size => 2,
          :colors => [
            [255, 255, 255],
            [210, 235, 250]
          ],
          :dir => 1,
          :area => [0, 110, 384, 300],
          :speed => [1.0, 2.0],
          :sway => 10,
          :zoom => [0.5, 0.9],
          :opacity => [150, 230],
          :layers => [:back, :mid, :front]
        },
        {
          :type => :twinkle,
          :count => 14,
          :shape => :spark,
          :size => 5,
          :colors => [
            [255, 255, 255],
            [210, 240, 255]
          ],
          :area => [0, 130, 384, 300],
          :speed => [2, 5],
          :zoom => [0.5, 0.9],
          :opacity => [160, 255],
          :layers => [:back, :mid],
          :blend => 1
        }
      ]
    },
    # <<< FLOODED_DUNES
    # >>> FLOWER_GARDEN
    :FLOWER_GARDEN => {
      :layers => [],
      :stages => {
        2 => {
          :layers => [
            {
              :bitmap => "pf_flower_garden2_sun",
              :hd => true,
              :x => 202.67,
              :y => 0.0,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :pulse,
              :min => 42,
              :max => 84,
              :period => 200
            }
          ]
        },
        3 => {
          :layers => [
            {
              :bitmap => "pf_flower_garden3_sun",
              :hd => true,
              :x => 202.67,
              :y => 0.0,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :pulse,
              :min => 48,
              :max => 96,
              :period => 200
            }
          ]
        },
        4 => {
          :layers => [
            {
              :bitmap => "pf_flower_garden4_sun",
              :hd => true,
              :x => 202.67,
              :y => 0.0,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :pulse,
              :min => 54,
              :max => 108,
              :period => 200
            }
          ]
        },
        5 => {
          :layers => [
            {
              :bitmap => "pf_flower_garden5_sun",
              :hd => true,
              :x => 202.67,
              :y => 0.0,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :pulse,
              :min => 60,
              :max => 120,
              :period => 200
            },
            {
              :bitmap => "pf_flower_garden5_glow",
              :hd => true,
              :x => 216.44,
              :y => 34.22,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 40,
              :max => 140,
              :period => 120
            }
          ]
        }
      }
    },
    # <<< FLOWER_GARDEN
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
        },
        {
          :type => :rise,
          :count => 5,
          :shape => :puff,
          :size => 14,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [128.3, 47.3, 138.3, 117.3],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [60, 120],
          :layers => [:back],
          :blend => 0
        }
      ],
      :layers => [
        {
          :bitmap => "pf_frozen_lake_window",
          :hd => true,
          :x => 112.0,
          :y => 121.78,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 120,
          :max => 220,
          :period => 70
        }
      ],
      :player_raise => 8
    },
    # <<< FROZEN_LAKE
    # >>> GLASS_DUNES
    :GLASS_DUNES => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_glass_dunes_prism",
          :rainbow => true,
          :speed => 2,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 88.89,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 2,
          :opacity => 200
        },
        "img002" => {
          :bitmap => "pf_glass_dunes_steam",
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
        }
      },
      :layers => [
        {
          :bitmap => "pf_glass_dunes_seams",
          :hd => true,
          :x => 0.0,
          :y => 119.56,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 70,
          :max => 210,
          :period => 95
        },
        {
          :bitmap => "pf_glass_dunes_facets",
          :hd => true,
          :x => 31.11,
          :y => 100.89,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 40,
          :max => 170,
          :period => 130,
          :phase => 1.2
        },
        {
          :bitmap => "pf_glass_dunes_pools",
          :hd => true,
          :x => 31.56,
          :y => 125.78,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 70,
          :period => 60
        },
        {
          :bitmap => "pf_glass_dunes_sun",
          :hd => true,
          :x => 178.22,
          :y => 4.89,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 110,
          :max => 190,
          :period => 210
        },
        {
          :bitmap => "pf_glass_dunes_plume",
          :hd => true,
          :x => 274.67,
          :y => 262.22,
          :ox => 32,
          :oy => 200,
          :z => 23,
          :frames => 8,
          :frame_time => 10,
          :zoom => 1.1,
          :phase_frames => 0,
          :opacity => 200
        },
        {
          :bitmap => "pf_glass_dunes_plume",
          :hd => true,
          :x => 159.56,
          :y => 203.11,
          :ox => 32,
          :oy => 200,
          :z => 23,
          :frames => 8,
          :frame_time => 12,
          :zoom => 1.1,
          :phase_frames => 31,
          :opacity => 200
        },
        {
          :bitmap => "pf_glass_dunes_plume",
          :hd => true,
          :x => 66.22,
          :y => 204.0,
          :ox => 32,
          :oy => 200,
          :z => 23,
          :frames => 8,
          :frame_time => 14,
          :zoom => 1.1,
          :phase_frames => 62,
          :opacity => 200
        },
        {
          :bitmap => "pf_glass_dunes_plume",
          :hd => true,
          :x => 190.67,
          :y => 131.11,
          :ox => 32,
          :oy => 200,
          :z => 3,
          :frames => 8,
          :frame_time => 16,
          :zoom => 0.9,
          :phase_frames => 93,
          :opacity => 200
        }
      ],
      :fx => [
        {
          :type => :twinkle,
          :count => 22,
          :shape => :spark,
          :size => 7,
          :colors => [
            [255, 255, 255],
            [200, 255, 220]
          ],
          :area => [0, 110, 384, 308],
          :speed => [4, 8],
          :zoom => [0.4, 0.9],
          :opacity => [170, 255],
          :layers => [:back, :mid],
          :blend => 1
        },
        {
          :type => :rise,
          :count => 8,
          :shape => :glow,
          :size => 4,
          :colors => [
            [255, 170, 70],
            [255, 220, 140]
          ],
          :area => [0, 140, 384, 308],
          :speed => [0.3, 0.7],
          :sway => 8,
          :zoom => [0.3, 0.6],
          :opacity => [140, 220],
          :layers => [:back, :mid],
          :blend => 1
        },
        {
          :type => :rise,
          :count => 5,
          :shape => :puff,
          :size => 18,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [269.7, 172.2, 279.7, 262.2],
          :speed => [0.4, 0.8],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [60, 120],
          :layers => [:back, :mid],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 5,
          :shape => :puff,
          :size => 18,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [154.6, 113.1, 164.6, 203.1],
          :speed => [0.4, 0.8],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [60, 120],
          :layers => [:back, :mid],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 5,
          :shape => :puff,
          :size => 18,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [61.2, 114.0, 71.2, 204.0],
          :speed => [0.4, 0.8],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [60, 120],
          :layers => [:back, :mid],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 5,
          :shape => :puff,
          :size => 18,
          :colors => [
            [235, 235, 238],
            [205, 210, 215]
          ],
          :area => [185.7, 41.1, 195.7, 131.1],
          :speed => [0.4, 0.8],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [60, 120],
          :layers => [:back, :mid],
          :blend => 0
        }
      ],
      :stages => {
        2 => {
          :art_extras => {
            "img001" => {
              :bitmap => "pf_glass_dunes_prism",
              :rainbow => true,
              :speed => 2,
              :flat => true,
              :ox => 0,
              :oy => 0,
              :x => 0,
              :y => 88.89,
              :zoom_x => 0.444444444,
              :zoom_y => 0.444444444,
              :z => 2,
              :opacity => 110
            },
            "img002" => {
              :bitmap => "pf_glass_dunes_mirror_cirrus",
              :scrolling => true,
              :speed => 0.3,
              :direction => 1,
              :flat => true,
              :ox => 0,
              :oy => 0,
              :x => 0,
              :y => 31.11,
              :zoom_x => 0.444444444,
              :zoom_y => 0.444444444,
              :z => 1
            }
          },
          :layers => [
            {
              :bitmap => "pf_glass_dunes_mirror_facets",
              :hd => true,
              :x => 23.56,
              :y => 73.78,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 40,
              :max => 190,
              :period => 110
            },
            {
              :bitmap => "pf_glass_dunes_mirror_sheen",
              :hd => true,
              :x => 0.0,
              :y => 82.67,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => [:drift, :pulse],
              :amp => 60,
              :min => 20,
              :max => 110,
              :period => 300
            },
            {
              :bitmap => "pf_glass_dunes_mirror_ponds",
              :hd => true,
              :x => 32.44,
              :y => 126.22,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 15,
              :max => 60,
              :period => 170
            },
            {
              :bitmap => "pf_glass_dunes_mirror_sun",
              :hd => true,
              :x => 189.33,
              :y => 7.11,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 110,
              :max => 180,
              :period => 240
            },
            {
              :bitmap => "pf_glass_dunes_mirror_sunglint",
              :hd => true,
              :x => 208.89,
              :y => 176.89,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 50,
              :max => 130,
              :period => 240,
              :phase => 1.0
            }
          ],
          :fx => [
            {
              :type => :twinkle,
              :count => 34,
              :shape => :spark,
              :size => 7,
              :colors => [
                [255, 255, 255],
                [215, 240, 255]
              ],
              :area => [0, 110, 384, 308],
              :speed => [3, 7],
              :zoom => [0.4, 1.0],
              :opacity => [180, 255],
              :layers => [:back, :mid],
              :blend => 1
            },
            {
              :type => :twinkle,
              :count => 10,
              :shape => :spark,
              :size => 5,
              :colors => [
                [255, 230, 250],
                [210, 255, 235],
                [220, 230, 255]
              ],
              :area => [0, 130, 384, 308],
              :speed => [2, 5],
              :zoom => [0.4, 0.8],
              :opacity => [140, 220],
              :layers => [:back],
              :blend => 1
            }
          ]
        }
      }
    },
    # <<< GLASS_DUNES
    # >>> GRAND_STAGE
    :GRAND_STAGE => {
      :art_extras => { "lightsA" => true, "spinLights" => true },
      :layers => [
        {
          :bitmap => "pf_grand_stage_spot",
          :hd => true,
          :x => 215.56,
          :y => 66.22,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 80,
          :max => 130,
          :period => 160
        },
        {
          :bitmap => "pf_grand_stage_pool",
          :hd => true,
          :x => 184.44,
          :y => 136.44,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 70,
          :max => 120,
          :period => 160
        },
        {
          :bitmap => "pf_grand_stage_footlights",
          :hd => true,
          :x => 9.33,
          :y => 279.56,
          :ox => 0,
          :oy => 0,
          :z => 24,
          :blend => 1,
          :anim => :pulse,
          :min => 120,
          :max => 200,
          :period => 90
        },
        {
          :bitmap => "pf_grand_stage_flatglow",
          :hd => true,
          :x => 158.67,
          :y => 68.89,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 30,
          :max => 70,
          :period => 220
        }
      ],
      :stages => {
        2 => {
          :layers => [
            {
              :bitmap => "pf_grand_stage_spot",
              :hd => true,
              :x => 215.56,
              :y => 66.22,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :pulse,
              :min => 80,
              :max => 130,
              :period => 160
            },
            {
              :bitmap => "pf_grand_stage_pool",
              :hd => true,
              :x => 184.44,
              :y => 136.44,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 70,
              :max => 120,
              :period => 160
            },
            {
              :bitmap => "pf_grand_stage_footlights",
              :hd => true,
              :x => 9.33,
              :y => 279.56,
              :ox => 0,
              :oy => 0,
              :z => 24,
              :blend => 1,
              :anim => :pulse,
              :min => 120,
              :max => 200,
              :period => 90
            },
            {
              :bitmap => "pf_grand_stage_flatglow",
              :hd => true,
              :x => 158.67,
              :y => 68.89,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 30,
              :max => 70,
              :period => 220
            },
            {
              :bitmap => "pf_grand_stage2_sweep0",
              :hd => true,
              :x => 111.11,
              :y => 66.67,
              :ox => 2,
              :oy => 2,
              :z => 2,
              :blend => 1,
              :anim => :sway,
              :amp => 14,
              :period => 150,
              :phase => 0,
              :opacity => 200
            },
            {
              :bitmap => "pf_grand_stage2_sweep1",
              :hd => true,
              :x => 226.67,
              :y => 66.67,
              :ox => 48,
              :oy => 1,
              :z => 2,
              :blend => 1,
              :anim => :sway,
              :amp => 14,
              :period => 190,
              :phase => 2,
              :opacity => 200
            }
          ],
          :fx => [
            {
              :type => :fall,
              :count => 34,
              :shape => :rect,
              :w => 3,
              :h => 2,
              :colors => [
                [255, 90, 90],
                [255, 200, 80],
                [120, 255, 120],
                [90, 200, 255],
                [190, 120, 255]
              ],
              :speed => [0.6, 1.3],
              :sway => 12,
              :zoom => [0.6, 1.0],
              :opacity => [200, 255],
              :spin => 8,
              :layers => [:back, :mid, :front]
            }
          ]
        },
        3 => {
          :layers => [
            {
              :bitmap => "pf_grand_stage_spot",
              :hd => true,
              :x => 215.56,
              :y => 66.22,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :pulse,
              :min => 80,
              :max => 130,
              :period => 160
            },
            {
              :bitmap => "pf_grand_stage_pool",
              :hd => true,
              :x => 184.44,
              :y => 136.44,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 70,
              :max => 120,
              :period => 160
            },
            {
              :bitmap => "pf_grand_stage_footlights",
              :hd => true,
              :x => 9.33,
              :y => 279.56,
              :ox => 0,
              :oy => 0,
              :z => 24,
              :blend => 1,
              :anim => :pulse,
              :min => 120,
              :max => 200,
              :period => 90
            },
            {
              :bitmap => "pf_grand_stage_flatglow",
              :hd => true,
              :x => 158.67,
              :y => 68.89,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 30,
              :max => 70,
              :period => 220
            },
            {
              :bitmap => "pf_grand_stage3_sweep0",
              :hd => true,
              :x => 111.11,
              :y => 66.67,
              :ox => 2,
              :oy => 2,
              :z => 2,
              :blend => 1,
              :anim => :sway,
              :amp => 14,
              :period => 150,
              :phase => 0,
              :opacity => 200
            },
            {
              :bitmap => "pf_grand_stage3_sweep1",
              :hd => true,
              :x => 226.67,
              :y => 66.67,
              :ox => 48,
              :oy => 1,
              :z => 2,
              :blend => 1,
              :anim => :sway,
              :amp => 14,
              :period => 190,
              :phase => 2,
              :opacity => 200
            },
            {
              :bitmap => "pf_grand_stage3_sweep2",
              :hd => true,
              :x => 342.22,
              :y => 66.67,
              :ox => 182,
              :oy => 2,
              :z => 2,
              :blend => 1,
              :anim => :sway,
              :amp => 14,
              :period => 230,
              :phase => 4,
              :opacity => 200
            },
            {
              :bitmap => "pf_grand_stage3_gold",
              :hd => true,
              :x => 95.56,
              :y => 78.67,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 50,
              :max => 120,
              :period => 70
            }
          ],
          :fx => [
            {
              :type => :fall,
              :count => 48,
              :shape => :rect,
              :w => 3,
              :h => 2,
              :colors => [
                [255, 90, 90],
                [255, 200, 80],
                [120, 255, 120],
                [90, 200, 255],
                [190, 120, 255]
              ],
              :speed => [0.6, 1.3],
              :sway => 12,
              :zoom => [0.6, 1.0],
              :opacity => [200, 255],
              :spin => 8,
              :layers => [:back, :mid, :front]
            },
            {
              :type => :fall,
              :count => 14,
              :shape => :dot,
              :size => 3,
              :colors => [
                [220, 30, 50],
                [255, 120, 140]
              ],
              :speed => [0.5, 1.0],
              :sway => 14,
              :zoom => [0.6, 1.0],
              :opacity => [220, 255],
              :spin => 6,
              :layers => [:mid, :front]
            },
            {
              :type => :twinkle,
              :count => 14,
              :shape => :spark,
              :size => 5,
              :colors => [
                [255, 230, 120],
                [255, 250, 200]
              ],
              :speed => [3, 6],
              :zoom => [0.5, 0.9],
              :opacity => [170, 255],
              :layers => [:back, :mid],
              :blend => 1
            }
          ]
        }
      }
    },
    # <<< GRAND_STAGE
    # >>> HOLLOW_CATHEDRAL
    :HOLLOW_CATHEDRAL => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_hollow_cathedral_mist",
          :scrolling => true,
          :speed => 0.5,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 133.33,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 4
        }
      },
      :layers => [
        {
          :bitmap => "pf_hollow_cathedral_rose",
          :hd => true,
          :x => 200.0,
          :y => 68.44,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 60,
          :max => 160,
          :period => 180
        },
        {
          :bitmap => "pf_hollow_cathedral_candles",
          :hd => true,
          :x => 199.11,
          :y => 112.0,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => [:pulse, :flicker],
          :min => 120,
          :max => 210,
          :period => 25,
          :chance => 0.03,
          :dropout => 2
        },
        {
          :bitmap => "pf_hollow_cathedral_moon0",
          :hd => true,
          :x => 140.89,
          :y => 66.22,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 30,
          :max => 80,
          :period => 240,
          :phase => 0
        },
        {
          :bitmap => "pf_hollow_cathedral_moon1",
          :hd => true,
          :x => 283.56,
          :y => 66.22,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 30,
          :max => 80,
          :period => 300,
          :phase => 2
        }
      ],
      :stages => {
        2 => {
          :layers => [
            {
              :bitmap => "pf_hollow_cathedral_consecrated_rose",
              :hd => true,
              :x => 200.0,
              :y => 68.44,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 120,
              :max => 220,
              :period => 140
            },
            {
              :bitmap => "pf_hollow_cathedral_candles",
              :hd => true,
              :x => 199.11,
              :y => 112.0,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => [:pulse, :flicker],
              :min => 120,
              :max => 210,
              :period => 25,
              :chance => 0.03,
              :dropout => 2
            },
            {
              :bitmap => "pf_hollow_cathedral_consecrated_holy0",
              :hd => true,
              :x => 158.67,
              :y => 84.0,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :pulse,
              :min => 50,
              :max => 110,
              :period => 200,
              :phase => 0.0
            },
            {
              :bitmap => "pf_hollow_cathedral_consecrated_holy1",
              :hd => true,
              :x => 214.22,
              :y => 84.0,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :pulse,
              :min => 50,
              :max => 110,
              :period => 250,
              :phase => 1.5
            },
            {
              :bitmap => "pf_hollow_cathedral_consecrated_holy2",
              :hd => true,
              :x => 261.33,
              :y => 84.0,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :pulse,
              :min => 50,
              :max => 110,
              :period => 300,
              :phase => 3.0
            }
          ],
          :fx => [
            {
              :type => :rise,
              :count => 18,
              :shape => :spark,
              :size => 5,
              :colors => [
                [255, 230, 120],
                [255, 250, 200],
                [255, 255, 255]
              ],
              :speed => [0.2, 0.5],
              :sway => 12,
              :zoom => [0.5, 0.9],
              :opacity => [170, 255],
              :layers => [:back, :mid, :front],
              :blend => 1
            },
            {
              :type => :drift,
              :count => 10,
              :shape => :dot,
              :size => 2,
              :colors => [
                [230, 220, 190],
                [255, 245, 220]
              ],
              :speed => [0.1, 0.3],
              :sway => 4,
              :zoom => [0.5, 0.8],
              :opacity => [90, 160],
              :layers => [:back, :mid]
            }
          ],
          :art_extras => { "lightsC" => true }
        }
      }
    },
    # <<< HOLLOW_CATHEDRAL
    # >>> INVERSE
    :INVERSE => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_inverse_static",
          :scrolling => true,
          :speed => 2,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 120.0,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 3
        }
      },
      :layers => [
        {
          :bitmap => "pf_inverse_rock0",
          :hd => true,
          :x => 87.56,
          :y => 106.67,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => :bob,
          :amp => 6,
          :period => 200,
          :phase => 0
        },
        {
          :bitmap => "pf_inverse_rock1",
          :hd => true,
          :x => 290.22,
          :y => 102.67,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => :bob,
          :amp => 6,
          :period => 250,
          :phase => 2
        }
      ]
    },
    # <<< INVERSE
    # >>> MEADOW
    :MEADOW => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_meadow_clouds",
          :scrolling => true,
          :speed => 0.17,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => -64.0,
          :y => 0.0,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 0,
          :parallax => [0.35, 0.18]
        },
        "img002" => {
          :bitmap => "pf_meadow_breeze",
          :scrolling => true,
          :speed => 2,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 133.33,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 3
        },
        "img003" => { :bitmap => "pf_meadow_front", :flat => true, :x => 0, :y => 0, :ox => 0, :oy => 0, :zoom_x => 0.444444444, :zoom_y => 0.444444444, :z => 1 }
      },
      :layers => [
        { :bitmap => "pf_meadow_sails", :hd => true, :x => 272.0, :y => 93.33, :ox => 27, :oy => 27, :z => 1, :anim => :rotate, :speed => 0.8 },
        {
          :bitmap => "pf_meadow_shaft0",
          :hd => true,
          :x => 43.56,
          :y => 25.78,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 80,
          :period => 190,
          :phase => 0.0
        },
        {
          :bitmap => "pf_meadow_shaft1",
          :hd => true,
          :x => 101.33,
          :y => 25.78,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 80,
          :period => 250,
          :phase => 1.9
        },
        {
          :bitmap => "pf_meadow_shaft2",
          :hd => true,
          :x => 159.11,
          :y => 25.78,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 80,
          :period => 310,
          :phase => 3.8
        },
        {
          :bitmap => "pf_meadow_grass0",
          :hd => true,
          :x => 88.89,
          :y => 149.33,
          :ox => 25,
          :oy => 50,
          :z => 2,
          :anim => :sway,
          :amp => 3,
          :period => 110,
          :phase => 0.0
        },
        {
          :bitmap => "pf_meadow_grass1",
          :hd => true,
          :x => 311.11,
          :y => 151.11,
          :ox => 22,
          :oy => 54,
          :z => 2,
          :anim => :sway,
          :amp => 3,
          :period => 119,
          :phase => 0.4
        },
        {
          :bitmap => "pf_meadow_grass2",
          :hd => true,
          :x => 6.22,
          :y => 287.11,
          :ox => 14,
          :oy => 151,
          :z => 24,
          :anim => :sway,
          :amp => 5,
          :period => 128,
          :phase => 0.8
        },
        {
          :bitmap => "pf_meadow_grass3",
          :hd => true,
          :x => 245.33,
          :y => 277.33,
          :ox => 57,
          :oy => 120,
          :z => 24,
          :anim => :sway,
          :amp => 5,
          :period => 137,
          :phase => 1.2
        },
        {
          :bitmap => "pf_meadow_grass4",
          :hd => true,
          :x => 364.44,
          :y => 269.33,
          :ox => 77,
          :oy => 161,
          :z => 24,
          :anim => :sway,
          :amp => 5,
          :period => 146,
          :phase => 1.6
        },
        {
          :bitmap => "pf_meadow_grass5",
          :hd => true,
          :x => 306.67,
          :y => 291.56,
          :ox => 45,
          :oy => 112,
          :z => 24,
          :anim => :sway,
          :amp => 5,
          :period => 155,
          :phase => 2.0
        },
        {
          :bitmap => "pf_meadow_grass6",
          :hd => true,
          :x => 191.11,
          :y => 302.22,
          :ox => 60,
          :oy => 92,
          :z => 24,
          :anim => :sway,
          :amp => 5,
          :period => 164,
          :phase => 2.4
        }
      ],
      :fx => [
        {
          :type => :drift,
          :count => 18,
          :shape => :dot,
          :size => 2,
          :colors => [
            [255, 255, 220],
            [255, 240, 160]
          ],
          :dir => 1,
          :speed => [0.6, 1.4],
          :sway => 14,
          :zoom => [0.5, 0.9],
          :opacity => [170, 240],
          :layers => [:back, :mid, :front],
          :blend => 1
        },
        {
          :type => :drift,
          :count => 8,
          :shape => :dot,
          :size => 3,
          :colors => [
            [255, 200, 220],
            [255, 240, 140],
            [210, 170, 255]
          ],
          :dir => 1,
          :speed => [0.6, 1.2],
          :sway => 16,
          :zoom => [0.6, 1.0],
          :opacity => [200, 255],
          :spin => 6,
          :layers => [:mid, :front]
        },
        {
          :type => :drift,
          :count => 3,
          :shape => :spark,
          :size => 5,
          :colors => [
            [255, 240, 120],
            [255, 255, 255]
          ],
          :speed => [0.3, 0.6],
          :sway => 20,
          :zoom => [0.6, 0.9],
          :opacity => [200, 255],
          :layers => [:mid]
        }
      ]
    },
    # <<< MEADOW
    # >>> MINDSCAPE
    :MINDSCAPE => {
      :art_extras => {
        "vacuum" => "dark006",
        "img001" => {
          :bitmap => "pf_mindscape_thought",
          :scrolling => true,
          :speed => 0.5,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 106.67,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 3
        }
      },
      :layers => [
        {
          :bitmap => "pf_mindscape_door",
          :hd => true,
          :x => 262.22,
          :y => 96.0,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 80,
          :max => 200,
          :period => 120
        },
        {
          :bitmap => "pf_mindscape_penrose",
          :hd => true,
          :x => 93.33,
          :y => 62.22,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 30,
          :max => 120,
          :period => 170,
          :phase => 1.0
        },
        {
          :bitmap => "pf_mindscape_shelf0",
          :hd => true,
          :x => 88.44,
          :y => 101.78,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => :bob,
          :amp => 4,
          :period => 160,
          :phase => 0
        },
        {
          :bitmap => "pf_mindscape_shelf1",
          :hd => true,
          :x => 310.67,
          :y => 146.22,
          :ox => 0,
          :oy => 0,
          :z => 22,
          :anim => :bob,
          :amp => 4,
          :period => 200,
          :phase => 1
        },
        {
          :bitmap => "pf_mindscape_shelf2",
          :hd => true,
          :x => 190.22,
          :y => 70.67,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => :bob,
          :amp => 4,
          :period => 240,
          :phase => 2
        },
        {
          :bitmap => "pf_mindscape_book0",
          :hd => true,
          :x => 236.62,
          :y => 93.66,
          :ox => 11,
          :oy => 6,
          :z => 2,
          :anim => [:bob, :sway],
          :amp => 5,
          :period => 100,
          :phase => 0
        },
        {
          :bitmap => "pf_mindscape_book1",
          :hd => true,
          :x => 299.68,
          :y => 78.59,
          :ox => 11,
          :oy => 6,
          :z => 2,
          :anim => [:bob, :sway],
          :amp => 5,
          :period => 113,
          :phase => 1
        },
        {
          :bitmap => "pf_mindscape_book2",
          :hd => true,
          :x => 307.58,
          :y => 82.89,
          :ox => 11,
          :oy => 6,
          :z => 2,
          :anim => [:bob, :sway],
          :amp => 5,
          :period => 126,
          :phase => 2
        },
        {
          :bitmap => "pf_mindscape_book3",
          :hd => true,
          :x => 265.24,
          :y => 88.01,
          :ox => 11,
          :oy => 6,
          :z => 2,
          :anim => [:bob, :sway],
          :amp => 5,
          :period => 139,
          :phase => 3
        },
        {
          :bitmap => "pf_mindscape_book4",
          :hd => true,
          :x => 320.76,
          :y => 102.64,
          :ox => 11,
          :oy => 6,
          :z => 2,
          :anim => [:bob, :sway],
          :amp => 5,
          :period => 152,
          :phase => 4
        },
        {
          :bitmap => "pf_mindscape_book5",
          :hd => true,
          :x => 143.24,
          :y => 84.63,
          :ox => 11,
          :oy => 6,
          :z => 2,
          :anim => [:bob, :sway],
          :amp => 5,
          :period => 165,
          :phase => 5
        },
        {
          :bitmap => "pf_mindscape_book6",
          :hd => true,
          :x => 276.69,
          :y => 100.39,
          :ox => 11,
          :oy => 6,
          :z => 2,
          :anim => [:bob, :sway],
          :amp => 5,
          :period => 178,
          :phase => 6
        },
        {
          :bitmap => "pf_mindscape_book7",
          :hd => true,
          :x => 312.72,
          :y => 90.06,
          :ox => 11,
          :oy => 6,
          :z => 2,
          :anim => [:bob, :sway],
          :amp => 5,
          :period => 191,
          :phase => 7
        }
      ],
      :stages => {
        2 => {
          :layers => [
            { :bitmap => "pf_mindscape_nightmare_eye", :hd => true, :x => 111.11, :y => 93.33, :z => 1, :frames => 4, :frame_time => 24, :zoom => 1.0 },
            { :bitmap => "pf_mindscape_nightmare_eye", :hd => true, :x => 311.11, :y => 84.44, :z => 1, :frames => 4, :frame_time => 31, :zoom => 1.6 },
            { :bitmap => "pf_mindscape_nightmare_eye", :hd => true, :x => 191.11, :y => 75.56, :z => 1, :frames => 4, :frame_time => 38, :zoom => 1.0 },
            { :bitmap => "pf_mindscape_nightmare_eye", :hd => true, :x => 355.56, :y => 146.67, :z => 1, :frames => 4, :frame_time => 45, :zoom => 1.6 },
            { :bitmap => "pf_mindscape_nightmare_eye", :hd => true, :x => 93.33, :y => 146.67, :z => 1, :frames => 4, :frame_time => 52, :zoom => 1.0 },
            {
              :bitmap => "pf_mindscape_nightmare_door",
              :hd => true,
              :x => 258.67,
              :y => 92.44,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 60,
              :max => 220,
              :period => 50
            }
          ],
          :fx => [
            {
              :type => :rise,
              :count => 16,
              :shape => :glow,
              :size => 5,
              :colors => [
                [60, 0, 20],
                [120, 10, 40],
                [20, 0, 10]
              ],
              :speed => [0.2, 0.5],
              :sway => 12,
              :zoom => [0.5, 1.0],
              :opacity => [140, 220],
              :layers => [:back, :mid, :front]
            },
            { :type => :flash, :color => [160, 0, 30], :alpha => 60, :interval => [160, 300], :decay => 10 }
          ],
          :art_extras => {
            "vacuum" => "dark006",
            "img001" => {
              :bitmap => "pf_mindscape_nightmare_dread",
              :scrolling => true,
              :speed => 0.5,
              :direction => -1,
              :flat => true,
              :ox => 0,
              :oy => 0,
              :x => 0,
              :y => 106.67,
              :zoom_x => 0.444444444,
              :zoom_y => 0.444444444,
              :z => 3
            }
          }
        }
      }
    },
    # <<< MINDSCAPE
    # >>> MOUNTAIN
    :MOUNTAIN => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_mountain_foam",
          :scrolling => true,
          :speed => 2,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 87.11,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 1,
          :opacity => 150
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
          :y => 80.0,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 3
        },
        "img003" => { :bitmap => "pf_mountain_crags", :flat => true, :x => 0, :y => 0, :ox => 0, :oy => 0, :zoom_x => 0.444444444, :zoom_y => 0.444444444, :z => 2 }
      },
      :layers => [
        {
          :bitmap => "pf_mountain_hawk",
          :hd => true,
          :x => 236.0,
          :y => 80.44,
          :ox => 13,
          :oy => 7,
          :z => 3,
          :anim => [:drift, :bob],
          :amp => 60,
          :period => 420
        },
        {
          :bitmap => "pf_mountain_spray",
          :hd => true,
          :x => 115.11,
          :y => 73.78,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 40,
          :max => 120,
          :period => 70
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
          :type => :rise,
          :count => 10,
          :shape => :dot,
          :size => 2,
          :colors => [
            [255, 255, 255],
            [210, 235, 255]
          ],
          :area => [90, 80, 300, 110],
          :speed => [0.3, 0.7],
          :sway => 6,
          :zoom => [0.5, 0.9],
          :opacity => [150, 230],
          :layers => [:back]
        }
      ]
    },
    # <<< MOUNTAIN
    # >>> NEON_GRID
    :NEON_GRID => {
      :art_extras => {
        "spinLights" => true,
        "img001" => {
          :bitmap => "pf_neon_grid_scan",
          :scrolling => true,
          :speed => 4,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 116.44,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 2
        }
      },
      :layers => [
        {
          :bitmap => "pf_neon_grid_circuits",
          :hd => true,
          :x => 0.0,
          :y => 65.78,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => [:pulse, :flicker],
          :min => 60,
          :max => 180,
          :period => 70,
          :chance => 0.008,
          :dropout => 4
        },
        {
          :bitmap => "pf_neon_grid_board0",
          :hd => true,
          :x => 92.44,
          :y => 39.11,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => [:bob, :flicker],
          :amp => 2,
          :period => 120,
          :chance => 0.01,
          :dropout => 5,
          :min => 60
        },
        {
          :bitmap => "pf_neon_grid_board1",
          :hd => true,
          :x => 283.56,
          :y => 25.78,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => [:bob, :flicker],
          :amp => 2,
          :period => 150,
          :chance => 0.01,
          :dropout => 5,
          :min => 60
        },
        {
          :bitmap => "pf_neon_grid_board2",
          :hd => true,
          :x => 230.22,
          :y => 79.11,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => [:bob, :flicker],
          :amp => 2,
          :period => 180,
          :chance => 0.01,
          :dropout => 5,
          :min => 60
        },
        {
          :bitmap => "pf_neon_grid_airship",
          :hd => true,
          :x => 145.78,
          :y => 9.78,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :anim => [:drift, :bob],
          :amp => 40,
          :period => 600
        }
      ],
      :stages => {
        2 => {
          :art_extras => {  },
          :layers => [
            {
              :bitmap => "pf_neon_grid_blackout_alarm",
              :hd => true,
              :x => 84.89,
              :y => 69.33,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 20,
              :max => 220,
              :period => 60
            },
            {
              :bitmap => "pf_neon_grid_blackout_sparks",
              :hd => true,
              :x => 143.56,
              :y => 145.78,
              :ox => 0,
              :oy => 0,
              :z => 2,
              :blend => 1,
              :anim => :flicker,
              :opacity => 0,
              :min => 255,
              :chance => 0.06,
              :dropout => 3
            },
            {
              :bitmap => "pf_neon_grid_blackout_flicker",
              :hd => true,
              :x => 0.0,
              :y => 68.0,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :flicker,
              :opacity => 0,
              :min => 160,
              :chance => 0.02,
              :dropout => 5
            }
          ],
          :fx => [
            {
              :type => :streak,
              :count => 8,
              :shape => :rect,
              :w => 10,
              :h => 1,
              :colors => [
                [200, 240, 255],
                [255, 255, 200]
              ],
              :area => [60, 130, 330, 300],
              :angle => 8,
              :speed => [8, 12],
              :zoom => [0.6, 1.0],
              :opacity => [180, 255],
              :layers => [:back, :mid],
              :blend => 1
            },
            {
              :type => :twinkle,
              :count => 14,
              :shape => :spark,
              :size => 5,
              :colors => [
                [200, 240, 255],
                [255, 255, 255]
              ],
              :area => [40, 130, 340, 300],
              :speed => [8, 14],
              :zoom => [0.4, 0.8],
              :opacity => [200, 255],
              :layers => [:back, :mid],
              :blend => 1
            },
            { :type => :flash, :color => [120, 200, 255], :alpha => 80, :interval => [120, 260], :decay => 20, :double => true }
          ]
        }
      }
    },
    # <<< NEON_GRID
    # >>> NEW_MOON
    :NEW_MOON => {
      :art_extras => {
        "vacuum" => "dark004",
        "img001" => {
          :bitmap => "pf_new_moon_shadow",
          :scrolling => true,
          :speed => 0.5,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 128.89,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 4
        }
      },
      :layers => [
        {
          :bitmap => "pf_new_moon_corona",
          :hd => true,
          :x => 224.0,
          :y => 52.44,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 50,
          :max => 150,
          :period => 200
        },
        {
          :bitmap => "pf_new_moon_windows",
          :hd => true,
          :x => 0.0,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :flicker,
          :opacity => 150,
          :min => 50,
          :chance => 0.01,
          :dropout => 10
        }
      ],
      :fx => [
        {
          :type => :twinkle,
          :count => 20,
          :bitmap => "star",
          :area => [0, 66, 384, 110],
          :speed => [1, 3],
          :zoom => [0.6, 1.2],
          :opacity => [140, 255],
          :layers => [:back]
        },
        {
          :type => :rise,
          :count => 8,
          :shape => :glow,
          :size => 5,
          :colors => [
            [150, 110, 220],
            [90, 70, 160]
          ],
          :speed => [0.2, 0.4],
          :sway => 10,
          :zoom => [0.5, 0.9],
          :opacity => [90, 160],
          :layers => [:back, :mid, :front],
          :blend => 1
        }
      ],
      :stages => {
        2 => {
          :layers => [
            {
              :bitmap => "pf_new_moon_abyss_rim",
              :hd => true,
              :x => 184.44,
              :y => 136.44,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 20,
              :max => 90,
              :period => 180
            }
          ],
          :fx => [
            {
              :type => :rise,
              :count => 12,
              :shape => :glow,
              :size => 5,
              :colors => [
                [90, 60, 160],
                [50, 30, 100]
              ],
              :speed => [0.1, 0.3],
              :sway => 10,
              :zoom => [0.5, 0.9],
              :opacity => [60, 130],
              :layers => [:back, :mid, :front],
              :blend => 1
            }
          ],
          :art_extras => {
            "vacuum" => "dark004",
            "img001" => {
              :bitmap => "pf_new_moon_abyss_void",
              :scrolling => true,
              :speed => 0.5,
              :direction => -1,
              :flat => true,
              :ox => 0,
              :oy => 0,
              :x => 0,
              :y => 106.67,
              :zoom_x => 0.444444444,
              :zoom_y => 0.444444444,
              :z => 4
            }
          }
        },
        3 => {
          :layers => [
            {
              :bitmap => "pf_new_moon_lamplight_lamps",
              :hd => true,
              :x => 69.33,
              :y => 122.22,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => [:pulse, :flicker],
              :min => 150,
              :max => 220,
              :period => 40,
              :chance => 0.008,
              :dropout => 3
            },
            {
              :bitmap => "pf_new_moon_lamplight_pools",
              :hd => true,
              :x => 121.78,
              :y => 153.33,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 40,
              :max => 80,
              :period => 120
            },
            {
              :bitmap => "pf_new_moon_lamplight_windows",
              :hd => true,
              :x => 74.67,
              :y => 130.67,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 120,
              :max => 200,
              :period => 90
            },
            {
              :bitmap => "pf_new_moon_corona",
              :hd => true,
              :x => 224.0,
              :y => 52.44,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 50,
              :max => 150,
              :period => 200
            }
          ],
          :fx => [
            {
              :type => :rise,
              :count => 8,
              :shape => :glow,
              :size => 4,
              :colors => [
                [255, 190, 100],
                [255, 150, 60]
              ],
              :area => [60, 110, 330, 180],
              :speed => [0.2, 0.4],
              :sway => 6,
              :zoom => [0.4, 0.7],
              :opacity => [120, 200],
              :layers => [:back, :mid],
              :blend => 1
            },
            {
              :type => :twinkle,
              :count => 18,
              :bitmap => "star",
              :area => [0, 70, 384, 130],
              :speed => [1, 3],
              :zoom => [0.6, 1.2],
              :opacity => [140, 255],
              :layers => [:back]
            }
          ],
          :art_extras => {  }
        }
      }
    },
    # <<< NEW_MOON
    # >>> PRISM_ARENA
    :PRISM_ARENA => {
      :art_extras => {
        "lightsA" => true,
        "img001" => {
          :bitmap => "pf_prism_arena_prism",
          :scrolling => true,
          :speed => 1,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 111.11,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 3
        }
      },
      :layers => [
        {
          :bitmap => "pf_prism_arena_crowd",
          :hd => true,
          :x => 0.0,
          :y => 87.11,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :frames => 2,
          :frame_time => 12,
          :opacity => 200
        },
        {
          :bitmap => "pf_prism_arena_plates",
          :hd => true,
          :x => 76.44,
          :y => 63.11,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 60,
          :max => 170,
          :period => 120
        },
        {
          :bitmap => "pf_prism_arena_sigil",
          :hd => true,
          :x => 78.67,
          :y => 147.56,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 40,
          :max => 160,
          :period => 150,
          :phase => 1.0
        },
        {
          :bitmap => "pf_prism_arena_beam0",
          :hd => true,
          :x => 102.22,
          :y => 66.67,
          :ox => 2,
          :oy => 2,
          :z => 2,
          :blend => 1,
          :anim => :sway,
          :amp => 12,
          :period => 220,
          :phase => 0,
          :opacity => 170
        },
        {
          :bitmap => "pf_prism_arena_beam1",
          :hd => true,
          :x => 231.11,
          :y => 66.67,
          :ox => 39,
          :oy => 1,
          :z => 2,
          :blend => 1,
          :anim => :sway,
          :amp => 12,
          :period => 280,
          :phase => 2,
          :opacity => 170
        },
        {
          :bitmap => "pf_prism_arena_beam2",
          :hd => true,
          :x => 360.0,
          :y => 66.67,
          :ox => 169,
          :oy => 2,
          :z => 2,
          :blend => 1,
          :anim => :sway,
          :amp => 12,
          :period => 340,
          :phase => 4,
          :opacity => 170
        }
      ],
      :fx => [
        {
          :type => :twinkle,
          :count => 18,
          :shape => :spark,
          :size => 7,
          :colors => [
            [255, 90, 90],
            [255, 200, 80],
            [120, 255, 120],
            [90, 200, 255],
            [190, 120, 255]
          ],
          :speed => [2, 5],
          :zoom => [0.5, 1.0],
          :opacity => [170, 255],
          :layers => [:back, :mid],
          :blend => 1
        },
        {
          :type => :fall,
          :count => 22,
          :shape => :rect,
          :w => 3,
          :h => 2,
          :colors => [
            [255, 90, 90],
            [255, 200, 80],
            [120, 255, 120],
            [90, 200, 255],
            [190, 120, 255]
          ],
          :speed => [0.5, 1.0],
          :sway => 12,
          :zoom => [0.6, 1.0],
          :opacity => [200, 255],
          :spin => 8,
          :layers => [:back, :mid, :front]
        },
        { :type => :flash, :color => [255, 255, 255], :alpha => 50, :interval => [90, 200], :decay => 10 }
      ]
    },
    # <<< PRISM_ARENA
    # >>> RAINBOW
    :RAINBOW => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_rainbow_mist",
          :scrolling => true,
          :speed => 0.5,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 115.56,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 2
        },
        "img002" => {
          :bitmap => "pf_rainbow_clouds",
          :scrolling => true,
          :speed => 1,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 266.67,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 26
        }
      },
      :layers => [
        {
          :bitmap => "pf_rainbow_shimmer",
          :hd => true,
          :x => 79.56,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 90,
          :period => 160
        }
      ]
    },
    # <<< RAINBOW
    # >>> SCRAPYARD
    :SCRAPYARD => {
      :art_extras => {
        "img002" => {
          :bitmap => "pf_scrapyard_smoke",
          :scrolling => true,
          :speed => 0.5,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 80.0,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 4
        }
      },
      :layers => [
        {
          :bitmap => "pf_scrapyard_dangle",
          :hd => true,
          :x => 151.11,
          :y => 132.44,
          :ox => 15,
          :oy => 2,
          :z => 2,
          :anim => :sway,
          :amp => 4,
          :period => 210
        },
        { :bitmap => "pf_scrapyard_chain", :hd => true, :x => 111.11, :y => 53.33, :ox => 11, :oy => 2, :z => 2, :anim => :sway, :amp => 2, :period => 260 },
        { :bitmap => "pf_scrapyard_alarm", :hd => true, :x => 182.67, :y => 112.0, :ox => 0, :oy => 0, :z => 3 },
        {
          :bitmap => "pf_scrapyard_alarmglow",
          :hd => true,
          :x => 101.78,
          :y => 52.44,
          :ox => 0,
          :oy => 0,
          :z => 3,
          :blend => 1,
          :anim => [:pulse, :flicker],
          :min => 10,
          :max => 130,
          :period => 50,
          :chance => 0.03,
          :dropout => 8
        },
        {
          :bitmap => "pf_scrapyard_spark",
          :hd => true,
          :x => 144.0,
          :y => 128.0,
          :ox => 0,
          :oy => 0,
          :z => 3,
          :blend => 1,
          :anim => :flicker,
          :opacity => 0,
          :min => 255,
          :chance => 0.05,
          :dropout => 3
        }
      ],
      :fx => [
        {
          :type => :rise,
          :count => 7,
          :shape => :puff,
          :size => 24,
          :colors => [
            [90, 86, 84],
            [70, 68, 70],
            [110, 104, 98]
          ],
          :area => [128.3, 6.7, 138.3, 146.7],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [60, 120],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 7,
          :shape => :puff,
          :size => 24,
          :colors => [
            [90, 86, 84],
            [70, 68, 70],
            [110, 104, 98]
          ],
          :area => [306.1, -6.7, 316.1, 133.3],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [60, 120],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 5,
          :shape => :puff,
          :size => 26,
          :colors => [
            [90, 86, 84],
            [70, 68, 70],
            [110, 104, 98]
          ],
          :area => [35.0, 128.9, 45.0, 248.9],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [50, 100],
          :layers => [:front],
          :blend => 0
        },
        {
          :type => :fall,
          :count => 5,
          :shape => :dot,
          :size => 2,
          :colors => [
            [255, 150, 50],
            [255, 100, 30],
            [255, 210, 90]
          ],
          :area => [146, 130, 156, 150],
          :speed => [2.0, 3.5],
          :sway => 3,
          :zoom => [0.5, 0.8],
          :opacity => [200, 255],
          :layers => [:back],
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
          :speed => [0.2, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :opacity => [80, 140],
          :layers => [:back, :mid]
        }
      ]
    },
    # <<< SCRAPYARD
    # >>> SILKWOOD
    :SILKWOOD => {
      :art_extras => {
        "lightsC" => true,
        "img001" => { :bitmap => "forestShade", :z => 1, :flat => true, :oy => 0, :y => 94, :sheet => true, :frames => 2, :speed => 16, :opacity => 120 }
      },
      :layers => [
        {
          :bitmap => "pf_silkwood_dew",
          :hd => true,
          :x => 16.0,
          :y => 51.11,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 40,
          :max => 220,
          :period => 60
        },
        { :bitmap => "pf_silkwood_strand0", :hd => true, :x => 146.67, :y => 66.67, :ox => 4, :oy => 2, :z => 2, :anim => :sway, :amp => 4, :period => 140 },
        { :bitmap => "pf_silkwood_strand1", :hd => true, :x => 182.22, :y => 66.67, :ox => 4, :oy => 2, :z => 2, :anim => :sway, :amp => 4, :period => 163 },
        { :bitmap => "pf_silkwood_strand2", :hd => true, :x => 275.56, :y => 66.67, :ox => 4, :oy => 2, :z => 2, :anim => :sway, :amp => 4, :period => 186 },
        { :bitmap => "pf_silkwood_strand3", :hd => true, :x => 306.67, :y => 66.67, :ox => 4, :oy => 2, :z => 2, :anim => :sway, :amp => 4, :period => 209 },
        { :bitmap => "pf_silkwood_strand4", :hd => true, :x => 102.22, :y => 66.67, :ox => 4, :oy => 2, :z => 2, :anim => :sway, :amp => 4, :period => 232 },
        { :bitmap => "pf_silkwood_cocoon0", :hd => true, :x => 128.89, :y => 66.67, :ox => 8, :oy => 2, :z => 2, :anim => :sway, :amp => 3, :period => 180 },
        { :bitmap => "pf_silkwood_cocoon1", :hd => true, :x => 288.89, :y => 66.67, :ox => 8, :oy => 2, :z => 2, :anim => :sway, :amp => 3, :period => 221 },
        {
          :bitmap => "pf_silkwood_canopy",
          :hd => true,
          :x => 138.67,
          :y => 15.11,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 30,
          :max => 90,
          :period => 200
        }
      ],
      :fx => [
        {
          :type => :drift,
          :count => 12,
          :shape => :rect,
          :w => 7,
          :h => 1,
          :colors => [
            [255, 255, 245]
          ],
          :speed => [0.3, 0.7],
          :sway => 8,
          :zoom => [0.6, 1.0],
          :opacity => [90, 170],
          :layers => [:back, :mid, :front]
        },
        {
          :type => :rise,
          :count => 12,
          :shape => :dot,
          :size => 3,
          :colors => [
            [200, 255, 160],
            [240, 255, 200],
            [170, 230, 120]
          ],
          :speed => [0.3, 0.7],
          :sway => 10,
          :zoom => [0.4, 0.8],
          :opacity => [120, 200],
          :layers => [:back, :mid],
          :blend => 1
        },
        {
          :type => :twinkle,
          :count => 8,
          :shape => :spark,
          :size => 5,
          :colors => [
            [255, 255, 230]
          ],
          :area => [60, 50, 330, 230],
          :speed => [3, 6],
          :zoom => [0.4, 0.8],
          :opacity => [150, 255],
          :layers => [:back],
          :blend => 1
        }
      ]
    },
    # <<< SILKWOOD
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
          :y => 111.11,
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
          :y => 168.89,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 26
        }
      },
      :layers => [
        {
          :bitmap => "pf_snowy_mountain_flags",
          :hd => true,
          :x => 222.22,
          :y => 70.22,
          :ox => 202,
          :oy => 2,
          :z => 2,
          :anim => :sway,
          :amp => 1.2,
          :period => 90
        },
        {
          :bitmap => "pf_snowy_mountain_glint",
          :hd => true,
          :x => 78.67,
          :y => 170.22,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 90,
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
    # >>> STORMFRONT
    :STORMFRONT => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_stormfront_scud",
          :scrolling => true,
          :speed => 1,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => -64.0,
          :y => 0.0,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 0,
          :parallax => [0.3, 0.15]
        },
        "img002" => {
          :bitmap => "pf_stormfront_mist",
          :scrolling => true,
          :speed => 4,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 124.44,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 26
        },
        "img003" => { :bitmap => "pf_stormfront_front", :flat => true, :x => 0, :y => 0, :ox => 0, :oy => 0, :zoom_x => 0.444444444, :zoom_y => 0.444444444, :z => 1 }
      },
      :layers => [
        { :bitmap => "pf_stormfront_pennant", :hd => true, :x => 114.22, :y => 7.56, :ox => 2, :oy => 13, :z => 2, :anim => :sway, :amp => 8, :period => 40 },
        {
          :bitmap => "pf_stormfront_lightning",
          :hd => true,
          :x => 164.0,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :flicker,
          :opacity => 0,
          :min => 150,
          :chance => 0.012,
          :dropout => 4
        }
      ]
    },
    # <<< STORMFRONT
    # >>> UNDERWATER
    :UNDERWATER => {
      :art_extras => {
        "bubbles" => true,
        "lightsC" => true,
        "img001" => { :bitmap => "forestShade", :z => 1, :flat => true, :oy => 0, :y => 94, :sheet => true, :frames => 2, :speed => 16, :opacity => 90 }
      },
      :layers => [
        {
          :bitmap => "pf_underwater_kelp0",
          :hd => true,
          :x => 53.33,
          :y => 308.0,
          :ox => 22,
          :oy => 258,
          :z => 24,
          :anim => :sway,
          :amp => 3,
          :period => 120
        },
        {
          :bitmap => "pf_underwater_kelp1",
          :hd => true,
          :x => 88.89,
          :y => 308.0,
          :ox => 22,
          :oy => 198,
          :z => 24,
          :anim => :sway,
          :amp => 3,
          :period => 141
        },
        {
          :bitmap => "pf_underwater_kelp2",
          :hd => true,
          :x => 351.11,
          :y => 308.0,
          :ox => 22,
          :oy => 280,
          :z => 24,
          :anim => :sway,
          :amp => 3,
          :period => 162
        },
        {
          :bitmap => "pf_underwater_kelp3",
          :hd => true,
          :x => 373.33,
          :y => 308.0,
          :ox => 22,
          :oy => 220,
          :z => 24,
          :anim => :sway,
          :amp => 3,
          :period => 183
        },
        {
          :bitmap => "pf_underwater_ray0",
          :hd => true,
          :x => 97.33,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 80,
          :period => 150,
          :phase => 0.0
        },
        {
          :bitmap => "pf_underwater_ray1",
          :hd => true,
          :x => 199.56,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 80,
          :period => 190,
          :phase => 1.7
        },
        {
          :bitmap => "pf_underwater_ray2",
          :hd => true,
          :x => 297.33,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => :pulse,
          :min => 20,
          :max => 80,
          :period => 230,
          :phase => 3.4
        }
      ]
    },
    # <<< UNDERWATER
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
          :y => 40.89,
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
          :y => 84.44,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 3
        }
      },
      :layers => [
        {
          :bitmap => "pf_wasteland_pools",
          :hd => true,
          :x => 56.89,
          :y => 109.33,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 30,
          :max => 110,
          :period => 100
        },
        {
          :bitmap => "pf_wasteland_flame",
          :hd => true,
          :x => 318.22,
          :y => 132.44,
          :ox => 13,
          :oy => 44,
          :z => 2,
          :frames => 4,
          :frame_time => 5,
          :zoom => 1.2
        },
        {
          :bitmap => "pf_wasteland_fireglow",
          :hd => true,
          :x => 279.56,
          :y => 94.67,
          :ox => 0,
          :oy => 0,
          :z => 2,
          :blend => 1,
          :anim => [:pulse, :flicker],
          :min => 90,
          :max => 170,
          :period => 30,
          :chance => 0.02,
          :dropout => 2
        }
      ],
      :fx => [
        {
          :type => :rise,
          :count => 5,
          :shape => :puff,
          :size => 20,
          :colors => [
            [90, 86, 84],
            [70, 68, 70],
            [110, 104, 98]
          ],
          :area => [141.7, 18.9, 151.7, 128.9],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [50, 100],
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
          :area => [60, 110, 330, 200],
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
    # >>> WATER_SURFACE
    :WATER_SURFACE => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_water_surface_glints",
          :scrolling => true,
          :speed => 0.5,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 104.89,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 1,
          :opacity => 150
        },
        "img002" => {
          :bitmap => "pf_water_surface_spray",
          :scrolling => true,
          :speed => 1,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 91.56,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 2
        }
      },
      :layers => [
        {
          :bitmap => "pf_water_surface_beacon",
          :hd => true,
          :x => 294.22,
          :y => 60.89,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 0,
          :max => 255,
          :period => 80
        },
        {
          :bitmap => "pf_water_surface_buoy",
          :hd => true,
          :x => 152.44,
          :y => 146.67,
          :ox => 14,
          :oy => 32,
          :z => 2,
          :anim => [:bob, :sway],
          :amp => 2,
          :period => 90
        },
        {
          :bitmap => "pf_water_surface_buoy2",
          :hd => true,
          :x => 361.33,
          :y => 200.0,
          :ox => 14,
          :oy => 32,
          :z => 22,
          :anim => [:bob, :sway],
          :amp => 3,
          :period => 110
        },
        {
          :bitmap => "pf_water_surface_boat",
          :hd => true,
          :x => 135.56,
          :y => 140.44,
          :ox => 51,
          :oy => 86,
          :z => 2,
          :anim => [:bob, :sway],
          :amp => 2.5,
          :period => 120
        },
        {
          :bitmap => "pf_water_surface_beam",
          :hd => true,
          :x => 305.78,
          :y => 72.44,
          :ox => 403,
          :oy => 30,
          :z => 1,
          :blend => 1,
          :anim => :sway,
          :amp => 26,
          :period => 320,
          :opacity => 170
        }
      ],
      :fx => [
        {
          :type => :twinkle,
          :count => 14,
          :shape => :spark,
          :size => 5,
          :colors => [
            [255, 255, 255]
          ],
          :area => [0, 110, 384, 300],
          :speed => [2, 5],
          :zoom => [0.5, 0.9],
          :opacity => [160, 255],
          :layers => [:back, :mid],
          :blend => 1
        },
        {
          :type => :drift,
          :count => 6,
          :shape => :rect,
          :w => 5,
          :h => 2,
          :colors => [
            [250, 250, 250]
          ],
          :area => [0, 20, 384, 100],
          :dir => -1,
          :speed => [0.6, 1.0],
          :sway => 8,
          :zoom => [0.6, 1.0],
          :opacity => [180, 240],
          :layers => [:back]
        }
      ]
    },
    # <<< WATER_SURFACE
    # >>> WILDFIRE
    :WILDFIRE => {
      :art_extras => {
        "img001" => {
          :bitmap => "pf_wildfire_smoke",
          :scrolling => true,
          :speed => 1,
          :direction => -1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 66.67,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 3
        },
        "img002" => {
          :bitmap => "pf_wildfire_heat",
          :scrolling => true,
          :speed => 1,
          :direction => 1,
          :flat => true,
          :ox => 0,
          :oy => 0,
          :x => 0,
          :y => 146.67,
          :zoom_x => 0.444444444,
          :zoom_y => 0.444444444,
          :z => 4
        }
      },
      :layers => [
        {
          :bitmap => "pf_wildfire_blaze",
          :hd => true,
          :x => 0.0,
          :y => 0.0,
          :ox => 0,
          :oy => 0,
          :z => 1,
          :blend => 1,
          :anim => :pulse,
          :min => 80,
          :max => 190,
          :period => 50
        },
        {
          :bitmap => "pf_wildfire_flame",
          :hd => true,
          :x => 93.33,
          :y => 111.11,
          :ox => 13,
          :oy => 44,
          :z => 1,
          :frames => 4,
          :frame_time => 4,
          :zoom => 1.6
        },
        {
          :bitmap => "pf_wildfire_flame",
          :hd => true,
          :x => 133.33,
          :y => 95.11,
          :ox => 13,
          :oy => 44,
          :z => 1,
          :frames => 4,
          :frame_time => 5,
          :zoom => 1.2
        },
        {
          :bitmap => "pf_wildfire_flame",
          :hd => true,
          :x => 168.89,
          :y => 104.89,
          :ox => 13,
          :oy => 44,
          :z => 1,
          :frames => 4,
          :frame_time => 6,
          :zoom => 1.0
        },
        {
          :bitmap => "pf_wildfire_flame",
          :hd => true,
          :x => 284.44,
          :y => 102.22,
          :ox => 13,
          :oy => 44,
          :z => 1,
          :frames => 4,
          :frame_time => 4,
          :zoom => 1.3
        },
        {
          :bitmap => "pf_wildfire_flame",
          :hd => true,
          :x => 320.0,
          :y => 111.11,
          :ox => 13,
          :oy => 44,
          :z => 1,
          :frames => 4,
          :frame_time => 5,
          :zoom => 1.7
        },
        {
          :bitmap => "pf_wildfire_flame",
          :hd => true,
          :x => 248.89,
          :y => 95.11,
          :ox => 13,
          :oy => 44,
          :z => 1,
          :frames => 4,
          :frame_time => 6,
          :zoom => 0.9
        },
        {
          :bitmap => "pf_wildfire_flame",
          :hd => true,
          :x => 53.33,
          :y => 213.33,
          :ox => 13,
          :oy => 44,
          :z => 22,
          :frames => 4,
          :frame_time => 4,
          :zoom => 2.4
        },
        {
          :bitmap => "pf_wildfire_flame",
          :hd => true,
          :x => 368.89,
          :y => 231.11,
          :ox => 13,
          :oy => 44,
          :z => 22,
          :frames => 4,
          :frame_time => 5,
          :zoom => 2.6
        },
        {
          :bitmap => "pf_wildfire_flame",
          :hd => true,
          :x => 111.11,
          :y => 146.67,
          :ox => 13,
          :oy => 44,
          :z => 2,
          :frames => 4,
          :frame_time => 6,
          :zoom => 1.0
        },
        {
          :bitmap => "pf_wildfire_flame",
          :hd => true,
          :x => 337.78,
          :y => 146.67,
          :ox => 13,
          :oy => 44,
          :z => 2,
          :frames => 4,
          :frame_time => 4,
          :zoom => 1.1
        }
      ],
      :fx => [
        {
          :type => :rise,
          :count => 34,
          :shape => :glow,
          :size => 5,
          :colors => [
            [255, 150, 50],
            [255, 100, 30],
            [255, 210, 90]
          ],
          :speed => [1.0, 2.4],
          :sway => 12,
          :zoom => [0.3, 0.7],
          :opacity => [180, 255],
          :layers => [:back, :mid, :front],
          :blend => 1
        },
        {
          :type => :fall,
          :count => 12,
          :shape => :dot,
          :size => 3,
          :colors => [
            [110, 110, 110],
            [150, 140, 130],
            [80, 80, 85]
          ],
          :speed => [0.4, 0.9],
          :sway => 14,
          :zoom => [0.4, 0.7],
          :opacity => [110, 180],
          :layers => [:back, :mid]
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 26,
          :colors => [
            [90, 86, 84],
            [70, 68, 70],
            [110, 104, 98]
          ],
          :area => [110.6, -17.8, 120.6, 102.2],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [70, 120],
          :layers => [:back],
          :blend => 0
        },
        {
          :type => :rise,
          :count => 6,
          :shape => :puff,
          :size => 26,
          :colors => [
            [90, 86, 84],
            [70, 68, 70],
            [110, 104, 98]
          ],
          :area => [306.1, -17.8, 316.1, 102.2],
          :speed => [0.25, 0.5],
          :sway => 6,
          :zoom => [0.5, 0.8],
          :grow => 1.6,
          :opacity => [70, 120],
          :layers => [:back],
          :blend => 0
        }
      ],
      :stages => {
        2 => {
          :art_extras => {
            "img001" => {
              :bitmap => "pf_wildfire_embers_smoke",
              :scrolling => true,
              :speed => 0.5,
              :direction => -1,
              :flat => true,
              :ox => 0,
              :oy => 0,
              :x => 0,
              :y => 84.44,
              :zoom_x => 0.444444444,
              :zoom_y => 0.444444444,
              :z => 3
            }
          },
          :layers => [
            {
              :bitmap => "pf_wildfire_embers_beds",
              :hd => true,
              :x => 42.22,
              :y => 152.44,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 90,
              :max => 230,
              :period => 90
            },
            {
              :bitmap => "pf_wildfire_embers_rims",
              :hd => true,
              :x => 0.0,
              :y => 0.0,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 50,
              :max => 190,
              :period => 140,
              :phase => 2.0
            },
            {
              :bitmap => "pf_wildfire_embers_warmth",
              :hd => true,
              :x => 60.44,
              :y => 199.56,
              :ox => 0,
              :oy => 0,
              :z => 1,
              :blend => 1,
              :anim => :pulse,
              :min => 40,
              :max => 110,
              :period => 160
            }
          ],
          :fx => [
            {
              :type => :rise,
              :count => 30,
              :shape => :glow,
              :size => 4,
              :colors => [
                [255, 150, 50],
                [255, 100, 30],
                [255, 210, 90]
              ],
              :speed => [0.5, 1.4],
              :sway => 12,
              :zoom => [0.3, 0.7],
              :opacity => [170, 255],
              :layers => [:back, :mid, :front],
              :blend => 1
            },
            {
              :type => :twinkle,
              :count => 12,
              :shape => :spark,
              :size => 5,
              :colors => [
                [255, 200, 100],
                [255, 240, 180]
              ],
              :area => [40, 140, 350, 308],
              :speed => [4, 8],
              :zoom => [0.4, 0.8],
              :opacity => [170, 255],
              :layers => [:back, :mid],
              :blend => 1
            },
            {
              :type => :fall,
              :count => 8,
              :shape => :dot,
              :size => 3,
              :colors => [
                [110, 110, 110],
                [150, 140, 130],
                [80, 80, 85]
              ],
              :speed => [0.3, 0.7],
              :sway => 16,
              :zoom => [0.4, 0.7],
              :opacity => [110, 170],
              :layers => [:back, :mid]
            },
            {
              :type => :rise,
              :count => 4,
              :shape => :puff,
              :size => 22,
              :colors => [
                [170, 150, 160],
                [140, 124, 136]
              ],
              :area => [128.3, 40.0, 138.3, 160.0],
              :speed => [0.25, 0.5],
              :sway => 6,
              :zoom => [0.5, 0.8],
              :grow => 1.6,
              :opacity => [40, 80],
              :layers => [:back],
              :blend => 0
            }
          ]
        }
      }
    },
    # <<< WILDFIRE
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
