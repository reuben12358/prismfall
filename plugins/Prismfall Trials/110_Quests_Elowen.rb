#===============================================================================
# Prismfall Trials - 110 Elowen: The Quiet Way (Chapters 1-4, implemented)
#-------------------------------------------------------------------------------
# Ionia-like: balance, spirits, pilgrimages, puzzles, kindness. Quests hang as
# paper lanterns on a rope; a finished one is lit and let go.
# Halls this early: the Ferrow's Landing wayshrine (100), the Saltmere Lantern
# House (140, next door to the theatre, which is the joke), the Briarwick Lantern
# House (120, the oldest in the south). Keepers: Brother Teasel (whispers),
# Sister Hollin (gave up on silence, writes on a slate), Mother Aldreth (blind,
# weaves the lanterns, knows what you did before you say it).
# Story order is SPINE Revision 14. Switches: S101 ferry done, S103 starter,
# S105 orchard done, S108 Saltmere pageant done (FLAGS.md).
# Map events: design/TRIAL_EVENTS.yaml. Dialogue doc: design/TRIALS_SCRIPT.md.
#===============================================================================
tr = Prismfall::Trials
tr::SPEAKERS.merge!({
  :TEASEL => "Brother Teasel", :HOLLIN => "Sister Hollin", :ALDRETH => "Mother Aldreth",
  :WENNA => "Wenna", :COLL => "Coll", :KESTREL => "Kestrel", :JUNO => "Juno", :HESPER => "Hesper",
  :DOCKMASTER => "Dockmaster", :DOBBS => "Dobbs", :FANE => "Marguerite Fane", :BRUSH => "Brush",
  :HETT => "Hett", :TAMSIN => "Tamsin", :STAGEHAND => "Ottilie", :ROPEGIRL => "Rope-skipping girl", :CARAMEL => "Caramel seller",
  :LARCH => "Larch", :DORIAN => "Dorian"
})

#===============================================================================
# CHAPTER 1 - Ferrow's Landing
#===============================================================================
tr.quest(:EL_FIRST_LESSON, {
  :trial => :ELOWEN, :title => "The First Lesson", :giver => "Brother Teasel", :map => 100,
  :where => "the wayshrine by the Accord plaque", :rank => 1, :points => 2, :rec_level => 5, :chapter => 1,
  :unlock => "switch(103)", :board => false, :tags => [:kindness, :tutorial],
  :summary => "Do one kind thing in Ferrow's Landing that nobody asked you to do. Then go back to Brother Teasel.",
  :steps => { :listen => "Do one kind thing nobody asks of you. Don't tell Brother Teasel what it was.",
              :return => "You did something. Go back to the wayshrine." },
  :reward => { :items => [[:ORANBERRY, 2]] },
  :outcomes => { :silent => { :effects => "RES+1" } },
  :touches => "Resonance (Harmony +1 for keeping quiet); starts the realm-wide Quiet Deeds tally",
  :scenes => {
    :offer => [
      { :map => "A young monk in grey stands by the wayshrine, a rope of paper lanterns strung over his head. His lips move." },
      "Brother Teasel is saying something. You can't hear a word of it.",
      [:TEASEL, :neutral, "...I SAID, WELCOME TO THE QUIET WAY."],
      [:TEASEL, :shocked, "Oh no. Oh, I'm so sorry. That's the loudest I've been in four years."],
      [:TEASEL, :neutral, "I keep the wayshrine. Folk hang their troubles on the rope, and somebody takes one down and makes it lighter."],
      [:TEASEL, :neutral, "But the first lesson isn't on the rope. The first lesson is: do one kind thing nobody asked you to do."],
      [:TEASEL, :happy, "Then come back. Don't tell me what it was. The Root will have heard."],
      { :choice => [:TEASEL, :neutral, "Will you take the first lesson?"],
        :options => [["I'll try.", [{ :accept => true }, [:TEASEL, :happy, "Go gently. Most people need three goes."],
                                    { :if => "deeds >= 1", :then => [[:TEASEL, :shocked, "...Oh. You already have, haven't you. I can tell."],
                                                                    { :step => :return }] }]],
                     ["Not now.", [[:TEASEL, :neutral, "The rope will still be here. So will I. Quietly."]]]] }
    ],
    :return => [
      { :if => "deeds >= 1", :then => [
          [:TEASEL, :happy, "Oh. You did something. You've got the look. Like you just put a stone down."],
          { :choice => "Tell him what you did?", :options => [
              ["Tell him everything.", [
                 "You tell him. All of it. With gestures.",
                 [:TEASEL, :neutral, "Mm. Mm-hm. And then you hung it all back up. Mm."],
                 [:TEASEL, :deadpan, "That's called boasting. Half a lantern."],
                 { :points => [:ELOWEN, -1] }, { :complete => :boasted }]],
              ["Say nothing.", [
                 "You say nothing. Teasel nods as if you'd said a great deal.",
                 [:TEASEL, :happy, "Good. That's the whole lesson. You only needed one go."],
                 { :complete => :silent }]]] },
          [:TEASEL, :neutral, "The Quiet Way keeps counting, wherever you go. Mother Aldreth in Briarwick keeps the tally. She'll know."],
          [:TEASEL, :neutral, "And the rope's yours now. Anything hanging there, you may take down."]
        ], :else => [
          [:TEASEL, :neutral, "Not yet. You'll know when. So will I, somehow. It's a bit unsettling."]
        ] }
    ],
    # The deeds themselves (map events in Ferrow's Landing; they count even without the quest).
    :deed_washing => [
      "A shirt has blown off the washing line and wrapped itself round a kelp rack.",
      { :choice => "Hang it back up?", :options => [
          ["Hang it up.", ["You peg the shirt back on the line. Nobody sees.", { :deed => :fl_washing },
                           { :if => "quest_step(:SELF) == :listen", :then => [{ :step => :return }] }]],
          ["Leave it.", []]] }
    ],
    :deed_rope => [
      [:ROPEGIRL, :sad, "We need a third to turn the rope. We can't finish the rhyme with two."],
      { :map => "The rope-skipping girls hold out the loose end." },
      { :choice => "Turn the rope?", :options => [
          ["Turn it.", ["You turn the rope. The girls skip all the way through the counting rhyme, to the very last Plate.",
                        "\"...and one that no one counted!\" They collapse, laughing.", { :deed => :fl_rope },
                        { :if => "quest_step(:SELF) == :listen", :then => [{ :step => :return }] }]],
          ["Not now.", []]] }
    ],
    :deed_sailor => [
      "The old sailor sits facing the empty berth where the ferries used to come in.",
      { :choice => "Sit with him?", :options => [
          ["Sit.", ["You sit. He doesn't say anything. After a while he pats your knee twice and gets up.",
                    { :deed => :fl_sailor }, { :if => "quest_step(:SELF) == :listen", :then => [{ :step => :return }] }]],
          ["Walk on.", []]] }
    ],
    :deed_kelp => [
      "A basket of drying kelp has tipped into a puddle. The kelp-drier is at the far end of the racks, not looking.",
      { :choice => "Rinse and re-hang it?", :options => [
          ["Do it.", ["It takes a while. Your hands smell of the sea for an hour.", { :deed => :fl_kelp },
                      { :if => "quest_step(:SELF) == :listen", :then => [{ :step => :return }] }]],
          ["Leave it.", []]] }
    ]
  }
})

