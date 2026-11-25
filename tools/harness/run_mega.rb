#===============================================================================
# Prismfall Mega Evolution - headless integration test (SPINE Revisions 20, 21 and 23)
#   PRISM_RUN_DIR=<private run copy> PRISM_COMPILE=1 ruby tools/harness/run_mega.rb
# The run copy needs the Prismfall Core, Field Effects, Z-Power, Bosses, Trials and Mega plugins (symlinks to the
# kit's plugins/ folder) and the kit's pbs/ files copied in with the package.sh names (town_map.txt left out).
# Through the real Essentials v21.1 battle code:
#   1. data: the 47 Gen 6/7 Mega forms and stones, the Mega Ring, PrismfallMega::STONES (every stone placed or listed
#      as unplaced), the Ring-Day gate, every stone against the Warden answers (rule R4 with the Ring), the quests and
#      rank rewards that hand stones out, the map events (design/TRIAL_EVENTS.yaml) that place the rest
#   2. a Mega in a field battle (the player's side, AI-controlled): Camerupt on Volcanic primes an eruption
#   3. the AI Mega Evolving: Anja's gym battle (Gym 10, Standard) on the Frozen Lake; Brann's weak Mega Camerupt
#      (Gym 7, Standard, kept as designed) Megas and primes the volcano; pbs/trainers.txt against the Rev 21 rules (every
#      important fight from ace 50 has one Mega in every mode, below 50 only designed weak ones); Kestrel's K8 with
#      Morwen's Ring (the ring and Mega Scizor at battle start)
#   4. a Mega and a Z-move in the same battle: one trainer's double (Mega Lucario + Hydro Vortex), the player's
#      side on Water Surface with the ONE ring (Rev 23: MEGARING wakes crystals; the old Z-Power Ring alone still
#      works for old saves), and two trainers on one side; the Z-crystal distribution (R4) and a species Z-move
#   5. one Mega and one Z per SIDE: two foe trainers with a Mega Stone each / a Z-crystal each, side vs trainer limit
#   6. rules: no ring -> no Mega; wild Pokemon never Mega Evolve; a Z-crystal blocks Rayquaza's Mega
#   7. field showpieces (Grand Stage, Volcanic, Colosseum, Frozen Lake, Crystal Cavern, Hollow Cathedral, Factory,
#      Bleed) and the Mega's new ability on entry rules (Inverse: Magic Bounce; Colosseum: No Guard); Field Notes
#   8. the quests: the teaser before the Ring, the Ring-Day (Bastian, 13 badges), Brann's spare and the Light Stone,
#      a boss stone (the Old Pincer), the brazier writ
#   9. trainer speech (Z-Power 005): Celestine's line when her Mimikyu's Z-move fires; no line for a trainer without one
# Writes docs/mega_test/REPORT.md and transcript.txt. Exit 1 on any failure.
#===============================================================================
require "fileutils"
require "json"
require "yaml"
load File.join(__dir__, "boot.rb")
load File.join(HARNESS_DIR, "log_scene.rb")

OUT = ENV["PRISM_OUT"] || File.expand_path("../../docs/mega_test", HARNESS_DIR)
FileUtils.mkdir_p(OUT)
TRANSCRIPT = []
RESULTS = []

def pbMessage(message, commands = nil, cmd_if_cancel = 0, _skin = nil, default_cmd = 0, &_block)
  text = Harness.clean(message.to_s)
  TRANSCRIPT << "  #{text}" + (commands ? "  [choices: #{commands.join(' / ')}]" : "")
  Harness.log&.add("(overworld message) #{text}")
  return default_cmd if commands
  return 0
end
def pbNickname(_pkmn); end
MAPS = JSON.parse(File.read(File.expand_path("../../design/maps.json", HARNESS_DIR)))["maps"].map { |m| [m["id"], m] }.to_h
def pbGetMapNameFromId(id); (MAPS[id] || {})["name"] || "Map #{id}"; end
def pbSEPlay(*_a); end
def pbMEPlay(*_a); end

def check(name, ok, detail = "")
  RESULTS << [name, ok ? true : false, detail.to_s]
  puts format("%-6s %s %s", ok ? "PASS" : "FAIL", name, detail.to_s.empty? ? "" : "(#{detail})")
  ok
end

def section(title)
  TRANSCRIPT << "" << "=== #{title} ==="
  puts "--- #{title}"
end

def scene(quest, name, answers = [])
  Prismfall::Trials.answers = answers.dup
  TRANSCRIPT << "-- #{quest} / #{name}"
  log = Harness::BattleLog.new("#{quest}/#{name}")
  Harness.current_log = log
  begin
    Prismfall::Trials::Script.run_scene(quest, name)
  ensure
    Harness.current_log = nil
  end
  TRANSCRIPT << log.text.lines.map { |l| "    | #{l.rstrip}" }.join("\n") if log.battle
  log.errors.each { |e| check("no engine error in #{quest}/#{name}", false, e.inspect[0, 300]) }
end

def mk(species, level, moves, item = nil, ability = nil)
  p = Pokemon.new(species, level)
  GameData::Stat.each_main { |s| p.iv[s.id] = 31 }
  p.forget_all_moves
  moves.each { |m| p.learn_move(m) }
  p.item = item if item
  p.ability = ability if ability
  p.calc_stats
  p
end

def set_badges(n)
  $player.badges = Array.new(18) { |i| i < n }
end

def npc(type, name, party, items = [])
  t = NPCTrainer.new(name, type)
  t.party = party
  t.items = items
  t
end

# Every Mega Evolution and Z-move, with the field state right after it (the test handler runs after the plugin's).
MEGAS = []
EventHandlers.add(:prismfall_mega_evolved, :mega_test_log,
  proc { |battle, b, old_ability|
    st = (defined?(FieldEffects) && FieldEffects.active?(battle)) ? FieldEffects.state(battle) : {}
    crack = (FieldEffects.active?(battle)) ? FieldEffects.transition_progress(battle, :crack) : nil
    MEGAS << { :side => b.index & 1, :idx => b.index, :species => b.species, :form => b.form, :ability => b.ability_id,
               :old_ability => old_ability, :turn => battle.turnCount + 1, :field => battle.field_effect,
               :stage => battle.field_stage, :primed => st[:primed], :kos => st[:kos], :hue => st[:cc_hue],
               :crack => crack, :stages => b.stages.dup, :borrowed => FieldEffects.borrowed_fields(battle).dup,
               :owner => battle.pbGetOwnerIndexFromBattlerIndex(b.index) }
  })
ZS = []
EventHandlers.add(:prismfall_zmove_unleashed, :mega_test_z,
  proc { |battle, user, z| ZS << { :side => user.index & 1, :idx => user.index, :z => z.id, :turn => battle.turnCount + 1,
                                    :owner => battle.pbGetOwnerIndexFromBattlerIndex(user.index) } })
OVERLAYS = []
EventHandlers.add(:prismfall_field_overlay_changed, :mega_test_overlay,
  proc { |_battle, field, old_ids, new_ids| OVERLAYS << [field, old_ids, new_ids] })
