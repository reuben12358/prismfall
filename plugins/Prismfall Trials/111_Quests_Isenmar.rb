#===============================================================================
# Prismfall Trials - 111 Isenmar: The Tally (Chapter 4, implemented)
#-------------------------------------------------------------------------------
# Viking-saga flavour: deeds, endurance, oaths, the sea, tavern contests. Quests
# are runes carved on the Tally Mast; a finished deed gets a notch and a verse
# from a skald, who exaggerates.
# Halls this early: the Half-Tally at the Two Hearths, Frostwick (573), a
# borderland board shared with Elowen's lanterns (Ingrith carves runes, her
# wife Maelon hangs lanterns, they argue about the board), and the Ebbmouth
# Net Loft (160/167, skald Bersi Gullsong). Also here: The Rehearsal (Elowen
# board, posted at the Half-Tally).
#===============================================================================
tr = Prismfall::Trials
tr::SPEAKERS.merge!({
  :INGRITH => "Ingrith", :MAELON => "Sister Maelon", :BERSI => "Bersi Gullsong", :BRENNA => "Brenna",
  :SIGVALD => "Sigvald", :HALVARD => "Halvard", :ASTA => "Old Asta", :GORM => "Gorm", :MARISOL => "Marisol",
  :GUDRUN => "Old Gudrun"
})

tr.quest(:IS_TWO_HEARTHS, {
  :trial => :ISENMAR, :title => "Two Hearths, One Pot", :giver => "Brenna and Sigvald", :map => 573,
  :where => "the Two Hearths inn, Frostwick", :rank => 1, :points => 2, :joint => { :ELOWEN => 2 },
  :rec_level => 16, :chapter => 4, :unlock => "badges >= 2", :board => true, :tags => [:delivery, :comedy, :borderland],
  :summary => "The Two Hearths has two fireplaces, two cooks and one cooking contest that has lasted nineteen years. Both cooks want you to fetch their secret ingredient.",
  :steps => { :ask => "Brenna wants wild honey from the Rimewood hives. Sigvald wants smoked eel from Halvard's Smokehouse.",
              :cook => "You have the honey and the eel. Go back to the Two Hearths." },
  :reward => { :items => [[:HONEY, 3], [:LAVACOOKIE, 2]] },
  :outcomes => { :one_pot => { :items => [[:RARECANDY, 1]] } },
  :touches => "Joint Trial (Elowen + Isenmar points); WORLD.md's Frostwick sidequest 'The Two Hearths'",
  :scenes => {
    :offer => [
      { :map => "Two fireplaces face each other across the inn. At the left, Brenna (Elowen, flour to the elbows). At the right, Sigvald (Isenmar, smoke in his beard)." },
      [:BRENNA, :happy, "A traveller! Settle something. Whose stew is better?"],
      [:SIGVALD, :deadpan, "Don't answer that. She's been asking travellers for nineteen years. They all lie to her."],
      [:BRENNA, :angry, "They lie to YOU."],
      [:SIGVALD, :neutral, "Midwinter cook-off's tonight. I need smoked eel from Halvard. Proper eel. Black as a boot."],
      [:BRENNA, :neutral, "And I need wild honey from the hives in the Rimewood. Frost honey. It tastes like the forest's asleep."],
      [:SIGVALD, :deadpan, "Fetch both. Then choose. Then never come back. That's the tradition."],
      { :choice => "Fetch both ingredients?", :options => [
          ["Both. Fine.", [{ :accept => true }, [:BRENNA, :happy, "A diplomat!"], [:SIGVALD, :deadpan, "A coward. Same thing."]]],
          ["Not tonight.", []]] }
    ],
    :hive => [
      { :if => "quest_flag(:SELF, :honey)", :then => ["The hive hums contentedly. You've already been tipped.", { :end => true }] },
      "A hive hangs from a frost-glazed oak, humming. A Combee peers out and looks you up and down.",
      "It drops a frozen comb of honey into your hands, like a tip, and goes back inside.",
      { :flag => [:honey, true] }, { :run => :check }
    ],
    :smokehouse => [
      { :if => "quest_flag(:SELF, :eel)", :then => [[:HALVARD, :neutral, "Go on. Tell Sigvald I smoked it twice. He'll know what that means."], { :end => true }] },
      [:HALVARD, :neutral, "Eel for Sigvald? Sit. Nobody leaves my smokehouse without hearing about my father's boat."],
      { :choice => "Sit and listen?", :options => [
          ["Sit.", ["Halvard tells you about his father's boat. It sank. Then it sank again, somehow. It takes a long time.",
                    [:HALVARD, :happy, "Good listener. Here. Black as a boot."], { :flag => [:eel, true] }, { :run => :check }]],
          ["Pay instead ($300).", [{ :if => "money >= 300", :then => [{ :pay => 300 }, [:HALVARD, :sad, "Money. Fine. The boat story's free next time."],
                                                                   { :flag => [:eel, true] }, { :run => :check }],
                                   :else => [[:HALVARD, :deadpan, "You haven't got it. Sit down."]] }]]] }
    ],
    :check => [
      { :if => "quest_flag(:SELF, :honey) && quest_flag(:SELF, :eel)", :then => [{ :step => :cook }] }
    ],
    :cook => [
      [:BRENNA, :happy, "You've got my honey!"],
      [:SIGVALD, :neutral, "And my eel. Now. Choose."],
      { :choice => "Who gets their ingredient?", :options => [
          ["Brenna gets the honey.", [
             "Brenna's honey-cake stew wins. Sigvald says nothing for an hour, then asks for the recipe in a whisper.",
             { :complete => :brenna }]],
          ["Sigvald gets the eel.", [
             "Sigvald's eel stew wins. Brenna throws a ladle, then a second ladle, then asks for seconds.",
             { :complete => :sigvald }]],
          ["Put both in one pot.", [
             "You tip the honey and the eel into the same pot. Both cooks scream in two accents.",
             "The pot bubbles. The whole inn goes quiet. Someone tastes it.",
             "Honey-glazed smoked eel. Sweet and black and salt-bitter. The room erupts.",
             [:BRENNA, :shocked, "...That's good."],
             [:SIGVALD, :shocked, "That's very good. I hate it."],
             [:BRENNA, :happy, "One pot. Nineteen years and nobody thought of one pot."],
             { :complete => :one_pot }]]] },
      "A rune is cut in the Half-Tally and a lantern is hung beside it. Both sides of the board claim you now."
    ]
  }
})

