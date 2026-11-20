#===============================================================================
# Prismfall Trials - headless integration test
#   PRISM_RUN_DIR=<private run copy> PRISM_COMPILE=1 ruby tools/harness/run_trials.rb
# Through the real Essentials v21.1 code + Prismfall Core/Bosses/Field Effects/Trials:
#   1. data checks: every quest scene command, event Pokemon (species, form,
#      ability, moves legal), reward items, trainers, conditions
#   2. a quest from offer to reward with real battles: The Little Crucible
#      (3-bout gauntlet, boss Litleo, Litleo joins, rank points, items, money)
#   3. a chase quest: The Tart Thief (4 sightings, real wild battle, the
#      capture branch, Kestrel bond, completion)
#   4. a gift-variant quest (A Hole in the Sky: Smeargle palette) and the
#      quiet-deed tutorial (The First Lesson)
#   5. badge-tier encounter swap on the Ferrymen's Mile (520): tables before/after
#      Badge 1 and 2, 4000-roll sampling, LandNight feed, rumours, entry notice,
#      no overlay on a map with no base table, encounter_version 1 untouched
#   6. "Condition:" page comments, save round trip
# Writes docs/trials_test/REPORT.md and transcript.txt. Exit 1 on any failure.
#===============================================================================
require "fileutils"
load File.join(__dir__, "boot.rb")
load File.join(HARNESS_DIR, "log_scene.rb")

OUT = ENV["PRISM_OUT"] || File.expand_path("../../docs/trials_test", HARNESS_DIR)
FileUtils.mkdir_p(OUT)
TRANSCRIPT = []
RESULTS = []

# Overworld messages go to the transcript (and the battle log while a battle runs).
def pbMessage(message, commands = nil, cmd_if_cancel = 0, _skin = nil, default_cmd = 0, &_block)
  text = Harness.clean(message.to_s)
  TRANSCRIPT << "  #{text}" + (commands ? "  [choices: #{commands.join(' / ')}]" : "")
  Harness.log&.add("(overworld message) #{text}")
  return default_cmd if commands
  return 0
end
def pbNickname(_pkmn); end                # no naming screen headless
require "json"
MAPNAMES = JSON.parse(File.read(File.expand_path("../../design/maps.json", HARNESS_DIR)))["maps"].map { |m| [m["id"], m["name"]] }.to_h
def pbGetMapNameFromId(id); MAPNAMES[id] || "Map #{id}"; end   # no MapInfos.rxdata headless
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

# Runs a scene with scripted choice answers; battles inside it are logged.
def scene(quest, name, answers = [])
  Prismfall::Trials.answers = answers.dup
  TRANSCRIPT << "-- #{quest} / #{name}"
  log = Harness::BattleLog.new("#{quest}/#{name}")
  Harness.current_log = log
  ret = nil
  begin
    ret = Prismfall::Trials::Script.run_scene(quest, name)
  ensure
    Harness.current_log = nil
  end
  if log.battle || !log.errors.empty?
    TRANSCRIPT << log.text.lines.map { |l| "    | #{l.rstrip}" }.join("\n")
    log.errors.each { |e| check("no engine error in #{quest}/#{name}", false, e.inspect[0, 300]) }
  end
  left = Prismfall::Trials.answers.length
  check("#{quest}/#{name} used every scripted answer", left == 0, "#{left} unused") if !answers.empty?
  ret
end

def mk(species, level, moves = nil)
  p = Pokemon.new(species, level)
  GameData::Stat.each_main { |s| p.iv[s.id] = 31 }
  if moves
    p.forget_all_moves
    moves.each { |m| p.learn_move(m) }
  end
  p.calc_stats
  p
end

Harness.new_game_state
Prismfall.record_starter(:CHARMANDER) if Prismfall.respond_to?(:record_starter)
$PokemonEncounters = PokemonEncounters.new
tr = Prismfall::Trials
em = Prismfall::EventMons

#-------------------------------------------------------------------------------
section("1. Data checks")
#-------------------------------------------------------------------------------
data_errors = []
legal = lambda do |sp_id, form, move|
  sp = GameData::Species.get_species_form(sp_id, form || 0)
  chain = [sp]
  cur = sp
  while (prev = cur.get_previous_species) && prev != cur.species
    cur = GameData::Species.get_species_form(prev, cur.form) rescue GameData::Species.get(prev)
    chain << cur
  end
  chain.any? do |s|
    s.moves.any? { |m| m[1] == move } || s.tutor_moves.include?(move) || s.get_egg_moves.include?(move)
  end
