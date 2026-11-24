#===============================================================================
# The Loyal Three at the Bride Grove (map 708, Chapter 10 "The Seat That
# Blooms"; story/28_SCRIPT_CH10.md "The Loyal Three", key event 2). Three wild
# bosses in a row: Okidogi, then Munkidori, then Fezandipiti, collars glowing
# Sweetrot pink. Field: Bleed. Never caught here (no main-story legendaries:
# they flee when the collars crack; the post-game Gloamwood Masks board hands
# them out), so :catch => false on all three and Core 027_LegendaryGate.rb
# under that.
#   :ch10_ogre == :ogre      -> the Ogre fights beside you (PARTNER_OGRE:
#                               Ogerpon, Teal Mask, Lv 48, AI-controlled; a 2v1)
#   :ch10_ogre == :hesitate  -> the PC alone (the same bars; the penalty is losing the partner)
#   Script: Prismfall::Bosses.loyal_three   (partner chosen from :ch10_ogre)
#   Afterwards (win): S127 CH10_LOYAL_THREE_DONE, V131 = 7 (the event sets them).
# The party is healed between bosses (the Ogre's grove berries); a loss ends
# the sequence (whiteout; the trial restarts at the stairhead).
# Levels under the Ch10 cap (51): 48 / 49 / 50. Bars: Casual 1, Standard 2,
# Hard 3. Toxic Chain on all three (the collars). Hard's "second Pokemon at
# its side" when alone is not built yet (TODO_QUOTA.md).
# Harness (winrates_r4.rb cells L3O L3M L3F L3OA L3FA; typical Lv 49-51 six, 60
# fights a cell): with the Ogre Standard 75 / 95 / 98%, alone Okidogi 53% and
# Fezandipiti 92%; Hard typical 18 / 40 / 58% (alone 5 / 57%), Hard prepared
# 90-100%; Casual 100%. Okidogi is the gate (no Bulk Up: it snowballed).
#===============================================================================
module Prismfall
  module Bosses
    LOYAL_THREE = [:LOYAL_THREE_OKIDOGI, :LOYAL_THREE_MUNKIDORI, :LOYAL_THREE_FEZANDIPITI].freeze
    LOYAL_THREE_PARTNER = [:PARTNER_OGRE, "Ogre", 0]

    def self.loyal_three_alone?
      choice = (defined?(Prismfall::Choices) ? (Prismfall::Choices.get(:ch10_ogre) rescue nil) : nil)
      return choice != :ogre
    end

    LOYAL_THREE_BARS = { :CASUAL => 1, :STANDARD => 2, :HARD => 3 }
    LOYAL_THREE_MULTS = {
      :CASUAL   => { :HP => 1.1 },
      :STANDARD => { :HP => 1.5, :ATTACK => 1.25, :SPECIAL_ATTACK => 1.25, :DEFENSE => 1.15, :SPECIAL_DEFENSE => 1.15 },
      :HARD     => { :HP => 1.5, :ATTACK => 1.25, :SPECIAL_ATTACK => 1.25, :DEFENSE => 1.2, :SPECIAL_DEFENSE => 1.2 }
    }

    # Runs the three fights; returns true only if all three are won.
    def self.loyal_three(partner: nil)
      partner = !loyal_three_alone? if partner.nil?
      partner = false if !GameData::TrainerType.exists?(LOYAL_THREE_PARTNER[0])
      begin
        LOYAL_THREE.each_with_index do |id, i|
          loyal_three_partner_rules if partner
          won = wild_battle(id)
          return false if !won
          $player.heal_party if i < LOYAL_THREE.length - 1 && $player   # the Ogre's grove berries
        end
      ensure
        pbDeregisterPartner if partner
      end
      return true
    end

    # One wild boss with the Ogre beside you: a 2v1 (v21 only lets a partner into a one-foe wild battle with a
    # size rule that isn't 1vN). Re-registered each fight, so the Ogre comes back fresh.
    def self.loyal_three_partner_rules
      pbRegisterPartner(*LOYAL_THREE_PARTNER)
      setBattleRule("2v1")
    end
  end
end

