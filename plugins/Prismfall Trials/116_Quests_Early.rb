#===============================================================================
# Prismfall Trials - 116 Early side content, Chapters 0-5 (2026-11-21)
#-------------------------------------------------------------------------------
# User: "try not to make each chapter thin please... we want every chapter to be
# significant." Each quest here hangs off its chapter's key event
# (design/CHAPTER_BEATS.md) and pays out the Reborn/Rejuvenation way: an event
# Pokemon, a boss that joins, a TM, a rare catch that waits for a badge.
#   Ch0  Two Unlisted (the last ferry; the NULL scan)      Tandemaus, Ch1 payoff
#   Ch2  The Crown in the Sand (after the Pageant)         boss Sandygast, TM54
#   Ch3  The Note Under the Glass (after the Matriarch)    Joltik after Badge 3
#   Ch3  Someone Apologising to Bugs (Shelly's cameo)      board pointer, completes on her fight
#   Ch4  Bracken Comes In (the Wolfsrime, 579)             Greavard, TM65
#   Ch5  The Names in Holmsby (Ebb Hollow, Bleed)          Galarian Corsola
#   Ch5  The Machine Wants Compliments (Lumen Concourse)   comedy; Cell Battery (was a stub)
#   Ch5  Customer Support (the Spire lobby)                Porygon (was a stub)
# SPINE Revision 16: nothing handed over with b badges answers Warden b+1 or b+2;
# the event Pokemon (133_EventMons_Ch0_5.rb) declare :badges and the headless
# test recomputes them. SPINE Rev 22: generic quest-givers get plain boxes (they
# are SPEAKERS, not Portrait cast). Talk rows: 153_Talk_Early.rb. Map events:
# design/TRIAL_EVENTS.yaml; built maps through mapgen/trial_overlay.py.
#===============================================================================
tr = Prismfall::Trials
tr::SPEAKERS.merge!({
  :CRATE_WOMAN => "Woman with crate", :SCULPTOR => "Sand-sculptor", :HECKLER => "Pageant-goer",
  :DROVER => "Old drover", :VEIL_FISHER => "Fisher at the Veil", :FIZZBOLT => "Fizzbolt machine",
  :HELPDESK => "Helpdesk Rotom", :CLERK_RECORDS => "Records clerk", :CLERK_APPROVALS => "Approvals clerk",
  :CLERK_COMPLIANCE => "Compliance clerk"
})