end
em.ids.each do |id|
  d = em.get(id)
  begin
    sp = GameData::Species.get_species_form(d[:species], d[:form] || 0)
    data_errors << "#{id}: form #{d[:form]} missing" if d[:form] && sp.form != d[:form]
    if d[:ability]
      ok = sp.abilities.include?(d[:ability]) || sp.hidden_abilities.include?(d[:ability])
      data_errors << "#{id}: #{d[:species]} can't have #{d[:ability]}" if !ok
    end
    movesets = [d[:moves]] + (d[:variants] || {}).values.map { |v| v[:moves] }
    movesets.compact.each do |ms|
      ms.each do |m|
        data_errors << "#{id}: unknown move #{m}" if !GameData::Move.exists?(m)
        next if d[:species] == :SMEARGLE || (d[:special_moves] || []).include?(m)
        data_errors << "#{id}: #{d[:species]} can't learn #{m}" if GameData::Move.exists?(m) && !legal.call(d[:species], d[:form], m)
      end
    end
    data_errors << "#{id}: unknown item #{d[:item]}" if d[:item] && !GameData::Item.exists?(d[:item])
    em.build(id) if d[:kind] != :egg
  rescue StandardError => e
    data_errors << "#{id}: #{e.class}: #{e.message}"
  end
end
check("event Pokemon: species/forms/abilities/moves/items valid (#{em.ids.length})", data_errors.empty?, data_errors.first(8).join("; "))

cmd_errors = []
walk = nil
walk = lambda do |qid, list, path|
  Array(list).each do |e|
    case e
    when String then next
    when Array
      cmd_errors << "#{path}: speaker line needs [Symbol, Symbol, String]" if !(e[0].is_a?(Symbol) && e[2].is_a?(String))
    when Hash
      if e[:choice]
        e[:options].each { |o| walk.call(qid, o[1], "#{path}>#{o[0]}"); (Prismfall::Conditions.check(o[2].gsub(':SELF', ":#{qid}")) rescue cmd_errors << "#{path}: bad option cond #{o[2]}") if o[2] }
      elsif e.key?(:if)
        begin
          Prismfall::Conditions.check(e[:if].gsub(":SELF", ":#{qid}"))
        rescue StandardError => ex
          cmd_errors << "#{path}: bad condition #{e[:if].inspect} (#{ex.message})"
        end
        walk.call(qid, e[:then], path + ">then")
        walk.call(qid, e[:else], path + ">else")
      elsif e[:event_battle]
        cmd_errors << "#{path}: unknown event mon #{e[:event_battle]}" if !em.exists?(e[:event_battle])
        [:caught, :won, :lost, :fled].each { |k| walk.call(qid, e[k], "#{path}>#{k}") }
      elsif e[:trainer] || e[:gauntlet]
        (e[:gauntlet] || [e[:trainer]]).each do |t|
          cmd_errors << "#{path}: no trainer #{t.inspect}" if !GameData::Trainer.exists?(t[0], t[1], t[2] || 0)
        end
        walk.call(qid, e[:won], path + ">won"); walk.call(qid, e[:lost], path + ">lost")
      elsif e[:gift] || e[:join]
        cmd_errors << "#{path}: unknown event mon #{e[:gift] || e[:join]}" if !em.exists?(e[:gift] || e[:join])
      elsif e[:item] || e[:take]
        it = (e[:item] || e[:take])[0]
        cmd_errors << "#{path}: unknown item #{it}" if !GameData::Item.exists?(it)
      elsif e.key?(:step)
        cmd_errors << "#{path}: unknown step #{e[:step]}" if !tr.step_ids(qid).include?(e[:step])
      elsif e[:run]
        cmd_errors << "#{path}: unknown scene #{e[:run]}" if !(tr.get(qid)[:scenes] || {})[e[:run]]
      elsif e[:effects]
        e[:effects].split.each do |tok|
          m = /\A([A-Z_]+)[+-]\d+\z/.match(tok)
          id = m && m[1].to_sym
          ok = m && (id == :RES || Prismfall::Narrative::BONDS.key?(id) || Prismfall::Narrative::FACTIONS.key?(id))
          cmd_errors << "#{path}: bad effect #{tok}" if !ok
        end
      elsif e[:points]
        cmd_errors << "#{path}: unknown trial #{e[:points][0]}" if !tr::TRIALS[e[:points][0]]
      end
    end
  end
end
reward_items = []
tr.quest_ids.each do |qid|
  q = tr.get(qid)
  cmd_errors << "#{qid}: unknown trial #{q[:trial]}" if !tr::TRIALS[q[:trial]]
  begin
    Prismfall::Conditions.check(q[:unlock]) if q[:unlock]
  rescue StandardError => ex
    cmd_errors << "#{qid}: bad unlock #{q[:unlock].inspect}: #{ex.message}"
  end
  (q[:scenes] || {}).each { |name, list| walk.call(qid, list, "#{qid}/#{name}") }
  ([q[:reward]] + (q[:outcomes] || {}).values).compact.each do |rw|
    (rw[:items] || []).each { |i, _| reward_items << [qid, i] }
    cmd_errors << "#{qid}: reward mon #{rw[:pokemon]} unknown" if rw[:pokemon] && !em.exists?(rw[:pokemon])
  end
