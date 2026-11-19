#===============================================================================
# Prismfall Field Effects - trainer field plays (data + two small hooks)
#-------------------------------------------------------------------------------
# Owner: trainer workstream (design/TRAINER_FIELD_PLAYBOOK.md). Everything here
# is alias-chained or a handler; no core file is edited.
#
# 1. WANTS - which field changes a trainer type's team is BUILT around.
#    AIField (007) scores a transition by how the active battlers' types fit the
#    two fields. That can't see a plan that lives in the party (Marisol's whole
#    team wants the fight Underwater; Magnus wants his Factory back), and it
#    never picks a status move whose only use is the transition (Noivern's
#    Sunny Day on the Stormfront "fails" as weather but opens the Rainbow).
#    WANTS adds a score for moves that advance or complete a listed change:
#      TRAINER_TYPE => { :FIELD => n, [:FIELD, stage] => n }   (n < 0 = avoid)
#    A [:FIELD, stage] key is checked before the plain :FIELD key.
#    Weather and terrain moves count when the weather / terrain they start
#    triggers one of the current field's transitions.
#
# 2. ENTRY_FIELDS - the field follows a trainer's Pokemon (the Eevee Octave
#    finale: Vesper's field becomes each Eeveelution's home Imprint as it enters).
#      TRAINER_TYPE => { :versions => [base versions], :fields => { SPECIES => :FIELD or [:FIELD, stage] },
#                        :message => "... {1} = Pokemon, {2} = field name" }
#    Difficulty variants (v+100, v+200) follow their base version.
#===============================================================================
module FieldEffects
  module TrainerPlays
    WANTS = {
      # Wardens
      :LEADER_DORIAN    => { [:GRAND_STAGE, 2] => 10, [:GRAND_STAGE, 3] => 10, [:GRAND_STAGE, 1] => -10 },
      :LEADER_TAMSIN    => { [:WILDFIRE, 2] => 20, :WILDFIRE => -25 },
      :LEADER_MARISOL   => { :UNDERWATER => 22, :WATER_SURFACE => -30 },
      :LEADER_ROOK      => { [:NEON_GRID, 1] => 22, [:NEON_GRID, 2] => -12 },
      :LEADER_SAHAR     => { [:DESERT, 1] => 22, [:DESERT, 2] => -20 },
      :LEADER_CORVIN    => { :WASTELAND => 20, :WATER_SURFACE => -25 },
      :LEADER_BRANN     => { :VOLCANIC => 22, :ASHEN_WASTE => -15 },
      :LEADER_JUNO      => { [:FLOWER_GARDEN, 2] => 14, [:FLOWER_GARDEN, 3] => 14, [:FLOWER_GARDEN, 4] => 14,
                             [:FLOWER_GARDEN, 5] => 8, :MEADOW => 18, :WILDFIRE => -25 },
      :LEADER_ANJA      => { :WATER_SURFACE => 10, :FROZEN_LAKE => 16 },
      :LEADER_ODESSA    => { :RAINBOW => 18 },
      :LEADER_ILSA      => { :INVERSE => 18, [:MINDSCAPE, 1] => 18, [:MINDSCAPE, 2] => -15 },
      :LEADER_BASTIAN   => { :CAVE => 14, :CRYSTAL_CAVERN => 22, :DARK_CRYSTAL => -25 },
      :LEADER_YSOLDE    => { [:HOLLOW_CATHEDRAL, 1] => 22, [:HOLLOW_CATHEDRAL, 2] => -25 },
      :LEADER_MAGNUS    => { :FACTORY => 25, :SCRAPYARD => -25 },
      :LEADER_NYX       => { [:NEW_MOON, 2] => 16, [:NEW_MOON, 1] => 12, [:NEW_MOON, 3] => -20 },
      :LEADER_CELESTINE => { :FAIRY_TALE => 22, :DRAGONS_DEN => -20 },
      :LEADER_SIGRUN    => { :DRAGONS_DEN => 22, [:DRAGONS_DEN, 2] => 12, :CAVE => -15, :FAIRY_TALE => -20 },
      # Rivals
      :RIVAL_JUNO       => { :FLOWER_GARDEN => 18, :MEADOW => 18, :WATER_SURFACE => 30, :WILDFIRE => -25 },
      :RIVAL_KESTREL    => { :DRAGONS_DEN => 16 },
      # Villains and story fights
      :HOLLOW_WICK        => { [:HOLLOW_CATHEDRAL, 2] => 30 },
      :HOLLOW_SABLE       => { :CAVE => 16 },
      :HOLLOW_ADMIN       => { :CAVE => 12 },
      :MERIDIAN_KROLL     => { [:MINDSCAPE, 2] => 16, [:CAVE, 2] => 12, [:CAVE, 1] => 12 },
      :MERIDIAN_QUENT     => { :ASHEN_WASTE => 22, :FACTORY => 14 },   # no Scrapyard bonus: Explosion hits his own partner in the Ch16 double
      :MERIDIAN_MARCHETTI => { :DARK_CRYSTAL => 22 },
      :ARCHSEER_DASK      => { :MINDSCAPE => 22, :INVERSE => 22 },
      # The Eevee Octave
      :OCTAVE_SINGER      => { :UNDERWATER => 18, :WATER_SURFACE => -25, :INVERSE => 22, [:NEW_MOON, 2] => 14,
                               [:NEON_GRID, 1] => 18, :VOLCANIC => 18 },
      :OCTAVE_VESPER      => { :INVERSE => 12 }
    }

    # SUPPORT - doubles support moves the v21 AI underrates against raw damage. Bonus to the move's score in a
    # double battle, under a condition: :first_turns (only on the battle's first two turns), :no_tailwind,
    # :no_rain, :partner (a partner is on the field).
    SUPPORT = {
      :LEADER_TAMSIN    => { :RAINDANCE => [25, :no_rain], :SILKTRAP => [8, :partner] },
      :LEADER_CORVIN    => { :TAILWIND => [20, :no_tailwind], :RAGEPOWDER => [15, :partner] },
      :LEADER_ODESSA    => { :TAILWIND => [35, :no_tailwind], :WIDEGUARD => [12, :partner], :HELPINGHAND => [10, :partner] },
      :LEADER_NYX       => { :FAKEOUT => [30, :first_turns], :HELPINGHAND => [10, :partner] },
      :LEADER_CELESTINE => { :FAKEOUT => [30, :first_turns], :DECORATE => [40, :first_turns], :FOLLOWME => [25, :partner] },
      :OCTAVE_VESPER    => { :HELPINGHAND => [15, :partner] },
      :OCTAVE_SINGER    => { :HELPINGHAND => [15, :partner] },
      :MERIDIAN_MARCHETTI => { :TAILWIND => [20, :no_tailwind] },
      :MERIDIAN_QUENT   => { :TRICKROOM => [20, :first_turns] }
    }

    ENTRY_FIELDS = {
      :OCTAVE_VESPER => {
        :versions => [2],
        :fields   => { :VAPOREON => :WATER_SURFACE, :JOLTEON => :NEON_GRID, :FLAREON => :VOLCANIC,
                       :ESPEON => :MINDSCAPE, :UMBREON => :NEW_MOON, :SYLVEON => :FAIRY_TALE,
                       :LEAFEON => [:FLOWER_GARDEN, 3], :GLACEON => :FROZEN_LAKE, :EEVEE => :GRAND_STAGE },
        :message  => "The Choir gardens answer {1}: the {2} it was raised beside rises around it!"
      }
    }

    WEATHER_CODES = { "StartSunWeather" => [:Sun, :HarshSun], "StartRainWeather" => [:Rain, :HeavyRain],
                      "StartSandstormWeather" => [:Sandstorm], "StartHailWeather" => [:Hail] }.freeze
    TERRAIN_CODES = { "StartElectricTerrain" => :Electric, "StartGrassyTerrain" => :Grassy,
                      "StartMistyTerrain" => :Misty, "StartPsychicTerrain" => :Psychic }.freeze

    module_function

    def rule_destination(battle, rule)
      if rule.key?(:to)
        to = rule[:to]
        to = FieldEffects.safe_call(to, battle) if to.is_a?(Proc)
        return [FieldEffects.normalize_id(to), 1]
      elsif rule[:stage] || rule[:stage_delta]
        return [FieldEffects.current(battle), rule[:stage] || (FieldEffects.stage(battle) + rule[:stage_delta].to_i)]
      end
      return nil
    end

    # [count, uses, [field, stage], even_if_failed] of the change this move works toward, or nil.
    # Adds weather- and terrain-triggered transitions to FieldEffects.transition_this_move_advances.
    def play_for(battle, user, move, type)
      info = FieldEffects.transition_this_move_advances(battle, user, move, type)
      rules = FieldEffects.transitions(battle)
      if info
        lenient = rules.any? do |r|
          r[:even_if_failed] && FieldEffects.move_trigger?(r) && !r[:target] &&
            FieldEffects.move_matches?(r, battle, user, nil, move, type)
        end
        return [info[0], info[1], info[2], lenient]
      end
      code = move.function_code
      if WEATHER_CODES[code]
        rule = rules.find { |r| r[:weather] && (Array(r[:weather]) & WEATHER_CODES[code]).any? }
        dest = rule && rule_destination(battle, rule)
        return [0, 1, dest, false] if dest
      elsif TERRAIN_CODES[code]
        rule = rules.find { |r| r[:terrain] && Array(r[:terrain]).include?(TERRAIN_CODES[code]) }
        dest = rule && rule_destination(battle, rule)
        return [0, 1, dest, false] if dest
      end
      return nil
    rescue StandardError
      return nil
    end

    # A plain :FIELD key only covers a change INTO that field from another one; a stage change inside the
    # current field needs its own [:FIELD, stage] key (a stage can go either way).
    def want(trainer_type, dest, current = nil)
      table = WANTS[trainer_type]
      return 0 if !table || !dest || dest[0].nil?
      exact = table[[dest[0], dest[1]]]
      return exact if exact
      return 0 if current && current == dest[0]
      return table[dest[0]] || 0
    end

    # Trainer type of the trainer who owns the battler the AI is choosing for. (Battle::AI::AITrainer has no
    # public reader for its trainer, so go through the battle.)
    def trainer_type_of(battle, battler_index)
      return nil if !battle.opponent || (battler_index & 1) == 0
      tr = battle.pbGetOwnerFromBattlerIndex(battler_index)
      return (tr && tr.respond_to?(:trainer_type)) ? tr.trainer_type : nil
    rescue StandardError
      return nil
    end

    # ENTRY_FIELDS: called as a battler enters (before the field's own on-entry rules).
    def apply_entry_field(battle, battler)
      return if ENTRY_FIELDS.empty? || !battler || battler.fainted? || !battle.respond_to?(:change_field)
      return if !battle.opponent || !battler.opposes?
      owner = battle.pbGetOwnerFromBattlerIndex(battler.index)
      spec = owner && owner.respond_to?(:trainer_type) && ENTRY_FIELDS[owner.trainer_type]
      return if !spec
      version = (owner.respond_to?(:version)) ? owner.version.to_i % 100 : 0
      return if spec[:versions] && !spec[:versions].include?(version)
      entry = spec[:fields][battler.species]
      return if !entry
      id, stage = FieldEffects.split_field_entry(entry)
      return if !FieldEffects.exists?(id)
      return if FieldEffects.current(battle) == id
      msg = FieldEffects.format(spec[:message] || "The field shifts around {1}!", battler.pbThis, FieldEffects.name_of(id))
      battle.set_field_stage(stage, "") if battle.change_field(id, msg) && stage > 1
    end
  end
