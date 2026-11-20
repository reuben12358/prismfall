#===============================================================================
# Prismfall Trials - 114 Mega Evolution: the Ring-Day and the stone quests
# (SPINE Revision 20; design/MEGA_EVOLUTION.md). Written by the battle-mechanics
# workstream; the stones' badge gates are checked by tools/harness/run_mega.rb.
#-------------------------------------------------------------------------------
# Lore (MEGA_EVOLUTION.md section 1): a Mega Stone is a "heartstone", an Imprint
# that has pearled inside one line of Pokemon. A Mega Ring is a Warden's ring: a
# fleck of the Crown's stone (Legend Plate grind, saved by the Hearthguild every
# time the stone is reset) in a gold band. Every type and none, so it opens any
# heartstone. One ring opens one heart at a time: one Mega to a side.
# Map events: design/TRIAL_EVENTS.yaml ("Mega Evolution" maps); talk rows: 152_Talk_Megas.rb; bosses:
# 132_EventMons_Megas.rb. Story quests (the Ring-Day, Juno, Brann's spare) are
# hidden and finish quietly (no Trial gong).
#===============================================================================
tr = Prismfall::Trials
tr::SPEAKERS.merge!({
  :BRANN => "Brann", :SAHAR => "Sahar", :DORIAN => "Dorian", :WENLOW => "Wenlow", :CORVIN => "Corvin",
  :TARN => "Roost-keeper Tarn", :POSTMASTER => "Postmaster Halloran", :WOODWARD => "The Woodward",
  :KENNELMASTER => "Kennel-master Grisk", :KAITO => "Kaito"
})
# Shown after a stone while the player has no Mega Ring yet (same words as PrismfallMega::TEASER_TEXT).
mega_teaser = { :if => "!mega_ring", :then => ["The stone is warm, and it hums faintly in your hand... then goes quiet, as if it were waiting for something."] }

#===============================================================================
# THE RING-DAY (Chapter 8, Cindervault, after Gym 7 and the Caldera Crisis)
#===============================================================================
tr.quest(:AS_RING_DAY, {
  :trial => :ASHKAAR, :title => "The Ring-Day", :giver => "Brann Holloway", :map => 244,
  :where => "the Hearthguild Hall, Cindervault (the morning after the Caldera Crisis)", :points => 0, :chapter => 8,
  :unlock => "badges >= 7 && made(:ch8_caldera) && !mega_ring", :board => false, :hidden => true, :tags => [:story, :mega],
  :summary => "Brann has something for you at the Hearthguild Hall.",
  :steps => { :ask => "Brann is waiting at the Hearthguild's anvil." },
  :reward => { :items => [[:MEGARING, 1], [:AGGRONITE, 1]] },
  :touches => "Gives the Mega Ring (Mega Evolution opens) and the Aggronite. Foreshadows the PC's splinter: the ring sings.",
  :scenes => {
    :ringday => [
      { :map => "Morning. Brann stands at the guild's great anvil with a folded cloth. Larch sits on a crate by the door, pretending to read." },
      { :if => "choice(:ch8_caldera) == :vent", :then => [
          { :map => "The great forge is cold. One candle-forge burns on the anvil." },
          [:BRANN, :sad, "Forge is cold for a season, thanks to you lot. Don't look like that. A ring wants a candle, not a caldera."]] },
      { :if => "choice(:ch8_caldera) == :dampers", :then => [
          [:BRANN, :happy, "Hear that? My forges, still singing. You kept 'em lit. I won't forget it."]] },
      { :if => "choice(:ch8_caldera) == :shutdown", :then => [
          [:BRANN, :happy, "You shut a Meridian tap with your own two hands. The Dominar's still talking about it. So am I."]] },
      [:BRANN, :worried, "About last night. The chestnuts. A fool talks too much over chestnuts. Forget the fool."],
      [:BRANN, :neutral, "Here's what a sober man says instead. Hold out your hand."],
      "He opens the cloth: a plain gold band, and set in it a chip of stone with no colour at all.",
      [:BRANN, :neutral, "A Warden's ring. Mega Ring, the Accord calls it. The guild's cut one for every seat since the Concordance."],
      [:BRANN, :neutral, "The chip is grind. Dust off the Crown's own stone, kept every time it's reset. The Legend Plate's every type and none, so a fleck of it opens any heartstone."],
      [:BRANN, :neutral, "Heartstones. Mega Stones, if you're Accord. Where an Imprint soaks into one kind of Pokemon long enough, it pearls. Your partner holds the stone, you wear the ring, and for one fight it carries its whole Imprint."],
      [:BRANN, :deadpan, "One heart at a time, mind. Two rings on the same side ring against each other. One Mega to a side, always. Remember it in a double."],
      "He sets the ring in your palm. The colourless chip catches the forge-light... and sings: one clear note, like a struck glass.",
      "Somewhere under your ribs, something answers it.",
      [:BRANN, :shocked, "..."],
      [:BRANN, :sad, "They don't sing. Thirty years at this anvil, and not one of them has ever sung."],
      { :map => "Larch has lowered her book." },
      [:BRANN, :worried, "...Old fool. It's the forge-hum. Here: an iron heart to start you off. Aron burrow under the Brinecut cliffs. Raise one into an Aggron and it'll know what to do."],
      { :script => proc { |_ctx| Prismfall::Trials.complete(:AS_RING_DAY, nil, false) } },
      { :if => "mega_stones > 1", :then => ["The other stones in your Bag are warm now, and quiet, as if they had stopped waiting."] },
      [:BRANN, :happy, "Now. Go and show Kaito what a ferry child does with a Warden's ring."]
    ]
  }
})

