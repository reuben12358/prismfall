#===============================================================================
# Headless RGSS / mkxp-z stub layer for running Pokemon Essentials v21.1 battle
# logic in plain Ruby. Nothing here draws anything: every graphics/audio/input
# object is an inert placeholder. Used ONLY by tools/harness (logic tests).
#===============================================================================
$VERBOSE = nil
$DEBUG_GAME = true
require "zlib"

# A permissive object: remembers attribute writes, returns neutral values.
class HeadlessObject
  def initialize(*_args); @__attrs = {}; @__disposed = false; end
  def dispose; @__disposed = true; end
  def disposed?; @__disposed; end
  def update(*_a); end
  def respond_to_missing?(_n, _p = false); true; end

  def method_missing(name, *args, &_blk)
    s = name.to_s
    @__attrs ||= {}
    if s.end_with?("=")
      @__attrs[s.chomp("=")] = args[0]
    elsif s.end_with?("?")
      false
    elsif @__attrs.key?(s)
      @__attrs[s]
    else
      default_for(s)
    end
  end

  NUMERIC_DEFAULTS = %w[x y z ox oy width height opacity angle bush_depth bush_opacity
                        zoom_x zoom_y blend_type contents_opacity back_opacity index
                        cursor_rect_x wave_amp wave_length wave_speed wave_phase].freeze
  def default_for(s)
    return 1.0 if s == "zoom_x" || s == "zoom_y"
    return 255 if s.include?("opacity")
    return 0 if NUMERIC_DEFAULTS.include?(s)
    nil
  end
end

class Color
  attr_accessor :red, :green, :blue, :alpha
  def initialize(r = 0, g = 0, b = 0, a = 255); set(r, g, b, a); end
  def set(r, g = 0, b = 0, a = 255)
    if r.is_a?(Color) then @red, @green, @blue, @alpha = r.red, r.green, r.blue, r.alpha
    else @red, @green, @blue, @alpha = r, g, b, a end
    self
  end
  def ==(o); o.is_a?(Color) && [red, green, blue, alpha] == [o.red, o.green, o.blue, o.alpha]; end
  def _dump(_d); [@red, @green, @blue, @alpha].pack("E4"); end
  def self._load(s); new(*s.unpack("E4")); end
end

class Tone
  attr_accessor :red, :green, :blue, :gray
  def initialize(r = 0, g = 0, b = 0, a = 0); set(r, g, b, a); end
  def set(r, g = 0, b = 0, a = 0)
    if r.is_a?(Tone) then @red, @green, @blue, @gray = r.red, r.green, r.blue, r.gray
    else @red, @green, @blue, @gray = r, g, b, a end
    self
  end
  def _dump(_d); [@red, @green, @blue, @gray].pack("E4"); end
  def self._load(s); new(*s.unpack("E4")); end
end

class Rect
  attr_accessor :x, :y, :width, :height
  def initialize(x = 0, y = 0, w = 0, h = 0); set(x, y, w, h); end
  def set(x, y = 0, w = 0, h = 0)
    if x.is_a?(Rect) then @x, @y, @width, @height = x.x, x.y, x.width, x.height
    else @x, @y, @width, @height = x, y, w, h end
    self
  end
  def empty; set(0, 0, 0, 0); end
end

class Table
  attr_reader :xsize, :ysize, :zsize
  def initialize(x, y = 1, z = 1)
    @xsize, @ysize, @zsize = x, y, z
    @data = Array.new(x * y * z, 0)
  end
  def [](x, y = 0, z = 0); @data[x + (y * @xsize) + (z * @xsize * @ysize)]; end
  def []=(*a); v = a.pop; x, y, z = a; @data[x + ((y || 0) * @xsize) + ((z || 0) * @xsize * @ysize)] = v; end
  def resize(x, y = 1, z = 1); @xsize, @ysize, @zsize = x, y, z; @data = Array.new(x * y * z, 0); end
  def _dump(_d); [3, @xsize, @ysize, @zsize, @data.size].pack("L5") + @data.pack("s*"); end
  def self._load(s)
    _dim, x, y, z, _n = s.unpack("L5")
    t = new(x, y, z); t.instance_variable_set(:@data, s[20..].unpack("s*")); t
  end
end

class Font < HeadlessObject
  class << self
    attr_accessor :default_name, :default_size, :default_bold, :default_italic, :default_color,
                  :default_shadow, :default_outline, :default_out_color
    def exist?(_n); true; end
  end
  self.default_name = "Arial"; self.default_size = 22; self.default_color = Color.new(255, 255, 255)
  attr_accessor :name, :size, :bold, :italic, :color
  def initialize(name = "Arial", size = 22); super(); @name = name; @size = size; @color = Color.new(255, 255, 255); end
end

class Bitmap < HeadlessObject
  attr_accessor :font
  def initialize(w = 32, h = 32, *_rest)
    super()
    if w.is_a?(String) then @w = 32; @h = 32 else @w = w; @h = h || 32 end
    @font = Font.new
  end
  def width; @w; end
  def height; @h; end
  def rect; Rect.new(0, 0, @w, @h); end
  def text_size(text); Rect.new(0, 0, text.to_s.length * 8, 24); end
  def draw_text(*_a); end
  def get_pixel(*_a); Color.new(0, 0, 0, 0); end
  def clone; self.class.new(@w, @h); end
  def self.max_size; 16_384; end
  %w[blt stretch_blt fill_rect clear clear_rect set_pixel hue_change blur radial_blur
     gradient_fill_rect raw_data= to_file].each { |m| define_method(m) { |*_a| nil } }
  def mega?; false; end
end

