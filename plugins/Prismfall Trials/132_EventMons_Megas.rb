#===============================================================================
# Prismfall Trials - 132 Event Pokemon for the Mega Stone quests (114_Quests_Megas.rb)
#-------------------------------------------------------------------------------
# Three Rejuvenation-style wild bosses that guard a Mega Stone. None of them joins
# (no :joins): they are someone's (Old Cinder), something's guardian (the Old
# Pincer), or a mother (the Matriarch). Levels: at or just under the cap of the
# badge count that opens them (12 badges -> cap 63, 15 -> 75, 16 -> 80).
# Wild Pokemon never Mega Evolve (Essentials), so the bosses fight in base form.
#===============================================================================
em = Prismfall::EventMons

em.register(:AS_OLD_CINDER, {
  :species => :CHARIZARD, :level => 72, :ability => :SOLARPOWER, :nature => :MODEST, :ivs => 28, :nickname => "Old Cinder",
  :moves => [:FLAMETHROWER, :AIRSLASH, :DRAGONPULSE, :ROOST],
  :kind => :boss, :field => :VOLCANIC, :badges => 15,
  :boss => { :bars => { :CASUAL => 1, :STANDARD => 2, :HARD => 3, :default => 2 },
             :stat_mults => { :HP => 1.2, :SPECIAL_DEFENSE => 1.1 },
             :intro => "Old Cinder spreads its scarred wings over the roost. The magma below flares to meet it!",
             :breaks => { 1 => { :message => "{1} remembers the front - and roars like it's still there!", :stats => { :SPECIAL_ATTACK => 1 } } } },
  :map => 248, :where => "Pyre Keep, the Dragon Roosts (high roost)", :chapter => 17,
  :quest => :AS_OLD_CINDER, :trigger => "Climb to the high roost and fight the grieving war-Charizard",
  :why => "Rejuvenation's boss-guarded stones; the reward is its old war-stone (Charizardite X), not the Charizard"
})

em.register(:EL_OLD_PINCER, {
  :species => :PINSIR, :level => 62, :ability => :MOXIE, :nature => :ADAMANT, :ivs => 28, :nickname => "Old Pincer",
  :moves => [:XSCISSOR, :CLOSECOMBAT, :STONEEDGE, :SWORDSDANCE],
  :kind => :boss, :field => :SILKWOOD, :badges => 12,
  :boss => { :bars => { :CASUAL => 1, :STANDARD => 2, :HARD => 3, :default => 2 },
             :stat_mults => { :HP => 1.25, :DEFENSE => 1.1 },
             :intro => "The Old Pincer unwinds from the sap tree, horns clacking like shears!",
             :breaks => { 1 => { :message => "{1} digs its claws into the bark and holds on!", :stats => { :DEFENSE => 1 } } } },
  :map => 703, :where => "Gossamer Heartwood, the great sap tree", :chapter => 14,
  :quest => :EL_OLD_PINCER, :trigger => "Free the Heartwood's sap tree (the Woodward's request)",
  :why => "Reborn's Pinsir fight, grown old; it drops the Pinsirite it has been clutching"
})

em.register(:IS_CAUSEWAY_MATRIARCH, {
  :species => :KANGASKHAN, :level => 78, :ability => :SCRAPPY, :nature => :ADAMANT, :ivs => 31, :nickname => "The Matriarch",
  :moves => [:DOUBLEEDGE, :DRAINPUNCH, :SUCKERPUNCH, :FAKEOUT],
  :kind => :boss, :badges => 16,
  :boss => { :bars => { :CASUAL => 2, :STANDARD => 3, :HARD => 3, :default => 3 },
             :stat_mults => { :HP => 1.3, :ATTACK => 1.1 },
             :intro => "The Matriarch plants her feet on the causeway's crown. Behind her, the young ones stop fishing to watch.",
             :breaks => { 1 => { :message => "{1} glances back at her young, and stands taller!", :stats => { :DEFENSE => 1 } },
                          2 => { :message => "{1} roars across the frozen flats!", :stats => { :ATTACK => 1 } } } },
  :map => 560, :where => "the Frostflat Causeway, the old cairn (low tide)", :chapter => 18,
  :quest => :IS_CAUSEWAY_MATRIARCH, :trigger => "Talk to her on the causeway's crown and prove you're worth the road",
  :why => "the strongest Mega Stone in the game (Parental Bond) behind the toughest wild boss, at 16 badges"
})
