#!/usr/bin/env ruby
#===============================================================================
# Builds the generated Trials docs from the plugin data (no engine needed):
#   design/TRIALS_QUESTS.md  - every quest per Trial + the full scripted dialogue
#                              of the implemented quests (one source: the plugin)
#   design/EVENT_POKEMON.md  - every event / quest-reward Pokemon
# Usage: ruby tools/trials_docs.rb
# Only the data files are loaded (config, registry, 1xx quests, 13x mons, 140
# rumours) with tiny stubs; nothing from the engine runs.
#===============================================================================
ROOT   = File.expand_path("..", __dir__)
PLUGIN = File.join(ROOT, "plugins", "Prismfall Trials")

def _INTL(s, *args)
  s = s.to_s.dup
  args.each_with_index { |a, i| s.gsub!("{#{i + 1}}", a.to_s) }
  s
end

module Prismfall
  module Trials
    def self.warn(msg); $stderr.puts("warn: #{msg}"); end
    module BadgeTiers; RUMOURS = {}; end
  end
end

["001_Trials_Config.rb", "003_Trials_Registry.rb"].each { |f| load File.join(PLUGIN, f) }
module Prismfall; module Trials; SPEAKERS = {} unless const_defined?(:SPEAKERS); end; end
Dir.children(PLUGIN).sort.select { |f| f =~ /\A1\d\d_.*\.rb\z/ }.each { |f| load File.join(PLUGIN, f) }

TR = Prismfall::Trials
EM = Prismfall::EventMons

def name_of(spk)
  TR::SPEAKERS[spk] || spk.to_s.split("_").map(&:capitalize).join(" ")
end

def mon_label(id)
  d = EM.get(id)
  return id.to_s if !d
  sp = d[:species].to_s.capitalize
  sp = "Galarian #{sp}" if d[:form] == 1 && [:PONYTA, :STUNFISK, :YAMASK].include?(d[:species])
  sp = "Alolan #{sp}" if d[:form] == 1 && d[:species] == :GRIMER
  nick = d[:nickname] ? " \"#{d[:nickname]}\"" : ""
  lv = d[:level].is_a?(Hash) ? (d[:level][:STANDARD] || d[:level][:default]) : d[:level]
  "#{sp}#{nick} Lv #{lv}" + (d[:ability] ? " (#{d[:ability]})" : "")
end

def esc(s)
  s.to_s.gsub("|", "/").gsub("\n", " ")
end