tr.quest(:EL_TART_THIEF, {
  :trial => :ELOWEN, :title => "The Tart Thief", :giver => "Wenna Hale", :map => 100,
  :where => "the tart stall on the quay", :rank => 1, :points => 2, :rec_level => 7, :chapter => 1,
  :unlock => "switch(103)", :board => true, :tags => [:chase, :event_mon, :comedy],
  :summary => "Someone keeps stealing Wenna Hale's bramble tarts. Brother Teasel's note on the lantern: \"The thief is hungry, not wicked.\"",
  :steps => { :ask => "Wenna's tarts keep vanishing. Watch the stall.",
              :chase => "A Nickit with jam on its whiskers! Follow it round Ferrow's Landing.",
              :loft => "The crumbs lead up into Tidewatch Station's loft.",
              :return => "Tell Wenna what happened to her tarts." },
  :reward => { :money => 200, :items => [[:ORANBERRY, 3]] },
  :outcomes => { :told => { :effects => "KESTREL-1" } },
  :touches => "Kestrel bond (+1 if you split the evidence, -1 if you tell on him)",
  :scenes => {
    :offer => [
      [:WENNA, :worried, "Twelve tarts this morning. Nine by the time I'd turned round. Six by the time I'd turned back."],
      [:WENNA, :angry, "It's not the gulls. Gulls don't take the paper cases with them."],
      [:WENNA, :neutral, "Watch the stall for me? I'll pay you in tarts. Well. In whatever tarts survive."],
      { :choice => "Watch the stall?", :options => [
          ["Of course.", [{ :accept => true }, [:WENNA, :happy, "You're a treasure. Stand by the barrels, look casual. Not that casual."]]],
          ["Maybe later.", [[:WENNA, :neutral, "I'll be here. Getting robbed."]]]] }
    ],
    :sighting => [
      { :if => "chase(:SELF) == 0", :then => [
          "Something small and russet slips out from under the stall with a tart in its jaws.",
          "It's a Nickit! It sees you, freezes, and bolts for the kelp racks.",
          { :chase => :advance }, { :step => :chase }, { :end => true }] },
      { :if => "chase(:SELF) == 1", :then => [
          { :map => "Kelp racks. The kelp-drier yelps as a russet streak tears through the hanging kelp." },
          "The Nickit leaves a trail of pastry flakes and vanishes under the pier.",
          { :chase => :advance }, { :end => true }] },
      { :if => "chase(:SELF) == 2", :then => [
          "Under the pier: crumbs, a paper case, and two bright eyes. The Nickit squeezes out the far side.",
          "It scampers up the lighthouse steps.",
          { :chase => :advance }, { :end => true }] },
      { :if => "chase(:SELF) == 3", :then => [
          [:HESPER, :angry, "THAT ANIMAL IS EATING MY GERANIUMS."],
          "The Nickit leaps the lighthouse wall and makes for Tidewatch Station, tail high.",
          { :chase => :advance }, { :step => :loft }] }
    ],
    :loft => [
      { :map => "The Nickit dives into the hay. Kestrel sits up in his bedroll with a bramble tart in each hand." },
      [:KESTREL, :angry, "What."],
      [:KESTREL, :annoyed, "...It brings them. I don't ask it to. It just turns up with pastry like I'm some kind of— don't look at me like that."],
      [:KESTREL, :annoyed, "They're Wenna's? Of course they're Wenna's. Nobody else in this dump can bake."],
      { :choice => "Kestrel has been eating stolen tarts.", :options => [
          ["You could have just asked her.", [
             [:KESTREL, :angry, "Asked. Asked Wenna Hale for charity. While her daughter watches. No."]]],
          ["Split the evidence?", [
             "You hold out a hand. Kestrel stares at it, then puts a tart in it.",
             [:KESTREL, :deadpan, "...Fine. You're an accessory now."], { :effects => "KESTREL+1" }]],
          ["I'm telling Wenna.", [
             [:KESTREL, :angry, "Go on, then. Tell her the Vane boy's a thief. She'll love that. Everyone does."],
             { :flag => [:told, true] }]]] },
      "The Nickit plants itself in front of its hoard and growls at you, every hair on end.",
      [:KESTREL, :smug, "It thinks you're after the stash. Fight it if you want it. It likes winners."],
      [:KESTREL, :deadpan, "Clearly it has awful taste. It picked me."],
      { :event_battle => :EL_NICKIT,
        :caught => [[:KESTREL, :neutral, "Huh. It went with you."],
                    [:KESTREL, :annoyed, "Feed it. It gets mean when it's hungry. So do I. Unrelated."],
                    { :step => :return }],
        :won => ["The Nickit scrambles up into the rafters to sulk. It'll come down when it's hungry.",
                 [:KESTREL, :deadpan, "You knocked out the pastry thief. Real heroic."]],
        :lost => [[:KESTREL, :smug, "You lost to a pastry thief."], [:KESTREL, :deadpan, "...Don't tell anyone. They'd think less of both of us."]],
        :fled => [] }
    ],
    :return => [
      [:WENNA, :neutral, "Well? Who's my thief?"],
      { :if => "quest_flag(:SELF, :told)", :then => [
          "You tell her about the Nickit, and the loft, and Kestrel.",
          [:WENNA, :sad, "Kestrel. Oh, that boy."],
          [:WENNA, :neutral, "He's been sleeping in that loft since he was twelve. And I've been baking two dozen too many since about then."],
          [:WENNA, :neutral, "I thought it was the gulls getting the extras. Turns out it was the right mouth all along."],
          { :complete => :told }
        ], :else => [
          "You tell her about the Nickit. Just the Nickit.",
          [:WENNA, :deadpan, "Mm. And this Nickit's about Kestrel's height, is it? Scowls a lot?"],
          [:WENNA, :happy, "Don't fret, love. I've known for years. I bake two dozen too many on purpose."],
          { :complete => :kept }
        ] },
      [:WENNA, :neutral, "I'll leave a plate by the station door from now on. Nobody has to ask anybody for anything."]
    ]
  }
})

