#===============================================================================
# The Battle of the Glass Dunes (map 926) and the Steamline (925): field-sequence
# probes for the war climax (field workstream; companion to run_all.rb).
#   PRISM_RUN_DIR=<private run dir> PRISM_OUT=<out dir> ruby tools/harness/run_glass_dunes.rb
# Real Essentials v21.1 battle code + Prismfall Core / Field Effects / Bosses. Logic test only.
#
#   A. scripted walk on 926's own default field: DESERT -> (Origin Pulse) FLOODED_DUNES -> (Blue Flare)
#      GLASS_DUNES -> two beam clashes -> BLEED, which may only echo the war's fields
#   B. Primal Kyogre: Primordial Sea floods the dunes at send-out; Reshiram's snuffed Blue Flare still glasses
#      them; two Origin Pulses re-flood the glass; Fusion Flare glasses it again (the tug of war)
#   C. AI vs AI: a 3-bar Reshiram boss (harness-only definition; its first break brings the flood-sea in)
#      against an AI-piloted Kyogre team on 926
#   D. AI vs AI: a Primal Kyogre boss (harness-only) against an AI-piloted fire team on 926
#   E. the tide: Flooded Dunes under Sunny Day drains into the Desert's Superbloom
#   F. the Steamline 925: default field is the Bleed, and it borrows only from the war pool
#      (control: the same Bleed on a map without a pool borrows from every field)
#   G. AI vs AI soldiers on 926 (Isenmar and Ashkaar captains from pbs/trainers.txt, if compiled in)
# Writes <PRISM_OUT>/<letter>_*.txt logs and SUMMARY.md, results.json. Every AI-chosen move is logged
# with FieldEffects::AIField's transition score.
#===============================================================================
require "json"
require "fileutils"
load File.join(__dir__, "boot.rb")
load File.join(HARNESS_DIR, "log_scene.rb")
load File.join(HARNESS_DIR, "probes.rb")

OUT_DIR = ENV["PRISM_OUT"] || File.expand_path("../../docs/battle_captures/glass_dunes", HARNESS_DIR)
FileUtils.mkdir_p(OUT_DIR)

WAR_POOL = FieldEffects::MAP_BORROW_POOLS[926] || []

