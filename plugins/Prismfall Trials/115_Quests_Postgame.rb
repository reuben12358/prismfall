#===============================================================================
# Prismfall Trials - 115 The post-game Registry's cards (the :POSTGAME board)
#-------------------------------------------------------------------------------
# story/41_SCRIPT_POSTGAME.md (the givers and their opening lines, the continuity
# fixes at the end) and Gemini's Part B.3 network (levels, places, structure;
# gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta).
# Tiers, clear switches (S271-S294) and the board are 013_Trials_Registry.rb; the
# legends are 134_EventMons_Postgame.rb; the givers' map events are 154_Talk_Postgame.rb
# and design/TRIAL_EVENTS.yaml.
# Tier 1 is wired (each card: the giver's offer, its encounters, its close). Tier 2 and
# Tier 3 are designed stubs: they show on the Registry once their tier opens, marked
# "NOT YET", and can't be taken until their maps exist.
# Every card unlocks on S160 + S270; no legendary is reachable from here before the
# post-game (and Core 027_LegendaryGate.rb would stop the ball if one were).
#===============================================================================
tr = Prismfall::Trials
pg_open = "switch(160) && switch(270)"

# A trainer bout that only happens once its PBS block exists (the Encore troupe, Kaito's five rounds).
pg_bout = lambda do |specs, field: nil, heal: true|
  proc do |ctx|
    here = specs.select { |t| GameData::Trainer.exists?(t[0], t[1], t[2] || 0) }
    next if here.empty?
    won = Prismfall::Trials.gauntlet(here, heal_between: false, field: field)
    $player.heal_party if heal && $player
    next if won
    ctx[:result] = :bout_lost
    raise Prismfall::Trials::Script::Halt     # the scene stops here; the step stays, so it can be tried again
  end
end

#--- T1-1 ------------------------------------------------------------------------------------------
tr.quest(:PG_MELOETTA, {
  :trial => :POSTGAME, :title => "Crownhaven Encore", :giver => "Dorian Pell", :map => 154, :where => "the Pell Playhouse stage door (Saltmere)",
  :points => 3, :rec_level => 85, :chapter => 22, :unlock => pg_open, :tags => [:legend, :boss],
  :summary => "A gold playbill, in Dorian's hand: \"She held back in Act One so you could shine, darling. Opening Night is hers.\"",
  :steps => { :playbill => "Take the gold playbill to Dorian.", :encore => "The Crownhaven Opera Hall: the Encore.",
              :bow => "Take a bow with Dorian." },
  :reward => { :items => [[:MAGICALSEED, 3]] },
  :touches => "S271 PG_T1_MELOETTA; Gym 1's Meloetta, caught on her last bar",
  :scenes => {
    :offer => [
      [:DORIAN, :happy, "She held back in Act One so you could shine, darling. Opening Night is hers."],
      [:DORIAN, :neutral, "The Opera Hall, Crownhaven. My troupe opens, she closes. Do wear something."],
      { :accept => true }, { :step => :encore }],
    :encore => [
      { :map => "The Crownhaven Opera Hall. The house is full. Standing Ovation before a note is sung." },
      { :script => pg_bout.call([[:LEADER_DORIAN, "Dorian", 91]], field: [:GRAND_STAGE, 3]) },
      { :script => proc { |_ctx| Prismfall::Trials.set_field([:GRAND_STAGE, 3]) } },   # Standing Ovation
      { :event_battle => :PG_MELOETTA,
        :caught => [{ :run => :bow }], :won => [{ :run => :bow }],
        :lost => ["The curtain comes down early. She'll sing again tomorrow night."] }],
    :bow => [
      { :step => :bow },
      [:DORIAN, :happy, "Take her on tour, darling. The whole world is a stage now."],
      { :complete => true }]
  }
})

