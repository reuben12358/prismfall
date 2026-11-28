#===============================================================================
# Prismfall Maps - Chapters 9 and 10 on the built Ironreach and Verdance maps (mapgen/layouts/story_ch9.py,
# story_ch10.py; story/27_SCRIPT_CH9.md, story/28_SCRIPT_CH10.md).
#   pfm_ch9_tag        the Conclave attack: PC + Kestrel (K4's team, Rival.version_for(4)) vs Sable 0 + Brisk 0
#   pfm_ch9_open(r)    one round of the Ironreach Open (1 Dunmore, 2 Ysa, 3 Gristle); true = won
#   title cards        END OF ACT II, Interlude II's "Five days earlier", Juno's note, the testament, the paper
# Nothing here sets a story variable: the map events do (design/FLAGS.md V130 / V131).
#===============================================================================
module PrismfallConclave
  # story/27 "the Ironreach Open": the rounds' LOSE lines are the script's, not the trainers' generic PBS LoseText
  OPEN = {
    1 => [:BLACKBELT, "Dunmore", "...I'm going to need a shirt."],
    2 => [:CRUSHGIRL, "Ysa", "GRAN. I did my BEST. ...She's saying \"the washing\". I can't hear her but I know."],
    3 => [:BLACKBELT, "Gristle", "You didn't cry. That's worse. Go on. The boy in the coat's waiting, and he's been staring at you for three rounds."]
  }

  module_function

  def trainer?(type, name, version = 0)
    return false if !defined?(GameData::Trainer)
    return GameData::Trainer.exists?(type, name, version) rescue false
  end

  def open_round(r)
    t = OPEN[r]
    return true if !t
    if !trainer?(t[0], t[1])
      pbMessage(_INTL("(Round {1} of the Open plays here once its trainer is in PBS.)", r))
      return true
    end
    setBattleRule("field", :COLOSSEUM) if defined?(FieldEffects)
    return TrainerBattle.start([t[0], t[1], 0, t[2]]) ? true : false
  end

  # story/27: "BATTLE: tag battle - PC + Kestrel (RIVAL_KESTREL as partner, version 40 + slot's team) vs
  # [HOLLOW_SABLE "Sable", version 0] + [HOLLOW_ADMIN "Brisk", version 0]. Field: Colosseum." A loss whites out
  # (no canLose): the sequence restarts at "The Vote".
  def tag
    if !trainer?(:HOLLOW_SABLE, "Sable") || !trainer?(:HOLLOW_ADMIN, "Brisk")
      pbMessage(_INTL("(The tag battle with Kestrel plays here once Sable and Brisk are in PBS.)"))
      return true
    end
    v = (defined?(Prismfall::Rival)) ? Prismfall::Rival.version_for(4) : 40
    pbRegisterPartner(:RIVAL_KESTREL, "Kestrel", v)
    setBattleRule("field", :COLOSSEUM) if defined?(FieldEffects)
    r = TrainerBattle.start(:HOLLOW_SABLE, "Sable", 0, :HOLLOW_ADMIN, "Brisk", 0)
    pbDeregisterPartner rescue nil
    return r ? true : false
  end
end

def pfm_ch9_tag;           return PrismfallConclave.tag;           end
def pfm_ch9_open(r);       return PrismfallConclave.open_round(r); end

if defined?(Prismfall::Cutscene) && Prismfall::Cutscene.respond_to?(:define)
  Prismfall::Cutscene.define(:PF_ACT2_END) do
    background :color, color: [0, 0, 0]
    title "END OF ACT II"
  end
  Prismfall::Cutscene.define(:PF_IL2_CARD) do
    background :color, color: [0, 0, 0]
    text "Five days earlier. Verdance."
  end
end
