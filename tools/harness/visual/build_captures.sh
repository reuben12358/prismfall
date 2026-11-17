#!/usr/bin/env bash
# Rebuilds docs/battle_captures/engine/ (GIFs + key frames) from saved engine frames.
# Frames come from run_engine_capture.sh (default location /home/claude/run/captures_keep/<battle>/).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
K="${1:-/home/claude/run/captures_keep}"
OUT="$HERE/../../../docs/battle_captures/engine"
mkdir -p "$OUT"; cd "$OUT"
G="$HERE/make_gif.py"
python3 -I "$G" "$K/volcanic" volcanic_to_ashen --title "Volcanic Field -> Ashen Waste | Gym 7 Warden Brann via Prismfall.gym_battle(7)" --ranges 140-520 \
  --key 163:"Field intro: :VOLCANIC intro_message; EBDX room = Bridge's MAGMA fallback + volcanic tone + ember FX" \
  --key 247:"Transition progress: Surf #1 of 2 toward VOLCANIC -> ASHEN_WASTE" \
  --key 268:"Field-boosted move: Lava Plume, Fire x1.5 type-mod message" \
  --key 275:"Field-boosted move: Lava Plume x1.5 move-mod message" \
  --key 475:"Field transition: Bridge flash in the configured steam colour [200,200,200]" \
  --key 493:"After the transition: Ashen Waste room (Bridge CAVE fallback + ash tone, falling-ash FX)"
python3 -I "$G" "$K/silkwood" silkwood_to_ashen --title "Silkwood -> Ashen Waste | Gym 1 Warden Tamsin via Prismfall.gym_battle(1)" --ranges 140-480,1330-1480 \
  --key 162:"Field intro: :SILKWOOD intro_message; EBDX forest room + Bridge tone; sticky-web entry effect follows" \
  --key 277:"Seed: Telluric Seed consumed on entry (Silkwood seed rule: Defense +1 and Ingrain)" \
  --key 384:"Field-boosted move: Ember, Fire x1.3 on the Silkwood (type-mod message)" \
  --key 1385:"Field transition: 3rd damaging Fire move burns the Silkwood; Bridge flash into ash" \
  --key 1397:"After the transition: Ashen Waste room"
python3 -I "$G" "$K/zekrom" zekrom_boss --title "Boss: Zekrom (ZEKROM_ENGINE, 3 HP bars) | Factory -> Scrapyard on the 2nd break" --ranges 120-330,540-640 \
  --key 140:"Boss intro on the Factory: EBDX boss databox with Prismfall Bosses' 3 bar pips (all lit)" \
  --key 267:"Bar 1 broken: HP hit 0, on_break message, one pip goes dark" \
  --key 294:"Bar refilled to full for bar 2; Attack +1 from on_break" \
  --key 600:"Bar 2 broken -> field change FACTORY -> SCRAPYARD: Bridge flash [255,150,40]" \
  --key 613:"Scrapyard break message (field transition from the boss break table)" \
  --key 760:"Later: one pip left; Scrapyard tone (shares EBDX's INDOOR room with Factory)"
