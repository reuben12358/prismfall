#===============================================================================
# Pokémon Prismfall — Rejuvenation-Style Chapter Opening Page Engine
# File: 020_ChapterOpeningCards.rb
# Target: Pokémon Essentials v21.1 / mkxp-z (drop into plugins/Prismfall Cutscenes/)
#-------------------------------------------------------------------------------
# Plays a 6.0-second cinematic Rejuvenation-grade Chapter Opening Page on the
# native 512x384 viewport:
#   - Slow Ken Burns pan & zoom over textless 512x384 chapter artwork
#   - 24 bespoke real-time chapter-specific particle emitters
#   - Sweeping dark translucent title ribbon + prismatic specular sheen
#   - Staggered serif typography reveal (Act -> Chapter Number -> Title -> Locale)
#   - Optional crystalline ME/SE chime (safe fallback if audio file not present)
#   - Clean curtain fade-in/out + optional graceful skip + photosensitive safety
#
# Quick usage from any RMXP map event or story script:
#   pbChapterOpeningCard(:CH01)
#   pbChapterOpeningCard(:PROLOGUE)
#   pbChapterOpeningCard(12)
#   pbChapterOpeningCard(:CH23, duration: 6.5, skippable: false)
#   pfm_chapter_card(:FALLMORN)
#===============================================================================

