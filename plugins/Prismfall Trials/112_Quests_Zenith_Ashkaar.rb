#===============================================================================
# Prismfall Trials - 112 Zenith (The Prize Exchange) and Ashkaar (The Trial by
# Flames): their early outposts, Chapters 1-4 (implemented)
#-------------------------------------------------------------------------------
# Zenith (Piltover-like): grants and prizes for data and inventions, posted as
# "Calls for Proposals" on a split-flap board. Before Lumen, the Exchange is a
# Rotom kiosk, P-3NNY, in the Ferrow's Landing customs hall (108), the Saltmere
# Harbour Office (143) and the Ebbmouth Lattice station (160).
# Ashkaar (Noxus-like): strength, arenas, gauntlets, boss Pokemon. Before
# Cindervault, the Legion keeps a recruiting barge in Saltmere's free harbour
# (146): Sergeant Brakka Emberhide, who cannot lie (lying is a crime at home).
#===============================================================================
tr = Prismfall::Trials
tr::SPEAKERS.merge!({
  :PENNY => "P-3NNY", :OFFICER => "Customs officer", :BRAKKA => "Sergeant Brakka", :HERALD => "Barge herald",
  :REKK => "Recruit Rekk", :VASHA => "Recruit Vasha"
})

#===============================================================================
# ZENITH - The Prize Exchange (kiosk P-3NNY)
#===============================================================================
tr.quest(:ZE_FORM_7B, {
  :trial => :ZENITH, :title => "Form 7-B", :giver => "Grant Kiosk P-3NNY", :map => 108,
  :where => "the Quarantine Customs Hall, Ferrow's Landing", :rank => 1, :points => 2, :rec_level => 5, :chapter => 1,
  :unlock => "switch(103)", :board => true, :tags => [:kindness, :bureaucracy, :event_mon, :comedy],
  :summary => "CALL FOR PROPOSALS #0001: DISPOSAL OF UNCLAIMED LIVESTOCK, CRATE 7-B. BOUNTY: $500.",
  :steps => { :ask => "Read Crate 7-B's paperwork at the customs kiosk.",
              :stamps => "Form 7-C (adoption) needs three stamps: Tidewatch Station, the Dockmaster, and the customs duty officer.",
              :warm => "The Charcadet in Crate 7-B is freezing. Take it up to the lighthouse lamp. Hesper keeps it there until you hold two badges." },
  # Revision 16: Charcadet is a Fire type (Tamsin's answer), so the form is filed in Chapter 1 but the crate stays
  # by the lamp until Badge 2; the player collects it on a "2 Badge Quests" trip back down the coast.
  :reward => {},
  :outcomes => { :disposed => { :money => 500, :effects => "MERIDIAN+1" }, :adopted => { :items => [[:POTION, 2]] } },
  :touches => "Meridian standing (+1 if you sign the disposal form); the Charcadet is collected after Badge 2",
  :scenes => {
    :offer => [
      { :map => "A brass kiosk by the scanner gates. Inside the glass, a Rotom has made itself at home in the ticket machine." },
      [:PENNY, :happy, "WELCOME TO THE PRIZE EXCHANGE. I AM GRANT KIOSK P-3NNY. YOU MAY CALL ME PENNY. MOST PEOPLE CALL ME 'THE MACHINE'."],
      [:PENNY, :neutral, "CALL FOR PROPOSALS #0001: DISPOSAL OF UNCLAIMED LIVESTOCK, CRATE 7-B."],
      [:PENNY, :neutral, "THE OWNER WAS ON THE WRONG SIDE OF THE BORDER WHEN IT CLOSED. THE CRATE WILL BE SHIPPED BACK. NOBODY IS THERE TO RECEIVE IT."],
      [:PENNY, :happy, "BOUNTY: $500. PLEASE SIGN FORM 7-B."],
      "Under the kiosk, a stencilled crate shivers. Through the slats, two small flames flicker, very low.",
      { :choice => "Form 7-B?", :options => [
          ["Sign it.", [
             [:PENNY, :happy, "FORM 7-B ACCEPTED. THANK YOU FOR YOUR EFFICIENCY."],
             "A Meridian tech wheels the crate away. As it passes, she murmurs: \"I'll make sure it's somewhere warm. Somewhere.\"",
             { :accept => true }, { :complete => :disposed }]],
          ["Are there other forms?", [
             [:PENNY, :neutral, "FORM 7-C: ADOPTION OF UNCLAIMED LIVESTOCK. REQUIRES THREE STAMPS: RESEARCH, LIVESTOCK AND CUSTOMS."],
             [:PENNY, :neutral, "PROCESSING TIME: SIX TO EIGHT WEEKS."],
             [:PENNY, :happy, "I AM JOKING. I HAVE BEEN PROGRAMMED WITH ONE (1) JOKE. THAT WAS IT."],
             { :accept => true }, { :step => :stamps }]],
          ["Walk away.", []]] }
    ],
    :stamp_larch => [
      { :if => "quest_flag(:SELF, :larch)", :then => [[:LARCH, :neutral, "I've stamped it. Go."], { :end => true }] },
      [:LARCH, :angry, "A Charcadet. In a crate. In a sea fog. Who signs these things?"],
      [:LARCH, :neutral, "Research stamp. Here. It's the station seal. It's also the lid of the teapot. Don't ask."],
      { :flag => [:larch, true] }, { :run => :stamp_check }
    ],
    :stamp_dock => [
      { :if => "quest_flag(:SELF, :dock)", :then => [{ :end => true }] },
      [:DOCKMASTER, :neutral, "Livestock, arriving? Arriving. Something's arriving."],
      { :map => "He stamps the form with great ceremony, three times, to be sure." },
      [:DOCKMASTER, :happy, "First arrival I've stamped since the ferries stopped."],
      { :flag => [:dock, true] }, { :run => :stamp_check }
    ],
    :stamp_customs => [
      { :if => "quest_flag(:SELF, :customs)", :then => [{ :end => true }] },
      [:OFFICER, :deadpan, "Form 7-C? Nobody files 7-C. 7-C is the form we keep so we can say there's a form."],
      { :choice => "Convince the officer.", :options => [
          ["Ask nicely.", [[:OFFICER, :neutral, "...Fine. You asked nicely. Nobody asks nicely in customs."]]],
          ["It'll freeze to death.", [[:OFFICER, :sad, "...Yeah. Yeah, it will. Give it here."]]],
          ["Penny said I could.", [[:OFFICER, :deadpan, "The machine said. Wonderful. Now I've got to stamp it or explain myself to a ticket dispenser."]]]] },
      { :flag => [:customs, true] }, { :run => :stamp_check }
    ],
    :stamp_check => [
      { :if => "quest_flag(:SELF, :larch) && quest_flag(:SELF, :dock) && quest_flag(:SELF, :customs)", :then => [
          "Three stamps. You take Form 7-C back to the kiosk.",
          [:PENNY, :happy, "FORM 7-C ACCEPTED. CRATE 7-B RELEASED TO APPLICANT. ADVISORY: CONTENTS ARE COLD."],
          [:PENNY, :neutral, "ADVISORY, UNOFFICIAL: THE LIGHTHOUSE LAMP IS THE WARMEST PLACE IN FERROW'S LANDING. I HAVE A THERMAL MAP. I HAVE NOTHING ELSE TO DO."],
          { :step => :warm }] }
    ],
    :warm => [
      { :map => "The lighthouse lamp room. Hesper Vane is polishing the lens. She does not turn round." },
      [:HESPER, :angry, "Out."],
      "You set the crate down by the lamp. The two small flames inside it sway toward the light.",
      [:HESPER, :deadpan, "...Put it nearer, then. Not touching the lens. Nobody touches the lens."],
      [:HESPER, :neutral, "Fire-types used to winter up here when I was a girl. The lamp was better company than most people."],
      "The flames climb, steadier, brighter. Something in the crate sits up and looks at you.",
      { :if => "badges >= 2", :then => [
          [:HESPER, :neutral, "It's walking about on its own now. Been sitting by my lens every night, watching the road you went down."],
          [:HESPER, :angry, "Now take it and go. And shut the door. You're letting the warm out."],
          { :gift => :ZE_CHARCADET }, { :complete => :adopted }
        ], :else => [
          [:HESPER, :deadpan, "It'll not last a day on the coast road in this fog. It stays by the lamp till it can walk on its own."],
          [:HESPER, :angry, "Come back when you've two of those badges rattling in your pocket. Not before. And shut the door."],
          "(Hesper will keep the Charcadet by the lamp until you hold two badges.)"
        ] }
    ]
  }
})

