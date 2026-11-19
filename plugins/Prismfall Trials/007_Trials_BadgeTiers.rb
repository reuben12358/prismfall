#===============================================================================
# Prismfall Trials - 007 Badge-gated encounters ("the grass rustles")
#-------------------------------------------------------------------------------
# After each badge, rarer species start to appear on maps the player has
# already walked (SPINE Revision 13 item 5). Data: pbs/encounters_badgetiers.txt,
# a normal v21.1 encounters file (compiled as PBS/encounters_badgetiers.txt) whose
# sections are OVERLAYS, never whole tables:
#   [520,101]  = extra slots for map 520 once the player holds 1+ badge
#   [520,104]  = ... 4+ badges.   Version = TIER_VERSION_BASE * (v + 1) + badges,
#                                  so [520,201] = 1+ badges while encounter_version is 1.
# Rules (design/BADGE_TIERS.md):
#  * Overlay slots are appended to the map's live table for the current
#    encounter version (they add weight; nothing is removed).
#  * A "Land" overlay also feeds LandDay/LandNight/LandMorning... when the base
#    table splits Land by time and the overlay doesn't define that variant itself.
#    Same for Cave and Water.
#  * An overlay may add a type the base table lacks (e.g. HeadbuttHigh); its step
#    chance comes from the overlay header ("Land,21") or the type's default.
#  * A map with no base table at all (a route still being built) gets nothing.
# Hints: a rumour per (map, tier) for Trial halls (pf_trial_rumours / board
# "Rumours"), the quest log's Rumours tab, and a one-time "rustling" notice the
# first time the player walks onto a map after its tier unlocked.
#===============================================================================
module Prismfall
  module Trials
    module BadgeTiers
      # Optional hand-written rumours: [map_id, badges] => "text". Anything
      # without one uses GENERIC_RUMOUR.
      RUMOURS = {}
      GENERIC_RUMOUR = "Folk say something rarer has been rustling around {1} since your {2} badge."
      ENTRY_NOTICE   = "The grass here rustles differently than you remember..."

      def self.version_for(badges, enc_version = nil)
        enc_version = ($PokemonGlobal) ? $PokemonGlobal.encounter_version.to_i : 0 if enc_version.nil?
        return TIER_VERSION_BASE * (enc_version + 1) + badges
      end

      def self.badges
        return Prismfall.badge_count
      end

      # Overlay data for map, tier b (or nil).
      def self.overlay(map_id, b, enc_version = nil)
        ver = version_for(b, enc_version)
        return nil if !GameData::Encounter.exists?(map_id, ver)
        return GameData::Encounter.get(map_id, ver)
      end

      # All tiers defined for a map (badge numbers), for the current encounter version.
      def self.tiers_for(map_id, enc_version = nil)
        return (1..Prismfall::BADGE_COUNT).select { |b| overlay(map_id, b, enc_version) }
      end

      # Highest tier the player has unlocked on this map (0 = none).
      def self.unlocked_tier(map_id)
        return tiers_for(map_id).select { |b| b <= badges }.max || 0
      end

      TIME_SUFFIXES = ["Day", "Night", "Morning", "Afternoon", "Evening"].freeze

      # Appends unlocked overlays onto tables/step chances (both Hashes, modified).
      def self.merge_into(map_id, tables, steps)
        held = badges
        return [] if held <= 0
        # No base table yet (a route still being built): add nothing.
        return [] if !GameData::Encounter.get(map_id, ($PokemonGlobal) ? $PokemonGlobal.encounter_version.to_i : 0)
        applied = []
        (1..held).each do |b|
          data = overlay(map_id, b)
          next if !data
          applied.push(b)
          data.types.each do |type, slots|
            next if !slots || slots.empty?
            targets = [type]
            TIME_SUFFIXES.each do |suf|
              variant = "#{type}#{suf}".to_sym
              targets.push(variant) if tables[variant] && !data.types[variant]
            end
            targets.each do |t|
              tables[t] ||= []
              slots.each { |s| tables[t].push(s.clone) }
              if !steps[t]
                st = data.step_chances[type]
                st ||= GameData::EncounterType.get(t).trigger_chance if GameData::EncounterType.exists?(t)
                steps[t] = st if st
              end
            end
          end
        end
        return applied
      end

      #-------------------------------------------------------------------------
      # Rumours / hints
      #-------------------------------------------------------------------------
      def self.map_name(map_id)
        return pbGetMapNameFromId(map_id) if defined?(pbGetMapNameFromId)
        return _INTL("map {1}", map_id)
      end

      # Rumour lines may say {map}; it becomes the map's current name, so
      # renamed routes don't break the hint.
      def self.rumour_text(map_id, b)
        text = RUMOURS[[map_id, b]]
        return _INTL(text).gsub("{map}", map_name(map_id)) if text
        badge = (Prismfall.gym(b)) ? _INTL("{1}", Prismfall.gym(b)[:city]) : b.to_s
        return _INTL(GENERIC_RUMOUR, map_name(map_id), badge)
      end

      # Called when a badge is awarded: every map with a tier for exactly that
      # badge count becomes a rumour.
      def self.on_badge(count)
        list = Prismfall::Trials.store[:rumours]
        GameData::Encounter.each do |enc|
          next if enc.version != version_for(count)
          key = [enc.map, count]
          list.push(key) if !list.include?(key)
        end
        refresh_current_map
      end

      def self.rumours
        return Prismfall::Trials.store[:rumours].select { |m, b| b <= badges }
      end

      # Rumours the player hasn't walked into yet (newest first).
      def self.fresh_rumours
        seen = Prismfall::Trials.store[:tiers_seen]
        return rumours.reject { |m, b| seen.has_key?(m) && seen[m] >= b }.reverse
      end

      def self.refresh_current_map
        return if !$PokemonEncounters || !$game_map
        $PokemonEncounters.setup($game_map.map_id)
      end

      # On entering a map: remember the tier, and queue the rustling notice
      # if this is the first visit since a new tier opened.
      def self.on_enter(map_id)
        return if tiers_for(map_id).empty?
        seen = Prismfall::Trials.store[:tiers_seen]
        t = unlocked_tier(map_id)
        if !seen.has_key?(map_id)   # first visit ever: nothing has "changed" yet
          seen[map_id] = t
          return
        end
        return if seen[map_id] >= t
        seen[map_id] = t
        Prismfall::Trials.store[:notice] = map_id if TIER_ENTRY_NOTICE
      end

      def self.show_notice
        st = Prismfall::Trials.store
        return if !st[:notice]
        return if $game_temp.nil? || $game_temp.message_window_showing || $game_temp.in_menu
        return if $game_player && ($game_player.moving? || $game_player.move_route_forcing)
        return if pbMapInterpreterRunning?
        st[:notice] = nil
        pbSEPlay("Player bump") rescue nil
        pbMessage(_INTL(ENTRY_NOTICE))
      end
    end
  end
