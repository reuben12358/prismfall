#===============================================================================
# Prismfall Core - the two player looks (Gemini's Player A / Player B packs)
# The intro's "That's me. (Style A/B)" calls pbChangePlayer(1/2), which reads stock player
# metadata 1/2 (Red/Leaf). This points those two at Prismfall's own trainer types and
# overworld sheets when the art and the PBS trainer types are installed; otherwise the stock
# ones stay. The movement sheets (run, bike, surf/dive, fishing; Gemini's pack of 2026-11-24) are each used when
# their file is installed: a missing run sheet runs in the walk sheet, the others fall back to the stock set.
# Surf-fishing reuses the fishing sheet, as stock Essentials does. (An Interlude's look wins over all of these:
# Core 028 wraps the same methods.)
#===============================================================================
module Prismfall
  PLAYER_LOOKS = {
    1 => { :trainer_type => :PLAYER_A, :walk => "trainer_PLAYER_A",
           :run => "PLAYER_A_run", :cycle => "PLAYER_A_bike", :surf => "PLAYER_A_surf", :dive => "PLAYER_A_surf",
           :fish => "PLAYER_A_fish_offset", :surf_fish => "PLAYER_A_fish_offset" },
    2 => { :trainer_type => :PLAYER_B, :walk => "trainer_PLAYER_B",
           :run => "PLAYER_B_run", :cycle => "PLAYER_B_bike", :surf => "PLAYER_B_surf", :dive => "PLAYER_B_surf",
           :fish => "PLAYER_B_fish_offset", :surf_fish => "PLAYER_B_fish_offset" }
  }

  def self.player_look(id)
    look = PLAYER_LOOKS[id]
    return nil if !look
    @player_look_ok ||= {}
    if !@player_look_ok.key?(id)
      @player_look_ok[id] = GameData::TrainerType.exists?(look[:trainer_type]) &&
                            pbResolveBitmap("Graphics/Characters/#{look[:walk]}") &&
                            pbResolveBitmap("Graphics/Trainers/#{look[:trainer_type]}")
    end
    return @player_look_ok[id] ? look : nil
  end

  # look[key] when that sheet is installed, else nil
  def self.player_sheet(look, key)
    name = look[key]
    return nil if !name
    @player_sheet_ok ||= {}
    @player_sheet_ok[name] = !!pbResolveBitmap("Graphics/Characters/#{name}") if !@player_sheet_ok.key?(name)
    return @player_sheet_ok[name] ? name : nil
  end
end

module GameData
  class PlayerMetadata
    alias pf_look_trainer_type trainer_type unless method_defined?(:pf_look_trainer_type)
    def trainer_type
      look = Prismfall.player_look(@id)
      return look ? look[:trainer_type] : pf_look_trainer_type
    end

    alias pf_look_walk_charset walk_charset unless method_defined?(:pf_look_walk_charset)
    def walk_charset
      look = Prismfall.player_look(@id)
      return look ? look[:walk] : pf_look_walk_charset
    end

    # without a Prismfall running sheet: run in the walk sheet rather than switch to stock Red/Leaf
    alias pf_look_run_charset run_charset unless method_defined?(:pf_look_run_charset)
    def run_charset
      look = Prismfall.player_look(@id)
      return look ? (Prismfall.player_sheet(look, :run) || look[:walk]) : pf_look_run_charset
    end

    [:cycle, :surf, :dive, :fish, :surf_fish].each do |kind|
      meth = :"#{kind}_charset"
      old = :"pf_look_#{meth}"
      next if !method_defined?(meth) || method_defined?(old)
      alias_method old, meth
      define_method(meth) do
        look = Prismfall.player_look(@id)
        next (look && Prismfall.player_sheet(look, kind)) || send(old)
      end
    end
  end
end