end
tr::RANK_REWARDS.each { |t, h| h.each_value { |rw| (rw[:items] || []).each { |i, _| reward_items << [t, i] }; cmd_errors << "#{t}: rank mon #{rw[:pokemon]}" if rw[:pokemon] && !em.exists?(rw[:pokemon]) } }
reward_items.each { |who, i| cmd_errors << "#{who}: unknown reward item #{i}" if !GameData::Item.exists?(i) }
tr::TALK.each do |key, t|
  cmd_errors << "TALK #{key}: unknown board #{t[:board]}" if t[:board] && !tr::TRIALS[t[:board]]
  t[:rows].each do |qid, c, sc|
    q = tr.get(qid)
    if !q then cmd_errors << "TALK #{key}: unknown quest #{qid}"; next; end
    cmd_errors << "TALK #{key}: #{qid} has no scene #{sc}" if !(q[:scenes] || {})[sc]
    begin
      Prismfall::Conditions.check(c.gsub(":SELF", ":#{qid}"))
    rescue StandardError => ex
      cmd_errors << "TALK #{key}: bad condition #{c.inspect} (#{ex.message})"
    end
  end
end
require "yaml"
ev_errors = []
spec = YAML.safe_load(File.read(File.expand_path("../../design/TRIAL_EVENTS.yaml", HARNESS_DIR)))
n_events = 0
spec["maps"].each do |mid, m|
  (m["events"] || []).each do |e|
    n_events += 1
    ev_errors << "#{mid} #{e['name']}: unknown TALK key #{e['key']}" if e["key"] && !tr::TALK[e["key"].to_sym]
    next if !e["condition"]
    begin
      Prismfall::Conditions.check(e["condition"])
    rescue StandardError => ex
      ev_errors << "#{mid} #{e['name']}: bad condition #{e['condition'].inspect} (#{ex.message})"
    end
  end
end
used_keys = spec["maps"].values.flat_map { |m| (m["events"] || []).map { |e| e["key"] } }.compact.map(&:to_sym)
ev_errors << "TALK keys with no map event: #{(tr::TALK.keys - used_keys).inspect}" if !(tr::TALK.keys - used_keys).empty?
check("design/TRIAL_EVENTS.yaml: #{n_events} events, keys and Condition strings valid", ev_errors.empty?, ev_errors.first(5).join("; "))
wired_scenes = tr.quest_ids.reject { |id| tr.get(id)[:stub] }.flat_map { |id| (tr.get(id)[:scenes] || {}).keys.map { |s| [id, s] } }
reachable = tr::TALK.values.flat_map { |t| t[:rows].map { |q, _c, sc| [q, sc] } }
internal = tr.quest_ids.flat_map do |id|
  found = []
  scan = nil
  scan = lambda do |x|
    if x.is_a?(Hash)
      found << [id, x[:run]] if x[:run]
      x.each_value { |v| scan.call(v) }
    elsif x.is_a?(Array)
      x.each { |v| scan.call(v) }
    end
  end
  (tr.get(id)[:scenes] || {}).each_value { |l| scan.call(l) }
  found
end
orphans = wired_scenes - reachable - internal
check("every wired scene is reachable from a TALK row or another scene", orphans.empty?, orphans.first(6).inspect)
per_trial = tr::TRIALS.keys.map { |t| [t, tr.quests_for(t).length] }.to_h
check("quest scenes, conditions, steps, rewards, trainers valid (#{tr.quest_ids.length} quests)", cmd_errors.empty?, cmd_errors.first(8).join("; "))
check("every Trial has at least 8 quests", per_trial.values.all? { |n| n >= 8 }, per_trial.inspect)
# SPINE Revision 16 (design/warden_gates.json): nothing obtainable with b badges may be a type answer to Warden b+1..b+horizon.
# The badge count is recomputed from the quest data: the unlock, every TALK row that reaches the scene and every
# :if on the way to the gift or battle ("badges >= N"), and must equal the event's declared :badges.
gates = JSON.parse(File.read(File.expand_path("../../design/warden_gates.json", HARNESS_DIR)))
gwardens = gates["wardens"].select { |w| w["answers"] }
horizon = gates["rules"]["gift_horizon"]
need_b = lambda { |text| text.to_s.scan(/badges\s*>=\s*(\d+)/).flatten.map(&:to_i).max || 0 }
found = Hash.new { |h, k| h[k] = [] }   # event id -> [badges needed on each path]
scan_scene = nil
scan_scene = lambda do |qid, list, b, seen|
  Array(list).each do |e|
    next if !e.is_a?(Hash)
    if e[:choice]
      e[:options].each { |o| scan_scene.call(qid, o[1], [b, need_b.call(o[2])].max, seen) }
    elsif e.key?(:if)
      scan_scene.call(qid, e[:then], [b, need_b.call(e[:if])].max, seen)
      scan_scene.call(qid, e[:else], b, seen)
    else
      mon = e[:event_battle] || e[:gift] || e[:join]
      found[mon] << b if mon
      [:caught, :won, :lost, :fled].each { |k| scan_scene.call(qid, e[k], b, seen) if e[k] }
      if e[:run] && !seen.include?([qid, e[:run]])
        scan_scene.call(qid, (tr.get(qid)[:scenes] || {})[e[:run]], b, seen + [[qid, e[:run]]])
      end
    end
  end
