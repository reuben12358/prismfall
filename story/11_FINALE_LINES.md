# Story Bible 11: Finale Lines — the Eighteen Locks

> For the True Finale (08_ACT_V, Ch21): six bars of three locks, in gym order. Between bars, the three Wardens of that bar **release** or **refuse**. Conditions are `WARDEN_CONSENT` in NARRATIVE_KEYS §5. Every refusal has a reason the player caused. A refusal forces the next lock (Arceus +1 all stats for that bar).
> Staging: the Warden kneels at their pylon; one line; on release the golden lock opens and the Plate rises into Arceus's wheel; on refusal they grip the pylon and the lock stays shut.
> §3 gives the *Homecoming, Unfinished* slide for each refusing Warden's city.

## 1. Release lines

| # | Warden (Plate) | Release line |
|---|---|---|
| 1 | Dorian (Blank) | "Three hundred years of pageants, and this is the only true scene I ever staged. Exit, pursued by nothing. Lights down." |
| 2 | Tamsin (Insect) | "Granny wove a whole village around this. I think she'd want me to finish the pattern. *Cut the thread.*" |
| 3 | Marisol (Splash) | "The Ebb ran both ways because of this. It'll run one way now, like any honest river. Go on, tides take you." |
| 4 | Rook (Zap) | "First time I've ever held it. Kinda thought it'd be heavier. ...Stay charged, wherever you're going." |
| 5 | Sahar (Earth) | "The desert keeps everything. I'm asking it, just this once, to give something back." |
| 6 | Corvin (Toxic) | "Dose makes the cure. Three hundred years is rather over the dose. Off you go, dear." |
| 7 | Brann (Flame) | "Forge it to break right, lad. Forge it to break *right*." *(He's weeping.)* |
| 8 | Kaito (Fist) | "A fist is a promise. So is an open hand." *(He opens it.)* |
| 9 | Juno (Meadow) | "Verdance has never had an autumn. I'd like to see one." *(She is always the first to let go in her bar.)* |
| 10 | Anja (Icicle) | "We'll move south. We've hauled heavier things than a city. Take it before I count my grandchildren's toes again." |
| 11 | Odessa (Sky) | "The wind doesn't care who owns it. Never did. Fly home." |
| 12 | Ilsa (Mind) | "I've heard everyone's thoughts but yours. I'd like the quiet. Go." *(If reconciled, she says it with one hand still on her father's shoulder.)* |
| 13 | Bastian (Stone) | "First time in three hundred years a Warden's had nothing in his keeping. Feels like setting down a sack of stone. Go on, then." |
| 14 | Ysolde (Spooky) | "Go home. All of you. Go home." *(The echoes in the stands fade as she says it. If Kestrel is beside her, he puts his hand over hers on the pylon.)* |
| 15 | Magnus (Iron) | "Tolerances exceeded. I'm releasing the part." *(A beat.)* "That was a joke. I'm told I should make them." |
| 16 | Nyx (Dread) | "My family kept one secret for three hundred years. I'm keeping none. It's yours, sweetheart. Take the dark with you." |
| 17 | Celestine (Pixie) | *(sung)* "Not chained, not broken, not bought, not crowned: given back, as a gift is found." |
| 18 | Sigrun (Draco) | "Dragons don't let anything through they haven't weighed. I've weighed this. It's too heavy for anyone. Go." |

## 2. Refusal lines (with the cause)

| # | Warden | Condition that fails | Refusal line |
|---|---|---|---|
| 1 | Dorian | `:ch5_lowlight_testimony` = mourner (you told the official story on record) | "You told them the pageant version, darling. So did I, for thirty years. I find I can't stop on cue." |
| 2 | Tamsin | `:ch2_tamsin` = keep_secret (the pylon still drains Briarwick) | "I can't. I *can't*. The contract's still running and there's nothing left in the village but this. I'm sorry — sorry —" |
| 3 | Marisol | Teo not saved and Bond < 3 | "My brother's in the river mud because of what this thing started. It owes Ebbmouth. It *stays*." |
| 4 | Rook | neither `ROOK_CUTS_GRID` nor `MARCHETTI_TURNED` (he can't reach his Plate) | "It's not mine to give! It never was! It's in *their* cradle, I can't even — chat, I can't reach it." |
| 5 | Sahar | `:ch6_drillsite` = directorate | "I buried the truth once because someone with a badge asked me to. You stood with the badge. I'll keep what the sand gave me." |
| 6 | Corvin | not `CORVIN_FREED` (a Choir porter in his mask holds the Plate) | Porter: "I — I'm not him. I don't know how. Nobody told me how." |
| 7 | Brann | `:ch8_lightstone` = dominar | "You gave my guild's Light away to a king, and now you'd have me give the fire too? No, lad. Not for you." |
| 8 | Kaito | not `KAITO_TESTIFIED` | "I never said it out loud. Marrowgate. A man who can't open his mouth can't open his hand." |
| 9 | Juno | Bond < 0 | "I let go of him. I let go of the dock we started on. I'm not letting go of the last thing that's mine because *you* asked." |
| 10 | Anja | `:ch11_anja` ≠ let_confess | "Rimeholt drowns without it. You threw me to the court for less. Ice remembers." |
| 11 | Odessa | `:ch12_letter` = burn | "Dead letters are the last thing some people ever said. You burned one. I don't hand things to people who burn them." |
| 12 | Ilsa | not reconciled and Bond < 5 | "He's dying on that Ring for a country that never thanked him. Someone in this family is going to keep something." |
| 13 | Bastian | `:ch14_telemetry` = leave | "You walked a Meridian beacon into my seams, child, and they came for my people by it. I'll keep my stone." |
| 14 | Ysolde | `KESTREL_FALLEN` and not reached | "She asked me to keep one boy safe and I couldn't. I won't lose the only place I can still hear them both." |
| 15 | Magnus | not `MAGNUS_KEPT_FAITH` | "I won't hand my city's future to a god. Gods have had three hundred years. Engineers have had ten." |
| 16 | Nyx | no bargain and Bond < 4 | "Everything has a price, sweetheart, and you never paid mine. The dark stays where it's useful." |
| 17 | Celestine | Resonance < 2 | "I cannot lie, so hear it plainly: you're singing in the wrong key, and I won't give the dusk to that song." |
| 18 | Sigrun | `:ch19_oath` = keep or ruin | "You swore over my fire you'd keep them, or end them. I believed you. So I'm keeping mine from you." |

**Forced-lock beat:** when a refused lock is broken by force, the Warden is thrown back from the pylon and the Plate tears free with a crack of Bleed light. No line. The camera holds on their empty hands.

## 3. *Homecoming, Unfinished* slides (one per refusing Warden, gym order)

| # | City | Last Shatter slide |
|---|---|---|
| 1 | Saltmere | "The one city the Bleed never touched has a glass promenade. The Lantern Theatre plays to it." |
| 2 | Briarwick | "The looms went still in one night. Tamsin weaves by hand now." |
| 3 | Ebbmouth | "The Ebb stopped, then ran out to sea and didn't come back. The mills are museums." |
| 4 | Lumen City | "The Lowlight's glass took three more streets before the dark came. Rook reads the names on air every year." |
| 5 | Duneholt | "The well never refilled. The caravans left by the east gate, in order of age." |
| 6 | Mirefen | "The mire went clear and killed everything that had learned to live in it. Corvin's Ward was empty by then." |
| 7 | Cindervault | "Mount Cinder went cold with its forges full. Brann's last blade is still in the stone." |
| 8 | Ironreach | "The shafts fell in on the Pit. Kaito dug for nine days." |
| 9 | Verdance | "Autumn came all at once, and winter the same week. Juno planted anyway." |
| 10 | Rimeholt | "The lake let go. The Holdfast is an island now, and Anja lights its beacon for nobody." |
| 11 | Skyreach | "The Stormfront fell on the masts. The Gale Post flies from Ebbmouth, when it flies." |
| 12 | Lucent | "The city in the sky came down on the city below. The Athenaeum's books were found as far as Gloaming." |
| 13 | Cragholm | "The crystal halls went dark and brittle. Pip carried her grandfather's lamp out." |
| 14 | Gravenmoor | "Every echo spoke at once, and then none ever did again. Ysolde keeps the candles lit out of habit." |
| 15 | Cogsworth | "The foundries seized mid-shift. The clock-towers stopped at eleven-forty, all of them." |
| 16 | Underveil | "The long night ended at noon, and the towers couldn't bear the light. Nadir moved up the lifts, uninvited." |
| 17 | Gloaming | "Dusk became midnight and stayed. The lantern-moths are the only stars." |
| 18 | Wyrmrest | "The dragons left the Rift in one flight and didn't choose a new one." |
