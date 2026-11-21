#===============================================================================
# Prismfall Trials - 120 Quest catalogue, Chapters 5+ (designed; :stub => true)
#-------------------------------------------------------------------------------
# Registered so boards, the quest log, the validator and the generated doc all
# see them. Stubs stay off boards in normal play (SHOW_STUBS_IN_DEBUG shows them
# in debug). To wire one: write its :scenes, place its events, drop :stub.
# Chapters follow story/00_OVERVIEW (Ch5 Lumen ... Ch19 Wyrmrest, Ch20-21 Festival);
# a chapter N town is reached holding about N-2 badges. Map IDs per WORLD.md §2.
#===============================================================================
tr = Prismfall::Trials
stub = lambda { |id, h| tr.quest(id, h.merge(:stub => true, :board => h.fetch(:board, true))) }

#===============================================================================
# ELOWEN - The Quiet Way (later)
#===============================================================================
# EL_SHELLY ("Someone Apologising to Bugs") is wired since 2026-11-21: 116_Quests_Early.rb.
stub.call(:EL_GERALD, {
  :trial => :ELOWEN, :title => "Gerald", :giver => "the Queen's Keeper of Small Creatures", :map => 682, :where => "the Royal Chase",
  :rank => 3, :points => 3, :rec_level => 44, :chapter => 10, :unlock => "badges >= 8 && switch(126)", :tags => [:chase, :comedy, :event_mon],
  :summary => "Queen Maelis's named Scatterbugs have escaped into the Royal Chase. Each one has a personality file. Gerald's is four pages long.",
  :steps => { :ask => "Find the six escaped royal Scatterbugs using their personality files.", :gerald => "Only Gerald is left. Gerald does not want to be found." },
  :reward => { :pokemon => :EL_GERALD, :items => [[:SHINYSTONE, 1]] }, :touches => "Elowen Crown favour (flavour); Queen Maelis comedy (15_COMEDY 'The Royal We')",
  :design => "Six hide-and-seek finds, each solved by reading its file (Doris likes warm stones, Percival hates the colour blue...). Gerald hides inside the Queen's own crown on its stand in the hunting lodge. Reward: Gerald, a Fancy-pattern Scatterbug."
})
stub.call(:EL_ROOTWARD_WAKE, {
  :trial => :ELOWEN, :title => "The Rootward Wake", :giver => "a Rootward laundress", :map => 296, :where => "the Rootward slums, Verdance",
  :rank => 3, :points => 3, :rec_level => 44, :chapter => 10, :unlock => "badges >= 8", :tags => [:spiritual, :kindness],
  :summary => "In Verdance nothing rots, so nothing is ever properly buried. The Rootward wants one funeral done right.",
  :steps => { :ask => "Gather the three things an old Elowen wake needs.", :wake => "Hold the wake at the Rootward's dead well." },
  :reward => { :items => [[:CLEANSETAG, 1], [:TM20, 1]] }, :touches => "Resonance; Rowan's theme ('everything that grows must be allowed to die')",
  :design => "Fetch a candle that's allowed to burn out, a flower picked from outside Verdance (it wilts on the way: that's the point) and a song nobody's sung since the Bleed. A Phantump comes to the wake and sits with the mourners. If Rowan's arc has turned (S124), one mourner is a Hollow sympathiser and says so."
})
stub.call(:EL_EVER_BLOOM, {
  :trial => :ELOWEN, :title => "What the Bride Tree Hears", :giver => "Juno", :map => 294, :where => "the Heartgarden, Verdance",
  :rank => 3, :points => 4, :rec_level => 46, :chapter => 10, :unlock => "badges >= 8 && switch(125)", :tags => [:bond, :spiritual, :event_mon],
  :summary => "Juno wants to know whether her Aunt Elin can still hear her. The Quiet Way says the Root carries voices. Juno says she'd like proof.",
  :steps => { :ask => "Help Juno carry a message to the Bride Tree the old way: by root, not by word.", :roots => "Follow the Heartgarden roots down to the place where they listen." },
  :reward => { :pokemon => :EL_EVER_BLOOM, :effects => "JUNO+2" }, :touches => "Juno bond (+2); Elin / Homecoming foreshadowing",
  :design => "A Mindscape-light puzzle under the Heartgarden: the roots repeat whatever you place against them, late, like an echo. Juno places a seed packet. Nothing. She places her bouquet. The roots hum the counting rhyme. Juno laughs and cries at once. Reward: a white Floette grown from the Bride Tree's blossoms (Juno names it Ever-Bloom)."
})
stub.call(:EL_TWILIGHT_CLOISTER, {
  :trial => :ELOWEN, :title => "The Twilight Cloister", :giver => "the Abbess", :map => 440, :where => "the Twilight Cloister, Gloaming",
  :rank => 5, :points => 5, :rec_level => 78, :chapter => 18, :unlock => "badges >= 16", :tags => [:spiritual, :puzzle, :final_trial],
  :summary => "The last trial of the Quiet Way: walk the dusk-chapels from end to end without saying anything at all.",
  :steps => { :ask => "Cross the seven dusk-chapels. Every dialogue choice you're offered is a test; the right answer is always silence.",
              :end => "Reach the eighth chapel." },
  :reward => { :items => [[:MAGICALSEED, 3]] }, :touches => "Resonance (Harmony +2); unlocks the Quiet Way's Evergreen rank",
  :design => "Every chapel stages a scene that begs a response (a child asks the way, a Thornguard insults you, a ghost of someone you failed). Each choice list has a silent option, worded differently each time. Speaking costs nothing but resets you to the first chapel. Celestine watches from the eighth and finally speaks to you as herself."
})

