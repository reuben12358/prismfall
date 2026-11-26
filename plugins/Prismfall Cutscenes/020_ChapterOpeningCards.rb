#===============================================================================
# Prismfall Cutscenes - 020 Chapter opening cards
# (Gemini spec 2026-11-24_rejuv-chapter-opening-cards: the 24 paintings, the
#  manifest and the particle emitter are Gemini's; the player, the once-a-chapter
#  flag and the V102 hook were reworked on install, see gemini_recommends/REVIEW.md)
#-------------------------------------------------------------------------------
# A six-second opening page for a chapter: the chapter's painting
# (Graphics/Pictures/ChapterCards/<slug>.png, 512x384, no text) under a slow
# pan, drifting particles, a dark ribbon, and "ACT / CHAPTER n / Title / place"
# coming in one line at a time. USE or BACK skips it after 1.5 s.
#
#   pf_chapter_card                 the card of the current chapter (V102), once a save
#   pf_chapter_card(12)             chapter 12's card, once a save
#   pf_chapter_card(:RUIN)          :PROLOGUE, :FALLMORN, :CH07, "ch05_ten_years_of_light", ...
#   pf_chapter_card(5, force: true) again, even if it has been shown
#   pbChapterOpeningCard(id, duration: 6.0, skippable: true, play_chime: true, duck_bgm: false)
#                                   Gemini's call: always plays, never marks the chapter as shown
#
# Automatic: when V102 STORY_CHAPTER is set by a map event, the card of that
# chapter plays there and then, once a save (the list is saved in
# $PokemonGlobal). Set from anywhere else (a battle, the debug menu) it waits
# until the player is standing free on the map. V102 0-21 are the Prologue and
# Chapters 1-21; 23 (post-game) is "Fallmorn"; 22 (the epilogue) has no card.
# The Ruin Route does not move V102: call pf_chapter_card(:RUIN) where it begins.
#   Prismfall::ChapterCards.auto = false    turns the automatic card off
# (it is off by default under the capture harness, ENV["DEMO_PLAN"]).
#
# Photosensitive mode (Prismfall::Cutscene.photosensitive?): no lightning or arc
# flashes in the particles; everything else is slow fades.
#===============================================================================
module Prismfall
  module ChapterCards
    C                = Prismfall::Cutscene
    ART_FOLDER       = "Graphics/Pictures/ChapterCards/"
    DEFAULT_DURATION = 6.0
    VIEWPORT_Z       = 100_000      # above message boxes and the black of a screen fade
    TARGET_W         = 512
    TARGET_H         = 384
    RIBBON_H         = 110   # [PF] was 96: the bottom rule struck through the location line (Gemini QA 2026-11-26)
    # Where each text line's middle sits, in pixels below the ribbon's top rule. text_sprite centres the drawn glyphs
    # on these, so they land in the same place whether the engine's draw_text centres text in its rect or puts it at
    # the top: in the Linux mkxp-z capture the old 40 px rects were top-aligned, so the act line sat on the top rule
    # and the location floated mid-ribbon (2026-11-26 capture).
    TEXT_MID         = { :act => 16, :num => 34, :title => 59, :loc => 87 }
    LEAD_SEC         = 0.30         # the map fades to black before the painting, and back after
    SKIP_GRACE_SEC   = 1.5
    SKIP_FADE_SEC    = 0.45
    CHAPTER_VAR      = 102          # V102 STORY_CHAPTER (design/FLAGS.md)
    POSTGAME_VALUE   = 23           # V102 in the post-game -> :CH22 "Fallmorn"

    CHIME_SE      = "Chapter Card Prismatic Wipe"     # audio/gemini_cc0/SE; silent when not installed
    RUIN_CHIME_SE = "Glitch Tear Static"

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

    @auto = nil
    @pending = nil
    @playing = false

    class << self
      attr_reader :pending

      def auto=(v); @auto = v; end

      def auto?
        return @auto if !@auto.nil?
        return ENV["DEMO_PLAN"].to_s.empty?
      end

      def playing?; return @playing; end

      def resolve_key(chapter_id)
        return format("CH%02d", chapter_id).to_sym if chapter_id.is_a?(Integer) && chapter_id.between?(0, 23)
        sym = chapter_id.to_s.strip.upcase.gsub(/[\s\-]+/, "_").to_sym
        return sym if CHAPTERS.has_key?(sym)
        return ALIASES[sym] if ALIASES.has_key?(sym)
        str = chapter_id.to_s.strip.downcase.sub(/\.png\z/, "")
        found = CHAPTERS.find { |_k, v| v[:slug] == str }
        return (found) ? found[0] : nil
      end

      # The card for a value of V102, or nil.
      def key_for_chapter(value)
        return nil if !value.is_a?(Integer)
        return format("CH%02d", value).to_sym if value.between?(0, 21)
        return :CH22 if value == POSTGAME_VALUE
        return nil
      end

      def photosensitive?
        return C.photosensitive? if C.respond_to?(:photosensitive?)
        return false
      end

      # Cards already shown in this save.
      def seen
        return (@seen_fallback ||= []) if !defined?($PokemonGlobal) || !$PokemonGlobal || !$PokemonGlobal.respond_to?(:pf_chapter_cards)
        return $PokemonGlobal.pf_chapter_cards
      end

      def seen?(id); key = resolve_key(id); return key ? seen.include?(key) : false; end

      def mark_seen(id)
        key = resolve_key(id)
        seen.push(key) if key && !seen.include?(key)
        return key
      end

      # Always plays. -> true when a card was shown
      def play(chapter_id, duration: DEFAULT_DURATION, skippable: true, play_chime: true, duck_bgm: false)
        key = resolve_key(chapter_id)
        if !key
          C::Util.log("chapter card: unknown chapter #{chapter_id.inspect}")
          return false
        end
        return false if @playing
        @playing = true
        begin
          Player.new(CHAPTERS[key], duration: duration.to_f, skippable: skippable, play_chime: play_chime, duck_bgm: duck_bgm).run
        ensure
          @playing = false
        end
        return true
      rescue StandardError => e
        C::Util.log("chapter card #{chapter_id.inspect} failed: #{e.class}: #{e.message}")
        raise if C.raise_errors
        return false
      end

      # Once a save (unless force:). id nil = the current chapter. -> true when shown
      def show_once(id = nil, force: false, **opts)
        id = key_for_chapter($game_variables[CHAPTER_VAR]) if id.nil? && defined?($game_variables) && $game_variables
        key = resolve_key(id)
        return false if !key
        return false if !force && seen.include?(key)
        mark_seen(key)
        @pending = nil if @pending == key
        return play(key, **opts)
      end

      # A blocking card can be shown right now: on the map, no battle, no message box up.
      def clear_to_play?
        return false if @playing
        return false if !defined?(Scene_Map) || !defined?($scene) || !$scene.is_a?(Scene_Map)
        return false if !defined?($game_temp) || !$game_temp
        return false if $game_temp.respond_to?(:in_battle) && $game_temp.in_battle
        return false if $game_temp.respond_to?(:message_window_showing) && $game_temp.message_window_showing
        return false if $game_temp.respond_to?(:in_menu) && $game_temp.in_menu
        return true
      end

      # V102 was just set to `value`.
      def chapter_changed(value)
        return if !auto?
        key = key_for_chapter(value)
        return if !key || seen.include?(key)
        if clear_to_play? && defined?(pbMapInterpreterRunning?) && pbMapInterpreterRunning?
          show_once(key)                  # set by a map event: the card belongs right here
        else
          @pending = key                  # set from somewhere else: wait for the map to be free
        end
      end

      # Scene_Map#update: a card that was waiting.
      def update_pending
        return if !@pending
        if !auto? || seen.include?(@pending)
          @pending = nil
          return
        end
        return if !clear_to_play?
        return if defined?(pbMapInterpreterRunning?) && pbMapInterpreterRunning?
        return if $game_temp.respond_to?(:player_transferring) && $game_temp.player_transferring
        return if defined?($game_player) && $game_player && $game_player.respond_to?(:moving?) && $game_player.moving?
        show_once(@pending)
      end
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
    # The card itself
    #---------------------------------------------------------------------------
    class Player
      def initialize(cfg, duration:, skippable:, play_chime:, duck_bgm:)
        @cfg        = cfg
        @duration   = [duration, 2.5].max
        @skippable  = skippable
        @play_chime = play_chime
        @duck_bgm   = duck_bgm
        @sprites    = {}
        @bitmaps    = []
      end

      def run
        @w = Graphics.width
        @h = Graphics.height
        @vp = Viewport.new(0, 0, @w, @h)
        @vp.z = VIEWPORT_Z
        build_layers
        @emitter = ParticleEmitter.new(@cfg[:particle], @w, @h, @cfg[:slug].sum)
        photosafe = ChapterCards.photosensitive?
        ducked = false
        if @duck_bgm && defined?($game_system) && $game_system && $game_system.respond_to?(:bgm_memorize)
          $game_system.bgm_memorize
          pbBGMFade(0.5) if defined?(pbBGMFade)
          ducked = true
        end
        start = C::Util.now
        chimed = false
        skip_at = nil
        fx_at = -1.0
        loop do
          Graphics.update
          Input.update
          t = C::Util.now - start - LEAD_SEC          # < 0: the map is still fading to black
          if t < 0
            @sprites[:curtain].opacity = (255 * (1.0 + (t / LEAD_SEC))).round
            next
          end
          show_layers if !@shown
          if @play_chime && !chimed && t >= 0.88
            chimed = true
            C::Sound.play(:se, (@cfg[:ruin]) ? RUIN_CHIME_SE : CHIME_SE, 85, 100)
          end
          if @skippable && skip_at.nil? && t >= SKIP_GRACE_SEC && t < @duration - 0.72 &&
             (Input.trigger?(Input::USE) || Input.trigger?(Input::BACK))
            skip_at = t
          end
          update_camera(t)
          if t - fx_at >= (1.0 / 30.0)                 # particles at 30 fps
            fx_at = t
            @emitter.draw(@sprites[:fx].bitmap, t, photosensitive: photosafe)
          end
          update_letterbox(t)
          update_ribbon_and_text(t)
          break if update_curtain(t, skip_at)
        end
        hide_layers                                    # black; now let the map back in
        out = C::Util.now
        loop do
          Graphics.update
          Input.update
          k = (C::Util.now - out) / LEAD_SEC
          break if k >= 1.0
          @sprites[:curtain].opacity = (255 * (1.0 - k)).round
        end
        $game_system.bgm_restore if ducked && $game_system.respond_to?(:bgm_restore)
      ensure
        dispose_all
      end

      private

      def clamp(v, lo, hi); return (v < lo) ? lo : ((v > hi) ? hi : v); end
      def lerp(a, b, t); return a + ((b - a) * t); end

      def smoothstep(e0, e1, x)
        t = clamp((x - e0) / (e1 - e0).to_f, 0.0, 1.0)
        return t * t * (3.0 - (2.0 * t))
      end

      def ease_out_cubic(t); return 1.0 - ((1.0 - clamp(t, 0.0, 1.0))**3); end
      def ease_in_out_sine(t); return -(Math.cos(Math::PI * clamp(t, 0.0, 1.0)) - 1.0) / 2.0; end

      def own(bmp)
        @bitmaps.push(bmp)
        return bmp
      end

      def sprite(key, bmp, z)
        sp = Sprite.new(@vp)
        sp.bitmap = bmp
        sp.z = z
        @sprites[key] = sp
        return sp
      end

      # The painting, or a plain two-tone backdrop when the file is missing.
      def load_art
        bmp = C::Gfx.load_bitmap(ART_FOLDER + @cfg[:slug])
        return own(bmp) if bmp
        C::Util.log("chapter card: no art #{ART_FOLDER}#{@cfg[:slug]}")
        bmp = own(Bitmap.new(@w, @h))
        acc = @cfg[:accent]
        bmp.fill_rect(0, 0, @w, @h, Color.new(10, 14, 24))
        bmp.fill_rect(0, @h / 3, @w, @h / 3, Color.new(acc[0] / 4, acc[1] / 4, acc[2] / 4))
        return bmp
      end

      def build_layers
        black = own(Bitmap.new(@w, @h))
        black.fill_rect(0, 0, @w, @h, Color.new(4, 6, 12))
        sprite(:back, black, 5)                        # nothing of the map shows at the painting's edges
        art = load_art
        bg = sprite(:bg, art, 10)
        bg.ox = art.width / 2
        bg.oy = art.height / 2
        bg.x = @w / 2
        bg.y = @h / 2
        sprite(:fx, own(Bitmap.new(@w, @h)), 20)
        sprite(:letterbox, own(Bitmap.new(@w, @h)), 30)
        @ribbon_y = ((@cfg[:ribbon_y] || 246) * @h / TARGET_H.to_f).to_i - 7
        rib_bmp = own(Bitmap.new(@w, RIBBON_H))
        draw_ribbon_bitmap(rib_bmp)
        rib = sprite(:ribbon, rib_bmp, 40)
        rib.y = @ribbon_y
        rib.opacity = 0
        gleam_bmp = own(Bitmap.new(120, RIBBON_H))
        acc = @cfg[:accent]
        120.times do |gx|
          dist = (gx - 60).abs / 60.0
          gleam_bmp.fill_rect(gx, 2, 1, RIBBON_H - 4, Color.new(acc[0], acc[1], acc[2], ((1.0 - dist) * (1.0 - dist) * 68).to_i))
        end
        gleam = sprite(:gleam, gleam_bmp, 45)
        gleam.x = -140
        gleam.y = @ribbon_y
        gleam.opacity = 0
        text_sprite(:act, @cfg[:act], 15, Color.new(*@cfg[:accent]), true, false, @ribbon_y + TEXT_MID[:act], 50)
        text_sprite(:num, "—  #{@cfg[:num]}  —", 17, Color.new(244, 224, 178), true, false, @ribbon_y + TEXT_MID[:num], 51)
        text_sprite(:title, @cfg[:title], 30, Color.new(252, 249, 240), true, true, @ribbon_y + TEXT_MID[:title], 52)
        text_sprite(:loc, @cfg[:location], 15, Color.new(204, 216, 238), false, false, @ribbon_y + TEXT_MID[:loc], 53)
        curtain = sprite(:curtain, black, 90)
        curtain.opacity = 0
        hide_layers
      end

      def layer_keys; return @sprites.keys - [:curtain]; end

      def hide_layers
        layer_keys.each { |k| @sprites[k].visible = false }
        @shown = false
      end

      def show_layers
        layer_keys.each { |k| @sprites[k].visible = true }
        @shown = true
      end

      def draw_ribbon_bitmap(bmp)
        acc  = @cfg[:accent]
        acc2 = @cfg[:accent2]
        @w.times do |x|
          edge = [x.to_f / (@w * 0.16), (@w - 1 - x).to_f / (@w * 0.16), 1.0].min
          bmp.fill_rect(x, 0, 1, RIBBON_H, Color.new(8, 11, 22, (95 + (edge * 120)).to_i))
          frac = x.to_f / [@w - 1, 1].max
          lcol = Color.new(lerp(acc[0], acc2[0], frac).to_i, lerp(acc[1], acc2[1], frac).to_i, lerp(acc[2], acc2[2], frac).to_i, (edge * 225).to_i)
          bmp.fill_rect(x, 0, 1, 2, lcol)
          bmp.fill_rect(x, RIBBON_H - 2, 1, 2, lcol)
        end
        cx = @w / 2
        white = Color.new(255, 248, 232, 245)
        [1, RIBBON_H - 2].each do |cy|
          bmp.fill_rect(cx - 2, cy - 1, 5, 3, white)
          bmp.fill_rect(cx - 1, cy - 2, 3, 5, white)
        end
      end

      # A line of text whose drawn glyphs are centred on mid_y. Engines differ in where draw_text puts a line inside
      # a taller rect (the Linux mkxp-z capture puts it at the top), so the sprite's origin comes from the pixels
      # actually drawn, not from the rect.
      def text_sprite(key, text, size, color, bold, italic, mid_y, z)
        box_h = (size * 2) + 12
        bmp = own(Bitmap.new(@w, box_h))
        style_font(bmp, size, bold, italic)
        bmp.font.color = Color.new(6, 8, 14, 225)
        [[-1, 0], [1, 0], [0, -1], [0, 1], [1, 2]].each { |dx, dy| bmp.draw_text(dx, 2 + dy, @w, box_h - 6, text, 1) }
        bmp.font.color = color
        bmp.draw_text(0, 2, @w, box_h - 6, text, 1)
        sp = sprite(key, bmp, z)
        sp.oy = ink_middle(bmp, text) || (box_h / 2)
        sp.y = mid_y
        sp.opacity = 0
        return sp
      end

      # the middle row of the drawn glyphs (nil when the engine can't read pixels back)
      def ink_middle(bmp, text)
        return nil if !bmp.respond_to?(:get_pixel)
        tw = (bmp.text_size(text.to_s).width rescue bmp.width) + 8
        x0 = [(bmp.width - tw) / 2, 0].max
        x1 = [x0 + tw, bmp.width].min
        rows = (0...bmp.height).select { |y| (x0...x1).step(2).any? { |x| bmp.get_pixel(x, y).alpha > 40 } }
        return nil if rows.empty?
        return (rows.first + rows.last) / 2
      rescue StandardError
        return nil
      end

      def style_font(bmp, size, bold, italic)
        pbSetSystemFont(bmp) if defined?(pbSetSystemFont)
        bmp.font.size = size
        bmp.font.bold = bold if bmp.font.respond_to?(:bold=)
        bmp.font.italic = italic if bmp.font.respond_to?(:italic=)
      end

      # A slow pan and zoom, never far enough to show the painting's edge.
      def update_camera(t)
        p = ease_in_out_sine(t / @duration)
        z0, z1, x0, x1, y0, y1 = @cfg[:cam]
        bg = @sprites[:bg]
        base = [@w.to_f / bg.bitmap.width, @h.to_f / bg.bitmap.height].max
        zoom = lerp(z0, z1, p) * base
        bg.zoom_x = zoom
        bg.zoom_y = zoom
        mx = [((bg.bitmap.width * zoom) - @w) / 2.0, 0.0].max
        my = [((bg.bitmap.height * zoom) - @h) / 2.0, 0.0].max
        bg.x = (@w / 2) + clamp(lerp(x0, x1, p) * @w, -mx, mx).round
        bg.y = (@h / 2) + clamp(lerp(y0, y1, p) * @h, -my, my).round
      end

      def update_letterbox(t)
        open_p  = smoothstep(0.0, 0.85, t)
        close_p = smoothstep(@duration - 0.75, @duration, t)
        bar_h   = (lerp(28.0, 12.0, open_p) + (close_p * 22.0)).to_i
        return if bar_h == @bar_h
        @bar_h = bar_h
        lb = @sprites[:letterbox].bitmap
        lb.clear
        col = Color.new(4, 6, 12, 236)
        lb.fill_rect(0, 0, @w, bar_h, col)
        lb.fill_rect(0, @h - bar_h, @w, bar_h, col)
      end

      def update_ribbon_and_text(t)
        out_fade = 1.0 - smoothstep(@duration - 0.85, @duration - 0.15, t)
        rib = @sprites[:ribbon]
        half_w = ((@w / 2) * ease_out_cubic((t - 0.88) / 0.72)).to_i
        if half_w > 0
          left = (@w / 2) - half_w
          rib.src_rect.set(left, 0, half_w * 2, RIBBON_H)
          rib.x = left
          rib.opacity = (255 * out_fade).to_i
        else
          rib.opacity = 0
        end
        gleam_t = clamp((t - 1.25) / 1.05, 0.0, 1.0)
        gleam = @sprites[:gleam]
        if gleam_t > 0.0 && gleam_t < 1.0
          gleam.x = lerp(-120.0, @w + 40.0, ease_in_out_sine(gleam_t)).to_i
          gleam.opacity = (Math.sin(gleam_t * Math::PI) * 235 * out_fade).to_i
        else
          gleam.opacity = 0
        end
        animate_text(@sprites[:act],   @ribbon_y + TEXT_MID[:act],   t, 1.35, 1.88, 5, out_fade)
        animate_text(@sprites[:num],   @ribbon_y + TEXT_MID[:num],   t, 1.65, 2.20, 6, out_fade)
        animate_text(@sprites[:title], @ribbon_y + TEXT_MID[:title], t, 2.00, 2.68, 9, out_fade)
        animate_text(@sprites[:loc],   @ribbon_y + TEXT_MID[:loc],   t, 2.52, 3.12, 4, out_fade)
      end

      def animate_text(sp, target_y, t, t0, t1, slide_px, out_fade)
        e = ease_out_cubic((t - t0) / [t1 - t0, 0.01].max)
        sp.y = (target_y + ((1.0 - e) * slide_px)).to_i
        sp.opacity = (smoothstep(t0, t1, t) * out_fade * 255).to_i
      end

      # -> true when the card is over (the curtain is fully black again)
      def update_curtain(t, skip_at)
        fade_in  = 1.0 - smoothstep(0.0, 0.72, t)
        fade_out = smoothstep(@duration - 0.72, @duration, t)
        fade_out = [fade_out, smoothstep(skip_at, skip_at + SKIP_FADE_SEC, t)].max if skip_at
        @sprites[:curtain].opacity = ([fade_in, fade_out].max * 255).to_i
        return true if skip_at && t >= skip_at + SKIP_FADE_SEC
        return t >= @duration
      end

      def dispose_all
        @sprites.each_value { |sp| sp.dispose if sp && !sp.disposed? }
        @sprites.clear
        @bitmaps.each { |b| b.dispose if b && !b.disposed? }
        @bitmaps.clear
        @vp.dispose if @vp && !@vp.disposed?
        @vp = nil
      end
    end
  end
