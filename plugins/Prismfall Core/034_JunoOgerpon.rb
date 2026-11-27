#===============================================================================
# Prismfall Core - 034 Juno's Ogerpon at the Festival (J4)
#-------------------------------------------------------------------------------
# OGERPON_TRUSTED (choice(:ch10_ogre) == :ogre; S223): the Gossamer Ogre stays with
# Juno after Ch10 and fights for her at the Festival (story/08_ACT_V.md "Juno (J4,
# fallback)", story/39_SCRIPT_CH20.md: "on *her* team: a Warden's partner, not the
# PC's"). Juno is main cast, so a legendary on her team is allowed; nothing is
# given to the player (Core 027's catch gate is untouched).
#
# J4 = RIVAL_JUNO versions 40-42 (Standard), 140-142 (Hard), 240-242 (Casual), i.e.
# Prismfall::Rival.version_for(4) plus the difficulty offset. Ogerpon (Teal Mask:
# the masks are the post-game's) takes Lilligant's slot, in place: Florges
# "Everbloom", Gardevoir "Veil" (her first Mega), the starter (Core 006 swaps it)
# and Tsareena "Sweetpea" (the ace) are fixed by the story, and Lilligant is the
# other unnamed Grass attacker. It keeps the slot's held item, IVs and EVs (the
# difficulty's own settings), except Hard's physical spread; one level over the
# slot on Standard / Hard, the slot's level on Casual.
# Hook: :on_trainer_load (TrainerBattle.start fires it for every trainer it
# loads), like PrismfallMega.morwen_ring_swap.
#===============================================================================
module Prismfall
  module JunoOgerpon
    TRAINER  = :RIVAL_JUNO
    BATTLE   = 4              # J4: (version % 100) / 10 == 4
    SPECIES  = :OGERPON
    REPLACES = :LILLIGANT
    FLAG     = :OGERPON_TRUSTED
    SETS = {
      :STANDARD => { :level => 1, :moves => [:IVYCUDGEL, :PLAYROUGH, :KNOCKOFF, :SPIKYSHIELD] },
      :HARD     => { :level => 1, :moves => [:IVYCUDGEL, :PLAYROUGH, :KNOCKOFF, :SWORDSDANCE],
                     :ev => { :HP => 4, :ATTACK => 252, :SPEED => 252 } },
      :CASUAL   => { :level => 0, :moves => [:IVYCUDGEL, :PLAYROUGH, :LOWSWEEP, :SYNTHESIS] }
    }.freeze

    def self.trusted?
      return false if !defined?(Prismfall::Narrative)
      return (Prismfall::Narrative.flag(FLAG) rescue false) ? true : false
    end

    def self.j4?(trainer)
      return false if !trainer.respond_to?(:trainer_type) || trainer.trainer_type != TRAINER
      return false if !trainer.respond_to?(:version) || !trainer.version.is_a?(Integer)
      return (trainer.version % 100) / 10 == BATTLE
    end

    # The difficulty of the version that was actually loaded (+100 Hard, +200 Casual).
    def self.set_for(version)
      return SETS[:CASUAL] if version >= 200
      return SETS[:HARD] if version >= 100
      return SETS[:STANDARD]
    end

    # Returns the Ogerpon put in, or nil. force = true skips the OGERPON_TRUSTED check (tests).
    def self.apply(trainer, force = false)
      return nil if !j4?(trainer) || !trainer.respond_to?(:party)
      return nil if !force && !trusted?
      return nil if trainer.party.any? { |p| p && p.isSpecies?(SPECIES) }
      i = trainer.party.index { |p| p && p.isSpecies?(REPLACES) }
      return nil if !i
      old = trainer.party[i]
      set = set_for(trainer.version)
      pkmn = Pokemon.new(SPECIES, [old.level + set[:level], GameData::GrowthRate.max_level].min, trainer)
      pkmn.form = 0
      pkmn.ability = :DEFIANT
      pkmn.nature = :JOLLY
      pkmn.item = old.item_id
      GameData::Stat.each_main do |s|
        pkmn.iv[s.id] = old.iv[s.id]
        pkmn.ev[s.id] = (set[:ev]) ? (set[:ev][s.id] || 0) : old.ev[s.id]
      end
      pkmn.forget_all_moves
      set[:moves].each { |m| pkmn.learn_move(m) if GameData::Move.exists?(m) }
      pkmn.shiny = false
      pkmn.calc_stats
      pkmn.heal
      trainer.party[i] = pkmn
      return pkmn
    end
  end
end

EventHandlers.add(:on_trainer_load, :prismfall_juno_ogerpon,
  proc { |trainer|
    Prismfall::JunoOgerpon.apply(trainer) if trainer
  }
)
