# Targeted win-rate cells for the Rev 24 field audit (design/BALANCE.md 9c): a player who brings the weather the old
# rule rewarded, against Gyms 10 (sun: the lake thawed at once), 13 (rain in the cavern) and 15 (sun in the foundry).
#   PRISM_RUN_DIR=<run copy> ruby tools/harness/run_weather_cells.rb [seeds]   (default 10)
load File.join(__dir__, "boot.rb")
load File.join(HARNESS_DIR, "log_scene.rb")
SEEDS = (ARGV[0] || "10").to_i
class Player < Trainer
  def skill_level; 100; end
end
module Harness
  def self.set_badges(count)
    $player.badges = Array.new([$player.badges.length, 18].max) { |i| i < count }
  end
end
def mon(sp, lv, moves, item, nature, ability = nil)
  p = Pokemon.new(sp, lv)
  GameData::Stat.each_main { |s| p.iv[s.id] = 25; p.ev[s.id] = 0 }
  p.ev[:HP] = 85; p.ev[:ATTACK] = 85; p.ev[:SPECIAL_ATTACK] = 85; p.ev[:SPEED] = 85
  p.nature = nature
  p.ability = ability if ability
  p.forget_all_moves
  moves.each { |m| p.learn_move(m) }
  p.item = item
  p.calc_stats
  p
end
TEAMS = {
  # Gym 10 Anja (cap 51): a sun team. Old rule: Drought melted the lake at once.
  10 => lambda { |lv| [mon(:TORKOAL, lv, [:LAVAPLUME, :EARTHPOWER, :SOLARBEAM, :PROTECT], :LEFTOVERS, :MODEST, :DROUGHT),
                       mon(:ARCANINE, lv, [:FLAREBLITZ, :EXTREMESPEED, :CLOSECOMBAT, :WILDCHARGE], :SITRUSBERRY, :ADAMANT),
                       mon(:LUCARIO, lv, [:CLOSECOMBAT, :FLASHCANNON, :EXTREMESPEED, :SWORDSDANCE], :SITRUSBERRY, :JOLLY),
                       mon(:MAGNEZONE, lv, [:THUNDERBOLT, :FLASHCANNON, :VOLTSWITCH, :THUNDERWAVE], :SITRUSBERRY, :MODEST),
                       mon(:VENUSAUR, lv, [:SOLARBEAM, :SLUDGEBOMB, :GROWTH, :SYNTHESIS], :SITRUSBERRY, :MODEST, :CHLOROPHYLL),
                       mon(:HERACROSS, lv, [:CLOSECOMBAT, :MEGAHORN, :STONEEDGE, :EARTHQUAKE], :SITRUSBERRY, :JOLLY)] },
  # Gym 13 Bastian (cap 63): a rain team. Old rule: rain worked in the cavern.
  13 => lambda { |lv| [mon(:PELIPPER, lv, [:SCALD, :HURRICANE, :UTURN, :ROOST], :DAMPROCK, :MODEST, :DRIZZLE),
                       mon(:KINGDRA, lv, [:HYDROPUMP, :DRACOMETEOR, :ICEBEAM, :FLASHCANNON], :SITRUSBERRY, :MODEST, :SWIFTSWIM),
                       mon(:LUDICOLO, lv, [:HYDROPUMP, :GIGADRAIN, :ICEBEAM, :RAINDANCE], :SITRUSBERRY, :MODEST, :SWIFTSWIM),
                       mon(:SWAMPERT, lv, [:WATERFALL, :EARTHQUAKE, :ICEPUNCH, :STEALTHROCK], :LEFTOVERS, :ADAMANT),
                       mon(:LUCARIO, lv, [:CLOSECOMBAT, :FLASHCANNON, :EXTREMESPEED, :SWORDSDANCE], :SITRUSBERRY, :JOLLY),
                       mon(:FERROTHORN, lv, [:POWERWHIP, :GYROBALL, :LEECHSEED, :PROTECT], :LEFTOVERS, :BRAVE)] },
  # Gym 15 Magnus (cap 71): a sun team. Old rule: sun lasted 7 turns in the foundry.
  15 => lambda { |lv| [mon(:TORKOAL, lv, [:LAVAPLUME, :EARTHPOWER, :SOLARBEAM, :PROTECT], :LEFTOVERS, :MODEST, :DROUGHT),
                       mon(:ARCANINE, lv, [:FLAREBLITZ, :EXTREMESPEED, :CLOSECOMBAT, :WILDCHARGE], :SITRUSBERRY, :ADAMANT),
                       mon(:CHANDELURE, lv, [:FLAMETHROWER, :SHADOWBALL, :ENERGYBALL, :CALMMIND], :SITRUSBERRY, :MODEST),
                       mon(:VENUSAUR, lv, [:SOLARBEAM, :SLUDGEBOMB, :EARTHPOWER, :SYNTHESIS], :SITRUSBERRY, :MODEST, :CHLOROPHYLL),
                       mon(:GARCHOMP, lv, [:EARTHQUAKE, :DRAGONCLAW, :FIREFANG, :SWORDSDANCE], :SITRUSBERRY, :JOLLY),
                       mon(:GYARADOS, lv, [:WATERFALL, :EARTHQUAKE, :DRAGONDANCE, :CRUNCH], :SITRUSBERRY, :ADAMANT)] }
}
Harness.new_game_state
Prismfall.record_starter(:CHARMANDER)
Prismfall::Difficulty.set(:STANDARD) rescue nil
TEAMS.each do |gym, team|
  g = Prismfall.gym(gym)
  wins = 0; seqs = Hash.new(0)
  SEEDS.times do |s|
    Harness.set_badges(gym - 1)
    $player.party = team.call(g[:cap])
    log = Harness.run_battle("weather G#{gym} s#{s}", :seed => 7000 + gym * 31 + s,
                             :setup => proc { |b| b.ally_items = [[:HYPERPOTION, :HYPERPOTION, :FULLHEAL]] }) do
      Prismfall.gym_battle(gym, :can_lose => true)
    end
    wins += 1 if log.outcome == 1
    seqs[log.field_changes.map { |o, n, st| (o == n) ? "#{n}#{st}" : n.to_s }.join(">")] += 1
  end
  puts format("WEATHER G%-3d won %2d/%d  fields %s", gym, wins, SEEDS, seqs.map { |k, v| "#{v}x #{k}" }.join(" | "))
end