end

#===============================================================================
# Saved with the game: the cards this save has shown.
#===============================================================================
if defined?(PokemonGlobalMetadata)
  class PokemonGlobalMetadata
    attr_writer :pf_chapter_cards

    def pf_chapter_cards; return @pf_chapter_cards ||= []; end
  end
end

# V102 STORY_CHAPTER moving on starts the new chapter's card.
if defined?(Game_Variables) && !Game_Variables.method_defined?(:prismfall_chapter_card_set)
  class Game_Variables
    alias prismfall_chapter_card_set []=

    def []=(variable_id, value)
      ret = prismfall_chapter_card_set(variable_id, value)
      Prismfall::ChapterCards.chapter_changed(value) if variable_id == Prismfall::ChapterCards::CHAPTER_VAR
      return ret
    end
  end
end

if defined?(Scene_Map) && !Scene_Map.method_defined?(:prismfall_chapter_card_update)
  class Scene_Map
    alias prismfall_chapter_card_update update

    def update
      prismfall_chapter_card_update
      Prismfall::ChapterCards.update_pending if Prismfall::ChapterCards.pending
    end
  end
end

#===============================================================================
# Event script calls
#===============================================================================
# The one call for map events and the engine: the chapter's card, once a save.
#   pf_chapter_card            the current chapter (V102)
#   pf_chapter_card(12)        pf_chapter_card(:RUIN)        pf_chapter_card(5, force: true)
def pf_chapter_card(id = nil, force: false, **opts)
  return Prismfall::ChapterCards.show_once(id, force: force, **opts)
