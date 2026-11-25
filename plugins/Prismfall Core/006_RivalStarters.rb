#===============================================================================
# Prismfall Core - 006 Rival starter system
#-------------------------------------------------------------------------------
# SPINE (LOCKED):
#   * Rival battle base version = battle_number * 10 + starter_slot
#     (slot 0 = player chose Grass, 1 = Fire, 2 = Water).
#   * PBS writes the rival's starter as the Gen 1 line. At battle start the
#     Gen 1 starter-line Pokémon is swapped to the same-generation counterpart
#     of the player's starter (same evolution stage); level-up moves are
#     regenerated, item/nature/EVs/IVs/shininess/nickname kept.
#
# Hook: EventHandlers :on_trainer_load (fires for TrainerBattle foes and
# registered partners), so it works with or without EBDX.
#===============================================================================
module Prismfall
  module Rival
    #---------------------------------------------------------------------------
    # Starter table lookup
    #---------------------------------------------------------------------------
    # species => { :gen, :slot, :stage }
    def self.table
      if !@table
        @table = {}
        STARTER_LINES.each do |gen, lines|
          lines.each_with_index do |line, slot|
            line.each_with_index do |species, stage|
              @table[species] = { :gen => gen, :slot => slot, :stage => stage }
            end
          end
        end
      end
      return @table
    end

    def self.lookup(species)
      species = species.species if species.respond_to?(:species) && !species.is_a?(Symbol)
      species = species.to_sym if species.is_a?(String)
      return table[species]
    end

    def self.line(gen, slot)
      lines = STARTER_LINES[gen]
      return (lines) ? lines[slot] : nil
    end

    # Validates every species in STARTER_LINES against the compiled data.
    # Returns an array of missing species IDs (empty = all good).
    def self.missing_species
      return table.keys.reject { |sp| GameData::Species.exists?(sp) }
    end

    #---------------------------------------------------------------------------
    # Player's starter
    #---------------------------------------------------------------------------
    # Event usage, right after the player receives their starter:
    #   Prismfall.record_starter(:CYNDAQUIL)
    #   Prismfall.record_starter($player.party[0])
    # For an off-table starter, pass gen:/slot: explicitly:
    #   Prismfall.record_starter(:PIKACHU, gen: 1, slot: 1)
    def self.record_starter(pkmn_or_species, gen: nil, slot: nil)
      species = pkmn_or_species
      species = pkmn_or_species.species if pkmn_or_species.is_a?(Pokemon)
      species = GameData::Species.get(species).species
      info = lookup(species)
      gen  ||= (info) ? info[:gen] : DEFAULT_STARTER_GEN
      slot ||= (info) ? info[:slot] : DEFAULT_STARTER_SLOT
      raise ArgumentError, "Starter slot must be 0 (Grass), 1 (Fire) or 2 (Water)" if !(0..2).include?(slot)
      raise ArgumentError, "No starter lines defined for Gen #{gen}" if !STARTER_LINES[gen]
      Prismfall.state.starter = {
        :species  => species,
        :gen      => gen,
        :slot     => slot,
        :stage    => (info) ? info[:stage] : 0,
        :inferred => false
      }
      return Prismfall.state.starter
    end

    # Looks through the player's Pokémon for the earliest-received starter-line
    # Pokémon originally caught by the player. Used if no starter was recorded.
    def self.infer_starter
      return nil if !$player
      best = nil
      best_time = nil
      check = lambda do |pkmn|
        next if !pkmn || pkmn.egg?
        info = lookup(pkmn.species)
        next if !info
        next if pkmn.owner && pkmn.owner.id != $player.id
        t = pkmn.timeReceived.to_i
        if best.nil? || t < best_time
          best = [pkmn.species, info]
          best_time = t
        end
      end
      $player.party.each { |pkmn| check.call(pkmn) }
      pbEachPokemon { |pkmn, _box| check.call(pkmn) } if $PokemonStorage
      return nil if !best
      return { :species => best[0], :gen => best[1][:gen], :slot => best[1][:slot],
               :stage => best[1][:stage], :inferred => true }
    end

    def self.starter_info
      st = Prismfall.state
      return st.starter if st.starter.is_a?(Hash)
      inferred = infer_starter
      if inferred
        st.starter = inferred   # persist so it stays stable
        return inferred
      end
      return { :species => nil, :gen => DEFAULT_STARTER_GEN, :slot => DEFAULT_STARTER_SLOT,
               :stage => 0, :inferred => true }
    end

    def self.starter_slot; return starter_info[:slot]; end
    def self.starter_gen;  return starter_info[:gen];  end
    def self.starter_species; return starter_info[:species]; end
    def self.starter_type; return STARTER_SLOT_TYPES[starter_slot]; end

    # Slot of the starter each rival picks (for cutscenes, dialogue, sprites).
    #   Kestrel: type advantage over the player's starter
    #   Juno:    weak to the player's starter
    def self.kestrel_slot; return (starter_slot + 1) % 3; end
    def self.juno_slot;    return (starter_slot + 2) % 3; end

    # Species a rival is using at the given evolution stage, in the player's
    # starter generation. rival = :KESTREL or :JUNO
    def self.rival_starter_species(rival, stage = 0)
      slot = (rival.to_s.upcase.include?("JUNO")) ? juno_slot : kestrel_slot
      ln = line(starter_gen, slot) || line(RIVAL_SOURCE_GEN, slot)
      return ln[stage.clamp(0, ln.length - 1)]
    end

    #---------------------------------------------------------------------------
    # Rival battles
    #---------------------------------------------------------------------------
    # Standard base version for rival battle N (difficulty offset is added by
    # the pbLoadTrainer hook, with fallback to this base version).
    def self.version_for(battle_number)
      return battle_number * 10 + starter_slot
    end

    # A rival who fights BESIDE the player with their own team (not one of the
    # numbered rival battles) uses the spare versions of a decade:
    #   decade * 10 + 3 + starter_slot   (x3 Grass, x4 Fire, x5 Water)
    # so the partner's starter still follows the player's pick and never
    # collides with a rival battle (K2 already owns 20-22, so the Ch21
    # "version 21" could not be used). Partners have one version: there is no
    # +100 / +200, and the pbLoadTrainer hook falls back to this one.
    #   pbRegisterPartner(:RIVAL_KESTREL, "Kestrel", Prismfall::Rival.partner_version(9))
    #   -> 93 / 94 / 95, Redeemed Kestrel beside the PC in Ch21.
    PARTNER_VERSION_OFFSET = 3
    def self.partner_version(decade)
      return decade * 10 + PARTNER_VERSION_OFFSET + starter_slot
    end

    # Event usage:
    #   Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 3)
    #   Prismfall.rival_battle(:RIVAL_JUNO, "Juno", 2, can_lose: true, lose_text: "...")
    #   Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 4, field: :COLOSSEUM, double: true)
    # Returns true if the player won.
    def self.battle(trainer_type, trainer_name, battle_number, lose_text: nil, can_lose: false,
                    double: false, field: nil, outcome_var: nil)
      version = version_for(battle_number)
      setBattleRule("canLose") if can_lose
      setBattleRule("double") if double
      setBattleRule("outcomeVar", outcome_var) if outcome_var
      Prismfall.set_field_rule(field) if field
      return TrainerBattle.start([trainer_type, trainer_name, version, lose_text])
    end

    #---------------------------------------------------------------------------
    # Starter swap
    #---------------------------------------------------------------------------
    def self.rival_trainer?(trainer)
      return false if !trainer.respond_to?(:trainer_type)
      return RIVAL_TRAINER_TYPES.include?(trainer.trainer_type)
    end

    # Swaps every Gen 1 starter-line Pokémon in a rival's party.
    # Returns the number of Pokémon swapped.
    def self.swap_trainer_party(trainer)
      return 0 if !RIVAL_SWAP_ENABLED || !trainer || !rival_trainer?(trainer)
      target_gen = starter_gen
      return 0 if target_gen == RIVAL_SOURCE_GEN || !STARTER_LINES[target_gen]
      count = 0
      trainer.party.each do |pkmn|
        next if !pkmn || pkmn.egg?
        info = lookup(pkmn.species)
        next if !info || info[:gen] != RIVAL_SOURCE_GEN
        new_line = line(target_gen, info[:slot])
        next if !new_line
        new_species = new_line[info[:stage]] || new_line.last
        next if !GameData::Species.exists?(new_species)
        swap_species(pkmn, new_species)
        count += 1
      end
      return count
    end

    # Changes pkmn into new_species at the same level, keeping item (Mega Stones
    # remapped), nature, EVs, IVs, shininess, nickname, gender where possible and
    # the ability slot. Level-up moves are regenerated for the new species.
    def self.swap_species(pkmn, new_species)
      old_species = pkmn.species
      level       = pkmn.level
      abil_index  = ability_slot_of(pkmn)
      old_item    = pkmn.item_id
      pkmn.species = new_species
      pkmn.level = level
      pkmn.ability_index = abil_index
      pkmn.item = remap_item(old_item, old_species, new_species)
      pkmn.reset_moves
      pkmn.calc_stats
      pkmn.heal
      return pkmn
    end

    # Index of the Pokémon's current ability in its species' list (0/1, or
    # 2+ for hidden abilities), so a PBS "Ability = X" maps to the same slot.
    def self.ability_slot_of(pkmn)
      sp = pkmn.species_data
      abil = pkmn.ability_id
      idx = sp.abilities.index(abil)
      return idx if idx
      idx = sp.hidden_abilities.index(abil)
      return 2 + idx if idx
      return pkmn.ability_index
    end

    def self.mega_stones_for(species)
      stones = []
      GameData::Species.each do |sp|
        next if sp.species != species || !sp.mega_stone
        stones.push(sp.mega_stone) if !stones.include?(sp.mega_stone)
      end
      return stones
    end

    def self.remap_item(item, old_species, new_species)
      return item if !item
      item_data = GameData::Item.try_get(item)
      # Black Sludge hurts a non-Poison holder: a Venusaur swapped into Meganium/Sceptile/... gets Leftovers
      if item_data && item_data.id == :BLACKSLUDGE
        sp = GameData::Species.try_get(new_species)
        return :LEFTOVERS if sp && !sp.types.include?(:POISON)
      end
      return item if !item_data || !item_data.is_mega_stone?
      old_stones = mega_stones_for(old_species)
      return item if !old_stones.include?(item_data.id)   # not this species' stone
      new_stones = mega_stones_for(new_species)
      if new_stones.length > 0
        idx = old_stones.index(item_data.id) || 0
        return new_stones[idx] || new_stones[0]
      end
      fallback = MEGA_STONE_FALLBACK_ITEM
      return (fallback && GameData::Item.exists?(fallback)) ? fallback : nil
    end
  end

  def self.rival_battle(trainer_type, trainer_name, battle_number, **kwargs)
    return Rival.battle(trainer_type, trainer_name, battle_number, **kwargs)
  end

  def self.record_starter(pkmn_or_species, **kwargs)
    return Rival.record_starter(pkmn_or_species, **kwargs)
  end
end

EventHandlers.add(:on_trainer_load, :prismfall_rival_starter_swap,
  proc { |trainer|
    Prismfall::Rival.swap_trainer_party(trainer) if trainer
  }
)
