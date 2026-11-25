#===============================================================================
# Prismfall Core - charset aliases for map events
# Built maps still name the stock placeholder charsets (trainer_RIVAL2 for Juno, ...).
# Once the cast's own overworld art is installed in Graphics/Characters, these swap it in
# with no map rebuild. An entry is only used when its art file exists, so a missing pack
# falls back to the placeholder.
#  - CHARSET_ALIASES: placeholders used by ONE character only, swapped everywhere.
#  - NAME_ALIASES: characters whose placeholder is a shared generic sprite (Dorian wears
#    trainer_GENTLEMAN, Tamsin trainer_LASS), swapped only on events named after them.
#===============================================================================
module Prismfall
  CHARSET_ALIASES = {
    "trainer_RIVAL2"    => "JUNO",      # Gemini pack, 2026-11-21
    "trainer_RIVAL1"    => "KESTREL",
    "trainer_PROFESSOR" => "LARCH",
    # Exclusive placeholders (audited across maps_out and war.py; Gemini wiring proposal 2026-11-22)
    "trainer_ROCKER"          => "ROOK",     # all 4 events are Rook (181/186/193/608)
    "trainer_ELITEFOUR_Lance" => "SIGRUN",   # 926 Glass Dunes "Partner"
    "trainer_LEADER_Misty"    => "MARISOL"   # 926 Glass Dunes "Partner"
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
    "Aurelius" => "AURELIUS"
  }

  def self.charset_alias(name, event_name = nil)
    return name if name.nil? || name.empty?
    @charset_alias_cache ||= {}
    key = [name, event_name]
    return @charset_alias_cache[key] if @charset_alias_cache.key?(key)
    target = CHARSET_ALIASES[name]
    if !target && event_name && name.start_with?("trainer_")
      NAME_ALIASES.each { |who, cs| target = cs if event_name[/\b#{who}\b/] }
    end
    target = nil if target && !pbResolveBitmap("Graphics/Characters/#{target}")
    @charset_alias_cache[key] = target || name
  end
end

class Game_Event < Game_Character
  def character_name
    return Prismfall.charset_alias(@character_name, (@event.name rescue nil))
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
