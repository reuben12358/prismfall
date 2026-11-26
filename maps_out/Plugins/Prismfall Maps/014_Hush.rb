#===============================================================================
# Prismfall Maps - 014 the Hush: a map with no sound (mapgen/ruby/014_Hush.rb, copied by build.py)
#-------------------------------------------------------------------------------
# story/34_SCRIPT_CH15.md "Map 808 - the Hush": "A Bleed zone where sound doesn't exist. BGM and BGS stop; SEs are
# muted for the map. The PC's footsteps show as ripples on the ground. Wild Pokemon move, and their cries show as
# rings with no sound." Battles there are silent too (HUSH_MUTES_BATTLES).
#
# On a HUSH_MAPS map Game_System plays no BGM, BGS, SE or ME (cries are SEs; battle music too), the map's own
# BGM and BGS are faded out on entry, and each step leaves a ripple (HUSH_RIPPLE_ANIMATION, an Animations.rxdata id;
# the stock dust puff until the ripple animation is drawn).
#   pfm_hush?            is this map silent right now?
#   pfm_hush_lift        the far edge: sound exists again for the rest of this visit ("wind, then a bird, then far
#                        off, hammers"), so the closing scene can play its BGS and SEs
#   pfm_hush_ring(event) the silent "cry": a ripple on that event's tile
#===============================================================================
module PrismfallMaps
  HUSH_MAPS              = [808]
  HUSH_MUTES_BATTLES     = true
  HUSH_RIPPLE_ANIMATION  = nil     # nil = Settings::DUST_ANIMATION_ID

  @hush_lifted = nil

  def self.hush?
    return false if !$game_map || !HUSH_MAPS.include?($game_map.map_id)
    return false if @hush_lifted == $game_map.map_id
    return false if !HUSH_MUTES_BATTLES && $game_temp && $game_temp.in_battle
    return true
  end

  def self.hush_lift
    @hush_lifted = ($game_map) ? $game_map.map_id : nil
    return true
  end

  def self.hush_enter
    @hush_lifted = nil if !$game_map || @hush_lifted != $game_map.map_id
    return if !hush?
    pbBGMStop(1.0)
    pbBGSStop(1.0)
  end

  def self.hush_ripple(x, y)
    return if !$scene || !$scene.respond_to?(:spriteset) || !$scene.spriteset
    id = HUSH_RIPPLE_ANIMATION || Settings::DUST_ANIMATION_ID
    $scene.spriteset.addUserAnimation(id, x, y, true, 1)
  rescue StandardError
    nil
  end
end

# Every sound in the game goes through Game_System (pbBGMPlay, pbSEPlay, cries, battle music, map autoplay).
class Game_System
  [:bgm_play, :bgs_play, :se_play, :me_play].each do |meth|
    old = :"pf_hush_#{meth}"
    next if method_defined?(old) || !method_defined?(meth)
    alias_method old, meth
    define_method(meth) do |*args|
      next nil if PrismfallMaps.hush?
      next send(old, *args)
    end
  end
end

def pfm_hush?;     return PrismfallMaps.hush?;     end
def pfm_hush_lift; return PrismfallMaps.hush_lift; end

def pfm_hush_ring(event)
  ev = event
  ev = $game_map.events[event] if event.is_a?(Integer)
  ev = $game_map.events.values.find { |e| e.name == event } if event.is_a?(String)
  PrismfallMaps.hush_ripple(ev.x, ev.y) if ev
  return true
end

EventHandlers.add(:on_enter_map, :prismfall_hush,
  proc { |_old_map_id| PrismfallMaps.hush_enter }
)
EventHandlers.add(:on_player_step_taken, :prismfall_hush_ripples,
  proc {
    next if !PrismfallMaps.hush? || !$game_player
    PrismfallMaps.hush_ripple($game_player.x, $game_player.y)
  }
)