#===============================================================================
# ISENMAR - The Tally (later)
#===============================================================================
stub.call(:IS_WHITE_STAG, {
  :trial => :ISENMAR, :title => "The White Stag", :giver => "the lodge-keeper", :map => 710, :where => "Snowbriar",
  :rank => 2, :points => 3, :rec_level => 48, :chapter => 11, :unlock => "badges >= 9", :tags => [:chase, :event_mon, :politics, :borderland],
  :summary => "A white stag has been seen in the royal hunting woods. Elowen law says it's the Crown's. The trappers say it's nobody's.",
  :steps => { :ask => "Track the white stag through the Northern Rimewood.", :choose => "You've cornered it. Whose law do you follow?" },
  :reward => { :money => 4000 }, :touches => "Elowen vs Isenmar clan rights (WORLD.md 'The White Stag'); Thane's standing flavour",
  :design => "Four-sighting chase in deep snow; it only appears at dawn. At the end: battle and catch (EVENT IS_WHITE_STAG), report it to the Crown's lodge (Elowen points), or let the trappers' children see it once and let it go (Harmony)."
})
stub.call(:IS_HARPOON_RITE, {
  :trial => :ISENMAR, :title => "The Harpoon Rite", :giver => "Old Halla Brinesdottir", :map => 306, :where => "the Great Tally, Rimeholt",
  :rank => 3, :points => 4, :rec_level => 50, :chapter => 11, :unlock => "badges >= 9", :tags => [:boss, :event_mon, :endurance],
  :summary => "Every Harpooner earns the rank by facing the Old Bull on the ice. The Old Bull is a Cetitan. It has never once been harpooned.",
  :steps => { :ask => "Walk out onto Lake Rime at dusk and face the Old Bull.", :bull => "The Old Bull is waiting at the ice-hole." },
  :reward => { :items => [[:NEVERMELTICE, 1]] }, :touches => "Before the Thaw only (expires on S128 CH11_THAW)",
  :design => "Boss Cetitan (3 bars) on :FROZEN_LAKE; the field cracks to :WATER_SURFACE at bar 2. Nobody harpoons it: the rite is to stand your ground. Win and it slaps the ice twice and swims under you (no catch). The calf that follows it out joins you (EVENT IS_CETODDLE)."
})
stub.call(:IS_ELEVEN_YEARS, {
  :trial => :ISENMAR, :title => "Eleven Years at One Hole", :giver => "Old Torstein", :map => 300, :where => "the ice-fishing flats, Rimeholt",
  :rank => 1, :points => 2, :rec_level => 47, :chapter => 11, :unlock => "badges >= 9", :tags => [:comedy, :fishing, :event_mon],
  :summary => "Old Torstein has fished one ice-hole for eleven years waiting for a single bite. He has not noticed he is sitting on an Avalugg.",
  :steps => { :ask => "Help Torstein land the one that got away.", :catch => "Fish his hole with the Super Rod." },
  :reward => { :pokemon => :IS_TATSUGIRI }, :touches => "15_COMEDY Isenmar bit",
  :design => "You fish his hole; a Tatsugiri has been nibbling the bait for eleven years without ever taking the hook. When Torstein stands up to cheer, his 'seat' stands up too. 'How long has that been there?' 'About eleven years, sir.' Reward: the Tatsugiri."
})
stub.call(:IS_SINKING_QUARTER, {
  :trial => :ISENMAR, :title => "The Sinking Quarter", :giver => "a net-mender of Net Row", :map => 309, :where => "the Sinking Quarter, Rimeholt",
  :rank => 3, :points => 4, :rec_level => 52, :chapter => 11, :unlock => "switch(128)", :tags => [:escort, :war],
  :summary => "After the Thaw, the lower town is going under. Three families won't leave without their boat, their grandmother and their Lapras, in that order.",
  :steps => { :ask => "Escort the three families up to the Icewall Gate before the tide.", :gate => "Get them past the Thane's martial-law checkpoint." },
  :reward => { :items => [[:EXPCANDYL, 2]] }, :touches => "Refugee arc (S168 ISENMAR_MARTIAL_LAW); Thane / Anja politics",
  :design => "Timed escort over breaking ice (floes sink after N steps); at the gate the checkpoint officer is an ISENMAR_OFFICER battle or a bribe or Anja's word if her bond is good."
})
stub.call(:IS_ALEXANDRA, {
  :trial => :ISENMAR, :title => "Crystal Sleep", :giver => "Old Halla Brinesdottir", :map => 309, :where => "the sunken lower town, Rimeholt",
  :rank => 3, :points => 3, :rec_level => 56, :chapter => 11, :unlock => "badges >= 10 && switch(128)", :tags => [:cameo, :battle],
  :summary => "Something sleeps in a block of ice in the sunken quarter: a woman, very much alive, very annoyed about it.",
  :steps => { :ask => "Thaw the sleeper in the sunken lower town.", :fight => "She wants to know whether this world is worth waking up in." },
  :reward => { :items => [[:ICYROCK, 1]] }, :touches => "CAMEOS.md #5 'Crystal Sleep' (FESTIVAL_ALEXANDRA)",
  :design => "Board pointer for the Alexandra cameo; her event completes the quest."
})
stub.call(:IS_SAGA_OF_THE_ICE, {
  :trial => :ISENMAR, :title => "The Saga of the Glass Dunes", :giver => "Bersi Gullsong", :map => 921, :where => "Skaldfast",
  :rank => 5, :points => 5, :rec_level => 70, :chapter => 15, :unlock => "badges >= 13", :tags => [:war, :final_trial],
  :summary => "Bersi wants to sing the war. Truthfully, for once. He needs a witness who stood on the glass.",
  :steps => { :ask => "Tell Bersi what really happened on the Glass Dunes.", :sing => "Hear the saga in the great hall of Skaldfast." },
  :reward => { :pokemon => :IS_RANK_LAPRAS }, :touches => "War choices (war_climax / war_terms): the saga's words follow what you chose",
  :design => "Bersi sings the war straight, no exaggeration, and it's the first time the hall goes silent for him: Skaldfast on the sand, the flood, the glass, the bone-carters. His verses use the war choice keys, so the saga is different on every war outcome."
})

