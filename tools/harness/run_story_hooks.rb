#===============================================================================
# Prismfall - headless checks for the Ch15-21 and post-game engine hooks
#   PRISM_RUN_DIR=<private run copy with Trials linked> PRISM_COMPILE=1 ruby tools/harness/run_story_hooks.rb
# Through the real Essentials v21.1 code + Prismfall Core / Bosses / Field Effects / Trials:
#   1. Interludes (Core 028): the five loadouts, V119, the stash, the leak purge, a save round trip
#   2. Timed prompts and GO_OVERTIME (Core 029)
#   3. pf_echo_follow (mapgen/ruby/013): the convoy and the crypt echo, on fake map events
#   4. The ceremony's data, the banners, the Grounds Ladder (Core 030)
#   5. The finale's rules (Core 033): lamps, montage, tag battle, the kneels on :prismfall_arceus_locks
#   6. Story battle hooks (Field Effects 013): K6's one-turn :BLEED overload, K8's tear-off, Valen's crystal
#   7. The Registry (Trials 013 / 115 / 134 / 154): tiers, switches, the board, a Tier 1 card with a real boss
# Prints PASS / FAIL lines; exit 1 on any failure. Writes nothing into the repo.
#===============================================================================
load File.join(__dir__, "boot.rb")
load File.join(HARNESS_DIR, "log_scene.rb")
MSG = []
def pbMessage(message, commands = nil, _c = 0, _s = nil, default_cmd = 0, &_b)
  MSG << Harness.clean(message.to_s)
  Harness.log&.add("(overworld message) #{Harness.clean(message.to_s)}")
  return commands ? default_cmd : 0
end
def pbNickname(_p); end
def pbSEPlay(*_a); end
def pbMEPlay(*_a); end
$fails = []
def check(name, ok, detail = nil)
  puts "#{ok ? 'PASS' : 'FAIL'}  #{name}#{ok ? '' : "  (#{detail.inspect})"}"
  $fails << name if !ok
  ok
end
def section(t); puts "--- #{t}"; end
def strong_team(n = 6)
  $player.party = [[:GARCHOMP, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :IRONHEAD]], [:TYRANITAR, [:CRUNCH, :STONEEDGE, :EARTHQUAKE, :ICEPUNCH]],
                   [:SCIZOR, [:BULLETPUNCH, :XSCISSOR, :UTURN, :SUPERPOWER]], [:HYDREIGON, [:DARKPULSE, :DRAGONPULSE, :FLAMETHROWER, :EARTHPOWER]],
                   [:VOLCARONA, [:BUGBUZZ, :FIERYDANCE, :GIGADRAIN, :HURRICANE]], [:AEGISLASH, [:SHADOWBALL, :FLASHCANNON, :SHADOWSNEAK, :SACREDSWORD]]].first(n).map do |sp, mv|
    p = Pokemon.new(sp, 100); GameData::Stat.each_main { |s| p.iv[s.id] = 31 }; p.forget_all_moves; mv.each { |m| p.learn_move(m) }; p.calc_stats; p
  end
end
# Engine error popups that start inside third-party AI scoring (the Gen 9 Pack's "AI New Move Rankings" raises on
# some moves when the harness AI plays the player's side) are not this suite's subject.
def own_errors(log)
  return log.errors.reject { |e| (e[:backtrace] || []).first.to_s =~ /Generation 9 Pack|_AI_|Battle_AI/ }
end
def boxes_empty?
  (0...$PokemonStorage.maxBoxes).all? { |b| (0...$PokemonStorage.maxPokemon(b)).all? { |i| $PokemonStorage[b, i].nil? } }
end

Harness.new_game_state
Prismfall.record_starter(:CHARMANDER)
18.times { |i| $player.badges[i] = true }
tr = Prismfall::Trials
em = Prismfall::EventMons

#-------------------------------------------------------------------------------
section "1. Interludes"
#-------------------------------------------------------------------------------
I = Prismfall::Interlude
$player.party = [Pokemon.new(:PIKACHU, 50), Pokemon.new(:EEVEE, 40)]
mine = $player.party.map(&:personalID)
expect = { 1 => [:STARAVIA, :HONEDGE], 2 => [:TREVENANT, :LEAVANNY, :ROSERADE, :SUNFLORA], 3 => [:AEGISLASH],
           4 => [:AMOONGUSS, :SWALOT, :GASTRODON], 5 => [:BRONZONG, :LAPRAS] }
