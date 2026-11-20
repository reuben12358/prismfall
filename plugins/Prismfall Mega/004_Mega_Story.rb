#===============================================================================
# Prismfall Mega - 004 Map-event helpers, conditions, debug menu
#-------------------------------------------------------------------------------
# Map events for stones (design/TRIAL_EVENTS.yaml ("Mega Evolution" maps)) make ONE call:
#   pf_mega_stone(:ABSOLITE)                       the item jingle + "obtained"
#   pf_mega_stone(:ABSOLITE, "A black stone...")   a line first
# Before the Ring (13 badges) the first stone also gets PrismfallMega::TEASER_TEXT.
# The Mega Ring and the quest stones come from Trials scenes
# (plugins/Prismfall Trials/114_Quests_Megas.rb), so all dialogue lives in one place.
# Conditions (Prismfall::Conditions): mega_ring, mega_stones (count in the Bag).
# Kestrel and Morwen's Ring: MORWEN_RING (001), applied when his trainer is loaded.
#===============================================================================
module PrismfallMega
  def self.stones_owned
    return 0 if !$bag
    n = 0
    GameData::Item.each { |it| n += 1 if it.is_mega_stone? && $bag.has?(it.id) }
    return n
  end

  # Core save data (Prismfall::SaveState#custom), so it survives saving.
  def self.custom
    return nil if !defined?(Prismfall) || !Prismfall.respond_to?(:state)
    st = Prismfall.state
    return nil if !st.respond_to?(:custom)
    st.custom ||= {}
    return st.custom
  end

  def self.teaser_seen?
    c = custom
    return c ? (c[:mega_teaser] ? true : false) : false
  end

  def self.mark_teaser
    c = custom
    c[:mega_teaser] = true if c
  end

  def self.give_stone(item, text = nil)
    item = item.to_sym
    return false if !GameData::Item.exists?(item)
    return false if $bag.has?(item)              # each stone exists once
    pbMessage(_INTL(text)) if text
    return false if !pbReceiveItem(item)
    if !ring? && !teaser_seen?
      pbMessage(_INTL(TEASER_TEXT))
      mark_teaser
    end
    return true
  end
end

module PrismfallMega
  def self.morwen_ring_given?
    key, val = MORWEN_RING_CHOICE
    return false if !defined?(Prismfall::Choices)
    return Prismfall::Choices.get(key) == val
  rescue StandardError
    return false
  end

  # K8 with Morwen's Ring: the ring and the Scizorite. Rival battles load through pbLoadTrainer, which doesn't pass the
  # version on, so this goes by the Scizor's level (K8 and K9 are his only battles at 90+, and K9 happens only when the
  # ring was kept). TrainerBattle.start fires :on_trainer_load for every trainer it loads.
  def self.morwen_ring_swap(trainer, force = false)
    mr = MORWEN_RING
    return false if !trainer.respond_to?(:trainer_type) || trainer.trainer_type != mr[:trainer]
    return false if !force && !morwen_ring_given?
    pkmn = trainer.party.find { |p| p && p.species == mr[:species] && p.level >= mr[:min_level] }
    return false if !pkmn
    pkmn.item = mr[:item]
    trainer.items.unshift(RING) if trainer.respond_to?(:items) && !trainer.items.include?(RING)
    return true
  end
end

EventHandlers.add(:on_trainer_load, :prismfall_mega_morwen_ring,
  proc { |trainer|
    PrismfallMega.morwen_ring_swap(trainer) if trainer
  }
)

def pf_mega_stone(item, text = nil)
  return PrismfallMega.give_stone(item, text)
end

if defined?(Prismfall::Conditions)
  module Prismfall
    module Conditions
      {
        "mega_ring"   => [0, proc { PrismfallMega.ring? }],
        "mega_stones" => [0, proc { PrismfallMega.stones_owned }]
      }.each { |name, fn| FUNCTIONS[name] = fn }
    end
  end
end

MenuHandlers.add(:debug_menu, :prismfall_mega_menu, {
  "name"        => _INTL("Prismfall Mega..."),
  "parent"      => :main,
  "description" => _INTL("Mega Ring, Mega Stones, the stone distribution."),
  "effect"      => proc {
    loop do
      cmds = [_INTL("Give the Mega Ring"), _INTL("Give every placed Mega Stone"),
              _INTL("Show stone distribution"), _INTL("Done")]
      c = pbMessage(_INTL("Prismfall Mega ({1} stones in the Bag, ring: {2})", PrismfallMega.stones_owned,
                          PrismfallMega.ring? ? "yes" : "no"), cmds, -1)
      case c
      when 0 then $bag.add(PrismfallMega::RING) if !PrismfallMega.ring?
      when 1 then PrismfallMega::STONES.each_key { |s| $bag.add(s) if GameData::Item.exists?(s) && !$bag.has?(s) }
      when 2
        PrismfallMega::STONES.sort_by { |_s, d| d[:badges] }.each_slice(6) do |rows|
          pbMessage(rows.map { |s, d| "#{d[:badges]}: #{GameData::Item.get(s).name} (#{d[:how]})" }.join("\n"))
        end
      else break
      end
    end
  }
})
