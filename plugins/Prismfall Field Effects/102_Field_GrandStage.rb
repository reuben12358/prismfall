#===============================================================================
# GRAND_STAGE - Gym 2 (Normal), Saltmere's opera house. The show must go on.
#===============================================================================
FieldEffects.register(:GRAND_STAGE, {
  :name          => "Grand Stage",
  :backdrop      => "field_grand_stage",
  :intro_message => "The curtain rises! The spotlight blazes over the stage!",
  :description   => "Indoor theater: no weather. Normal moves, songs and dances steal the show.",
  :nature_power  => :HYPERVOICE,
  :camouflage    => :NORMAL,
  :secret_power  => 0,
  :type_mods     => { :NORMAL => 1.5 },
  :type_messages => { :NORMAL => "The crowd roared for {1}!" },
  :move_mods     => { :PAYDAY => 2.0, :ACROBATICS => 1.5, :DRUMBEATING => 1.5, :LASTRESORT => 1.3,
                      :FAKEOUT => 1.5 },
  :move_messages => { :PAYDAY      => "Coins rained down onto the stage!",
                      :ACROBATICS  => "{1} dazzled the audience with acrobatics!",
                      :DRUMBEATING => "The drums thundered through the hall!" },
  :damage_mods   => [
    { :flags => ["Sound"], :mult => 1.5, :message => "{2} resonated through the theater!" },
    { :flags => ["Dance"], :category => :damaging, :mult => 1.5,
      :message => "The spotlight followed {1}'s dance!" },
    { :flags => ["Sound"], :user => { :abilities => [:PUNKROCK, :LIQUIDVOICE] }, :mult => 1.2 }
  ],
  :accuracy_mods => [
    { :moves => [:SING, :GRASSWHISTLE, :SUPERSONIC, :METALSOUND], :mult => 1.3 }
  ],
  :added_effects => [
    { :flags => ["Sound"], :category => :damaging, :chance => 10, :confuse => true,
      :message => "The deafening applause rattled {1}!" }
  ],
  :move_stat_boosts => [
    { :flags => ["Dance"], :category => :status, :user_stats => { :SPEED => 1 },
      :message => "The audience cheered {1}'s performance!" },
    { :moves => [:CELEBRATE], :user_stats => { :ATTACK => 1, :DEFENSE => 1, :SPECIAL_ATTACK => 1,
                                                     :SPECIAL_DEFENSE => 1, :SPEED => 1 },
      :message => "A standing ovation for {1}!" },
    { :moves => [:CHARM, :CAPTIVATE, :TEARFULLOOK], :target_stats => { :SPECIAL_ATTACK => -1 },
      :message => "{1} won the crowd over!" }
  ],
  :on_entry => [
    { :battlers => { :abilities => [:DANCER] }, :stats => { :SPEED => 1 },
      :message => "{1} took center stage!" },
    { :battlers => { :abilities => [:PUNKROCK, :LIQUIDVOICE] }, :stats => { :SPECIAL_ATTACK => 1 },
      :message => "{1} warmed up its voice for the crowd!" }
  ],
  :weather => { :block => [:Sun, :Rain, :Sandstorm, :Hail],
                :block_message => "The theater's roof keeps the weather out!" },
  :seed => { :item => :MAGICALSEED, :stats => { :SPEED => 1 }, :effects => [:laser_focus],
             :message => "{1}'s {2} cast a spotlight on it!" }
})