end

def pfm_chapter_card(id = nil, **opts); return pf_chapter_card(id, **opts); end

# Gemini's name for it: always plays, does not touch the shown list.
def pbChapterOpeningCard(chapter_id, duration: Prismfall::ChapterCards::DEFAULT_DURATION,
                         skippable: true, play_chime: true, duck_bgm: false)
  return Prismfall::ChapterCards.play(chapter_id, duration: duration, skippable: skippable, play_chime: play_chime, duck_bgm: duck_bgm)
end

# Debug menu: preview any card.
if defined?(MenuHandlers)
  MenuHandlers.add(:debug_menu, :prismfall_chapter_cards, {
    "name"        => _INTL("Chapter opening cards"),
    "parent"      => :prismfall_cutscenes_menu,
    "description" => _INTL("Preview any of the 24 chapter opening cards."),
    "effect"      => proc {
      keys = Prismfall::ChapterCards::CHAPTERS.keys
      cmds = keys.map { |k| "#{Prismfall::ChapterCards::CHAPTERS[k][:num]}: #{Prismfall::ChapterCards::CHAPTERS[k][:title]}" }
      cmd = 0
      loop do
        cmd = pbShowCommands(nil, cmds, -1, cmd)
        break if cmd < 0
        pbChapterOpeningCard(keys[cmd])
      end
    }
  })
end