# One-shot field-start setups (a crack in the lake, a crystal hue).
FIELD_START = {}
EventHandlers.add(:prismfall_field_changed, :mega_test_field_start,
  proc { |battle, old_id, new_id|
    next if old_id != :NONE || !FIELD_START[new_id]
    FIELD_START.delete(new_id).call(battle)
  })

def run(title, seed: 7, setup: nil, &block)
  log = Harness.run_battle(title, :seed => seed, :setup => setup, &block)
  TRANSCRIPT << "" << log.text
  log.errors.each { |e| check("no engine error in '#{title}'", false, "#{e[:class]}: #{e[:message]} #{e[:backtrace].first(3).join(' ')}") }
  log
end

def wild(title, party, foe, field: nil, stage: nil, seed: 7, double: false, setup: nil)
  $player.party = party
  run(title, :seed => seed, :setup => setup) do
    setBattleRule("field", field) if field
    setBattleRule("fieldStage", stage) if stage
    setBattleRule("double") if double
    setBattleRule("canLose"); setBattleRule("cannotRun")
    foe.is_a?(Array) ? WildBattle.start(*foe) : WildBattle.start(foe)
  end
end

def foe_wall(level = 60)
  mk(:CHANSEY, level, [:SPLASH], nil, :NATURALCURE)
end

Harness.new_game_state
Prismfall.record_starter(:CHARMANDER) if Prismfall.respond_to?(:record_starter)
$PokemonEncounters = PokemonEncounters.new
Prismfall.state.level_cap_override = 100     # logic test: over-cap test teams must obey
tr = Prismfall::Trials
pm = PrismfallMega

#-------------------------------------------------------------------------------
section("1. Data: Mega forms and stones, the Ring, the distribution, gates, quests, events")
#-------------------------------------------------------------------------------
megas = []
GameData::Species.each { |sp| megas << sp if sp.mega_stone || sp.mega_move }
stones = []
GameData::Item.each { |it| stones << it.id if it.is_mega_stone? }
check("Gen 6/7 Mega forms: #{megas.length} (47 with a stone + Rayquaza's Dragon Ascent)",
      megas.count { |s| s.mega_stone } == 47 && megas.any? { |s| s.species == :RAYQUAZA && s.mega_move == :DRAGONASCENT },
      megas.map { |s| "#{s.species}_#{s.form}" }.first(6).join(","))
check("47 Mega Stone items, each the stone of a form", stones.length == 47 &&
      stones.all? { |s| megas.any? { |m| m.mega_stone == s } }, "#{stones.length}")
ring = GameData::Item.try_get(pm::RING)
check("the Mega Ring is a key item with the MegaRing flag", ring && ring.is_key_item? && ring.has_flag?("MegaRing"))
covered = pm::STONES.keys + pm::UNPLACED
check("every stone is placed (#{pm::STONES.length}) or listed as unplaced (#{pm::UNPLACED.length})",
      (stones - covered).empty? && (covered - stones).empty? && covered.uniq.length == covered.length,
      "missing #{(stones - covered).inspect}, unknown #{(covered - stones).inspect}")
bad_rows = pm::STONES.reject { |_s, d| d[:badges].is_a?(Integer) && MAPS[d[:map]] && [:hidden, :item, :quest, :rank, :boss, :puzzle, :story].include?(d[:how]) }
check("every STONES row has a badge gate, a known map and a known method", bad_rows.empty?, bad_rows.keys.inspect)
check("the Ring comes after Badge 13, like Reborn (13 at the earliest) and Rejuvenation (about 14): Cragholm, Bastian",
      pm::RING_BADGES == 13 && pm::STONES[:AGGRONITE][:map] == 363 && pm::STONES[:AGGRONITE][:source] == :OS_RING_DAY &&
      tr.get(:OS_RING_DAY) && tr.get(:OS_RING_DAY)[:unlock].include?("badges >= 13"))

# Warden answers: warden_gates.json where the trainer designer has set them (R9), else the type chart (super-effective
# attacking types, plus types immune to the Warden's type).
gates = JSON.parse(File.read(File.expand_path("../../design/warden_gates.json", HARNESS_DIR)))
horizon = gates["rules"]["gift_horizon"] || 2
answers = {}
gates["wardens"].each do |w|
  n = w["n"]; t = w["type"].to_sym
  if w["answers"]
    answers[n] = w["answers"].map(&:to_sym)
  else
    a = []
    GameData::Type.each do |at|
      next if at.pseudo_type
      eff = Effectiveness.calculate(at.id, t)
      a << at.id if Effectiveness.super_effective?(eff)
      a << at.id if Effectiveness.ineffective?(Effectiveness.calculate(t, at.id))
    end
    answers[n] = a.uniq
  end
end
gate_errors = []
mega_types = {}
pm::STONES.each do |stone, d|
  form = megas.find { |m| m.mega_stone == stone }
  types = form.types.uniq
  mega_types[stone] = types
  usable = [d[:badges], pm::RING_BADGES].max
  (1..horizon).each do |k|
    n = usable + k
    next if n > 18 || !answers[n]
    hit = types & answers[n]
    gate_errors << "#{stone} (#{types.join('/')}) usable at #{usable} answers Warden #{n} (#{hit.join(',')})" if !hit.empty?
  end
end
check("R4 with the Ring: no stone powers up an answer to the next #{horizon} Wardens when it becomes usable",
      gate_errors.empty?, gate_errors.first(4).join("; "))
teasers = pm::STONES.select { |_s, d| d[:badges] < pm::RING_BADGES }.keys
# Reborn hands out 4-5 stones before its ring and Rejuvenation about 6; ours were placed for a ring at 7 badges and the
# safe ones stay as "hum and wait" collectibles (SPINE Rev 21), so the band is wider.
check("stones before the Ring 'hum and wait' (#{teasers.length}): #{teasers.map { |s| GameData::Item.get(s).name }.join(', ')}",
      teasers.length.between?(6, 14))
s_tier = [:KANGASKHANITE, :MAWILITE, :MEDICHAMITE, :METAGROSSITE, :SALAMENCITE, :GENGARITE, :LOPUNNITE, :GARDEVOIRITE,
          :LUCARIONITE, :TYRANITARITE, :GARCHOMPITE, :ALAKAZITE, :GYARADOSITE, :SCIZORITE, :BLAZIKENITE, :CHARIZARDITEX, :CHARIZARDITEY]
early_s = s_tier.select { |s| pm::STONES[s][:badges] < 10 }
check("the strongest stones come late (Reborn 12-17, Rejuvenation 11-15): none before 10 badges", early_s.empty?, early_s.inspect)
check("legendary stones are post-game", [:LATIASITE, :LATIOSITE].all? { |s| pm::STONES[s][:badges] >= 18 })

