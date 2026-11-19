#===============================================================================
# Prismfall Trials - 131 Event Pokemon, Chapters 5+ (designed; :stub => true)
#-------------------------------------------------------------------------------
# Rewards of the catalogue quests (120). Registered so the harness checks the
# species/forms/abilities/moves and the doc tool can list them; moves left out
# use the level-up set. Levels sit a few below the level cap of the chapter.
#===============================================================================
em = Prismfall::EventMons
later = lambda { |id, h| em.register(id, h.merge(:stub => true)) }

#--- Zenith -------------------------------------------------------------------------
later.call(:ZE_PORYGON, { :species => :PORYGON, :level => 24, :ability => :DOWNLOAD, :kind => :gift, :chapter => 5,
  :map => 185, :where => "Meridian Spire lobby", :quest => :ZE_CUSTOMER_SUPPORT, :trigger => "Cancel the form that cancels the form",
  :why => "Download Porygon: the Upgrade and Dubious Disc lines in Zenith, Act I" })
later.call(:ZE_DEX_PICHU, { :species => :PICHU, :level => 25, :ability => :LIGHTNINGROD, :kind => :gift, :chapter => 6,
  :moves => [:VOLTTACKLE, :NASTYPLOT, :CHARM, :SWEETKISS], :special_moves => [:VOLTTACKLE], :nickname => "Spark",
  :map => 608, :where => "Dex's shrine in the Shattered Lowlight", :quest => :ZE_LOWLIGHT_LAMPS, :trigger => "Sit with the shrine at dusk",
  :why => "Volt Tackle Pichu (no other source) and the emotional heart of the Lowlight" })
later.call(:ZE_KLEFKI, { :species => :KLEFKI, :level => 50, :ability => :PRANKSTER, :kind => :gift, :chapter => 12,
  :map => 730, :where => "Anchorhold", :quest => :ZE_COURIER, :trigger => "Hide the key-ring from the embargo inspectors",
  :why => "Prankster Steel/Fairy screen-setter" })

#--- Nadir --------------------------------------------------------------------------
later.call(:NA_GRIMER, { :species => :GRIMER, :form => 1, :level => 30, :ability => :POISONTOUCH, :kind => :gift, :chapter => 7,
  :map => 220, :where => "the Mirefen noodle cart", :quest => :NA_NOODLE_SCORE, :trigger => "Score a five out of ten",
  :why => "Alolan Grimer (Poison/Dark): an Imprinted variant found only near Mirefen" })
later.call(:NA_FALINKS, { :species => :FALINKS, :level => 38, :ability => :DEFIANT, :kind => :boss, :chapter => 9,
  :boss => { :bars => 3, :stat_mults => { :HP => 1.2 } }, :joins => { :level => 36 },
  :map => 263, :where => "the Iron Pit, Ironreach", :quest => :NA_PIT_RINGER, :trigger => "Win six bouts, then beat the Brass Formation",
  :why => "No Guard / Defiant Fighting type with No Retreat before Kaito's Colosseum" })
later.call(:NA_POLTCHAGEIST, { :species => :POLTCHAGEIST, :level => 72, :ability => :HOSPITALITY, :kind => :gift, :chapter => 18,
  :map => 423, :where => "the Moon Market, Underveil", :quest => :NA_SWEETROT, :trigger => "Brew Larch's kelp tea for the Sweetrot vendors",
  :why => "Grass/Ghost with Hospitality; pays off running gag 1" })

#--- Ashkaar ------------------------------------------------------------------------
later.call(:AS_DRUDDIGON, { :species => :DRUDDIGON, :level => 37, :ability => :ROUGHSKIN, :kind => :boss, :chapter => 8, :field => :VOLCANIC,
  :boss => { :bars => 2, :stat_mults => { :HP => 1.15 } }, :joins => { :level => 35 },
  :map => 664, :where => "Mt. Cinder lava tubes", :quest => :AS_DRUDDIGON, :trigger => "Beat the lava-tube boss",
  :why => "Rough Skin Dragon with Dragon Tail; Dragon has 13 families by Badge 8 and this is the bulkiest" })
later.call(:AS_NOIBAT, { :species => :NOIBAT, :level => 36, :ability => :INFILTRATOR, :kind => :gift, :chapter => 8,
  :map => 248, :where => "the Dragon Roosts, Cindervault", :quest => :AS_AFRAID_OF_HEIGHTS, :trigger => "Train Tamm's Trapinch until it flies",
  :why => "Flying/Dragon speedster (Noivern) in the Dragon kingdom" })
later.call(:AS_HOUNDOUR, { :species => :HOUNDOUR, :level => 34, :ability => :FLASHFIRE, :kind => :gift, :chapter => 8,
  :moves => [:FIREFANG, :SUCKERPUNCH, :BITE, :HOWL],
  :map => 650, :where => "Scaldwater", :quest => :AS_ASHES, :trigger => "Carry a legionnaire's urn home",
  :why => "Sucker Punch Houndour (egg move) and a story about who the war is spending" })
later.call(:AS_AXEW_EGG, { :species => :AXEW, :level => 1, :kind => :egg, :chapter => 9,
  :map => 248, :where => "the far roost, Mt. Cinder", :quest => :AS_EGG_RUN, :trigger => "Keep the egg warm across Mt. Cinder",
  :why => "The earliest Axew (wild only from Badge 17): Haxorus" })