end

class Battle
  alias prismfall_plays_pbEntryHazards pbEntryHazards
  def pbEntryHazards(battler)
    begin
      FieldEffects::TrainerPlays.apply_entry_field(self, battler)
    rescue StandardError => e
      raise e if $DEBUG
    end
    prismfall_plays_pbEntryHazards(battler)
  end
end

class Battle::AI
  # A move that "fails" as weather / as a move on this field but still counts toward a
  # transition the trainer wants (rules marked :even_if_failed) is not a failed move.
  alias prismfall_plays_pbPredictMoveFailure pbPredictMoveFailure
  def pbPredictMoveFailure
    failed = prismfall_plays_pbPredictMoveFailure
    return failed if !failed || !FieldEffects.active?(@battle)
    tt = FieldEffects::TrainerPlays.trainer_type_of(@battle, @user.index)
    return failed if !tt || !FieldEffects::TrainerPlays::WANTS[tt]
    play = FieldEffects::TrainerPlays.play_for(@battle, @user.battler, @move.move, @move.rough_type)
    return failed if !play || !play[3]
    return false if FieldEffects::TrainerPlays.want(tt, play[2], FieldEffects.current(@battle)) > 0
    return failed
  end
end

Battle::AI::Handlers::GeneralMoveScore.add(:prismfall_trainer_plays,
  proc { |score, move, user, ai, battle|
    next score if !FieldEffects.active?(battle) || !ai.trainer.medium_skill?
    tt = FieldEffects::TrainerPlays.trainer_type_of(battle, user.index)
    next score if !tt || !FieldEffects::TrainerPlays::WANTS[tt]
    play = FieldEffects::TrainerPlays.play_for(battle, user.battler, move.move, move.rough_type)
    next score if !play
    count, uses, dest = play
    want = FieldEffects::TrainerPlays.want(tt, dest, FieldEffects.current(battle))
    next score if want == 0
    # Starting a multi-use play is worth most of the value, finishing it all of it.
    weight = (uses <= 1) ? 1.0 : 0.6 + 0.4 * (count + 1) / uses.to_f
    delta = (want * weight).round
    old = score
    if want > 0 && move.statusMove?
      # A status move whose point is the field change: don't let "does nothing else" bury it.
      score = [score, Battle::AI::MOVE_BASE_SCORE].max + delta
    else
      score += delta
    end
    PBDebug.log_score_change(score - old, "trainer field play (#{dest[0]})")
    next score
  }
)

Battle::AI::Handlers::GeneralMoveScore.add(:prismfall_trainer_support,
  proc { |score, move, user, ai, battle|
    next score if !ai.trainer.medium_skill? || battle.pbSideSize(user.index) < 2
    tt = FieldEffects::TrainerPlays.trainer_type_of(battle, user.index)
    table = tt && FieldEffects::TrainerPlays::SUPPORT[tt]
    rule = table && table[move.id]
    next score if !rule
    bonus, cond = rule
    side = user.battler.pbOwnSide
    ok = case cond
         when :first_turns then battle.turnCount <= 1
         when :no_tailwind then side.effects[PBEffects::Tailwind] <= 0
         when :no_rain     then ![:Rain, :HeavyRain].include?(battle.pbWeather)
         when :partner     then battle.allSameSideBattlers(user.index).any? { |b| b.index != user.index && !b.fainted? }
         else true
         end
    next score if !ok
    PBDebug.log_score_change(bonus, "trainer doubles support (#{move.id})")
    next score + bonus
  }
)
