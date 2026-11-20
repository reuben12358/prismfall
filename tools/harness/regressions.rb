#===============================================================================
# Regression checks for bugs found by the playtests and win-rate runs (loaded by run_all.rb, section 4).
# Each check is a short scripted battle (Harness::Probes.mini: the player's moves are scripted, the foe uses Splash).
#   * Psycho Shift, with a status and without one: the Generation 9 Pack 3.2.5 override called
#     paldea_pbEffectAgainstTarget without (user, target) and crashed the battle (fixed in-memory by
#     plugins/~Prismfall Base Fixes/003_Gen9_PsychoShift.rb, which boot.rb loads first like the game does).
#   * The Dive loop: Water Surface <-> Underwater. Diving down is a transform strike (x1.3) and moves the battle on the
#     turn Dive strikes; surfacing is not a strike. One Dive = one field change.
# Every check returns { :name, :ok, :detail, :log }; exceptions land in the log's errors (run_all counts them).
#===============================================================================
module Harness
  module Regressions
    def self.foe_hits(log)
      log.hits.select { |idx, _dmg| idx == 1 }.map { |_idx, dmg| dmg }
    end

    def self.changes(log)
      log.field_changes.reject { |o, n, _s| o == :NONE || o == n }.map { |o, n, _s| [o, n] }
    end

    # Runs the block with FieldEffects::TRANSFORM_BOOST set to `value` (to tell whether a hit was a transform strike).
    def self.with_transform_boost(value)
      old = FieldEffects::TRANSFORM_BOOST
      FieldEffects.send(:remove_const, :TRANSFORM_BOOST)
      FieldEffects.const_set(:TRANSFORM_BOOST, value)
      yield
    ensure
      FieldEffects.send(:remove_const, :TRANSFORM_BOOST)
      FieldEffects.const_set(:TRANSFORM_BOOST, old)
    end

    def self.psycho_shift(status)
      user = Probes.mk(:ALAKAZAM, 50, :moves => [:PSYCHOSHIFT], :status => status)
      foe  = Probes.mk(:LAPRAS, 50)   # Water Absorb: nothing blocks or cures the status
      label = status ? "with #{status}" : "without a status"
      log, info = Probes.mini("REGRESSION Psycho Shift #{label} (Gen 9 Pack override)", :field => :NONE,
                              :user => user, :foe => foe, :script => [:PSYCHOSHIFT], :rng => :mid)
      b = info[:battle]
      mine  = b&.battlers&.[](0)&.status
      their = b&.battlers&.[](1)&.status
      ok = log.errors.empty? && !log.outcome.nil?
      if status
        ok &&= (their == status && mine == :NONE)
        detail = "user #{status} -> #{mine}, target NONE -> #{their}"
      else
        ok &&= (their == :NONE) && log.include?(/But it failed/)
        detail = "no status to pass: #{log.include?(/But it failed/) ? '"But it failed!"' : 'no failure message'}, target #{their}"
      end
      detail += ", #{log.errors.size} exception(s)" if !log.errors.empty?
      { :name => "Psycho Shift #{label}", :ok => ok, :detail => detail, :log => log }
    end

    # One Dive from `field`: [log, damage to the foe, field changes]. Fixed rolls (no crits, no misses).
    def self.dive_from(field, boost)
      log = nil
      with_transform_boost(boost) do
        log, = Probes.mini("REGRESSION Dive from #{field} (TRANSFORM_BOOST #{boost})", :field => field,
                           :user => Probes.mk(:MILOTIC, 50, :moves => [:DIVE]), :foe => Probes.mk(:SNORLAX, 100),
                           :script => [:DIVE, :SPLASH], :rng => :mid)
      end
      [log, foe_hits(log).sum, changes(log)]
    end

    def self.dive_checks
      out = []
      [[:WATER_SURFACE, :UNDERWATER, true], [:UNDERWATER, :WATER_SURFACE, false]].each do |from, to, strike|
        log_a, dmg_boost, ch = dive_from(from, 1.3)
        log_b, dmg_plain, = dive_from(from, 1.0)
        boosted = dmg_boost > dmg_plain
        ok = log_a.errors.empty? && log_b.errors.empty? && ch == [[from, to]] && boosted == strike && dmg_plain > 0
        out << { :name => "Dive from #{from}: one change, #{strike ? 'a' : 'not a'} transform strike", :ok => ok,
                 :detail => "field changes #{ch.map { |o, n| "#{o}->#{n}" }.join(', ')}; damage #{dmg_boost} " \
                            "(x1.3 strike on) vs #{dmg_plain} (off)", :log => log_a }
      end
      # The loop itself: two Dives in a row from the surface. Down (strike), back up (no strike), two changes.
      log = nil
      with_transform_boost(1.3) do
        log, = Probes.mini("REGRESSION Dive twice from WATER_SURFACE", :field => :WATER_SURFACE,
                           :user => Probes.mk(:MILOTIC, 50, :moves => [:DIVE]), :foe => Probes.mk(:SNORLAX, 100),
                           :script => [:DIVE, :DIVE, :SPLASH], :rng => :mid)
      end
      ch = changes(log)
      ok = log.errors.empty? && ch == [[:WATER_SURFACE, :UNDERWATER], [:UNDERWATER, :WATER_SURFACE]] && foe_hits(log).size == 2
      out << { :name => "Dive twice from WATER_SURFACE: down, then back up", :ok => ok,
               :detail => "#{foe_hits(log).size} hits, field changes #{ch.map { |o, n| "#{o}->#{n}" }.join(', ')}",
               :log => log }
      out
    end

    def self.run
      Harness.set_badges(18)
      [psycho_shift(:BURN), psycho_shift(:PARALYSIS), psycho_shift(nil)] + dive_checks
    end
  end
end