tr.quest(:IS_OATH_PARCEL, {
  :trial => :ISENMAR, :title => "The Oathbound Parcel", :giver => "Ingrith", :map => 573,
  :where => "the Half-Tally, Frostwick", :rank => 1, :points => 3, :rec_level => 17, :chapter => 4,
  :unlock => "badges >= 2", :board => true, :tags => [:delivery, :event_mon, :comedy, :oath],
  :summary => "Carry a sealed oath-parcel from Frostwick to the Net Loft in Ebbmouth. In Isenmar a carried oath is not opened. Not ever.",
  :steps => { :carry => "Carry Ingrith's sealed parcel to Bersi Gullsong at the Ebbmouth Net Loft. Do not open it.",
              :deliver => "Deliver the parcel (or what's left of it) to Bersi in Ebbmouth." },
  :reward => { :money => 500 },
  :touches => "Isenmar 'oath' flavour: opening it costs a Trial point and earns you a very rude verse",
  :scenes => {
    :offer => [
      [:INGRITH, :neutral, "This goes to the Net Loft in Ebbmouth. Sealed with my rune. You carry it, you swear on it."],
      [:MAELON, :worried, "Ingrith, it's moving."],
      [:INGRITH, :deadpan, "It's settling."],
      [:MAELON, :worried, "It's settling with its teeth."],
      [:INGRITH, :neutral, "Whatever it does, you don't open it. A carried oath is a carried oath. Swear?"],
      { :choice => "Swear on the parcel?", :options => [
          ["I swear.", [{ :accept => true }, [:INGRITH, :happy, "Good. Hold it the right way up. That way."], [:MAELON, :deadpan, "That way is upside down."]]],
          ["What's in it?", [[:INGRITH, :deadpan, "An oath. Swear or don't."]]]] }
    ],
    :rattle => [
      { :if => "quest_flag(:SELF, :rattled)", :then => [{ :end => true }] },
      { :flag => [:rattled, true] },
      "On the cliff path, the parcel lurches in your arms. Something inside it says \"snom\" in a small, offended voice.",
      "A corner of the wrapping has been chewed through. Frost is creeping out of the hole.",
      { :choice => "Open the parcel?", :options => [
          ["Open it.", [
             "You tear open the parcel. A Snom tumbles out, coughing up rime-silk, and stares at you with enormous eyes.",
             "It has decided you are its mother. It climbs into your bag and refuses to leave.",
             { :gift => :IS_SNOM }, { :flag => [:opened, true] }, { :step => :deliver }]],
          ["Keep your oath.", [
             "You hold the parcel tighter. It says \"snom\" again, sulkily, and goes back to chewing.",
             { :step => :deliver }]]] }
    ],
    :deliver => [
      { :if => "quest_step(:SELF) == :carry", :then => [{ :step => :deliver }] },
      { :if => "quest_flag(:SELF, :opened)", :then => [
          [:BERSI, :shocked, "You OPENED it?"],
          [:BERSI, :angry, "OATH-BREAKER! Oath-breaker in my loft! I'll sing of this! I'll sing of this for YEARS!"],
          "The Snom peeks out of your bag.",
          [:BERSI, :deadpan, "...Well, it ate the oath anyway. Ingrith always seals them in rime-silk. Snom love rime-silk."],
          [:BERSI, :neutral, "Keep it. It's bonded. Taking it off you now would be crueller than the verse I'm going to write."],
          { :points => [:ISENMAR, -1] }, { :complete => :opened }
        ], :else => [
          [:BERSI, :happy, "Ingrith's rune, unbroken! Ha! A true carrier!"],
          "Bersi slits the seal. A Snom falls out, fat with rime-silk, and immediately crawls back toward you.",
          [:BERSI, :neutral, "Ingrith seals her oaths in rime-silk. And Snom eat rime-silk. Every year. Every year she forgets."],
          [:BERSI, :happy, "It's imprinted on the hands that carried it. Those are yours. Take it, oath-keeper."],
          { :gift => :IS_SNOM }, { :complete => :kept }
        ] }
    ]
  }
})

