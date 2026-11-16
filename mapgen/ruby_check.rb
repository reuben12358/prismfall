# Loads OUR generated .rxdata files with Ruby's own Marshal (stub RGSS classes) to prove they parse.
# Only ever run this on files produced by mapgen (never on third-party data).
module RPG
  class Map; attr_accessor :tileset_id, :width, :height, :autoplay_bgm, :bgm, :autoplay_bgs, :bgs, :encounter_list, :encounter_step, :data, :events; end
  class MapInfo; attr_accessor :name, :parent_id, :order, :expanded, :scroll_x, :scroll_y; end
  class Event; attr_accessor :id, :name, :x, :y, :pages
    class Page; attr_accessor :condition, :graphic, :move_type, :move_speed, :move_frequency, :move_route, :walk_anime, :step_anime, :direction_fix, :through, :always_on_top, :trigger, :list
      class Condition; attr_accessor :switch1_valid, :switch2_valid, :variable_valid, :self_switch_valid, :switch1_id, :switch2_id, :variable_id, :variable_value, :self_switch_ch; end
      class Graphic; attr_accessor :tile_id, :character_name, :character_hue, :direction, :pattern, :opacity, :blend_type; end
    end
  end
  class EventCommand; attr_accessor :code, :indent, :parameters; end
  class MoveRoute; attr_accessor :repeat, :skippable, :list; end
  class MoveCommand; attr_accessor :code, :parameters; end
  class AudioFile; attr_accessor :name, :volume, :pitch; end
end
class Table
  attr_reader :xsize, :ysize, :zsize, :data
  def self._load(s); t = allocate; t.instance_variable_set(:@raw, s); d = s.unpack("l5"); t.instance_variable_set(:@xsize, d[1]); t.instance_variable_set(:@ysize, d[2]); t.instance_variable_set(:@zsize, d[3]); raise "bad table" if s.bytesize != 20 + 2 * d[4] || d[4] != d[1] * d[2] * d[3]; t; end
end
class Tone; def self._load(s); raise "bad tone" if s.bytesize != 32; allocate; end; end
class Color; def self._load(s); raise "bad color" if s.bytesize != 32; allocate; end; end
ok = 0
ARGV.each do |f|
  m = Marshal.load(File.binread(f))
  if m.is_a?(RPG::Map)
    raise "#{f}: size" if m.data.xsize != m.width || m.data.ysize != m.height || m.data.zsize != 3
    m.events.each do |id, ev|
      raise "#{f}: event id #{id}" if ev.id != id
      ev.pages.each do |pg|
        raise "#{f}: list must end with code 0" if pg.list.last.code != 0 || pg.list.last.indent != 0
        pg.list.each { |c| raise "#{f}: bad cmd" if !c.is_a?(RPG::EventCommand) || !c.parameters.is_a?(Array) }
      end
    end
  end
  ok += 1
end
puts "ruby Marshal.load OK: #{ok}/#{ARGV.length}"
