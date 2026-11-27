#===============================================================================
# Prismfall Field Effects - story battle hooks (data + three small alias-chained hooks; no core file is edited)
#-------------------------------------------------------------------------------
# 1. FLICKERS - a trainer's field flickers to another field for a turn, then comes back.
#    story/34_SCRIPT_CH15.md "K6": "Mid-battle (on the turn his 4th Pokemon enters), the overload: 'Kestrel's
#    Gauntlet is overloading!' The field flickers to :BLEED for one turn, then back to :HOLLOW_CATHEDRAL."
#      { :trainer => [:TYPE, "Name"], :versions => [base versions] (v+100 / v+200 follow their base),
#        :on_sendout => n (the trainer's n-th different Pokemon enters), :field => :ID, :rounds => 1,
#        :message => "...", :revert_message => "..." }
#    The field (and its stage) from before the flicker is restored at the end of the last flicker round, unless
#    something else changed the field in between.
#
# 2. Valen's crystal (story/40_SCRIPT_CH21.md "The Final"): "Each time the field cycles (a battle hook, Valen only):
#    his crystal visibly spreads from shoulder to throat, shown as a sprite overlay plus a line."
#    Every Plates turn on :PRISM_ARENA against CHAMPION_VALEN (the Final: v0 / 100 / 200) raises a crystal stage
#    (1..CRYSTAL_MAX) and fires   EventHandlers :prismfall_valen_crystal, proc { |battle, stage| ... }
#    (the EBDX Bridge draws the overlay from it once the art exists). The last stage reached is kept in
#    Prismfall.state.custom[:valen_crystal] for the Coronation's staging; FieldEffects::StoryHooks.valen_crystal reads it.
#    The LINE itself is spoken by Prismfall Bosses 113_Boss_ValenZygarde.rb (same event); this file only says it
#    when that plugin isn't installed, so it is never shown twice.
#
# 3. K8, the Redeemed Kestrel (story/39_SCRIPT_CH20.md "Day 6: Semifinal"): "At the first field-cycle, he looks
#    at the Gauntlet's light, tears it off and throws it across the arena floor. (The battle hook ends the
#    Gauntlet's field control.)" On the first Plates turn against RIVAL_KESTREL 80-82 he says his line and the
#    arena goes still (no field) for the rest of the fight. The Fallen Kestrel (90-92) keeps it on.
#
# 4. The Ruin Route's Inverse (story/12_RUIN_ROUTE.md R3 / R4 / R7, story/42_SCRIPT_RUIN_KING.md R7):
#    - INVERSE_OVERLAYS: the type chart is inverted ON TOP of the battle's own field, from the first turn:
#      Gym 16 (Ruin) Nyx v1, ":NEW_MOON running Inverse matchups"; the Hijack, Gilded King Aurelius v0, ":PRISM_ARENA
#      running Inverse" ("the Prism field turns inside out: strengths to weaknesses"), under every Plates turn.
#      The overlay is the Inverse Field's own chart (FieldEffects.invert_effectiveness, after the fields' own rules;
#      airborne Pokemon still dodge Ground moves) and never flips twice: with :INVERSE itself up it adds nothing.
#      It needs a field up (all three fights have one). Events can ask for it too: setBattleRule("inverse").
#      FieldEffects::StoryHooks.inverse_overlay?(battle) / set_inverse_overlay(battle, on, message).
#    - LAST_POKEMON_FIELDS: Gym 17 (Ruin) Celestine v1, ":FAIRY_TALE turns :INVERSE for her last Pokemon ('Once
#      upon a time, which was the only time')": when she is down to her last able Pokemon she says the line and the
#      field itself becomes :INVERSE (a field change, as the script says), once.
#===============================================================================
module FieldEffects
  module StoryHooks
    FLICKERS = [
      { :trainer => [:RIVAL_KESTREL, "Kestrel"], :versions => [60, 61, 62], :on_sendout => 4,
        :field => :BLEED, :rounds => 1,
        :message => "Kestrel's Gauntlet is overloading!",
        :revert_message => "The Gauntlet gutters. The nave's candles steady again." }
    ]

    CRYSTAL_TRAINER = :CHAMPION_VALEN
    CRYSTAL_VERSIONS = [0]   # the Final; the Ruin Route's Last Tuning (v1) has no spread
    CRYSTAL_MAX     = 4      # shoulder (the glove comes off) -> collarbone -> throat -> jaw
    CRYSTAL_LINE    = "The crystal climbs Valen's throat..."

    TEAROFF = { :trainer => [:RIVAL_KESTREL, "Kestrel"], :versions => [80, 81, 82],
                :line => "No. Not like this. If I beat you, I beat you.",
                :message => "Kestrel tore the Gauntlet off and threw it across the arena floor! The Plates fall still." }

    INVERSE_OVERLAYS = [
      { :trainer => [:LEADER_NYX, "Nyx"], :versions => [1],
        :message => "Nyx's illusions turn the new moon inside out! Type matchups are reversed!" },
      { :trainer => [:GILDED_AURELIUS, "Aurelius"], :versions => [0],
        :message => "The eighteen pylons flare Aureate gold, and the Prism field turns inside out! Type matchups are reversed!" }
    ]
    INVERSE_RULE_MESSAGE = "The world turns inside out... Type matchups are reversed!"

    LAST_POKEMON_FIELDS = [
      { :trainer => [:LEADER_CELESTINE, "Celestine"], :versions => [1], :field => :INVERSE,
        :line => "Once upon a time, which was the only time." }
    ]

    module_function

    def state(battle)
      st = battle.instance_variable_get(:@pf_story_hooks)
      st = battle.instance_variable_set(:@pf_story_hooks, { :seen => {}, :fired => {}, :queue => [] }) if !st
      return st
    end

    def base_version(v)
      return v.to_i % 100
    end

    def trainer_matches?(t, spec, versions = nil)
      return false if !t || !spec
      return false if (t.trainer_type rescue nil) != spec[0]
      return false if spec[1] && (t.name rescue nil) != spec[1]
      return true if versions.nil?
      v = (t.respond_to?(:version)) ? t.version : 0
      return versions.include?(base_version(v))
    end

    # [trainer, owner index] for an opposing battler, or nil.
    def owner(battle, b)
      return nil if !battle || !b || !battle.opponent || !b.opposes?
      idx = battle.pbGetOwnerIndexFromBattlerIndex(b.index)
      t = battle.opponent[idx]
      return (t) ? [t, idx] : nil
    end

    def opposing_trainer(battle, spec, versions = nil)
      return nil if !battle.opponent
      return battle.opponent.find { |t| trainer_matches?(t, spec, versions) }
    end

    #---------------------------------------------------------------------------
    # 1. Flickers
    #---------------------------------------------------------------------------
    def note_sendout(battle, b)
      t, idx = owner(battle, b)
      return if !t
      st = state(battle)
      seen = (st[:seen][idx] ||= [])
      return if seen.include?(b.pokemonIndex)
      seen.push(b.pokemonIndex)
      FLICKERS.each_with_index do |row, i|
        next if st[:fired][[:flicker, i]]
        next if !trainer_matches?(t, row[:trainer], row[:versions])
        next if seen.length != row[:on_sendout]
        st[:fired][[:flicker, i]] = true
        start_flicker(battle, row)
      end
      check_last_pokemon(battle)
    end

    def start_flicker(battle, row)
      return false if !battle.respond_to?(:change_field)
      st = state(battle)
      back = [battle.field_effect, battle.field_stage]
      battle.pbDisplay(FieldEffects.format(row[:message])) if row[:message]
      return false if !battle.change_field(row[:field])
      st[:flicker] = { :back => back, :to => FieldEffects.normalize_id(row[:field]), :turn => battle.turnCount,
                       :rounds => row[:rounds] || 1, :revert_message => row[:revert_message] }
      return true
    end

    def end_flicker(battle)
      st = state(battle)
      f = st[:flicker]
      return if !f
      return if battle.turnCount < f[:turn] + f[:rounds]     # the round it began in doesn't count
      st[:flicker] = nil
      return if battle.field_effect != f[:to]                # something else changed the field: leave it
      id, stage = f[:back]
      battle.change_field(id, f[:revert_message] || "")
      battle.set_field_stage(stage, "") if stage && stage > 1 && battle.respond_to?(:set_field_stage)
    end

    #---------------------------------------------------------------------------
    # 2 and 3. The Plates turn
    #---------------------------------------------------------------------------
    def on_overlay_change(battle, field_id)
      return if field_id != :PRISM_ARENA || !battle.opponent
      st = state(battle)
      if opposing_trainer(battle, [CRYSTAL_TRAINER], CRYSTAL_VERSIONS)
        st[:queue].push(:crystal) if !st[:queue].include?(:crystal)   # one turn of the Plates = one spread
      elsif !st[:fired][:tearoff] && opposing_trainer(battle, TEAROFF[:trainer], TEAROFF[:versions])
        st[:fired][:tearoff] = true
        st[:queue].push(:tearoff)
      end
    end

    def valen_crystal(battle = nil)
      return state(battle)[:crystal].to_i if battle
      return 0 if !defined?(Prismfall) || !Prismfall.respond_to?(:state)
      return Prismfall.state.custom[:valen_crystal].to_i
    end

    def crystal_spread(battle)
      st = state(battle)
      st[:crystal] = [st[:crystal].to_i + 1, CRYSTAL_MAX].min
      if defined?(Prismfall) && Prismfall.respond_to?(:state)
        c = Prismfall.state.custom
        c[:valen_crystal] = [c[:valen_crystal].to_i, st[:crystal]].max
      end
      line_owner = defined?(Prismfall::Bosses) && Prismfall::Bosses.const_defined?(:VALEN_CRYSTAL_LINE)
      battle.pbDisplay(FieldEffects.format(CRYSTAL_LINE)) if !line_owner
      EventHandlers.trigger(:prismfall_valen_crystal, battle, st[:crystal])
    end

    def speak(battle, trainer, line)
      idx = battle.opponent.index(trainer) || 0
      scene = battle.scene
      text = FieldEffects.format(line)
      if scene.respond_to?(:pbTrainerSpeak) && defined?(EliteBattle)
        scene.pbTrainerSpeak([text], nil, idx) rescue battle.pbDisplayPaused("#{trainer.name}: #{text}")
      else
        battle.pbDisplayPaused("#{trainer.name}: #{text}")
      end
    end

    def tearoff(battle)
      t = opposing_trainer(battle, TEAROFF[:trainer], TEAROFF[:versions])
      return if !t
      speak(battle, t, TEAROFF[:line])
      battle.change_field(FieldEffects::NONE, TEAROFF[:message])
    end

    # Runs what the Plates' turn queued, once the arena has finished turning.
    def flush(battle)
      st = state(battle)
      until st[:queue].empty?
        case st[:queue].shift
        when :crystal then crystal_spread(battle)
        when :tearoff then tearoff(battle)
        end
      end
    end

    #---------------------------------------------------------------------------
    # 4. The Ruin Route's Inverse
    #---------------------------------------------------------------------------
    def inverse_overlay?(battle)
      return (battle && battle.instance_variable_get(:@fe_inverse_overlay)) ? true : false
    end

    # Turns the overlay on (true) or off; the message is shown when it turns on.
    def set_inverse_overlay(battle, on, message = nil)
      return false if !battle
      was = inverse_overlay?(battle)
      battle.instance_variable_set(:@fe_inverse_overlay, on ? true : false)
      FieldEffects.invalidate_cache(battle)
      battle.pbDisplay(FieldEffects.format(message)) if on && !was && message && !message.empty?
      return true
    end

    # Battle start, right after the field's own intro: setBattleRule("inverse"), then the trainer table.
    def start_overlays(battle)
      rule = battle.instance_variable_get(:@fe_inverse_rule)
      set_inverse_overlay(battle, true, INVERSE_RULE_MESSAGE) if rule
      return if !battle.opponent
      INVERSE_OVERLAYS.each do |row|
        next if !opposing_trainer(battle, row[:trainer], row[:versions])
        set_inverse_overlay(battle, true, row[:message])
      end
    end

    # A trainer down to the last able Pokemon of their party: their field turns (once), after their line.
    def check_last_pokemon(battle)
      return if !battle || !battle.opponent || battle.decision != 0 || !battle.respond_to?(:change_field)
      st = state(battle)
      LAST_POKEMON_FIELDS.each_with_index do |row, i|
        next if st[:fired][[:last, i]]
        t = opposing_trainer(battle, row[:trainer], row[:versions])
        next if !t || t.party.count { |p| p && p.able? } != 1
        st[:fired][[:last, i]] = true
        speak(battle, t, row[:line]) if row[:line]
        battle.change_field(row[:field], row[:message])     # no :message = the new field's own intro
      end
    end
  end

  # The overlay in the type chart (damage, immunities and the AI all go through these two).
  class << self
    alias prismfall_inv_modify_effectiveness modify_effectiveness unless method_defined?(:prismfall_inv_modify_effectiveness)
    def modify_effectiveness(battle, move, move_type, def_type, user, target, eff)
      eff = prismfall_inv_modify_effectiveness(battle, move, move_type, def_type, user, target, eff)
      return eff if !StoryHooks.inverse_overlay?(battle)
      return eff if active_defs(battle).any? { |d| d[:inverse] }     # already the Inverse chart: no double flip
      return invert_effectiveness(eff)
    end

    alias prismfall_inv_effectiveness_rules_active? effectiveness_rules_active? unless method_defined?(:prismfall_inv_effectiveness_rules_active?)
    def effectiveness_rules_active?(battle)
      return true if StoryHooks.inverse_overlay?(battle)
      return prismfall_inv_effectiveness_rules_active?(battle)
    end

    alias prismfall_inv_apply_battle_rule apply_battle_rule unless method_defined?(:prismfall_inv_apply_battle_rule)
    def apply_battle_rule(battle)
      rules = ($game_temp) ? $game_temp.battle_rules : nil
      battle.instance_variable_set(:@fe_inverse_rule, rules["inverse"]) if rules && rules["inverse"]
      return prismfall_inv_apply_battle_rule(battle)
    end

    alias prismfall_inv_on_battle_start on_battle_start unless method_defined?(:prismfall_inv_on_battle_start)
    def on_battle_start(battle)
      prismfall_inv_on_battle_start(battle)
      StoryHooks.start_overlays(battle)
    end
  end
