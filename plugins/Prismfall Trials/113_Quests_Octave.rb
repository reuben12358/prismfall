#===============================================================================
# Prismfall Trials - 113 The Eevee Octave (SPINE Revision 19; design/EEVEE_OCTAVE.md)
#-------------------------------------------------------------------------------
# Eight singers of the Prism Choir, Glassfall orphans the Choir raised, sent
# home each to one kingdom's Imprint. Each has a quest on that kingdom's Trial
# board. Helping them is recorded in order ({ :octave_help => :ID },
# 012_Trials_Octave.rb); Carol in Crownhaven is always last (her quest needs the
# other seven). Then Vesper Lindqvist, who asked you to look in on them in
# Saltmere, hosts the gauntlet in the Glassfall Memorial Garden (489).
# Order of first meeting follows the gyms:
#   Lyra (Elowen, Ch3) - Aria (Isenmar, Ch4) - Cadence (Zenith, Ch5) - Sona (Ossaria, Ch6) - Noct (Nadir, Ch7)
#   - Forte (Ashkaar, Ch8) - Lento (Antumbra, Ch13) - Carol (Crownhaven, Ch20)
# No quest expires: a singer missed on the way can be helped on a later visit.
# Duels: pbs/trainers_trials.txt v50 (provisional, the trainer designer tunes them).
#===============================================================================
tr = Prismfall::Trials
tr::SPEAKERS.merge!({
  :VESPER => "Vesper", :LYRA => "Lyra", :ARIA => "Aria", :CADENCE => "Cadence", :SONA => "Sona", :NOCT => "Noct",
  :FORTE => "Forte", :LENTO => "Lento", :CAROL => "Carol", :REFLECTION => "Lento's reflection",
  :OTTOLINE => "Six-Fingers Ottoline", :FERRYMAN => "Marsh ferryman", :KOSK => "Legate Varra Kosk",
  :SAFFI => "Lector Saffi Ivarne", :NASRIN => "Curator-Elect Nasrin Vael"
})

#===============================================================================
# The thread: Vesper's request (Ch2) and the gauntlet (Ch20)
#===============================================================================
tr.quest(:CR_OCTAVE, {
  :trial => :CROWNHAVEN, :title => "The Eevee Octave", :giver => "Vesper Lindqvist", :map => 145,
  :where => "backstage at the Lantern Theatre, Saltmere (asked); the Glassfall Memorial Garden, Crownhaven (489)",
  :rank => 1, :points => 5, :rec_level => 90, :chapter => 2, :board => false, :tags => [:gauntlet, :zmove, :event_mon],
  :summary => "Vesper asked you to look in on the eight singers of the Octave as your road takes you through the kingdoms.",
  :steps => { :road => "Look in on the Octave's singers as you travel: Lyra (Briarwick), Aria (Ebbmouth), Cadence (Lumen City), Sona (Duneholt), Noct (Mirefen), Forte (Cindervault), Lento (the Mirror Mere). Carol never leaves Crownhaven.",
              :garden => "All eight singers have had your help. Vesper is waiting in the Glassfall Memorial Garden in Crownhaven." },
  :reward => { :pokemon => :CR_OCTAVE_EEVEE, :items => [[:EEVIUMZ, 1]] },   # SPINE Rev 23: no ring; the Warden's ring wakes it
  :touches => "The gauntlet runs in the order you helped the singers (each Eeveelution uses its Z-move); S177 EEVEE_OCTAVE_DONE",
  :scenes => {
    :saltmere => [
      { :map => "After the duet backstage (S190). Vesper is folding Amen's ribbon back into her sleeve." },
      [:VESPER, :neutral, "We sing together once a year, for the Pageant. Tomorrow we scatter again. Each of us lives beside a Plate now, one each, in all seven kingdoms."],
      [:VESPER, :happy, "Except Carol. Carol never leaves Crownhaven. Someone has to sing to the ones who didn't get out."],
      [:VESPER, :neutral, "They're very good at singing and very bad at being alone. If your road takes you past any of them... would you look in on them?"],
      { :choice => "Look in on the Octave?", :options => [
          ["I will.", [[:VESPER, :happy, "Thank you. Lyra's going home to Briarwick, so she's first, if you go that way."],
                       { :accept => true }]],
          ["Why me?", [[:VESPER, :neutral, "Because you looked at Understudy the way they look at their Eevee. Like it was a person."],
                       [:VESPER, :happy, "And because nobody else asked. That's usually how."],
                       { :accept => true }]]] },
      [:VESPER, :neutral, "Lyra in Briarwick. Aria in Ebbmouth. Cadence in Lumen City. Sona in Duneholt. Noct in Mirefen. Forte in Cindervault. Lento at the Mirror Mere."],
      [:VESPER, :happy, "I'll be at the Festival. We always are."]
    ],
    :lucent => [
      { :map => "Chapter 13, the Athenaeum cloister, after Vesper's sparring double (S191)." },
      [:VESPER, :neutral, "Carol writes to me every week. The others write when something has gone wrong."],
      { :if => "octave_helped >= 5", :then => [
          [:VESPER, :happy, "So I've had a lot of letters about you. Good letters. Forte's had three exclamation marks in it."]
        ], :else => [
          [:VESPER, :neutral, "None of them has mentioned you yet. That's all right. Roads are long."]
        ] },
      { :if => "!octave_has(:LENTO)", :then => [
          [:VESPER, :sad, "Lento hasn't written at all. She's at the Mirror Mere, past Glassmere. It's frozen, they say. In summer."]
        ] }
    ],
    :garden => [
      { :map => "The Glassfall Memorial Garden. White stone, a ring of glass figures among the roses, and eight singers standing in a half-circle with their Eeveelutions. Vesper steps out to meet you." },
      [:VESPER, :happy, "You came. Everyone, it's them."],
      [:VESPER, :neutral, "All eight of them have written to the Choir about you. Lyra's Eevee came down off its stone. Aria got Brine back out of the river. Cadence still has her job, somehow."],
      [:VESPER, :neutral, "Sona's bell rings at noon again. Noct's lamp-runners sleep in a bed. Forte has a Writ of Flame. Lento's reflection comes and goes as it likes. And Carol finished her song."],
      [:VESPER, :happy, "They wanted to thank you. Properly. And the Choir has a custom: before we pass on the power of Eevee, someone has to prove they can carry it."],
      [:VESPER, :neutral, "So: all eight of them, in the order you helped them, one after another. Then me, and Amen. No rest between."],
      { :choice => [:VESPER, :neutral, "Will you sing with all of us?"], :options => [
          ["Begin.", [
             [:VESPER, :happy, "Then from the first note."],
             { :octave_gauntlet => true,
               :won => [
                 { :map => "The last note. Amen sits down in the grass, very pleased with itself. The singers clap, out of time, on purpose." },
                 [:VESPER, :happy, "That was every note we have. You were worth all of them."],
                 [:VESPER, :neutral, "This Eevee was born in the garden this spring. It hasn't decided anything yet. We'd like it to grow up with you."],
                 [:VESPER, :neutral, "And this. We sang over it together: a sliver of the Crown's glass from the Glassfall, tuned to every Imprint at once."],
                 [:VESPER, :neutral, "You won't need a cantor's ring for it. That Warden's ring of yours hears it. Its chip and our glass came off the same crown."],
                 { :if => "party_has(:EEVEE)", :then => [
                     [:VESPER, :happy, "It works for Understudy too, if it's still undecided. An Eevee who knows Last Resort and holds that crystal can become everything at once, for a moment."]
                   ] },
                 { :script => proc { |_ctx| $game_switches[177] = true if $game_switches } },
                 { :complete => true },
                 [:VESPER, :happy, "Whatever it becomes, it'll become it because of you. I said that once before, didn't I?"]],
               :lost => [
                 [:VESPER, :neutral, "Rest. Sing it again when you're ready. We aren't going anywhere. We never miss a Festival."]] }]],
          ["Not yet.", [[:VESPER, :neutral, "Then we'll wait. We're good at it."]]]] }
    ],
    :after => [
      [:VESPER, :happy, "The Octave sings at dusk, here, every day of the Festival. You know all the words now."]
    ]
  }
})

