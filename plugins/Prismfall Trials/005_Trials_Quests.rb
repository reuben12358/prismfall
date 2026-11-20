#===============================================================================
# Prismfall Trials - 005 Quest lifecycle, rewards, ranks, event helpers
#-------------------------------------------------------------------------------
# States: :locked (unlock/requires not met) -> :available -> :active -> :done
#         (or :failed / :expired). Only :active/:done/:failed are stored.
# Event usage (Script / Conditional Branch > Script):
#   pf_quest_offer(:ID)          summary + "Take it?"; starts it on yes
#   pf_quest_start(:ID)          start without asking
#   pf_quest_step(:ID, :step)    move to a step       pf_quest_at?(:ID, :step)
#   pf_quest_complete(:ID[, :outcome])  rewards + points + toast
#   pf_quest_active?(:ID)  pf_quest_done?(:ID)  pf_quest_available?(:ID)
#   pf_quest_flag(:ID, :k[, v])  pf_quest_count(:ID, :k[, +n])
#   pf_quest_run(:ID, :scene)    run a scripted scene (004)
#   pf_trial_rank(:ELOWEN)       1-5
# Page conditions: a Comment "Condition: quest_step(:ID) == :chase" (010).
#===============================================================================
module Prismfall
  module Trials
    #---------------------------------------------------------------------------
    # State queries
    #---------------------------------------------------------------------------
    def self.record(id)
      return store[:quests][id.to_sym]
    end

    def self.unlocked?(id)
      q = get(id)
      return false if !q
      return false if q[:requires] && !q[:requires].all? { |r| done?(r) }
      return false if q[:rank] && rank(q[:trial]) < q[:rank]
      return cond(q[:unlock], q[:id])
    end

    def self.state(id)
      id = id.to_sym
      return :unknown if !exists?(id)
      r = record(id)
      return r[:state] if r && r[:state] != :done
      return :done if r && r[:state] == :done && !get(id)[:repeatable]
      q = get(id)
      return :expired if !r && q[:expires] && cond(q[:expires], id)
      return unlocked?(id) ? :available : :locked
    end

    def self.active?(id);    r = record(id); return !!(r && r[:state] == :active); end
    def self.done?(id);      r = record(id); return !!(r && (r[:state] == :done || (r[:times] || 0) > 0)); end
    def self.failed?(id);    r = record(id); return !!(r && r[:state] == :failed); end
    def self.available?(id); return state(id) == :available; end
    def self.step(id);       r = record(id); return (r) ? r[:step] : nil;  end
    def self.outcome(id);    r = record(id); return (r) ? r[:outcome] : nil; end

    def self.at?(id, step_id)
      return active?(id) && step(id) == step_id.to_sym
    end

    def self.flag(id, key)
      r = record(id)
      return (r) ? r[:flags][key.to_sym] : nil
    end

    def self.count(id, key)
      r = record(id)
      return (r) ? (r[:counts][key.to_sym] || 0) : 0
    end

    #---------------------------------------------------------------------------
    # Transitions
    #---------------------------------------------------------------------------
    def self.new_record
      return { :state => :active, :step => nil, :flags => {}, :counts => {}, :outcome => nil,
               :log => [], :accepted => play_time, :finished => nil, :times => 0 }
    end

    def self.start(id, show = TOASTS)
      id = id.to_sym
      q = get(id)
      raise ArgumentError, "Unknown quest #{id.inspect}" if !q
      r = record(id)
      return false if r && r[:state] == :active
      return false if r && r[:state] == :done && !q[:repeatable]
      times = (r) ? r[:times] : 0
      r = store[:quests][id] = new_record
      r[:times] = times
      first = step_ids(id).first
      r[:step] = first
      r[:log].push(first) if first
      toast(_INTL("NEW QUEST: \"{1}\"", _INTL(q[:title])), step_text(id, first)) if show
      EventHandlers.trigger(:prismfall_quest_changed, id, :started) if defined?(EventHandlers)
      refresh_map
      return true
    end

    def self.set_step(id, step_id, show = TOASTS)
      id = id.to_sym
      start(id, show) if !active?(id)
      r = record(id)
      step_id = step_id.to_sym
      warn("Quest #{id}: unknown step #{step_id.inspect}") if !step_ids(id).include?(step_id)
      return false if r[:step] == step_id
      r[:step] = step_id
      r[:log].push(step_id)
      toast(_INTL("QUEST LOG: \"{1}\"", _INTL(get(id)[:title])), step_text(id, step_id)) if show
      EventHandlers.trigger(:prismfall_quest_changed, id, step_id) if defined?(EventHandlers)
      refresh_map
      return true
    end

    def self.set_flag(id, key, value = true)
      start(id, false) if !record(id)
      record(id)[:flags][key.to_sym] = value
      refresh_map
      return value
    end

    def self.add_count(id, key, n = 1)
      start(id, false) if !record(id)
      c = record(id)[:counts]
      c[key.to_sym] = (c[key.to_sym] || 0) + n
      refresh_map
      return c[key.to_sym]
    end

    def self.complete(id, outcome = nil, show = TOASTS)
      id = id.to_sym
      q = get(id)
      raise ArgumentError, "Unknown quest #{id.inspect}" if !q
      start(id, false) if !active?(id)
      r = record(id)
      r[:state]    = :done
      r[:outcome]  = outcome
      r[:finished] = play_time
      r[:times]    = (r[:times] || 0) + 1
      t = TRIALS[q[:trial]]
      pbMessage("\\me[Slots win]" + _INTL(t[:done])) if show && t && t[:done]
      toast(_INTL("QUEST COMPLETE: \"{1}\"", _INTL(q[:title])), nil) if show
      give_reward(reward_for(q, outcome))
      add_points(q[:trial], q[:points] || 1, show)
      (q[:joint] || {}).each { |trial, pts| add_points(trial, pts, show) }
      EventHandlers.trigger(:prismfall_quest_changed, id, :done) if defined?(EventHandlers)
      refresh_map
      return true
    end

    def self.fail(id, show = TOASTS)
      id = id.to_sym
      start(id, false) if !record(id)
      r = record(id)
      r[:state] = :failed
      r[:finished] = play_time
      toast(_INTL("QUEST FAILED: \"{1}\"", _INTL(get(id)[:title])), nil) if show
      EventHandlers.trigger(:prismfall_quest_changed, id, :failed) if defined?(EventHandlers)
      refresh_map
      return true
    end

    def self.reset(id)   # debug
      store[:quests].delete(id.to_sym)
      store[:chases].delete(id.to_sym)
      refresh_map
    end

    def self.step_text(id, step_id)
      q = get(id)
      return nil if !q || !step_id || !q[:steps]
      s = q[:steps][step_id]
      return (s) ? _INTL(s) : nil
    end

    def self.toast(title, text)
      msg = "\\se[GUI save choice]" + title
      msg += "\n" + text if text && !text.empty?
      pbMessage(msg)
    end

    #---------------------------------------------------------------------------
    # Offer (board or NPC)
    #---------------------------------------------------------------------------
    def self.offer(id, ask = true)
      q = get(id)
      raise ArgumentError, "Unknown quest #{id.inspect}" if !q
      case state(id)
      when :active  then return true
      when :done    then pbMessage(_INTL("You have already answered this request.")); return false
      when :expired then pbMessage(_INTL("This request has expired.")); return false
      when :locked
        if q[:rank] && rank(q[:trial]) < q[:rank]
          pbMessage(_INTL("This needs the rank of {1} in {2}.", rank_name(q[:trial], q[:rank]), trial_name(q[:trial])))
        else
          pbMessage(_INTL("Not yet. Come back later."))
        end
        return false
      end
      pbMessage(_INTL("\"{1}\"\n{2}", _INTL(q[:title]), _INTL(q[:summary].to_s))) if q[:summary]
      return start(id) if !ask
      if pick(_INTL("Take this request?"), [_INTL("Yes"), _INTL("No")], 1) == 0
        t = TRIALS[q[:trial]]
        pbMessage(_INTL(t[:accept])) if t && t[:accept]
        return start(id)
      end
      return false
    end

    #---------------------------------------------------------------------------
    # Rewards
    #---------------------------------------------------------------------------
    def self.reward_for(q, outcome)
      base = q[:reward] || {}
      return base if !outcome || !q[:outcomes] || !q[:outcomes][outcome]
      o = q[:outcomes][outcome]
      return o[:replace] ? o : base.merge(o) { |_k, a, b| (a.is_a?(Array) && b.is_a?(Array)) ? a + b : b }
    end

    def self.give_reward(rw)
      return if !rw || rw.empty?
      pbMessage(_INTL(rw[:text])) if rw[:text]
      give_money(rw[:money]) if rw[:money] && rw[:money] > 0
      (rw[:items] || []).each { |item, qty| pbReceiveItem(item, qty || 1) }
      Prismfall::EventMons.gift(rw[:pokemon]) if rw[:pokemon]
      Prismfall::Narrative.apply_effects(rw[:effects]) if rw[:effects]
      Prismfall::Choices.make(rw[:choice][0], rw[:choice][1]) if rw[:choice]
    end

    def self.give_money(n)
      return if !$player || n.to_i <= 0
      $player.money += n.to_i
      pbMessage("\\me[Item get]" + _INTL("\\PN received ${1}!", n.to_i.to_s_formatted) + "\\wtnp[30]")
    end

    #---------------------------------------------------------------------------
    # Points and ranks
    #---------------------------------------------------------------------------
    def self.points(trial)
      return store[:points][trial.to_sym] || 0
    end

    def self.rank(trial)
      pts = points(trial)
      r = 1
      RANK_POINTS.each_with_index { |need, i| r = i + 1 if pts >= need }
      return r
    end

    def self.rank_name(trial, r = nil)
      t = TRIALS[trial.to_sym]
      return "?" if !t
      r ||= rank(trial)
      return _INTL(t[:ranks][r - 1] || t[:ranks].last)
    end

    def self.add_points(trial, n, show = TOASTS)
      trial = trial.to_sym
      return if !TRIALS[trial] || n.to_i == 0
      old = rank(trial)
      store[:points][trial] = points(trial) + n.to_i
      new = rank(trial)
      if show && new > old
        pbMessage("\\me[Badge get]" + _INTL("Your standing in {1} rose to {2}!", trial_name(trial), rank_name(trial, new)))
      end
      EventHandlers.trigger(:prismfall_trial_rank, trial, old, new) if new != old && defined?(EventHandlers)
    end

    # Hall keeper: hands out rank rewards not yet given. Returns how many.
    def self.pay_rank_rewards(trial)
      trial = trial.to_sym
      paid = store[:ranks_paid][trial] || 1
      given = 0
      ((paid + 1)..rank(trial)).each do |r|
        rw = (RANK_REWARDS[trial] || {})[r]
        if rw
          pbMessage(_INTL("For reaching the rank of {1}, take this.", rank_name(trial, r)))
          give_reward(rw)
        end
        store[:ranks_paid][trial] = r
        given += 1
      end
      return given
    end

    #---------------------------------------------------------------------------
    # Chases and quiet deeds
    #---------------------------------------------------------------------------
    def self.chase(id);         return store[:chases][id.to_sym] || 0; end
    def self.chase_reset(id);   store[:chases][id.to_sym] = 0; refresh_map; return 0; end
    def self.chase_advance(id)
      v = store[:chases][id.to_sym] = chase(id) + 1
      refresh_map
      return v
    end

    def self.record_deed(id)
      first = !store[:deeds][id.to_sym]
      store[:deeds][id.to_sym] = true
      return first
    end
    def self.deed?(id);   return !!store[:deeds][id.to_sym]; end
    def self.deeds;       return store[:deeds].length;      end

    #---------------------------------------------------------------------------
    # Battles used by quest scripts
    #---------------------------------------------------------------------------
    # field: :ID, :NONE, or [:ID, stage]
    def self.set_field(field)
      return if field.nil? || !defined?(FieldEffects)
      id, stage = (field.is_a?(Array)) ? field : [field, nil]
      setBattleRule("field", (id == :NONE) ? "none" : id)
      setBattleRule("fieldstage", stage) if stage && id != :NONE
    end

    def self.trainer_battle(spec, field: nil, double: nil, lose_text: nil)
      ttype, name, version = spec
      setBattleRule("canLose")
      setBattleRule("double") if double
      set_field(field)
      ret = TrainerBattle.start([ttype, name, version || 0, lose_text])
      $player.heal_party if !ret && $player   # quest losses never black out
      return ret ? true : false
    end

    # Back-to-back battles; no healing between unless heal_between.
    def self.gauntlet(list, heal_between: false, field: nil)
      list.each_with_index do |spec, i|
        pbMessage(_INTL("Bout {1} of {2}!", i + 1, list.length)) if list.length > 1
        return false if !trainer_battle(spec, field: field)
        $player.heal_party if heal_between && $player
      end
      return true
    end

    #---------------------------------------------------------------------------
    # Quest log feed (009) - lines for active/done quests
    #---------------------------------------------------------------------------
    def self.active_ids; return quest_ids.select { |id| active?(id) }; end
    def self.done_ids;   return quest_ids.select { |id| done?(id) && !active?(id) }; end
    def self.failed_ids; return quest_ids.select { |id| failed?(id) }; end
  end
