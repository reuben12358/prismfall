#===============================================================================
# Prismfall Core - 002 Save state
#-------------------------------------------------------------------------------
# All Core state lives in one object, $prismfall (Prismfall::SaveState), which
# is registered with SaveData. Old saves that predate the plugin simply get a
# fresh state (no ensure_class, so SaveData.valid? never rejects them).
#===============================================================================
module Prismfall
  class SaveState
    STATE_VERSION = 1

    attr_accessor :data_version
    # Difficulty
    attr_accessor :difficulty          # Symbol, key of Prismfall::DIFFICULTIES
    attr_accessor :difficulty_chosen   # true once chosen at new game
    attr_accessor :difficulty_log      # [[old, new, play_time_seconds], ...]
    # Rival starter system
    attr_accessor :starter             # { :species, :gen, :slot, :stage, :inferred } or nil
    # Level caps
    attr_accessor :level_cap_override  # Integer or nil (story-forced cap)
    attr_accessor :level_caps_disabled # true = no caps at all
    attr_accessor :finale_cap_unlocked # true = post-Badge-18 cap is FESTIVAL_FINALE_CAP
    # Festival of Champions
    attr_accessor :festival            # Hash (see 009_Festival.rb) or nil
    # Free storage for later Core features (keeps old saves loadable)
    attr_accessor :custom

    def initialize
      @data_version        = STATE_VERSION
      @difficulty          = Prismfall::DIFFICULTY_DEFAULT
      @difficulty_chosen   = false
      @difficulty_log      = []
      @starter             = nil
      @level_cap_override  = nil
      @level_caps_disabled = false
      @finale_cap_unlocked = false
      @festival            = nil
      @custom              = {}
    end

    # Fills in anything missing from older versions of this object.
    def migrate!
      @difficulty = Prismfall::DIFFICULTY_DEFAULT if !Prismfall::DIFFICULTIES.has_key?(@difficulty)
      @difficulty_chosen   = false if @difficulty_chosen.nil?
      @difficulty_log    ||= []
      @level_caps_disabled = false if @level_caps_disabled.nil?
      @finale_cap_unlocked = false if @finale_cap_unlocked.nil?
      @custom            ||= {}
      @data_version        = STATE_VERSION
      return self
    end
  end

  # Always returns a state object (creates a temporary one on the title screen).
  def self.state
    $prismfall = Prismfall::SaveState.new if !$prismfall.is_a?(Prismfall::SaveState)
    return $prismfall
  end
end

SaveData.register(:prismfall_core) do
  save_value { Prismfall.state }
  load_value do |value|
    $prismfall = (value.is_a?(Prismfall::SaveState)) ? value : Prismfall::SaveState.new
    $prismfall.migrate!
    Prismfall.ensure_badge_array if Prismfall.respond_to?(:ensure_badge_array)
  end
  new_game_value { Prismfall::SaveState.new }
end