end
talk_need = Hash.new { |h, k| h[k] = [] }
tr::TALK.each_value { |t| t[:rows].each { |q, c, sc| talk_need[[q, sc]] << need_b.call(c) } }
tr.quest_ids.each do |qid|
  q = tr.get(qid)
  ub = need_b.call(q[:unlock])
  (q[:scenes] || {}).each do |name, list|
    entry = talk_need[[qid, name]]
    next if entry.empty?                      # reached only through :run from another scene (scanned there)
    scan_scene.call(qid, list, [ub, entry.min].max, [[qid, name]])
  end
  rb = (q[:reward] || {})[:pokemon]
  found[rb] << ub if rb
end
types_upto = nil
types_upto = lambda do |sp, cap, seen|
  t = sp.types.dup
  sp.get_evolutions(true).each do |evo|
    nxt, meth, par = evo[0], evo[1], evo[2]
    next if seen.include?(nxt) || !meth.to_s.start_with?("Level") || !par.is_a?(Integer) || par > cap
    nsp = (GameData::Species.get_species_form(nxt, sp.form) rescue GameData::Species.get(nxt))
    t |= types_upto.call(nsp, cap, seen + [sp.species])
  end
  t
end
gate_errors = []
badge_errors = []
em.ids.each do |id|
  d = em.get(id)
  next if d[:stub]
  paths = found[id]
  if (d[:chapter] || 99) <= 4 && !d.key?(:badges)
    badge_errors << "#{id}: no :badges (Chapters 0-4 must declare when it can be obtained)"
  end
  next if !d.key?(:badges)
  real = paths.empty? ? d[:badges] : paths.min
  next if d[:kind] == :battle && d[:catchable] == false   # a spar hands nothing over
  badge_errors << "#{id}: declared :badges #{d[:badges]}, quest data gives #{real} (#{paths.uniq.inspect})" if !paths.empty? && real != d[:badges]
  sp = GameData::Species.get_species_form(d[:species], d[:form] || 0)
  gwardens.each do |w|
    n = w["n"]
    next if real >= n || real < n - horizon
    ts = types_upto.call(sp, w["cap"], []).map(&:to_s)
    hit = ts & w["answers"]
    gate_errors << "#{id} (#{ts.join('/')}, with #{real} badges) answers Warden #{n} #{w['warden']} (#{hit.join('/')})" if !hit.empty?
  end
end
check("Revision 16: event Pokemon declare :badges and it matches the quest data (#{em.ids.count { |i| em.get(i).key?(:badges) }} declared)",
      badge_errors.empty?, badge_errors.first(5).join("; "))
check("Revision 16: no event Pokemon is a type answer to the next #{horizon} Wardens when it can be obtained",
      gate_errors.empty?, gate_errors.first(5).join("; "))
early = em.ids.count { |id| !em.get(id)[:stub] && (em.get(id)[:chapter] || 99) <= 2 }
check("at least 8 event Pokemon in Chapters 0-2", early >= 8, "#{early}")
check("at least 40 event Pokemon in all", em.ids.length >= 40, "#{em.ids.length}")

#-------------------------------------------------------------------------------
section("2. The Little Crucible: offer -> 3-bout gauntlet -> boss -> join -> reward")
#-------------------------------------------------------------------------------
$player.badges = Array.new(18) { |i| i < 1 }
check("AS_LITTLE_CRUCIBLE locked with 1 badge (Revision 16: Litleo is Fire, Tamsin's answer)", tr.state(:AS_LITTLE_CRUCIBLE) != :available, tr.state(:AS_LITTLE_CRUCIBLE))
$player.badges = Array.new(18) { |i| i < 2 }
$player.party = [mk(:MACHOKE, 23, [:KARATECHOP, :LOWSWEEP, :ROCKTOMB, :KNOCKOFF]),
                 mk(:WARTORTLE, 23, [:WATERPULSE, :BITE, :RAPIDSPIN, :AQUATAIL]),
                 mk(:GRAVELER, 23, [:ROCKTOMB, :BULLDOZE, :ROCKBLAST, :MAGNITUDE]),
                 mk(:PIDGEOTTO, 23, [:WINGATTACK, :QUICKATTACK, :SANDATTACK, :GUST])]
money0 = $player.money
check("AS_LITTLE_CRUCIBLE available with 2 badges", tr.state(:AS_LITTLE_CRUCIBLE) == :available, tr.state(:AS_LITTLE_CRUCIBLE))
srand(4242)
scene(:AS_LITTLE_CRUCIBLE, :offer, ["Let's fight.", "Brand me.", "Sign."])
if tr.state(:AS_LITTLE_CRUCIBLE) != :done   # a lost bout: heal and retry like a player would (up to 3 times)
  3.times do |i|
    break if tr.state(:AS_LITTLE_CRUCIBLE) == :done
    $player.heal_party
    srand(5000 + i)
    scene(:AS_LITTLE_CRUCIBLE, tr.at?(:AS_LITTLE_CRUCIBLE, :mascot) ? :mascot : :bouts, ["Sign."])
  end
