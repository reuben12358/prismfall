#===============================================================================
# Prismfall Core - 001 Configuration
#-------------------------------------------------------------------------------
# Every tunable of the Core plugin lives in this file. Gym order/type/city/
# Warden/field/level cap come from design/SPINE.md and are LOCKED: change the
# SPINE first, then this table.
#
# Save data: the plugin stores its state in $prismfall (see 002_SaveState.rb),
# never in Game Switches/Variables (101-300 belong to the story team).
#===============================================================================
module Prismfall
  CORE_VERSION = "1.0.0"

  #-----------------------------------------------------------------------------
  # Gyms (SPINE, LOCKED)
  #-----------------------------------------------------------------------------
  # :index        => gym number 1-18 (badge index = index - 1)
  # :trainer_type => trainer type ID of the Warden's gym battle (LEADER_<FIRSTNAME>)
  # :trainer_name => trainer name used in trainers.txt
  # :version      => Standard base version of the gym battle (difficulty
  #                  offsets are added automatically)
  # :rival_battle => if set, the gym battle uses the rival versioning scheme
  #                  (battle_number * 10 + starter_slot) instead of :version.
  #                  Gym 9 is Juno's J3 battle.
  # :double       => true = the Warden battle is a double battle (story: Gyms 2,
  #                  6, 11, 16 and 17). Prismfall.gym_battle sets the rule.
  BADGE_COUNT = 18

  GYMS = [
    { index: 1,  type: :BUG,      city: "Briarwick",   warden: "Tamsin Loom",      trainer_name: "Tamsin",    trainer_type: :LEADER_TAMSIN,    field: :SILKWOOD,         cap: 15, version: 0 },
    { index: 2,  type: :NORMAL,   city: "Saltmere",    warden: "Dorian Pell",      trainer_name: "Dorian",    trainer_type: :LEADER_DORIAN,    field: :GRAND_STAGE,      cap: 19, version: 0, double: true },
    { index: 3,  type: :WATER,    city: "Ebbmouth",    warden: "Marisol Reyes",    trainer_name: "Marisol",   trainer_type: :LEADER_MARISOL,   field: :WATER_SURFACE,    cap: 23, version: 0 },
    { index: 4,  type: :ELECTRIC, city: "Lumen City",  warden: "Rook Calder",      trainer_name: "Rook",      trainer_type: :LEADER_ROOK,      field: :NEON_GRID,        cap: 27, version: 0 },
    { index: 5,  type: :GROUND,   city: "Duneholt",    warden: "Sahar Ostrand",    trainer_name: "Sahar",     trainer_type: :LEADER_SAHAR,     field: :DESERT,           cap: 31, version: 0 },
    { index: 6,  type: :POISON,   city: "Mirefen",     warden: "Corvin Mott",      trainer_name: "Corvin",    trainer_type: :LEADER_CORVIN,    field: :CORROSIVE_MIRE,   cap: 35, version: 0, double: true },
    { index: 7,  type: :FIRE,     city: "Cindervault", warden: "Brann Holloway",   trainer_name: "Brann",     trainer_type: :LEADER_BRANN,     field: :VOLCANIC,         cap: 39, version: 0 },
    { index: 8,  type: :FIGHTING, city: "Ironreach",   warden: "Kaito Ren",        trainer_name: "Kaito",     trainer_type: :LEADER_KAITO,     field: :COLOSSEUM,        cap: 43, version: 0 },
    { index: 9,  type: :GRASS,    city: "Verdance",    warden: "Juno Hale",        trainer_name: "Juno",      trainer_type: :LEADER_JUNO,      field: :FLOWER_GARDEN,    cap: 47, version: 0, rival_battle: 3 },
    { index: 10, type: :ICE,      city: "Rimeholt",    warden: "Anja Sorrel",      trainer_name: "Anja",      trainer_type: :LEADER_ANJA,      field: :FROZEN_LAKE,      cap: 51, version: 0 },
    { index: 11, type: :FLYING,   city: "Skyreach",    warden: "Odessa Gale",      trainer_name: "Odessa",    trainer_type: :LEADER_ODESSA,    field: :STORMFRONT,       cap: 55, version: 0, double: true },
    { index: 12, type: :PSYCHIC,  city: "Lucent",      warden: "Ilsa Marr",        trainer_name: "Ilsa",      trainer_type: :LEADER_ILSA,      field: :MINDSCAPE,        cap: 59, version: 0 },
    { index: 13, type: :ROCK,     city: "Cragholm",    warden: "Bastian Ore",      trainer_name: "Bastian",   trainer_type: :LEADER_BASTIAN,   field: :CRYSTAL_CAVERN,   cap: 63, version: 0 },
    { index: 14, type: :GHOST,    city: "Gravenmoor",  warden: "Ysolde Ashgrave",  trainer_name: "Ysolde",    trainer_type: :LEADER_YSOLDE,    field: :HOLLOW_CATHEDRAL, cap: 67, version: 0 },
    { index: 15, type: :STEEL,    city: "Cogsworth",   warden: "Magnus Strade",    trainer_name: "Magnus",    trainer_type: :LEADER_MAGNUS,    field: :FACTORY,          cap: 71, version: 0 },
    { index: 16, type: :DARK,     city: "Underveil",   warden: "Nyx Calloway",     trainer_name: "Nyx",       trainer_type: :LEADER_NYX,       field: :NEW_MOON,         cap: 75, version: 0, double: true },
    { index: 17, type: :FAIRY,    city: "Gloaming",    warden: "Celestine Aubade", trainer_name: "Celestine", trainer_type: :LEADER_CELESTINE, field: :FAIRY_TALE,       cap: 80, version: 0, double: true },
    { index: 18, type: :DRAGON,   city: "Wyrmrest",    warden: "Sigrun Ashfall",   trainer_name: "Sigrun",    trainer_type: :LEADER_SIGRUN,    field: :DRAGONS_DEN,      cap: 85, version: 0 }
  ].each { |g| g.freeze }.freeze

  #-----------------------------------------------------------------------------
  # Field moves (HMs). Applied to Settings::BADGE_FOR_* at load time.
  #-----------------------------------------------------------------------------
  # true  = the number is "at least N badges owned".
  # false = the number is "gym N's badge specifically" (1-18, NOT 0-based here;
  #         converted to Essentials' 0-based badge index automatically).
  FIELD_MOVES_COUNT_BADGES = true
  # Values follow design/WORLD.md section 4 (badge counts).
  FIELD_MOVE_BADGES = {
    :CUT       => 1,    # HM01, Briarwick Cutter's House
    :ROCKSMASH => 2,    # TM98, Brinecut miner
    :FLASH     => 4,    # TM70, Rook Calder
    :STRENGTH  => 5,    # HM04, Duneholt excavators
    :SURF      => 6,    # HM03, Mirefen ferrymen
    :FLY       => 8,    # HM02, Skyreach courier
    :ROCKCLIMB => 10,   # TM100, Rimeholt ice-climbers (handler: 022_RockClimb.rb)
    :WATERFALL => 11,   # HM05, Skyreach sky-river guides
    :DIVE      => 15    # HM06, Cogsworth bathysphere works
  }

  #-----------------------------------------------------------------------------
  # Level caps
  #-----------------------------------------------------------------------------
  LEVEL_CAPS_ENABLED       = true
  FESTIVAL_CAP             = 90    # after Badge 18 and during the Festival bracket
  FESTIVAL_FINALE_CAP      = 100   # after Prismfall::LevelCap.unlock_finale!
  SHOW_CAP_IN_PAUSE_MENU   = true  # info box in the pause menu
  SHOW_CAP_EXP_MESSAGE     = true  # "X is at the level cap" once per battle per Pokémon
  ANNOUNCE_CAP_ON_BADGE    = true  # Prismfall.award_badge shows the new cap
  DAYCARE_RESPECTS_CAP     = true  # Day Care can't level past the cap
  RARE_CANDY_EVOLVES_AT_CAP = false # true = Rare Candy at cap only triggers a pending level evolution
  # Base Exp per EXP Candy (used to limit how many can be used at once).
  EXP_CANDY_AMOUNTS = {
    :EXPCANDYXS => 100,
    :EXPCANDYS  => 800,
    :EXPCANDYM  => 3_000,
    :EXPCANDYL  => 10_000,
    :EXPCANDYXL => 30_000
  }

  #-----------------------------------------------------------------------------
  # Difficulty modes
  #-----------------------------------------------------------------------------
  # Trainer variant scheme (SPINE, LOCKED): base version v = Standard,
  # v + 100 = Hard, v + 200 = Casual; falls back to v when the variant is
  # missing. Versions >= TRAINER_VARIANT_STRIDE are treated as explicit and are
  # never remapped.
  TRAINER_VARIANT_STRIDE = 100
  DIFFICULTY_ORDER       = [:CASUAL, :STANDARD, :HARD]
  DIFFICULTY_DEFAULT     = :STANDARD
  # :any        - the player may change difficulty freely (via Prismfall::Difficulty.change_menu)
  # :lower_only - may only switch to an easier mode
  # :locked     - chosen once at new game
  DIFFICULTY_CHANGE_RULE = :any

  # Per-mode tunables:
  #   :version_offset    trainer variant offset (SPINE: 0 / 100 / 200)
  #   :exp_multiplier    multiplier applied to battle Exp (before the cap clamp)
  #   :force_set_style   true = "Set" battle style is forced (unless a battle rule says otherwise)
  #   :trainer_bag_items false = Bag can't be used in trainer battles
  #   :obedience         true = Pokémon above (cap + :obedience_margin) may disobey
  #   :obedience_margin  levels above the cap that still obey
  #   :exp_at_cap        true = Pokémon keep gaining Exp past the cap (caps become soft)
  #   :candy_at_cap      true = Rare Candy / EXP Candy ignore the cap
  #   :cap_bonus         added to every gym level cap
  #   :ai_skill_min      minimum AI skill for NPC trainers (nil = unchanged; 48 = "high", 100 = "best")
  #   :ai_skill_max      maximum AI skill for NPC trainers (nil = unchanged)
  DIFFICULTIES = {
    :CASUAL => {
      :name              => "Casual",
      :description       => "Gentler teams, bonus Exp, Bag usable everywhere. For enjoying the story.",
      :version_offset    => 200,
      :exp_multiplier    => 1.5,
      :force_set_style   => false,
      :trainer_bag_items => true,
      :obedience         => false,
      :obedience_margin  => 0,
      :exp_at_cap        => false,
      :candy_at_cap      => false,
      :cap_bonus         => 0,
      :ai_skill_min      => nil,
      :ai_skill_max      => nil
    },
    :STANDARD => {
      :name              => "Standard",
      :description       => "The intended experience. Level caps and full trainer teams.",
      :version_offset    => 0,
      :exp_multiplier    => 1.0,
      :force_set_style   => false,
      :trainer_bag_items => true,
      :obedience         => true,
      :obedience_margin  => 0,
      :exp_at_cap        => false,
      :candy_at_cap      => false,
      :cap_bonus         => 0,
      :ai_skill_min      => nil,
      :ai_skill_max      => nil
    },
    :HARD => {
      :name              => "Hard",
      :description       => "Stronger teams, Set battle style, no Bag items in trainer battles.",
      :version_offset    => 100,
      :exp_multiplier    => 1.0,
      :force_set_style   => true,
      :trainer_bag_items => false,
      :obedience         => true,
      :obedience_margin  => 0,
      :exp_at_cap        => false,
      :candy_at_cap      => false,
      :cap_bonus         => 0,
      :ai_skill_min      => 48,
      :ai_skill_max      => nil
    }
  }

  #-----------------------------------------------------------------------------
  # Rival starter system (starters: any Gen 1-9 starter, SPINE Revision 2)
  #-----------------------------------------------------------------------------
  RIVAL_SWAP_ENABLED   = true
  # Trainer types whose Gen 1 starter-line Pokémon are swapped at battle start.
  RIVAL_TRAINER_TYPES  = [:RIVAL_KESTREL, :RIVAL_JUNO, :LEADER_JUNO]
  RIVAL_SOURCE_GEN     = 1       # PBS always writes the Gen 1 line
  DEFAULT_STARTER_GEN  = 1       # used if no starter was recorded/inferred
  DEFAULT_STARTER_SLOT = 0
  # Replacement for a Mega Stone that has no counterpart for the swapped
  # species (nil = remove the item).
  MEGA_STONE_FALLBACK_ITEM = :LIFEORB
  # Slot order (SPINE, LOCKED): 0 = Grass, 1 = Fire, 2 = Water
  STARTER_SLOT_TYPES = [:GRASS, :FIRE, :WATER]
  # gen => [grass line, fire line, water line], each line = [stage 0, stage 1, stage 2]
  # (IDs verified against the Gen 9 Pack PBS in /home/claude/ref/ebdx/PBS)
  STARTER_LINES = {
    1 => [[:BULBASAUR, :IVYSAUR,   :VENUSAUR],   [:CHARMANDER, :CHARMELEON, :CHARIZARD],  [:SQUIRTLE, :WARTORTLE,  :BLASTOISE]],
    2 => [[:CHIKORITA, :BAYLEEF,   :MEGANIUM],   [:CYNDAQUIL,  :QUILAVA,    :TYPHLOSION], [:TOTODILE, :CROCONAW,   :FERALIGATR]],
    3 => [[:TREECKO,   :GROVYLE,   :SCEPTILE],   [:TORCHIC,    :COMBUSKEN,  :BLAZIKEN],   [:MUDKIP,   :MARSHTOMP,  :SWAMPERT]],
    4 => [[:TURTWIG,   :GROTLE,    :TORTERRA],   [:CHIMCHAR,   :MONFERNO,   :INFERNAPE],  [:PIPLUP,   :PRINPLUP,   :EMPOLEON]],
    5 => [[:SNIVY,     :SERVINE,   :SERPERIOR],  [:TEPIG,      :PIGNITE,    :EMBOAR],     [:OSHAWOTT, :DEWOTT,     :SAMUROTT]],
    6 => [[:CHESPIN,   :QUILLADIN, :CHESNAUGHT], [:FENNEKIN,   :BRAIXEN,    :DELPHOX],    [:FROAKIE,  :FROGADIER,  :GRENINJA]],
    7 => [[:ROWLET,    :DARTRIX,   :DECIDUEYE],  [:LITTEN,     :TORRACAT,   :INCINEROAR], [:POPPLIO,  :BRIONNE,    :PRIMARINA]],
    8 => [[:GROOKEY,   :THWACKEY,  :RILLABOOM],  [:SCORBUNNY,  :RABOOT,     :CINDERACE],  [:SOBBLE,   :DRIZZILE,   :INTELEON]],
    9 => [[:SPRIGATITO, :FLORAGATO, :MEOWSCARADA], [:FUECOCO,  :CROCALOR,   :SKELEDIRGE], [:QUAXLY,   :QUAXWELL,   :QUAQUAVAL]]
  }

  #-----------------------------------------------------------------------------
  # Trainer Card (18 badges, 2 rows of 9)
  #-----------------------------------------------------------------------------
  # Badge sheet: Graphics/UI/Trainer Card/icon_badges_18.png
  #   (BADGE_COLS * 32) x (BADGE_ROWS * 32) = 288x64, badge i at
  #   column i % 9, row i / 9. Falls back to the vanilla icon_badges.png
  #   (8 per row) if missing.
  # Optional slot frame: Graphics/UI/Trainer Card/icon_badge_slot.png (32x32);
  #   if missing, a faint box is drawn in code.
  module TrainerCardLayout
    SHEET          = "Graphics/UI/Trainer Card/icon_badges_18"
    SHEET_FALLBACK = "Graphics/UI/Trainer Card/icon_badges"
    SLOT_FRAME     = "Graphics/UI/Trainer Card/icon_badge_slot"
    ICON_SIZE      = 32
    COLS           = 9
    ROWS           = 2
    ORIGIN_X       = 64    # left edge of badge 1
    ORIGIN_Y       = 294   # top edge of row 1
    SPACING_X      = 44
    SPACING_Y      = 38
    DRAW_EMPTY_SLOTS = true
    EMPTY_SLOT_COLOR = [0, 0, 0, 48]
  end
end
