#===============================================================================
# PRISM_ARENA - Crownhaven, the Festival of Champions finale (hijack + Arceus).
# The 18 Plates hang in a ring overhead. After a 3-round opening they "turn"
# every 3 rounds: the arena borrows the next GYM field's effects, in a fixed,
# curated order, and every turn is announced one round in advance. Built on the
# :borrow mechanism (like :BLEED) but sequential and hook-driven; works with
# whichever gym fields are registered (missing ones are skipped).
#-------------------------------------------------------------------------------
# BOSS / STORY CONTRACT  (Arceus's type follows the ascendant Plate)
#   FieldEffects.state(battle)[:prism] -> Hash, present while PRISM_ARENA is the
#   current field (nil otherwise):
#     :field        gym field ID currently borrowed (nil during the opening)
#     :type         that field's gym type (SPINE table); :NORMAL when none
#     :plate        that type's Plate item; :LEGENDPLATE when none
#     :next_field, :next_type, :next_plate   what the next turn brings
#     :rounds_left  end-of-rounds until the next turn
#     :rotation     number of turns so far
#     :interval     rounds per turn (default 3). WRITABLE - applied from the next turn
#     :telegraph    rounds of warning before a turn (default 1; at most :interval - 1).
#                   WRITABLE. 2 = "begins to glow... In two turns", then "glows brighter"
#                   the round before (Bosses :prism_telegraph; Arceus on Casual, BALANCE.md section 7)
#     :type_map     { gym_field_id => type },  :plate_map { type => plate item }
#     :turn         lambda { |battle| } - turn the Plates NOW (announced, re-types
#                   Multitype). Use this rather than FieldEffects.rotate_borrowed,
#                   e.g. when a boss HP bar breaks.
#     :order        the gym fields the arena is cycling through now (default: the
#                   curated order below), :mode  :curated / :gym_order / :custom
#     :gym_order    the 18 gym fields in GYM order (Core's GYMS: Grand Stage,
#                   Silkwood, Water Surface ... Dragon's Den)
#     :set_order    lambda { |battle, fields, mode = :custom, start = nil| } - cycle
#                   only among `fields`, from the first one (or from `start`, a field
#                   of the list, then on in list order), starting with the NEXT turn
#                   (call :turn afterwards to go there at once). The True Finale uses it:
#                   bar k of Arceus holds the Plates of gyms 3k-2..3k, so within a
#                   bar the arena cycles those three fields in gym order (Bosses
#                   :prism_order, design/BALANCE.md section 7). nil/[] = curated.
#   FieldEffects.prism_state(battle) is a frozen SUMMARY for read-only callers;
#   anything that turns the Plates or writes :interval needs the live Hash above.
#   The hash is updated BEFORE the engine rotates, so a handler on
#   :prismfall_field_overlay_changed already sees the new :type/:plate.
#   Battlers with Multitype are re-typed automatically (pbChangeTypes) on every
#   turn and on entry; the boss plugin only has to swap Arceus's form/sprite.
#   Judgment (and Nature Power -> Judgment) takes the ascendant Plate's type.
# (Helpers inside the lambda so they don't leak into TOPLEVEL_BINDING.)
#===============================================================================
FieldEffects.register(:PRISM_ARENA, (lambda do
  # Curated order: the starter triangle opens, Dragon's Den is the climax and the
  # Grand Stage the curtain call. No two consecutive types (wrap-around included)
  # share a weakness, so no single counter-type covers two turns in a row - the
  # player has to re-plan every turn, and so does the attuned boss.
  order = [:VOLCANIC, :WATER_SURFACE, :FLOWER_GARDEN, :NEON_GRID, :FROZEN_LAKE, :COLOSSEUM,
           :DESERT, :CORROSIVE_MIRE, :STORMFRONT, :MINDSCAPE, :SILKWOOD, :CRYSTAL_CAVERN,
           :HOLLOW_CATHEDRAL, :NEW_MOON, :FAIRY_TALE, :FACTORY, :DRAGONS_DEN, :GRAND_STAGE]
  types = { :SILKWOOD => :BUG, :GRAND_STAGE => :NORMAL, :WATER_SURFACE => :WATER, :NEON_GRID => :ELECTRIC,
            :DESERT => :GROUND, :CORROSIVE_MIRE => :POISON, :VOLCANIC => :FIRE, :COLOSSEUM => :FIGHTING,
            :FLOWER_GARDEN => :GRASS, :FROZEN_LAKE => :ICE, :STORMFRONT => :FLYING, :MINDSCAPE => :PSYCHIC,
            :CRYSTAL_CAVERN => :ROCK, :HOLLOW_CATHEDRAL => :GHOST, :FACTORY => :STEEL, :NEW_MOON => :DARK,
            :FAIRY_TALE => :FAIRY, :DRAGONS_DEN => :DRAGON }.freeze
  plates = { :BUG => :INSECTPLATE, :NORMAL => :BLANKPLATE, :WATER => :SPLASHPLATE, :ELECTRIC => :ZAPPLATE,
             :GROUND => :EARTHPLATE, :POISON => :TOXICPLATE, :FIRE => :FLAMEPLATE, :FIGHTING => :FISTPLATE,
             :GRASS => :MEADOWPLATE, :ICE => :ICICLEPLATE, :FLYING => :SKYPLATE, :PSYCHIC => :MINDPLATE,
             :ROCK => :STONEPLATE, :GHOST => :SPOOKYPLATE, :STEEL => :IRONPLATE, :DARK => :DREADPLATE,
             :FAIRY => :PIXIEPLATE, :DRAGON => :DRACOPLATE }.freeze
  interval = 3
  # Gym order (the True Finale's locks): Core's GYMS when it is loaded, else the SPINE Rev 14 table.
  gym_order = lambda do
    list = (defined?(Prismfall::GYMS) ? Prismfall::GYMS.sort_by { |g| g[:index] }.map { |g| g[:field] } : nil)
    list = nil if !list || list.length != 18 || !list.all? { |f| types[f] }
    list || [:GRAND_STAGE, :SILKWOOD, :WATER_SURFACE, :NEON_GRID, :DESERT, :CORROSIVE_MIRE, :VOLCANIC, :COLOSSEUM,
             :FLOWER_GARDEN, :FROZEN_LAKE, :STORMFRONT, :MINDSCAPE, :CRYSTAL_CAVERN, :HOLLOW_CATHEDRAL, :FACTORY,
             :NEW_MOON, :FAIRY_TALE, :DRAGONS_DEN]
  end

  prism     = lambda { |battle| FieldEffects.state(battle)[:prism] }
  item_name = lambda { |item| GameData::Item.get(item).name }
  ascendant = lambda { |battle| (pr = prism.call(battle)) && pr[:field] ? pr : nil }

  # The field the engine's sequential rotation picks `ahead` turns from now.
  peek = lambda do |battle, ahead|
    spec = FieldEffects.current_definition(battle)&.[](:borrow)
    next nil if !spec
    pool = FieldEffects.borrow_pool(battle, spec)
    next nil if pool.empty?
    pool[(battle.fe_state[:borrow_cursor] + ahead) % pool.length]
  end

  set_current = lambda do |pr, field|
    pr[:field] = field
    pr[:type]  = (field && types[field]) || :NORMAL
    pr[:plate] = (field && plates[pr[:type]]) || :LEGENDPLATE
  end

  set_next = lambda do |pr, field|
    pr[:next_field] = field
    pr[:next_type]  = field && types[field]
    pr[:next_plate] = field && plates[types[field]]
  end

  # Narrow (or restore) the cycle. The next turn takes fields[0] (or `start`, then on in list order); nothing
  # changes until then.
  set_order = lambda do |battle, fields, mode = :custom, start = nil|
    pr = prism.call(battle)
    next false if !pr || !FieldEffects.field_is?(battle, :PRISM_ARENA)
    list = Array(fields).select { |f| types[f] && FieldEffects.exists?(f) }
    if list.empty?
      list = order
      mode = :curated
    end
    battle.fe_state[:borrow_pool]   = (mode == :curated) ? nil : list.dup
    battle.fe_state[:borrow_cursor] = (start && list.index(start)) || 0
    pr[:order] = list.dup
    pr[:mode]  = mode
    set_next.call(pr, peek.call(battle, 0))
    true
  end

  attune = lambda do |battle, battler|
    pr = ascendant.call(battle)
    next false if !pr || battler.fainted? || !battler.hasActiveAbility?(:MULTITYPE)
    next false if battler.pbTypes == [pr[:type]]
    battler.pbChangeTypes(pr[:type])
    battle.pbDisplay(FieldEffects.format("{1}'s Multitype resonated with the {2}! It became the {3} type!",
                                         battler.pbThis, item_name.call(pr[:plate]),
                                         GameData::Type.get(pr[:type]).name))
    true
  end

  turn = lambda do |battle|
    pr = prism.call(battle)
    next false if !pr || !FieldEffects.field_is?(battle, :PRISM_ARENA)
    upcoming = peek.call(battle, 0)
    next false if !upcoming
    pr[:rotation]   += 1
    pr[:rounds_left] = pr[:interval]
    set_current.call(pr, upcoming)
    set_next.call(pr, peek.call(battle, 1))
    battle.pbDisplay(FieldEffects.format("The Plates turn! The {1} blazes, and the arena becomes the {2}!",
                                         item_name.call(pr[:plate]), FieldEffects.name_of(upcoming)))
    FieldEffects.rotate_borrowed(battle)
    actual = battle.fe_state[:borrowed].first
    if actual != upcoming   # Shouldn't happen; stay truthful if it does
      set_current.call(pr, actual)
      set_next.call(pr, peek.call(battle, 0))
    end
    battle.allBattlers.each { |b| attune.call(battle, b) }
    true
  end

  {
    :name          => "Prism Arena",
    :backdrop      => "field_prism_arena",
    :family        => :magical,
    :intro_message => "The eighteen Plates blaze in a ring above Crownhaven's arena!",
    :description   => "The Festival finale. Every 3 turns the Plates turn and the arena takes on the next gym field, in a fixed order announced a turn ahead.",
    :notes         => ["Opening: the Plates rest for 3 turns. Then every 3 turns they turn, and the arena takes on a gym field's effects.",
                       "Each turn is announced one turn ahead. Fixed order: Fire, Water, Grass, Electric, Ice, Fighting, Ground, Poison, Flying, Psychic, Bug, Rock, Ghost, Dark, Fairy, Steel, Dragon, Normal.",
                       "Multitype Pokémon take the ascendant Plate's type; Judgment and Nature Power strike with it.",
                       "Super-effective hits on Pokémon of the ascendant type x1.2. Holding the ascendant Plate heals 1/16 HP a turn.",
                       "Tri Attack x1.3, Prismatic Laser x1.2. Borrowed fields never transform the arena."],
    :nature_power  => :JUDGMENT,
    :camouflage    => :NORMAL,
    :secret_power  => 0,
    # Rotation is driven by the :end_of_round hook below (so it can be announced a
    # round ahead and keep :prism in sync); the engine's own timer is parked.
    :borrow        => { :pool => order, :order => :sequential, :count => 1, :interval => 999,
                        :start_immediately => false },
    :move_mods     => { :TRIATTACK => 1.3, :PRISMATICLASER => 1.2 },
    :move_messages => { :PRISMATICLASER => "The Plates' light refracted through the beam!" },
    :damage_mods   => [
      # Dissonance - the fairness lever against an attuned boss
      { :category => :damaging, :mult => 1.2, :message => "{2} struck a dissonant chord with the ascendant Plate!",
        :condition => proc { |battle, user, target, move, type|
          pr = ascendant.call(battle)
          next false if !pr || !target || !type
          target.pbHasType?(pr[:type]) && Effectiveness.super_effective_type?(type, pr[:type])
        } }
    ],
    :end_of_round  => [
      { :battlers => { :condition => proc { |battle, b|
          pr = ascendant.call(battle)
          pr && b.hasActiveItem?(pr[:plate])
        } },
        :heal => 1/16r, :message => "{1}'s Plate resonated with the arena!" }
    ],
    :hooks         => {
      :on_start => proc { |battle, old_id|
        pr = { :rounds_left => interval, :rotation => 0, :interval => interval, :telegraph => 1,
               :type_map => types, :plate_map => plates, :turn => turn,
               :order => order.dup, :mode => :curated, :gym_order => gym_order.call, :set_order => set_order }
        set_current.call(pr, nil)
        FieldEffects.state(battle)[:prism] = pr
        set_next.call(pr, peek.call(battle, 0))
      },
      :on_entry => proc { |battle, battler| attune.call(battle, battler) },
      :end_of_round => proc { |battle|
        pr = prism.call(battle)
        next if !pr
        actual = battle.fe_state[:borrowed].first
        if actual != pr[:field]   # Someone rotated outside :turn - resync
          set_current.call(pr, actual)
          set_next.call(pr, peek.call(battle, 0))
          pr[:rounds_left] = pr[:interval]
          battle.allBattlers.each { |b| attune.call(battle, b) }
        end
        pr[:rounds_left] -= 1
        # Rounds of warning (writable :telegraph, 1 by default): the glow starts that many rounds ahead.
        lead = [[pr[:telegraph].to_i, 1].max, [pr[:interval].to_i - 1, 1].max].min
        if pr[:rounds_left] <= 0
          pr[:rounds_left] = pr[:interval] if !turn.call(battle)
        elsif pr[:next_field] && pr[:rounds_left] == lead
          msg = (lead == 1) ? "The {1} begins to glow... After the next turn, the arena becomes the {2}!" :
                              "The {1} begins to glow... In {3} turns, the arena becomes the {2}!"
          battle.pbDisplay(FieldEffects.format(msg, item_name.call(pr[:next_plate]), FieldEffects.name_of(pr[:next_field]),
                                               pr[:rounds_left]))
        elsif pr[:next_field] && pr[:rounds_left] == 1
          battle.pbDisplay(FieldEffects.format("The {1} glows brighter... After the next turn, the arena becomes the {2}!",
                                               item_name.call(pr[:next_plate]), FieldEffects.name_of(pr[:next_field])))
        end
      },
      :base_type => proc { |battle, user, move, type|
        pr = ascendant.call(battle)
        (pr && move.id == :JUDGMENT) ? pr[:type] : nil
      }
    },
    :seed => { :item => :MAGICALSEED, :stats => { :SPECIAL_ATTACK => 1, :SPECIAL_DEFENSE => 1 },
               :message => "{1}'s {2} refracted the light of the Plates!" }
  }
end).call)