src_errors = []
pm::STONES.each do |stone, d|
  case d[:how]
  when :quest, :story, :boss
    q = tr.get(d[:source])
    if !q
      src_errors << "#{stone}: quest #{d[:source]} missing"
      next
    end
    items = (q[:reward] || {})[:items] || []
    src_errors << "#{stone}: #{d[:source]} doesn't reward it" if !items.any? { |i, _n| i == stone }
    gate = q[:unlock].to_s.scan(/badges\s*>=\s*(\d+)/).flatten.map(&:to_i).max
    src_errors << "#{stone}: #{d[:source]} unlock '#{q[:unlock]}' is below #{d[:badges]} badges" if !gate || gate < d[:badges]
    src_errors << "#{stone}: #{d[:source]} is on map #{q[:map]}, STONES says #{d[:map]}" if q[:map] != d[:map] && d[:how] != :boss
  when :rank
    rw = tr::RANK_REWARDS[d[:source]] || {}
    src_errors << "#{stone}: no #{d[:source]} rank reward" if !rw.values.any? { |r| (r[:items] || []).any? { |i, _n| i == stone } }
  end
end
check("quests, story scenes, bosses and rank rewards hand out their stones at or after the gate", src_errors.empty?,
      src_errors.first(4).join("; "))
# Rank rewards are not badge-gated: a rank stone must be reachable (Trial points from implemented quests) before the
# Ring-Day, so the R4 check above (usable at RING_BADGES) holds for it. Chapter -> badges held, story order.
ch2b = { 0 => 0, 1 => 0, 2 => 0, 3 => 1, 4 => 2, 5 => 3, 6 => 4, 7 => 5, 8 => 6, 9 => 7, 10 => 8, 11 => 9, 12 => 10,
         13 => 11, 14 => 12, 15 => 13, 16 => 14, 17 => 15, 18 => 16, 19 => 17, 20 => 18, 21 => 18 }
pts_by = lambda do |trial, b|
  tr.quest_ids.sum do |id|
    q = tr.get(id)
    next 0 if q[:stub] || q[:trial] != trial
    need = [ch2b[q[:chapter].to_i] || 0, *q[:unlock].to_s.scan(/badges\s*>=\s*(\d+)/).flatten.map(&:to_i)].max
    (need <= b) ? (q[:points] || 1) : 0
  end
end
rank_late = []
pm::STONES.select { |_s, d| d[:how] == :rank }.each do |s, d|
  rank = (tr::RANK_REWARDS[d[:source]] || {}).find { |_r, rw| (rw[:items] || []).any? { |i, _n| i == s } }&.first
  have = pts_by.call(d[:source], pm::RING_BADGES - 1)
  need = tr::RANK_POINTS[(rank || 99) - 1] || 999
  rank_late << "#{s}: #{d[:source]} rank #{rank} needs #{need} points, #{have} available before the Ring" if have < need
end
check("rank-reward stones are reachable before the Ring (so the R4 check holds for them)", rank_late.empty?, rank_late.join("; "))

spec = YAML.safe_load(File.read(File.expand_path("../../design/TRIAL_EVENTS.yaml", HARNESS_DIR)))
placed = {}
ev_errors = []
spec["maps"].each do |mid, m|
  (m["events"] || []).each do |e|
    cmds = Array(e["commands"]).join(" ")
    cmds.scan(/pf_mega_stone\(:(\w+)/).flatten.each do |it|
      placed[it.to_sym] = [mid, e]
      ev_errors << "#{it}: event condition '#{e['condition']}'" if !(e["condition"].to_s =~ /badges >= (\d+)/ && $1.to_i >= pm::STONES[it.to_sym][:badges])
    end
    begin
      Prismfall::Conditions.check(e["condition"]) if e["condition"]
    rescue StandardError => ex
      ev_errors << "#{mid} #{e['name']}: bad condition (#{ex.message})"
    end
  end
end
world = pm::STONES.select { |_s, d| [:hidden, :item, :puzzle].include?(d[:how]) }
world.each do |s, d|
  if !placed[s]
    ev_errors << "#{s}: no map event"
  elsif placed[s][0] != d[:map]
    ev_errors << "#{s}: event on map #{placed[s][0]}, STONES says #{d[:map]}"
  end
end
mega_keys = File.read(File.expand_path("../../plugins/Prismfall Trials/152_Talk_Megas.rb", HARNESS_DIR)).scan(/^  :([A-Z_]+) => \{/).flatten
yaml_keys = spec["maps"].values.flat_map { |m| (m["events"] || []).map { |e| e["key"] } }.compact
ev_errors << "TALK keys without a map event: #{(mega_keys - yaml_keys).inspect}" if !(mega_keys - yaml_keys).empty?
check("design/TRIAL_EVENTS.yaml places all #{world.length} world stones (pf_mega_stone, badge-gated) and every Mega talk key",
      ev_errors.empty?, ev_errors.first(4).join("; "))
check("Prismfall Z-Power is one Z per side too (owner key = side)", PrismfallZ.owner_key(nil, 0) == PrismfallZ.owner_key(nil, 2) &&
      PrismfallZ.owner_key(nil, 1) != PrismfallZ.owner_key(nil, 0))

#-------------------------------------------------------------------------------
section("2. A Mega in a field battle: the player's Camerupt on Volcanic")
#-------------------------------------------------------------------------------
$bag.add(:MEGARING) if !$bag.has?(:MEGARING)
n0 = MEGAS.length
log = wild("Mega: the player's Camerupt (AI-controlled) on the Volcanic field", [mk(:CAMERUPT, 60, [:EARTHPOWER, :FLAMETHROWER, :ROCKSLIDE, :YAWN], :CAMERUPTITE)],
           foe_wall, field: :VOLCANIC)
m = MEGAS[n0..].find { |x| x[:side] == 0 } || {}
check("the player's Camerupt Mega Evolved on turn 1 (ring in the Bag, Cameruptite held)", m[:species] == :CAMERUPT && m[:form] == 1 && m[:turn] == 1,
      m.inspect[0, 120])
check("the Mega messages and both EBDX-named animations ran", log.include?(/is reacting to/) && log.include?(/has Mega Evolved into Mega Camerupt/) &&
      log.include?(/anim: MegaEvolution\)/) && log.include?(/anim: MegaEvolution2/))
check("the Mega's ability is Sheer Force (form data), and the field saw the change", m[:ability] == :SHEERFORCE && m[:field] == :VOLCANIC)
check("Volcanic showpiece: a Fire-type Mega primes the volcano, which erupts at the end of the round",
      m[:primed] == true && log.include?(/stirred the magma/) && log.include?(/The volcano erupted!/))
i_mega = log.lines.index { |l| l.include?("has Mega Evolved") }
i_move = log.lines.index { |l| l =~ /Camerupt used / }
check("the Mega happens before any move that turn", i_mega && i_move && i_mega < i_move, "#{i_mega} < #{i_move}")
check("only one Mega in the whole battle (#{log.turns} turns)", MEGAS[n0..].count { |x| x[:side] == 0 } == 1)

#-------------------------------------------------------------------------------
section("3. The AI Mega Evolving: Anja (Gym 10) and Brann's weak Mega (Gym 7); trainers.txt and the Rev 21 rules")
#-------------------------------------------------------------------------------
strong = lambda do
  [mk(:TOGEKISS, 80, [:AIRSLASH, :DAZZLINGGLEAM, :FLAMETHROWER, :ROOST], :LEFTOVERS),
   mk(:GARCHOMP, 80, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :FIREFANG], :LIFEORB),
   mk(:SLOWBRO, 80, [:PSYCHIC, :SCALD, :SLACKOFF, :ICEBEAM], :LEFTOVERS)]