#--- T1-2 ------------------------------------------------------------------------------------------
tr.quest(:PG_OGERPON, {
  :trial => :POSTGAME, :title => "The Masks of Gloamwood", :giver => "Juno", :map => 708, :where => "the Bride Tree (the Bride Grove)",
  :points => 3, :rec_level => 88, :chapter => 22, :unlock => pg_open, :tags => [:legend, :boss],
  :summary => "Juno, at the Bride Tree: three shapes at the border stones, and a small one that still watches the road.",
  :steps => { :ask => "Meet Juno at the Bride Tree.", :stones => "Lay the Loyal Three to rest at Elowen's three border stones.",
              :ogre => "The Bride Tree: the little ogre and its four masks.", :home => "Tell Juno." },
  :reward => { :items => [[:PPMAX, 1]], :effects => "JUNO+1" },
  :touches => "S272 PG_T1_OGERPON; Ogerpon joins the party only here (continuity fix 3)",
  :scenes => {
    :offer => [
      [:JUNO, :neutral, "They've been standing at the border stones for three hundred years being ashamed. Somebody should tell them it's over."],
      { :if => "choice(:ch10_ogre) == :hesitate",
        :then => [{ :map => "Juno's reconciliation beat (Ch10 :hesitate) plays here first; its lines are the story team's." }] },
      { :accept => true }, { :step => :stones }],
    :stone_okidogi => [
      { :event_battle => :PG_OKIDOGI, :caught => [{ :flag => [:okidogi, true] }, { :run => :stones_check }],
        :won => [{ :flag => [:okidogi, true] }, { :run => :stones_check }], :lost => ["It stands at the stone again. It isn't going anywhere."] }],
    :stone_munkidori => [
      { :event_battle => :PG_MUNKIDORI, :caught => [{ :flag => [:munkidori, true] }, { :run => :stones_check }],
        :won => [{ :flag => [:munkidori, true] }, { :run => :stones_check }], :lost => ["It stands at the stone again. It isn't going anywhere."] }],
    :stone_fezandipiti => [
      { :event_battle => :PG_FEZANDIPITI, :caught => [{ :flag => [:fezandipiti, true] }, { :run => :stones_check }],
        :won => [{ :flag => [:fezandipiti, true] }, { :run => :stones_check }], :lost => ["It stands at the stone again. It isn't going anywhere."] }],
    :stones_check => [
      { :if => "quest_flag(:SELF, :okidogi) && quest_flag(:SELF, :munkidori) && quest_flag(:SELF, :fezandipiti)",
        :then => ["All three border stones are quiet.", { :step => :ogre }] }],
    :ogre => [
      { :script => proc { |_ctx| Prismfall::Trials.set_field([:FLOWER_GARDEN, 3]) } },
      { :event_battle => :PG_OGERPON,
        :caught => [{ :step => :home }], :won => [{ :step => :home }],
        :lost => ["It pulls the mask back down and climbs the Bride Tree. It will come down again."] }],
    :home => [
      [:JUNO, :happy, "It chose. Good. Somebody in this garden should get to."],
      { :complete => true }]
  }
})

