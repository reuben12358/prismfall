#===============================================================================
# Prismfall Bosses - 005 Bar breaks, defeat scripts and on-break effects
#===============================================================================
module Prismfall
  module Bosses
    PRIMAL_ORBS    = { :KYOGRE => :BLUEORB, :GROUDON => :REDORB }
    HAZARD_EFFECTS = [:StealthRock, :Spikes, :ToxicSpikes, :StickyWeb]
    SCREEN_EFFECTS = [:Reflect, :LightScreen, :AuroraVeil]

    #---------------------------------------------------------------------------
    # Safe point: resolve pending breaks/defeats, then sync PRISM_ARENA followers.
    #---------------------------------------------------------------------------
    def self.process(battle)
      return if !battle || !battle.respond_to?(:prismfall_boss_states)
      return if battle.instance_variable_get(:@prismfall_bosses_busy)
      return if battle.prismfall_boss_states.empty? && !battle.instance_variable_get(:@prismfall_prism_dirty)
      battle.instance_variable_set(:@prismfall_bosses_busy, true)
      begin
        battle.battlers.each do |b|
          next if !b || battle.decision > 0
          st = battle.prismfall_boss_states[b.pokemon]
          next if !st || !st.pending
          (st.pending == :break) ? break_bar(battle, b, st) : run_defeat(battle, b, st, st.pending_defeat)
        end
        apply_prism_interval(battle)
        apply_prism_order_once(battle)
        sync_prism_followers(battle) if battle.instance_variable_get(:@prismfall_prism_dirty) && battle.decision == 0
      ensure
        battle.instance_variable_set(:@prismfall_bosses_busy, false)
      end
    end

    def self.effect_list(value)
      value = resolve(value)
      return [] if value.nil?
      return value.is_a?(Array) ? value.compact : [value]
    end

    def self.condition_ok?(e, battle, battler, st)
      return true if !e[:condition]
      return e[:condition].call(battle, battler, st) ? true : false
    end

    def self.break_bar(battle, battler, st)
      st.pending     = nil
      st.breaks_done += 1
      n              = st.breaks_done          # the n-th bar was just depleted
      st.bars_left  -= 1
      st.phase_turn  = 0
      effects = effect_list(st.data[:on_break]) + effect_list((st.data[:breaks] || {})[n])
      effects = effects.select { |e| condition_ok?(e, battle, battler, st) }
      msg = st.data.key?(:break_message) ? st.data[:break_message] : BREAK_MESSAGE
      battle.pbDisplay(text(msg, battler.pbThis)) if msg && !msg.empty?
      battle.scene.pbTrainerBattleSpeech("bossBreak#{n}") if battle.scene.respond_to?(:pbTrainerBattleSpeech) rescue nil
      # Refill for the next bar (overflow already discarded).
      frac = effects.map { |e| e[:refill] }.compact.last || 1.0
      target = [[(battler.totalhp * frac).round, 1].max, battler.totalhp].min
      battler.pbRecoverHP(target - battler.hp) if target > battler.hp
      effects.each { |e| apply_effect(battle, battler, st, e) }
      update_ball_rule(battle, st)
      battle.scene.pbRefreshOne(battler.index) if battle.scene.respond_to?(:pbRefreshOne)
      PBDebug.log("[Prismfall Bosses] #{battler.pbThis} bar #{n} broke; #{st.bars_left} left")
      EventHandlers.trigger(:prismfall_boss_bar_broken, battle, battler, st.id, n, st.bars_left)
      finish_battle(battle, st) if st.end_decision
    end

    # Survival-type on-defeat effects (:end_battle / :survive) whose condition holds now.
    def self.survive_defeat_effects(battle, battler, st)
      list = effect_list(st.data[:on_defeat]).select { |e| e[:end_battle] || e[:survive] }
      list = list.select { |e| condition_ok?(e, battle, battler, st) }
      return (list.empty?) ? nil : list
    end

    # effects = nil: called from pbFaint (the boss really faints); only effects
    # without :end_battle/:survive run. Otherwise the boss stays at 1 HP.
    def self.run_defeat(battle, battler, st, effects)
      return if st.defeated
      st.pending  = nil
      st.defeated = true
      st.bars_left = 0
      if effects.nil?
        effects = effect_list(st.data[:on_defeat]).reject { |e| e[:end_battle] || e[:survive] }
        effects = effects.select { |e| condition_ok?(e, battle, battler, st) }
      end
      effects.each { |e| apply_effect(battle, battler, st, e) }
      EventHandlers.trigger(:prismfall_boss_defeated, battle, battler, st.id, st.result)
      finish_battle(battle, st) if st.end_decision
    end

    def self.finish_battle(battle, st)
      battle.decision = st.end_decision if battle.decision == 0
    end

    #---------------------------------------------------------------------------
    # One effect Hash. Keys are applied in this fixed order.
    #---------------------------------------------------------------------------
    def self.apply_effect(battle, b, st, e)
      name = b.pbThis
      (Array(e[:message]) + Array(e[:messages])).each { |m| battle.pbDisplay(text(m, name)) }
      battle.pbCommonAnimation(e[:animation], b) if e[:animation]
      battle.scene.pbTrainerBattleSpeech(e[:speech].to_s) if e[:speech] && battle.scene.respond_to?(:pbTrainerBattleSpeech)
      if e[:cure_status]
        b.pbCureStatus(true) if b.status != :NONE
        b.pbCureConfusion if e[:cure_status] == :all && b.respond_to?(:pbCureConfusion)
      end
      reset_stats(b, e[:reset_stats]) if e[:reset_stats]
      if e.key?(:form)
        f = (e[:form] == :match_type) ? form_for_type(b.species, b.types[0]) : resolve(e[:form], battle, b)
        change_form(b, st, f, e[:form_message])
      end
      if e[:types]
        t = Array(e[:types])
        (t.length == 1) ? b.pbChangeTypes(t[0]) : b.types = t
      end
      change_ability(b, e[:ability]) if e[:ability]
      b.item = e[:item] if e.key?(:item)
      set_moves(battle, b, resolve(e[:moves], battle, b)) if e[:moves]
      learn_moves(battle, b, e[:learn]) if e[:learn]
      raise_stats(b, e[:stats]) if e[:stats]
      battle.change_field(e[:field], e[:field_message]) if e[:field] && battle.respond_to?(:change_field)
      (apply_prism_order(battle, b, st) || prism_turn(battle)) if e[:prism_turn]   # :prism_order bosses move to the new bar's fields
      start_weather(battle, b, e[:weather], e[:weather_permanent]) if e[:weather]
      battle.pbStartTerrain(b, e[:terrain], !e[:terrain_permanent]) if e[:terrain]
      clear_side_effects(battle, b, e[:clear_hazards], HAZARD_EFFECTS, "The hazards around {1} were swept away!") if e[:clear_hazards]
      clear_side_effects(battle, b, e[:clear_screens] == true ? :foe : e[:clear_screens], SCREEN_EFFECTS,
                         "{1} shattered the barriers!") if e[:clear_screens]
      Array(e[:heal_allies] ? b.allAllies : []).each { |a| a.pbRecoverHP((a.totalhp * e[:heal_allies]).round) if a.canHeal? }
      summon(battle, b, e[:summon]) if e[:summon]
      pbBGMPlay(e[:music]) if e[:music]
      primal(battle, b) if e[:primal]
      e[:proc].call(battle, b, st) if e[:proc]
      st.result = e[:result] if e.key?(:result)
      st.end_decision = ((e[:end_battle] == true) ? 1 : e[:end_battle]) if e[:end_battle]
    end

    def self.reset_stats(b, mode)
      if mode == :negative
        b.stages.each_key { |s| b.stages[s] = 0 if b.stages[s] < 0 }
      else
        b.pbResetStatStages
      end
    end

    def self.raise_stats(b, stats)
      stats.each do |stat, n|
        if n > 0
          b.pbRaiseStatStage(stat, n, b) if b.pbCanRaiseStatStage?(stat, b)
        elsif n < 0
          b.pbLowerStatStage(stat, -n, b) if b.pbCanLowerStatStage?(stat, b)
        end
      end
    end

    def self.change_form(b, st, form, msg)
      return if !form.is_a?(Integer)
      msg ||= text("{1} transformed!", b.pbThis)
      # A trainer's PBS "Form = n" pins the form (Pokemon#forced_form) for species with a getForm handler
      # (Silvally, Arceus, Giratina): unpin it, or the battler changes form but keeps the old form's types and stats.
      pk = b.pokemon
      pk.forced_form = nil if pk && pk.respond_to?(:forced_form=) && !pk.forced_form.nil?
      b.pbChangeForm(form, text(msg, b.pbThis))
      ab = resolve(st.data[:ability])   # Pokemon#form= clears a forced ability
      if ab
        b.pokemon.ability = ab
        b.ability = ab
      end
    end

    def self.change_ability(b, ability)
      old = b.ability_id
      b.ability = ability
      b.battle.pbDisplay(text("{1} gained {2}!", b.pbThis, GameData::Ability.get(ability).name))
      b.pbOnLosingAbility(old) if b.respond_to?(:pbOnLosingAbility)
      b.pbTriggerAbilityOnGainingIt if b.respond_to?(:pbTriggerAbilityOnGainingIt)
    end

    # The form of `species` whose only type is `type` (Arceus/Silvally style).
    def self.form_for_type(species, type)
      return nil if !type
      (0..40).each do |f|
        sp = GameData::Species.get_species_form(species, f)
        next if !sp || sp.form != f
        return f if sp.types == [type]
      end
      return nil
    end

    def self.set_moves(battle, b, list)
      list = Array(list).compact.first(Pokemon::MAX_MOVES)
      return if list.empty? || b.effects[PBEffects::Transform] == true
      return if b.moves.map { |m| m && m.id } == list
      pkmn = b.pokemon
      pkmn.forget_all_moves
      list.each { |m| pkmn.learn_move(m) }
      b.moves = pkmn.moves.map { |m| Battle::Move.from_pokemon_move(battle, m) }
      b.effects[PBEffects::ChoiceBand] = nil if defined?(PBEffects::ChoiceBand)
    end

    # { slot => :MOVE } or [:MOVE, ...] (fills empty slots, then replaces the last).
    def self.learn_moves(battle, b, spec)
      list = b.moves.map { |m| m && m.id }
      if spec.is_a?(Hash)
        spec.each { |slot, m| list[slot] = m }
      else
        Array(spec).each do |m|
          next if list.include?(m)
          (list.compact.length < Pokemon::MAX_MOVES) ? list[list.compact.length] = m : list[-1] = m
        end
      end
      set_moves(battle, b, list.compact)
      Array(spec.is_a?(Hash) ? spec.values : spec).each do |m|
        battle.pbDisplay(text("{1} learned {2}!", b.pbThis, GameData::Move.get(m).name))
      end
    end

    def self.start_weather(battle, b, w, permanent)
      w = Array(w)
      battle.pbStartWeather(b, w[0], !permanent, true)
    end

    # which: true/:own = the boss's side, :foe = the player's side, :both.
    def self.clear_side_effects(battle, b, which, names, msg)
      sides = case which
              when :foe  then [b.pbOpposingSide]
              when :both then [b.pbOwnSide, b.pbOpposingSide]
              else            [b.pbOwnSide]
              end
      cleared = false
      sides.each do |side|
        names.each do |n|
          next if !PBEffects.const_defined?(n)
          eff = PBEffects.const_get(n)
          v = side.effects[eff]
          next if !v || v == 0
          side.effects[eff] = (v == true) ? false : 0
          cleared = true
        end
      end
      battle.pbDisplay(text(msg, b.pbThis)) if cleared
    end

    def self.primal(battle, b)
      orb = PRIMAL_ORBS[b.species]
      b.item = orb if orb && !b.hasActiveItem?(orb)
      return if !battle.respond_to?(:pbPrimalReversion)
      battle.pbPrimalReversion(b.index)
      b.pbTriggerAbilityOnGainingIt if b.respond_to?(:pbTriggerAbilityOnGainingIt)
    end

    #---------------------------------------------------------------------------
    # Summon an ally: spec = { :species, :level, :moves, :item, :ability, :boss => :ID, :message }
    #---------------------------------------------------------------------------
    def self.summon(battle, boss, spec)
      spec = resolve(spec, battle, boss)
      return if !spec.is_a?(Hash) || !spec[:species]
      level = spec[:level] || boss.level
      if !battle.wildBattle?
        battle.pbDisplay(text("...but no help came!"))
        return
      end
      party = battle.pbParty(boss.index)
      if battle.respond_to?(:pbGenerateAllyBattler)   # EBDX Renovation SOS helper (wild battles)
        before = battle.battlers.map { |x| x && x.pokemon }
        battle.pbGenerateAllyBattler(spec[:species], level)
        b = battle.battlers.find { |x| x && x.pokemon && !x.opposes?(boss.index) && before.none? { |p| p.equal?(x.pokemon) } }
        return if !b
        dress_ally(b.pokemon, spec)
        b.pbInitPokemon(b.pokemon, b.pokemonIndex)
        battle.scene.pbRefreshOne(b.index) if battle.scene.respond_to?(:pbRefreshOne)
        battle.pbDisplay(text(spec[:message], boss.pbThis(true), b.pokemon.name)) if spec[:message]
        return
      end
      # Vanilla: only into an existing, fainted slot on the boss's side.
      slot = battle.battlers.find { |x| x && x.index != boss.index && !x.opposes?(boss.index) && x.fainted? }
      if !slot
        battle.pbDisplay(text("...but no help came!"))
        return
      end
      pkmn = Pokemon.new(spec[:species], level)
      dress_ally(pkmn, spec)
      party.push(pkmn)
      battle.pbPartyOrder(boss.index).push(party.length - 1)
      battle.pbRecallAndReplace(slot.index, party.length - 1, true)
      battle.pbDisplay(text(spec[:message] || "{2} came to {1}'s aid!", boss.pbThis(true), pkmn.name))
      battle.pbOnBattlerEnteringBattle(slot.index)
    end

    def self.dress_ally(pkmn, spec)
      if spec[:moves]
        pkmn.forget_all_moves
        Array(spec[:moves]).first(Pokemon::MAX_MOVES).each { |m| pkmn.learn_move(m) }
      end
      pkmn.item    = spec[:item] if spec.key?(:item)
      pkmn.ability = spec[:ability] if spec[:ability]
      pkmn.prismfall_boss_id = spec[:boss] if spec[:boss] && exists?(spec[:boss])
      pkmn.calc_stats
      pkmn.heal
    end

    #---------------------------------------------------------------------------
    # PRISM_ARENA (Field Effects plugin, 136_Field_PrismArena.rb)
    #---------------------------------------------------------------------------
    # The arena's LIVE state Hash (writable :interval, the :turn / :set_order lambdas). Not
    # FieldEffects.prism_state: that is a frozen read-only summary without the lambdas, and going through it
    # left :prism_turn dead on every bar break and made :prism_interval raise FrozenError (2026-11-25).
    def self.prism_state(battle)
      return nil if !defined?(FieldEffects) || !battle
      st = FieldEffects.state(battle)
      pr = (st.is_a?(Hash)) ? st[:prism] : nil
      return (pr.is_a?(Hash)) ? pr : nil
    end

    # :prism_interval => n sets the arena's (writable) rounds-per-turn once it exists.
    def self.apply_prism_interval(battle)
      return if battle.instance_variable_get(:@prismfall_prism_interval_done)
      pr = prism_state(battle)
      return if !pr
      boss_battlers(battle).each do |b|
        n = resolve(state_for(b).data[:prism_interval])
        next if !n.is_a?(Integer)
        pr[:interval] = n
        battle.instance_variable_set(:@prismfall_prism_interval_done, true)
      end
    end

    # Turns the Plates now through the arena's own announced :turn.
    def self.prism_turn(battle)
      pr = prism_state(battle)
      return false if !pr || !pr[:turn].respond_to?(:call)
      ret = pr[:turn].call(battle)
      sync_prism_followers(battle)
      return ret
    end

    # :prism_order => [[field, ...], ...] (one list per bar; the last list repeats) or a proc returning that:
    # the arena only cycles among the current bar's fields (Arceus: each bar's three gym fields, in gym order).
    # Set when the boss enters (and the Plates turn at once to the bar's first field) and again at every break.
    def self.prism_window(st)
      order = resolve(st.data[:prism_order])
      return nil if !order.is_a?(Array) || order.empty?
      list = order[[st.phase - 1, order.length - 1].min]
      return (list.is_a?(Array) && !list.empty?) ? list : nil
    end

    # Once per battle, as soon as the arena's state exists: the first bar's fields, and the Plates turn to them.
    def self.apply_prism_order_once(battle)
      return if battle.instance_variable_get(:@prismfall_prism_order_done) || battle.decision != 0
      return if !prism_state(battle)
      boss_battlers(battle).each do |b|
        st = state_for(b)
        next if !prism_window(st)
        battle.instance_variable_set(:@prismfall_prism_order_done, true)
        apply_prism_order(battle, b, st)
        break
      end
    end

    def self.apply_prism_order(battle, battler, st, turn_now = true)
      window = prism_window(st)
      pr = prism_state(battle)
      return false if !window || !pr || !pr[:set_order].respond_to?(:call)
      return false if !pr[:set_order].call(battle, window)
      prism_turn(battle) if turn_now
      return true
    end

    # Bosses with :follow_prism take the form (sprite) and moveset of the
    # ascendant Plate's type. The arena already re-types Multitype battlers.
    #   :items => { :FIRE => :FIREMEMORY, ..., :default => nil }   also swaps the held item (Silvally's Memories)
    # Nothing changes during the arena's opening rounds (no Plate ascendant yet).
    def self.sync_prism_followers(battle)
      battle.instance_variable_set(:@prismfall_prism_dirty, false)
      pr = prism_state(battle)
      return if !pr || !pr[:field]
      type = pr[:type] || :NORMAL
      boss_battlers(battle).each do |b|
        fp = resolve(state_for(b).data[:follow_prism])
        next if !fp.is_a?(Hash)
        items = resolve(fp[:items])
        if items.is_a?(Hash)
          it = items.key?(type) ? items[type] : items[:default]
          it = nil if it && !GameData::Item.exists?(it)
          b.item = it if b.item_id != it
        end
        if fp[:form] != false
          f = form_for_type(b.species, type)
          if f && f != b.form
            msg = fp[:form_message]
            msg = msg.call(type) if msg.respond_to?(:call)     # a proc { |type| "..." } may word each type itself
            change_form(b, state_for(b), f, text(msg || "{1} took on the {2} type!", b.pbThis,
                                                 GameData::Type.get(type).name))
          end
        end
        sets = resolve(fp[:movesets])
        set_moves(battle, b, sets[type] || sets[:default]) if sets.is_a?(Hash) && (sets[type] || sets[:default])
      end
    end
  end
end

# The arena rotates on its own every few rounds; follow it at the next safe point
# (after its Multitype announcement), not mid-rotation.
EventHandlers.add(:prismfall_field_overlay_changed, :prismfall_bosses_follow_prism,
  proc { |battle, field_id, _old_ids, _new_ids|
    battle.instance_variable_set(:@prismfall_prism_dirty, true) if field_id == :PRISM_ARENA
  }
)