#--- Ossaria ------------------------------------------------------------------------
later.call(:OS_CARBINK, { :species => :CARBINK, :level => 28, :ability => :STURDY, :nickname => "Kevin", :kind => :gift, :chapter => 6,
  :map => 209, :where => "the Dig Lab, Duneholt", :quest => :OS_KEVIN, :trigger => "Wake Kevin",
  :why => "Rock/Fairy wall with Reflect/Light Screen; Kevin" })
later.call(:OS_TRAPINCH, { :species => :TRAPINCH, :level => 27, :ability => :SHEERFORCE, :kind => :gift, :chapter => 6,
  :map => 610, :where => "Copperdune", :quest => :OS_RIDDLE_CARAVAN, :trigger => "Answer the riddle trader's riddles",
  :why => "Sheer Force Trapinch (hidden ability) on the way to Flygon" })
later.call(:OS_STUNFISK, { :species => :STUNFISK, :form => 1, :level => 31, :ability => :MIMICRY, :kind => :boss, :chapter => 7, :field => :DESERT,
  :boss => { :bars => 2, :stat_mults => { :HP => 1.2, :DEFENSE => 1.1 } }, :joins => { :level => 30 },
  :map => 628, :where => "Sinkfield", :quest => :OS_SINKFIELD, :trigger => "Beat the sinkhole boss",
  :why => "Galarian Stunfisk (Ground/Steel, Mimicry changes type with the field): made for a field game" })
later.call(:OS_YAMASK, { :species => :YAMASK, :form => 1, :level => 60, :ability => :WANDERINGSPIRIT, :kind => :gift, :chapter => 14,
  :map => 770, :where => "Vigil", :quest => :OS_UNQUIET_ELECTOR, :trigger => "Hold the dead Elector's last election",
  :why => "Galarian Yamask (Ground/Ghost) for Runerigus" })

#--- Elowen (later) -------------------------------------------------------------------
later.call(:EL_GERALD, { :species => :SCATTERBUG, :level => 40, :ability => :COMPOUNDEYES, :nickname => "Gerald", :kind => :gift, :chapter => 10,
  :map => 682, :where => "the Royal Chase", :quest => :EL_GERALD, :trigger => "Find all six royal Scatterbugs; Gerald last",
  :why => "Compound Eyes Vivillon line with Quiver Dance (and Gerald's four-page personality file)" })
later.call(:EL_EVER_BLOOM, { :species => :FLOETTE, :form => 4, :level => 44, :ability => :FLOWERVEIL, :nickname => "Ever-Bloom", :kind => :gift, :chapter => 10,
  :map => 294, :where => "the Heartgarden, Verdance", :quest => :EL_EVER_BLOOM, :trigger => "Carry Juno's message to the Bride Tree",
  :why => "White Floette from the Bride Tree's blossoms (Florges with a Shiny Stone); a Juno keepsake" })

#--- Isenmar (later) -----------------------------------------------------------------
later.call(:IS_WHITE_STAG, { :species => :SAWSBUCK, :form => 3, :level => 48, :ability => :SAPSIPPER, :kind => :battle, :chapter => 11,
  :map => 701, :where => "the Northern Rimewood", :quest => :IS_WHITE_STAG, :trigger => "Corner the white stag at dawn",
  :why => "Sap Sipper Sawsbuck; the winter coat is cosmetic (Essentials sets the season form) but the stag is the point" })
later.call(:IS_CETODDLE, { :species => :CETODDLE, :level => 46, :ability => :THICKFAT, :kind => :gift, :chapter => 11,
  :map => 300, :where => "Lake Rime", :quest => :IS_HARPOON_RITE, :trigger => "Stand your ground against the Old Bull",
  :why => "Thick Fat Ice type with Ice Shard; a calf of the Old Bull" })
later.call(:IS_TATSUGIRI, { :species => :TATSUGIRI, :form => 1, :level => 48, :ability => :COMMANDER, :kind => :gift, :chapter => 11,
  :map => 300, :where => "the ice-fishing flats, Rimeholt", :quest => :IS_ELEVEN_YEARS, :trigger => "Land the bite Torstein waited eleven years for",
  :why => "Dragon/Water with Commander for doubles" })

#--- Antumbra --------------------------------------------------------------------------
later.call(:AN_INDEEDEE, { :species => :INDEEDEE, :form => 1, :level => 55, :ability => :PSYCHICSURGE, :kind => :gift, :chapter => 13,
  :map => 753, :where => "Glassmere", :quest => :AN_OTHER_HALF, :trigger => "Choose between two husbands",
  :why => "Psychic Surge setter that came back 'reversed' (the female form, male household)" })
later.call(:AN_HATENNA, { :species => :HATENNA, :level => 54, :ability => :MAGICBOUNCE, :kind => :gift, :chapter => 13,
  :map => 743, :where => "the Antumbra Threshold", :quest => :AN_UMBRELLA, :trigger => "Open the umbrella indoors (which is outdoors)",
  :why => "Magic Bounce Hatterene line" })

#--- Crownhaven ------------------------------------------------------------------------
later.call(:CR_PRISM_EEVEE, { :species => :EEVEE, :level => 50, :shiny => true, :ability => :ADAPTABILITY, :nickname => "Prism", :kind => :gift, :chapter => 20,
  :map => 890, :where => "Pilgrim's Rest", :quest => :CR_EIGHTEEN_SHRINES, :trigger => "Visit all eighteen shrines on the Pilgrim Pass",
  :why => "A shiny 'prism-coated' Eevee for any Eeveelution, after the Octave gauntlet" })
