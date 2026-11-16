#===============================================================================
# INVERSE - Antumbra, the Kingdom Behind the Glass (recurring). Giratina's mirrored realm,
# where the type chart itself is turned upside down.
#===============================================================================
FieldEffects.register(:INVERSE, {
  :name          => "Inverse Field",
  :backdrop      => "field_inverse",
  :intro_message => "The world turns inside out... Type matchups are reversed!",
  :description   => "Inverse type chart. The Reverse World empowers Ghost, Psychic and Dark and twists the rooms.",
  :nature_power  => :TRIATTACK,
  :camouflage    => :GHOST,
  :secret_power  => 4,
  :inverse       => true,
  :type_mods     => { :GHOST => 1.2, :PSYCHIC => 1.2, :DARK => 1.2 },
  :type_messages => { :GHOST => "The Reverse World answers {1}'s call!" },
  :move_mods     => { :SHADOWFORCE => 1.5, :PHANTOMFORCE => 1.3, :MIRRORSHOT => 1.5, :PSYSHOCK => 1.2,
                      :FOULPLAY => 1.3 },
  :move_messages => { :SHADOWFORCE => "The Distortion surged through {2}!",
                      :FOULPLAY    => "{1} turned the foe's strength against it!" },
  :accuracy_mods => [{ :moves => [:CONFUSERAY, :HYPNOSIS, :DARKVOID], :mult => 1.2 }],
  :move_stat_boosts => [
    { :moves => [:TOPSYTURVY], :user_stats => { :SPEED => 1 },
      :message => "{1} moves freely in the upside-down world!" }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:CONTRARY] }, :stats => { :SPEED => -1 },
      :message => "{1} feels right at home in the reversed world!" }
  ],
  :terrain       => { :extend => { :Psychic => 3 } },
  :hooks         => {
    # The Reverse World stretches Trick Room / Magic Room / Wonder Room
    :after_move => proc { |battle, user, targets, move, num_hits|
      next if user.lastMoveFailed
      eff = { :TRICKROOM => PBEffects::TrickRoom, :MAGICROOM => PBEffects::MagicRoom,
              :WONDERROOM => PBEffects::WonderRoom }[move.id]
      next if !eff || battle.field.effects[eff] <= 0
      battle.field.effects[eff] += 3
      battle.pbDisplay(FieldEffects.format("The Reverse World twisted the dimensions even further!"))
    }
  },
  :seed => { :item => :MAGICALSEED, :stats => { :SPEED => -2, :ATTACK => 1, :SPECIAL_ATTACK => 1 },
             :message => "{1}'s {2} turned its world upside down!" }
})
