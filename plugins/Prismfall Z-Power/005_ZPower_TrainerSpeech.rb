#===============================================================================
# Prismfall Z-Power - trainer speech when a trainer's Z-move or Mega fires.
#-------------------------------------------------------------------------------
# A small, data-driven hook (like EBDX's battle-script "megaOpp" keys, but per
# trainer and for Z-moves too). When an opposing trainer's Pokemon unleashes its
# Z-move (:prismfall_zmove_unleashed, after "...unleashed its full-force
# Z-Move!" and before the move hits) or Mega Evolves (:prismfall_mega_evolved),
# that trainer says their line from LINES, once per battle per event.
#
# Display: with Elite Battle: DX the trainer slides in and speaks through EBDX's
# own trainer dialogue (Battle::Scene#pbTrainerSpeak); without EBDX, or while the
# trainer type has no front sprite yet, the line is a paused battle message,
# "Name: line".
#
# LINES keys: [trainer type, name] (every version of that trainer) or
# [trainer type, name, version] (one version; wins over the general key).
# Values: { :zmove => line, :mega => line }; a line is a String or an Array of
# Strings (one message box each).
#===============================================================================
module PrismfallSpeech
  LINES = {
    # Gym 17 (and her Ruin-route copy and Festival draw): Mimikyu @ Mimikium Z, Let's Snuggle Forever.
    # story/08_ACT_V.md Ch18; mapgen/REQUESTS.md (story editor, Celestine item 4).
    [:LEADER_CELESTINE, "Celestine"] => {
      :zmove => "This is the part where it hugs you. Hold still. It's worse if you don't."
    }
  }

  module_function

  def line_for(trainer, event)
    return nil if !trainer
    type = (trainer.trainer_type rescue nil)
    name = (trainer.name rescue nil)
    return nil if !type || !name
    ver = (trainer.respond_to?(:version) ? trainer.version : nil)
    row = (ver && LINES[[type, name, ver]]) || LINES[[type, name]]
    return row && row[event]
  end

  # EBDX slides the trainer's front sprite in; a trainer type without one would show EBDX's "?" placeholder.
  def sprite?(trainer)
    return !(GameData::TrainerType.front_sprite_filename(trainer.trainer_type) rescue nil).nil?
  end

  # The opposing trainer who owns battler `b`, and their index in battle.opponent.
  def owner(battle, b)
    return nil if !battle || !b || !battle.opponent || !b.opposes?
    idx = battle.pbGetOwnerIndexFromBattlerIndex(b.index)
    t = battle.opponent[idx]
    return t ? [t, idx] : nil
  end

  def say(battle, b, event)
    t, idx = owner(battle, b)
    line = line_for(t, event)
    return false if !line
    done = (battle.instance_variable_get(:@prismfall_speech) || battle.instance_variable_set(:@prismfall_speech, {}))
    key = [idx, event]
    return false if done[key]
    done[key] = true
    lines = (line.is_a?(Array) ? line : [line]).map { |l| _INTL(l) }
    scene = battle.scene
    if scene.respond_to?(:pbTrainerSpeak) && defined?(EliteBattle) && sprite?(t)
      scene.pbTrainerSpeak(lines.map(&:dup), nil, idx)
    else
      lines.each { |l| battle.pbDisplayPaused(_INTL("{1}: {2}", t.name, l)) }
    end
    EventHandlers.trigger(:prismfall_trainer_speech, battle, b, event, lines)
    return true
  rescue StandardError => e
    PBDebug.log("[Prismfall speech] #{e.class}: #{e.message}") if defined?(PBDebug)
    return false
  end
end

EventHandlers.add(:prismfall_zmove_unleashed, :prismfall_trainer_speech,
  proc { |battle, user, _z| PrismfallSpeech.say(battle, user, :zmove) })

EventHandlers.add(:prismfall_mega_evolved, :prismfall_trainer_speech,
  proc { |battle, b, _old_ability| PrismfallSpeech.say(battle, b, :mega) })
