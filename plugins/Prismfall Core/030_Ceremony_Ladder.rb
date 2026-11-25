#===============================================================================
# Prismfall Core - 030 Chapter 20: the Opening Ceremony's data, the consent
# banners, and the Grounds Ladder
#-------------------------------------------------------------------------------
# story/39_SCRIPT_CH20.md "Day 1: The Opening Ceremony" (the procession table),
# "Day 0: Arrival" (the Consent display) and "Rosters (Ch20)" (the Grounds Ladder).
# This file is data and rules only; the map side that walks the 18 Warden events
# and lights the pylons is mapgen/ruby/018_Crownhaven.rb (pf_ceremony_*).
#
# THE PROCESSION  Prismfall::Ceremony.procession -> 18 rows in gym order:
#   { :gym, :warden (Symbol), :name, :plate ("Blank" ...), :type, :color [r, g, b],
#     :bearer  (the event that carries the reliquary: the Warden, or "Meridian officer"
#               for a fired Rook, or "Choir porter" unless CORVIN_FREED),
#     :watcher (a Warden who only watches from the crowd, else nil),
#     :with    (events that walk beside the bearer: Pip, Magnus's guards),
#     :staging (the script's one line of staging, for the map builder) }
#
# THE BANNERS  Prismfall::Ceremony.banner(gym) -> { :color => :white / :grey, :line }
#   White = that Warden would let go (WARDEN_CONSENT, NARRATIVE_KEYS section 5; the same
#   reading the pylons show in Chapter 21). pf_banner_white?(gym) for page conditions,
#   pf_banner_read(gym) for the interact. Before Day 1 every banner still hangs in
#   its kingdom colour ("Look at the colours tomorrow").
#
# THE GROUNDS LADDER  12 open challengers in the kingdom pavilions, Lv 88-90.
#   Prismfall::GroundsLadder.challenge(:WEAVER)   one pavilion's challenger (its kingdom's field)
#   Prismfall::GroundsLadder.run                  climb from the lowest unbeaten rung, one after
#                                                 another, until a loss or "That's enough"
#   .beaten?(:WEAVER)  .count  .cleared?  .next_rung
#   pf_ladder(:WEAVER) / pf_ladder_run / pf_ladder_beaten?(:WEAVER) / pf_ladder_count
#   The teams are PBS (tools/trainer_gen): ROSTER names each one as [type, "Name", version].
#   A challenger whose PBS block doesn't exist yet is "not at the pavilion" (a line, no
#   battle, no crash) and doesn't count against clearing the Ladder.
#===============================================================================
module Prismfall
  module Ceremony
    # Gym order. :plate is the Plate's short name in the script's table; :color is its pylon light.
    PLATES = [
      [:DORIAN,    "Blank",  :NORMAL,   [220, 220, 200], "bowing to all four sides"],
      [:TAMSIN,    "Insect", :BUG,      [168, 200, 48],  "pins still in her sleeve"],
      [:MARISOL,   "Splash", :WATER,    [64, 144, 240],  nil],
      [:ROOK,      "Zap",    :ELECTRIC, [248, 208, 48],  "the Plate still cracked, in a cradle"],
      [:SAHAR,     "Earth",  :GROUND,   [224, 192, 104], nil],
      [:CORVIN,    "Toxic",  :POISON,   [160, 64, 160],  nil],
      [:BRANN,     "Flame",  :FIRE,     [240, 128, 48],  nil],
      [:KAITO,     "Fist",   :FIGHTING, [192, 48, 40],   nil],
      [:JUNO,      "Meadow", :GRASS,    [120, 200, 80],  nil],
      [:ANJA,      "Icicle", :ICE,      [152, 216, 216], nil],
      [:ODESSA,    "Sky",    :FLYING,   [168, 144, 240], nil],
      [:ILSA,      "Mind",   :PSYCHIC,  [248, 88, 136],  nil],
      [:BASTIAN,   "Stone",  :ROCK,     [184, 160, 56],  "leaning on Pip"],
      [:YSOLDE,    "Spooky", :GHOST,    [112, 88, 152],  nil],
      [:MAGNUS,    "Iron",   :STEEL,    [184, 184, 208], nil],
      [:NYX,       "Dread",  :DARK,     [112, 88, 72],   nil],
      [:CELESTINE, "Pixie",  :FAIRY,    [238, 153, 172], nil],
      [:SIGRUN,    "Draco",  :DRAGON,   [112, 56, 248],  nil]
    ].freeze

    # Why a banner hangs grey: Tamsin's reading of her colleagues (story/11_FINALE_LINES.md section 2, the causes).
    GREY_REASONS = [
      "You told the pageant version, on record. So did he, for thirty years.",
      "The contract's still running. There's nothing left in the village but this.",
      "Her brother's in the river mud because of what this thing started.",
      "His Plate sits in someone else's cradle. He can't reach it.",
      "She buried the truth once because a badge asked. You stood with the badge.",
      "A porter wears his mask. Nobody told the porter how.",
      "You gave his guild's Light away to a king.",
      "He never said it out loud. Marrowgate.",
      "She let go of the dock you both started on. She won't let go of this.",
      "Rimeholt drowns without it. Ice remembers.",
      "You burned a dead letter. She doesn't hand things to people who burn them.",
      "Her father is dying on that Ring for a country that never thanked him.",
      "A Meridian beacon walked into his seams, and they came for his people by it.",
      "She was asked to keep one boy safe.",
      "He won't hand his city's future to a god.",
      "Everything has a price, and hers was never paid.",
      "She cannot lie: she hears a song in the wrong key.",
      "An oath was sworn over her fire. She believed it."
    ].freeze

    def self.warden_name(sym)
      return sym.to_s.capitalize
    end

    def self.consent?(gym)
      cond = Prismfall::Narrative::WARDEN_CONSENT[gym - 1]
      return true if !cond
      return (Prismfall::Conditions.evaluate(cond) rescue true) ? true : false
    end

    def self.row(gym)
      w, plate, type, color, staging = PLATES[gym - 1]
      return nil if !w
      name = warden_name(w)
      r = { :gym => gym, :warden => w, :name => name, :plate => plate, :type => type, :color => color,
            :bearer => name, :watcher => nil, :with => [], :staging => staging }
      case w
      when :ROOK
        if Prismfall::Choices.get(:ch16_rook) == :leak_now   # fired: an officer carries it, Rook watches with his collar up
          r[:bearer]  = "Meridian officer"
          r[:watcher] = name
          r[:staging] = "a Meridian officer carries the cracked Plate; Rook watches from the crowd with his collar up"
        end
      when :CORVIN
        if !Prismfall::Narrative.flag(:CORVIN_FREED)
          r[:bearer]  = "Choir porter"
          r[:staging] = "carried by a Choir porter in Corvin's mask"
        end
      when :BASTIAN
        r[:with] = ["Pip"]
      when :MAGNUS
        if Prismfall::Narrative.flag(:MAGNUS_EXPOSED)
          r[:with]    = ["Magnus guard 1", "Magnus guard 2"]
          r[:staging] = "under guard"
        end
      end
      return r
    end

    def self.procession
      return (1..18).map { |g| row(g) }
    end

    # The Festival day, 0 before it has started (Festival.day alone answers 1 then).
    def self.day
      return 0 if !(Prismfall::Festival.started? rescue false)
      return (Prismfall::Festival.day rescue 0).to_i
    end

    # The woven banner for a gym: its colour today and what reading it says.
    def self.banner(gym)
      r = row(gym)
      return nil if !r
      if day < 1
        return { :color => :kingdom,
                 :line => _INTL("The {1} banner. Every thread is Tamsin's. The dye is still drying.", r[:plate]) }
      end
      if consent?(gym)
        return { :color => :white,
                 :line => _INTL("The {1} banner hangs white. {2} would let go.", r[:plate], r[:name]) }
      end
      return { :color => :grey,
               :line => _INTL("The {1} banner hangs grey. {2}", r[:plate], _INTL(GREY_REASONS[gym - 1])) }
    end

    def self.read_banner(gym)
      b = banner(gym)
      pbMessage(b[:line]) if b
      return b ? b[:color] : nil
    end

    def self.white_count
      return (1..18).count { |g| consent?(g) }
    end
  end

  #=============================================================================
  # The Grounds Ladder
  #=============================================================================
  module GroundsLadder
    VERSION = 20   # the PBS version of every Ladder team (Hard / Casual at +100 / +200 as usual)

    # Rung order = the script's roster table. :trainer is [type, "Name", version]; :types lists other trainer
    # types the same name may be filed under. Fields are each kingdom's Imprint, as their pavilion flies it.
    ROSTER = [
      { :key => :WEAVER,     :kingdom => "Elowen",     :who => "a Briarwick weaver",
        :trainer => [:PAINTER, "Linnet", VERSION],      :field => :SILKWOOD },
      { :key => :HARPOONER,  :kingdom => "Isenmar",    :who => "a Rimeholt harpooner",
        :trainer => [:FISHERMAN, "Brynjar", VERSION],   :field => :FROZEN_LAKE },
      { :key => :STREAMER,   :kingdom => "Zenith",     :who => "a Lumen streamer",
        :trainer => [:ROCKER, "Vix", VERSION],          :field => :NEON_GRID },
      { :key => :FOREMAN,    :kingdom => "Zenith",     :who => "a Cogsworth foreman",
        :trainer => [:ENGINEER, "Dobbin", VERSION],     :field => :FACTORY },
      { :key => :BROKER,     :kingdom => "Nadir",      :who => "a Moon Market broker",
        :trainer => [:GAMBLER, "Quill", VERSION],       :field => :NEW_MOON },
      { :key => :RIDER,      :kingdom => "Ashkaar",    :who => "a Wyrmrest rider",
        :trainer => [:TAMER, "Asgerd", VERSION],        :field => :DRAGONS_DEN },
      { :key => :LAMPRUNNER, :kingdom => "Ossaria",    :who => "a Cragholm lamp-runner (Pip's rival)",
        :trainer => [:YOUNGSTER, "Tam", VERSION],       :field => :CRYSTAL_CAVERN },
      { :key => :WELLKEEPER, :kingdom => "Ossaria",    :who => "a Duneholt well-keeper",
        :trainer => [:RUINMANIAC, "Nasrin", VERSION],   :field => :DESERT },
      { :key => :PRIEST,     :kingdom => "Antumbra",   :who => "a Gravenmoor lantern-priest",
        :trainer => [:CHANNELER, "Osric", VERSION],     :field => :HOLLOW_CATHEDRAL },
      { :key => :EMBALMER,   :kingdom => "Antumbra",   :who => "a Vigil embalmer",
        :trainer => [:SCIENTIST, "Thessaly", VERSION],  :field => :HOLLOW_CATHEDRAL },
      { :key => :WARDGUARD,  :kingdom => "Crownhaven", :who => "a Wardguard",
        :trainer => [:COOLTRAINER_M, "Halvard", VERSION], :field => :GRAND_STAGE },
      { :key => :CANTOR,     :kingdom => "Crownhaven", :who => "a Choir cantor",
        :trainer => [:LADY, "Liesl", VERSION],          :field => [:HOLLOW_CATHEDRAL, 2] }
    ]

    @answers = []   # scripted answers for run's "Next challenger?" (headless tests)

    class << self
      attr_accessor :answers

      def store
        c = Prismfall.state.custom
        c[:grounds_ladder] = {} if !c[:grounds_ladder].is_a?(Hash)
        return c[:grounds_ladder]
      end

      def rung(key)
        return ROSTER[key] if key.is_a?(Integer)
        return ROSTER.find { |r| r[:key] == key.to_sym }
      end

      # The PBS trainer for a rung: the exact key, else the same name under another type or version
      # (the PBS writer may have filed "Linnet" differently), else nil.
      def resolve(r)
        type, name, version = r[:trainer]
        return [type, name, version] if GameData::Trainer.exists?(type, name, version)
        Array(r[:types]).each { |t| return [t, name, version] if GameData::Trainer.exists?(t, name, version) }
        found = nil
        GameData::Trainer.each do |t|
          next if t.real_name != name
          next if t.version >= 100                      # difficulty variants are picked at load, not here
          found = [t.trainer_type, t.real_name, t.version] if !found || t.version == version
        end
        return found
      end

      def present?(key)
        r = rung(key)
        return (r && resolve(r)) ? true : false
      end

      def beaten?(key)
        r = rung(key)
        return (r && store[r[:key]]) ? true : false
      end

      def count
        return ROSTER.count { |r| store[r[:key]] }
      end

      def present_rungs
        return ROSTER.select { |r| resolve(r) }
      end

      # Every challenger who is at the grounds has been beaten (and at least one is).
      def cleared?
        here = present_rungs
        return !here.empty? && here.all? { |r| store[r[:key]] }
      end

      def next_rung
        return present_rungs.find { |r| !store[r[:key]] }
      end

      def set_field(field)
        return if field.nil? || !defined?(FieldEffects)
        id, stage = (field.is_a?(Array)) ? field : [field, nil]
        setBattleRule("field", id)
        setBattleRule("fieldstage", stage) if stage
      end

      # One pavilion's challenger. Returns true on a win, false on a loss, nil if nobody is there.
      def challenge(key, rematch: false)
        r = rung(key)
        raise ArgumentError, "Unknown Grounds Ladder rung #{key.inspect}" if !r
        spec = resolve(r)
        if !spec
          pbMessage(_INTL("The {1} pavilion's challenger hasn't come down to the grounds yet.", _INTL(r[:kingdom])))
          return nil
        end
        if store[r[:key]] && !rematch
          pbMessage(_INTL("You've already climbed past {1}.", spec[1]))
          return true
        end
        first_clear = !cleared?
        setBattleRule("canLose")
        set_field(r[:field])
        won = TrainerBattle.start(spec) ? true : false
        if won
          store[r[:key]] = true
          if first_clear && cleared?
            pbMessage("\\me[Slots win]" + _INTL("The Grounds Ladder is climbed. All {1} pavilions lower their challenge flags.", present_rungs.length))
            EventHandlers.trigger(:prismfall_grounds_ladder_cleared)
          end
        else
          $player.heal_party if $player     # the grounds have healers; an open challenge never blacks you out
        end
        return won
      end

      def ask_next(r, spec)
        if @answers && !@answers.empty?
          return @answers.shift ? true : false
        end
        return true if defined?(Harness)
        msg = _INTL("Next on the Ladder: {1} of {2}, {3}. Climb?", spec[1], _INTL(r[:kingdom]), _INTL(r[:who]))
        return pbMessage(msg, [_INTL("Climb"), _INTL("That's enough")], 2) == 0
      end

      # The challengers in sequence, from the lowest unbeaten rung. Returns how many were beaten this climb.
      def run(heal_between: false)
        beaten = 0
        if !next_rung
          pbMessage(cleared? ? _INTL("Every pavilion's flag is down. The Ladder is yours.")
                             : _INTL("No challenger is waiting at the pavilions yet."))
          return 0
        end
        while (r = next_rung)
          spec = resolve(r)
          break if !ask_next(r, spec)
          won = challenge(r[:key])
          break if !won
          beaten += 1
          $player.heal_party if heal_between && $player
        end
        return beaten
      end
    end
  end
end

def pf_banner_white?(gym); return Prismfall::Ceremony.consent?(gym);      end
def pf_banner_read(gym);   return Prismfall::Ceremony.read_banner(gym);   end
def pf_ladder(key, **opts);  return Prismfall::GroundsLadder.challenge(key, **opts); end
def pf_ladder_run(**opts);   return Prismfall::GroundsLadder.run(**opts);            end
def pf_ladder_beaten?(key);  return Prismfall::GroundsLadder.beaten?(key);           end
def pf_ladder_count;         return Prismfall::GroundsLadder.count;                  end
