# Festival cameo champions (design/CAMEOS.md). Levels are offsets from the ace (0).
# Sidequest cameos (design/CAMEOS.md, SPINE Rev 4): version 1 = the sidequest fight at its placement level,
# version 2 = post-game rematch at 100. Levels in team lists are offsets from the ace (0).
# versions: {version: (ace_level, mode)}; mode None = full team, "last4" = last four (tag-double halves), "flat" = all at ace.
PLACEMENT = {
    "FESTIVAL_SHELLY":    {1: (21, None), 2: (100, None)},   # Act I Gossamer Deepwood after Gym 2 (SPINE Rev 14), DOUBLE (v1 uses V1_TEAMS)
    "FESTIVAL_VENAM":     {1: (38, None), 2: (100, None)},   # Act II Miasma Caverns, :CORROSIVE_MIRE
    "FESTIVAL_GARRET":    {1: (46, None), 2: (100, None)},   # Act II Ironreach lower shafts, :COLOSSEUM
    "FESTIVAL_MELIA":     {1: (50, None), 2: (100, None)},   # Act III Royal Chase
    "FESTIVAL_ALEXANDRA": {1: (56, None), 2: (100, None)},   # Act III Rimeholt sunken town
    "FESTIVAL_AMARIA":    {1: (78, "last4"), 2: (100, None)},  # Act IV Aurelia, tag DOUBLE with Titania, :WATER_SURFACE
    "FESTIVAL_TITANIA":   {1: (78, "last4"), 2: (100, None)},
    "FESTIVAL_SHIV":      {1: (84, None), 2: (100, None)},   # Act V Gloaming dusk-chapels
    "FESTIVAL_LIN":       {1: (100, "flat")},                # post-game superboss
    "FESTIVAL_NOVA":      {1: (90, None)},                   # Ruin Route R5 Mirrorwalk
}

