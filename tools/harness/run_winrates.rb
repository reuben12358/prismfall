#===============================================================================
# Prismfall realistic win-rate test (trainer workstream; companion to run_trainers.rb).
#   PRISM_RUN_DIR=<private run dir> PRISM_OUT=<out dir> PRISM_COMPILE=1 ruby tools/harness/run_winrates.rb
# Real Essentials v21.1 battle code + Prismfall plugins, AI on both sides. Logic test only.
#
# The challenger is a REALISTIC player, not an ideal-counter team: a starter plus what design/POKEMON_AVAILABILITY.md
# and design/EVENT_POKEMON.md make available before that fight (POOLS below), caught and grinded a little (starter at
# the cap, the rest 1-2 under), evolved by level where the level allows, the moves the game teaches by level-up (no
# TMs, no Move Relearner), random natures and IVs 5-25, one Oran Berry. The challenger is piloted by the v21 AI at
# PRISM_PLAYER_SKILL (default 100: the AI's best play, i.e. sensible moves and switches) and, on Casual and Standard,
# uses the few healing items a player carries (BAG below; Hard forbids the Bag in trainer battles).
#
#   PRISM_MODES=CASUAL,STANDARD,HARD   PRISM_FIGHTS=K1,J1,G1,G2,G3,K2   PRISM_SEEDS=20 (per starter)
# Writes WINRATES.md and winrates.json to PRISM_OUT (default docs/battle_captures/winrates).
#===============================================================================
require "json"
require "fileutils"
load File.join(__dir__, "boot.rb")
load File.join(HARNESS_DIR, "log_scene.rb")

OUT_DIR = ENV["PRISM_OUT"] || File.expand_path("../../docs/battle_captures/winrates", HARNESS_DIR)
FileUtils.mkdir_p(File.join(OUT_DIR, "logs"))
MODES  = (ENV["PRISM_MODES"] || "CASUAL,STANDARD,HARD").split(",").map { |s| s.strip.upcase.to_sym }
FIGHTS = (ENV["PRISM_FIGHTS"] || "K1,J1,G1,G2,G3,K2").split(",").map { |s| s.strip.upcase }
SEEDS  = (ENV["PRISM_SEEDS"] || "20").to_i
KEEP_LOGS = ENV["PRISM_KEEP_LOGS"] == "1"
PLAYER_SKILL = (ENV["PRISM_PLAYER_SKILL"] || "100").to_i
class Player < Trainer
  def skill_level; PLAYER_SKILL; end
end

# The healing items the challenger may use (from battle.ally_items[0], mirrored in $bag); harness-only shim so the
# player's AI can spend them. Casual and Standard only.
class Battle
  alias __winrates__pbConsumeItemInBag pbConsumeItemInBag unless method_defined?(:__winrates__pbConsumeItemInBag)
  def pbConsumeItemInBag(item, idxBattler)
    if pbOwnedByPlayer?(idxBattler) && @ally_items && @ally_items[0]
      i = @ally_items[0].index(item)
      @ally_items[0].delete_at(i) if i
      $bag.add(item) if !$bag.has?(item)   # never raise inside the harness
    end
    __winrates__pbConsumeItemInBag(item, idxBattler)
  end
end

module Harness
  def self.set_badges(count)
    $player.badges = Array.new([$player.badges.length, 18].max) { |i| i < count }
  end
end