#--- T1-3 ------------------------------------------------------------------------------------------
tr.quest(:PG_PECHARUNT, {
  :trial => :POSTGAME, :title => "The Bitter Mochi Seal", :giver => "Corvin (or Mother Gutter)", :map => 423, :where => "the Moon Market (Underveil)",
  :points => 3, :rec_level => 86, :chapter => 22, :unlock => pg_open, :tags => [:legend, :boss],
  :summary => "A Sweetrot echo under the Moon Market. Wenlow's notes are the lead: his handwriting, all the way down the margin.",
  :steps => { :ask => "Ask at the Moon Market about the echo.", :tea => "Larch's kelp tea breaks the dormant shell. Ask Larch.",
              :seal => "The Lightless Deep: pour the tea. Seal it, or catch it.", :report => "Go back to the Moon Market." },
  :reward => { :items => [[:BLACKSLUDGE, 1], [:EXPCANDYXL, 2]] },
  :touches => "S273 PG_T1_PECHARUNT; not Wenlow (he died in Interlude IV): Corvin if CORVIN_FREED, else Mother Gutter",
  :scenes => {
    :offer => [
      { :if => "flag(:CORVIN_FREED)",
        :then => [[:CORVIN, :neutral, "The boy kept notes. Of course he did. He'd read the book twice. There's an echo of it under the Market, dear, and his notes say what dissolves the shell."]],
        :else => [[:MOTHER_GUTTER, :neutral, "The medic's boy left a notebook in my ledger. Says there's something sweet still breathing under my Market. Says what kills the shell. I can't read the last word."]] },
      "The last word is \"kelp\".",
      { :accept => true }, { :step => :tea }],
    :tea => [
      [:LARCH, :smug, "My tea. You want my tea. As a solvent."],
      [:LARCH, :neutral, "...It would work. Don't tell anyone it would work."],
      { :flag => [:tea, true] }, { :step => :seal }],
    :seal => [
      "You pour Larch's kelp tea over the shell. It hisses. It smells exactly as it always has.",
      { :event_battle => :PG_PECHARUNT,
        :caught => [{ :step => :report }], :won => ["The shell closes over it, for good this time.", { :step => :report }],
        :lost => ["It pulls the shell shut. There's tea left."] }],
    :report => [
      { :if => "flag(:CORVIN_FREED)",
        :then => [[:CORVIN, :sad, "Somebody has to turn the glass ones. He'd have wanted this one turned, too."]],
        :else => [[:MOTHER_GUTTER, :neutral, "Then it's off my books. Leave the notebook. I'll keep it with the others."]] },
      { :complete => true }]
  }
})

#--- T1-4 ------------------------------------------------------------------------------------------
tr.quest(:PG_REGIS, {
  :trial => :POSTGAME, :title => "The Stonesleep Braille", :giver => "Sahar", :map => 788, :where => "the Stonesleep monolith",
  :points => 4, :rec_level => 90, :chapter => 22, :unlock => pg_open, :tags => [:legend, :boss],
  :summary => "Sahar has read the whole monolith under Stonesleep. It isn't a warning.",
  :steps => { :ask => "Meet Sahar at the Stonesleep monolith.", :three => "Wake the three: rock in Stonesleep, ice in the Whalebone Vault, steel in Cogsworth's core.",
              :twins => "The twin chambers: the electromagnet in the Static Tunnels, the dragon-fang in the Wyrmscar.",
              :gigas => "The Aurelia Ruin Vault: the one the five were made to wake.", :report => "Tell Sahar." },
  :reward => { :items => [[:ABILITYPATCH, 1]] },
  :touches => "S274 PG_T1_REGIS; six legends across Ossaria, Isenmar and Zenith",
  :scenes => {
    :offer => [
      [:SAHAR, :neutral, "The braille under Stonesleep. I read it the day the sky closed. It's an invitation."],
      { :accept => true }, { :step => :three }],
    :regirock  => [{ :event_battle => :PG_REGIROCK,  :caught => [{ :flag => [:rock, true] }, { :run => :check }],  :won => [{ :flag => [:rock, true] }, { :run => :check }],  :lost => ["The dots go dark. They'll light again."] }],
    :regice    => [{ :event_battle => :PG_REGICE,    :caught => [{ :flag => [:ice, true] }, { :run => :check }],   :won => [{ :flag => [:ice, true] }, { :run => :check }],   :lost => ["The dots go dark. They'll light again."] }],
    :registeel => [{ :event_battle => :PG_REGISTEEL, :caught => [{ :flag => [:steel, true] }, { :run => :check }], :won => [{ :flag => [:steel, true] }, { :run => :check }], :lost => ["The dots go dark. They'll light again."] }],
    :regieleki => [{ :event_battle => :PG_REGIELEKI, :caught => [{ :flag => [:eleki, true] }, { :run => :check }], :won => [{ :flag => [:eleki, true] }, { :run => :check }], :lost => ["The dots go dark. They'll light again."] }],
    :regidrago => [{ :event_battle => :PG_REGIDRAGO, :caught => [{ :flag => [:drago, true] }, { :run => :check }], :won => [{ :flag => [:drago, true] }, { :run => :check }], :lost => ["The dots go dark. They'll light again."] }],
    :check => [
      { :if => "quest_step(:SELF) == :three && quest_flag(:SELF, :rock) && quest_flag(:SELF, :ice) && quest_flag(:SELF, :steel)",
        :then => ["Far off, in two places at once, something answers.", { :step => :twins }] },
      { :if => "quest_step(:SELF) == :twins && quest_flag(:SELF, :eleki) && quest_flag(:SELF, :drago)",
        :then => ["Five lights. Under Aurelia, a sixth door has been waiting for exactly five.", { :step => :gigas }] }],
    :regigigas => [{ :event_battle => :PG_REGIGIGAS, :caught => [{ :step => :report }], :won => [{ :step => :report }],
                     :lost => ["It sits back down. It has waited longer than this."] }],
    :report => [
      [:SAHAR, :happy, "The desert keeps everything. I'm glad it kept this for someone who'd knock first."],
      { :complete => true }]
  }
})

