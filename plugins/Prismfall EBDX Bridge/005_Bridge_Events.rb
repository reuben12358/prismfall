#===============================================================================
# Prismfall EBDX Bridge - event registration (contract: design/SPINE.md,
# design/FIELD_API.md). Both events may fire at battle start; signature checks
# make repeated notifications for an unchanged field/stage free.
#   :prismfall_field_changed        (battle, old_id, new_id)  LOCKED
#   :prismfall_field_overlay_changed (battle, field_id, old_ids, new_ids)
# Live-testing: in battle press F9 (Debug) -> Field effects... -> Field effect.
#===============================================================================
EventHandlers.add(:prismfall_field_changed, :prismfall_ebdx_bridge,
  proc { |battle, old_id, new_id|
    PrismfallEBDX.on_field_changed(battle, old_id, new_id)
  }
)

EventHandlers.add(:prismfall_field_overlay_changed, :prismfall_ebdx_bridge,
  proc { |battle, field_id, old_ids, new_ids|
    PrismfallEBDX.on_overlay_changed(battle, field_id, old_ids, new_ids)
  }
)
