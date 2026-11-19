# Dumps every field definition (plugins/Prismfall Field Effects/1xx_Field_*.rb) as JSON for tools/trainer_gen/field_fit.py.
#   ruby tools/trainer_gen/dump_fields.rb [out.json]
ROOT = File.expand_path("../..", __dir__)
PLUGIN_DIR = File.join(ROOT, "plugins", "Prismfall Field Effects")
load File.join(PLUGIN_DIR, "001_FieldEffects_Schema.rb")
module FieldEffects
  @registered = {}
  class << self; attr_reader :registered; end
  def self.register(id, d); @registered[id] = d; id; end
end
Dir[File.join(PLUGIN_DIR, "1*_Field_*.rb")].sort.each { |f| load f }
require "json"
def clean(o)
  case o
  when Proc then "<proc>"
  when Hash then o.each_with_object({}) { |(k, v), h| h[k.to_s] = clean(v) }
  when Array then o.map { |v| clean(v) }
  when Symbol then o.to_s
  when Rational then o.to_f.round(4)
  else o
  end
end
out = {}
FieldEffects.registered.each do |id, d|
  out[id.to_s] = clean(d.reject { |k, _| [:notes, :hooks].include?(k) })
  out[id.to_s]["hooks"] = (d[:hooks] || {}).keys.map(&:to_s)
end
OUT_PATH = ARGV[0] || "/tmp/prismfall_fields.json"
File.write(OUT_PATH, JSON.pretty_generate(out))
puts "#{out.keys.size} fields -> #{OUT_PATH}"