#===============================================================================
# CHAPTER 0 - the last ferry (109) -> Ferrow's Landing (100) and the customs hall (108)
#===============================================================================
tr.quest(:EL_STOWAWAYS, {
  :trial => :ELOWEN, :title => "Two Unlisted", :giver => "the woman with the crate", :map => 109,
  :where => "the deck of the Dovetail (the last ferry)", :rank => 1, :points => 2, :rec_level => 5, :chapter => 0,
  :expires => "switch(102)", :board => false, :tags => [:kindness, :event_mon, :comedy],
  :summary => "On the last ferry, a passenger's crate squeaks. Twice. In harmony. She would be grateful if nobody mentioned it to customs.",
  :steps => { :landed => "Find the woman with the crate in Ferrow's Landing, once you have a Pokemon of your own.",
              :find => "Her crate came open at the customs gate. Two mice are loose somewhere warm in the Quarantine Customs Hall.",
              :return => "Bring the mice back to the woman with the crate, by the Ferrow's Landing quay." },
  :reward => { :items => [[:ORANBERRY, 2]] },
  :touches => "the Prologue's NULL scan: the crate went through the gate with you, and the gate saw nothing in either",
  :scenes => {
    :offer => [
      { :map => "A woman sits on a crate by the rail, holding the lid down with both hands. The crate squeaks." },
      [:CRATE_WOMAN, :neutral, "Tea service. My sister's. It's settling."],
      "The crate squeaks again. Twice. In harmony.",
      { :choice => "Tea services don't squeak.", :options => [
          ["Tea services don't squeak.", [
             [:CRATE_WOMAN, :sad, "...Two mice. They got into it in port, over there. Abroad. They were in the crate before I was."],
             [:CRATE_WOMAN, :neutral, "The Landing scans everyone now. Anything without papers goes back on the boat, and after tonight the boat doesn't come back."],
             [:CRATE_WOMAN, :neutral, "So they're a tea service. Just till Saltmere. You didn't hear anything."],
             { :accept => true },
             "(Your bag gives a small squeak of its own. No. That was the crate.)"]],
          ["(Say nothing.)", [
             "You say nothing. She looks at you for a long moment, then pats the crate.",
             [:CRATE_WOMAN, :happy, "Good. You'll do well here. Velmora's mostly things nobody mentions."],
             { :accept => true }]]] }
    ],
    :landed => [
      [:CRATE_WOMAN, :sad, "You! From the ferry. They've gone."],
      [:CRATE_WOMAN, :neutral, "I went through the gate with the crate under my arm, and it went 'Blank, Saltmere', lovely, and then the little girl's Wingull went BING and flapped off and I jumped and the lid came off."],
      [:CRATE_WOMAN, :neutral, "Two mice, straight under the customs desk. Nobody saw. The gate didn't see. It didn't see you either, I heard. Funny gate."],
      [:CRATE_WOMAN, :sad, "I can't go in there and ask for them back. I'd have to fill in a form saying they exist."],
      { :step => :find }
    ],
    :mice => [
      { :map => "Under the kiosk, against the slats of Crate 7-B, two small mice are curled up together, warming their paws on whatever is inside it." },
      "The two small flames in Crate 7-B lean toward them, the way you'd lean toward a friend. It's the warmest place in the building.",
      { :choice => "The mice?", :options => [
          ["Scoop them up.", [
             "They don't run. They climb into your sleeve together, as if they've done it before, and stay very still past the customs officer.",
             { :step => :return }]],
          ["Leave them by the crate for now.", ["The mice tuck their tails round each other. They're in no hurry."]]] }
    ],
    :return => [
      "The mice tumble out of your sleeve and run straight up the woman's coat.",
      [:CRATE_WOMAN, :happy, "There you are! Oh, you horrible things. You stink of customs."],
      [:CRATE_WOMAN, :neutral, "...The Saltmere Harbour Office has one of those machines too. Penny, it's called. It counts everything that comes in."],
      [:CRATE_WOMAN, :sad, "I can't keep them. They're unlisted. They'd go back."],
      [:CRATE_WOMAN, :neutral, "You're unlisted too, I hear. NULL. So nobody's counting you. Take them. They've already picked you; they were in your sleeve before you asked."],
      { :gift => :EL_TANDEMAUS },
      [:CRATE_WOMAN, :happy, "Two of them, one Poke Ball. They say that's how this kind works. Don't ask me. I'm a tea service."],
      { :complete => true }
    ]
  }
})