#--- T1-5 ------------------------------------------------------------------------------------------
tr.quest(:PG_LAKES, {
  :trial => :POSTGAME, :title => "The Three Mirror Lakes", :giver => "Archseer Dask and Ilsa", :map => 346, :where => "the Speculum (Lucent)",
  :points => 3, :rec_level => 84, :chapter => 22, :unlock => pg_open, :tags => [:legend, :boss],
  :summary => "Three ripples on three lakes, with nothing under them. Dask and Ilsa heard them the same night.",
  :steps => { :ask => "Ask Dask and Ilsa at the Speculum.", :lakes => "Knowledge in Mirror Mere, Emotion in Lake Rime, Will in Lake Sallow.",
              :report => "Go back to the Speculum." },
  :reward => { :items => [[:ELEMENTALSEED, 3]], :effects => "ILSA+1" },
  :touches => "S275 PG_T1_LAKES",
  :scenes => {
    :offer => [
      [:DASK, :neutral, "Three ripples. Knowledge, Emotion, Will. Lucent, Rime, Sallow."],
      [:ILSA, :neutral, "They aren't thinking anything. That's how I know they're there."],
      { :accept => true }, { :step => :lakes }],
    :uxie    => [{ :event_battle => :PG_UXIE,    :caught => [{ :flag => [:uxie, true] }, { :run => :check }],    :won => [{ :flag => [:uxie, true] }, { :run => :check }],    :lost => ["The lake goes flat. It will ripple again."] }],
    :mesprit => [{ :event_battle => :PG_MESPRIT, :caught => [{ :flag => [:mesprit, true] }, { :run => :check }], :won => [{ :flag => [:mesprit, true] }, { :run => :check }], :lost => ["The lake goes flat. It will ripple again."] }],
    :azelf   => [{ :event_battle => :PG_AZELF,   :caught => [{ :flag => [:azelf, true] }, { :run => :check }],   :won => [{ :flag => [:azelf, true] }, { :run => :check }],   :lost => ["The lake goes flat. It will ripple again."] }],
    :check => [
      { :if => "quest_flag(:SELF, :uxie) && quest_flag(:SELF, :mesprit) && quest_flag(:SELF, :azelf)",
        :then => ["Three lakes, three mirrors, all of them still.", { :step => :report }] }],
    :report => [
      [:ILSA, :happy, "Quiet. All three. I'd forgotten what the lakes sound like with nobody in them."],
      { :complete => true }]
  }
})