tr.quest(:EL_SCARECROW, {
  :trial => :ELOWEN, :title => "The Scarecrow Walks", :giver => "Coll Hale", :map => 523,
  :where => "the Hale farmhouse", :rank => 1, :points => 2, :rec_level => 9, :chapter => 1,
  :unlock => "switch(103)", :board => true, :tags => [:mystery, :event_mon, :comedy],
  :summary => "Coll Hale's scarecrow keeps moving to a different field. Coll did not build a scarecrow.",
  :steps => { :ask => "Look at the 'scarecrow' in the Hale orchard on Windfall Row. Don't let it see you looking.",
              :bottle => "It hates the rain. Ask Wenna in Ferrow's Landing for her Squirt Bottle.",
              :water => "Water the scarecrow." },
  :reward => {},
  :outcomes => { :caught => { :money => 300 }, :spared => { :items => [[:MIRACLESEED, 1]], :effects => "RES+1" } },
  :touches => "Resonance (Harmony +1 if you leave it be)",
  :scenes => {
    :offer => [
      [:COLL, :deadpan, "Scarecrow's moved again."],
      [:COLL, :neutral, "Monday it was in the plum rows. Tuesday, the pears. This morning it was in my chair."],
      [:COLL, :deadpan, "I didn't build a scarecrow."],
      { :choice => "Look into it?", :options => [
          ["I'll look.", [{ :accept => true }, [:COLL, :neutral, "Have a look at it. Don't let it see you looking."]]],
          ["Not now.", [[:COLL, :deadpan, "Fine. It'll be in the kitchen by supper, I expect."]]]] }
    ],
    :watch => [
      "It's a scarecrow. Probably. It has a lot of very green hands.",
      "A drop of rain lands on it. The scarecrow shudders, and edges sideways under the nearest tree.",
      "Scarecrows don't do that. Wenna keeps a Squirt Bottle for her window boxes...",
      { :step => :bottle }
    ],
    :bottle => [
      { :if => "has_item(:SQUIRTBOTTLE)", :then => [[:WENNA, :happy, "You've got it already! Go on, give it a good soak."], { :end => true }] },
      [:WENNA, :shocked, "Coll's scarecrow? We haven't got a scarecrow."],
      [:WENNA, :neutral, "Take the bottle. If it's a Pokémon, it'll thank you. If it's a scarecrow, nobody's lost anything but water."],
      { :item => [:SQUIRTBOTTLE, 1] }, { :step => :water }
    ],
    :water => [
      "The scarecrow stands very, very still. It is trying extremely hard to be a tree.",
      { :choice => "Water the scarecrow?", :options => [
          ["Give it a squirt.", [
             "You give it a squirt.", "The 'scarecrow' screams, rips its roots out of the ground and charges!",
             { :event_battle => :EL_SUDOWOODO,
               :caught => [[:COLL, :deadpan, "...It was a Sudowoodo."], [:COLL, :neutral, "Best scarecrow I ever had. Look after it."],
                           { :complete => :caught }],
               :won => ["The Sudowoodo bolts into the plum rows, sobbing dry tears. It'll be back. It always comes back to the plums."],
               :lost => ["The Sudowoodo stops attacking and goes back to being a tree, looking smug."] }]],
          ["Leave it be.", [
             "You put the bottle away. The scarecrow relaxes so hard that a leaf falls off.",
             "The Rookidee stay out of the orchard all afternoon.",
             [:COLL, :neutral, "...Leaving it, are you. All right. It's a better scarecrow than a scarecrow, I'll give it that."],
             { :complete => :spared }]]] }
    ],
    # Afterwards: the spared Sudowoodo can still be challenged (map event condition: quest_outcome(:EL_SCARECROW) == :spared).
    :rematch => [
      "The Sudowoodo is guarding the plum rows. It eyes your Squirt Bottle warily.",
      { :choice => "Challenge it?", :options => [
          ["Challenge it.", [{ :event_battle => :EL_SUDOWOODO,
                               :caught => [[:COLL, :neutral, "Taking the scarecrow, then. Fair enough. I'll build a real one. Probably."]] }]],
          ["Leave it.", []]] }
    ]
  }
})