module WR
  STARTERS = { "Grass" => [:BULBASAUR, :IVYSAUR], "Fire" => [:CHARMANDER, :CHARMELEON], "Water" => [:SQUIRTLE, :WARTORTLE] }
  # What a player can have caught before each fight (SPINE Rev 16: no counter to the next Warden is handed out, so
  # the pools hold only what the availability doc gives at that point). Edit with design/POKEMON_AVAILABILITY.md.
  POOLS = {
    # Ch1 (520 Ferrymen's Mile, 521 Windfall Row) + the Strand Road (527/528) + Ch1 gifts. No Fighting type before Gym 1.
    :ch1_2 => [:FLETCHLING, :SHINX, :LITLEO, :NIDORANmA, :NIDORANfE, :PIKIPEK, :NICKIT, :SMOLIV, :WATTREL, :CHARCADET,
               :LILLIPUP, :BOUNSWEET, :ROLYCOLY, :ZIGZAGOON, :PIDOVE, :SKWOVET],
    # + after Gym 1: Eevee "Understudy", the Weavers' Road (541/552/540/544-545/524) and the Saltmere gifts.
    :ch3   => [:EEVEE, :SHINX, :NIDORANmA, :PIKIPEK, :NICKIT, :SMOLIV, :WATTREL, :LILLIPUP, :BOUNSWEET, :RALTS,
               :KECLEON, :BUNNELBY, :MACHOP, :FLABEBE, :SURSKIT, :MAREEP, :TIMBURR, :FLETCHLING],
    # + after Gym 2: the Hoar Road (566/577/578), Frostwick, the Rimewood, the Gullcry Cliffs.
    :ch4   => [:EEVEE, :LUXIO, :NIDORINO, :TRUMBEAK, :MACHOP, :KECLEON, :RALTS, :HERACROSS, :SNOVER, :STANTLER, :TEDDIURSA,
               :DEERLING, :CUBCHOO, :SNOM, :FLETCHINDER, :MAREEP, :SKIDDO, :WINGULL]
  }
  # TMs the story has handed over by then (TM42 Facade from Dorian, TM98 Rock Smash at Brinecut, TM89 U-turn from Tamsin):
  # each goes to the first party member that can learn it, replacing its weakest move.
  TMS = { :none => [], :g2 => [:FACADE, :ROCKSMASH], :g3 => [:FACADE, :ROCKSMASH, :UTURN] }
  # A PREPARED player (PRISM_PREPARED=1): the same rules, but the catches are the best type answers the availability
  # doc allows by then (resists / super-effective STAB vs the Warden's type), not a random handful.
  PREPARED = {
    :ch1_2 => [:ROLYCOLY, :SUDOWOODO, :NICKIT, :WATTREL, :CHARCADET, :LITLEO, :FLETCHLING, :SHINX],
    :ch3   => [:ROLYCOLY, :FLETCHLING, :LITLEO, :CHARCADET, :WATTREL, :EEVEE, :KECLEON, :RALTS],
    :ch4   => [:LUXIO, :WATTREL, :MAREEP, :SMOLIV, :BOUNSWEET, :ODDISH, :RALTS, :EEVEE]
  }
  PREP = ENV["PRISM_PREPARED"] == "1"
  BAG = { :none => [], :g1 => [:POTION] * 3, :g2 => [:POTION, :POTION, :SUPERPOTION, :SUPERPOTION],
          :g3 => [:SUPERPOTION] * 3 }
  # fight => level cap, badges held, team size (starter included), catch pool, bag, how it starts
  FIGHTS = {
    "K1" => { :label => "K1 Kestrel (intro, Lv 5 starter alone)", :cap => 5, :lvcap => 15, :badges => 0, :size => 1, :pool => :ch1_2,
              :bag => :none, :stage => 0, :start => proc { Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 1, :can_lose => true) } },
    "J1" => { :label => "J1 Juno (Saltmere green, before Gym 1)", :cap => 15, :badges => 0, :size => 6, :pool => :ch1_2,
              :bag => :g1, :stage => 0, :start => proc { Prismfall.rival_battle(:RIVAL_JUNO, "Juno", 1, :can_lose => true) } },
    "G1" => { :label => "Gym 1 Dorian (Grand Stage, single)", :cap => 15, :badges => 0, :size => 6, :pool => :ch1_2,
              :bag => :g1, :stage => 0, :start => proc { Prismfall.gym_battle(1, :can_lose => true) } },
    "G2" => { :label => "Gym 2 Tamsin (Silkwood, double)", :cap => 19, :badges => 1, :size => 6, :pool => :ch3,
              :bag => :g2, :tms => :g2, :stage => 1, :start => proc { Prismfall.gym_battle(2, :can_lose => true) } },
    "K2" => { :label => "K2 Kestrel (Gullcry Cliffs, before Gym 3)", :cap => 23, :badges => 2, :size => 6, :pool => :ch4,
              :bag => :g3, :tms => :g3, :stage => 1, :start => proc { Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 2, :can_lose => true) } },
    "G3" => { :label => "Gym 3 Marisol (Water Surface)", :cap => 23, :badges => 2, :size => 6, :pool => :ch4,
              :bag => :g3, :tms => :g3, :stage => 1, :start => proc { Prismfall.gym_battle(3, :can_lose => true) } }
  }
  FILLER = [:GROWL, :LEER, :TAILWHIP, :BABYDOLLEYES, :SANDATTACK, :SMOKESCREEN, :SWEETSCENT, :STRINGSHOT, :SPLASH,
            :HARDEN, :WITHDRAW, :DEFENSECURL, :CHARM, :PLAYNICE, :HELPINGHAND, :FOCUSENERGY, :ODORSLEUTH,
            :CAMOUFLAGE, :SCARYFACE, :SCREECH, :CONFIDE, :COPYCAT, :WORKUP, :TEARFULLOOK, :MIMIC].freeze

  # Level-up evolution (the only kind a player reliably has by then).
  def self.evolve(species, level)
    loop do
      nxt = GameData::Species.get(species).get_evolutions.find do |_sp, method, param|
        GameData::Evolution.get(method).id == :Level && param.to_i <= level
      end
      break if !nxt
      species = nxt[0]
    end
    species
  end

  def self.mon(species, level, rng)
    p = Pokemon.new(evolve(species, level), level)
    GameData::Stat.each_main { |s| p.iv[s.id] = 5 + rng.rand(21) }
    p.nature = GameData::Nature.keys.sample(random: rng)
    learned = p.species_data.moves.select { |lv, _m| lv <= level }.map { |_lv, m| m }.uniq.reverse
    keep = learned.reject { |m| FILLER.include?(m) }.first(4)
    keep += (learned - keep).first(4 - keep.size) if keep.size < 4
    p.forget_all_moves
    keep.reverse.each { |m| p.learn_move(m) }
    p.calc_stats
    p
  end

  def self.party(fight, starter_lines, seed)
    rng = Random.new(seed)
    f = FIGHTS[fight]
    st = starter_lines[f[:stage]] || starter_lines[0]
    list = [[st, f[:cap]]]
    pool = (PREP ? PREPARED : POOLS)[f[:pool]]
    catches = PREP ? pool.first(f[:size] + 1).shuffle(random: rng).first(f[:size] - 1) : pool.shuffle(random: rng).first(f[:size] - 1)
    offsets = [1, 1, 2, 2, 3]   # starter at the cap; the rest a little behind it
    catches.each_with_index { |sp, i| list << [sp, f[:cap] - offsets[i % offsets.size]] }
    party = list.map { |sp, lv| mon(sp, lv, rng) }
    TMS[f[:tms] || :none].each do |tm|
      pk = party.find { |pp| pp.compatible_with_move?(tm) && !pp.hasMove?(tm) }
      next if !pk
      if pk.numMoves < 4
        pk.learn_move(tm)
      else
        weakest = pk.moves.min_by { |m| m.power.to_i }
        pk.moves[pk.moves.index(weakest)] = Pokemon::Move.new(tm)
      end
    end
    party = party.rotate(rng.rand(party.size)) if party.size > 1   # the starter does not always lead
    party[0].item = :ORANBERRY if f[:size] > 1
    party
  end
