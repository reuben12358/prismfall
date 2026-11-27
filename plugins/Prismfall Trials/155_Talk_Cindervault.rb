#===============================================================================
# Prismfall Trials - 155 Talk rows for Cindervault (121_Quests_Cindervault.rb)
#-------------------------------------------------------------------------------
# Same rules as 150. Map events (mapgen/trial_overlay.py, design/TRIAL_EVENTS.yaml):
#   240 Forge Terraces: "Adequate Swords Owner" (patch ADEQUATE_OWNER), "Honest Sign: Adequate Swords" (patch
#       ADEQUATE_SIGN), Kessa beside "Honest Sign: Excellent Swords" (new, EXCELLENT_SMITH), "Legate Varra Kosk"
#       (patch CRUCIBLE_LEGATE: Too Loud for the Choir, the Brazier Writ, Seven Bouts), "Forte" (patch OCTAVE_FORTE)
#   247 Hall of Oaths: "Herald Pyke" (patch HERALD_PYKE; his own lines still offer the Ashkaar board), "Oath-Scribe"
#       (patch HONEST_COURT), Tribune Halden at the Great Oath-Brazier while the Trial of Truth is open (new, HALDEN)
#   248 Dragon Roosts: Gemini's Tarn and Old Cinder call ROOST_KEEPER / OLD_CINDER (152_Talk_Megas.rb) directly.
#===============================================================================
Prismfall::Trials::TALK.merge!({
  #--- Cindervault market (240): Adequate Swords ------------------------------------------------
  :ADEQUATE_OWNER => { :rows => [
    [:AS_ADEQUATE_SWORDS, "quest_state(:SELF) == :available", :offer],
    [:AS_ADEQUATE_SWORDS, "quest_step(:SELF) == :home", :home],
    [:AS_ADEQUATE_SWORDS, "quest_done(:SELF)", :after]] },
  :ADEQUATE_SIGN => { :rows => [[:AS_ADEQUATE_SWORDS, "quest_done(:SELF)", :sign]] },
  :EXCELLENT_SMITH => { :rows => [
    [:AS_ADEQUATE_SWORDS, "quest_step(:SELF) == :test", :test],
    [:AS_ADEQUATE_SWORDS, "quest_done(:SELF)", :kessa_after]],
    :idle => "Kessa of EXCELLENT SWORDS: Excellent swords. It says so on the sign, and the sign's under oath." },
  #--- Pyre Keep, the Hall of Oaths (247) -------------------------------------------------------
  :HONEST_COURT => { :rows => [[:AS_ADEQUATE_SWORDS, "quest_step(:SELF) == :court", :court]] },
  :HERALD_PYKE => { :board => :ASHKAAR, :rows => [
    [:AS_TRIAL_OF_TRUTH, "quest_state(:SELF) == :available", :offer],
    [:AS_TRIAL_OF_TRUTH, "quest_step(:SELF) == :testify", :testify],
    [:AS_TRIAL_OF_TRUTH, "quest_step(:SELF) == :duel", :duel],
    [:AS_TRIAL_OF_TRUTH, "quest_done(:SELF) && quest_outcome(:SELF) != :silent && !quest_flag(:SELF, :told)", :after]] },
  :HALDEN => { :rows => [
    [:AS_TRIAL_OF_TRUTH, "quest_step(:SELF) == :testify", :testify],
    [:AS_TRIAL_OF_TRUTH, "quest_step(:SELF) == :duel", :duel]],
    :idle => "Tribune Halden stands at the brazier with his palm on the bronze. He doesn't look at you." }
})
# The Legate's other rite: Seven Bouts, after her Octave and Brazier rows (Forte's second and the 15-badge writ first).
if Prismfall::Trials::TALK[:CRUCIBLE_LEGATE]
  Prismfall::Trials::TALK[:CRUCIBLE_LEGATE][:rows].push(
    [:AS_SEVEN_BOUTS, "quest_state(:SELF) == :available", :offer],
    [:AS_SEVEN_BOUTS, "quest_step(:SELF) == :bouts", :again],
    [:AS_SEVEN_BOUTS, "quest_done(:SELF) && !quest_flag(:SELF, :told)", :after])
end