tr.quest(:EL_MASTER_OF_NOTHING, {
  :trial => :ELOWEN, :title => "Master of Nothing", :giver => "the Dockmaster", :map => 107,
  :where => "the Dockmaster's House", :rank => 1, :points => 2, :rec_level => 6, :chapter => 1,
  :unlock => "switch(101) && switch(103)", :board => true, :tags => [:kindness, :event_mon],
  :summary => "The Dockmaster wants to close the Dovetail's ledger properly. Something is still aboard.",
  :steps => { :ask => "Search the laid-up Dovetail for whatever is still living aboard.",
              :ledger => "Take what you found back to the Dockmaster." },
  :reward => { :items => [[:POTION, 2]] },
  :touches => "none (a quiet one)",
  :scenes => {
    :offer => [
      [:DOCKMASTER, :neutral, "Every ship gets a last line in the ledger. 'Laid up. Crew discharged. Nothing aboard.'"],
      [:DOCKMASTER, :sad, "I can't write it for the Dovetail. Something's aboard. Every night, a crackle in the rigging, like a kettle that can't decide."],
      [:DOCKMASTER, :neutral, "I'm too old for ropes. Would you look? Then I can close the book."],
      { :choice => "Search the Dovetail?", :options => [
          ["I'll look.", [{ :accept => true }, [:DOCKMASTER, :neutral, "Captain Morrow's left the gangplank down. She says it's for the gulls. It isn't."]]],
          ["Not now.", []]] }
    ],
    :rigging => [
      { :map => "On the Dovetail's deck, under the furled mainsail: a nest of tarred rope fibre and fishing line." },
      "A Wattrel peers out of the nest. Its feathers crackle with static.",
      "It's been waiting for the ferry to sail, so it can follow it home. The ferry is never going to sail.",
      "The Wattrel looks at the empty sea, then at you. It hops onto your shoulder and settles there, crackling.",
      { :step => :ledger }
    ],
    :ledger => [
      [:DOCKMASTER, :neutral, "A Wattrel. Of course. They follow ships. That one followed the last one in and had nowhere left to follow."],
      { :map => "He dips his pen and writes slowly." },
      [:DOCKMASTER, :neutral, "'Dovetail. Laid up. Crew discharged. One Wattrel, rehomed.'"],
      [:DOCKMASTER, :happy, "There. The first ledger line I've liked in a year."],
      { :gift => :EL_WATTREL }, { :complete => true }
    ]
  }
})

#===============================================================================
# CHAPTER 2 - the Gym 1 leg (Lacecliff Walk 527, Marram Down 528) and Saltmere (Gym 1)
#===============================================================================
tr.quest(:EL_TIDE_POOL_FEUD, {
  :trial => :ELOWEN, :title => "The Tide-Pool Feud", :giver => "Dobbs the shell-gatherer", :map => 527,
  :where => "the shell-gatherers' steps on Lacecliff Walk", :rank => 1, :points => 2, :rec_level => 12, :chapter => 2,
  :unlock => "switch(103)", :board => true, :tags => [:rival_duel, :event_mon],
  :summary => "A Crabrawler and a Clobbopus have been fighting over one rock for three days. The shell-gatherers can't reach the pools.",
  :steps => { :ask => "Settle the feud at the big tide-pool below Lacecliff Walk." },
  :reward => { :items => [[:SUPERPOTION, 2]] },
  :touches => "none; the side you help punches open a sea-cave under the cliff (flag :sea_cave, items inside)",
  :scenes => {
    :offer => [
      [:DOBBS, :worried, "Don't go down to the big pool. There's a fight on."],
      [:DOBBS, :neutral, "Three days now. A Crabrawler and a Clobbopus. Over a rock."],
      [:DOBBS, :neutral, "It's a nice rock, to be fair. Flat. Sun on it all afternoon. I'd fight for it."],
      [:DOBBS, :worried, "But the good pools are past it, and I can't gather shells with a war on."],
      { :choice => "Settle the feud?", :options => [
          ["I'll sort it.", [{ :accept => true }, [:DOBBS, :happy, "Pick a side. They respect that. Neither of them respects me."]]],
          ["Not now.", []]] }
    ],
    :pool => [
      "The Crabrawler and the Clobbopus circle the flat rock, fists up, tentacles up, neither blinking.",
      { :choice => "Whose side are you on?", :options => [
          ["Help the Clobbopus.", [
             "The Clobbopus slaps the rock with a tentacle, delighted. The Crabrawler turns on you!",
             { :event_battle => :EL_TIDE_CRABRAWLER,
               :caught => [{ :run => :victory_clob }], :won => [{ :run => :victory_clob }] }]],
          ["Help the Crabrawler.", [
             "The Crabrawler clacks its claws, delighted. The Clobbopus turns on you!",
             { :event_battle => :EL_TIDE_CLOBBOPUS,
               :caught => [{ :run => :victory_crab }], :won => [{ :run => :victory_crab }] }]],
          ["Leave them to it.", ["You back away. Neither of them noticed you were there."]]] }
    ],
    :victory_clob => [
      "The Clobbopus climbs onto its rock, sunbathes for a moment... then punches the cliff behind it, out of sheer joy.",
      "The cliff caves in. Behind it: a sea-cave nobody's seen in a hundred years, full of driftwood and old smugglers' crates.",
      { :flag => [:sea_cave, true] }, { :complete => :clobbopus }
    ],
    :victory_crab => [
      "The Crabrawler climbs onto its rock, then, to celebrate, punches the cliff behind it.",
      "The cliff caves in. Behind it: a sea-cave nobody's seen in a hundred years, full of driftwood and old smugglers' crates.",
      { :flag => [:sea_cave, true] }, { :complete => :crabrawler }
    ]
  }
})