# Act III return (10 badges): Brann's spare heartstone, the twin of his own Camerupt's.
tr.quest(:AS_FORGE_REMEMBERS, {
  :trial => :ASHKAAR, :title => "The Forge Remembers", :giver => "Brann Holloway", :map => 244,
  :where => "the Hearthguild Hall, Cindervault (Act III)", :points => 0, :chapter => 12,
  :unlock => "badges >= 10 && quest_done(:AS_RING_DAY)", :requires => [:AS_RING_DAY], :board => false, :hidden => true,
  :tags => [:story, :mega], :summary => "Brann found something in the slag.",
  :steps => { :ask => "Brann wants a word at the Hearthguild." },
  :reward => { :items => [[:CAMERUPTITE, 1]] },
  :scenes => {
    :spare => [
      [:BRANN, :happy, "There you are! War on the doorstep and you still come by. Sit. No, not there, that's hot."],
      [:BRANN, :neutral, "You remember Cinder, my Camerupt? The one that tried to erupt on you."],
      [:BRANN, :neutral, "Every heartstone's got a twin somewhere. Hers turned up in the slag this spring, still warm. The caldera makes them like other mountains make gravel."],
      [:BRANN, :smug, "I'd give it to a Warden. You'll do better than most Wardens."],
      { :script => proc { |_ctx| Prismfall::Trials.complete(:AS_FORGE_REMEMBERS, nil, false) } },
      [:BRANN, :deadpan, "Your ring still singing? ...No. Don't tell me. I sleep badly enough."]
    ]
  }
})

#===============================================================================
# ELOWEN - the Quiet Way
#===============================================================================
# Before the Ring (3 badges): the lamp lens Morwen set in the Ferrow lighthouse.
tr.quest(:EL_LAMP_LENS, {
  :trial => :ELOWEN, :title => "The Humming Lamp", :giver => "Hesper Vane", :map => 106,
  :where => "the Ferrow Lighthouse lamp room", :rank => 1, :points => 1, :rec_level => 23, :chapter => 5,
  :unlock => "badges >= 3", :board => true, :tags => [:mega, :kindness],
  :summary => "A paper lantern from the lighthouse: 'THE LAMP HUMS. MAKE IT STOP. - H.V.'",
  :steps => { :ask => "Hesper's lamp hums at night. Look behind the great lens." },
  :reward => { :items => [[:AMPHAROSITE, 1]] },
  :touches => "Kestrel's family: Morwen set the stone; it hums for the PC.",
  :scenes => {
    :offer => [
      [:HESPER, :deadpan, "You again. The lamp's been humming every night since you came back down the coast. Like a kettle that won't boil."],
      [:HESPER, :neutral, "My daughter set a stone in the lens when she was a girl. Lumen lamp-glass, she said. An Ampharos's heart. It never made a sound in thirty years."],
      { :choice => "Look behind the lens?", :options => [
          ["Look.", [
             { :accept => true },
             "Behind the great lens, a yellow stone sits in a brass claw. When you lean close, the hum climbs a note.",
             [:HESPER, :shocked, "...It's you it's humming at."],
             [:HESPER, :deadpan, "Take it. Take it out of my lamp before it hums me into the sea. Some Warden down the road can tell you what it's for. I won't."],
             { :complete => true }, mega_teaser,
             [:HESPER, :sad, "Morwen's ring used to make it glow. I'd forgotten that."]]],
          ["Not now.", [[:HESPER, :deadpan, "Then don't stand in my light."]]]] }
    ]
  }
})