#--- T1-6 ------------------------------------------------------------------------------------------
tr.quest(:PG_TYPENULL, {
  :trial => :POSTGAME, :title => "Project NULL, Unmasked", :giver => "Calla Wren (or the NULL CRADLE KEY)", :map => 699, :where => "the Meridian Black Site",
  :points => 4, :rec_level => 88, :chapter => 22, :unlock => pg_open + " && (switch(180) || flag(:CALLA_ALIVE))", :tags => [:legend, :gift, :boss],
  :summary => "The Black Site's cradle is still sealed, and still powered. Something in it has been waiting since Chapter 10.",
  :steps => { :ask => "Go to the Black Site door.", :raid => "Through Quent's automated security to the cradle.",
              :null => "Open the cradle.", :genesect => "The archive: Meridian's first prototype is awake.", :out => "Leave the Black Site." },
  :reward => { :items => [[:ABILITYCAPSULE, 1]] },
  :touches => "S276 PG_T1_TYPENULL; the Ch10 promise (S180) kept; Calla only if CALLA_ALIVE, Kestrel only if not KESTREL_LOST (continuity fix 2)",
  :scenes => {
    :offer => [
      { :if => "flag(:CALLA_ALIVE)",
        :then => [[:CALLA, :neutral, "I know the Black Site's codes. I wrote half of them."]],
        :else => ["The NULL CRADLE KEY turns in the Black Site door. It has been waiting to."] },
      { :accept => true }, { :step => :raid }],
    :raid => [
      { :map => "Quent's automated security: the corridor fights are the map's own trainers (PBS pending). Kestrel walks in beside you unless KESTREL_LOST." },
      "The last shutter grinds up. The cradle room is exactly as cold as you remember.",
      { :step => :null }],
    :cradle => [
      "The cradle opens. It looks at your badge case first. Then at you.",
      { :gift => :PG_TYPENULL },
      { :step => :genesect }],
    :archive => [
      { :event_battle => :PG_GENESECT,
        :caught => [{ :step => :out }], :won => ["It powers down, at last, with nobody's hand on the switch.", { :step => :out }],
        :lost => ["It resets. It has been resetting for years."] }],
    :out => [
      { :if => "flag(:CALLA_ALIVE)", :then => [[:CALLA, :sad, "I wrote the line that kept it asleep. You've just deleted it. Thank you."]] },
      { :complete => true }]
  }
})

#--- T1-7 ------------------------------------------------------------------------------------------
tr.quest(:PG_KUBFU, {
  :trial => :POSTGAME, :title => "The Pit-Dojo Scrolls", :giver => "Kaito", :map => 263, :where => "the Iron Pit (Ironreach)",
  :points => 3, :rec_level => 90, :chapter => 22, :unlock => pg_open, :tags => [:gift, :gauntlet],
  :summary => "Kaito: \"Five rounds. No items. You're the Champion; you can afford to lose.\"",
  :steps => { :ask => "Go down to the Iron Pit.", :pit => "Five rounds in the Iron Pit. No items.", :scrolls => "Kaito has something for whoever is still standing." },
  :reward => { :items => [[:PPMAX, 1]] },
  :touches => "S277 PG_T1_KUBFU; Kubfu (gift) and both scroll towers",
  :scenes => {
    :offer => [
      [:KAITO, :neutral, "Five rounds. No items. You're the Champion; you can afford to lose."],
      { :accept => true }, { :step => :pit }],
    :pit => [
      # The five pit fighters' PBS blocks are pending; until they exist the Pit is Kaito himself (his Festival team).
      { :script => pg_bout.call([[:BLACKBELT, "Ren", 22], [:CRUSHGIRL, "Mako", 22], [:BLACKBELT, "Oda", 22], [:CRUSHGIRL, "Sen", 22]]) },
      { :trainer => [:LEADER_KAITO, "Kaito", 92], :field => :COLOSSEUM,
        :won => [{ :run => :scrolls }],
        :lost => [[:KAITO, :happy, "Good. Now you know what round five feels like. Again, when you're ready."]] }],
    :scrolls => [
      { :step => :scrolls },
      [:KAITO, :happy, "A fist is a promise. This one hasn't made any yet. Teach it good ones."],
      { :gift => :PG_KUBFU },
      "Kaito marks two towers on your map: the Tide Tower on the Ebbmouth cliffs, the Shadow Tower in Underveil.",
      { :complete => true }]
  }
})

