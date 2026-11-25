#===============================================================================
# Prismfall Z-Power - more trainer barks, through 005's PrismfallSpeech.
#-------------------------------------------------------------------------------
# BARKS keys: [trainer type, name] (every version) or [trainer type, name, version].
#   :sendout => { :SPECIES => line, [:SP1, :SP2] => line }   the first time that
#               species (or any species of the array) enters; an array key
#               speaks once for the whole group
#   :ace_low => line   at the end of a round, when the trainer's last Pokemon is
#               below a third of its HP
#   :round1  => line   at the end of the first round
# A line is a String or an Array of Strings. Each line speaks once per battle.
#===============================================================================
module PrismfallSpeech
  BARKS = {
    # Ruin Route R7, the Hijack: Gilded King Aurelius (Gemini rework 2026-11-23, story/42_SCRIPT_RUIN_KING.md D4).
    # "mongrel" stops when Gilt comes out: from then on he is talking to a rival.
    [:GILDED_AURELIUS, "Aurelius"] => {
      :sendout => {
        :GOLURK    => "Witness the original, mongrel. That corroded toy Voss dredged from the silt was my doorstep's dust.",
        :AEGISLASH => ["A thousand blades were forged after Aurelia sank. Every one a crude copy of mine.",
                       "Regalia. Show them royal steel."],
        [:KYOGRE, :GROUDON] => ["Before I forged a chain for heaven, I leashed the sea and the earth to plow my gardens!",
                                "Let us see if you survive the Year of Two Weathers."],
        :REGIGIGAS => "Even a sleeping titan stands when its king commands. Survive five heartbeats, and earn being crushed.",
        :GHOLDENGO => ["Hmph...! You tore through my court and my titans alike? Splendid!",
                       "Then drown in the whole treasury of Aurelia. Gilt, make it rain!"]
      },
      :round1  => "Even heaven's own laws twist backward beneath my heels! Adapt, or shatter!",
      :ace_low => ["Hahaha! Yes! That cold, unflinching glare: neither kneeling nor begging!",
                   "Strike harder, challenger! Show me the fang that dares bite a god!"]
    }
  }

  module_function

  def bark_row(trainer)
    return nil if !trainer
    type = (trainer.trainer_type rescue nil)
    name = (trainer.name rescue nil)
    return nil if !type || !name
    ver = (trainer.respond_to?(:version) ? trainer.version : nil)
    return (ver && BARKS[[type, name, ver]]) || BARKS[[type, name]]
  end

  # Speaks `line` for battler b's owner once per battle (keyed by tag).
  def bark(battle, b, tag, line)
    return false if !line
    t, idx = owner(battle, b)
    return false if !t
    done = (battle.instance_variable_get(:@prismfall_speech) || battle.instance_variable_set(:@prismfall_speech, {}))
    key = [idx, :bark, tag]
    return false if done[key]
    done[key] = true
    lines = (line.is_a?(Array) ? line : [line]).map { |l| _INTL(l) }
    scene = battle.scene
    if scene.respond_to?(:pbTrainerSpeak) && defined?(EliteBattle) && sprite?(t)
      scene.pbTrainerSpeak(lines.map(&:dup), nil, idx)
    else
      lines.each { |l| battle.pbDisplayPaused(_INTL("{1}: {2}", t.name, l)) }
    end
    EventHandlers.trigger(:prismfall_trainer_speech, battle, b, tag, lines)
    return true
  rescue StandardError => e
    PBDebug.log("[Prismfall barks] #{e.class}: #{e.message}") if defined?(PBDebug)
    return false
  end

  def on_sendout(battle, b)
    t, _idx = owner(battle, b)
    row = bark_row(t)
    return if !row || !row[:sendout]
    row[:sendout].each do |key, line|
      next if !Array(key).include?(b.species)
      bark(battle, b, [:sendout, key], line)
    end
  end

  def on_round_end(battle)
    return if !battle.opponent
    battle.allOtherSideBattlers(0).each do |b|
      next if !b || b.fainted?
      t, idx = owner(battle, b)
      row = bark_row(t)
      next if !row
      bark(battle, b, :round1, row[:round1]) if row[:round1] && battle.turnCount <= 1
      next if !row[:ace_low] || b.hp * 3 >= b.totalhp
      party = battle.pbParty(b.index).select.with_index { |_p, i| battle.pbGetOwnerIndexFromPartyIndex(b.index, i) == idx }
      next if party.count { |p| p && p.able? } > 1
      bark(battle, b, :ace_low, row[:ace_low])
    end
  end
end

class Battle
  alias prismfall_barks_pbOnBattlerEnteringBattle pbOnBattlerEnteringBattle unless method_defined?(:prismfall_barks_pbOnBattlerEnteringBattle)
  def pbOnBattlerEnteringBattle(battler_index, skip_event_reset = false)
    ret = prismfall_barks_pbOnBattlerEnteringBattle(battler_index, skip_event_reset)
    Array(battler_index).flatten.each do |i|
      b = @battlers[i]
      PrismfallSpeech.on_sendout(self, b) if b && !b.fainted? && b.opposes?
    end
    return ret
  end

  alias prismfall_barks_pbEndOfRoundPhase pbEndOfRoundPhase unless method_defined?(:prismfall_barks_pbEndOfRoundPhase)
  def pbEndOfRoundPhase
    ret = prismfall_barks_pbEndOfRoundPhase
    PrismfallSpeech.on_round_end(self) if !@decision || @decision == 0
    return ret
  end
end
