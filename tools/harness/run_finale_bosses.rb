#===============================================================================
# Prismfall Bosses - headless test of the Chapter 21 / Ruin R1 bosses and the True Finale's rotation
#   PRISM_RUN_DIR=<private run copy> PRISM_COMPILE=1 ruby tools/harness/run_finale_bosses.rb
# (the run copy as in .agent_brief.md: current pbs/trainers.txt, the Prismfall plugins symlinked).
# Through the real Essentials v21.1 battle code, with the player's moves scripted where a check needs it:
#   1. Arceus (:ARCEUS_FINALE, Bosses 103) on :PRISM_ARENA
#        - the :prism_turn regression: every bar break turns the Plates (it was dead: a frozen summary Hash)
#        - :prism_interval writes the arena's interval (it raised FrozenError)
#        - bars by STORY VARIANT (Bound 6, Miscalibrated 5, War 7, Judgment 7), never by difficulty
#        - :gym_order: bar k cycles the gym fields of gyms 3k-2..3k, in gym order, inside the bar and at breaks
#        - forced locks (+1 a refusing Warden, for that bar only; War: all, capped), Miscalibrated's six-Plate bar 5,
#          the seventh bar (??? type; Judgment on :INVERSE), HARMONY_BUFF; Casual's easing (and only Casual's)
#        - the Eighteen Locks (Bosses 116): release / refusal lines, Juno first, the porter, the choir, forced beats;
#          Gilded's three refills and the Gilded Chain; Judgment's Giratina partner; Standard's 2 Recovers a bar
#   2. Valen's Zygarde (:VALEN_ZYGARDE_ORDER, Bosses 113): Power Construct waits for the last bar; Complete Forme
#      and his line there; bars by difficulty; the Last Tuning (v1) is untouched; the crystal line on each turn
#   3. Voss's / Quent's Silvally (Bosses 114): three bars; re-indexes with the arena (Memory, form, type); the
#      conduit choice between bars 2 and 3 (only if KESTREL_FALLEN); bar-3 regeneration on :let_go only; VOSS_FEIGNED
#   4. Giratina's Origin trial (:GIRATINA_ORIGIN_TRIAL, Bosses 115): Origin Forme on :INVERSE; holding back ends it
#      (only once armed); breaking every bar ends it too; uncatchable
# Prints one line per check; writes REPORT.md and transcript.txt to PRISM_OUT if it is set. Exit 1 on any failure.
#===============================================================================
require "fileutils"
load File.join(__dir__, "boot.rb")
load File.join(HARNESS_DIR, "log_scene.rb")

OUT = ENV["PRISM_OUT"]
FileUtils.mkdir_p(OUT) if OUT
TRANSCRIPT = []
RESULTS = []

def check(name, ok, detail = "")
  RESULTS << [name, ok ? true : false, detail.to_s]
  puts "#{ok ? 'PASS' : 'FAIL'}  #{name}#{ok || detail.to_s.empty? ? '' : "  -- #{detail}"}"
end

def section(title)
  RESULTS << [title, nil, ""]
  puts "", "== #{title}"
end

def mk(species, level, moves, item = nil, ability = nil)
  p = Pokemon.new(species, level)
  GameData::Stat.each_main { |s| p.iv[s.id] = 31 }
  p.forget_all_moves
  moves.each { |m| p.learn_move(m) }
  p.item = item if item
  p.ability = ability if ability
  p.calc_stats
  p.heal
  p
end

# A test Pokemon that can't be knocked out and hits as hard as asked (logic checks, not balance).
def god(pkmn, hp: 60_000, atk: nil, speed: 999)
  pkmn.instance_variable_set(:@totalhp, hp)
  pkmn.instance_variable_set(:@hp, hp)
  if atk
    pkmn.instance_variable_set(:@attack, atk)
    pkmn.instance_variable_set(:@spatk, atk)
  end
  pkmn.instance_variable_set(:@speed, speed)
  pkmn
end

def fresh(difficulty = :STANDARD)
  Harness.new_game_state
  $prismfall = Prismfall::SaveState.new    # new_game_state keeps the loaded state: choices and bonds must not leak between runs
  Prismfall.record_starter(:CHARMANDER) if Prismfall.respond_to?(:record_starter)
  $PokemonEncounters = PokemonEncounters.new
  $player.badges = Array.new(18, true)
  Prismfall.state.level_cap_override = 100
  Prismfall.set_difficulty(difficulty)
  Prismfall::Bosses.arceus_variant_override = nil
  Prismfall::Bosses.arceus_consent_override = proc { |_gym| true }
end

# The player's side: chooser.call(battle, battler) -> a move id to use this turn, or nil for the AI's own pick.
def scripted(&chooser)
  lambda do |battle|
    ai = battle.instance_variable_get(:@battleAI)
    orig = ai.method(:pbDefaultChooseEnemyCommand)
    ai.define_singleton_method(:pbDefaultChooseEnemyCommand) do |idx|
      b = @battle.battlers[idx]
      mv = @battle.pbOwnedByPlayer?(idx) ? chooser.call(@battle, b) : nil
      next orig.call(idx) if !mv
      b.moves.each { |m| m.pp = m.total_pp if m }      # logic checks: the script never runs dry
      i = b.moves.index { |m| m.id == mv }
      if !i
        b.moves[0] = Battle::Move.from_pokemon_move(@battle, Pokemon::Move.new(mv))
        i = 0
      end
      orig.call(idx) if !@battle.pbRegisterMove(idx, i, false)
    end
  end
end

# setup that also records, after every round, whatever `snap` returns.
def recording(rows, chooser = nil, &snap)
  inner = chooser ? scripted(&chooser) : nil
  lambda do |battle|
    inner&.call(battle)
    battle.define_singleton_method(:pbEndOfRoundPhase) do
      ret = super()
      row = snap.call(self)
      rows << row if row
      ret
    end
  end
end

def run(title, seed: 7, setup: nil, &block)
  log = Harness.run_battle(title, :seed => seed, :setup => setup, &block)
  TRANSCRIPT << "" << log.text
  log.errors.each { |e| check("no engine error in '#{title}'", false, "#{e[:class]}: #{e[:message]} #{e[:backtrace].first(3).join(' ')}") }
  log
end

