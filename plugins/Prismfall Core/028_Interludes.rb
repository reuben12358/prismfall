#===============================================================================
# Prismfall Core - 028 Interludes: play as someone else for a scene
#-------------------------------------------------------------------------------
# The ONE party / charset swap every Interlude uses (design/FLAGS.md V119
# INTERLUDE_ACTIVE). Scripts: story/24_SCRIPT_CH5.md "Interlude I" (Kestrel),
# 27_SCRIPT_CH9.md "Interlude II" (Rowan), 31_SCRIPT_CH12.md "Interlude III"
# (Kestrel), 35_SCRIPT_CH16.md "INTERLUDE IV - Clear Air" (Wenlow) and
# 39_SCRIPT_CH20.md "INTERLUDE V, The Last Night" (Valen).
#
# Event usage (Script commands):
#   pf_interlude_start(4)     store the PC's party, load the Interlude's loadout,
#                             swap the walking charset (and the name shown by \PN),
#                             set V119 = 4. Call it on a black screen.
#   pf_interlude_end          restore the party, the look and the name; V119 = 0.
#                             Anything from the loadout is taken back, wherever it
#                             went (party or PC boxes), so nothing leaks into the
#                             save, legendaries least of all.
#   pf_interlude?             is one running?     pf_interlude?(4)  is it this one?
#   pf_interlude_heal         heal the loadout (a lost Interlude battle only resets
#                             the task: "can't be failed, only replayed")
#   pf_interlude_title(4)     the title card text ("INTERLUDE IV - Clear Air")
#
# While an Interlude runs: wild encounters are off unless the loadout says
# :encounters => true; Poke Balls do nothing (:can_catch => true to allow);
# the loadout's :menu => false shuts the pause menu and :walk_only => true
# stops running (Valen: "slow, one arm").
#
# Loadouts (LOADOUTS below) are either inline Pokemon rows
#   [:SPECIES, level, { :ability, :item, :nature, :moves, :nickname, :form, :gender, :ivs, :evs }]
# or a PBS trainer's own party
#   :trainer => [:TYPE, "Name", version or proc], :drop => [species], :only => [species],
#   :level_shift => n, :no_legendaries => true
# A missing trainer or species never crashes a scene: the row is skipped (and
# logged), and if nothing at all could be built the PC keeps a healed copy of
# their own lead so the scene can still run.
#
# The stash is Prismfall.state.custom[:interlude], so saving mid-Interlude is
# safe; on load a stash with V119 == 0 (a debug warp out of a scene) is put back.
#===============================================================================
module Prismfall
  module Interlude
    VARIABLE = 119   # V119 INTERLUDE_ACTIVE (design/FLAGS.md)

    # :charset is a list of candidates in Graphics/Characters; the first one that exists is used
    # (the cast's own sheet, then the trainer placeholder), else the PC's own sheet stays.
    LOADOUTS = {
      # I "Lamplight" (Ch5, Ferrow Lighthouse 105/106): Honedge "Morwen", Staravia, the counter-starter, K2's levels + 2.
      1 => { :id => :LAMPLIGHT, :title => "INTERLUDE I — Lamplight", :name => "Kestrel",
             :charset => ["KESTREL", "trainer_RIVAL_KESTREL", "trainer_RIVAL1"], :trainer_type => :RIVAL_KESTREL,
             :trainer => [:RIVAL_KESTREL, "Kestrel", proc { Prismfall::Rival.version_for(2) }],
             :drop => [:SANDILE], :level_shift => 2,
             :encounters => true },   # the Bleed-touched Haunter on the stairs is a scripted wild battle
      # II "Bride Tree" (Ch9, the Heartgarden 294): Rowan's Warden team at K4's levels. No battles, no encounters.
      2 => { :id => :BRIDE_TREE, :title => "INTERLUDE II — The Bride Tree", :name => "Rowan",
             :charset => ["ROWAN", "trainer_LEADER_ROWAN", "MOURNER"], :trainer_type => :LEADER_ROWAN,
             :party => [
               [:TREVENANT, 42, { :nickname => "Glasswood", :ability => :NATURALCURE, :item => :SITRUSBERRY, :nature => :ADAMANT,
                                  :moves => [:WOODHAMMER, :SHADOWCLAW, :HORNLEECH, :WILLOWISP] }],
               [:LEAVANNY, 41, { :ability => :SWARM, :nature => :JOLLY, :moves => [:LEAFBLADE, :XSCISSOR, :STICKYWEB, :SWORDSDANCE] }],
               [:ROSERADE, 41, { :ability => :NATURALCURE, :nature => :TIMID, :moves => [:GIGADRAIN, :SLUDGEBOMB, :SLEEPPOWDER, :SYNTHESIS] }],
               [:SUNFLORA, 41, { :ability => :CHLOROPHYLL, :nature => :MODEST, :moves => [:SOLARBEAM, :EARTHPOWER, :SUNNYDAY, :LEECHSEED] }]
             ] },
      # III "Dead Letters" (Ch12, Voss's office): Kestrel's K5 team, healed.
      3 => { :id => :DEAD_LETTERS, :title => "INTERLUDE III — Dead Letters", :name => "Kestrel",
             :charset => ["KESTREL", "trainer_RIVAL_KESTREL", "trainer_RIVAL1"], :trainer_type => :RIVAL_KESTREL,
             :trainer => [:RIVAL_KESTREL, "Kestrel", proc { Prismfall::Rival.version_for(5) }] },
      # IV "Clear Air" (Ch16, Mirefen 220/223): Wenlow with Corvin's spare Pokemon, Lv 62. Two Directorate officers
      # (Grane, Tull) on :CORROSIVE_MIRE; the Interlude can't be failed.
      4 => { :id => :CLEAR_AIR, :title => "INTERLUDE IV — Clear Air", :name => "Wenlow",
             :charset => ["WENLOW", "trainer_WENLOW"], :trainer_type => :PARTNER_WENLOW,
             :party => [
               [:AMOONGUSS, 62, { :ability => :REGENERATOR, :item => :BLACKSLUDGE, :nature => :BOLD,
                                  :moves => [:SPORE, :GIGADRAIN, :SLUDGEBOMB, :CLEARSMOG], :ivs => 25,
                                  :evs => { :HP => 252, :DEFENSE => 128, :SPECIAL_DEFENSE => 128 } }],
               [:SWALOT, 62, { :ability => :STICKYHOLD, :item => :SITRUSBERRY, :nature => :RELAXED,
                               :moves => [:SLUDGEBOMB, :EARTHQUAKE, :ICEBEAM, :YAWN], :ivs => 25,
                               :evs => { :HP => 252, :DEFENSE => 128, :SPECIAL_ATTACK => 128 } }],
               [:GASTRODON, 62, { :ability => :STORMDRAIN, :item => :LEFTOVERS, :nature => :MODEST,
                                  :moves => [:EARTHPOWER, :SCALD, :ICEBEAM, :RECOVER], :ivs => 25,
                                  :evs => { :HP => 252, :SPECIAL_ATTACK => 252 } }]
             ] },
      # V "The Last Night" (Ch20, the Sovereign's Sanctum): Valen, slow, one arm. No battles. His own team, without
      # Zygarde (the Cell is on the windowsill, and no legendary ever sits in the player's party in the story).
      5 => { :id => :LAST_NIGHT, :title => "INTERLUDE V — The Last Night", :name => "Valen",
             :charset => ["VALEN_GLOVELESS", "VALEN", "trainer_CHAMPION_VALEN"], :trainer_type => :CHAMPION_VALEN,
             :trainer => [:CHAMPION_VALEN, "Valen", 0], :no_legendaries => true,
             :menu => false, :walk_only => true, :walk_speed => 2 }
    }

    class << self
      #-------------------------------------------------------------------------
      # State
      #-------------------------------------------------------------------------
      def stash
        return Prismfall.state.custom[:interlude]
      end

      def active?(n = nil)
        st = stash
        return false if !st.is_a?(Hash)
        return n.nil? || st[:n] == n
      end

      def current
        return active? ? stash[:n] : 0
      end

      def loadout(n = nil)
        n ||= current
        return LOADOUTS[n]
      end

      # The running Interlude's effective settings (LOADOUTS row + start overrides).
      def settings
        return {} if !active?
        return (LOADOUTS[stash[:n]] || {}).merge(stash[:overrides] || {})
      end

      def title(n)
        row = LOADOUTS[n]
        return (row) ? _INTL(row[:title]) : ""
      end

      def log(msg)
        PBDebug.log("[Prismfall Interlude] #{msg}") if defined?(PBDebug)
        echoln("[Prismfall Interlude] #{msg}") if $DEBUG && defined?(echoln)
      end

      #-------------------------------------------------------------------------
      # Building the loadout
      #-------------------------------------------------------------------------
      def build_row(row)
        species, level, o = row
        o ||= {}
        if !GameData::Species.exists?(species)
          log("unknown species #{species.inspect}; skipped")
          return nil
        end
        pkmn = Pokemon.new(species, level)
        pkmn.form = o[:form] if o[:form]
        pkmn.makeMale if o[:gender] == 0
        pkmn.makeFemale if o[:gender] == 1
        pkmn.nature = o[:nature] if o[:nature] && GameData::Nature.exists?(o[:nature])
        pkmn.ability = o[:ability] if o[:ability] && GameData::Ability.exists?(o[:ability])
        pkmn.item = o[:item] if o[:item] && GameData::Item.exists?(o[:item])
        if o[:moves]
          moves = o[:moves].select { |m| GameData::Move.exists?(m) }
          if !moves.empty?
            pkmn.forget_all_moves
            moves.each { |m| pkmn.learn_move(m) }
          end
        end
        if o[:ivs]
          GameData::Stat.each_main do |s|
            pkmn.iv[s.id] = o[:ivs].is_a?(Hash) ? (o[:ivs][s.id] || pkmn.iv[s.id]) : o[:ivs].to_i
          end
        end
        (o[:evs] || {}).each { |stat, v| pkmn.ev[stat] = v }
        pkmn.name = _INTL(o[:nickname]) if o[:nickname]
        return pkmn
      end

      def trainer_party(cfg)
        type, name, version = cfg[:trainer]
        version = version.call if version.respond_to?(:call)
        version ||= 0
        data = GameData::Trainer.try_get(type, name, version)
        if !data
          log("no trainer #{[type, name, version].inspect}; loadout skipped")
          return []
        end
        party = data.to_trainer.party.compact
        party = party.reject { |p| cfg[:drop].include?(p.species) } if cfg[:drop]
        party = party.select { |p| cfg[:only].include?(p.species) } if cfg[:only]
        if cfg[:no_legendaries] && Prismfall.respond_to?(:legendary_species?)
          party = party.reject { |p| Prismfall.legendary_species?(p.species) }
        end
        if cfg[:level_shift].to_i != 0
          max = GameData::GrowthRate.max_level
          party.each { |p| p.level = (p.level + cfg[:level_shift]).clamp(1, max) }
        end
        return party
      end

      # Returns the Pokemon for a loadout Hash (never raises on missing data).
      def build_party(cfg)
        party = []
        party.concat(trainer_party(cfg)) if cfg[:trainer]
        (cfg[:party] || []).each do |row|
          pkmn = row.is_a?(Pokemon) ? row : build_row(row)
          party.push(pkmn) if pkmn
        end
        party = party.first(Settings::MAX_PARTY_SIZE)
        party.each do |p|
          p.owner = Pokemon::Owner.new_from_trainer($player) if $player   # no disobedience, no boosted Exp
          p.calc_stats
          p.heal
        end
        return party
      end

      def resolve_charset(cfg)
        Array(cfg[:charset]).each do |c|
          return c if pbResolveBitmap("Graphics/Characters/#{c}")
        end
        return nil
      end

      #-------------------------------------------------------------------------
      # Start / finish
      #-------------------------------------------------------------------------
      # overrides: any LOADOUTS key (e.g. party: [...], charset: "X", name: "Y", encounters: true).
      # Returns true when the swap happened.
      def start(n, **overrides)
        row = LOADOUTS[n]
        raise ArgumentError, "Unknown Interlude #{n.inspect}" if !row
        if active?
          log("start(#{n}) while Interlude #{current} runs; ignored")
          return false
        end
        return false if !$player
        cfg = row.merge(overrides)
        party = build_party(cfg)
        if party.empty?   # nothing could be built: keep the scene playable
          lead = $player.party.find { |p| p && !p.egg? }
          if lead
            copy = lead.clone
            copy.heal
            party = [copy]
          end
          log("Interlude #{n}: empty loadout; using a copy of the lead")
        end
        st = {
          :n          => n,
          :overrides  => overrides.reject { |k, _| k == :party },
          :party      => $player.party.dup,
          :name       => $player.name,
          :ids        => party.map { |p| p.personalID },
          :charset    => resolve_charset(cfg),
          :encounters => ($game_system) ? $game_system.encounter_disabled : false,
          :menu       => ($game_system) ? $game_system.menu_disabled : false
        }
        Prismfall.state.custom[:interlude] = st
        $player.party = party
        $player.name = _INTL(cfg[:name]) if cfg[:name] && cfg[:rename] != false
        if $game_system
          $game_system.encounter_disabled = true if !cfg[:encounters]
          $game_system.menu_disabled = true if cfg[:menu] == false
        end
        $game_variables[VARIABLE] = n if $game_variables
        refresh_look
        return true
      end

      # Takes back every loadout Pokemon, wherever it went.
      def purge(ids)
        return if !ids || ids.empty?
        if $PokemonStorage
          (0...$PokemonStorage.maxBoxes).each do |box|
            (0...$PokemonStorage.maxPokemon(box)).each do |i|
              pkmn = $PokemonStorage[box, i]
              $PokemonStorage[box, i] = nil if pkmn && ids.include?(pkmn.personalID)
            end
          end
        end
      rescue StandardError => e
        log("purge: #{e.class}: #{e.message}")
      end

      def finish
        st = stash
        return false if !st.is_a?(Hash)
        cfg = settings
        purge(st[:ids])
        # Anything caught as the Interlude character (only if :can_catch) stays with the PC, in the boxes.
        extras = ($player.party || []).reject { |p| !p || st[:ids].include?(p.personalID) }
        $player.party = st[:party] || []
        $player.name = st[:name] if st[:name]
        extras.each do |p|
          next if $player.party.include?(p)
          if !$player.party_full? then $player.party.push(p)
          elsif $PokemonStorage then $PokemonStorage.pbStoreCaught(p)
          end
        end
        if $game_system
          $game_system.encounter_disabled = st[:encounters] ? true : false
          $game_system.menu_disabled = st[:menu] ? true : false if cfg[:menu] == false
        end
        Prismfall.state.custom.delete(:interlude)
        $game_variables[VARIABLE] = 0 if $game_variables
        refresh_look
        return true
      end
      alias stop finish

      def heal
        return false if !active?
        $player.party.each { |p| p&.heal }
        return true
      end

      # Re-reads the player's charset (the PlayerMetadata aliases below answer for the Interlude).
      def refresh_look
        return if !$game_player
        $game_player.charsetData = nil if $game_player.respond_to?(:charsetData=)
        $game_player.refresh_charset if $game_player.respond_to?(:refresh_charset)
        speed = settings[:walk_speed]
        $game_player.move_speed = speed if speed && $game_player.respond_to?(:move_speed=)
      rescue StandardError => e
        log("refresh_look: #{e.class}: #{e.message}")
      end

      def charset
        return (active?) ? stash[:charset] : nil
      end

      def trainer_type
        return nil if !active?
        tt = settings[:trainer_type]
        return nil if !tt || !GameData::TrainerType.exists?(tt)
        return nil if !pbResolveBitmap("Graphics/Trainers/#{tt}_back") && !pbResolveBitmap("Graphics/Trainers/#{tt}")
        return tt
      end

      # After loading a save: a stash without V119 means a scene was left by a debug warp; put the PC back.
      def repair
        return if !active? || !$game_variables
        finish if $game_variables[VARIABLE].to_i == 0
      end
    end
  end
