#===============================================================================
# Prismfall Puzzles - the Saltmere audience (SPINE Revision 19, item 3).
#
# "The more people you meet around town, the more audience shows up for your fight... based on the number of people
# in the crowd, the battle starts at a specific stage."
#
#   V313 STAGE_AUDIENCE  how many Saltmere townsfolk you have met (each counts once) plus the Saltmere Trial-board
#                        quests you have finished.  Map 154's seats fill by it (event pages [V313 >= k]) and each
#                        person you met takes their own seat in the stalls.
#   The house            sparse (< 7): Grand Stage starts at stage 1, Opening Night
#                        good   (7-13): stage 2, Encore
#                        full   (14+): stage 3, Standing Ovation
#   Your fans            from a good house up, the people you met cheer for YOUR side: at Encore and above your
#                        Pokemon bask in the applause (1/16 HP a round), as Dorian's Normal types do at Standing
#                        Ovation (the Grand Stage field reads FieldEffects.home_crowd?).  And the bigger the house,
#                        the more Standing Ovation is yours (FieldEffects.home_crowd_foe? / home_crowd_full?): at a
#                        good house Dorian's troupe basks at half; at a full house only your side basks, only your
#                        attacks get its +1 crit stage and his Sing can miss.  Still a show, not a free win: Dorian's
#                        Normal moves are x1.5 from the first turn.
#   The takings          after the win, your share of the box office: $150 a head.
#
# Townsfolk call pfm_audience(:key) from their own event (the map builder places the call: mapgen/REQUESTS.md);
# Trial-board quests are counted when map 150 or 154 loads (pf_audience_sync).
#===============================================================================
module PrismfallPuzzles
  AUDIENCE_VAR = 313
  # key => [name, map] (the people who count: Saltmere's named townsfolk you can meet before Gym 1)
  AUDIENCE_PEOPLE = {
    :caramel_seller  => ["Caramel Seller", 140],     :busker          => ["Busker", 140],
    :ogre_child      => ["Child with an Ogre puppet", 140], :retired_actor => ["Retired Actor", 140],
    :hound_two       => ["Hound Number Two", 140],   :fishwife        => ["Fishwife", 140],
    :ferry_woman     => ["Woman from the ferry", 140], :eevee_breeder => ["Eevee breeder", 140],
    :salt_raker      => ["Salt raker", 140],         :harbourmaster   => ["Harbourmaster", 143],
    :saltwife        => ["Saltwife", 144],           :stevedore       => ["Stevedore", 146],
    :old_angler      => ["Old angler", 146],         :fisherman       => ["Fisherman", 146],
    :old_sailor      => ["Old Sailor", 146],         :smoke_stagehand => ["Stagehand on a smoke break", 146],
    :costumier       => ["Costumier", 147],          :street_player   => ["Street player", 147]
  }
  # Saltmere Trial-board quests finishable before Gym 1 => seats they fill
  AUDIENCE_QUESTS = { :EL_LANTERNS => 3 }
  HOUSE = [[14, 3, "a full house"], [7, 2, "a good house"], [0, 1, "a sparse house"]]   # [from, stage, name]
  FANS_FROM = 7

  def self.audience
    return $game_variables ? $game_variables[AUDIENCE_VAR].to_i : 0
  end

  def self.house
    return HOUSE.find { |from, _, _| self.audience >= from }
  end

  def self.audience_add(key, n = 1)
    flags = PrismfallMaps.flags rescue nil
    return false if !flags || flags[("aud_" + key.to_s).to_sym]
    flags[("aud_" + key.to_s).to_sym] = true
    $game_variables[AUDIENCE_VAR] = self.audience + n
    $game_map.need_refresh = true if $game_map
    return true
  end

  # Trial-board quests are counted when the Playhouse loads (no hook in the Trials code needed).
  def self.audience_sync
    AUDIENCE_QUESTS.each do |q, n|
      done = defined?(pf_quest_done?) ? (pf_quest_done?(q) rescue false) : false
      self.audience_add("quest_#{q}", n) if done
    end
  end

  # Map 154's house manager: every person you met takes their own seat (event "Fan <key>", self switch A).
  def self.seat_fans
    return if !$game_map
    flags = PrismfallMaps.flags rescue {}
    $game_map.events.each_value do |ev|
      next if !ev.name[/^Fan (\S+)/]
      key = $1
      $game_self_switches[[$game_map.map_id, ev.id, "A"]] = !!flags[("aud_" + key).to_sym]
    end
    $game_map.need_refresh = true
  end
end

# Call from a townsperson's event, first thing: counts them once into the Saltmere audience.
def pfm_audience(key)
  return PrismfallPuzzles.audience_add(key)
end

def pf_audience;      return PrismfallPuzzles.audience;   end
def pf_house_stage;   return PrismfallPuzzles.house[1];   end
def pf_house_name;    return PrismfallPuzzles.house[2];   end
def pf_audience_sync; PrismfallPuzzles.audience_sync; PrismfallPuzzles.seat_fans if $game_map&.map_id == 154; end

class Game_Temp
  attr_accessor :pf_home_crowd      # the number of your fans in the house, for the next battle only
end

# Dorian's show: the house decides the Grand Stage's opening stage, and your fans come with you.
def pf_house_rules
  setBattleRule("fieldStage", pf_house_stage)
  $game_temp.pf_home_crowd = (pf_audience >= PrismfallPuzzles::FANS_FROM) ? pf_audience : nil
end

EventHandlers.add(:on_end_battle, :pf_home_crowd_clear,
  proc { |_outcome, _can_lose| $game_temp.pf_home_crowd = nil if $game_temp }
)

module FieldEffects
  # Grand Stage (102_Field_GrandStage.rb): does this battler have fans in the house?  Only the player's side, only in a
  # battle that pf_house_rules set up (Dorian's), only from a good house up.
  def self.home_crowd?(battle, battler)
    return false if !$game_temp || !$game_temp.pf_home_crowd || !battler
    return battler.respond_to?(:pbOwnedByPlayer?) && battler.pbOwnedByPlayer?
  end

  # ...and is this battler on the other side of that house?  With your fans in, Standing Ovation's bask skips Dorian's
  # troupe: the house cheers you, not him.
  def self.home_crowd_foe?(battle, battler)
    return false if !$game_temp || !$game_temp.pf_home_crowd || !battler
    return battler.respond_to?(:opposes?) && battler.opposes?
  end

  # ...and is it a full house (14+)?  Then Standing Ovation is all yours: only your side basks, only your attacks get
  # its crit stage, and Dorian's Sing can miss.  At a good house his troupe still basks, at half.
  def self.home_crowd_full?(battle)
    return false if !$game_temp || !$game_temp.pf_home_crowd
    return $game_temp.pf_home_crowd >= PrismfallPuzzles::HOUSE[0][0]
  end
end
