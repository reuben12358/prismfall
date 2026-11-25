#!/usr/bin/env python3
"""design/MAP_AUDIO.yaml -> maps_out/Plugins/Prismfall Maps/013_MapAudio.rb (map BGM / BGS, Audio v4.3).

usage: python3 -I mapgen/map_audio.py [--check]
build.py calls write(specs) on every build, so the plugin always matches the yaml. Running this file alone
regenerates the plugin without rebuilding any map (--check only validates and prints).

The yaml is the default for every map; a spec's own `map_audio: {bgm:, bgm_volume:, bgs:, bgs_volume:, rain:}` block
wins over it key by key. Nothing is baked into MapNNN.rxdata: the plugin patches the loaded map at run time and only
with files that exist, so the spec's `bgm:` stays the fallback for a project without the Prismfall audio installed."""
import csv, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
YAML = os.path.join(ROOT, 'design', 'MAP_AUDIO.yaml')
OUT = os.path.join(ROOT, 'maps_out', 'Plugins', 'Prismfall Maps', '013_MapAudio.rb')
KEYS = ('bgm', 'bgm_volume', 'bgs', 'bgs_volume', 'rain')

RUBY = r'''
  RAIN_BGS         = "Rain"
  RAIN_BGS_VOLUME  = 65
  RAIN_WEATHERS    = [:Rain, :Storm, :HeavyRain]

  def self.audio_file?(folder, name)
    return false if name.nil? || name.to_s.empty?
    return true if !FileTest.respond_to?(:audio_exist?)
    return FileTest.audio_exist?("Audio/#{folder}/#{name}")
  rescue StandardError
    return false
  end

  # Patches a loaded RPG::Map with its MAP_AUDIO entry (only files that exist). Safe to call again.
  def self.apply_map_audio(map_id, map)
    e = MAP_AUDIO[map_id]
    return map if !e || !map
    if e[:bgm] && audio_file?("BGM", e[:bgm])
      map.bgm = RPG::AudioFile.new(e[:bgm], e[:bgm_volume] || 100, 100) if map.bgm.nil? || map.bgm.name != e[:bgm]
      map.autoplay_bgm = true
    end
    if e[:bgs] == ""            # an interior: stop the ambience of the map before it
      map.bgs = RPG::AudioFile.new("", 80, 100)
      map.autoplay_bgs = true
    elsif e[:bgs] && audio_file?("BGS", e[:bgs])
      map.bgs = RPG::AudioFile.new(e[:bgs], e[:bgs_volume] || 80, 100) if map.bgs.nil? || map.bgs.name != e[:bgs]
      map.autoplay_bgs = true
    end
    return map
  rescue StandardError => err
    echoln("[Prismfall Maps] map audio #{map_id}: #{err.class}: #{err.message}") if defined?(echoln)
    return map
  end

  # While it rains on a map flagged :rain, the Rain loop replaces the map's own ambience; when it stops, the
  # map's loop comes back. Weather is rolled on entering a map, so this runs there and after every autoplay.
  def self.sync_weather_bgs
    return if !$game_map || !$game_screen || !$game_system
    e = MAP_AUDIO[$game_map.map_id]
    playing = $game_system.playing_bgs
    raining = RAIN_WEATHERS.include?(($game_screen.weather_type rescue nil))
    if e && e[:rain] && raining && audio_file?("BGS", RAIN_BGS)
      pbBGSPlay(RAIN_BGS, RAIN_BGS_VOLUME) if !playing || playing.name != RAIN_BGS
    elsif playing && playing.name == RAIN_BGS && e
      map = $game_map.instance_variable_get(:@map)
      pbBGSPlay(map.bgs) if map && map.autoplay_bgs     # an empty name stops the loop
    end
  rescue StandardError => err
    echoln("[Prismfall Maps] weather BGS: #{err.class}: #{err.message}") if defined?(echoln)
  end
end

EventHandlers.add(:on_game_map_setup, :prismfall_map_audio,
  proc { |map_id, map, _tileset| PrismfallMaps.apply_map_audio(map_id, map) }
)
EventHandlers.add(:on_enter_map, :prismfall_map_audio_weather,
  proc { |_old_map_id| PrismfallMaps.sync_weather_bgs }
)

class Game_Map
  if !method_defined?(:prismfall_audio_autoplay)
    alias prismfall_audio_autoplay autoplay
    alias prismfall_audio_autoplayAsCue autoplayAsCue
  end

  # (a save made before this plugin holds an unpatched map: patch it here too)
  def autoplay
    PrismfallMaps.apply_map_audio(@map_id, @map)
    prismfall_audio_autoplay
    PrismfallMaps.sync_weather_bgs if $game_map.equal?(self)
  end

  def autoplayAsCue
    PrismfallMaps.apply_map_audio(@map_id, @map)
    prismfall_audio_autoplayAsCue
    PrismfallMaps.sync_weather_bgs if $game_map.equal?(self)
  end
end

class Scene_Map
  # The stock method reads the next map's file directly, so it has to see the patched BGM / BGS too: otherwise
  # every door between two maps that share a Prismfall track would fade it out and restart it. It also faded the
  # BGM (not the BGS) when only the ambience differed, which restarted the music on every town -> interior door.
  def autofade(mapid)
    playing_bgm = $game_system.playing_bgm
    playing_bgs = $game_system.playing_bgs
    return if !playing_bgm && !playing_bgs
    map = PrismfallMaps.apply_map_audio(mapid, load_data(sprintf("Data/Map%03d.rxdata", mapid)))
    if playing_bgm && map.autoplay_bgm
      name = map.bgm.name
      name += "_n" if PBDayNight.isNight? && FileTest.audio_exist?("Audio/BGM/" + name + "_n")
      pbBGMFade(0.8) if playing_bgm.name != name
    end
    pbBGSFade(0.8) if playing_bgs && map.autoplay_bgs && playing_bgs.name != map.bgs.name
    Graphics.frame_reset
  end
end
'''