#===============================================================================
# ELOWEN - The Quiet Way: Lyra and Moss (Leafeon), Briarwick, Chapter 3
#===============================================================================
tr.quest(:EL_OCTAVE_MOSS, {
  :trial => :ELOWEN, :title => "The Moss Hymn", :giver => "Lyra of the Octave", :map => 120,
  :where => "under the Lantern House tree, Briarwick; the moss-stone in Gossamer Wood (524)", :rank => 1, :points => 3,
  :rec_level => 18, :chapter => 3, :unlock => "badges >= 1", :board => true, :tags => [:octave, :spiritual, :duel],
  :summary => "A singer of the Octave has been singing to her Eevee for three days. It will not come down from the moss-stone in Gossamer Wood.",
  :steps => { :ask => "Go with Lyra to the moss-stone in Gossamer Wood.",
              :stone => "Lyra's Eevee won't come down from the moss-stone. Mother Aldreth says: stop singing at it.",
              :duel => "Moss came down a Leafeon. Lyra wants a duel so it knows it can stand on its own." },
  :reward => { :money => 800, :items => [[:BIGROOT, 1]] },
  :touches => "The Octave: Lyra (1 of 8 in gym order)",
  :scenes => {
    :offer => [
      { :map => "A girl in Choir grey sits under the Lantern House tree with her knees up, humming the same four notes over and over." },
      [:LYRA, :sad, "Oh. Sorry. Was I humming? I'm always humming. The plants don't mind."],
      [:LYRA, :neutral, "I'm Lyra. Of the Octave. Vesper's Octave. I came home to Briarwick after the Pageant, and my Eevee, Moss, went straight up the old moss-stone in Gossamer Wood and won't come down."],
      [:LYRA, :sad, "Three days. I've sung it everything I know. Mother Aldreth says I should stop singing at it. I don't know what that means. I'm a singer."],
      { :if => "party_has(:EEVEE)", :then => [[:LYRA, :happy, "Is that an Eevee? Hello. Has yours decided yet? Mine is trying to."]] },
      { :choice => "Go with Lyra to the moss-stone?", :options => [
          ["I'll come.", [{ :accept => true }, { :step => :stone },
                          [:LYRA, :happy, "Thank you. It's past the silk walls, where the moss grows on the north side of everything."]]],
          ["Not now.", [[:LYRA, :neutral, "That's all right. I'll be here. Humming."]]]] }
    ],
    :stone => [
      { :map => "The moss-stone: a grey boulder furred green to the top. A small brown Eevee sits on the summit with its eyes shut. Lyra is already there, mid-note." },
      [:LYRA, :neutral, "Moss. Moss, please. I'll sing the one you like."],
      "The Eevee's ears flatten a little more with every note.",
      { :choice => "What do you do?", :options => [
          ["Sing along.", [
             "You join in. The Eevee curls up tighter. Lyra stops, and looks at you, and laughs at herself.",
             [:LYRA, :sad, "It's not working when two of us do it either."]]],
          ["Sit down by the stone and say nothing.", [
             "You sit. After a while, Lyra stops singing and sits down next to you.",
             "The wood is very loud when nobody is singing: leaves, water somewhere, the moss creaking as it drinks.",
             "The Eevee opens its eyes. It listens too.",
             { :map => "Moss climbs down the stone. The green on the stone is the green on its fur, then all of it: a Leafeon steps off the last ledge." },
             [:LYRA, :happy, "Oh. Oh, look at you. You weren't stuck. You were listening."],
             [:LYRA, :neutral, "And I was too loud to hear it. Mother Aldreth is going to be unbearable."],
             { :step => :duel }, { :run => :duel }]],
          ["Tell Lyra to stop singing.", [
             [:LYRA, :sad, "Everyone keeps telling me that. Fine. Fine. I'll stop."],
             "She stops for almost three seconds, then starts humming again without noticing."]]] }
    ],
    :duel => [
      [:LYRA, :neutral, "Will you duel us? Moss has never stood on its own feet in a fight. I want it to know it can."],
      { :trainer => [:OCTAVE_SINGER, "Lyra", 50],
        :won => [
          [:LYRA, :happy, "It stood. It stood the whole time. Thank you."],
          [:LYRA, :neutral, "I'll write to Vesper tonight. She'll say she knew. She always knew."],
          { :octave_help => :LYRA }, { :complete => true }],
        :lost => [
          [:LYRA, :neutral, "Moss liked that. Come back and try again? We'll be at the Lantern House tree."]] }
    ],
    :after => [
      [:LYRA, :happy, "Moss sits in the Lantern House now and listens to Mother Aldreth not talking. They get on very well."]
    ]
  }
})

