#===============================================================================
# Prismfall Trials - 001 Config: the eight Trial institutions, ranks, settings
#-------------------------------------------------------------------------------
# Rejuvenation has Help Centers; Velmora has Trials (SPINE Revision 13). Each
# kingdom runs its own institution with its own name, hall, ranks and flavour of
# quest. Design: design/TRIALS.md. Quest data: 1xx_Quests_*.rb. Event Pokemon:
# 13x_EventMons_*.rb. Badge-gated encounters: pbs/encounters_badgetiers.txt.
# Map IDs are the current maps.json IDs (names are changing; IDs move with
# the world-map work, so keep :halls in step with maps.json).
#===============================================================================
module Prismfall
  module Trials
    # Rank thresholds are Trial points (each quest gives :points). Index 0 = rank 1.
    RANK_POINTS = [0, 3, 8, 15, 25].freeze

    TRIALS = {
      :ELOWEN => {
        :name     => "The Quiet Way",
        :kingdom  => "Elowen",
        :keeper   => "the Order of the Listening Root",
        :posted   => "lantern",          # how quests appear on the board (flavour text)
        :board    => "Lantern Rope",
        :ranks    => ["Seedling", "Sapling", "Bough", "Heartwood", "Evergreen"],
        :halls    => { 100 => "the Ferrow's Landing wayshrine", 140 => "the Saltmere Lantern House",
                       120 => "the Briarwick Lantern House", 280 => "the Hall of the Listening Root (Verdance)",
                       440 => "the Twilight Cloister (Gloaming)" },
        :accept   => "You untie the lantern from the rope.",
        :done     => "The lantern is lit and let go. It rises over the roofs.",
        :greeting => "The Root listens. What would you take down from the rope?"
      },
      :ISENMAR => {
        :name     => "The Tally",
        :kingdom  => "Isenmar",
        :keeper   => "the Tallykeepers and their skalds",
        :posted   => "rune",
        :board    => "Tally Mast",
        :ranks    => ["Driftwood", "Oarhand", "Harpooner", "Shieldwall", "Sagaborn"],
        :halls    => { 573 => "the Half-Tally at the Two Hearths (Frostwick)", 160 => "the Ebbmouth Net Loft",
                       306 => "the Great Tally in the Mead Hall of Rimeholt" },
        :accept   => "You run your thumb along the carved rune. The deed is yours to do.",
        :done     => "A new notch is cut in the Tally Mast, beside your name.",
        :greeting => "The sea keeps count. So do we. What deed do you take?"
      },
      :ZENITH => {
        :name     => "The Prize Exchange",
        :kingdom  => "Zenith",
        :keeper   => "the Registry of Patents and Prizes",
        :posted   => "call",
        :board    => "Split-Flap Board",
        :ranks    => ["Applicant", "Licensee", "Fellow", "Patent-Holder", "Laureate"],
        :halls    => { 108 => "Grant Kiosk P-3NNY (Ferrow's Landing customs hall)",
                       143 => "Grant Kiosk P-3NNY/1 (Saltmere Harbour Office)",
                       160 => "Grant Kiosk P-3NNY/2 (Ebbmouth Lattice station)",
                       194 => "the Prize Exchange floor (Lumen City, Council Ward)" },
        :accept   => "The board clacks. Your name flips into the ACCEPTED column.",
        :done     => "The board clacks: PRIZE AWARDED. Somewhere a small bell rings.",
        :greeting => "WELCOME TO THE PRIZE EXCHANGE. PLEASE SELECT A CALL FOR PROPOSALS."
      },
      :NADIR => {
        :name     => "The Gutter Book",
        :kingdom  => "Nadir",
        :keeper   => "Six-Fingers Ottoline, fixer of the Last Rung",
        :posted   => "chalk mark",
        :board    => "Gutter Board",
        :ranks    => ["Drip", "Runner", "Fixer", "Sumpwise", "Undercrown"],
        :halls    => { 220 => "the Mirefen noodle-cart board", 630 => "the Charwell char-burners' wall",
                       260 => "the Last Rung (Ironreach)", 423 => "the Moon Market stall (Underveil)" },
        :accept   => "Ottoline wipes the chalk mark off with her thumb. \"It's yours. Don't make it mine.\"",
        :done     => "The job's chalked through. Ottoline takes her cut. You get the rest.",
        :greeting => "Nobody down here gets anything free. Want work?"
      },
      :ASHKAAR => {
        :name     => "The Trial by Flames",
        :kingdom  => "Ashkaar",
        :keeper   => "the Ember Legion's Crucible",
        :posted   => "brand",
        :board    => "Wall of Writs",
        :ranks    => ["Kindling", "Ember", "Brand", "Pyre", "Dragonsworn"],
        :halls    => { 146 => "the Legion recruiting barge (Saltmere harbour)", 650 => "the Scaldwater truce-baths",
                       240 => "the Crucible (Cindervault caldera)", 460 => "the Wyrmrest proving ground" },
        :accept   => "The writ is branded with your mark. There's no taking it back.",
        :done     => "The Herald strikes the gong. Your brand goes up on the Wall of the Proven.",
        :greeting => "Strength is the only honest coin. Show us yours."
      },
      :OSSARIA => {
        :name     => "The Rolls of Unearthing",
        :kingdom  => "Ossaria",
        :keeper   => "the Curators-Elect of the Dig Lab",
        :posted   => "clay tablet",
        :board    => "Tablet Rack",
        :ranks    => ["Sandsifter", "Digger", "Delver", "Tombwise", "Bonewright"],
        :halls    => { 610 => "the Copperdune caravanserai rack", 200 => "the Hall of Unearthing (Duneholt)",
                       770 => "the Vigil embalmers' rack", 360 => "the Cragholm lift-house rack" },
        :accept   => "You take the clay tablet. Finished work breaks it; unfinished work keeps it heavy.",
        :done     => "You crack the tablet in two. The Curator files both halves.",
        :greeting => "Everything is buried somewhere. Choose what to dig up."
      },
      :ANTUMBRA => {
        :name     => "The Rite of Reflection",
        :kingdom  => "Antumbra",
        :keeper   => "the Lectors of the Speculum",
        :posted   => "mirror-writing",
        :board    => "Speculum Glass",
        :ranks    => ["Glimpse", "Gleam", "Mirror", "Speculum", "Behind-the-Glass"],
        :halls    => { 753 => "the Glassmere reading-pool", 346 => "the Speculum (Lucent)",
                       380 => "the lantern-priests' glass (Gravenmoor)" },
        :accept   => "You read it backwards, which is forwards here. It reads you back.",
        :done     => "Your reflection signs the Speculum. It signs a little late.",
        :greeting => "Look into it. No, the other way. There. Which do you take?"
      },
      :CROWNHAVEN => {
        :name     => "The Hall of Petitions",
        :kingdom  => "Crownhaven",
        :keeper   => "the Accord's Petition Office",
        :posted   => "sealed petition",
        :board    => "Petition Wall",
        :ranks    => ["Petitioner", "Courier", "Envoy", "Concordant", "Hand of the Accord"],
        :halls    => { 890 => "the Pilgrim's Rest shrine-post", 496 => "the Hall of Petitions (Market Ring)",
                       497 => "the Pilgrims' Quarter board" },
        :accept   => "You break the seal. Clerk Fenwright stamps it twice, for luck and for the archive.",
        :done     => "The petition is marked ANSWERED in red ink and filed in the eighteenth drawer.",
        :greeting => "All eighteen gates send their troubles here. Take a seal, any seal."
      }
    }.freeze

    # Rank-up rewards, given by the hall keeper when a rank is reached (rank 2..5).
    # Values use the same reward keys as quests (see 005_Trials_Quests.rb).
    # Mega Stones (SPINE Rev 20, design/MEGA_EVOLUTION.md): rank rewards are not badge-gated, so only stones that are
    # safe whenever they arrive go here (Sharpedonite, Manectite: usable from the Ring-Day, 7 badges); later stones
    # are rank-gated commissions with a badge unlock (114_Quests_Megas.rb).
    RANK_REWARDS = {
      :ELOWEN  => { 2 => { :items => [[:SOOTHEBELL, 1]] }, 3 => { :items => [[:TM20, 1]] },
                    4 => { :pokemon => :EL_RANK_COMFEY }, 5 => { :items => [[:MAGICALSEED, 3]] } },
      :ISENMAR => { 2 => { :items => [[:MYSTICWATER, 1]] }, 3 => { :items => [[:TM72, 1], [:SHARPEDONITE, 1]] },
                    4 => { :items => [[:NEVERMELTICE, 1]] }, 5 => { :pokemon => :IS_RANK_LAPRAS } },
      :ZENITH  => { 2 => { :items => [[:EXPCANDYS, 3]] }, 3 => { :items => [[:CELLBATTERY, 2], [:MANECTITE, 1]] },
                    4 => { :items => [[:SYNTHETICSEED, 3]] }, 5 => { :items => [[:ABILITYPATCH, 1]] } },
      :NADIR   => { 2 => { :items => [[:BLACKSLUDGE, 1]] }, 3 => { :items => [[:TM12, 1]] },
                    4 => { :items => [[:EXPCANDYL, 2]] }, 5 => { :items => [[:EXPCANDYXL, 2]] } },
      :ASHKAAR => { 2 => { :items => [[:CHARCOAL, 1]] }, 3 => { :items => [[:FLAMEORB, 1]] },
                    4 => { :pokemon => :AS_RANK_DEINO }, 5 => { :items => [[:LIFEORB, 1]] } },
      :OSSARIA => { 2 => { :items => [[:SOFTSAND, 1]] }, 3 => { :items => [[:TM28, 1]] },
                    4 => { :items => [[:TELLURICSEED, 3]] }, 5 => { :items => [[:ABILITYCAPSULE, 1]] } },
      :ANTUMBRA => { 2 => { :items => [[:SPELLTAG, 1]] }, 3 => { :items => [[:TM48, 1]] },
                     4 => { :items => [[:ELEMENTALSEED, 3]] }, 5 => { :items => [[:ABILITYPATCH, 1]] } },
      :CROWNHAVEN => { 2 => { :items => [[:PPUP, 2]] }, 3 => { :items => [[:PPMAX, 1]] },
                       4 => { :items => [[:RARECANDY, 3]] }, 5 => { :items => [[:MASTERBALL, 1]] } }
    }.freeze

    # Show "QUEST LOG: ..." toasts when a quest starts / changes step / ends.
    TOASTS            = true
    # Board entries show "Rec. Lv." like Rejuvenation's Help Centers.
    SHOW_REC_LEVEL    = true
    # First time a map with a newly unlocked badge tier is entered, a short
    # "the grass rustles" notice plays (see 007_Trials_BadgeTiers.rb).
    TIER_ENTRY_NOTICE = true
    # Encounter-version base for badge tiers: tier b on encounter version v
    # lives at version TIER_VERSION_BASE * (v + 1) + b  (v0: 101-118, v1: 201-218 ...).
    TIER_VERSION_BASE = 100
    # Quests marked :stub (designed, not yet wired on any map) stay off boards
    # unless $DEBUG and this is true.
    SHOW_STUBS_IN_DEBUG = true
    # Pause menu entry "Quests".
    QUEST_LOG_IN_PAUSE_MENU = true
  end
end
