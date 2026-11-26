#===============================================================================
# Prismfall Trials - 134 Event Pokemon of the post-game Registry (115_Quests_Postgame.rb)
#-------------------------------------------------------------------------------
# story/41_SCRIPT_POSTGAME.md "The capture rule: every post-game legendary is a
# Prismfall::Bosses fight. Each has 2-3 bars (3-4 on Hard) and :catch => :last_bar:
# the player breaks the shields before Poke Balls work. Gifts (Type: Null, Kubfu)
# are given after a trial." Levels and fields: Gemini's Part B.3 tables.
# None of this is reachable before S160: every card unlocks on switch(160), and
# Core 027_LegendaryGate.rb deflects every ball at a legendary until then anyway.
# No :badges key on purpose (the Revision 16 type-gate check is for the main story).
# A staged field (Standing Ovation, the garden in bloom) is set by the card's scene just before the battle
# (Trials.set_field); :field here is the plain id the boss falls back to.
#===============================================================================
em = Prismfall::EventMons

# A legend met on a card: a bar boss that can be caught on its last bar and fought again if it wins.
legend = lambda do |id, species, level, field, where, quest, extra = {}|
  boss = { :bars => { :CASUAL => 2, :STANDARD => 2, :HARD => 3, :default => 2 }, :catch => :last_bar }
  boss = boss.merge(extra.delete(:boss) || {})
  em.register(id, { :species => species, :level => level, :kind => :boss, :field => field, :boss => boss,
                    :on_ko => :retry, :where => where, :chapter => 22, :quest => quest }.merge(extra))
end

#--- T1-1 Crownhaven Encore ----------------------------------------------------------------------
legend.call(:PG_MELOETTA, :MELOETTA, 85, :GRAND_STAGE, "the Crownhaven Opera Hall (Opening Night)", :PG_MELOETTA,
            :nickname => "Prima Donna",
            :boss => { :intro => "The house lights go down. One spotlight. She was always going to take the second act.",
                       :breaks => { 1 => { :message => "{1} spins out of the aria and into the dance!", :stats => { :SPEED => 1 } } } },
            :why => "Gym 1 callback: Dorian's muse, at full power, on a Standing Ovation stage")

#--- T1-2 The Masks of Gloamwood -----------------------------------------------------------------
[[:PG_OKIDOGI, :OKIDOGI, "the north border stone"], [:PG_MUNKIDORI, :MUNKIDORI, "the east border stone"],
 [:PG_FEZANDIPITI, :FEZANDIPITI, "the south border stone"]].each do |id, sp, where|
  legend.call(id, sp, 84, :FAIRY_TALE, "Elowen's #{where}", :PG_OGERPON,
              :boss => { :intro => "It has stood at the border stone for three hundred years, ashamed." })
end
legend.call(:PG_OGERPON, :OGERPON, 88, :FLOWER_GARDEN, "the Bride Grove (708), under the Bride Tree", :PG_OGERPON,
            :boss => { :bars => { :CASUAL => 3, :STANDARD => 4, :HARD => 4, :default => 4 },
                       :intro => "The little ogre lowers its mask. It wants to know if you meant it.",
                       :breaks => { 1 => { :message => "{1} tries the next mask!", :stats => { :SPEED => 1 } },
                                    2 => { :message => "{1} tries the next mask!", :stats => { :ATTACK => 1 } },
                                    3 => { :message => "{1} tries the last mask!", :stats => { :DEFENSE => 1 } } } },
            :joins => {},
            :why => "It joins the party only here (continuity fix 3): caught on the last bar, or it follows you home after a win")

#--- T1-3 The Bitter Mochi Seal -------------------------------------------------------------------
legend.call(:PG_PECHARUNT, :PECHARUNT, 86, :NEW_MOON, "the Lightless Deep, under the Moon Market", :PG_PECHARUNT,
            :boss => { :intro => "The kelp tea eats through the shell. Inside, something small and sweet and furious wakes up." })