# Renders a scene script as an indented markdown list.
def render(list, depth, out)
  pad = "  " * depth
  Array(list).each do |e|
    case e
    when String then out << "#{pad}- *#{e}*"
    when Array  then out << "#{pad}- **#{name_of(e[0])}** _(#{e[1]})_: #{e[2]}"
    when Hash
      if e[:map]     then out << "#{pad}- [stage] #{e[:map]}"
      elsif e[:note] then out << "#{pad}- [note] #{e[:note]}"
      elsif e[:choice]
        prompt = e[:choice].is_a?(Array) ? "**#{name_of(e[:choice][0])}**: #{e[:choice][2]}" : e[:choice]
        out << "#{pad}- **CHOICE:** #{prompt}"
        e[:options].each do |o|
          out << "#{pad}  - > #{o[0]}" + (o[2] ? " _(only if #{o[2]})_" : "")
          render(o[1], depth + 2, out)
        end
      elsif e.key?(:if)
        out << "#{pad}- [if `#{e[:if]}`]"
        render(e[:then], depth + 1, out)
        if e[:else] && !e[:else].empty?
          out << "#{pad}- [else]"
          render(e[:else], depth + 1, out)
        end
      elsif e[:event_battle]
        out << "#{pad}- [battle] #{mon_label(e[:event_battle])}"
        [:caught, :won, :lost, :fled].each do |k|
          next if !e[k] || e[k].empty?
          out << "#{pad}  - on #{k}:"
          render(e[k], depth + 2, out)
        end
      elsif e[:trainer] || e[:gauntlet]
        list2 = e[:gauntlet] || [e[:trainer]]
        out << "#{pad}- [#{e[:gauntlet] ? 'gauntlet, no healing' : 'trainer battle'}] " +
               list2.map { |t| "#{t[0]} #{t[1]} (v#{t[2] || 0})" }.join(" -> ") + (e[:field] ? " on `:#{e[:field]}`" : "")
        [:won, :lost].each do |k|
          next if !e[k] || e[k].empty?
          out << "#{pad}  - on #{k}:"
          render(e[k], depth + 2, out)
        end
      elsif e[:octave_help]
        out << "#{pad}- [the Octave remembers that you helped #{e[:octave_help].to_s.capitalize}: the gauntlet order]"
      elsif e[:octave_gauntlet]
        out << "#{pad}- [gauntlet, no healing: the eight singers (`OCTAVE_SINGER` v60) in the order you helped them, " \
               "each on their Eeveelution's home field, each using its Z-move -> `OCTAVE_VESPER` Vesper (v60), Eevee with the Eevium Z, on `:GRAND_STAGE`]"
        [:won, :lost].each do |k|
          next if !e[k] || e[k].empty?
          out << "#{pad}  - on #{k}:"
          render(e[k], depth + 2, out)
        end
      elsif e[:octave_verses]
        out << "#{pad}- [for each singer you helped, in that order:]"
        e[:octave_verses].each do |sid, entry|
          out << "#{pad}  - #{sid.to_s.capitalize}:"
          render([entry], depth + 2, out)
        end
      elsif e[:accept]       then out << "#{pad}- [quest accepted]"
      elsif e.key?(:step)    then out << "#{pad}- [quest step: #{e[:step]}]"
      elsif e.key?(:complete) then out << "#{pad}- [quest complete#{e[:complete] == true ? '' : ": #{e[:complete]}"}]"
      elsif e[:fail]         then out << "#{pad}- [quest failed]"
      elsif e[:gift]         then out << "#{pad}- [receive #{mon_label(e[:gift])}#{e[:variant] ? " (#{e[:variant]} palette)" : ''}]"
      elsif e[:join]         then out << "#{pad}- [#{mon_label(e[:join])} joins]"
      elsif e[:item]         then out << "#{pad}- [receive #{e[:item][0]} x#{e[:item][1] || 1}]"
      elsif e[:take]         then out << "#{pad}- [hand over #{e[:take][0]}]"
      elsif e[:money]        then out << "#{pad}- [receive $#{e[:money]}]"
      elsif e[:pay]          then out << "#{pad}- [pay $#{e[:pay]}]"
      elsif e[:effects]      then out << "#{pad}- [effects: #{e[:effects]}]"
      elsif e[:points]       then out << "#{pad}- [#{e[:points][1]} #{TR.trial(e[:points][0])[:name]} points]"
      elsif e[:deed]         then out << "#{pad}- [quiet deed recorded: #{e[:deed]}]"
      elsif e[:chase]        then out << "#{pad}- [chase #{e[:chase]}]"
      elsif e[:run]          then out << "#{pad}- [continue: #{e[:run]}]"
      elsif e[:end]          then out << "#{pad}- [end scene]"
      elsif e.key?(:flag)    then next
      elsif e.key?(:count)   then next
      elsif e[:wait]         then out << "#{pad}- [pause]"
      else out << "#{pad}- [#{e.keys.first}]"
      end
    end
  end
end

def reward_text(rw)
  return "" if !rw
  parts = []
  parts << "$#{rw[:money]}" if rw[:money]
  (rw[:items] || []).each { |i, q| parts << "#{i}#{q && q > 1 ? " x#{q}" : ''}" }
  parts << mon_label(rw[:pokemon]) if rw[:pokemon]
  parts << rw[:effects] if rw[:effects]
  parts.join(", ")
end

def rewards(q)
  s = reward_text(q[:reward])
  (q[:outcomes] || {}).each { |o, rw| s += "; #{o}: #{reward_text(rw)}" }
  s += "; +#{q[:points] || 1} pts" + ((q[:joint] || {}).map { |t, p| " (+#{p} #{TR.trial(t)[:name]})" }.join)
  s.sub(/\A; /, "")
end

#-------------------------------------------------------------------------------
# TRIALS_QUESTS.md
#-------------------------------------------------------------------------------
out = ["# TRIALS_QUESTS — every Trial quest, and the full script of the implemented ones",
       "",
       "> **Generated** by `ruby tools/trials_docs.rb` from `plugins/Prismfall Trials/1xx_*.rb`. Edit the plugin data, not this file.",
       "> Design of the institutions, ranks and boards: `design/TRIALS.md`. Event Pokémon: `design/EVENT_POKEMON.md`.",
       "> Map IDs are current `maps.json` IDs (names change; IDs don't). Chapters and order follow SPINE Revision 14.",
       "> **Status:** *wired* = scenes written and testable (map events in `design/TRIAL_EVENTS.yaml`); *designed* = `:stub`, off the boards until wired.",
       ""]
total = TR.quest_ids.length
wired = TR.quest_ids.count { |id| !TR.get(id)[:stub] }
out << "**#{total} quests** (#{wired} wired, #{total - wired} designed) across #{TR::TRIALS.length} Trials."
out << ""
out << "| Trial | Quests | Wired |"
out << "|---|---|---|"
TR::TRIALS.each_key do |t|
  ids = TR.quests_for(t)
  out << "| #{TR.trial(t)[:name]} (#{TR.trial(t)[:kingdom]}) | #{ids.length} | #{ids.count { |i| !TR.get(i)[:stub] }} |"
end
out << ""
out << "## Part 1. Catalogue"
TR::TRIALS.each do |t, td|
  out << "" << "### #{td[:name]} — #{td[:kingdom]}" << ""
  out << "| Quest | Ch | Unlock | Giver · where (map) | Rank · Rec Lv | What happens | Reward | Touches | Status |"
  out << "|---|---|---|---|---|---|---|---|---|"
  TR.quests_for(t).sort_by { |id| [TR.get(id)[:chapter] || 99, TR.order.index(id)] }.each do |id|
    q = TR.get(id)
    what = q[:summary].to_s
    what += " **Twist:** #{q[:design]}" if q[:design]
    unlock = [q[:unlock], (q[:requires] && !q[:requires].empty?) ? "after #{q[:requires].join(', ')}" : nil].compact.join("; ")
    out << "| **#{q[:title]}** `#{id}` | #{q[:chapter]} | `#{esc(unlock)}` | #{esc(q[:giver])} · #{esc(q[:where])} (#{q[:map]}) | " \
           "#{'★' * (q[:rank] || 1)} · #{q[:rec_level]} | #{esc(what)} | #{esc(rewards(q))} | #{esc(q[:touches])} | #{q[:stub] ? 'designed' : 'wired'} |"
  end
end
out << "" << "## Part 2. Full scripts of the wired quests (Chapters 1–4, and the Eevee Octave across the game)" << ""
out << "Conventions: *italics* = narration box; **Name** _(expression)_ = a line under a portrait bubble (`pf_say`);"
out << "[stage] = what the map event shows (the map builder stages it); [if ...] = a `Prismfall::Conditions` check; `> option` = a choice."
TR::TRIALS.each_key do |t|
  ids = TR.quests_for(t).reject { |id| TR.get(id)[:stub] }
  next if ids.empty?
  out << "" << "### #{TR.trial(t)[:name]}"
  ids.each do |id|
    q = TR.get(id)
    out << "" << "#### #{q[:title]} (`#{id}`)" << ""
    out << "*Chapter #{q[:chapter]} · #{q[:giver]}, #{q[:where]} (map #{q[:map]}) · rank #{q[:rank] || 1} · #{q[:points] || 1} points · unlock `#{q[:unlock]}`*"
    out << "" << "#{q[:summary]}" << ""
    out << "**Quest log steps:** " + (q[:steps] || {}).map { |k, v| "`#{k}`: #{v}" }.join(" · ")
    out << "" << "**Reward:** #{rewards(q)}. **Touches:** #{q[:touches]}."
    (q[:scenes] || {}).each do |name, list|
      out << "" << "**Scene `#{name}`** (event: `pf_quest_run(:#{id}, :#{name})`)" << ""
      render(list, 0, out)
    end
  end
end
File.write(File.join(ROOT, "design", "TRIALS_QUESTS.md"), out.join("\n") + "\n")

#-------------------------------------------------------------------------------
# EVENT_POKEMON.md
#-------------------------------------------------------------------------------
ids = EM.ids.sort_by { |id| [EM.get(id)[:chapter] || 99, EM.ids.index(id)] }
kinds = { :battle => "wild battle, catch it", :gift => "gift", :egg => "egg", :boss => "boss battle, then it joins" }
ev = ["# EVENT_POKEMON — quest-reward and event Pokémon",
      "",
      "> **Generated** by `ruby tools/trials_docs.rb` from `plugins/Prismfall Trials/13x_EventMons_*.rb` (edit those). Engine: `Prismfall::EventMons` (`006_Trials_EventMons.rb`): `pf_event_battle(:ID)`, `pf_event_gift(:ID)`, bosses through Prismfall Bosses.",
      "> The spirit of the user's examples (SPINE Rev 13): **chases** that end in a battle and a catch (Rejuvenation's Nidoran), **boss Pokémon that join or pay out** (Rejuvenation's Spidops/Litleo), **rival-bug duels** where you pick a side (Reborn's Pinsir/Heracross), **gifts for a kindness** (Reborn's Torchic).",
      "> Rules: every event Pokémon carries something its area lacks (a type, ability or move); levels sit just under the cap of its chapter; a knocked-out battle event can be retried (`:on_ko => :retry`) unless stated; boss rewards join at a lower level than the boss; moves are legal (level-up, TM/tutor or egg) except a listed `:special_moves` event move. The headless test checks all of this.",
      "> **SPINE Revision 16** (`design/DISTRIBUTION_STUDY.md`, `design/warden_gates.json`): the **Badges** column is the fewest badges with which the Pokémon can be obtained (the test recomputes it from the quest unlock, the TALK rows and the scene's own gates). Nothing obtainable with *b* badges is a type answer to Warden *b*+1 or *b*+2 (Dorian: Fighting/Ghost; Tamsin: Fire/Flying/Rock; Marisol: Electric/Grass; Rook: Ground). A spar you can't catch (`:catchable => false`) hands nothing over.",
      ""]
early = ids.count { |id| (EM.get(id)[:chapter] || 99) <= 2 }
ev << "**#{ids.length} event Pokémon** (#{ids.count { |i| !EM.get(i)[:stub] }} implemented, the rest designed with data); **#{early} in Chapters 0–2.**"
ev << ""
ev << "| # | Pokémon | Kind | Ch | Badges | Where (map) | How it plays | Why it's worth having | Quest | Status |"
ev << "|---|---|---|---|---|---|---|---|---|---|"
ids.each_with_index do |id, i|
  d = EM.get(id)
  moves = d[:moves] ? " — " + d[:moves].join(", ") : ""
  moves = " — palettes: " + d[:variants].keys.join(" / ") if d[:variants]
  q = d[:quest] ? (TR.get(d[:quest]) ? "#{TR.get(d[:quest])[:title]} `#{d[:quest]}`" : d[:quest].to_s) : ""
  kind = (d[:kind] == :battle && d[:catchable] == false) ? "spar (can't be caught)" : (kinds[d[:kind]] || d[:kind])
  ev << "| #{i + 1} | **#{mon_label(id)}**#{esc(moves)} `#{id}` | #{kind} | #{d[:chapter]} | #{d.key?(:badges) ? d[:badges] : ''} | #{esc(d[:where])} (#{d[:map]}) | " \
        "#{esc(d[:trigger])} | #{esc(d[:why])} | #{esc(q)} | #{d[:stub] ? 'designed' : 'implemented'} |"
end
File.write(File.join(ROOT, "design", "EVENT_POKEMON.md"), ev.join("\n") + "\n")
puts "design/TRIALS_QUESTS.md: #{total} quests (#{wired} wired); design/EVENT_POKEMON.md: #{ids.length} event Pokemon (#{early} in Ch0-2)"
