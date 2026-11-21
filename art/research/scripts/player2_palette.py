"""player2_palette.py - the colour plan for the player pair (v2 redo). 3 colours + 1 accent per guide 2.4:
1 sailcloth cream (jacket, his hat)  2 deep-sea slate (tee, trousers/shorts, boots)  3 prism teal (sea bag, hat band, hair tie)
accent: ferry-ticket yellow (the tag on the bag rope; one more spot at most). Skin, eyes, hair and outline are not counted.
SCHEMES: 'main' (recommended) and 'ash' (the alternate: the "colourless" look the user once floated - ash hair, chalk + grey)."""

K = '18121e'                                           # outline: tinted near-black
SKIN = ('fff0e2', 'f7d0ae', 'e09c7c', 'ae6458')        # hi, base, shadow, deep (shadow hue-shifted toward red)
CREAM = ('fffbf2', 'f0e5cf', 'cdbdb9', '978a9e')       # sailcloth: lavender shadows, never grey
SLATE = ('5d7ea0', '3e5a7c', '2b405f', '1c2a44')
TEAL = ('86dccf', '3fb2a8', '288289', '1c5a68')
YEL = ('fff2a0', 'ffd23e', 'd88c22')
EYE_W = 'fbf8f4'; HL = 'ffffff'
MOUTH = ('8e3a40', '4a1424', 'fbf6f2', 'c4545e')       # line, interior, teeth, tongue
BLUSH = 'f2a08e'

SCHEMES = {
    'A': {
        'main': {'hair': ('c09890', '8e5c46', '663c34', '442630', '2c1822'),     # cocoa brown: highlight is a cool mauve
                 'iris': ('3aa0c4', '1e5486'), 'brow': '3e2329',
                 'cream': CREAM, 'slate': SLATE, 'teal': TEAL, 'yel': YEL},
        'ash': {'hair': ('ffffff', 'd8d4ea', 'a9a3c8', '777096', '4c4670'),     # ash: lavender mids, white arc (reads styled, not old)
                'iris': ('3aa0c4', '1e5486'), 'brow': '6b6490',
                'cream': ('ffffff', 'eef0f4', 'c3c3d8', '8c8aa8'),              # chalk white
                'slate': ('8a90a8', '646b86', '4a4f68', '30344a'),              # ash grey-violet
                'teal': TEAL, 'yel': ('ffb8a8', 'f0645a', 'b03a3c')},            # the old red ferry tag
    },
    'B': {
        'main': {'hair': ('dc9cb8', 'a65a80', '7e3c62', '5a2648', '3a1630'),     # plum-brown (v3 idea): rose-violet arc
                 'iris': ('3aa0c4', '1e5486'), 'brow': '5a2648',
                 'cream': CREAM, 'slate': SLATE, 'teal': TEAL, 'yel': YEL},
        'ash': {'hair': ('ffffff', 'd8d4ea', 'a9a3c8', '777096', '4c4670'),
                'iris': ('3aa0c4', '1e5486'), 'brow': '6b6490',
                'cream': ('ffffff', 'eef0f4', 'c3c3d8', '8c8aa8'),
                'slate': ('8a90a8', '646b86', '4a4f68', '30344a'),
                'teal': TEAL, 'yel': ('ffb8a8', 'f0645a', 'b03a3c')},
    },
}
