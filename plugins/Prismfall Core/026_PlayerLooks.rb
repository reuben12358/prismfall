#===============================================================================
# Prismfall Core - the two player looks (Gemini's Player A / Player B packs)
# The intro's "That's me. (Style A/B)" calls pbChangePlayer(1/2), which reads stock player
# metadata 1/2 (Red/Leaf). This points those two at Prismfall's own trainer types and
# overworld sheets when the art and the PBS trainer types are installed; otherwise the stock
# ones stay. Running uses the walk sheet; cycle/surf/fish sets stay stock until Prismfall versions exist.
#===============================================================================
module Prismfall
  PLAYER_LOOKS = {
    1 => { :trainer_type => :PLAYER_A, :walk => "trainer_PLAYER_A" },
    2 => { :trainer_type => :PLAYER_B, :walk => "trainer_PLAYER_B" }
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

    # no Prismfall running sheet yet: run in the walk sheet rather than switch to stock Red/Leaf
    alias pf_look_run_charset run_charset unless method_defined?(:pf_look_run_charset)
    def run_charset
      look = Prismfall.player_look(@id)
      return look ? (look[:run] || look[:walk]) : pf_look_run_charset
    end
  end
end
