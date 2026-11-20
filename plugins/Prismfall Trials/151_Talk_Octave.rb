#===============================================================================
# Prismfall Trials - 151 Talk rows for the Eevee Octave (113_Quests_Octave.rb)
#-------------------------------------------------------------------------------
# Same rules as 150: a map event calls pf_trial_talk(:KEY); the first row whose
# condition holds runs its scene. Map events: design/TRIAL_EVENTS.yaml
# ("Eevee Octave" maps). Repeated objects (notes, junctions, drifts, lamps,
# cracks) erase themselves with self switch A after their call, like the
# Ferrow's Landing planks; the scenes count them.
#===============================================================================
Prismfall::Trials::TALK.merge!({
  #--- Vesper Lindqvist: Saltmere (Ch2), Lucent (Ch13), Crownhaven (Ch20) ------------------
  :VESPER_SALTMERE => { :rows => [[:CR_OCTAVE, "quest_state(:SELF) == :available", :saltmere]] },
  :VESPER_LUCENT   => { :rows => [[:CR_OCTAVE, "!quest_done(:SELF)", :lucent]] },
  :VESPER_GARDEN   => { :rows => [
    [:CR_OCTAVE, "octave_ready && !quest_done(:SELF)", :garden],
    [:CR_OCTAVE, "quest_done(:SELF)", :after]] },
  #--- Lyra: Briarwick (120), the moss-stone in Gossamer Wood (524) ------------------------
  :OCTAVE_LYRA => { :rows => [
    [:EL_OCTAVE_MOSS, "quest_state(:SELF) == :available", :offer],
    [:EL_OCTAVE_MOSS, "quest_step(:SELF) == :duel", :duel],
    [:EL_OCTAVE_MOSS, "quest_done(:SELF)", :after]],
    :idle => "Lyra is humming to the Lantern House tree. It doesn't seem to mind." },
  :MOSS_STONE => { :rows => [[:EL_OCTAVE_MOSS, "quest_step(:SELF) == :stone", :stone]],
                   :idle => "An old grey stone, furred with moss to the top. It is very quiet here." },
  #--- Aria: Ebbmouth (160), the Mill Quay (167) -------------------------------------------
  :OCTAVE_ARIA => { :rows => [
    [:IS_OCTAVE_DROWNED_NOTE, "quest_state(:SELF) == :available", :offer],
    [:IS_OCTAVE_DROWNED_NOTE, "quest_step(:SELF) == :duel", :duel],
    [:IS_OCTAVE_DROWNED_NOTE, "quest_done(:SELF)", :after]],
    :idle => "Aria: Ear right to the water! The steps, the fish-market slip, the Mill Quay steps!" },
  :EBB_NOTE   => { :rows => [[:IS_OCTAVE_DROWNED_NOTE, "quest_step(:SELF) == :listen", :note]] },
  :MILL_WHEEL => { :rows => [[:IS_OCTAVE_DROWNED_NOTE, "quest_step(:SELF) == :wheel", :wheel]],
                   :idle => "The Mill Quay wheel turns, slow and black. The Lattice hum is quieter here." },
  #--- Cadence: the Lowlight, Lumen City (181) ----------------------------------------------
  :OCTAVE_CADENCE => { :rows => [
    [:ZE_OCTAVE_OFF_BEAT, "quest_state(:SELF) == :available", :offer],
    [:ZE_OCTAVE_OFF_BEAT, "quest_step(:SELF) == :duel", :duel],
    [:ZE_OCTAVE_OFF_BEAT, "quest_done(:SELF)", :after]],
    :idle => "Cadence drums in fours. Every fourth beat, the streetlamps flicker." },
  :LATTICE_JUNCTION => { :rows => [[:ZE_OCTAVE_OFF_BEAT, "quest_step(:SELF) == :junctions", :junction]] },
  #--- Sona: the Temple of the Noon Sun (215) -----------------------------------------------
  :OCTAVE_SONA => { :rows => [
    [:OS_OCTAVE_NOON_BELL, "quest_state(:SELF) == :available", :offer],
    [:OS_OCTAVE_NOON_BELL, "quest_step(:SELF) == :noon", :noon],
    [:OS_OCTAVE_NOON_BELL, "quest_done(:SELF)", :after]],
    :idle => "Sona: The second drift's the deep one. You were about to ask." },
  :SUN_DRIFT => { :rows => [[:OS_OCTAVE_NOON_BELL, "quest_step(:SELF) == :dig", :drift]] },
  #--- Noct: the ferry steps, Mirefen (220) -------------------------------------------------
  :FERRYMAN_MIREFEN => { :board => :NADIR, :rows => [[:NA_OCTAVE_LAMPS_OUT, "quest_state(:SELF) == :available", :offer]],
                         :idle => "Ferryman: Lamps are lit. For now." },
  :FERRY_LAMP  => { :rows => [[:NA_OCTAVE_LAMPS_OUT, "quest_step(:SELF) == :lamps", :lamp]] },
  :OCTAVE_NOCT => { :rows => [
    [:NA_OCTAVE_LAMPS_OUT, "quest_step(:SELF) == :noct", :noct],
    [:NA_OCTAVE_LAMPS_OUT, "quest_step(:SELF) == :duel", :duel],
    [:NA_OCTAVE_LAMPS_OUT, "quest_done(:SELF)", :after]] },
  #--- Forte: the Crucible, Cindervault (240) -----------------------------------------------
  :OCTAVE_FORTE => { :rows => [
    [:AS_OCTAVE_TOO_LOUD, "quest_state(:SELF) == :available", :offer],
    [:AS_OCTAVE_TOO_LOUD, "quest_step(:SELF) == :duel", :duel],
    [:AS_OCTAVE_TOO_LOUD, "quest_done(:SELF)", :after]],
    :idle => "Forte: The Legate's inside! Go on! Don't let me talk!" },
  :CRUCIBLE_LEGATE => { :board => :ASHKAAR, :rows => [[:AS_OCTAVE_TOO_LOUD, "quest_step(:SELF) == :legate", :legate]] },
  #--- Lento: the Mirror Mere (742) ---------------------------------------------------------
  :OCTAVE_LENTO => { :rows => [
    [:AN_OCTAVE_STILL_WATER, "quest_state(:SELF) == :available", :offer],
    [:AN_OCTAVE_STILL_WATER, "quest_step(:SELF) == :duel", :duel],
    [:AN_OCTAVE_STILL_WATER, "quest_done(:SELF)", :after]],
    :idle => "Lento: Backwards. Backwards. From the end to the start." },
  :MERE_CRACK => { :rows => [[:AN_OCTAVE_STILL_WATER, "quest_step(:SELF) == :cracks", :crack]] },
  #--- Carol: the Glassfall Memorial Garden, Crownhaven (489) -------------------------------
  :OCTAVE_CAROL => { :rows => [
    [:CR_OCTAVE_NINTH_VERSE, "quest_state(:SELF) == :available", :offer],          # unlock: S155 and the other seven helped
    [:CR_OCTAVE_NINTH_VERSE, "quest_state(:SELF) == :locked && switch(155)", :not_yet],
    [:CR_OCTAVE_NINTH_VERSE, "quest_step(:SELF) == :duel", :duel],
    [:CR_OCTAVE_NINTH_VERSE, "quest_done(:SELF)", :after]] }
})
