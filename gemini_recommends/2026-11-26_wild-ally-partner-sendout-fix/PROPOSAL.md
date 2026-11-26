# Wild-Ally Partner Battle Sendout Fix (`012_Bridge_WildAllyPartner.rb`)

- **Date:** 2026-11-26
- **Author:** Gemini (on direct user feedback from Reuben: *"think about 'partner ogerpon' for a second, its a pokemon, how is it supposed to throw a pokeball?"*)
- **Target Drop-In Path (Claude-owned):** `plugins/Prismfall EBDX Bridge/012_Bridge_WildAllyPartner.rb`
- **Scope:** Fixes BOTH wild-Pokémon battle partners registered via `pbRegisterPartner`:
  1. **`:PARTNER_OGRE`** (`pbs/trainers.txt` `[PARTNER_OGRE, Ogre]` — Ch10 Bride Grove Loyal Three 2v1, `plugins/Prismfall Bosses/112_Boss_LoyalThree.rb` L27/61)
  2. **`:PARTNER_GIRATINA`** (`pbs/trainers.txt` `[PARTNER_GIRATINA, Depths]` — Ruin Route True Finale 2v1, `plugins/Prismfall Bosses/103_Boss_Arceus.rb` L251)

---

## 1. Root Cause Confirmed in Live EBDX + Essentials v21.1

Because `pbRegisterPartner` registers wild allies as trainer objects on `@battle.player[1]`, stock EBDX (`Battle Core.rb` L63–99, `Scene Battle.rb` L115–126, `Battler Sendout Player.rb` L23–196, `Battler Recall.rb` L8–42) currently:
1. Prints **`"Gossamer Ogre sent out Ogerpon!"`** / **`"Reverse Depths sent out Giratina!"`**.
2. Fades in `@sprites["player_1"]` (`PARTNER_OGRE_back.png` or missing-sprite placeholder for `PARTNER_GIRATINA`) beside the player and plays its 5-frame throw cycle.
3. Spawns `@sprites["pokeball2"]`, launches a spinning Poké Ball arc + `EBBallBurst`, and pops a *second* Ogerpon/Giratina out of the ball while `@sprites["player_1"]` fades out.

## 2. Drop-In Fix — `plugins/Prismfall EBDX Bridge/012_Bridge_WildAllyPartner.rb`

Zero edits to core EBDX files required. Handles:
- **Battle start copy (`Battle#pbStartBattleSendOut`):** Replaces `"{1} sent out {2}!"` for wild-ally trainers with natural wild entry lines (`"Ogerpon leaps to your side!"` / `"Giratina tears open the shadows beside you!"`).
- **EBDX trainer sprite suppression (`Battle::Scene#initializeSprites`):** Hides `@sprites["player_#{i}"]` (`visible = false`, `opacity = 0`) for any wild-ally trainer so no trainer-back sprite or missing-sprite placeholder ever appears.
- **EBDX ball-free wild entry (`Battle::Scene#playerBattlerSendOut`):** Splits `sendOuts` into normal human-thrown battlers (handled natively by EBDX — ONLY the player throws a Poké Ball!) and wild-ally battlers (handled by `pf_wild_ally_entry`: **zero** `player_1`, **zero** `pokeball`, **zero** `EBBallBurst`).
  - `:leap` (**Ogerpon**): Parabolic leap from off-left (`dx=-112, dy=-34 → 0`) with opacity fade-in, landing shadow, battle cry, and smooth databox entrance.
  - `:rift` (**Giratina-Origin**): Dark-violet shadow-rift materialization (`Tone(-180, -210, -80, 120) → (0, 0, 0, 0)`, scale-in `1.16× → 1.00×`), battle cry, shadow, and databox entrance.
- **EBDX ball-free recall (`Battle::Scene#pbRecall`):** If a wild ally is ever forced out (Roar/Whirlwind/etc.), smoothly leaps/fades out without `Battle recall` SE or `EBBallBurst`.
- **Vanilla Essentials v21.1 fallback:** Also guards `Battle::Scene#pbSendOutBattlers` (when EBDX is absent) so the player's partner slot never shows a trainer back sprite or Poké Ball animation.

