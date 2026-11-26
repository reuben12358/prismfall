#===============================================================================
# The Eighteen Locks, battle side - the forced-lock beat and the unasked bars
# (Bosses 103 :ARCEUS_FINALE; story/11_FINALE_LINES.md section 2, the staging
# in story/40_SCRIPT_CH21.md "The True Finale").
#   The kneels themselves (each Warden's release or refusal line, the stage
#   directions, the lock opening or staying shut, the record V118 / lock_state)
#   are Core 033_Finale.rb's Finale.kneel_bar on :prismfall_arceus_locks, as a
#   bar starts. This file adds what plays around them:
#   * the bar breaks (:prismfall_arceus_locks_broken): each refused lock is
#     broken by force: "the Warden is thrown back from the pylon and the Plate
#     tears free with a crack of Bleed light. No line." (11 section 2); the
#     Finale record marks the lock :forced;
#   * War ("the shard eats the types") and Judgment ("No Warden releases
#     anything; all eighteen locks hold", story/12_RUIN_ROUTE.md R7) ask
#     nobody: one line a bar instead of the kneels, and every Plate tears free
#     without a Warden at the pylon.
#===============================================================================
module Prismfall
  module Bosses
    ARCEUS_TYPE_PLATES = {
      :NORMAL => :BLANKPLATE, :BUG => :INSECTPLATE, :WATER => :SPLASHPLATE, :ELECTRIC => :ZAPPLATE,
      :GROUND => :EARTHPLATE, :POISON => :TOXICPLATE, :FIRE => :FLAMEPLATE, :FIGHTING => :FISTPLATE,
      :GRASS => :MEADOWPLATE, :ICE => :ICICLEPLATE, :FLYING => :SKYPLATE, :PSYCHIC => :MINDPLATE,
      :ROCK => :STONEPLATE, :GHOST => :SPOOKYPLATE, :STEEL => :IRONPLATE, :DARK => :DREADPLATE,
      :FAIRY => :PIXIEPLATE, :DRAGON => :DRACOPLATE
    }.freeze

    # One line a bar when nobody is asked (in place of the kneels).
    ARCEUS_UNASKED_LINES = {
      :ARCEUS_WAR      => "The shard in your chest pulls at the locks before anyone can kneel. Nobody is asked.",
      :ARCEUS_JUDGMENT => "No Warden kneels. All three locks hold."
    }.freeze

    def self.arceus_gym_plate_name(gym)
      g = Prismfall.gym(gym)
      it = g && ARCEUS_TYPE_PLATES[g[:type]]
      return GameData::Item.get(it).name if it && GameData::Item.exists?(it)
      return (g) ? _INTL("{1} Plate", GameData::Type.get(g[:type]).name) : _INTL("Plate")
    end

    # Who stands at a refused pylon: the Warden, or Corvin's Choir porter.
    def self.arceus_pylon_holder(gym)
      return _INTL("The porter") if gym == 6
      g = Prismfall.gym(gym)
      return (g) ? g[:trainer_name] : _INTL("The Warden")
    end

    def self.arceus_unasked_beat(battle, _bar, gyms, _forced)
      line = ARCEUS_UNASKED_LINES[arceus_variant[:id]]
      battle.pbDisplay(_INTL(line)) if line && !gyms.empty? && battle.decision == 0
    end

    def self.arceus_forced_beats(battle, _bar, gyms, forced, _final)
      return if battle.decision != 0
      unasked = ARCEUS_UNASKED_LINES.key?(arceus_variant[:id])
      gyms.each do |n|
        next if !forced.include?(n)
        plate = arceus_gym_plate_name(n)
        if unasked
          battle.pbDisplay(_INTL("The {1} tears free in a crack of Bleed light!", plate))
        else
          battle.pbDisplay(_INTL("{1} is thrown back from the pylon! The {2} tears free in a crack of Bleed light!",
                                 arceus_pylon_holder(n), plate))
        end
        if defined?(Prismfall::Finale) && Prismfall::Finale.respond_to?(:locks)
          Prismfall::Finale.locks[n] = :forced
        end
      end
    end
  end
end

EventHandlers.add(:prismfall_arceus_locks, :prismfall_arceus_unasked,
  proc { |battle, bar, gyms, forced| Prismfall::Bosses.arceus_unasked_beat(battle, bar, gyms || [], forced || []) }
)

EventHandlers.add(:prismfall_arceus_locks_broken, :prismfall_arceus_forced_beats,
  proc { |battle, bar, gyms, forced, final| Prismfall::Bosses.arceus_forced_beats(battle, bar, gyms || [], forced || [], final) }
)