end

Harness.new_game_state
RESULTS = []
ERRORS = []
MODES.each do |mode|
  Prismfall::Difficulty.set(mode)
  FIGHTS.each do |fight|
    f = WR::FIGHTS[fight] or next
    WR::STARTERS.each do |sname, lines|
      Prismfall.record_starter(lines[0])
      runs = (1..SEEDS).map do |s|
        seed = 40_000 + fight.sum * 7 + s * 101 + lines[0].to_s.sum
        Harness.set_badges(f[:badges])
        Prismfall::LevelCap.set_override(f[:lvcap] || f[:cap])
        $player.party = WR.party(fight, lines, seed)
        bag = (mode == :HARD) ? [] : WR::BAG[f[:bag]].dup
        $bag.clear if $bag.respond_to?(:clear)
        bag.each { |it| $bag.add(it) }
        foe_left = nil
        log = Harness.run_battle("#{f[:label]} #{mode} #{sname} seed #{s}", :seed => seed,
                                 :setup => proc { |b| b.ally_items = [bag.dup] }) { f[:start].call }
        Prismfall::LevelCap.clear_override
        b = log.battle
        if b
          foe_left = b.pbParty(1).count { |pk| pk && !pk.fainted? }
          mine_left = b.pbParty(0).count { |pk| pk && !pk.fainted? }
        end
        if KEEP_LOGS || log.errors.any?
          File.write(File.join(OUT_DIR, "logs", "#{fight}_#{mode}_#{sname}_s#{s}.txt"),
                     "LOGIC-TEST OUTPUT (headless harness). Not a game screenshot.\n\n" + log.text)
        end
        log.errors.each { |e| ERRORS << e.merge(:name => log.title) }
        { :outcome => log.outcome, :turns => log.turns, :foe_left => foe_left, :mine_left => mine_left,
          :party => $player.party.map { |pk| "#{pk.species} #{pk.level}" } }
      end
      wins = runs.count { |r| r[:outcome] == 1 }
      row = { :mode => mode, :fight => fight, :label => f[:label], :starter => sname, :runs => runs.size, :wins => wins,
              :avg_turns => (runs.sum { |r| r[:turns] } / runs.size.to_f).round(1),
              :avg_foe_left_on_loss => (l = runs.reject { |r| r[:outcome] == 1 }).empty? ? 0 : (l.sum { |r| r[:foe_left].to_i } / l.size.to_f).round(2),
              :avg_mine_left_on_win => (w = runs.select { |r| r[:outcome] == 1 }).empty? ? 0 : (w.sum { |r| r[:mine_left].to_i } / w.size.to_f).round(2),
              :errors => runs.count { |r| r[:outcome].nil? } }
      RESULTS << row
      puts format("%-8s %-3s %-5s won %2d/%-2d  %.1f turns  foe left on loss %.2f  mine left on win %.2f",
                  mode, fight, sname, wins, runs.size, row[:avg_turns], row[:avg_foe_left_on_loss], row[:avg_mine_left_on_win])
    end
  end