# 9 badges: Juno, the new Grass Warden, after J3 (the Bride Tree's heartstone).
tr.quest(:EL_BRIDE_TREE_HEART, {
  :trial => :ELOWEN, :title => "The Bride Tree's Heart", :giver => "Juno Hale", :map => 294,
  :where => "the Heartgarden, Verdance, under the Bride Tree (after J3)", :points => 0, :chapter => 11,
  :unlock => "badges >= 9", :board => false, :hidden => true, :tags => [:story, :mega],
  :summary => "Juno is waiting under the Bride Tree.",
  :steps => { :ask => "Juno is under the Bride Tree." },
  :reward => { :items => [[:VENUSAURITE, 1]] },
  :touches => "Sets up J4: the Grass Warden's ring won't answer Juno yet.",
  :scenes => {
    :heart => [
      [:JUNO, :happy, "You came! Sit, sit. Mind the roots, they've got opinions."],
      [:JUNO, :neutral, "Uncle Rowan kept a seed-tin in the potting shed. Label says NOT SEEDS. Guess what was in it."],
      "She opens her hand: a stone the green of new leaves, with a pink flower caught inside it.",
      [:JUNO, :neutral, "It grew in the Bride Tree's roots. A Venusaur's heart, the Order says. The tree's been in bloom for forty years. I suppose it had to put the extra somewhere."],
      [:JUNO, :sad, "He left me his ring, too. The Grass Warden's ring. It won't answer me. I hold it and it's just... his."],
      [:JUNO, :happy, "Yours sings, though. Don't look at me like that, I can hear it from here. So you take the stone. Somebody should."],
      { :script => proc { |_ctx| Prismfall::Trials.complete(:EL_BRIDE_TREE_HEART, nil, false) } },
      [:JUNO, :happy, "And next time we fight, I'll have the ring talking to me. You'll see. Probably. Hopefully."]
    ]
  }
})

# 9 badges: the doll in the Thistledown attic (Banettite).
tr.quest(:EL_DOLL_WHO_WAITED, {
  :trial => :ELOWEN, :title => "The Doll Who Waited", :giver => "A doll in the attic", :map => 547,
  :where => "Thistledown Manor attic", :rank => 1, :points => 2, :rec_level => 50, :chapter => 11,
  :unlock => "badges >= 9", :board => true, :tags => [:mega, :ghost, :kindness],
  :summary => "A lantern with a child's scrawl: 'SOMETHING KNOCKS IN THE THISTLEDOWN ATTIC. IT WANTS ITS BUTTONS.'",
  :steps => { :ask => "Something knocks in the Thistledown Manor attic.",
              :buttons => "The doll's three buttons are somewhere in the manor.",
              :return => "You have all three buttons. Take them back to the attic." },
  :reward => { :items => [[:BANETTITE, 1]] },
  :scenes => {
    :offer => [
      "In the attic dust sits a rag doll with a zipped mouth and no buttons for eyes. As you step closer, it turns its head toward you. Knock. Knock. Knock.",
      { :choice => "The doll waits.", :options => [
          ["Find its buttons.", [{ :accept => true }, { :step => :buttons },
             "The doll's head tilts. Downstairs, something small rolls across a floorboard."]],
          ["Back away slowly.", ["The doll keeps watching you all the way down the stairs."]]] }
    ],
    :button => [
      { :count => [:buttons, 1] },
      "A black button, the size of a coin, still warm.",
      { :if => "quest_count(:SELF, :buttons) >= 3", :then => [{ :step => :return }, "That's three. Upstairs, the knocking has stopped."] }
    ],
    :return => [
      "You press the buttons on. The doll blinks. It looks at the attic window, at the road below, for a long time.",
      "Then it lets go of something it has held for a very long time: a grey stone drops from its stitched hands into yours.",
      { :complete => true },
      "When you look back, it is only a doll, sitting in the sun."
    ]
  }
})

# 12 badges: the Old Pincer of the Gossamer Heartwood (boss).
tr.quest(:EL_OLD_PINCER, {
  :trial => :ELOWEN, :title => "The Old Pincer", :giver => "the Woodward", :map => 526,
  :where => "the Woodward's Hut, Gossamer Wood; the fight is in the Gossamer Heartwood", :rank => 2, :points => 3,
  :rec_level => 62, :chapter => 14, :unlock => "badges >= 12", :board => true, :tags => [:mega, :boss],
  :summary => "A lantern from the Woodward: 'THE OLD PINCER HAS TAKEN THE HEARTWOOD SAP. BRING SOMEONE STRONG.'",
  :steps => { :ask => "The Woodward wants the Old Pincer out of the Heartwood's sap tree.",
              :fight => "Face the Old Pincer at the sap tree in the Gossamer Heartwood." },
  :reward => { :items => [[:PINSIRITE, 1]] },
  :scenes => {
    :offer => [
      [:WOODWARD, :neutral, "There's a Pinsir in the Heartwood older than my hut. Old Pincer, we call it. This spring it took the great sap tree and nothing gets near it."],
      [:WOODWARD, :worried, "The silk-moths need that sap. So does the Loomhouse. I'd ask a Warden, but the Wardens are busy being at war."],
      { :choice => "Take on the Old Pincer?", :options => [
          ["I'll go.", [{ :accept => true }, { :step => :fight }, [:WOODWARD, :happy, "Bless you. Bring a Fire type. Bring two."]]],
          ["Not yet.", [[:WOODWARD, :neutral, "It's not going anywhere. That's the problem."]]]] }
    ],
    :fight => [
      "The sap tree weeps amber. Wrapped around its trunk, a Pinsir the size of a cart clacks its horns at you.",
      { :event_battle => :EL_OLD_PINCER,
        :won => ["The Old Pincer lets go of the trunk and sits down heavily in the moss. Something drops from between its horns: a stone the brown of old bark.",
                 "It watches you pick it up, then wanders off into the Heartwood to sleep.",
                 { :complete => true }],
        :lost => ["The Old Pincer clacks once, satisfied, and wraps itself around the tree again."] }
    ]
  }
})