#===============================================================================
# ZENITH - The Prize Exchange (later)
#===============================================================================
# ZE_CUSTOMER_SUPPORT is wired since 2026-11-21: 116_Quests_Early.rb.
# ZE_FIZZBOLT is wired since 2026-11-21: 116_Quests_Early.rb.
stub.call(:ZE_LOWLIGHT_LAMPS, {
  :trial => :ZENITH, :title => "Ten Years of Light", :giver => "a Lowlight lamp-tender", :map => 608, :where => "the Lowlight (Shattered)",
  :rank => 2, :points => 3, :rec_level => 28, :chapter => 6, :unlock => "switch(114)", :tags => [:kindness, :bleed, :event_mon],
  :summary => "After the Shatter, someone has been lighting small lamps at the feet of the glassed people. Nobody admits to it.",
  :steps => { :ask => "Find who lights the Lowlight lamps.", :shrine => "Visit Dex's shrine at dusk." },
  :reward => { :pokemon => :ZE_DEX_PICHU }, :touches => "Dex shrine (S164); Homecoming foreshadowing",
  :design => "It's Dex's Pichu, who escaped the Shatter and has been carrying spark-lamps to every glassed figure, starting with his. If you sit by the shrine it comes to you. No battle; it chooses you. It knows Volt Tackle."
})
stub.call(:ZE_ROTOM_RECALL, {
  :trial => :ZENITH, :title => "Product Recall", :giver => "the Lumen Arcade floor manager", :map => 183, :where => "Lumen Arcade Dept. Store",
  :rank => 2, :points => 3, :rec_level => 26, :chapter => 5, :unlock => "badges >= 3", :tags => [:chase, :comedy],
  :summary => "Five display appliances have walked off the shop floor. They were not supposed to be able to walk.",
  :steps => { :ask => "Round up the five possessed appliances on both floors.", :last => "The last one is hiding in the staff kitchen, pretending to be a kettle." },
  :reward => { :items => [[:EXPCANDYM, 2]] }, :touches => "Teaches Rotom forms before the Sluiceworks Rotom",
  :design => "A hide-and-seek in the department store; each appliance (fan, mower, fridge, washer, oven) dashes between counters when you look away. Reward: a voucher the Sluiceworks Rotom can use to change form at the Arcade."
})
stub.call(:ZE_COURIER, {
  :trial => :ZENITH, :title => "Cut Loose", :giver => "a pilot at the anchor-smithy", :map => 730, :where => "Anchorhold",
  :rank => 3, :points => 4, :rec_level => 52, :chapter => 12, :unlock => "badges >= 10", :tags => [:delivery, :smuggling, :event_mon],
  :summary => "Deliver a sealed key-ring to an airship before the embargo inspectors board. The key-ring jingles by itself.",
  :steps => { :ask => "Carry the key-ring up the Mast Glacier to the airship Wren's Folly.", :inspect => "The inspectors are boarding. Decide what to show them." },
  :reward => { :pokemon => :ZE_KLEFKI }, :touches => "Meridian standing (handing it to the inspectors) vs the smugglers (WORLD 'Cut Loose')",
  :design => "The key-ring is a Klefki carrying the airship's ignition keys. Give it up and Meridian thanks you; hide it in your bag and the ship cuts loose, and the Klefki, having nobody left to hold keys for, holds yours."
})
stub.call(:ZE_LAUREATE, {
  :trial => :ZENITH, :title => "The Laureate's Prize", :giver => "Registrar Odalys Venn", :map => 194, :where => "the Prize Exchange, Lumen City",
  :rank => 5, :points => 5, :rec_level => 72, :chapter => 16, :unlock => "badges >= 14", :tags => [:arena, :final_trial, :politics],
  :summary => "The Exchange's highest prize: enter a machine of your own design in the Cogsworth Invention Bout. Your machine is your team.",
  :steps => { :ask => "Register for the Invention Bout at the Strade Works.", :bout => "Three rounds on the Factory field, each round a different handicap." },
  :reward => { :items => [[:ABILITYPATCH, 1]] }, :touches => "Magnus / Meridian politics (MAGNUS_KEPT_FAITH flavour)",
  :design => "Rounds: Steel-only, no items, and Factory-to-Scrapyard mid-battle. The Registrar admits the prize was always rigged for Meridian entrants and that you won anyway."
})

#===============================================================================
# NADIR - The Gutter Book
#===============================================================================
stub.call(:NA_CLEAN_WATER, {
  :trial => :NADIR, :title => "Clean Water", :giver => "a char-burner", :map => 630, :where => "Charwell",
  :rank => 1, :points => 3, :rec_level => 32, :chapter => 7, :unlock => "badges >= 5", :tags => [:delivery, :politics, :borderland],
  :summary => "Ossarian bone-char filters clean Nadir's poison. Someone is skimming the filter carts. Find who, then decide who you tell.",
  :steps => { :ask => "Follow the filter carts from the char-pits to the sump-folk.", :choose => "You know who's skimming. Who gets to know?" },
  :reward => { :money => 3000 }, :touches => "Hollow vs Meridian standing (WORLD 'Clean Water')",
  :design => "The skimmer is a sump-folk grandmother selling filters to families the cart route skips. Tell Meridian (MERIDIAN+1), tell the Hollow (HOLLOW+1), or reroute the carts yourself (a puzzle on the canal locks; Harmony)."
})
stub.call(:NA_NOODLE_SCORE, {
  :trial => :NADIR, :title => "A Five Out of Ten", :giver => "the noodle-cart cook", :map => 220, :where => "Mirefen",
  :rank => 1, :points => 2, :rec_level => 32, :chapter => 7, :unlock => "badges >= 5", :tags => [:comedy, :event_mon],
  :summary => "Mirefen's noodle cart rates its customers out of ten. Nobody has scored above a four. Corvin has a two and comes daily.",
  :steps => { :ask => "Find out how the noodle cart scores people.", :score => "Earn a five." },
  :reward => { :pokemon => :NA_GRIMER }, :touches => "15_COMEDY Nadir bit; Corvin (Ch7)",
  :design => "The score isn't about manners: it's about whether you notice the cook's Alolan Grimer cleaning the pots. Thank the Grimer and you get a five (the first ever). The cook, overcome, gives you one of its babies. Corvin demands a recount."
})
stub.call(:NA_GUTTER_DEBTS, {
  :trial => :NADIR, :title => "Mother Gutter's Ledger", :giver => "Mother Gutter", :map => 423, :where => "the Moon Market, Underveil",
  :rank => 3, :points => 4, :rec_level => 72, :chapter => 17, :unlock => "badges >= 15", :tags => [:moral, :battle],
  :summary => "Collect five debts for the oldest sump-baron in Nadir. Or don't collect them. She'll know either way.",
  :steps => { :ask => "Visit the five debtors on Mother Gutter's list.", :return => "Bring Mother Gutter her money. Or her excuses." },
  :reward => { :money => 8000 }, :touches => "Nadir independence arc (S149); Nyx bond flavour",
  :design => "Each debtor has a reason (a sick Pokemon, a Mandate fine, a lie). You can pay one debt yourself, forgive one, fight one. Mother Gutter rewards whatever you did, as long as you did it on purpose. Her Muk is the size of a cart and attends the meeting."
})
stub.call(:NA_PIT_RINGER, {
  :trial => :NADIR, :title => "Pit Ringer", :giver => "the Iron Pit announcer", :map => 263, :where => "the Iron Pit, Ironreach",
  :rank => 2, :points => 4, :rec_level => 41, :chapter => 9, :unlock => "badges >= 7", :tags => [:arena, :gauntlet, :event_mon],
  :summary => "An unlicensed pit in the old mine shafts: six fights, no breaks, and the house brings a brass formation for the last one.",
  :steps => { :ask => "Win six bouts in a row in the Iron Pit.", :formation => "The final bout: the Brass Formation." },
  :reward => { :pokemon => :NA_FALINKS }, :touches => "Kaito / Ironreach Open foreshadowing; the announcer narrates everything (15_COMEDY)",
  :design => "Gauntlet on :COLOSSEUM with crowd-mood effects; the last bout is a boss Falinks whose break summons the rest of the troop. Win and the troop's runt follows you out."
})
stub.call(:NA_LIFT_STRIKE, {
  :trial => :NADIR, :title => "The Lift Strike", :giver => "the lift-workers' union", :map => 830, :where => "Midstair",
  :rank => 3, :points => 4, :rec_level => 70, :chapter => 16, :unlock => "badges >= 14", :tags => [:politics, :escort, :borderland],
  :summary => "The cable-lift workers have stopped every lift between Zenith and Nadir. The Directorate wants them moving by morning.",
  :steps => { :ask => "Talk to both sides of the Midstair lift strike.", :choose => "Carry the union's demands up, or the Directorate's orders down." },
  :reward => { :money => 6000 }, :touches => "Meridian vs Hollow standing; Mandate (S115) state",
  :design => "A vertical map of stalled lift cages; you climb between them. The Directorate officer is a MERIDIAN_DIRECTORATE battle if you side with the union."
})
stub.call(:NA_LAMPLIGHTER_KIDS, {
  :trial => :NADIR, :title => "Lamplighter Kids", :giver => "Pip's friend from the lamp-runners", :map => 260, :where => "Ironreach",
  :rank => 2, :points => 3, :rec_level => 40, :chapter => 9, :unlock => "badges >= 7", :tags => [:escort, :rescue],
  :summary => "Three lamp-runner children went into the old sumps after a rumour of treasure. Their lamps are running out.",
  :steps => { :ask => "Find the three lamp-runners in the flooded shafts.", :out => "Lead them out before the last lamp dies." },
  :reward => { :items => [[:EXPCANDYM, 3]] }, :touches => "none",
  :design => "Darkness puzzle: each found child carries a lamp that lights a radius; you choose the route by which shafts their lamps can reach. The 'treasure' is a Sableye's gem hoard, which the Sableye would like back."
})
stub.call(:NA_SWEETROT, {
  :trial => :NADIR, :title => "Sweetrot", :giver => "a Sweetrot vendor", :map => 423, :where => "the Moon Market, Underveil",
  :rank => 4, :points => 4, :rec_level => 76, :chapter => 18, :unlock => "switch(150)", :tags => [:mystery, :event_mon],
  :summary => "The Sweetrot vendors woke from Pecharunt's spell craving tea. Terrible tea. One cup in particular.",
  :steps => { :ask => "Find the tea the vendors keep asking for.", :cup => "Brew it." },
  :reward => { :pokemon => :NA_POLTCHAGEIST }, :touches => "Running gag 1 (Larch's kelp tea)",
  :design => "The only tea bitter enough is Larch's kelp tea. Bring a cup (mailed from Tidewatch at your request, with a furious note). A Poltchageist climbs into the cup and refuses to leave."
})
stub.call(:NA_VENAM, {
  :trial => :NADIR, :title => "Sewer Royalty", :giver => "Six-Fingers Ottoline", :map => 644, :where => "the Miasma Caverns under Mirefen",
  :rank => 2, :points => 3, :rec_level => 38, :chapter => 7, :unlock => "badges >= 6 && switch(118)", :tags => [:cameo, :battle],
  :summary => "Somebody has crowned herself queen of the Miasma Caverns. Ottoline wants to know who's charging tolls on her sumps.",
  :steps => { :ask => "Find the 'queen' of the Miasma Caverns.", :fight => "She settles disputes the usual way." },
  :reward => { :items => [[:BLACKSLUDGE, 1]] }, :touches => "CAMEOS.md #2 'Sewer Royalty' (FESTIVAL_VENAM)",
  :design => "Board pointer for the Venam cameo; her event completes the quest."
})
stub.call(:NA_GARRET, {
  :trial => :NADIR, :title => "Two Lucarios", :giver => "Six-Fingers Ottoline", :map => 263, :where => "Ironreach's lower shafts",
  :rank => 3, :points => 3, :rec_level => 46, :chapter => 9, :unlock => "switch(123)", :tags => [:cameo, :battle],
  :summary => "A foreign trainer is asking every pit-fighter in Ironreach the same question about his Lucario.",
  :steps => { :ask => "Find the foreigner in the lower shafts.", :fight => "Answer his question in battle." },
  :reward => { :items => [[:BLACKBELT, 1]] }, :touches => "CAMEOS.md #3 'Two Lucarios' (FESTIVAL_GARRET)",
  :design => "Board pointer for the Garret cameo; his event completes the quest."
})

