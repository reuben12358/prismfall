#===============================================================================
# Prismfall Maps - runtime support for the generated maps (debug installer action)
# Adds "Install Prismfall maps" to Debug menu > Files. Reads Data/mapinfos_prismfall.txt
# (id<TAB>parent_id<TAB>name, written by mapgen/build.py) and merges those entries into the
# project's own Data/MapInfos.rxdata using the game's Marshal. Existing entries are never
# changed; ID collisions with differently-named maps are reported and skipped.
# Close RPG Maker XP before running it (RMXP rewrites MapInfos.rxdata when it saves).
#===============================================================================
module PrismfallMapInstaller
  LIST_FILE = "Data/mapinfos_prismfall.txt"
  INFOS     = "Data/MapInfos.rxdata"

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

  def install
    return pbMessage(_INTL("{1} not found.", LIST_FILE)) if !FileTest.exist?(LIST_FILE)
    infos = load_data(INFOS)
    list = entries
    ours = list.map { |e| e[0] }
    max_order = 0
    infos.each_value { |info| max_order = info.order if info && info.order > max_order }
    added = 0
    collisions = []
    missing_files = []
    # parents first
    list.sort_by! { |e| [ours.include?(e[1]) ? 1 : 0, e[0]] }
    list.each do |id, parent, name|
      if infos[id]
        collisions.push(sprintf("%03d %s (existing: %s)", id, name, infos[id].name)) if infos[id].name != name
        next
      end
      missing_files.push(id) if !FileTest.exist?(sprintf("Data/Map%03d.rxdata", id))
      info = RPG::MapInfo.new
      info.name      = name
      info.parent_id = (infos[parent] || ours.include?(parent)) ? parent : 0
      max_order += 1
      info.order     = max_order
      infos[id] = info
      added += 1
    end
    if added > 0
      backup = INFOS + ".prismfall-bak"
      File.open(backup, "wb") { |f| f.write(File.open(INFOS, "rb") { |g| g.read }) } if !FileTest.exist?(backup)
      save_data(infos, INFOS)
      $game_temp.map_infos = nil if $game_temp
    end
    msg = _INTL("Prismfall maps: {1} added to MapInfos.", added)
    msg += "\n" + _INTL("Collisions skipped: {1}", collisions.length) if collisions.length > 0
    msg += "\n" + _INTL("Missing map files: {1}", missing_files.length) if missing_files.length > 0
    pbMessage(msg)
    collisions.each { |c| echoln("[Prismfall Maps] ID collision: " + c) }
    missing_files.each { |m| echoln(sprintf("[Prismfall Maps] Data/Map%03d.rxdata missing", m)) }
  end
end

MenuHandlers.add(:debug_menu, :prismfall_install_maps, {
  "name"        => _INTL("Install Prismfall maps"),
  "parent"      => :files_menu,
  "description" => _INTL("Add the generated Prismfall maps to MapInfos.rxdata (close RPG Maker XP first)."),
  "effect"      => proc { PrismfallMapInstaller.install }
})
