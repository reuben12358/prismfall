#===============================================================================
# Prismfall Core - 012 Narrative data (SAMPLE / PLACEHOLDER)
#-------------------------------------------------------------------------------
# Data tables for Bonds, Standing, Resonance, Choices, Game Overs and Endings.
# Every key here is a placeholder until design/NARRATIVE_KEYS.md /
# story/10_CHOICES_ENDINGS.md are final; then transcribe their keys here.
# Unregistered keys still work at runtime (with a console warning in debug), so
# events can be written before this table is complete.
# Conditions are strings for Prismfall::Conditions (see 014_Conditions.rb).
#===============================================================================
module Prismfall
  module Narrative
    WARN_UNREGISTERED = true   # console warning for keys missing from the tables
    HISTORY_LIMIT     = 300    # entries kept in the change history (debug aid)

    #---------------------------------------------------------------------------
    # Bonds (affinity with key characters)
    #---------------------------------------------------------------------------
    BOND_DEFAULT = { :min => -10, :max => 10, :start => 0 }
    BONDS = {
      :JUNO    => { :name => "Juno",          :start => 2 },
      :KESTREL => { :name => "Kestrel",       :start => -1 },
      :VALEN   => { :name => "Valen" },
      :VOSS    => { :name => "Aurelian Voss" },
      :MOURNER => { :name => "the Mourner" },
      :ROWAN   => { :name => "Rowan Ashby" }
    }
    # [lower bound, tier]; ascending. A value takes the last tier whose bound it
    # reaches; values below the first bound get the first tier.
    BOND_TIERS = [[-6, :hostile], [-2, :wary], [0, :neutral], [3, :friendly], [6, :close], [9, :devoted]]
    # Optional feedback text when a bond changes with show: true.
    BOND_UP_TEXT   = "{1} will remember that."
    BOND_DOWN_TEXT = "{1} will remember that."

    #---------------------------------------------------------------------------
    # Faction standing
    #---------------------------------------------------------------------------
    STANDING_DEFAULT = { :min => -10, :max => 10, :start => 0 }
    FACTIONS = {
      :HOLLOW   => { :name => "the Hollow" },
      :MERIDIAN => { :name => "the Meridian Concord", :start => 1 },
      :ACCORD   => { :name => "the Accord", :start => 1 }
    }
    STANDING_TIERS = [[-6, :enemy], [-2, :distrusted], [0, :neutral], [3, :trusted], [7, :ally]]

    #---------------------------------------------------------------------------
    # Resonance: Legend Plate axis. Positive = Harmony, negative = Ruin.
    #---------------------------------------------------------------------------
    RESONANCE_MIN   = -10
    RESONANCE_MAX   = 10
    RESONANCE_START = 0
    RESONANCE_BANDS = [[-10, :ruin], [-5, :ruin_leaning], [-1, :balanced], [2, :harmony_leaning], [6, :harmony]]

    #---------------------------------------------------------------------------
    # Choices (named decisions). :values = allowed values (nil = any);
    # :once = can't be changed after it's made.
    #---------------------------------------------------------------------------
    CHOICES = {
      :ferry_stowaway  => { :values => [:hid, :reported], :once => true, :description => "Act I: the stowaway on the last ferry" },
      :rowan_exile     => { :values => [:defended, :exiled], :once => true, :description => "Act III: Rowan Ashby's exile from Verdance" },
      :kestrel_truth   => { :values => [:kept_secret, :told, :betrayed], :once => true, :description => "Kestrel's father's disgrace" },
      :valen_secret    => { :values => [:kept, :exposed], :once => true, :description => "Valen's knowledge of the Bleed" },
      :exposed         => { :values => [:nobody, :meridian, :hollow, :accord], :description => "What the player exposed before the Festival" },
      :mourner_fate    => { :values => [:spare, :unmask, :abandon], :once => true, :description => "The Mourner's fate" },
      :final_decision  => { :values => [:restore, :release, :bind, :shatter], :once => true, :description => "The Plates, at the end" }
    }

    #---------------------------------------------------------------------------
    # Game overs (>= 12 per SPINE Rev. 3). Finding every registered one unlocks
    # the Ruin Route (unless :ruin_exempt). :hint is shown in the Ledger viewer
    # for unfound entries when LEDGER_SHOW_HINTS is true. :me = optional ME.
    #---------------------------------------------------------------------------
    LEDGER_SHOW_HINTS = false
    GAME_OVERS = {
      :GO_LAST_FERRY    => { :title => "The Last Ferry",        :epitaph => "You stayed aboard. The coast faded behind the fog, and Velmora with it.", :hint => "Act I" },
      :GO_BLEED_TIDE    => { :title => "Swallowed by the Bleed", :epitaph => "Unimprinted is not the same as unbreakable.", :hint => "Act I" },
      :GO_HOLLOW_PYRE   => { :title => "Kindling",              :epitaph => "The Hollow burned the Plate, and you with it. They wept while they did it.", :hint => "Act II" },
      :GO_SIGNED_INK    => { :title => "Signed in Ink",         :epitaph => "Meridian keeps its contracts. You became one of its assets.", :hint => "Act II" },
      :GO_NADIR_DEBT    => { :title => "Debt Below",            :epitaph => "In Nadir, every favour is a loan. Yours came due.", :hint => "Act II" },
      :GO_BEHIND_GLASS  => { :title => "Behind the Glass",      :epitaph => "Antumbra let you in. It never promised to let you out.", :hint => "Act III" },
      :GO_FROZEN_SEA    => { :title => "The Frozen Sea",        :epitaph => "Isenmar's ice keeps everything. Now it keeps you.", :hint => "Act III" },
      :GO_BONE_SANDS    => { :title => "Bones in the Sand",     :epitaph => "Ossaria has a fossil for every traveller who trusted the wrong map.", :hint => "Act III" },
      :GO_DRAGONFIRE    => { :title => "Dragonfire",            :epitaph => "Ashkaar's lords do not forgive a broken oath.", :hint => "Act IV" },
      :GO_DROWNED_CROWN => { :title => "The Drowned Crown",     :epitaph => "The tide came in, and the crown sank with its bearer.", :hint => "Act IV" },
      :GO_VANES_FALL    => { :title => "Vane's Fall",           :epitaph => "You pushed Kestrel too far, and both of you fell.", :hint => "Act IV" },
      :GO_SOVEREIGN_LIE => { :title => "The Sovereign's Lie",   :epitaph => "Valen's lie held for thirty years. It will hold for thirty more.", :hint => "Act V" }
    }

    #---------------------------------------------------------------------------
    # Endings. ENDING_RULES is checked in order by Prismfall::Endings.determine;
    # the first condition that holds wins, else DEFAULT_ENDING.
    #   :kind          :good / :bad / :grey / :ruin
    #   :common_event  common event ID to run (epilogue), optional
    #   :credits       true = roll Scene_Credits afterwards
    #---------------------------------------------------------------------------
    ENDINGS = {
      :END_RETURN    => { :name => "The Return",       :kind => :good, :credits => true },
      :END_SILENCE   => { :name => "Silence",          :kind => :bad,  :credits => true },
      :END_ACCORD    => { :name => "The New Accord",   :kind => :grey, :credits => true },
      :END_HOLLOW    => { :name => "The Hollow Crown", :kind => :grey, :credits => true },
      :END_MERIDIAN  => { :name => "Concordance",      :kind => :grey, :credits => true },
      :END_WANDERER  => { :name => "The Wanderer",     :kind => :grey, :credits => true },
      :END_RUIN      => { :name => "Unmade",           :kind => :ruin, :credits => true }
    }
    ENDING_RULES = [
      [:END_RUIN,     "ruin_route && resonance_band == :ruin"],
      [:END_RETURN,   "choice(:final_decision) == :restore && resonance >= 4 && bond(:JUNO) >= 3 && bond(:KESTREL) >= 0"],
      [:END_SILENCE,  "choice(:final_decision) == :bind"],
      [:END_HOLLOW,   "choice(:final_decision) == :shatter && standing(:HOLLOW) >= 3"],
      [:END_MERIDIAN, "standing(:MERIDIAN) >= 5 && choice(:exposed) != :meridian"],
      [:END_ACCORD,   "standing(:ACCORD) >= 3"]
    ]
    DEFAULT_ENDING = :END_WANDERER
  end
end