module Prismfall
  module ChapterCards
    VERSION          = "1.0.0"
    ART_SUBDIR       = "ChapterCards"
    DEFAULT_DURATION = 6.0
    VIEWPORT_Z       = 99_995
    TARGET_W         = 512
    TARGET_H         = 384
    RIBBON_H         = 96
    SKIP_GRACE_SEC   = 1.5
    SKIP_FADE_SEC    = 0.45

    # Audio cues tried in order (ME first, then SE fallback). Missing files are silently skipped.
    DEFAULT_ME_CUES = ["Chapter Card Prismatic Wipe", "BP Fanfare"].freeze
    DEFAULT_SE_CUES = ["Chapter Card Prismatic Wipe", "Mining ping", "GUI trainer card open"].freeze
    RUIN_SE_CUES    = ["Glitch Tear Static", "Anim/Darkness3", "GUI trainer card open"].freeze

    # Complete 24-chapter manifest (Prologue, Chapters 1-21, Post-Game Fallmorn, Ruin Route)
    CHAPTERS = {
      :CH00 => {
        slug:     "ch00_prologue",
        num:      "PROLOGUE",
        title:    "The Last Ferry",
        act:      "ACT I · THE LAST FERRY",
        location: "Ferrow's Landing · Hallow Strait",
        particle: :fog,
        accent:   [98, 208, 220],
        accent2:  [242, 184, 102],
        cam:      [1.09, 1.02, -0.028, 0.022, 0.012, -0.008],
        ribbon_y: 244,
        ruin:     false
      },
      :CH01 => {
        slug:     "ch01_tidewatch",
        num:      "CHAPTER 1",
        title:    "Tidewatch",
        act:      "ACT I · THE LAST FERRY",
        location: "Tidewatch Headland · Elowen Coast",
        particle: :seaspray,
        accent:   [116, 212, 224],
        accent2:  [255, 214, 148],
        cam:      [1.08, 1.015, 0.025, -0.020, 0.015, -0.010],
        ribbon_y: 248,
        ruin:     false
      },
      :CH02 => {
        slug:     "ch02_curtain_call",
        num:      "CHAPTER 2",
        title:    "Curtain Call",
        act:      "ACT I · THE LAST FERRY",
        location: "The Lantern Theatre · Saltmere",
        particle: :stagedust,
        accent:   [234, 185, 103],
        accent2:  [217, 91, 108],
        cam:      [1.02, 1.095, 0.0, 0.0, 0.018, -0.015],
        ribbon_y: 248,
        ruin:     false
      },
      :CH03 => {
        slug:     "ch03_weavers_debt",
        num:      "CHAPTER 3",
        title:    "The Weaver's Debt",
        act:      "ACT I · THE LAST FERRY",
        location: "Briarwick · Gossamer Wood",
        particle: :silk,
        accent:   [156, 227, 138],
        accent2:  [255, 202, 110],
        cam:      [1.09, 1.02, -0.022, 0.024, -0.014, 0.012],
        ribbon_y: 248,
        ruin:     false
      },
      :CH04 => {
        slug:     "ch04_both_ways",
        num:      "CHAPTER 4",
        title:    "Both Ways",
        act:      "ACT I · THE LAST FERRY",
        location: "Ebbmouth Locks · River Ebb",
        particle: :stormrain,
        accent:   [110, 197, 216],
        accent2:  [154, 216, 236],
        cam:      [1.02, 1.09, 0.016, -0.016, -0.015, 0.014],
        ribbon_y: 246,
        ruin:     false
      },
      :CH05 => {
        slug:     "ch05_ten_years_of_light",
        num:      "CHAPTER 5",
        title:    "Ten Years of Light",
        act:      "ACT I · THE LAST FERRY",
        location: "Meridian Spire · Lumen City",
        particle: :neonrain,
        accent:   [92, 230, 255],
        accent2:  [210, 124, 255],
        cam:      [1.09, 1.015, 0.0, 0.0, 0.028, -0.022],
        ribbon_y: 248,
        ruin:     false
      },
      :CH06 => {
        slug:     "ch06_what_the_sand_keeps",
        num:      "CHAPTER 6",
        title:    "What the Sand Keeps",
        act:      "ACT II · IMPRINTS",
        location: "Duneholt & Ossuary · Bone Sands",
        particle: :sand,
        accent:   [240, 180, 91],
        accent2:  [255, 224, 154],
        cam:      [1.085, 1.015, 0.026, -0.024, 0.008, -0.010],
        ribbon_y: 248,
        ruin:     false
      },
      :CH07 => {
        slug:     "ch07_quiet_ward",
        num:      "CHAPTER 7",
        title:    "The Quiet Ward",
        act:      "ACT II · IMPRINTS",
        location: "Mirefen Infirmary · Nadir",
        particle: :fireflies,
        accent:   [76, 240, 224],
        accent2:  [255, 184, 92],
        cam:      [1.02, 1.085, -0.022, 0.020, 0.012, -0.010],
        ribbon_y: 248,
        ruin:     false
      },
      :CH08 => {
        slug:     "ch08_light_stone",
        num:      "CHAPTER 8",
        title:    "The Light Stone",
        act:      "ACT II · IMPRINTS",
        location: "Cindervault Caldera · Ashkaar",
        particle: :embers,
        accent:   [255, 141, 68],
        accent2:  [255, 227, 140],
        cam:      [1.09, 1.02, -0.018, 0.022, 0.022, -0.018],
        ribbon_y: 248,
        ruin:     false
      },
      :CH09 => {
        slug:     "ch09_iron_conclave",
        num:      "CHAPTER 9",
        title:    "The Iron Conclave",
        act:      "ACT II · IMPRINTS",
        location: "The Iron Pit · Ironreach",
        particle: :duskrain,
        accent:   [144, 184, 232],
        accent2:  [232, 168, 100],
        cam:      [1.02, 1.09, 0.0, 0.0, -0.024, 0.020],
        ribbon_y: 246,
        ruin:     false
      },
      :CH10 => {
        slug:     "ch10_seat_that_blooms",
        num:      "CHAPTER 10",
        title:    "The Seat That Blooms",
        act:      "ACT III · FAULT LINES",
        location: "Heartgarden & Bride Tree · Verdance",
        particle: :petals,
        accent:   [255, 180, 200],
        accent2:  [255, 224, 125],
        cam:      [1.085, 1.015, -0.024, 0.022, 0.016, -0.014],
        ribbon_y: 248,
        ruin:     false
      },
      :CH11 => {
        slug:     "ch11_the_thaw",
        num:      "CHAPTER 11",
        title:    "The Thaw",
        act:      "ACT III · FAULT LINES",
        location: "Rimeholt · Frozen Lake Rime",
        particle: :snow,
        accent:   [118, 220, 255],
        accent2:  [255, 158, 82],
        cam:      [1.09, 1.015, 0.024, -0.022, -0.010, 0.018],
        ribbon_y: 246,
        ruin:     false
      },
      :CH12 => {
        slug:     "ch12_dead_letters",
        num:      "CHAPTER 12",
        title:    "Dead Letters",
        act:      "ACT III · FAULT LINES",
        location: "Skyreach Spires · The Stormfront",
        particle: :cloudgale,
        accent:   [236, 188, 106],
        accent2:  [174, 144, 240],
        cam:      [1.09, 1.02, -0.024, 0.022, 0.016, -0.014],
        ribbon_y: 246,
        ruin:     false
      },
      :CH13 => {
        slug:     "ch13_behind_the_glass",
        num:      "CHAPTER 13",
        title:    "Behind the Glass",
        act:      "ACT III · FAULT LINES",
        location: "Glass Court · Lucent, Antumbra",
        particle: :glassshards,
        accent:   [198, 162, 255],
        accent2:  [146, 228, 255],
        cam:      [1.02, 1.09, 0.0, 0.0, -0.016, 0.016],
        ribbon_y: 248,
        ruin:     false
      },
      :CH14 => {
        slug:     "ch14_deep_seams",
        num:      "CHAPTER 14",
        title:    "The Deep Seams",
        act:      "ACT IV · THE DROWNED CROWN",
        location: "Cragholm Caverns · Ossaria",
        particle: :crystaldust,
        accent:   [98, 206, 255],
        accent2:  [255, 186, 78],
        cam:      [1.085, 1.015, -0.020, 0.022, -0.018, 0.018],
        ribbon_y: 248,
        ruin:     false
      },
      :CH15 => {
        slug:     "ch15_hollow_cathedral",
        num:      "CHAPTER 15",
        title:    "The Hollow Cathedral",
        act:      "ACT IV · THE DROWNED CROWN",
        location: "Hollow Cathedral · Gravenmoor",
        particle: :spectralmist,
        accent:   [192, 146, 248],
        accent2:  [248, 198, 114],
        cam:      [1.02, 1.09, 0.016, -0.018, 0.014, -0.014],
        ribbon_y: 248,
        ruin:     false
      },
      :CH16 => {
        slug:     "ch16_clear_air",
        num:      "CHAPTER 16",
        title:    "Clear Air",
        act:      "ACT IV · THE DROWNED CROWN",
        location: "Strade Works · Cogsworth",
        particle: :electricarcs,
        accent:   [114, 212, 255],
        accent2:  [255, 198, 92],
        cam:      [1.09, 1.02, -0.022, 0.020, 0.020, -0.018],
        ribbon_y: 248,
        ruin:     false
      },
      :CH17 => {
        slug:     "ch17_drowned_crown",
        num:      "CHAPTER 17",
        title:    "The Drowned Crown",
        act:      "ACT IV · THE DROWNED CROWN",
        location: "Sunken Sun Court · Aurelia",
        particle: :bubbles,
        accent:   [88, 232, 218],
        accent2:  [250, 206, 98],
        cam:      [1.02, 1.09, 0.0, 0.0, 0.022, -0.016],
        ribbon_y: 248,
        ruin:     false
      },
      :CH18 => {
        slug:     "ch18_once_upon_a_time",
        num:      "CHAPTER 18",
        title:    "Once Upon a Time",
        act:      "ACT V · SOVEREIGN",
        location: "Lantern-Moth Market · Gloaming",
        particle: :lanternmoths,
        accent:   [255, 206, 126],
        accent2:  [234, 152, 224],
        cam:      [1.085, 1.015, -0.018, 0.020, -0.012, 0.014],
        ribbon_y: 248,
        ruin:     false
      },
      :CH19 => {
        slug:     "ch19_last_gate",
        num:      "CHAPTER 19",
        title:    "The Last Gate",
        act:      "ACT V · SOVEREIGN",
        location: "The Glass Dunes · Bone Sands",
        particle: :warembers,
        accent:   [255, 148, 86],
        accent2:  [118, 186, 255],
        cam:      [1.09, 1.015, 0.026, -0.024, 0.010, -0.012],
        ribbon_y: 246,
        ruin:     false
      },
      :CH20 => {
        slug:     "ch20_festival_of_champions",
        num:      "CHAPTER 20",
        title:    "The Festival of Champions",
        act:      "ACT V · SOVEREIGN",
        location: "Prism Arena · Crownhaven",
        particle: :festivalmotes,
        accent:   [248, 206, 102],
        accent2:  [112, 216, 255],
        cam:      [1.09, 1.015, -0.022, 0.022, 0.014, -0.012],
        ribbon_y: 248,
        ruin:     false
      },
      :CH21 => {
        slug:     "ch21_sovereign",
        num:      "CHAPTER 21",
        title:    "Sovereign",
        act:      "ACT V · SOVEREIGN",
        location: "The Prismatic Apex · Crownhaven",
        particle: :prismrays,
        accent:   [255, 226, 134],
        accent2:  [162, 226, 255],
        cam:      [1.02, 1.095, 0.0, 0.0, 0.024, -0.022],
        ribbon_y: 248,
        ruin:     false
      },
      :CH22 => {
        slug:     "ch22_postgame_fallmorn",
        num:      "POST-GAME",
        title:    "Fallmorn",
        act:      "POST-GAME · FALLMORN",
        location: "Ferrow's Landing · Dawn Strait",
        particle: :fallmorn,
        accent:   [248, 198, 104],
        accent2:  [122, 218, 196],
        cam:      [1.085, 1.015, -0.024, 0.022, 0.010, -0.008],
        ribbon_y: 246,
        ruin:     false
      },
      :CH23 => {
        slug:     "ch23_ruin_route",
        num:      "RUIN ROUTE",
        title:    "Every Type and None",
        act:      "RUIN ROUTE · GILDED KING",
        location: "Shattered Sanctuary · AF 0",
        particle: :gildeddust,
        accent:   [255, 192, 74],
        accent2:  [255, 236, 162],
        cam:      [1.02, 1.095, 0.0, 0.0, 0.018, -0.016],
        ribbon_y: 248,
        ruin:     true
      }
    }.freeze

    ALIASES = {
      :PROLOGUE              => :CH00,
      :THE_LAST_FERRY        => :CH00,
      :TIDEWATCH             => :CH01,
      :CURTAIN_CALL          => :CH02,
      :WEAVERS_DEBT          => :CH03,
      :BOTH_WAYS             => :CH04,
      :TEN_YEARS_OF_LIGHT    => :CH05,
      :WHAT_THE_SAND_KEEPS   => :CH06,
      :QUIET_WARD            => :CH07,
      :LIGHT_STONE           => :CH08,
      :IRON_CONCLAVE         => :CH09,
      :SEAT_THAT_BLOOMS      => :CH10,
      :THE_THAW              => :CH11,
      :DEAD_LETTERS          => :CH12,
      :BEHIND_THE_GLASS      => :CH13,
      :DEEP_SEAMS            => :CH14,
      :HOLLOW_CATHEDRAL      => :CH15,
      :CLEAR_AIR             => :CH16,
      :DROWNED_CROWN         => :CH17,
      :ONCE_UPON_A_TIME      => :CH18,
      :LAST_GATE             => :CH19,
      :FESTIVAL_OF_CHAMPIONS => :CH20,
      :SOVEREIGN             => :CH21,
      :POSTGAME              => :CH22,
      :FALLMORN              => :CH22,
      :POST_GAME             => :CH22,
      :RUIN                  => :CH23,
      :RUIN_ROUTE            => :CH23,
      :EVERY_TYPE_AND_NONE   => :CH23
    }.freeze

    module_function

    def resolve_key(chapter_id)
      return format("CH%02d", chapter_id).to_sym if chapter_id.is_a?(Integer) && chapter_id.between?(0, 23)
      sym = chapter_id.to_s.strip.upcase.gsub(/[\s\-]+/, "_").to_sym
      return sym if CHAPTERS.key?(sym)
      return ALIASES[sym] if ALIASES.key?(sym)
      # Match by slug (e.g. "ch05_ten_years_of_light")
      str = chapter_id.to_s.strip.downcase.sub(/\.png\z/, "")
      found = CHAPTERS.find { |_k, v| v[:slug] == str }
      return found ? found[0] : nil
    end

    def photosensitive?
      return Prismfall::Cutscene.photosensitive? if defined?(Prismfall::Cutscene) && Prismfall::Cutscene.respond_to?(:photosensitive?)
      return false
    end

    def play(chapter_id, duration: DEFAULT_DURATION, skippable: true, play_chime: true, duck_bgm: false)
      key = resolve_key(chapter_id)
      unless key && CHAPTERS[key]
        PBDebug.log("[Prismfall::ChapterCards] Unknown chapter_id: #{chapter_id.inspect}") if defined?(PBDebug)
        return false
      end
      Player.new(CHAPTERS[key], duration: duration.to_f, skippable: skippable, play_chime: play_chime, duck_bgm: duck_bgm).run
      return true
    end

    #---------------------------------------------------------------------------
    # Lightweight deterministic particle emitter tuned per chapter
    #---------------------------------------------------------------------------
    class ParticleEmitter
      Particle = Struct.new(:x0, :y0, :vx, :vy, :size, :phase, :speed, :pick, :alpha)

      COUNTS = {
        :fog          => 28,
        :seaspray     => 48,
        :stagedust    => 54,
        :silk         => 32,
        :stormrain    => 78,
        :neonrain     => 76,
        :sand         => 68,
        :fireflies    => 46,
        :embers       => 62,
        :duskrain     => 76,
        :petals       => 54,
        :snow         => 84,
        :cloudgale    => 56,
        :glassshards  => 50,
        :crystaldust  => 54,
        :spectralmist => 38,
        :electricarcs => 52,
        :bubbles      => 56,
        :lanternmoths => 46,
        :warembers    => 72,
        :festivalmotes => 60,
        :prismrays    => 56,
        :fallmorn     => 50,
        :gildeddust   => 62
      }.freeze

      PRISM_RGB = [
        [255, 118, 126], [255, 184, 92], [255, 236, 118],
        [124, 236, 152], [96, 224, 255], [168, 146, 255], [255, 150, 222]
      ].freeze

      def initialize(type, width, height, seed = 2026)
        @type   = type
        @w      = width
        @h      = height
        rng     = Random.new(seed)
        count   = COUNTS[type] || 48
        @items  = Array.new(count) do
          Particle.new(
            rng.rand * @w,
            rng.rand * @h,
            rng.rand - 0.5,
            rng.rand,
            rng.rand,
            rng.rand * Math::PI * 2.0,
            0.45 + rng.rand * 0.95,
            rng.rand,
            0.28 + rng.rand * 0.72
          )
        end
      end

      def draw(bmp, t, photosensitive: false)
        bmp.clear
        case @type
        when :fog, :spectralmist
          draw_mist_and_wisps(bmp, t)
        when :stormrain, :neonrain, :duskrain
          draw_rain(bmp, t, photosensitive)
        when :snow, :fallmorn, :petals, :seaspray
          draw_drifting_organic(bmp, t)
        when :embers, :warembers, :bubbles, :prismrays
          draw_ascending(bmp, t)
        when :sand, :cloudgale
          draw_wind_streaks(bmp, t, photosensitive)
        when :electricarcs
          draw_electric(bmp, t, photosensitive)
        else
          # :stagedust, :silk, :fireflies, :glassshards, :crystaldust,
          # :lanternmoths, :festivalmotes, :gildeddust
          draw_luminous_motes(bmp, t)
        end
      end

      private

      def draw_dot(bmp, x, y, r, color)
        ix = x.to_i
        iy = y.to_i
        ir = [r.to_i, 1].max
        return if ix + ir < 0 || ix - ir >= @w || iy + ir < 0 || iy - ir >= @h
        bmp.fill_rect(ix - ir, iy - ir, ir * 2, ir * 2, color)
      end

      def draw_streak(bmp, x, y, dx, dy, steps, color)
        steps.times do |s|
          frac = s.to_f / [steps, 1].max
          px = (x + dx * frac).to_i
          py = (y + dy * frac).to_i
          bmp.fill_rect(px, py, 2, 2, color) if px >= 0 && px < @w && py >= 0 && py < @h
        end
      end

      def draw_mist_and_wisps(bmp, t)
        violet = (@type == :spectralmist)
        @items.each_with_index do |p, i|
          if i < 14
            x = ((p.x0 + t * (12.0 + p.speed * 14.0)) % (@w + 120.0)) - 60.0
            y = 140.0 + (p.y0 / @h) * 210.0 + Math.sin(t * 0.9 + p.phase) * 8.0
            rw = (28 + p.size * 38).to_i
            rh = (6 + p.size * 10).to_i
            col = violet ? Color.new(178, 132, 255, (28 * p.alpha).to_i) : Color.new(184, 214, 228, (24 * p.alpha).to_i)
            bmp.fill_rect((x - rw).to_i, (y - rh).to_i, rw * 2, rh * 2, col)
          else
            x = (p.x0 + Math.sin(t * 1.4 + p.phase) * 18.0) % @w
            y = (p.y0 - t * (10.0 + p.speed * 14.0)) % @h
            tw = 0.4 + 0.6 * Math.sin(t * 3.0 + p.phase)
            col = violet ? Color.new(212, 174, 255, (185 * tw * p.alpha).to_i) : Color.new(255, 206, 126, (175 * tw * p.alpha).to_i)
            draw_dot(bmp, x, y, 1 + p.size * 1.6, col)
          end
        end
      end

      def draw_rain(bmp, t, photosensitive)
        if @type == :stormrain && !photosensitive
          flash = [Math.sin(t * 1.9 + 0.4) * Math.sin(t * 7.3), 0.0].max**10
          bmp.fill_rect(0, 0, @w, @h, Color.new(190, 226, 255, (flash * 52).to_i)) if flash > 0.03
        end
        neon_cols = [[92, 234, 255], [218, 128, 255], [255, 216, 120]]
        @items.each_with_index do |p, i|
          vx = (@type == :stormrain) ? 110.0 : 52.0
          vy = (@type == :stormrain) ? 310.0 : 250.0
          x = (p.x0 - t * (vx + p.speed * 70.0)) % (@w + 40.0) - 20.0
          y = (p.y0 + t * (vy + p.speed * 140.0)) % (@h + 40.0) - 20.0
          len = 9.0 + p.size * 10.0
          col =
            if @type == :neonrain
              rgb = neon_cols[i % 3]
              Color.new(rgb[0], rgb[1], rgb[2], (115 * p.alpha).to_i)
            elsif @type == :duskrain
              Color.new(176, 210, 240, (110 * p.alpha).to_i)
            else
              Color.new(196, 228, 248, (108 * p.alpha).to_i)
            end
          draw_streak(bmp, x, y, -len * 0.28, len, 5, col)
        end
      end

      def draw_drifting_organic(bmp, t)
        @items.each do |p|
          if @type == :snow
            x = (p.x0 - t * (54.0 + p.speed * 78.0) + Math.sin(t * 2.2 + p.phase) * 12.0) % @w
            y = (p.y0 + t * (46.0 + p.speed * 72.0)) % @h
            col = (p.pick > 0.8) ? Color.new(178, 234, 255, (195 * p.alpha).to_i) : Color.new(244, 250, 255, (215 * p.alpha).to_i)
            draw_dot(bmp, x, y, 1 + p.size * 1.8, col)
          else
            x = (p.x0 + t * (22.0 + p.speed * 26.0) + Math.sin(t * 1.8 + p.phase) * 14.0) % @w
            y = (p.y0 + t * (12.0 + p.speed * 18.0) + Math.cos(t * 1.5 + p.phase) * 8.0) % @h
            col =
              case @type
              when :petals
                (p.pick > 0.45) ? Color.new(255, 198, 214, (215 * p.alpha).to_i) : Color.new(255, 236, 158, (210 * p.alpha).to_i)
              when :fallmorn
                (p.pick > 0.35) ? Color.new(248, 194, 88, (210 * p.alpha).to_i) : Color.new(255, 244, 214, (190 * p.alpha).to_i)
              else
                (p.pick > 0.45) ? Color.new(255, 248, 242, (205 * p.alpha).to_i) : Color.new(224, 250, 255, (145 * p.alpha).to_i)
              end
            draw_dot(bmp, x, y, 1.2 + p.size * 2.0, col)
          end
        end
      end

      def draw_ascending(bmp, t)
        @items.each_with_index do |p, i|
          x = (p.x0 + Math.sin(t * 1.8 + p.phase) * 16.0) % @w
          vy = (@type == :bubbles) ? (20.0 + p.speed * 34.0) : (32.0 + p.speed * 54.0)
          y = (p.y0 - t * vy) % @h
          tw = 0.45 + 0.55 * Math.sin(t * 4.5 + p.phase)
          col =
            case @type
            when :bubbles
              (p.pick > 0.25) ? Color.new(192, 248, 255, (165 * p.alpha).to_i) : Color.new(255, 230, 148, (185 * tw * p.alpha).to_i)
            when :prismrays
              rgb = PRISM_RGB[i % PRISM_RGB.length]
              Color.new(rgb[0], rgb[1], rgb[2], (215 * tw * p.alpha).to_i)
            when :warembers
              (p.pick > 0.4) ? Color.new(255, 152, 64, (225 * tw * p.alpha).to_i) : Color.new(168, 218, 255, (185 * tw * p.alpha).to_i)
            else
              (p.pick > 0.45) ? Color.new(255, 156, 56, (230 * tw * p.alpha).to_i) : Color.new(255, 232, 148, (235 * tw * p.alpha).to_i)
            end
          draw_dot(bmp, x, y, 1 + p.size * 2.0, col)
        end
      end

      def draw_wind_streaks(bmp, t, photosensitive)
        if @type == :cloudgale && !photosensitive
          flash = [Math.sin(t * 1.6 + 0.9) * Math.sin(t * 6.8), 0.0].max**12
          bmp.fill_rect(0, 0, @w, @h, Color.new(255, 232, 176, (flash * 48).to_i)) if flash > 0.03
        end
        @items.each do |p|
          x = (p.x0 - t * (92.0 + p.speed * 125.0)) % (@w + 60.0) - 30.0
          y = (p.y0 + Math.sin(t * 2.1 + p.phase) * 9.0) % @h
          len = 8.0 + p.size * 16.0
          col = (@type == :sand) ? Color.new(248, 212, 146, (105 * p.alpha).to_i) : Color.new(242, 224, 255, (112 * p.alpha).to_i)
          draw_streak(bmp, x, y, len, -len * 0.14, 5, col)
        end
      end

      def draw_electric(bmp, t, photosensitive)
        @items.each_with_index do |p, i|
          if i < 10 && !photosensitive
            pulse = [Math.sin(t * 6.5 + p.phase) * Math.sin(t * 11.2 + i), 0.0].max**6
            if pulse > 0.25
              x = 180.0 + (p.x0 / @w) * 230.0
              y = 18.0 + (p.y0 / @h) * 140.0
              col = (i.even?) ? Color.new(124, 228, 255, (215 * pulse).to_i) : Color.new(255, 228, 134, (200 * pulse).to_i)
              draw_streak(bmp, x, y, (p.vx * 36.0), 16.0 + p.size * 18.0, 6, col)
            end
          else
            x = (p.x0 + Math.sin(t * 1.4 + p.phase) * 14.0) % @w
            y = (p.y0 - t * (20.0 + p.speed * 26.0)) % @h
            tw = 0.4 + 0.6 * Math.sin(t * 5.0 + p.phase)
            col = (p.pick > 0.5) ? Color.new(120, 224, 255, (195 * tw * p.alpha).to_i) : Color.new(255, 214, 118, (185 * tw * p.alpha).to_i)
            draw_dot(bmp, x, y, 1 + p.size * 1.6, col)
          end
        end
      end

      def draw_luminous_motes(bmp, t)
        @items.each_with_index do |p, i|
          x = (p.x0 + Math.sin(t * 1.15 + p.phase) * 20.0 + t * (p.vx * 12.0)) % @w
          y = (p.y0 - t * (7.0 + p.speed * 11.0) + Math.cos(t * 1.3 + p.phase) * 8.0) % @h
          tw = 0.3 + 0.7 * (0.5 + 0.5 * Math.sin(t * 3.4 + p.phase))
          col =
            case @type
            when :fireflies
              (p.pick > 0.36) ? Color.new(82, 248, 240, (225 * tw * p.alpha).to_i) : Color.new(255, 206, 112, (215 * tw * p.alpha).to_i)
            when :crystaldust
              (p.pick > 0.48) ? Color.new(96, 214, 255, (225 * tw * p.alpha).to_i) : Color.new(255, 198, 86, (225 * tw * p.alpha).to_i)
            when :glassshards
              (p.pick > 0.5) ? Color.new(212, 188, 255, (215 * tw * p.alpha).to_i) : Color.new(184, 240, 255, (215 * tw * p.alpha).to_i)
            when :lanternmoths
              (p.pick > 0.3) ? Color.new(255, 224, 134, (235 * tw * p.alpha).to_i) : Color.new(255, 184, 208, (215 * tw * p.alpha).to_i)
            when :festivalmotes
              rgb = PRISM_RGB[i % PRISM_RGB.length]
              Color.new(rgb[0], rgb[1], rgb[2], (210 * tw * p.alpha).to_i)
            when :gildeddust
              (p.pick > 0.25) ? Color.new(255, 206, 86, (235 * tw * p.alpha).to_i) : Color.new(255, 244, 196, (220 * tw * p.alpha).to_i)
            when :silk
              (p.pick > 0.45) ? Color.new(236, 255, 246, (190 * tw * p.alpha).to_i) : Color.new(255, 222, 116, (215 * tw * p.alpha).to_i)
            else
              Color.new(255, 226, 146, (215 * tw * p.alpha).to_i)
            end
          draw_dot(bmp, x, y, 1.0 + p.size * 2.0, col)
        end
      end
    end

    #---------------------------------------------------------------------------
    # Self-contained animated Rejuvenation Chapter Opening Page player
    #---------------------------------------------------------------------------
    class Player
      def initialize(cfg, duration:, skippable:, play_chime:, duck_bgm:)
        @cfg        = cfg
        @duration   = [duration, 2.5].max
        @skippable  = skippable
        @play_chime = play_chime
        @duck_bgm   = duck_bgm
        @sprites    = {}
        @owned_bmps = []
      end

      def run
        @w = Graphics.respond_to?(:width) ? Graphics.width : TARGET_W
        @h = Graphics.respond_to?(:height) ? Graphics.height : TARGET_H
        @vp = Viewport.new(0, 0, @w, @h)
        @vp.z = VIEWPORT_Z

        build_layers
        @emitter = ParticleEmitter.new(@cfg[:particle], @w, @h, @cfg[:slug].hash.abs)

        elapsed       = 0.0
        chime_fired   = false
        skipping_at   = nil
        last_time     = Time.now
        photosafe     = ChapterCards.photosensitive?
        fx_accum      = 0.0

        saved_bgm_vol = nil
        if @duck_bgm && defined?($game_system) && $game_system.respond_to?(:bgm_memorize)
          $game_system.bgm_memorize
          pbBGMFade(0.5) if defined?(pbBGMFade)
          saved_bgm_vol = true
        end

        loop do
          Graphics.update
          Input.update

          now = Time.now
          dt  = now - last_time
          last_time = now
          dt = 1.0 / 60.0 if dt <= 0.0
          dt = 0.05 if dt > 0.05
          elapsed += dt
          fx_accum += dt

          if @play_chime && !chime_fired && elapsed >= 0.88
            chime_fired = true
            fire_audio_chime
          end

          if @skippable && skipping_at.nil? && elapsed >= SKIP_GRACE_SEC &&
             (Input.trigger?(Input::USE) || Input.trigger?(Input::BACK))
            skipping_at = elapsed
          end

          update_camera(elapsed)
          if fx_accum >= (1.0 / 30.0)
            fx_accum = 0.0
            @emitter.draw(@sprites[:fx].bitmap, elapsed, photosensitive: photosafe)
          end
          update_letterbox(elapsed)
          update_ribbon_and_text(elapsed)
          done = update_curtain(elapsed, skipping_at)
          break if done
        end

        if saved_bgm_vol && defined?($game_system) && $game_system.respond_to?(:bgm_restore)
          $game_system.bgm_restore
        end
      ensure
        dispose_all
      end

      private

      def clamp(v, lo, hi)
        return lo if v < lo
        return hi if v > hi
        v
      end

      def lerp(a, b, t)
        a + (b - a) * t
      end

      def smoothstep(e0, e1, x)
        t = clamp((x - e0) / (e1 - e0).to_f, 0.0, 1.0)
        t * t * (3.0 - 2.0 * t)
      end

      def ease_out_cubic(t)
        1.0 - ((1.0 - clamp(t, 0.0, 1.0))**3)
      end

      def ease_in_out_sine(t)
        -(Math.cos(Math::PI * clamp(t, 0.0, 1.0)) - 1.0) / 2.0
      end

      def track_bmp(bmp)
        @owned_bmps << bmp
        bmp
      end

      def load_card_bitmap
        rel = "#{ART_SUBDIR}/#{@cfg[:slug]}"
        if defined?(RPG::Cache) && RPG::Cache.respond_to?(:picture)
          begin
            return [RPG::Cache.picture(rel), false]
          rescue StandardError
            # Fall through to direct path probe
          end
        end
        ["Graphics/Pictures/#{rel}.png", "graphics/Pictures/#{rel}.png"].each do |path|
          if File.exist?(path)
            return [track_bmp(Bitmap.new(path)), true]
          end
        end
        # Fallback gradient backdrop so missing art never crashes
        bmp = track_bmp(Bitmap.new(@w, @h))
        acc = @cfg[:accent]
        bmp.fill_rect(0, 0, @w, @h, Color.new(10, 14, 24))
        bmp.fill_rect(0, @h / 3, @w, @h / 3, Color.new(acc[0] / 4, acc[1] / 4, acc[2] / 4))
        [bmp, true]
      end

      def build_layers
        # 1. Backdrop artwork
        art_bmp, _owned = load_card_bitmap
        bg = Sprite.new(@vp)
        bg.bitmap = art_bmp
        bg.ox = art_bmp.width / 2.0
        bg.oy = art_bmp.height / 2.0
        bg.x  = @w / 2.0
        bg.y  = @h / 2.0
        bg.z  = 10
        @sprites[:bg] = bg

        # 2. Particle FX overlay
        fx = Sprite.new(@vp)
        fx.bitmap = track_bmp(Bitmap.new(@w, @h))
        fx.z = 20
        @sprites[:fx] = fx

        # 3. Letterbox bars
        lb = Sprite.new(@vp)
        lb.bitmap = track_bmp(Bitmap.new(@w, @h))
        lb.z = 30
        @sprites[:letterbox] = lb

        # 4. Sweeping dark translucent ribbon + metallic hairlines
        ry = (@cfg[:ribbon_y] || 246) * (@h.to_f / TARGET_H)
        @ribbon_y = ry.to_i
        rib_bmp = track_bmp(Bitmap.new(@w, RIBBON_H))
        draw_ribbon_bitmap(rib_bmp)
        rib = Sprite.new(@vp)
        rib.bitmap = rib_bmp
        rib.x = @w / 2
        rib.y = @ribbon_y
        rib.z = 40
        rib.opacity = 0
        @sprites[:ribbon] = rib

        # 4b. Specular light gleam sweeping across the ribbon
        gleam_bmp = track_bmp(Bitmap.new(120, RIBBON_H))
        acc = @cfg[:accent]
        120.times do |gx|
          dist = (gx - 60).abs / 60.0
          a = ((1.0 - dist) * (1.0 - dist) * 68).to_i
          gleam_bmp.fill_rect(gx, 2, 1, RIBBON_H - 4, Color.new(acc[0], acc[1], acc[2], a))
        end
        gleam = Sprite.new(@vp)
        gleam.bitmap = gleam_bmp
        gleam.x = -140
        gleam.y = @ribbon_y
        gleam.z = 45
        gleam.opacity = 0
        @sprites[:gleam] = gleam

        # 5. Staggered text sprites
        @sprites[:act]   = build_text_sprite(@cfg[:act], 15, Color.new(*@cfg[:accent]), bold: true, italic: false, y: @ribbon_y + 7, z: 50)
        @sprites[:num]   = build_text_sprite("—  #{@cfg[:num]}  —", 17, Color.new(244, 224, 178), bold: true, italic: false, y: @ribbon_y + 24, z: 51)
        @sprites[:title] = build_text_sprite(@cfg[:title], 30, Color.new(252, 249, 240), bold: true, italic: true, y: @ribbon_y + 42, z: 52)
        @sprites[:loc]   = build_text_sprite(@cfg[:location], 15, Color.new(204, 216, 238), bold: false, italic: false, y: @ribbon_y + 74, z: 53)

        # 6. Curtain fade overlay
        curtain = Sprite.new(@vp)
        curtain.bitmap = track_bmp(Bitmap.new(@w, @h))
        curtain.bitmap.fill_rect(0, 0, @w, @h, Color.new(4, 6, 12))
        curtain.z = 90
        curtain.opacity = 255
        @sprites[:curtain] = curtain
      end

      def draw_ribbon_bitmap(bmp)
        acc  = @cfg[:accent]
        acc2 = @cfg[:accent2]
        # Horizontal translucent dark slate gradient (feathered left/right edges)
        @w.times do |x|
          edge = [x.to_f / (@w * 0.16), (@w - 1 - x).to_f / (@w * 0.16), 1.0].min
          alpha = (95 + edge * 120).to_i
          bmp.fill_rect(x, 0, 1, RIBBON_H, Color.new(8, 11, 22, alpha))

          # Top & bottom metallic gradient hairline rules
          frac = x.to_f / [@w - 1, 1].max
          r = lerp(acc[0], acc2[0], frac).to_i
          g = lerp(acc[1], acc2[1], frac).to_i
          b = lerp(acc[2], acc2[2], frac).to_i
          line_a = (edge * 225).to_i
          lcol = Color.new(r, g, b, line_a)
          bmp.fill_rect(x, 0, 1, 2, lcol)
          bmp.fill_rect(x, RIBBON_H - 2, 1, 2, lcol)
        end
        # Central diamond crests on top and bottom hairlines
        cx = @w / 2
        white = Color.new(255, 248, 232, 245)
        [1, RIBBON_H - 2].each do |cy|
          bmp.fill_rect(cx - 2, cy - 1, 5, 3, white)
          bmp.fill_rect(cx - 1, cy - 2, 3, 5, white)
        end
      end

      def build_text_sprite(text, size, color, bold:, italic:, y:, z:)
        sp = Sprite.new(@vp)
        bmp = track_bmp(Bitmap.new(@w, 42))
        pbSetSystemFont(bmp) if defined?(pbSetSystemFont)
        bmp.font.name   = ["Georgia", "Liberation Serif", "Times New Roman", "Power Green"] if bmp.font.respond_to?(:name=)
        bmp.font.size   = size
        bmp.font.bold   = bold
        bmp.font.italic = italic
        shadow = Color.new(6, 8, 14, 225)
        bmp.font.color = shadow
        [[-1, 0], [1, 0], [0, -1], [0, 1], [1, 2]].each do |dx, dy|
          bmp.draw_text(dx, dy, @w, 40, text, 1)
        end
        bmp.font.color = color
        bmp.draw_text(0, 0, @w, 40, text, 1)
        sp.bitmap  = bmp
        sp.x       = 0
        sp.y       = y
        sp.z       = z
        sp.opacity = 0
        sp
      end

      def update_camera(t)
        p = ease_in_out_sine(t / @duration)
        z0, z1, x0, x1, y0, y1 = @cfg[:cam]
        bg = @sprites[:bg]
        base_scale = [@w.to_f / bg.bitmap.width, @h.to_f / bg.bitmap.height].max
        zoom = lerp(z0, z1, p) * base_scale
        bg.zoom_x = zoom
        bg.zoom_y = zoom
        bg.x = (@w * 0.5) + lerp(x0, x1, p) * @w
        bg.y = (@h * 0.5) + lerp(y0, y1, p) * @h
      end

      def update_letterbox(t)
        lb = @sprites[:letterbox]
        lb.bitmap.clear
        open_p  = smoothstep(0.0, 0.85, t)
        close_p = smoothstep(@duration - 0.75, @duration, t)
        bar_h   = (lerp(28.0, 12.0, open_p) + close_p * 22.0).to_i
        col     = Color.new(4, 6, 12, 236)
        lb.bitmap.fill_rect(0, 0, @w, bar_h, col)
        lb.bitmap.fill_rect(0, @h - bar_h, @w, bar_h, col)
      end

      def update_ribbon_and_text(t)
        out_fade = 1.0 - smoothstep(@duration - 0.85, @duration - 0.15, t)
        rib_p = ease_out_cubic((t - 0.88) / 0.72)
        rib = @sprites[:ribbon]
        half_w = ((@w * 0.5) * rib_p).to_i
        if half_w > 0
          left = (@w / 2) - half_w
          rib.src_rect.set(left, 0, half_w * 2, RIBBON_H)
          rib.x = left
          rib.opacity = (255 * out_fade).to_i
        else
          rib.opacity = 0
        end

        # Sweeping light gleam across ribbon (1.25s -> 2.30s)
        gleam_t = clamp((t - 1.25) / 1.05, 0.0, 1.0)
        gleam = @sprites[:gleam]
        if gleam_t > 0.0 && gleam_t < 1.0
          gleam.x = lerp(-120.0, @w + 40.0, ease_in_out_sine(gleam_t)).to_i
          gleam.opacity = (Math.sin(gleam_t * Math::PI) * 235 * out_fade).to_i
        else
          gleam.opacity = 0
        end

        # Staggered serif text reveals
        animate_text(@sprites[:act],   @ribbon_y + 7,  t, 1.35, 1.88, 5, out_fade)
        animate_text(@sprites[:num],   @ribbon_y + 24, t, 1.65, 2.20, 6, out_fade)
        animate_text(@sprites[:title], @ribbon_y + 42, t, 2.00, 2.68, 9, out_fade)
        animate_text(@sprites[:loc],   @ribbon_y + 74, t, 2.52, 3.12, 4, out_fade)
      end

      def animate_text(sprite, target_y, t, t0, t1, slide_px, out_fade)
        a = smoothstep(t0, t1, t) * out_fade
        e = ease_out_cubic((t - t0) / [t1 - t0, 0.01].max)
        sprite.y       = (target_y + (1.0 - e) * slide_px).to_i
        sprite.opacity = (a * 255).to_i
      end

      def update_curtain(t, skipping_at)
        fade_in  = 1.0 - smoothstep(0.0, 0.72, t)
        fade_out = smoothstep(@duration - 0.72, @duration, t)
        if skipping_at
          skip_fade = smoothstep(skipping_at, skipping_at + SKIP_FADE_SEC, t)
          fade_out = [fade_out, skip_fade].max
          @sprites[:curtain].opacity = ([fade_in, fade_out].max * 255).to_i
          return (t >= skipping_at + SKIP_FADE_SEC)
        end
        @sprites[:curtain].opacity = ([fade_in, fade_out].max * 255).to_i
        return (t >= @duration)
      end

      def fire_audio_chime
        if @cfg[:ruin]
          try_play_se(RUIN_SE_CUES)
          return
        end
        return if try_play_me(DEFAULT_ME_CUES)
        try_play_se(DEFAULT_SE_CUES)
      end

      def try_play_me(list)
        return false unless defined?(pbMEPlay)
        list.each do |name|
          if !defined?(pbResolveAudioME) || pbResolveAudioME(name)
            pbMEPlay(name, 85, 100)
            return true
          end
        end
        false
      rescue StandardError
        false
      end

      def try_play_se(list)
        return false unless defined?(pbSEPlay)
        list.each do |name|
          if !defined?(pbResolveAudioSE) || pbResolveAudioSE(name)
            pbSEPlay(name, 85, 100)
            return true
          end
        end
        false
      rescue StandardError
        false
      end

      def dispose_all
        @sprites.each_value { |sp| sp.dispose if sp && !sp.disposed? }
        @sprites.clear
        @owned_bmps.each { |b| b.dispose if b && !b.disposed? }
        @owned_bmps.clear
        @vp.dispose if @vp && !@vp.disposed?
        @vp = nil
      end
    end
  end