#===============================================================================
# CHAPTER 2 - Marram Down (528), after the Pageant (S108) and Badge 1
#===============================================================================
tr.quest(:EL_SAND_CROWN, {
  :trial => :ELOWEN, :title => "The Crown in the Sand", :giver => "the sand-sculptor", :map => 528,
  :where => "the sand Crown on Marram Down", :rank => 1, :points => 3, :rec_level => 18, :chapter => 2,
  :unlock => "badges >= 1 && switch(108)", :board => true, :tags => [:boss, :event_mon, :spiritual, :comedy],
  :summary => "Since the Pageant went grey, someone walks out from Saltmere and kicks down the sand Crown on Marram Down every night. Every morning it's back, taller. The sculptor didn't rebuild it.",
  :steps => { :ask => "Watch the sand Crown on Marram Down after dark.",
              :report => "Tell the sand-sculptor what has been rebuilding her Crown." },
  :reward => { :items => [[:TM54, 1]] },
  :outcomes => { :centrepiece => { :items => [[:STARDUST, 2]], :effects => "RES+1" } },
  :touches => "the Pageant hijack (Ch2 key event): Saltmere's anger at the Sovereign; Resonance (Harmony +1 if you leave the Sandygast to be the Crown)",
  :scenes => {
    :offer => [
      [:SCULPTOR, :angry, "Every night since the Pageant, somebody walks out from Saltmere and kicks my Crown in."],
      [:SCULPTOR, :neutral, "'Ask your Sovereign!' they shout. As if the Sovereign's ever been to Marram Down. As if he'd notice a sand Crown."],
      [:SCULPTOR, :worried, "And every morning it's back. Taller. I didn't rebuild it. I've been sleeping in the wagon with a shovel."],
      [:SCULPTOR, :deadpan, "Something ate the shovel."],
      { :choice => "Watch the Crown tonight?", :options => [
          ["I'll watch it.", [{ :accept => true },
                              [:SCULPTOR, :happy, "After dark, then. Bring something that isn't a shovel."]]],
          ["Not now.", [[:SCULPTOR, :neutral, "Then it's me and the wagon again. And no shovel."]]]] }
    ],
    :crown => [
      { :if => "!night", :then => [
          "In daylight it's just a very good sand Crown, as tall as you, with a chipped stone in the middle. The sand is warm.",
          "(The sculptor asked you to watch it after dark.)",
          { :end => true }] },
      { :map => "Moonlight on the dunes. Footsteps on the Saltmere road: a man in a Pageant-goer's good coat, red in the face." },
      [:HECKLER, :angry, "Ask your Sovereign! ASK HIM! Three hundred years of--"],
      "He kicks the Crown. His boot goes in up to the ankle. The sand closes round it.",
      [:HECKLER, :shocked, "It's got me! The Crown's got me! I take it back! Long live the Sovereign!"],
      "The sand lets go. He runs all the way back to Saltmere with one boot.",
      "Then the Crown turns round to look at you. There's a shovel handle sticking out of the top of it.",
      { :event_battle => :EL_SANDYGAST,
        :won => [{ :run => :after }], :caught => [{ :run => :after }],
        :lost => ["The Crown slumps into an ordinary heap of sand. By morning it'll be taller."] }
    ],
    :after => [
      "The Sandygast sags into a smaller, rounder heap. Pressed into its sand is a brass letter from a ship's name-board: a W, from THE WANDERING CHORUS, the theatre barge buried in the dunes.",
      "It isn't a crown. It's a stage set made of an old stage, and it's lonely for an audience.",
      { :choice => "What do you do?", :options => [
          ["Take it with you.", [
             "The Sandygast gathers itself up and follows you, leaving a neat trail.",
             { :join => :EL_SANDYGAST }, { :flag => [:took, true] }, { :step => :report }]],
          ["Leave it to be the Crown.", [
             "You pat the sand smooth. It rebuilds itself, a little taller, and settles in to be looked at.",
             { :flag => [:centrepiece, true] }, { :step => :report }]]] }
    ],
    :report => [
      { :if => "quest_flag(:SELF, :centrepiece)", :then => [
          [:SCULPTOR, :shocked, "It's a Sandygast? My Crown is a Sandygast? It bites hecklers?"],
          [:SCULPTOR, :happy, "A Crown that rebuilds itself and bites anyone who kicks it. The free port is going to LOVE that."],
          "(By morning she's charging a penny a look.)",
          [:SCULPTOR, :neutral, "Here. I won this in a raffle. 'False Swipe'. I tried it on sand. It doesn't work on sand."],
          { :complete => :centrepiece }
        ], :else => [
          [:SCULPTOR, :shocked, "A Sandygast. My Crown was a Sandygast. And now it's yours."],
          [:SCULPTOR, :neutral, "Well. It had better taste than the people kicking it. I'll build another. A smaller one. With a fence."],
          [:SCULPTOR, :neutral, "Take this. I won it in a raffle. 'False Swipe'. I tried it on sand. It doesn't work on sand."],
          { :complete => :took }
        ] }
    ]
  }
})