#===============================================================================
# ASHKAAR - The Trial by Flames (the Crucible, Cindervault)
#===============================================================================
stub.call(:AS_SEVEN_BOUTS, {
  :trial => :ASHKAAR, :title => "Seven Bouts", :giver => "Legate Varra Kosk", :map => 240, :where => "the Crucible, Cindervault",
  :rank => 1, :points => 4, :rec_level => 38, :chapter => 8, :unlock => "badges >= 6", :tags => [:arena, :gauntlet],
  :summary => "The Crucible's entry rite: seven legion fighters, back to back, on the caldera floor. No items. No healing. No complaining.",
  :steps => { :ask => "Win seven bouts in a row on the Crucible floor.", :brand => "Receive your brand from the Legate." },
  :reward => { :items => [[:CHARCOAL, 1], [:FIRESTONE, 1]] }, :touches => "Ashkaar recruitment flag from the Saltmere barge is honoured here (skip bout 1)",
  :design => "Volcanic field; each bout raises the field's heat stage. Bout 4 is a double. Bout 7 is the Legate's adjutant on a Dragon's Den preview. The Herald introduces you with whatever the Saltmere barge called you."
})
stub.call(:AS_DRUDDIGON, {
  :trial => :ASHKAAR, :title => "The Lava-Tube Terror", :giver => "a Hearthguild smith", :map => 664, :where => "The Cinderhorn",
  :rank => 2, :points => 4, :rec_level => 40, :chapter => 8, :unlock => "badges >= 6", :tags => [:boss, :hunt, :event_mon],
  :summary => "A Druddigon has made the Cinderhorn lava tubes its own. Three smiths' Pokemon came back scorched. The Legion wants it beaten, not killed.",
  :steps => { :ask => "Track the Druddigon through the lava tubes (follow the scorched claw marks).", :den => "Fight it in its den." },
  :reward => { :pokemon => :AS_DRUDDIGON }, :touches => "Honesty law: report how the fight really went (lying costs the reward)",
  :design => "Boss Druddigon (Rough Skin, 2 bars) on :VOLCANIC; it joins after. Back at the Crucible the Herald asks how it went. Exaggerate (Isenmar-style) and you're fined for lying."
})
stub.call(:AS_ADEQUATE_SWORDS, {
  :trial => :ASHKAAR, :title => "Adequate Swords", :giver => "the owner of ADEQUATE SWORDS", :map => 240, :where => "Cindervault market",
  :rank => 1, :points => 2, :rec_level => 38, :chapter => 8, :unlock => "badges >= 6", :tags => [:comedy, :battle],
  :summary => "A rival shop has opened across the street: EXCELLENT SWORDS. The owner of ADEQUATE SWORDS suspects a lie. Lying is a crime.",
  :steps => { :ask => "Find out whether EXCELLENT SWORDS is lying.", :court => "Bring your evidence to the Honest Court." },
  :reward => { :items => [[:METALCOAT, 1]] }, :touches => "15_COMEDY Ashkaar honest-signs bit",
  :design => "You test the swords (a battle against the rival smith's Honedge on a 'sharpness' rule). The swords are excellent. ADEQUATE SWORDS loses the case, renames itself ADEQUATE SWORDS (STILL), and is happier."
})
stub.call(:AS_AFRAID_OF_HEIGHTS, {
  :trial => :ASHKAAR, :title => "Afraid of Heights", :giver => "Recruit Tamm", :map => 248, :where => "the Dragon Roosts, Cindervault",
  :rank => 2, :points => 3, :rec_level => 40, :chapter => 8, :unlock => "badges >= 6", :tags => [:comedy, :training, :event_mon],
  :summary => "A dragon-rider recruit is afraid of heights and has been assigned a Trapinch 'until he's ready'. He has been not-ready for two years.",
  :steps => { :ask => "Help Tamm train his Trapinch until it evolves.", :flight => "Vibrava wants to fly. Tamm does not." },
  :reward => { :pokemon => :AS_NOIBAT }, :touches => "15_COMEDY Ashkaar bit",
  :design => "Three training battles with Tamm's Trapinch in your party as a guest. When it becomes a Vibrava it takes Tamm three feet off the ground and he screams with joy. He gives you the Noibat he was also assigned, because 'it looks at me like it knows'."
})
stub.call(:AS_ASHES, {
  :trial => :ASHKAAR, :title => "Ashes Home", :giver => "the Legion quartermaster", :map => 650, :where => "Scaldwater",
  :rank => 2, :points => 4, :rec_level => 37, :chapter => 8, :unlock => "badges >= 6", :tags => [:escort, :kindness, :event_mon, :war],
  :summary => "A Nadir-born legionnaire died at the caldera. His Houndour won't leave his urn. Somebody has to carry both of them home to Scaldwater.",
  :steps => { :ask => "Carry the urn (and the Houndour) along the Sulfur Reach to Scaldwater.", :home => "Find his mother's house in Scaldwater." },
  :reward => { :pokemon => :AS_HOUNDOUR }, :touches => "War arc: Ashkaar recruiting Nadir youths (WORLD border E); Harmony",
  :design => "No battles unless you take the short road (Legion deserters who want the urn's silver). At the door the mother takes the urn and tells the Houndour to go and keep marching, with someone who will come back."
})
stub.call(:AS_EGG_RUN, {
  :trial => :ASHKAAR, :title => "The Egg Run", :giver => "the Roost-mistress", :map => 248, :where => "the Dragon Roosts, Cindervault",
  :rank => 3, :points => 4, :rec_level => 42, :chapter => 9, :unlock => "badges >= 7", :tags => [:escort, :stealth, :event_mon],
  :summary => "Carry a warm dragon egg across the Cinderhorn to the far roost. Egg-hunters know the route. The egg must not get cold.",
  :steps => { :ask => "Cross the Cinderhorn with the egg; stay near lava vents to keep it warm.", :roost => "Hand the egg over at the far roost." },
  :reward => { :pokemon => :AS_AXEW_EGG }, :touches => "none; earliest Axew (wild only from Badge 17)",
  :design => "A warmth meter (steps since the last vent) instead of a timer; egg-hunter ambushes (trainer battles) at the vents. At the far roost the egg hatches early in your hands. It decides you're its roost."
})
stub.call(:AS_TRIAL_OF_TRUTH, {
  :trial => :ASHKAAR, :title => "The Trial of Truth", :giver => "Herald Pyke", :map => 247, :where => "the Hall of Oaths, Cindervault",
  :rank => 3, :points => 4, :rec_level => 41, :chapter => 8, :unlock => "badges >= 6 && switch(120)", :tags => [:battle, :moral],
  :summary => "Ashkaar judges a lie by combat. A Hearthguild officer swears the caldera crisis wasn't the Legion's fault. You were there.",
  :steps => { :ask => "Testify in the Hall of Oaths about the caldera crisis.", :duel => "If your word contradicts his, you fight for it." },
  :reward => { :items => [[:FLAMEORB, 1]] }, :touches => "Caldera result (V110) and Brann's bond flavour; Ashkaar war politics (S121)",
  :design => "Whatever you say is a choice with consequences; contradicting the officer starts an ASHKAAR_OFFICER duel on :VOLCANIC under 'oath rules' (if you switch, you concede). Win and the Legion admits fault publicly, which nobody in the hall has seen before."
})
stub.call(:AS_DRAGONSWORN, {
  :trial => :ASHKAAR, :title => "Dragonsworn", :giver => "Legate Varra Kosk", :map => 460, :where => "the Wyrmrest proving ground",
  :rank => 5, :points => 5, :rec_level => 83, :chapter => 19, :unlock => "badges >= 17", :tags => [:arena, :boss, :final_trial],
  :summary => "The highest brand in Ashkaar. Stand in the Dragon's Den and fight the Legate's own dragon while the legions watch.",
  :steps => { :ask => "Face the Legate on the Dragon's Den.", :sworn => "Take the oath, or refuse it." },
  :reward => { :items => [[:LIFEORB, 1]] }, :touches => "DOMINAR_SWAYED flavour; Sigrun bond (she watches)",
  :design => "ASHKAAR_OFFICER Legate team ending in a boss Haxorus. Afterwards you're offered the Dragonsworn oath (to the Dominar). Refusing is also honoured: 'Strength that won't kneel. Good.'"
})

