#===============================================================================
# Prismfall Core - charset aliases for map events
# Built maps still name the stock placeholder charsets (trainer_RIVAL2 for Juno, ...).
# Once the cast's own overworld art is installed in Graphics/Characters, an entry here
# swaps every event using the placeholder, with no map rebuild. An entry is only used
# when its art file exists, so a missing pack falls back to the placeholder.
#===============================================================================
module Prismfall
  CHARSET_ALIASES = {
    "trainer_RIVAL2" => "JUNO"        # Gemini pack, 2026-11-21
    # "trainer_RIVAL1"    => "KESTREL",  (add when the pack lands)
    # "trainer_PROFESSOR" => "LARCH",
  }

  def self.charset_alias(name)
    return name if name.nil? || name.empty?
    @charset_alias_cache ||= {}
    return @charset_alias_cache[name] if @charset_alias_cache.key?(name)
    target = CHARSET_ALIASES[name]
    target = nil if target && !pbResolveBitmap("Graphics/Characters/#{target}")
    @charset_alias_cache[name] = target || name
  end
end

class Game_Event < Game_Character
  def character_name
    return Prismfall.charset_alias(@character_name)
  end
end
