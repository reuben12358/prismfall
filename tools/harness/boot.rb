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
    files = script_files("Data/Scripts").reject { |f| f.include?("999_Main") }
    files.each do |f|
      code = File.read(f, :encoding => "UTF-8")
      eval(code, TOPLEVEL_BINDING, f)
      BOOT[:scripts] << f
    end
  end
end

Harness.load_engine
load File.join(HARNESS_DIR, "engine_shims.rb")

MessageTypes.load_default_messages if FileTest.exist?("Data/messages_core.dat")
PluginManager.runPlugins
Harness::BOOT[:plugins] = PluginManager.plugins.dup
if ENV["PRISM_COMPILE"] == "1" || !File.exist?("Data/species.dat")
  Compiler.compile_pbs_files
end
Game.initialize