module Harness
  module GlassDunes
    module_function

    def mk(*a, **k); Harness::Probes.mk(*a, **k); end

    def borrowed_log
      @borrowed_log ||= []
    end

    # AIField transition score of every move of battler idx, as a log line.
    def log_ai_scores(battle, idx)
      b = battle.battlers[idx]
      return if !b || b.fainted?
      parts = b.moves.map do |m|
        next nil if !m
        type = m.pbCalcType(b)
        s = FieldEffects::AIField.score_change(battle, b, m, type)
        info = FieldEffects.transition_this_move_advances(battle, b, m, type)
        dest = info ? " -> #{info[2][0]}#{info[2][1] > 1 ? " st#{info[2][1]}" : ''} (#{info[0] + 1}/#{info[1]})" : ""
        "#{m.name} #{format('%+d', s)}#{dest}"
      end.compact
      Harness.log&.add("[AIField @ #{battle.field_effect}#{battle.field_stage > 1 ? " st#{battle.field_stage}" : ''}] " \
                       "#{b.name}: #{parts.join(', ')}", "  ")
    end

    # A wild battle with both sides scripted (move IDs per turn; nil/empty = Splash for the foe, end for the player).
    def duel(title, party:, foe:, player:, foe_moves:, map: 926, field: nil, seed: 4242, rng: :mid)
      $game_map = Harness::FakeMap.new(map)
      $player.party = Array(party)
      setup = lambda do |battle|
        battle.define_singleton_method(:pbRandom) { |x| (rng == :mid) ? x / 2 : 0 } if rng
        pq = player.dup
        fq = foe_moves.dup
        battle.instance_variable_get(:@battleAI).define_singleton_method(:pbDefaultChooseEnemyCommand) do |idx|
          b = @battle.battlers[idx]
          mine = @battle.pbOwnedByPlayer?(idx)
          step = (mine ? pq : fq).shift
          if step.nil?
            if mine
              @battle.decision = 3
              next
            end
            step = :SPLASH
          end
          Harness::GlassDunes.log_ai_scores(@battle, idx)
          i = b.moves.index { |m| m && m.id == step }
          if !i
            b.moves[0] = Battle::Move.from_pokemon_move(@battle, Pokemon::Move.new(step))
            i = 0
          end
          @battle.pbRegisterMove(idx, i, false)
        end
      end
      Harness.run_battle(title, :seed => seed, :setup => setup) do
        setBattleRule("field", field) if field
        setBattleRule("canLose")
        setBattleRule("cannotRun")
        WildBattle.start(foe)
      end
    end

    # AI on both sides (player side piloted by the harness AI); every choice logs AIField scores first.
    def ai_setup
      lambda do |battle|
        ai = battle.instance_variable_get(:@battleAI)
        orig = ai.method(:pbDefaultChooseEnemyCommand)
        ai.define_singleton_method(:pbDefaultChooseEnemyCommand) do |idx|
          Harness::GlassDunes.log_ai_scores(@battle, idx)
          orig.call(idx)
        end
      end
    end

    def ai_boss(title, party:, boss:, map: 926, seed: 77)
      $game_map = Harness::FakeMap.new(map)
      $player.party = party
      Harness.run_battle(title, :seed => seed, :setup => ai_setup) do
        Prismfall::Bosses.wild_battle(boss, :can_lose => true)
      end
    end

    def ai_trainer(title, party:, type:, name:, version:, map: 926, seed: 99)
      $game_map = Harness::FakeMap.new(map)
      $player.party = party
      Harness.run_battle(title, :seed => seed, :setup => ai_setup) do
        setBattleRule("canLose")
        TrainerBattle.start(type, name, version)
      end
    end

    def seq(log)
      log.field_changes.map { |o, n, st| (o == n) ? "#{n} st#{st}" : n.to_s }
    end

    def chain_ok?(log, *ids)
      s = log.field_changes.map { |_o, n, _st| n }
      i = 0
      s.each { |id| i += 1 if i < ids.length && id == ids[i] }
      i == ids.length
    end

    def write(name, log)
      banner = "LOGIC-TEST OUTPUT (headless harness, real Essentials v21.1 battle code + Prismfall plugins).\n" \
               "Not a game screenshot: no EBDX visuals were rendered.\n\n"
      File.write(File.join(OUT_DIR, "#{name}.txt"), banner + log.text)
    end
  end
end

EventHandlers.add(:prismfall_field_overlay_changed, :glass_dunes_pool,
  proc { |battle, field_id, _old, new_ids| Harness::GlassDunes.borrowed_log << [$game_map.map_id, field_id, new_ids.dup] })

def strong(species, level, moves, ability: nil, item: nil)
  Harness::Probes.mk(species, level, :moves => moves, :ability => ability, :item => item)
end

# Scripted walks must outlast every scripted turn: 252 HP / 252 Sp. Def, Leftovers.
def bulky(species, level, moves, ability: nil)
  p = strong(species, level, moves, :ability => ability, :item => :LEFTOVERS)
  p.ev[:HP] = 252
  p.ev[:SPECIAL_DEFENSE] = 252
  p.calc_stats
  p
end

Harness.new_game_state
Prismfall.record_starter(:CHARMANDER)
$player.badges = Array.new(18) { true }
Prismfall::LevelCap.unlock_finale!
G = Harness::GlassDunes
RES = { :war_pool => WAR_POOL, :scenarios => [] }

def record(key, title, log, checks)
  G.write(key, log)
  ok = checks.values.all?
  RES[:scenarios] << { :key => key, :title => title, :outcome => Harness::OUTCOMES[log.outcome] || "CRASHED",
                       :turns => log.turns, :errors => log.errors.size, :fields => G.seq(log), :checks => checks,
                       :ok => ok && log.errors.empty? }
  puts format("%-44s %-11s %3d turns  errors:%d  %s", key, RES[:scenarios].last[:outcome], log.turns, log.errors.size,
              ok ? "checks ok" : "CHECKS FAILED #{checks.reject { |_k, v| v }.keys.inspect}")
  puts "    fields: #{G.seq(log).join(' > ')}"