# 16 badges: Dorian's encore at the Pell Playhouse (Lopunnite).
tr.quest(:EL_ENCORE, {
  :trial => :ELOWEN, :title => "Encore", :giver => "Dorian Pell", :map => 154,
  :where => "the Grand Stage, Pell Playhouse, Saltmere", :rank => 1, :points => 2, :rec_level => 80, :chapter => 18,
  :unlock => "badges >= 16", :board => true, :tags => [:mega, :comedy],
  :summary => "A gilt-edged lantern: 'ONE NIGHT ONLY. THE PLAYHOUSE REQUIRES A STAR. - D.P.'",
  :steps => { :ask => "Dorian needs a star for one last show before the Festival." },
  :reward => { :items => [[:LOPUNNITE, 1]] },
  :scenes => {
    :offer => [
      [:DORIAN, :happy, "Enter, stage left, our returning hero! Sixteen badges! Darling, you've been practically everywhere. Saltmere is so proud. I am so proud. I've had posters made."],
      [:DORIAN, :neutral, "One last show before the Festival. My leading lady retired, and the house wants a closing number. You. A spotlight. A Pokemon. Something unforgettable."],
      { :accept => true },
      { :choice => "Your closing number?", :options => [
          ["A dance.", [[:DORIAN, :happy, "A dance! Bold! Ancient! The audience weeps!"]]],
          ["A fight scene.", [[:DORIAN, :happy, "Violence! The audience adores violence, it's very Ashkaari of them."]]],
          ["Stand very still.", [[:DORIAN, :shocked, "...Avant-garde. Terrifying. The critics will call it 'a meditation'. Brilliant."]]]] },
      "The curtain rises. The house is full. For three minutes, the whole of Saltmere forgets there is a war.",
      [:DORIAN, :sad, "Lovely. Lovely. Here. My leading lady's heartstone. Her Lopunny could kick a chandelier and land on the beat. She'd want it on a stage, not in my drawer."],
      { :complete => true },
      [:DORIAN, :happy, "Bow, darling. Always bow. They remember the bow."]
    ]
  }
})

#===============================================================================
# ISENMAR - the Tally
#===============================================================================
# 16 badges: the Causeway Matriarch (boss).
tr.quest(:IS_CAUSEWAY_MATRIARCH, {
  :trial => :ISENMAR, :title => "The Causeway Matriarch", :giver => "the Matriarch", :map => 560,
  :where => "the Frostflat Causeway at low tide", :rank => 1, :points => 3, :rec_level => 78, :chapter => 18,
  :unlock => "badges >= 16", :board => false, :tags => [:mega, :boss],
  :summary => "A Kangaskhan the size of a hut has taken the Frostflat Causeway.",
  :steps => { :ask => "Prove yourself to the Causeway Matriarch." },
  :reward => { :items => [[:KANGASKHANITE, 1]] },
  :scenes => {
    :offer => [
      "On the causeway's crown, where the old cairn stands, a Kangaskhan as big as a fishing hut stands between you and the road. Behind her, half a dozen young ones are fishing.",
      "She doesn't charge. She waits, the way the Tally waits: for you to prove you're worth the road.",
      { :choice => "Face her?", :options => [
          ["Face her.", [{ :accept => true },
             { :event_battle => :IS_CAUSEWAY_MATRIARCH,
               :won => ["The Matriarch snorts, and steps aside. From the stones of the cairn she digs out something she has kept warm a long time, and drops it at your feet.",
                        { :complete => true }, "A skald would cut this into the Tally Mast. You do it yourself, in the frost on the cairn."],
               :lost => ["The Matriarch pushes you, gently, all the way back down the causeway."] }]],
          ["Wait for the tide.", ["The young ones splash. The Matriarch doesn't move."]]] }
    ]
  }
})

