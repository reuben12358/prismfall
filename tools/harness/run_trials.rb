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
#   7. Z-Power (SPINE Rev 19): data, the AI and the player's Fight menu, the ring,
#      once per battle, Protect, wild Pokemon, crystals unlosable, field rules
#   8. the Eevee Octave: all eight singer quests out of gym order, the help order,
#      Carol last, a lost and a won 9-bout gauntlet (fields, Z-moves, no healing),
#      the reward Eevee's Extreme Evoboost on the Grand Stage
#   9. the early side content (116_Quests_Early.rb, Chapters 0-5): every new quest
#      through its TALK rows, badge and story gates, real boss and wild battles
#      (Sandygast, Greavard, Galarian Corsola, Rotom), both Matriarch branches,
#      Shelly's cameo hook, the rank-reward badge gate
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
      cmd_errors << "#{path}: 4th element must be :bubble or an options Hash" if e.length > 3 && !(e[3] == :bubble || e[3].is_a?(Hash))
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
      elsif e[:octave_help]
        cmd_errors << "#{path}: unknown Octave singer #{e[:octave_help]}" if !tr::Octave::SINGERS[e[:octave_help]]
      elsif e[:octave_gauntlet]
        specs = tr::Octave::SINGERS.values.map { |sg| [tr::Octave::GAUNTLET_TYPE, sg[:name], tr::Octave::GAUNTLET_VERSION] } + [tr::Octave::HOST]
        specs.each { |t| cmd_errors << "#{path}: no gauntlet trainer #{t.inspect}" if !GameData::Trainer.exists?(t[0], t[1], t[2]) }
        walk.call(qid, e[:won], path + ">won"); walk.call(qid, e[:lost], path + ">lost")
      elsif e[:octave_verses]
        e[:octave_verses].each do |sid, entry|
          cmd_errors << "#{path}: unknown Octave singer #{sid}" if !tr::Octave::SINGERS[sid]
          walk.call(qid, [entry], "#{path}>#{sid}")
        end
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
check("a done quest can't complete twice", tr.record(:EL_PAINT_LOFT)[:times] == 1 && !tr.complete(:EL_PAINT_LOFT, nil, false))

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
section("7. Z-Power (plugins/Prismfall Z-Power): data, AI and player use, once per battle, Protect, fields")
#-------------------------------------------------------------------------------
# Logic test: lift the level cap so the over-cap test teams obey (Standard mode makes Pokemon above the cap disobey,
# and a disobedient Pokemon never uses Z-Power). Balance at the real caps is the trainer designer's (BALANCE.md).
cap_override0 = Prismfall.state.level_cap_override
Prismfall.state.level_cap_override = 100
ZLOG = []
EventHandlers.add(:prismfall_zmove_unleashed, :harness_zlog,
  proc { |battle, user, z|
    foe = battle.battlers.find { |b| b && b.opposes?(user.index) && !b.fainted? }
    entry = { :foe => (battle.opponent ? battle.opponent.map(&:name).join("+") : "wild"), :side => user.index & 1,
              :z => z.id, :base => z.prism_base ? z.prism_base.id : nil, :species => user.species, :power => z.power,
              :category => z.category, :field => (battle.respond_to?(:field_effect) ? battle.field_effect : nil),
              :base_pp => z.prism_base ? z.prism_base.pp : nil, :base_total => z.prism_base ? z.prism_base.total_pp : nil }
    if foe && defined?(FieldEffects) && z.damagingMove?
      entry[:z_mult] = FieldEffects.damage_multiplier(battle, user, foe, z, z.pbCalcType(user))
      entry[:base_mult] = FieldEffects.damage_multiplier(battle, user, foe, z.prism_base, z.prism_base.pbCalcType(user)) if z.prism_base
    end
    ZLOG << entry
  })
ZDONE = []
EventHandlers.add(:prismfall_zmove_done, :harness_zdone,
  proc { |_battle, user, z| ZDONE << { :z => z.id, :side => user.index & 1, :stages => user.stages.dup } })
ZCHOSEN = []
EventHandlers.add(:prismfall_zmove_chosen, :harness_zchosen,
  proc { |battle, idx, z|
    ZCHOSEN << { :foe => (battle.opponent ? battle.opponent.map(&:name).join("+") : "wild"), :side => idx & 1, :z => z.id,
                 :turn => battle.turnCount + 1 }
  })
zp = PrismfallZ
zdata_err = []
zp::TYPE_ZMOVES.each_value { |m| zdata_err << "#{m} missing" if !GameData::Move.exists?(m) }
zp::EXCLUSIVE.each_value { |e| zdata_err << "#{e[:zmove]} missing" if !GameData::Move.exists?(e[:zmove]) }
zp.zmove_ids.each do |m|
  next if !GameData::Move.exists?(m)
  d = GameData::Move.get(m)
  zdata_err << "#{m}: no ZMove flag" if !d.has_flag?("ZMove")
  zdata_err << "#{m}: can be protected against" if d.has_flag?("CanProtect")
  zdata_err << "#{m}: class #{d.function_code} missing" if !Object.const_defined?("Battle::Move::#{d.function_code}")
end
zp.all_crystals.each { |i| zdata_err << "#{i} missing/unflagged" if !GameData::Item.exists?(i) || !GameData::Item.get(i).has_flag?("ZCrystal") }
zdata_err << "ZPOWERRING (kept for old saves) not a key item" if !GameData::Item.exists?(:ZPOWERRING) || !GameData::Item.get(:ZPOWERRING).is_key_item?
zdata_err << "the one ring isn't MEGARING" if zp::RING != :MEGARING
check("Z data: #{zp.zmove_ids.length} Z-moves (ZMove flag, no CanProtect, classes), #{zp.all_crystals.length} crystals, the one ring",
      zdata_err.empty?, zdata_err.first(5).join("; "))
pw = [[50, 100], [60, 120], [80, 160], [90, 175], [100, 180], [120, 190], [140, 200]].reject { |b, z| zp.power_for(b) == z }
check("Gen 7 power table (50->100, 80->160, 90->175, 120->190, 140->200)", pw.empty?, pw.inspect)

wild_z = lambda do |title, party, foe, field: nil, seed: 3, setup: nil|
  $player.party = party
  Harness.run_battle(title, :seed => seed, :setup => setup) do
    setBattleRule("field", field) if field
    setBattleRule("canLose"); setBattleRule("cannotRun")
    WildBattle.start(foe)
  end
end
vap = lambda { |moves = [:SCALD, :DIVE]| v = mk(:VAPOREON, 70, moves); v.item = :WATERIUMZ; v }
protector = mk(:SNORLAX, 60, [:PROTECT]); protector.ability = :IMMUNITY

