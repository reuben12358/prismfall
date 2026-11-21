#===============================================================================
# Prismfall Maps - 012 Lumen City (map builder 15; mapgen/ruby/012_Lumen.rb, copied by build.py)
#-------------------------------------------------------------------------------
# pfm_lumen_box(i)             the Lowlight blackout (181): junction box i (1-4) is done; when all four are, S423 goes
#                              on and the "Blackout ends" autorun brings the lights back (V125 CH5_STEP -> 5).
#                              V321 = the boxes done (bits); S424 = the blackout is on.
# pfm_lumen_battle(t, n, v)    a story trainer battle that waits gracefully while the trainer designer adds the PBS
#                              entry (it plays as a win with a note); returns true on a win.
# pfm_lumen_tag(partner, a, b) the Gala raid's tag battle (PC + Juno vs two trainers), same graceful fallback.
# pfm_lumen_live_wire?         the vault boss's bar-break prompt chose "Grab the cracked Plate and run" (GO_LIVE_WIRE).
#===============================================================================
module PrismfallLumen
  BOXES_VAR, BOXES_DONE, BLACKOUT = 321, 423, 424
  module_function

  def box(i)
    $game_variables[BOXES_VAR] = $game_variables[BOXES_VAR].to_i | (1 << (i - 1))
    $game_switches[BOXES_DONE] = true if $game_variables[BOXES_VAR] & 15 == 15
    $game_map.need_refresh = true
  end

  def trainer?(type, name, ver = 0)
    return GameData::Trainer.exists?(type, name, ver) rescue false
  end

  def battle(type, name, ver = 0)
    if !trainer?(type, name, ver)
      pbMessage(_INTL("(The battle with {1} plays here once the trainer is in PBS.)", name))
      return true
    end
    setBattleRule("canLose") if false
    return TrainerBattle.start(type, name, ver)
  end

  def tag(partner, a, b)
    if !trainer?(*partner) || !trainer?(*a) || !trainer?(*b)
      pbMessage(_INTL("(The tag battle with Juno plays here once the Lumen trainers are in PBS.)"))
      return true
    end
    pbRegisterPartner(*partner)
    r = TrainerBattle.start(a[0], a[1], a[2], b[0], b[1], b[2])
    pbDeregisterPartner rescue nil
    return r
  end
end

def pfm_lumen_box(i);                return PrismfallLumen.box(i);                 end
def pfm_lumen_battle(t, n, v = 0);   return PrismfallLumen.battle(t, n, v);        end
def pfm_lumen_tag(partner, a, b);    return PrismfallLumen.tag(partner, a, b);     end
def pfm_lumen_live_wire?;            return (pfm_get(:live_wire) rescue false) ? true : false; end

#-------------------------------------------------------------------------------
# The Lowlight swap (story/24_SCRIPT_CH5.md; FLAGS V104 LOWLIGHT_STATE): from the Shatter (1) until the Homecoming (3)
# the Lowlight is map 608, not 181.  Walking in from the Concourse's east edge (the edge connection goes to 181) puts
# you on 608 at the same spot; 608's west landing warps back to the Concourse.
#-------------------------------------------------------------------------------
if defined?(EventHandlers)
  EventHandlers.add(:on_enter_map, :pf_lowlight_swap,
    proc { |_old_map_id|
      next if !$game_map || $game_map.map_id != 181
      st = $game_variables[104].to_i
      next if st < 1 || st >= 3
      $game_temp.player_new_map_id    = 608
      $game_temp.player_new_x         = $game_player.x
      $game_temp.player_new_y         = $game_player.y
      $game_temp.player_new_direction = $game_player.direction
      $game_temp.player_transferring  = true
    }
  )
end
