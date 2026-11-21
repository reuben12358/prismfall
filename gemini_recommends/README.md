# gemini_recommends/

This is where Gemini (or anyone helping the creator) drops suggestions for Prismfall. Claude reviews every one: it adopts it, adapts it, or rejects it with a reason. **The creator has the final say on everything.**

## How to propose something
Make one folder per idea, named `YYYY-MM-DD_short-name/`, containing:
- `PROPOSAL.md`, which says:
  - **What:** one or two sentences.
  - **Why:** the problem it solves or what it adds.
  - **Where it plugs in:** which system, map, character, field or doc. Point at the file if you can.
  - **Sources:** links for anything referenced (art packs, music, tutorials, plugins).
- Any files that go with it: images, sprite sheets, audio and so on. For art meant for the game, use the exact formats in [`../art/HANDOFF_GEMINI.md`](../art/HANDOFF_GEMINI.md), in a `Graphics/` tree, so installing it is a straight copy.

Read first, so your ideas fit what's already decided:
- [`../design/SPINE.md`](../design/SPINE.md): the creator's decisions. The newest revision wins.
- [`../research/README.md`](../research/README.md): what has already been researched, and where it is.

## How Claude responds
Claude records each verdict in [`REVIEW.md`](REVIEW.md), one entry per proposal:
- **ADOPT:** used as is. Says where it went and the commit.
- **ADAPT:** used with changes. Says what changed and why.
- **REJECT:** not used. Says why: for example, it conflicts with a SPINE decision, breaks a game rule, duplicates something that exists, doesn't fit the format, or the quality isn't there.
- **ASK:** needs the creator's decision. Gives the question as a clear choice.
