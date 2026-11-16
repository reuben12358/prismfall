#===============================================================================
# Prismfall Core - 016 Ledger (cross-save record of game overs and endings)
#-------------------------------------------------------------------------------
# Stored next to the save file (System.data_directory) as a small text file,
# NOT inside Game.rxdata, so it survives new games and save deletion:
#   Prismfall_Ledger.txt
#     # Prismfall Ledger 1
#     gameover GO_LAST_FERRY 1731700000 2
#     ending END_RETURN 1731800000 1
# (type, ID, first-found Unix time, times reached). Parsing accepts only
# [A-Za-z0-9_] IDs and integers; anything else is ignored.
#===============================================================================
module Prismfall
  module Ledger
    FILENAME = "Prismfall_Ledger.txt"
    HEADER   = "# Prismfall Ledger 1"
    KINDS    = { "gameover" => :game_overs, "ending" => :endings }

    def self.path
      return File.join(File.dirname(SaveData::FILE_PATH), FILENAME)
    end

    def self.blank
      return { :game_overs => {}, :endings => {} }
    end

    def self.data
      @data = read if !@data
      return @data
    end

    def self.reload!
      @data = nil
      return data
    end

    def self.read
      d = blank
      return d if !File.file?(path)
      File.open(path, "rb") do |f|
        f.each_line do |line|
          parts = line.strip.split(/\s+/)
          next if parts.length < 2 || parts[0].start_with?("#")
          bucket = KINDS[parts[0]]
          next if !bucket || parts[1] !~ /\A[A-Za-z0-9_]+\z/
          d[bucket][parts[1].to_sym] = [parts[2].to_i, [parts[3].to_i, 1].max]
        end
      end
      return d
    rescue StandardError
      return blank
    end

    def self.write
      lines = [HEADER]
      KINDS.each do |word, bucket|
        data[bucket].each { |id, v| lines.push("#{word} #{id} #{v[0]} #{v[1]}") }
      end
      tmp = path + ".tmp"
      File.open(tmp, "wb") { |f| f.write(lines.join("\n") + "\n") }
      File.delete(path) if File.file?(path)
      File.rename(tmp, path)
      return true
    rescue StandardError => e
      Prismfall::Narrative.warn("Ledger write failed: #{e.message}")
      return false
    end

    # Returns true if this is the first time the entry was recorded.
    def self.record(bucket, id)
      id = id.to_sym
      entry = data[bucket][id]
      if entry
        entry[1] += 1
      else
        data[bucket][id] = [Time.now.to_i, 1]
      end
      write
      return entry.nil?
    end

    def self.record_game_over(id); return record(:game_overs, id); end
    def self.record_ending(id);    return record(:endings, id);    end

    def self.game_over_found?(id); return data[:game_overs].has_key?(id.to_sym); end
    def self.ending_seen?(id);     return data[:endings].has_key?(id.to_sym);    end
    def self.game_overs_found;     return data[:game_overs].keys;                 end
    def self.endings_seen;         return data[:endings].keys;                    end

    # Registered game overs that count toward the Ruin Route.
    def self.ruin_requirements
      reg = Prismfall::Narrative::GAME_OVERS
      return reg.keys.reject { |id| reg[id][:ruin_exempt] }
    end

    def self.ruin_progress
      req = ruin_requirements
      return [req.count { |id| game_over_found?(id) }, req.length]
    end

    def self.ruin_unlocked?
      found, total = ruin_progress
      return total > 0 && found >= total
    end

    def self.clear!   # debug
      @data = blank
      write
    end
  end

  # Ruin Route in THIS save (story starts it once Ledger.ruin_unlocked?).
  def self.ruin_route?
    return Prismfall.state.narrative[:ruin_route] ? true : false
  end

  # Event usage: Conditional Branch > Script: Prismfall.start_ruin_route
  # Returns false if the Ledger hasn't unlocked it.
  def self.start_ruin_route(force = false)
    return false if !force && !Ledger.ruin_unlocked?
    Prismfall.state.narrative[:ruin_route] = true
    EventHandlers.trigger(:prismfall_ruin_route_started)
    return true
  end
end