#===============================================================================
# CHAPTER 3 - after the Glass Matriarch (S107): Briarwick (126) and Cocoonfall Hollow (548)
#===============================================================================
tr.quest(:EL_MATRIARCH_HUM, {
  :trial => :ELOWEN, :title => "The Note Under the Glass", :giver => "Mother Aldreth", :map => 126,
  :where => "the Briarwick Lantern House", :rank => 1, :points => 3, :rec_level => 23, :chapter => 3,
  :unlock => "switch(107)", :board => true, :tags => [:spiritual, :event_mon, :revisit],
  :summary => "Since the Glass Matriarch fell, Mother Aldreth's lantern-loom hums at night. One note, from the direction of Cocoonfall Hollow.",
  :steps => { :ask => "Find what is humming in Cocoonfall Hollow.",
              :wait => "A small glass cocoon by the Matriarch's nest hums one note under your badge case's chord. It is waiting for a third note (Badge 3)." },
  :reward => { :items => [[:EXPCANDYM, 2]] },
  :touches => "the Glass Matriarch (Ch3 key event) and :ch2_matriarch: a soothed Matriarch's last cocoon hatches to you; a silenced one's is afraid of you",
  :scenes => {
    :offer => [
      [:ALDRETH, :neutral, "You went into the Hollow and came out. The wood is quieter. The moths are eating again."],
      [:ALDRETH, :neutral, "But my loom hums at night now. One note. Lower than the looms, higher than the wind."],
      [:ALDRETH, :neutral, "It comes from the Hollow. Something the Matriarch left. Go and listen, and don't touch what you don't understand."],
      [:ALDRETH, :deadpan, "Which is everything, at your age. Touch it anyway. You will."],
      { :choice => "Go and listen?", :options => [
          ["I'll listen.", [{ :accept => true }]],
          ["Not now.", [[:ALDRETH, :neutral, "It will still be humming. Things that hum are patient."]]]] }
    ],
    :cocoon => [
      { :if => "quest_step(:SELF) == :ask", :then => [
          { :map => "Among the Matriarch's glass cocoons, one is smaller than the others, and warm. It hums." },
          "You hold your badge case near it. The case answers with its own chord: the Footlight's note and the Weft's.",
          "The cocoon's note sits just under them, patient, as if it's waiting for a third."] },
      { :if => "badges >= 3", :then => [{ :run => :hatch }], :else => [
          { :if => "quest_step(:SELF) == :wait", :then => ["The little cocoon hums under the glass. Your case has two notes. It wants three."] },
          { :step => :wait }] }
    ],
    :hatch => [
      "Your badge case sounds three notes together: the Footlight, the Weft, and the new one from Ebbmouth. The cocoon's hum climbs to meet them.",
      "The glass cracks like ice on a pond. A Joltik tumbles out, fizzing, and looks up at you with four bright eyes.",
      { :if => "choice(:ch2_matriarch) == :soothe", :then => [
          "It remembers you. You sat with its mother all night while she calmed.",
          "It climbs your sleeve and settles in your collar, humming in tune with the case.",
          { :gift => :EL_JOLTIK }, { :complete => :soothed }
        ], :else => [
          "It sees your hand, and the static goes out of its fur. It remembers the hand that emptied its mother.",
          "It bares its mandibles, and every hair stands up.",
          { :event_battle => :EL_JOLTIK,
            :caught => ["It goes quiet in the ball. Maybe it will hum again, one day.", { :complete => :silenced }],
            :won => ["It skitters back into the shards of its cocoon. Come back. It can't stay angry for ever, and neither can glass."],
            :lost => ["It sparks once, triumphant, and hides in the shards of its cocoon."] }
        ] }
    ]
  }
})

tr.quest(:EL_SHELLY, {
  :trial => :ELOWEN, :title => "Someone Apologising to Bugs", :giver => "Mother Aldreth", :map => 120,
  :where => "the Briarwick Lantern House", :rank => 2, :points => 3, :rec_level => 21, :chapter => 3,
  :unlock => "badges >= 2", :board => true, :tags => [:cameo, :battle],
  :summary => "A stranger with pink hair is lost in the Gossamer Deepwood, apologising to the Bug Pokemon. The spirits of the wood are uneasy.",
  :steps => { :ask => "Find the lost stranger in the Gossamer Deepwood, past the Cut tree, and help her home." },
  :reward => {},
  :touches => "Ledger cameo record (FESTIVAL_SHELLY); CAMEOS.md #1. Her Deepwood event gives Silver Powder and her TM; the quest completes when she is beaten (CAMEO_QUESTS, the :prismfall_cameo_beaten handler)",
  :design => "Board pointer to CAMEOS.md 'Lost in the Gossamer'. The cameo event on 525 calls Prismfall.cameo_battle(:FESTIVAL_SHELLY, \"Shelly\", 1, double: true); the Trials plugin completes this quest when that fight is won (no map change needed).",
  :scenes => {
    :offer => [
      [:ALDRETH, :neutral, "There's a girl in the Deepwood who apologises to the Bugs. All of them. One at a time."],
      [:ALDRETH, :neutral, "She isn't from here. She isn't from anywhere I can hear. The wood keeps re-weaving the paths round her, to keep her, I think. It likes being apologised to."],
      [:ALDRETH, :deadpan, "Go and fetch her before it decides she's a moth."],
      { :choice => "Find the stranger?", :options => [
          ["I'll find her.", [{ :accept => true }]],
          ["Not now.", []]] }
    ]
  }
})