end

#-------------------------------------------------------------------------------
# A. Scripted walk on the map's own default field
#-------------------------------------------------------------------------------
G.borrowed_log.clear
kyogre   = bulky(:KYOGRE, 100, [:ORIGINPULSE, :HYDROPUMP, :ICEBEAM, :THUNDER], :ability => :PRESSURE)
reshiram = bulky(:RESHIRAM, 100, [:BLUEFLARE, :FUSIONFLARE, :DRAGONPULSE, :EARTHPOWER])
# T1 Origin Pulse floods the desert; T2 Blue Flare glasses the flood; T3-T4 both beams land on the glass in the
# same round (two clashes) -> the Bleed; T5-T10 quiet, so the Bleed rotates through its echoes.
log = G.duel("A. Glass Dunes walk (map 926 default, no field rule): Kyogre vs Reshiram, both scripted",
             :party => kyogre, :foe => reshiram,
             :player    => [:ORIGINPULSE, :SPLASH, :ORIGINPULSE, :HYDROPUMP] + [:SPLASH] * 6,
             :foe_moves => [:DRAGONPULSE, :BLUEFLARE, :BLUEFLARE, :FUSIONFLARE] + [:SPLASH] * 6)
a_borrowed = G.borrowed_log.select { |m, f, _| m == 926 && f == :BLEED }.flat_map(&:last).uniq
record("A_walk_desert_flood_glass_bleed", log.title, log, {
  :starts_on_desert     => log.field_changes.first == [:NONE, :DESERT, 1],
  :desert_flood_glass   => G.chain_ok?(log, :DESERT, :FLOODED_DUNES, :GLASS_DUNES),
  :beam_clash_to_bleed  => G.chain_ok?(log, :DESERT, :FLOODED_DUNES, :GLASS_DUNES, :BLEED),
  :transform_strike     => log.include?("The sea answered the pulse") && log.include?("fused the drowned sand into glass"),
  :steam_on_flood       => log.include?("scalding steam"),
  :clash_progress       => log.include?("The glass is singing with both Imprints"),
  :bleed_echoes_war_only => !a_borrowed.empty? && (a_borrowed - WAR_POOL).empty?
})
puts "    Bleed echoed: #{a_borrowed.inspect}"

#-------------------------------------------------------------------------------
# B. Primal Kyogre: the sea at send-out, the snuffed Blue Flare still glasses it
#-------------------------------------------------------------------------------
pk = bulky(:KYOGRE, 85, [:ORIGINPULSE, :WATERSPOUT, :ICEBEAM, :THUNDER], :ability => :PRIMORDIALSEA)
rs = bulky(:RESHIRAM, 100, [:BLUEFLARE, :FUSIONFLARE, :DRAGONPULSE, :EARTHPOWER])
log = G.duel("B. Primal Kyogre (Primordial Sea) vs Reshiram on 926: flood at send-out, glass under the heavy rain",
             :party => pk, :foe => rs,
             :player    => [:THUNDER, :ORIGINPULSE, :ORIGINPULSE, :THUNDER, :THUNDER],
             :foe_moves => [:BLUEFLARE, :DRAGONPULSE, :DRAGONPULSE, :FUSIONFLARE, :DRAGONPULSE])
first_turn = log.lines.index { |l| l.include?("--- Turn 1 ---") } || 0
flood_line = log.lines.index { |l| l.include?("FIELD CHANGE: DESERT -> FLOODED_DUNES") } || 9999
record("B_primal_sea_tug_of_war", log.title, log, {
  :flood_before_turn_1   => flood_line < first_turn,
  :snuffed_flare_glasses => log.include?("fizzled out in the heavy rain") && G.chain_ok?(log, :DESERT, :FLOODED_DUNES, :GLASS_DUNES),
  :origin_pulse_refloods => G.chain_ok?(log, :DESERT, :FLOODED_DUNES, :GLASS_DUNES, :FLOODED_DUNES),
  :fusion_flare_reglass  => G.chain_ok?(log, :DESERT, :FLOODED_DUNES, :GLASS_DUNES, :FLOODED_DUNES, :GLASS_DUNES)
})