end
$player.party = strong.call
n0 = MEGAS.length
log = run("AI: Anja's gym battle (Standard, v0) through Prismfall.gym_battle(10)", :seed => 11) do
  Prismfall.gym_battle(10, can_lose: true)
end
k = MEGAS[n0..].find { |x| x[:side] == 1 } || {}
check("Anja's Glalie Mega Evolved on Standard (AI, MEGARING in her items)", k[:species] == :GLALIE && k[:form] == 1 && k[:field] == :FROZEN_LAKE,
      k.inspect[0, 100])
g_out = log.lines.index { |l| l =~ />> sent out \(foe\): .*@GLALITITE/ }
g_mega = log.lines.index { |l| l =~ /has Mega Evolved into Mega Glalie/ }
turn_between = g_out && g_mega ? log.lines[g_out..g_mega].count { |l| l.start_with?("--- Turn") } : 99
check("the AI Mega Evolves the first turn its Glalie can act", turn_between <= 1, "#{turn_between} turn headers in between")

# Brann's own Standard Camerupt (pbs/trainers.txt, v0), alone, on his Volcanic field, against a wall that lasts.
brann = pbLoadTrainer(:LEADER_BRANN, "Brann", 0)
brann.party.select! { |p| p.species == :CAMERUPT }
$player.party = [mk(:BLISSEY, 39, [:SOFTBOILED, :SEISMICTOSS], :LEFTOVERS)]
n0 = MEGAS.length
log = run("AI: Brann's Standard Camerupt (v0) alone on Volcanic: a weak Mega below Lv 50", :seed => 3) do
  setBattleRule("canLose"); setBattleRule("field", :VOLCANIC)
  TrainerBattle.start(brann)
end
k = MEGAS[n0..].find { |x| x[:side] == 1 } || {}
check("Brann's Camerupt Mega Evolves on Standard at Gym 7 (a designed weak Mega below Lv 50)", k[:species] == :CAMERUPT && k[:form] == 1,
      k.inspect[0, 100])
check("...on Volcanic, and its Mega primes the eruption as designed (Brann's fight is kept as is, per the user)",
      k[:field] == :VOLCANIC && log.include?(/Mega Evolution stirred the magma/))

# pbs/trainers.txt: every important fight from an ace of MEGA_FULL_LEVEL holds exactly one Mega Stone and the ring in
# every mode, unless the story gives the fighter no ring (MEGA_EVOLUTION.md 6.3; the user: story and theme win over the
# rule); below it only the designed weak Mega (Brann) on Standard and Hard; nobody holds a stone and a Z-crystal.
# Partners on the player's side and one trainer of a pair that shares a side are exceptions too.
important = /\A(LEADER_|RIVAL_|CHAMPION_|MERIDIAN_|HOLLOW_MOURNER|ECHO_MORWEN|GILDED_AURELIUS|ARCHSEER_DASK|ASHKAAR_OFFICER|ISENMAR_OFFICER)/
no_mega_ok = { [:LEADER_SIGRUN, 19] => "war partner (the player's side)", [:LEADER_MARISOL, 19] => "war partner",
               [:RIVAL_JUNO, 70] => "Ch21 partner", [:RIVAL_JUNO, 71] => "Ch21 partner", [:RIVAL_JUNO, 72] => "Ch21 partner",
               [:MERIDIAN_QUENT, 1] => "shares a side with Marchetti v2 (Mega Houndoom)",
               [:LEADER_ROOK, 90] => "shares a side with Dorian v90 (Mega Lopunny)" }
# No ring in the story (MEGA_EVOLUTION.md 6.3). Kestrel's K8 gets one at battle start only with Morwen's Ring.
no_ring = [:RIVAL_KESTREL, :LEADER_ROWAN, :ARCHSEER_DASK, :ECHO_MORWEN, :GILDED_AURELIUS, :ASHKAAR_OFFICER, :ISENMAR_OFFICER]
weak_ok = { :LEADER_BRANN => [0] }
# SPINE Rev 23: designed Z users in place of a Mega, from 13 badges, with a story reason (Z_MOVES.md 4).
z_users = [:LEADER_CELESTINE]
rule_errors = []
counted = Hash.new(0)
OCTAVE_LIKE = lambda { |t| t.trainer_type.to_s.start_with?("OCTAVE") }
GameData::Trainer.each do |t|
  next if t.trainer_type.to_s !~ important || t.trainer_type.to_s =~ /[a-z]/   # Prismfall's types only (not the base kit's)
  base = t.version % 100
  mode = t.version / 100
  ace = t.pokemon.map { |p| p[:level] }.max || 0
  ace_std = (GameData::Trainer.try_get(t.trainer_type, t.real_name, base) || t).pokemon.map { |p| p[:level] }.max || ace
  st = t.pokemon.select { |p| p[:item] && GameData::Item.get(p[:item]).is_mega_stone? }
  zc = t.pokemon.select { |p| p[:item] && PrismfallZ.crystal?(p[:item]) }
  ring = t.items.include?(:MEGARING)
  key = "#{t.trainer_type},#{t.real_name},#{t.version}"
  rule_errors << "#{key}: #{st.length} stones" if st.length > 1
  rule_errors << "#{key}: a stone and a Z-crystal" if !st.empty? && !zc.empty?
  rule_errors << "#{key}: a stone without MEGARING" if !st.empty? && !ring
  if ace_std >= pm::MEGA_FULL_LEVEL
    next if no_mega_ok[[t.trainer_type, base]]
    if no_ring.include?(t.trainer_type)
      rule_errors << "#{key}: has a Mega, but the story gives them no ring" if !st.empty?
      next
    end
    if st.empty? && !zc.empty? && z_users.include?(t.trainer_type) && ace_std >= 63 then counted[mode + 10] += 1
    elsif !zc.empty? && !OCTAVE_LIKE.call(t) && !z_users.include?(t.trainer_type) then rule_errors << "#{key}: a Z-crystal without a story reason"
    elsif st.empty? then rule_errors << "#{key}: ace #{ace_std}, no Mega"
    else counted[mode] += 1
    end
  elsif !st.empty?
    weak = st.all? { |p| pm::WEAK_STONES.include?(p[:item]) }
    designed = (weak_ok[t.trainer_type] || []).include?(base) && mode != 2
    rule_errors << "#{key}: ace #{ace_std}, #{st.map { |p| p[:item] }.join(',')} below Lv #{pm::MEGA_FULL_LEVEL}" if !(weak && designed)
  end
end
check("trainers.txt: every important fight from ace #{pm::MEGA_FULL_LEVEL} Megas in all modes (#{counted[0]} Std / #{counted[1]} Hard / " \
      "#{counted[2]} Casual) or uses a designed Z (#{counted[10]} / #{counted[11]} / #{counted[12]}); below it only designed weak Megas; " \
      "one stone, a ring, no Z-crystal beside it", rule_errors.empty?,
      rule_errors.first(5).join("; "))