#--- T1-4 The Stonesleep Braille -----------------------------------------------------------------
[[:PG_REGIROCK, :REGIROCK, 84, :CAVE, "Stonesleep (788), the west chamber"],
 [:PG_REGICE, :REGICE, 84, :FROZEN_LAKE, "the Whalebone Vault (308)"],
 [:PG_REGISTEEL, :REGISTEEL, 84, :FACTORY, "the Cogsworth core"],
 [:PG_REGIELEKI, :REGIELEKI, 86, :NEON_GRID, "the Static Tunnels, the electromagnet chamber"],
 [:PG_REGIDRAGO, :REGIDRAGO, 86, :DRAGONS_DEN, "the Wyrmscar, the dragon-fang chamber"],
 [:PG_REGIGIGAS, :REGIGIGAS, 90, :CAVE, "the Aurelia Ruin Vault"]].each do |id, sp, lv, field, where|
  legend.call(id, sp, lv, field, where, :PG_REGIS, :boss => { :intro => "The dots on the wall light, one by one. It was an invitation." })
end

#--- T1-5 The Three Mirror Lakes -----------------------------------------------------------------
[[:PG_UXIE, :UXIE, :MINDSCAPE, "Mirror Mere (Lucent): Knowledge"],
 [:PG_MESPRIT, :MESPRIT, :WATER_SURFACE, "Lake Rime (300): Emotion"],
 [:PG_AZELF, :AZELF, :WATER_SURFACE, "Lake Sallow (650): Will"]].each do |id, sp, field, where|
  legend.call(id, sp, 84, field, where, :PG_LAKES, :boss => { :intro => "A ripple with nothing under it. Then something under it." })
end

#--- T1-6 Project NULL, Unmasked -----------------------------------------------------------------
em.register(:PG_TYPENULL, {
  :species => :TYPENULL, :level => 82, :kind => :gift, :nickname => "Null", :happiness => 0,
  :obtain_text => "The Black Site cradle",
  :where => "the Meridian Black Site (699), the cradle", :chapter => 22, :quest => :PG_TYPENULL,
  :why => "The Ch10 promise (S180 TYPE_NULL_GIFT), kept at last: it remembers the PC's badge case"
})
legend.call(:PG_GENESECT, :GENESECT, 88, :FACTORY, "the Black Site archive, the prototype bay", :PG_TYPENULL,
            :boss => { :intro => "Meridian's first draft powers up. Nobody ever told it the project was cancelled." })

#--- T1-7 The Pit-Dojo Scrolls -------------------------------------------------------------------
em.register(:PG_KUBFU, {
  :species => :KUBFU, :level => 80, :kind => :gift,
  :obtain_text => "Kaito's Iron Pit",
  :where => "the Iron Pit (263), after five rounds", :chapter => 22, :quest => :PG_KUBFU,
  :why => "Replaces the banned Act IV gift; both scroll towers open with it"
})