#===============================================================================
# ISENMAR - The Tally: Aria and Brine (Vaporeon), Ebbmouth, Chapter 4
#===============================================================================
tr.quest(:IS_OCTAVE_DROWNED_NOTE, {
  :trial => :ISENMAR, :title => "The Drowned Note", :giver => "Aria of the Octave", :map => 160,
  :where => "the river steps, Ebbmouth; the Mill Quay wheel (167)", :rank => 1, :points => 3, :rec_level => 22,
  :chapter => 4, :unlock => "badges >= 2", :board => true, :tags => [:octave, :search, :duel],
  :summary => "A singer's Vaporeon melted into the Ebb when the river stuttered and hasn't come out. She can still hear it, sometimes.",
  :steps => { :listen => "Listen for Brine's note at three places on the Ebb: the river steps, the fish-market slip and the Mill Quay steps.",
              :wheel => "Aria thinks Brine is hiding under the Mill Quay wheel.",
              :duel => "Brine is back. Bersi wants a fight for the saga." },
  :reward => { :money => 1200, :items => [[:SHELLBELL, 1]] },
  :touches => "The Octave: Aria (2 of 8 in gym order); a verse on the Tally Mast",
  :scenes => {
    :offer => [
      { :map => "On the river steps a young woman in a wet Choir robe is sitting in the shallows up to her waist, singing a sea-shanty with the words wrong on purpose." },
      [:ARIA, :happy, "Morning! It's lovely in. The cold's just the sea saying hello."],
      [:ARIA, :neutral, "I'm Aria. Octave. My Vaporeon, Brine, melted into the river three days ago, when it did that stutter. They do that, Vaporeon. Go to water."],
      [:ARIA, :sad, "It always comes back. It hasn't come back. But I can hear it. A note in the water, here and there, like it's calling from a long way down."],
      [:ARIA, :happy, "You've got young ears. Will you listen with me? Bersi says if I find it he'll carve it on the Tally Mast."],
      { :choice => "Help Aria listen for Brine?", :options => [
          ["Let's listen.", [{ :accept => true },
                             [:ARIA, :happy, "Try here on the steps, at the fish-market slip, and down at the Mill Quay steps. Put your ear right to the water."]]],
          ["Later.", [[:ARIA, :neutral, "I'll stay in. I'm warm now. Don't tell me if I'm not."]]]] }
    ],
    :note => [
      { :map => "You kneel and put your ear to the water. Somewhere under the noise of the river, a long, low note." },
      { :count => [:notes, 1] },
      { :if => "quest_count(:SELF, :notes) >= 3", :then => [
          "The third note is lower than the others, and it comes from upstream, where the Mill Quay wheel turns.",
          [:ARIA, :happy, "The wheel! It's hiding under the wheel. The Lattice hum is quieter there. It never liked the hum."],
          { :step => :wheel }
        ], :else => [
          "The note fades. It came from further up the river."
        ] }
    ],
    :wheel => [
      { :map => "Under the Mill Quay wheel the water is black and slow. Aria wades in to her chest and sings one note, the same one you heard." },
      [:ARIA, :neutral, "Come on, then. I know it's loud up here. I'm loud too. You like me anyway."],
      { :map => "The water stands up, gathers into a shape, and becomes a Vaporeon, coughing." },
      [:ARIA, :happy, "Brine! You great puddle!"],
      { :step => :duel }, { :run => :duel }
    ],
    :duel => [
      [:ARIA, :happy, "Bersi says a saga needs a fight in it or the Tally won't take it. Fight us? He'll make it sound bigger than it was."],
      { :trainer => [:OCTAVE_SINGER, "Aria", 50],
        :won => [
          [:ARIA, :happy, "Ha! Wrong note, right song. Bersi's already carving."],
          { :map => "At the Net Loft, Bersi Gullsong cuts a notch on the Tally Mast beside your name." },
          [:BERSI, :happy, "'And the stranger heard the river's sorrow, and the drowned beast rose.' Something like that. I'll fix it later. I never fix it later."],
          { :octave_help => :ARIA }, { :complete => true }],
        :lost => [
          [:ARIA, :happy, "Ha! The river wins today. Come back, we'll be on the steps."]] }
    ],
    :after => [
      [:ARIA, :happy, "Brine goes back in the river every morning now, and comes out every morning. That's all I wanted."]
    ]
  }
})

