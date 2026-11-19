#===============================================================================
# Prismfall headless trainer run (trainer workstream; companion to run_all.rb).
#   PRISM_RUN_DIR=<private run dir> PRISM_OUT=<out dir> PRISM_COMPILE=1 ruby tools/harness/run_trainers.rb
# Real Essentials v21.1 battle code + Prismfall plugins, AI on both sides. Logic test only.
#
#   A. every Warden, PRISM_SEEDS seeded fights each (default 6), through Prismfall.gym_battle
#   B. rivals K1-K9 / J1-J4, admins, bosses, Festival and story teams (field from TRAINER_FIELDS)
#   C. Gyms 1-3 on Standard against a realistic early-game challenger (a starter plus route catches at the
#      level cap, level-up moves, middling IVs, no EVs): win rates per starter
# For A and B it reports which designed field plays (design/TRAINER_FIELD_PLAYBOOK.md) the AI actually used.
# PRISM_PART=A,B,C limits the parts; PRISM_ONLY_T=LEADER_MARISOL,... limits A/B to trainer types.
# Writes logs/, PLAYS.md and results_trainers.json to PRISM_OUT (default docs/battle_captures/trainers).
#===============================================================================
require "json"
require "fileutils"
load File.join(__dir__, "boot.rb")
load File.join(HARNESS_DIR, "log_scene.rb")

OUT_DIR = ENV["PRISM_OUT"] || File.expand_path("../../docs/battle_captures/trainers", HARNESS_DIR)
FileUtils.mkdir_p(File.join(OUT_DIR, "logs"))
SEEDS  = (ENV["PRISM_SEEDS"] || "6").to_i
PARTS  = (ENV["PRISM_PART"] || "A,B,C").split(",").map(&:strip)
ONLY_T = ENV["PRISM_ONLY_T"]&.split(",")&.map { |s| s.strip.upcase.to_sym }