#-------------------------------------------------------------------------------
# C. AI duel: 3-bar Reshiram boss, the flood-sea comes in on its first break
#-------------------------------------------------------------------------------
Prismfall::Bosses.register(:HARNESS_RESHIRAM_GLASSDUNES, {
  :species => :RESHIRAM, :level => 85, :ability => :TURBOBLAZE, :nature => :MODEST, :ivs => 31,
  :evs => { :HP => 252, :SPECIAL_ATTACK => 252, :SPEED => 4 },
  :moves => [:BLUEFLARE, :DRAGONPULSE, :EARTHPOWER, :FLAMETHROWER], :bars => 3,
  :intro => ["The Light Stone cracks white... Reshiram unfolds over the Siege Camp!"],
  :on_break => { :cure_status => true, :reset_stats => :negative },
  :breaks => { 1 => { :messages => ["The Northern Sea stands up on the horizon - Kyogre's flood-sea is pouring over the dunes!"],
                      :field => :FLOODED_DUNES, :field_message => "", :weather => :Rain } }
})
party_c = [strong(:KYOGRE, 85, [:ORIGINPULSE, :ICEBEAM, :THUNDER, :CALMMIND], :ability => :DRIZZLE),
           strong(:GARCHOMP, 85, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :SWORDSDANCE]),
           strong(:LAPRAS, 85, [:HYDROPUMP, :FREEZEDRY, :THUNDERBOLT, :ICESHARD])]
log = G.ai_boss("C. AI vs AI: Reshiram boss (3 bars, break 1 = the flood-sea) vs Kyogre, Garchomp, Lapras on 926",
                :party => party_c, :boss => :HARNESS_RESHIRAM_GLASSDUNES)
fired_flare = log.lines.count { |l| l.include?("used Blue Flare") }
record("C_ai_reshiram_boss", log.title, log, {
  :starts_on_desert => log.field_changes.first&.[](1) == :DESERT,
  :reaches_flood    => G.chain_ok?(log, :FLOODED_DUNES),
  :reaches_glass    => G.chain_ok?(log, :FLOODED_DUNES, :GLASS_DUNES),
  :no_exceptions    => log.errors.empty?
})
puts "    Reshiram used Blue Flare #{fired_flare}x"

#-------------------------------------------------------------------------------
# D. AI duel: Primal Kyogre boss against a fire team (backing Ashkaar)
#-------------------------------------------------------------------------------
Prismfall::Bosses.register(:HARNESS_KYOGRE_GLASSDUNES, {
  :species => :KYOGRE, :level => 85, :ability => :PRIMORDIALSEA, :nature => :MODEST, :ivs => 31,
  :evs => { :HP => 252, :SPECIAL_ATTACK => 252, :SPEED => 4 },
  :moves => [:ORIGINPULSE, :ICEBEAM, :THUNDER, :CALMMIND], :bars => 2,
  :intro => ["Kyogre rises out of its flood-sea, Primal markings blazing!"]
})
party_d = [strong(:RESHIRAM, 85, [:BLUEFLARE, :FUSIONFLARE, :DRAGONPULSE, :EARTHPOWER]),
           strong(:CHARIZARD, 85, [:OVERHEAT, :AIRSLASH, :SOLARBEAM, :DRAGONPULSE]),
           strong(:GARCHOMP, 85, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :SWORDSDANCE])]
log = G.ai_boss("D. AI vs AI: Primal Kyogre boss (2 bars) vs Reshiram, Charizard, Garchomp on 926",
                :party => party_d, :boss => :HARNESS_KYOGRE_GLASSDUNES)
record("D_ai_primal_kyogre_boss", log.title, log, {
  :flooded_at_start => G.chain_ok?(log, :DESERT, :FLOODED_DUNES),
  :no_exceptions    => log.errors.empty?
})

#-------------------------------------------------------------------------------
# E. The tide: Sunny Day on the Flooded Dunes drains it into the Superbloom
#-------------------------------------------------------------------------------
log = G.duel("E. Tide: Flooded Dunes, the player's Sunny Day drains the flood (sun: 2 a round)",
             :party => strong(:NINETALES, 85, [:SUNNYDAY, :FLAMETHROWER]), :foe => strong(:SNORLAX, 85, [:SPLASH]),
             :field => :FLOODED_DUNES, :player => [:SUNNYDAY, :FLAMETHROWER, :FLAMETHROWER, :FLAMETHROWER],
             :foe_moves => [])
