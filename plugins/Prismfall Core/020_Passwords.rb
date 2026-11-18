#===============================================================================
# Prismfall Core - 020 New-game passwords (Rejuvenation-style)
#-------------------------------------------------------------------------------
# Intro event (right after the difficulty choice):  Script: Prismfall::Passwords.prompt
# The player types passwords one at a time (blank = done). Entry closes after
# the prompt, so passwords are new-game only.
#
# TABLE: "word" => {
#   :id          Symbol stored in the save (Prismfall.state.narrative[:passwords])
#   :name, :description
#   :aliases     other accepted words
#   :conflicts   ids that can't be combined with this one
#   :overrides   difficulty tunables to override (see DIFFICULTIES in 001)
#   :param       :type = ask for a type when entered (monotype)
#   :apply       proc { |param| ... } run once when accepted
# }
# Hooks below implement :FULL_IVS, :EXP_ALL_OFF and :MONOTYPE. Overrides cover
# :LITEMODE. :NO_LEVEL_CAPS and :HARD_LOCK use :apply plus Difficulty checks.
#===============================================================================
module Prismfall
  module Passwords
    TABLE = {
      "nocap"    => { :id => :NO_LEVEL_CAPS, :name => "No Level Caps", :aliases => ["nolevelcaps"],
                      :description => "Level caps are switched off for this save.",
                      :apply => proc { Prismfall::LevelCap.disable! } },
      "fullivs"  => { :id => :FULL_IVS, :name => "Perfect IVs", :aliases => ["perfectivs"],
                      :description => "Your Pokémon use 31 for every IV." },
      "noexpall" => { :id => :EXP_ALL_OFF, :name => "No Exp. All",
                      :description => "Only Pokémon that battle (or hold an Exp. Share) gain Exp." },
      "monotype" => { :id => :MONOTYPE, :name => "Monotype", :param => :type,
                      :description => "Only Pokémon of one chosen type can battle." },
      "hardonly" => { :id => :HARD_LOCK, :name => "Hard Lock", :conflicts => [:LITEMODE],
                      :description => "Hard difficulty, and it can't be lowered.",
                      :apply => proc { Prismfall::Difficulty.set(:HARD) } },
      "litemode" => { :id => :LITEMODE, :name => "Lite Mode", :conflicts => [:HARD_LOCK],
                      :description => "Double Exp, no disobedience, gentler AI.",
                      :overrides => { :exp_multiplier => 2.0, :obedience => false, :ai_skill_max => 32 } },
      # NARRATIVE_KEYS section 14
      "ledgerhints" => { :id => :LEDGER_HINTS, :name => "Ledger Hints",
                         :description => "The Ledger shows a hint for every game over you haven't found." },
      "nomercy"     => { :id => :NO_MERCY, :name => "No Mercy",
                         :description => "No checkpoints: a story game over sends you back to your last manual save." },
      "openbook"    => { :id => :OPEN_BOOK, :name => "Open Book",
                         :description => "The Ties page shows numbers next to each tier." },
      "colorless"   => { :id => :COLORLESS, :name => "Colorless",
                         :description => "Every Resonance swing is halved. Harmony and Ruin are both harder to reach." },
      # GYM_PUZZLES section 4 item 12: apprentices offer "Skip this room" (Reborn's Puzzle Skip). Mirrors Game Switch 301.
      "puzzleskip"  => { :id => :PUZZLE_SKIP, :name => "Puzzle Skip", :aliases => ["skippuzzles"],
                         :description => "Gym apprentices can solve a puzzle room for you.",
                         :apply => proc { $game_switches[301] = true if $game_switches } },
      "secondferry" => { :id => :SECOND_FERRY, :name => "The Second Ferry",
                         :description => "New Game+: carry over what the Ledger remembers.",
                         :requires => proc { !Prismfall::Ledger.endings_seen.empty? },
                         :refusal => "The ferry only sails for those who've reached an ending." }
    }

    def self.store
      return Prismfall.state.narrative[:passwords]
    end

    def self.closed?
      return Prismfall.state.narrative[:passwords_closed] ? true : false
    end

    def self.close!
      Prismfall.state.narrative[:passwords_closed] = true
    end

    def self.find(word)
      w = word.to_s.strip.downcase.delete(" ")
      return nil if w.empty?
      TABLE.each do |key, d|
        return d if key == w || (d[:aliases] || []).include?(w)
      end
      return nil
    end

    def self.definition(id)
      return TABLE.values.find { |d| d[:id] == id }
    end

    def self.active?(id)
      return store.has_key?(id.to_sym)
    end

    def self.param(id)
      v = store[id.to_sym]
      return (v == true) ? nil : v
    end

    def self.active_ids
      return store.keys
    end

    # First active password that overrides difficulty tunable `key`, or nil.
    def self.override(key)
      store.each_key do |id|
        d = definition(id)
        next if !d || !d[:overrides] || !d[:overrides].has_key?(key)
        return d[:overrides][key]
      end
      return nil
    end

    def self.choose_type
      types = []
      GameData::Type.each { |t| types.push(t) if !t.pseudo_type }
      cmds = types.map { |t| t.name }
      idx = pbMessage(_INTL("Choose your type."), cmds, -1)
      return (idx >= 0) ? types[idx].id : nil
    end

    # Activates a password definition. Returns true on success.
    def self.enable(d, show = true)
      if active?(d[:id])
        pbMessage(_INTL("That password is already active.")) if show
        return false
      end
      clash = (d[:conflicts] || []).find { |c| active?(c) }
      if clash
        other = definition(clash)
        pbMessage(_INTL("That can't be combined with {1}.", _INTL(other[:name]))) if show
        return false
      end
      if d[:requires] && !d[:requires].call
        pbMessage(_INTL(d[:refusal] || "That password can't be used yet.")) if show
        return false
      end
      value = true
      if d[:param] == :type
        value = choose_type
        return false if !value
      end
      store[d[:id]] = value
      d[:apply].call(value) if d[:apply]
      EventHandlers.trigger(:prismfall_password_enabled, d[:id], value)
      pbMessage(_INTL("Password accepted: {1}.\n{2}", _INTL(d[:name]), _INTL(d[:description]))) if show
      return true
    end

    def self.disable(id)   # debug only; :apply effects aren't undone
      store.delete(id.to_sym)
    end

    # The new-game prompt. Returns the list of active ids.
    def self.prompt(force = false)
      if closed? && !force
        pbMessage(_INTL("Passwords can only be entered when starting a new game."))
        return active_ids
      end
      if pbConfirmMessage(_INTL("Would you like to enter a password?"))
        loop do
          word = pbMessageFreeText(_INTL("Enter a password (leave blank to finish)."), "", false, 16)
          break if word.nil? || word.strip.empty?
          d = find(word)
          if d
            enable(d)
          else
            pbMessage(_INTL("That password isn't recognised."))
          end
          break if !pbConfirmMessage(_INTL("Enter another password?"))
        end
      end
      close!
      return active_ids
    end

    def self.owned_by_player?(pkmn)
      return false if !$player || !pkmn.owner
      return pkmn.owner.id == $player.id
    end

    def self.monotype_blocks?(pkmn)
      return false if !active?(:MONOTYPE) || !$game_temp || !$game_temp.in_battle
      type = param(:MONOTYPE)
      return false if !type || pkmn.egg? || !owned_by_player?(pkmn)
      return !pkmn.hasType?(type)
    end
  end