#===============================================================================
# OSSARIA - The Rolls of Unearthing
#===============================================================================
stub.call(:OS_KEVIN, {
  :trial => :OSSARIA, :title => "Kevin", :giver => "the Dig Lab interns", :map => 209, :where => "the Dig Lab, Duneholt",
  :rank => 1, :points => 2, :rec_level => 29, :chapter => 6, :unlock => "badges >= 4", :tags => [:comedy, :mystery, :event_mon],
  :summary => "The interns revived a fossil they can't identify. They call it Kevin. Kevin is a rock. Kevin is in the staff photo.",
  :steps => { :ask => "Find out what Kevin is.", :wake => "Kevin needs something to wake it." },
  :reward => { :pokemon => :OS_CARBINK }, :touches => "15_COMEDY Ossaria bit",
  :design => "Three tests (light, sound, being talked to kindly) over three visits. On the third Kevin turns out to be a Carbink that was asleep, and it has been listening to the interns' gossip for a month. It knows everything."
})
stub.call(:OS_RIDDLE_CARAVAN, {
  :trial => :OSSARIA, :title => "The Riddle Trader", :giver => "a caravan trader", :map => 610, :where => "Copperdune caravanserai",
  :rank => 1, :points => 2, :rec_level => 27, :chapter => 6, :unlock => "badges >= 4", :tags => [:puzzle, :comedy, :borderland, :event_mon],
  :summary => "A caravan trader only barters in riddles. She doesn't know the answers either. She wants you to find them.",
  :steps => { :ask => "Solve the trader's three riddles by finding their answers around Copperdune.", :trade => "Trade the answers." },
  :reward => { :pokemon => :OS_TRAPINCH }, :touches => "15_COMEDY Ossaria bit",
  :design => "The riddles have real answers hidden in Copperdune (a buried locomotive, a mural, a Sandile who only comes out at noon). When you give her the third answer she says 'Oh! I always thought it was a goat,' and pays you in a Trapinch."
})
stub.call(:OS_TOMB_FREIGHT, {
  :trial => :OSSARIA, :title => "Tomb Freight", :giver => "the freight-depot foreman", :map => 610, :where => "Copperdune",
  :rank => 2, :points => 3, :rec_level => 30, :chapter => 6, :unlock => "badges >= 4", :tags => [:mystery, :politics, :borderland],
  :summary => "A locked railway car bound for Lumen is heavier than its manifest. Meridian says machine parts. The tomb-guild says grave goods.",
  :steps => { :ask => "Find out what's really in car nine.", :choose => "Return it to the tombs, let it go to Lumen, or sell the information." },
  :reward => { :money => 3500 }, :touches => "Meridian vs Ossarian Electors (WORLD 'Tomb Freight'); Prince-Elector Kassan",
  :design => "Stealth into the depot at night; the car holds an Elector's sarcophagus with an Unown inscription that names the Prismfall."
})
stub.call(:OS_SINKFIELD, {
  :trial => :OSSARIA, :title => "Something in the Sinkholes", :giver => "a Sinkwells water-carrier", :map => 628, :where => "Sinkfield",
  :rank => 2, :points => 4, :rec_level => 31, :chapter => 7, :unlock => "badges >= 5", :tags => [:boss, :rescue, :bleed, :event_mon],
  :summary => "Something flat and grinning is dragging water-carriers' Pokemon into the Sinkfield sinkholes.",
  :steps => { :ask => "Go into Sinkfield (only you can) and find what's in the sinkholes.", :boss => "It's waiting where the sand moves." },
  :reward => { :pokemon => :OS_STUNFISK }, :touches => "Bleed zone; Imprinted variant",
  :design => "Boss Galarian Stunfisk (trap-jaw) on :DESERT/:BLEED that hides in random sinkholes between turns of a little overworld puzzle; beaten, it gives back the carriers' Pokemon and joins."
})
stub.call(:OS_UNQUIET_ELECTOR, {
  :trial => :OSSARIA, :title => "The Unquiet Elector", :giver => "an embalmer of Vigil", :map => 770, :where => "Vigil",
  :rank => 3, :points => 4, :rec_level => 62, :chapter => 14, :unlock => "badges >= 12", :tags => [:spiritual, :mystery, :event_mon, :borderland],
  :summary => "A dead Elector keeps walking out of his tomb-mirror to vote. The Veiled Synod says the dead are theirs. Vigil says the dead are Vigil's.",
  :steps => { :ask => "Find out what the Elector wants.", :vote => "Hold one last election, for him." },
  :reward => { :pokemon => :OS_YAMASK }, :touches => "Tomb-law vs the Synod (WORLD 'The Unquiet Elector'); Antumbra joint points",
  :design => "A mirror-mystery across the Obsidian Barrows; the Elector never got to cast the vote that would have stopped the Prince-Elector's grandfather. You stage it. He votes, and rests. His Galarian Yamask stays with you."
})
stub.call(:OS_UNOWN_MURALS, {
  :trial => :OSSARIA, :title => "The Mural Gallery's Missing Letter", :giver => "Curator-Elect Nasrin Vael", :map => 207, :where => "the Mural Gallery, Duneholt",
  :rank => 2, :points => 3, :rec_level => 30, :chapter => 6, :unlock => "switch(116)", :tags => [:puzzle, :lore],
  :summary => "One Unown is missing from the gallery's great inscription, and the sentence is wrong without it.",
  :steps => { :ask => "Find the missing Unown letter in the Ossuary of Dunes.", :read => "Read the corrected inscription." },
  :reward => { :items => [[:TM28, 1]] }, :touches => "Lore (Prismfall, Legend Plate seed)",
  :design => "Catch the Unown form the sentence needs (the inscription tells you which by grammar). The corrected sentence reads differently from the one Sahar teaches: 'nineteen fell'."
})
stub.call(:OS_UNDERSANDS, {
  :trial => :OSSARIA, :title => "Where the Well Went", :giver => "Sahar's foreman", :map => 783, :where => "the Duneholt Undersands",
  :rank => 4, :points => 4, :rec_level => 62, :chapter => 14, :unlock => "badges >= 12 && switch(137)", :tags => [:dungeon, :escort],
  :summary => "Duneholt's well is dry. The diggers think the water went down. They want someone to follow it.",
  :steps => { :ask => "Escort the dig crew into the Undersands.", :spring => "Find where the water went." },
  :reward => { :items => [[:TELLURICSEED, 2], [:EXPCANDYL, 2]] }, :touches => "Groudon arc prelude (S140); V109 DUNEHOLT_WELL",
  :design => "Strength-boulder escort through collapsing galleries; the crew can fall behind. At the bottom: warm stone breathing like something asleep."
})
stub.call(:OS_BONEWRIGHT, {
  :trial => :OSSARIA, :title => "The Bonewright's Rite", :giver => "Curator-Elect Nasrin Vael", :map => 360, :where => "Cragholm",
  :rank => 5, :points => 5, :rec_level => 64, :chapter => 14, :unlock => "badges >= 13", :tags => [:fossil, :final_trial],
  :summary => "Reassemble a whole fossil skeleton from the pieces the Rolls have collected across Ossaria, in the right order, in front of the Curators.",
  :steps => { :ask => "Bring the five fossil pieces (one from each Ossarian dig) to Cragholm.", :assemble => "Assemble the skeleton." },
  :reward => { :items => [[:ABILITYCAPSULE, 1]] }, :touches => "Cragholm fossil revival (POKEMON_AVAILABILITY §2)",
  :design => "A drag-and-place puzzle; wrong orders produce a creature that the Curators politely call 'Kevin II'."
})

