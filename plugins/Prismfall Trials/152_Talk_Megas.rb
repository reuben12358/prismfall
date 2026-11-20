#===============================================================================
# Prismfall Trials - 152 Talk rows for the Mega Evolution quests (114_Quests_Megas.rb)
#-------------------------------------------------------------------------------
# Same rules as 150: a map event calls pf_trial_talk(:KEY); the first row whose
# condition holds runs its scene. Map events: design/TRIAL_EVENTS.yaml ("Mega Evolution"). Repeated
# objects (buttons, letters, beds, cages) erase themselves with self switch A
# after their call; the scenes count them. Stones lying in the world are not
# quests: their events call pf_mega_stone(:ITEM) (plugins/Prismfall Mega).
#===============================================================================
Prismfall::Trials::TALK.merge!({
  #--- Cragholm, the Lift Galleries (363): Bastian's lamp-room, the Ring-Day (SPINE Revision 21) ----------
  :BASTIAN_LAMPROOM => { :rows => [[:OS_RING_DAY, "quest_state(:SELF) == :available", :ringday]],
                         :idle => "Bastian is cleaning a lamp he can't possibly need. He hums, flat, a note behind the tune." },
  #--- Cindervault, the Hearthguild Hall (244): Brann ------------------------------------
  :BRANN_HEARTHGUILD => { :rows => [[:AS_FORGE_REMEMBERS, "quest_state(:SELF) == :available", :spare]],
    :idle => "Brann hums at the anvil, badly, and very loudly." },
  #--- Verdance, the Heartgarden (294): Juno, after J3 --------------------------------------
  :JUNO_BRIDE_TREE => { :rows => [[:EL_BRIDE_TREE_HEART, "quest_state(:SELF) == :available", :heart]],
                        :idle => "Juno is talking to the Bride Tree. It seems to be listening." },
  #--- Thistledown Manor (546) and its attic (547) -----------------------------------------
  :ATTIC_DOLL => { :rows => [
    [:EL_DOLL_WHO_WAITED, "quest_state(:SELF) == :available", :offer],
    [:EL_DOLL_WHO_WAITED, "quest_step(:SELF) == :return", :return]],
    :idle => "A rag doll sits in the attic sun." },
  :DOLL_BUTTON => { :rows => [[:EL_DOLL_WHO_WAITED, "quest_step(:SELF) == :buttons", :button]] },
  #--- Gossamer Wood: the Woodward's Hut (526) and the Heartwood (703) ----------------------
  :WOODWARD_PINCER => { :board => :ELOWEN, :rows => [[:EL_OLD_PINCER, "quest_state(:SELF) == :available", :offer]] },
  :OLD_PINCER => { :rows => [[:EL_OLD_PINCER, "quest_step(:SELF) == :fight", :fight]],
                   :idle => "A huge Pinsir is wrapped around the sap tree. It clacks its horns at you." },
  #--- Saltmere, the Grand Stage (154): Dorian ----------------------------------------------
  :DORIAN_ENCORE => { :board => :ELOWEN, :rows => [[:EL_ENCORE, "quest_state(:SELF) == :available || quest_active(:SELF)", :offer]] },
  #--- Frostflat Causeway (560): the Matriarch (boss) ----------------------------------------
  :CAUSEWAY_MATRIARCH => { :rows => [[:IS_CAUSEWAY_MATRIARCH, "quest_state(:SELF) == :available || quest_active(:SELF)", :offer]] },
  #--- Skyreach: Gale Post Hall (325) and three doors (320, 323, 324) ------------------------
  :GALE_POSTMASTER => { :board => :ZENITH, :rows => [
    [:ZE_RETURN_TO_SENDER, "quest_state(:SELF) == :available", :offer],
    [:ZE_RETURN_TO_SENDER, "quest_step(:SELF) == :return", :return]] },
  :DEAD_LETTER_DOOR => { :rows => [[:ZE_RETURN_TO_SENDER, "quest_step(:SELF) == :letters", :letter]] },
  #--- Pyre Keep, the Dragon Roosts (248): Tarn and Old Cinder --------------------------------
  :ROOST_KEEPER => { :board => :ASHKAAR, :rows => [[:AS_OLD_CINDER, "quest_state(:SELF) == :available", :offer]] },
  :OLD_CINDER => { :rows => [[:AS_OLD_CINDER, "quest_step(:SELF) == :fight", :fight]],
                   :idle => "A scarred Charizard is curled round an empty saddle." },
  #--- Mirefen, Corvin Mott's Infirmary (223): Wenlow and the Quiet Ward ---------------------
  :WENLOW_INFIRMARY => { :board => :NADIR, :rows => [
    [:NA_BEDSIDE_MANNER, "quest_state(:SELF) == :available", :offer],
    [:NA_BEDSIDE_MANNER, "quest_step(:SELF) == :return", :return]] },
  :CORVIN_INFIRMARY => { :rows => [[:NA_BEDSIDE_MANNER, "!quest_done(:SELF)", :corvin]] },
  :WARD_BED => { :rows => [[:NA_BEDSIDE_MANNER, "quest_step(:SELF) == :beds", :bed]],
                 :idle => "Under the glass, a patient's eyes move, dreaming." },
  #--- Underveil, the Moon Market (423): Ottoline and the kennel cages -------------------------
  :OTTOLINE_MOON_MARKET => { :board => :NADIR, :rows => [
    [:NA_MOON_MARKET_DOGS, "quest_state(:SELF) == :available", :offer],
    [:NA_MOON_MARKET_DOGS, "quest_step(:SELF) == :return", :return]] },
  :KENNEL_CAGE => { :rows => [[:NA_MOON_MARKET_DOGS, "quest_step(:SELF) == :cages", :cage]] },
  #--- Ironreach, the Last Rung (260): Ottoline's pawn shelf ------------------------------------
  :OTTOLINE_LAST_RUNG => { :board => :NADIR, :rows => [
    [:NA_MEMORY_KATA, "quest_state(:SELF) == :available || quest_active(:SELF)", :offer]] },
  #--- Duneholt, Sahar's Dig Lab (209) -----------------------------------------------------------
  :SAHAR_DIGLAB => { :board => :OSSARIA, :rows => [
    [:OS_AMBER_AGAIN, "quest_state(:SELF) == :available || quest_active(:SELF)", :offer]] },
  #--- Cragholm rack (360) and the third vertebra on the Vertebrae (773) -----------------------
  :NASRIN_CRAGHOLM => { :board => :OSSARIA, :rows => [
    [:OS_TYRANT_HEART, "quest_state(:SELF) == :available", :offer],
    [:OS_TYRANT_HEART, "quest_step(:SELF) == :return", :return]] },
  :THIRD_VERTEBRA => { :rows => [[:OS_TYRANT_HEART, "quest_step(:SELF) == :ask", :dig]],
                       :idle => "A vertebra the size of a house. The rock under it is warm." },
  #--- Lucent, the Speculum (346): Lector Saffi and the third pane --------------------------------
  :SAFFI_SPECULUM => { :board => :ANTUMBRA, :rows => [
    [:AN_SMILE_BEHIND_GLASS, "quest_state(:SELF) == :available", :offer],
    [:AN_SMILE_BEHIND_GLASS, "quest_step(:SELF) == :return", :return]] },
  :THIRD_PANE => { :rows => [[:AN_SMILE_BEHIND_GLASS, "quest_step(:SELF) == :ask", :pane]],
                   :idle => "Your reflection looks back. Only one mouth." }
})
# Existing keepers get the new rows too (their map events are already placed).
Prismfall::Trials::TALK[:HESPER][:rows].push([:EL_LAMP_LENS, "quest_state(:SELF) == :available", :offer]) if Prismfall::Trials::TALK[:HESPER]
if Prismfall::Trials::TALK[:CRUCIBLE_LEGATE]
  Prismfall::Trials::TALK[:CRUCIBLE_LEGATE][:rows].push([:AS_BRAZIER_WRIT, "quest_state(:SELF) == :available || quest_active(:SELF)", :offer])
end
