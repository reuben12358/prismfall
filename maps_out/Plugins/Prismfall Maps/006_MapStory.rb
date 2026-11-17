#===============================================================================
# Prismfall Maps - 006 story helpers for the generated map events (mapgen/ruby/006_MapStory.rb, copied by build.py)
#-------------------------------------------------------------------------------
# pfm?(:key) / pfm_set(:key) / pfm_add(:key)  small saved story flags and counters for map scenes and sidequests
#                                             (kept in $PokemonGlobal, so no Game Switch IDs are used up)
# pfm_item(:ID, qty, "Name")                  pbReceiveItem when the item exists in PBS; otherwise a "You obtained"
#                                             message and the id is remembered (pfm_has?) so story items work today
# pfm_has?(:ID)                               bag check that also knows the remembered story items
# pfm_take(:ID)                               remove a real or remembered story item
# pfm_quest(:id, "Title", "text")             quest log entry + message; pfm_quest_done(:id) marks it complete
# pfm_money(n)                                give money with a message
# pfm_card(:SCENE, "line", ...)               plays a Prismfall cutscene (title cards below) or shows the lines
# pfm_dusk / pfm_day                          temporary dusk / night tone for a scene, then back to the map tone
#===============================================================================
class PokemonGlobalMetadata
  attr_writer :pf_map_flags, :pf_quests

  def pf_map_flags; return @pf_map_flags ||= {}; end
  def pf_quests;    return @pf_quests ||= {};    end
end

module PrismfallMaps
  def self.flags; return $PokemonGlobal.pf_map_flags; end
end

def pfm?(key);              return !!PrismfallMaps.flags[key];                                   end
def pfm_get(key);           return PrismfallMaps.flags[key];                                     end
def pfm_set(key, v = true); PrismfallMaps.flags[key] = v; return true;                           end
def pfm_add(key, n = 1);    PrismfallMaps.flags[key] = (PrismfallMaps.flags[key] || 0) + n; return PrismfallMaps.flags[key]; end
def pfm_count(key);         return PrismfallMaps.flags[key] || 0;                                end

def pfm_item(id, qty = 1, name = nil)
  return pbReceiveItem(id, qty) if GameData::Item.exists?(id)
  nm = name || id.to_s.capitalize
  nm = "#{nm} ×#{qty}" if qty > 1
  pbMessage("\\me[Key item get]" + _INTL("You obtained \\c[1]{1}\\c[0]!", nm) + "\\wtnp[40]")
  (PrismfallMaps.flags[:story_items] ||= []) << id
  return true
end

def pfm_has?(id)
  return true if GameData::Item.exists?(id) && $bag.has?(id)
  return (PrismfallMaps.flags[:story_items] || []).include?(id)
end

def pfm_take(id, qty = 1)
  if GameData::Item.exists?(id)
    $bag.remove(id, qty)
  else
    (PrismfallMaps.flags[:story_items] || []).delete(id)
  end
  return true
end

def pfm_quest(id, title, text = "")
  q = $PokemonGlobal.pf_quests
  return false if q[id]
  q[id] = { :title => title, :text => text, :done => false }
  pbMessage("\\se[GUI save choice]" + _INTL("QUEST LOG: \"{1}\" — {2}", title, text))
  return true
end

def pfm_quest_done(id)
  q = $PokemonGlobal.pf_quests[id]
  return false if !q || q[:done]
  q[:done] = true
  pbMessage("\\se[GUI save choice]" + _INTL("QUEST COMPLETE: \"{1}\"", q[:title]))
  return true
end

def pfm_quest?(id);      return !$PokemonGlobal.pf_quests[id].nil?;                 end
def pfm_quest_done?(id); q = $PokemonGlobal.pf_quests[id]; return !!(q && q[:done]); end

def pfm_money(n)
  $player.money += n
  pbMessage("\\me[Item get]" + _INTL("\\PN received ${1}!", n.to_s_formatted) + "\\wtnp[30]")
  return true
end

def pfm_card(scene, *lines)
  if defined?(Prismfall::Cutscene) && Prismfall::Cutscene.respond_to?(:exists?) && Prismfall::Cutscene.exists?(scene)
    pbCutscene(scene)
  else
    lines.each { |l| pbMessage(l) }
  end
  return true
end

def pfm_dusk(frames = 20)
  $game_screen.start_tone_change(Tone.new(-60, -70, -10, 60), frames)
  pbWait(frames / 20.0) if frames > 0
end

def pfm_day(frames = 20)
  t = (defined?(PrismfallMaps::MAP_TONES) && PrismfallMaps::MAP_TONES[$game_map.map_id]) || [0, 0, 0, 0]
  $game_screen.start_tone_change(Tone.new(*t), frames)
  pbWait(frames / 20.0) if frames > 0
end

# Title cards and short text scenes used by the early maps (optional: without the Cutscenes plugin the lines show as messages)
if defined?(Prismfall::Cutscene) && Prismfall::Cutscene.respond_to?(:define)
  Prismfall::Cutscene.define(:PF_PROLOGUE_CARD) do
    background :color, color: [0, 0, 0]
    text "Spring, AF 300."
    text "The Concert of Regions has sealed the borders of Velmora."
    text "This is the final civilian crossing."
  end
  Prismfall::Cutscene.define(:PF_ACT1_TITLE) do
    background :color, color: [0, 0, 0]
    title "ACT I — THE LAST FERRY"
  end
  Prismfall::Cutscene.define(:PF_CH1_NOTEBOOK) do
    background :color, color: [10, 14, 24]
    text "Subject reads NULL. Calms Bleed-struck fauna on approach. No tint after one day; I do not expect one after a hundred."
    text "Second such reading in my life."
    text "The first was in Crownhaven, AF 290."
    text "God help us, Ines."
  end
end
