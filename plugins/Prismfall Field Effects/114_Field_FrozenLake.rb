#===============================================================================
# FROZEN_LAKE - Gym 10 (Ice), Rimeholt in Isenmar, the Frozen Sea. Thick blue
# lake ice under the aurora. Skaters glide and build speed, boulders freeze
# solid, quakes splinter the surface into jagged spikes. Heat and heavy blows
# crack it (ice attacks refreeze the cracks); when it gives way the battle
# drops into the water (WATER_SURFACE). Three rounds of sunlight thaw it
# (Rev 24 audit: it used to melt at once, though the ice is too thick to Dig).
# "Ice remembers. Every crack. Every weight." - Anja Sorrel
# Family: Elemental.
#===============================================================================
FieldEffects.register(:FROZEN_LAKE, (lambda do
  quakes  = [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :STOMPINGTANTRUM]
  heavies = [:HIGHHORSEPOWER, :HEAVYSLAM, :BODYPRESS, :HEADLONGRUSH, :HEATCRASH]
  slides  = [:QUICKATTACK, :EXTREMESPEED, :AQUAJET, :ACCELEROCK, :FEINT, :MACHPUNCH, :BULLETPUNCH, :JETPUNCH,
             :FIRSTIMPRESSION, :SHADOWSNEAK, :ICESHARD, :ROLLOUT, :ICEBALL, :STEAMROLLER, :SPINOUT, :ICESPINNER,
             :LUNGE, :DEFENSECURL]
  {
    :name          => "Frozen Lake",
    :backdrop      => "field_frozen_lake",
    :family        => :elemental,
    :intro_message => "The battle is taking place on a frozen lake!",
    :description   => "Skaters glide and build speed, boulders freeze, quakes splinter the ice into spikes. Fire, quakes and heavy blows crack it; ice attacks refreeze it; a few rounds of sunlight thaw it.",
    :notes         => ["Ice x1.5. Rock moves freeze into ice boulders (also Ice).",
                       "Skating: Rapid Spin, Rollout, Ice Ball x1.5; Triple Axel, Ice Spinner, Spin Out, Aqua Step, Chilling Water x1.3.",
                       "Sliding: grounded users of priority strikes, Ice Shard, Rollout, Ice Ball, Steamroller, Spin Out, Ice Spinner, Lunge or Defense Curl gain +1 Speed.",
                       "Icy Wind and Glaciate drop Speed one stage more. Slush Rush, Snow Cloak and Ice Body work without hail; Ice Scales and Thick Fat +1 Def on entry.",
                       "Quakes splinter the ice: Earthquake, Magnitude, Bulldoze, Fissure and Stomping Tantrum lay a layer of Spikes on both sides.",
                       "Dig fails (the ice is far too thick). Hail lasts 3 turns longer; Aurora Veil works without hail. Grassy Terrain can't take root.",
                       "Cracking: 3 hits from any mix of damaging Fire moves, quakes and heavy blows (High Horsepower, Heavy Slam, Body Press, Headlong Rush, Heat Crash) -> Water Surface. Each damaging Ice move refreezes one crack.",
                       "Thaw: 3 rounds of sunlight melt the lake (each damaging Ice move refreezes one round's thaw); the harsh sun of Desolate Land melts it at once.",
                       "Elemental Seed: +2 Speed - but the holder skates straight across the jagged ice (1/8 HP)."],
    :nature_power  => :ICEBEAM,
    :camouflage    => :ICE,
    :secret_power  => 9,
    :activate_abilities => [:SLUSHRUSH, :SNOWCLOAK, :ICEBODY],
    :type_mods     => { :ICE => 1.5 },
    :type_messages => { :ICE => "The frozen lake lent its cold to {2}!" },
    :move_mods     => { :RAPIDSPIN => 1.5, :ROLLOUT => 1.5, :ICEBALL => 1.5, :TRIPLEAXEL => 1.3, :ICESPINNER => 1.3,
                        :SPINOUT => 1.3, :AQUASTEP => 1.3, :CHILLINGWATER => 1.3 },
    :move_messages => { :TRIPLEAXEL => "{1} spun gracefully across the ice!",
                        :AQUASTEP   => "{1} danced across the ice!",
                        :ROLLOUT    => "{1} picked up speed on the slick ice!",
                        :ICEBALL    => "{1} picked up speed on the slick ice!",
                        :RAPIDSPIN  => "{1} spun like a top on the ice!" },
    :extra_types   => [
      { :types => [:ROCK], :category => :damaging, :add => :ICE, :message => "The boulders came out frozen solid!" }
    ],
    :move_stat_boosts => [
      { :moves => slides, :user => { :grounded => true }, :user_stats => { :SPEED => 1 },
        :message => "{1} slid across the ice!" },
      { :moves => [:ICYWIND, :GLACIATE], :target_stats => { :SPEED => -1 }, :message => "The lake's chill bit even deeper!" }
    ],
    :move_fails    => [{ :moves => [:DIG], :message => "The ice is far too thick to dig through!" }],
    :on_entry      => [
      { :battlers => { :abilities => [:ICESCALES, :THICKFAT] }, :stats => { :DEFENSE => 1 },
        :message => "{1} settled comfortably onto the ice!" }
    ],
    :weather       => { :extend => { :Hail => 3 } },
    :weather_as    => [{ :moves => [:AURORAVEIL], :as => :Hail }],
    :terrain       => { :block => [:Grassy], :block_message => "Nothing can take root on solid ice!" },
    :hooks         => {
      # Quakes splinter the surface into jagged ice spikes on both sides
      :after_move => proc { |battle, user, targets, move, num_hits|
        next if user.lastMoveFailed || !quakes.include?(move.id)
        added = false
        battle.sides.each do |side|
          next if side.effects[PBEffects::Spikes] >= 3
          side.effects[PBEffects::Spikes] += 1
          added = true
        end
        battle.pbDisplay(FieldEffects.format("The quake splintered the ice into jagged spikes!")) if added
      }
    },
    :transitions   => [
      # One shared "crack meter": fire melts, quakes and heavy bodies split the ice
      { :id => :crack, :condition => proc { |battle, user, target, move, type|
          (type == :FIRE && move.damagingMove?) || quakes.include?(move.id) || heavies.include?(move.id)
        },
        :to => :WATER_SURFACE, :uses => 3,
        :progress_message => "The lake ice groaned and cracked! ({1} more)",
        :message => "The ice gave way! The battle plunged into the freezing lake!" },
      # Ice attacks refreeze the cracks and the thaw (rewind each meter by one)
      { :types => [:ICE], :category => :damaging, :rewind => [:crack, :thaw],
        :message => "The cold sealed the cracks in the ice!" },
      { :id => :thaw, :check => proc { |battle| battle.pbWeather == :Sun }, :to => :WATER_SURFACE, :uses => 3,
        :progress_message => "The sun is softening the lake ice... ({1} more)",
        :message => "The sunlight melted the lake ice into open water!" },
      { :weather => [:HarshSun], :to => :WATER_SURFACE,
        :message => "The blazing sun melted the lake ice into open water!" }
    ],
    :seed => { :item => :ELEMENTALSEED, :stats => { :SPEED => 2 }, :damage => 1/8r,
               :message => "{1}'s {2} sent it skating at full speed - straight across the jagged ice!" }
  }
end).call)
