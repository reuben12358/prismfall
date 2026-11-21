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
#   PRISM_STARTERS=Fire (only those starters)   PRISM_FORCE=SPECIES (the first catch is that species: "a player who
#   found it"; a fight's own :force list does the same for every run of that fight)
#   PRISM_FOE_NOMEGA=1 takes MEGARING from every foe (the same fight without its Mega, for comparison)
#   PRISM_FOE_NOZ=1 swaps every foe's Z-crystal for a Life Orb (the same fight without its Z-move)
#   G7M, G10M, M12M, K5M, G11M and G17M (SPINE Rev 21/23: the Mega agent's hand-built prepared teams for the first
#   Mega fights) have PREPARED pools only: run them with PRISM_PREPARED=1.
#   Round 4 (tools/harness/winrates_r4.rb): G4-G18, K3-K9, J2, J4, WICK, Q8, MOURN, M12, KR13, M14, KR17, Q17, VALEN,
#   VOSS, QH against a TYPICAL team (default) or a PREPARED one (PRISM_PREPARED=1) built from what the game hands out
#   by then (winrate_pools.json + gifts, TMs, stones, the Mega Ring from 13 badges).
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

# The Saltmere audience (Prismfall Puzzles 007_Puzzles_SaltmereCrowd.rb): pf_house_rules sets the Grand Stage's opening
# stage and $game_temp.pf_home_crowd, which the field's "fans" rule reads through FieldEffects.home_crowd?. The run
# folder has no Puzzles plugin, so load that one file (its map-side helpers are only called from events).
CROWD_RB = File.expand_path("../../plugins/Prismfall Puzzles/007_Puzzles_SaltmereCrowd.rb", HARNESS_DIR)
load CROWD_RB if File.exist?(CROWD_RB)
def wr_house(audience)
  stage = (audience >= 14) ? 3 : (audience >= 7) ? 2 : 1
  setBattleRule("fieldStage", stage) if stage > 1
  $game_temp.pf_home_crowd = (audience >= 7) ? audience : nil if $game_temp.respond_to?(:pf_home_crowd=)
end

