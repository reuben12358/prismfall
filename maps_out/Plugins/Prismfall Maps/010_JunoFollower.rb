#===============================================================================
# Prismfall Maps - 010 Juno as a follower (mapgen/ruby/010_JunoFollower.rb, copied by build.py)
#-------------------------------------------------------------------------------
# Built on Essentials v21.1's own Followers ($PokemonGlobal.followers is saved with the game, and the generated doors
# already call Followers.follow_into_door / hide_followers / put_followers_on_player).
#
#   pfm_juno_join(:leg)                 Juno starts following (the script's "(Juno becomes a follower.)"). She steps
#                                       out behind the player.
#   pfm_juno_join(:leg, "Event name")   ...taking the place and look of that map event, whose self switch B is then set
#                                       (give the event an empty last page with cond self B).
#   pfm_juno_part                       Juno stops following ("(She stops following.)").
#   pfm_juno_part("Event name")         ...and that map event is moved onto her tile, facing her way, and shown, so the
#                                       scene's move route walks her off from where she really stood.
#   pfm_juno?                           is she following?
#
# The leg (pfm :juno_leg: :errand, :saltmere, :weavers) is the story's record. On every map entry the follower is
# re-synced with it (old saves, debug warps), and she is hidden on JUNO_WAITS maps: in the Glassed Orchard after
# Lecture One she waits at the gate (the map's own Juno event stands there) and falls in again when you leave.
#===============================================================================
module PrismfallMaps
  JUNO_NAME    = "Juno"
  JUNO_CHARSET = "trainer_RIVAL2"
  JUNO_WAITS   = { 522 => proc { $game_switches[105] } }   # map => when she waits outside instead of following in
  # Her map stand-ins elsewhere (same scene, earlier leg): erased while she follows, so there is never a second Juno.
  JUNO_STANDINS = { 100 => ["Juno (sendoff)"], 103 => ["Juno (station)"] }

  module_function

  def juno_follower
    return nil if !$game_temp || !$PokemonGlobal
    return $game_temp.followers.get_follower_by_name(JUNO_NAME)
  end

  def juno_data
    return nil if !$PokemonGlobal
    return $PokemonGlobal.followers.find { |f| f.name == JUNO_NAME }
  end

  def juno_find_event(name)
    return nil if !name || !$game_map
    return $game_map.events.values.find { |e| e && e.name == name }
  end

  # Adds the follower from a map event, or from a stand-in event on the player's tile.
  def juno_add(source = nil)
    return juno_follower if juno_data
    event = source
    if !event
      rpg = RPG::Event.new($game_player.x, $game_player.y)
      rpg.id   = 9000 + $game_map.map_id   # a stand-in: never a real event id on any map
      rpg.name = JUNO_NAME
      event = Game_Event.new($game_map.map_id, rpg, $game_map)
      event.character_name = JUNO_CHARSET
      event.character_hue  = 0
      event.direction      = $game_player.direction
    end
    $game_temp.followers.add_follower(event, JUNO_NAME, nil)
    $game_temp.followers.put_followers_on_player if !source
    return juno_follower
  end

  def juno_remove
    $game_temp.followers.remove_follower_by_name(JUNO_NAME) if juno_data
  end

  def juno_apply_visibility
    data = juno_data
    return if !data || !$game_map
    rule = JUNO_WAITS[$game_map.map_id]
    data.visible = !(rule && rule.call)
  end

  def juno_erase_standins
    (JUNO_STANDINS[$game_map.map_id] || []).each { |n| e = juno_find_event(n); e.erase if e }
  end

  # on_enter_map: make the follower match the story's record.
  def juno_sync
    return if !$game_temp || !$PokemonGlobal || !$game_map || !$game_player
    if pfm_get(:juno_leg)
      juno_add if !juno_data
      juno_apply_visibility
      juno_erase_standins
    elsif juno_data
      juno_remove
    end
  end

  def juno_shown?(e)
    return e.is_a?(Game_Event) && !e.instance_variable_get(:@erased) &&
           (e.character_name.to_s != "" || e.tile_id.to_i > 0) && e.opacity.to_i > 0 && !e.transparent
  end

  # The portrait bubble of a Juno line points at the follower unless one of her map events is on show: the line's own
  # event (\pf[JUNO,expr,,Event]) or, for a plain \pf[JUNO,...], an event called "Juno".
  def juno_bubble_target(found, explicit)
    f = juno_follower
    return found if !f || !$game_map || f.map_id != $game_map.map_id || !juno_data&.visible?
    own = (explicit) ? found : $game_map.events.values.find { |e| e.respond_to?(:name) && e.name.to_s.downcase == "juno" }
    return own if juno_shown?(own)
    return f
  end
end

def pfm_juno?
  return !!pfm_get(:juno_leg) && !PrismfallMaps.juno_data.nil?
end

def pfm_juno_join(leg = :road, event_name = nil)
  pfm_set(:juno_leg, leg)
  source = PrismfallMaps.juno_find_event(event_name)
  if source && !PrismfallMaps.juno_data
    PrismfallMaps.juno_add(source)
    $game_self_switches[[$game_map.map_id, source.id, "B"]] = true
    $game_map.need_refresh = true
  else
    PrismfallMaps.juno_add
  end
  PrismfallMaps.juno_apply_visibility
  PrismfallMaps.juno_erase_standins
  return true
end

def pfm_juno_part(event_name = nil)
  follower = PrismfallMaps.juno_follower
  target   = PrismfallMaps.juno_find_event(event_name)
  if target && follower && follower.map_id == $game_map.map_id && PrismfallMaps.juno_data&.visible?
    target.moveto(follower.x, follower.y)
    target.direction = follower.direction
  end
  PrismfallMaps.juno_remove
  pfm_set(:juno_leg, nil)
  return true
end

if defined?(Prismfall::Portrait) && Prismfall::Portrait.respond_to?(:speaker)
  class << Prismfall::Portrait
    alias_method :pfm_speaker_before_juno, :speaker
    def speaker(spec)
      found = pfm_speaker_before_juno(spec)
      return found if !spec.is_a?(Hash) || spec[:id] != :JUNO || !PrismfallMaps.juno_data
      explicit = spec[:event] || (respond_to?(:person) ? person(:JUNO)[:event] : nil)
      return PrismfallMaps.juno_bubble_target(found, explicit)
    rescue StandardError
      return found
    end
  end
end

EventHandlers.add(:on_enter_map, :prismfall_juno_follower,
  proc { |_old_map_id| PrismfallMaps.juno_sync }
)
