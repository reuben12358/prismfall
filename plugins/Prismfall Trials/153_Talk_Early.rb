#===============================================================================
# Prismfall Trials - 153 Talk rows for the early side content (116_Quests_Early.rb)
#-------------------------------------------------------------------------------
# Same rules as 150: a map event calls pf_trial_talk(:KEY); the first row whose
# condition holds runs its scene. Map events: design/TRIAL_EVENTS.yaml; on built
# maps they are laid by mapgen/trial_overlay.py (new events and PATCHES branches
# on existing story NPCs). Repeated objects (relays, boundary stones) erase
# themselves with self switch A after their call; the scenes count them.
#===============================================================================
Prismfall::Trials::TALK.merge!({
  #--- Ch0-1: the Dovetail deck (109), Ferrow's Landing (100), the customs hall (108) ------
  :CRATE_WOMAN => { :rows => [
    [:EL_STOWAWAYS, "quest_state(:SELF) == :available", :offer],
    [:EL_STOWAWAYS, "quest_step(:SELF) == :landed && switch(103)", :landed],
    [:EL_STOWAWAYS, "quest_step(:SELF) == :return", :return]] },
  :STOWAWAY_MICE => { :rows => [[:EL_STOWAWAYS, "quest_step(:SELF) == :find", :mice]] },
  #--- Ch2: Marram Down (528) --------------------------------------------------------------
  :SCULPTOR => { :rows => [
    [:EL_SAND_CROWN, "quest_state(:SELF) == :available", :offer],
    [:EL_SAND_CROWN, "quest_step(:SELF) == :report", :report]] },
  :SAND_CROWN => { :rows => [[:EL_SAND_CROWN, "quest_step(:SELF) == :ask", :crown]],
                   :idle => "A sand Crown as tall as you. The stone in the middle is a little chipped." },
  #--- Ch3: Cocoonfall Hollow (548); Mother Aldreth's new rows are appended below -----------
  :GLASS_COCOON => { :rows => [[:EL_MATRIARCH_HUM, "quest_active(:SELF)", :cocoon]],
                     :idle => "Glass cocoons, cold and empty. Something here used to hum." },
  #--- Ch4: the Wolfsrime (579) ----------------------------------------------------------
  :DROVER => { :rows => [
    [:EL_DROVERS_BELL, "quest_state(:SELF) == :available", :offer],
    [:EL_DROVERS_BELL, "quest_step(:SELF) == :return", :return]] },
  :WOLF_DEN => { :rows => [[:EL_DROVERS_BELL, "quest_step(:SELF) == :ask", :den]] },
  #--- Ch5: the Reedholms (580) and Ebb Hollow (588) --------------------------------------
  # The fisher beside the Veil is a story NPC (24_SCRIPT_CH5, 580 item 6): patch it with pf_trial_ready?(:VEIL_FISHER).
  :VEIL_FISHER => { :rows => [
    [:IS_EBB_HOLLOW, "quest_state(:SELF) == :available", :offer],
    [:IS_EBB_HOLLOW, "quest_step(:SELF) == :return", :return]] },
  :HOLLOW_STONE => { :rows => [[:IS_EBB_HOLLOW, "quest_step(:SELF) == :ask", :stone]] },
  :HOLLOW_CORAL => { :rows => [[:IS_EBB_HOLLOW, "quest_step(:SELF) == :coral", :coral]] },
  #--- Ch5: Lumen City, the Concourse (180) and the Spire lobby (185) ------------------------
  # Not during the Gala, the raid and the Lowlight aftermath (V125 CH5_STEP 7-12): CHAPTER_BEATS keeps that stretch clear.
  :FIZZBOLT_MACHINE => { :rows => [
    [:ZE_FIZZBOLT, "quest_state(:SELF) == :available && (var(125) < 7 || var(125) >= 13)", :offer],
    [:ZE_FIZZBOLT, "quest_active(:SELF) && (var(125) < 7 || var(125) >= 13)", :compliment]],
    :idle => "The Fizzbolt machine hums to itself. Every so often a drink rolls out, warm, for nobody in particular." },
  :HELPDESK_ROTOM => { :rows => [
    [:ZE_CUSTOMER_SUPPORT, "quest_state(:SELF) == :available && (var(125) < 7 || var(125) >= 13)", :offer],
    [:ZE_CUSTOMER_SUPPORT, "quest_step(:SELF) == :return", :return]],
    :idle => "Helpdesk Rotom: THANK YOU FOR CONTACTING MERIDIAN. YOU ARE CALLER NUMBER ONE." },
  :DESK_RECORDS    => { :rows => [[:ZE_CUSTOMER_SUPPORT, "quest_step(:SELF) == :ask", :records]],
                        :idle => "Records clerk: Records. If it happened, we have it. If we don't have it, it didn't happen." },
  :DESK_APPROVALS  => { :rows => [[:ZE_CUSTOMER_SUPPORT, "quest_step(:SELF) == :ask", :approvals]],
                        :idle => "Approvals clerk: Approved! Sorry. Reflex. What was it?" },
  :DESK_COMPLIANCE => { :rows => [[:ZE_CUSTOMER_SUPPORT, "quest_step(:SELF) == :ask", :compliance]],
                        :idle => "Compliance clerk: One window. Two windows. Nobody uses the second window." }
})

# Mother Aldreth (126) also posts the Matriarch's cocoon and Shelly's board pointer.
[[:EL_MATRIARCH_HUM, "quest_state(:SELF) == :available", :offer],
 [:EL_SHELLY, "quest_state(:SELF) == :available", :offer]].each do |row|
  rows = Prismfall::Trials::TALK[:ALDRETH][:rows]
  rows.push(row) if !rows.include?(row)
end