Prismfall::Bosses.register(:LOYAL_THREE_OKIDOGI, {
  :species    => :OKIDOGI,
  :level      => 48,
  :ability    => :TOXICCHAIN,
  :nature     => :ADAMANT,
  :ivs        => 20,
  :evs        => { :HP => 252, :DEFENSE => 128, :SPECIAL_DEFENSE => 128 },
  :moves      => [:POISONJAB, :FORCEPALM, :LOWKICK, :BITE],
  :bars       => Prismfall::Bosses::LOYAL_THREE_BARS,
  # No Bulk Up (with the break's +1 Attack it snowballed: Hard 3% alone); less raw Attack than its siblings (harness).
  :stat_mults => { :CASUAL   => { :HP => 1.1 },
                   :STANDARD => { :HP => 1.5, :ATTACK => 1.15, :DEFENSE => 1.15, :SPECIAL_DEFENSE => 1.15 },
                   :HARD     => { :HP => 1.5, :ATTACK => 1.1, :DEFENSE => 1.2, :SPECIAL_DEFENSE => 1.2 } },
  :field      => :BLEED,
  :catch      => false,
  :can_lose   => false,
  :intro      => ["The dog's collar blazes pink! Okidogi bares its teeth at the Plate!"],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    1 => { :messages => ["The chain round Okidogi's middle pulls tight! Its muscles swell!"],
           :stats => { :ATTACK => 1 }, :learn => { 3 => :BRUTALSWING } },
    2 => { :messages => ["Okidogi howls, and the grove's roots shake!"], :stats => { :DEFENSE => 1 } }
  },
  :on_defeat  => [{ :messages => ["Okidogi staggers back into the bloom, its collar flickering..."] }],
  :description => "Ch10 Bride Grove (708): the Loyal Three, 1 of 3 (Okidogi); uncatchable, flees"
})

Prismfall::Bosses.register(:LOYAL_THREE_MUNKIDORI, {
  :species    => :MUNKIDORI,
  :level      => 49,
  :ability    => :TOXICCHAIN,
  :nature     => :TIMID,
  :ivs        => 20,
  :evs        => { :HP => 252, :SPECIAL_DEFENSE => 252 },
  :moves      => [:PSYBEAM, :CLEARSMOG, :FAKEOUT, :FLATTER],
  :bars       => Prismfall::Bosses::LOYAL_THREE_BARS,
  :stat_mults => Prismfall::Bosses::LOYAL_THREE_MULTS,
  :field      => :BLEED,
  :catch      => false,
  :intro      => ["The monkey's painted face splits into a grin. Munkidori's eyes slide to the green light!"],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    1 => { :messages => ["Munkidori's collar pulses! Its mind reaches for yours!"],
           :learn => { 0 => :PSYCHIC } },
    2 => { :messages => ["Munkidori drinks the Sweetrot in the air!"],
           :learn => { 1 => :SLUDGEWAVE }, :stats => { :SPECIAL_ATTACK => 1 } }
  },
  :on_defeat  => [{ :messages => ["Munkidori shrieks and scrambles up into the branches..."] }],
  :description => "Ch10 Bride Grove (708): the Loyal Three, 2 of 3 (Munkidori); uncatchable, flees"
})

Prismfall::Bosses.register(:LOYAL_THREE_FEZANDIPITI, {
  :species    => :FEZANDIPITI,
  :level      => 50,
  :ability    => :TOXICCHAIN,
  :nature     => :JOLLY,
  :ivs        => 20,
  :evs        => { :HP => 252, :DEFENSE => 128, :SPEED => 128 },
  :moves      => [:CROSSPOISON, :WINGATTACK, :DISARMINGVOICE, :ATTRACT],
  :bars       => Prismfall::Bosses::LOYAL_THREE_BARS,
  :stat_mults => Prismfall::Bosses::LOYAL_THREE_MULTS,
  :field      => :BLEED,
  :catch      => false,
  :intro      => ["The pheasant fans its tail like a court lady. The peach smell grows thick enough to taste..."],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    1 => { :messages => ["Fezandipiti spreads its tail! For a second you'd agree with anyone about anything..."],
           :learn => { 3 => :FLATTER } },
    2 => { :messages => ["The Ogre's club comes down, and the smell breaks!", "Fezandipiti's collar cracks down the middle!"],
           :learn => { 2 => :TAILSLAP }, :stats => { :SPEED => 1 } }
  },
  :on_defeat  => [{ :messages => ["The three collars crack. All at once. The pink goes out of them like a lamp blown out."] }],
  :description => "Ch10 Bride Grove (708): the Loyal Three, 3 of 3 (Fezandipiti); uncatchable, flees"
})