#===============================================================================
# ZENITH - the Prize Exchange
#===============================================================================
# 10 badges: the Gale Post's dead letters (Pidgeotite).
tr.quest(:ZE_RETURN_TO_SENDER, {
  :trial => :ZENITH, :title => "Return to Sender", :giver => "Postmaster Halloran", :map => 325,
  :where => "Gale Post Hall, Skyreach", :rank => 1, :points => 2, :rec_level => 54, :chapter => 12,
  :unlock => "badges >= 10", :board => true, :tags => [:mega, :delivery, :comedy],
  :summary => "CALL FOR PROPOSALS #0412: DEAD LETTERS, THREE (3). DELIVER BY HAND. PRIZE: ONE (1) DRAWER, CLEARED.",
  :steps => { :ask => "Postmaster Halloran has three dead letters for Skyreach.",
              :letters => "Deliver the three dead letters to their doors in Skyreach.",
              :return => "All three are delivered. Go back to the Postmaster." },
  :reward => { :items => [[:PIDGEOTITE, 1]] },
  :scenes => {
    :offer => [
      [:POSTMASTER, :deadpan, "Three letters. No stamps. Addresses in a hand I'd call 'enthusiastic'. The Gale Post delivers everything. Eventually."],
      [:POSTMASTER, :neutral, "Our couriers are all flying for the war. You've got legs. And a ring, I see. Hm."],
      { :choice => "Deliver the dead letters?", :options => [
          ["I'll take them.", [{ :accept => true }, { :step => :letters }, [:POSTMASTER, :neutral, "Mast Ward, the Lower Gantries, the Skybridge. Knock twice. Nobody in Skyreach answers one knock."]]],
          ["Not today.", [[:POSTMASTER, :deadpan, "They've waited eleven years. They'll wait."]]]] }
    ],
    :letter => [
      { :count => [:letters, 1] },
      "You knock twice. A hand takes the letter, then the door shuts.",
      { :if => "quest_count(:SELF, :letters) >= 3", :then => [{ :step => :return }, "That's the last one."] }
    ],
    :return => [
      [:POSTMASTER, :happy, "All three! The Post thanks you. The Post also owes you a drawer."],
      [:POSTMASTER, :neutral, "In it: the heartstone the Post's first courier-bird wore. Odessa says it's wasted in a drawer. Odessa says that about most things in drawers."],
      { :complete => true }
    ]
  }
})

#===============================================================================
# ASHKAAR - the Trial by Flames
#===============================================================================
# 11 badges: Old Cinder, a retired Legion war-Charizard (boss; Charizardite X).
tr.quest(:AS_OLD_CINDER, {
  :trial => :ASHKAAR, :title => "Old Cinder", :giver => "Roost-keeper Tarn", :map => 248,
  :where => "Pyre Keep, the Dragon Roosts", :rank => 1, :points => 3, :rec_level => 58, :chapter => 13,
  :unlock => "badges >= 11", :board => true, :tags => [:mega, :boss, :war],
  :summary => "WRIT: The war-Charizard Old Cinder will not leave the high roost. Its rider fell at the front. Bring it down, honourably.",
  :steps => { :ask => "Roost-keeper Tarn wants Old Cinder brought down from the high roost.",
              :fight => "Face Old Cinder on the high roost." },
  :reward => { :items => [[:CHARIZARDITEX, 1]] },
  :scenes => {
    :offer => [
      [:TARN, :sad, "Old Cinder's rider died at the Glass Dunes. Since then it won't come down. It won't eat. It burns anyone who climbs."],
      [:TARN, :neutral, "In Ashkaar we don't put a dragon down for grief. We give it a fight worth having. Then it remembers it's alive."],
      { :choice => "Climb to the high roost?", :options => [
          ["I'll fight it.", [{ :accept => true }, { :step => :fight }, [:TARN, :neutral, "Say true or say nothing, up there. It can tell."]]],
          ["Not yet.", [[:TARN, :neutral, "It's not going anywhere. That's the trouble."]]]] }
    ],
    :fight => [
      "On the high roost, a scarred black-eyed Charizard lifts its head. A cracked Legion harness still hangs from its neck.",
      { :event_battle => :AS_OLD_CINDER,
        :won => ["Old Cinder folds its wings and lowers its head to you, the way it must once have lowered it to its rider.",
                 "From the harness, Tarn unclips a stone as black as the Pyre Road, with a blue flame caught in it.",
                 [:TARN, :neutral, "Its war-stone. It hasn't worn it since. It wants you to have it. Don't argue with a dragon."],
                 { :complete => true }],
        :lost => ["Old Cinder turns its back and curls around the empty saddle again."] }
    ]
  }
})

