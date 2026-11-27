#===============================================================================
# Prismfall Trials - 121 Cindervault (Chapter 8): the Ashkaar quests on the built maps
#-------------------------------------------------------------------------------
# Gemini built Cindervault on 2026-11-26/27: the Forge Terraces (240, the market
# and the Crucible), Pyre Keep (245-248, 254). These replace the catalogue stubs
# of 120_Quests_Catalogue.rb (this file loads after it; the board order stays):
#   Adequate Swords    the market (240) -> EXCELLENT SWORDS across the lane -> the
#                      Honest Court (the Oath-Scribe, Hall of Oaths 247) -> home
#   Seven Bouts        the Crucible (240): Legate Varra Kosk's entry rite, seven
#                      bouts, no healing, no bag; the barge's paper skips bout 1
#   The Trial of Truth the Hall of Oaths (247): Herald Pyke; the PC heard Haskar
#                      say who sent him for the Light Stone ("Whose Is It", 244)
# Talk rows: 155_Talk_Cindervault.rb. Map events: mapgen/trial_overlay.py (240,
# 247) and design/TRIAL_EVENTS.yaml. Trainers: tools/trainer_gen/gen.py
# ("Ch8 Trials", v50 / 150 / 250).
#===============================================================================
tr = Prismfall::Trials
tr::SPEAKERS.merge!({
  :ADEQUATE => "Adequate Swords", :KESSA => "Kessa of Excellent Swords", :SCRIBE => "Oath-Scribe",
  :PYKE => "Herald Pyke", :HALDEN => "Tribune Halden", :CRUCIBLE_HERALD => "Crucible Herald"
})

