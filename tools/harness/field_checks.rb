#===============================================================================
# Field logic checks (SPINE Rev 24, design/FIELD_LOGIC_AUDIT.md), loaded by regressions.rb and run by run_all.rb
# section 4. Short scripted battles through the real battle code: the player's moves are scripted (a step can also be
# [:SWITCH, party index]); the foe uses Splash unless it has its own script.
#   Glass Dunes: Hot Glass cools into Mirror Glass after 4 rounds without Fire (sun holds the heat, rain halves the
#   wait), Fire reheats it, damaging sound moves crack it, cracks survive the cooling and Fire anneals one, broken
#   glass stays on the ground as an entry hazard (Heavy-Duty Boots, airborne, Rapid Spin), glass insulates against
#   Electric, Mirror Glass ricochets beams and multiplies Double Team.
#   Audit changes: the Frozen Lake thaws over 3 rounds of sun (Ice moves refreeze it); Sky Drop no longer surfaces an
#   underwater battle; gusts no longer blow a Wildfire out; caverns block sun, rain and hail.
# Every check returns { :name, :ok, :detail, :log }.
#===============================================================================
module Harness
  module FieldChecks
    module_function

    def mk(*a, **k); Probes.mk(*a, **k); end

    # A scripted wild battle with a full party. script / foe_script: move IDs, [:SWITCH, i], or nil (= end).
    def mini(title, field:, party:, foe:, script:, foe_script: nil, stage: nil, rng: :mid, seed: 4242)
      $player.party = party
      info = { :snaps => [] }
      setup = lambda do |battle|
        info[:battle] = battle
        battle.define_singleton_method(:pbRandom) { |x| (rng == :mid) ? x / 2 : 0 } if rng
        queue = script.dup
        fq = foe_script&.dup
        battle.instance_variable_get(:@battleAI).define_singleton_method(:pbDefaultChooseEnemyCommand) do |idx|
          b = @battle.battlers[idx]
          if !@battle.pbOwnedByPlayer?(idx)
            mv = fq ? (fq.shift || :SPLASH) : nil
            i = mv ? b.moves.index { |m| m.id == mv } : 0
            if mv && !i
              b.moves[0] = Battle::Move.from_pokemon_move(@battle, Pokemon::Move.new(mv)); i = 0
            end
            @battle.pbRegisterMove(idx, i, false)
          else
            info[:snaps] << { :turn => @battle.turnCount, :hp => b.hp, :totalhp => b.totalhp, :name => b.name,
                              :stages => b.stages.dup, :field => @battle.field_effect, :stage => @battle.field_stage,
                              :foe_hp => @battle.battlers[1]&.hp }
            step = queue.shift
            if step.nil?
              @battle.decision = 3
            elsif step.is_a?(Array) && step[0] == :SWITCH
              @battle.pbRegisterSwitch(idx, step[1])
            else
              i = b.moves.index { |m| m.id == step }
              if !i
                b.moves[0] = Battle::Move.from_pokemon_move(@battle, Pokemon::Move.new(step)); i = 0
              end
              @battle.pbRegisterMove(idx, i, false)
            end
          end
        end
      end
      log = Harness.run_battle(title, :seed => seed, :setup => setup) do
        setBattleRule("field", (field == :NONE) ? "none" : field)
        setBattleRule("fieldStage", stage) if stage
        setBattleRule("canLose")
        setBattleRule("cannotRun")
        WildBattle.start(foe)
      end
      [log, info]
    end

    def changes(log)
      log.field_changes.reject { |o, _n, _s| o == :NONE }
    end

    def fmt(ch)
      ch.map { |o, n, s| o == n ? "#{o} stage #{s}" : "#{o}->#{n}" }.join(", ")
    end

    def result(name, ok, detail, log)
      detail += ", #{log.errors.size} exception(s)" if !log.errors.empty?
      { :name => name, :ok => ok && log.errors.empty? && !log.outcome.nil?, :detail => detail, :log => log }
    end

    # The turn (1-based) at the end of which the field first reached [id, stage]: from the snapshots.
    def turn_of(info, id, stage)
      s = info[:snaps].find { |x| x[:field] == id && x[:stage] == stage }
      s ? s[:turn] : nil
    end

    #---------------------------------------------------------------------------
    # Glass Dunes
    #---------------------------------------------------------------------------
    def glass_cooling
      out = []
      foe = mk(:SNORLAX)
      log, info = mini("CHECK Glass Dunes: Hot Glass cools after 4 rounds without Fire", :field => :GLASS_DUNES,
                       :party => [mk(:MEW, :moves => [:CALMMIND])], :foe => foe, :script => [:CALMMIND] * 6)
      t = turn_of(info, :GLASS_DUNES, 2)
      ok = changes(log) == [[:GLASS_DUNES, :GLASS_DUNES, 2]] && t == 4 && log.include?(/cooled into|have cooled/)
      out << result("Glass Dunes: Hot Glass cools into Mirror Glass after 4 rounds", ok,
                    "stage 2 from turn #{t.inspect} (want 4); changes #{fmt(changes(log))}", log)
      log, info = mini("CHECK Glass Dunes: sunlight keeps the glass hot", :field => :GLASS_DUNES,
                       :party => [mk(:MEW, :moves => [:SUNNYDAY, :CALMMIND])], :foe => mk(:SNORLAX),
                       :script => [:SUNNYDAY] + [:CALMMIND] * 5)
      ok = changes(log).empty? && info[:snaps].last[:stage] == 1
      out << result("Glass Dunes: sunlight holds the heat (6 rounds, still Hot Glass)", ok,
                    "changes #{fmt(changes(log)).then { |s| s.empty? ? 'none' : s }}", log)
      log, info = mini("CHECK Glass Dunes: rain cools it twice as fast", :field => :GLASS_DUNES,
                       :party => [mk(:MEW, :moves => [:RAINDANCE, :CALMMIND])], :foe => mk(:SNORLAX),
                       :script => [:RAINDANCE] + [:CALMMIND] * 3)
      t = turn_of(info, :GLASS_DUNES, 2)
      out << result("Glass Dunes: rain cools it in 2 rounds", t == 2, "stage 2 from turn #{t.inspect} (want 2)", log)
      log, info = mini("CHECK Glass Dunes: a Fire move every 4th round keeps it hot", :field => :GLASS_DUNES,
                       :party => [mk(:MEW, :moves => [:CALMMIND, :EMBER])], :foe => mk(:SNORLAX),
                       :script => [:CALMMIND, :CALMMIND, :CALMMIND, :EMBER, :CALMMIND, :CALMMIND, :CALMMIND])
      ok = changes(log).empty? && info[:snaps].last[:stage] == 1
      out << result("Glass Dunes: Ember on round 4 resets the cooling", ok,
                    "changes #{fmt(changes(log)).then { |s| s.empty? ? 'none' : s }} after 7 rounds", log)
      log, info = mini("CHECK Glass Dunes: Fire reheats Mirror Glass", :field => :GLASS_DUNES, :stage => 2,
                       :party => [mk(:MEW, :moves => [:EMBER])], :foe => mk(:SNORLAX), :script => [:EMBER, :SPLASH])
      ok = changes(log) == [[:GLASS_DUNES, :GLASS_DUNES, 1]] && log.include?(/flooded back into the glass/)
      out << result("Glass Dunes: a damaging Fire move reheats Mirror Glass", ok, "changes #{fmt(changes(log))}", log)
      out
    end

    def glass_cracking
      out = []
      log, info = mini("CHECK Glass Dunes: three sound moves shatter Mirror Glass", :field => :GLASS_DUNES, :stage => 2,
                       :party => [mk(:MEW, :moves => [:HYPERVOICE])], :foe => mk(:SNORLAX),
                       :script => [:HYPERVOICE] * 3 + [:SPLASH])
      ok = changes(log) == [[:GLASS_DUNES, :DESERT, 1]] && log.include?(/Hyper Voice set the glass ringing/) &&
           log.include?(/shattered into a thousand pieces/)
      out << result("Glass Dunes: 3 damaging sound moves shatter Mirror Glass to the Desert", ok,
                    "changes #{fmt(changes(log))}", log)
      log, info = mini("CHECK Glass Dunes: a crack survives the cooling", :field => :GLASS_DUNES,
                       :party => [mk(:MEW, 50, :moves => [:EARTHQUAKE, :CALMMIND, :BOOMBURST])], :foe => mk(:SNORLAX),
                       :script => [:EARTHQUAKE, :CALMMIND, :CALMMIND, :CALMMIND, :BOOMBURST, :BOOMBURST, :SPLASH])
      ok = changes(log) == [[:GLASS_DUNES, :GLASS_DUNES, 2], [:GLASS_DUNES, :DESERT, 1]] &&
           turn_of(info, :DESERT, 1) == 6
      out << result("Glass Dunes: Earthquake on Hot Glass + 2 Boombursts on Mirror Glass = 3 cracks", ok,
                    "changes #{fmt(changes(log))}; Desert from turn #{turn_of(info, :DESERT, 1).inspect} (want 6)", log)
      log, info = mini("CHECK Glass Dunes: Fire reheats and anneals one crack", :field => :GLASS_DUNES, :stage => 2,
                       :party => [mk(:MEW, 50, :moves => [:HYPERVOICE, :EMBER])], :foe => mk(:SNORLAX),
                       :script => [:HYPERVOICE, :HYPERVOICE, :EMBER, :HYPERVOICE, :HYPERVOICE, :SPLASH])
      ok = changes(log) == [[:GLASS_DUNES, :GLASS_DUNES, 1], [:GLASS_DUNES, :DESERT, 1]] &&
           turn_of(info, :DESERT, 1) == 5 && log.include?(/annealed the cracks/)
      out << result("Glass Dunes: Ember after 2 cracks reheats and anneals one (the 5th move breaks it)", ok,
                    "changes #{fmt(changes(log))}; Desert from turn #{turn_of(info, :DESERT, 1).inspect} (want 5)", log)
      log, info = mini("CHECK Glass Dunes: in the rain the broken glass falls into the flood", :field => :GLASS_DUNES,
                       :party => [mk(:MEW, :moves => [:RAINDANCE, :BULLDOZE])], :foe => mk(:SNORLAX),
                       :script => [:RAINDANCE, :BULLDOZE, :BULLDOZE, :BULLDOZE, :SPLASH])
      ok = changes(log).last&.first(2) == [:GLASS_DUNES, :FLOODED_DUNES]
      out << result("Glass Dunes: 3 cracks in the rain -> Flooded Dunes", ok, "changes #{fmt(changes(log))}", log)
      out
    end

    def glass_shards
      out = []
      party = [mk(:MEW, :moves => [:SPLASH]), mk(:SNORLAX, 50, :moves => [:SPLASH]),
               mk(:GOLEM, 50, :moves => [:SPLASH], :item => :HEAVYDUTYBOOTS)]
      log, info = mini("CHECK Glass Dunes: broken glass is an entry hazard", :field => :GLASS_DUNES, :stage => 2,
                       :party => party, :foe => mk(:EXPLOUD, 60, :moves => [:HYPERVOICE]),
                       :foe_script => [:HYPERVOICE, :SPLASH, :SPLASH],
                       :script => [:SPLASH, [:SWITCH, 1], [:SWITCH, 2], :SPLASH])
      sx = party[1]
      stepped = log.lines.select { |l| l =~ /stepped on the broken glass/ }
      hp_line = log.lines.find { |l| l =~ /HP Snorlax \(player\): (\d+) -> (\d+) \/ (\d+)/ }
      lost = hp_line && (hp_line[/: (\d+) ->/, 1].to_i - hp_line[/-> (\d+)/, 1].to_i)
      want = (sx.totalhp / 16.0).round
      ok = log.include?(/Broken glass lies scattered on the ground around your team/) && stepped.size == 1 &&
           stepped.first.include?("Snorlax") && lost == want
      out << result("Glass Dunes: a crack leaves broken glass; grounded switch-in takes 1/16, Heavy-Duty Boots none", ok,
                    "#{stepped.size} step(s) (#{stepped.map(&:strip).join('; ')}); Snorlax lost #{lost.inspect} (want #{want})", log)
      party = [mk(:MEW, :moves => [:RAPIDSPIN]), mk(:SNORLAX, 50, :moves => [:SPLASH])]
      log, info = mini("CHECK Glass Dunes: Rapid Spin sweeps the glass away", :field => :GLASS_DUNES, :stage => 2,
                       :party => party, :foe => mk(:EXPLOUD, 60, :moves => [:HYPERVOICE]),
                       :foe_script => [:HYPERVOICE, :SPLASH, :SPLASH],
                       :script => [:SPLASH, :RAPIDSPIN, [:SWITCH, 1], :SPLASH])
      ok = log.include?(/swept the broken glass away/) && !log.include?(/stepped on the broken glass/)
      out << result("Glass Dunes: Rapid Spin clears the broken glass", ok,
                    "#{log.include?(/swept the broken glass away/) ? 'swept' : 'NOT swept'}; " \
                    "#{log.include?(/stepped on the broken glass/) ? 'still stepped on' : 'no step after'}", log)
      out
    end

    def glass_insulation_and_mirror
      out = []
      dmg = lambda do |field, stage, move, user = :MEW|
        log, = mini("CHECK Glass Dunes: #{move} on #{field}#{stage ? " stage #{stage}" : ''}", :field => field,
                    :stage => stage, :party => [mk(user, :moves => [move])], :foe => mk(:SNORLAX), :script => [move])
        [log, log.lines.find { |l| l =~ /HP Snorlax \(foe\)/ }.then { |l| l ? l[/: (\d+) ->/, 1].to_i - l[/-> (\d+)/, 1].to_i : nil }]
      end
      la, on = dmg.call(:GLASS_DUNES, nil, :THUNDERBOLT)
      lb, off = dmg.call(:NONE, nil, :THUNDERBOLT)
      r = (on && off && off > 0) ? (on.to_f / off).round(2) : nil
      out << result("Glass Dunes: glass insulates (Thunderbolt x0.8 against a grounded target)", r && r.between?(0.75, 0.85),
                    "#{on.inspect} on glass vs #{off.inspect} with no field (x#{r.inspect})", la)
      log, = mini("CHECK Glass Dunes: Electric Terrain can't form", :field => :GLASS_DUNES,
                  :party => [mk(:MEW, :moves => [:ELECTRICTERRAIN])], :foe => mk(:SNORLAX), :script => [:ELECTRICTERRAIN])
      out << result("Glass Dunes: Electric Terrain fails on the glass", log.include?(/glass won't carry a current/),
                    log.include?(/glass won't carry a current/) ? "blocked" : "NOT blocked", log)
      lm, mir = dmg.call(:GLASS_DUNES, 2, :FLASHCANNON)
      lh, hot = dmg.call(:GLASS_DUNES, nil, :FLASHCANNON)
      _, none = dmg.call(:NONE, nil, :FLASHCANNON)
      rm = (mir && none && none > 0) ? (mir.to_f / none).round(2) : nil
      rh = (hot && none && none > 0) ? (hot.to_f / none).round(2) : nil
      out << result("Glass Dunes: Flash Cannon x1.3 on Hot Glass, x1.5 ricocheting on Mirror Glass",
                    rm && rh && rm.between?(1.45, 1.55) && rh.between?(1.25, 1.35),
                    "hot x#{rh.inspect}, mirror x#{rm.inspect} (#{hot.inspect} / #{mir.inspect} vs #{none.inspect})", lm)
      log, info = mini("CHECK Glass Dunes: Double Team on Mirror Glass", :field => :GLASS_DUNES, :stage => 2,
                       :party => [mk(:MEW, :moves => [:DOUBLETEAM])], :foe => mk(:SNORLAX), :script => [:DOUBLETEAM, :SPLASH])
      eva = info[:snaps].last&.[](:stages)&.[](:EVASION)
      # Gemini review 2026-11-21: Mirror Glass no longer amplifies evasion (RNG cheese); normal +1
      out << result("Glass Dunes: Double Team is normal strength on Mirror Glass (+1, no amplification)", eva == 1,
                    "evasion stage #{eva.inspect} after one Double Team", log)
      out
    end

    #---------------------------------------------------------------------------
    # Audit changes elsewhere
    #---------------------------------------------------------------------------
    def frozen_lake_thaw
      out = []
      log, info = mini("CHECK Frozen Lake: 3 rounds of sun melt it", :field => :FROZEN_LAKE,
                       :party => [mk(:MEW, :moves => [:SUNNYDAY, :CALMMIND])], :foe => mk(:SNORLAX),
                       :script => [:SUNNYDAY, :CALMMIND, :CALMMIND, :CALMMIND, :SPLASH])
      t = turn_of(info, :WATER_SURFACE, 1)
      ok = changes(log).map { |o, n, _| [o, n] } == [[:FROZEN_LAKE, :WATER_SURFACE]] && t == 3
      out << result("Frozen Lake: sunlight thaws it over 3 rounds (not at once)", ok,
                    "Water Surface from turn #{t.inspect} (want 3: sun on rounds 1-3)", log)
      log, info = mini("CHECK Frozen Lake: an Ice move in the sun refreezes the thaw", :field => :FROZEN_LAKE,
                       :party => [mk(:MEW, :moves => [:SUNNYDAY, :CALMMIND, :ICEBEAM])], :foe => mk(:SNORLAX),
                       :script => [:SUNNYDAY, :CALMMIND, :ICEBEAM, :CALMMIND, :SPLASH])
      t = turn_of(info, :WATER_SURFACE, 1)
      out << result("Frozen Lake: Ice Beam during the thaw sets it back a round", t == 4,
                    "Water Surface from turn #{t.inspect} (want 4)", log)
      out
    end

    def other_audit_changes
      out = []
      log, = mini("CHECK Underwater: Sky Drop fails and stays down", :field => :UNDERWATER,
                  :party => [mk(:MEW, :moves => [:SKYDROP])], :foe => mk(:SNORLAX), :script => [:SKYDROP, :SPLASH])
      out << result("Underwater: Sky Drop fails and no longer surfaces the battle", changes(log).empty?,
                    "changes #{fmt(changes(log)).then { |s| s.empty? ? 'none' : s }}", log)
      log, = mini("CHECK Wildfire: Tailwind fans the fire, it doesn't blow it out", :field => :WILDFIRE,
                  :party => [mk(:MEW, :moves => [:TAILWIND])], :foe => mk(:SNORLAX), :script => [:TAILWIND, :SPLASH])
      out << result("Wildfire: Tailwind no longer turns it to Embers", changes(log).empty?,
                    "changes #{fmt(changes(log)).then { |s| s.empty? ? 'none' : s }}", log)
      log, = mini("CHECK Crystal Cavern: no sun underground", :field => :DARK_CRYSTAL,
                  :party => [mk(:MEW, :moves => [:SUNNYDAY])], :foe => mk(:SNORLAX), :script => [:SUNNYDAY, :SPLASH])
      ok = changes(log).empty? && log.include?(/no sky down here|can't reach the cavern/)
      out << result("Dark Crystal Cavern: Sunny Day fails underground (no longer relights it)", ok,
                    "changes #{fmt(changes(log)).then { |s| s.empty? ? 'none' : s }}", log)
      out
    end

    def run
      glass_cooling + glass_cracking + glass_shards + glass_insulation_and_mirror + frozen_lake_thaw + other_audit_changes
    end
  end
end