(1..5).each do |n|
  ok = pf_interlude_start(n)
  sp = $player.party.map(&:species)
  check("Interlude #{n}: loadout in, V119 = #{n}, name #{I.loadout(n)[:name]}",
        ok && $game_variables[119] == n && $player.name == I.loadout(n)[:name] && (expect[n] - sp).empty?, sp)
  check("Interlude #{n}: a second start is refused", pf_interlude_start(n) == false)
  $PokemonStorage.pbStoreCaught($player.party[0])                       # try to leak a loadout Pokemon into the PC
  pf_interlude_end
  check("Interlude #{n}: party, name and V119 back; nothing left in the boxes",
        $player.party.map(&:personalID) == mine && $player.name == "Tester" && $game_variables[119] == 0 && boxes_empty?)
end
pf_interlude_start(4)
check("Wenlow: three Lv 62, encounters off", $player.party.all? { |p| p.level == 62 } && $game_system.encounter_disabled)
pf_interlude_end
pf_interlude_start(5)
check("Valen: no legendary in the loadout, menu shut, walk only",
      $player.party.none? { |p| Prismfall.legendary_species?(p.species) } && $game_system.menu_disabled && I.settings[:walk_only])
$prismfall = Marshal.load(Marshal.dump(Prismfall.state))
check("mid-Interlude save round trip keeps the stash", pf_interlude?(5) && I.stash[:party].map(&:species) == [:PIKACHU, :EEVEE])
$game_variables[119] = 0
I.repair
check("a stash with V119 == 0 is put back on map entry", !pf_interlude? && $player.party.map(&:species) == [:PIKACHU, :EEVEE] && !$game_system.menu_disabled)

#-------------------------------------------------------------------------------
section "2. Timed prompts and GO_OVERTIME"
#-------------------------------------------------------------------------------
TP = Prismfall::TimedPrompt
TP.answers = [0]
check("a scripted answer is returned", Prismfall.timed_choice("Finish copying?", ["Stay.", "Go."], default: 1) == 0 && !TP.timed_out?)
check("no answer = timeout = the default (Go)", Prismfall.timed_choice("Finish copying?", ["Stay.", "Go."], default: 1) == 1 && TP.timed_out?)
go = nil
Prismfall.define_singleton_method(:game_over) { |id, *_a| go = id; true }
TP.answers = [:timeout]
check("Overtime: walking away at the first whistle = :go", pf_overtime == :go && go.nil?)
TP.answers = ["Stay.", "Go."]
check("Overtime: stay once, then go", pf_overtime == :go && go.nil?)
TP.answers = ["Stay.", "Stay.", :timeout]
check("Overtime: the third prompt timing out is still Go", pf_overtime == :go && go.nil?)
MSG.clear
TP.answers = ["Stay.", "Stay.", "Stay."]
check("Overtime: staying three times is GO_OVERTIME; Rook warns twice",
      pf_overtime == :game_over && go == :GO_OVERTIME && MSG.count { |m| m.start_with?("Rook:") } == 2, [go, MSG])

#-------------------------------------------------------------------------------
section "3. pf_echo_follow"
#-------------------------------------------------------------------------------
load File.expand_path("../../mapgen/ruby/006_MapStory.rb", HARNESS_DIR)
load File.expand_path("../../mapgen/ruby/013_EchoFollow.rb", HARNESS_DIR)
class FakeEv
  attr_accessor :x, :y, :direction, :through, :move_speed, :name, :id
  def initialize(id, name, x, y); @id = id; @name = name; @x = x; @y = y; @direction = 2; @through = false; end
  def moveto(x, y); @x = x; @y = y; end
  def move_down(_t = true); @y += 1; end
  def move_up(_t = true); @y -= 1; end
  def move_left(_t = true); @x -= 1; end
  def move_right(_t = true); @x += 1; end
  def moving?; false; end
end
class FakeEchoMap
  attr_accessor :map_id, :events, :need_refresh
  def initialize(id); @map_id = id; @events = {}; end
  def terrain_tag(_x, y); (y == 5) ? 7 : 0; end
