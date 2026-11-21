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
#
#   Talking to her (map builder 12): face the follower and press USE. She turns to you and says the next of her lines for
#   the map you are on (JUNO_TALK, cycling), or every fourth time a line for the time of day (JUNO_TALK_TIME); on maps
#   with no lines she has a few for anywhere (JUNO_TALK_ANY). pfm_juno_talk runs it; no common event is needed.
#===============================================================================
module PrismfallMaps
  JUNO_NAME    = "Juno"
  JUNO_CHARSET = "JUNO"
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

#-------------------------------------------------------------------------------
# Juno's lines when you talk to her while she follows (map builder 12). [expression, text]; her voice from
# story/03_CAST.md and the Chapter 0-3 scripts: plant facts, chatter, a little nerve under it.
#-------------------------------------------------------------------------------
module PrismfallMaps
  JUNO_TALK = {
    100 => [[:happy, "This is the most exciting thing to happen on this dock since the lighthouse cat got stuck in the lighthouse. Twice."],
            [:neutral, "Mum's stall is the one with the bramble jam. If she offers you a tart, say yes. If she offers you two, run."],
            [:deadpan, "Meridian put that customs gate up in a week. Things that go up in a week come down in a week. That's a carpentry fact, not a political one."]],
    520 => [[:neutral, "Ferrymen's oaks. They plant one for every crossing that came home. ...There are fewer at this end. I try not to count."],
            [:happy, "Hawthorn in the hedges. In spring it smells like cake. In autumn it smells like a different, worse cake."],
            [:neutral, "Larches drop their needles every winter so they don't snap. I've told you that. I'm going to keep telling you. It's a good fact."]],
    521 => [[:happy, "Every apple on Windfall Row is free. Technically. Dad says 'technically' is how you lose a finger."],
            [:panic, "The Pruett orchard's past the cordon. Nobody goes in. Biscuit goes in. Biscuit is not a role model."]],
    522 => [[:panic, "Don't touch the glass apples. Don't lick them either. I'm not saying anyone did. I'm saying don't."],
            [:neutral, "Larch says the Bleed doesn't hurt you if you stay calm. I am extremely calm. This is my calm voice."]],
    523 => [[:neutral, "Mind the third stair. It isn't broken, it just has opinions."],
            [:blush, "That's my room. Don't look at the seed packets. Only some of them are labelled honestly."]],
    527 => [[:happy, "Chalk is just very old sea creatures, very squashed. We're walking on the most crowded graveyard in Elowen. ...Sorry. That got dark."],
            [:panic, "Forty bramble tarts in this satchel. If I trip, Saltmere goes hungry and Mum never speaks to me again."],
            [:happy, "Sea pinks on the cliff edge! They grow where nothing else will. I respect that. I'd like to be a sea pink."]],
    528 => [[:happy, "Marram grass holds the whole dune together with its roots and nobody thanks it. I thank it. Thank you, marram."],
            [:blush, "The players' wagons! I've wanted to see the Pageant since I was six. I'm being very cool about it. This is me being cool."]],
    140 => [[:happy, "Every second building is a theatre. The others are where the actors sleep, I think. Or where they practise sleeping."],
            [:smug, "Salt-caramel. I can smell it from here. That isn't a hint. ...It's a little bit of a hint."],
            [:neutral, "Dorian Pell calls everyone 'darling'. Professor says he means it about a third of the time. I want to be in the third."]],
    541 => [[:neutral, "Glasswort. You can pickle it. You can eat it raw, too, if you like your mouth to feel like the sea."],
            [:happy, "The salt pans go pink when the brine's ready. Something in it blooms. Even salt has flowers here."]],
    542 => [[:happy, "This is the cosiest room I've ever been in, and it smells entirely of fish."]],
    544 => [[:neutral, "It's warmer down here than it should be. Salt keeps the heat, the miner said. Or ghosts. He said salt."],
            [:deadpan, "Don't lick the walls. I know it's salt. I KNOW."]],
    546 => [[:panic, "I'm not scared. I'm holding your sleeve for structural reasons."],
            [:neutral, "If a ghost asks me to stay for the second act, I'm saying no. Politely. Then running."]],
    552 => [[:happy, "Red, blue, yellow. The river's wearing a dress. ...Don't let my veil near the water, it'll come out purple."],
            [:neutral, "Madder for the red, woad for the blue, weld for the yellow. I know all the plants and none of the people. Hello, people!"]],
    540 => [[:happy, "Nobody's mown this meadow in sixty years. Look at it. It's having the best time of its life."],
            [:sad, "The orange flags go right toward the Glasswood. That's... probably fine?"]],
    524 => [[:happy, "Silk on every branch. Uncle Rowan says the moths spin for the weavers on purpose. I think they just like the company."],
            [:sad, "The survey flags go deeper in. I don't like how straight they are. Nothing in a wood should be that straight."]],
    526 => [[:deadpan, "Someone lives here who really, really likes kindling."]],
    120 => [[:happy, "Look up. No, further up. The houses are IN the trees. I want to live in a tree. I'd never come down."]]
  }
  JUNO_TALK_SAME = { 146 => 140, 147 => 140, 141 => 140, 545 => 544, 547 => 546, 101 => 100, 102 => 100 }
  JUNO_TALK_WEAVERS_140 = [
    [:sad, "He sounded sad. The Mourner. I keep thinking about it. Is it bad that I keep thinking about it?"],
    [:neutral, "Briarwick's up the Weavers' Road. Uncle Rowan wants silk-moth eggs and I want a hot bath, in that order."]]
  JUNO_TALK_TIME = {
    :morning => [[:happy, "Dew on everything. That's free water for every leaf for a mile. Best deal in the world."],
                 [:neutral, "Mum says the first hour of the morning belongs to the bees. We're just borrowing it."]],
    :day     => [[:happy, "Sun's high. Somewhere a sunflower is very pleased with itself."],
                 [:neutral, "Bees are out. Bees are always out. Bees have never once taken a day off, and I find that very relatable."]],
    :evening => [[:neutral, "The light's going gold. Uncle Rowan calls it the gardener's hour. Everything looks like it's about to say something."],
                 [:deadpan, "Bats soon. They eat the moths that eat the leaves. Everybody's somebody's dinner. That's ecology. Sorry."]],
    :night   => [[:neutral, "Moonflowers open about now. Not here. But somewhere. I like knowing that."],
                 [:panic, "It's dark. I'm fine. I'm humming so you know where I am, not because I'm scared."]]
  }
  JUNO_TALK_ANY = [
    [:happy, "I'm right behind you. Literally. My veil's caught on your bag."],
    [:neutral, "If you ever need a plant fact, I've got about four hundred. That's not a threat."],
    [:happy, "We should name this road. Not officially. Just us. ...'The one with the good rock.' There. Done."]]

  module_function

  def juno_time_key
    return :night if !defined?(PBDayNight)
    return :morning if PBDayNight.isMorning?
    return :evening if PBDayNight.isEvening?
    return :night if PBDayNight.isNight?
    return :day
  end

  def juno_line
    mid = $game_map.map_id
    mid = JUNO_TALK_SAME[mid] || mid
    lines = (mid == 140 && pfm_get(:juno_leg) == :weavers) ? JUNO_TALK_WEAVERS_140 : JUNO_TALK[mid]
    n = pfm_add(:juno_talks)
    if !lines || n % 4 == 0
      pool = (n % 4 == 0) ? JUNO_TALK_TIME[juno_time_key] : JUNO_TALK_ANY
      pool = JUNO_TALK_ANY if !pool || pool.empty?
      return pool[(n / 4) % pool.size]
    end
    key = ("juno_talk_" + mid.to_s + (lines.equal?(JUNO_TALK_WEAVERS_140) ? "w" : "")).to_sym
    k = pfm_add(key) - 1
    return lines[k % lines.size]
  end
end

def pfm_juno_talk
  expr, text = PrismfallMaps.juno_line
  if defined?(pf_say)
    pf_say(:JUNO, expr, text)
  else
    pbMessage(_INTL("Juno: {1}", text))
  end
  return true
end

# Essentials' FollowerData#interact runs a common event; Juno has none, so she talks through pfm_juno_talk.
class FollowerData
  alias_method :pfm_interact_before_juno, :interact
  def interact(event)
    return pfm_interact_before_juno(event) if @name != PrismfallMaps::JUNO_NAME
    return if !event || !visible?
    $game_map.refresh if $game_map.need_refresh
    event.turn_toward_player
    list = [RPG::EventCommand.new(355, 0, ["pfm_juno_talk"]), RPG::EventCommand.new(0, 0, [])]
    pbMapInterpreter.setup(list, 0, event.map.map_id)
  end
end

EventHandlers.add(:on_enter_map, :prismfall_juno_follower,
  proc { |_old_map_id| PrismfallMaps.juno_sync }
)