tr.quest(:IS_SKALDS_SAGA, {
  :trial => :ISENMAR, :title => "A Deed for the Skald", :giver => "Bersi Gullsong", :map => 160,
  :where => "the Ebbmouth Net Loft", :rank => 1, :points => 2, :rec_level => 19, :chapter => 4,
  :unlock => "badges >= 2", :board => true, :tags => [:comedy, :battle, :contest],
  :summary => "The Ebb Guild feast is tonight and Bersi has no new saga. He needs a deed. Any deed. He'll handle the exaggerating.",
  :steps => { :ask => "Do something saga-worthy in Ebbmouth: beat Gorm the dock bully, or out-fish Old Gudrun (catch 3 Water-type Pokemon).",
              :feast => "Go back to the Net Loft for the feast." },
  :reward => { :items => [[:MYSTICWATER, 1]] },
  :outcomes => { :bully => { :effects => "MARISOL+1" }, :tall_tale => { :replace => true, :items => [[:POTION, 1]] } },
  :touches => "Marisol bond (+1 for flattening Gorm, who she can't touch because he's Guild)",
  :scenes => {
    :offer => [
      [:BERSI, :sad, "A skald with no saga is just a man shouting in a loft."],
      [:BERSI, :neutral, "Feast's tonight. Nothing's happened in Ebbmouth for a month except the river stopping, and nobody wants a song about that."],
      [:BERSI, :happy, "So. Do something! Anything! I'll make it bigger. That's the job."],
      { :choice => "What deed will you do?", :options => [
          ["Flatten Gorm the dock bully.", [{ :accept => true }, { :flag => [:deed, :bully] },
             [:BERSI, :happy, "Gorm! He charges the net-menders a toll to walk past his crates. Nobody stops him, he's Guild."]]],
          ["Out-fish Old Gudrun.", [{ :accept => true }, { :flag => [:deed, :fish] },
             [:BERSI, :happy, "Catch three water beasts before the feast! Gudrun caught two in a morning, once, in her prime. In AF 261."]]],
          ["I already did something great.", [{ :accept => true }, { :flag => [:deed, :tale] },
             [:BERSI, :shocked, "You did? What?"],
             { :choice => "Your great deed:", :options => [
                 ["I punched a Gyarados.", [{ :flag => [:tale, :gyarados] }]],
                 ["I walked through a Bleed Veil.", [{ :flag => [:tale, :veil] }]],
                 ["I ate Larch's kelp tea.", [{ :flag => [:tale, :tea] }]]] },
             [:BERSI, :happy, "MAGNIFICENT. A skald never checks his sources. To the feast!"], { :step => :feast }, { :run => :feast }]]] }
    ],
    :gorm => [
      [:GORM, :smug, "Toll's ten. Twenty for you. You look like you've got pockets."],
      { :trainer => [:SAILOR, "Gorm", 50],
        :won => [[:GORM, :angry, "Fine! FINE. Walk past my crates. Walk on them. See if I care."],
                 "The net-menders cheer from the quay. Somebody throws a fish. It might be a celebration.", { :step => :feast }],
        :lost => [[:GORM, :smug, "That'll be twenty."]] }
    ],
    :feast => [
      { :if => "quest_flag(:SELF, :deed) == :fish && quest_count(:SELF, :fish) < 3", :then => [
          [:BERSI, :neutral, "Not enough fish yet! Gudrun's watching. Catch more!"], { :end => true }] },
      { :map => "The Ebb Guild feast. Long tables, eel pies, Marisol at the head of one table with her boots on it. Bersi climbs onto a barrel." },
      { :if => "quest_flag(:SELF, :deed) == :bully", :then => [
          [:BERSI, :happy, "HEAR, Ebbmouth! The saga of the one who came off the last ferry and met GORM OF THE CRATES!"],
          [:BERSI, :happy, "Gorm, whose shoulders blot the sun! Gorm, who eats a net a day! Gorm, who was taller then than he is now!"],
          [:BERSI, :happy, "And with ONE command the traveller cast him down, and the crates were free, and the gulls wept!"],
          [:MARISOL, :smug, "Gorm's about five foot four."],
          [:BERSI, :angry, "IN THE SAGA HE IS NINE FOOT."],
          [:MARISOL, :happy, "To the traveller! Somebody had to. I'm not allowed. He pays dues."],
          { :complete => :bully }] },
      { :if => "quest_flag(:SELF, :deed) == :fish", :then => [
          [:BERSI, :happy, "HEAR, Ebbmouth! The saga of the angler who drained the Ebb itself!"],
          [:BERSI, :happy, "Three beasts from the black water, each one heavier than the last, the third one heavier than the harbour!"],
          [:GUDRUN, :deadpan, "Two of mine were bigger."],
          [:BERSI, :neutral, "Gudrun, you caught a boot in AF 270 and I sang that as a sea-serpent. Let me work."],
          { :complete => :fish }] },
      { :if => "quest_flag(:SELF, :deed) == :tale", :then => [
          [:BERSI, :happy, "HEAR, Ebbmouth! A saga, freshly told to me by its hero, and therefore completely true!"],
          { :if => "quest_flag(:SELF, :tale) == :gyarados", :then => [
              [:BERSI, :happy, "They punched a Gyarados! With a fist! The Gyarados apologised!"],
              [:MARISOL, :deadpan, "...My Gyarados is right there. He's very confused."]] },
          { :if => "quest_flag(:SELF, :tale) == :veil", :then => [
              [:BERSI, :happy, "They walked through a Bleed Veil, where no living soul may pass, and came out humming!"],
              "The hall laughs. Marisol doesn't. She looks at you for a long moment over her cup."] },
          { :if => "quest_flag(:SELF, :tale) == :tea", :then => [
              [:BERSI, :happy, "They drank the kelp tea of Imelda Larch! The whole cup! And lived!"],
              "Three separate people at the feast put their cups down and stare at you in horror."] },
          [:BERSI, :neutral, "...A good saga. Short on witnesses. Half a notch."],
          { :complete => :tall_tale }] }
    ]
  }
})