end
real_map, real_player = $game_map, $game_player
$game_map = FakeEchoMap.new(925)
3.times { |i| $game_map.events[i + 1] = FakeEv.new(i + 1, "Sledge #{i + 1}", 2, 9) }
$game_map.events[9] = FakeEv.new(9, "Morwen's echo", 0, 0)
PL = Struct.new(:x, :y, :direction, :move_speed).new(3, 5, 6, 3)
$game_player = PL
EF = PrismfallMaps::EchoFollow
walk = lambda { |dx, dy| PL.x += dx; PL.y += dy; EF.on_step }
pos = lambda { (1..3).map { |i| e = $game_map.events[i]; [e.x, e.y] } }
EF.on_enter_map
check("convoy starts on the player's tile", pf_echo_follow(:convoy, "Sledge", lane_tag: 7))
4.times { walk.call(1, 0) }
check("three sledges on the player's footprints", pos.call == [[6, 5], [5, 5], [4, 5]], pos.call)
walk.call(0, 1)
check("off the line: the convoy waits", pf_echo_follow(:off?) && pos.call == [[6, 5], [5, 5], [4, 5]])
walk.call(0, -1)
check("back on the last footprint: on again, nobody moved", !pf_echo_follow(:off?) && pos.call == [[6, 5], [5, 5], [4, 5]])
walk.call(1, 0)
check("the line resumes", pos.call == [[7, 5], [6, 5], [5, 5]], pos.call)
saved = Marshal.dump($PokemonGlobal.pf_map_flags)
(1..3).each { |i| $game_map.events[i].moveto(2, 9) }
$PokemonGlobal.pf_map_flags = Marshal.load(saved)
EF.on_enter_map
check("after a load the sledges stand where the record says", pos.call == [[7, 5], [6, 5], [5, 5]], pos.call)
check("arrived? / lead_at? / stop", pf_echo_follow(:arrived?, 5, 5, 7, 5) && pf_echo_follow(:lead_at?, 7, 5) && pf_echo_follow(:stop) && !pf_echo_follow(:active?))
$game_map.map_id = 393
PL.x = 10; PL.y = 10
EF.on_enter_map
pf_echo_follow(:record, max: 12, var: 370)
[[1, 0], [1, 0], [0, -1], [0, -1], [-1, 0]].each { |d| walk.call(*d) }
check("the crypt bell: five steps recorded, V370 = 5", pf_echo_follow(:length) == 5 && $game_variables[370] == 5)
10.times { walk.call(0, 1) }
check("capped at twelve", pf_echo_follow(:length) == 12 && $game_variables[370] == 12)
n = pf_echo_follow(:replay, "Morwen's echo", self_switch: "A")
e = $game_map.events[9]
check("Morwen's echo walks the twelve steps and stays (and holds the plate)",
      n == 12 && [e.x, e.y] == [11, 15] && $game_self_switches[[393, 9, "A"]] == true && pf_echo_follow(:echo_at?, "Morwen's echo", 11, 15), [n, e.x, e.y])
pf_echo_follow(:clear, "Morwen's echo")
check("ringing again erases her", $game_self_switches[[393, 9, "A"]] == false && pf_echo_follow(:length) == 0 && $game_variables[370] == 0)
$game_map, $game_player = real_map, real_player

#-------------------------------------------------------------------------------
section "4. The ceremony, the banners, the Grounds Ladder"
#-------------------------------------------------------------------------------
C = Prismfall::Ceremony
rows = C.procession
check("eighteen bearers in gym order, types as GYMS", rows.length == 18 && rows.each_with_index.all? { |r, i| Prismfall::GYMS[i][:trainer_name] == r[:name] && Prismfall::GYMS[i][:type] == r[:type] })
check("Corvin's Plate is carried by a Choir porter unless he was freed", rows[5][:bearer] == "Choir porter")
check("Bastian leans on Pip", rows[12][:with] == ["Pip"])
check("before Day 1 the banners hang in kingdom colours", C.banner(1)[:color] == :kingdom)
Prismfall::Festival.start(force: true) rescue nil
Prismfall::Festival.set_day(1) rescue nil
check("from Day 1: white = consent, grey = not, with its reason",
      C.day >= 1 && C.banner(1)[:color] == (C.consent?(1) ? :white : :grey) && C.banner(6)[:color] == :grey && C.banner(6)[:line].include?("porter"), [C.day, C.banner(6)])