# Experiments on the full house (PRISM_EXP_HOUSE, harness only; proposals for the puzzle engineer / field owner).
# Shipped since (102_Field_GrandStage.rb): good house = his troupe basks at half; full house = only your side basks,
# only your attacks get the crit stage, his Sing can miss. These switches override those rules when set.
#   crit   with your fans in, Standing Ovation's +1 crit stage is for your side only ("the house is yours")
#   nobask with your fans in, Dorian's Normal types don't bask at Standing Ovation (the house cheers you, not him)
#   halfbask with your fans in, Dorian's Normal types bask for 1/32 instead of 1/16
#   heal8  your fans heal 1/8 at Standing Ovation instead of 1/16
if (EXP_HOUSE = ENV["PRISM_EXP_HOUSE"]) && FieldEffects.exists?(:GRAND_STAGE)
  d = FieldEffects.get(:GRAND_STAGE)
  nd = d.dup; nd.delete(:id)
  nd[:stages] = d[:stages].transform_values { |v| v.dup }
  s3 = nd[:stages][3]
  not_house_foe = proc { |_battle, b| !($game_temp.pf_home_crowd && b.opposes?) }
  EXP_HOUSE.split("+").each do |e|
    case e
    when "crit"
      s3[:crit_mods] = [{ :category => :damaging, :user => { :condition => not_house_foe }, :add => 1 }]
    when "nobask"
      s3[:end_of_round] = s3[:end_of_round].map do |r|
        next r if !r[:message].to_s.include?("basked")
        r2 = r.dup; r2[:battlers] = (r[:battlers] || {}).merge(:condition => not_house_foe); r2
      end
    when "halfbask"
      s3[:end_of_round] = s3[:end_of_round].flat_map do |r|
        next [r] if !r[:message].to_s.include?("basked")
        mine = r.dup; mine[:battlers] = (r[:battlers] || {}).merge(:condition => not_house_foe)
        theirs = r.dup; theirs[:battlers] = (r[:battlers] || {}).merge(:condition => proc { |bt, b| !not_house_foe.call(bt, b) })
        theirs[:heal] = 1/32r
        [mine, theirs]
      end
    when "heal8"
      s3[:end_of_round] = s3[:end_of_round].map { |r| r[:message].to_s.include?("stalls") ? r.merge(:heal => 1/8r) : r }
    end
  end
  FieldEffects.register(:GRAND_STAGE, nd)
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
    # Chapter 1 at Windfall Row (Picnicker Ada): the Ferrymen's Mile 520 and Windfall Row 521 (day and night, Headbutt
    # x0.3) plus the Tart Thief's Nickit (Ch1 quest). Flying is common (Pidove, Pikipek, Rookidee, Hoothoot).
    :ch1a  => { :SKWOVET => 20, :LECHONK => 15, :LILLIPUP => 15, :WOOLOO => 13, :PIKIPEK => 13, :YUNGOOS => 9,
                :ROOKIDEE => 8, :FLETCHLING => 4, :ROLYCOLY => 3, :HOOTHOOT => 20, :NICKIT => 25, :TAROUNTULA => 15,
                :RATTATA => 8, :SPINARAK => 15, :PIDOVE => 17, :BOUNSWEET => 12, :GOSSIFLEUR => 10, :SMOLIV => 12,
                :FIDOUGH => 9, :NIDORANfE => 10, :NIDORANmA => 10, :ZIGZAGOON => 12, :PIDGEY => 5, :SHINX => 4,
                :LITLEO => 3, :MEOWTH => 15, :POOCHYENA => 10, :NYMBLE => 10, :ODDISH => 15, :PINECO => 12,
                :COMBEE => 9, :BURMY => 6, :SQUAWKABILLY => 6, :AIPOM => 3 },
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
                :SHINX => 4, :MAREEP => 5, :JOLTIK => 5, :BLITZLE => 4, :GRUBBIN => 4,
                :EMOLGA => 2 }   # 5% at night only, in the secret Rimewood Glade (563, behind the Cut sapling)
  }
  # TMs the story has handed over by then (TM42 Facade from Dorian, TM98 Rock Smash at Brinecut, TM89 U-turn from Tamsin):
  # each goes to the first party member that can learn it, replacing its weakest move.
  TMS = { :none => [], :g2 => [:FACADE, :ROCKSMASH], :g3 => [:FACADE, :ROCKSMASH, :UTURN],
          :late => [:FACADE, :ROCKSMASH, :UTURN, :SURF] }   # Surf: Volcanic's advertised answer (two quench it)
  # The team is built over the whole journey: later pools include the earlier ones (a species keeps its best weight).
  POOLS[:ch3] = POOLS[:ch1_2].merge(POOLS[:ch3]) { |_k, a, b| [a, b].max }
  %i[g7 g10 k5 g11 m12 g17].each { |k| POOLS[k] = POOLS[:ch4] }   # (realistic runs of the *M cells fall back to Chapter 4: use PREPARED)
  POOLS[:ch4] = POOLS[:ch3].merge(POOLS[:ch4]) { |_k, a, b| [a, b].max }
  # A PREPARED player (PRISM_PREPARED=1): grinds every catch to the cap, keeps its strongest moves and hunts the best
  # type answers the availability doc allows by then (rare finds included), first listed first.
  PREPARED = {
    :ch1_2 => [:NACLI, :DWEBBLE, :SANDYGAST, :ROLYCOLY, :NICKIT, :KECLEON, :SHINX, :FLETCHLING],
    # SPINE Rev 21, the first Mega fights (POKEMON_AVAILABILITY.md 5, level-up evolution only; no ring: the player Megas
    # from 13 badges). Gym 7 (6 badges): Water, Ground, Rock for Brann.
    :g7  => [:WOOPER, :BARBOACH, :HIPPOPOTAS, :TYMPOLE, :BINACLE, :MUDBRAY],
    # Gym 10 (9 badges): Fire, Fighting, Steel and Electric for Anja.
    :g10 => [:MAKUHITA, :MIENFOO, :KLINK, :SKARMORY, :MAREEP, :HOUNDOUR],
    # K5 (10 badges): Fire for Scizor and Aegislash, Electric / Ice for Staraptor, Fighting and Fairy for the Dark types.
    :k5  => [:HOUNDOUR, :LAPRAS, :MAKUHITA, :SNUBBULL, :MAREEP, :FLETCHLING],
    # Gym 11 (10 badges): Electric, Rock, Ice for Odessa's fliers.
    :g11 => [:MAREEP, :ELECTRIKE, :RHYHORN, :LAPRAS, :ROCKRUFF, :BLITZLE],
    # Ch12 Marchetti (10 badges): Ground, Fighting, Fire for the Directorate's dogs and Corviknight.
    :m12 => [:HIPPOPOTAS, :MAKUHITA, :RHYHORN, :LAPRAS, :HOUNDOUR, :MIENFOO],
    # Gym 17 (16 badges): Steel and Poison for Celestine.
    :g17 => [:BELDUM, :DRILBUR, :GRIMER, :SKORUPI, :SKARMORY, :KLINK],
    :ch3   => [:PONYTA, :NACLI, :DWEBBLE, :FLETCHLING, :SPEAROW, :DODUO, :HOOTHOOT, :LITLEO],
    :ch4   => [:EMOLGA, :MAREEP, :SHINX, :JOLTIK, :SKIDDO, :SNOVER, :DEERLING, :HERACROSS]
  }
  PREP = ENV["PRISM_PREPARED"] == "1"
  FORCE = ENV["PRISM_FORCE"]&.split(",")&.map { |x| x.strip.upcase.to_sym }
  BAG = { :none => [], :ch1 => [:POTION] * 2, :g1 => [:POTION] * 3, :g2 => [:POTION, :POTION, :SUPERPOTION, :SUPERPOTION],
          :g3 => [:SUPERPOTION] * 3, :late => [:HYPERPOTION] * 3 }
  # fight => level cap, badges held, team size (starter included), catch pool, bag, how it starts
  FIGHTS = {
    # Chapter 1, Windfall Row (521, Meadow): Picnicker Ada (Oddish 6, Budew 7), the playtest's wall for the Water starter.
    # A sensible player there: the starter at Lv 9 (the playtest's Mudkip was 9-11), two catches from 520 / 521 at Lv 7
    # and 6, two Potions, healed at the Ferrow Poke Center before the road.
    "ADA" => { :label => "Picnicker Ada (Windfall Row, Ch1, Meadow)", :cap => 9, :lvcap => 15, :badges => 0, :size => 3,
               :pool => :ch1a, :bag => :ch1, :stage => 0, :offsets => [2, 3],
               :start => proc { setBattleRule("field", :MEADOW); setBattleRule("canLose"); TrainerBattle.start(:PICNICKER, "Ada") } },
    # The same fight with the starter alone (no catches: the wall a Water starter meets if it skips the grass).
    "ADA1" => { :label => "Picnicker Ada, the starter alone (Lv 9)", :cap => 9, :lvcap => 15, :badges => 0, :size => 1,
                :pool => :ch1a, :bag => :ch1, :stage => 0,
                :start => proc { setBattleRule("field", :MEADOW); setBattleRule("canLose"); TrainerBattle.start(:PICNICKER, "Ada") } },
    "K1" => { :label => "K1 Kestrel (intro, Lv 5 starter alone)", :cap => 5, :lvcap => 15, :badges => 0, :size => 1, :pool => :ch1_2,
              :bag => :none, :stage => 0, :start => proc { Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 1, :can_lose => true) } },
    "J1" => { :label => "J1 Juno (Saltmere green, before Gym 1)", :cap => 15, :badges => 0, :size => 6, :pool => :ch1_2,
              :bag => :g1, :stage => 0, :start => proc { Prismfall.rival_battle(:RIVAL_JUNO, "Juno", 1, :can_lose => true) } },
    "G1" => { :label => "Gym 1 Dorian (Grand Stage, single)", :cap => 15, :badges => 0, :size => 6, :pool => :ch1_2,
              :bag => :g1, :stage => 0, :start => proc { Prismfall.gym_battle(1, :can_lose => true) } },
    # Revision 19: the Saltmere crowd you met sets the Grand Stage's starting stage (1-3) for Dorian's fight.
    # Revision 19: the Saltmere audience (V313) sets the opening stage: 0-6 stage 1, 7-13 stage 2 + your fans heal your
    # side 1/16 a round, 14+ stage 3 (the fans keep cheering). G1S2 = 10 met, G1S3 = 18 met (pf_house_rules).
    "G1S2" => { :label => "Gym 1 Dorian, good house (10 met: Encore + fans)", :cap => 15, :badges => 0, :size => 6, :pool => :ch1_2,
                :bag => :g1, :stage => 0, :start => proc { wr_house(10); Prismfall.gym_battle(1, :can_lose => true) } },
    "G1S3" => { :label => "Gym 1 Dorian, full house (18 met: Standing Ovation + fans)", :cap => 15, :badges => 0, :size => 6, :pool => :ch1_2,
                :bag => :g1, :stage => 0, :start => proc { wr_house(18); Prismfall.gym_battle(1, :can_lose => true) } },
    # The same three houses with a team a level lower (starter 14, catches 14/13/13/12/12): a player who did not grind.
    "G1L14" => { :label => "Gym 1 Dorian, sparse house, Lv 14 team", :cap => 14, :badges => 0, :size => 6, :pool => :ch1_2,
                :bag => :g1, :stage => 0, :lvcap => 15, :offsets => [0, 1, 1, 2, 2], :start => proc { Prismfall.gym_battle(1, :can_lose => true) } },
    "G1S2L14" => { :label => "Gym 1 Dorian, good house, Lv 14 team", :cap => 14, :badges => 0, :size => 6, :pool => :ch1_2,
                :bag => :g1, :stage => 0, :lvcap => 15, :offsets => [0, 1, 1, 2, 2], :start => proc { wr_house(10); Prismfall.gym_battle(1, :can_lose => true) } },
    "G1S3L14" => { :label => "Gym 1 Dorian, full house, Lv 14 team", :cap => 14, :badges => 0, :size => 6, :pool => :ch1_2,
                :bag => :g1, :stage => 0, :lvcap => 15, :offsets => [0, 1, 1, 2, 2], :start => proc { wr_house(18); Prismfall.gym_battle(1, :can_lose => true) } },
    "G2" => { :label => "Gym 2 Tamsin (Silkwood, double)", :cap => 19, :badges => 1, :size => 6, :pool => :ch3,
              :bag => :g2, :tms => :g2, :stage => 1, :start => proc { Prismfall.gym_battle(2, :can_lose => true) } },
    "K2" => { :label => "K2 Kestrel (Gullcry Cliffs, before Gym 3)", :cap => 23, :badges => 2, :size => 6, :pool => :ch4,
              :bag => :g3, :tms => :g3, :stage => 1, :start => proc { Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 2, :can_lose => true) } },
    "G3" => { :label => "Gym 3 Marisol (Water Surface)", :cap => 23, :badges => 2, :size => 6, :pool => :ch4,
              :bag => :g3, :tms => :g3, :stage => 1, :start => proc { Prismfall.gym_battle(3, :can_lose => true) } },
    # The earned Electric answer for a Fire starter: the night-only Emolga of the secret Rimewood Glade (5%, Lv 17-19).
    "G3E" => { :label => "Gym 3 Marisol, a team that found the Glade's night Emolga", :cap => 23, :badges => 2, :size => 6,
               :pool => :ch4, :bag => :g3, :tms => :g3, :stage => 1, :force => [:EMOLGA],
               :start => proc { Prismfall.gym_battle(3, :can_lose => true) } },
    # SPINE Rev 21: the first Mega fights, prepared teams only (PRISM_PREPARED=1), no Mega on the player's side.
    "G7M" => { :label => "Gym 7 Brann (Volcanic; weak Mega Camerupt)", :cap => 39, :badges => 6, :size => 6, :pool => :g7,
              :bag => :late, :tms => :late, :stage => 1, :start => proc { Prismfall.gym_battle(7, :can_lose => true) } },
    "G10M" => { :label => "Gym 10 Anja (Frozen Lake; Mega Glalie)", :cap => 51, :badges => 9, :size => 6, :pool => :g10,
               :bag => :late, :tms => :late, :stage => 1, :start => proc { Prismfall.gym_battle(10, :can_lose => true) } },
    "K5M" => { :label => "K5 Kestrel (Skyreach, Stormfront; no Mega: no ring yet)", :cap => 55, :badges => 10, :size => 6, :pool => :k5,
              :bag => :late, :tms => :late, :stage => 1,
              :start => proc { Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 5, :can_lose => true, :field => :STORMFRONT) } },
    "M12M" => { :label => "Ch12 Marchetti (Skyreach catwalks, Stormfront; Mega Manectric)", :cap => 55, :badges => 10, :size => 6,
               :pool => :m12, :bag => :late, :tms => :late, :stage => 1,
               :start => proc { setBattleRule("canLose"); setBattleRule("field", :STORMFRONT)
                                TrainerBattle.start(:MERIDIAN_MARCHETTI, "Helene", 0) } },
    "G17M" => { :label => "Gym 17 Celestine (Fairy Tale, double; Mimikyu's Z-move)", :cap => 80, :badges => 16, :size => 6,
               :pool => :g17, :bag => :late, :tms => :late, :stage => 1, :start => proc { Prismfall.gym_battle(17, :can_lose => true) } },
    "G11M" => { :label => "Gym 11 Odessa (Stormfront, double; Mega Pidgeot)", :cap => 55, :badges => 10, :size => 6, :pool => :g11,
               :bag => :late, :tms => :late, :stage => 1, :start => proc { Prismfall.gym_battle(11, :can_lose => true) } }
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
  # SPINE Rev 21 late cells (G7M, G10M, K5M, G11M, M12M, G17M): a PREPARED late-game player has more than level-up moves. Fixed sets
  # with the mid-game TMs (Surf, Rock Slide, Bulldoze by Gym 7; Earthquake, Flamethrower, Ice Beam, Thunderbolt and the
  # like by Gym 10), IV 20-31, EV 85 each (Standard trainers' own default), a fitting nature; the starter (at the cap)
  # gets its own set; five of the six listed answers, shuffled by seed. No Mega: the player has no ring before 13.
  # [species, ability, nature, moves]
  LATE = {
    :g7 => { "Grass" => [:VENUSAUR, :OVERGROW, :MODEST, [:GIGADRAIN, :SLUDGEBOMB, :BULLDOZE, :SLEEPPOWDER]],
             "Fire" => [:CHARIZARD, :BLAZE, :TIMID, [:FLAMETHROWER, :AIRSLASH, :DRAGONCLAW, :ROCKSLIDE]],
             "Water" => [:BLASTOISE, :TORRENT, :MODEST, [:SURF, :ICEBEAM, :BULLDOZE, :PROTECT]],
             :team => [[:QUAGSIRE, :WATERABSORB, :RELAXED, [:SURF, :BULLDOZE, :YAWN, :PROTECT]],
                       [:WHISCASH, :OBLIVIOUS, :ADAMANT, [:WATERFALL, :BULLDOZE, :ROCKSLIDE, :ZENHEADBUTT]],
                       [:HIPPOWDON, :SANDSTREAM, :IMPISH, [:BULLDOZE, :ROCKSLIDE, :CRUNCH, :SLACKOFF]],
                       [:SEISMITOAD, :SWIFTSWIM, :MODEST, [:SURF, :BULLDOZE, :SLUDGEBOMB, :FOCUSBLAST]],
                       [:BARBARACLE, :TOUGHCLAWS, :ADAMANT, [:RAZORSHELL, :ROCKSLIDE, :XSCISSOR, :NIGHTSLASH]],
                       [:MUDSDALE, :STAMINA, :ADAMANT, [:HIGHHORSEPOWER, :ROCKSLIDE, :HEAVYSLAM, :BODYPRESS]]] },
    :g10 => { "Grass" => [:VENUSAUR, :OVERGROW, :MODEST, [:GIGADRAIN, :SLUDGEBOMB, :EARTHPOWER, :SLEEPPOWDER]],
              "Fire" => [:CHARIZARD, :BLAZE, :TIMID, [:FLAMETHROWER, :AIRSLASH, :DRAGONPULSE, :FOCUSBLAST]],
              "Water" => [:BLASTOISE, :TORRENT, :MODEST, [:SURF, :ICEBEAM, :DARKPULSE, :FOCUSBLAST]],
              # Fire, Fighting and Steel that don't drown in Walrein's Water or Mamoswine's Ground; Electric for the
              # Water-Ice pair (the Rock types are 4x weak to Anja's coverage).
              :team => [[:HARIYAMA, :THICKFAT, :ADAMANT, [:CLOSECOMBAT, :KNOCKOFF, :BULLETPUNCH, :HEAVYSLAM]],
                        [:MIENSHAO, :REGENERATOR, :JOLLY, [:CLOSECOMBAT, :STONEEDGE, :KNOCKOFF, :UTURN]],
                        [:KLINKLANG, :CLEARBODY, :ADAMANT, [:GEARGRIND, :WILDCHARGE, :SHIFTGEAR, :PROTECT]],
                        [:SKARMORY, :STURDY, :IMPISH, [:BODYPRESS, :IRONHEAD, :BRAVEBIRD, :ROOST]],
                        [:AMPHAROS, :STATIC, :MODEST, [:THUNDERBOLT, :DISCHARGE, :FOCUSBLAST, :POWERGEM]],
                        [:HOUNDOOM, :FLASHFIRE, :TIMID, [:FLAMETHROWER, :DARKPULSE, :SLUDGEBOMB, :NASTYPLOT]]] },
    :k5 => { "Grass" => [:VENUSAUR, :OVERGROW, :MODEST, [:GIGADRAIN, :SLUDGEBOMB, :EARTHPOWER, :SLEEPPOWDER]],
             "Fire" => [:CHARIZARD, :BLAZE, :TIMID, [:FLAMETHROWER, :AIRSLASH, :DRAGONPULSE, :FOCUSBLAST]],
             "Water" => [:BLASTOISE, :TORRENT, :MODEST, [:SURF, :ICEBEAM, :DARKPULSE, :FOCUSBLAST]],
             # Fire for Scizor and Aegislash, Water / Ice for Krookodile and Zweilous, Electric for Staraptor, Fighting
             # and Fairy for the Dark types.
             :team => [[:HOUNDOOM, :FLASHFIRE, :TIMID, [:FLAMETHROWER, :DARKPULSE, :SLUDGEBOMB, :NASTYPLOT]],
                       [:LAPRAS, :WATERABSORB, :MODEST, [:SURF, :ICEBEAM, :THUNDERBOLT, :FREEZEDRY]],
                       [:HARIYAMA, :THICKFAT, :ADAMANT, [:CLOSECOMBAT, :KNOCKOFF, :BULLETPUNCH, :STONEEDGE]],
                       [:GRANBULL, :INTIMIDATE, :ADAMANT, [:PLAYROUGH, :CLOSECOMBAT, :FIREFANG, :THUNDERFANG]],
                       [:AMPHAROS, :STATIC, :MODEST, [:THUNDERBOLT, :DRAGONPULSE, :FOCUSBLAST, :POWERGEM]],
                       [:TALONFLAME, :FLAMEBODY, :ADAMANT, [:FLAREBLITZ, :BRAVEBIRD, :UTURN, :ROOST]]] },
    # Gym 17 Celestine (Fairy Tale, double, 80; SPINE Rev 23: her Mimikyu's Z-move). Steel and Poison (Fire is no Steel
    # answer here: dragonfire); Protect for the double.
    :g17 => { "Grass" => [:VENUSAUR, :OVERGROW, :MODEST, [:SLUDGEBOMB, :EARTHPOWER, :GIGADRAIN, :PROTECT]],
              "Fire" => [:CHARIZARD, :BLAZE, :TIMID, [:AIRSLASH, :FOCUSBLAST, :FLAMETHROWER, :PROTECT]],
              "Water" => [:BLASTOISE, :TORRENT, :MODEST, [:FLASHCANNON, :SURF, :ICEBEAM, :PROTECT]],
              :team => [[:METAGROSS, :CLEARBODY, :ADAMANT, [:METEORMASH, :ZENHEADBUTT, :BULLETPUNCH, :PROTECT]],
                        [:EXCADRILL, :MOLDBREAKER, :JOLLY, [:IRONHEAD, :EARTHQUAKE, :ROCKSLIDE, :PROTECT]],
                        [:MUK, :STENCH, :ADAMANT, [:GUNKSHOT, :POISONJAB, :SHADOWSNEAK, :PROTECT]],
                        [:DRAPION, :SNIPER, :JOLLY, [:CROSSPOISON, :KNOCKOFF, :EARTHQUAKE, :PROTECT]],
                        [:SKARMORY, :STURDY, :IMPISH, [:IRONHEAD, :BRAVEBIRD, :ROOST, :PROTECT]],
                        [:KLINKLANG, :CLEARBODY, :ADAMANT, [:GEARGRIND, :WILDCHARGE, :SHIFTGEAR, :PROTECT]]] },
    :m12 => { "Grass" => [:VENUSAUR, :OVERGROW, :MODEST, [:GIGADRAIN, :SLUDGEBOMB, :EARTHPOWER, :SLEEPPOWDER]],
              "Fire" => [:CHARIZARD, :BLAZE, :TIMID, [:FLAMETHROWER, :AIRSLASH, :DRAGONPULSE, :FOCUSBLAST]],
              "Water" => [:BLASTOISE, :TORRENT, :MODEST, [:SURF, :ICEBEAM, :DARKPULSE, :FOCUSBLAST]],
              # Ground for the Electric dogs and Arcanine, Fighting for Mabosstiff, Fire for Corviknight.
              :team => [[:HIPPOWDON, :SANDSTREAM, :IMPISH, [:EARTHQUAKE, :STONEEDGE, :CRUNCH, :SLACKOFF]],
                        [:HARIYAMA, :THICKFAT, :ADAMANT, [:CLOSECOMBAT, :KNOCKOFF, :BULLETPUNCH, :STONEEDGE]],
                        [:RHYDON, :LIGHTNINGROD, :ADAMANT, [:STONEEDGE, :EARTHQUAKE, :MEGAHORN, :FIREPUNCH]],
                        [:LAPRAS, :WATERABSORB, :MODEST, [:SURF, :ICEBEAM, :THUNDERBOLT, :FREEZEDRY]],
                        [:HOUNDOOM, :FLASHFIRE, :TIMID, [:FLAMETHROWER, :DARKPULSE, :SLUDGEBOMB, :NASTYPLOT]],
                        [:MIENSHAO, :REGENERATOR, :JOLLY, [:CLOSECOMBAT, :STONEEDGE, :KNOCKOFF, :UTURN]]] },
    :g11 => { "Grass" => [:VENUSAUR, :OVERGROW, :MODEST, [:GIGADRAIN, :SLUDGEBOMB, :EARTHPOWER, :PROTECT]],
              "Fire" => [:CHARIZARD, :BLAZE, :TIMID, [:FLAMETHROWER, :AIRSLASH, :ROCKSLIDE, :PROTECT]],
              "Water" => [:BLASTOISE, :TORRENT, :MODEST, [:SURF, :ICEBEAM, :FLASHCANNON, :PROTECT]],
              :team => [[:AMPHAROS, :STATIC, :MODEST, [:THUNDERBOLT, :DISCHARGE, :POWERGEM, :PROTECT]],
                        [:MANECTRIC, :LIGHTNINGROD, :TIMID, [:THUNDERBOLT, :FLAMETHROWER, :SNARL, :PROTECT]],
                        [:RHYDON, :LIGHTNINGROD, :ADAMANT, [:ROCKSLIDE, :STONEEDGE, :EARTHQUAKE, :PROTECT]],
                        [:LAPRAS, :WATERABSORB, :MODEST, [:ICEBEAM, :THUNDERBOLT, :SURF, :PROTECT]],
                        [:LYCANROC, :SANDRUSH, :JOLLY, [:ROCKSLIDE, :STONEEDGE, :CRUNCH, :PROTECT]],
                        [:ZEBSTRIKA, :LIGHTNINGROD, :TIMID, [:THUNDERBOLT, :DISCHARGE, :OVERHEAT, :PROTECT]]] }
  }
  def self.late_mon(entry, level, rng)
    sp, ab, nat, moves = entry
    p = Pokemon.new(sp, level)
    GameData::Stat.each_main { |s| p.iv[s.id] = 20 + rng.rand(12); p.ev[s.id] = 85 }
    p.ability = ab if p.species_data.abilities.include?(ab) || p.species_data.hidden_abilities.include?(ab)
    p.nature = nat
    p.forget_all_moves
    moves.each { |m| p.learn_move(m) }
    p.calc_stats
    p
  end

  EVENT_IN = { :ch1a => [:NICKIT], :ch1_2 => [:KECLEON, :NICKIT], :ch3 => [:KECLEON, :NICKIT, :TIMBURR, :CRABRAWLER, :SMEARGLE, :RALTS, :PONYTA_G],
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
    return WR4.party(fight, f, starter_lines, seed, PREP, Prismfall::Difficulty.current) if f[:r4]
    if PREP && LATE[f[:pool]]
      late = LATE[f[:pool]]
      sname = STARTERS.key(starter_lines)
      party = [late_mon(late[sname], f[:cap], rng)]
      late[:team].shuffle(random: rng).first(f[:size] - 1).each { |e| party << late_mon(e, f[:cap], rng) }
      party = party.rotate(rng.rand(party.size))
      party[0].item = :ORANBERRY
      return party
    end
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
    forced = FORCE || f[:force]
    if forced   # the player found it: it takes the first catch slot (cap - 1)
      catches = (forced + (catches - forced)).first(f[:size] - 1)
    end
    offsets = f[:offsets] || [1, 1, 2, 2, 3]   # starter at the cap; the rest a little behind it
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

load File.join(HARNESS_DIR, "winrates_r4.rb")
WR4.fights.each { |k, v| WR::FIGHTS[k] = v }

Harness.new_game_state
if ENV["PRISM_FOE_NOZ"] == "1"
  EventHandlers.add(:on_trainer_load, :winrates_foe_noz,
    proc { |tr| tr.party.each { |pk| pk.item = :LIFEORB if pk && PrismfallZ.crystal?(pk.item_id) } if tr && tr.respond_to?(:party) })
end
if ENV["PRISM_FOE_NOMEGA"] == "1"
  EventHandlers.add(:on_trainer_load, :winrates_foe_nomega, proc { |tr| tr.items.delete(:MEGARING) if tr && tr.respond_to?(:items) })
end
RESULTS = []
ERRORS = []
MODES.each do |mode|
  Prismfall::Difficulty.set(mode)
  FIGHTS.each do |fight|
    f = WR::FIGHTS[fight] or next
    WR::STARTERS.each do |sname, lines|
      next if ENV["PRISM_STARTERS"] && !ENV["PRISM_STARTERS"].split(",").map(&:strip).include?(sname)
      Prismfall.record_starter(lines[0])
      runs = (1..SEEDS).map do |s|
        seed = 40_000 + fight.sum * 7 + s * 101 + lines[0].to_s.sum
        Harness.set_badges(f[:badges])
        Prismfall::LevelCap.set_override(f[:lvcap] || f[:cap])
        $player.party = WR.party(fight, lines, seed)
        if ENV["PRISM_SHOW_TEAMS"] && s <= ENV["PRISM_SHOW_TEAMS"].to_i
          puts "  #{mode} #{fight} #{sname} s#{s}: " + $player.party.map { |pk|
            "#{pk.species} #{pk.level} @#{pk.item_id} [#{pk.ability_id}] #{pk.moves.map(&:id).join('/')}" }.join(" | ")
        end
        bag = (mode == :HARD && ENV["PRISM_HARD_BAG"] != "1") ? [] : (f[:r4] ? WR4::BAG[WR4.bag_for(f[:badges])] : WR::BAG[f[:bag]]).dup
        $bag.clear if $bag.respond_to?(:clear)
        bag.each { |it| $bag.add(it) }
        $bag.add(:MEGARING) if f[:r4] && f[:badges] >= 13   # SPINE Rev 21/23: the ring from Badge 13 (Megas and Z-moves)
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