tr.quest(:EL_LANTERNS, {
  :trial => :ELOWEN, :title => "The Borrowed Lanterns", :giver => "Sister Hollin", :map => 140,
  :where => "the Saltmere Lantern House", :rank => 1, :points => 3, :rec_level => 12, :chapter => 2,
  :unlock => "switch(103)", :board => true, :tags => [:search, :event_mon, :comedy, :kindness],
  :summary => "The theatre district keeps 'borrowing' the Lantern House's lanterns as props. Five are missing before the Night of Floating.",
  :steps => { :search => "Find the five borrowed lanterns around Saltmere.",
              :return => "Take the lanterns back to Sister Hollin." },
  :reward => { :items => [[:SILKSCARF, 1]] },
  :outcomes => { :left_one => { :money => 400, :effects => "RES+1" } },
  :touches => "Resonance (Harmony +1 if you leave the stagehand her lantern)",
  :scenes => {
    :offer => [
      { :map => "The Saltmere Lantern House shares a wall with the Lantern Theatre. Through it, someone is rehearsing a death scene. Loudly." },
      "Sister Hollin has earplugs in. She writes on a slate and holds it up.",
      "\"THEY TOOK MY LANTERNS. AGAIN.\"",
      "She wipes it and writes again. \"FIVE. NIGHT OF FLOATING IS IN THREE DAYS. HELP.\"",
      [:HOLLIN, :angry, "THE QUIET WAY HAS KEPT A HOUSE HERE FOR NINETY YEARS AND I HAVE NOT HAD ONE QUIET— sorry. Sorry."],
      { :choice => "Find the lanterns?", :options => [
          ["I'll find them.", [{ :accept => true }, "Sister Hollin writes: \"BLESS YOU. CHECK THE PROP ROOM FIRST. IT'S ALWAYS THE PROP ROOM.\""]],
          ["Not now.", ["Sister Hollin writes: \"COWARD.\" Then, smaller: \"(lovingly)\""]]] }
    ],
    :prop_room => [
      "The prop room is a forest of crowns, swords and painted trees. On a shelf sits a paper lantern.",
      "...The lantern blinks.",
      { :choice => "Poke the lantern?", :options => [
          ["Poke it.", [
             "The lantern turns green, grows a tongue and licks your hand. It's a Kecleon!",
             { :event_battle => :EL_KECLEON,
               :caught => ["Behind where the Kecleon was sitting is the real lantern, slightly licked.",
                           { :flag => [:prop_room, true] }, { :run => :found }],
               :won => ["The Kecleon flees up into the fly loft, turning the colour of embarrassment.",
                        "Behind where it was sitting is the real lantern, slightly licked.",
                        { :flag => [:prop_room, true] }, { :run => :found }],
               :lost => ["The Kecleon goes back to being a lantern. A smug lantern."] }]],
          ["Leave it.", []]] }
    ],
    :stall => [
      [:CARAMEL, :neutral, "This? It's my display lamp. Makes the caramel glow. Sales went up forty percent."],
      [:CARAMEL, :sad, "...It's the Lantern House's, isn't it. She wrote me a note. In capitals."],
      "The caramel seller hands over the lantern and a bag of broken caramel 'for your trouble'.",
      { :flag => [:stall, true] }, { :run => :found }
    ],
    :boat => [
      "A fishing boat at the harbour wall has a paper lantern tied to its bow, glowing in the fog.",
      "A note on the tiller: \"Borrowed for luck. Bring it back by Floating, sister. - G.\"",
      "Luck can be borrowed back. You untie it.",
      { :flag => [:boat, true] }, { :run => :found }
    ],
    :ropewalk => [
      "Halfway down the Old Town ropewalk, a lantern hangs from a hook where the rope-makers can see their twists.",
      "The rope-makers argue for a while about whose turn it was to return it, then about rope, then about each other's mothers.",
      "Nobody notices you take it.",
      { :flag => [:ropewalk, true] }, { :run => :found }
    ],
    :stagehand => [
      { :map => "The empty Lantern Theatre, after hours. A young stagehand stands centre stage with a paper lantern at her feet, murmuring lines." },
      [:STAGEHAND, :shocked, "Oh! I— nobody's meant to be in here. Ottilie. Stagehand. Understudy. Very understudy."],
      [:STAGEHAND, :sad, "I freeze when there's an audience. So I practise with this. I pretend the light is one face. Just one."],
      [:STAGEHAND, :neutral, "It's the Lantern House's, isn't it. You can take it. I'll... pretend harder."],
      { :choice => "Take the lantern?", :options => [
          ["Take it back.", [[:STAGEHAND, :neutral, "Of course. Thank you for not laughing."],
                             { :flag => [:stagehand, true] }, { :run => :found }]],
          ["Leave it with her.", [[:STAGEHAND, :happy, "Really? I'll— I'll bring it back after opening night. I promise."],
                                  { :flag => [:stagehand, true] }, { :flag => [:left_one, true] }, { :run => :found_left }]]] }
    ],
    :found => [
      { :count => [:lanterns, 1] },
      { :if => "quest_count(:SELF, :lanterns) + quest_count(:SELF, :left) >= 5", :then => [{ :step => :return }],
        :else => ["That's one more lantern. Sister Hollin will be pleased, in capitals."] }
    ],
    :found_left => [
      { :count => [:left, 1] },
      { :if => "quest_count(:SELF, :lanterns) + quest_count(:SELF, :left) >= 5", :then => [{ :step => :return }] }
    ],
    :return => [
      { :if => "quest_flag(:SELF, :left_one)", :then => [
          "You hand Sister Hollin four lanterns and explain about the fifth.",
          "She reads your face for a long moment. Then she writes, very small: \"then it is doing what lanterns are for.\"",
          [:HOLLIN, :happy, "Four is plenty. Floating's about letting go, after all. I'm told."],
          { :complete => :left_one }
        ], :else => [
          "Sister Hollin counts the lanterns twice, hugs them, and writes: \"FIVE. I COULD KISS YOU. I WON'T. VOW.\"",
          { :complete => :all_five }
        ] }
    ]
  }
})

tr.quest(:EL_PAINT_LOFT, {
  :trial => :ELOWEN, :title => "A Hole in the Sky", :giver => "Marguerite Fane", :map => 145,
  :where => "the Lantern Theatre paint loft", :rank => 1, :points => 1, :rec_level => 13, :chapter => 2,
  :unlock => "badges >= 1 && switch(108)", :board => true, :tags => [:gift, :event_mon, :comedy],
  :summary => "The Mourner walked straight through the Pageant's painted sky. The scene-painter needs a new backdrop, and a second opinion.",
  :steps => { :ask => "Help Marguerite Fane and her Smeargle choose the colours for the new backdrop." },
  :reward => {},
  :touches => "none; the colours you pick decide the Smeargle's moves (Water, Fire, Grass or Ghost coverage)",
  :scenes => {
    :offer => [
      { :map => "The paint loft. A torn backdrop of the Plates falling hangs from the rigging with a person-shaped hole in it." },
      [:FANE, :angry, "Eleven weeks, that sky took. Eleven. And a man in a bark mask walks through it like a curtain."],
      [:FANE, :sad, "Brush won't paint since. Sulks. Look at him."],
      "A Smeargle sits in the corner with its tail-brush in its mouth, glaring at the hole.",
      [:FANE, :neutral, "He paints whatever moves him. Nothing's moved him since. Tell him what Saltmere looks like to you. Maybe he'll listen to a stranger."],
      { :choice => "Help pick the colours?", :options => [
          ["Let's paint.", [{ :accept => true }, { :run => :choose }]],
          ["Not now.", []]] }
    ],
    :choose => [
      "Brush looks at you, tail-brush raised.",
      { :choice => "What does Saltmere look like to you?", :options => [
          ["Fog on the breakwater.", [{ :flag => [:palette, :sea] }, "Brush slaps on grey-blue and white. The new sky is all fog and lamplight.", { :run => :finish_sea }]],
          ["Footlights.", [{ :flag => [:palette, :ember] }, "Brush paints in amber and red. The new sky is the inside of a lantern.", { :run => :finish_ember }]],
          ["The road inland.", [{ :flag => [:palette, :grove] }, "Brush paints green. The new sky is the forest seen from underneath.", { :run => :finish_grove }]],
          ["After the show.", [{ :flag => [:palette, :night] }, "Brush paints violet and black and one small star.", { :run => :finish_night }]]] }
    ],
    :finish_sea   => [{ :run => :finish }, { :gift => :EL_SMEARGLE, :variant => :sea },   { :complete => :sea }],
    :finish_ember => [{ :run => :finish }, { :gift => :EL_SMEARGLE, :variant => :ember }, { :complete => :ember }],
    :finish_grove => [{ :run => :finish }, { :gift => :EL_SMEARGLE, :variant => :grove }, { :complete => :grove }],
    :finish_night => [{ :run => :finish }, { :gift => :EL_SMEARGLE, :variant => :night }, { :complete => :night }],
    :finish => [
      [:FANE, :shocked, "He's... he's painted Dorian's face in the corner. He always paints Dorian's face in the corner."],
      [:FANE, :happy, "That's how I know he's better."],
      "Brush finishes, puts down his tail, and walks over to stand beside you. He doesn't walk back.",
      [:FANE, :neutral, "Oh, I see. He's moving on. Painters do."],
      [:FANE, :happy, "Take him. Saltmere's painted. Paint something bigger."]
    ]
  }
})

