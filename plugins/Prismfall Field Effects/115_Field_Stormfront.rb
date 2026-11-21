#===============================================================================
# STORMFRONT - Gym 11 (Flying), Skyreach in Zenith. An airship deck at the top
# of the spire, inside the permanent storm wall. Fliers ride the gale, wind
# moves howl, Tailwinds last, hazards blow off the deck, and in the rain the
# lightning seeks out whatever flies highest - unless an Electric Pokemon
# channels it first. Call the sun twice and the storm breaks into a RAINBOW.
# "Skyreach's got one law: the wind doesn't care." - Odessa Gale
# Family: Elemental.
#===============================================================================
FieldEffects.register(:STORMFRONT, (lambda do
  winds  = [:GUST, :TWISTER, :HURRICANE, :AIRCUTTER, :RAZORWIND, :ICYWIND, :HEATWAVE, :FAIRYWIND, :SILVERWIND,
            :OMINOUSWIND, :PETALBLIZZARD, :BLIZZARD, :BLEAKWINDSTORM, :WILDBOLTSTORM, :SANDSEARSTORM,
            :SPRINGTIDESTORM, :AEROBLAST]
  storms = [:HURRICANE, :THUNDER, :BLEAKWINDSTORM, :WILDBOLTSTORM, :SANDSEARSTORM, :SPRINGTIDESTORM]
  rainy  = [:Rain, :HeavyRain]
  {
    :name          => "Stormfront",
    :backdrop      => "field_stormfront",
    :family        => :elemental,
    :intro_message => "Gale-force winds howl across the airship deck!",
    :description   => "Fliers ride the gale, wind and Electric moves surge, Tailwind lingers and hazards blow off the deck. In rain, lightning strikes the highest flier - or an Electric Pokemon channels it.",
    :notes         => ["Electric x1.3, Flying x1.2. Wind moves (Gust, Twister, Hurricane, Air Cutter, Icy Wind, Heat Wave, Silver Wind, the four Storm moves...) x1.2.",
                       "Smack Down x2 and Thousand Arrows x1.5 (slammed onto the deck); Fly, Bounce, Sky Drop, Sky Attack, Dragon Ascent x1.3.",
                       "Hurricane, Thunder and the Storm moves never miss.",
                       "Spikes, Toxic Spikes and Sticky Web blow off the deck (they fail). Tailwind lasts 2 turns longer.",
                       "On entry: Wind Rider +1 Attack, Wind Power charged, Big Pecks +1 Defense, Levitate +1 Speed.",
                       "Lightning (rain only): each turn every airborne Pokemon may be struck (15%, 1/8 HP, Electric-scaled). Airborne Electric types channel it instead (+1 Sp. Atk); Lightning Rod (+1 Sp. Atk), Motor Drive (+1 Speed) and Volt Absorb (heals 1/8) draw the bolts.",
                       "The storm swallows the sun: Sun can't start. Electric Terrain lasts 3 turns longer.",
                       "2 Sunny Days (they count even though the sun can't break through) tear the storm open -> Rainbow.",
                       "Elemental Seed: +1 Speed and Charge."],
    :nature_power  => :HURRICANE,
    :camouflage    => :FLYING,
    :secret_power  => 0,
    :type_mods     => { :FLYING => 1.2, :ELECTRIC => 1.3 },
    :type_messages => { :ELECTRIC => "The storm supercharged {2}!",
                        :FLYING   => "{1} rode the gale into the attack!" },
    :move_mods     => { :SMACKDOWN => 2.0, :THOUSANDARROWS => 1.5, :FLY => 1.3, :BOUNCE => 1.3, :SKYDROP => 1.3,
                        :SKYATTACK => 1.3, :DRAGONASCENT => 1.3 },
    :move_messages => { :SMACKDOWN      => "The gale slammed the target onto the deck!",
                        :THOUSANDARROWS => "The gale slammed the target onto the deck!",
                        :FLY            => "{1} rode the updraft!",
                        :SKYATTACK      => "{1} dove out of the storm clouds!" },
    :damage_mods   => [
      { :moves => winds, :category => :damaging, :mult => 1.2, :message => "The gale whipped {2} into a frenzy!" }
    ],
    :accuracy_mods => [{ :moves => storms, :always_hit => true }],
    :move_fails    => [
      { :moves => [:SPIKES, :TOXICSPIKES, :STICKYWEB], :message => "The gale blew {2} right off the deck!" }
    ],
    :effect_durations => { :TAILWIND => [2, "The storm will carry the Tailwind for longer!"] },
    :on_entry      => [
      { :battlers => { :abilities => [:WINDRIDER] }, :stats => { :ATTACK => 1 }, :also_on_change => true,
        :message => "{1} caught the gale!" },
      { :battlers => { :abilities => [:WINDPOWER] }, :effects => [:charge], :also_on_change => true,
        :message => "The howling wind charged {1} with power!" },
      { :battlers => { :abilities => [:BIGPECKS] }, :stats => { :DEFENSE => 1 },
        :message => "{1} puffed up its feathers against the wind!" },
      { :battlers => { :abilities => [:LEVITATE] }, :stats => { :SPEED => 1 },
        :message => "{1} drifted on the storm currents!" }
    ],
    :end_of_round  => [
      # In the rain the storm breaks: lightning finds the highest target...
      { :battlers => { :grounded => false, :in_weather => rainy, :not_types => [:ELECTRIC],
                       :not_abilities => [:LIGHTNINGROD, :VOLTABSORB, :MOTORDRIVE] },
        :chance => 15, :damage => 1/8r, :damage_type => :ELECTRIC, :animation => "Paralysis",
        :message => "Lightning arced down at {1}!" },
      # ...unless something channels it
      { :battlers => { :grounded => false, :in_weather => rainy, :types => [:ELECTRIC],
                       :not_abilities => [:LIGHTNINGROD, :VOLTABSORB, :MOTORDRIVE] },
        :chance => 15, :stats => { :SPECIAL_ATTACK => 1 }, :message => "{1} channelled the lightning!" },
      { :battlers => { :abilities => [:LIGHTNINGROD], :in_weather => rainy },
        :chance => 15, :stats => { :SPECIAL_ATTACK => 1 }, :message => "{1} drew a lightning bolt!" },
      { :battlers => { :abilities => [:MOTORDRIVE], :in_weather => rainy },
        :chance => 15, :stats => { :SPEED => 1 }, :message => "{1} drew a lightning bolt!" },
      { :battlers => { :abilities => [:VOLTABSORB], :in_weather => rainy },
        :chance => 15, :heal => 1/8r, :message => "{1} drew a lightning bolt!" }
    ],
    :weather       => { :block => [:Sun], :block_message => "A shaft of sun pries at the storm clouds!" },   # reads as progress: it counts toward Rainbow
    :terrain       => { :extend => { :Electric => 3 } },
    :transitions   => [
      { :moves => [:SUNNYDAY], :even_if_failed => true, :to => :RAINBOW, :uses => 2,
        :progress_message => "A shaft of sunlight pierces the storm wall... ({1} more)",
        :message => "The sun tore the storm open! A rainbow arcs over the airship deck!" }
    ],
    :seed => { :item => :ELEMENTALSEED, :stats => { :SPEED => 1 }, :effects => [:charge],
               :message => "{1}'s {2} crackled with storm energy!" }
  }
end).call)