# 15 badges, Trial by Flames rank 2: the Dragonsworn writ (Salamencite).
tr.quest(:AS_DRAGONSWORN, {
  :trial => :ASHKAAR, :title => "Dragonsworn", :giver => "Legate Varra Kosk", :map => 240,
  :where => "the Crucible, Cindervault", :rank => 2, :points => 4, :rec_level => 75, :chapter => 17,
  :unlock => "badges >= 15", :board => true, :tags => [:mega, :oath],
  :summary => "WRIT OF THE DRAGONSWORN: the Crucible keeps one heartstone for one who earns it without being born to a dragon.",
  :steps => { :ask => "Swear the Dragonsworn oath before Legate Kosk." },
  :reward => { :items => [[:SALAMENCITE, 1]] },
  :scenes => {
    :offer => [
      [:KOSK, :neutral, "The Crucible keeps a heartstone for the Dragonsworn who wasn't born to a dragon. In forty years nobody has taken it."],
      [:KOSK, :neutral, "The oath is one question, at the brazier. Lie and the writ burns. Ashkaar law."],
      { :accept => true },
      { :choice => [:KOSK, :neutral, "Why do you fight?"], :options => [
          ["For the people I've met.", [{ :run => :sworn }]],
          ["Because I'm good at it.", [{ :run => :sworn }]],
          ["I don't know yet.", [[:KOSK, :smug, "The first honest answer in forty years."], { :run => :sworn }]],
          ["For the glory of Ashkaar.", [[:KOSK, :deadpan, "...No. The brazier says otherwise. The writ burns. Come back when you'll say true."]]]] }
    ],
    :sworn => [
      [:KOSK, :neutral, "Say true, and the fire keeps you. Dragonsworn."],
      "She takes a blue stone with a red heart from a niche above the brazier. It is hot enough that she hands it over in tongs.",
      { :complete => true }
    ]
  }
})

#===============================================================================
# NADIR - the Gutter Book
#===============================================================================
# 8 badges: Wenlow and the Quiet Ward (Audinite).
tr.quest(:NA_BEDSIDE_MANNER, {
  :trial => :NADIR, :title => "Bedside Manner", :giver => "Wenlow", :map => 223,
  :where => "Corvin Mott's Infirmary, Mirefen", :rank => 1, :points => 2, :rec_level => 44, :chapter => 10,
  :unlock => "badges >= 8", :board => true, :tags => [:mega, :kindness],
  :summary => "CHALK: INFIRMARY NEEDS VISITORS. NOT DOCTORS. JUST VISITORS. - W.",
  :steps => { :ask => "Wenlow wants someone to sit with the Quiet Ward's patients.",
              :beds => "Sit with three of the Quiet Ward's patients.",
              :return => "Tell Wenlow how the visits went." },
  :reward => { :items => [[:AUDINITE, 1]] },
  :scenes => {
    :offer => [
      [:WENLOW, :happy, "You're back! Hi! Sorry. Hi. I'm doing rounds and I've got forty patients and two hands, and the Doctor says talking helps."],
      [:WENLOW, :neutral, "Their eyes move under the glass, did he tell you? Like they're dreaming. So I talk to them. Will you? Just three. They like new voices."],
      { :choice => "Sit with the patients?", :options => [
          ["Of course.", [{ :accept => true }, { :step => :beds }, [:WENLOW, :happy, "Thank you! Start with Missus Pell by the window, she likes the weather."]]],
          ["Not now.", [[:WENLOW, :neutral, "That's all right. They're not going anywhere. Sorry. Doctor's joke."]]]] }
    ],
    :bed => [
      { :count => [:beds, 1] },
      "You sit and talk for a while: the weather, the road, the Festival. Under the glass, an eye moves.",
      { :if => "quest_count(:SELF, :beds) >= 3", :then => [{ :step => :return }] }
    ],
    :return => [
      [:WENLOW, :happy, "They liked you. I can tell. Mister Coyle's hand twitched, that's practically a party."],
      [:WENLOW, :neutral, "Here. Matron, the Ward's Audino, came in with this round her neck. A heartstone, the Doctor says. She's too old for fighting, and you've got a ring now."],
      [:WENLOW, :happy, "Bring it back and show her sometime! She'd like that."],
      { :complete => true }
    ],
    # After the Sump Purge (Ch16) Wenlow is gone; Corvin hands it over instead (his event only exists then).
    :corvin => [
      [:CORVIN, :sad, "Ah. You. He left something for you. Labelled, of course. He labelled everything."],
      "A pink stone on a loop of bandage, and a tag in round handwriting: FOR THE ONE WITH THE SINGING RING. SHOW MATRON SOMETIME!",
      [:CORVIN, :deadpan, "Matron's heartstone. She's too old for fighting. I'm too old for most things. Take it before I get sentimental. It's bad for the patients."],
      { :complete => true }
    ]
  }
})