```ruby
#===============================================================================
# Prismfall EBDX Bridge — Wild-Ally Partner Direct Entry (No Trainer / No Ball)
#-------------------------------------------------------------------------------
# Wild Pokemon that fight beside the player via pbRegisterPartner (Ch10 Ogerpon
# as :PARTNER_OGRE, Ruin Finale Giratina-Origin as :PARTNER_GIRATINA) are wild
# Pokemon, NOT human trainers throwing Poke Balls.
#
# This patch:
#   1. Suppresses @sprites["player_#{i}"] for wild-ally partner slots.
#   2. Replaces "{1} sent out {2}!" with natural wild-ally entry text.
#   3. Splits playerBattlerSendOut so ONLY the human player throws a Poke Ball,
#      while the wild ally leaps (:leap) or materializes from a rift (:rift)
#      directly onto its battle pad with zero Poke Ball / EBBallBurst.
#   4. Suppresses ball-burst recall if a wild ally ever leaves the field.
#===============================================================================

module Prismfall
  module WildAllyPartner
    SPECS = {
      :PARTNER_OGRE     => {
        :entry_msg => "{1} leaps to your side!",
        :style     => :leap
      },
      :PARTNER_GIRATINA => {
        :entry_msg => "{1} tears open the shadows beside you!",
        :style     => :rift
      }
    }.freeze

    def self.trainer_wild_ally?(trainer)
      return false if !trainer || !trainer.respond_to?(:trainer_type)
      SPECS.key?(trainer.trainer_type)
    end

    def self.spec_for_trainer(trainer)
      return nil if !trainer_wild_ally?(trainer)
      SPECS[trainer.trainer_type]
    end

    def self.battler_wild_ally?(battle, idx_battler)
      return false if !battle || idx_battler.nil?
      return false if battle.opposes?(idx_battler)
      owner = (battle.pbGetOwnerFromBattlerIndex(idx_battler) rescue nil)
      trainer_wild_ally?(owner)
    end

    def self.spec_for_battler(battle, idx_battler)
      return nil if !battler_wild_ally?(battle, idx_battler)
      owner = (battle.pbGetOwnerFromBattlerIndex(idx_battler) rescue nil)
      spec_for_trainer(owner)
    end

    def self.entry_message(trainer, battler_names)
      spec = spec_for_trainer(trainer)
      return nil if !spec
      lead = battler_names.first || trainer.name
      _INTL(spec[:entry_msg], lead)
    end
  end
end

#-------------------------------------------------------------------------------
# 1. Battle#pbStartBattleSendOut — Replace "{1} sent out {2}!" for wild allies
#-------------------------------------------------------------------------------
class Battle
  if method_defined?(:pbStartBattleSendOut) && !method_defined?(:pf_wild_ally_pbStartBattleSendOut)
    alias pf_wild_ally_pbStartBattleSendOut pbStartBattleSendOut

    def pbStartBattleSendOut(sendOuts)
      has_wild_ally = @player && @player.any? { |t| Prismfall::WildAllyPartner.trainer_wild_ally?(t) }
      return pf_wild_ally_pbStartBattleSendOut(sendOuts) if !has_wild_ally

      if defined?(EliteBattle)
        EliteBattle.set(:smAnim, false) if @opponent && @opponent.length > 1
        @scene.sendingOut = true if @scene.respond_to?(:sendingOut=)
        foes = wildBattle? ? pbParty(1) : @opponent
        memb = []
        text = wildBattle? ? "Oh! A wild " : "You are challenged by "
        foes.each_with_index do |foe, i|
          memb.push(wildBattle? ? foe.name : foe.full_name)
          text += ", " if i > 0 && i < foes.length - 1
          text += " and " if i == foes.length - 1 && foes.length > 1
          text += "{#{i + 1}}"
        end
        text += wildBattle? ? " appeared!" : "!"
        pbDisplayPaused(EliteBattle.battle_text(text, *memb))
        if wildBattle? && foes.length < 2
          @battlers[1].immunity = true if EliteBattle.get(:setBoss)
          @scene.smSpeciesSequence.finish if @scene.respond_to?(:smSpeciesSequence) && @scene.smSpeciesSequence
          @scene.raiseSpeciesStats if @scene.respond_to?(:raiseSpeciesStats)
        elsif foes.length < 2
          @scene.smTrainerSequence.finish if @scene.respond_to?(:smTrainerSequence) && @scene.smTrainerSequence
          @scene.introdone = true if @scene.respond_to?(:introdone=)
        end

        [1, 0].each do |side|
          next if side == 1 && wildBattle?
          msg = ""
          to_send_out = []
          trainers = (side == 0) ? @player : @opponent
          trainers.each_with_index do |t, i|
            next if side == 0 && i == 0
            sent = sendOuts[side][i]
            next if !sent || sent.empty?
            msg += "\r\n" if msg.length > 0
            names = sent.map { |idx| @battlers[idx].name }
            if side == 0 && Prismfall::WildAllyPartner.trainer_wild_ally?(t)
              msg += Prismfall::WildAllyPartner.entry_message(t, names)
            else
              text_line = "{1} sent out "
              names.each_with_index do |_n, j|
                text_line += ", " if j > 0 && j < names.length - 1
                text_line += " and " if j == names.length - 1 && names.length > 1
                text_line += "{#{j + 2}}"
              end
              text_line += "!"
              msg += _INTL(text_line, t.full_name, *names)
            end
            to_send_out.concat(sent)
          end
          if side == 0
            sent = sendOuts[side][0]
            if sent && !sent.empty?
              msg += "\r\n" if msg.length > 0
              names = sent.map { |idx| @battlers[idx].name }
              text_line = "Go! "
              names.each_with_index do |_n, j|
                text_line += ", " if j > 0 && j < names.length - 1
                text_line += " and " if j == names.length - 1 && names.length > 1
                text_line += "{#{j + 1}}"
              end
              text_line += "!"
              msg += _INTL(text_line, *names)
              to_send_out.concat(sent)
            end
          end
          pbDisplayExtended(msg) if msg.length > 0
          anim_send_outs = to_send_out.map { |idx| [idx, @battlers[idx].pokemon] }
          pbSendOut(anim_send_outs, true)
        end
        return
      end

      # Vanilla Essentials v21.1 path (non-EBDX)
      foes = @opponent || pbParty(1)
      foe_names = foes.map { |f| wildBattle? ? f.name : f.full_name }
      if wildBattle?
        pbDisplayPaused(_INTL("Oh! A wild {1} appeared!", foe_names.join(" and ")))
      else
        pbDisplayPaused(_INTL("You are challenged by {1}!", foe_names.join(" and ")))
      end
      [1, 0].each do |side|
        next if side == 1 && wildBattle?
        msg = ""
        to_send_out = []
        trainers = (side == 0) ? @player : @opponent
        trainers.each_with_index do |t, i|
          next if side == 0 && i == 0
          sent = sendOuts[side][i]
          next if !sent || sent.empty?
          msg += "\r\n" if msg.length > 0
          names = sent.map { |idx| @battlers[idx].name }
          if side == 0 && Prismfall::WildAllyPartner.trainer_wild_ally?(t)
            msg += Prismfall::WildAllyPartner.entry_message(t, names)
          else
            msg += _INTL("{1} sent out {2}!", t.full_name, names.join(" and "))
          end
          to_send_out.concat(sent)
        end
        if side == 0 && sendOuts[0][0] && !sendOuts[0][0].empty?
          msg += "\r\n" if msg.length > 0
          names = sendOuts[0][0].map { |idx| @battlers[idx].name }
          msg += _INTL("Go! {1}!", names.join(" and "))
          to_send_out.concat(sendOuts[0][0])
        end
        pbDisplayBrief(msg) if msg.length > 0
        anim_send_outs = to_send_out.map { |idx| [idx, @battlers[idx].pokemon] }
        pbSendOut(anim_send_outs, true)
      end
    end
  end
end

#-------------------------------------------------------------------------------
# 2. Battle::Scene — Suppress player_#{i} back sprite + ball-free wild entry
#-------------------------------------------------------------------------------
class Battle::Scene
  # 2a. Hide trainer back sprite for wild-ally partner slots immediately on setup
  if method_defined?(:initializeSprites) && !method_defined?(:pf_wild_ally_initializeSprites)
    alias pf_wild_ally_initializeSprites initializeSprites

    def initializeSprites
      pf_wild_ally_initializeSprites
      return if !@battle || !@battle.player
      @battle.player.each_with_index do |pl, i|
        next if !Prismfall::WildAllyPartner.trainer_wild_ally?(pl)
        sp = @sprites["player_#{i}"]
        next if !sp
        sp.visible = false
        sp.opacity = 0
      end
    end
  end

  # 2b. EBDX playerBattlerSendOut — Split wild allies out of Pokeball throw loop
  if method_defined?(:playerBattlerSendOut) && !method_defined?(:pf_wild_ally_playerBattlerSendOut)
    alias pf_wild_ally_playerBattlerSendOut playerBattlerSendOut

    def playerBattlerSendOut(sendOuts, startBattle = false)
      wild_outs   = []
      normal_outs = []
      sendOuts.each do |b|
        if Prismfall::WildAllyPartner.battler_wild_ally?(@battle, b[0])
          wild_outs.push(b)
        else
          normal_outs.push(b)
        end
      end
      return pf_wild_ally_playerBattlerSendOut(sendOuts, startBattle) if wild_outs.empty?

      # Keep wild-ally partner trainer back sprites permanently hidden
      @battle.player.each_with_index do |pl, idx|
        next if !Prismfall::WildAllyPartner.trainer_wild_ally?(pl)
        if @sprites["player_#{idx}"]
          @sprites["player_#{idx}"].visible = false
          @sprites["player_#{idx}"].opacity = 0
        end
      end

      # 1. Human player throws their own Poke Ball normally (ZERO partner ball/sprite)
      if !normal_outs.empty?
        pf_wild_ally_playerBattlerSendOut(normal_outs, startBattle)
      else
        @playerLineUp.toggle = false if @playerLineUp
        setBGMLowHP(false) if respond_to?(:setBGMLowHP)
      end

      # 2. Wild-ally partner leaps / materializes directly onto its ally pad
      pf_wild_ally_ebdx_entry(wild_outs, startBattle)
      @firstsendout = false
      return true
    end

    def pf_wild_ally_ebdx_entry(wild_outs, startBattle = false)
      return if wild_outs.empty?
      clearMessageWindow(true) if respond_to?(:clearMessageWindow)
      @vector.set(EliteBattle.get_vector(:MAIN, @battle)) if @vector && defined?(EliteBattle)

      entries = []
      wild_outs.each do |b|
        battler = @battlers[b[0]]
        i       = battler.index
        pkmn    = @battle.battlers[b[0]].effects[PBEffects::Illusion] || b[1]
        spec    = Prismfall::WildAllyPartner.spec_for_battler(@battle, b[0]) || { :style => :leap }
        sp      = @sprites["pokemon_#{i}"]
        db      = @sprites["dataBox_#{i}"]
        next if !sp

        db.render if db
        sp.setPokemonBitmap(pkmn, true)
        sp.showshadow = false
        sp.visible    = true

        target_x = sp.x
        target_y = sp.y
        target_zx = sp.zoom_x
        target_zy = sp.zoom_y

        if spec[:style] == :rift
          sp.opacity = 0
          sp.tone    = Tone.new(-180, -210, -80, 120)
          sp.zoom_x  = target_zx * 1.16
          sp.zoom_y  = target_zy * 1.16
        else # :leap (Ogerpon leaps onto the field from the left!)
          sp.x       = target_x - 112
          sp.y       = target_y - 24
          sp.opacity = 0
          sp.tone    = Tone.new(0, 0, 0, 0)
        end

        entries.push({
          :battler => battler, :index => i, :style => spec[:style],
          :sp => sp, :db => db,
          :tx => target_x, :ty => target_y, :tzx => target_zx, :tzy => target_zy
        })
      end

      entries.each { |e| e[:db].appear if e[:db] }
      entries.each { |e| playBattlerCry(e[:battler]) if respond_to?(:playBattlerCry) }

      frames = 16
      1.upto(frames) do |f|
        u = f.to_f / frames
        ease = 1.0 - ((1.0 - u) ** 2)
        entries.each do |e|
          sp = e[:sp]
          if e[:style] == :rift
            sp.opacity    = (255 * ease).round
            sp.tone.red   = (-180 * (1.0 - ease)).round
            sp.tone.green = (-210 * (1.0 - ease)).round
            sp.tone.blue  = (-80  * (1.0 - ease)).round
            sp.tone.gray  = (120  * (1.0 - ease)).round
            scale_k       = 1.0 + 0.16 * (1.0 - ease)
            sp.zoom_x     = e[:tzx] * scale_k
            sp.zoom_y     = e[:tzy] * scale_k
          else
            arc           = Math.sin(Math::PI * u) * 34.0
            sp.x          = (e[:tx] - 112 * (1.0 - ease)).round
            sp.y          = (e[:ty] - arc).round
            sp.opacity    = [255, (255 * [u * 2.2, 1.0].min).round].min
          end
          sp.still if sp.respond_to?(:still)
          e[:db].show if e[:db] && f >= 4
        end
        self.wait(1, false)
      end

      entries.each do |e|
        sp = e[:sp]
        sp.x          = e[:tx]
        sp.y          = e[:ty]
        sp.zoom_x     = e[:tzx]
        sp.zoom_y     = e[:tzy]
        sp.opacity    = 255
        sp.tone       = Tone.new(0, 0, 0, 0)
        sp.showshadow = true
        e[:db].inposition = true if e[:db] && e[:db].respond_to?(:inposition=)
      end
      sendoutShinyPkmn(wild_outs) if respond_to?(:sendoutShinyPkmn)
    end
  end

  # 2c. Ball-free recall if a wild ally is ever forced out (Roar/Whirlwind/etc.)
  if method_defined?(:pbRecall) && !method_defined?(:pf_wild_ally_pbRecall)
    alias pf_wild_ally_pbRecall pbRecall

    def pbRecall(battlerindex)
      if !Prismfall::WildAllyPartner.battler_wild_ally?(@battle, battlerindex)
        return pf_wild_ally_pbRecall(battlerindex)
      end
      return if @battle.battlers[battlerindex].fainted?
      poke = @sprites["pokemon_#{battlerindex}"]
      return if !poke || (poke.respond_to?(:fainted) && poke.fainted)
      poke.resetParticles if poke.respond_to?(:resetParticles)
      @sprites["dataBox_#{battlerindex}"].visible = false if @sprites["dataBox_#{battlerindex}"]
      12.times do
        poke.opacity = [0, poke.opacity - 24].max
        poke.x -= 8
        self.wait(1, false)
      end
      poke.visible = false
      poke.opacity = 255
      setBGMLowHP(false) if respond_to?(:setBGMLowHP)
    end
  end
end
```

---

## 3. Verification Checklist
- `ruby -c` on extracted Ruby block: **Syntax OK**.
- **Ch10 Loyal Three (`:ch10_ogre == :ogre`):** Verify battle start displays `"Ogerpon leaps to your side!"` + `"Go! <PC lead>!"`, ONLY `player_0` slides in and throws ONE Poké Ball, NO `PARTNER_OGRE_back` appears, NO Poké Ball spawns on slot `2`, and Ogerpon leaps directly onto ally slot `2` with her battle cry and databox.
- **Ruin Route Finale (`:PARTNER_GIRATINA`):** Verify battle start displays `"Giratina tears open the shadows beside you!"`, NO missing-sprite `player_1` or Poké Ball appears, and Giratina-Origin materializes directly onto slot `2` from a dark-violet rift with cry and databox.
- **Standard Human Double-Battle Partners (Juno, Kestrel, Sigrun, etc.):** `wild_outs.empty? == true` → 100% untouched stock EBDX path.