$bag.add(:MEGARING) if !$bag.has?(:MEGARING)   # the one ring (SPINE Rev 23: the Warden's ring wakes crystals)
n0 = ZLOG.length
log = wild_z.call("Z: player's Vaporeon (AI-controlled) with the ring vs a wild Snorlax that only Protects", [vap.call], protector,
                  field: :WATER_SURFACE)
mine = ZLOG[n0..].select { |z| z[:side] == 0 }
TRANSCRIPT << "" << "=== Z-Power battle 1 ===" << log.text
z1 = mine.first || {}
check("AI (controlPlayer) unleashed Hydro Vortex from a Water move with the ring", z1[:z] == :HYDROVORTEX && [:SCALD, :DIVE].include?(z1[:base]),
      mine.map { |z| "#{z[:z]}<-#{z[:base]}" }.inspect)
check("once per battle: one Z-move in a #{log.turns}-turn battle", mine.length == 1 && log.turns >= 2, "#{mine.length} in #{log.turns} turns")
check("Z power from the base move (Scald/Dive 80 -> 160), category from the base", z1[:power] == 160 &&
      z1[:category] == GameData::Move.get(z1[:base] || :SCALD).category, "#{z1[:power]} cat #{z1[:category]}")
check("the base move lost 1 PP for the Z-move", z1[:base_pp] == (z1[:base_total] || 0) - 1, "#{z1[:base_pp]}/#{z1[:base_total]}")
check("Z-move hits through Protect for 1/4 ('couldn't fully protect itself')", log.include?(/couldn't fully protect itself/))
check("Z-Power messages and the Z-move's name in the battle log",
      log.include?(/surrounded itself with its Z-Power/) && log.include?(/full-force Z-Move/) && log.include?(/Hydro Vortex/))
check("field rule 1: Water Surface's Water x1.5 powers Hydro Vortex", (z1[:z_mult] || 0).round(2) == 1.5, z1[:z_mult].inspect)
dive_z = ZLOG[n0..].find { |z| z[:base] == :DIVE }
check("field rule 2: a base-move rule (Water Surface: Dive x1.3) does not follow it into its Z-move",
      dive_z.nil? || (dive_z[:base_mult] > dive_z[:z_mult]), dive_z ? "Dive #{dive_z[:base_mult].round(2)} vs Z #{dive_z[:z_mult].round(2)}" : "(Scald was the base)")
b0 = log.battle && log.battle.battlers[0]
check("crystals can't be knocked off or stolen (unlosableItem?) and stay held",
      b0 && b0.unlosableItem?(:WATERIUMZ) && b0.unlosableItem?(:EEVIUMZ) && !b0.unlosableItem?(:ORANBERRY) && $player.party[0].item_id == :WATERIUMZ)

$bag.remove(:MEGARING)
n0 = ZLOG.length
log = wild_z.call("Z: same battle without the ring", [vap.call], mk(:SNORLAX, 60, [:PROTECT]))
check("without the ring the player's side never uses Z-Power", ZLOG[n0..].none? { |z| z[:side] == 0 } && log.outcome, "#{ZLOG[n0..].length} Z")
$bag.add(:MEGARING)

menus = lambda do |answer|
  proc do |battle|
    battle.controlPlayer = false
    sc = battle.scene
    sc.define_singleton_method(:pbCommandMenu) { |_i, _f| 0 }
    sc.define_singleton_method(:pbFightMenu) { |_i, _m = false, &blk| [0, 1, 2, 3].each { |mi| break if blk.call(mi) } }   # first move; next if refused
    sc.define_singleton_method(:pbDisplayConfirmMessage) do |msg|
      ans = msg.to_s.include?("Z-Power") ? answer : true
      Harness.log&.add("#{Harness.clean(msg)}  [player answers: #{ans ? 'Yes' : 'No'}]")
      ans
    end
  end
end
n0 = ZLOG.length
log = wild_z.call("Z: the player's own Fight menu, answering Yes", [vap.call([:SCALD])], mk(:MAGIKARP, 5), setup: menus.call(true))
check("player's Fight menu: choosing Scald asks 'Unleash ... Z-Power?'; Yes -> Hydro Vortex",
      log.include?(/Unleash Vaporeon's Z-Power\? \(Scald becomes Hydro Vortex\)/) && ZLOG[n0..].count { |z| z[:side] == 0 } == 1)
n0 = ZLOG.length
log = wild_z.call("Z: the player's own Fight menu, answering No", [vap.call([:SCALD])], mk(:MAGIKARP, 5), setup: menus.call(false))
check("answering No uses plain Scald", log.include?(/used Scald!/) && ZLOG[n0..].none? { |z| z[:side] == 0 })
# Each gauntlet singer (v60) against a neutral, slower wall: all eight crystals in battle.
oct = Prismfall::Trials::Octave
per_singer = oct::SINGERS.map do |id, sg|
  wall = mk(:SNORLAX, 100, [:BODYSLAM, :REST]); wall.ability = :IMMUNITY
  $player.party = [wall]
  n0 = ZLOG.length
  c0 = ZCHOSEN.length
  lg = Harness.run_battle("Z: #{sg[:name]} (OCTAVE_SINGER v60) vs a neutral Snorlax", :seed => 40 + id.to_s.length) do
    Prismfall::Trials.trainer_battle([oct::GAUNTLET_TYPE, sg[:name], oct::GAUNTLET_VERSION], field: sg[:field])
  end
  TRANSCRIPT << "" << lg.text
  want = PrismfallZ::TYPE_ZMOVES[GameData::Species.get(sg[:species]).types[0]]
  ch = ZCHOSEN[c0..].find { |z| z[:side] == 1 }
  un = ZLOG[n0..].find { |z| z[:side] == 1 }
  [sg[:name], want, ch && ch[:z] == want && ch[:turn] == 1 && un && un[:z] == want, "#{ch && ch[:z]}@t#{ch && ch[:turn]}"]
end
check("each gauntlet singer's Eeveelution uses its crystal's Z-move on turn 1 against a neutral target (all 8 crystals)",
      per_singer.all? { |r| r[2] }, per_singer.map { |n, w, ok, d| "#{n}:#{ok ? w : "MISSING #{w} (#{d})"}" }.join(", "))
wild_foe = mk(:VAPOREON, 40, [:SCALD]); wild_foe.item = :WATERIUMZ
n0 = ZLOG.length
log = wild_z.call("Z: a wild Pokemon holding a crystal", [mk(:SNORLAX, 60, [:BODYSLAM])], wild_foe)
check("wild Pokemon never use Z-Power", ZLOG[n0..].none? { |z| z[:side] == 1 })

#-------------------------------------------------------------------------------
section("8. The Eevee Octave: eight quests, the help order, the 9-bout gauntlet, the reward")
#-------------------------------------------------------------------------------
oc = tr::Octave
def otalk(key, answers = [])
  Prismfall::Trials.answers = answers.dup
  TRANSCRIPT << "-- talk #{key}"
  log = Harness::BattleLog.new("talk #{key}")
  Harness.current_log = log
  ret = nil
  begin
    ret = pf_trial_talk(key)
  ensure
    Harness.current_log = nil
  end
  if log.battle || !log.errors.empty?
    TRANSCRIPT << log.text.lines.map { |l| "    | #{l.rstrip}" }.join("\n")
    log.errors.each { |e| check("no engine error in talk #{key}", false, e.inspect[0, 300]) }
  end
  left = Prismfall::Trials.answers.length
  check("talk #{key} used every scripted answer", left == 0, "#{left} unused") if !answers.empty?
  [ret, log]
end
NIGHT = [false]
PBDayNight.singleton_class.send(:alias_method, :__harness_isNight?, :isNight?) if !PBDayNight.respond_to?(:__harness_isNight?)
PBDayNight.define_singleton_method(:isNight?) { |*_a| NIGHT[0] }
# A strong Lv 100 test team (a logic test of the chain, not a balance test: see BALANCE.md / REQUESTS.md).
gauntlet_team = lambda do
  [[:SNORLAX, [:BODYSLAM, :HEAVYSLAM, :CRUNCH, :EARTHQUAKE], :LEFTOVERS, [:HP, :ATTACK]],
   [:GARCHOMP, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :FIREFANG], :LIFEORB, [:ATTACK, :SPEED]],
   [:METAGROSS, [:METEORMASH, :ZENHEADBUTT, :EARTHQUAKE, :BULLETPUNCH], :LEFTOVERS, [:HP, :ATTACK]],
   [:TYRANITAR, [:STONEEDGE, :CRUNCH, :EARTHQUAKE, :ICEPUNCH], :LEFTOVERS, [:HP, :ATTACK]],
   [:VOLCARONA, [:FIERYDANCE, :BUGBUZZ, :QUIVERDANCE, :GIGADRAIN], :LEFTOVERS, [:SPECIAL_ATTACK, :SPEED]],
   [:TOGEKISS, [:AIRSLASH, :DAZZLINGGLEAM, :AURASPHERE, :ROOST], :LEFTOVERS, [:HP, :SPECIAL_ATTACK]]].map do |sp, mv, it, evs|
    pk = mk(sp, 100, mv)
    evs.each { |st| pk.ev[st] = 252 }
    pk.item = it; pk.calc_stats; pk
  end
end
$player.party = gauntlet_team.call
$bag.remove(:ZPOWERRING) while $bag.has?(:ZPOWERRING)
[:CR_OCTAVE, *oc::SINGERS.values.map { |sg| sg[:quest] }].each { |q| tr.reset(q) }
oc.reset
$player.badges = Array.new(18) { |i| i < 1 }
otalk(:VESPER_SALTMERE, ["Why me?"])
check("Ch2 Saltmere: Vesper's request starts 'The Eevee Octave' (step :road)", tr.at?(:CR_OCTAVE, :road), tr.state(:CR_OCTAVE))
check("Carol isn't met before Crownhaven: her quest is locked until S155", tr.state(:CR_OCTAVE_NINTH_VERSE) == :locked && !tr.talk_ready?(:OCTAVE_CAROL))
$game_switches[155] = true
otalk(:OCTAVE_CAROL)
check("Carol with 0 of 7 helped: :not_yet lists the missing singers; her petition stays off the board", tr.state(:CR_OCTAVE_NINTH_VERSE) == :locked &&
      TRANSCRIPT.last(14).join("\n").include?("Lento, on the Mirror Mere"))
$game_switches[155] = false
# Lyra (Elowen), gym order says first; done first here.
otalk(:OCTAVE_LYRA, ["I'll come."])
otalk(:MOSS_STONE, ["Sing along."])
check("Lyra: singing along doesn't work (still at the stone)", tr.at?(:EL_OCTAVE_MOSS, :stone))
srand(11)
otalk(:MOSS_STONE, ["Sit down by the stone and say nothing."])
check("Lyra: the quiet answer -> Leafeon -> duel won -> quest done, helped 1st", tr.done?(:EL_OCTAVE_MOSS) && oc.position(:LYRA) == 1,
      "#{tr.state(:EL_OCTAVE_MOSS)} pos #{oc.position(:LYRA)}")
# Out of gym order on purpose: Cadence (Zenith) before Aria (Isenmar), Forte before Sona and Noct.
$player.badges = Array.new(18) { |i| i < 6 }
otalk(:OCTAVE_CADENCE, ["How do we fix it?"])
srand(12)
2.times { otalk(:LATTICE_JUNCTION) }
otalk(:LATTICE_JUNCTION, ["'A Lattice tuning fault.'"])   # the third box -> the duel -> P-3NNY's report
check("Cadence: three junctions -> duel on the Neon Grid -> filed as a fault (Meridian +1)", tr.done?(:ZE_OCTAVE_OFF_BEAT) &&
      tr.outcome(:ZE_OCTAVE_OFF_BEAT) == :fault && oc.position(:CADENCE) == 2, "#{tr.state(:ZE_OCTAVE_OFF_BEAT)} #{tr.outcome(:ZE_OCTAVE_OFF_BEAT)}")
otalk(:OCTAVE_ARIA, ["Let's listen."])
otalk(:EBB_NOTE); otalk(:EBB_NOTE)
check("Aria: two notes heard, still listening", tr.at?(:IS_OCTAVE_DROWNED_NOTE, :listen) && tr.count(:IS_OCTAVE_DROWNED_NOTE, :notes) == 2)
otalk(:EBB_NOTE)
srand(13)
otalk(:MILL_WHEEL)
check("Aria: third note -> the Mill Quay wheel -> Brine reforms -> duel won, helped 3rd", tr.done?(:IS_OCTAVE_DROWNED_NOTE) && oc.position(:ARIA) == 3)
otalk(:OCTAVE_FORTE, ["Why do you want to join the Legion?"])
otalk(:OCTAVE_FORTE, ["I'll stand for you."])
srand(14)
otalk(:CRUCIBLE_LEGATE, ["Tell her who you are, Forte."])
check("Forte: the truth before the Legate -> duel on Volcanic -> Writ, helped 4th", tr.done?(:AS_OCTAVE_TOO_LOUD) && oc.position(:FORTE) == 4)
otalk(:OCTAVE_SONA, ["Yes."])
3.times { otalk(:SUN_DRIFT) }
NIGHT[0] = true
otalk(:OCTAVE_SONA)
check("Sona: at night the noon light can't come (still :noon)", tr.at?(:OS_OCTAVE_NOON_BELL, :noon))
NIGHT[0] = false
srand(15)
otalk(:OCTAVE_SONA)
check("Sona: three drifts, noon -> Noon's jewel lights -> duel won, helped 5th", tr.done?(:OS_OCTAVE_NOON_BELL) && oc.position(:SONA) == 5)
$player.badges = Array.new(18) { |i| i < 11 }
otalk(:OCTAVE_LENTO, ["How?"])
3.times { otalk(:MERE_CRACK) }
check("Lento: three cracks walked backwards -> the reflection lets go -> duel won, helped 6th", tr.done?(:AN_OCTAVE_STILL_WATER) && oc.position(:LENTO) == 6,
      "#{tr.state(:AN_OCTAVE_STILL_WATER)} step #{tr.step(:AN_OCTAVE_STILL_WATER)}")
otalk(:FERRYMAN_MIREFEN, ["I'll watch the lamps."])
NIGHT[0] = true
3.times { otalk(:FERRY_LAMP) }
srand(16)
otalk(:OCTAVE_NOCT, ["Marsh gas. It happens."])
NIGHT[0] = false
check("Noct: three lamps at night -> the lamplighter -> covered for him -> duel won, helped 7th", tr.done?(:NA_OCTAVE_LAMPS_OUT) &&
      tr.outcome(:NA_OCTAVE_LAMPS_OUT) == :covered && oc.position(:NOCT) == 7)
check("Vesper not in the garden yet (7 of 8)", !oc.ready? && !tr.talk_ready?(:VESPER_GARDEN))
$player.badges = Array.new(18) { true }
$game_switches[155] = true
TRANSCRIPT << "-- (Carol's verses follow, in the order helped)"
mark = TRANSCRIPT.length
srand(17)
otalk(:OCTAVE_CAROL)
verses = TRANSCRIPT[mark..].join("\n")
seen = { :LYRA => "Lyra!", :CADENCE => "Cadence kept", :ARIA => "Aria and the river", :FORTE => "Forte's letter",
         :SONA => "Sona said", :LENTO => "Lento's reflection", :NOCT => "Noct doesn't write" }.map { |id, t| [id, verses.index(t)] }
order_ok = seen.all? { |_id, i| i } && seen.map { |_id, i| i } == seen.map { |_id, i| i }.sort
check("Carol tells the seven verses in the order you helped them", order_ok, seen.map { |id, i| "#{id}@#{i}" }.join(" "))
check("Carol last: duel on Fairy Tale won, helped 8th; Vesper's quest moves to :garden", tr.done?(:CR_OCTAVE_NINTH_VERSE) &&
      oc.position(:CAROL) == 8 && tr.at?(:CR_OCTAVE, :garden), "#{tr.state(:CR_OCTAVE_NINTH_VERSE)} #{tr.step(:CR_OCTAVE)}")
expected = [:LYRA, :CADENCE, :ARIA, :FORTE, :SONA, :LENTO, :NOCT, :CAROL]
check("help order recorded: #{oc.order.map { |i| oc::SINGERS[i][:name] }.join(' > ')}", oc.order == expected)
check("Vesper appears in the Glassfall Memorial Garden (condition octave_ready)", oc.ready? && tr.talk_ready?(:VESPER_GARDEN) &&
      Prismfall::Conditions.evaluate("octave_ready"))
# A lost gauntlet: heal, nothing recorded, try again later.
keep = $player.party
$player.party = [mk(:MAGIKARP, 5, [:SPLASH])]
srand(18)
otalk(:VESPER_GARDEN, ["Begin."])
check("losing the gauntlet: quest stays at :garden, party healed, order kept", tr.at?(:CR_OCTAVE, :garden) && $player.party[0].hp == $player.party[0].totalhp &&
      oc.order == expected)
$player.party = keep
$player.heal_party
n0 = ZLOG.length
c0 = ZCHOSEN.length
mark = TRANSCRIPT.length
HP_START = []; HP_END = []
EventHandlers.add(:on_start_battle, :harness_hp, proc { HP_START << $player.party.sum(&:hp) })
EventHandlers.add(:on_end_battle, :harness_hp, proc { |_d, _c| HP_END << $player.party.sum(&:hp) })
srand(19)
_r, glog = otalk(:VESPER_GARDEN, ["Begin."])
EventHandlers.remove(:on_start_battle, :harness_hp)
EventHandlers.remove(:on_end_battle, :harness_hp)
bouts = TRANSCRIPT[mark..].join("\n").scan(/^  Bout (\d) of 9: (\w+) and (\w+)!/)   # overworld lines, not the battle-log copy
check("the gauntlet runs 9 bouts in the order helped, Vesper last",
      bouts.map { |b| b[1] } == expected.map { |i| oc::SINGERS[i][:name] } + ["Vesper"], bouts.map { |b| b[1] }.join(" > "))
fields = glog.text.scan(/^\s*field: (\w+)/).flatten.map(&:to_sym)
want_f = expected.map { |i| f = oc::SINGERS[i][:field]; f.is_a?(Array) ? f[0] : f } + [oc::HOST_FIELD]
check("each bout on its Eeveelution's home field (host: Grand Stage)", fields == want_f, fields.join(", "))
check("Flower Garden bout starts at stage 3", glog.text.include?("field: FLOWER_GARDEN (stage 3)"))
want_z = expected.map { |i| PrismfallZ::TYPE_ZMOVES[GameData::Species.get(oc::SINGERS[i][:species]).types[0]] } + [:EXTREMEEVOBOOST]
chosen = ZCHOSEN[c0..].select { |z| z[:side] == 1 }
first_pick = chosen.group_by { |z| z[:foe] }.map { |foe, zs| [foe, zs.first] }.to_h
names = expected.map { |i| oc::SINGERS[i][:name] } + ["Vesper"]
wrong = names.each_with_index.select { |n, i| first_pick[n] && first_pick[n][:z] != want_z[i] }
check("in the gauntlet each singer who chose Z-Power chose its own crystal's Z-move (#{first_pick.length}/9 did; " \
      "the AI holds it back against an immune target)", wrong.empty? && first_pick.length >= 6,
      names.map { |n| first_pick[n] ? "#{n}:#{first_pick[n][:z]}@t#{first_pick[n][:turn]}" : "#{n}:-" }.join(", "))
foe_z = ZLOG[n0..].select { |z| z[:side] == 1 }
check("Z-moves unleashed by the singers who got to act (#{foe_z.length}/9), each once",
      foe_z.length >= 1 && foe_z.map { |z| z[:foe] }.uniq.length == foe_z.length && (foe_z.map { |z| z[:z] } - want_z).empty?,
      foe_z.map { |z| "#{z[:foe]}:#{z[:z]}" }.join(", "))
carried = (1...HP_START.length).all? { |i| HP_START[i] == HP_END[i - 1] }
check("no healing between bouts: each bout starts with the HP the last one ended with",
      HP_START.length == 9 && carried && HP_START.last < $player.party.sum(&:totalhp), "start HP #{HP_START.inspect} / end #{HP_END.inspect}")
check("gauntlet won: 'The Eevee Octave' done, S177 EEVEE_OCTAVE_DONE on", tr.done?(:CR_OCTAVE) && $game_switches[177], tr.state(:CR_OCTAVE))
eevee = $player.party.find { |p| p.isSpecies?(:EEVEE) } || ($PokemonStorage && $PokemonStorage.boxes.flat_map { |b| b.pokemon.compact }.find { |p| p.isSpecies?(:EEVEE) })
check("reward: an Eevee (Lv 70, Last Resort) + the Eevium Z, and no separate ring (SPINE Rev 23: the Warden's ring wakes it)",
      eevee && eevee.level == 70 && eevee.hasMove?(:LASTRESORT) && $bag.has?(:EEVIUMZ) && !$bag.has?(:ZPOWERRING),
      eevee ? "#{eevee.name} Lv#{eevee.level}" : "no Eevee")
check("Crownhaven points from Carol (4) + the Octave (5)", tr.points(:CROWNHAVEN) >= 9, tr.points(:CROWNHAVEN))
# The reward in use: the player's new Eevee with the Eevium Z on the Grand Stage.
if eevee
  eevee.item = :EEVIUMZ
  n0 = ZLOG.length
  log = wild_z.call("Z: the reward Eevee holding the Eevium Z on the Grand Stage", [eevee], mk(:SNORLAX, 60, [:BODYSLAM]), field: :GRAND_STAGE)
  TRANSCRIPT << "" << "=== Extreme Evoboost ===" << log.text
  ev = ZLOG[n0..].find { |z| z[:side] == 0 }
  dn = ZDONE.reverse.find { |z| z[:side] == 0 && z[:z] == :EXTREMEEVOBOOST }
  st = dn ? dn[:stages] : {}
  check("Eevee + Eevium Z: Last Resort becomes Extreme Evoboost on turn 1 (even with its other moves unused)",
        ev && ev[:z] == :EXTREMEEVOBOOST && ev[:base] == :LASTRESORT && log.include?(/Extreme Evoboost/), ev.inspect)
  check("Extreme Evoboost: +2 Attack, Defense, Sp. Atk, Sp. Def and Speed",
        [:ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED].all? { |s| (st[s] || 0) >= 2 }, st.inspect)
  check("field showpiece: the Z-move lifts the Grand Stage to Encore (stage 2)", log.field_changes.any? { |o, n, sg| n == :GRAND_STAGE && sg == 2 },
        log.field_changes.inspect)
end
# The shipped base project's Generation 9 Pack runs with Settings::CHAMPIONS_MECHANICS = true: Last Resort can't be chosen
# until the user's other moves have been used (found in the real-engine run: Amen never chose Extreme Evoboost). This
# harness's Gen 9 Pack is older (same alias, paldea_pbCanChooseMove?, without the rule), so emulate the rule where the
# pack puts it: above paldea_pbCanChooseMove? and below Z-Power in the alias chain.
class Battle::Battler
  alias __harness_below_z prismfall_z_pbCanChooseMove?
  def prismfall_z_pbCanChooseMove?(move, commandPhase, showMessages = true, specialUsage = false)
    if move.function_code == "FailsIfUserHasUnusedMove" && @moves.any? { |m| m.id != move.id && !@movesUsed.include?(m.id) }
      @battle.pbDisplayPaused(_INTL("This move can't be used!")) if showMessages
      return false
    end
    return __harness_below_z(move, commandPhase, showMessages, specialUsage)
  end
end
champ = lambda do |title, party, setup = nil|
  $player.party = party
  n0 = ZLOG.length
  lg = Harness.run_battle(title, :seed => 61, :setup => setup) { Prismfall::Trials.trainer_battle([:OCTAVE_VESPER, "Vesper", 60], field: :GRAND_STAGE) }
  TRANSCRIPT << "" << lg.text
  [lg, ZLOG[n0..]]
end
lugia = lambda { pk = mk(:LUGIA, 100, [:AEROBLAST, :ROOST]); pk.item = :LEFTOVERS; pk.calc_stats; pk }
lg, zs = champ.call("Champions rule: Vesper's Amen vs a Lv 100 Lugia", [lugia.call])
check("Champions rule (shipped Gen 9 Pack): Amen still opens with Extreme Evoboost although Last Resort is locked",
      zs.any? { |z| z[:side] == 1 && z[:z] == :EXTREMEEVOBOOST && z[:base] == :LASTRESORT }, zs.map { |z| z[:z] }.inspect)
if eevee
  $bag.add(:MEGARING) if !$bag.has?(:MEGARING)   # the one ring (SPINE Rev 23)
  eevee.item = :EEVIUMZ; eevee.heal
  lr = eevee.moves.index { |m| m.id == :LASTRESORT }
  eevee.moves[0], eevee.moves[lr] = eevee.moves[lr], eevee.moves[0] if lr && lr > 0   # Last Resort first in the menu
  lg, zs = champ.call("Champions rule: the player's Eevee, Fight menu, Last Resort -> Yes", [eevee, lugia.call], menus.call(true))
  check("Champions rule: the player may pick a locked Last Resort for its Z-move; Yes -> Extreme Evoboost",
        zs.any? { |z| z[:side] == 0 && z[:z] == :EXTREMEEVOBOOST } && lg.include?(/Last Resort becomes Extreme Evoboost/), zs.map { |z| z[:z] }.inspect)
  eevee.heal
  lg, zs = champ.call("Champions rule: the player's Eevee, Fight menu, Last Resort -> No", [eevee, lugia.call], menus.call(false))
  check("Champions rule: answering No undoes the locked Last Resort ('This move can't be used!')",
        zs.none? { |z| z[:side] == 0 } && lg.include?(/This move can't be used!/) && !lg.include?(/Amen.*used Last Resort|Eevee used Last Resort/), lg.outcome.inspect)
  eevee.heal
end
class Battle::Battler
  alias prismfall_z_pbCanChooseMove? __harness_below_z
end
PBDayNight.define_singleton_method(:isNight?) { |*a| __harness_isNight?(*a) }
Prismfall.state.level_cap_override = cap_override0

#-------------------------------------------------------------------------------
section("9. Early side content, Chapters 0-5 (116_Quests_Early.rb): every new quest through its map events")
#-------------------------------------------------------------------------------
# Driven only through pf_trial_talk (the TALK rows the map events call), with real battles where the quest fights;
# a capture is forced the way section 3 forces it (the headless AI never throws a ball).
NIGHT[0] = false
PBDayNight.define_singleton_method(:isNight?) { |*_a| NIGHT[0] }
all_mons9 = lambda { $player.party + $PokemonStorage.boxes.flat_map { |b| b.pokemon.compact } }
badges9 = lambda { |n| $player.badges = Array.new(18) { |i| i < n } }
force_catch = lambda do |&blk|
  orig = em.method(:battle)
  em.define_singleton_method(:battle) { |id| set_status(id, :caught); $player.party << build(id) if $player.party.length < 6; :caught }
  begin
    blk.call
  ensure
    em.define_singleton_method(:battle, orig)
  end
end
# Like otalk, for a fight that may be lost and retried: answers after a lost battle are simply dropped.
def ftalk(key, answers = [])
  Prismfall::Trials.answers = answers.dup
  TRANSCRIPT << "-- talk #{key}"
  log = Harness::BattleLog.new("talk #{key}")
  Harness.current_log = log
  begin
    pf_trial_talk(key)
  ensure
    Harness.current_log = nil
    Prismfall::Trials.answers = []
  end
  TRANSCRIPT << log.text.lines.map { |l| "    | #{l.rstrip}" }.join("\n") if log.battle || !log.errors.empty?
  log.errors.each { |e| check("no engine error in talk #{key}", false, e.inspect[0, 300]) }
end
retry_fight = lambda do |quest, key, answers, tries = 4|
  tries.times do |i|
    break if !tr.talk_ready?(key) || !tr.active?(quest)
    $player.heal_party
    srand(9000 + i)
    ftalk(key, answers)
  end
end
$player.party = [mk(:QUILAVA, 15, [:EMBER, :QUICKATTACK, :SMOKESCREEN, :FLAMEWHEEL])]

# --- Ch0 -> Ch1: Two Unlisted ----------------------------------------------------
[101, 102].each { |s| $game_switches[s] = false }
badges9.call(0)
check("Two Unlisted is offered on the Dovetail deck (Ch0, before the scan)", tr.state(:EL_STOWAWAYS) == :available && tr.talk_ready?(:CRATE_WOMAN), tr.state(:EL_STOWAWAYS))
$game_switches[102] = true
check("Two Unlisted expires at the dock scan if not taken (S102)", tr.state(:EL_STOWAWAYS) == :expired, tr.state(:EL_STOWAWAYS))
$game_switches[102] = false
otalk(:CRATE_WOMAN, ["Tea services don't squeak."])
check("deck: accepted, step :landed", tr.at?(:EL_STOWAWAYS, :landed), tr.step(:EL_STOWAWAYS))
[101, 102].each { |s| $game_switches[s] = true }
$game_switches[103] = false
check("in town before the starter the woman keeps her own lines (no gift before S103)", !tr.talk_ready?(:CRATE_WOMAN))
$game_switches[103] = true
otalk(:CRATE_WOMAN)
check("after the starter: the crate came open at the gate -> step :find", tr.at?(:EL_STOWAWAYS, :find), tr.step(:EL_STOWAWAYS))
otalk(:STOWAWAY_MICE, ["Scoop them up."])
otalk(:CRATE_WOMAN)
mice = all_mons9.call.find { |p| p.isSpecies?(:TANDEMAUS) }
check("Two Unlisted done: Tandemaus 'Plus-One' Lv 6 with Pickup, 0 badges", tr.done?(:EL_STOWAWAYS) && mice && mice.level == 6 &&
      mice.ability_id == :PICKUP && mice.name == "Plus-One", mice ? "#{mice.name} Lv#{mice.level} #{mice.ability_id}" : "none")

# --- Ch2: The Crown in the Sand (boss Sandygast) ---------------------------------------
$game_switches[108] = false
badges9.call(1)
check("Crown in the Sand locked before the Pageant (S108)", tr.state(:EL_SAND_CROWN) == :locked, tr.state(:EL_SAND_CROWN))
$game_switches[108] = true
badges9.call(0)
check("Crown in the Sand locked with 0 badges", tr.state(:EL_SAND_CROWN) == :locked, tr.state(:EL_SAND_CROWN))
badges9.call(1)
otalk(:SCULPTOR, ["I'll watch it."])
NIGHT[0] = false
otalk(:SAND_CROWN)
check("by day the Crown is only sand (no fight, still :ask)", tr.at?(:EL_SAND_CROWN, :ask) && em.status(:EL_SANDYGAST).nil?, em.status(:EL_SANDYGAST).inspect)
NIGHT[0] = true
$player.party = [mk(:IVYSAUR, 22, [:RAZORLEAF, :TAKEDOWN, :SLEEPPOWDER, :LEECHSEED]),
                 mk(:SNEASEL, 22, [:ICYWIND, :BITE, :QUICKATTACK, :LEER]),
                 mk(:HAUNTER, 22, [:HEX, :NIGHTSHADE, :SUCKERPUNCH, :CONFUSERAY])]
retry_fight.call(:EL_SAND_CROWN, :SAND_CROWN, ["Take it with you."])
crown = all_mons9.call.find { |p| p.isSpecies?(:SANDYGAST) }
check("boss Sandygast (Lv 20, 2 bars on Standard) beaten at night; 'Crown' joins at Lv 16 with Water Compaction",
      crown && crown.level == 16 && crown.ability_id == :WATERCOMPACTION && em.status(:EL_SANDYGAST) == :joined,
      crown ? "#{crown.name} Lv#{crown.level} #{crown.ability_id} #{em.status(:EL_SANDYGAST)}" : "status #{em.status(:EL_SANDYGAST).inspect}")
check("the joined Sandygast has no Grass move (no answer to Marisol, R6)", crown && crown.moves.none? { |m| GameData::Move.get(m.id).type == :GRASS })
otalk(:SCULPTOR)
check("Crown in the Sand done (:took) with TM54 False Swipe", tr.outcome(:EL_SAND_CROWN) == :took && $bag.has?(:TM54), tr.outcome(:EL_SAND_CROWN).inspect)
NIGHT[0] = false

# --- Ch3: The Note Under the Glass (the Matriarch's cocoon, Badge 3) ----------------------------
$game_switches[107] = false
check("Note Under the Glass locked before the Matriarch (S107)", tr.state(:EL_MATRIARCH_HUM) == :locked)
$game_switches[107] = true
check("Mother Aldreth carries the new rows (Matriarch's cocoon, Shelly)",
      [:EL_MATRIARCH_HUM, :EL_SHELLY].all? { |q| tr::TALK[:ALDRETH][:rows].any? { |r| r[0] == q && r[2] == :offer } })
badges9.call(2)
scene(:EL_MATRIARCH_HUM, :offer, ["I'll listen."])
otalk(:GLASS_COCOON)
check("with 2 badges the cocoon only hums (step :wait, no Joltik: Electric answers Marisol)",
      tr.at?(:EL_MATRIARCH_HUM, :wait) && all_mons9.call.none? { |p| p.isSpecies?(:JOLTIK) }, tr.step(:EL_MATRIARCH_HUM))
badges9.call(3)
Prismfall::Choices.clear(:ch2_matriarch)
Prismfall::Choices.make(:ch2_matriarch, :silence, false)
force_catch.call { otalk(:GLASS_COCOON) }
check("silenced Matriarch: the hatchling fights (caught) -> :silenced", tr.outcome(:EL_MATRIARCH_HUM) == :silenced, tr.outcome(:EL_MATRIARCH_HUM).inspect)
tr.reset(:EL_MATRIARCH_HUM)
Prismfall::Trials.store[:event_mons].delete(:EL_JOLTIK)
Prismfall::Choices.clear(:ch2_matriarch)
Prismfall::Choices.make(:ch2_matriarch, :soothe, false)
scene(:EL_MATRIARCH_HUM, :offer, ["I'll listen."])
otalk(:GLASS_COCOON)
jolt = all_mons9.call.select { |p| p.isSpecies?(:JOLTIK) }.last
check("soothed Matriarch: Joltik Lv 22 (Compound Eyes, Electroweb) comes to you with Badge 3 -> :soothed",
      tr.outcome(:EL_MATRIARCH_HUM) == :soothed && jolt && jolt.level == 22 && jolt.ability_id == :COMPOUNDEYES && jolt.hasMove?(:ELECTROWEB),
      "#{tr.outcome(:EL_MATRIARCH_HUM).inspect} #{jolt ? jolt.level : 'none'}")

# --- Ch3: Someone Apologising to Bugs (Shelly's cameo, completed by her fight) -----------------
badges9.call(2)
pts0 = tr.points(:ELOWEN)
scene(:EL_SHELLY, :offer, ["I'll find her."])
check("Shelly's board pointer accepted from Mother Aldreth", tr.active?(:EL_SHELLY))
EventHandlers.trigger(:prismfall_cameo_beaten, :FESTIVAL_SHELLY, true)
check("beating Shelly's cameo completes the quest (no map change needed); Elowen +3",
      tr.done?(:EL_SHELLY) && tr.points(:ELOWEN) == pts0 + 3, "#{tr.state(:EL_SHELLY)} #{pts0}->#{tr.points(:ELOWEN)}")
EventHandlers.trigger(:prismfall_cameo_beaten, :FESTIVAL_SHELLY, false)
check("a second cameo win doesn't complete it twice", tr.record(:EL_SHELLY)[:times] == 1)

# --- Ch4: Bracken Comes In (the Wolfsrime, 579) -------------------------------------------------
badges9.call(1)
check("Bracken locked with 1 badge", tr.state(:EL_DROVERS_BELL) == :locked)
badges9.call(2)
otalk(:DROVER, ["I'll ring it."])
$player.party = [mk(:CROCONAW, 22, [:BITE, :WATERGUN, :SCARYFACE, :ICEFANG])]
srand(2024)
ftalk(:WOLF_DEN)
first9 = em.status(:EL_GREAVARD)
check("the den: a real wild battle vs Greavard 'Bracken' ran", [:won, :lost, :caught].include?(first9), first9.inspect)
if first9 != :caught
  check("a knocked-out Bracken comes back to play (still :ask, den still there)", tr.at?(:EL_DROVERS_BELL, :ask) && tr.talk_ready?(:WOLF_DEN))
  force_catch.call { otalk(:WOLF_DEN) }
end
isen0 = tr.points(:ISENMAR)
otalk(:DROVER)
brk = all_mons9.call.find { |p| p.isSpecies?(:GREAVARD) }
check("Bracken done: Greavard Lv 20 Fluffy with Howl (no Dig before Rook), TM65, Isenmar +1 (joint)",
      tr.done?(:EL_DROVERS_BELL) && brk && brk.ability_id == :FLUFFY && brk.hasMove?(:HOWL) && !brk.hasMove?(:DIG) &&
      $bag.has?(:TM65) && tr.points(:ISENMAR) == isen0 + 1, brk ? "#{brk.name} #{brk.ability_id}" : "none")
check("Wolfsrime (579) badge tiers have their own rumours", tr::BadgeTiers::RUMOURS.key?([579, 3]) && tr::BadgeTiers::RUMOURS.key?([579, 4]))

# --- Ch5: The Names in Holmsby (Ebb Hollow, Bleed) -------------------------------------------
badges9.call(2)
check("Names in Holmsby locked with 2 badges", tr.state(:IS_EBB_HOLLOW) == :locked)
badges9.call(3)
otalk(:VEIL_FISHER, ["I'll go in."])
2.times { otalk(:HOLLOW_STONE) }
check("two stones read -> the coral-covered third (:coral)", tr.at?(:IS_EBB_HOLLOW, :coral), tr.step(:IS_EBB_HOLLOW))
$player.party = [mk(:MIGHTYENA, 26, [:CRUNCH, :BITE, :TAKEDOWN, :HOWL]), mk(:HOUNDOUR, 25, [:BITE, :EMBER, :ROAR, :SMOG])]
retry_fight.call(:IS_EBB_HOLLOW, :HOLLOW_CORAL, [])
check("real wild battle vs Galarian Corsola on :BLEED ran", [:won, :caught].include?(em.status(:IS_CORSOLA)), em.status(:IS_CORSOLA).inspect)
force_catch.call { otalk(:HOLLOW_CORAL) } if tr.at?(:IS_EBB_HOLLOW, :coral)
otalk(:VEIL_FISHER)
check("Names in Holmsby done (Big Pearl, Exp. Candy M)", tr.done?(:IS_EBB_HOLLOW) && $bag.has?(:BIGPEARL))
cor = em.build(:IS_CORSOLA)
check("Holmsby's Corsola is the Galarian form (Ghost) with Cursed Body", cor.form == 1 && cor.types == [:GHOST] && cor.ability_id == :CURSEDBODY,
      "form #{cor.form} #{cor.types.inspect}")

# --- Ch5: The Machine Wants Compliments (Lumen Concourse) ------------------------------------------
$game_variables[125] = 4
otalk(:FIZZBOLT_MACHINE, ["Say something nice.", "Your glass is very clean."])
otalk(:FIZZBOLT_MACHINE, ["Your glass is very clean."])
check("a repeated compliment makes it sulk (no progress)", tr.flag(:ZE_FIZZBOLT, :sulking) == true && tr.count(:ZE_FIZZBOLT, :nice) == 1,
      "nice=#{tr.count(:ZE_FIZZBOLT, :nice)}")
otalk(:FIZZBOLT_MACHINE)
check("next visit it forgives you", tr.flag(:ZE_FIZZBOLT, :sulking) == false)
["You hum in a lovely key.", "Best machine on the Concourse.", "I like your little dent."].each { |c| otalk(:FIZZBOLT_MACHINE, [c]) }
$game_variables[125] = 8
check("the machine is shut during the raid (V125 7-12: nothing new between the Gala and the Interlude)", !tr.talk_ready?(:FIZZBOLT_MACHINE))
$game_variables[125] = 13
otalk(:FIZZBOLT_MACHINE, ["You're brave, standing out here all day."])
check("five different compliments: done, Soda Pop x6 and a Cell Battery", tr.done?(:ZE_FIZZBOLT) && $bag.quantity(:SODAPOP) >= 6 && $bag.has?(:CELLBATTERY))

# --- Ch5: Customer Support (the Spire lobby) ------------------------------------------------------
$game_variables[125] = 4
otalk(:HELPDESK_ROTOM, ["I'll walk it round."])
otalk(:DESK_RECORDS); otalk(:DESK_APPROVALS); otalk(:DESK_COMPLIANCE, ["Window one: Compliance."])
check("the three desks each want another's stamp first (none given)", [:records, :approvals, :compliance].none? { |f| tr.flag(:ZE_CUSTOMER_SUPPORT, f) })
otalk(:DESK_COMPLIANCE, ["Window two: Cancellations of Cancellations."])
otalk(:DESK_APPROVALS); otalk(:DESK_RECORDS)
check("the second window breaks the loop: all three stamps -> :return", tr.at?(:ZE_CUSTOMER_SUPPORT, :return), tr.step(:ZE_CUSTOMER_SUPPORT))
otalk(:HELPDESK_ROTOM)
pory = all_mons9.call.find { |p| p.isSpecies?(:PORYGON) }
check("Customer Support done: Porygon Lv 24 with Download (3 badges)", tr.done?(:ZE_CUSTOMER_SUPPORT) && pory && pory.level == 24 && pory.ability_id == :DOWNLOAD,
      pory ? "Lv#{pory.level} #{pory.ability_id}" : "none")

# --- Ch5: Off the Beat after the Shatter (Cadence on the Concourse) --------------------------------------
saved_ob = tr.record(:ZE_OCTAVE_OFF_BEAT) ? Marshal.load(Marshal.dump(tr.record(:ZE_OCTAVE_OFF_BEAT))) : nil
tr.reset(:ZE_OCTAVE_OFF_BEAT)
$game_switches[114] = true
check("after the Shatter Cadence's row skips the dead junctions", tr.talk_ready?(:OCTAVE_CADENCE) &&
      tr::TALK[:OCTAVE_CADENCE][:rows].first[2] == :after_shatter)
orig_tb = tr.method(:trainer_battle)
tr.define_singleton_method(:trainer_battle) { |*_a, **_k| true }
otalk(:OCTAVE_CADENCE, ["'Source unknown.'"])
tr.define_singleton_method(:trainer_battle, orig_tb)
check("Off the Beat finishes after the Shatter (straight to the duel)", tr.done?(:ZE_OCTAVE_OFF_BEAT), tr.state(:ZE_OCTAVE_OFF_BEAT))
$game_switches[114] = false
tr.store[:quests][:ZE_OCTAVE_OFF_BEAT] = saved_ob if saved_ob

# --- Rank rewards wait for their badges (SPINE Rev 16) --------------------------------------------
badges9.call(2)
tr.store[:points][:ELOWEN] = [tr.points(:ELOWEN), 16].max
tr.store[:ranks_paid][:ELOWEN] = 3
tr.store[:event_mons].delete(:EL_RANK_COMFEY)
tr.pay_rank_rewards(:ELOWEN)
check("Quiet Way rank 4 reached with 2 badges: the Lv 35 Comfey is held back", em.status(:EL_RANK_COMFEY).nil? &&
      tr.store[:ranks_paid][:ELOWEN] == 3, "#{em.status(:EL_RANK_COMFEY).inspect} paid #{tr.store[:ranks_paid][:ELOWEN]}")
badges9.call(8)
tr.pay_rank_rewards(:ELOWEN)
check("with 8 badges the keeper hands the Comfey over", em.status(:EL_RANK_COMFEY) == :gifted, em.status(:EL_RANK_COMFEY).inspect)
rank_gate_errors = []
tr::RANK_REWARDS.each do |t, h|
  h.each do |r, rw|
    next if !rw[:pokemon]
    d = em.get(rw[:pokemon])
    b = rw[:badges] || 0
    rank_gate_errors << "#{t} rank #{r} #{rw[:pokemon]}: no :badges gate" if !rw[:badges]
    sp = GameData::Species.get_species_form(d[:species], d[:form] || 0)
    gwardens.each do |w|
      next if b >= w["n"] || b < w["n"] - horizon
      hit = types_upto.call(sp, w["cap"], []).map(&:to_s) & w["answers"]
      rank_gate_errors << "#{rw[:pokemon]} with #{b} badges answers #{w['warden']} (#{hit.join('/')})" if !hit.empty?
    end
  end
end
check("every rank-reward Pokemon has a badge gate and answers none of the next #{horizon} Wardens at it",
      rank_gate_errors.empty?, rank_gate_errors.first(4).join("; "))
PBDayNight.define_singleton_method(:isNight?) { |*a| __harness_isNight?(*a) }

#-------------------------------------------------------------------------------
fails = RESULTS.reject { |r| r[1] }
File.write(File.join(OUT, "transcript.txt"), "LOGIC-TEST OUTPUT (headless harness, real Essentials v21.1 code).\n" + TRANSCRIPT.join("\n") + "\n")
report = ["# Prismfall Trials - headless test report", "",
          "Generated by `tools/harness/run_trials.rb` (real Essentials v21.1 + Prismfall Core, Bosses, Field Effects, Trials, Z-Power; PBS compiled in a private run folder).",
          "Logic test only: no screens. Dialogue and battle logs: `transcript.txt`.", "",
          "**#{RESULTS.length - fails.length}/#{RESULTS.length} checks passed.**", "",
          "| | Check | Detail |", "|---|---|---|"] +
         RESULTS.map { |n, ok, d| "| #{ok ? 'PASS' : '**FAIL**'} | #{n} | #{d.gsub('|', '/')[0, 160]} |" }
File.write(File.join(OUT, "REPORT.md"), report.join("\n") + "\n")
puts "#{RESULTS.length - fails.length}/#{RESULTS.length} checks passed. Report: #{OUT}/REPORT.md"
exit(fails.empty? ? 0 : 1)