#===============================================================================
# ANTUMBRA - The Rite of Reflection
#===============================================================================
stub.call(:AN_OTHER_HALF, {
  :trial => :ANTUMBRA, :title => "Your Other Half", :giver => "a Glassmere fisherwoman", :map => 753, :where => "Glassmere",
  :rank => 1, :points => 3, :rec_level => 56, :chapter => 13, :unlock => "badges >= 11", :tags => [:mystery, :spiritual, :event_mon, :borderland],
  :summary => "Her husband came back from the Mere reversed: left-handed, kinder, and worse at fishing. She'd like the old one back. Probably.",
  :steps => { :ask => "Find the original husband on the other side of the Mere.", :choose => "Two husbands. One house." },
  :reward => { :pokemon => :AN_INDEEDEE }, :touches => "WORLD 'Your Other Half'; mirror gag (running gag 8)",
  :design => "Swap through the Mere twice; the reflection doesn't want to go back. The fisherwoman chooses (you can influence it). The couple's Indeedee also came back reversed, and stays with you."
})
stub.call(:AN_UMBRELLA, {
  :trial => :ANTUMBRA, :title => "It Keeps the Rain In", :giver => "a man with an umbrella", :map => 743, :where => "the Antumbra Threshold",
  :rank => 1, :points => 2, :rec_level => 55, :chapter => 13, :unlock => "badges >= 11", :tags => [:comedy, :puzzle, :event_mon],
  :summary => "His umbrella keeps the rain in. He'd like it to keep the rain out. He's tried holding it the other way up. That keeps the rain up.",
  :steps => { :ask => "Fix the umbrella using Inverse logic." },
  :reward => { :pokemon => :AN_HATENNA }, :touches => "15_COMEDY Antumbra bit",
  :design => "The answer is to open it indoors (which is outdoors here). The tiny storm inside it was a Hatenna that hates noise and was hiding from the Threshold's echoes; it comes with you."
})
stub.call(:AN_STUDENT, {
  :trial => :ANTUMBRA, :title => "Better Marks", :giver => "a Lucent student", :map => 344, :where => "the Athenaeum, Lucent",
  :rank => 2, :points => 3, :rec_level => 58, :chapter => 13, :unlock => "badges >= 11", :tags => [:comedy, :battle],
  :summary => "Her reflection has been attending lectures for her. It gets better marks. She is furious and wants to sit the final herself.",
  :steps => { :ask => "Distract the reflection on exam morning.", :exam => "Help her pass without it." },
  :reward => { :items => [[:TWISTEDSPOON, 1]] }, :touches => "15_COMEDY Antumbra bit",
  :design => "Battle the REFLECTION trainer type (her team, mirrored). She passes with a lower mark than her reflection got, and is prouder of it."
})
stub.call(:AN_GIMMIGHOUL_COINS, {
  :trial => :ANTUMBRA, :title => "Nine Hundred and Ninety-Nine", :giver => "a lantern-priest", :map => 380, :where => "Gravenmoor",
  :rank => 2, :points => 3, :rec_level => 64, :chapter => 15, :unlock => "badges >= 13", :tags => [:collection],
  :summary => "Gimmighoul coins keep turning up in the Gravenmoor collection plates. The priests want to know where they're coming from.",
  :steps => { :ask => "Follow the coin trail across Antumbra.", :chest => "Find the chest the coins came out of." },
  :reward => { :items => [[:RELICGOLD, 1]] }, :touches => "POKEMON_AVAILABILITY §3 Gimmighoul hunt",
  :design => "Wraps the existing Gimmighoul coins hunt in a Trial quest; the chest is a Gimmighoul who has been tithing."
})
stub.call(:AN_ECHO_HALL, {
  :trial => :ANTUMBRA, :title => "The Echo That Answers First", :giver => "Lector Saffi Ivarne", :map => 346, :where => "the Speculum, Lucent",
  :rank => 3, :points => 4, :rec_level => 60, :chapter => 13, :unlock => "badges >= 12", :tags => [:puzzle],
  :summary => "An echo in the Speculum answers questions before they're asked. The Lectors would like to ask it one.",
  :steps => { :ask => "Work out which question the echo is already answering.", :ask_it => "Ask it." },
  :reward => { :items => [[:TM48, 1]] }, :touches => "Mindscape lore; Ilsa (Ch13) foreshadowing",
  :design => "A reverse-dialogue puzzle: answers come first and you assemble the question from them."
})
stub.call(:AN_SHADOWS_UP, {
  :trial => :ANTUMBRA, :title => "Shadows Fall Upward", :giver => "a Vigil medium", :map => 760, :where => "the Obsidian Barrows",
  :rank => 3, :points => 4, :rec_level => 60, :chapter => 13, :unlock => "badges >= 12", :tags => [:puzzle, :borderland],
  :summary => "In the Barrows, shadows fall upward. Somebody's shadow has fallen all the way up and got stuck on the inverted desert in the sky.",
  :steps => { :ask => "Get the shadow down.", :return => "Reunite it with its owner." },
  :reward => { :items => [[:ELEMENTALSEED, 2]] }, :touches => "Antumbra / Ossaria borderland I",
  :design => "Light-source puzzle on the Inverse field: move lamps so the stuck shadow is cast back down onto the sand."
})
stub.call(:AN_BEHIND_THE_GLASS, {
  :trial => :ANTUMBRA, :title => "Behind the Glass", :giver => "Archseer Dask's reflection", :map => 347, :where => "the Palace of Glass, Lucent",
  :rank => 5, :points => 5, :rec_level => 70, :chapter => 15, :unlock => "badges >= 14 && switch(143)", :tags => [:final_trial, :spiritual],
  :summary => "Antumbra's last rite: spend one night as your own reflection.",
  :steps => { :ask => "Step through the Archseer's mirror.", :night => "Live one night on the wrong side of the glass." },
  :reward => { :items => [[:ABILITYPATCH, 1]] }, :touches => "Mirror gag payoff (running gag 8); Ruin Route seed",
  :design => "A short playable stretch as the PC's reflection, which sees everything the PC did and has opinions. No joke after this one is safe in a mirror."
})
stub.call(:AN_SHIV, {
  :trial => :ANTUMBRA, :title => "Dreamwalker", :giver => "Lector Saffi Ivarne", :map => 440, :where => "the dusk-chapels of Gloaming",
  :rank => 4, :points => 3, :rec_level => 82, :chapter => 18, :unlock => "badges >= 17", :tags => [:cameo, :battle],
  :summary => "A stranger has been walking through other people's dreams in Gloaming and leaving them better rested. The Lectors want a word.",
  :steps => { :ask => "Find the dreamwalker in the dusk-chapels.", :fight => "Fight her inside the dream." },
  :reward => { :items => [[:MAGICALSEED, 1]] }, :touches => "CAMEOS.md #7 'Dreamwalker' (FESTIVAL_SHIV)",
  :design => "Board pointer for the Shiv cameo; her event completes the quest."
})