#===============================================================================
# ZENITH - The Prize Exchange: Cadence and Snare (Jolteon), the Lowlight, Chapter 5
#===============================================================================
tr.quest(:ZE_OCTAVE_OFF_BEAT, {
  :trial => :ZENITH, :title => "Off the Beat", :giver => "Grant Kiosk P-3NNY / Cadence of the Octave", :map => 181,
  :where => "the Lowlight steps, Lumen City", :rank => 1, :points => 3, :rec_level => 26, :chapter => 5,
  :unlock => "badges >= 3", :board => true, :tags => [:octave, :data, :duel],
  :summary => "CALL FOR PROPOSALS #0031: NOISE COMPLIANCE, LOWLIGHT BLOCK 9. A STREET DRUMMER'S JOLTEON BLACKS OUT THE BLOCK. BOUNTY: $800.",
  :steps => { :ask => "Find the drummer on the Lowlight steps.",
              :junctions => "Cadence's Jolteon syncs to her drumming, and the Lattice syncs to it. Shift the three Lattice junction boxes on Block 9 off her beat.",
              :duel => "The block stayed lit. Cadence wants to play it out properly." },
  :reward => { :money => 800, :items => [[:CELLBATTERY, 2]] },
  :outcomes => { :unknown => { :effects => "RES+1" }, :fault => { :money => 800, :effects => "MERIDIAN+1" } },
  :touches => "The Octave: Cadence (3 of 8 in gym order); Meridian standing if you file it as a Lattice fault",
  :scenes => {
    :offer => [
      { :map => "The Lowlight steps after dark. A woman in a cut-down Choir robe drums on a stack of paint tins, fast, in fours. A Jolteon bristles beside her in time. Every fourth beat, the streetlamps on the block flicker." },
      [:CADENCE, :deadpan, "If you're from Meridian, I've got a permit. If you're not, I haven't got a permit."],
      [:CADENCE, :neutral, "Cadence. Octave. Yes, that Octave. The Choir pays in hymns. Meridian pays in money. I tune their Lattice junctions on nights. Guess which one buys noodles."],
      [:CADENCE, :sad, "Snare picks up my beat and the Lattice picks up Snare. One-two-three-four, blackout. They've posted a bounty on 'the source'. The source is me."],
      { :choice => "Help Cadence?", :options => [
          ["How do we fix it?", [
             [:CADENCE, :neutral, "Three junction boxes on this block. They're tuned to a four-count, because some engineer liked a four-count. Shift each one off the beat and Snare can't drive them."],
             [:CADENCE, :deadpan, "I'd do it myself but I'm the source. They'd notice the source fiddling with the junctions."],
             { :accept => true }, { :step => :junctions }]],
          ["Not tonight.", [[:CADENCE, :deadpan, "Nobody's ever free tonight. That's why it's always tonight."]]]] }
    ],
    :junction => [
      { :map => "A brass Lattice junction box, humming. A dial on the front ticks in fours, exactly in time with Cadence's drumming." },
      "You turn the dial to a three-count. The hum stumbles and finds a new, lopsided rhythm. Down the steps, Snare's fur settles a little.",
      { :count => [:shifted, 1] },
      { :if => "quest_count(:SELF, :shifted) >= 3", :then => [
          { :map => "Cadence plays a long roll. Snare crackles. The streetlamps stay on." },
          [:CADENCE, :happy, "Ha. Listen to that. It's terrible. It's the best thing I've ever heard."],
          { :step => :duel }, { :run => :duel }] }
    ],
    :duel => [
      [:CADENCE, :neutral, "Snare's never been allowed to go flat out on this block. Let's find out what it's got. One, two, three, four."],
      { :trainer => [:OCTAVE_SINGER, "Cadence", 50], :field => :NEON_GRID,
        :won => [
          [:CADENCE, :happy, "Off the beat. Mine, not yours. Again tomorrow?"],
          [:CADENCE, :neutral, "P-3NNY still wants a report on 'the source'. Your name, your report."],
          { :choice => "File the report as...", :options => [
              ["'Source unknown.'", [
                 [:PENNY, :neutral, "REPORT FILED: SOURCE UNKNOWN. BOUNTY WITHHELD. THE REGISTRY IS DISAPPOINTED. THE REGISTRY WILL LIVE."],
                 { :octave_help => :CADENCE }, { :complete => :unknown }]],
              ["'A Lattice tuning fault.'", [
                 [:PENNY, :happy, "REPORT FILED: TUNING FAULT, BLOCK 9. MERIDIAN WILL CORRECT IT. BOUNTY RELEASED."],
                 [:CADENCE, :deadpan, "They'll send someone to fix it. It'll be me. On nights. Fine."],
                 { :octave_help => :CADENCE }, { :complete => :fault }]]] }],
        :lost => [
          [:CADENCE, :deadpan, "Off your beat, that. Come back when you've got one."]] }
    ],
    :after => [
      [:CADENCE, :neutral, "Snare still drums. The lamps don't. Best of both."]
    ]
  }
})