record("E_tide_drains_to_superbloom", log.title, log, {
  :drains_to_desert_bloom => log.field_changes.any? { |o, n, st| o == :DESERT && n == :DESERT && st == 2 } &&
                             G.chain_ok?(log, :FLOODED_DUNES, :DESERT),
  :warned                 => log.include?("sinking into the sand")
})

# E2. AI vs AI under Drought: the AI's keep-the-tide score (Flooded Dunes :ai_score hook) runs at a low tide
$game_map = Harness::FakeMap.new(926)
$player.party = [bulky(:KYOGRE, 55, [:SURF, :ICEBEAM, :THUNDER, :CALMMIND], :ability => :PRESSURE)]
log = Harness.run_battle("E2. AI vs AI on the Flooded Dunes: Kyogre vs a Drought Ninetales (sun drains the tide)",
                         :seed => 52, :setup => G.ai_setup) do
  setBattleRule("field", :FLOODED_DUNES)
  setBattleRule("canLose")
  setBattleRule("cannotRun")
  WildBattle.start(bulky(:NINETALES, 85, [:FLAMETHROWER, :SOLARBEAM, :NASTYPLOT, :WILLOWISP], :ability => :DROUGHT))
end
record("E2_ai_low_tide", log.title, log, { :no_exceptions => log.errors.empty?,
                                           :warned => log.include?("sinking into the sand") })

#-------------------------------------------------------------------------------
# F. The Steamline (925): its default is the Bleed, echoing only the war's fields
#-------------------------------------------------------------------------------
G.borrowed_log.clear
log = G.duel("F. The Steamline (map 925 default, no field rule): 15 quiet rounds of Bleed rotation",
             :party => strong(:MEW, 85, [:SPLASH]), :foe => strong(:SNORLAX, 85, [:SPLASH]), :map => 925,
             :player => [:SPLASH] * 15, :foe_moves => [], :rng => nil, :seed => 925)
f_borrowed = G.borrowed_log.select { |m, f, _| m == 925 && f == :BLEED }.flat_map(&:last)
record("F_steamline_bleed_war_pool", log.title, log, {
  :default_is_bleed => log.field_changes.first&.[](1) == :BLEED,
  :rotated          => f_borrowed.size >= 4,
  :war_pool_only    => !f_borrowed.empty? && (f_borrowed - WAR_POOL).empty?
})
puts "    Steamline echoes: #{f_borrowed.inspect}"
G.borrowed_log.clear
log = G.duel("F2. Control: the Bleed on a map without a pool (990) borrows from every field",
             :party => strong(:MEW, 85, [:SPLASH]), :foe => strong(:SNORLAX, 85, [:SPLASH]), :map => 990, :field => :BLEED,
             :player => [:SPLASH] * 15, :foe_moves => [], :rng => nil, :seed => 925)
f2 = G.borrowed_log.select { |m, f, _| m == 990 }.flat_map(&:last)
record("F2_control_open_bleed", log.title, log, { :borrows_outside_war_pool => !(f2 - WAR_POOL).empty? })
puts "    open Bleed echoes: #{f2.inspect}"

#-------------------------------------------------------------------------------
# G. Soldiers on 926 (AI vs AI), if the war trainers are compiled into this run
#-------------------------------------------------------------------------------
def trainer_exists?(type, name, version)
  !GameData::Trainer.try_get(type, name, version).nil?
rescue StandardError
  false
end

challenger = lambda do
  [strong(:GARCHOMP, 85, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :FIREFANG]),
   strong(:STARMIE, 85, [:SURF, :ICEBEAM, :THUNDERBOLT, :PSYCHIC]),
   strong(:CHARIZARD, 85, [:FLAMETHROWER, :AIRSLASH, :DRAGONPULSE, :EARTHQUAKE]),
   strong(:LUCARIO, 85, [:AURASPHERE, :FLASHCANNON, :EXTREMESPEED, :CLOSECOMBAT])]