L = Prismfall::GroundsLadder
missing = L::ROSTER.reject { |r| L.resolve(r) }.map { |r| r[:trainer][1] }
puts "      (Ladder PBS blocks not in trainers.txt yet: #{missing.join(', ')})" if !missing.empty?
check("a challenger with no PBS block is skipped, never a crash", L.challenge(:WEAVER).nil? || L.present?(:WEAVER))
backup = L::ROSTER.map { |r| r[:trainer] }
if L.present_rungs.length < 2   # stand-ins while the Ladder's own PBS blocks are missing (any trainer will do for the driver)
  L::ROSTER[0][:trainer] = [:HOLLOW_GRUNT_M, "Grunt", 0]
  L::ROSTER[2][:trainer] = [:HOLLOW_GRUNT_F, "Grunt", 0]
end
strong_team
want = L.present_rungs.first(2).map { |r| Array(r[:field]).first.to_s }
before = L.count
beat = nil
log = Harness.run_battle("ladder", seed: 2) { L.answers = [true, true, false]; beat = L.run; $game_variables[1] }
fought = log.text.scan(/field: (\w+)/).flatten
check("the Ladder: rungs in roster order, each on its kingdom's field, until a loss or \"That's enough\"",
      beat && beat >= 1 && L.count == before + beat && fought == want.first(fought.length) && fought.length == [beat + 1, 2].min && own_errors(log).empty?,
      [beat, L.count, fought, want, own_errors(log).first])
check("a beaten rung isn't fought twice; the next rung is the first unbeaten one", L.beaten?(L.present_rungs.first[:key]) && L.next_rung != L.present_rungs.first)
L::ROSTER.each_with_index { |r, i| r[:trainer] = backup[i] }

#-------------------------------------------------------------------------------
section "5. The finale"
#-------------------------------------------------------------------------------
F = Prismfall::Finale
check("eleven lamps = tally(:ENGINE_BREAKS)", F.lamps.length == 11 && F.lamp_total == pf_tally(:ENGINE_BREAKS))
Prismfall::Choices.make(:ch14_telemetry, :sabotage) rescue nil
Prismfall::Choices.make(:ch20_calla, :send_back) rescue nil
beats = F.montage
check("the montage follows the flags (Larch's two lamps, Calla's two)",
      beats.find { |b| b[:id] == :LARCH }&.dig(:lamps) == [0, 1] && beats.find { |b| b[:id] == :CALLA_BACK }&.dig(:lamps) == [6, 7], beats.map { |b| [b[:id], b[:lamps]] })
check("the always-beats are there (Sigrun, Marisol, Tamsin, Kaito)", ([:SIGRUN, :MARISOL, :TAMSIN, :KAITO] - beats.map { |b| b[:id] }).empty?)
check("playing the montage lights exactly tally(:ENGINE_BREAKS) lamps", F.play_montage(cut: 0) == pf_tally(:ENGINE_BREAKS))
check("V117 ENGINE_WEAKPOINTS is recomputed", $game_variables[117] == F::WEAKPOINTS.count { |c| Prismfall::Conditions.evaluate(c) })
check("the partner is never K2's Lv 21 team", GameData::Trainer.get(*F.partner).pokemon.map { |p| p[:level] }.max >= 80, F.partner)
check("two tag foes at v21", F.tag_foes.length == 2 && F.tag_foes.all? { |t| t[2] == 21 }, F.tag_foes)
F.answers = [1]
check("his hand, refused (no game over)", F.his_hand == :refused)
go = nil
F.answers = [0]
check("his hand, taken without VOSS_ACCEPTED: GO_HIS_HAND", F.his_hand == :game_over && go == :GO_HIS_HAND, go)
if Prismfall::Bosses.respond_to?(:arceus_consent_override=)
  Prismfall::Bosses.arceus_consent_override = proc { |g| g != 2 }
  strong_team(2)
  log = Harness.run_battle("arceus", seed: 1) { Prismfall::Bosses.wild_battle(:ARCEUS_FINALE) }
  t = log.text
  check("the Arceus battle: bar 1's Wardens kneel; Dorian releases, Tamsin refuses, Marisol releases",
        t.include?("Dorian kneels at the Blank pylon.") && t.include?("Tamsin: I can't. I can't.") && t.include?("Marisol: The Ebb ran both ways"), t.lines.grep(/kneels/).first(3))
  check("the record: 1 and 3 released, 2 refused; V118 counts releases", F.lock_state(1) == :released && [:refused, :forced].include?(F.lock_state(2)) && $game_variables[118] == F.released_count)
  check("a refuser's Last Shatter slide / empty pedestal line", F.shatter_slides.map(&:first).include?("Briarwick") && F.pedestal_line(2) && F.pedestal_line(1).nil?)
  Prismfall::Bosses.arceus_consent_override = nil