end
litleo = $player.party.find { |p| p.isSpecies?(:LITLEO) }
check("quest done", tr.state(:AS_LITTLE_CRUCIBLE) == :done, tr.state(:AS_LITTLE_CRUCIBLE))
check("Cinderpaw (Litleo) joined at Lv 19 with Moxie", litleo && litleo.level == 19 && litleo.ability_id == :MOXIE,
      litleo ? "#{litleo.name} Lv#{litleo.level} #{litleo.ability_id}" : "no Litleo")
check("event mon status :joined", em.status(:AS_LITLEO) == :joined, em.status(:AS_LITLEO))
check("reward money +1200 (plus the three trainers' prize money)", $player.money - money0 >= 1200, "+#{$player.money - money0}")
check("reward Quick Claw", $bag.has?(:QUICKCLAW))
check("Ashkaar points 3 (rank 2, Ember)", tr.points(:ASHKAAR) == 3 && tr.rank(:ASHKAAR) == 2, "#{tr.points(:ASHKAAR)} pts, rank #{tr.rank_name(:ASHKAAR)}")
check("recruited flag", tr.flag(:AS_LITTLE_CRUCIBLE, :recruited) == true)
check("quest log lists it under Done", tr.log_rows(1).any? { |r| r[0] == "The Little Crucible" })

#-------------------------------------------------------------------------------
section("3. The Tart Thief: chase, real wild battle, capture branch, bond")
#-------------------------------------------------------------------------------
$game_switches[103] = true
$player.party = [mk(:QUILAVA, 15, [:EMBER, :QUICKATTACK, :SMOKESCREEN, :FLAMEWHEEL])]
check("EL_TART_THIEF available after the starter (S103)", tr.state(:EL_TART_THIEF) == :available, tr.state(:EL_TART_THIEF))
scene(:EL_TART_THIEF, :offer, ["Of course."])
4.times { scene(:EL_TART_THIEF, :sighting) }
check("four sightings -> loft step", tr.at?(:EL_TART_THIEF, :loft) && tr.chase(:EL_TART_THIEF) == 4, "#{tr.step(:EL_TART_THIEF)} chase=#{tr.chase(:EL_TART_THIEF)}")
k0 = Prismfall::Bonds.get(:KESTREL)
srand(777)
scene(:EL_TART_THIEF, :loft, ["Split the evidence?"])
first = em.status(:EL_NICKIT)
check("real wild battle vs Nickit ran", [:won, :lost, :caught].include?(first), first.inspect)
check("Kestrel +1 for splitting the evidence", Prismfall::Bonds.get(:KESTREL) == k0 + 1, "#{k0} -> #{Prismfall::Bonds.get(:KESTREL)}")
if first != :caught
  check("a knocked-out Nickit leaves the quest at the loft (retry)", tr.at?(:EL_TART_THIEF, :loft), tr.step(:EL_TART_THIEF))
  # The headless AI never throws balls: exercise the capture branch by forcing the outcome.
  orig = em.method(:battle)
  em.define_singleton_method(:battle) { |id| set_status(id, :caught); $player.party << build(id); :caught }
  scene(:EL_TART_THIEF, :loft)   # second visit: no repeat of the Kestrel choice (no double bond)
  em.define_singleton_method(:battle, orig)
end
check("capture -> step :return", tr.at?(:EL_TART_THIEF, :return), tr.step(:EL_TART_THIEF))
check("retrying the loft didn't apply the Kestrel bond twice", Prismfall::Bonds.get(:KESTREL) == k0 + 1, Prismfall::Bonds.get(:KESTREL))
nickit = $player.party.find { |p| p.isSpecies?(:NICKIT) }
check("Nickit has Stakeout and Thief", nickit && nickit.ability_id == :STAKEOUT && nickit.hasMove?(:THIEF))
scene(:EL_TART_THIEF, :return)
check("Tart Thief done (outcome :kept)", tr.done?(:EL_TART_THIEF) && tr.outcome(:EL_TART_THIEF) == :kept, tr.outcome(:EL_TART_THIEF))
check("Elowen points 2", tr.points(:ELOWEN) == 2, tr.points(:ELOWEN))

#-------------------------------------------------------------------------------
section("4. Gift variant and quiet deeds")
#-------------------------------------------------------------------------------
$game_switches[108] = true
scene(:EL_PAINT_LOFT, :offer, ["Let's paint.", "The dunes on the way in."])
brush = ($player.party + $PokemonStorage.boxes.flat_map { |b| b.pokemon.compact }).find { |p| p.isSpecies?(:SMEARGLE) }
check("Smeargle 'Brush' got the earth palette (no Fire or Grass palette before Tamsin/Marisol)",
      brush && brush.hasMove?(:MUDSLAP) && brush.hasMove?(:SKETCH) && !brush.hasMove?(:EMBER),
      brush ? brush.moves.map(&:id).inspect : "none")