tr.quest(:IS_EGG_THIEF, {
  :trial => :ISENMAR, :title => "The Egg Thief of Gullcry", :giver => "Old Asta", :map => 561,
  :where => "the egg-gatherers' hut on the Gullcry Cliffs", :rank => 2, :points => 3, :rec_level => 24, :chapter => 4,
  :unlock => "badges >= 3", :board => true, :tags => [:boss, :event_mon, :comedy],
  :summary => "Something is taking eggs off the Gullcry ledges. Old Asta wants it stopped. Then she wants it stopped harder.",
  :steps => { :ask => "Climb to the high egg ledges on the Gullcry Cliffs and find the egg thief.",
              :report => "Tell Old Asta what was really happening to her eggs." },
  :reward => { :money => 1000 },
  :outcomes => { :let_go => { :items => [[:EXPCANDYM, 2]], :effects => "RES+1" } },
  :touches => "Resonance (Harmony +1 if you let the Bombirdier keep its route)",
  :scenes => {
    :offer => [
      [:ASTA, :angry, "Forty years I've gathered off these ledges. Forty! Never lost more than the gulls could spare."],
      [:ASTA, :angry, "This month: a dozen a night. Gone. And then they turn up in the wrong nests! Wingull eggs under Ducklett! It's chaos!"],
      { :choice => "Find the egg thief?", :options => [
          ["I'll climb up.", [{ :accept => true }, [:ASTA, :neutral, "Take the high path. Mind the wind. Mind the thief. Mind my eggs. In that order."]]],
          ["Not now.", []]] }
    ],
    :ledge => [
      { :map => "The highest ledge. A Bombirdier lands with an egg under each wing, inspects a Ducklett nest, swaps an egg in, and takes one out." },
      "It isn't stealing them. It's delivering them. Very carefully. To completely the wrong nests.",
      "It sees you, sees you seeing it, and drops into a dive.",
      { :event_battle => :IS_BOMBIRDIER,
        :won => [{ :run => :after }],
        :lost => ["The Bombirdier circles once, drops a pebble on your head with great precision, and goes back to work."] }
    ],
    :after => [
      "The Bombirdier lands on the ledge, puffs up, and offers you an egg. Then it waits for a tip.",
      { :choice => "What do you do with it?", :options => [
          ["Take it with you.", ["The Bombirdier hops onto your arm. It looks pleased. It looks like it has always wanted a proper route.",
                                 { :join => :IS_BOMBIRDIER }, { :flag => [:took, true] }, { :step => :report }]],
          ["Let it keep its route.", ["You leave it to its deliveries. It salutes with one wing and dives off the cliff with an egg.",
                                      { :flag => [:let_go, true] }, { :step => :report }]]] }
    ],
    :report => [
      [:ASTA, :shocked, "Delivering them? It's a Bombirdier, of course it's delivering them. That's all they think about."],
      [:ASTA, :deadpan, "...Wingull, Ducklett. They're all eggs. The birds don't seem to mind whose they sit on."],
      [:ASTA, :neutral, "Eggs is eggs."],
      { :if => "quest_flag(:SELF, :let_go)", :then => [{ :complete => :let_go }], :else => [{ :complete => :took }] }
    ]
  }
})