end
check("ending vignettes are keyed by ending ID", F.vignette?(:bride_tree, :END_HOMECOMING) && !F.vignette?(:bride_tree, :END_GILDED_CHAIN) && F.vignettes(:END_UNFINISHED).any? { |v| v[:key] == :last_shatter })

#-------------------------------------------------------------------------------
section "6. Story battle hooks"
#-------------------------------------------------------------------------------
strong_team
log = Harness.run_battle("K6", seed: 3) { Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 6, field: :HOLLOW_CATHEDRAL) }
t = log.text
i1 = t.index("Kestrel's Gauntlet is overloading!")
i2 = t.index("FIELD CHANGE: HOLLOW_CATHEDRAL -> BLEED")
i3 = t.index("FIELD CHANGE: BLEED -> HOLLOW_CATHEDRAL")
check("K6: the Gauntlet overloads once, the field flickers to the Bleed and back", log.errors.empty? && i1 && i2 && i3 && i1 < i2 && i2 < i3 && t.scan("is overloading").length == 1, [i1, i2, i3, log.errors.first])
if i2 && i3
  turns = t[i2...i3].scan(/--- Turn \d+ ---/).length
  check("K6: the Bleed lasts one full turn", turns == 1, turns)
end
strong_team
setBattleRule("field", :PRISM_ARENA)
log = Harness.run_battle("K8", seed: 5) { Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 8) }
check("K8 (Redeemed): at the first Plates turn he tears the Gauntlet off and the arena goes still",
      log.errors.empty? && log.text.include?("Not like this") && log.text.scan("The Plates turn!").length == 1, log.errors.first)
strong_team
setBattleRule("field", :PRISM_ARENA)
Prismfall.state.custom[:valen_crystal] = 0
log = Harness.run_battle("Final", seed: 5) { TrainerBattle.start(:CHAMPION_VALEN, "Valen", 0) }
turns = log.text.scan("The Plates turn!").length
check("the Final: one crystal line per Plates turn (#{turns}); the stage is kept for the Coronation",
      turns > 0 && log.text.scan("The crystal climbs Valen's throat").length == turns && FieldEffects::StoryHooks.valen_crystal == [turns, 4].min,
      [turns, log.text.scan("The crystal climbs").length, FieldEffects::StoryHooks.valen_crystal])

#-------------------------------------------------------------------------------
section "7. The Registry"
#-------------------------------------------------------------------------------
R = tr::Registry
Prismfall.state.narrative[:postgame] = false
check("19 cards in three tiers (8 / 5 / 6), all registered", R.cards.length == 19 && [1, 2, 3].map { |x| R.cards(x).length } == [8, 5, 6])
check("before S160: no scope, Larch's own lines play, nothing is available, the catch gate holds",
      R.scope == :none && R.larch == false && R.cards.none? { |id| tr.state(id) == :available } && Prismfall.story_legendary_locked?(Pokemon.new(:MELOETTA, 85)))
$game_switches[160] = true
tr.answers = [-1]
MSG.clear
R.larch
check("Larch's first post-game talk opens the Registry (S270, V143 = 1)", $game_switches[270] && $game_variables[143] == 1 && MSG.any? { |m| m.include?("I'm calling it the Registry") })
rows = R.board_rows
check("the board lists the eight Tier 1 cards first, then the sealed tiers",
      rows.first(8).map { |r| r[1] } == R.cards(1) && rows[8][1].nil? && rows[8][0].include?("Tier 2") && rows[9][0].include?("Tier 3"), rows.map { |r| r[1] })