#===============================================================================
# CROWNHAVEN - The Hall of Petitions
#===============================================================================
stub.call(:CR_EIGHTEEN_SHRINES, {
  :trial => :CROWNHAVEN, :title => "Eighteen Shrines", :giver => "the Pilgrim's Rest keeper", :map => 890, :where => "Pilgrim's Rest",
  :rank => 1, :points => 4, :rec_level => 85, :chapter => 20, :unlock => "badges >= 18", :tags => [:pilgrimage],
  :summary => "Eighteen roadside shrines on the Pilgrim Pass, one per Plate. Ashkaar charges a toll at six of them.",
  :steps => { :ask => "Visit all eighteen shrines on the Pilgrim Pass.", :crown => "Report to the shrine-keeper at the Crown gate." },
  :reward => { :items => [[:FIRESTONE, 1], [:WATERSTONE, 1], [:THUNDERSTONE, 1], [:LEAFSTONE, 1], [:ICESTONE, 1]] },
  :touches => "Ashkaar tolls (pay, fight or talk); WORLD 'Eighteen Shrines'",
  :design => "Each shrine asks one line of the counting rhyme; the eighteenth asks for the line nobody sings ('...and one that no one counted'). The keeper gives you the five Imprint stones the shrines kept (the Octave's Eevee, SPINE Rev 19, replaced the old 'Prism' Eevee here)."
})
stub.call(:CR_LOST_PROPERTY, {
  :trial => :CROWNHAVEN, :title => "Lost Property", :giver => "the lost-property clerk", :map => 499, :where => "the Court of Eight Pavilions",
  :rank => 1, :points => 2, :rec_level => 88, :chapter => 20, :unlock => "switch(155)", :tags => [:comedy],
  :summary => "The Festival lost-property tent has one item. Every day. It's an eel receipt.",
  :steps => { :ask => "Find out whose eel receipt keeps turning up.", :return => "Return it." },
  :reward => { :items => [[:RARECANDY, 2]] }, :touches => "Kestrel bond (+1); 15_COMEDY Crownhaven bit; Ebbmouth's 'THE BOY (4 EELS, DAILY)'",
  :design => "It's Kestrel's, from Ebbmouth, from Chapter 4. He has been carrying it for sixteen chapters. He denies it until you show him the date. Then he takes it back very carefully."
})
stub.call(:CR_DELEGATION_DISPUTE, {
  :trial => :CROWNHAVEN, :title => "The Pavilion Line", :giver => "Clerk-Superior Amadeus Fenwright", :map => 499, :where => "the Court of Eight Pavilions",
  :rank => 2, :points => 3, :rec_level => 88, :chapter => 20, :unlock => "switch(155)", :tags => [:politics, :comedy],
  :summary => "Ashkaar's pavilion is four inches over the line into Isenmar's. Neither delegation will speak to the other. Both will speak to you.",
  :steps => { :ask => "Carry messages between the Ashkaar and Isenmar pavilions.", :settle => "Settle the four inches." },
  :reward => { :items => [[:PPMAX, 1]] }, :touches => "War outcome flavour (war_terms); Dominar / Thane",
  :design => "Every message gets ruder in translation. The fix is to move the line, not the pavilion; Fenwright is appalled and then promoted."
})
stub.call(:CR_MASQUE_INVITES, {
  :trial => :CROWNHAVEN, :title => "Invitations to the Masque", :giver => "the Basilica steward", :map => 483, :where => "the Basilica Close",
  :rank => 2, :points => 3, :rec_level => 88, :chapter => 20, :unlock => "switch(156)", :tags => [:delivery, :social],
  :summary => "Deliver eight invitations to the Night of Masques. One recipient doesn't exist. One is dead. One is you.",
  :steps => { :ask => "Deliver the eight Masque invitations around Crownhaven.", :last => "The last invitation has your name on it." },
  :reward => { :items => [[:RARECANDY, 2]] }, :touches => "Night of Masques (S157) staging",
  :design => "A social route through the capital meeting every delegation; the dead recipient is Morwen Vane, and Kestrel sees you holding it."
})
stub.call(:CR_HOLLIS_LEDGER, {
  :trial => :CROWNHAVEN, :title => "The Chancellor's Other Ledger", :giver => "an anonymous petition", :map => 486, :where => "the Accord Palace",
  :rank => 3, :points => 4, :rec_level => 90, :chapter => 20, :unlock => "switch(155)", :tags => [:mystery, :stealth, :politics],
  :summary => "An unsigned petition, sealed with all eighteen kingdom seals: Chancellor Hollis keeps a second ledger.",
  :steps => { :ask => "Find the Chancellor's second ledger in the Accord Palace.", :choose => "Who gets the ledger?" },
  :reward => { :money => 12000 }, :touches => "Hollis's arrest in the epilogue; ACCORD / MERIDIAN standing",
  :design => "Palace stealth during a reception; the petition was written by Clerk Fenwright, who has been waiting thirty years for someone to answer it."
})
stub.call(:CR_VALENS_ERRAND, {
  :trial => :CROWNHAVEN, :title => "An Old Man's Errand", :giver => "Valen Corrigan", :map => 489, :where => "the Memorial Garden",
  :rank => 3, :points => 4, :rec_level => 90, :chapter => 20, :unlock => "switch(158)", :tags => [:bond, :kindness],
  :summary => "Valen asks you, not as Sovereign, to fetch something from the Memorial Garden that he can't bend down to pick up any more.",
  :steps => { :ask => "Find the stone Valen means in the Memorial Garden.", :give => "Bring it to him." },
  :reward => { :items => [[:PPMAX, 1]], :effects => "VALEN+2" }, :touches => "Valen bond (+2) before the Final",
  :design => "The stone is the AF 290 marker; the name on it is the PC's mother's. He doesn't explain. He says thank you twice."
})
stub.call(:CR_ACCORD_CHAMPIONS, {
  :trial => :CROWNHAVEN, :title => "Hand of the Accord", :giver => "Clerk-Superior Amadeus Fenwright", :map => 496, :where => "the Hall of Petitions",
  :rank => 5, :points => 5, :rec_level => 95, :chapter => 21, :unlock => "switch(160)", :tags => [:final_trial, :gauntlet],
  :summary => "Answer one petition from every kingdom in a single day. Each is a battle. Each Warden who still speaks to you sends one.",
  :steps => { :ask => "Answer the eight kingdom petitions (postgame Warden rematch gauntlet).", :hand => "Receive the Hand of the Accord." },
  :reward => { :items => [[:MASTERBALL, 1]] }, :touches => "Postgame Warden's Gauntlet (S160); every Trial's rank 5 counts",
  :design => "Requires rank 4+ in at least five Trials. The gauntlet's order is the eight Trials' halls; between bouts, each Trial's keeper says one line about what you did in their kingdom."
})
stub.call(:CR_LIN, {
  :trial => :CROWNHAVEN, :title => "The Meteor Champion", :giver => "a petition in a hand nobody recognises", :map => 105, :where => "Ferrow Lighthouse",
  :rank => 4, :points => 5, :rec_level => 100, :chapter => 22, :unlock => "switch(160)", :tags => [:cameo, :superboss],
  :summary => "A petition arrives from nowhere: 'Come back to where you landed.'",
  :steps => { :ask => "Go back to Ferrow's Landing lighthouse.", :fight => "She is waiting at the lamp." },
  :reward => { :items => [[:ABILITYPATCH, 1]] }, :touches => "CAMEOS.md #8 (FESTIVAL_LIN superboss)",
  :design => "Board pointer for the Lin postgame cameo; her event completes the quest."
})