end

#-------------------------------------------------------------------------------
# The Interlude character's look: every movement set uses the one walking sheet
#-------------------------------------------------------------------------------
module GameData
  class PlayerMetadata
    [:walk_charset, :run_charset, :cycle_charset, :surf_charset, :dive_charset, :fish_charset,
     :surf_fish_charset].each do |meth|
      next if !method_defined?(meth)
      old = :"pf_interlude_#{meth}"
      next if method_defined?(old)
      alias_method old, meth
      define_method(meth) do
        cs = Prismfall::Interlude.charset
        next cs if cs
        next send(old)
      end
    end

    if method_defined?(:trainer_type) && !method_defined?(:pf_interlude_trainer_type)
      alias_method :pf_interlude_trainer_type, :trainer_type
      def trainer_type
        tt = Prismfall::Interlude.trainer_type
        return tt || pf_interlude_trainer_type
      end
    end
  end
end

class Game_Player
  if method_defined?(:can_run?) && !method_defined?(:pf_interlude_can_run?)
    alias pf_interlude_can_run? can_run?
    def can_run?
      return false if Prismfall::Interlude.active? && Prismfall::Interlude.settings[:walk_only] && !@move_route_forcing
      return pf_interlude_can_run?
    end
  end

  if method_defined?(:set_movement_type) && !method_defined?(:pf_interlude_set_movement_type)
    alias pf_interlude_set_movement_type set_movement_type
    def set_movement_type(type)
      pf_interlude_set_movement_type(type)
      speed = Prismfall::Interlude.active? ? Prismfall::Interlude.settings[:walk_speed] : nil
      self.move_speed = speed if speed && !@move_route_forcing
    end
  end
end

# Nobody else's Pokemon are caught on someone's last night (or with someone else's hands).
class Battle
  if method_defined?(:pbThrowPokeBall) && !method_defined?(:pf_interlude_pbThrowPokeBall)
    alias pf_interlude_pbThrowPokeBall pbThrowPokeBall
    def pbThrowPokeBall(*args)
      if Prismfall::Interlude.active? && !Prismfall::Interlude.settings[:can_catch] && !@internalBattle.nil? && @internalBattle
        pbDisplay(_INTL("This isn't the time for that."))
        return
      end
      return pf_interlude_pbThrowPokeBall(*args)
    end
  end
end

EventHandlers.add(:on_enter_map, :prismfall_interlude_repair,
  proc { |_old_map_id|
    Prismfall::Interlude.repair
  }
)

def pf_interlude_start(n, **overrides); return Prismfall::Interlude.start(n, **overrides); end
def pf_interlude_end;                   return Prismfall::Interlude.finish;                end
def pf_interlude?(n = nil);             return Prismfall::Interlude.active?(n);            end
def pf_interlude_heal;                  return Prismfall::Interlude.heal;                  end
def pf_interlude_title(n);              return Prismfall::Interlude.title(n);              end