end

#===============================================================================
# Global Essentials v21.1 Event Script Helpers
#===============================================================================
def pbChapterOpeningCard(chapter_id, duration: Prismfall::ChapterCards::DEFAULT_DURATION,
                         skippable: true, play_chime: true, duck_bgm: false)
  Prismfall::ChapterCards.play(
    chapter_id,
    duration:   duration,
    skippable:  skippable,
    play_chime: play_chime,
    duck_bgm:   duck_bgm
  )
end

def pfm_chapter_card(chapter_id, **opts)
  pbChapterOpeningCard(chapter_id, **opts)
end

#===============================================================================
# Optional Essentials v21.1 F9 Debug Menu Previewer (all 24 chapters)
#===============================================================================
if defined?(MenuHandlers)
  MenuHandlers.add(:debug_menu, :prismfall_chapter_cards, {
    "name"        => _INTL("Chapter Opening Cards (24)"),
    "parent"      => :playtest_menu,
    "description" => _INTL("Preview any of the 24 Rejuvenation-style Chapter Opening Pages."),
    "effect"      => proc {
      keys = Prismfall::ChapterCards::CHAPTERS.keys
      cmds = keys.map do |k|
        c = Prismfall::ChapterCards::CHAPTERS[k]
        "#{c[:num]}: #{c[:title]}"
      end
      cmd = 0
      loop do
        cmd = pbShowCommands(nil, cmds, -1, cmd)
        break if cmd < 0
        pbChapterOpeningCard(keys[cmd])
      end
    }
  })
end
