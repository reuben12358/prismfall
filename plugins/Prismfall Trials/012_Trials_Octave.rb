#===============================================================================
# Prismfall Trials - 012 The Eevee Octave (SPINE Revision 19)
#-------------------------------------------------------------------------------
# Eight singers of the Prism Choir, one per kingdom, each with an Eeveelution
# raised beside that kingdom's Imprint. Each has a quest on their kingdom's
# Trial board (113_Quests_Octave.rb; map events: 151_Talk_Octave.rb). The order the player helps them in is
# kept here; once all eight are helped, Vesper Lindqvist waits in the Glassfall
# Memorial Garden (Crownhaven, 489) with the gauntlet: the eight singers in that
# order, then her own Eevee, back to back with no healing. Each singer's
# Eeveelution holds its type's Z-crystal; Vesper's Eevee has the Eevium Z.
# Design: design/EEVEE_OCTAVE.md. Z-moves: plugins/Prismfall Z-Power.
# Save data: Prismfall.state.trials[:octave] = [singer ids in the order helped].
# Script commands:   { :octave_help => :LYRA }
#                    { :octave_gauntlet => true, :won => [...], :lost => [...] }
#                    { :octave_verses => { :LYRA => { :run => :verse_lyra }, ... } }   (in help order)
# Conditions:        octave_helped (count)   octave_has(:LYRA)   octave_pos(:LYRA)   octave_ready
#===============================================================================
module Prismfall
  module Trials
    module Octave
      # In gym order (the order most players will meet them). :field is the field of the singer's gauntlet bout:
      # the Imprint their Eeveelution was raised beside (design/TRAINER_FIELD_PLAYBOOK.md section 6).
      SINGERS = {
        :LYRA    => { :name => "Lyra",    :species => :LEAFEON,  :trial => :ELOWEN,     :quest => :EL_OCTAVE_MOSS,
                      :where => "Briarwick",                                :field => [:FLOWER_GARDEN, 3], :chapter => 3 },
        :ARIA    => { :name => "Aria",    :species => :VAPOREON, :trial => :ISENMAR,    :quest => :IS_OCTAVE_DROWNED_NOTE,
                      :where => "Ebbmouth",                                 :field => :WATER_SURFACE,      :chapter => 4 },
        :CADENCE => { :name => "Cadence", :species => :JOLTEON,  :trial => :ZENITH,     :quest => :ZE_OCTAVE_OFF_BEAT,
                      :where => "the Lowlight, Lumen City",                 :field => :NEON_GRID,          :chapter => 5 },
        :SONA    => { :name => "Sona",    :species => :ESPEON,   :trial => :OSSARIA,    :quest => :OS_OCTAVE_NOON_BELL,
                      :where => "the Temple of the Noon Sun, Duneholt",     :field => :MINDSCAPE,          :chapter => 6 },
        :NOCT    => { :name => "Noct",    :species => :UMBREON,  :trial => :NADIR,      :quest => :NA_OCTAVE_LAMPS_OUT,
                      :where => "the ferry steps, Mirefen",                 :field => :NEW_MOON,           :chapter => 7 },
        :FORTE   => { :name => "Forte",   :species => :FLAREON,  :trial => :ASHKAAR,    :quest => :AS_OCTAVE_TOO_LOUD,
                      :where => "the Crucible, Cindervault",                :field => :VOLCANIC,           :chapter => 8 },
        :LENTO   => { :name => "Lento",   :species => :GLACEON,  :trial => :ANTUMBRA,   :quest => :AN_OCTAVE_STILL_WATER,
                      :where => "the Mirror Mere",                          :field => :FROZEN_LAKE,        :chapter => 13 },
        :CAROL   => { :name => "Carol",   :species => :SYLVEON,  :trial => :CROWNHAVEN, :quest => :CR_OCTAVE_NINTH_VERSE,
                      :where => "the Glassfall Memorial Garden, Crownhaven", :field => :FAIRY_TALE,        :chapter => 20 }
      }.freeze
      LAST     = :CAROL                                # always helped last: her quest needs the other seven
      TRACKER  = :CR_OCTAVE                            # "The Eevee Octave": Vesper's request and the gauntlet
      GAUNTLET_TYPE    = :OCTAVE_SINGER
      GAUNTLET_VERSION = 60
      HOST       = [:OCTAVE_VESPER, "Vesper", 60]
      HOST_FIELD = :GRAND_STAGE                        # where the Octave began: Saltmere's stage, Chapter 2

      def self.order
        st = Prismfall::Trials.store
        st[:octave] = [] if !st[:octave].is_a?(Array)
        return st[:octave]
      end

      def self.helped?(id);  return order.include?(id.to_sym);  end
      def self.count;        return order.length;                end
      def self.ready?;       return SINGERS.keys.all? { |id| helped?(id) }; end
      def self.position(id); i = order.index(id.to_sym); return (i) ? i + 1 : 0; end

      # The others, in gym order, not yet helped.
      def self.missing(except = LAST)
        return SINGERS.keys.reject { |id| id == except || helped?(id) }
      end

      # Records a singer as helped (once). Returns their place in the order.
      def self.help(id)
        id = id.to_sym
        raise ArgumentError, "Unknown Octave singer #{id.inspect}" if !SINGERS[id]
        return position(id) if helped?(id)
        order.push(id)
        tr = Prismfall::Trials
        tr.start(TRACKER, false) if tr.exists?(TRACKER) && !tr.active?(TRACKER) && !tr.done?(TRACKER)
        tr.set_step(TRACKER, :garden) if ready? && tr.active?(TRACKER)
        tr.refresh_map
        return order.length
      end

      def self.bout_specs
        return order.map { |id| [GAUNTLET_TYPE, SINGERS[id][:name], GAUNTLET_VERSION] } + [HOST]
      end

      def self.species_name(sp)
        return (GameData::Species.exists?(sp)) ? GameData::Species.get(sp).name : sp.to_s.capitalize
      end

      # The chained battles. No healing between bouts; a loss ends it (Trials heals the party: quest losses never black out).
      def self.run_gauntlet
        return false if !ready?
        tr = Prismfall::Trials
        total = order.length + 1
        order.each_with_index do |id, i|
          s = SINGERS[id]
          pbMessage(_INTL("Bout {1} of {2}: {3} and {4}!", i + 1, total, s[:name], species_name(s[:species])))
          return false if !tr.trainer_battle([GAUNTLET_TYPE, s[:name], GAUNTLET_VERSION], field: s[:field])
        end
        pbMessage(_INTL("Bout {1} of {1}: Vesper and Amen!", total))
        return tr.trainer_battle(HOST, field: HOST_FIELD)
      end

      def self.reset   # debug
        order.clear
        Prismfall::Trials.refresh_map
      end
    end

    #---------------------------------------------------------------------------
    # Script commands
    #---------------------------------------------------------------------------
    Script::COMMANDS[:octave_help] = proc { |e, _ctx|
      id = e[:octave_help]
      first = !Octave.helped?(id)
      n = Octave.help(id)
      if first
        name = Octave::SINGERS[id.to_sym][:name]
        pbMessage(_INTL("(The Octave will remember that you helped {1}: {2} of {3}.)", name, n, Octave::SINGERS.length))
      end
    }
    Script::COMMANDS[:octave_gauntlet] = proc { |e, ctx|
      won = Octave.run_gauntlet
      Script.exec(won ? (e[:won] || []) : (e[:lost] || []), ctx)
    }
    # Runs one entry per singer, in the order the player helped them (singers not yet helped are skipped).
    Script::COMMANDS[:octave_verses] = proc { |e, ctx|
      Octave.order.each do |id|
        entry = e[:octave_verses][id]
        Script.exec_one(entry, ctx) if entry
      end
    }
  end

  module Conditions
    oc = Prismfall::Trials::Octave
    {
      "octave_helped" => [0, proc { oc.count }],
      "octave_has"    => [1, proc { |id| oc.helped?(id) }],
      "octave_pos"    => [1, proc { |id| oc.position(id) }],
      "octave_ready"  => [0, proc { oc.ready? }]
    }.each { |name, fn| FUNCTIONS[name] = fn }
  end
end

MenuHandlers.add(:debug_menu, :prismfall_trials_octave, {
  "name"        => _INTL("Eevee Octave..."),
  "parent"      => :prismfall_trials_menu,
  "description" => _INTL("See or set the order you helped the Octave's singers in."),
  "effect"      => proc {
    oc = Prismfall::Trials::Octave
    pbMessage(_INTL("Helped ({1}/8): {2}", oc.count, oc.order.map { |id| oc::SINGERS[id][:name] }.join(", ")))
    opts = [_INTL("Help the next singer (gym order)"), _INTL("Help all eight"), _INTL("Reset the order")]
    case pbMessage(_INTL("Octave?"), opts, -1)
    when 0
      nxt = oc::SINGERS.keys.find { |id| !oc.helped?(id) }   # Carol is last in the table
      oc.help(nxt) if nxt
    when 1 then oc::SINGERS.keys.each { |id| oc.help(id) }
    when 2 then oc.reset
    end
  }
})