#===============================================================================
# Adequate Swords (Ch8, the market on 240)
#===============================================================================
tr.quest(:AS_ADEQUATE_SWORDS, {
  :trial => :ASHKAAR, :title => "Adequate Swords", :giver => "the owner of ADEQUATE SWORDS", :map => 240,
  :where => "Cindervault market, the Forge Terraces", :rank => 1, :points => 2, :rec_level => 38, :chapter => 8,
  :unlock => "badges >= 6", :board => true, :tags => [:comedy, :battle, :honesty],
  :summary => "A rival shop has opened across the lane: EXCELLENT SWORDS. The owner of ADEQUATE SWORDS suspects a lie. Lying is a crime.",
  :steps => { :test => "Test the blades at EXCELLENT SWORDS, across the lane.",
              :court => "Take the result to the Honest Court: the Oath-Scribe in the Hall of Oaths, Pyre Keep.",
              :home => "Tell ADEQUATE SWORDS what the court said." },
  :reward => { :items => [[:METALCOAT, 1]] },
  :touches => "15_COMEDY Ashkaar honest-signs bit; the Oath-Scribe's 'Excellent' cases (247)",
  :design => "You test the swords (a battle against Kessa's Honedge line on the caldera floor). The swords are excellent. ADEQUATE SWORDS loses the case, renames itself ADEQUATE SWORDS (STILL), and is happier.",
  :scenes => {
    :offer => [
      [:ADEQUATE, :neutral, "You've a Warden's badges. Good. I need a witness, and witnesses here have to be able to hit things."],
      [:ADEQUATE, :angry, "Look across the lane. EXCELLENT SWORDS. Painted last week. In gold."],
      [:ADEQUATE, :neutral, "Lying's a crime in Ashkaar. If her swords are only adequate, that sign's a lie, and the Honest Court will have it down by supper."],
      [:ADEQUATE, :neutral, "I can't test them. I'm the other shop. You can. Ask her for a blade-test and see if they're as good as the paint says."],
      { :choice => "Test the swords at EXCELLENT SWORDS?", :options => [
          ["I'll test them.", [{ :accept => true }, [:ADEQUATE, :happy, "Ha! Be honest about it. That's the only rule. Well. That and don't get cut."]]],
          ["Are your swords any good?", [[:ADEQUATE, :neutral, "They're adequate. It says so on the sign. I'd be arrested otherwise."],
                                         [:ADEQUATE, :neutral, "Ask me again when you'll do the test."]]]] }
    ],
    :test => [
      [:KESSA, :neutral, "A blade-test? From HIM? ...Fine. Sharpness rules: my blades against your team. The last edge still standing decides."],
      [:KESSA, :smug, "If my swords are only adequate, I'll paint the sign over myself. In front of everyone. In beige."],
      { :trainer => [:CRUSHGIRL, "Kessa", 50], :field => :VOLCANIC,
        :won => [
          [:KESSA, :shocked, "...You beat my blades. That's not the test, mind. The test is whether they're sharp."],
          "You look at her Honedge's edge. You look at Doublade's. You have never seen steel this good. You don't know much about steel, and you can still tell.",
          [:KESSA, :neutral, "Well? Say true. The Honest Court will ask you the same thing, word for word."],
          { :step => :court },
          [:KESSA, :happy, "Off you go, then. The Hall of Oaths, up at Pyre Keep. The Oath-Scribe hears shop cases. He has a whole plinth for the word 'excellent'."]],
        :lost => [
          [:KESSA, :smug, "Sharp enough for you? Heal up and test them again. Honest work takes as long as it takes."]] }
    ],
    :court => [
      [:SCRIBE, :neutral, "A shop case. ADEQUATE against EXCELLENT. My nine hundred and forty-first 'excellent'. Witness, the oath first."],
      [:SCRIBE, :neutral, "Say true or say nothing. Are the swords of EXCELLENT SWORDS excellent?"],
      { :choice => "What do you swear?", :options => [
          ["They're excellent.", [
             [:SCRIBE, :neutral, "Then the sign is true and stays up. EXCELLENT SWORDS is excellent. Recorded."],
             [:SCRIBE, :neutral, "And ADEQUATE SWORDS? Also true. Two honest shops on one lane. That almost never happens."],
             { :flag => [:verdict, :excellent] }]],
          ["They're adequate.", [
             "The brazier in the middle of the hall spits once, loudly, and everyone in the hall turns to look at you.",
             [:SCRIBE, :deadpan, "The flame disagrees. So does my ledger: you beat her blades and you held them up to the light. Try again."],
             [:SCRIBE, :neutral, "Are they excellent?"],
             { :choice => "...", :options => [["They're excellent.", [[:SCRIBE, :neutral, "Recorded. The sign stays up. No fine for the first try; everyone flinches once."],
                                                                     { :flag => [:verdict, :excellent] }]]] }]]] },
      { :step => :home },
      [:SCRIBE, :neutral, "Go and tell the plaintiff. Gently. They always take it hard."]
    ],
    :home => [
      [:ADEQUATE, :sad, "Excellent. Really excellent? ...The court said so?"],
      [:ADEQUATE, :neutral, "Then she's not lying. Then I'm not the only honest shop on the lane. Then I've been glaring at an honest woman for a week."],
      { :map => "He takes a chisel off the bench, goes out to his sign, and cuts two new words under the old ones. It takes a while. He looks happier with every stroke." },
      [:ADEQUATE, :happy, "There. ADEQUATE SWORDS. (STILL.) A sign that's true twice. Take this. Keeps an edge, keeps a promise."],
      { :complete => true },
      [:ADEQUATE, :happy, "I'm going to buy one of hers. For the shop. To remind me what excellent looks like."]
    ],
    :after => [
      [:ADEQUATE, :happy, "ADEQUATE SWORDS (STILL). Business is up. People trust a shop that loses honestly."]
    ],
    :sign => [
      "ADEQUATE SWORDS. And under it, freshly cut: (STILL.)"
    ],
    :kessa_after => [
      [:KESSA, :happy, "He bought one of my swords. He's hung it over his counter with a little card: EXCELLENT. (NOT MINE.)"]
    ]
  }
})