#===============================================================================
# CHAPTER 4 - the Wolfsrime (579): the old drove road between the Rimewood and Frostwick Pass
#===============================================================================
tr.quest(:EL_DROVERS_BELL, {
  :trial => :ELOWEN, :title => "Bracken Comes In", :giver => "the old drover", :map => 579,
  :where => "the Wolfsrime, by the cold kiln", :rank => 1, :points => 2, :joint => { :ISENMAR => 1 }, :rec_level => 21,
  :chapter => 4, :unlock => "badges >= 2", :board => false, :tags => [:spiritual, :event_mon],
  :summary => "Every autumn the old drover's da rang the bell on the Wolfsrime to call his dog in off the fell. The last autumn, Bracken never came. Something still answers the bell.",
  :steps => { :ask => "Ring the drover's bell up the Wolfsrime and follow whatever answers it.",
              :return => "Bring Bracken down to the old drover by the cold kiln." },
  :reward => { :items => [[:TM65, 1]] },
  :touches => "borderland (Elowen + Isenmar points); the Wolfsrime's den and bell (map builder 14's lines)",
  :scenes => {
    :offer => [
      [:DROVER, :neutral, "My da drove sheep down this road every autumn. Bracken did the work. Da walked behind and took the credit."],
      [:DROVER, :sad, "The year they blazed the North Gate road, Bracken went up the fell for a stray and never came down. Wolves, Da said. He rang that bell every night till the snow came."],
      [:DROVER, :neutral, "I ring it, some years. Can't get up there now, with these knees. Something answers. The boy says wolves."],
      [:DROVER, :deadpan, "Wolves don't answer bells. Dogs do."],
      { :choice => "Ring the bell for him?", :options => [
          ["I'll ring it.", [{ :accept => true },
                             [:DROVER, :neutral, "Up the road, on the birch past the clawed one. Ring it, then follow your ears. Bracken always came the long way."]]],
          ["Not now.", [[:DROVER, :neutral, "No hurry. Fifty years. What's another one."]]]] }
    ],
    :den => [
      { :map => "In the hollow under the fallen giant, among the old bones, something grey and dog-shaped is digging. It looks up, ears high, tail going." },
      "It's a Greavard. Round its neck is a drover's collar with a brass tag, green with age: BRACKEN.",
      "It drops an old bone at your feet, backs off two steps, and crouches. It wants to play.",
      { :event_battle => :EL_GREAVARD,
        :caught => ["Bracken's tail thumps against the inside of the ball.", { :step => :return }],
        :won => ["Bracken bounds off into the birches, delighted, and comes straight back with the bone. It wants to go again."],
        :lost => ["Bracken licks your face and trots back into its den. It isn't tired. It has never once been tired."] }
    ],
    :return => [
      "Bracken sits down at the old man's feet, the way it must have sat at his father's.",
      [:DROVER, :shocked, "...That's his collar. That's Da's knot on it."],
      [:DROVER, :sad, "He came in. Took him fifty years, but he came in."],
      [:DROVER, :neutral, "Take him down the Pass. He always liked the Pass. And take this. It was Da's. He kept it for the wolves. Never once hit one."],
      { :complete => true }
    ]
  }
})

