#===============================================================================
# Prismfall Maps - 008 gym order helpers (mapgen/ruby/008_GymOrder.rb, copied by build.py)
#-------------------------------------------------------------------------------
# SPINE Revision 14 swapped Gyms 1 and 2 (Dorian/Saltmere first, Tamsin/Briarwick second). Gym maps never hard-code
# a gym number: they look their Warden up in Core's Prismfall::GYMS, so the maps stay right whatever order that
# table is in.
#   pfm_gym(:LEADER_DORIAN)        -> the gym number (1-18) of that Warden
#   pfm_gym_won?(:LEADER_TAMSIN)   -> the player holds that Warden's badge
#===============================================================================
def pfm_gym(trainer_type)
  return nil if !defined?(Prismfall::GYMS)
  g = Prismfall::GYMS.find { |h| h[:trainer_type] == trainer_type }
  return g ? g[:index] : nil
end

def pfm_gym_won?(trainer_type)
  n = pfm_gym(trainer_type)
  return false if !n || !$player
  return $player.badges[n - 1] == true
end