#--- Elowen board, posted at the Frostwick Half-Tally (borderland) ---------------
tr.quest(:EL_REHEARSAL, {
  :trial => :ELOWEN, :title => "The Rehearsal", :giver => "Sister Maelon", :map => 573,
  :where => "the Half-Tally, Frostwick", :rank => 2, :points => 3, :rec_level => 20, :chapter => 4,
  :unlock => "badges >= 2", :board => true, :tags => [:spiritual, :mystery, :event_mon, :bleed],
  :summary => "Off the Frostflat Causeway, a stretch of road replays five seconds of a wagon crash, over and over. Something out there is practising a tragedy.",
  :steps => { :ask => "Go into The Rehearsal (only you can) and watch the loop. Find out what doesn't belong.",
              :loop => "Watch the loop three times. Each time, something is a little different.",
              :finish => "You know who is playing every part. Finish the scene." },
  :reward => { :items => [[:SPELLTAG, 1]] },
  :touches => "Resonance (Harmony +1)",
  :scenes => {
    :offer => [
      [:MAELON, :worried, "Twelve years ago a wagon went over on the causeway road. Everyone lived. Everyone. I checked."],
      [:MAELON, :worried, "Then the Bleed came, and that stretch of road started doing it again. The wagon, the horse, a little girl in the road. Five seconds. Again."],
      [:INGRITH, :neutral, "It's a ghost."],
      [:MAELON, :neutral, "It's not a ghost. Nobody died. It's something rehearsing. Something that saw it once and keeps practising it, because it never saw how it ended."],
      [:MAELON, :sad, "We can't go past the Veil. You can. Will you watch it for me?"],
      { :choice => "Watch the Rehearsal?", :options => [
          ["I'll watch.", [{ :accept => true }]],
          ["Not now.", []]] }
    ],
    :watch => [
      { :step => :loop },
      { :count => [:loops, 1] },
      { :if => "quest_count(:SELF, :loops) == 1", :then => [
          "The wagon tips. The horse screams. The girl in the road turns her head. Five seconds. Silence. It begins again.",
          "The horse's scream is a little late. As if it's waiting for its cue."] },
      { :if => "quest_count(:SELF, :loops) == 2", :then => [
          "The wagon tips. This time the driver's face is the horse's face, for a moment. Then it fixes itself.",
          "Everyone in the scene is the same shade of pale pink at the edges."] },
      { :if => "quest_count(:SELF, :loops) >= 3", :then => [
          "The wagon tips. The girl in the road turns her head... and looks straight at you. She has your face for a frame.",
          "It's one thing. One small, pink thing, playing the wagon and the horse and the girl, because it saw them once and liked the story.",
          { :step => :finish }] }
    ],
    :finish => [
      "You walk into the scene as it starts again. You take the girl's hand and step her out of the road.",
      "The wagon stops tipping. It doesn't know what to do. Nobody ever showed it what happens next.",
      "The girl, the horse and the wagon melt into one wobbling pink blob. A Ditto. It looks at you, delighted.",
      "Then it becomes you.",
      { :event_battle => :EL_DITTO,
        :caught => ["The Rehearsal's road is quiet. Just frost, and an old wheel-rut, and nothing happening at all.",
                    { :effects => "RES+1" }, { :complete => true }],
        :won => ["The Ditto puddles away into the frost. Somewhere down the road, faintly, a horse screams on cue. It's started again."],
        :lost => ["Your double bows. The Rehearsal begins again."] }
    ]
  }
})

#--- Quest counter hook: Old Gudrun's fishing contest ---------------------------
EventHandlers.add(:on_wild_battle_end, :prismfall_trials_fishing,
  proc { |species, _level, outcome|
    next if outcome != 4
    t = Prismfall::Trials
    next if !t.at?(:IS_SKALDS_SAGA, :ask) || t.flag(:IS_SKALDS_SAGA, :deed) != :fish
    sp = GameData::Species.get(species) rescue nil
    next if !sp || !sp.types.include?(:WATER)
    n = t.add_count(:IS_SKALDS_SAGA, :fish, 1)
    if n >= 3
      t.set_step(:IS_SKALDS_SAGA, :feast)
    else
      pbMessage(_INTL("That's {1} of 3 for the skald's saga.", n))
    end
  }
) if defined?(EventHandlers)