BREAKS = []
EventHandlers.add(:prismfall_boss_bar_broken, :finale_test_breaks,
  proc { |battle, b, id, n, left|
    pr = FieldEffects.state(battle)[:prism]
    BREAKS << { :id => id, :n => n, :left => left, :field => battle.field_effect, :borrowed => FieldEffects.borrowed_fields(battle).first,
                :order => pr && pr[:order].dup, :next => pr && pr[:next_field], :form => b.form, :types => b.pbTypes(true), :stages => b.stages.dup,
                :hp => b.hp, :totalhp => b.totalhp, :item => b.item_id, :moves => b.moves.map(&:id) }
  })
OVERLAYS = []
EventHandlers.add(:prismfall_field_overlay_changed, :finale_test_overlay,
  proc { |_battle, field, _old_ids, new_ids| OVERLAYS << new_ids.first if field == :PRISM_ARENA })
LOCKS = []
EventHandlers.add(:prismfall_arceus_locks, :finale_test_locks, proc { |_battle, bar, gyms, forced| LOCKS << [bar, gyms, forced] })

bs = Prismfall::Bosses
GYM_FIELDS = (1..18).map { |n| Prismfall.gym(n)[:field] }
TRIOS = GYM_FIELDS.each_slice(3).to_a
sweeper = lambda { [god(mk(:GARCHOMP, 100, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :FIREFANG], :LEFTOVERS), :atk => 3000)] }
arceus = lambda do |title, variant: nil, refuse: [], difficulty: :STANDARD, setup: nil, party: nil, resonance: nil|
  fresh(difficulty)
  bs.arceus_variant_override = variant
  bs.arceus_consent_override = proc { |g| !refuse.include?(g) }
  Prismfall::Resonance.set(resonance) if resonance
  $player.party = party || sweeper.call
  BREAKS.clear; OVERLAYS.clear; LOCKS.clear
  run(title, :seed => 3, :setup => setup) { bs.wild_battle(:ARCEUS_FINALE, :can_lose => true) }
end

#-------------------------------------------------------------------------------
section("1. Arceus: :prism_turn, bars by variant, the :gym_order rotation")
#-------------------------------------------------------------------------------
check("Prismfall::Festival::Draw (the scripts' name for the draw API) resolves and gives a variant",
      defined?(Prismfall::Festival::Draw) && Prismfall::Festival::Draw.arceus_variant.is_a?(Hash))
fresh
check("a blank save draws ARCEUS_BOUND: six bars on every difficulty",
      [:CASUAL, :STANDARD, :HARD].map { |d| Prismfall.set_difficulty(d); bs.bars_for(bs.get(:ARCEUS_FINALE)) } == [6, 6, 6])
check("gym order: bar 1 Grand Stage / Silkwood / Water Surface ... bar 6 New Moon / Fairy Tale / Dragon's Den",
      bs.arceus_prism_order == TRIOS && TRIOS[0] == [:GRAND_STAGE, :SILKWOOD, :WATER_SURFACE] &&
      TRIOS[5] == [:NEW_MOON, :FAIRY_TALE, :DRAGONS_DEN], bs.arceus_prism_order.inspect)

log = arceus.call("Arceus, Bound (everyone consents): a sweep through six bars")
check("Bound: won after five breaks (six bars)", log.outcome == 1 && BREAKS.length == 5, "outcome #{log.outcome}, breaks #{BREAKS.length}")
check("the last bar's fall frees Arceus: result :freed, and it never faints", bs.last_result[:result] == :freed && !log.include?(/Arceus fainted/) &&
      log.include?(/The last chain falls away/), bs.last_result[:result].inspect)
released = (1..18).select { |g| log.include?(Prismfall::Finale::RELEASE_LINES[g - 1]) }
check("all 18 Wardens kneel and say their release line (story/11_FINALE_LINES.md section 1)", released.length == 18, "missing #{((1..18).to_a - released).inspect}")
check("...each release opens its lock: 18 golden locks, no refusals", log.lines.count { |l| l.include?("The golden lock opens") } == 18 &&
      !log.include?(/grips the pylon/))
check("the stage directions are staged (Brann weeping, Kaito's open hand, the echoes fade, Celestine sings)",
      log.include?(/Brann is weeping\./) && log.include?(/Kaito opens his hand\./) && log.include?(/The echoes in the stands fade\./) &&
      log.include?(/Celestine sings\./))
check("the Finale record: all 18 released, V118 = 18", (1..18).all? { |g| Prismfall::Finale.lock_state(g) == :released } && $game_variables[118] == 18)
dor = log.lines.index { |l| l.include?("Dorian kneels at the Blank pylon") }
check("bar 1 opens with Dorian at the Blank Plate's pylon, before the first blow", dor && dor < (log.lines.index { |l| l =~ /Garchomp used/ } || 0))
check("bar 6: Celestine's song is taken up by the choirs and the crowd", log.include?(/Celestine: Not chained, not broken/) &&
      log.include?(/Forty thousand people singing/))
# BALANCE.md section 7 "Phase break" (2026-11-27): the Plates skip to the trio's field best against the player's active
# Pokemon. Garchomp (Ground / Dragon): Electric 0 / Ground 1 / Poison 0.5 -> Desert; Fire 0.25 / Fighting 1 / Grass 1 ->
# Colosseum (a tie keeps gym order); Ice 4 -> Frozen Lake; Rock 0.5 / Ghost 1 / Steel 1 -> Hollow Cathedral; Dark 1 /
# Fairy 2 / Dragon 2 -> Fairy Tale.
BEST_VS_GARCHOMP = [:DESERT, :COLOSSEUM, :FROZEN_LAKE, :HOLLOW_CATHEDRAL, :FAIRY_TALE]
check("REGRESSION :prism_turn - every break turns the Plates, to the next trio's field best against the player's active (Garchomp)",
      BREAKS.map { |b| b[:borrowed] } == BEST_VS_GARCHOMP, BREAKS.map { |b| b[:borrowed] }.inspect)
check("...and the cycle goes on from there in gym order (Desert -> Corrosive Mire, Colosseum -> Flower Garden ...)",
      BREAKS.map { |b| b[:next] } == [:CORROSIVE_MIRE, :FLOWER_GARDEN, :STORMFRONT, :FACTORY, :DRAGONS_DEN], BREAKS.map { |b| b[:next] }.inspect)
check("...a skip away from the trio's first field is announced (\"turns the Plates against Garchomp\"): every break but the one into bar 4 (Frozen Lake is first)",
      log.lines.count { |l| l.include?("turns the Plates against Garchomp!") } == 4)