end

#-------------------------------------------------------------------------------
# Condition functions (read-only) for Prismfall::Conditions strings
#-------------------------------------------------------------------------------
module Prismfall
  module Conditions
    tr = Prismfall::Trials
    {
      "quest_state"    => [1, proc { |id| tr.state(id) }],
      "quest_step"     => [1, proc { |id| tr.active?(id) ? tr.step(id) : nil }],
      "quest_active"   => [1, proc { |id| tr.active?(id) }],
      "quest_done"     => [1, proc { |id| tr.done?(id) }],
      "quest_outcome"  => [1, proc { |id| tr.outcome(id) }],
      "quest_flag"     => [2, proc { |id, k| tr.flag(id, k) }],
      "quest_count"    => [2, proc { |id, k| tr.count(id, k) }],
      "trial_rank"     => [1, proc { |t| tr.rank(t) }],
      "trial_points"   => [1, proc { |t| tr.points(t) }],
      "chase"          => [1, proc { |id| tr.chase(id) }],
      "deed"           => [1, proc { |id| tr.deed?(id) }],
      "deeds"          => [0, proc { tr.deeds }],
      "event_mon"      => [1, proc { |id| Prismfall::EventMons.status(id) }],
      "has_item"       => [1, proc { |i| ($bag) ? $bag.has?(i) : false }],
      "item_qty"       => [1, proc { |i| ($bag) ? $bag.quantity(i) : 0 }],
      "money"          => [0, proc { ($player) ? $player.money : 0 }],
      "party_size"     => [0, proc { ($player) ? $player.party.length : 0 }],
      "party_has"      => [1, proc { |s| ($player) ? $player.party.any? { |p| !p.egg? && p.isSpecies?(s) } : false }],
      "party_has_type" => [1, proc { |t| ($player) ? $player.party.any? { |p| !p.egg? && p.hasType?(t) } : false }],
      "night"          => [0, proc { (defined?(PBDayNight)) ? PBDayNight.isNight? : false }],
      "fields_seen"    => [0, proc { (defined?(FieldEffects::FieldNotes)) ? FieldEffects::FieldNotes.seen_count : 0 }],
      "tier"           => [1, proc { |m| Prismfall::Trials::BadgeTiers.unlocked_tier(m) }],
      "map_id"         => [0, proc { ($game_map) ? $game_map.map_id : 0 }]
    }.each { |name, fn| FUNCTIONS[name] = fn }
  end