end

md = ["# Realistic win-rate test (logic test, AI on both sides)", "",
      "Generated by `tools/harness/run_winrates.rb`: a realistic challenger (starter + what the availability doc allows, levels",
      "at the cap or 1-2 under, level-up moves, random natures, IV 5-25, Oran Berry; healing items on Casual/Standard)",
      "piloted by the v21 AI at skill #{PLAYER_SKILL}#{WR::PREP ? ', PREPARED catches (best type answers allowed by then)' : ''}. #{SEEDS} seeded fights per starter. \"Won\" is the challenger.", ""]
md << "| Fight | " + MODES.map(&:to_s).join(" | ") + " |"
md << "|---|" + MODES.map { "---" }.join("|") + "|"
FIGHTS.each do |fight|
  next if !WR::FIGHTS[fight]
  cells = MODES.map do |mode|
    rows = RESULTS.select { |r| r[:mode] == mode && r[:fight] == fight }
    w = rows.sum { |r| r[:wins] }; n = rows.sum { |r| r[:runs] }
    n.zero? ? "-" : "#{(100.0 * w / n).round}% (#{rows.map { |r| "#{r[:starter][0]} #{r[:wins]}" }.join(', ')} of #{SEEDS})"
  end
  md << "| #{WR::FIGHTS[fight][:label]} | #{cells.join(' | ')} |"
end
md << "" << "Exceptions: **#{ERRORS.size}**"
ERRORS.uniq { |e| [e[:class], e[:message]] }.first(8).each { |e| md << "- #{e[:name]}: #{e[:class]}: #{e[:message]} (#{Array(e[:backtrace]).first})" }
File.write(File.join(OUT_DIR, "WINRATES.md"), md.join("\n") + "\n")
File.write(File.join(OUT_DIR, "winrates.json"), JSON.pretty_generate(RESULTS))
puts md.join("\n")