#===============================================================================
# Seven Bouts (Ch8, the Crucible on 240)
#===============================================================================
# Seven back-to-back bouts on the caldera floor: no healing between them, and the bag stays shut (noBagItems). The
# Crucible's sand ring is :VOLCANIC (the Volcanic field has no stages, so the "heat rising" is the Herald's), bout 4
# is a double, bout 7 is the Legate's adjutant on a Dragon's Den preview. The Saltmere barge's paper (AS_LITTLE_CRUCIBLE
# flag :recruited) counts as bout 1. Losing any bout sends you back to the start; nothing is lost but the afternoon.
noitems = { :script => proc { |_ctx| setBattleRule("noBagItems") } }
tr.quest(:AS_SEVEN_BOUTS, {
  :trial => :ASHKAAR, :title => "Seven Bouts", :giver => "Legate Varra Kosk", :map => 240, :where => "the Crucible, Cindervault",
  :rank => 1, :points => 4, :rec_level => 38, :chapter => 8, :unlock => "badges >= 6", :board => true, :tags => [:arena, :gauntlet],
  :summary => "The Crucible's entry rite: seven legion fighters, back to back, on the caldera floor. No items. No healing. No complaining.",
  :steps => { :bouts => "Win seven bouts in a row on the Crucible floor (no healing, no bag).",
              :brand => "Receive your brand from the Legate." },
  :reward => { :items => [[:CHARCOAL, 1], [:FIRESTONE, 1]] },
  :touches => "Ashkaar recruitment flag from the Saltmere barge is honoured here (skip bout 1)",
  :design => "Volcanic field; bout 4 is a double; bout 7 is the Legate's adjutant on a Dragon's Den preview. The Herald introduces you with whatever the Saltmere barge called you.",
  :scenes => {
    :offer => [
      [:KOSK, :neutral, "The Crucible's rite is seven bouts. Seven of the Legion, one after another, on the caldera floor."],
      [:KOSK, :neutral, "No potions. No healing between. Nobody complains, because complaining is a statement and statements here are under oath."],
      { :if => "quest_flag(:AS_LITTLE_CRUCIBLE, :recruited)", :then => [
          [:KOSK, :smug, "You signed Brakka's paper on the Saltmere barge. Ember-recruit. That's one bout fought already, in my book."]] },
      { :choice => "Take the Crucible's rite?", :options => [
          ["Seven bouts. Now.", [{ :accept => true }, [:KOSK, :neutral, "Herald. Ring the sand."], { :run => :start }]],
          ["Not yet.", [[:KOSK, :neutral, "An honest 'not yet'. The sand will keep."]]]] }
    ],
    :again => [
      [:KOSK, :neutral, "Back for the rite. From the first bout, then. The sand doesn't remember who it nearly beat."],
      { :choice => "Fight the seven bouts?", :options => [
          ["Ring the sand.", [{ :run => :start }]],
          ["Not yet.", [[:KOSK, :neutral, "Then rest. Honestly."]]]] }
    ],
    :start => [
      { :if => "quest_flag(:AS_LITTLE_CRUCIBLE, :recruited)", :then => [
          [:CRUCIBLE_HERALD, :happy, "ON THE SAND! SIGNED ON THE SALTMERE BARGE, BRANDED BY SERGEANT BRAKKA HERSELF: EMBER-RECRUIT \\PN!"],
          [:CRUCIBLE_HERALD, :neutral, "The barge's paper is honoured. Bout one is FOUGHT. To bout two!"],
          { :run => :bout2 }],
        :else => [
          [:CRUCIBLE_HERALD, :happy, "ON THE SAND! FROM ELOWEN, WITH A WARDEN'S BADGES AND NOBODY'S PAPERS: CHALLENGER \\PN!"],
          { :run => :bout1 }] }
    ],
    :bout1 => [
      [:CRUCIBLE_HERALD, :happy, "BOUT ONE! Recruit Orrin! He's been waiting all morning and he's said so, under oath, four times!"],
      noitems,
      { :trainer => [:ASHKAAR_SOLDIER_M, "Orrin", 50], :field => :VOLCANIC,
        :won => [{ :run => :bout2 }], :lost => [{ :run => :fell }] }
    ],
    :bout2 => [
      [:CRUCIBLE_HERALD, :happy, "BOUT TWO! Legionnaire Tavi! Three years on the Pyre Road, and she's never once said she enjoyed it!"],
      noitems,
      { :trainer => [:ASHKAAR_SOLDIER_F, "Tavi", 50], :field => :VOLCANIC,
        :won => [{ :run => :bout3 }], :lost => [{ :run => :fell }] }
    ],
    :bout3 => [
      [:CRUCIBLE_HERALD, :happy, "BOUT THREE! Hollen of the Slag Ward! The sand's warm now! Hollen's warmer!"],
      noitems,
      { :trainer => [:ASHKAAR_SOLDIER_M, "Hollen", 50], :field => :VOLCANIC,
        :won => [{ :run => :bout4 }], :lost => [{ :run => :fell }] }
    ],
    :bout4 => [
      [:CRUCIBLE_HERALD, :happy, "BOUT FOUR, AND IT'S A DOUBLE! Ember-rider Ilka brings two at once! She says it's fair! It is, technically!"],
      noitems,
      { :trainer => [:ASHKAAR_EMBER_RIDER, "Ilka", 50], :field => :VOLCANIC, :double => true,
        :won => [{ :run => :bout5 }], :lost => [{ :run => :fell }] }
    ],
    :bout5 => [
      [:CRUCIBLE_HERALD, :happy, "BOUT FIVE! Legionnaire Senna! She asked to be fifth! She says the fifth bout is where people start lying to themselves!"],
      noitems,
      { :trainer => [:ASHKAAR_SOLDIER_F, "Senna", 50], :field => :VOLCANIC,
        :won => [{ :run => :bout6 }], :lost => [{ :run => :fell }] }
    ],
    :bout6 => [
      [:CRUCIBLE_HERALD, :happy, "BOUT SIX! Rusk the Quiet! He hasn't said a word since the Pyre Road! Nobody's sure if that's an oath or a cold!"],
      noitems,
      { :trainer => [:ASHKAAR_SOLDIER_M, "Rusk", 50], :field => :VOLCANIC,
        :won => [{ :run => :bout7 }], :lost => [{ :run => :fell }] }
    ],
    :bout7 => [
      { :map => "The Herald lowers the brazier-screens. The sand ring's heat changes: dry and old, like the inside of a dragon's den." },
      [:CRUCIBLE_HERALD, :neutral, "BOUT SEVEN. The Legate's adjutant, Captain Corran. On the Den's own ground."],
      [:KOSK, :neutral, "Corran fights the way Wyrmrest fights. Consider it a preview. Consider it a courtesy."],
      noitems,
      { :trainer => [:ASHKAAR_OFFICER, "Corran", 50], :field => :DRAGONS_DEN,
        :won => [{ :step => :brand }, { :run => :brand }], :lost => [{ :run => :fell }] }
    ],
    :fell => [
      [:CRUCIBLE_HERALD, :neutral, "DOWN! On the sand, honestly! The Crucible thanks the challenger!"],
      [:KOSK, :neutral, "No shame in it. Some shame in it. The rite starts again from the first bout whenever you're ready."]
    ],
    :brand => [
      [:CRUCIBLE_HERALD, :happy, "SEVEN! SEVEN FOR SEVEN! RING THE SAND!"],
      [:KOSK, :neutral, "Seven bouts. No bag, no rest. And you didn't complain once, which I'm told is rarer than the winning."],
      { :map => "The Legate heats a small iron in the brazier and presses it, briefly, to the leather of your bag strap. It smells of hot leather and something like pride." },
      [:KOSK, :neutral, "The Crucible's brand. Legion fighters will step aside for it on the Pyre Road. Some of them will want to fight you for it. Let them."],
      { :heal => true },
      { :complete => true }
    ],
    :after => [
      [:KOSK, :neutral, "Branded on my sand. If you ever want the higher writs, they're on the Herald's board in the Hall of Oaths."],
      { :flag => [:told, true] }
    ]
  }
})