module Harness
  # Generic challenger (same idea as run_all.rb): plain attacking sets, perfect IVs, no items.
  TIERS = [
    [23,  { :GROWLITHE => [:EMBER, :BITE, :FLAMEWHEEL], :STARAVIA => [:WINGATTACK, :QUICKATTACK, :AERIALACE],
            :ROGGENROLA => [:ROCKBLAST, :HEADBUTT, :SMACKDOWN], :MAREEP => [:THUNDERSHOCK, :CHARGEBEAM, :TAKEDOWN],
            :LOMBRE => [:BUBBLEBEAM, :MEGADRAIN, :FAKEOUT], :MACHOP => [:KARATECHOP, :LOWSWEEP, :KNOCKOFF, :REVENGE] }],
    [47,  { :MAGMAR => [:FIREPUNCH, :THUNDERPUNCH, :LAVAPLUME, :CLEARSMOG],
            :PIDGEOT => [:AIRSLASH, :AERIALACE, :UTURN, :FACADE], :GRAVELER => [:ROCKSLIDE, :BULLDOZE, :FIREPUNCH],
            :AMPHAROS => [:DISCHARGE, :POWERGEM, :SIGNALBEAM, :DRAGONPULSE],
            :VAPOREON => [:SCALD, :AURORABEAM, :WATERPULSE, :SHADOWBALL],
            :HARIYAMA => [:FORCEPALM, :KNOCKOFF, :BULLETPUNCH, :WAKEUPSLAP] }],
    [100, { :GARCHOMP => [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :FIREFANG],
            :TOGEKISS => [:AIRSLASH, :DAZZLINGGLEAM, :AURASPHERE, :FLAMETHROWER],
            :STARMIE => [:SURF, :ICEBEAM, :THUNDERBOLT, :PSYCHIC],
            :MAGNEZONE => [:THUNDERBOLT, :FLASHCANNON, :TRIATTACK, :VOLTSWITCH],
            :LUCARIO => [:AURASPHERE, :FLASHCANNON, :EXTREMESPEED, :CLOSECOMBAT],
            :CHARIZARD => [:FLAMETHROWER, :AIRSLASH, :DRAGONPULSE, :EARTHQUAKE] }]
  ].freeze

  def self.generic_party(level, rotate = 0)
    team = TIERS.find { |cap, _| level <= cap }[1].to_a.rotate(rotate)
    team.map do |species, moves|
      p = Pokemon.new(species, level)
      GameData::Stat.each_main { |s| p.iv[s.id] = 31 }
      p.nature = :HARDY
      p.forget_all_moves
      moves.each { |m| p.learn_move(m) }
      p.calc_stats
      p
    end
  end

  # Realistic early-game party: [species, level] list, IV 15, no EVs, HARDY. Moves: what the game teaches by level-up
  # at that level, minus the pure stat-drop filler a player replaces or never clicks (Growl, Leer, Tail Whip...),
  # newest first, up to four. No TMs, no held items but one Oran Berry.
  FILLER = [:GROWL, :LEER, :TAILWHIP, :BABYDOLLEYES, :SANDATTACK, :SMOKESCREEN, :SWEETSCENT, :STRINGSHOT, :SPLASH,
            :HARDEN, :WITHDRAW, :DEFENSECURL, :CHARM, :PLAYNICE, :HELPINGHAND, :FOCUSENERGY, :CHARGE, :ODORSLEUTH,
            :CAMOUFLAGE, :SCARYFACE, :SCREECH, :CONFIDE, :COPYCAT, :WORKUP].freeze
  def self.casual_party(list, item_on_first = :ORANBERRY)
    party = list.map do |species, level|
      p = Pokemon.new(species, level)
      GameData::Stat.each_main { |s| p.iv[s.id] = 15 }
      p.nature = :HARDY
      learned = p.species_data.moves.select { |lv, _m| lv <= level }.map { |_lv, m| m }.uniq.reverse
      keep = learned.reject { |m| FILLER.include?(m) }.first(4)
      keep += (learned - keep).first(4 - keep.size) if keep.size < 4
      p.forget_all_moves
      keep.reverse.each { |m| p.learn_move(m) }
      p.calc_stats
      p
    end
    party[0].item = item_on_first if item_on_first
    party
  end

  def self.set_badges(count)
    $player.badges = Array.new([$player.badges.length, 18].max) { |i| i < count }
  end

  # Who made each field / stage change, and every move the foe used. The change is credited to the nearest preceding
  # action line (a move, a held seed, an ability splash, a send-out, or the end of the round).
  def self.analyse(log)
    foe_moves = Hash.new(0)
    changes = []
    actions = []
    turn = 0
    log.lines.each do |l|
      turn = $1.to_i if l =~ /--- Turn (\d+) ---/
      if l =~ /^\s*The opposing (.+?) used (.+?)!/
        foe_moves[$2] += 1
        actions << :foe
      elsif l =~ /^\s*(.+?) used (.+?)!/
        actions << ((l =~ /Warden|Leader|opposing/) ? :foe : :player)
      elsif l =~ /Seed|\[ability:/
        actions << ((l =~ /opposing/) ? :foe_entry : :player_entry)
      elsif l =~ /sent out \((foe|player)\)/
        actions << (($1 == "foe") ? :foe_entry : :player_entry)
      elsif l =~ /\(end of round\)/
        actions << :end_of_round
      elsif l =~ /answer .*: the .* it was raised beside/
        actions << :foe_entry
      end
      by = actions.last
      if l =~ /## FIELD CHANGE: (\w+) -> (\w+)/
        changes << { :from => $1, :to => $2, :by => by, :turn => turn } if $1 != "NONE"
      elsif l =~ /## FIELD STAGE: (\w+) is now stage (\d+)/
        changes << { :from => $1, :to => "#{$1}:#{$2}", :by => by, :turn => turn }
      end
    end
    { :foe_moves => foe_moves, :changes => changes }
  end
end

Harness.new_game_state
Prismfall.record_starter(:CHARMANDER)
# Calibration switches for part C: PRISM_NOBAG=1 strips the Warden's bag items, PRISM_NOFIELD=1 fights without a field,
# PRISM_EARLY_GYMS=1,2 limits the gyms.
if ENV["PRISM_NOBAG"] == "1"
  EventHandlers.add(:on_trainer_load, :harness_nobag, proc { |tr| tr.items.clear if tr && tr.respond_to?(:items) })
end
EARLY_FIELD = (ENV["PRISM_NOFIELD"] == "1") ? false : true
# PRISM_PLAYER_SKILL=n: the AI skill that pilots the challenger (default: the player trainer type's, 60 in the base PBS).
if ENV["PRISM_PLAYER_SKILL"]
  PLAYER_SKILL = ENV["PRISM_PLAYER_SKILL"].to_i
  class Player < Trainer
    def skill_level; PLAYER_SKILL; end
  end
end
EARLY_GYMS  = ENV["PRISM_EARLY_GYMS"]&.split(",")&.map(&:to_i)
RESULTS = { :wardens => [], :others => [], :early => [], :errors => [] }

def run_one(title, file, seed, level, party, badges: nil, cap: nil, size_check: nil)
  if badges
    Harness.set_badges(badges)
  else
    Harness.set_badges(18)
    Prismfall::LevelCap.set_override(cap || level)
  end
  $player.party = party
  sizes = nil
  log = Harness.run_battle(title, :seed => seed, :setup => proc { |b| sizes = [b.pbSideSize(0), b.pbSideSize(1)] }) { yield }
  Prismfall::LevelCap.clear_override
  File.write(File.join(OUT_DIR, "logs", "#{file}_s#{seed}.txt"),
             "LOGIC-TEST OUTPUT (headless harness). Not a game screenshot.\n\n" + log.text)
  log.errors.each { |e| RESULTS[:errors] << e.merge(:name => title) }
  a = Harness.analyse(log)
  { :seed => seed, :outcome => log.outcome, :turns => log.turns, :errors => log.errors.size, :sizes => sizes,
    :start_field => (log.lines.find { |l| l =~ /field: (\w+)/ } && $1), :foe_moves => a[:foe_moves], :changes => a[:changes] }
end

# plays: { "label" => proc { |run| true if the designed play happened in this run } }
def used?(run, *moves); moves.any? { |m| run[:foe_moves][m].to_i > 0 }; end
def changed?(run, to, by = [:foe, :foe_entry]); run[:changes].any? { |c| c[:to] == to && Array(by).include?(c[:by]) }; end

def summarise(label, runs, plays, store)
  wins = runs.count { |r| r[:outcome] == 1 }
  row = { :label => label, :runs => runs.size, :player_wins => wins, :errors => runs.sum { |r| r[:errors] },
          :sizes => runs.map { |r| r[:sizes] }.uniq, :start_field => runs.map { |r| r[:start_field] }.uniq,
          :avg_turns => (runs.sum { |r| r[:turns] } / runs.size.to_f).round(1),
          :plays => plays.map { |name, pr| [name, runs.count { |r| pr.call(r) }] }.to_h,
          :foe_changes => runs.flat_map { |r| r[:changes].select { |c| [:foe, :foe_entry].include?(c[:by]) }.map { |c| "#{c[:from]}->#{c[:to]}" } }.tally,
          :player_changes => runs.flat_map { |r| r[:changes].select { |c| [:player, :player_entry].include?(c[:by]) }.map { |c| "#{c[:from]}->#{c[:to]}" } }.tally }
  store << row
  puts format("%-34s player won %d/%d  avg %.1f turns  errors %d  plays: %s", label, wins, runs.size, row[:avg_turns], row[:errors],
              row[:plays].map { |k, v| "#{k} #{v}/#{runs.size}" }.join("; "))
  row
end

#-------------------------------------------------------------------------------
# A. Wardens
#-------------------------------------------------------------------------------
WARDEN_PLAYS = {
  # SPINE Rev 14: Gym 1 = Dorian (single), Gym 2 = Tamsin (double).
  1  => { "Minccino / Chatot songs (Echoed Voice, Round, Chatter, Hyper Voice)" => proc { |r| used?(r, "Echoed Voice", "Round", "Chatter", "Hyper Voice") },
          "applause raised by Dorian" => proc { |r| changed?(r, "GRAND_STAGE:2") || changed?(r, "GRAND_STAGE:3") } },
  2  => { "Surskit Rain Dance" => proc { |r| used?(r, "Rain Dance") },
          "Electroweb / String Shot (spread speed control)" => proc { |r| used?(r, "Electroweb", "String Shot") },
          "Silk Trap used" => proc { |r| used?(r, "Silk Trap") },
          "Tamsin douses a Wildfire -> Embers" => proc { |r| changed?(r, "WILDFIRE:2") } },
  3  => { "Lucky's Dive -> Underwater" => proc { |r| changed?(r, "UNDERWATER") } },
  4  => { "Charge used" => proc { |r| used?(r, "Charge") },
          "grid rebooted by Rook" => proc { |r| changed?(r, "NEON_GRID:1") } },
  5  => { "Sand Tomb / Dig used" => proc { |r| used?(r, "Sand Tomb", "Dig") },
          "Superbloom baked back by Sahar" => proc { |r| changed?(r, "DESERT:1", [:foe, :foe_entry, :end_of_round]) } },
  6  => { "Heat Wave used" => proc { |r| used?(r, "Heat Wave") },
          "Corvin -> Wasteland" => proc { |r| changed?(r, "WASTELAND") } },
  7  => { "Lava Plume used" => proc { |r| used?(r, "Lava Plume") },
          "Brann re-melts -> Volcanic" => proc { |r| changed?(r, "VOLCANIC") } },
  8  => { "Frenzy reached" => proc { |r| r[:changes].any? { |c| c[:to] == "COLOSSEUM:2" } } },
  9  => { "Growth / Leech Seed / Aromatherapy / Grassy Terrain" => proc { |r| used?(r, "Growth", "Leech Seed", "Aromatherapy", "Grassy Terrain") },
          "garden grown by Juno" => proc { |r| r[:changes].any? { |c| c[:to] =~ /FLOWER_GARDEN:[2-5]/ && [:foe, :foe_entry].include?(c[:by]) } } },
  10 => { "Body Press / High Horsepower used" => proc { |r| used?(r, "Body Press", "High Horsepower") },
          "Anja cracks lake -> Water Surface" => proc { |r| changed?(r, "WATER_SURFACE") },
          "Anja refreezes -> Frozen Lake" => proc { |r| changed?(r, "FROZEN_LAKE") } },
  11 => { "Tailwind used" => proc { |r| used?(r, "Tailwind") }, "Wide Guard / Helping Hand" => proc { |r| used?(r, "Wide Guard", "Helping Hand") },
          "Sunny Day used" => proc { |r| used?(r, "Sunny Day") },
          "Odessa -> Rainbow" => proc { |r| changed?(r, "RAINBOW") } },
  12 => { "Trick Room used" => proc { |r| used?(r, "Trick Room") }, "Psychic Noise used" => proc { |r| used?(r, "Psychic Noise") },
          "Ilsa -> Inverse" => proc { |r| changed?(r, "INVERSE") },
          "Ilsa calms Nightmare" => proc { |r| changed?(r, "MINDSCAPE:1") } },
  13 => { "Explosion used" => proc { |r| used?(r, "Explosion") },
          "Bastian -> Cave" => proc { |r| changed?(r, "CAVE") },
          "Bastian relights -> Crystal Cavern" => proc { |r| changed?(r, "CRYSTAL_CAVERN") } },
  14 => { "Will-O-Wisp used" => proc { |r| used?(r, "Will-O-Wisp") },
          "Curse / Destiny Bond used" => proc { |r| used?(r, "Curse", "Destiny Bond") },
          "Ysolde re-haunts" => proc { |r| changed?(r, "HOLLOW_CATHEDRAL:1") } },
  15 => { "Shift Gear / Gear Grind" => proc { |r| used?(r, "Shift Gear", "Gear Grind") },
          "Magnet Rise used" => proc { |r| used?(r, "Magnet Rise") },
          "Magnus restarts -> Factory" => proc { |r| changed?(r, "FACTORY") } },
  16 => { "Abyss opened by Nyx" => proc { |r| changed?(r, "NEW_MOON:2") },
          "Fake Out / Snarl used" => proc { |r| used?(r, "Fake Out", "Snarl") },
          "Nyx snuffs Lamplight" => proc { |r| changed?(r, "NEW_MOON:1") } },
  17 => { "Fake Out / Helping Hand used" => proc { |r| used?(r, "Fake Out", "Helping Hand") }, "Follow Me used" => proc { |r| used?(r, "Follow Me") },
          "Celestine tames -> Fairy Tale" => proc { |r| changed?(r, "FAIRY_TALE") } },
  18 => { "Dragon Dance used" => proc { |r| used?(r, "Dragon Dance") },
          "Wyrmfire awakened by Sigrun" => proc { |r| changed?(r, "DRAGONS_DEN:2") },
          "Sigrun retakes -> Dragon's Den" => proc { |r| changed?(r, "DRAGONS_DEN") } }
}

if PARTS.include?("A")
  Prismfall::GYMS.each do |g|
    next if ONLY_T && !ONLY_T.include?(g[:trainer_type])
    runs = (1..SEEDS).map do |s|
      run_one("Gym #{g[:index]} #{g[:trainer_name]} seed #{s}", format("gym%02d", g[:index]), 2000 + g[:index] * 20 + s, g[:cap],
              Harness.generic_party(g[:cap], s), :badges => g[:index] - 1) { Prismfall.gym_battle(g[:index], :can_lose => true) }
    end
    summarise("Gym #{g[:index]} #{g[:trainer_name]} (#{g[:field]})", runs, WARDEN_PLAYS[g[:index]] || {}, RESULTS[:wardens])
  end
end

#-------------------------------------------------------------------------------
# B. Rivals, admins, bosses, Festival, story teams
#-------------------------------------------------------------------------------
def top_level(type, name, version)
  GameData::Trainer.get(type, name, version).pokemon.map { |p| p[:level] }.max
end

OTHERS = []
def other(label, level, plays = {}, double: false, &blk); OTHERS << [label, level, plays, double, blk]; end

[[1, 7], [2, 23], [3, 35], [4, 43], [5, 55], [6, 67], [7, 80], [8, 94], [9, 94]].each do |n, cap|
  plays = case n
          when 2 then { "Staravia seed Tailwind" => proc { |r| true } }   # checked from the log text below
          when 7 then { "Kestrel -> Dragon's Den" => proc { |r| changed?(r, "DRAGONS_DEN") } }
          else {}
          end
  plays = {} if n == 2
  other("RIVAL_KESTREL K#{n}", cap, plays) { Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", n, :can_lose => true) }
end
[[1, 19, { "Grassy Terrain used" => proc { |r| used?(r, "Grassy Terrain") }, "Juno -> Flower Garden" => proc { |r| changed?(r, "FLOWER_GARDEN") } }],
 [2, 35, { "Misty Terrain used" => proc { |r| used?(r, "Misty Terrain") }, "Juno cleanses -> Water Surface" => proc { |r| changed?(r, "WATER_SURFACE") } }],
 [4, 90, {}]].each do |n, cap, plays|
  other("RIVAL_JUNO J#{n}", cap, plays) { Prismfall.rival_battle(:RIVAL_JUNO, "Juno", n, :can_lose => true) }
end
def tb(type, name, version = 0, double: false)
  proc {
    setBattleRule("canLose")
    setBattleRule("double") if double
    TrainerBattle.start(type, name, version)
  }
end
other("HOLLOW_THISTLE Thistle", 15, {}, &tb(:HOLLOW_THISTLE, "Thistle"))
other("HOLLOW_TEO Teo", 23, {}, &tb(:HOLLOW_TEO, "Teo"))
other("HOLLOW_WICK Wick", 35, { "Heal Bell / Dazzling Gleam used" => proc { |r| used?(r, "Heal Bell", "Dazzling Gleam") },
                                 "Wick consecrates" => proc { |r| changed?(r, "HOLLOW_CATHEDRAL:2") } }, &tb(:HOLLOW_WICK, "Wick"))
other("MERIDIAN_QUENT Percival v0", 39, { "Rain Dance used" => proc { |r| used?(r, "Rain Dance") },
                                          "Quent damps -> Cinderglass" => proc { |r| changed?(r, "ASHEN_WASTE") } }, &tb(:MERIDIAN_QUENT, "Percival", 0))
other("HOLLOW_SABLE Sable (double)", 43, { "quake used" => proc { |r| used?(r, "Bulldoze", "Earthquake") },
                                            "Sable -> Cave" => proc { |r| changed?(r, "CAVE") } }, &tb(:HOLLOW_SABLE, "Sable", 0, :double => true))
other("HOLLOW_MOURNER Mourner", 43, { "Protect / Spiky Shield used" => proc { |r| used?(r, "Protect", "Spiky Shield") } }, &tb(:HOLLOW_MOURNER, "Mourner"))
other("MERIDIAN_MARCHETTI Helene v0", 55, {}, &tb(:MERIDIAN_MARCHETTI, "Helene", 0))
other("MERIDIAN_KROLL Sabine v0", 59, { "Kroll -> Nightmare" => proc { |r| changed?(r, "MINDSCAPE:2") } }, &tb(:MERIDIAN_KROLL, "Sabine", 0))
other("MERIDIAN_MARCHETTI Helene v1", 63, { "Marchetti re-darkens" => proc { |r| changed?(r, "DARK_CRYSTAL") } }, &tb(:MERIDIAN_MARCHETTI, "Helene", 1))
other("MERIDIAN_QUENT Percival v1 (double)", 71, { "Explosion used" => proc { |r| used?(r, "Explosion") },
                                                    "Quent wrecks -> Scrapyard" => proc { |r| changed?(r, "SCRAPYARD") },
                                                    "Quent restarts -> Factory" => proc { |r| changed?(r, "FACTORY") } }, &tb(:MERIDIAN_QUENT, "Percival", 1, :double => true))
other("MERIDIAN_KROLL Sabine v1", 75, { "ceiling cracked by Kroll" => proc { |r| changed?(r, "CAVE:2") } }, &tb(:MERIDIAN_KROLL, "Sabine", 1))
other("OCTAVE_VESPER Vesper v0", 19, {}, &tb(:OCTAVE_VESPER, "Vesper", 0))
other("OCTAVE_VESPER Vesper v1 (double)", 59, {}, &tb(:OCTAVE_VESPER, "Vesper", 1, :double => true))
[["Aria", 1, { "Aria Dive -> Underwater" => proc { |r| changed?(r, "UNDERWATER") } }], ["Cadence", 2, {}], ["Forte", 3, {}], ["Lento", 4, {}],
 ["Lyra", 5, { "garden grows on entry" => proc { |r| r[:changes].any? { |c| c[:to] == "FLOWER_GARDEN:4" } } }],
 ["Sona", 6, { "Sona -> Inverse" => proc { |r| changed?(r, "INVERSE") } }],
 ["Noct", 7, { "Abyss on entry" => proc { |r| r[:changes].any? { |c| c[:to] == "NEW_MOON:2" } } }], ["Carol", 8, {}]].each do |nm, v, plays|
  other("OCTAVE_SINGER #{nm} v#{v}", 90, plays, &tb(:OCTAVE_SINGER, nm, v))
end
other("OCTAVE_VESPER Vesper v2 (finale)", 92,
      { "field followed 3+ Eeveelutions" => proc { |r| r[:changes].count { |c| c[:by] == :foe_entry } >= 3 } }, &tb(:OCTAVE_VESPER, "Vesper", 2))
other("ASHKAAR_OFFICER Captain", 85, { "re-melt / eruption moves" => proc { |r| used?(r, "Lava Plume") } }) {
  setBattleRule("field", :ASHEN_WASTE); setBattleRule("canLose"); TrainerBattle.start(:ASHKAAR_OFFICER, "Captain", 0) }
other("ISENMAR_OFFICER Captain", 85, { "Aurora Veil used" => proc { |r| used?(r, "Aurora Veil") } }) {
  setBattleRule("field", :FROZEN_LAKE); setBattleRule("canLose"); TrainerBattle.start(:ISENMAR_OFFICER, "Captain", 0) }
other("LEADER_MARISOL Marisol v90 (Festival R16)", 90, {}, &tb(:LEADER_MARISOL, "Marisol", 90))
other("CHAMPION_VALEN Valen", 96, { "Stealth Rock / Trick Room in the opening" => proc { |r| used?(r, "Stealth Rock", "Trick Room") },
                                    "Rain Dance used" => proc { |r| used?(r, "Rain Dance") } }, &tb(:CHAMPION_VALEN, "Valen", 0))
other("MERIDIAN_VOSS Aurelian", 100, { "Shift Gear in the opening" => proc { |r| used?(r, "Shift Gear") } }) {
  setBattleRule("field", :PRISM_ARENA); setBattleRule("canLose"); TrainerBattle.start(:MERIDIAN_VOSS, "Aurelian", 0) }
other("ARCHSEER_DASK Imre v92", 92, { "Topsy-Turvy used" => proc { |r| used?(r, "Topsy-Turvy") },
                                      "Dask flips the field" => proc { |r| changed?(r, "MINDSCAPE") || changed?(r, "INVERSE") } }, &tb(:ARCHSEER_DASK, "Imre", 92))

if PARTS.include?("B")
  OTHERS.each do |label, level, plays, _double, blk|
    next if ONLY_T && !ONLY_T.include?(label.split(" ").first.to_sym)
    file = label.downcase.gsub(/[^a-z0-9]+/, "_")
    n = [SEEDS, 4].min
    runs = (1..n).map do |s|
      run_one("#{label} seed #{s}", file, 5000 + s, level, Harness.generic_party(level, s), :cap => level) { blk.call }
    end
    summarise(label, runs, plays, RESULTS[:others])
  end
end

#-------------------------------------------------------------------------------
# C. Gyms 1-3, Standard, realistic early-game challenger
#-------------------------------------------------------------------------------
# A starter (unevolved at 15, middle stage from 16) plus catches a player meets on the way, levels at or just under
# the cap, the moves the game gives them at that level, IV 15, no EVs, one Oran Berry. The AI plays both sides, with
# no bag items for the player and no switching for a type edge, so a careful human should do better than this.
EARLY = {
  # SPINE Rev 14 route order (design/SWAP_GYM1_GYM2.md). Gym 1 (Dorian, single): Ch1 catches, Strand Road. Gym 2 (Tamsin, DOUBLE):
  # inland -> Briarwick, with Eevee "Understudy" (gifted after Gym 1). Gym 3 (Marisol): north to Ebbmouth.
  1 => { :cap => 15, :starters => { "Grass starter" => [[:BULBASAUR, 15]], "Fire starter" => [[:CHARMANDER, 15]], "Water starter" => [[:SQUIRTLE, 15]] },
         # Ch1 catches only (520 Ferrymen's Mile, 521 Windfall Row): no Fighting type exists before Saltmere.
         :catches => [[:FLETCHLING, 13], [:SHINX, 12], [:ROLYCOLY, 12], [:LITLEO, 12], [:NIDORANmA, 12]] },
  2 => { :cap => 19, :starters => { "Grass starter" => [[:IVYSAUR, 19]], "Fire starter" => [[:CHARMELEON, 19]], "Water starter" => [[:WARTORTLE, 19]] },
         # + Eevee "Understudy" (after Gym 1), the Strand Road and the Weavers' Road (Crabrawler, Machop in Brinecut).
         :catches => [[:FLETCHINDER, 18], [:EEVEE, 17], [:LUXIO, 17], [:CRABRAWLER, 17], [:MACHOP, 17]] },
  3 => { :cap => 23, :starters => { "Grass starter" => [[:IVYSAUR, 23]], "Fire starter" => [[:CHARMELEON, 23]], "Water starter" => [[:WARTORTLE, 23]] },
         :catches => [[:FLETCHINDER, 21], [:LUXIO, 22], [:EEVEE, 21], [:MANKEY, 21], [:LOMBRE, 21], [:SEWADDLE, 20]] }
}
EARLY_STARTER_SPECIES = { "Grass starter" => :BULBASAUR, "Fire starter" => :CHARMANDER, "Water starter" => :SQUIRTLE }
if PARTS.include?("C")
  n = (ENV["PRISM_EARLY_SEEDS"] || "20").to_i
  EARLY.each do |gym, spec|
    next if EARLY_GYMS && !EARLY_GYMS.include?(gym)
    spec[:starters].each do |sname, starter|
      runs = (1..n).map do |s|
        keep = { 1 => 3, 2 => 4, 3 => 5 }[gym]   # 4 / 5 / 6 Pokemon: what a player has caught by then
        list = starter + spec[:catches].rotate(s % spec[:catches].size).first(keep)
        list = list.rotate(s % 2)   # the starter leads half the time
        run_one("Gym #{gym} realistic (#{sname}) seed #{s}", format("early_gym%d_%s", gym, sname[0, 1].downcase), 9000 + gym * 100 + s,
                spec[:cap], Harness.casual_party(list), :badges => gym - 1) { Prismfall.gym_battle(gym, :can_lose => true, :field => EARLY_FIELD) }
      end
      summarise("Gym #{gym} realistic, #{sname}", runs, {}, RESULTS[:early])
    end
  end
end

#-------------------------------------------------------------------------------
# Report
#-------------------------------------------------------------------------------
md = ["# Trainer harness run (logic test, AI on both sides)", "",
      "Generated by `tools/harness/run_trainers.rb`. Real Essentials v21.1 battle code and the Prismfall plugins; no visuals.",
      "\"Player won\" is the harness challenger, not a person.", ""]
unless RESULTS[:wardens].empty?
  md << "## Wardens (#{SEEDS} seeded fights each, generic cap-level challenger)" << ""
  md << "| Warden | Size | Player won | Avg turns | Designed plays used (fights out of #{SEEDS}) | Changes made by the Warden | Changes made by the challenger |"
  md << "|---|---|---|---|---|---|---|"
  RESULTS[:wardens].each do |r|
    md << "| #{r[:label]} | #{r[:sizes].map { |a| a ? "#{a[0]}v#{a[1]}" : '?' }.join(', ')} | #{r[:player_wins]}/#{r[:runs]} | #{r[:avg_turns]} | " \
          "#{r[:plays].map { |k, v| "#{k}: #{v}" }.join('; ')} | #{r[:foe_changes].map { |k, v| "#{k} x#{v}" }.join(', ')} | " \
          "#{r[:player_changes].map { |k, v| "#{k} x#{v}" }.join(', ')} |"
  end
  md << ""
end
unless RESULTS[:others].empty?
  md << "## Rivals, admins, bosses, Festival and story teams" << ""
  md << "| Battle | Start field | Size | Player won | Avg turns | Designed plays used | Changes made by the trainer |"
  md << "|---|---|---|---|---|---|---|"
  RESULTS[:others].each do |r|
    md << "| #{r[:label]} | #{r[:start_field].join(', ')} | #{r[:sizes].map { |a| a ? "#{a[0]}v#{a[1]}" : '?' }.join(', ')} | #{r[:player_wins]}/#{r[:runs]} | #{r[:avg_turns]} | " \
          "#{r[:plays].map { |k, v| "#{k}: #{v}/#{r[:runs]}" }.join('; ')} | #{r[:foe_changes].map { |k, v| "#{k} x#{v}" }.join(', ')} |"
  end
  md << ""
end
unless RESULTS[:early].empty?
  md << "## Gyms 1-3, Standard, realistic early-game challenger" << ""
  md << "| Fight | Challenger won | Avg turns |" << "|---|---|---|"
  RESULTS[:early].each { |r| md << "| #{r[:label]} | #{r[:player_wins]}/#{r[:runs]} (#{(100.0 * r[:player_wins] / r[:runs]).round}%) | #{r[:avg_turns]} |" }
  md << ""
end
md << "Exceptions: **#{RESULTS[:errors].size}**"
RESULTS[:errors].uniq { |e| [e[:class], e[:message]] }.first(8).each { |e| md << "- #{e[:name]}: #{e[:class]}: #{e[:message]} (#{Array(e[:backtrace]).first})" }
suffix = PARTS.sort.join
File.write(File.join(OUT_DIR, "PLAYS_#{suffix}.md"), md.join("\n") + "\n")
File.write(File.join(OUT_DIR, "results_trainers_#{suffix}.json"), JSON.pretty_generate(RESULTS))
puts "errors: #{RESULTS[:errors].size}"
RESULTS[:errors].uniq { |e| [e[:class], e[:message]] }.first(6).each do |e|
  puts "  [#{e[:name]}] #{e[:class]}: #{e[:message]}"
  puts "      " + Array(e[:backtrace]).first(6).join("\n      ")
end