#--- T1-8 Roamers, Guardians and Encores: one rumour per Warden's pin (the first of Gemini's list;
#--- the rest of the list is added card by card as their maps are placed) --------------------------
[[:HEATRAN, 86, :VOLCANIC, "Brann: the Cinderhorn caldera (664)"],
 [:DARKRAI, 86, :HOLLOW_CATHEDRAL, "Ysolde: Vane Hall, the music room"],
 [:CRESSELIA, 86, :MINDSCAPE, "Ysolde: the Dreaming Quarter (768)"],
 [:ARTICUNO, 85, :FROZEN_LAKE, "Odessa: the Hoarwood"],
 [:ZAPDOS, 85, :STORMFRONT, "Odessa: the Stormfront"],
 [:MOLTRES, 85, :VOLCANIC, "Odessa: the Cinderhorn"],
 [:LATIAS, 86, :WATER_SURFACE, "Marisol: the Hallow Strait (900)"],
 [:LATIOS, 86, :WATER_SURFACE, "Marisol: the Hallow Strait (901)"],
 [:MANAPHY, 84, :UNDERWATER, "Marisol: the Hallow Strait seabed"],
 [:DIANCIE, 85, :FAIRY_TALE, "Celestine: the Gloamwood"],
 [:SHAYMIN, 84, :FLOWER_GARDEN, "Celestine: the Gloamwood clearing"],
 [:CELEBI, 84, :SILKWOOD, "Celestine: the oldest tree in the Gloamwood"],
 [:DEOXYS, 88, :CRYSTAL_CAVERN, "Bastian: the meteor in the Crystal Cavern"],
 [:RAIKOU, 85, :NEON_GRID, "Rook: the Static Tunnels"],
 [:ENTEI, 85, :DESERT, "Sahar: the Undersands road"],
 [:SUICUNE, 85, :WATER_SURFACE, "Anja: Lake Rime at dawn"],
 [:COBALION, 86, :COLOSSEUM, "Kaito: the shafts above the Iron Pit"],
 [:TERRAKION, 86, :CAVE, "Kaito: the Long Drop"],
 [:VIRIZION, 86, :MEADOW, "Juno: the Royal Chase"],
 [:VICTINI, 84, :GRAND_STAGE, "Dorian: the Lantern Theatre's lucky seat"],
 [:JIRACHI, 84, :RAINBOW, "Tamsin: a wish-tag on the Lantern Rope"],
 [:ZERAORA, 86, :NEON_GRID, "Magnus: the Cogsworth grid at night"],
 [:HOOPA, 86, :NEW_MOON, "Nyx: a ring for sale in the Moon Market"],
 [:VOLCANION, 86, :ASHEN_WASTE, "Sigrun: the Scaldwater vents"],
 [:MARSHADOW, 86, :HOLLOW_CATHEDRAL, "Corvin: the Quiet Ward's shadows"],
 [:MEW, 84, :MINDSCAPE, "Ilsa: a thought nobody in Lucent is thinking"]].each do |sp, lv, field, where|
  legend.call(:"PG_ROAM_#{sp}", sp, lv, field, where, :PG_ROAMERS)
end

#--- Tier 3: the story's own legends, rematched and caught at last (designed; their cards are stubs
#--- until the Tier 1 maps are in). The rematch boss ids named in Gemini's table (:KYOGRE_PG_CATCH ...)
#--- belong to Prismfall Bosses; these rows are the Registry's record of who is on which card. ------
[[:PG_KYOGRE, :KYOGRE, 95, :WATER_SURFACE, "the Whalebone Keep ice vault (308): Anja", :PG_WEATHER_TRIO],
 [:PG_GROUDON, :GROUDON, 95, :DESERT, "the Duneholt Undersands (783): Sahar", :PG_WEATHER_TRIO],
 [:PG_RAYQUAZA, :RAYQUAZA, 98, :STORMFRONT, "the Skyreach summit", :PG_WEATHER_TRIO],
 [:PG_ZEKROM, :ZEKROM, 95, :STORMFRONT, "the Stormwatch Spire roof (746): Rook", :PG_TAO_TRIO],
 [:PG_RESHIRAM, :RESHIRAM, 95, :DRAGONS_DEN, "the Wyrmscar depths: Sigrun tests you first", :PG_TAO_TRIO],
 [:PG_KYUREM, :KYUREM, 98, :FROZEN_LAKE, "the Frostfang core", :PG_TAO_TRIO],
 [:PG_GIRATINA, :GIRATINA, 98, :INVERSE, "the Distortion Core (910)", :PG_GIRATINA],
 [:PG_ZYGARDE, :ZYGARDE, 98, :PRISM_ARENA, "Valen's memorial (Crownhaven)", :PG_ZYGARDE],
 [:PG_ARCEUS, :ARCEUS, 100, :PRISM_ARENA, "the Prism Arena, on the Ring where Valen held it", :PG_ARCEUS]].each do |id, sp, lv, field, where, quest|
  bars = (sp == :ARCEUS) ? { :CASUAL => 3, :STANDARD => 4, :HARD => 4, :default => 4 }
                         : { :CASUAL => 2, :STANDARD => 3, :HARD => 4, :default => 3 }
  legend.call(id, sp, lv, field, where, quest, :stub => true, :boss => { :bars => bars })
end
