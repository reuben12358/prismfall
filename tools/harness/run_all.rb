#===============================================================================
# Prismfall headless battle integration run.
#   ruby tools/harness/run_all.rb            (from the kit folder)
# Runs, through the real Essentials v21.1 battle code with the Prismfall plugins:
#   * one full AI-vs-AI battle on each of the 31 fields
#   * scripted probes per field (boosted move, every transition, seeds, end-of-round)
#   * multi-bar boss fights and a PRISM_ARENA rotation battle
# Writes logs + summary to docs/battle_captures/. Logic test only - no visuals.
#===============================================================================
require "json"
require "fileutils"
load File.join(__dir__, "boot.rb")
load File.join(HARNESS_DIR, "log_scene.rb")
load File.join(HARNESS_DIR, "probes.rb")

OUT_DIR = ENV["PRISM_OUT"] || File.expand_path("../../docs/battle_captures", HARNESS_DIR)
FileUtils.mkdir_p(File.join(OUT_DIR, "logs"))
FileUtils.mkdir_p(File.join(OUT_DIR, "probes"))
ONLY = ENV["PRISM_ONLY"]&.split(",")&.map { |s| s.strip.upcase.to_sym }

module Harness
  # Challenger teams: plain, type-diverse, attacking movesets, perfect IVs, no EVs, no items
  # (except the field's seed on the lead). One tier per stretch of the level curve.
  PARTY_TIERS = [
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

  def self.challenger_party(level, seed_item = nil)
    team = PARTY_TIERS.find { |cap, _| level <= cap }[1]
    party = team.map do |species, moves|
      p = Pokemon.new(species, level)
      GameData::Stat.each_main { |s| p.iv[s.id] = 31 }
      p.nature = :HARDY
      p.forget_all_moves
      moves.each { |m| p.learn_move(GameData::Move.get(m).id) }
      p.calc_stats
      p
    end
    party[0].item = seed_item if seed_item
    party
  end

  def self.set_badges(count)
    $player.badges = Array.new([$player.badges.length, 18].max) { |i| i < count }
  end

  def self.field_seed(field)
    Array(FieldEffects.get(field)[:seed]).compact.first&.[](:item)
  end

  # Every message string a field definition can show, as regexps.
  def self.field_message_patterns(field)
    found = []
    walk = lambda do |obj, key|
      case obj
      when Hash
        obj.each do |k, v|
          if [:type_messages, :move_messages].include?(k) && v.is_a?(Hash)
            v.each_value { |s| found << s if s.is_a?(String) }
          else
            walk.call(v, k)
          end
        end
      when Array then obj.each { |v| walk.call(v, key) }
      when String
        found << obj if [:message, :progress_message, :block_message, :intro_message].include?(key)
      end
    end
    ids = [field] + Array(FieldEffects.get(field)[:transitions]).map { |t| t[:to] }.select { |t| t.is_a?(Symbol) }
    ids.uniq.each { |id| d = FieldEffects.get(id); walk.call(d, nil) if d }
    found.uniq.reject(&:empty?).map { |s| [s, Harness.message_regexp(s)] }
  end

  def self.message_regexp(str)
    Regexp.new(Regexp.escape(str).gsub(/\\\{\d\\\}/, ".+"))
  end

  def self.observed_field_messages(log, field)
    field_message_patterns(field).select { |_s, re| log.lines.any? { |l| l =~ re } }.map(&:first)
  end

  def self.write_log(subdir, name, log)
    path = File.join(OUT_DIR, subdir, "#{name}.txt")
    banner = "LOGIC-TEST OUTPUT (headless harness, real Essentials v21.1 battle code + Prismfall plugins).\n" \
             "Not a game screenshot: no EBDX visuals were rendered.\n\n"
    File.write(path, banner + log.text)
    path
  end
end

Harness.new_game_state
Prismfall.record_starter(:CHARMANDER)   # the rival-starter system needs a recorded starter
RESULTS = { :boot => { :engine_scripts => Harness::BOOT[:scripts].size, :plugins => PluginManager.plugins,
                       :species => GameData::Species.count, :moves => GameData::Move.count,
                       :trainers => GameData::Trainer.count, :fields => FieldEffects.ids.size },
            :battles => [], :probes => {}, :bosses => [], :errors => [] }

def record_errors(kind, name, log)
  log.errors.each { |e| RESULTS[:errors] << e.merge(:kind => kind, :name => name) }
end

#-------------------------------------------------------------------------------
# 1. Full battles: every Warden on their signature field, then the other fields.
#-------------------------------------------------------------------------------
FULL_BATTLES = Prismfall::GYMS.map do |g|
  { :field => g[:field], :type => g[:trainer_type], :name => g[:trainer_name], :version => g[:version],
    :gym => g[:index], :badges => g[:index] - 1, :level => g[:cap], :label => "Gym #{g[:index]} Warden #{g[:trainer_name]}" }
end
# Fields with no gym: story/Festival trainers from pbs/trainers.txt, challenger at the foe's top level.
OTHER_FIELD_TRAINERS = {
  :UNDERWATER => [:FISHERMAN, nil], :INVERSE => [:ECHO_MORWEN, nil], :ASHEN_WASTE => [:HIKER, nil],
  :BLEED => [:HOLLOW_THISTLE, nil], :MOUNTAIN => [:BLACKBELT, nil], :BEACH => [:PICNICKER, nil],
  :PRISM_ARENA => [:CHAMPION_VALEN, nil], :DARK_CRYSTAL => [:HOLLOW_TEO, nil], :SCRAPYARD => [:MERIDIAN_KROLL, nil],
  :CAVE => [:CAMPER, nil], :SNOWY_MOUNTAIN => [:FESTIVAL_SHELLY, nil], :RAINBOW => [:FESTIVAL_AMARIA, nil],
  :WASTELAND => [:MERIDIAN_VOSS, nil]
}.freeze
(FieldEffects.ids - FULL_BATTLES.map { |b| b[:field] }).each do |field|
  ttype, = OTHER_FIELD_TRAINERS[field] || [:HIKER, nil]
  tr = nil
  GameData::Trainer.each { |t| tr ||= t if t.trainer_type == ttype && t.version < 100 }
  raise "no trainer of type #{ttype} for #{field}" if !tr
  FULL_BATTLES << { :field => field, :type => tr.trainer_type, :name => tr.real_name, :version => tr.version,
                    :badges => nil, :level => tr.pokemon.map { |p| p[:level] }.max,
                    :label => "#{GameData::TrainerType.get(tr.trainer_type).name} #{tr.real_name}" }
end

FULL_BATTLES.each_with_index do |b, i|
  next if ONLY && !ONLY.include?(b[:field])
  field = b[:field]
  if b[:badges]
    Harness.set_badges(b[:badges])
    cap = Prismfall.level_cap
    raise "level cap mismatch for #{b[:label]}: #{cap} vs #{b[:level]}" if cap != b[:level]
  else
    Harness.set_badges(18)
  end
  $player.party = Harness.challenger_party(b[:level], Harness.field_seed(field))
  title = "#{FieldEffects.name_of(field)} [#{field}] - #{b[:label]} vs challenger (Lv.#{b[:level]})"
  log = Harness.run_battle(title, :seed => 1000 + i) do
    if b[:gym]
      Prismfall.gym_battle(b[:gym], :can_lose => true)   # the kit's own event call (sets the field rule)
    else
      setBattleRule("field", field)
      setBattleRule("canLose")
      TrainerBattle.start(b[:type], b[:name], b[:version])
    end
  end
  seen = Harness.observed_field_messages(log, field)
  path = Harness.write_log("logs", format("%02d_%s", i + 1, field.to_s.downcase), log)
  RESULTS[:battles] << { :field => field, :label => b[:label], :level => b[:level], :outcome => log.outcome,
                         :outcome_text => Harness::OUTCOMES[log.outcome] || "CRASHED", :turns => log.turns,
                         :errors => log.errors.size, :field_changes => log.field_changes,
                         :field_messages => seen, :log => path.sub(OUT_DIR + "/", "") }
  record_errors(:battle, title, log)
  puts format("battle %-18s %-11s %3d turns  %2d field msgs  %d errors", field, RESULTS[:battles].last[:outcome_text],
              log.turns, seen.size, log.errors.size)
end

#-------------------------------------------------------------------------------
# 2. Scripted probes per field.
#-------------------------------------------------------------------------------
Harness.set_badges(18)
Prismfall::LevelCap.unlock_finale!   # cap 100, so the Lv.100 probe Pokemon obey
FieldEffects.ids.each do |field|
  next if ONLY && !ONLY.include?(field)
  res = Harness::Probes.run_field(field)
  RESULTS[:probes][field] = res[:summary]
  File.write(File.join(OUT_DIR, "probes", "#{field.to_s.downcase}.txt"), res[:text])
  res[:errors].each { |e| RESULTS[:errors] << e.merge(:kind => :probe, :name => field.to_s) }
  s = res[:summary]
  puts format("probe  %-18s boost:%-5s transitions:%d/%d seeds:%d/%d eor:%d/%d errors:%d", field,
              s[:boost][:ok] ? "ok" : "MISS", s[:transitions].count { |t| t[:ok] }, s[:transitions].size,
              s[:seeds].count { |t| t[:ok] }, s[:seeds].size, s[:eor].count { |t| t[:ok] }, s[:eor].size,
              res[:errors].size)
end

#-------------------------------------------------------------------------------
# 3. Multi-bar bosses and the PRISM_ARENA rotation.
#-------------------------------------------------------------------------------
if !ONLY || ONLY.include?(:BOSSES)
  Harness::Probes.run_bosses.each do |r|
    RESULTS[:bosses] << r[:summary]
    Harness.write_log("logs", r[:file], r[:log])
    record_errors(:boss, r[:summary][:name], r[:log])
    s = r[:summary]
    puts format("boss   %-28s %-11s %3d turns  bars broken:%d  errors:%d", s[:name], s[:outcome_text], s[:turns],
                s[:bar_breaks].size, r[:log].errors.size)
  end
end

File.write(File.join(OUT_DIR, "results.json"), JSON.pretty_generate(RESULTS))
puts "errors: #{RESULTS[:errors].size}"
RESULTS[:errors].uniq { |e| [e[:class], e[:message], e[:backtrace].first] }.first((ENV["PRISM_NERR"] || 6).to_i).each do |e|
  puts "  [#{e[:kind]} #{e[:name]}] #{e[:class]}: #{e[:message]}"
  puts "      " + e[:backtrace].first(9).join("\n      ")
end
