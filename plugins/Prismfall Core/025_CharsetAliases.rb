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
    "trainer_PROFESSOR" => "LARCH"
  }
  NAME_ALIASES = {
    "Dorian" => "DORIAN",
    "Tamsin" => "TAMSIN"
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