end

# setBattleRule("inverse"): the Inverse overlay for this battle, on top of whatever field it has.
class Game_Temp
  alias prismfall_inv_add_battle_rule add_battle_rule unless method_defined?(:prismfall_inv_add_battle_rule)
  def add_battle_rule(rule, var = nil)
    if rule.to_s.downcase == "inverse"
      self.battle_rules["inverse"] = true
      return
    end
    prismfall_inv_add_battle_rule(rule, var)
  end
end

EventHandlers.add(:prismfall_field_overlay_changed, :prismfall_story_hooks,
  proc { |battle, field_id, _old_ids, _new_ids|
    FieldEffects::StoryHooks.on_overlay_change(battle, field_id)
  }
)

class Battle
  alias prismfall_story_pbOnAllBattlersEnteringBattle pbOnAllBattlersEnteringBattle unless method_defined?(:prismfall_story_pbOnAllBattlersEnteringBattle)
  def pbOnAllBattlersEnteringBattle
    if opponent
      allOtherSideBattlers(0).each { |b| FieldEffects::StoryHooks.note_sendout(self, b) if b && !b.fainted? }
    end
    return prismfall_story_pbOnAllBattlersEnteringBattle
  end

  alias prismfall_story_pbOnBattlerEnteringBattle pbOnBattlerEnteringBattle unless method_defined?(:prismfall_story_pbOnBattlerEnteringBattle)
  def pbOnBattlerEnteringBattle(battler_index, skip_event_reset = false)
    ret = prismfall_story_pbOnBattlerEnteringBattle(battler_index, skip_event_reset)
    if opponent
      Array(battler_index).flatten.each do |i|
        b = @battlers[i]
        FieldEffects::StoryHooks.note_sendout(self, b) if b && !b.fainted? && b.opposes?
      end
    end
    return ret
  end

  alias prismfall_story_pbEndOfRoundPhase pbEndOfRoundPhase unless method_defined?(:prismfall_story_pbEndOfRoundPhase)
  def pbEndOfRoundPhase
    ret = prismfall_story_pbEndOfRoundPhase
    if (!@decision || @decision == 0) && @pf_story_hooks
      FieldEffects::StoryHooks.flush(self)
      FieldEffects::StoryHooks.end_flicker(self)
      FieldEffects::StoryHooks.check_last_pokemon(self)
    end
    return ret
  end
end