#===============================================================================
# The Trial of Truth (Ch8, the Hall of Oaths on 247)
#===============================================================================
# After "Whose Is It" (244, CH8_STEP 7): the PC heard Envoy Haskar say it in the Hall: "The Dominar told me to take it
# while everyone was looking at the mountain." Here a Legion officer swears the opposite before the Great Oath-Brazier.
# Ashkaar judges a lie by combat: contradict him and you fight for your word on the caldera's own field. Silence is
# honoured (no reward, no shame); agreeing with him is a lie, and lying in the Hall ends the case against you.
tr.quest(:AS_TRIAL_OF_TRUTH, {
  :trial => :ASHKAAR, :title => "The Trial of Truth", :giver => "Herald Pyke", :map => 247,
  :where => "the Hall of Oaths, Pyre Keep", :rank => 3, :points => 4, :rec_level => 41, :chapter => 8,
  :unlock => "badges >= 6 && switch(120) && var(129) >= 7", :board => true, :tags => [:battle, :moral, :honesty],
  :summary => "Ashkaar judges a lie by combat. A Legion officer swears that on the night of the caldera crisis the Dominion's hands were clean. You were there.",
  :steps => { :testify => "Testify before the Great Oath-Brazier in the Hall of Oaths.",
              :duel => "Your word contradicts Tribune Halden's. Defend it in the Hall, under oath rules." },
  :reward => { :items => [[:FLAMEORB, 1]] },
  :outcomes => { :silent => { :replace => true } },              # silence is honoured: the points, not the orb
  :touches => "Caldera result (V110) and the Light Stone (:ch8_lightstone); Ashkaar war politics (S121)",
  :design => "Whatever you say is a choice with consequences; contradicting the officer starts an ASHKAAR_OFFICER duel on :VOLCANIC under 'oath rules'. Win and the Legion admits the Dominar's order publicly, which nobody in the hall has seen before.",
  :scenes => {
    :offer => [
      [:PYKE, :neutral, "The Dominion convenes a Trial of Truth. Tribune Halden of the Legion has sworn an oath about the night of the five bells."],
      [:PYKE, :neutral, "Every witness who was in Cindervault that night may answer it. You were in Cindervault that night."],
      [:PYKE, :neutral, "Say true, or say nothing. Both are honoured here. Lying is not."],
      { :choice => "Testify before the brazier?", :options => [
          ["I'll testify.", [{ :accept => true }, { :run => :testify }]],
          ["Not today.", [[:PYKE, :neutral, "The Trial waits. Oaths keep in this hall; it's the only place they do."]]]] }
    ],
    :testify => [
      { :map => "The Great Oath-Brazier. Tribune Halden stands at it with one palm on the bronze, in red lacquer, very still. The hall is full and very quiet." },
      [:HALDEN, :neutral, "I swear by the flame: on the night of the five bells, the Dominion's hands were clean."],
      [:HALDEN, :neutral, "The Meridian put a pipe in our fire. The Hollow poured a lake on it. The Envoy guarded the Light Stone while the city burned, as a friend guards a friend's house."],
      { :if => "var(110) == 1", :then => [[:HALDEN, :neutral, "Cindervault's forges are cold. That is the Hollow's doing and Zenith's. Not ours."]] },
      { :if => "var(110) == 2", :then => [[:HALDEN, :neutral, "Zenith has bound the Flame with brass and calls it mended. That is Zenith's doing. Not ours."]] },
      { :if => "var(110) == 0", :then => [[:HALDEN, :neutral, "A child shut Zenith's tap with their own hands. The Dominion honours it. The Dominion also had no part in what came before."]] },
      [:PYKE, :neutral, "Witness. You were in the Hearthguild Hall that night. Does his oath stand?"],
      { :choice => "What do you say?", :options => [
          ["Haskar said the Dominar told him to take it.", [
             [:PYKE, :neutral, "...Say it again, for the scribe. Exactly."],
             "You say it exactly: 'The Dominar told me to take it while everyone was looking at the mountain.' Envoy Haskar's words, to Sigrun, in front of Brann.",
             "The hall makes a sound like a held breath. Tribune Halden takes his palm off the bronze.",
             [:HALDEN, :angry, "Then your word and mine can't both stand at this fire. In Ashkaar that's settled the old way."],
             [:PYKE, :neutral, "Oath rules. Steel decides which word stands. Lose, and his oath stands. Win, and the Legion answers for it."],
             { :step => :duel }, { :run => :duel }]],
          ["I was down at the tap. I'll say nothing.", [
             [:PYKE, :neutral, "Say true or say nothing. You said nothing. That is honoured in this hall."],
             [:HALDEN, :neutral, "Then my oath stands."],
             [:PYKE, :neutral, "It stands because nobody answered it. That's not the same as true. The Trial is closed."],
             { :complete => :silent }]],
          ["His oath is true.", [
             "The brazier in the middle of the hall roars up and spits a long tongue of fire straight at the vault.",
             [:PYKE, :angry, "The flame says otherwise. You were in that hall. You heard the Envoy."],
             [:PYKE, :neutral, "A witness who lies at the fire is struck from the Trial. Go. Your word is worth nothing here today."],
             { :fail => true }]]] }
    ],
    :duel => [
      { :map => "Tribune Halden steps back from the brazier onto the hall's open floor. The crowd draws back to the plinths." },
      [:HALDEN, :neutral, "Under oath rules. No speeches. Just steel."],
      { :trainer => [:ASHKAAR_OFFICER, "Halden", 50], :field => :VOLCANIC,
        :won => [
          "Tribune Halden looks at his last Pokémon for a long moment. Then he walks back to the brazier and puts his palm on the bronze again.",
          [:HALDEN, :sad, "I withdraw my oath. The Envoy took the Light Stone because the Dominar ordered it, while the city burned. The Legion knew."],
          "Nobody in the hall moves. Somewhere in the gallery, an old legionnaire starts to clap, very slowly, and stops because nobody joins in.",
          [:PYKE, :neutral, "Recorded. The Legion has admitted fault before the flame. I have kept this hall for thirty years. I have never written that line."],
          [:PYKE, :neutral, "The Dominion thanks the witness. It will not like you for it. Those are different things here."],
          { :complete => true }],
        :lost => [
          [:HALDEN, :neutral, "My oath stands. Not because it's true. Because you lost."],
          [:PYKE, :neutral, "That is the law, and it's an ugly one today. The Trial stays open. Come back and answer him again."]] }
    ],
    :after => [
      [:PYKE, :neutral, "Halden's withdrawn oath is on the fourth plinth now. People come up from the terraces to read it."],
      { :flag => [:told, true] }
    ]
  }
})