end

#-------------------------------------------------------------------------------
# Event helpers
#-------------------------------------------------------------------------------
def pf_quest_offer(id, ask = true);       return Prismfall::Trials.offer(id, ask);              end
def pf_quest_start(id);                   return Prismfall::Trials.start(id);                   end
def pf_quest_step(id, step);              return Prismfall::Trials.set_step(id, step);          end
def pf_quest_at?(id, step);               return Prismfall::Trials.at?(id, step);               end
def pf_quest_complete(id, outcome = nil); return Prismfall::Trials.complete(id, outcome);       end
def pf_quest_fail(id);                    return Prismfall::Trials.fail(id);                    end
def pf_quest_active?(id);                 return Prismfall::Trials.active?(id);                 end
def pf_quest_done?(id);                   return Prismfall::Trials.done?(id);                   end
def pf_quest_available?(id);              return Prismfall::Trials.available?(id);              end
def pf_quest_state(id);                   return Prismfall::Trials.state(id);                   end
def pf_trial_rank(trial);                 return Prismfall::Trials.rank(trial);                 end
def pf_quiet_deed(id);                    return Prismfall::Trials.record_deed(id);             end
def pf_chase(id);                         return Prismfall::Trials.chase(id);                   end
def pf_chase_advance(id);                 return Prismfall::Trials.chase_advance(id);           end

def pf_quest_flag(id, key, value = nil)
  return Prismfall::Trials.flag(id, key) if value.nil?
  return Prismfall::Trials.set_flag(id, key, value)
end

def pf_quest_count(id, key, add = nil)
  return Prismfall::Trials.count(id, key) if add.nil?
  return Prismfall::Trials.add_count(id, key, add)
end