def manifest_names():
    """{'BGM': {names}, 'BGS': {...}}: every final_name of audio/manifest.tsv whose staged stand-in file exists."""
    have = {}
    with open(os.path.join(ROOT, 'audio', 'manifest.tsv'), newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            src = row['local_source']
            if src.startswith('(') or not os.path.exists(os.path.join(ROOT, 'audio', src)):
                continue
            have.setdefault(row['folder'], set()).add(row['final_name'])
    return have


def load(specs=None):
    """-> ({map id: entry}, [warnings]).  specs: build.py's loaded spec dicts (None = read mapgen/specs/*.yaml)."""
    import yaml
    data = (yaml.safe_load(open(YAML, encoding='utf-8')) or {}).get('maps') or {} if os.path.exists(YAML) else {}
    if specs is None:
        specs = []
        for f in sorted(glob.glob(os.path.join(HERE, 'specs', '*.yaml'))):
            specs += [s for s in yaml.safe_load_all(open(f, encoding='utf-8')) if s]
    names = {s['id']: s['name'] for s in specs}
    entries, warns = {}, []
    for mid, e in data.items():
        entries[int(mid)] = {k: v for k, v in (e or {}).items() if k in KEYS}
        bad = [k for k in (e or {}) if k not in KEYS]
        if bad: warns.append('%s: unknown key(s) %s' % (mid, ', '.join(bad)))
    for s in specs:
        ov = s.get('map_audio')
        if ov:
            entries.setdefault(s['id'], {}).update({k: v for k, v in ov.items() if k in KEYS})
    have = manifest_names()
    for mid in sorted(entries):
        e = entries[mid]
        e['_name'] = names.get(mid, '?')
        if mid not in names: warns.append('%d: not a built map' % mid)
        for key, folder in (('bgm', 'BGM'), ('bgs', 'BGS')):
            if e.get(key) and e[key] not in have.get(folder, ()):
                warns.append('%d %s: %s "%s" is not staged in audio/manifest.tsv (the map keeps its own %s until the file is installed)'
                             % (mid, e['_name'], folder, e[key], key))
        if 'rain' not in e:
            e['rain'] = bool(e.get('bgs'))
    for mid in sorted(set(names) - set(entries)):
        warns.append('%d %s: no MAP_AUDIO entry (keeps the spec bgm, no ambience)' % (mid, names[mid]))
    return entries, warns


def ruby(entries):
    rs = lambda s: '"%s"' % str(s).replace('\\', '\\\\').replace('"', '\\"')
    rb = ['# GENERATED by mapgen/map_audio.py from design/MAP_AUDIO.yaml (+ spec `map_audio:` blocks) - do not edit.',
          '# Map BGM / BGS (Audio v4.3). An entry is applied when its map loads, and only with files that exist:',
          '# a track that is not installed leaves the map\'s own baked-in music alone.',
          'module PrismfallMaps', '  MAP_AUDIO = {']
    for mid in sorted(entries):
        e = entries[mid]; parts = []
        if e.get('bgm'):
            parts.append(':bgm => %s' % rs(e['bgm']))
            if int(e.get('bgm_volume', 100)) != 100: parts.append(':bgm_volume => %d' % int(e['bgm_volume']))
        if 'bgs' in e and e['bgs'] is not None:
            parts.append(':bgs => %s' % rs(e['bgs']))
            if e['bgs']: parts.append(':bgs_volume => %d' % int(e.get('bgs_volume', 80)))
        if e.get('rain'): parts.append(':rain => true')
        if parts:
            rb.append('    %d => { %s },   # %s' % (mid, ', '.join(parts), e['_name']))
    rb.append('  }')
    return '\n'.join(rb) + RUBY


def write(specs=None, quiet=False):
    entries, warns = load(specs)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(ruby(entries))
    if not quiet:
        for w in warns: print('MAP_AUDIO ' + w)
    return entries, warns


def main():
    if '--check' in sys.argv:
        entries, warns = load()
    else:
        entries, warns = write(quiet=True)
    for w in warns: print('MAP_AUDIO ' + w)
    print('map audio: %d maps (%d with a Prismfall BGM, %d with ambience, %d silenced interiors), %d warning(s)' % (
        len(entries), sum(1 for e in entries.values() if e.get('bgm')), sum(1 for e in entries.values() if e.get('bgs')),
        sum(1 for e in entries.values() if e.get('bgs') == ''), len(warns)))


if __name__ == '__main__':
    main()