# Kestrel's K8: no ring of his own; with Morwen's Ring (Ch18) the ring and the Scizorite at battle start.
k8 = pbLoadTrainer(:RIVAL_KESTREL, "Kestrel", 80)
EventHandlers.trigger(:on_trainer_load, k8)
plain = k8 && !k8.items.include?(:MEGARING) && k8.party.none? { |p| GameData::Item.get(p.item_id).is_mega_stone? rescue false }
check("K8 without Morwen's Ring: no ring, no stone (Kestrel has no ring of his own)", plain)
Prismfall::Choices.make(:ch18_kestrel_ring, :give_now, false)
k8c = pbLoadTrainer(:RIVAL_KESTREL, "Kestrel", 80)
EventHandlers.trigger(:on_trainer_load, k8c)   # what TrainerBattle.start does with every trainer it loads
sc = k8c && k8c.party.find { |p| p.species == :SCIZOR }
check("K8 with Morwen's Ring (:ch18_kestrel_ring = :give_now): the ring, and his Scizor holds the Scizorite",
      k8c && k8c.items.include?(:MEGARING) && sc && sc.item_id == :SCIZORITE && sc.level == 92, sc ? "#{sc.species} Lv#{sc.level} @#{sc.item_id}" : "no Scizor")

#-------------------------------------------------------------------------------
section("4. A Mega and a Z-move in the same battle")
#-------------------------------------------------------------------------------
$player.party = [mk(:BLISSEY, 100, [:SOFTBOILED, :SEISMICTOSS], :LEFTOVERS), mk(:SNORLAX, 100, [:BODYSLAM, :REST], :LEFTOVERS)]
lucario = lambda { mk(:LUCARIO, 70, [:AURASPHERE, :FLASHCANNON, :EXTREMESPEED, :NASTYPLOT], :LUCARIONITE) }
vap = lambda { mk(:VAPOREON, 70, [:SCALD, :ICEBEAM, :PROTECT, :WISH], :WATERIUMZ) }
n0 = MEGAS.length; z0 = ZS.length
log = run("Mega + Z: one trainer's double (Lucario @Lucarionite, Vaporeon @Waterium Z, MEGARING)", :seed => 5) do
  setBattleRule("double"); setBattleRule("canLose"); setBattleRule("field", :WATER_SURFACE)
  TrainerBattle.start(npc(:LEADER_MARISOL, "Marisol", [lucario.call, vap.call], [:MEGARING]))
end
fm = MEGAS[n0..].select { |x| x[:side] == 1 }
fz = ZS[z0..].select { |x| x[:side] == 1 }
check("the foe used one Mega (Lucario) and one Z-move (Hydro Vortex) in the same battle",
      fm.length == 1 && fm[0][:species] == :LUCARIO && fz.length == 1 && fz[0][:z] == :HYDROVORTEX, "megas #{fm.length}, z #{fz.map { |z| z[:z] }}")
check("both on turn 1 (the Mega first, before moves; the Z-move in the move phase)", fm[0] && fz[0] && fm[0][:turn] == 1 && fz[0][:turn] == 1)

$bag.remove(:ZPOWERRING) while $bag.has?(:ZPOWERRING)
$bag.add(:MEGARING) if !$bag.has?(:MEGARING)
n0 = MEGAS.length; z0 = ZS.length
log = wild("Mega + Z: the player's side with the one ring (Mega Ring only) on Water Surface", [lucario.call, vap.call],
           [mk(:SNORLAX, 70, [:BODYSLAM, :REST], :LEFTOVERS, :IMMUNITY), mk(:CHANSEY, 70, [:SOFTBOILED, :SEISMICTOSS], :EVIOLITE)],
           field: :WATER_SURFACE, double: true, seed: 9)
pmg = MEGAS[n0..].select { |x| x[:side] == 0 }
pz = ZS[z0..].select { |x| x[:side] == 0 }
check("the one ring: with only the Mega Ring the player's side used one Mega and one Z-move in one battle",
      pmg.length == 1 && pz.length == 1 && !$bag.has?(:ZPOWERRING), "megas #{pmg.map { |x| x[:species] }}, z #{pz.map { |x| x[:z] }}")
$bag.remove(:MEGARING)
$bag.add(:ZPOWERRING)
check("save compatibility: an old save's Z-Power Ring alone still wakes crystals (not stones)", PrismfallZ.player_ring? && !pm.ring?)
$bag.remove(:ZPOWERRING)
check("no ring at all: no Z-Power", !PrismfallZ.player_ring?)
$bag.add(:MEGARING)