#===============================================================================
# Afraid of Heights (Ch8, the Dragon Roosts on 248: Gemini's Recruit Tamm and his Trapinch)
#===============================================================================
# The catalogue's "Trapinch as a guest in your party" needs a guest mechanic the Trials don't have; here you train it
# the Ashkaar way, by sparring it three times on the roost floor (it grows each time; the third spar it is a Vibrava).
tr.quest(:AS_AFRAID_OF_HEIGHTS, {
  :trial => :ASHKAAR, :title => "Afraid of Heights", :giver => "Recruit Tamm", :map => 248, :where => "the Dragon Roosts, Pyre Keep",
  :rank => 2, :points => 3, :rec_level => 40, :chapter => 8, :unlock => "badges >= 6", :board => true,
  :tags => [:comedy, :training, :event_mon],
  :summary => "A dragon-rider recruit is afraid of heights and has been assigned a Trapinch 'until he's ready'. He has been not-ready for two years.",
  :steps => { :train => "Spar with Tamm's Trapinch on the roost floor until it's ready (three spars).",
              :flight => "Vibrava wants to fly. Tamm does not." },
  :reward => { :pokemon => :AS_NOIBAT },
  :touches => "15_COMEDY Ashkaar bit; story/29 line 98 ('I'm afraid of heights. They don't know.')",
  :design => "Three spars with Tamm's Trapinch (Lv 34, 35, then a Vibrava at 36). When it becomes a Vibrava it takes Tamm three feet off the ground and he screams with joy. He gives you the Noibat he was also assigned, because 'it looks at me like it knows'.",
  :scenes => {
    :offer => [
      [:TAMM, :sad, "You know. Everyone knows. I told the Roost-mistress myself; I can't lie, it's the law, it's AWFUL."],
      [:TAMM, :neutral, "They gave me Grit until I'm 'ready'. Grit's a Trapinch. Trapinch don't fly. Neither do I. It's been two years."],
      [:TAMM, :neutral, "The Roost-mistress says a Trapinch gets its wings by fighting. If you spar with Grit... maybe one of us gets ready."],
      { :choice => "Spar with Tamm's Trapinch?", :options => [
          ["Let's train Grit.", [{ :accept => true }, [:TAMM, :happy, "Really? Grit! Grit, we're TRAINING! ...Oh no. Oh no, that means flying eventually."],
                                { :run => :spar }]],
          ["Not now.", [[:TAMM, :neutral, "That's fine. Honestly fine. I'll be here. On the ground."]]]] }
    ],
    :spar => [
      { :if => "quest_count(:SELF, :spars) >= 2", :then => [
          [:TAMM, :neutral, "Third spar. Grit's been glowing at the edges since breakfast. I'm choosing not to think about it."],
          { :trainer => [:ASHKAAR_SOLDIER_M, "Tamm", 52], :field => :DRAGONS_DEN,
            :won => [{ :count => [:spars, 1] }, { :step => :flight }, { :run => :flight }],
            :lost => [[:TAMM, :happy, "We WON? Grit, we won! ...Don't tell anyone. No, wait, I have to. It's the law."]] }],
        :else => [
          { :if => "quest_count(:SELF, :spars) == 1", :then => [
              [:TAMM, :neutral, "Again? Grit's ready. Grit's always ready. It's me that's the problem."],
              { :trainer => [:ASHKAAR_SOLDIER_M, "Tamm", 51], :field => :DRAGONS_DEN,
                :won => [{ :count => [:spars, 1] }, [:TAMM, :happy, "Did you see that? Grit jumped! Almost a foot! That's practically altitude."]],
                :lost => [[:TAMM, :shocked, "Grit won? Grit WON. I'm going to need a minute."]] }],
            :else => [
              { :trainer => [:ASHKAAR_SOLDIER_M, "Tamm", 50], :field => :DRAGONS_DEN,
                :won => [{ :count => [:spars, 1] }, [:TAMM, :neutral, "That's one. Grit's not even upset. Grit likes you. Come back when you can; we'll be here. Low down."]],
                :lost => [[:TAMM, :happy, "Grit! You did it! ...Sorry. That was a spar. We're supposed to be helping each other."]] }] }] }
    ],
    :flight => [
      { :map => "Grit glows white. When the light goes, a green-winged Vibrava is buzzing in the air, delighted with itself. It grabs Tamm's collar." },
      "The Vibrava lifts Recruit Tamm three feet off the roost floor. He screams. It's the happiest scream you've ever heard.",
      [:TAMM, :crying, "I'M FLYING. I'M THREE FEET UP. THIS IS THE WORST AND BEST DAY OF MY LIFE."],
      { :map => "Grit puts him down. He sits on the floor for a while. A Noibat drops off a rafter and lands on his head." },
      [:TAMM, :neutral, "They assigned me this one too. For 'when I'm ready'. It keeps looking at me like it knows. It knows I'm not."],
      [:TAMM, :happy, "You take it. You're ready. It looks at you like it knows that too."],
      { :complete => true }
    ],
    :after => [
      [:TAMM, :happy, "Grit and I go up every morning now. Three feet. Then four. The Roost-mistress says by spring I'll be a rider. I said that's a lie. She said it's a forecast."],
      { :flag => [:told, true] }
    ]
  }
})
tr::SPEAKERS.merge!({ :TAMM => "Recruit Tamm" })