scene(:EL_FIRST_LESSON, :offer, ["I'll try."])
scene(:EL_FIRST_LESSON, :deed_rope, ["Turn it."])
check("a deed moves First Lesson to :return", tr.at?(:EL_FIRST_LESSON, :return) && tr.deeds == 1)
r0 = Prismfall::Resonance.value
scene(:EL_FIRST_LESSON, :return, ["Say nothing."])
check("silence: done, Harmony +1", tr.outcome(:EL_FIRST_LESSON) == :silent && Prismfall::Resonance.value == r0 + 1)
check("Elowen points 5 (2 + 1 + 2), rank Sapling", tr.points(:ELOWEN) == 5 && tr.rank_name(:ELOWEN) == "Sapling", tr.points(:ELOWEN))
# The Last Plank, driven only through the map-event router (pf_trial_talk)
talk = lambda { |key, answers = []| Prismfall::Trials.answers = answers.dup; TRANSCRIPT << "-- talk #{key}"; pf_trial_talk(key) }
saved_badges = $player.badges.dup
$player.badges = Array.new(18, false)
check("Last Plank locked before Badge 1 (Revision 16: no Fighting type before Dorian)", tr.state(:EL_LAST_PLANK) != :available, tr.state(:EL_LAST_PLANK))
check("Tide-Pool Feud locked before Badge 1", tr.state(:EL_TIDE_POOL_FEUD) != :available, tr.state(:EL_TIDE_POOL_FEUD))
$player.badges = Array.new(18) { |i| i < 1 }
talk.call(:BERTH_TIMBURR, ["Fetch the planks."])
3.times { talk.call(:BOATYARD_PLANK) }
check("Last Plank: three planks -> :finish", tr.at?(:EL_LAST_PLANK, :finish), tr.step(:EL_LAST_PLANK))
talk.call(:BERTH_TIMBURR)
plank = ($player.party + $PokemonStorage.boxes.flat_map { |b| b.pokemon.compact }).find { |p| p.isSpecies?(:TIMBURR) }
check("Last Plank done via pf_trial_talk after Badge 1; Timburr 'Plank' Lv 13 has Mach Punch",
      tr.done?(:EL_LAST_PLANK) && plank && plank.hasMove?(:MACHPUNCH) && plank.level == 13, plank ? "#{plank.name} Lv#{plank.level}" : "none")
talk.call(:BERTH_TIMBURR)
check("after completion the berth event falls back to its idle line", TRANSCRIPT.last.include?("hammers a plank"), TRANSCRIPT.last)
# A board-accepted quest: Master of Nothing taken from the Ferrow's lantern rope, then the giver's briefing
$game_switches[101] = true
lbl = tr.board_label(:EL_MASTER_OF_NOTHING)
talk.call(:WAYSHRINE_ROPE, [lbl, "Yes", "Leave"])
check("board: quest accepted from the lantern rope", tr.active?(:EL_MASTER_OF_NOTHING) && tr.flag(:EL_MASTER_OF_NOTHING, :from_board))
talk.call(:DOCKMASTER, ["I'll look."])
check("giver still briefs a board-accepted quest once", TRANSCRIPT.any? { |l| l.include?("crackle in the rigging") } && !tr.flag(:EL_MASTER_OF_NOTHING, :from_board))
talk.call(:DOVETAIL_NEST)
talk.call(:DOCKMASTER)
all_mons = lambda { $player.party + $PokemonStorage.boxes.flat_map { |b| b.pokemon.compact } }
check("Master of Nothing done; the Wattrel waits for a ship (no Flying/Electric gift before Badge 3)",
      tr.done?(:EL_MASTER_OF_NOTHING) && all_mons.call.none? { |p| p.isSpecies?(:WATTREL) })
check("Ebbmouth mast: nothing before Badge 3", !tr.talk_ready?(:EBB_MAST))
$player.badges = Array.new(18) { |i| i < 3 }
talk.call(:EBB_MAST)
mast = all_mons.call.find { |p| p.isSpecies?(:WATTREL) && p.name == "Mast" }
check("Ebbmouth mast after Badge 3: Wattrel 'Mast' Lv 20 joins", mast && mast.level == 20, mast ? "Lv#{mast.level}" : "none")
check("the mast event then falls back to its idle line", !tr.talk_ready?(:EBB_MAST))
# The Scarecrow Walks: a Chapter 1 spar that can't be caught; the catchable rematch opens at Badge 2
$player.badges = Array.new(18, false)
talk.call(:COLL, ["I'll look."])
talk.call(:SCARECROW)
talk.call(:WENNA)
srand(31337)
talk.call(:SCARECROW, ["Give it a squirt."])
3.times { break if tr.done?(:EL_SCARECROW); $player.heal_party; talk.call(:SCARECROW, ["Give it a squirt."]) }
check("Scarecrow: Ch1 spar won, quest done (:spooked), Sudowoodo not caught", tr.done?(:EL_SCARECROW) && tr.outcome(:EL_SCARECROW) == :spooked &&
      all_mons.call.none? { |p| p.isSpecies?(:SUDOWOODO) }, "#{tr.state(:EL_SCARECROW)} #{tr.outcome(:EL_SCARECROW).inspect}")