#===============================================================================
# OSSARIA - The Rolls of Unearthing: Sona and Noon (Espeon), the sun temple, Chapter 6
#===============================================================================
tr.quest(:OS_OCTAVE_NOON_BELL, {
  :trial => :OSSARIA, :title => "The Noon Bell", :giver => "Sona of the Octave", :map => 215,
  :where => "the Temple of the Noon Sun, outside Duneholt (new map, off Sunbleach Flats 613)", :rank => 1, :points => 3,
  :rec_level => 30, :chapter => 6, :unlock => "badges >= 4", :board => true, :tags => [:octave, :dig, :duel],
  :summary => "Clay tablet: the old sun temple's light-shaft has filled with sand. Its keeper needs diggers. Its keeper says she knew you'd read this.",
  :steps => { :ask => "Find the keeper of the Temple of the Noon Sun.",
              :dig => "Dig the three sand drifts out of the temple's light-shaft.",
              :noon => "The shaft is clear. Be in the temple at noon (any time of day, not at night)." },
  :reward => { :money => 1500, :items => [[:SUNSTONE, 1]] },
  :touches => "The Octave: Sona (4 of 8 in gym order)",
  :scenes => {
    :offer => [
      { :map => "A round sandstone temple, half swallowed by a dune. Inside, in the gloom, a woman in Choir grey sits beside a sleeping Espeon whose forehead jewel has gone dull. She speaks before you do." },
      [:SONA, :neutral, "Yes, I'm the keeper. Yes, the sand. No, it isn't dangerous. You were going to ask all three."],
      [:SONA, :neutral, "Sona. Of the Octave. Noon sleeps here, where the light used to fall at midday. The dune came down the shaft in the spring and the light stopped."],
      [:SONA, :sad, "Its jewel has been dark for a month. It still knows when noon is. It wakes, and looks up, and goes back to sleep."],
      [:SONA, :deadpan, "You're going to say yes. I'll get the spade."],
      { :choice => "Dig out the light-shaft?", :options => [
          ["Yes.", [{ :accept => true }, { :step => :dig }, [:SONA, :neutral, "Three drifts. I heard you'd be quick."]]],
          ["No.", [[:SONA, :neutral, "Hm. I didn't hear that coming. I'm glad. It's boring, being right."]]]] }
    ],
    :drift => [
      { :map => "A drift of sand packed into the light-shaft. You dig until a broken clay tablet slides out of it and the sand runs away under your feet." },
      { :count => [:drifts, 1] },
      { :if => "quest_count(:SELF, :drifts) >= 3", :then => [
          "Daylight falls down the shaft for the first time in a month and lies on the temple floor in a hot white circle.",
          [:SONA, :happy, "There. Now we wait for noon. Noon will wait too. It's very good at it."],
          { :step => :noon }
        ], :else => ["A little more light gets in. The shaft is not clear yet."] }
    ],
    :noon => [
      { :if => "night", :then => [[:SONA, :neutral, "It's night. Even I can't make it noon. Come back in the day."], { :end => true }] },
      { :map => "Noon. The circle of light slides onto the sleeping Espeon. Its jewel lights red, then white, and it opens its eyes." },
      [:SONA, :happy, "Hello, Noon."],
      [:NASRIN, :neutral, "(From the doorway, out of breath:) The Rolls will want that tablet, you know. And a full record of the dig. ...It's lovely, though."],
      [:SONA, :neutral, "Noon wants to stretch. It hasn't fought in a month. You knew I'd ask."],
      { :trainer => [:OCTAVE_SINGER, "Sona", 50],
        :won => [
          [:SONA, :happy, "I heard that coming. I still couldn't stop it. That's the nice kind."],
          [:SONA, :neutral, "Ring the bell on your way out. It's been a long time since anyone rang it at noon."],
          { :octave_help => :SONA }, { :complete => true }],
        :lost => [
          [:SONA, :neutral, "I knew you'd want another go. It'll be noon again tomorrow."]] }
    ],
    :after => [
      [:SONA, :neutral, "You're going to ask if Noon is happy. Yes. You're going to ask if I am. ...Come back another day and ask that."]
    ]
  }
})