check("T1-6 needs the cradle key (S180) or Calla alive", tr.state(:PG_TYPENULL) == :locked && ($game_switches[180] = true) && tr.state(:PG_TYPENULL) == :available)
bosses = em.ids.select { |i| i.to_s.start_with?("PG_") && em.get(i)[:kind] == :boss }
check("every Registry legend is a bar boss caught on its last bar (#{bosses.length}); the gifts are gifts",
      bosses.all? { |i| em.get(i)[:boss][:catch] == :last_bar } && [:PG_TYPENULL, :PG_KUBFU].all? { |i| em.get(i)[:kind] == :gift })
check("the catch gate is open in the post-game", Prismfall.legendary_catch_allowed?(Pokemon.new(:MELOETTA, 85)))
idx = R.board_rows.index { |r| r[1] == :PG_MELOETTA }
tr.answers = [idx, "Yes", -1]
R.board
check("a card taken from the board; the giver briefs once", tr.active?(:PG_MELOETTA) && tr.talk_ready?(:PG_DORIAN) && tr.talk(:PG_DORIAN) && tr.step(:PG_MELOETTA) == :encore)
3.times do |i|
  break if tr.done?(:PG_MELOETTA)
  strong_team
  log = Harness.run_battle("encore #{i}", seed: 11 + i) { tr.talk(:PG_OPERA_STAGE); $game_variables[1] }
  check("the Encore: a real boss battle on a Standing Ovation stage, no engine error", log.errors.empty? && log.text.include?("field: GRAND_STAGE (stage 3)"), log.errors.first)
end
check("T1-1 cleared: S271 on", tr.done?(:PG_MELOETTA) && $game_switches[271] && R.clears(1) == 1)
[272, 273, 274].each { |n| $game_switches[n] = true }
check("Tier 2 stays sealed without the Distortion Core, opens with it (S279)",
      R.refresh_tiers(false).empty? && ($game_switches[268] = true) && R.refresh_tiers(false) == [2] && $game_switches[279])
idx = R.board_rows.index { |r| r[1] == :PG_UBS }
tr.answers = [idx, -1]
MSG.clear
R.board
check("a designed (stub) card shows but can't be taken", idx && !tr.active?(:PG_UBS) && MSG.any? { |m| m.include?("NOT YET") })
[280, 281, 282].each { |n| $game_switches[n] = true }
check("Tier 3 needs the Gauntlet (S267) too (S285)", R.refresh_tiers(false).empty? && ($game_switches[267] = true) && R.refresh_tiers(false) == [3] && $game_switches[285])
$game_switches[265] = true
check("Ruin world: no Convergence card", R.scope == :ruin && R.board_rows.none? { |r| r[1] == :PG_ARCEUS })
$game_switches[265] = false
check("otherwise the Convergence is on the board", R.board_rows.any? { |r| r[1] == :PG_ARCEUS })
MSG.clear
tr.answers = [-1]
R.larch
check("the black card (S267): S269 on, V143 = 5", $game_switches[269] && $game_variables[143] == 5 && MSG.any? { |m| m.include?("He kept them") })
Prismfall.state.narrative[:postgame] = :END_CONCORD_DAWN
$game_switches[279] = false
$game_switches[285] = false
check("Concord Dawn / Hollow Spring: Tier 1 only", R.scope == :partial && R.refresh_tiers(false).empty? && !R.tier_open?(2))
Prismfall.state.narrative[:postgame] = :END_HOMECOMING
tr.start(:PG_ROAMERS, false)
strong_team
log = Harness.run_battle("rumour", seed: 3) { pf_registry_roamer(:HEATRAN); $game_variables[1] }
check("a Warden's rumour is a real boss battle", log.errors.empty? && !em.status(:PG_ROAM_HEATRAN).nil?, log.errors.first)
em.ids.select { |i| i.to_s.start_with?("PG_ROAM_") }.first(8).each { |i| em.set_status(i, :won) }
strong_team
Harness.run_battle("rumour 2", seed: 3) { pf_registry_roamer(:DIANCIE); $game_variables[1] }
tr.answers = [-1]
R.larch
check("eight rumours settled: Larch closes T1-8 (S278)", tr.done?(:PG_ROAMERS) && $game_switches[278])
check("save round trip", Marshal.load(Marshal.dump(Prismfall.state)).trials[:quests][:PG_MELOETTA][:state] == :done)

puts
puts "#{$fails.length} failed" + ($fails.empty? ? "" : ": " + $fails.join(" | "))
exit(($fails.empty?) ? 0 : 1)