#===============================================================================
# CHAPTER 5 - the Lock Road and Lumen (story/24_SCRIPT_CH5.md; maps by map builder 15). The script already carries
# the Ice Elevator (590), the heat-contract satchel (592/596), Lamp 47's clue (593) and the Sluiceworks Rotom (585);
# the Trials add the drowned village behind the Reedholms Veil and the two Lumen hooks the script asks for
# (the Concourse's Fizzbolt machine, 180; the Spire's helpdesk Rotom, 185). Off the Beat's after-Shatter
# route is in 113 (Cadence moves to the Concourse).
#===============================================================================
tr.quest(:IS_EBB_HOLLOW, {
  :trial => :ISENMAR, :title => "The Names in Holmsby", :giver => "the fisher at the Veil", :map => 580,
  :where => "the Bleed Veil on the Reedholms' south bank", :rank => 1, :points => 3, :rec_level => 25, :chapter => 5,
  :unlock => "badges >= 3", :board => true, :tags => [:bleed, :event_mon, :saga],
  :summary => "In AF 296 the Ebb lifted itself off its bed over Holmsby and never put itself down. Everyone walked out under it. Their names are still cut on the village's boundary stones, under the Bleed, and the Tally has never counted them.",
  :steps => { :ask => "Walk into Ebb Hollow (only you can) and read the names off Holmsby's boundary stones.",
              :coral => "The last stone is by the old eel-weir, under something white.",
              :return => "Bring the names back to the fisher at the Veil." },
  :reward => { :items => [[:EXPCANDYM, 2], [:BIGPEARL, 1]] },
  :touches => "the Bleed's reach (Ch5's key event is the Lowlight's wound; this is an old scar of the same kind); the Tally Mast at Ebbmouth",
  :scenes => {
    :offer => [
      [:VEIL_FISHER, :neutral, "Holmsby. The Ebb took it in AF 296. Didn't flood it. Lifted the river clean off its bed and left it hanging."],
      [:VEIL_FISHER, :neutral, "We all walked out under it. Every soul. Bersi made a song of it, the liar. He gave us a whale."],
      [:VEIL_FISHER, :sad, "But we left the names. Every family in Holmsby cuts its name on a boundary stone, and the stones are in there, under all that water. The Tally's never counted us."],
      [:VEIL_FISHER, :neutral, "...They say you can walk in. Read me the names, and I'll have them cut on the Tally Mast at Ebbmouth. So the sea keeps count."],
      { :choice => "Read the names?", :options => [
          ["I'll go in.", [{ :accept => true }]],
          ["Not now.", [[:VEIL_FISHER, :neutral, "The stones aren't going anywhere. That's rather the problem."]]]] }
    ],
    :stone => [
      { :count => [:stones, 1] },
      { :if => "quest_count(:SELF, :stones) >= 2", :then => [
          "A boundary stone, perfectly dry under a hanging drop of river. Names cut deep, then cut again, smaller, by children: SKARD. VEN. THE VEN TWINS. BOTH OF THEM.",
          "Two stones read. The fisher said three. By the old eel-weir, something white is growing over the last one.",
          { :step => :coral }
        ], :else => [
          "A boundary stone, perfectly dry. A trout drifts past it at head height, asleep. You read the names out loud, because it seems rude not to: ORM. LITTLE ORM. ORM'S DOG."] }
    ],
    :coral => [
      { :map => "By the old eel-weir, under a drop of river the size of a house, coral has grown out of fresh water, white as bone. It moves." },
      "A Corsola, bleached white by the Bleed, has wrapped itself round the last stone. It isn't guarding it. It's holding on.",
      { :event_battle => :IS_CORSOLA,
        :caught => [{ :run => :names }], :won => [{ :run => :names }],
        :lost => ["The white coral tightens round the stone. It isn't letting go yet."] }
    ],
    :names => [
      "The last stone is clear. Its names are the oldest: HALDIS. BRENNA. And under them, in chalk that should have washed off years ago and didn't: WE'LL BE BACK SATERDAY.",
      { :step => :return }
    ],
    :return => [
      [:VEIL_FISHER, :sad, "...Saterday. That's my niece. She chalked it on number nine as well. She still spells it like that, to annoy her mother."],
      [:VEIL_FISHER, :neutral, "I'll take the names up to Bersi at the Net Loft myself. You've done the walking."],
      [:VEIL_FISHER, :happy, "He'll make it rhyme. He'll make the river forty feet high and give it teeth. Let him. As long as the names are right."],
      { :complete => true }
    ]
  }
})