# 15 badges: the Sump Barons' kennel in the Moon Market (Houndoominite).
tr.quest(:NA_MOON_MARKET_DOGS, {
  :trial => :NADIR, :title => "Dogs of the Moon Market", :giver => "Six-Fingers Ottoline", :map => 423,
  :where => "the Moon Market, Underveil", :rank => 1, :points => 3, :rec_level => 74, :chapter => 17,
  :unlock => "badges >= 15", :board => true, :tags => [:mega, :heist],
  :summary => "CHALK: BARONS' KENNEL. THREE CAGES. NOBODY SAW NOTHING.",
  :steps => { :ask => "Ottoline has a job at the Barons' kennel.",
              :cages => "Open the three kennel cages behind the Moon Market.",
              :return => "The cages are open. See Ottoline." },
  :reward => { :items => [[:HOUNDOOMINITE, 1]] },
  :scenes => {
    :offer => [
      [:OTTOLINE, :neutral, "The Barons starve Houndoom for the pit fights. Starved dogs bite harder. I want the dogs out and the Barons embarrassed. Mostly the second."],
      [:OTTOLINE, :smug, "There's a prize in the kennel-master's lockbox. You get it. I get the story."],
      { :choice => "Take the job?", :options => [
          ["Open the cages.", [{ :accept => true }, { :step => :cages }]],
          ["Not my business.", [[:OTTOLINE, :deadpan, "Everything down here is your business. You just don't know it yet."]]]] }
    ],
    :cage => [
      { :count => [:cages, 1] },
      "The latch gives. A thin Houndoom looks at you, then at the open door, then it's gone into the dark.",
      { :if => "quest_count(:SELF, :cages) >= 3", :then => [{ :step => :return },
          [:KENNELMASTER, :angry, "HEY! Those were Baron property! ...You know what, I'm not paid enough. Take the box. Take the whole thing."]] }
    ],
    :return => [
      [:OTTOLINE, :happy, "The whole market saw. The Barons will be furious for a week. Beautiful."],
      [:OTTOLINE, :neutral, "Your cut. A pit champion's heartstone. Don't sell it down here; everyone will know where you got it."],
      { :complete => true }
    ]
  }
})

# 17 badges, Gutter Book rank 2: the Memory Kata (Lucarionite).
tr.quest(:NA_MEMORY_KATA, {
  :trial => :NADIR, :title => "The Memory Kata", :giver => "Six-Fingers Ottoline", :map => 260,
  :where => "the Last Rung, Ironreach", :rank => 2, :points => 4, :rec_level => 82, :chapter => 19,
  :unlock => "badges >= 17", :board => true, :tags => [:mega, :kaito],
  :summary => "CHALK: PAWN SHELF, TOP ROW. A WARDGUARD STONE. THE OWNER WANTS IT GONE TO SOMEONE WHO'LL USE IT.",
  :steps => { :ask => "Buy the Wardguard heartstone off Ottoline's pawn shelf ($20,000)." },
  :reward => { :items => [[:LUCARIONITE, 1]] },
  :scenes => {
    :offer => [
      [:OTTOLINE, :neutral, "Top shelf. A Wardguard unit's ring-stone. Pawned here the winter after Marrowgate. The man who pawned it comes in every year to look at it."],
      [:OTTOLINE, :neutral, "This year he said sell it. To someone who'll use it. Twenty thousand. I'm sentimental, not stupid."],
      { :choice => "Pay $20,000?", :options => [
          ["Pay.", [
             { :if => "money >= 20000", :then => [{ :accept => true }, { :pay => 20000 }, { :run => :kata }],
               :else => [[:OTTOLINE, :deadpan, "Come back with twenty thousand. The stone isn't going anywhere."]] }]],
          ["Not yet.", [[:OTTOLINE, :deadpan, "It's waited fifteen years."]]]] }
    ],
    :kata => [
      { :map => "Kaito is at the bar, wraps on, a cup of something he isn't drinking." },
      [:KAITO, :neutral, "It was my unit's. Memory's mother wore it, at Marrowgate. She could feel them through the gate. So could I."],
      [:KAITO, :neutral, "It remembers for me. Now it can remember for you. Use it on someone who deserves it."],
      { :complete => true },
      [:KAITO, :neutral, "Stand up. Again. That's the whole kata."]
    ]
  }
})

