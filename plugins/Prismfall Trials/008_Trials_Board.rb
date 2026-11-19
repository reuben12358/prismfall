#===============================================================================
# Prismfall Trials - 008 Trial boards and hall keepers
#-------------------------------------------------------------------------------
# Event usage (the board / the keeper NPC in any of the Trial's halls):
#   Script: pf_trial_board(:ELOWEN)    the board menu (Rejuvenation Help Center
#                                      style: title, stars = rank, Rec. Lv.)
#   Script: pf_trial_keeper(:ISENMAR)  rank-up rewards + the latest rumours
# Board quests come from every hall of that Trial; the entry says where the
# giver waits. Quests with :board => false are only offered by their NPC.
#===============================================================================
module Prismfall
  module Trials
    def self.board_ids(trial)
      quests_for(trial).select do |id|
        q = get(id)
        next false if q[:hidden] || q[:board] == false
        next false if q[:stub] && !($DEBUG && SHOW_STUBS_IN_DEBUG)
        st = state(id)
        next true if st == :active
        next st == :available
      end
    end

    def self.board_label(id)
      q = get(id)
      stars = "*" * (q[:rank] || 1)
      label = "#{stars} #{_INTL(q[:title])}"
      label += _INTL(" (taken)") if active?(id)
      label += _INTL(" | Rec. Lv. {1}", q[:rec_level]) if SHOW_REC_LEVEL && q[:rec_level] && !active?(id)
      label += " [stub]" if q[:stub]
      return label
    end

    def self.board(trial)
      trial = trial.to_sym
      t = TRIALS[trial]
      raise ArgumentError, "Unknown Trial #{trial.inspect}" if !t
      pay_rank_rewards(trial)
      pbMessage(_INTL(t[:greeting]))
      200.times do   # bounded: a headless run with no scripted answers can't spin forever
        ids = board_ids(trial)
        header = _INTL("{1} - {2}: {3} ({4} pts)", trial_name(trial), _INTL(t[:board]), rank_name(trial), points(trial))
        cmds = ids.map { |id| board_label(id) }
        cmd_rumours = cmds.length
        cmds.push(_INTL("Rumours"))
        cmds.push(_INTL("Leave"))
        if ids.empty?
          pbMessage(_INTL("Nothing hangs on the {1} for you right now.", _INTL(t[:board])))
        end
        choice = pick(header, cmds, cmds.length - 1)
        break if choice.nil? || choice < 0 || choice >= cmds.length - 1
        if choice == cmd_rumours
          pf_trial_rumours(3)
          next
        end
        id = ids[choice]
        q = get(id)
        if active?(id)
          pbMessage(_INTL("\"{1}\" - {2}", _INTL(q[:title]), step_text(id, step(id)) || _INTL(q[:summary].to_s)))
          next
        end
        where = (q[:where]) ? _INTL("\nAsk {1} at {2}.", _INTL(q[:giver].to_s), _INTL(q[:where])) : ""
        pbMessage(_INTL("{1}{2}", _INTL(q[:summary].to_s), where))
        if pick(_INTL("Take this request?"), [_INTL("Yes"), _INTL("No")], 1) == 0
          pbMessage(_INTL(t[:accept])) if t[:accept]
          start(id)
          set_flag(id, :from_board, true) if q[:scenes] && q[:scenes][:offer]
          run_scene_if(id, :accepted)
        end
      end
      return true
    end

    def self.run_scene_if(id, scene)
      q = get(id)
      return nil if !q || !q[:scenes] || !q[:scenes][scene]
      return Script.run_scene(id, scene)
    end

    def self.keeper(trial)
      trial = trial.to_sym
      given = pay_rank_rewards(trial)
      if given == 0
        nxt = RANK_POINTS[rank(trial)]
        if nxt
          pbMessage(_INTL("You stand as {1}. {2} more points to {3}.", rank_name(trial), nxt - points(trial),
                          rank_name(trial, rank(trial) + 1)))
        else
          pbMessage(_INTL("You stand as {1}. There is no higher rank.", rank_name(trial)))
        end
      end
      pf_trial_rumours(2)
      return true
    end
  end
end

def pf_trial_board(trial);  return Prismfall::Trials.board(trial);  end
def pf_trial_keeper(trial); return Prismfall::Trials.keeper(trial); end