# One "silence" spot: listen once per spot (flag), three spots in all.
silence = lambda do |spot, text|
  [{ :if => "quest_flag(:SELF, :#{spot})", :then => ["You've already listened here. The sea is still breathing.", { :end => true }] },
   text,
   { :choice => "Stand still and listen?", :options => [
       ["Listen.", [
          { :wait => 1.5 },
          "...Under everything, so faint you'd never hear it with a crowd: the sea, breathing in and out against the stones.",
          { :flag => [spot, true] }, { :count => [:silences, 1] },
          { :if => "quest_count(:SELF, :silences) >= 3",
            :then => ["You've heard it three times now. The same breath, everywhere. You think you know where it's coming from.",
                      { :step => :breakwater }] }]],
       ["Move on.", []]] }]
end

tr.quest(:EL_SOUND_OF_SALTMERE, {
  :trial => :ELOWEN, :title => "The Sound of Saltmere", :giver => "Sister Hollin", :map => 140,
  :where => "the Saltmere Lantern House", :rank => 1, :points => 3, :rec_level => 14, :chapter => 2,
  :unlock => "badges >= 1", :requires => [:EL_LANTERNS], :board => true, :tags => [:puzzle, :spiritual, :event_mon],
  :summary => "A koan: find the sound Saltmere makes when nobody is performing.",
  :steps => { :ask => "Find three true silences in Saltmere. Stand still in each and listen.",
              :breakwater => "Take the three silences to the very end of the breakwater." },
  :reward => {},
  :touches => "Resonance (Harmony +1)",
  :scenes => {
    :offer => [
      "Sister Hollin takes her earplugs out. Slowly. It seems to hurt.",
      [:HOLLIN, :neutral, "You found my lanterns. So you can find things. Here's a harder one."],
      [:HOLLIN, :neutral, "Every town has a sound it makes when nobody's watching. Saltmere is always watched. Always performing."],
      [:HOLLIN, :neutral, "Find three places where it stops. Stand in each. Listen. Then take what you heard to the end of the breakwater."],
      [:HOLLIN, :deadpan, "Don't ask me what happens then. I've never managed it. Too loud in here."],
      { :choice => "Take the koan?", :options => [
          ["I'll listen.", [{ :accept => true }, "Sister Hollin puts her earplugs back in, with visible relief."]],
          ["Not now.", []]] }
    ],
    :silence_stage    => silence.call(:stage, "The Lantern Theatre after the last bow. The seats creak as they cool."),
    :silence_ropewalk => silence.call(:ropewalk, "The Old Town ropewalk, empty. A rope on the long frame turns very slightly in a draught, by itself."),
    :silence_stall    => silence.call(:stall, "The caramel stall, shuttered. Sugar ticks as it sets in the cold pans."),
    :breakwater => [
      { :map => "The very end of the breakwater. Fog. The lamps of Saltmere behind you, the dark sea ahead." },
      "You stand still. You breathe out when the sea does.",
      { :wait => 1.5 },
      "Something small steps out of the fog and stands beside you. It is breathing out when you do.",
      "A Ralts. Its horn glows faintly, the colour of the lamps behind you.",
      "Ralts feel what people feel. In Saltmere everyone's feelings are performed. This one has been hiding out here, where the only feeling is the sea's.",
      "It looks up at you as if you're the first quiet thing it's met in a long time.",
      { :gift => :EL_RALTS }, { :effects => "RES+1" }, { :complete => true }
    ]
  }
})

