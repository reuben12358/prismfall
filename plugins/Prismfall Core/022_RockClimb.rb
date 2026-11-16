#===============================================================================
# Prismfall Core - 022 Rock Climb field move (v21 has none)
#-------------------------------------------------------------------------------
# Badge requirement: FIELD_MOVE_BADGES[:ROCKCLIMB] (10), exposed as
# Prismfall::BADGE_FOR_ROCKCLIMB and Settings::BADGE_FOR_ROCKCLIMB.
#
# Mapping a cliff: put an Action Button event on the cliff's bottom tile and
# another on its top tile, both named "RockClimb" or "RockClimb(N)" (N = tiles
# to travel, default 2), with no graphic and the script:
#     Script: pbRockClimb          (or pbRockClimb(3) to override N)
# Facing the event and pressing USE asks to climb; the player then moves N
# tiles forward in the facing direction with Through on (up from the bottom,
# down from the top). Using Rock Climb from the party menu while facing such an
# event does the same. Make sure the tile N steps ahead is passable.
#===============================================================================
module Prismfall
  BADGE_FOR_ROCKCLIMB = (FIELD_MOVES_COUNT_BADGES) ? FIELD_MOVE_BADGES[:ROCKCLIMB] :
                                                     [FIELD_MOVE_BADGES[:ROCKCLIMB] - 1, 0].max
  ROCK_CLIMB_DEFAULT_STEPS = 2
  ROCK_CLIMB_EVENT_NAME    = /rockclimb(?:\((\d+)\))?/i

  # Tiles to climb for a cliff event (from its name), or nil if not a cliff.
  def self.rock_climb_steps(event)
    return nil if !event || !event.name
    m = ROCK_CLIMB_EVENT_NAME.match(event.name)
    return nil if !m
    return (m[1]) ? m[1].to_i : ROCK_CLIMB_DEFAULT_STEPS
  end

  # Moves the player `steps` tiles forward ignoring passability, then waits.
  def self.climb_forward(steps)
    steps = steps.to_i.clamp(1, 20)
    pbSEPlay("Rock climb") if pbResolveAudioSE("Rock climb")
    pbMoveRoute($game_player, [PBMoveRoute::FORWARD] * steps)
    while $game_player.move_route_forcing
      Graphics.update
      Input.update
      pbUpdateSceneMap
    end
    $game_player.through = false
    return true
  end
end

Settings.const_set(:BADGE_FOR_ROCKCLIMB, Prismfall::BADGE_FOR_ROCKCLIMB) if !Settings.const_defined?(:BADGE_FOR_ROCKCLIMB, false)

# Event helper (mirrors pbRockSmash / pbWaterfall).
def pbRockClimb(steps = nil)
  move = :ROCKCLIMB
  steps ||= Prismfall.rock_climb_steps($game_player.pbFacingEvent(true)) || Prismfall::ROCK_CLIMB_DEFAULT_STEPS
  movefinder = $player.get_pokemon_with_move(move)
  if !pbCheckHiddenMoveBadge(Prismfall::BADGE_FOR_ROCKCLIMB, false) || (!$DEBUG && !movefinder)
    pbMessage(_INTL("A steep, rugged cliff. A Pokémon may be able to climb it."))
    return false
  end
  return false if !pbConfirmMessage(_INTL("The cliff looks climbable.\nWould you like to use Rock Climb?"))
  speciesname = (movefinder) ? movefinder.name : $player.name
  pbMessage(_INTL("{1} used {2}!", speciesname, GameData::Move.get(move).name))
  pbHiddenMoveAnimation(movefinder)
  return Prismfall.climb_forward(steps)
end

HiddenMoveHandlers::CanUseMove.add(:ROCKCLIMB, proc { |move, pkmn, showmsg|
  next false if !pbCheckHiddenMoveBadge(Prismfall::BADGE_FOR_ROCKCLIMB, showmsg)
  if !Prismfall.rock_climb_steps($game_player.pbFacingEvent)
    pbMessage(_INTL("You can't use that here.")) if showmsg
    next false
  end
  next true
})

HiddenMoveHandlers::UseMove.add(:ROCKCLIMB, proc { |move, pokemon|
  if !pbHiddenMoveAnimation(pokemon)
    pbMessage(_INTL("{1} used {2}!", pokemon.name, GameData::Move.get(move).name))
  end
  next Prismfall.climb_forward(Prismfall.rock_climb_steps($game_player.pbFacingEvent) ||
                               Prismfall::ROCK_CLIMB_DEFAULT_STEPS)
})