#===============================================================================
# NADIR - The Gutter Book: Noct and Wick (Umbreon), Mirefen, Chapter 7
#===============================================================================
tr.quest(:NA_OCTAVE_LAMPS_OUT, {
  :trial => :NADIR, :title => "Lamps Out", :giver => "Six-Fingers Ottoline (chalk job) / the marsh ferryman", :map => 220,
  :where => "the ferry steps on the runoff marsh, Mirefen (at night)", :rank => 1, :points => 3, :rec_level => 34,
  :chapter => 7, :unlock => "badges >= 5", :board => true, :tags => [:octave, :night, :moral, :duel],
  :summary => "Chalk job: someone keeps putting out the night-ferry lamps on the marsh. The ferrymen pay a cut to whoever stops it.",
  :steps => { :lamps => "At night, watch the three ferry lamps on the marsh.",
              :noct => "Something with gold rings in the dark put the lamps out. Find the lamplighter.",
              :duel => "Noct wants to know if you can be trusted with the dark." },
  :reward => { :money => 1000, :items => [[:DUSKBALL, 5]] },
  :outcomes => { :truth => { :money => 1000 }, :covered => { :effects => "HOLLOW+1" } },
  :touches => "The Octave: Noct (5 of 8 in gym order); the Gutter Book takes its cut either way",
  :scenes => {
    :offer => [
      { :map => "The ferry steps on the runoff marsh. A ferryman with a pole and a grudge." },
      [:FERRYMAN, :angry, "Every night. Every lamp on the crossing, out, one after another. I've had two boats on the mud this week."],
      [:OTTOLINE, :neutral, "(Chalked on the board above him, in Ottoline's hand:) LAMPS OUT. FERRYMEN PAY. MY CUT'S A FIFTH. IT'S YOURS. DON'T MAKE IT MINE."],
      { :choice => "Take the job?", :options => [
          ["I'll watch the lamps.", [{ :accept => true }, { :step => :lamps }, [:FERRYMAN, :neutral, "Nights only. In the day they behave."]]],
          ["Not my business.", [[:FERRYMAN, :angry, "Nobody's business. That's the business down here."]]]] }
    ],
    :lamp => [
      { :if => "!night", :then => ["The lamp is unlit and harmless in the daylight. Come back after dark.", { :end => true }] },
      { :map => "A ferry lamp on a pole over the black water. As you watch, two gold rings blink in the reeds, and the flame folds down and goes out." },
      { :count => [:lamps, 1] },
      { :if => "quest_count(:SELF, :lamps) >= 3", :then => [
          "The gold rings slip away across the boardwalk, toward the old lamplighter's hut at the end of the steps.",
          { :step => :noct }
        ], :else => ["The gold rings are gone. Another lamp, further out, is still lit. For now."] }
    ],
    :noct => [
      { :map => "The lamplighter's hut. A young man in a soot-black Choir robe, a pole with a hook, and an Umbreon with its rings glowing. Behind him, under a sail, four sleeping children." },
      [:NOCT, :neutral, "...Shh."],
      [:NOCT, :neutral, "Noct. Octave. The lamps are mine. So is putting them out."],
      [:NOCT, :sad, "Sweetrot runners come up the crossing at night looking for lamp-runners. Kids who'll carry for them. They look where it's lit."],
      [:NOCT, :neutral, "Wick puts the lamps out when they come. Dark's the only thing down here that's free."],
      { :choice => "What do you tell the Gutter Book?", :options => [
          ["The truth. The ferrymen should know why.", [
             [:NOCT, :neutral, "...Fine. Tell them. Then they can keep a lookout instead of a grudge."],
             { :flag => [:told, :truth] }]],
          ["Marsh gas. It happens.", [
             [:NOCT, :neutral, "...Marsh gas. Ottoline will know. She'll take her fifth anyway."],
             { :flag => [:told, :covered] }]]] },
      { :step => :duel }, { :run => :duel }
    ],
    :duel => [
      [:NOCT, :neutral, "Wick wants to know if you're safe in the dark. Show it."],
      { :trainer => [:OCTAVE_SINGER, "Noct", 50],
        :won => [
          [:NOCT, :neutral, "...Good. Now you know where the dark is."],
          [:NOCT, :neutral, "Corvin has beds at the infirmary. I'll take them in the morning. Thank you."],
          { :octave_help => :NOCT },
          { :if => "quest_flag(:SELF, :told) == :covered", :then => [{ :complete => :covered }], :else => [{ :complete => :truth }] }],
        :lost => [
          [:NOCT, :neutral, "...Again. When you can see better."]] }
    ],
    :after => [
      [:NOCT, :neutral, "The lamps stay lit now. The kids sleep at Corvin's. Wick sulks. ...It's fine."]
    ]
  }
})

#===============================================================================
# ASHKAAR - The Trial by Flames: Forte and Bellows (Flareon), the Crucible, Chapter 8
#===============================================================================
tr.quest(:AS_OCTAVE_TOO_LOUD, {
  :trial => :ASHKAAR, :title => "Too Loud for the Choir", :giver => "Forte of the Octave", :map => 240,
  :where => "the Crucible on the caldera rim, Cindervault", :rank => 1, :points => 3, :rec_level => 38, :chapter => 8,
  :unlock => "badges >= 6", :board => true, :tags => [:octave, :honesty, :duel],
  :summary => "Writ of Flame: a Choir singer wants a Writ. The Crucible will hear her if she brings a second.",
  :steps => { :ask => "Find the singer outside the Crucible.",
              :legate => "Stand as Forte's second before Legate Varra Kosk.",
              :duel => "The Legate's trial: Forte fights her own second, in the Crucible." },
  :reward => { :money => 2000, :items => [[:HEATROCK, 1]] },
  :touches => "The Octave: Forte (6 of 8 in gym order); Ashkaar honesty (she must say who she is)",
  :scenes => {
    :offer => [
      { :map => "Outside the Crucible's gate a young woman in a scorched Choir robe is arguing with a herald twice her size, and winning on volume." },
      [:FORTE, :angry, "I can fight! Look at me! LOOK at me!"],
      { :map => "The herald walks away. She turns on you, still shouting, then sees your badges and stops." },
      [:FORTE, :happy, "Oh! You're a challenger. Brilliant. Forte. Octave. That's Bellows. Bellows, say hello. Not like that. Not on fire."],
      [:FORTE, :neutral, "I want a Writ of Flame. The Legion. They won't hear a 'Choir child' without a second to stand for her. Will you stand for me?"],
      { :choice => "Stand as Forte's second?", :options => [
          ["I'll stand for you.", [{ :accept => true }, { :step => :legate }, [:FORTE, :happy, "YES. The Legate's inside. Don't let me talk."]]],
          ["Why do you want to join the Legion?", [
             [:FORTE, :neutral, "Because everyone looks at us like we're sad. The Glassfall orphans. Poor things. I'm not a poor thing. I'm loud."],
             [:FORTE, :neutral, "Ask me again when you'll stand for me."]]]] }
    ],
    :legate => [
      { :map => "The Crucible: a sand ring on the caldera rim. Legate Varra Kosk sits on the steps with a ledger on her knee." },
      [:KOSK, :neutral, "You told my herald you were twenty, from the Cinder Cape, and a Legion family. Which of those was true?"],
      [:FORTE, :sad, "...None of them."],
      [:KOSK, :neutral, "Lying is a crime here. Not a large one. It ends the conversation. Unless your second has something to say."],
      { :choice => "What do you say?", :options => [
          ["Tell her who you are, Forte.", [
             [:FORTE, :neutral, "...I'm a Choir orphan. From the Glassfall. I sing. I'm also the strongest person in this ring, and I'm not sorry."],
             [:KOSK, :happy, "There. That's a Writ's worth of truth. Now show me the strong part."]]],
          ["She's the strongest singer you'll ever meet.", [
             [:KOSK, :neutral, "That's your truth, second. I asked for hers."],
             [:FORTE, :neutral, "...I'm a Choir orphan. I sing. And I'm strong. That's all of it."],
             [:KOSK, :happy, "Better. Now show me."]]]] },
      [:KOSK, :neutral, "The trial is simple. Fight your second. Win, or lose well. Both are honest."],
      { :step => :duel }, { :run => :duel }
    ],
    :duel => [
      [:FORTE, :happy, "Don't go easy. If you go easy I'll know and I'll shout."],
      { :trainer => [:OCTAVE_SINGER, "Forte", 50], :field => :VOLCANIC,
        :won => [
          [:FORTE, :happy, "Too loud? ...No. Just right. You were louder."],
          [:KOSK, :neutral, "Lost well. Honestly. That is a Writ."],
          { :map => "The Legate brands an iron token with Forte's mark. Forte holds it up to Bellows, who sneezes on it." },
          { :octave_help => :FORTE }, { :complete => true }],
        :lost => [
          [:KOSK, :neutral, "She won. That's also a Writ, but not for you. Come back when your second can stand."]] }
    ],
    :after => [
      [:FORTE, :happy, "I'm a Legion recruit AND I'm in the Octave. Vesper cried. Happy crying. I think."]
    ]
  }
})