tr.quest(:EL_GLASS_FOAL, {
  :trial => :ELOWEN, :title => "The Orchard Sings", :giver => "Brother Teasel", :map => 100,
  :where => "the Ferrow's Landing wayshrine", :rank => 1, :points => 3, :rec_level => 15, :chapter => 2,
  :unlock => "badges >= 1 && switch(105)", :board => true, :tags => [:spiritual, :chase, :event_mon, :bleed],
  :summary => "Since your badge, folk on the orchard lane hear chiming at night, like hooves on glass.",
  :steps => { :ask => "Go into the Glassed Orchard (only you can) and follow the chiming.",
              :follow => "Follow the glass hoofprints deeper into the Orchard.",
              :foal => "The hoofprints end at the oldest glassed tree." },
  :reward => { :items => [[:MOONSTONE, 1]] },
  :touches => "Resonance (Harmony +1 if you approach slowly)",
  :scenes => {
    :offer => [
      [:TEASEL, :neutral, "The orchard lane folk say the glass has started singing. Not the wind-chime apples. Something walking."],
      [:TEASEL, :worried, "None of us can go past the Veil. You can. I don't know why. I'm not asking why. Out loud."],
      { :choice => "Go and listen?", :options => [
          ["I'll go.", [{ :accept => true }, [:TEASEL, :neutral, "Whatever it is, it's frightened. Glass is a frightening thing to become."]]],
          ["Not now.", []]] }
    ],
    :hoofprint => [
      { :if => "chase(:SELF) == 0", :then => [
          "Hoofprints in the glass dust, each one ringing faintly. Something pale moves between the trees and is gone.",
          { :chase => :advance }, { :step => :follow }, { :end => true }] },
      { :if => "chase(:SELF) == 1", :then => [
          "A foal-shaped shimmer, mane like spun sugar, looks back at you once, then trots off through a glass hedge without breaking it.",
          { :chase => :advance }, { :end => true }] },
      { :if => "chase(:SELF) == 2", :then => [
          "The chiming stops. The hoofprints circle the oldest tree in the orchard, the one that glassed first.",
          { :chase => :advance }, { :step => :foal }] }
    ],
    :foal => [
      "A Ponyta stands under the glassed tree. Not a fire Ponyta. Its mane is pale and full of light, like the inside of a soap bubble.",
      "It was born in here. It has never seen a tree that wasn't glass.",
      { :choice => "How do you approach?", :options => [
          ["Slowly, palms open.", ["You walk so slowly it takes a full minute. The Ponyta lets you get close enough to see your face in its eyes... then lowers its horn, curious, testing.",
                                   { :effects => "RES+1" }, { :run => :fight }]],
          ["Quickly, before it runs.", ["You lunge. It doesn't run. It rears, and the glass around you rings like a struck bell.", { :run => :fight }]]] }
    ],
    :fight => [
      { :event_battle => :EL_GLASS_PONYTA,
        :caught => ["The Ponyta's mane dims to a gentle glow inside the ball. Outside the Orchard, for the first time, it will see a tree that moves.",
                    { :complete => true }],
        :won => ["The Ponyta skitters back into the glass trees. Its hoofprints still ring. It isn't gone. It's waiting to see if you come back."],
        :lost => ["You stagger out past the Veil. Behind you, faintly, the glass is still singing."] }
    ]
  }
})

#===============================================================================
# CHAPTER 3 - the Weavers' Road (Grey Saltings 541, Dyers' Ford 552, Thistledown Lea 540),
#             Gossamer Wood (524) and Briarwick (Gym 2); Deepwood (525) needs Cut (2 badges)
#===============================================================================
tr.quest(:EL_THREE_KNOTS, {
  :trial => :ELOWEN, :title => "Three Loyal, Three Knots", :giver => "Mother Aldreth", :map => 120,
  :where => "the Briarwick Lantern House", :rank => 1, :points => 3, :rec_level => 16, :chapter => 3,
  :unlock => "badges >= 1", :board => true, :tags => [:pilgrimage, :puzzle, :spiritual, :lore],
  :summary => "A pilgrimage: re-tie the silk knots at the three wayshrines of the Loyal Three, and answer what each shrine asks.",
  :steps => { :ask => "Tie a silk knot at the river shrine at the Dyers' Ford, the shrine in Gossamer Wood, and the Loyal Three shrine in Briarwick.",
              :return => "All three knots are tied. Go back to Mother Aldreth." },
  :reward => { :items => [[:MAGICALSEED, 2]] },
  :touches => "Lore seed for the Loyal Three / Ogerpon arc (story/04_ACT_I, Elowen legendary arc)",
  :scenes => {
    :offer => [
      { :map => "The Briarwick Lantern House is a hollow tree. Mother Aldreth sits at a lantern-loom, weaving paper and silk without looking." },
      [:ALDRETH, :neutral, "You walked in here the way the Saltmere children walk. All elbows. Sit."],
      [:ALDRETH, :neutral, "Three shrines, three knots. The Loyal Three walked this road when they came home with the ogre's... with their prize."],
      [:ALDRETH, :neutral, "Every spring someone ties the knots again. This spring the Glasswood got there first, and nobody's young enough to walk it."],
      [:ALDRETH, :deadpan, "Each shrine asks a question. Answer honestly. They can tell. So can I."],
      { :choice => "Walk the pilgrimage?", :options => [
          ["I'll walk it.", [{ :accept => true }, "Mother Aldreth gives you three lengths of silk cord."]],
          ["Not now.", []]] }
    ],
    :shrine_river => [
      "A stone shrine by the ford, carved with a hound. Its collar is carved as a chain. The dyers' runoff has stained it blue.",
      "Words on the plinth: \"WHAT DID THE FIRST OF THE THREE WEAR AT ITS THROAT?\"",
      { :choice => "Your answer?", :options => [
          ["A chain of poison.", ["The old cord falls away at your touch. You tie the new knot.", { :flag => [:river, true] }, { :run => :knot }]],
          ["A golden collar.", ["Nothing happens. The hound's carved eyes seem disappointed in you."]],
          ["Nothing. It was free.", ["Nothing happens. The carved chain is right there."]]] }
    ],
    :shrine_wood => [
      "A shrine in a hollow of Gossamer silk, carved with a monkey clutching something to its chest.",
      "\"WHAT DID THE SECOND OF THE THREE CARRY HOME?\"",
      { :choice => "Your answer?", :options => [
          ["A mask that wasn't theirs.", ["The silk sighs. You tie the new knot.", { :flag => [:wood, true] }, { :run => :knot }]],
          ["The ogre's head.", ["Nothing happens. A Spinarak somewhere tuts."]],
          ["A basket of peaches.", ["Nothing happens. It's a lovely thought, though."]]] }
    ],
    :shrine_square => [
      "The Loyal Three shrine in Briarwick's square. Children's ogre masks hang around it on pegs.",
      "\"WHO WEPT IN THE WOOD WHEN THE THREE CAME HOME?\"",
      { :choice => "Your answer?", :options => [
          ["The ogre.", ["The masks on their pegs turn, very slightly, in no wind. You tie the knot.", { :flag => [:square, true] }, { :run => :knot }]],
          ["The villagers, for joy.", ["Nothing happens. That's the story they tell. It isn't what the shrine asked."]],
          ["Nobody.", ["Nothing happens."]]] }
    ],
    :knot => [
      { :count => [:knots, 1] },
      { :if => "quest_count(:SELF, :knots) >= 3", :then => [{ :step => :return }] }
    ],
    :return => [
      [:ALDRETH, :neutral, "Three knots. I felt each one pull tight. Here." ],
      { :map => "She taps her own throat, then her chest, then her eyes." },
      [:ALDRETH, :neutral, "A chain. A stolen face. And the one who wept was the one they called the monster."],
      [:ALDRETH, :deadpan, "You heard the true story. Don't tell the children. They like the other one."],
      [:ALDRETH, :neutral, "An old woman sang it to me better than that once. Never saw her again. Never saw anything again, mind you."],
      { :complete => true }
    ]
  }
})

