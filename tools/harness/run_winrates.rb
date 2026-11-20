#===============================================================================
# Prismfall realistic win-rate test (trainer workstream; companion to run_trainers.rb).
#   PRISM_RUN_DIR=<private run dir> PRISM_OUT=<out dir> PRISM_COMPILE=1 ruby tools/harness/run_winrates.rb
# Real Essentials v21.1 battle code + Prismfall plugins, AI on both sides. Logic test only.
#
# The challenger is a REALISTIC player, not an ideal-counter team: a starter plus what design/POKEMON_AVAILABILITY.md
# and design/EVENT_POKEMON.md make available before that fight (POOLS below), caught and grinded a little (starter at
# the cap, the rest 1-2 under), evolved by level where the level allows, the moves the game teaches by level-up (no
# TMs but the story's, no Move Relearner; when a new move is learned the weakest attack goes), random natures and IVs
# 5-25, one Oran Berry. The challenger is piloted by the v21 AI at
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
  # What a player can have caught before each fight, weighted by how often the player meets it: the best wild rate of
  # each land / cave species on the maps walked before that fight (Headbutt and Rock Smash rates x0.3: a few trees and
  # rocks per map) (pbs/encounters.txt after the SPINE Rev 16
  # distribution pass; fishing-only species left out) plus the hand-outs of design/POKEMON_AVAILABILITY.md 2a and
  # EVENT_POKEMON.md. Gated answers keep their 2-4% weight, so a realistic team holds one only now and then.
  # Regenerate the wild part with /home/claude/work/trainers2/pools.py-style counting if the tables change.
  POOLS = {
    # Before Gym 1 / J1 (0 badges): 520, 521, 522, 527, 528, Saltmere. No Fighting type at all; Ghost = Sandygast 3%.
    :ch1_2 => { :PIDOVE => 17, :HOOTHOOT => 20, :PIKIPEK => 15, :WINGULL => 15, :SKWOVET => 20, :LILLIPUP => 15,
                :NICKIT => 25, :MEOWTH => 15, :SPINARAK => 18, :TAROUNTULA => 15, :GOSSIFLEUR => 15, :ODDISH => 15,
                :BOUNSWEET => 12, :SMOLIV => 12, :ZIGZAGOON => 12, :BUNEARY => 12, :NIDORANmA => 10, :NIDORANfE => 10,
                :POOCHYENA => 10, :LECHONK => 15, :WOOLOO => 13, :NYMBLE => 13, :CUTIEFLY => 10, :NOIBAT => 10,
                :FIDOUGH => 9, :TANDEMAUS => 16, :SQUAWKABILLY => 9, :COMBEE => 10, :KECLEON => 15,   # lantern quest
                :FLETCHLING => 4, :SHINX => 4, :NACLI => 4, :DWEBBLE => 4, :ROLYCOLY => 3, :LITLEO => 3,
                :BUNNELBY => 3, :SANDYGAST => 3 },
    # Before Gym 2 (1 badge): + the Weavers' Road (541, 544/545, 552, 540, 546, 524) and the Badge-1 hand-outs.
    :ch3   => { :EEVEE => 60, :ABRA => 20, :TIMBURR => 25, :CRABRAWLER => 20, :RALTS => 15, :SMEARGLE => 10, :PONYTA_G => 10,
                :PIDOVE => 17, :HOOTHOOT => 20, :PIKIPEK => 15, :WINGULL => 15, :SPEAROW => 10, :DODUO => 12, :DUCKLETT => 8,
                :NICKIT => 15, :MEOWTH => 15, :LILLIPUP => 15, :SKWOVET => 15, :SHUPPET => 20, :FLABEBE => 18, :ZUBAT => 18,
                :GREAVARD => 18, :VENONAT => 15, :PHANTUMP => 15, :KARRABLAST => 15, :SHELMET => 15, :WHISMUR => 15,
                :DUSKULL => 15, :COTTONEE => 14, :WOOBAT => 13, :MACHOP => 13, :MINCCINO => 13, :SMOLIV => 12,
                :BOUNSWEET => 12, :SENTRET => 12, :SUNKERN => 12, :SABLEYE => 12, :MAWILE => 12, :SINISTEA => 12,
                :GASTLY => 12, :NIDORANmA => 10, :MANKEY => 10, :STUNKY => 10, :PURRLOIN => 10, :SNUBBULL => 10,
                :FOONGUS => 10, :MORELULL => 10, :SURSKIT => 9, :SEWADDLE => 8, :PETILIL => 8, :SKIDDO => 8, :MEDITITE => 8,
                :KECLEON => 10, :COMBEE => 12, :SQUAWKABILLY => 12,
                :FLETCHLING => 4, :SHINX => 4, :NACLI => 4, :DWEBBLE => 4, :ROLYCOLY => 3, :LITLEO => 3, :SIZZLIPEDE => 3,
                :ROGGENROLA => 4, :ARON => 4, :MAREEP => 5 },
    # Before K2 / Gym 3 (2 badges): + Deepwood, Cocoonfall, the Hoar Road, Frostwick, the Rimewood, Gullcry, Rock Smash
    # and the Badge-2 hand-outs (Charcadet, Litleo, Sudowoodo, Heracross or Pinsir, Spidops, Snom, Ditto).
    :ch4   => { :EEVEE => 60, :ABRA => 15, :TIMBURR => 20, :CRABRAWLER => 15, :RALTS => 15, :PONYTA_G => 10,
                :CHARCADET => 15, :LITLEO => 15, :SUDOWOODO => 10, :HERACROSS => 10, :PINSIR => 8, :SPIDOPS => 10, :SNOM => 15,
                :DWEBBLE => 15, :NACLI => 14, :ROGGENROLA => 9, :BINACLE => 6, :SNORUNT => 18, :SNOVER => 16, :SKIDDO => 15,
                :SHUCKLE => 5, :DEERLING => 14, :CUBCHOO => 14, :SMOOCHUM => 14, :TEDDIURSA => 12, :GLAMEOW => 12,
                :SPHEAL => 12, :YANMA => 12, :LEDYBA => 12, :DUCKLETT => 12, :DODUO => 12, :PIDOVE => 17, :WINGULL => 17,
                :HOOTHOOT => 20, :SHUPPET => 20, :ZUBAT => 18, :GREAVARD => 18, :MACHOP => 13, :MANKEY => 10, :NICKIT => 15,
                :LILLIPUP => 15, :FLABEBE => 18, :VENONAT => 15, :PHANTUMP => 15, :MAWILE => 12, :SABLEYE => 12,
                :SWABLU => 10, :SNEASEL => 5, :STANTLER => 6, :SPINDA => 10, :DUNSPARCE => 10, :KECLEON => 10,
                :SHINX => 4, :MAREEP => 5, :JOLTIK => 5, :BLITZLE => 4, :GRUBBIN => 4 }
  }
  # TMs the story has handed over by then (TM42 Facade from Dorian, TM98 Rock Smash at Brinecut, TM89 U-turn from Tamsin):
  # each goes to the first party member that can learn it, replacing its weakest move.
  TMS = { :none => [], :g2 => [:FACADE, :ROCKSMASH], :g3 => [:FACADE, :ROCKSMASH, :UTURN] }
  # The team is built over the whole journey: later pools include the earlier ones (a species keeps its best weight).
  POOLS[:ch3] = POOLS[:ch1_2].merge(POOLS[:ch3]) { |_k, a, b| [a, b].max }
  POOLS[:ch4] = POOLS[:ch3].merge(POOLS[:ch4]) { |_k, a, b| [a, b].max }
  # A PREPARED player (PRISM_PREPARED=1): grinds every catch to the cap, keeps its strongest moves and hunts the best
  # type answers the availability doc allows by then (rare finds included), first listed first.
  PREPARED = {
    :ch1_2 => [:NACLI, :DWEBBLE, :SANDYGAST, :ROLYCOLY, :NICKIT, :KECLEON, :SHINX, :FLETCHLING],
    :ch3   => [:PONYTA, :NACLI, :DWEBBLE, :FLETCHLING, :SPEAROW, :DODUO, :HOOTHOOT, :LITLEO],
    :ch4   => [:MAREEP, :SHINX, :JOLTIK, :SKIDDO, :SNOVER, :DEERLING, :HERACROSS, :ODDISH]
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
    # Revision 19: the Saltmere crowd you met sets the Grand Stage's starting stage (1-3) for Dorian's fight.
    "G1S2" => { :label => "Gym 1 Dorian, crowd start: Encore (stage 2)", :cap => 15, :badges => 0, :size => 6, :pool => :ch1_2,
                :bag => :g1, :stage => 0, :start => proc { setBattleRule("fieldStage", 2); Prismfall.gym_battle(1, :can_lose => true) } },
    "G1S3" => { :label => "Gym 1 Dorian, crowd start: Standing Ovation (stage 3)", :cap => 15, :badges => 0, :size => 6, :pool => :ch1_2,
                :bag => :g1, :stage => 0, :start => proc { setBattleRule("fieldStage", 3); Prismfall.gym_battle(1, :can_lose => true) } },
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

  # Hand-outs keep their event ability, form and moves (plugins/Prismfall Trials/130_EventMons_Early.rb); level-up moves
  # learned since then replace filler first.
  EVENT = {
    :KECLEON => [:PROTEAN, 13, [:FURYSWIPES, :FEINT, :BIND, :THIEF]],
    :NICKIT => [:STAKEOUT, 7, [:QUICKATTACK, :BEATUP, :THIEF, :TAILWHIP]],
    :TIMBURR => [:GUTS, 13, [:LOWKICK, :ROCKTHROW, :LEER, :MACHPUNCH]],
    :CRABRAWLER => [:IRONFIST, 14, [:ROCKSMASH, :BUBBLE, :LEER, :POWERUPPUNCH]],
    :SMEARGLE => [:TECHNICIAN, 14, [:SKETCH, :AQUAJET, :ICYWIND]],
    :RALTS => [:TRACE, 13, [:CONFUSION, :DISARMINGVOICE, :DOUBLETEAM, :HYPNOSIS]],
    :PONYTA_G => [:PASTELVEIL, 15, [:CONFUSION, :FAIRYWIND, :TAILWHIP, :HYPNOSIS], 1],
    :HERACROSS => [:MOXIE, 19, [:FURYATTACK, :HORNATTACK, :REVENGE, :ENDURE]],
    :PINSIR => [:MOXIE, 19, [:VISEGRIP, :BIND, :SEISMICTOSS, :BUGBITE]],
    :SPIDOPS => [:STAKEOUT, 18, [:SILKTRAP, :BUGBITE, :FEINT, :ASSURANCE]],
    :LITLEO => [:MOXIE, 19, [:EMBER, :HEADBUTT, :WORKUP, :NOBLEROAR]],
    :CHARCADET => [:FLAMEBODY, 18, [:EMBER, :CLEARSMOG, :FIRESPIN, :WILLOWISP]],
    :SUDOWOODO => [:ROCKHEAD, 20, [:ROCKTHROW, :FLAIL, :FAKETEARS, :COPYCAT]],
    :SNOM => [:ICESCALES, 15, [:POWDERSNOW, :STRUGGLEBUG, :MIRRORCOAT, :FAIRYWIND]]
  }
  EVENT_IN = { :ch1_2 => [:KECLEON, :NICKIT], :ch3 => [:KECLEON, :NICKIT, :TIMBURR, :CRABRAWLER, :SMEARGLE, :RALTS, :PONYTA_G],
               :ch4 => [:KECLEON, :NICKIT, :TIMBURR, :CRABRAWLER, :RALTS, :PONYTA_G, :HERACROSS, :PINSIR, :SPIDOPS,
                        :LITLEO, :CHARCADET, :SUDOWOODO, :SNOM] }

  def self.mon(species, level, rng, pool = nil)
    ev = (pool && EVENT_IN[pool]&.include?(species)) ? EVENT[species] : nil
    species = :PONYTA if species == :PONYTA_G
    p = Pokemon.new(evolve(species, level), level)
    p.form = ev[3] if ev && ev[3]
    GameData::Stat.each_main { |s| p.iv[s.id] = 5 + rng.rand(21) }
    p.nature = GameData::Nature.keys.sample(random: rng)
    learned = p.species_data.moves.select { |lv, _m| lv <= level }.map { |_lv, m| m }.uniq.reverse
    if true
      # A player declines the weak moves when a new one is learned: the three strongest attacks (power x STAB x accuracy), then the
      # best of what is left (a fourth attack, or the newest non-filler status move).
      score = lambda do |m|
        mv = GameData::Move.get(m)
        next 0 if mv.power.to_i <= 1
        mv.power * (p.types.include?(mv.type) ? 1.5 : 1.0) * ((mv.accuracy.to_i == 0) ? 100 : mv.accuracy) / 100.0
      end
      attacks = learned.select { |m| score.call(m) > 0 }.sort_by { |m| -score.call(m) }
      keep = attacks.first(3)
      rest = learned.reject { |m| keep.include?(m) || FILLER.include?(m) }
      keep += rest.first(4 - keep.size)
    else
      keep = learned.reject { |m| FILLER.include?(m) }.first(4)
    end
    keep += (learned - keep).first(4 - keep.size) if keep.size < 4
    if ev
      p.ability = ev[0] if p.species_data.abilities.include?(ev[0]) || p.species_data.hidden_abilities.include?(ev[0])
      newer = p.species_data.moves.select { |lv, _m| lv > ev[1] && lv <= level }.map { |_lv, m| m }.uniq.reverse
      keep = (newer.reject { |m| FILLER.include?(m) } + ev[2].reject { |m| FILLER.include?(m) } + ev[2]).uniq.first(4)
    end
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
    if PREP
      catches = PREPARED[f[:pool]].first(f[:size] + 1).shuffle(random: rng).first(f[:size] - 1)
    else   # weighted draw without replacement
      bag_w = POOLS[f[:pool]].to_a
      catches = []
      (f[:size] - 1).times do
        tot = bag_w.sum { |_sp, w| w }
        r = rng.rand * tot
        i = bag_w.index { |_sp, w| (r -= w) < 0 } || (bag_w.size - 1)
        catches << bag_w.delete_at(i)[0]
      end
    end
    offsets = [1, 1, 2, 2, 3]   # starter at the cap; the rest a little behind it
    catches.each_with_index { |sp, i| list << [sp, f[:cap] - (PREP ? 0 : offsets[i % offsets.size])] }   # prepared = grinded to the cap
    party = list.map { |sp, lv| mon(sp, lv, rng, f[:pool]) }
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
        bag = (mode == :HARD && ENV["PRISM_HARD_BAG"] != "1") ? [] : WR::BAG[f[:bag]].dup
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