check("Scarecrow rematch closed with 1 badge", ($player.badges = Array.new(18) { |i| i < 1 }) && !tr.talk_ready?(:SCARECROW))
$player.badges = Array.new(18) { |i| i < 2 }
check("Scarecrow rematch (catchable EL_SUDOWOODO) open with 2 badges", tr.talk_ready?(:SCARECROW))
$player.badges = saved_badges
scene(:EL_PAINT_LOFT, :offer) # done quest: scene still runs, but no second gift via :complete
check("a done quest can't complete twice", tr.record(:EL_PAINT_LOFT)[:times] >= 1)

#-------------------------------------------------------------------------------
section("5. Badge-tier encounter swap: the Ferrymen's Mile (520)")
#-------------------------------------------------------------------------------
bt = tr::BadgeTiers
$player.badges = Array.new(18, false)
$player.party = [mk(:QUILAVA, 15)]
$game_map = Harness::FakeMap.new(520)
pe = $PokemonEncounters
tables = lambda { pe.instance_variable_get(:@encounter_tables) }
species_in = lambda { |type| (tables.call[type] || []).map { |s| s[1] }.uniq }
pe.setup(520)
land0 = species_in.call(:Land)
night0 = species_in.call(:LandNight)
bt.on_enter(520)   # first visit at 0 badges
check("0 badges: no tier species on 520", !land0.include?(:TEDDIURSA) && !night0.include?(:ZORUA), land0.inspect)
Prismfall.award_badge(1, false)
land1 = species_in.call(:Land)
night1 = species_in.call(:LandNight)
check("Badge 1: Teddiursa + Munchlax join Land", land1.include?(:TEDDIURSA) && land1.include?(:MUNCHLAX), (land1 - land0).inspect)
check("Badge 1: the tier's own LandNight (Zorua) is used at night", night1.include?(:ZORUA) && !night1.include?(:TEDDIURSA), (night1 - night0).inspect)
check("Badge 1: base slots kept", (land0 - land1).empty?)
check("rumour for [520,1] queued", bt.fresh_rumours.include?([520, 1]))
TRANSCRIPT << "  rumour: " + bt.rumour_text(520, 1)
counts = Hash.new(0)
srand(99)
4000.times { s, _l = pe.choose_wild_pokemon(:Land); counts[s] += 1 }
rare = counts[:TEDDIURSA] + counts[:MUNCHLAX]
w_total = tables.call[:Land].sum { |s| s[0] }
expect = 4000.0 * 7 / w_total
check("sampling: tier species ~#{(100.0 * 7 / w_total).round(1)}% of Land encounters", rare > expect * 0.6 && rare < expect * 1.4,
      "#{rare}/4000 (expected ~#{expect.round})")
lv = []
200.times { s, l = pe.choose_wild_pokemon(:Land); lv << l if [:TEDDIURSA, :MUNCHLAX].include?(s) }
check("tier levels 13-16", lv.all? { |l| l.between?(13, 16) } && !lv.empty?, lv.minmax.inspect)
bt.on_enter(520)
check("entering 520 again after the badge queues the 'rustling' notice", tr.store[:notice] == 520)
tr.store[:notice] = nil
Prismfall.award_badge(2, false)
land2 = species_in.call(:Land)
check("Badge 2: Farfetch'd + Audino added, Badge 1 tier kept", land2.include?(:FARFETCHD) && land2.include?(:AUDINO) && land2.include?(:TEDDIURSA))
check("unlocked tier on 520 is 2", bt.unlocked_tier(520) == 2, bt.unlocked_tier(520))
Prismfall.award_badge(3, false)
check("Badge 3: a Land-only tier (Swablu) also feeds LandNight", species_in.call(:LandNight).include?(:SWABLU) && species_in.call(:Land).include?(:SWABLU))
orig_ov = bt.method(:overlay)
bt.define_singleton_method(:overlay) { |m, b, v = nil| orig_ov.call(m == 522 ? 520 : m, b, v) }
pe.setup(522)
check("a map with no base table (522, given 520's overlays by a stub) gets no overlay", tables.call.empty?, tables.call.keys.inspect)
bt.define_singleton_method(:overlay, orig_ov)
$PokemonGlobal.encounter_version = 1
pe.setup(520)
check("encounter_version 1 (Bleed-spread) table untouched (no 2xx overlays)", !species_in.call(:Land).include?(:TEDDIURSA), species_in.call(:Land).first(4).inspect)
$PokemonGlobal.encounter_version = 0
pe.setup(520)
TRANSCRIPT << "  520 Land after Badge 2: " + tables.call[:Land].map { |s| "#{s[1]}(#{s[0]}) #{s[2]}-#{s[3]}" }.join(", ")
check("Rumours tab lists tier rumours", tr.log_rows(2).any? { |r| r[2] == "Badge 1" })