tr.quest(:EL_HORN_AND_PINCER, {
  :trial => :ELOWEN, :title => "The Horn and the Pincer", :giver => "the lantern rope (no one signed it)", :map => 524,
  :where => "the sap tree on the old trail, Gossamer Wood", :rank => 1, :points => 2, :rec_level => 15, :chapter => 3,
  :unlock => "badges >= 1", :board => true, :tags => [:rival_duel, :event_mon],
  :summary => "Two great Bug Pokémon are fighting over the sap tree on the old trail. The trail has been blocked for a week.",
  :steps => { :ask => "Find the sap tree on the old trail in Gossamer Wood and end the fight." },
  :reward => { :items => [[:HONEY, 2]] },
  :touches => "none; the one you help clears a shortcut (Heracross tears a silk wall, Pinsir crushes a log)",
  :scenes => {
    :tree => [
      "A Heracross and a Pinsir are locked horn-to-pincer at the foot of a weeping sap tree, shoving each other in slow circles.",
      "Both of them stop and look at you. Then at each other. Then at you.",
      { :choice => "Who do you stand with?", :options => [
          ["Stand with the Heracross.", [
             "The Heracross bows. The Pinsir's mandibles open wide.",
             { :event_battle => :EL_PINSIR,
               :caught => [{ :run => :hera_helps }], :won => ["The Pinsir crashes away into the undergrowth.", { :run => :hera_helps }] }]],
          ["Stand with the Pinsir.", [
             "The Pinsir clacks once, approving. The Heracross lowers its horn.",
             { :event_battle => :EL_HERACROSS,
               :caught => [{ :run => :pinsir_helps }], :won => ["The Heracross buzzes away over the canopy.", { :run => :pinsir_helps }] }]],
          ["Back away.", []]] }
    ],
    :hera_helps => [
      "The Heracross drinks from the sap tree, then hooks its horn into the silk wall behind it and tears it down in one heave.",
      "A shortcut through the Gossamer opens toward Briarwick. The Heracross bows appreciatively and flies off.",
      { :flag => [:helper, :heracross] }, { :complete => :heracross }
    ],
    :pinsir_helps => [
      "The Pinsir drinks from the sap tree, then grips the fallen log across the trail and crushes it to splinters.",
      "A shortcut through the Gossamer opens toward Briarwick. The Pinsir nods appreciatively and stalks off.",
      { :flag => [:helper, :pinsir] }, { :complete => :pinsir }
    ]
  }
})

tr.quest(:EL_SILKTHIEF, {
  :trial => :ELOWEN, :title => "The Silkthief", :giver => "Hett", :map => 123,
  :where => "the Weavers' Guildhall", :rank => 2, :points => 3, :rec_level => 20, :chapter => 3,
  :unlock => "badges >= 2", :board => true, :tags => [:boss, :event_mon, :mystery],
  :summary => "Somebody is stealing finished silk straight off the drying racks at night. Hett has a theory, and it has eight legs.",
  :steps => { :ask => "Find out where Briarwick's silk is going. Hett thinks the Deepwood.",
              :nest => "Silk threads lead to the old moth nests in Gossamer Deepwood.",
              :report => "Tell Hett what you found." },
  :reward => { :money => 800 },
  :outcomes => { :guardian => { :items => [[:SILVERPOWDER, 1]], :effects => "RES+1" } },
  :touches => "Resonance (Harmony +1 if you leave the Spidops guarding the moths); Briarwick's moth tally board",
  :scenes => {
    :offer => [
      [:HETT, :angry, "Three bolts last night. Four the night before. Finished silk, dyed, ready for the barge."],
      [:HETT, :neutral, "No footprints. Just a thread, one thread, running off the rack into the dark. Toward the Deepwood."],
      [:HETT, :worried, "Tamsin's got enough on her plate. Will you follow the thread? I'd go myself but I'm a weaver, not an idiot."],
      { :choice => "Follow the thread?", :options => [
          ["I'll follow it.", [{ :accept => true }]],
          ["Not now.", []]] }
    ],
    :nest => [
      { :map => "Deep in the Deepwood, the old silk-moth nests hang like paper lanterns. Each one is wrapped in fresh, dyed Briarwick silk." },
      "Inside the nests, the cocoons of the dying silk-moths are warm. Someone has been keeping them warm.",
      { :step => :nest },
      { :event_battle => :EL_SPIDOPS,
        :won => [{ :run => :after }], :caught => [{ :run => :after }],
        :lost => ["The Silkthief hauls itself back up into the canopy and keeps watch over its nests."] }
    ],
    :after => [
      "The Spidops crouches between you and the nests, legs shaking. It isn't guarding the silk. It's guarding the moths.",
      "The Glasswood's cold has been killing the cocoons. The Spidops has been stealing silk to wrap them warm.",
      { :choice => "What do you do?", :options => [
          ["Take it with you.", ["The Spidops looks back at its nests once, then follows you.", { :join => :EL_SPIDOPS },
                                 { :flag => [:took, true] }, { :step => :report }]],
          ["Leave it guarding the nests.", ["You leave it. It settles back over the cocoons like a hen.", { :flag => [:guardian, true] }, { :step => :report }]]] }
    ],
    :report => [
      [:HETT, :shocked, "It was keeping the moths alive? With our silk?"],
      { :if => "quest_flag(:SELF, :guardian)", :then => [
          [:HETT, :neutral, "Then it can have the offcuts. Every night, on the end rack. Tell no one I'm soft."],
          { :complete => :guardian }
        ], :else => [
          [:HETT, :neutral, "And now it's yours. Well. We'll wrap the nests ourselves. Should've been doing it all along."],
          { :complete => :took }
        ] }
    ]
  }
})