def CAMEOS(P):
    C = []
    def c(tt, nm, exhib, lose, mons, mega_std=False):
        C.append(dict(tt=tt, nm=nm, exhib=exhib, lose=lose, mons=mons, mega_std=mega_std))

    c("FESTIVAL_LIN", "Lin", 96, "hm. you're still holding it gently. keep doing that.", [
        P("FERROTHORN", -4, "IRONBARBS", "LEFTOVERS", "RELAXED", "STEALTHROCK,LEECHSEED,POWERWHIP,GYROBALL", "PD", tr=True),
        P("VOLCARONA", -2, "FLAMEBODY", "HEAVYDUTYBOOTS", "TIMID", "QUIVERDANCE,FIERYDANCE,BUGBUZZ,GIGADRAIN", "S"),
        P("GARDEVOIR", -2, "TRACE", "CHOICESPECS", "TIMID", "MOONBLAST,PSYCHIC,FOCUSBLAST,TRICK", "S",
          hard={"item": "GARDEVOIRITE", "moves": "HYPERVOICE,PSYSHOCK,FOCUSBLAST,CALMMIND"},
          casual={"item": "SITRUSBERRY", "moves": "MOONBLAST,PSYCHIC,FOCUSBLAST,CALMMIND"}),
        P("GARCHOMP", -1, "ROUGHSKIN", "LIFEORB", "JOLLY", "EARTHQUAKE,OUTRAGE,STONEEDGE,SWORDSDANCE", "A",
          casual={"item": "SITRUSBERRY"}),
        P("HYDREIGON", -1, "LEVITATE", "CHOICESCARF", "TIMID", "DRACOMETEOR,DARKPULSE,FLAMETHROWER,UTURN", "S",
          casual={"item": "SITRUSBERRY"}),
        P("TOGEKISS", 0, "SERENEGRACE", "LEFTOVERS", "TIMID", "OBLIVIONWING,DAZZLINGGLEAM,NASTYPLOT,ROOST", "S",
          hard={"moves": "OBLIVIONWING,DAZZLINGGLEAM,FLAMETHROWER,NASTYPLOT"},
          casual={"moves": "AIRSLASH,DAZZLINGGLEAM,NASTYPLOT,ROOST"}),
    ])
    c("FESTIVAL_AMARIA", "Amaria", 93, "Oh... the water says you won. I think I knew that.", [
        P("STARMIE", -3, "NATURALCURE", "LIFEORB", "TIMID", "HYDROPUMP,PSYCHIC,ICEBEAM,THUNDERBOLT", "S", nick="Twinkle",
          casual={"item": "SITRUSBERRY"}),
        P("GOLISOPOD", -3, "EMERGENCYEXIT", "ASSAULTVEST", "ADAMANT", "FIRSTIMPRESSION,LIQUIDATION,LEECHLIFE,KNOCKOFF", "BA"),
        P("LUDICOLO", -2, "SWIFTSWIM", "LIFEORB", "MODEST", "HYDROPUMP,GIGADRAIN,ICEBEAM,RAINDANCE", "S", nick="Indiana",
          casual={"item": "SITRUSBERRY"}),
        # Water Surface (v1): the water soothes burns, so the Flame Orb + Marvel Scale trick doesn't hold. Competitive
        # punishes Intimidate in the tag double instead.
        P("MILOTIC", -2, "COMPETITIVE", "LEFTOVERS", "BOLD", "SCALD,ICEBEAM,RECOVER,HAZE", "BPD"),
        P("KINGDRA", -1, "SWIFTSWIM", "DAMPROCK", "MODEST", "HYDROPUMP,DRACOMETEOR,ICEBEAM,RAINDANCE", "S", nick="Atlantica"),
        P("LAPRAS", 0, "SHELLARMOR", "LEFTOVERS", "MODEST", "SPARKLINGARIA,FREEZEDRY,THUNDERBOLT,HYDROPUMP", "BS",
          nick="Deliverer", hard={"ab": "WATERABSORB", "item": "ASSAULTVEST"}),
    ])
    c("FESTIVAL_SHELLY", "Shelly", 93, "S-sorry! Um. That was really good. Your bugs— er, Pokémon— are lovely.", [
        P("MASQUERAIN", -3, "INTIMIDATE", "FOCUSSASH", "TIMID", "STICKYWEB,AIRSLASH,BUGBUZZ,QUIVERDANCE", "S"),
        P("GALVANTULA", -2, "COMPOUNDEYES", "LIFEORB", "TIMID", "THUNDER,BUGBUZZ,ELECTROWEB,STICKYWEB", "S",
          casual={"item": "SITRUSBERRY"}),
        P("ARAQUANID", -2, "WATERBUBBLE", "SITRUSBERRY", "ADAMANT", "LIQUIDATION,LEECHLIFE,WIDEGUARD,PROTECT", "HA"),
        P("FROSMOTH", -1, "ICESCALES", "LEFTOVERS", "TIMID", "QUIVERDANCE,ICEBEAM,BUGBUZZ,HURRICANE", "S"),
        P("SCIZOR", -1, "TECHNICIAN", "LIFEORB", "ADAMANT", "BULLETPUNCH,UTURN,KNOCKOFF,SWORDSDANCE", "HA",
          casual={"item": "METALCOAT"}),
        P("VOLCARONA", 0, "FLAMEBODY", "HEAVYDUTYBOOTS", "MODEST", "HEATWAVE,BUGBUZZ,QUIVERDANCE,PROTECT", "S",
          hard={"moves": "HEATWAVE,BUGBUZZ,QUIVERDANCE,GIGADRAIN"}),
    ])
    c("FESTIVAL_ALEXANDRA", "Alexandra", 95, "Thank you. ...If yours wake up, will you write to me?", [
        P("SIGILYPH", -4, "MAGICGUARD", "LIFEORB", "TIMID", "PSYCHIC,AIRSLASH,HEATWAVE,COSMICPOWER", "S"),
        P("STARMIE", -3, "ANALYTIC", "LIFEORB", "TIMID", "HYDROPUMP,PSYCHIC,ICEBEAM,RECOVER", "S", casual={"item": "SITRUSBERRY"}),
        # Her sidequest fight is in Rimeholt's sunken lower town (open water after the Thaw): Earthquake and Stealth Rock
        # fail on Water Surface, so the dragons carry moves that work there.
        P("ALTARIA", -2, "NATURALCURE", "LEFTOVERS", "JOLLY", "DRAGONDANCE,DRAGONCLAW,IRONTAIL,ROOST", "A"),
        P("GARCHOMP", -2, "ROUGHSKIN", "ROCKYHELMET", "JOLLY", "DRAGONCLAW,STONEEDGE,IRONHEAD,SWORDSDANCE", "A"),
        P("DRAGONITE", -1, "MULTISCALE", "LUMBERRY", "ADAMANT", "DRAGONDANCE,EXTREMESPEED,DRAGONCLAW,FIREPUNCH", "A"),
        P("LATIAS", 0, "LEVITATE", "SOULDEW", "TIMID", "DRACOMETEOR,PSYCHIC,CALMMIND,RECOVER", "S",
          hard={"item": "LATIASITE", "moves": "DRACOMETEOR,PSYSHOCK,MISTBALL,RECOVER"},
          casual={"item": "SITRUSBERRY"}),
    ])
    c("FESTIVAL_VENAM", "Venam", 93, "Okay, OKAY, you're good! Don't let it go to your head, glass-boy-or-girl!", [
        P("TOXTRICITY", -3, "PUNKROCK", "THROATSPRAY", "MODEST", "OVERDRIVE,SLUDGEBOMB,BOOMBURST,VOLTSWITCH", "S"),
        P("GARBODOR", -3, "AFTERMATH", "ROCKYHELMET", "ADAMANT", "GUNKSHOT,DRAINPUNCH,TOXICSPIKES,STOMPINGTANTRUM", "BA"),
        P("MUK", -2, "POISONTOUCH", "ASSAULTVEST", "ADAMANT", "POISONJAB,KNOCKOFF,FIREPUNCH,SHADOWSNEAK", "BA", form=1),
        # Corrosive Mire (v1): Venoshock is always doubled against grounded targets; Corrosion is +1 Attack on entry;
        # two Flamethrowers burn the marsh gas off (-> Wasteland) and scorch grounded foes on the way.
        P("SALAZZLE", -2, "CORROSION", "BLACKSLUDGE", "TIMID", "VENOSHOCK,SLUDGEBOMB,FLAMETHROWER,NASTYPLOT", "S", gender="female"),
        # Synthetic Seed on the Mire: +1 Atk, +1 Sp. Atk and a poisoning a Poison type shrugs off.
        P("TOXICROAK", -1, "DRYSKIN", "SYNTHETICSEED", "JOLLY", "GUNKSHOT,DRAINPUNCH,SUCKERPUNCH,SWORDSDANCE", "A",
          casual={"item": "BLACKSLUDGE"}),
        P("SEVIPER", 0, "INFILTRATOR", "LIFEORB", "NAIVE", "POISONJAB,FLAMETHROWER,EARTHQUAKE,SUCKERPUNCH", "MX",
          casual={"item": "BLACKSLUDGE", "ab": "SHEDSKIN"}),
    ])
    c("FESTIVAL_SHIV", "Shiv", 94, "Huh. In the dream, you lost. Dreams lie. Most of them, anyway.", [
        P("SABLEYE", -4, "PRANKSTER", "LEFTOVERS", "CAREFUL", "WILLOWISP,FOULPLAY,RECOVER,TAUNT", "SD"),
        P("LIEPARD", -3, "PRANKSTER", "FOCUSSASH", "JOLLY", "FAKEOUT,FOULPLAY,ENCORE,THUNDERWAVE", "A"),
        P("HYPNO", -2, "INSOMNIA", "LEFTOVERS", "CALM", "PSYCHIC,FOCUSBLAST,TRICKROOM,NASTYPLOT", "SD"),
        P("MALAMAR", -2, "CONTRARY", "SITRUSBERRY", "ADAMANT", "SUPERPOWER,KNOCKOFF,PSYCHOCUT,TOPSYTURVY", "BA"),
        P("CINCCINO", -1, "SKILLLINK", "KINGSROCK", "JOLLY", "TAILSLAP,ROCKBLAST,BULLETSEED,UTURN", "A"),
        P("AMBIPOM", 0, "TECHNICIAN", "SILKSCARF", "JOLLY", "FAKEOUT,DOUBLEHIT,KNOCKOFF,UTURN", "HS", nick="Aipom",
          hard={"moves": "FAKEOUT,DOUBLEHIT,KNOCKOFF,TAUNT", "item": "LIFEORB", "ev": "HA"}),
    ])
    c("FESTIVAL_GARRET", "Garret", 94, "...Good. Now we talk.", [
        P("HARIYAMA", -4, "GUTS", "FLAMEORB", "ADAMANT", "CLOSECOMBAT,KNOCKOFF,BULLETPUNCH,HEAVYSLAM", "HA",
          casual={"item": "SITRUSBERRY"}),
        P("SCRAFTY", -3, "INTIMIDATE", "LEFTOVERS", "CAREFUL", "DRAINPUNCH,KNOCKOFF,BULKUP,FAKEOUT", "SPD"),
        P("BRELOOM", -2, "TECHNICIAN", "LIFEORB", "JOLLY", "MACHPUNCH,BULLETSEED,ROCKTOMB,SPORE", "A",
          casual={"moves": "MACHPUNCH,BULLETSEED,ROCKTOMB,STUNSPORE", "item": "SITRUSBERRY"}),
        P("PANGORO", -2, "IRONFIST", "ASSAULTVEST", "ADAMANT", "DRAINPUNCH,KNOCKOFF,ICEPUNCH,BULLETPUNCH", "HA"),
        # Colosseum (v1): Steadfast is +1 crit stage here and the Leek +2, so every hit is a critical hit.
        P("SIRFETCHD", -1, "STEADFAST", "LEEK", "JOLLY", "METEORASSAULT,CLOSECOMBAT,BRAVEBIRD,KNOCKOFF", "A"),
        P("LUCARIO", 0, "JUSTIFIED", "LUCARIONITE", "JOLLY", "SWORDSDANCE,CLOSECOMBAT,METEORMASH,EXTREMESPEED", "A",
          casual_item_fallback="LIFEORB"),
    ], mega_std=True)
    c("FESTIVAL_MELIA", "Melia", 92, "You decided. I can see it. ...I'm glad.", [
        P("SNORLAX", -3, "THICKFAT", "LEFTOVERS", "CAREFUL", "BODYSLAM,CURSE,REST,EARTHQUAKE", "SPD"),
        P("LOPUNNY", -2, "LIMBER", "LIFEORB", "JOLLY", "FAKEOUT,HIGHJUMPKICK,RETURN,ICEPUNCH", "A", casual={"item": "SITRUSBERRY"}),
        P("MIMIKYU", -2, "DISGUISE", "LIFEORB", "JOLLY", "PLAYROUGH,SHADOWCLAW,SHADOWSNEAK,SWORDSDANCE", "A",
          casual={"item": "SITRUSBERRY"}),
        P("DUDUNSPARCE", -1, "SERENEGRACE", "LEFTOVERS", "CALM", "HYPERDRILL,AIRSLASH,GLARE,ROOST", "SD"),
        P("ZOROARK", -1, "ILLUSION", "LIFEORB", "TIMID", "NIGHTDAZE,FLAMETHROWER,FOCUSBLAST,NASTYPLOT", "S",
          casual={"item": "SITRUSBERRY"}),
        P("TOGEKISS", 0, "SERENEGRACE", "LEFTOVERS", "BOLD", "AIRSLASH,DAZZLINGGLEAM,WISH,PROTECT", "BS", nick="Hapi",
          hard={"moves": "AIRSLASH,DAZZLINGGLEAM,NASTYPLOT,ROOST"}),
    ])
    c("FESTIVAL_TITANIA", "Titania", 94, "Hmph. A worthy blade. Amaria, we're leaving— no, fine, ONE photo.", [
        P("KLEFKI", -4, "PRANKSTER", "LIGHTCLAY", "BOLD", "REFLECT,LIGHTSCREEN,SPIKES,PLAYROUGH", "PD"),
        P("ESCAVALIER", -3, "OVERCOAT", "ASSAULTVEST", "ADAMANT", "IRONHEAD,MEGAHORN,KNOCKOFF,DRILLRUN", "HA", tr=True),
        P("CORVIKNIGHT", -2, "MIRRORARMOR", "LEFTOVERS", "IMPISH", "BRAVEBIRD,BODYPRESS,BULKUP,ROOST", "BPD"),
        P("MAWILE", -2, "INTIMIDATE", "LIFEORB", "ADAMANT", "PLAYROUGH,IRONHEAD,SUCKERPUNCH,SWORDSDANCE", "HA",
          hard={"item": "MAWILITE"}, casual={"item": "SITRUSBERRY"}),
        P("KINGAMBIT", -1, "SUPREMEOVERLORD", "BLACKGLASSES", "ADAMANT", "KOWTOWCLEAVE,IRONHEAD,SUCKERPUNCH,SWORDSDANCE", "HA",
          casual={"ab": "DEFIANT"}),
        P("AEGISLASH", 0, "STANCECHANGE", "WEAKNESSPOLICY", "QUIET", "KINGSSHIELD,SHADOWBALL,SACREDSWORD,SHADOWSNEAK", "BS",
          casual={"item": "LEFTOVERS"}),
    ])
    c("FESTIVAL_NOVA", "Nova", 96, "Wake up, then. ...It'll still be here when you're tired.", [
        P("BANETTE", -4, "CURSEDBODY", "SITRUSBERRY", "ADAMANT", "SHADOWCLAW,SHADOWSNEAK,GUNKSHOT,WILLOWISP", "A",
          hard={"item": "BANETTITE", "ab": "FRISK"}),
        P("FARIGIRAF", -3, "ARMORTAIL", "LEFTOVERS", "MODEST", "TWINBEAM,HYPERVOICE,NASTYPLOT,THUNDERBOLT", "BS"),
        P("MUSHARNA", -2, "TELEPATHY", "LEFTOVERS", "BOLD", "MOONBLAST,PSYCHIC,YAWN,CALMMIND", "BPD"),
        P("REUNICLUS", -2, "MAGICGUARD", "LIFEORB", "QUIET", "PSYCHIC,FOCUSBLAST,SHADOWBALL,TRICKROOM", "BS", tr=True,
          casual={"item": "SITRUSBERRY"}),
        P("ESPATHRA", -1, "OPPORTUNIST", "LIFEORB", "TIMID", "LUMINACRASH,DAZZLINGGLEAM,SHADOWBALL,CALMMIND", "S",
          casual={"item": "SITRUSBERRY"}),
        P("GOTHITELLE", 0, "SHADOWTAG", "LEFTOVERS", "BOLD", "PSYCHIC,THUNDERBOLT,CALMMIND,REST", "BPD",
          casual={"ab": "COMPETITIVE"}),
    ])
    V1 = {"FESTIVAL_SHELLY": [
        P("MASQUERAIN", -1, "INTIMIDATE", "SITRUSBERRY", "TIMID", "STRUGGLEBUG,BUBBLEBEAM,QUICKATTACK,STICKYWEB", "S"),
        P("JOLTIK", -1, "COMPOUNDEYES", "ORANBERRY", "TIMID", "ELECTROWEB,STRUGGLEBUG,BUGBITE,THUNDERWAVE", "S", only="nocasual"),
        P("ARAQUANID", 0, "WATERBUBBLE", "SITRUSBERRY", "ADAMANT", "BUBBLEBEAM,BUGBITE,WIDEGUARD,PROTECT", "HA", only="hard"),
        P("LARVESTA", 0, "FLAMEBODY", "ORANBERRY", "MODEST", "FLAMECHARGE,STRUGGLEBUG,LEECHLIFE,STRINGSHOT", "S"),
        P("SCYTHER", 0, "TECHNICIAN", "EVIOLITE", "JOLLY", "FURYCUTTER,WINGATTACK,QUICKATTACK,FOCUSENERGY", "A",
          hard={"moves": "BUGBITE,AERIALACE,QUICKATTACK,SWORDSDANCE"}),
    ]}
    for cm in C:
        cm["versions"] = PLACEMENT[cm["tt"]]
        cm["v1_mons"] = V1.get(cm["tt"])
    return C