#--- T1-8 ------------------------------------------------------------------------------------------
tr.quest(:PG_ROAMERS, {
  :trial => :POSTGAME, :title => "Roamers, Guardians and Encores", :giver => "the Wardens' pinned rumours", :map => 493, :where => "the Registry board",
  :points => 4, :rec_level => 86, :chapter => 22, :unlock => pg_open, :tags => [:legend, :roaming],
  :summary => "Eighteen columns of rumours, one legend or mythical tied to each Warden's kingdom. Settle eight and Larch will call the column filled.",
  :steps => { :rumours => "Follow the Wardens' rumours (each legend's place is on its pin).", :report => "Tell Larch." },
  :reward => { :items => [[:MASTERBALL, 1]] },
  :touches => "S278 PG_T1_ROAMERS; map events call pf_registry_roamer(:SPECIES); clears at 8 settled (Registry::ROAMERS_NEEDED)"
})

#--- Tier 2 and Tier 3: designed, shown on the Registry when their tier opens, not yet takeable -----
stub = lambda { |id, h| tr.quest(id, h.merge(:trial => :POSTGAME, :chapter => 22, :stub => true, :board => true)) }
stub.call(:PG_UBS, {
  :title => "The Eleven Bleed Rifts", :giver => "Ysolde", :map => 380, :where => "Gravenmoor", :rec_level => 92, :points => 4,
  :unlock => "switch(279)", :summary => "Ysolde: \"The Glass is mending. Slowly. Things are getting through while it does.\"",
  :steps => { :rifts => "Close the ten kingdom rifts.", :last => "The last rift." },
  :design => "Giratina's wound (Ch15) is still open; ten kingdom-matched rifts, Poipole from the last. S280."
})
stub.call(:PG_TAPUS, {
  :title => "Guardians of the Shardfall", :giver => "Edda", :map => 905, :where => "the Shardfall Isles ferry", :rec_level => 92, :points => 4,
  :unlock => "switch(279)", :summary => "The quarantine's first islands. Edda's ferry runs there now.",
  :steps => { :ruins => "The four compass ruins of the Shardfall Isles." },
  :design => "Four Tapus, each guarding a monolith; the terrain changes on bar breaks. S281."
})
stub.call(:PG_RUIN_QUARTET, {
  :title => "The Four Cursed Stakes of Aurelius", :giver => "Sahar and Celestine", :map => 200, :where => "the Hall of Unearthing (Duneholt)", :rec_level => 93, :points => 4,
  :unlock => "switch(279)", :summary => "The Gilded King's four curses, buried in four kingdoms' shrines under sixteen stakes.",
  :steps => { :stakes => "Pull the sixteen stakes.", :shrines => "The four shrines." },
  :design => "Wo-Chien, Chien-Pao, Ting-Lu, Chi-Yu; stakes tracked in the quest log. S282."
})
stub.call(:PG_PARADOX, {
  :title => "Prism Echoes", :giver => "Larch", :map => 905, :where => "the Shardfall deep crater", :rec_level => 94, :points => 4,
  :unlock => "switch(279)", :summary => "Where the Bleed made echoes of the past and the future.",
  :steps => { :crater => "The deep crater of the Shardfall Isles." },
  :design => "Two three-legend Paradox anomalies as 2-bar bosses. S283."
})
stub.call(:PG_CALYREX, {
  :title => "Crown of the Hoarwood", :giver => "Anja and Ysolde", :map => 306, :where => "the Great Tally (Rimeholt)", :rec_level => 93, :points => 4,
  :unlock => "switch(279)", :summary => "Anja and Ysolde's winter legend: two steeds and a king who lost his harvest.",
  :steps => { :steeds => "Tame both steeds.", :king => "Unite the Harvest King." },
  :design => "Glastrier, Spectrier, Calyrex and the Reins of Unity. S284."
})
stub.call(:PG_WEATHER_TRIO, {
  :title => "The Thawed Sea and the Deep Seams", :giver => "Anja and Sahar", :map => 308, :where => "the Whalebone Keep ice vault", :rec_level => 98, :points => 5,
  :unlock => "switch(285)", :summary => "Kyogre and Groudon, awake and unbound. Anja and Sahar were there the first time.",
  :steps => { :sea => "Kyogre, in the ice vault.", :seams => "Groudon, in the Undersands.", :sky => "The Skyreach summit." },
  :design => "3-bar rematches, :catch => :last_bar; both open Rayquaza. S286."
})
stub.call(:PG_TAO_TRIO, {
  :title => "Ideals, Truth and the Husk", :giver => "Rook and Sigrun", :map => 746, :where => "the Stormwatch Spire roof", :rec_level => 98, :points => 5,
  :unlock => "switch(285)", :summary => "Zekrom over Zenith. Reshiram chose Sigrun, so Sigrun tests you first.",
  :steps => { :ideals => "Zekrom.", :truth => "Sigrun, then Reshiram.", :husk => "The Frostfang core." },
  :design => "Zekrom and Reshiram rematches, then Kyurem and the DNA Splicers. S287."
})
stub.call(:PG_GIRATINA, {
  :title => "The Distortion Core", :giver => "Archseer Dask", :map => 910, :where => "Vigil's Grave Glass", :rec_level => 98, :points => 5,
  :unlock => "switch(285) && switch(268)", :summary => "Dask: \"The wound in its side. It never closed. Go and see it. Don't look back on the way in.\"",
  :steps => { :core => "Walk the inverted labyrinth.", :wound => "Giratina, guarding the hole it can't mend." },
  :design => "Giratina Origin Lv 98 with the Griseous Core, :catch => :last_bar; the rifts stop opening after. S288."
})
stub.call(:PG_ZYGARDE, {
  :title => "Valen's Order", :giver => "Ilsa", :map => 483, :where => "Valen's memorial (the Basilica garden)", :rec_level => 98, :points => 5,
  :unlock => "switch(285)", :summary => "The Cell on the plinth, and every other Cell in Velmora.",
  :steps => { :cells => "Gather the Cells from all seven kingdoms.", :order => "Valen's memorial." },
  :design => "Zygarde Complete; already the PC's if ZYGARDE_CHOOSES (P3), then this is its 100% form. S289."
})
stub.call(:PG_BOX_LEGENDS, {
  :title => "Echoes of Distant Worlds", :giver => "Larch", :map => 493, :where => "the Registry board", :rec_level => 98, :points => 5,
  :unlock => "switch(285)", :summary => "Three sets of things that were never Velmora's: Creation and Life, Light and Crown, Tera and Apex.",
  :steps => { :creation => "Creation and Life.", :light => "Light and Crown.", :apex => "Tera and Apex." },
  :design => "The box legends in three anomaly sets, each with a cameo or Warden guide. S290-S292."
})
stub.call(:PG_ARCEUS, {
  :title => "The 18-Plate Convergence", :giver => "the eighteen Wardens", :map => 491, :where => "the Prism Arena", :rec_level => 100, :points => 5,
  :unlock => "switch(285) && switch(267) && !switch(265)", :requires => [:PG_WEATHER_TRIO, :PG_TAO_TRIO, :PG_GIRATINA, :PG_ZYGARDE],
  :summary => "On the Ring where Valen held it, the eighteen Wardens kneel at the pylons again, empty-handed this time, because they want to see.",
  :steps => { :ring => "Stand on the Ring." },
  :design => "Arceus Lv 100 with the Legend Plate, 4 bars, :catch => :last_bar. Never on the Ruin Route (S265), never after the Gilded Chain. S294."
})