end
[[:ISENMAR_OFFICER, "Captain", 1], [:ASHKAAR_OFFICER, "Captain", 1], [:ISENMAR_SOLDIER_F, "Soldier", 1],
 [:ASHKAAR_SOLDIER_F, "Soldier", 1]].each_with_index do |(tt, nm, v), i|
  if !trainer_exists?(tt, nm, v)
    puts "G: #{tt} #{nm} #{v} not compiled in this run - skipped"
    next
  end
  log = G.ai_trainer("G#{i + 1}. AI vs AI on 926: #{tt} #{nm} v#{v} vs Lv.85 challenger", :party => challenger.call,
                     :type => tt, :name => nm, :version => v, :seed => 300 + i)
  record("G#{i + 1}_soldier_#{tt.to_s.downcase}_#{v}", log.title, log, { :no_exceptions => log.errors.empty?,
                                                                           :starts_on_desert => log.field_changes.first&.[](1) == :DESERT })
end

# G'. The same captains with the WANTS the field plan suggests to the trainer workstream (mapgen/REQUESTS.md).
# Harness-only: 012_FieldEffects_TrainerPlays.rb is the trainer workstream's file and is not edited.
SUGGESTED_WANTS = {
  :ISENMAR_OFFICER => { :FLOODED_DUNES => 20, :FROZEN_LAKE => 16, [:DESERT, 2] => 8, :GLASS_DUNES => -20 },
  :ASHKAAR_OFFICER => { :GLASS_DUNES => 20, :VOLCANIC => 16, :FLOODED_DUNES => -20, [:DESERT, 2] => -10 }
}
[[:ISENMAR_OFFICER, "Captain", 1], [:ASHKAAR_OFFICER, "Captain", 1]].each_with_index do |(tt, nm, v), i|
  next if !trainer_exists?(tt, nm, v)
  old = FieldEffects::TrainerPlays::WANTS[tt]
  FieldEffects::TrainerPlays::WANTS[tt] = SUGGESTED_WANTS[tt]
  log = G.ai_trainer("G'#{i + 1}. AI vs AI on 926 with the suggested WANTS: #{tt} #{nm} v#{v} vs Lv.85 challenger",
                     :party => challenger.call, :type => tt, :name => nm, :version => v, :seed => 300 + (i * 2))
  if old then FieldEffects::TrainerPlays::WANTS[tt] = old else FieldEffects::TrainerPlays::WANTS.delete(tt) end
  record("Gw#{i + 1}_wants_#{tt.to_s.downcase}_#{v}", log.title, log, { :no_exceptions => log.errors.empty? })
end

#-------------------------------------------------------------------------------
# Summary
#-------------------------------------------------------------------------------
md = ["# The Glass Dunes field sequence - headless logic test", "",
      "> Logic-test output (real Essentials v21.1 battle code + Prismfall Core, Field Effects and Bosses, text scene).",
      "> Not game footage. Regenerate: `PRISM_RUN_DIR=<private run dir> PRISM_OUT=<dir> ruby tools/harness/run_glass_dunes.rb`.",
      "", "War pool (MAP_BORROW_POOLS[925/926]): #{WAR_POOL.join(', ')}", "",
      "| Scenario | Result | Turns | Fields | Checks |", "|---|---|---|---|---|"]
RES[:scenarios].each do |s|
  checks = s[:checks].map { |k, v| "#{k} #{v ? 'ok' : '**FAIL**'}" }.join("; ")
  md << "| #{s[:title]} | #{s[:outcome]} | #{s[:turns]} | #{s[:fields].join(' > ')} | #{checks}#{s[:errors] > 0 ? " ; **#{s[:errors]} exceptions**" : ''} |"
end
File.write(File.join(OUT_DIR, "SUMMARY.md"), md.join("\n") + "\n")
File.write(File.join(OUT_DIR, "results.json"), JSON.pretty_generate(RES))
bad = RES[:scenarios].reject { |s| s[:ok] }
puts "scenarios: #{RES[:scenarios].size}, failed: #{bad.size}#{bad.empty? ? '' : ' ' + bad.map { |s| s[:key] }.inspect}"