check("at each break the arena's cycle is narrowed to that bar's trio", BREAKS.map { |b| b[:order] } == TRIOS[1..5])
type_of = FieldEffects.get(:PRISM_ARENA) && lambda { |f| { :GRAND_STAGE => :NORMAL, :SILKWOOD => :BUG, :WATER_SURFACE => :WATER, :NEON_GRID => :ELECTRIC,
            :DESERT => :GROUND, :CORROSIVE_MIRE => :POISON, :VOLCANIC => :FIRE, :COLOSSEUM => :FIGHTING, :FLOWER_GARDEN => :GRASS,
            :FROZEN_LAKE => :ICE, :STORMFRONT => :FLYING, :MINDSCAPE => :PSYCHIC, :CRYSTAL_CAVERN => :ROCK, :HOLLOW_CATHEDRAL => :GHOST,
            :FACTORY => :STEEL, :NEW_MOON => :DARK, :FAIRY_TALE => :FAIRY, :DRAGONS_DEN => :DRAGON }[f] }
check("Arceus takes each new Plate's type, form and moveset at the break",
      BREAKS.all? { |b| t = type_of.call(b[:borrowed]); b[:types] == [t] && b[:form] == bs.form_for_type(:ARCEUS, t) && b[:moves] == bs.arceus_movesets[t] },
      BREAKS.map { |b| [b[:borrowed], b[:types], b[:form]] }.inspect)
check("the fight opens on Gym 1's field at once (no resting rounds): the Grand Stage", OVERLAYS.first == :GRAND_STAGE, OVERLAYS.first.inspect)
check("event :prismfall_arceus_locks fired for all six bars, nothing forced", LOCKS.map { |l| l[0] } == [1, 2, 3, 4, 5, 6] && LOCKS.all? { |l| l[2].empty? },
      LOCKS.inspect)

# Inside one bar: nobody attacks for ten rounds; the arena must cycle the trio, in gym order, every three rounds.
rows = []
wall = lambda { [god(mk(:BLISSEY, 100, [:SPLASH, :SOFTBOILED], :LEFTOVERS))] }
log = arceus.call("Arceus, Bound: ten idle rounds inside bar 1", :party => wall.call,
                  :setup => recording(rows, proc { |_battle, _b| :SPLASH }) { |battle|
                    battle.decision = 3 if battle.turnCount >= 9
                    FieldEffects.borrowed_fields(battle).first })
check("inside bar 1 the arena cycles Grand Stage -> Silkwood -> Water Surface -> Grand Stage, three rounds each",
      rows.first(10) == [:GRAND_STAGE] * 2 + [:SILKWOOD] * 3 + [:WATER_SURFACE] * 3 + [:GRAND_STAGE] * 2, rows.inspect)
check("...and each turn is still announced a round ahead", log.include?(/Insect Plate begins to glow\.\.\. After the next turn/) &&
      log.include?(/Splash Plate begins to glow/))
check("Standard telegraphs 1 round ahead: no 'In 2 turns', no 'glows brighter'", !log.include?(/In 2 turns/) && !log.include?(/glows brighter/))
rows = []
log = arceus.call("Arceus, Bound (Casual): ten idle rounds inside bar 1", :party => wall.call, :difficulty => :CASUAL,
                  :setup => recording(rows, proc { |_battle, _b| :SPLASH }) { |battle|
                    battle.decision = 3 if battle.turnCount >= 9
                    FieldEffects.borrowed_fields(battle).first })
glow = log.lines.index { |l| l.include?("The Insect Plate begins to glow... In 2 turns, the arena becomes the Silkwood!") }
bright = log.lines.index { |l| l.include?("The Insect Plate glows brighter... After the next turn, the arena becomes the Silkwood!") }
turned = log.lines.index { |l| l.include?("The Insect Plate blazes") }
check("Casual telegraphs 2 rounds ahead (BALANCE.md section 7): 'begins to glow... In 2 turns', then 'glows brighter', then the turn",
      glow && bright && turned && glow < bright && bright < turned, [glow, bright, turned].inspect)
check("...on the same three-round rhythm as Standard", rows.first(10) == [:GRAND_STAGE] * 2 + [:SILKWOOD] * 3 + [:WATER_SURFACE] * 3 + [:GRAND_STAGE] * 2,
      rows.inspect)