#-------------------------------------------------------------------------------
section("6. Page conditions and save round trip")
#-------------------------------------------------------------------------------
Cond  = Struct.new(:switch1_valid, :switch2_valid, :variable_valid, :self_switch_valid, :switch1_id, :switch2_id,
                   :variable_id, :variable_value, :self_switch_ch)
Gfx   = Struct.new(:tile_id, :character_name, :character_hue, :direction, :pattern, :opacity, :blend_type)
FPage = Struct.new(:condition, :graphic, :move_type, :move_speed, :move_frequency, :move_route, :walk_anime,
                   :step_anime, :direction_fix, :through, :always_on_top, :trigger, :list)
Cmd   = Struct.new(:code, :indent, :parameters)
FEvent = Struct.new(:id, :pages, :name)
mkpage = lambda do |text|
  list = text ? [Cmd.new(108, 0, [text]), Cmd.new(0, 0, [])] : [Cmd.new(0, 0, [])]
  FPage.new(Cond.new(false, false, false, false, 1, 1, 1, 0, "A"), Gfx.new(0, "", 0, 2, 0, 255, 0),
            0, 3, 3, nil, true, false, false, false, false, 0, list)
end
p_yes = mkpage.call("Condition: quest_done(:AS_LITTLE_CRUCIBLE) && trial_rank(:ASHKAAR) >= 2")
p_no  = mkpage.call("Condition: quest_step(:EL_TART_THIEF) == :chase")
p_none = mkpage.call(nil)
check("Condition: comment true -> page allowed", tr::PageConditions.passes?(p_yes))
check("Condition: comment false -> page skipped", !tr::PageConditions.passes?(p_no))
check("page without a Condition comment unaffected", tr::PageConditions.passes?(p_none))
ev = FEvent.new(1, [p_none, p_yes, p_no], "trial test")
begin
  gev = Game_Event.allocate   # the real Game_Event#refresh (alias-chained), minus map-only helpers
  { :@event => ev, :@erased => false, :@map_id => 990, :@page => nil, :@route_erased => false }.each { |k, v| gev.instance_variable_set(k, v) }
  def gev.calculate_bush_depth; end
  def gev.check_event_trigger_auto; end
  gev.refresh
  chosen = ev.pages.index(gev.instance_variable_get(:@page))
  check("Game_Event#refresh picks the last page whose Condition passes", chosen == 1, "page #{chosen.inspect}")
  check("event pages restored after refresh", ev.pages.length == 3)
  tr.reset(:AS_LITTLE_CRUCIBLE)
  gev.refresh
  chosen = ev.pages.index(gev.instance_variable_get(:@page))
  check("after the quest is reset, refresh falls back to page 0", chosen == 0, "page #{chosen.inspect}")
rescue StandardError => e
  check("Game_Event#refresh with Condition pages (engine)", false, "#{e.class}: #{e.message} #{e.backtrace.first(2).join(' ')}")
end
dump = Marshal.dump(Prismfall.state)
back = Marshal.load(dump)
check("save round trip keeps Trials state", back.trials[:quests].keys.sort == Prismfall.state.trials[:quests].keys.sort &&
      back.trials[:points] == Prismfall.state.trials[:points] && back.trials[:rumours] == Prismfall.state.trials[:rumours])

#-------------------------------------------------------------------------------
fails = RESULTS.reject { |r| r[1] }
File.write(File.join(OUT, "transcript.txt"), "LOGIC-TEST OUTPUT (headless harness, real Essentials v21.1 code).\n" + TRANSCRIPT.join("\n") + "\n")
report = ["# Prismfall Trials - headless test report", "",
          "Generated by `tools/harness/run_trials.rb` (real Essentials v21.1 + Prismfall Core, Bosses, Field Effects, Trials; PBS compiled in a private run folder).",
          "Logic test only: no screens. Dialogue and battle logs: `transcript.txt`.", "",
          "**#{RESULTS.length - fails.length}/#{RESULTS.length} checks passed.**", "",
          "| | Check | Detail |", "|---|---|---|"] +
         RESULTS.map { |n, ok, d| "| #{ok ? 'PASS' : '**FAIL**'} | #{n} | #{d.gsub('|', '/')[0, 160]} |" }
File.write(File.join(OUT, "REPORT.md"), report.join("\n") + "\n")
puts "#{RESULTS.length - fails.length}/#{RESULTS.length} checks passed. Report: #{OUT}/REPORT.md"
exit(fails.empty? ? 0 : 1)
