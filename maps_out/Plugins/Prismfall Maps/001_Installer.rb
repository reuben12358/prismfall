#===============================================================================
# Prismfall Maps - runtime support for the generated maps (debug installer action)
# Adds "Install Prismfall maps" to Debug menu > Files. Uses the game's own Marshal:
# 1. Tilesets: merges the RPG::Tileset entries of Data/Tilesets_prismfall.rxdata
#    (a Hash id => tileset, written by mapgen/export_tilesets_rxdata.py) into the
#    project's Data/Tilesets.rxdata. Empty slots below an ID are padded with blank
#    tilesets (RMXP's Database needs every slot). A slot already holding a tileset
#    with a different name is reported and left alone.
# 2. MapInfos: reads Data/mapinfos_prismfall.txt (id<TAB>parent_id<TAB>name,
#    written by mapgen/build.py) and adds those entries to Data/MapInfos.rxdata.
#    Entries Essentials' compiler made for our map files ("MAP100" etc., added on
#    every Debug boot for map files without an entry) get our name and parent.
#    Any other entry is kept; an ID used by a differently named map is reported.
# Each file is backed up once (*.prismfall-bak) before its first change. Running
# the installer again changes nothing unless the kit's files changed.
# Close RPG Maker XP before running it (RMXP rewrites these files when it saves).
#===============================================================================
module PrismfallMapInstaller
  LIST_FILE     = "Data/mapinfos_prismfall.txt"
  INFOS         = "Data/MapInfos.rxdata"
  TILESETS_FILE = "Data/Tilesets_prismfall.rxdata"
  TILESETS      = "Data/Tilesets.rxdata"
  BACKUP_SUFFIX = ".prismfall-bak"

  module_function

  def entries
    ret = []
    File.open(LIST_FILE, "rb") do |f|
      f.each_line do |line|
        line = line.force_encoding(Encoding::UTF_8).chomp
        next if line.strip.empty? || line.start_with?("#")
        id, parent, name = line.split("\t", 3)
        ret.push([id.to_i, parent.to_i, name])
      end
    end
    return ret
  end

  def backup(path)
    bak = path + BACKUP_SUFFIX
    return if FileTest.exist?(bak)
    File.open(bak, "wb") { |f| f.write(File.open(path, "rb") { |g| g.read }) }
  end

  # The name Compiler.import_new_maps gives a map file that has no MapInfos entry
  def placeholder?(id, info)
    return info.name.to_s == sprintf("MAP%03d", id)
  end

  def tileset_free?(ts)
    return ts.nil? || (ts.name.to_s.empty? && ts.tileset_name.to_s.empty?)
  end

  # -> [installed ids, updated ids, collision strings], or nil without the kit file
  def install_tilesets
    return nil if !FileTest.exist?(TILESETS_FILE)
    ours = load_data(TILESETS_FILE)
    tilesets = load_data(TILESETS)
    installed = []
    updated = []
    collisions = []
    ours.keys.sort.each do |id|
      ts = ours[id]
      next if !ts.is_a?(RPG::Tileset)
      cur = tilesets[id]
      if !tileset_free?(cur) && cur.name != ts.name
        collisions.push(sprintf("%03d %s (existing: %s)", id, ts.name,
                                cur.name.to_s.empty? ? cur.tileset_name : cur.name))
        next
      end
      ts.id = id
      next if cur && Marshal.dump(cur) == Marshal.dump(ts)   # already installed
      (tilesets.length...id).each do |i|                     # pad empty slots
        next if tilesets[i] || i == 0
        blank = RPG::Tileset.new
        blank.id = i
        tilesets[i] = blank
      end
      (tileset_free?(cur) ? installed : updated).push(id)
      tilesets[id] = ts
    end
    if installed.length + updated.length > 0
      backup(TILESETS)
      save_data(tilesets, TILESETS)
      $data_tilesets = tilesets if $data_tilesets
    end
    return installed, updated, collisions
  end

  # Our maps in tree order (parents before children), so RMXP's map tree nests them
  def tree_order(list)
    by_parent = {}
    ids = list.map { |e| e[0] }
    list.each { |e| (by_parent[ids.include?(e[1]) ? e[1] : 0] ||= []).push(e) }
    ret = []
    walk = proc do |parent|
      (by_parent[parent] || []).sort_by { |e| e[0] }.each do |e|
        ret.push(e)
        walk.call(e[0]) if e[0] != parent
      end
    end
    walk.call(0)
    ret += (list - ret).sort_by { |e| e[0] }   # parent loops: keep them, unnested order
    return ret
  end

  # -> [added, renamed, collision strings, missing map file ids]
  def install_mapinfos
    infos = load_data(INFOS)
    list = tree_order(entries)
    ours = list.map { |e| e[0] }
    managed = list.select { |id, _p, _n| infos[id].nil? || placeholder?(id, infos[id]) }.map { |e| e[0] }
    collisions = []
    list.each do |id, _parent, name|
      next if managed.include?(id) || infos[id].name == name
      collisions.push(sprintf("%03d %s (existing: %s)", id, name, infos[id].name))
    end
    missing_files = ours.reject { |id| FileTest.exist?(sprintf("Data/Map%03d.rxdata", id)) }
    added = 0
    renamed = 0
    if managed.length > 0
      max_order = 0
      infos.each { |id, info| max_order = info.order if info && !managed.include?(id) && info.order > max_order }
      list.each do |id, parent, name|
        next if !managed.include?(id)
        info = infos[id]
        if info
          renamed += 1
        else
          info = RPG::MapInfo.new
          added += 1
        end
        info.name      = name
        info.parent_id = (infos[parent] || ours.include?(parent)) ? parent : 0
        max_order += 1
        info.order     = max_order
        infos[id] = info
      end
      backup(INFOS)
      save_data(infos, INFOS)
      $game_temp.map_infos = nil if $game_temp && $game_temp.respond_to?(:map_infos=)
    end
    return added, renamed, collisions, missing_files
  end

  # new_game: called from the New Game start check (004_NewGameStart.rb), which carries on without a restart
  def install(new_game: false)
    return pbMessage(_INTL("{1} not found.", LIST_FILE)) if !FileTest.exist?(LIST_FILE)
    msg = []
    ts = install_tilesets
    if ts.nil?
      msg.push(_INTL("Tilesets: {1} not found.", TILESETS_FILE))
    else
      msg.push(_INTL("Tilesets: {1} installed, {2} updated.", ts[0].length, ts[1].length))
      msg.push(_INTL("Tileset ID collisions skipped: {1}", ts[2].length)) if ts[2].length > 0
      ts[2].each { |c| echoln("[Prismfall Maps] Tileset ID collision: " + c) }
    end
    added, renamed, collisions, missing_files = install_mapinfos
    msg.push(_INTL("Maps: {1} added to MapInfos, {2} renamed.", added, renamed))
    msg.push(_INTL("Map ID collisions skipped: {1}", collisions.length)) if collisions.length > 0
    msg.push(_INTL("Missing map files: {1}", missing_files.length)) if missing_files.length > 0
    collisions.each { |c| echoln("[Prismfall Maps] Map ID collision: " + c) }
    missing_files.each { |m| echoln(sprintf("[Prismfall Maps] Data/Map%03d.rxdata missing", m)) }
    changed = (ts && ts[0].length + ts[1].length > 0) || added + renamed > 0
    if !changed
      msg.push(_INTL("Everything was already installed."))
    elsif !new_game
      msg.push(_INTL("Restart the game now."))
    end
    echoln("[Prismfall Maps] " + msg.join(" "))
    pbMessage(msg.join("\n"))
  end
end

MenuHandlers.add(:debug_menu, :prismfall_install_maps, {
  "name"        => _INTL("Install Prismfall maps"),
  "parent"      => :files_menu,
  "description" => _INTL("Add the Prismfall tilesets and maps to Tilesets.rxdata and MapInfos.rxdata (close RPG Maker XP first)."),
  "effect"      => proc { PrismfallMapInstaller.install }
})