tr.quest(:ZE_FIZZBOLT, {
  :trial => :ZENITH, :title => "The Machine Wants Compliments", :giver => "a Fizzbolt vending machine", :map => 180,
  :where => "Lumen City Concourse", :rank => 1, :points => 2, :rec_level => 24, :chapter => 5,
  :unlock => "badges >= 3", :board => true, :tags => [:comedy],
  :summary => "A Lumen vending machine has gained sentience from the free current and only sells Fizzbolt to people who compliment it.",
  :steps => { :ask => "Pay the Fizzbolt machine five different compliments. It knows when you've said one before." },
  :reward => { :items => [[:SODAPOP, 6], [:CELLBATTERY, 1]] },
  :touches => "none (15_COMEDY: the vending quest); the free current's Rotom, one more of Lumen's",
  :scenes => {
    :offer => [
      { :map => "A brass-and-glass Fizzbolt machine on the Concourse, with a Rotom-shaped dent in the glass. A card is taped beside the coin slot." },
      "The card reads: THIS UNIT IS UNDER OBSERVATION. PLEASE DO NOT ENCOURAGE IT. - MERIDIAN VENDING.",
      [:FIZZBOLT, :sad, "Coins. Coins, coins, coins. Nobody ever says anything NICE."],
      { :choice => "The machine is waiting.", :options => [
          ["Say something nice.", [{ :accept => true }, { :run => :compliment }]],
          ["Walk on.", [[:FIZZBOLT, :sad, "...Nobody ever stays, either."]]]] }
    ],
    :compliment => [
      { :if => "quest_flag(:SELF, :sulking)", :then => [
          "The machine's lights are off. It's facing the wall. As much as a vending machine can face anything.",
          "...After a while, one light flickers back on. It has decided to forgive you. Once.",
          { :flag => [:sulking, false] }, { :end => true }] },
      { :choice => [:FIZZBOLT, :neutral, "Well? Go on."], :options => [
          ["Your glass is very clean.", [{ :if => "quest_flag(:SELF, :c1)", :then => [{ :run => :sulk }], :else => [{ :flag => [:c1, true] }, { :run => :nice }] }]],
          ["You hum in a lovely key.", [{ :if => "quest_flag(:SELF, :c2)", :then => [{ :run => :sulk }], :else => [{ :flag => [:c2, true] }, { :run => :nice }] }]],
          ["Best machine on the Concourse.", [{ :if => "quest_flag(:SELF, :c3)", :then => [{ :run => :sulk }], :else => [{ :flag => [:c3, true] }, { :run => :nice }] }]],
          ["Your buttons are lovely to press.", [{ :if => "quest_flag(:SELF, :c4)", :then => [{ :run => :sulk }], :else => [{ :flag => [:c4, true] }, { :run => :nice }] }]],
          ["I like your little dent.", [{ :if => "quest_flag(:SELF, :c5)", :then => [{ :run => :sulk }], :else => [{ :flag => [:c5, true] }, { :run => :nice }] }]],
          ["You're brave, standing out here all day.", [{ :if => "quest_flag(:SELF, :c6)", :then => [{ :run => :sulk }], :else => [{ :flag => [:c6, true] }, { :run => :nice }] }]]] }
    ],
    :nice => [
      { :count => [:nice, 1] },
      { :if => "quest_count(:SELF, :nice) >= 5", :then => [{ :run => :jackpot }, { :end => true }] },
      { :if => "quest_count(:SELF, :nice) == 1", :then => [[:FIZZBOLT, :shocked, "...Oh. Oh. Say that again. No, don't. I'll remember it."]] },
      { :if => "quest_count(:SELF, :nice) == 2", :then => [[:FIZZBOLT, :happy, "Two! Two nice things! I'm going to tell the ticket machine. It's going to be SO jealous."]] },
      { :if => "quest_count(:SELF, :nice) == 3", :then => [[:FIZZBOLT, :happy, "Three. I've had a Fizzbolt stuck in my chute since spring. I think it's coming loose."]] },
      { :if => "quest_count(:SELF, :nice) == 4", :then => [[:FIZZBOLT, :neutral, "Four. One more and I don't know what I'll do. Something unprofessional."]] },
      "(Come back and say something else. It will want a new one.)"
    ],
    :sulk => [
      [:FIZZBOLT, :angry, "You SAID that. You said that ALREADY."],
      "Every light on the machine goes out. It's sulking.",
      { :flag => [:sulking, true] }
    ],
    :jackpot => [
      [:FIZZBOLT, :happy, "FIVE."],
      "The machine shudders, rings like a till, and dispenses everything it has at once. Fizzbolt rolls across the Concourse in every direction.",
      "A Rotom shoots out of the dent in the glass, does a lap of the Concourse, high-fives a streetlamp, and dives back in.",
      [:FIZZBOLT, :happy, "Take them. Take them all. And this, it was rattling about in my coin box. I don't know what it is. I don't care. I'm LOVED."],
      { :complete => true }
    ]
  }
})

