#===============================================================================
# Prismfall Cutscenes - 019 Chapter 20-21 staging hooks: Larch's lamp board, the live-map letterbox, and the
# Hijack's hook points
#-------------------------------------------------------------------------------
# story/40_SCRIPT_CH21.md "The Hijack", "The allies move" and "Map and event needs (Chapter 21)":
#   "The Larch lamp board: an 11-lamp picture overlay, lit by tally(:ENGINE_BREAKS)."
#   "The allies montage: one shot per condition, a 2-second cut each (cutscene plugin)."
# The rules (which lamp, which beat, whose hand) are Core 033_Finale.rb; the pylons are mapgen/ruby/018_Crownhaven.rb.
# Everything here is drawn in code (no art file is needed) and is safe to call on an arena that is only half built:
# a missing event is skipped.
#
#   Prismfall::Cutscene.lamp_board([0, 4, 9], [4])   Larch's board, top right: lamps 0, 4 and 9 lit, lamp 4 just lit
#                                                    (it flares). Stays up across messages until lamp_board_off.
#   Prismfall::Cutscene.lamp_board_off
#   Prismfall::Cutscene.map_letterbox(true / false)  cinema bars over the live map that stay through the event's
#                                                    own messages (the scene DSL's letterbox ends with its scene)
#   pfm_cutscene ids (map events call these; each returns true):
#     :LAMP_BOARD        the board as it stands now (Core's Finale.lamps)   :LAMP_BOARD_DARK  all eleven dark
#     :LAMP_BOARD_OFF    :LETTERBOX_ON  :LETTERBOX_OFF
#     :CH20_VISION / :CH20_VISION_END   the white vision (the PC glows; white over 60 frames; white to black)
#     :HJ_RINGS   "[anim: the arena's eighteen-sided rings ignite gold, ring after ring, from the rim inward; the
#                 floor at the Ring's centre splits]"  (events "Arena ring 1".. get self switch A, outermost first)
#     :HJ_CRADLE  the golden hand rises out of the floor (event "Cradle": self switch A, fades in)
#     :HJ_LOCKS   "The Ring's pylons sprout golden locks. Eighteen."
#     :HJ_CROWN   the Crown slams into the cradle's palm (event "Crown") and the PC is dragged to their knees there
#     :HJ_DESCENT the hijacker comes down from the Meridian box (event "Voss" / "Quent" / "Aurelius" by
#                 Finale.hijacker, along "Descent 1", "Descent 2" ... waypoint events)
#     :CH21_BLEED_SKY   "[anim: the sky goes white and opens like an eye; the caldera's tone shifts to Bleed-violet]"
#     :CH21_VALEN_LIGHT "His crystal isn't white any more. It's light." Valen fades into it; the Crown rolls and stops.
#     :MONTAGE_<ID>     optional shots for the allies' montage (none registered yet: Finale.play_montage holds a
#                       2-second cut on the map for a beat with no shot)
#===============================================================================
module Prismfall
  module Cutscene
    LAMP_Z       = 99_990
    LAMP_SIZE    = 18
    LAMP_GAP     = 6
    LAMP_ON      = [255, 214, 96]
    LAMP_FLARE   = [255, 250, 220]
    LAMP_OFF     = [58, 54, 62]
    BOARD_WOOD   = [92, 62, 40]
    BOARD_EDGE   = [44, 28, 18]
    BARS_Z       = 99_900
    BAR_HEIGHT   = 48

    @lamp_sprite = nil
    @bar_sprites = nil

    class << self
      #-------------------------------------------------------------------------
      # Larch's eleven lamps
      #-------------------------------------------------------------------------
      def lamp_count
        return (defined?(Prismfall::Finale)) ? Prismfall::Finale::LAMP_COUNT : 11
      end

      def lamp_board_visible?
        return @lamp_sprite && !@lamp_sprite.disposed? ? true : false
      end

      # Which lamps the board last showed lit (for tests and for the capture harness).
      attr_reader :lamp_board_lit

      def draw_lamp(b, x, y, state)
        s = LAMP_SIZE
        b.fill_rect(x, y, s, s, Color.new(*BOARD_EDGE))
        rgb = (state == :flare) ? LAMP_FLARE : ((state == :on) ? LAMP_ON : LAMP_OFF)
        b.fill_rect(x + 2, y + 2, s - 4, s - 4, Color.new(*rgb))
        return if state == :off
        b.fill_rect(x + 4, y + 4, 4, 4, Color.new(255, 255, 255))            # the glint
        return if state != :flare
        b.fill_rect(x - 2, y + (s / 2) - 1, 2, 2, Color.new(*LAMP_FLARE))     # four short rays
        b.fill_rect(x + s, y + (s / 2) - 1, 2, 2, Color.new(*LAMP_FLARE))
        b.fill_rect(x + (s / 2) - 1, y - 2, 2, 2, Color.new(*LAMP_FLARE))
        b.fill_rect(x + (s / 2) - 1, y + s, 2, 2, Color.new(*LAMP_FLARE))
      end

      def lamp_board(lit = [], flare = [])
        n = lamp_count
        w = (n * LAMP_SIZE) + ((n + 1) * LAMP_GAP)
        h = LAMP_SIZE + (LAMP_GAP * 2)
        if !lamp_board_visible?
          @lamp_sprite = Sprite.new
          @lamp_sprite.bitmap = Bitmap.new(w, h)
          @lamp_sprite.z = LAMP_Z
          @lamp_sprite.x = Graphics.width - w - 12
          @lamp_sprite.y = 12
        end
        b = @lamp_sprite.bitmap
        b.clear
        b.fill_rect(0, 0, w, h, Color.new(*BOARD_EDGE))
        b.fill_rect(2, 2, w - 4, h - 4, Color.new(*BOARD_WOOD))
        n.times do |i|
          state = (flare.include?(i) && lit.include?(i)) ? :flare : (lit.include?(i) ? :on : :off)
          draw_lamp(b, LAMP_GAP + (i * (LAMP_SIZE + LAMP_GAP)), LAMP_GAP, state)
        end
        @lamp_board_lit = lit.sort
        return true
      end

      def lamp_board_off
        if @lamp_sprite && !@lamp_sprite.disposed?
          @lamp_sprite.bitmap.dispose if @lamp_sprite.bitmap && !@lamp_sprite.bitmap.disposed?
          @lamp_sprite.dispose
        end
        @lamp_sprite = nil
        return true
      end

      #-------------------------------------------------------------------------
      # Cinema bars over the live map
      #-------------------------------------------------------------------------
      def map_letterbox?
        return @bar_sprites ? true : false
      end

      def map_letterbox(on = true)
        if on
          return true if @bar_sprites
          @bar_sprites = [0, Graphics.height - BAR_HEIGHT].map do |y|
            s = Sprite.new
            s.bitmap = Bitmap.new(Graphics.width, BAR_HEIGHT)
            s.bitmap.fill_rect(0, 0, Graphics.width, BAR_HEIGHT, Color.new(0, 0, 0))
            s.z = BARS_Z
            s.y = y
            s
          end
        elsif @bar_sprites
          @bar_sprites.each do |s|
            next if s.disposed?
            s.bitmap.dispose if s.bitmap && !s.bitmap.disposed?
            s.dispose
          end
          @bar_sprites = nil
        end
        return true
      end

      # Nothing drawn here may outlive its scene: a title-screen return or a map transfer clears it.
      def clear_map_overlays
        lamp_board_off
        map_letterbox(false)
      end

      #-------------------------------------------------------------------------
      # Small helpers for the hook points (all tolerate a missing event)
      #-------------------------------------------------------------------------
      def stage_flash(r, g, b, dur = 8, alpha = 150)
        return if !$game_screen
        if defined?(pfm_flash) then pfm_flash(r, g, b, dur, alpha)
        elsif !photosensitive? then $game_screen.start_flash(Color.new(r, g, b, alpha), dur)
        end
      end

      def stage_shake(power = 4, speed = 12, dur = 10)
        return if !$game_screen
        power = [power / 2, 1].max if photosensitive?
        $game_screen.start_shake(power, speed, dur)
      end

      def stage_wait(seconds)
        pbWait(seconds) if defined?(pbWait) && seconds > 0
      end

      def stage_switch(ev, ch, value = true)
        return if !ev || !$game_self_switches || !$game_map
        $game_self_switches[[$game_map.map_id, ev.id, ch]] = value
        $game_map.need_refresh = true
      end

      def stage_events(prefix)
        return [] if !$game_map
        list = $game_map.events.values.select { |e| e.name =~ /\A#{Regexp.escape(prefix)} \d+\z/ }
        return list.sort_by { |e| e.name[/\d+\z/].to_i }
      end

      def stage_walk(ev, x, y)
        return if !ev
        if defined?(PrismfallCrownhaven) then PrismfallCrownhaven.walk_to(ev, x, y)
        else ev.moveto(x, y)
        end
      end
    end

    #---------------------------------------------------------------------------
    # The hook points
    #---------------------------------------------------------------------------
    CUTSCENE_SCENES.merge!({
      :LAMP_BOARD => proc {
        lamps = (defined?(Prismfall::Finale)) ? Prismfall::Finale.lamps : []
        Cutscene.lamp_board((0...lamps.length).select { |i| lamps[i] })
      },
      :LAMP_BOARD_DARK => proc { Cutscene.lamp_board([]) },
      :LAMP_BOARD_OFF  => proc { Cutscene.lamp_board_off },
      :LETTERBOX_ON    => proc { Cutscene.map_letterbox(true) },
      :LETTERBOX_OFF   => proc { Cutscene.map_letterbox(false) },
      :CH20_VISION     => proc { (defined?(pf_ceremony_vision)) ? pf_ceremony_vision : true },
      :CH20_VISION_END => proc { (defined?(pf_ceremony_vision_end)) ? pf_ceremony_vision_end : true },

      :HJ_RINGS => proc {
        rings = Cutscene.stage_events("Arena ring")
        steps = [rings.length, 3].max
        steps.times do |i|
          Cutscene.stage_switch(rings[i], "A") if rings[i]
          (pbSEPlay("Mining reveal", 80, 70 + (i * 12)) rescue nil)
          Cutscene.stage_flash(255, 208, 64, 6, 90 + (i * 20))
          Cutscene.stage_wait(0.35)
        end
        Cutscene.stage_shake(6, 14, 16)
        Cutscene.stage_switch(Cutscene.find_event("Ring floor"), "A")       # the floor at the centre splits
        Cutscene.stage_wait(0.6)
        true
      },
      :HJ_CRADLE => proc {
        ev = Cutscene.find_event("Cradle")
        Cutscene.stage_switch(ev, "A")
        Cutscene.stage_shake(3, 10, 24)
        if ev && defined?(pfm_appear) then pfm_appear("Cradle", 30)
        else Cutscene.stage_wait(1.2)
        end
        true
      },
      :HJ_LOCKS => proc {
        (defined?(pf_pylon_lock)) ? pf_pylon_lock(:all) : Cutscene.stage_flash(255, 208, 64, 10, 120)
        true
      },
      :HJ_CROWN => proc {
        cradle = Cutscene.find_event("Cradle")
        crown = Cutscene.find_event("Crown")
        Cutscene.stage_flash(255, 255, 255, 4, 120)
        crown.moveto(cradle.x, cradle.y) if crown && cradle
        Cutscene.stage_switch(crown, "A")
        (pbSEPlay("Battle damage super") rescue nil)
        Cutscene.stage_shake(5, 16, 8)
        if cradle && $game_player            # pulled after it by your own chest, to your knees at the golden hand
          Cutscene.stage_walk($game_player, cradle.x, cradle.y + 1)
          $game_player.turn_up if $game_player.respond_to?(:turn_up)
          if pbResolveBitmap("Graphics/Characters/kneel_PLAYER")
            $game_player.instance_variable_set(:@character_name, "kneel_PLAYER")
          end
        end
        true
      },
      :HJ_DESCENT => proc {
        who = (defined?(Prismfall::Finale)) ? Prismfall::Finale.hijacker : :VOSS
        ev = Cutscene.find_event(who.to_s.capitalize)
        if ev
          Cutscene.stage_switch(ev, "A")
          Cutscene.stage_events("Descent").each { |pt| Cutscene.stage_walk(ev, pt.x, pt.y) }
        else
          Cutscene.stage_wait(0.8)
        end
        true
      },
      :CH21_BLEED_SKY => proc {
        Cutscene.stage_flash(255, 255, 255, 16, 200)
        Cutscene.stage_wait(0.8)
        if $game_screen                       # Bleed-violet over the whole caldera until the map sets its own tone again
          $game_screen.start_tone_change(Tone.new(34, -20, 68, 40), 40)
          Cutscene.stage_wait(2.0)
        end
        true
      },
      :CH21_VALEN_LIGHT => proc {
        valen = Cutscene.find_event("Valen")
        3.times do |i|
          Cutscene.stage_flash(255, 255, 255, 10, 80 + (i * 40))
          Cutscene.stage_wait(0.5)
        end
        if valen
          if defined?(pfm_vanish) then pfm_vanish("Valen", 40)
          else valen.erase
          end
        end
        crown = Cutscene.find_event("Crown")
        if crown && valen                     # the Crown falls, empty, rolls a little way, and stops
          crown.moveto(valen.x, valen.y)
          Cutscene.stage_switch(crown, "B")
          (pbSEPlay("Battle ball drop") rescue nil)
          Cutscene.stage_walk(crown, crown.x + 2, crown.y)
        end
        Cutscene.stage_wait(1.0)
        true
      }
    })
  end
end

EventHandlers.add(:on_leave_map, :prismfall_finale_overlays,
  proc { |_new_map_id, _new_map|
    Prismfall::Cutscene.clear_map_overlays
  }
)
