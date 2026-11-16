#===============================================================================
# NEW_MOON - Gym 16 (Dark), Underveil, the heart of Nadir, the City Below.
# A black sky with a dead moon and a cold starfield over the undercity rooftops.
# Darkness blinds all but Dark/Ghost Pokemon and keen eyes; the moon gives no
# light, but stars and true light pierce the dark (3 light moves clear it).
#===============================================================================
FieldEffects.register(:NEW_MOON, {
  :name          => "New Moon",
  :backdrop      => "field_new_moon",
  :intro_message => "The moon has gone dark over Underveil... Something moves in the shadows.",
  :description   => "Dark is empowered and the dark lowers accuracy. Moonlight fails; starlight and true light pierce the dark.",
  :notes         => ["Dark x1.5. Non-Dark, non-Ghost Pokemon are less accurate (Keen Eye, Illuminate, etc. see fine).",
                     "Moonlight fails and Moonblast is weaker. Swift, Meteor Mash and Meteor Beam draw on the stars.",
                     "Light moves (Dazzling Gleam, Flash Cannon, Photon Geyser...) x1.3. Flash blinds even more.",
                     "Sun can't break through. 3 light moves (Flash counts) end the darkness."],
  :nature_power  => :DARKPULSE,
  :camouflage    => :DARK,
  :secret_power  => 8,
  :type_mods     => { :DARK => 1.5 },
  :type_messages => { :DARK => "The darkness of the new moon deepened!" },
  :move_mods     => { :MOONBLAST => 0.75, :SWIFT => 1.5, :METEORMASH => 1.3, :METEORBEAM => 1.3,
                      :NIGHTDAZE => 1.3, :FEINTATTACK => 1.5, :THIEF => 1.5 },
  :move_messages => { :MOONBLAST => "With no moon in the sky, {2} lost its glow...",
                      :SWIFT     => "A shower of stars rained down!",
                      :METEORMASH => "The starfield lent {1} its power!",
                      :METEORBEAM => "The starfield lent {1} its power!",
                      :FEINTATTACK => "{1} struck from the shadows!",
                      :THIEF     => "{1} pilfered under cover of darkness!" },
  # True light pierces the dark
  :damage_mods   => [
    { :moves => [:DAZZLINGGLEAM, :LIGHTOFRUIN, :PHOTONGEYSER, :PRISMATICLASER, :LUSTERPURGE, :MIRRORSHOT,
                 :FLASHCANNON, :LUMINACRASH, :AURORABEAM, :SIGNALBEAM], :mult => 1.3,
      :message => "{2} pierced the darkness!" }
  ],
  :accuracy_mods => [
    # The dark blinds everything that can't see in it
    { :user => { :not_types => [:DARK, :GHOST],
                 :not_abilities => [:KEENEYE, :ILLUMINATE, :MINDSEYE, :COMPOUNDEYES, :NOGUARD] }, :mult => 0.9 },
    { :moves => [:NIGHTDAZE], :set => 100 }
  ],
  :move_fails    => [{ :moves => [:MOONLIGHT], :message => "But there is no moon in the sky tonight..." }],
  :move_stat_boosts => [
    { :moves => [:FLASH], :target_stats => { :ACCURACY => -1 },
      :message => "The sudden flash was blinding in the dark!" },
    { :moves => [:COSMICPOWER], :user_stats => { :SPECIAL_ATTACK => 1 },
      :message => "{1} drew power from the cold stars!" }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:ILLUMINATE] }, :stats => { :ACCURACY => 1 },
      :message => "{1}'s glow lit up the darkness!" }
  ],
  :weather       => { :block => [:Sun, :HarshSun], :block_message => "The new moon swallowed the sunlight!" },
  :transitions   => [
    { :moves => [:FLASH, :TAILGLOW, :DAZZLINGGLEAM, :LIGHTOFRUIN, :PHOTONGEYSER, :PRISMATICLASER,
                 :LUSTERPURGE, :MIRRORSHOT, :FLASHCANNON, :LUMINACRASH], :to => :NONE, :uses => 3,
      :progress_message => "Light pierces the darkness... ({1} more)",
      :message => "Light floods the Underveil! The lamps of Nadir flicker back to life." }
  ],
  :seed => { :item => :MAGICALSEED, :stats => { :ACCURACY => 1 }, :effects => [:focus_energy],
             :message => "{1}'s {2} sharpened its night vision!" }
})