tr.quest(:ZE_CUSTOMER_SUPPORT, {
  :trial => :ZENITH, :title => "Customer Support", :giver => "Helpdesk Rotom", :map => 185,
  :where => "Meridian Spire lobby, Lumen City", :rank => 1, :points => 3, :rec_level => 24, :chapter => 5,
  :unlock => "badges >= 3", :board => true, :tags => [:comedy, :bureaucracy, :event_mon],
  :summary => "Walk a form through the Spire's three lobby desks. The form is to cancel the form.",
  :steps => { :ask => "Get Form 0 (Cancellation of Form 0) stamped at Records, Approvals and Compliance.",
              :return => "Every desk has stamped it. Take Form 0 back to the helpdesk." },
  :reward => { :pokemon => :ZE_PORYGON },
  :touches => "15_COMEDY Zenith bit 'Customer Support'",
  :scenes => {
    :offer => [
      { :map => "The helpdesk in the Spire lobby: a brass console with a Rotom living in its screen, wearing a headset it has no ears for." },
      [:HELPDESK, :happy, "THANK YOU FOR CONTACTING MERIDIAN. YOUR CALL IS IMPORTANT TO US. YOU ARE CALLER NUMBER ONE. YOU HAVE ALWAYS BEEN CALLER NUMBER ONE."],
      [:HELPDESK, :neutral, "I HAVE A FORM I WOULD LIKE TO CANCEL. IT IS FORM 0. FORM 0 IS THE FORM FOR CANCELLING FORMS."],
      [:HELPDESK, :sad, "IT NEEDS THREE STAMPS: RECORDS, APPROVALS AND COMPLIANCE. I CANNOT LEAVE THE DESK. I AM THE DESK."],
      { :choice => "Take Form 0?", :options => [
          ["I'll walk it round.", [{ :accept => true },
                                   [:HELPDESK, :happy, "THANK YOU. PLEASE RATE YOUR EXPERIENCE. NOT YET. LATER. I GET AHEAD OF MYSELF."]]],
          ["Not now.", [[:HELPDESK, :neutral, "YOUR CALL HAS BEEN PLACED IN A QUEUE. YOU ARE STILL NUMBER ONE."]]]] }
    ],
    :records => [
      { :if => "quest_flag(:SELF, :records)", :then => ["(Records has stamped it. The clerk is pretending not to see you, in case you have another form.)", { :end => true }] },
      { :if => "quest_flag(:SELF, :approvals)", :then => [
          [:CLERK_RECORDS, :neutral, "Approved? Approved. Then it can be recorded. RECORDED."],
          "(Thunk.)", { :flag => [:records, true] }, { :run => :check }
        ], :else => [
          [:CLERK_RECORDS, :deadpan, "I can't record a form that hasn't been approved. That would be a record of nothing. Approvals, next desk."]] }
    ],
    :approvals => [
      { :if => "quest_flag(:SELF, :approvals)", :then => ["(Approvals has stamped it. The clerk gives you a thumbs-up without looking.)", { :end => true }] },
      { :if => "quest_flag(:SELF, :compliance)", :then => [
          [:CLERK_APPROVALS, :happy, "Compliant! Then it's approved. Lovely. I love it when things are approved."],
          "(Thunk.)", { :flag => [:approvals, true] }, { :run => :check }
        ], :else => [
          [:CLERK_APPROVALS, :neutral, "I can't approve something that might not comply. Compliance, end desk, two windows."]] }
    ],
    :compliance => [
      { :if => "quest_flag(:SELF, :compliance)", :then => ["(Compliance has stamped it, at the second window.)", { :end => true }] },
      { :choice => "The Compliance desk has two windows. One says COMPLIANCE. The other says CANCELLATIONS OF CANCELLATIONS.", :options => [
          ["Window one: Compliance.", [
             [:CLERK_COMPLIANCE, :deadpan, "Has it been recorded? I can't check a form for compliance unless there's a record of it. Records. Other end."]]],
          ["Window two: Cancellations of Cancellations.", [
             "The same clerk slides along to the second window, puts on a different hat, and clears her throat.",
             [:CLERK_COMPLIANCE, :neutral, "A cancellation of a cancellation form? Those need no stamps at all. That's the point of them. Nobody ever comes to this window."],
             [:CLERK_COMPLIANCE, :happy, "Different window, different rules. Stamped. Compliant. Don't tell the other window."],
             "(Thunk.)", { :flag => [:compliance, true] }, { :run => :check }]]] }
    ],
    :check => [
      { :if => "quest_flag(:SELF, :records) && quest_flag(:SELF, :approvals) && quest_flag(:SELF, :compliance)", :then => [
          "Three stamps. Form 0 is complete. It is now the most legitimate piece of paper in Lumen.", { :step => :return }] }
    ],
    :return => [
      [:HELPDESK, :happy, "THREE STAMPS. FORM 0 IS NOW CANCELLED. CANCELLING FORM 0 CANCELS FORM 0."],
      "The form folds itself in half. Then in half again. Then into a shape paper can't fold into, all corners, pink and blue, and it blinks at you.",
      [:HELPDESK, :shocked, "OH. IT WAS A PORYGON. IT WAS A PORYGON THE WHOLE TIME. IT HAS BEEN IN THE SYSTEM SINCE AF 291."],
      [:HELPDESK, :neutral, "IT IS NOT MERIDIAN PROPERTY. IT IS NOT ANY FORM. PLEASE TAKE IT. PLEASE RATE YOUR EXPERIENCE. NOW. NOW IS THE TIME."],
      { :complete => true }
    ]
  }
})
#-------------------------------------------------------------------------------
# Cameo quests complete when their cameo fight is won (Core's cameo_battle fires
# :prismfall_cameo_beaten), so the cameo's own map event needs no quest call.
#-------------------------------------------------------------------------------
module Prismfall
  module Trials
    CAMEO_QUESTS = { :FESTIVAL_SHELLY => :EL_SHELLY }

    def self.on_cameo_beaten(trainer_type)
      qid = CAMEO_QUESTS[trainer_type]
      return false if !qid || !exists?(qid) || get(qid)[:stub] || done?(qid)
      return complete(qid)
    end
  end
end

if defined?(EventHandlers)
  EventHandlers.add(:prismfall_cameo_beaten, :prismfall_trials_cameo_quests,
    proc { |trainer_type, _first| Prismfall::Trials.on_cameo_beaten(trainer_type) }
  )
end
