#===============================================================================
# Prismfall Core - charset aliases for map events
# Built maps still name the stock placeholder charsets (trainer_RIVAL2 for Juno, ...).
# Once the cast's own overworld art is installed in Graphics/Characters, these swap it in
# with no map rebuild. An entry is only used when its art file exists, so a missing pack
# falls back to the placeholder.
#  - CHARSET_ALIASES: placeholders used by ONE character only, swapped everywhere.
#  - NAME_ALIASES: characters whose placeholder is a shared generic sprite (Dorian wears
#    trainer_GENTLEMAN, Tamsin trainer_LASS, Captain Edda "NPC 14"), swapped only on events
#    named after them (whole words; "Wenna's cousin" is not Wenna).
#  - TYPE_CHARSETS: uniformed classes. An event that battles as one of these wears
#    trainer_<TYPE> instead of the stock stand-in its map was built with.
#===============================================================================
module Prismfall
  CHARSET_ALIASES = {
    "trainer_RIVAL2"    => "JUNO",      # Gemini pack, 2026-11-21
    "trainer_RIVAL1"    => "KESTREL",
    "trainer_PROFESSOR" => "LARCH",
    # Exclusive placeholders (audited across maps_out and war.py; Gemini wiring proposal 2026-11-22)
    "trainer_ROCKER"          => "ROOK"      # all 4 events are Rook (181/186/193/608)
    # (2026-11-26: the 926 "Partner" rows for trainer_ELITEFOUR_Lance / trainer_LEADER_Misty went with the Ch19 rebuild;
    #  no built map uses either sheet. A Sigrun or Marisol event is reached by name below.)
  }
  NAME_ALIASES = {
    "Dorian" => "DORIAN",  "Tamsin" => "TAMSIN",  "Marisol" => "MARISOL", "Voss" => "VOSS",
    "Aurelian" => "VOSS",  "Valen" => "VALEN",    "Rook" => "ROOK",       "Sahar" => "SAHAR",
    "Corvin" => "CORVIN",  "Brann" => "BRANN",    "Kaito" => "KAITO",     "Anja" => "ANJA",
    "Odessa" => "ODESSA",  "Ilsa" => "ILSA",      "Bastian" => "BASTIAN", "Ysolde" => "YSOLDE",
    "Magnus" => "MAGNUS",  "Nyx" => "NYX",        "Celestine" => "CELESTINE", "Sigrun" => "SIGRUN",
    "Mourner" => "MOURNER",
    # Art Drop 13
    "Vesper" => "VESPER", "Thistle" => "THISTLE", "Marchetti" => "MARCHETTI", "Helene" => "MARCHETTI",
    "Quent" => "QUENT", "Percival" => "QUENT", "Kroll" => "KROLL", "Sabine" => "KROLL", "Sable" => "SABLE",
    # The Gilded King (Path B rename, 2026-11-23): "Aurelius" never matches Voss's "Aurelian" (whole words). Not bare
    # "Gilded King": the Night of Masques actor who plays him would get the real King's sprite.
    "Aurelius" => "AURELIUS",
    # Art Drop 14 and earlier cast whose sheets were never aliased (Gemini wiring audit 2026-11-24)
    "Maelis" => "MAELIS", "Rowan" => "ROWAN", "Teo" => "TEO", "Wick" => "WICK", "Wenlow" => "WENLOW",
    "Morwen" => "MORWEN", "Dask" => "DASK", "Imre" => "DASK",
    # Art Drop 15: story NPCs. Not bare "Pip": 151's "Apprentice Pip" is a Saltmere stagehand and two route
    # trainers are called Pip; Bastian's granddaughter is "Pip Ore" (name her events that, or set charset PIP).
    "Edda" => "EDDA", "Calla" => "CALLA", "Wenna" => "WENNA", "Hesper" => "HESPER", "Coll" => "COLL",
    "Dex" => "DEX", "Pip Ore" => "PIP", "Hollis" => "HOLLIS", "Martin" => "MARTIN",
    "Maud" => "MAUD", "Ellery" => "MAUD", "Hierophant" => "MAUD",
    # Art Drops 15-16: rulers and the Council
    "Eirik" => "EIRIK", "Hrothgar" => "HROTHGAR", "Kassan" => "KASSAN", "Okoro" => "OKORO",
    "Gutter" => "GUTTER", "Renata" => "RENATA", "Sallow" => "RENATA",
    # Riot Punk Zara (the old punk "Venam" art, moved to an original character 2026-11-24)
    "Zara" => "ZARA",
    # Sister-game cameos in their home-game looks (design/CAMEOS.md; Gemini cameo waves 1-3)
    "Venam" => "VENAM", "Shelly" => "SHELLY", "Melia" => "MELIA", "Alexandra" => "ALEXANDRA",
    "Amaria" => "AMARIA", "Titania" => "TITANIA", "Garret" => "GARRET", "Shiv" => "SHIV",
    "Lin" => "LIN", "Nova" => "NOVA"
  }
  # Not the Hollow or Meridian agents: some are in disguise on purpose (145 "Pageant" is a grunt in a gentleman's coat).
  TYPE_CHARSETS = %i[
    ASHKAAR_SOLDIER ASHKAAR_SOLDIER_M ASHKAAR_SOLDIER_F ASHKAAR_OFFICER ASHKAAR_EMBER_RIDER
    ISENMAR_SOLDIER_M ISENMAR_SOLDIER_F ISENMAR_OFFICER ISENMAR_TRENCHER ISENMAR_HIRDMAN
    MERIDIAN_DIRECTORATE THORNGUARD THORNWATCH
  ]

  def self.charset_alias(name, event_name = nil)
    return name if name.nil? || name.empty?
    @charset_alias_cache ||= {}
    key = [name, event_name]
    return @charset_alias_cache[key] if @charset_alias_cache.key?(key)
    target = CHARSET_ALIASES[name]
    # Stock stand-ins only: trainer_* sheets and the "NPC 01".."NPC 29" townsfolk (Vesper on 145 is "NPC 14").
    if !target && event_name && (name.start_with?("trainer_") || name.start_with?("NPC "))
      # (?!'s): a possessive is someone else ("Wenna's cousin" on 520)
      NAME_ALIASES.each { |who, cs| target = cs if event_name[/\b#{who}\b(?!['’]s\b)/] }
    end
    target = nil if target && !pbResolveBitmap("Graphics/Characters/#{target}")
    @charset_alias_cache[key] = target || name
  end

  # The one trainer type an event battles as (its TrainerBattle.start calls), or nil.
  def self.event_trainer_type(event)
    types = []
    event.pages.each do |page|
      page.list.each do |cmd|
        next if cmd.code != 355 && cmd.code != 655 && cmd.code != 111
        cmd.parameters.each do |prm|
          next if !prm.is_a?(String) || !prm.include?("TrainerBattle.start")
          prm.scan(/:([A-Za-z0-9_]+)\s*,\s*["']/) { |m| types.push(m[0].to_sym) }   # every :TYPE, "Name" pair
        end
      end
    end
    types.uniq!
    return (types.length == 1) ? types[0] : nil
  rescue StandardError
    return nil
  end

  # "trainer_<TYPE>" for an event of a TYPE_CHARSETS class whose own sheet is installed, else nil.
  def self.type_charset(map_id, event)
    return nil if !event
    @type_charset_cache ||= {}
    key = [map_id, event.id]
    return @type_charset_cache[key] || nil if @type_charset_cache.key?(key)
    type = event_trainer_type(event)
    sheet = nil
    if type && TYPE_CHARSETS.include?(type)
      # the class's own sheet, or the one Core 032 lends it (ASHKAAR_SOLDIER -> _M)
      file = (GameData::TrainerType.charset_filename(type) rescue nil)
      file ||= "Graphics/Characters/trainer_#{type}" if pbResolveBitmap("Graphics/Characters/trainer_#{type}")
      sheet = file.sub(%r{\AGraphics/Characters/}, "") if file
    end
    @type_charset_cache[key] = sheet || false
    return sheet
  end
end

class Game_Event < Game_Character
  def character_name
    name = @character_name
    if name && name.start_with?("trainer_") && !Prismfall::CHARSET_ALIASES.key?(name)
      sheet = Prismfall.type_charset(@map_id, @event)
      return sheet if sheet
    end
    return Prismfall.charset_alias(name, (@event.name rescue nil))
  end
end

#===============================================================================
# "You are challenged by The Mourner Mourner!": when a trainer type's display name already ends with
# the trainer's own name (type "The Mourner", trainer "Mourner"), say it once.
#===============================================================================
class Trainer
  alias __prismfall_full_name full_name unless method_defined?(:__prismfall_full_name)

  def full_name
    tn = (trainer_type_name rescue "").to_s
    return tn if !name.to_s.empty? && tn.end_with?(name.to_s)
    return __prismfall_full_name
  end
end