end

#===============================================================================
# Effects
#===============================================================================
module Prismfall
  module Difficulty
    module_function

    # Modes the player may pick (Hard Lock password restricts to :HARD).
    def allowed_modes(modes = nil)
      modes ||= DIFFICULTY_ORDER
      return [:HARD] & modes if Prismfall::Passwords.active?(:HARD_LOCK)
      return modes
    end
  end
end

class Pokemon
  alias __prismfall_core_calcIV calcIV unless method_defined?(:__prismfall_core_calcIV)

  def calcIV
    ret = __prismfall_core_calcIV
    if Prismfall::Passwords.active?(:FULL_IVS) && Prismfall::Passwords.owned_by_player?(self)
      ret.each_key { |s| ret[s] = Pokemon::IV_STAT_LIMIT }
    end
    return ret
  end

  alias __prismfall_core_able? able? unless method_defined?(:__prismfall_core_able?)

  def able?
    return false if Prismfall::Passwords.monotype_blocks?(self)
    return __prismfall_core_able?
  end
end

class Player
  alias __prismfall_core_has_exp_all has_exp_all unless method_defined?(:__prismfall_core_has_exp_all)

  def has_exp_all
    return false if Prismfall::Passwords.active?(:EXP_ALL_OFF)
    return __prismfall_core_has_exp_all
  end
end

class PokemonBag
  alias __prismfall_core_has? has? unless method_defined?(:__prismfall_core_has?)

  def has?(item, qty = 1)
    return false if item == :EXPALL && Prismfall::Passwords.active?(:EXP_ALL_OFF)
    return __prismfall_core_has?(item, qty)
  end
end
