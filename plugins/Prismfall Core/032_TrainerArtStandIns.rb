#===============================================================================
# Prismfall Core - 032 Trainer art stand-ins
#-------------------------------------------------------------------------------
# A trainer class added to PBS before its art exists would open its battle with no
# trainer sprite. Until Graphics/Trainers/<TYPE>.png (or Characters/trainer_<TYPE>.png)
# is installed, such a class borrows the nearest class of its own faction (a new
# Ashkaar or Isenmar unit is at least in the right uniform) or a stock Essentials
# figure of the same trade. Own art always wins: the
# table is only read when the class's own file is missing, and a stand-in whose own
# file is missing too is followed one more step (ASHKAAR_SOLDIER -> _M).
# tools/check_art_wiring.py lists what is still borrowed.
#===============================================================================
module Prismfall
  TRAINER_ART_STAND_INS = {
    # genderless base classes (trainers normally use _M / _F)
    :HOLLOW_GRUNT        => :HOLLOW_GRUNT_M,
    :MERIDIAN_AGENT      => :MERIDIAN_AGENT_M,
    :ASHKAAR_SOLDIER     => :ASHKAAR_SOLDIER_M,
    :ISENMAR_SOLDIER     => :ISENMAR_SOLDIER_M,
    # The 17 Act III-V and Grounds Ladder rows retired 2026-11-26: Gemini delivered their front strips and overworld
    # sheets (gemini_recommends/2026-11-26_claude-integration-handoff §3). Add a row here for any new artless class.
  }
end

module GameData
  class TrainerType
    class << self
      if method_defined?(:check_file) && !method_defined?(:pf_standin_check_file)
        alias_method :pf_standin_check_file, :check_file
        def check_file(tr_type, path, optional_suffix = "", suffix = "")
          ret = pf_standin_check_file(tr_type, path, optional_suffix, suffix)
          return ret if ret
          id = (self.try_get(tr_type)&.id rescue nil)
          2.times do
            id = Prismfall::TRAINER_ART_STAND_INS[id]
            break if !id
            ret = pf_standin_check_file(id, path, optional_suffix, suffix)
            return ret if ret
          end
          return nil
        end
      end
    end
  end
end
