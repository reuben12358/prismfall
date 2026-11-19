#===============================================================================
# Prismfall Trials - 006 Event Pokemon (quest rewards, chases, boss rewards)
#-------------------------------------------------------------------------------
# Prismfall::EventMons.register(:ID, {
#   :species => :NICKIT, :level => 6, :ability => :STAKEOUT, :moves => [...],
#   :nature => :JOLLY, :ivs => 20 (or Hash), :item => :ORANBERRY, :nickname => "...",
#   :kind => :battle | :gift | :egg | :boss,
#   :field => :MEADOW, :can_run => false, :catchable => true, :on_ko => :retry,
#   :boss => { :bars => 2, :stat_mults => {...}, :breaks => {...} },   # :kind :boss
#   :joins => { :level => 12 },  # after a boss win the (stripped) Pokemon joins
#   :variants => { :sea => { :moves => [...] } } })
# Event usage:
#   pf_event_battle(:ID)  -> :caught / :won / :lost / :fled   (also stores status)
#   pf_event_gift(:ID[, :variant])  -> true if added
#   pf_event_mon(:ID)     -> status Symbol or nil
#===============================================================================
module Prismfall
  module EventMons
    OUTCOMES = { 1 => :won, 2 => :lost, 3 => :fled, 4 => :caught, 5 => :lost }.freeze

    def self.status(id)
      return Prismfall::Trials.store[:event_mons][id.to_sym]
    end

    def self.set_status(id, value)
      Prismfall::Trials.store[:event_mons][id.to_sym] = value
      Prismfall::Trials.refresh_map
      return value
    end

    # Value or difficulty Hash ({ :CASUAL => 9, :STANDARD => 10, :HARD => 12, :default => 10 }) or proc.
    def self.resolve(v)
      v = v.call if v.is_a?(Proc)
      if v.is_a?(Hash) && (v.key?(:default) || v.key?(:STANDARD))
        diff = (defined?(Prismfall::Difficulty) && Prismfall::Difficulty.respond_to?(:current)) ? Prismfall::Difficulty.current : nil
        return v[diff] || v[:default] || v[:STANDARD]
      end
      return v
    end

    def self.build(id, variant = nil, overrides = nil)
      d = get(id)
      raise ArgumentError, "Unknown event mon #{id.inspect}" if !d
      d = d.merge((d[:variants] || {})[variant] || {}) if variant
      d = d.merge(overrides) if overrides
      pkmn = Pokemon.new(d[:species], resolve(d[:level]) || 5)
      pkmn.form = d[:form] if d[:form]
      pkmn.makeMale if d[:gender] == 0
      pkmn.makeFemale if d[:gender] == 1
      pkmn.shiny = true if d[:shiny]
      pkmn.nature = d[:nature] if d[:nature]
      if d[:ability]
        pkmn.ability = d[:ability]
      elsif d[:ability_index]
        pkmn.ability_index = d[:ability_index]
      end
      pkmn.item = d[:item] if d[:item]
      if d[:moves]
        pkmn.forget_all_moves
        d[:moves].each { |m| pkmn.learn_move(m) }
      end
      if d[:ivs]
        GameData::Stat.each_main do |s|
          pkmn.iv[s.id] = d[:ivs].is_a?(Hash) ? (d[:ivs][s.id] || pkmn.iv[s.id]) : d[:ivs].to_i
        end
      end
      (d[:evs] || {}).each { |stat, v| pkmn.ev[stat] = v }
      pkmn.name = _INTL(d[:nickname]) if d[:nickname]
      pkmn.poke_ball = d[:ball] if d[:ball]
      pkmn.happiness = d[:happiness] if d[:happiness]
      pkmn.obtain_text = _INTL(d[:obtain_text]) if d[:obtain_text]
      pkmn.calc_stats
      pkmn.heal
      return pkmn
    end

    #---------------------------------------------------------------------------
    # Gifts (rewards, kindness gifts, eggs)
    #---------------------------------------------------------------------------
    def self.gift(id, variant = nil)
      d = get(id)
      raise ArgumentError, "Unknown event mon #{id.inspect}" if !d
      pkmn = build(id, variant)
      if d[:kind] == :egg
        egg = pbGenerateEgg(pkmn.species, _INTL(d[:obtain_text] || "A gift"))
        ok = (egg) ? true : false
      else
        ok = pbAddPokemon(pkmn)
      end
      set_status(id, :gifted) if ok
      return ok
    end

    #---------------------------------------------------------------------------
    # Battles
    #---------------------------------------------------------------------------
    def self.battle(id)
      d = get(id)
      raise ArgumentError, "Unknown event mon #{id.inspect}" if !d
      return boss_battle(id) if d[:kind] == :boss
      pbMessage(_INTL(d[:intro])) if d[:intro]
      pkmn = build(id)
      setBattleRule((d[:can_run]) ? "canRun" : "cannotRun")
      setBattleRule("disablePokeBalls") if d[:catchable] == false
      setBattleRule("canLose")
      Prismfall::Trials.set_field(d[:field])
      WildBattle.start(pkmn, can_override: false)
      res = OUTCOMES[$game_variables[1]] || :lost
      $player.heal_party if res == :lost && $player
      set_status(id, (res == :won && d[:on_ko] == :lost) ? :lost : res)
      return res
    end

    # Boss battle (Prismfall Bosses when installed); after a win, the
    # Pokemon can join (:joins) as a normal Pokemon.
    def self.boss_battle(id)
      d = get(id)
      pbMessage(_INTL(d[:intro])) if d[:intro]
      if defined?(Prismfall::Bosses) && d[:boss]
        bid = "EVENT_#{id}".to_sym
        if !Prismfall::Bosses.exists?(bid)
          Prismfall::Bosses.register(bid, d[:boss].merge(:species => d[:species], :level => d[:level],
                                                         :field => d[:field], :can_lose => true))
        end
        pkmn = Prismfall::Bosses.create_pokemon(bid)
        apply_mon_overrides(pkmn, d)
        Prismfall::Bosses.start_wild(pkmn, bid, :can_lose => true)
      else
        pkmn = build(id)
        setBattleRule("cannotRun")
        setBattleRule("canLose")
        Prismfall::Trials.set_field(d[:field])
        WildBattle.start(pkmn, can_override: false)
      end
      res = OUTCOMES[$game_variables[1]] || :lost
      $player.heal_party if res == :lost && $player
      set_status(id, res)
      if (res == :won || res == :caught) && d[:joins]
        joined = (res == :caught) ? true : pbAddPokemon(build(id, nil, d[:joins]))
        set_status(id, :joined) if joined
      end
      return res
    end

    # Moves/ability/nature of the event definition on top of a boss Pokemon.
    def self.apply_mon_overrides(pkmn, d)
      pkmn.ability = d[:ability] if d[:ability]
      pkmn.nature = d[:nature] if d[:nature]
      if d[:moves]
        pkmn.forget_all_moves
        d[:moves].each { |m| pkmn.learn_move(m) }
      end
      pkmn.calc_stats
      pkmn.heal
    end
  end
end

def pf_event_battle(id);              return Prismfall::EventMons.battle(id);        end
def pf_event_gift(id, variant = nil); return Prismfall::EventMons.gift(id, variant); end
def pf_event_mon(id);                 return Prismfall::EventMons.status(id);        end
