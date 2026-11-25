#===============================================================================
# Round 4 of the win-rate test (trainer workstream): Gyms 4-18, the rivals K3-K8 / J2 / J4, the villains and the
# Festival bosses, against TYPICAL and PREPARED player teams built from what the game hands out by that badge count.
# Loaded by run_winrates.rb (which owns the battle loop); these fights carry :r4 => true.
#
# What a player can have by badge count b:
#   * wild: tools/harness/winrate_pools.json (tools/trainer_gen/pools.py): each species' best encounter rate on any
#     table usable with b badges (map segment, method unlocks, badge-tier overlays; trees / rocks / rods x0.3, Surf x0.6)
#   * hand-outs: EVENTS below (POKEMON_AVAILABILITY.md 2, EVENT_POKEMON.md; a designed event in chapter c counts from
#     c - 2 badges), the three starter eggs, the Act IV fossils
#   * evolution: by level at or under the level; stones, trade (Linking Cord), friendship and the rest from Lumen
#     (3 badges) on
#   * TMs (WORLD.md 6): gym TMs 1..b, field TMs by segment, HMs by badge, Protect / Thunder Wave from the Lumen mart
#   * the Mega Ring after Badge 13 (MEGARING + the stones and Z-crystals of PrismfallMega::STONES / Z_CRYSTALS by then)
# TYPICAL (default): the starter at the cap plus five catches drawn by encounter rate x (final BST / 450)^4, with a
#   penalty for a type already on the team (a player keeps the strong ones and spreads types; no foe knowledge);
#   cap - 0..2; random natures, IV 5-25, EVs min(1.5 x level, 85) (what battling leaves); the three best attacks by
#   power x STAB x accuracy over level-up moves and the main-path TMs, a fourth attack or (half the time) a setup move;
#   a Sitrus on the lead, berries / type boosters / one Leftovers / one Life Orb by badges; a Mega only if a team
#   member's stone is out by then (6 in 10), no Z-moves.
# PREPARED (PRISM_PREPARED=1): the starter plus five of the six best answers to this foe's actual team (offence and
#   defence by type, weighed by the battle field's type multipliers as the field notes give them, BST), rare finds included; every catch at the cap, IV 20-31, a fitting nature,
#   252/252 EVs from 8 badges (85 each before); moves chosen against the foe's types with every TM out by then (Bleed
#   zones too), a setup or recovery move, Protect in doubles; Life Orb / Choice / Leftovers / Focus Sash / Assault Vest
#   by role; from 13 badges one Mega (the best member with a stone out by then) and one Z-crystal.
#===============================================================================
module WR4
  POOL = JSON.parse(File.read(File.join(HARNESS_DIR, "winrate_pools.json")))["species"]

  def self.wild(b)
    out = {}
    POOL.each do |k, hist|
      r = nil
      hist.each { |bb, rate| r = rate if bb <= b }
      out[k.to_sym] = r if r && r > 0
    end
    out
  end

  # species => [min badges, weight] (gifts and quest Pokemon count about like a common catch: a player takes them)
  EVENTS = {
    :EEVEE => [1, 40], :ABRA => [1, 15], :TIMBURR => [1, 20], :CRABRAWLER => [1, 15], :RALTS => [1, 15],
    :PONYTA_1 => [1, 8], :HERACROSS => [2, 10], :PINSIR => [2, 8], :SPIDOPS => [2, 8], :LITLEO => [2, 12],
    :CHARCADET => [2, 12], :SUDOWOODO => [2, 8], :SNOM => [2, 10], :BOMBIRDIER => [3, 8], :WATTREL => [3, 10],
    :PORYGON => [3, 10], :AERODACTYL => [4, 12], :PICHU => [4, 8], :TRAPINCH => [4, 12], :CARBINK => [4, 5],
    :KABUTO => [5, 6], :OMANYTE => [5, 6], :GRIMER_1 => [5, 8], :STUNFISK_1 => [5, 5],
    :DEINO => [6, 15], :DRUDDIGON => [6, 8], :NOIBAT => [6, 10], :HOUNDOUR => [6, 12], :FALINKS => [7, 6],
    :AXEW => [7, 15], :RIOLU => [8, 15], :COMFEY => [8, 6], :FLOETTE => [8, 6], :SCATTERBUG => [8, 5],
    :LAPRAS => [9, 20], :SAWSBUCK => [9, 5], :CETODDLE => [9, 8], :TATSUGIRI => [9, 5], :KLEFKI => [10, 8],
    :TYPENULL => [10, 8], :INDEEDEE => [11, 5], :HATENNA => [11, 8], :KUBFU => [12, 15], :YAMASK_1 => [12, 6],
    :AMAURA => [13, 5], :TYRUNT => [13, 6], :CRANIDOS => [13, 5], :SHIELDON => [13, 4], :LILEEP => [13, 4],
    :ANORITH => [13, 4], :ARCHEN => [13, 5], :TIRTOUGA => [13, 5], :DRACOVISH => [13, 6], :ARCTOZOLT => [13, 4],
    :POLTCHAGEIST => [16, 5]
  }
  # The starter eggs (POKEMON_AVAILABILITY 2): any Grass starter after B6, Fire after B9, Water after B12
  # (not the line the player picked). Starters are strong, so a player raises one.
  EGGS = { 6 => [:CHESPIN, :TURTWIG, :TREECKO, :SNIVY, :ROWLET, :GROOKEY, :SPRIGATITO, :CHIKORITA],
           9 => [:TORCHIC, :CHIMCHAR, :TEPIG, :FENNEKIN, :LITTEN, :SCORBUNNY, :FUECOCO, :CYNDAQUIL],
           12 => [:MUDKIP, :PIPLUP, :OSHAWOTT, :FROAKIE, :POPPLIO, :SOBBLE, :QUAXLY, :TOTODILE] }
  EGG_WEIGHT = 25
  EGG_LINE = { 6 => "Grass", 9 => "Fire", 12 => "Water" }

  GYM_TMS = [nil, :FACADE, :UTURN, :WATERPULSE, :VOLTSWITCH, :BULLDOZE, :POISONJAB, :FLAMETHROWER, :BRICKBREAK,
             :ENERGYBALL, :ICEBEAM, :ROOST, :PSYCHIC, :STEALTHROCK, :SHADOWBALL, :FLASHCANNON, :DARKPULSE,
             :DAZZLINGGLEAM, :DRAGONPULSE]
  # field TMs by segment (WORLD.md 6); the Bleed-zone ones (optional) only for a prepared player
  FIELD_TMS = { :GIGADRAIN => 1, :XSCISSOR => 2, :BRINE => 2, :SCALD => 3, :THUNDERBOLT => 3, :PROTECT => 3,
                :THUNDERWAVE => 3, :EARTHQUAKE => 7, :DRAINPUNCH => 8, :CALMMIND => 12, :DRAGONCLAW => 17,
                :HYPERBEAM => 18, :ROCKSMASH => 1, :STRENGTH => 5, :SURF => 6, :FLY => 8, :WATERFALL => 11 }
  BLEED_TMS = { :WORKUP => 2, :WILLOWISP => 14, :TRICKROOM => 16 }
  HM_ONLY = [:ROCKSMASH, :STRENGTH, :FLY, :CUT]   # field moves ride on an HM slave, not on the team

  def self.tms(b, prepared)
    l = GYM_TMS[1..[b, 18].min].compact
    FIELD_TMS.each { |m, s| l << m if s <= b }
    BLEED_TMS.each { |m, s| l << m if s <= b } if prepared
    l.uniq
  end

  FIXED_POWER = { :LOWKICK => 70, :GRASSKNOT => 70, :HEAVYSLAM => 80, :HEATCRASH => 80, :GYROBALL => 70,
                  :ELECTROBALL => 70, :SEISMICTOSS => 65, :NIGHTSHADE => 65 }
  NEVER = [:FOCUSPUNCH, :EXPLOSION, :SELFDESTRUCT, :MISTYEXPLOSION, :DREAMEATER, :FAKEOUT, :LASTRESORT, :BELCH,
           :SYNCHRONOISE, :SNORE, :COUNTER, :MIRRORCOAT, :METALBURST, :ENDEAVOR, :FINALGAMBIT, :SUPERFANG, :NATUREPOWER,
           :FLING, :NATURALGIFT, :SPITUP, :MEMENTO, :HEALINGWISH, :UPROAR, :THRASH, :PETALDANCE, :OUTRAGE, :STEELBEAM,
           :MINDBLOWN, :SKYDROP, :BIDE, :FUTURESIGHT, :DOOMDESIRE, :ROLLOUT, :ICEBALL, :STOMPINGTANTRUM, :RAGE,
           :TRUMPCARD, :SPLASH, :PRESENT, :MAGNITUDE, :BEATUP, :RETURN, :FRUSTRATION, :HIDDENPOWER, :BURNUP,
           :DOUBLEIRONBASH, :PAYDAY, :STRUGGLE, :THIEF, :COVET, :ROUND, :ECHOEDVOICE, :FURYCUTTER, :STEELROLLER,
           :ICESPINNER, :EXPANDINGFORCE, :RISINGVOLTAGE, :GRAVAPPLE, :TERRAINPULSE, :WEATHERBALL, :LASHOUT,
           :BARBBARRAGE, :INFERNALPARADE, :CEASELESSEDGE, :STONEAXE,   # Gen 9 Pack 3.2.5 AI bug (`b` undefined)
           :POLTERGEIST, :SUCKERPUNCH, :FIRSTIMPRESSION, :BOLTBEAK, :FISHIOUSREND, :SOLARBLADE, :SOLARBEAM,
           :METEORBEAM, :SKYATTACK, :RAZORWIND, :SKULLBASH, :FREEZESHOCK, :ICEBURN, :GEOMANCY, :DIG, :DIVE,
           :BOUNCE, :PHANTOMFORCE, :SHADOWFORCE, :FLY]
  HALF = [:HYPERBEAM, :GIGAIMPACT, :BLASTBURN, :HYDROCANNON, :FRENZYPLANT, :ROCKWRECKER, :ROAROFTIME, :PRISMATICLASER,
          :ETERNABEAM, :METEORASSAULT, :OVERHEAT, :DRACOMETEOR, :LEAFSTORM, :PSYCHOBOOST, :FLEURCANNON, :MAKEITRAIN,
          :SUPERPOWER, :HAMMERARM, :ICEHAMMER, :VCREATE, :HEADSMASH, :BRAVEBIRD, :FLAREBLITZ, :WOODHAMMER,
          :VOLTTACKLE, :WAVECRASH, :DOUBLEEDGE, :HEADCHARGE, :TAKEDOWN, :SUBMISSION, :CLOSECOMBAT]
  SETUP = { :SWORDSDANCE => 0, :DRAGONDANCE => 0, :BULKUP => 0, :SHIFTGEAR => 0, :COIL => 0, :HONECLAWS => 0,
            :VICTORYDANCE => 0, :NASTYPLOT => 1, :CALMMIND => 1, :QUIVERDANCE => 1, :TAILGLOW => 1, :SHELLSMASH => 2,
            :WORKUP => 2, :GROWTH => 2, :AGILITY => 2 }
  RECOVERY = [:ROOST, :RECOVER, :SLACKOFF, :SOFTBOILED, :MOONLIGHT, :MORNINGSUN, :SYNTHESIS, :MILKDRINK, :SHOREUP,
              :STRENGTHSAP, :WISH]
  BOOST = { :NORMAL => :SILKSCARF, :FIRE => :CHARCOAL, :WATER => :MYSTICWATER, :GRASS => :MIRACLESEED,
            :ELECTRIC => :MAGNET, :ICE => :NEVERMELTICE, :FIGHTING => :BLACKBELT, :POISON => :POISONBARB,
            :GROUND => :SOFTSAND, :FLYING => :SHARPBEAK, :PSYCHIC => :TWISTEDSPOON, :BUG => :SILVERPOWDER,
            :ROCK => :HARDSTONE, :GHOST => :SPELLTAG, :DRAGON => :DRAGONFANG, :DARK => :BLACKGLASSES,
            :STEEL => :METALCOAT, :FAIRY => :FAIRYFEATHER }

  # Sensitivity knobs for the typical model (defaults = the round 4 model): PRISM_TYP_BST=6 PRISM_TYP_MIN=420 is a
  # player who boxes everything weak and keeps only the strongest catches.
  TYP_BST_EXP = (ENV["PRISM_TYP_BST"] || "4").to_f
  TYP_MIN_BST = (ENV["PRISM_TYP_MIN"] || "0").to_i

  def self.sp_data(sym)
    GameData::Species.try_get(sym)
  end

  def self.bst(sd)
    sd.base_stats.values.sum
  end

  # Evolve as a player would by then: level evolutions up to the level, and (from 3 badges, when Lumen sells stones
  # and the Linking Cord) every other kind; a branch is picked by rng.
  def self.evolve(sym, level, b, rng)
    sd = sp_data(sym) or return nil
    form = sd.form
    sp = sd.species
    8.times do
      cur = GameData::Species.get_species_form(sp, form)
      opts = cur.get_evolutions.select do |tgt, meth, par|
        ev = GameData::Evolution.try_get(meth)
        next false if !ev
        if ev.parameter == Integer
          par.to_i <= level
        else
          b >= 3 && !meth.to_s.start_with?("Location")
        end
      end
      break if opts.empty?
      sp = opts.sample(random: rng)[0]
    end
    form = 0 if !GameData::Species.exists?(GameData::Species.get_species_form(sp, form).id) ||
                GameData::Species.get_species_form(sp, form).form != form
    GameData::Species.get_species_form(sp, form)
  end

  # Can its line be reached by the level? (a Lv 1 egg or a Deino joins far under the cap: the player raises it)
  def self.catch_list(b, prepared)
    l = wild(b)
    EVENTS.each { |sp, (mb, w)| l[sp] = [l[sp] || 0, w].max if b >= mb }
    EGGS.each { |eb, list| list.each { |sp| l[sp] = [l[sp] || 0, EGG_WEIGHT / 2.0].max } if b >= eb }
    l.reject! { |sp, _| !sp_data(sp) }
    l
  end

  #----------------------------------------------------------------------------- moves
  def self.atk_stats(sd)
    [sd.base_stats[:ATTACK], sd.base_stats[:SPECIAL_ATTACK]]
  end

  def self.move_power(m)
    d = GameData::Move.get(m)
    return 0 if d.category == 2 || NEVER.include?(m)
    pw = FIXED_POWER[m] || d.power.to_i
    return 0 if pw <= 1
    pw = pw * 0.75 if HALF.include?(m)
    pw
  end

  def self.eff(type, foe_types)
    Effectiveness.calculate(type, *foe_types)
  end

  # A prepared player reads the field notes: the battle field's type multipliers (FieldEffects :type_mods).
  def self.field_mods(field)
    return {} if !field || !defined?(FieldEffects) || !FieldEffects.exists?(field)
    FieldEffects.get(field)[:type_mods] || {}
  rescue StandardError
    {}
  end

  # foe: nil (typical) or a list of [types] of the foe's Pokemon; the score favours super-effective coverage
  def self.attack_score(sd, m, foe, fmods = {})
    d = GameData::Move.get(m)
    pw = move_power(m)
    return 0 if pw <= 0
    acc = (d.accuracy.to_i == 0) ? 100 : d.accuracy
    a, s = atk_stats(sd)
    st = (d.category == 0) ? a : s
    ratio = st.to_f / [a, s].max
    sc = pw * acc / 100.0 * (sd.types.include?(d.type) ? 1.5 : 1.0) * ratio**2 * (fmods[d.type] || 1.0)
    if foe && !foe.empty?
      mult = foe.sum { |ft| [eff(d.type, ft), 2.0].min } / foe.size
      sc *= mult**1.3
    end
    sc
  end

  def self.pick_moves(pk, b, prepared, foe, double, rng, fmods = {})
    sd = pk.species_data
    learned = sd.moves.select { |lv, _m| lv <= pk.level }.map { |_lv, m| m }
    pool = (learned + tms(b, prepared).select { |m| pk.compatible_with_move?(m) }).uniq - HM_ONLY
    attacks = pool.select { |m| move_power(m) > 0 }
    chosen = []
    3.times do
      best = attacks.reject { |m| chosen.include?(m) }.max_by do |m|
        t = GameData::Move.get(m).type
        attack_score(sd, m, prepared ? foe : nil, prepared ? fmods : {}) * (chosen.any? { |c| GameData::Move.get(c).type == t } ? 0.35 : 1.0)
      end
      chosen << best if best
    end
    a, s = atk_stats(sd)
    phys = a >= s
    setup = pool.select { |m| SETUP.key?(m) && (SETUP[m] == 2 || SETUP[m] == (phys ? 0 : 1)) }
    rec = pool.select { |m| RECOVERY.include?(m) }
    fourth = nil
    if double && pool.include?(:PROTECT) && (prepared || rng.rand < 0.4)
      fourth = :PROTECT
    elsif prepared
      fourth = setup.first || rec.first
    elsif rng.rand < 0.5
      fourth = setup.first || rec.first
    end
    if !fourth
      fourth = attacks.reject { |m| chosen.include?(m) }.max_by do |m|
        t = GameData::Move.get(m).type
        attack_score(sd, m, prepared ? foe : nil, prepared ? fmods : {}) * (chosen.any? { |c| GameData::Move.get(c).type == t } ? 0.35 : 1.0)
      end
    end
    chosen << fourth if fourth
    chosen = (chosen + learned.reverse).uniq.first(4) if chosen.size < 4
    chosen.compact
  end

  #----------------------------------------------------------------------------- one Pokemon
  def self.make(sd, level, b, prepared, foe, double, rng, fmods = {})
    pk = Pokemon.new(sd.species, level)
    pk.form = sd.form if sd.form > 0
    GameData::Stat.each_main do |st|
      pk.iv[st.id] = prepared ? 20 + rng.rand(12) : 5 + rng.rand(21)
      pk.ev[st.id] = prepared ? 85 : [level * 3 / 2, 85].min
    end
    a, s = atk_stats(sd)
    fast = sd.base_stats[:SPEED] >= 85
    if prepared
      pk.nature = (a >= s) ? (fast ? :JOLLY : :ADAMANT) : (fast ? :TIMID : :MODEST)
      if b >= 8
        GameData::Stat.each_main { |st| pk.ev[st.id] = 0 }
        pk.ev[(a >= s) ? :ATTACK : :SPECIAL_ATTACK] = 252
        pk.ev[fast ? :SPEED : :HP] = 252
        pk.ev[fast ? :HP : :DEFENSE] = 4
      end
    else
      pk.nature = GameData::Nature.keys.sample(random: rng)
    end
    abil = sd.abilities
    pk.ability_index = rng.rand([abil.size, 1].max) if abil.size > 1
    pk.forget_all_moves
    pick_moves(pk, b, prepared, foe, double, rng, fmods).each { |m| pk.learn_move(m) }
    pk.calc_stats
    pk
  end

  #----------------------------------------------------------------------------- the foe
  def self.foe_types(f)
    return f[:foe_types].call if f[:foe_types]   # a wild boss cell (no trainer to load)
    tt, nm, ver = f[:foe].call
    tr = pbLoadTrainer(tt, nm, ver) rescue nil
    return [] if !tr
    tr.party.compact.map { |pk| pk.types }
  end

  # How good an answer is this species to the foe's team? Offence by STAB, defence against the foe's own types,
  # base stats; Mega-capable species from the ring on get their stone's lift.
  def self.answer_score(sd, foe, fmods = {})
    return 0 if foe.empty?
    off = foe.sum { |ft| sd.types.map { |t| [eff(t, ft), 2.0].min * (fmods[t] || 1.0) }.max } / foe.size
    dfn = foe.sum { |ft| ft.map { |t| eff(t, sd.types) * (fmods[t] || 1.0) }.max } / foe.size
    (bst(sd) / 500.0)**2.5 * off**1.4 / [dfn, 0.25].max**0.9
  end

  def self.mega_for(species, b)
    return nil if b < 13
    PrismfallMega::STONES.each do |stone, h|
      next if h[:badges] > b
      found = false
      GameData::Species.each { |s| found = true if s.species == species && s.mega_stone == stone }
      return stone if found
    end
    nil
  end

  def self.zcrystal_for(type, b)
    return nil if b < 13
    PrismfallMega::Z_CRYSTALS.each do |cr, h|
      next if h[:badges] > b
      it = GameData::Item.try_get(cr)
      next if !it
      zt = PrismfallZ::CRYSTALS[cr] rescue nil
      zt = zt[:type] if zt.is_a?(Hash)
      return cr if zt == type
    end
    nil
  end

  #----------------------------------------------------------------------------- the team
  @cache = {}
  def self.party(fight, f, starter_lines, seed, prepared, mode)
    rng = Random.new(seed)
    b, cap, double = f[:badges], f[:cap], f[:double]
    sname = WR::STARTERS.key(starter_lines)
    key = [fight, mode, sname, prepared]
    foe = (@cache[[:foe] + key] ||= foe_types(f))
    st_sd = evolve(starter_lines[0], cap, b, rng)
    team = [[st_sd, cap]]
    taken = [st_sd.species]
    egg_skip = EGG_LINE.select { |_eb, nm| nm == sname }.keys   # no second copy of the player's own starter type
    cands = (@cache[[:cands, b]] ||= catch_list(b, prepared).to_a)
    if prepared
      scored = (@cache[[:scored] + key] ||= begin
        seen = {}
        cands.each do |sp, _w|
          sd = evolve(sp, cap, b, Random.new(sp.to_s.sum))
          next if !sd || seen[sd.species]
          next if egg_skip.any? { |eb| EGGS[eb].include?(sp) }
          sc = answer_score(sd, foe, field_mods(f[:field]))
          sc *= 1.25 if mega_for(sd.species, b)
          seen[sd.species] = [sd, sc]
        end
        seen.values.sort_by { |_sd, sc| -sc }
      end)
      picks = []
      scored.each do |sd, sc|
        break if picks.size >= 8
        next if taken.include?(sd.species) || picks.any? { |p| p[0].species == sd.species }
        # spread types a little: a third Pokemon of one type has to be much better than the alternatives
        same = (picks.map { |p| p[0] } + [st_sd]).count { |o| (o.types & sd.types).any? }
        next if same >= 2
        picks << [sd, sc]
      end
      chosen = picks.first(6).shuffle(random: rng).first(f[:size] - 1)
      chosen.each { |sd, _| team << [sd, cap] }
    else
      bag_w = cands.map do |sp, w|
        sd = evolve(sp, cap, b, rng)
        next nil if !sd || egg_skip.any? { |eb| EGGS[eb].include?(sp) }
        next nil if bst(sd) < TYP_MIN_BST
        [sd, w * (bst(sd) / 450.0)**TYP_BST_EXP]
      end.compact
      offsets = [0, 0, 1, 1, 2]
      (f[:size] - 1).times do |i|
        ws = bag_w.map do |sd, w|
          next 0 if taken.include?(sd.species)
          shared = team.count { |o, _| (o.types & sd.types).any? }
          w * (0.35**shared)
        end
        tot = ws.sum
        break if tot <= 0
        r = rng.rand * tot
        j = ws.index { |w| (r -= w) < 0 } || (ws.size - 1)
        sd = bag_w[j][0]
        taken << sd.species
        team << [sd, cap - offsets[i % offsets.size]]
      end
    end
    party = team.map { |sd, lv| make(sd, lv, b, prepared, prepared ? foe : nil, double, rng, field_mods(f[:field])) }
    give_items(party, b, prepared, rng)
    party = party.rotate(rng.rand(party.size))
    party
  end

  def self.give_items(party, b, prepared, rng)
    used = []
    phys = lambda { |pk| pk.attack >= pk.spatk }
    power = lambda { |pk| [pk.attack, pk.spatk].max * (pk.speed + 100) }
    bulk = lambda { |pk| pk.totalhp * (pk.defense + pk.spdef) }
    booster = lambda do |pk|
      t = pk.moves.map { |m| GameData::Move.get(m.id) }.select { |d| d.category != 2 && pk.types.include?(d.type) }.first
      it = t && BOOST[t.type]
      (it && GameData::Item.exists?(it)) ? it : :SITRUSBERRY
    end
    if prepared
      order = party.sort_by { |pk| -power.call(pk) }
      party.each { |pk| pk.item = nil }
      if b >= 13   # the ring: one Mega, one Z-crystal
        mpk = order.find { |pk| mega_for(pk.species, b) }
        mpk.item = mega_for(mpk.species, b) if mpk
        order.each do |pk|
          next if pk.item
          d = pk.moves.map { |m| GameData::Move.get(m.id) }.select { |x| x.category != 2 }.max_by { |x| move_power(x.id) }
          cr = d && zcrystal_for(d.type, b)
          if cr
            pk.item = cr
            break
          end
        end
      end
      free = order.reject { |pk| pk.item }
      lo = free.shift if b >= 7
      lo.item = :LIFEORB if lo
      if b >= 10 && (ch = free.shift)
        ch.item = phys.call(ch) ? :CHOICEBAND : :CHOICESPECS
        # a Choice item with a status move is wasted: that slot gets the best attack it doesn't have
        st = ch.moves.find { |m| GameData::Move.get(m.id).category == 2 }
        if st
          sd = ch.species_data
          pool = (sd.moves.select { |lv, _m| lv <= ch.level }.map { |_lv, m| m } +
                  tms(b, true).select { |m| ch.compatible_with_move?(m) }).uniq - HM_ONLY
          alt = pool.reject { |m| ch.hasMove?(m) }.select { |m| move_power(m) > 0 }.max_by { |m| attack_score(sd, m, nil) }
          ch.moves[ch.moves.index(st)] = Pokemon::Move.new(alt) if alt
        end
      end
      if b >= 5 && (lf = free.max_by { |pk| bulk.call(pk) })
        lf.item = :LEFTOVERS
        free.delete(lf)
      end
      if b >= 12 && (av = free.max_by { |pk| bulk.call(pk) })
        av.item = :ASSAULTVEST if av.moves.all? { |m| GameData::Move.get(m.id).category != 2 }
        free.delete(av) if av.item
      end
      if b >= 8 && (fs = free.min_by { |pk| bulk.call(pk) })
        fs.item = :FOCUSSASH
        free.delete(fs)
      end
      free.each_with_index { |pk, i| pk.item = i.even? ? booster.call(pk) : :SITRUSBERRY }
    else
      party.each_with_index do |pk, i|
        r = rng.rand
        pk.item = if i == 0 then :SITRUSBERRY
                  elsif b >= 5 && !used.include?(:LEFTOVERS) && r < 0.2 then :LEFTOVERS
                  elsif b >= 8 && !used.include?(:LIFEORB) && r < 0.35 then :LIFEORB
                  elsif r < 0.65 then booster.call(pk)
                  elsif r < 0.9 then :SITRUSBERRY
                  end
        used << pk.item
      end
      if b >= 13   # a typical player uses a Mega if one of the team's stones is out by then (6 in 10)
        cand = party.select { |pk| mega_for(pk.species, b) }
        if !cand.empty? && rng.rand < 0.6
          pk = cand.sample(random: rng)
          pk.item = mega_for(pk.species, b)
        end
      end
    end
  end

  BAG = { :mid => [:SUPERPOTION, :SUPERPOTION, :HYPERPOTION, :HYPERPOTION], :late => [:HYPERPOTION] * 3,
          :ring => [:FULLRESTORE, :FULLRESTORE, :HYPERPOTION, :HYPERPOTION] }
  def self.bag_for(b)
    (b >= 13) ? :ring : (b >= 6) ? :late : :mid
  end

  #----------------------------------------------------------------------------- the fights
  def self.gym(n, b, size = 6)
    g = Prismfall.gym(n)
    foe = if g[:rival_battle]
            proc { [g[:trainer_type], g[:trainer_name], Prismfall::Rival.version_for(g[:rival_battle])] }
          else
            proc { [g[:trainer_type], g[:trainer_name], g[:version] || 0] }
          end
    { :label => "Gym #{n} #{g[:trainer_name]} (#{g[:field]}#{g[:double] ? ', double' : ''})", :cap => g[:cap], :field => g[:field],
      :badges => b, :size => size, :double => g[:double], :foe => foe, :r4 => true,
      :start => proc { Prismfall.gym_battle(n, :can_lose => true) } }
  end

  def self.rival(tt, nm, num, b, cap, field, label)
    { :label => label, :cap => cap, :badges => b, :size => 6, :field => field, :foe => proc { [tt, nm, Prismfall::Rival.version_for(num)] },
      :r4 => true, :start => proc { Prismfall.rival_battle(tt, nm, num, :can_lose => true, :field => field) } }
  end

  def self.story(tt, nm, v, b, cap, field, label)
    { :label => label, :cap => cap, :badges => b, :size => 6, :field => field, :foe => proc { [tt, nm, v] }, :r4 => true,
      :start => proc { setBattleRule("canLose"); setBattleRule("field", field) if field; TrainerBattle.start(tt, nm, v) } }
  end

  # Ch10 Loyal Three (Bosses 112): one boss a cell; partner = the Ogre beside you (:ch10_ogre == :ogre).
  def self.loyal(boss, partner, label)
    { :label => label, :cap => 51, :badges => 8, :size => 6, :field => :BLEED, :foe => proc { [:NONE, "", 0] }, :r4 => true,
      :foe_types => proc { [GameData::Species.get(Prismfall::Bosses.get(boss)[:species]).types] },
      :start => proc {
        setBattleRule("canLose")
        Prismfall::Bosses.loyal_three_partner_rules if partner
        Prismfall::Bosses.wild_battle(boss)
        pbDeregisterPartner if partner
      } }
  end

  # A wild multi-bar boss at its chapter's cap (TODO_QUOTA §3: the Ch14-16 captures saw these sweep AI parties).
  def self.wild_boss(boss, cap, badges, label)
    { :label => label, :cap => cap, :badges => badges, :size => 6, :foe => proc { [:NONE, "", 0] }, :r4 => true,
      :foe_types => proc { [GameData::Species.get(Prismfall::Bosses.get(boss)[:species]).types] },
      :start => proc { setBattleRule("canLose"); Prismfall::Bosses.wild_battle(boss) } }
  end

  def self.fights
    h = {}
    h["BKYO"] = wild_boss(:KYOGRE_ISENMAR, 55, 10, "Ch12 Kyogre, Isenmar (Frozen Lake -> Water Surface; cap 55)")
    h["BGRO"] = wild_boss(:GROUDON_UNDERSANDS, 67, 13, "Ch14 Groudon, the Undersands (Desert; cap 67)")
    h["BGIR"] = wild_boss(:GIRATINA_DEPTHS, 71, 14, "Ch15 Giratina, Reverse Depths (Inverse; cap 71)")
    h["BZEK"] = wild_boss(:ZEKROM_ENGINE, 75, 15, "Ch16 Zekrom, the Cogsworth Engine (Factory -> Scrapyard; cap 75)")
    h["L3O"] = loyal(:LOYAL_THREE_OKIDOGI, true, "Ch10 Loyal Three 1/3 Okidogi, with the Ogre (Bleed)")
    h["L3M"] = loyal(:LOYAL_THREE_MUNKIDORI, true, "Ch10 Loyal Three 2/3 Munkidori, with the Ogre (Bleed)")
    h["L3F"] = loyal(:LOYAL_THREE_FEZANDIPITI, true, "Ch10 Loyal Three 3/3 Fezandipiti, with the Ogre (Bleed)")
    h["L3OA"] = loyal(:LOYAL_THREE_OKIDOGI, false, "Ch10 Loyal Three 1/3 Okidogi, alone (:hesitate)")
    h["L3FA"] = loyal(:LOYAL_THREE_FEZANDIPITI, false, "Ch10 Loyal Three 3/3 Fezandipiti, alone (:hesitate)")
    (4..18).each { |n| h["G#{n}"] = gym(n, n - 1) }
    h["K3"] = rival(:RIVAL_KESTREL, "Kestrel", 3, 5, 35, :DESERT, "K3 Kestrel (Ossuary exit, Desert)")
    h["J2"] = rival(:RIVAL_JUNO, "Juno", 2, 5, 35, :CORROSIVE_MIRE, "J2 Juno (Mirefen stilt-walk, Corrosive Mire)")
    h["K4"] = rival(:RIVAL_KESTREL, "Kestrel", 4, 7, 43, :COLOSSEUM, "K4 Kestrel (Ironreach Open final, Colosseum)")
    h["K5"] = rival(:RIVAL_KESTREL, "Kestrel", 5, 10, 55, :STORMFRONT, "K5 Kestrel (Skyreach, Stormfront)")
    h["K6"] = rival(:RIVAL_KESTREL, "Kestrel", 6, 13, 67, :HOLLOW_CATHEDRAL, "K6 Kestrel (Gravenmoor, Hollow Cathedral)")
    h["K7"] = rival(:RIVAL_KESTREL, "Kestrel", 7, 16, 80, :FAIRY_TALE, "K7 Kestrel (Gloaming, Fairy Tale)")
    h["K8"] = rival(:RIVAL_KESTREL, "Kestrel", 8, 18, 94, :PRISM_ARENA, "K8 Kestrel (Festival SF, Prism Arena)")
    h["K9"] = rival(:RIVAL_KESTREL, "Kestrel", 9, 18, 94, :PRISM_ARENA, "K9 Kestrel, fallen (Festival SF, Prism Arena)")
    h["J4"] = rival(:RIVAL_JUNO, "Juno", 4, 18, 90, :PRISM_ARENA, "J4 Juno (Festival R16, Prism Arena)")
    h["WICK"] = story(:HOLLOW_WICK, "Wick", 0, 5, 35, :HOLLOW_CATHEDRAL, "Ch7 Brother Wick (Hollow Cathedral)")
    h["Q8"] = story(:MERIDIAN_QUENT, "Percival", 0, 6, 39, :VOLCANIC, "Ch8 Dr. Quent (Volcanic)")
    h["MOURN"] = story(:HOLLOW_MOURNER, "Mourner", 0, 7, 43, :COLOSSEUM, "Ch9 the Mourner (Colosseum; Trevenant boss)")
    h["M12"] = story(:MERIDIAN_MARCHETTI, "Helene", 0, 10, 55, :STORMFRONT, "Ch12 Marchetti (Stormfront; Mega Manectric)")
    h["KR13"] = story(:MERIDIAN_KROLL, "Sabine", 0, 11, 59, :MINDSCAPE, "Ch13 Kroll (Mindscape; Mega Sharpedo)")
    h["M14"] = story(:MERIDIAN_MARCHETTI, "Helene", 1, 13, 63, :DARK_CRYSTAL, "Ch14 Marchetti (Dark Crystal; Mega Houndoom)")
    h["KR17"] = story(:MERIDIAN_KROLL, "Sabine", 1, 15, 75, :CAVE, "Ch17 Kroll (Sun Court, Cave; Mega Sharpedo)")
    h["Q17"] = story(:MERIDIAN_QUENT, "Percival", 2, 15, 75, :CAVE, "Ch17 Quent (Sun Court, Cave; Mega Metagross)")
    h["VALEN"] = story(:CHAMPION_VALEN, "Valen", 0, 18, 96, :PRISM_ARENA, "Final: Valen (Prism Arena; Mega Gallade)")
    h["VOSS"] = story(:MERIDIAN_VOSS, "Aurelian", 0, 18, 100, :PRISM_ARENA, "Hijack: Voss (Prism Arena; Mega Ampharos)")
    h["KING"] = story(:GILDED_AURELIUS, "Aurelius", 0, 18, 100, :PRISM_ARENA, "Hijack (Ruin): Gilded King Aurelius (Prism Arena)")
    h["QH"] = story(:MERIDIAN_QUENT, "Percival", 99, 18, 100, :PRISM_ARENA, "Hijack: Quent (Prism Arena; Mega Metagross)")
    h
  end
end