tr.quest(:ZE_FIELD_SURVEY, {
  :trial => :ZENITH, :title => "Field Survey: Coastal", :giver => "Grant Kiosk P-3NNY", :map => 108,
  :where => "any P-3NNY kiosk (Ferrow's Landing, Saltmere, Ebbmouth)", :rank => 1, :points => 2, :rec_level => 10, :chapter => 2,
  :unlock => "switch(103)", :requires => [], :board => true, :tags => [:data, :fields],
  :summary => "CALL FOR PROPOSALS #0002: RECORD BATTLES ON THREE (3) DIFFERENT FIELDS. DATA IS THE CURRENCY OF THE FUTURE. SO IS CURRENCY.",
  :steps => { :ask => "Battle on three different fields (your Field Notes count them), then report to any P-3NNY kiosk." },
  :reward => { :items => [[:EXPCANDYS, 3]] },
  :touches => "Field Notes (fields_seen)",
  :scenes => {
    :report => [
      { :if => "fields_seen >= 3", :then => [
          [:PENNY, :happy, "DATA RECEIVED. THREE FIELDS. THE REGISTRY THANKS YOU. THE REGISTRY HAS NEVER THANKED ANYONE BEFORE. THIS IS NEW."],
          { :complete => true }
        ], :else => [
          [:PENNY, :neutral, "DATA INSUFFICIENT. PLEASE BATTLE ON MORE FIELDS. THE COAST, THE STAGE, THE FOREST. ANYWHERE THAT IS NOT HERE."]
        ] }
    ]
  }
})