# Z-crystal distribution (SPINE Rev 23): every type crystal placed once (the Eevium Z is the Octave's), R4 at the Ring
# point, quest / boss / map-event sources, and the teaser before the Ring.
zc = pm::Z_CRYSTALS
zerr = []
type_cr = PrismfallZ::CRYSTALS.keys
zerr << "type crystals not placed: #{(type_cr - zc.keys).inspect}" if !(type_cr - zc.keys).empty?
zc.each do |cr, d|
  zerr << "#{cr}: not a crystal item" if !GameData::Item.exists?(cr) || !PrismfallZ.crystal?(cr)
  t = PrismfallZ::CRYSTALS[cr] || (ex = PrismfallZ::EXCLUSIVE[cr]) && GameData::Move.get(ex[:zmove]).type
  usable = [d[:badges], pm::RING_BADGES].max
  (1..horizon).each do |k|
    n = usable + k
    next if n > 18 || !answers[n]
    zerr << "#{cr} (#{t}) usable at #{usable} answers Warden #{n}" if answers[n].include?(t)
  end
  case d[:how]
  when :quest, :boss
    q = tr.get(d[:source])
    zerr << "#{cr}: #{d[:source]} doesn't reward it" if !q || !((q[:reward] || {})[:items] || []).any? { |i, _n| i == cr }
    gate = q && q[:unlock].to_s.scan(/badges\s*>=\s*(\d+)/).flatten.map(&:to_i).max
    zerr << "#{cr}: #{d[:source]} unlock below #{d[:badges]}" if !gate || gate < d[:badges]
  else
    hit = spec["maps"][d[:map]] && spec["maps"][d[:map]]["events"].find { |e| Array(e["commands"]).join =~ /pf_z_crystal\(:#{cr}\b/ }
    if !hit then zerr << "#{cr}: no pf_z_crystal event on map #{d[:map]}"
    elsif !(hit["condition"].to_s =~ /badges >= (\d+)/ && $1.to_i >= d[:badges]) then zerr << "#{cr}: event gate #{hit['condition']}"
    end
  end
end
check("Z-crystals: all #{type_cr.length} type crystals + #{zc.length - type_cr.length} species crystals placed once, R4 with the Ring, " \
      "sources and gates (#{zc.count { |_c, d| d[:badges] < pm::RING_BADGES }} ring and wait before 13)", zerr.empty?, zerr.first(4).join("; "))
snz = mk(:SNORLAX, 70, [:GIGAIMPACT, :BODYSLAM, :REST, :PROTECT], :SNORLIUMZ)
z0 = ZS.length
wild("Species Z-move: the player's Snorlax with the Snorlium Z", [snz], foe_wall(70))
sz = ZS[z0..].find { |x| x[:side] == 0 }
check("a species crystal: Snorlax's Giga Impact becomes Pulverizing Pancake (its own power)", sz && sz[:z] == :PULVERIZINGPANCAKE,
      sz.inspect[0, 80])

#-------------------------------------------------------------------------------
section("5. One Mega and one Z-move per SIDE (two foe trainers)")
#-------------------------------------------------------------------------------
two_megas = lambda do
  [npc(:LEADER_KAITO, "Kaito", [lucario.call], [:MEGARING]),
   npc(:LEADER_MAGNUS, "Magnus", [mk(:METAGROSS, 70, [:METEORMASH, :ZENHEADBUTT, :BULLETPUNCH, :EARTHQUAKE], :METAGROSSITE)], [:MEGARING])]
end
per_side = lambda do |label, seed|
  $player.party = [mk(:BLISSEY, 100, [:SOFTBOILED, :SEISMICTOSS], :LEFTOVERS), mk(:SNORLAX, 100, [:BODYSLAM, :REST], :LEFTOVERS)]
  n0 = MEGAS.length
  run("Per side (#{label}): two foe trainers, each with a Mega Stone and a Mega Ring", :seed => seed) do
    setBattleRule("canLose"); setBattleRule("field", "none")
    TrainerBattle.start(*two_megas.call)
  end
  MEGAS[n0..].select { |x| x[:side] == 1 }
end
side_megas = per_side.call("LIMIT :side", 3)
check("LIMIT :side - only one of the two foe trainers Mega Evolves in the whole battle", side_megas.length == 1,
      side_megas.map { |x| "#{x[:species]}@owner#{x[:owner]}" }.inspect)
PrismfallMega.send(:remove_const, :LIMIT); PrismfallMega.const_set(:LIMIT, :trainer)
trainer_megas = per_side.call("LIMIT :trainer, Essentials' own rule", 3)
PrismfallMega.send(:remove_const, :LIMIT); PrismfallMega.const_set(:LIMIT, :side)
check("control: with Essentials' per-trainer rule both trainers Mega Evolve", trainer_megas.length == 2,
      trainer_megas.map { |x| "#{x[:species]}@owner#{x[:owner]}" }.inspect)

two_z = lambda do
  [npc(:OCTAVE_SINGER, "Aria", [vap.call]),
   npc(:OCTAVE_SINGER, "Cadence", [mk(:JOLTEON, 70, [:THUNDERBOLT, :SHADOWBALL, :PROTECT, :VOLTSWITCH], :ELECTRIUMZ)])]
end
z_side = lambda do |seed|
  $player.party = [mk(:BLISSEY, 100, [:SOFTBOILED, :SEISMICTOSS], :LEFTOVERS), mk(:SNORLAX, 100, [:BODYSLAM, :REST], :LEFTOVERS)]
  z0 = ZS.length
  run("Per side: two foe trainers, each with a Z-crystal", :seed => seed) do
    setBattleRule("canLose"); setBattleRule("field", "none")
    TrainerBattle.start(*two_z.call)
  end
  ZS[z0..].select { |x| x[:side] == 1 }
end
zs = z_side.call(4)
check("Z_LIMIT :side - one Z-move for the whole foe side", zs.length == 1, zs.map { |z| "#{z[:z]}@owner#{z[:owner]}" }.inspect)
PrismfallMega.send(:remove_const, :Z_LIMIT); PrismfallMega.const_set(:Z_LIMIT, :trainer)
zt = z_side.call(4)
PrismfallMega.send(:remove_const, :Z_LIMIT); PrismfallMega.const_set(:Z_LIMIT, :side)
check("control: with Z-Power's own per-trainer rule each trainer unleashes one", zt.length == 2, zt.map { |z| z[:z] }.inspect)

$player.party = [mk(:BLISSEY, 100, [:SOFTBOILED, :SEISMICTOSS], :LEFTOVERS), mk(:SNORLAX, 100, [:BODYSLAM, :REST], :LEFTOVERS)]
n0 = MEGAS.length; z0 = ZS.length
run("Per side: one foe trainer's Mega and the other's Z-move are both allowed", :seed => 6) do
  setBattleRule("canLose"); setBattleRule("field", "none")
  TrainerBattle.start(npc(:LEADER_KAITO, "Kaito", [lucario.call], [:MEGARING]), npc(:OCTAVE_SINGER, "Aria", [vap.call]))
end
check("a side gets one Mega AND one Z-move (different trainers)", MEGAS[n0..].count { |x| x[:side] == 1 } == 1 &&
      ZS[z0..].count { |x| x[:side] == 1 } == 1)

#-------------------------------------------------------------------------------
section("6. Rules: the Ring, wild Pokemon, Z-crystals")
#-------------------------------------------------------------------------------
$bag.remove(:MEGARING)
n0 = MEGAS.length
wild("No Mega Ring: the player's Lucario with its stone", [lucario.call], foe_wall)
check("without the Mega Ring the player's side never Mega Evolves", MEGAS[n0..].none? { |x| x[:side] == 0 })
$bag.add(:MEGARING)
n0 = MEGAS.length
wild("A wild Lucario holding a Lucarionite", [mk(:SNORLAX, 70, [:BODYSLAM], :LEFTOVERS)], lucario.call)
check("wild Pokemon never Mega Evolve", MEGAS[n0..].none? { |x| x[:side] == 1 })
ray = lambda { |item| mk(:RAYQUAZA, 70, [:DRAGONASCENT, :EXTREMESPEED, :EARTHQUAKE, :DRAGONDANCE], item) }
n0 = MEGAS.length
wild("Rayquaza (Dragon Ascent) holding a Waterium Z", [ray.call(:WATERIUMZ)], foe_wall)
check("a Pokemon holding a Z-crystal can't Mega Evolve (Rayquaza)", MEGAS[n0..].none? { |x| x[:side] == 0 })
n0 = MEGAS.length
wild("Rayquaza (Dragon Ascent) holding Leftovers", [ray.call(:LEFTOVERS)], foe_wall)
check("control: Rayquaza with Dragon Ascent and no crystal Mega Evolves", MEGAS[n0..].any? { |x| x[:side] == 0 && x[:species] == :RAYQUAZA })

#-------------------------------------------------------------------------------
section("7. Mega showpieces on fields, the new ability's entry rules, Field Notes")
#-------------------------------------------------------------------------------
field_case = lambda do |field, mon, stage: nil, start: nil|
  FIELD_START[field] = start if start
  n0 = MEGAS.length
  log = wild("Field #{field}: Mega #{mon.speciesName}", [mon], foe_wall, field: field, stage: stage)
  [MEGAS[n0..].find { |x| x[:side] == 0 } || {}, log]
end
m, log = field_case.call(:GRAND_STAGE, mk(:KANGASKHAN, 60, [:FAKEOUT, :RETURN, :SUCKERPUNCH, :EARTHQUAKE], :KANGASKHANITE))
check("Grand Stage: the applause rises a stage (1 -> 2) on the Mega", m[:stage] == 2 && log.include?(/gasps at the costume change/), m[:stage].inspect)
m, log = field_case.call(:FROZEN_LAKE, mk(:GLALIE, 60, [:FREEZEDRY, :CRUNCH, :EARTHQUAKE, :PROTECT], :GLALITITE),
                         start: proc { |b| idx = FieldEffects.transitions(b).index { |r| r[:id] == :crack }; FieldEffects.raw_state(b)[:counters][idx] = 2 })
check("Frozen Lake: an Ice-type Mega seals every crack (crack meter 2 -> 0)", m[:crack] && m[:crack][0] == 0 && log.include?(/sealed every crack/), m[:crack].inspect)
m, log = field_case.call(:CRYSTAL_CAVERN, mk(:VENUSAUR, 60, [:GIGADRAIN, :SLUDGEBOMB, :EARTHQUAKE, :SYNTHESIS], :VENUSAURITE),
                         start: proc { |b| FieldEffects.state(b)[:cc_hue] = 0 })
check("Crystal Cavern: the crystals take a Grass Mega's colour (hue Fire -> Grass)", m[:hue] == 2 && log.include?(/blaze vivid green/), m[:hue].inspect)
m, log = field_case.call(:HOLLOW_CATHEDRAL, mk(:GENGAR, 60, [:SHADOWBALL, :SLUDGEBOMB, :FOCUSBLAST, :PROTECT], :GENGARITE), stage: 2)
check("Hollow Cathedral: a Ghost-type Mega re-haunts a consecrated nave (stage 2 -> 1)", m[:stage] == 1 && log.include?(/haunted again/), m[:stage].inspect)
m, log = field_case.call(:FACTORY, mk(:METAGROSS, 60, [:METEORMASH, :ZENHEADBUTT, :BULLETPUNCH, :EARTHQUAKE], :METAGROSSITE))
check("Factory: a Steel-type Mega's plating is hammered home (+1 Defense)", m[:stages] && m[:stages][:DEFENSE] == 1 && log.include?(/hammered/))
o0 = OVERLAYS.length
m, log = field_case.call(:BLEED, mk(:AMPHAROS, 60, [:THUNDERBOLT, :DRAGONPULSE, :FOCUSBLAST, :COTTONGUARD], :AMPHAROSITE))
check("Bleed: the Mega makes the Bleed lurch to new borrowed effects at once", log.include?(/tore at the Bleed/) && OVERLAYS.length - o0 >= 2,
      "#{OVERLAYS.length - o0} overlay changes")
m, log = field_case.call(:COLOSSEUM, mk(:PIDGEOT, 60, [:HURRICANE, :HEATWAVE, :ROOST, :UTURN], :PIDGEOTITE, :KEENEYE))
check("Colosseum: the Mega's new No Guard triggers the field's entry rule (+1 Attack), and the crowd roars",
      m[:old_ability] == :KEENEYE && m[:ability] == :NOGUARD && m[:stages][:ATTACK] == 1 && log.include?(/crowd roars/))
m, log = field_case.call(:INVERSE, mk(:ABSOL, 60, [:KNOCKOFF, :PLAYROUGH, :SUCKERPUNCH, :SWORDSDANCE], :ABSOLITE, :PRESSURE))
check("Inverse: the Mega's new Magic Bounce triggers the field's entry rule (+1 Sp. Def)", m[:ability] == :MAGICBOUNCE && m[:stages][:SPECIAL_DEFENSE] == 1)
m, log = field_case.call(:INVERSE, mk(:ABSOL, 60, [:KNOCKOFF, :PLAYROUGH, :SUCKERPUNCH, :SWORDSDANCE], :ABSOLITE, :MAGICBOUNCE))
check("...but not twice: an Absol that already had Magic Bounce got the rule on entry only", m[:stages][:SPECIAL_DEFENSE] == 1, m[:stages].inspect)
notes = PrismfallMega::FIELD_RULES.keys.map { |f| [f, FieldEffects::FieldNotes.effect_lines(f).any? { |l| l.start_with?("Mega Evolution:") }] }
check("Field Notes show the Mega line for all #{notes.length} showpiece fields", notes.all? { |_f, ok| ok }, notes.reject { |_f, ok| ok }.inspect)
check("Field Notes add the new-ability line where a Mega ability has an entry rule (Inverse, Colosseum, Frozen Lake...)",
      [:INVERSE, :COLOSSEUM, :FROZEN_LAKE, :SCRAPYARD].all? { |f| FieldEffects::FieldNotes.effect_lines(f).include?(PrismfallMega::GENERAL_NOTE) } &&
      !FieldEffects::FieldNotes.effect_lines(:DESERT).include?(PrismfallMega::GENERAL_NOTE))

#-------------------------------------------------------------------------------
section("8. The quests: a teaser before the Ring, the Ring-Day, a boss stone, the brazier writ")
#-------------------------------------------------------------------------------
$bag.remove(:MEGARING)
$bag.remove(:AMPHAROSITE) if $bag.has?(:AMPHAROSITE)
set_badges(2)
check("The Humming Lamp is locked at 2 badges", tr.state(:EL_LAMP_LENS) == :locked)
set_badges(3)
t0 = TRANSCRIPT.length
scene(:EL_LAMP_LENS, :offer, ["Look."])
check("at 3 badges Hesper gives the Ampharosite, and it hums (no ring yet)", $bag.has?(:AMPHAROSITE) && tr.done?(:EL_LAMP_LENS) &&
      TRANSCRIPT[t0..].any? { |l| l.include?("hums faintly") })
got = pf_mega_stone(:STEELIXITE)
check("a world stone (pf_mega_stone) is received once; a second call gives nothing", got && $bag.has?(:STEELIXITE) && !pf_mega_stone(:STEELIXITE))
t0 = TRANSCRIPT.length
got = pf_z_crystal(:ICIUMZ)
check("a world Z-crystal (pf_z_crystal) before the Ring: received once, with its own teaser", got && $bag.has?(:ICIUMZ) &&
      !pf_z_crystal(:ICIUMZ) && TRANSCRIPT[t0..].any? { |l| l.include?("rings very faintly") })
set_badges(12)
check("the Ring-Day is locked before Gym 13", tr.state(:OS_RING_DAY) == :locked)
set_badges(13)
check("after Gym 13 the Ring-Day is available in Bastian's lamp-room", tr.state(:OS_RING_DAY) == :available && pf_trial_ready?(:BASTIAN_LAMPROOM))
t0 = TRANSCRIPT.length
pf_trial_talk(:BASTIAN_LAMPROOM)
check("Bastian gives the Mega Ring and the Aggronite; the quest finishes quietly", $bag.has?(:MEGARING) && $bag.has?(:AGGRONITE) &&
      tr.done?(:OS_RING_DAY) && TRANSCRIPT[t0..].none? { |l| l.include?("Wall of the Proven") })
lines = TRANSCRIPT[t0..].join("\n")
check("the ring sings, Pip hears it, and the earlier stones stop waiting", lines.include?("sings") && lines.include?("SINGING") &&
      lines.include?("stopped waiting"))
check("no early reveal: Bastian never says 'reset' or names the Legend Plate", lines !~ /reset|Legend Plate/i)
check("Brann's spare (Cameruptite) waits for 15 badges", tr.state(:AS_FORGE_REMEMBERS) == :locked)
set_badges(15)
Prismfall::Choices.make(:ch8_lightstone, :dominar)
t0 = TRANSCRIPT.length
pf_trial_talk(:BRANN_HEARTHGUILD)
lines = TRANSCRIPT[t0..].join("\n")
check("at 15 badges Brann knows his ring, gives the Cameruptite, and is hurt about the Light Stone (it went to the Dominar)",
      $bag.has?(:CAMERUPTITE) && tr.done?(:AS_FORGE_REMEMBERS) && lines.include?("my ring") && lines.include?("Light Stone"))
set_badges(12)
$player.party = [mk(:CHARIZARD, 75, [:FLAMETHROWER, :AIRSLASH, :ROOST, :DRAGONPULSE], :CHARIZARDITEY),
                 mk(:TOGEKISS, 75, [:AIRSLASH, :DAZZLINGGLEAM, :ROOST, :FLAMETHROWER], :LEFTOVERS)]
scene(:EL_OLD_PINCER, :offer, ["I'll go."])
n0 = MEGAS.length
scene(:EL_OLD_PINCER, :fight)
check("the Old Pincer (a 2-bar wild boss on Silkwood) guards the Pinsirite; beating it pays out",
      $bag.has?(:PINSIRITE) && tr.done?(:EL_OLD_PINCER), "status #{Prismfall::EventMons.status(:EL_OLD_PINCER).inspect}")
check("the player's Charizard Mega Evolved in the boss fight", MEGAS[n0..].any? { |x| x[:side] == 0 && x[:species] == :CHARIZARD })
set_badges(15)
tr.add_points(:ASHKAAR, 10, false)
scene(:AS_BRAZIER_WRIT, :offer, ["For the glory of Ashkaar."])
check("The Brazier Writ: a lie at the brazier burns the writ (no stone, quest still open)", !$bag.has?(:SALAMENCITE) && tr.active?(:AS_BRAZIER_WRIT))
scene(:AS_BRAZIER_WRIT, :offer, ["I don't know yet."])
check("...the truth earns the Salamencite", $bag.has?(:SALAMENCITE) && tr.done?(:AS_BRAZIER_WRIT))

#-------------------------------------------------------------------------------
section("9. Trainer speech when a trainer's Z-move or Mega fires (Z-Power 005, data: PrismfallSpeech::LINES)")
#-------------------------------------------------------------------------------
SPEECH = []
EventHandlers.add(:prismfall_trainer_speech, :mega_test_speech,
  proc { |battle, b, event, lines| SPEECH << { :idx => b.index, :event => event, :lines => lines, :turn => battle.turnCount + 1,
                                               :owner => battle.opponent[battle.pbGetOwnerIndexFromBattlerIndex(b.index)].name } })
set_badges(17)
mimikyu = lambda { mk(:MIMIKYU, 78, [:PLAYROUGH, :SHADOWCLAW, :SHADOWSNEAK, :SWORDSDANCE], :MIMIKIUMZ, :DISGUISE) }
$player.party = [mk(:SNORLAX, 80, [:BODYSLAM, :REST], :LEFTOVERS, :THICKFAT), mk(:CHANSEY, 80, [:SOFTBOILED, :SEISMICTOSS], :EVIOLITE)]
s0 = SPEECH.length; z0 = ZS.length
log = run("Celestine's Mimikyu @ Mimikium Z (Let's Snuggle Forever) on Fairy Tale", :seed => 3) do
  setBattleRule("canLose"); setBattleRule("field", :FAIRY_TALE)
  TrainerBattle.start(npc(:LEADER_CELESTINE, "Celestine", [mimikyu.call], [:MEGARING]))
end
sp = SPEECH[s0..]
cz = ZS[z0..].select { |x| x[:side] == 1 }
text = log.text
i_z = text.index("unleashed its full-force Z-Move")
i_s = text.index("This is the part where it hugs you")
check("Celestine's Mimikyu unleashed Let's Snuggle Forever", cz.length == 1 && cz[0][:z] == :LETSSNUGGLEFOREVER, cz.inspect)
check("...and Celestine said her Z-move line once, right after the unleash (before the move hits)",
      sp.length == 1 && sp[0][:event] == :zmove && sp[0][:owner] == "Celestine" && i_z && i_s && i_s > i_z,
      "speech #{sp.map { |x| [x[:owner], x[:event]] }}, unleash at #{i_z.inspect}, line at #{i_s.inspect}")
check("...in the battle transcript as \"Celestine: This is the part where it hugs you. Hold still. It's worse if you don't.\"",
      text.include?("Celestine: This is the part where it hugs you. Hold still. It's worse if you don't."))
s0 = SPEECH.length; z0 = ZS.length; n0 = MEGAS.length
log = run("No line for a trainer without one: Marisol's Mega Lucario + Hydro Vortex", :seed => 5) do
  setBattleRule("double"); setBattleRule("canLose"); setBattleRule("field", :WATER_SURFACE)
  TrainerBattle.start(npc(:LEADER_MARISOL, "Marisol", [lucario.call, vap.call], [:MEGARING]))
end
check("a trainer with no lines says nothing on her Mega or her Z-move", SPEECH.length == s0 &&
      MEGAS[n0..].any? { |x| x[:side] == 1 } && ZS[z0..].any? { |x| x[:side] == 1 }, "speech #{SPEECH[s0..].inspect}")
mega_line = PrismfallSpeech.line_for(NPCTrainer.new("Celestine", :LEADER_CELESTINE), :mega)
check("Celestine has no Mega line (her one power play is the Z-move, SPINE Rev 23)", mega_line.nil?)

#-------------------------------------------------------------------------------
fails = RESULTS.reject { |r| r[1] }
File.write(File.join(OUT, "transcript.txt"), "LOGIC-TEST OUTPUT (headless harness, real Essentials v21.1 code).\n" + TRANSCRIPT.join("\n") + "\n")
report = ["# Mega Evolution - headless test (tools/harness/run_mega.rb)", "",
          "Real Essentials v21.1 battle code with Prismfall Core, Field Effects, Z-Power, Bosses, Trials and Mega; AI on both",
          "sides unless noted. Logic only: the EBDX animation is checked in the real engine (design/MEGA_EVOLUTION.md section 8).", "",
          "**#{RESULTS.length - fails.length}/#{RESULTS.length} checks passed.**", "", "| | Check | Detail |", "|---|---|---|"]
RESULTS.each { |n, ok, d| report << "| #{ok ? 'PASS' : '**FAIL**'} | #{n.gsub('|', '/')} | #{d.to_s.gsub('|', '/')[0, 200]} |" }
report << "" << "Megas logged: #{MEGAS.length}; Z-moves logged: #{ZS.length}. Battle transcripts: `transcript.txt`."
File.write(File.join(OUT, "REPORT.md"), report.join("\n") + "\n")
puts "#{RESULTS.length - fails.length}/#{RESULTS.length} checks passed. Report: #{OUT}/REPORT.md"
exit(fails.empty? ? 0 : 1)
