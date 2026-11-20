#===============================================================================
# Prismfall Mega - 003 Mega Evolution on Prismfall fields
#-------------------------------------------------------------------------------
# 1. The new ability (Reborn's pbAbilitiesOnSwitchIn(true) after a Mega):
#    a field's on-entry rules keyed on abilities (FIELD_API.md 4.6, e.g. Inverse's
#    Magic Bounce +1 Sp. Def, Colosseum's No Guard +1 Attack, Frozen Lake's Thick
#    Fat +1 Defense, Scrapyard's Scrappy +1 Attack) normally run only when a
#    Pokemon enters. A Mega that GAINS such an ability gets the rule now; a rule
#    that already matched its old ability is not run twice.
# 2. Showpieces: PrismfallMega::FIELD_RULES (001), on the current field only.
# Everything else a field does already follows the Mega: type boosts and cuts,
# always-on abilities (:activate_abilities), speed and damage rules read the
# battler as it is now, and a Mega's weather ability (Drought, Sand Stream,
# Snow Warning) starts its weather through the normal path, so field weather
# rules (Volcanic's Sun +3, Frozen Lake's Sun melt...) apply to it.
#===============================================================================
module PrismfallMega
  def self.field_active?(battle)
    return defined?(FieldEffects) && battle.respond_to?(:field_effect) && FieldEffects.active?(battle)
  end

  def self.reapply_entry_abilities(battle, b, old_ability)
    return 0 if !field_active?(battle) || b.fainted? || b.ability_id == old_ability
    n = 0
    FieldEffects.rules(battle, :on_entry).each do |rule|
      spec = rule[:battlers]
      next if !spec || !spec[:abilities]
      list = Array(spec[:abilities])
      next if !list.include?(b.ability_id) || list.include?(old_ability)
      next if !FieldEffects.battler_matches?(spec, battle, b)
      n += 1 if FieldEffects.apply_battler_effect(battle, b, rule)
      break if b.fainted?
    end
    return n
  end

  def self.field_showpieces(battle, b)
    return 0 if !field_active?(battle) || b.fainted?
    rules = FIELD_RULES[FieldEffects.current(battle)]
    return 0 if !rules
    n = 0
    rules.each do |rule|
      next if rule[:battlers] && !FieldEffects.battler_matches?(rule[:battlers], battle, b)
      n += 1 if FieldEffects.apply_battler_effect(battle, b, rule)
      break if b.fainted?
    end
    return n
  end

  #-----------------------------------------------------------------------------
  # Showpiece helpers (FIELD_RULES procs). Each returns true if it did something.
  #-----------------------------------------------------------------------------
  def self.raise_stage(battle, messages)
    id = FieldEffects.current(battle)
    nxt = FieldEffects.stage(battle) + 1
    return false if nxt > FieldEffects.max_stage(id) || !messages[nxt]
    return battle.set_field_stage(nxt, messages[nxt])
  end

  def self.prime_volcano(battle, b)
    st = FieldEffects.state(battle)
    return false if st[:primed]
    st[:primed] = true
    battle.pbDisplay(_INTL("{1}'s Mega Evolution stirred the magma... the volcano is about to erupt!", b.pbThis))
    return true
  end

  def self.colosseum_roar(battle, b)
    st = FieldEffects.state(battle)
    return false if FieldEffects.stage(battle) >= FieldEffects.max_stage(:COLOSSEUM)
    st[:kos] = (st[:kos] || 0) + 1
    battle.pbDisplay(_INTL("The crowd roars at {1}'s Mega Evolution!", b.pbThis(true)))
    return true
  end

  def self.seal_ice(battle, b)
    prog = FieldEffects.transition_progress(battle, :crack)
    return false if !prog || prog[0] <= 0
    FieldEffects.rewind_transitions(battle, { :crack => prog[1] })
    battle.pbDisplay(_INTL("{1}'s frost sealed every crack in the lake ice!", b.pbThis))
    return true
  end

  CRYSTAL_HUES  = [:FIRE, :WATER, :GRASS, :PSYCHIC].freeze
  CRYSTAL_TEXTS = ["The Mega light flooded the crystals! They blaze fiery red!",
                   "The Mega light flooded the crystals! They blaze ocean blue!",
                   "The Mega light flooded the crystals! They blaze vivid green!",
                   "The Mega light flooded the crystals! They blaze amethyst!"].freeze
  def self.flood_crystals(battle, b)
    idx = b.pbTypes(true).map { |t| CRYSTAL_HUES.index(t) }.compact.first
    st = FieldEffects.state(battle)
    return false if idx.nil? || (st[:cc_hue] || 0) == idx
    st[:cc_hue] = idx
    battle.pbDisplay(_INTL(CRYSTAL_TEXTS[idx]))
    return true
  end

  def self.rehaunt(battle, b)
    return false if FieldEffects.stage(battle) != 2
    return battle.set_field_stage(1, _INTL("{1}'s Mega Evolution called the dead back into the nave! The cathedral is haunted again!", b.pbThis))
  end

  def self.lurch_bleed(battle, b)
    return false if !FieldEffects.current_definition(battle)&.[](:borrow)
    battle.pbDisplay(_INTL("{1}'s Mega Evolution tore at the Bleed! The Imprints lurch!", b.pbThis))
    FieldEffects.rotate_borrowed(battle)
    return true
  end
end

EventHandlers.add(:prismfall_mega_evolved, :prismfall_mega_fields,
  proc { |battle, battler, old_ability|
    next if !PrismfallMega.field_active?(battle)
    PrismfallMega.reapply_entry_abilities(battle, battler, old_ability)
    PrismfallMega.field_showpieces(battle, battler)
  }
)

#-------------------------------------------------------------------------------
# Field Notes: a field's Mega lines go after its own notes.
#-------------------------------------------------------------------------------
if defined?(FieldEffects::FieldNotes)
  module FieldEffects
    module FieldNotes
      class << self
        alias prismfall_mega_effect_lines effect_lines unless method_defined?(:prismfall_mega_effect_lines)
        def effect_lines(id)
          ret = prismfall_mega_effect_lines(id)
          (PrismfallMega::FIELD_NOTES[id] || []).each { |n| ret.push(_INTL(n)) }
          ret.push(_INTL(PrismfallMega::GENERAL_NOTE)) if PrismfallMega.ability_entry_rules?(id)
          return ret
        end
      end
    end
  end
end

module PrismfallMega
  # True if the field has on-entry rules keyed on abilities that some Mega form has.
  def self.ability_entry_rules?(id)
    defn = defined?(FieldEffects) ? FieldEffects.get(id) : nil
    return false if !defn || !defn[:on_entry]
    @mega_abilities ||= begin
      list = []
      GameData::Species.each { |sp| list.concat(sp.abilities) if sp.mega_stone || sp.mega_move }
      list.uniq
    end
    return defn[:on_entry].any? { |r| r[:battlers] && (Array(r[:battlers][:abilities]) & @mega_abilities).any? }
  end
end
