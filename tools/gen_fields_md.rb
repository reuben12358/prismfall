#!/usr/bin/env ruby
# encoding: utf-8
#===============================================================================
# Regenerates the per-field sections of design/FIELDS.md ("## Silkwood" up to "## Every battle has a field") from
# the field files: :intro_message, :description, :notes, transitions (per stage) and seeds. Everything above and
# below that region (the intro, "What changed", the transition map, "Every battle has a field") is hand-written.
#   ruby tools/gen_fields_md.rb            # writes design/FIELDS.md
#   ruby tools/gen_fields_md.rb --check    # exit 1 if FIELDS.md is stale
#   FE_DIR=<dir> ...                        # read the field files from another folder (a dev copy)
# Pure data: loads 001_FieldEffects_Schema.rb and stubs FieldEffects.register (no Essentials runtime).
#===============================================================================
ROOT = File.expand_path("..", __dir__)
PLUGIN_DIR = ENV["FE_DIR"] || File.join(ROOT, "plugins", "Prismfall Field Effects")
MD = File.join(ROOT, "design", "FIELDS.md")
load File.join(PLUGIN_DIR, "001_FieldEffects_Schema.rb")
module FieldEffects
  @reg = {}
  class << self; attr_reader :reg; end
  def self.register(id, d); @reg[id] = d; end
end
Dir[File.join(PLUGIN_DIR, "1*.rb")].sort.each { |f| load f }
R = FieldEffects.reg

# Rules whose trigger or destination is a proc: how to say them in words ([field, transition :id] => [trigger, dest]).
DOC = {
  [:GLASS_DUNES, :shatter] => ["cracks: quakes, heavy blows, damaging sound moves (and big Ice moves on Hot Glass) x3",
                              "**Desert** (in rain: **Flooded Dunes**)"],
  [:GLASS_DUNES, :clash]   => ["beam clash x2", nil],
  [:FROZEN_LAKE, :thaw]    => ["3 rounds of sunlight (each damaging Ice move refreezes one)", nil]
}.freeze
# Changes made by a field's hooks rather than a transition rule (listed after its rules).
HOOK_CHANGES = {
  :GLASS_DUNES => { 1 => ["4 rounds without a damaging Fire move (sun holds the heat, rain cools it twice as fast) → stage 2 (Mirror Glass)",
                          "damaging FIRE-type moves anneal one crack"],
                    2 => ["a damaging FIRE-type move → stage 1 (Hot Glass), and anneals one crack"] },
  :FLOODED_DUNES => { 1 => ["the tide runs out (5 rounds; rain holds it, Water attacks feed it, sun x2) → **Desert** stage 2 (Superbloom)"] }
}.freeze

def nm(id); R[id] ? R[id][:name] : id.to_s; end

def trig(t)
  s = []
  mv = Array(t[:moves]).map(&:to_s)
  s << (mv.size > 5 ? mv.first(5).join(", ") + " +#{mv.size - 5} more" : mv.join(", ")) if t[:moves]
  s << Array(t[:types]).join("/") + "-type moves" if t[:types]
  s << "weather " + Array(t[:weather]).join("/") if t[:weather]
  s << "terrain " + Array(t[:terrain]).join("/") if t[:terrain]
  s << "after #{t[:turns]} rounds" if t[:turns]
  s << "a field condition (see notes)" if t[:check]
  s << "in " + Array(t[:in_weather]).join("/") if t[:in_weather]
  s << Array(t[:flags]).join("/") + " moves" if t[:flags]
  s << "a field-specific move condition (see notes)" if t[:condition] && s.empty?
  s << "(see notes)" if s.empty?
  r = s.join(", ")
  r += " x#{t[:uses]}" if t[:uses] && t[:uses] > 1
  r += " (even if they fail)" if t[:even_if_failed] && t[:to] && t[:moves] && t[:boost] != false
  r
end

FB = { :INVERSE => " (else Mindscape)", :RAINBOW => " (else Meadow)" }.freeze

def dest(t, fallback)
  return "returns to the previous field#{fallback}" if t[:to].is_a?(Proc)
  return "**#{nm(t[:to])}**" + (t[:stage] ? " (stage #{t[:stage]})" : "") if t[:to]
  return "stage #{t[:stage]}" if t[:stage]
  return "stage #{format('%+d', t[:stage_delta])}" if t[:stage_delta]
  return "rewinds progress" if t[:rewind]
  "?"
end

def line(id, t)
  tr, de = DOC[[id, t[:id]]]
  "#{tr || trig(t)} → #{de || dest(t, FB[id].to_s)}"
end

out = []
R.each do |id, d|
  out << "## #{d[:name]} (`:#{id}`)"
  out << ""
  out << "*#{d[:family].to_s.capitalize} field. Backdrop `#{d[:backdrop]}`. Nature Power: #{d[:nature_power] || '-'}. Natural type: #{d[:camouflage] || '-'}.*"
  out << ""
  out << "> #{d[:intro_message]}"
  out << ""
  out << d[:description].to_s
  out << ""
  Array(d[:notes]).each { |n| out << "- #{n}" }
  tr = Array(d[:transitions]).map { |t| line(id, t) }.uniq + Array(HOOK_CHANGES.dig(id, 1))
  out << "" << "**Changes:**" unless tr.empty? && !d[:stages]
  tr.each { |l| out << "- #{l}" }
  (d[:stages] || {}).each do |n, s|
    out << "- *Stage #{n}* (`#{s[:backdrop] || d[:backdrop]}`): #{s[:description]}"
    next if !s[:transitions] && !HOOK_CHANGES.dig(id, n)
    (Array(s[:transitions]).map { |t| line(id, t) }.uniq + Array(HOOK_CHANGES.dig(id, n))).each { |l| out << "  - #{l}" }
  end
  Array(d[:seed].is_a?(Hash) ? [d[:seed]] : d[:seed]).each do |s|
    bits = []
    bits << s[:stats].map { |k, v| "#{k} #{format('%+d', v)}" }.join(", ") if s[:stats]
    bits << "effects: " + Array(s[:effects]).join(", ") if s[:effects]
    bits << "becomes part #{s[:add_type]} type" if s[:add_type]
    bits << "status: #{s[:status]}" if s[:status]
    bits << "heals" if s[:heal]
    bits << "special effect" if s[:proc]
    out << "" << "**Seed (#{s[:item]}):** #{bits.join('; ')}."
  end
  out << ""
end
body = out.join("\n")

md = File.read(MD, :encoding => "UTF-8")
a = md.index("## #{R.values.first[:name]} (") or abort("FIELDS.md: first field section not found")
b = md.index("## Every battle has a field") or abort("FIELDS.md: 'Every battle has a field' not found")
new_md = md[0...a] + body + "\n" + md[b..]
if ARGV.include?("--check")
  if new_md == md
    puts "FIELDS.md per-field sections are up to date (#{R.size} fields)"
  else
    puts "FIELDS.md per-field sections are STALE: run ruby tools/gen_fields_md.rb"
    exit 1
  end
else
  File.write(MD, new_md, :encoding => "UTF-8")
  puts "wrote #{MD} (#{R.size} field sections)"
end