#===============================================================================
# OSSARIA - the Rolls of Unearthing
#===============================================================================
# 12 badges: Sahar and the Old Amber's other half (Aerodactylite).
tr.quest(:OS_AMBER_AGAIN, {
  :trial => :OSSARIA, :title => "Amber, Again", :giver => "Sahar Ostrand", :map => 209,
  :where => "Sahar's Dig Lab, Duneholt", :rank => 1, :points => 2, :rec_level => 60, :chapter => 14,
  :unlock => "badges >= 12", :board => true, :tags => [:mega, :fossil],
  :summary => "TABLET: The Old Amber held two things. The Warden kept one. Bring her the other, alive.",
  :steps => { :ask => "Show Sahar an Aerodactyl revived from the Old Amber." },
  :reward => { :items => [[:AERODACTYLITE, 1]] },
  :scenes => {
    :offer => [
      [:SAHAR, :deadpan, "The Old Amber from the Brinecut mine. Two things were in it. A sleeping Aerodactyl, which Lumen woke for you. And this, which I kept."],
      [:SAHAR, :neutral, "Shameful. I'm a curator. Curators keep things. Show me the first one alive and well, and the second is yours."],
      { :accept => true },
      { :if => "party_has(:AERODACTYL)", :then => [{ :run => :show }],
        :else => [[:SAHAR, :neutral, "No Aerodactyl with you. The amber waited a hundred thousand years; I can wait an afternoon."]] }
    ],
    :show => [
      "Your Aerodactyl sniffs at Sahar's coat, then at the drawer she unlocks.",
      [:SAHAR, :sad, "...It remembers. Look at that. Here. The amber's other half. Its heart, set hard."],
      { :complete => true },
      [:SAHAR, :deadpan, "The desert keeps everything. It just doesn't keep it where you left it. Neither do I, apparently."]
    ]
  }
})

# 15 badges, Rolls of Unearthing rank 2: the Bonewright's commission (Tyranitarite).
tr.quest(:OS_BONEWRIGHT, {
  :trial => :OSSARIA, :title => "The Bonewright's Commission", :giver => "Curator-Elect Nasrin Vael", :map => 360,
  :where => "the Cragholm lift-house rack; the dig is on the Vertebrae", :rank => 2, :points => 4, :rec_level => 75, :chapter => 17,
  :unlock => "badges >= 15", :board => true, :tags => [:mega, :dig],
  :summary => "TABLET: A tyrant's heart lies in the third vertebra. Dig it out whole.",
  :steps => { :ask => "Dig the tyrant's heart out of the third vertebra on the Vertebrae.",
              :return => "Take the heartstone to Curator-Elect Nasrin." },
  :reward => { :items => [[:TYRANITARITE, 1]] },
  :scenes => {
    :offer => [
      [:NASRIN, :neutral, "A commission for a Delver, not a Sandsifter. The Vertebrae are a Tyranitar's spine, a mountain of it. The third vertebra has a heart in it."],
      [:NASRIN, :neutral, "Dig it out whole and the Rolls will write your name in the good ink."],
      { :choice => "Take the commission?", :options => [
          ["Take it.", [{ :accept => true }, [:NASRIN, :happy, "Wonderful. Bring a shovel and something that can carry a mountain."]]],
          ["Not yet.", [[:NASRIN, :neutral, "It's been there a while."]]]] }
    ],
    :dig => [
      "Under the third vertebra, the rock is warm. You dig until your hands are raw, and there it is: a stone the green of old armour, with a dark heart.",
      { :step => :return }
    ],
    :return => [
      [:NASRIN, :happy, "Whole! Not a crack! The Rolls thank you. The Rolls also say you keep it; we only wanted it written down."],
      { :complete => true }
    ]
  }
})

#===============================================================================
# ANTUMBRA - the Rite of Reflection
#===============================================================================
# 13 badges, Rite of Reflection rank 2: the smile behind the glass (Mawilite).
tr.quest(:AN_SMILE_BEHIND_GLASS, {
  :trial => :ANTUMBRA, :title => "The Smile Behind the Glass", :giver => "Lector Saffi Ivarne", :map => 346,
  :where => "the Speculum, Lucent", :rank => 2, :points => 3, :rec_level => 64, :chapter => 15,
  :unlock => "badges >= 13", :board => true, :tags => [:mega, :mirror],
  :summary => "MIRROR-WRITING: Somebody's reflection in the Speculum is smiling with too many teeth.",
  :steps => { :ask => "A reflection in the Speculum smiles with too many teeth. Face it.",
              :return => "Tell Lector Saffi what was behind the glass." },
  :reward => { :items => [[:MAWILITE, 1]] },
  :scenes => {
    :offer => [
      [:SAFFI, :neutral, "In the third pane of the Speculum, every reflection smiles. Including the people who don't. Particularly them."],
      [:SAFFI, :deadpan, "It's a Rite. You stand there until it stops. Most people leave. Will you stay?"],
      { :choice => "Face the third pane?", :options => [
          ["I'll stay.", [{ :accept => true }, [:SAFFI, :neutral, "Don't smile back. It counts as an answer."]]],
          ["No thank you.", [[:SAFFI, :neutral, "Wise. Rare, but wise."]]]] }
    ],
    :pane => [
      "Your reflection smiles. Behind it, a second mouth opens, wider than the first, full of steel teeth.",
      "You don't smile back. You wait. After a long time, the second mouth closes, and something falls out of the glass onto the floor: a stone, pink and grey.",
      { :step => :return }
    ],
    :return => [
      [:SAFFI, :happy, "A Mawile's heart. It was hiding in the glass, eating everyone's smiles. Now it has nothing to hide behind."],
      { :complete => true }
    ]
  }
})