#===============================================================================
# ANTUMBRA - The Rite of Reflection: Lento and Hush (Glaceon), the Mirror Mere, Chapter 13
#===============================================================================
tr.quest(:AN_OCTAVE_STILL_WATER, {
  :trial => :ANTUMBRA, :title => "The Still Water", :giver => "Lento of the Octave (the Rite, read at Glassmere)", :map => 742,
  :where => "the frozen Mirror Mere, past Glassmere (753)", :rank => 1, :points => 4, :rec_level => 58, :chapter => 13,
  :unlock => "badges >= 11", :board => true, :tags => [:octave, :inverse, :duel],
  :summary => "Mirror-writing in the reading-pool: the Mirror Mere froze in summer. Its singer won't leave the ice. Her reflection is under it.",
  :steps => { :ask => "Find the singer on the frozen Mirror Mere.",
              :cracks => "Lector Saffi: in Antumbra you free a thing by holding it backwards. Walk the three cracks in the ice from their ends to their starts.",
              :duel => "The ice is thin and Lento is ready to let go." },
  :reward => { :money => 4000, :items => [[:MIRRORHERB, 1]] },
  :touches => "The Octave: Lento (7 of 8 in gym order); the Rite of Reflection",
  :scenes => {
    :offer => [
      { :map => "The Mirror Mere, frozen white in high summer. In the middle of the ice a woman in Choir grey stands perfectly still beside a Glaceon. Under the ice, her reflection stands upside down, beating softly on it." },
      [:LENTO, :neutral, "Hello. Hello."],
      [:LENTO, :neutral, "I'm Lento. Lento. Of the Octave. I say things twice. Once for me, once for her. Habit. Habit."],
      [:LENTO, :sad, "Reflections wander here. Mine wanted to go. Hush froze the mere so she couldn't. I didn't ask it to. I didn't ask it not to."],
      [:LENTO, :sad, "Now she's under there and I'm up here, and neither of us can leave. Slowly, slowly, I've noticed this is worse."],
      { :choice => "Help Lento?", :options => [
          ["How?", [
             [:LENTO, :neutral, "Lector Saffi would know. She reads the Rite at Glassmere. She'll tell you backwards. Listen backwards."],
             [:SAFFI, :neutral, "(Her mirror-writing in the reading-pool, read in the glass:) TO FREE A THING IN ANTUMBRA, HOLD IT BACKWARDS. WALK EACH CRACK FROM ITS END TO ITS START."],
             { :accept => true }, { :step => :cracks }]],
          ["I'll come back.", [[:LENTO, :neutral, "Slowly. Slowly. We'll be here."]]]] }
    ],
    :crack => [
      { :map => "A long crack across the ice. You find where it ends and walk it back to where it began. Under your feet, the reflection walks it with you, upside down, the other way." },
      { :count => [:cracks, 1] },
      { :if => "quest_count(:SELF, :cracks) >= 3", :then => [
          "On the third crack the ice sighs. It does not break. It just stops holding on.",
          { :map => "Lento's reflection rises to the underside of the ice, presses one hand to it, and lets go. It drifts off across the mere, slowly, toward the Glass." },
          [:REFLECTION, :happy, "(Faint, from under the ice, said once:) Thank you."],
          [:LENTO, :sad, "She only said it once. She's never done that."],
          [:LENTO, :neutral, "It's all right. It's all right. She'll come back. Slowly."],
          { :step => :duel }, { :run => :duel }
        ], :else => ["The ice creaks. It is still holding on."] }
    ],
    :duel => [
      [:LENTO, :neutral, "Hush is upset. Hush is upset. It thinks it did something wrong. Duel us? It needs to do something right."],
      { :trainer => [:OCTAVE_SINGER, "Lento", 50], :field => :FROZEN_LAKE,
        :won => [
          [:LENTO, :happy, "Slowly, slowly. You got there first anyway."],
          [:LENTO, :neutral, "I'm going to write to Vesper. I'm going to write to Vesper. She'll be cross I didn't write sooner. Once."],
          { :octave_help => :LENTO }, { :complete => true }],
        :lost => [
          [:LENTO, :neutral, "Again. Again. When the ice is kinder."]] }
    ],
    :after => [
      [:LENTO, :happy, "She comes back some evenings and stands beside me in the water. Then she goes. That's what reflections are for. For."]
    ]
  }
})