log = arceus.call("Arceus, Bound: Tamsin (2), Brann (7) and Kaito (8) refuse", :refuse => [2, 7, 8])
forced = LOCKS.map { |l| l[2] }
check("forced locks: bar 1 has one (gym 2), bar 3 two (gyms 7, 8), the rest none", forced == [[2], [], [7, 8], [], [], []], forced.inspect)
check("refusal lines: Tamsin, Brann and Kaito say theirs and grip the pylon", log.include?(/Tamsin: I can't\. I can't\./) &&
      log.include?(/Brann: You gave my guild's Light away/) && log.include?(/Kaito: I never said it out loud/) &&
      log.lines.count { |l| l.include?("grips the pylon. The lock stays shut.") } == 3)
check("the forced-lock beat when bar 1 breaks: Tamsin thrown back, the Insect Plate torn free (no line)",
      log.include?(/Tamsin is thrown back from the pylon! The Insect Plate tears free in a crack of Bleed light!/))
ju = log.lines.index { |l| l.include?("Juno kneels") }
br = log.lines.index { |l| l.include?("Brann kneels") }
check("Juno, letting go, is the first to kneel in her bar (before Brann)", ju && br && ju < br, "#{ju.inspect} #{br.inspect}")
check("released Wardens still release: Juno's line and her lock opens", log.include?(/Juno: Verdance has never had an autumn/))

check("forced-lock lines shown (one lock, then two)", log.include?(/One lock holds fast!/) && log.include?(/2 locks hold fast!/))
# stages recorded when a bar breaks = that bar's forced stages plus whatever Arceus set up itself
df = BREAKS.map { |b| [b[:stages][:ATTACK], b[:stages][:SPEED], b[:stages][:DEFENSE]] }
check("a refusal raises its Plate's one stat for that bar (2026-11-26): Kaito's Fist -> Attack +1 in bar 3, Tamsin's " \
      "Insect -> Speed +1 in bar 1, both gone with their bar; Defense untouched",
      df.map(&:first) == [0, 1, 0, 0, 0] && df.all? { |_a, sp, d| sp == 0 && d == 0 } &&
      log.include?(/The wild Arceus's Speed rose!/) && log.include?(/The wild Arceus's Attack rose!/) &&
      log.include?(/The wild Arceus's Special Attack rose!/), df.inspect)
check("...the old +1-to-every-stat rule is still the switch (ARCEUS_REFUSAL_SCOPE)", bs::ARCEUS_REFUSAL_SCOPE == :plate &&
      bs.arceus_forced_boosts([7, 8]) == { :SPECIAL_ATTACK => 1, :ATTACK => 1 } && bs.arceus_forced_boosts([3, 6, 9]) == { :SPECIAL_DEFENSE => 3 })
check("the Finale record after the fight: 2, 7, 8 :forced (their locks broken by force), the rest :released",
      [2, 7, 8].all? { |g| Prismfall::Finale.lock_state(g) == :forced } && Prismfall::Finale.lock_state(9) == :released)
log = arceus.call("Arceus, Bound: Corvin not freed (a porter holds his Plate)", :refuse => [6])
check("Corvin's refusal is the porter's: he speaks it, grips the pylon, and is thrown back when the bar breaks",
      log.include?(/Porter: I — I'm not him/) && log.include?(/The porter grips the pylon/) && log.include?(/The porter is thrown back from the pylon!/))

log = arceus.call("Arceus, War (Standard): every lock forced, capped at +2", :variant => :ARCEUS_WAR)
check("War: seven bars; every lock of bars 1-6 forced", bs.arceus_bars == 7 && LOCKS.first(6).all? { |l| l[2] == l[1] }, LOCKS.inspect)
df = BREAKS.first(5).map { |b| b[:stages][:DEFENSE] }
check("War on Standard: the forced stages are capped at +2 a bar", df.uniq == [2], df.inspect)
check("War / Judgment: a forced lock hardens (Defense / Sp. Def) without sharpening: no Attack stages from the locks",
      BREAKS.first(5).all? { |b| b[:stages][:ATTACK] == 0 }, BREAKS.first(5).map { |b| b[:stages] }.inspect[0, 200])
last = BREAKS.find { |b| b[:left] == 1 }
check("War: the seventh bar is the Legend Plate phase (??? type, no Plates turning)", last && last[:types] == [:QMARKS] &&
      last[:field] != :PRISM_ARENA && last[:moves] == bs::ARCEUS_LEGEND_MOVES, last.inspect[0, 200])
arceus.call("Arceus, War (Hard): every lock forced, +3", :variant => :ARCEUS_WAR, :difficulty => :HARD)
df = BREAKS.first(3).map { |b| b[:stages][:DEFENSE] }
check("War on Hard: +3 a bar", df.uniq == [3], df.inspect)

log = arceus.call("Arceus, Miscalibrated (TELEMETRY_SABOTAGED): five bars", :variant => :ARCEUS_MISCALIBRATED)
check("Miscalibrated: five bars; bar 5 cycles all six fields of gyms 13-18", bs.arceus_bars == 5 && BREAKS.length == 4 &&
      BREAKS.last[:order] == GYM_FIELDS[12, 6], BREAKS.last && BREAKS.last[:order].inspect)
check("Miscalibrated: bar 5 starts at x0.85 HP", BREAKS.last && BREAKS.last[:hp] == (BREAKS.last[:totalhp] * 0.85).round,
      BREAKS.last && "#{BREAKS.last[:hp]}/#{BREAKS.last[:totalhp]}")

side = []
log = arceus.call("Arceus, Judgment (Ruin Route): seven bars, the last on Inverse, Giratina at your side", :variant => :ARCEUS_JUDGMENT,
                  :setup => lambda { |battle| side << battle.pbParty(0).map(&:species) << battle.player.length })
last = BREAKS.find { |b| b[:left] == 1 }
check("Judgment: seven bars; the seventh on :INVERSE as the ??? type", bs.arceus_bars == 7 && last && last[:field] == :INVERSE && last[:types] == [:QMARKS],
      last.inspect[0, 160])
check("Judgment: Giratina-Origin fights at the PC's side (PARTNER_GIRATINA, a 2v1), and is gone again after",
      side[0].include?(:GIRATINA) && side[1] == 2 && log.include?(/Reverse Depths sent out Giratina/) && $PokemonGlobal.partner.nil?, side.inspect)
check("Judgment: no Warden kneels; every lock forced (Standard: +2 a bar, capped like War)", !log.include?(/kneels at the/) &&
      log.include?(/No Warden kneels\. All three locks hold\./) && BREAKS.first(5).map { |b| b[:stages][:DEFENSE] }.uniq == [2],
      BREAKS.first(5).map { |b| b[:stages][:DEFENSE] }.inspect)
check("Judgment: the Plates tear free without a Warden at the pylon", log.include?(/The Blank Plate tears free in a crack of Bleed light!/) &&
      !log.include?(/thrown back/))
fresh
check("Bound and the others fight alone (no partner)", bs.resolve(bs.get(:ARCEUS_FINALE)[:partner]).nil?)

log = arceus.call("Arceus, Gilded (ENGINE_CALIBRATED): the last bar can't be broken", :variant => :ARCEUS_GILDED)
refills = log.lines.count { |l| l.include?("The Engine binds the chain shut again!") }
check("Gilded: the last bar refills three times, then the Gilded Chain closes (result :gilded_chain, the battle ends)",
      refills == 3 && bs.last_result[:result] == :gilded_chain && bs.last_result[:revives] == 3 && log.outcome == 1 &&
      log.include?(/The Gilded Chain closes around/) && log.include?(/Valen kneels, crystal to the jaw/), "refills #{refills}, #{bs.last_result.inspect[0, 120]}")
check("Gilded: the last bar's locks are never broken (no forced beats after the last bar, no :freed)", !log.include?(/The last chain falls away/))
hp = log.lines.select { |l| l =~ /HP Arceus \(foe\): 1 -> (\d+) \/ (\d+)/ }.map { |l| l =~ /1 -> (\d+) \/ (\d+)/ && [$1.to_i, $2.to_i] }.compact
check("Gilded: the last bar is one bar in four pieces (0.4, then three refills of 0.2)",
      hp.length >= 4 && hp[-4][0] == (hp[-4][1] * 0.4).round && hp.last(3).all? { |a, t| a == (t * 0.2).round }, hp.last(4).inspect)
check("Gilded: a big hit carries on into the refills (all three and the chain in one turn)",
      log.lines.each_index.select { |i| log.lines[i].include?("binds the chain shut") }.each_cons(2).all? { |a, b|
        log.lines[a..b].none? { |l| l.include?("--- Turn") } }, "")

# Standard's Recover limit: two a bar. A Blissey that chips 100 a round, so Arceus wants to Recover.
recov = []
tosser = lambda { [god(mk(:BLISSEY, 100, [:SONICBOOM, :SOFTBOILED], :LEFTOVERS))] }   # 20 a round: Arceus wants Recover
counter_snap = lambda do |battle|
  battle.decision = 3 if battle.turnCount >= 40
  f = battle.battlers[1]
  st = f && bs.state_for(f)
  st ? st.counters.select { |k, _v| k[1] == :RECOVER }.dup : nil
end
log = arceus.call("Arceus, Bound (Standard): 40 rounds of Sonic Boom against Recover", :party => tosser.call,
                  :setup => recording(recov, proc { |_battle, _b| :SONICBOOM }, &counter_snap))
uses = recov.last || {}
check("Standard: Arceus Recovers at most twice a bar (BALANCE.md section 7), and the limit is reached",
      !uses.empty? && uses.values.max <= 2 && uses.values.include?(2), uses.inspect)
recov = []
log = arceus.call("Arceus, Bound (Hard): the same, no limit", :party => tosser.call, :difficulty => :HARD,
                  :setup => recording(recov, proc { |_battle, _b| :SONICBOOM }, &counter_snap))
check("Hard: no Recover limit", bs.resolve(bs.get(:ARCEUS_FINALE)[:move_limits]).nil? && log.lines.count { |l| l =~ /Arceus used Recover/ } > 2,
      log.lines.count { |l| l =~ /Arceus used Recover/ }.to_s)

fresh(:CASUAL); c = bs.create_pokemon(:ARCEUS_FINALE)
fresh(:STANDARD); s = bs.create_pokemon(:ARCEUS_FINALE)
fresh(:HARD); h = bs.create_pokemon(:ARCEUS_FINALE)
b0 = bs.create_pokemon(:ARCEUS_FINALE); bs.strip(b0)
check("bar HP by difficulty (2026-11-26): Casual x0.5, Standard x0.32, Hard x0.32 of Arceus's max HP",
      c.totalhp == (b0.totalhp * 0.5).round && s.totalhp == (b0.totalhp * 0.32).round && h.totalhp == (b0.totalhp * 0.32).round,
      [b0.totalhp, c.totalhp, s.totalhp, h.totalhp].inspect)
check("offence: Casual x0.6 < Standard x0.8 = Hard x0.8; Hard is faster", c.spatk < s.spatk && s.spatk == h.spatk && h.speed > s.speed,
      [c.spatk, s.spatk, h.spatk, s.speed, h.speed].inspect)
bs.arceus_variant_override = :ARCEUS_JUDGMENT
Prismfall.set_difficulty(:STANDARD)
check("variant bar HP: Judgment x1.45 on Standard (its partner)", bs.arceus_stat_mults[:HP] == (0.32 * 1.45).round(3))
Prismfall.set_difficulty(:CASUAL)
check("...not on Casual", bs.arceus_stat_mults[:HP] == 0.5)
bs.arceus_variant_override = :ARCEUS_WAR
check("...War's bars x0.4 on Casual too (it fell to 5% / 12%)", bs.arceus_stat_mults[:HP] == 0.2)
bs.arceus_variant_override = nil
check("Casual only is eased: offence x0.6, no Recover and no Calm Mind in any Plate set", c.spatk < b0.spatk &&
      bs.arceus_movesets.values.none? { |m| m.include?(:RECOVER) || m.include?(:CALMMIND) })
Prismfall.set_difficulty(:STANDARD)
check("...Standard keeps Recover (and Calm Mind on the Blank, Mind and Dread Plates)", bs.arceus_movesets[:WATER][3] == :RECOVER && bs.arceus_movesets[:NORMAL][3] == :CALMMIND)
arceus.call("Arceus, Bound (Casual): Tamsin, Brann and Kaito refuse", :refuse => [2, 7, 8], :difficulty => :CASUAL)
cs = BREAKS.map { |b| [b[:stages][:DEFENSE], b[:stages][:ATTACK]] }
check("Casual: a forced lock hardens (Defense / Sp. Def) without sharpening (Attack stays 0)", cs.first(3) == [[0, 0], [2, 0], [0, 0]], cs.inspect)

rows = []
log = arceus.call("Arceus, Bound, Resonance +6: HARMONY_BUFF at a break", :resonance => 6,
                  :party => [god(mk(:GARCHOMP, 100, [:EARTHQUAKE, :DRAGONCLAW], :LEFTOVERS), :atk => 3000, :speed => 1)])
check("HARMONY_BUFF (Resonance >= 6): the shard steadies the player's Pokemon at a break", log.include?(/your Pokémon steady/))
log = arceus.call("Arceus, Bound, Resonance 0: no HARMONY_BUFF")
check("...and not below Resonance 6", !log.include?(/your Pokémon steady/))

# :prism_interval (any boss): the arena's interval is writable through the live state.
bs.register(:TEST_PRISM_INTERVAL, { :species => :SNORLAX, :level => 50, :bars => 1, :field => :PRISM_ARENA, :prism_interval => 2,
                                    :moves => [:SPLASH], :catch => false })
fresh
$player.party = wall.call
rows = []
log = run("A boss with :prism_interval => 2 on the Prism Arena", :setup => recording(rows, proc { |_battle, _b| :SPLASH }) { |battle|
            battle.decision = 3 if battle.turnCount >= 5
            (FieldEffects.state(battle)[:prism] || {})[:interval] }) { bs.wild_battle(:TEST_PRISM_INTERVAL, :can_lose => true) }
check("REGRESSION :prism_interval - no FrozenError, the arena's interval becomes 2", log.errors.empty? && rows.first == 2, rows.first(3).inspect)

#-------------------------------------------------------------------------------
section("2. Valen's Zygarde: Complete Forme on the last bar")
#-------------------------------------------------------------------------------
# His ace alone (the rule fires on trainer load, as TrainerBattle.start does it), against fixed 100-damage hits.
valen = lambda do |version, difficulty = :STANDARD|
  fresh(difficulty)
  t = pbLoadTrainer(:CHAMPION_VALEN, "Valen", version)
  EventHandlers.trigger(:on_trainer_load, t)
  t.party = t.party.select { |p| p.species == :ZYGARDE }
  t
end
t = valen.call(0)
z = t.party[0]
check("the Final (v0): Zygarde \"Order\" is the boss, 2 bars on Standard, in its 50% Forme, Lv 96, his PBS set untouched",
      z.prismfall_boss_id == :VALEN_ZYGARDE_ORDER && bs.bars_for(bs.get(:VALEN_ZYGARDE_ORDER)) == 2 && z.form == 0 && z.level == 96 &&
      z.moves.map(&:id) == [:THOUSANDARROWS, :DRAGONTAIL, :DRAGONDANCE, :STONEEDGE] && z.ability_id == :POWERCONSTRUCT,
      "#{z.prismfall_boss_id} form #{z.form} Lv#{z.level} #{z.moves.map(&:id)} #{z.ability_id}")
base_hp = z.totalhp
rows = []
BREAKS.clear; OVERLAYS.clear
$player.party = [god(mk(:BLISSEY, 100, [:SEISMICTOSS, :SOFTBOILED], :LEFTOVERS))]
log = run("Valen's Zygarde (Standard, 2 bars) against 100 damage a round on the Prism Arena",
          :setup => recording(rows, proc { |_battle, _b| :SEISMICTOSS }) { |battle|
            f = battle.battlers[1]
            st = f && bs.state_for(f)
            st ? [st.bars_left, f.form, f.hp, f.totalhp] : nil }) do
  setBattleRule("canLose"); setBattleRule("field", :PRISM_ARENA)
  TrainerBattle.start(t)
end
held = rows.select { |r| r[0] > 1 && r[2] <= r[3] / 2 }
check("Power Construct waits: under half HP on bar 1 (#{held.length} round ends) it stays in the 50% Forme",
      !held.empty? && held.all? { |r| r[1] == 0 } && rows.select { |r| r[0] > 1 }.all? { |r| r[1] == 0 }, rows.first(6).inspect)
br = BREAKS.find { |b| b[:id] == :VALEN_ZYGARDE_ORDER }
check("the last bar: Complete Forme (max HP #{br && br[:totalhp]} vs #{base_hp}), starting at 0.6 of it on Standard (2026-11-26)",
      br && br[:left] == 1 && br[:form] == 2 && br[:hp] == (br[:totalhp] * 0.6).round && br[:totalhp] > base_hp * 1.5, br.inspect[0, 160])
check("...with Power Construct's lines and Valen's", log.include?(/You sense the presence of many!/) && log.include?(/transformed into its Complete Forme/) &&
      log.include?(/Order, not justice\. I chose order\./))
check("Valen lost after the Complete bar (the battle is winnable)", log.outcome == 1, log.outcome.inspect)
n_crystal = log.lines.count { |l| l.include?("The crystal climbs Valen's throat") }
check("\"The crystal climbs Valen's throat...\" on each of the arena's turns (#{OVERLAYS.length})", n_crystal == OVERLAYS.length && n_crystal > 0,
      "#{n_crystal} lines, #{OVERLAYS.length} turns")
t = valen.call(100, :HARD)
check("Hard (v100): 3 bars at x0.7 HP (2026-11-26), offence untouched", t.party[0].prismfall_boss_id == :VALEN_ZYGARDE_ORDER &&
      bs.bars_for(bs.get(:VALEN_ZYGARDE_ORDER)) == 3 && bs.stat_mults(t.party[0]) == { :HP => 0.7 })
rows = []
BREAKS.clear
$player.party = [god(mk(:BLISSEY, 100, [:SEISMICTOSS, :SOFTBOILED], :LEFTOVERS))]
log = run("Valen's Zygarde (Hard, 3 bars)", :setup => recording(rows, proc { |_battle, _b| :SEISMICTOSS }) { |battle|
            f = battle.battlers[1]; st = f && bs.state_for(f); st ? [st.bars_left, f.form] : nil }) do
  setBattleRule("canLose"); setBattleRule("field", :PRISM_ARENA)
  TrainerBattle.start(t)
end
check("Hard: 50% Forme through bars 1 and 2, Complete only on bar 3", BREAKS.map { |b| b[:form] } == [0, 2] &&
      rows.select { |r| r[0] > 1 }.all? { |r| r[1] == 0 }, BREAKS.map { |b| [b[:left], b[:form]] }.inspect)
t = valen.call(200, :CASUAL)
zc = t.party[0]
plain = Pokemon.new(:ZYGARDE, zc.level); GameData::Stat.each_main { |s| plain.iv[s.id] = zc.iv[s.id]; plain.ev[s.id] = zc.ev[s.id] }; plain.nature = zc.nature; plain.calc_stats
check("Casual (v200): 2 bars at x0.55 HP each", bs.bars_for(bs.get(:VALEN_ZYGARDE_ORDER)) == 2 && zc.totalhp == (plain.totalhp * 0.55).round,
      "#{zc.totalhp} vs #{plain.totalhp}")
t = valen.call(1)
check("the Ruin Route's Last Tuning (v1): not a bar boss; Complete Forme from the start", t.party[0].prismfall_boss_id.nil? && t.party[0].form == 2,
      "#{t.party[0].prismfall_boss_id.inspect} form #{t.party[0].form}")

#-------------------------------------------------------------------------------
section("3. Silvally \"NULL\": the arena's type, the conduit bar")
#-------------------------------------------------------------------------------
hijack = lambda do |title, type: :MERIDIAN_VOSS, name: "Aurelian", version: 0, difficulty: :STANDARD, prep: nil|
  fresh(difficulty)
  prep&.call
  t = pbLoadTrainer(type, name, version)
  EventHandlers.trigger(:on_trainer_load, t)
  t.party = t.party.select { |p| p.species == :SILVALLY }
  pre = { :id => t.party[0].prismfall_boss_id, :level => t.party[0].level, :mults => bs.stat_mults(t.party[0]),
          :bars => bs.bars_for(bs.get(t.party[0].prismfall_boss_id || :VOSS_SILVALLY_NULL)), :totalhp => t.party[0].totalhp }
  rows = []
  BREAKS.clear; OVERLAYS.clear
  $player.party = [god(mk(:BLISSEY, 100, [:SEISMICTOSS, :SOFTBOILED], :LEFTOVERS))]
  log = run(title, :setup => recording(rows, proc { |_battle, _b| :SEISMICTOSS }) { |battle|
              f = battle.battlers[1]
              st = f && bs.state_for(f)
              pr = FieldEffects.state(battle)[:prism]
              st ? { :bars => st.bars_left, :field => pr && pr[:field], :type => pr && pr[:type], :types => f.pbTypes(true), :item => f.item_id,
                     :form => f.form, :hp => f.hp, :stages => f.stages.dup } : nil }) do
    setBattleRule("canLose"); setBattleRule("field", :PRISM_ARENA)
    TrainerBattle.start(t)
  end
  [log, rows, pre]
end
fallen = proc { Prismfall::Bonds.change(:KESTREL, -8) }

log, rows, n = hijack.call("Voss's NULL (Standard): Kestrel redeemed, no conduit")
check("the Hijack (Voss v0): Silvally \"NULL\" is the boss, 3 bars, Lv 100, no stat multipliers on Standard",
      n[:id] == :VOSS_SILVALLY_NULL && n[:bars] == 3 && n[:level] == 100 && n[:mults].nil?, n.inspect)
opening = rows.select { |r| r[:field].nil? }
check("the opening rounds: it keeps its Steel Memory", !opening.empty? && opening.all? { |r| r[:item] == :STEELMEMORY && r[:types] == [:STEEL] }, opening.first.inspect[0, 120])
turned = rows.select { |r| r[:field] }
check("after every turn of the Plates its type, form and Memory are the ascendant Plate's (#{turned.map { |r| r[:type] }.uniq.join(', ')})",
      turned.length >= 6 && turned.all? { |r| r[:types] == [r[:type]] && r[:item] == bs::NULL_MEMORIES[r[:type]] && r[:form] == bs.form_for_type(:SILVALLY, r[:type]) },
      turned.find { |r| r[:types] != [r[:type]] || r[:item] != bs::NULL_MEMORIES[r[:type]] }.inspect[0, 160])
check("\"NULL re-indexes to the X Memory!\" shown", log.include?(/re-indexes to the Fire Memory!/))
check("three bars broke in order and Voss lost", BREAKS.map { |b| b[:n] } == [1, 2] && log.outcome == 1, "#{BREAKS.map { |b| b[:n] }} outcome #{log.outcome}")
check("Voss's NULL on Standard: every stat stage resets at a break, its own boosts too (2026-11-26)",
      BREAKS.length == 2 && BREAKS.all? { |b| b[:stages].values.all? { |v| v == 0 } }, BREAKS.map { |b| b[:stages] }.inspect[0, 160])
check("Voss's two mid-battle lines at the first two breaks", log.include?(/a god dropped its furniture on her/) && log.include?(/we don't need it/))
check("Kestrel redeemed: no conduit scene, no choice, no regeneration", !log.include?(/Harnessed into the Engine/) && !log.include?(/regenerated!/) &&
      !Prismfall::Choices.made?(:ch21_reach_kestrel))

log, rows, = hijack.call("Voss's NULL: Kestrel fallen, the choice asked in battle (no Reach: bond too low; the harness takes the first option, Burn)", :prep => fallen)
check("KESTREL_FALLEN: the floor opens between bars 2 and 3 and the choice is asked (Reach not offered without CAN_REACH_KESTREL)",
      log.include?(/Harnessed into the Engine under it/) && log.include?("[auto: Burn it off.]") && Prismfall::Choices.get(:ch21_reach_kestrel) == :burn,
      Prismfall::Choices.get(:ch21_reach_kestrel).inspect)
check(":burn breaks the conduit: no bar-3 regeneration; result :conduit_broken", log.include?(/has lost its conduit/) && !log.include?(/regenerated!/) &&
      bs.last_result[:result] == :conduit_broken, bs.last_result[:result].inspect)

log, rows, = hijack.call("Voss's NULL: Kestrel fallen, Morwen's letter kept (Reach offered and taken)",
                         :prep => proc { fallen.call; Prismfall::Choices.make(:ch12_letter, :keep, false) })
check("with the letter kept: Reach is offered first, and Morwen's words are said", log.include?("[auto: Reach him.]") &&
      log.include?(/I'll carry the name/) && log.include?(/She carried yours\. Put it down\./) && Prismfall::Choices.get(:ch21_reach_kestrel) == :reach)

log, rows, = hijack.call("Voss's NULL: Kestrel fallen, :let_go already chosen (a retry): the conduit fires",
                         :prep => proc { fallen.call; Prismfall::Choices.make(:ch21_reach_kestrel, :let_go, false) })
regen = log.lines.each_index.select { |i| log.lines[i].include?("regenerated!") }
bar3 = rows.select { |r| r[:bars] == 1 }
check(":let_go (already made: not asked again): NULL regenerates every round of bar 3, and only bar 3",
      !log.include?("[auto:") && log.include?(/the Engine fires through its conduit/) && regen.length >= 2 && bs.last_result[:result] == :conduit_fired &&
      log.lines.index { |l| l.include?("regenerated!") } > log.lines.index { |l| l.include?("Harnessed into the Engine") },
      "#{regen.length} regenerations; result #{bs.last_result[:result].inspect}")
check("...1/8 of its max HP a round on Standard, and KESTREL_LOST is set", Prismfall::Narrative.flag(:KESTREL_LOST) &&
      bar3.each_cons(2).any? { |a, b| b[:hp] - a[:hp] == (n[:totalhp] / 8.0).round - 100 }, bar3.first(4).map { |r| r[:hp] }.inspect)

log, rows, = hijack.call("Voss's NULL: VOSS_FEIGNED", :prep => proc { Prismfall::Choices.make(:ch17_voss_offer, :feign, false) })
check("VOSS_FEIGNED: his line, and NULL at -1 to every stat for three rounds",
      log.include?(/You were close\. You let me get close\./) && log.include?(/All its stats fell!/) &&
      rows.first(2).all? { |r| [:DEFENSE, :SPECIAL_DEFENSE].all? { |s| r[:stages][s] == -1 } } &&     # (it sets up Attack / Speed itself)
      [:DEFENSE, :SPECIAL_DEFENSE].all? { |s| rows[2][:stages][s] == 0 }, rows.first(4).map { |r| r[:stages][:DEFENSE] }.inspect)

log, rows, q = hijack.call("Quent's NULL (Voss discredited): MERIDIAN_QUENT v99", :type => :MERIDIAN_QUENT, :name => "Percival", :version => 99)
check("Quent as the hijacker (v99): the same three-bar NULL, without Voss's lines", q[:id] == :QUENT_SILVALLY_NULL &&
      BREAKS.length == 2 && !log.include?(/Voss:/) && log.include?(/re-indexes to the/))
fresh
q = pbLoadTrainer(:MERIDIAN_QUENT, "Percival", 21); EventHandlers.trigger(:on_trainer_load, q)
check("Quent's other teams (the v21 tag foe) are not bar bosses", q.party.none? { |p| p.prismfall_boss_id })
c = hijack.call("Voss's NULL (Casual)", :version => 200, :difficulty => :CASUAL)[2]
check("Casual (v200): 3 bars at x0.55 HP", c[:bars] == 3 && c[:mults] == { :HP => 0.55 }, c.inspect)

#-------------------------------------------------------------------------------
section("4. Giratina's Origin trial (Ruin R1)")
#-------------------------------------------------------------------------------
trial = lambda do |title, difficulty: :STANDARD, &chooser|
  fresh(difficulty)
  BREAKS.clear
  $player.party = [god(mk(:GARCHOMP, 100, [:DRAGONCLAW, :SWORDSDANCE, :EARTHQUAKE, :PROTECT], :LEFTOVERS), :atk => 3000)]
  rows = []
  log = run(title, :setup => recording(rows, chooser) { |battle| f = battle.battlers[1]; f ? [f.form, f.pbTypes(true), battle.field_effect] : nil }) do
    bs.wild_battle(:GIRATINA_ORIGIN_TRIAL, :can_lose => true)
  end
  [log, rows]
end
fresh
g = bs.create_pokemon(:GIRATINA_ORIGIN_TRIAL)
check("Giratina is created in its Origin Forme (Griseous Core), Lv 72, 3 bars on Standard, uncatchable",
      g.form == 1 && g.level == 72 && g.item_id == :GRISEOUSCORE && bs.bars_for(bs.get(:GIRATINA_ORIGIN_TRIAL)) == 3 && bs.get(:GIRATINA_ORIGIN_TRIAL)[:catch] == false,
      "form #{g.form} @#{g.item_id}")
check("bars: Casual 2, Standard 3, Hard 4", [:CASUAL, :STANDARD, :HARD].map { |d| Prismfall.set_difficulty(d); bs.bars_for(bs.get(:GIRATINA_ORIGIN_TRIAL)) } == [2, 3, 4])

log, rows = trial.call("Origin trial: holding back from the first round (before any bar breaks), then fighting") do |battle, _b|
  (battle.turnCount < 2) ? :SWORDSDANCE : :DRAGONCLAW
end
check("on :INVERSE, in the Origin Forme (Ghost / Dragon)", rows.first && rows.first == [1, [:GHOST, :DRAGON], :INVERSE], rows.first.inspect)
check("holding back before the first break does not end it (two idle rounds first, then the fight goes on)",
      log.turns > 2 && BREAKS.length >= 1 && !log.include?(/You hold your hand still/), "turns #{log.turns}, breaks #{BREAKS.length}")
check("breaking every bar ends it as a win, result :overpowered; it does not faint", log.outcome == 1 && bs.last_result[:result] == :overpowered &&
      BREAKS.length == 2 && !log.include?(/Giratina fainted/), "outcome #{log.outcome} result #{bs.last_result[:result].inspect} breaks #{BREAKS.length}")

log, rows = trial.call("Origin trial: one bar broken, then the player holds back (Swords Dance)") do |_battle, _b|
  BREAKS.empty? ? :DRAGONCLAW : :SWORDSDANCE
end
check("the tell is shown at the arming break", log.include?(/It is watching your hand/))
check("armed after one break: one round without an attack ends the trial as a win, result :restraint", log.outcome == 1 &&
      bs.last_result[:result] == :restraint && BREAKS.length == 1 && log.include?(/You hold your hand still/),
      "outcome #{log.outcome} result #{bs.last_result[:result].inspect} breaks #{BREAKS.length}")

log, rows = trial.call("Origin trial (Hard): one bar broken then two idle rounds, then a second bar, then holding back", :difficulty => :HARD) do |battle, _b|
  idle = (battle.instance_variable_get(:@test_idle) || 0)
  if BREAKS.length == 1 && idle < 2
    battle.instance_variable_set(:@test_idle, idle + 1)
    :SWORDSDANCE
  elsif BREAKS.length < 2 then :DRAGONCLAW
  else :SWORDSDANCE
  end
end
check("Hard: armed only after two breaks (holding back after one does nothing)", log.outcome == 1 && bs.last_result[:result] == :restraint && BREAKS.length == 2,
      "result #{bs.last_result[:result].inspect} breaks #{BREAKS.length}")

log, rows = trial.call("Origin trial: a status move aimed at Giratina is not holding back") do |battle, _b|
  n = battle.instance_variable_get(:@test_screech).to_i
  if BREAKS.length == 1 && n < 3
    battle.instance_variable_set(:@test_screech, n + 1)
    :SCREECH
  else
    :DRAGONCLAW
  end
end
check("a hostile status move (three rounds of Screech) does not count as holding back", !log.include?(/You hold your hand still/) &&
      bs.last_result[:result] == :overpowered, bs.last_result[:result].inspect)

#-------------------------------------------------------------------------------
fails = RESULTS.count { |_n, ok, _d| ok == false }
total = RESULTS.count { |_n, ok, _d| !ok.nil? }
puts "", "#{total - fails}/#{total} checks passed"
if OUT
  lines = ["# Finale bosses - headless test", "", "#{total - fails}/#{total} checks passed (tools/harness/run_finale_bosses.rb).", ""]
  RESULTS.each { |n, ok, d| lines << (ok.nil? ? "\n## #{n}" : "- #{ok ? 'PASS' : '**FAIL**'} #{n}#{ok || d.empty? ? '' : " (#{d})"}") }
  File.write(File.join(OUT, "REPORT.md"), lines.join("\n") + "\n")
  File.write(File.join(OUT, "transcript.txt"), TRANSCRIPT.join("\n"))
end
exit(fails.zero? ? 0 : 1)