end

#-------------------------------------------------------------------------------
# Encounter hooks (alias-chained)
#-------------------------------------------------------------------------------
class PokemonEncounters
  alias __prismfall_trials__setup setup unless method_defined?(:__prismfall_trials__setup)

  def setup(map_ID)
    __prismfall_trials__setup(map_ID)
    @prismfall_tiers = Prismfall::Trials::BadgeTiers.merge_into(map_ID, @encounter_tables, @step_chances)
  end

  def prismfall_tiers; return @prismfall_tiers || []; end

  alias __prismfall_trials__choose_for_map choose_wild_pokemon_for_map unless method_defined?(:__prismfall_trials__choose_for_map)

  # Bug-Catching-Contest style lookups see the same overlays.
  def choose_wild_pokemon_for_map(map_ID, enc_type)
    base = GameData::Encounter.get(map_ID, $PokemonGlobal.encounter_version)
    return __prismfall_trials__choose_for_map(map_ID, enc_type) if !base
    tables = Marshal.load(Marshal.dump(base.types))
    Prismfall::Trials::BadgeTiers.merge_into(map_ID, tables, {})
    list = tables[enc_type]
    return nil if !list || list.empty?
    total = list.sum { |a| a[0] }
    rnd = rand(total)
    list.each do |enc|
      rnd -= enc[0]
      next if rnd >= 0
      return [enc[1], rand(enc[2]..enc[3])]
    end
    return nil
  end
end

EventHandlers.add(:prismfall_badge_awarded, :prismfall_trials_tiers,
  proc { |_n| Prismfall::Trials::BadgeTiers.on_badge(Prismfall.badge_count) }
)

EventHandlers.add(:on_enter_map, :prismfall_trials_tiers,
  proc { |_old_map_id|
    next if !$game_map
    Prismfall::Trials::BadgeTiers.on_enter($game_map.map_id)
  }
)

EventHandlers.add(:on_frame_update, :prismfall_trials_tier_notice,
  proc {
    next if !$prismfall.is_a?(Prismfall::SaveState)
    t = $prismfall.instance_variable_get(:@trials)
    next if !t || !t[:notice]
    Prismfall::Trials::BadgeTiers.show_notice
  }
)

# Lines for a Trial-hall NPC: "Heard anything?"
def pf_trial_rumours(max = 2)
  list = Prismfall::Trials::BadgeTiers.fresh_rumours
  if list.empty?
    pbMessage(_INTL("Nothing new on the roads. Earn another badge and folk will start talking."))
    return false
  end
  list.first(max).each { |m, b| pbMessage(Prismfall::Trials::BadgeTiers.rumour_text(m, b)) }
  return true
end