class Viewport < HeadlessObject
  attr_accessor :rect, :z, :ox, :oy, :color, :tone, :visible
  def initialize(*a)
    super()
    @rect = a[0].is_a?(Rect) ? a[0] : Rect.new(a[0] || 0, a[1] || 0, a[2] || 512, a[3] || 384)
    @z = 0; @ox = 0; @oy = 0; @color = Color.new(0, 0, 0, 0); @tone = Tone.new; @visible = true
  end
  def flash(*_a); end
end

class Sprite < HeadlessObject
  attr_accessor :bitmap, :viewport, :visible, :color, :tone, :src_rect
  def initialize(viewport = nil)
    super()
    @viewport = viewport; @visible = true
    @color = Color.new(0, 0, 0, 0); @tone = Tone.new; @src_rect = Rect.new
  end
  def flash(*_a); end
  def width; @src_rect.width; end
  def height; @src_rect.height; end
  # Real accessors (engine code aliases these).
  { :x => 0, :y => 0, :z => 0, :ox => 0, :oy => 0, :zoom_x => 1.0, :zoom_y => 1.0, :angle => 0,
    :mirror => false, :opacity => 255, :blend_type => 0, :bush_depth => 0, :bush_opacity => 128,
    :wave_amp => 0, :wave_length => 180, :wave_speed => 360, :wave_phase => 0.0 }.each do |attr, dflt|
    define_method(attr) { v = instance_variable_get("@#{attr}"); v.nil? ? dflt : v }
    define_method("#{attr}=") { |v| instance_variable_set("@#{attr}", v) }
  end
end

class Plane < Sprite; end
class Window < HeadlessObject
  attr_accessor :viewport, :visible, :contents, :windowskin, :cursor_rect
  def initialize(viewport = nil); super(); @viewport = viewport; @visible = true; @cursor_rect = Rect.new; end
end
class Tilemap < HeadlessObject
  attr_accessor :viewport
  def initialize(viewport = nil); super(); @viewport = viewport; end
  def autotiles; @autotiles ||= []; end
end

module Graphics
  @frame_count = 0; @frame_rate = 60; @brightness = 255
  class << self
    attr_accessor :frame_count, :frame_rate, :brightness, :fullscreen, :scale, :show_cursor
    def update; @frame_count += 1; System.tick; end
    def width; 512; end
    def height; 384; end
    def delta; 1.0 / 60; end
    def average_frame_rate; 60.0; end
    def snap_to_bitmap; Bitmap.new(512, 384); end
    def method_missing(_n, *_a); nil; end   # freeze, transition, wait, center, resize_screen...
    def respond_to_missing?(_n, _p = false); true; end
  end
end

module System
  VERSION = "2.4.2/c9378cf"
  @clock = 0.0
  class << self
    def tick; @clock += 1.0 / 60; end
    # Virtual clock: advances on every read so engine timing loops terminate instantly.
    def uptime; @clock += 0.05; end
    def delta; (1_000_000 / 60); end
    def game_title; "Prismfall headless harness"; end
    def platform; "Linux"; end
    def data_directory; Dir.pwd + "/"; end
    def user_language; "en_US"; end
    def user_name; "harness"; end
    def is_really_windows?; false; end
    def set_window_title(_t); end
    def method_missing(_n, *_a); nil; end
    def respond_to_missing?(_n, _p = false); true; end
  end
end

module Input
  %w[DOWN LEFT RIGHT UP A B C X Y Z L R SHIFT CTRL ALT F5 F6 F7 F8 F9].each_with_index { |n, i| const_set(n, i + 1) }
  USE = C; BACK = B; ACTION = A; JUMPUP = X; JUMPDOWN = Y; SPECIAL = Z; AUX1 = L; AUX2 = R
  class << self
    def update; end
    def press?(_k); false; end
    def trigger?(_k); false; end
    def repeat?(_k); false; end
    def release?(_k); false; end
    def dir4; 0; end
    def dir8; 0; end
    def mouse_x; 0; end
    def mouse_y; 0; end
    def text_input; false; end
    def text_input=(_v); end
    def gets; ""; end
    def clipboard; ""; end
    def method_missing(_n, *_a); false; end
    def respond_to_missing?(_n, _p = false); true; end
  end
end

module Audio
  class << self
    def method_missing(_n, *_a); nil; end
    def respond_to_missing?(_n, _p = false); true; end
  end
end

module RPG
  class AudioFile
    attr_accessor :name, :volume, :pitch
    def initialize(name = "", volume = 100, pitch = 100); @name = name; @volume = volume; @pitch = pitch; end
  end
  class Weather < HeadlessObject; end
  # Plain RGSS data containers (only needed so data files/class bodies resolve).
  %w[Map MapInfo Event EventCommand MoveRoute MoveCommand System Tileset CommonEvent
     Animation Actor Class Skill Item Weapon Armor Enemy Troop State].each do |n|
    const_set(n, Class.new(HeadlessObject)) unless const_defined?(n, false)
  end
  class Event; Page = Class.new(HeadlessObject); end
  class Animation; Frame = Class.new(HeadlessObject); Timing = Class.new(HeadlessObject); end
  class System; Words = Class.new(HeadlessObject); TestBattler = Class.new(HeadlessObject); end
end

class Win32API
  def initialize(*_a); end
  def call(*_a); 0; end
  alias Call call
end

class Hangup < Exception; end unless defined?(Hangup)
class Reset < Exception; end unless defined?(Reset)

def load_data(filename)
  File.open(filename, "rb") { |f| Marshal.load(f) }
end

def save_data(obj, filename)
  File.open(filename, "wb") { |f| Marshal.dump(obj, f) }
end

def rgss_main; yield; end
def msgbox(*a); $stderr.puts("[msgbox] " + a.join(" ")); end
def msgbox_p(*a); $stderr.puts("[msgbox] " + a.map(&:inspect).join(" ")); end