#===============================================================================
# CROWNHAVEN - The Hall of Petitions: Carol and Ribbon (Sylveon), Chapter 20, always last
#===============================================================================
tr.quest(:CR_OCTAVE_NINTH_VERSE, {
  :trial => :CROWNHAVEN, :title => "The Ninth Verse", :giver => "Carol of the Octave", :map => 489,
  :where => "the Glassfall Memorial Garden, Crownhaven", :rank => 1, :points => 4, :rec_level => 88, :chapter => 20,
  :unlock => "switch(155) && octave_helped >= 7", :board => true, :tags => [:octave, :story, :duel],
  :summary => "Petition, sealed in eight waxes: a singer is writing the Octave's Festival song and needs someone who has met them all.",
  :steps => { :ask => "Tell Carol about the other seven singers of the Octave.",
              :duel => "Carol has every verse but the one in the middle, where the fight goes." },
  :reward => { :money => 6000, :items => [[:PPUP, 3]] },
  :touches => "The Octave: Carol (always 8 of 8); she sends for Vesper",
  :scenes => {
    :not_yet => [
      { :map => "Among the glass figures of the Memorial Garden a young woman in Choir white is writing on a slate, with a Sylveon's ribbons wrapped round her wrist." },
      [:CAROL, :happy, "Hello! You're the one Vesper writes about. I'm Carol. I'm the one who never leaves."],
      [:CAROL, :neutral, "I'm writing the Octave's song for the Festival. A verse for everyone. But I can only write what I know, and I don't know what happened to them out there."],
      [:CAROL, :sad, "Some of them haven't written. Have you met them? These ones I haven't heard about:"],
      { :if => "!octave_has(:LYRA)", :then => ["Lyra, in Briarwick."] },
      { :if => "!octave_has(:ARIA)", :then => ["Aria, in Ebbmouth."] },
      { :if => "!octave_has(:CADENCE)", :then => ["Cadence, on the Lowlight steps in Lumen City."] },
      { :if => "!octave_has(:SONA)", :then => ["Sona, at the Temple of the Noon Sun outside Duneholt."] },
      { :if => "!octave_has(:NOCT)", :then => ["Noct, at the ferry steps in Mirefen."] },
      { :if => "!octave_has(:FORTE)", :then => ["Forte, at the Crucible in Cindervault."] },
      { :if => "!octave_has(:LENTO)", :then => ["Lento, on the Mirror Mere past Glassmere."] },
      [:CAROL, :happy, "Come back when you've met them all. I'll be here. I'm always here."]
    ],
    :offer => [
      { :map => "Carol, among the glass figures, with her slate. She has written eight titles on it and nothing else." },
      [:CAROL, :happy, "You've met them all! Everyone's written about you. Sit down, sit down. Tell me everything, in the order it happened."],
      { :accept => true },
      { :octave_verses => {
          :LYRA    => { :run => :verse_lyra },    :ARIA  => { :run => :verse_aria },  :CADENCE => { :run => :verse_cadence },
          :SONA    => { :run => :verse_sona },    :NOCT  => { :run => :verse_noct },  :FORTE   => { :run => :verse_forte },
          :LENTO   => { :run => :verse_lento } } },
      [:CAROL, :neutral, "That's seven. And me, the eighth: the one with no Plate. Ribbon became a Sylveon because it loved me, and I've always thought that meant I was the one without an Imprint."],
      [:CAROL, :happy, "But listening to you, I think the bond is the Imprint. Everyone you met was saved by somebody staying."],
      [:CAROL, :neutral, "Every story needs a fight in the middle, though. That's the verse I can't write. Will you help me with that one too?"],
      { :step => :duel }, { :run => :duel }
    ],
    :verse_lyra    => [[:CAROL, :happy, "Lyra! 'And the moss came down when no one sang.' Oh, that's good. I'm keeping that."]],
    :verse_aria    => [[:CAROL, :happy, "Aria and the river. 'The drowned note rose.' Bersi wrote me eleven pages about that. Eleven."]],
    :verse_cadence => [[:CAROL, :happy, "Cadence kept her job? Cadence kept a JOB? 'And the lamps stayed lit on Block Nine.'"]],
    :verse_sona    => [[:CAROL, :happy, "Sona said you'd tell me that. She said you'd tell it well. 'The bell rang at noon.'"]],
    :verse_noct    => [[:CAROL, :neutral, "Noct doesn't write. Noct sent a lamp wick in an envelope. Now I know what it meant. 'Dark is the only thing that's free.'"]],
    :verse_forte   => [[:CAROL, :happy, "Forte's letter was all capitals. 'TOO LOUD FOR THE CHOIR.' I'm putting it in exactly like that."]],
    :verse_lento   => [[:CAROL, :neutral, "Lento's reflection. 'She said it once.' ...Oh. I'll write that one slowly."]],
    :duel => [
      [:CAROL, :happy, "Ribbon, the middle of the story. Your favourite part."],
      { :trainer => [:OCTAVE_SINGER, "Carol", 50], :field => :FAIRY_TALE,
        :won => [
          [:CAROL, :happy, "And they all lived. That's the whole ending. They all lived."],
          [:CAROL, :neutral, "The song's finished. I have to show Vesper. VESPER!"],
          { :map => "Carol runs off between the roses. Across the garden, the other seven singers are arriving for the Festival, one by one." },
          { :octave_help => :CAROL }, { :complete => true }],
        :lost => [
          [:CAROL, :happy, "The middle's always the hard part. Try again? I'll keep the ending warm."]] }
    ],
    :after => [
      [:CAROL, :happy, "We sing it at dusk. You're in every verse, you know. You're the one who stayed."]
    ]
  }
})
