#===============================================================================
# Giratina (Origin) tests the Renegade - the Ruin Route, R1 "Twenty-Three
# Graves" (the graves floor under Giratina's Reverse Depths 806;
# story/12_RUIN_ROUTE.md R1 beat 5, design/NARRATIVE_KEYS.md section 7
# "boss config GIRATINA_ORIGIN_TRIAL ... on :INVERSE"). After the Reflection's
# mirror battle: "a multi-bar trial, not a hunt. It ends when the PC stops
# attacking for one turn."
#   * Origin Forme from the start (Griseous Core), Lv 72, on :INVERSE.
#     Bars: Casual 2, Standard 3, Hard 4. Uncatchable (no main-story
#     legendaries; the post-game Distortion Core is where it is caught).
#   * The trial. Giratina first makes the Renegade fight: restraint counts only
#     once ORIGIN_TRIAL_ARMED_AFTER bars are broken (Casual / Standard 1, Hard
#     2). From then on, the first round in which none of the player's own
#     Pokemon chooses a move aimed at the foe (a switch, an item, a move on
#     itself or its side all count as holding back) ends the battle as a win,
#     result :restraint. A Pokemon that was only stopped (asleep, flinched,
#     recharging) did not hold back: the CHOICE is what is read.
#   * Breaking every bar also ends it (it doesn't faint or flee), result
#     :overpowered: the story may read the difference
#     (Prismfall::Bosses.last_result[:result]); R1's beat 6 follows either way.
#   Script: Prismfall::Bosses.wild_battle(:GIRATINA_ORIGIN_TRIAL)
# Casual only is eased (HP x0.75, offence x0.6, like the other legend bosses);
# Standard and Hard are as designed.
# Harness: tools/harness/winrates_r4.rb cell BORI (the AI never holds back, so
# its numbers are the :overpowered road).
#===============================================================================
module Prismfall
  module Bosses
    ORIGIN_TRIAL_ARMED_AFTER = { :CASUAL => 1, :STANDARD => 1, :HARD => 2 }

    def self.origin_trial_armed?(st)
      return st.breaks_done >= (resolve(ORIGIN_TRIAL_ARMED_AFTER) || 1)
    end

    # True if, this round, every one of the player's own battlers chose something other than a move aimed at the foe.
    def self.player_held_back?(battle)
      chose = false
      battle.battlers.each do |b|
        next if !b || b.opposes? || !battle.pbOwnedByPlayer?(b.index)
        ch = battle.choices[b.index]
        next if !ch || ch[0] == :None
        chose = true
        next if ch[0] != :UseMove
        move = ch[2]
        next if !move
        return false if move.damagingMove?
        hostile = (move.pbTarget(b).targets_foe rescue true)
        return false if hostile
      end
      return chose
    end

    ORIGIN_TRIAL_END_OF_ROUND = proc { |battle, b, st|
      bs = Prismfall::Bosses
      next if !bs.origin_trial_armed?(st) || b.fainted?
      next if !bs.player_held_back?(battle)
      ["You hold your hand still. Nothing strikes.",
       "{1} stops with you. It was waiting for that.",
       "It lowers its head through the black glass. The trial is over."].each do |m|
        battle.pbDisplay(bs.text(m, b.pbThis))
      end
      st.result = :restraint
      st.end_decision = 1
    }

    # Shown at the break that arms the trial (the only tell the player gets).
    ORIGIN_TRIAL_HINT = {
      :condition => proc { |_battle, _b, st| st.breaks_done == (Prismfall::Bosses.resolve(ORIGIN_TRIAL_ARMED_AFTER) || 1) },
      :messages  => ["{1} is not watching your Pokémon. It is watching your hand.",
                     "It is waiting to see whether you can stop."]
    }.freeze
  end
end

Prismfall::Bosses.register(:GIRATINA_ORIGIN_TRIAL, {
  :species    => :GIRATINA,
  :form       => 1,
  :item       => :GRISEOUSCORE,     # the Gen 9 form handler: no Core, no Origin Forme
  :level      => 72,
  :ability    => :LEVITATE,
  :nature     => :ADAMANT,
  :ivs        => 31,
  :evs        => { :HP => 252, :ATTACK => 252, :SPECIAL_DEFENSE => 4 },
  :moves      => { :CASUAL  => [:SHADOWCLAW, :DRAGONCLAW, :SHADOWSNEAK, :ANCIENTPOWER],
                   :default => [:POLTERGEIST, :DRAGONCLAW, :SHADOWSNEAK, :EARTHQUAKE] },
  :bars       => { :CASUAL => 2, :STANDARD => 3, :HARD => 4 },
  :stat_mults => { :CASUAL => { :HP => 0.75, :ATTACK => 0.6, :SPECIAL_ATTACK => 0.6 },
                   :HARD   => { :DEFENSE => 1.15, :SPECIAL_DEFENSE => 1.15 } },
  :field      => :INVERSE,
  :catch      => false,
  :intro      => ["The twenty-three graves turn over, all at once...",
                  "Giratina rises through the floor in its true shape, and looks at the Renegade!"],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    1 => { :CASUAL  => [{ :messages => ["The black glass rings like a struck bell!"] },
                        Prismfall::Bosses::ORIGIN_TRIAL_HINT],
           :default => [{ :messages => ["The black glass rings like a struck bell! {1} presses harder!"],
                          :stats => { :ATTACK => 1 } },
                        Prismfall::Bosses::ORIGIN_TRIAL_HINT] },
    2 => [{ :messages => ["The graves' names run like wet ink. {1} moves faster through them!"],
            :stats => { :SPEED => 1 } },
          Prismfall::Bosses::ORIGIN_TRIAL_HINT],
    3 => { :messages => ["{1} stops holding anything back!"],
           :stats => { :ATTACK => 1 }, :clear_hazards => true }
  },
  :end_of_round => Prismfall::Bosses::ORIGIN_TRIAL_END_OF_ROUND,
  :on_defeat  => [
    { :messages => ["{1} cannot be struck down here. It simply stops.",
                    "You never held your hand. It saw that, too.",
                    "It lowers its head through the black glass. The trial is over."],
      :end_battle => 1, :result => :overpowered }
  ],
  :description => "Ruin R1 graves floor (under 806): Giratina-Origin tests the Renegade on Inverse; ends when the player holds back a round"
})
