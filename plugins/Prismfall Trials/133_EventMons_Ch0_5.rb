#===============================================================================
# Prismfall Trials - 133 Event Pokemon for the early side content, Chapters 0-5
# (116_Quests_Early.rb, 2026-11-21)
#-------------------------------------------------------------------------------
# Same rules as 130: :badges = the fewest badges with which the player can obtain
# it (the headless test recomputes it from the quest data); nothing obtainable
# with b badges is a type answer to Warden b+1 or b+2 (warden_gates.json:
# Dorian Fighting/Ghost; Tamsin Fire/Flying/Rock; Marisol Electric/Grass; Rook
# Ground), counting what the line becomes by level at or below that cap; no
# tailored answer moves (no Mega Drain on a Sandygast before Marisol, no Dig on
# a Greavard before Rook). Levels sit just under the chapter's cap; a boss is at
# or above the cap and joins below it. Caps: 15 / 19 / 23 / 27 / 31.
#===============================================================================
em = Prismfall::EventMons

#--- Chapter 0 -> 1: the last ferry's stowaways ------------------------------------
em.register(:EL_TANDEMAUS, {
  :species => :TANDEMAUS, :level => 6, :ability => :PICKUP, :nature => :JOLLY, :ivs => 20, :nickname => "Plus-One",
  :moves => [:POUND, :BABYDOLLEYES, :ECHOEDVOICE, :TICKLE], :obtain_text => "the last ferry",
  :kind => :gift, :badges => 0,
  :map => 100, :where => "Ferrow's Landing quay (the crate came across on the last ferry; the mice hid by Crate 7-B)", :chapter => 1,
  :quest => :EL_STOWAWAYS, :trigger => "Keep the squeaking crate quiet on the Dovetail (Ch0), then find the mice in the customs hall after your starter",
  :why => "A foreign stowaway: no Tandemaus lives in Velmora. Pickup finds items, Super Fang at 11; Normal answers neither Dorian nor Tamsin. Maushold at 25"
})

#--- Chapter 2, after the Pageant (S108) and Badge 1 ---------------------------------
em.register(:EL_SANDYGAST, {
  :species => :SANDYGAST, :level => 20, :ability => :WATERCOMPACTION, :nature => :BOLD, :ivs => 25, :nickname => "Crown",
  :moves => [:SANDTOMB, :ASTONISH, :SANDATTACK, :HARDEN],
  :kind => :boss, :field => :BEACH, :badges => 1,
  :boss => { :bars => { :CASUAL => 1, :STANDARD => 2, :HARD => 2, :default => 2 },
             :stat_mults => { :HP => 1.15, :DEFENSE => 1.1 },
             :intro => "The sand Crown heaves itself up out of the dune!",
             :breaks => { 1 => { :message => "{1} pulls the beach up round itself and rebuilds, taller!", :stats => { :DEFENSE => 1 } } } },
  :joins => { :level => 16 }, :join_choice => true,
  :map => 528, :where => "the sand Crown on Marram Down (after dark)", :chapter => 2,
  :quest => :EL_SAND_CROWN, :trigger => "Watch the sculptor's Crown after dark, beat the boss, then take it or leave it to be the Crown",
  :why => "Rejuvenation-style boss reward after Dorian: Water Compaction and Ghost/Ground (it was already a 2-3% wild find on Marram Down); no Mega Drain, so no Grass answer for Marisol"
})

#--- Chapter 3, after the Glass Matriarch (S107); hatches with Badge 3 -------------------
em.register(:EL_JOLTIK, {
  :species => :JOLTIK, :level => 22, :ability => :COMPOUNDEYES, :nature => :TIMID, :ivs => 25,
  :moves => [:ELECTROWEB, :BUGBITE, :THUNDERWAVE, :ELECTROBALL], :obtain_text => "the Matriarch's last cocoon",
  :kind => :gift, :badges => 3, :on_ko => :retry,
  :map => 548, :where => "Cocoonfall Hollow, the Matriarch's glass cocoons (after Badge 3)", :chapter => 3,
  :quest => :EL_MATRIARCH_HUM, :trigger => "Hear the cocoon in Ch3; it hatches to your badge case's third note. Soothed Matriarch: it comes to you. Silenced: it fights (catch it)",
  :why => "The Glass Matriarch's heir: Compound Eyes Electroweb Joltik (Galvantula at 36). Electric answers Marisol, so it waits for her badge (Revision 16)"
})

#--- Chapter 4: the Wolfsrime (579) ---------------------------------------------------
em.register(:EL_GREAVARD, {
  :species => :GREAVARD, :level => 20, :ability => :FLUFFY, :nature => :ADAMANT, :ivs => 20, :nickname => "Bracken",
  :moves => [:LICK, :BITE, :HEADBUTT, :HOWL], :item => :ORANBERRY,
  :kind => :battle, :on_ko => :retry, :badges => 2,
  :map => 579, :where => "the old den on the Wolfsrime", :chapter => 4,
  :quest => :EL_DROVERS_BELL, :trigger => "Ring the drover's bell, follow what answers to the den, and play (battle, then catch)",
  :why => "The drovers' dog, fifty years late: Fluffy Greavard with Howl (egg move); no Dig before Rook. Ghost answers neither Marisol nor Rook. Houndstone at 30, at night"
})

#--- Chapter 5: Ebb Hollow (588) and Lumen (185) -------------------------------------
em.register(:IS_CORSOLA, {
  :species => :CORSOLA, :form => 1, :level => 24, :ability => :CURSEDBODY, :nature => :CALM, :ivs => 25,
  :moves => [:ASTONISH, :DISABLE, :SPITE, :ANCIENTPOWER],
  :kind => :battle, :field => :BLEED, :on_ko => :retry, :badges => 3,
  :map => 588, :where => "Ebb Hollow, over the last boundary stone by the eel-weir (Bleed)", :chapter => 5,
  :quest => :IS_EBB_HOLLOW, :trigger => "Read two boundary stones in the drowned village, then free the third from the white coral",
  :why => "An Imprinted variant found only under the Bleed (as the Orchard's Galarian Ponyta): Cursed Body Galarian Corsola, Cursola at 38. Ghost is no answer to Rook"
})

em.register(:ZE_PORYGON, {
  :species => :PORYGON, :level => 24, :ability => :DOWNLOAD, :nature => :MODEST, :ivs => 20,
  :moves => [:TACKLE, :CONVERSION, :THUNDERSHOCK, :PSYBEAM], :obtain_text => "Form 0, Meridian Spire",
  :kind => :gift, :badges => 3,
  :map => 185, :where => "the helpdesk in the Meridian Spire lobby", :chapter => 5,
  :quest => :ZE_CUSTOMER_SUPPORT, :trigger => "Cancel the form that cancels the form",
  :why => "Download Porygon (the Upgrade and Dubious Disc lines) in Zenith, Act I. Normal answers neither Rook nor Sahar"
})