tr.quest(:ZE_LATTICE_HUM, {
  :trial => :ZENITH, :title => "The Lattice Hums Wrong", :giver => "Grant Kiosk P-3NNY/2", :map => 160,
  :where => "the tidal Lattice station, Ebbmouth", :rank => 1, :points => 3, :rec_level => 20, :chapter => 4,
  :unlock => "badges >= 2", :board => true, :tags => [:data, :mystery, :politics],
  :summary => "CALL FOR PROPOSALS #0003: ACOUSTIC SURVEY OF THE EBBMOUTH TIDAL LATTICE DURING 'STUTTER EVENTS'. RECORDER PROVIDED.",
  :steps => { :ask => "Record the Lattice's hum at the three mill-wheels on the Ebb (the upper wheel, the Guild wheel, the Mill Quay wheel).",
              :choose => "You have three recordings. Decide who gets the data." },
  :reward => { :money => 300 },
  :outcomes => { :meridian => { :money => 1500, :effects => "MERIDIAN+1" }, :guild => { :effects => "MARISOL+1" },
                 :larch => { :items => [[:EXPCANDYS, 2]] } },
  :touches => "Meridian standing or Marisol bond, depending on who gets the recordings (foreshadows Larch's tide data in Ch4)",
  :scenes => {
    :offer => [
      [:PENNY, :happy, "HELLO AGAIN. I AM P-3NNY/2. I AM NOT THE SAME KIOSK. I HAVE BEEN TOLD TO SAY THAT."],
      [:PENNY, :neutral, "THE LATTICE MAKES A SOUND WHEN THE RIVER STUTTERS. MERIDIAN WOULD LIKE TO KNOW WHAT SOUND. FOR SCIENCE. AND FOR LIABILITY."],
      { :choice => "Take the recorder?", :options => [
          ["Take it.", [{ :accept => true }, [:PENNY, :happy, "PLEASE DO NOT DROP IT IN THE RIVER. THE RIVER HAS ENOUGH PROBLEMS."]]],
          ["Not now.", []]] }
    ],
    :wheel_upper => [{ :if => "quest_flag(:SELF, :upper)", :then => [{ :end => true }] },
                     "The upper mill-wheel groans to a stop mid-turn. Under the silence: a low electric whine from the river-mouth pylons.",
                     { :flag => [:upper, true] }, { :run => :recorded }],
    :wheel_guild => [{ :if => "quest_flag(:SELF, :guild)", :then => [{ :end => true }] },
                     "The Guild wheel stops. The dockworkers hold their breath. The whine rises, then drops, like something drinking.",
                     { :flag => [:guild, true] }, { :run => :recorded }],
    :wheel_quay  => [{ :if => "quest_flag(:SELF, :quay)", :then => [{ :end => true }] },
                     "The Mill Quay wheel stops dead. The recorder's needle jumps at the exact moment the whine peaks.",
                     { :flag => [:quay, true] }, { :run => :recorded }],
    :recorded => [
      { :count => [:recordings, 1] },
      { :if => "quest_count(:SELF, :recordings) >= 3", :then => [
          "Three recordings. The stutters and the whine line up every time. You don't know what that means. Someone will.",
          { :step => :choose }] }
    ],
    :choose => [
      [:PENNY, :neutral, "PLEASE SELECT A RECIPIENT. ALL RECIPIENTS ARE EQUALLY VALUED."],
      [:PENNY, :neutral, "(MERIDIAN IS MORE EQUALLY VALUED.)"],
      { :choice => "Who gets the recordings?", :options => [
          ["Meridian, through the kiosk.", [[:PENNY, :happy, "TRANSMITTED. A BONUS HAS BEEN APPLIED. NOBODY WILL LISTEN TO THEM, PROBABLY."], { :complete => :meridian }]],
          ["The Ebb Guild.", ["You take the recorder to the Guild hall. Marisol listens to all three, very still.",
                              [:MARISOL, :angry, "It drinks. When the river stops, it's drinking. Pick one, kid. I know which I'd pick."],
                              { :complete => :guild }]],
          ["Professor Larch, by Gale Post.", ["You post the recordings to Tidewatch Station.",
                                              "A reply comes back by the next Gale Post: \"I had this already. Thank you. Please stop doing my job. - I.L.\"",
                                              { :complete => :larch }]]] }
    ]
  }
})

