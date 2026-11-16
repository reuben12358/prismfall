#===============================================================================
# Boots Pokemon Essentials v21.1 headlessly:
#   1. RGSS stubs  2. every engine script in numbered order (except 999_Main)
#   3. plugins through the real PluginManager  4. PBS through the real Compiler
# Run from the harness run directory (default /home/claude/run), which holds
# Data/Scripts, PBS/ and Plugins/ (the Prismfall plugins are symlinked to the
# kit's plugins/ folder, so fixes made there are what gets tested).
#===============================================================================
HARNESS_DIR = File.expand_path(__dir__)
RUN_DIR     = ENV["PRISM_RUN_DIR"] || "/home/claude/run"
Dir.chdir(RUN_DIR)
$DEBUG = true            # Essentials debug mode (plugins + PBS get compiled)
$stdout.sync = true
require File.join(HARNESS_DIR, "rgss_stub.rb")

module Harness
  BOOT = { :scripts => [], :plugins => [], :load_errors => [] }

  def self.script_files(dir)
    out = []
    Dir.children(dir).sort.each do |e|
      path = File.join(dir, e)
      if File.directory?(path) then out.concat(script_files(path))
      elsif e.end_with?(".rb") then out << path end
    end
    out
  end

  def self.load_engine
    # Data/Scripts = the base project's Scripts.rxdata, extracted one file per section in order.
    # The Main section is loaded too (it defines pbCallTitle/mainFunction, which plugins alias), minus
    # its trailing game loop.
    files = script_files("Data/Scripts")
    files.each do |f|
      code = File.read(f, :encoding => "UTF-8")
      if File.basename(f) =~ /\A\d+_Main\.rb\z/
        cut = code.index(/^loop do/) or raise "Main section layout changed"
        code = code[0...cut]
      end
      eval(code, TOPLEVEL_BINDING, f)
      BOOT[:scripts] << f
    end
  end
end

Harness.load_engine
load File.join(HARNESS_DIR, "engine_shims.rb")

MessageTypes.load_default_messages if FileTest.exist?("Data/messages_core.dat")
File.delete("Data/PluginScripts.rxdata") if File.exist?("Data/PluginScripts.rxdata")   # always recompile plugins
PluginManager.runPlugins
Harness::BOOT[:plugins] = PluginManager.plugins.dup
if ENV["PRISM_COMPILE"] == "1" || !File.exist?("Data/species.dat")
  Compiler.compile_pbs_files
end
# Game.initialize minus the RPG Maker data files (animations, tilesets, maps) battles don't need.
$game_temp   = Game_Temp.new
$game_system = Game_System.new
$data_animations = []; $data_tilesets = []; $data_common_events = []
GameData.load_all