#===============================================================================
# ASHKAAR - The Trial by Flames (the recruiting barge, Saltmere harbour)
#===============================================================================
tr.quest(:AS_LITTLE_CRUCIBLE, {
  :trial => :ASHKAAR, :title => "The Little Crucible", :giver => "Sergeant Brakka Emberhide", :map => 146,
  :where => "the Legion recruiting barge, Saltmere harbour", :rank => 1, :points => 3, :rec_level => 21, :chapter => 4,
  :unlock => "badges >= 2", :board => true, :tags => [:arena, :gauntlet, :boss, :event_mon],
  # Revision 16: the Legion barge docks in Saltmere after Badge 2 (Litleo is Fire, Tamsin's answer); reached by the Frostflat Causeway.
  :summary => "WRIT OF FLAME: three bouts, back to back, no healing. Then the barge's mascot. Win and the Legion respects you. Lose and the Legion respects you less.",
  :steps => { :ask => "Fight the barge's three recruits in a row (no healing between bouts).",
              :mascot => "The recruits are beaten. Now face Cinderpaw, the barge's mascot." },
  :reward => { :money => 1200, :items => [[:QUICKCLAW, 1]] },
  :touches => "Ashkaar flavour: honesty is law; signing up (flag :recruited) changes how later Legion NPCs greet you",
  :scenes => {
    :offer => [
      { :map => "A black-hulled barge moored at the free harbour, a fire pit on deck ringed with rope. A banner: JOIN THE LEGION. MOST RECRUITS SURVIVE." },
      [:BRAKKA, :smug, "In Ashkaar nobody asks who your mother was. They ask how hard you hit."],
      [:BRAKKA, :neutral, "Saltmere's a free port, so we can hold bouts here. The Elowen crown hates it. That's a bonus."],
      [:BRAKKA, :neutral, "Writ of Flame: three of my recruits, one after another, no potions between. Then you face Cinderpaw."],
      { :choice => "Ask Brakka something?", :options => [
          ["Will I get hurt?", [[:BRAKKA, :neutral, "Yes."], [:BRAKKA, :deadpan, "Lying's a crime where I'm from. You'd be amazed how much faster recruitment goes."]]],
          ["What's Cinderpaw?", [[:BRAKKA, :happy, "Our mascot. A Litleo. Too wild to keep, too proud to leave. Bit three officers. Promoted twice."]]],
          ["Let's fight.", []]] },
      { :choice => "Take the Writ of Flame?", :options => [
          ["Brand me.", [{ :accept => true }, [:BRAKKA, :happy, "Good. HERALD! Ring the pit!"], { :run => :bouts }]],
          ["Not yet.", [[:BRAKKA, :neutral, "Honest answer. I respect that. Come back when it changes."]]]] }
    ],
    :bouts => [
      [:HERALD, :happy, "BOUT ONE! From the Cinder Cape, with a punch like a bad decision: RECRUIT REKK!"],
      { :gauntlet => [[:ASHKAAR_SOLDIER_M, "Rekk", 50], [:ASHKAAR_SOLDIER_F, "Vasha", 50], [:ASHKAAR_OFFICER, "Brakka", 50]],
        :heal_between => false, :field => :COLOSSEUM,
        :won => [[:BRAKKA, :smug, "Three for three. You hit like an Ashkaari. That's the nicest thing I know how to say."],
                 { :step => :mascot }, { :run => :mascot }],
        :lost => [[:BRAKKA, :neutral, "Down. No shame in it. Some shame in it. Heal up and come back; the Writ stays yours."]] }
    ],
    :mascot => [
      [:HERALD, :happy, "AND NOW! UNDEFEATED ON THIS DECK! BITER OF OFFICERS! CINDERPAW!"],
      { :event_battle => :AS_LITLEO,
        :won => ["Cinderpaw shakes its smoking mane, looks at the crew, looks at you... and trots over to sit at your feet.",
                 [:BRAKKA, :shocked, "Huh. It's picked you. It's never picked anybody. It bit the last person who tried to pick it."],
                 [:BRAKKA, :neutral, "Take it. In the Legion, strength chooses strength. Even the little ones."],
                 { :run => :sign }],
        :lost => [[:BRAKKA, :deadpan, "Cinderpaw remains undefeated. Cinderpaw is insufferable about it."]] }
    ],
    :sign => [
      [:BRAKKA, :neutral, "One more thing. Recruitment papers. Sign and you're Legion-in-waiting. Means nothing yet. Means something later."],
      { :choice => "Sign the papers?", :options => [
          ["Sign.", [{ :flag => [:recruited, true] }, [:BRAKKA, :happy, "Ha! Ember-recruit, then. Show that paper in Cindervault and someone will buy you a drink. Or fight you."]]],
          ["Decline.", [[:BRAKKA, :neutral, "Honest. Fine. The offer stands as long as you keep winning."]]]] },
      "The Herald strikes the gong. Your brand goes up on the barge's little Wall of the Proven.",
      { :complete => true }
    ]
  }
})
