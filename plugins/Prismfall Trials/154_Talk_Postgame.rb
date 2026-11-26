#===============================================================================
# Prismfall Trials - 154 Talk rows for the post-game Registry's Tier 1 cards (115_Quests_Postgame.rb)
#-------------------------------------------------------------------------------
# Same rules as 150: a map event calls pf_trial_talk(:KEY); the first row whose condition holds runs its
# scene. Map events: design/TRIAL_EVENTS.yaml ("Post-game Registry"). Larch and the board themselves are
# pf_registry_larch / pf_registry_board (013_Trials_Registry.rb), and the T1-8 rumours are
# pf_registry_roamer(:SPECIES): none of those need a row here.
# A giver whose card was taken from the board gives the briefing (:offer) once, like every Trial.
#===============================================================================
Prismfall::Trials::TALK.merge!({
  #--- T1-1 Crownhaven Encore: the Pell Playhouse stage door (154), the Opera Hall stage -------------
  :PG_DORIAN => { :rows => [
    [:PG_MELOETTA, "quest_state(:SELF) == :available", :offer]] },
  :PG_OPERA_STAGE => { :rows => [[:PG_MELOETTA, "quest_step(:SELF) == :encore", :encore]],
                       :idle => "An empty stage, a ghost light, and one seat with a reserved card on it." },
  #--- T1-2 The Masks of Gloamwood: the Bride Tree (708) and Elowen's three border stones ------------
  :PG_JUNO_BRIDE_TREE => { :rows => [
    [:PG_OGERPON, "quest_state(:SELF) == :available", :offer],
    [:PG_OGERPON, "quest_step(:SELF) == :home", :home]] },
  :PG_STONE_NORTH => { :rows => [[:PG_OGERPON, "quest_step(:SELF) == :stones && !quest_flag(:SELF, :okidogi)", :stone_okidogi]],
                       :idle => "A border stone. Somebody stood here for a very long time." },
  :PG_STONE_EAST  => { :rows => [[:PG_OGERPON, "quest_step(:SELF) == :stones && !quest_flag(:SELF, :munkidori)", :stone_munkidori]],
                       :idle => "A border stone. Somebody stood here for a very long time." },
  :PG_STONE_SOUTH => { :rows => [[:PG_OGERPON, "quest_step(:SELF) == :stones && !quest_flag(:SELF, :fezandipiti)", :stone_fezandipiti]],
                       :idle => "A border stone. Somebody stood here for a very long time." },
  :PG_BRIDE_TREE_OGRE => { :rows => [[:PG_OGERPON, "quest_step(:SELF) == :ogre", :ogre]] },
  #--- T1-3 The Bitter Mochi Seal: the Moon Market (423), Larch (493), the Lightless Deep ------------
  :PG_MOON_MARKET_ECHO => { :rows => [
    [:PG_PECHARUNT, "quest_state(:SELF) == :available", :offer],
    [:PG_PECHARUNT, "quest_step(:SELF) == :report", :report]] },
  :PG_LARCH_TEA => { :rows => [[:PG_PECHARUNT, "quest_step(:SELF) == :tea", :tea]] },
  :PG_MOCHI_SHELL => { :rows => [[:PG_PECHARUNT, "quest_step(:SELF) == :seal", :seal]],
                       :idle => "A shell like a sugared peach, shut tight. It smells of nothing at all." },
  #--- T1-4 The Stonesleep Braille ----------------------------------------------------------------
  :PG_SAHAR_MONOLITH => { :rows => [
    [:PG_REGIS, "quest_state(:SELF) == :available", :offer],
    [:PG_REGIS, "quest_step(:SELF) == :report", :report]] },
  :PG_REGI_ROCK   => { :rows => [[:PG_REGIS, "quest_step(:SELF) == :three && !quest_flag(:SELF, :rock)", :regirock]] },
  :PG_REGI_ICE    => { :rows => [[:PG_REGIS, "quest_step(:SELF) == :three && !quest_flag(:SELF, :ice)", :regice]] },
  :PG_REGI_STEEL  => { :rows => [[:PG_REGIS, "quest_step(:SELF) == :three && !quest_flag(:SELF, :steel)", :registeel]] },
  :PG_REGI_ELEKI  => { :rows => [[:PG_REGIS, "quest_step(:SELF) == :twins && !quest_flag(:SELF, :eleki)", :regieleki]] },
  :PG_REGI_DRAGO  => { :rows => [[:PG_REGIS, "quest_step(:SELF) == :twins && !quest_flag(:SELF, :drago)", :regidrago]] },
  :PG_REGI_GIGAS  => { :rows => [[:PG_REGIS, "quest_step(:SELF) == :gigas", :regigigas]],
                       :idle => "Six sockets in the wall. Five of them want something." },
  #--- T1-5 The Three Mirror Lakes ----------------------------------------------------------------
  :PG_DASK_ILSA => { :rows => [
    [:PG_LAKES, "quest_state(:SELF) == :available", :offer],
    [:PG_LAKES, "quest_step(:SELF) == :report", :report]] },
  :PG_LAKE_UXIE    => { :rows => [[:PG_LAKES, "quest_step(:SELF) == :lakes && !quest_flag(:SELF, :uxie)", :uxie]] },
  :PG_LAKE_MESPRIT => { :rows => [[:PG_LAKES, "quest_step(:SELF) == :lakes && !quest_flag(:SELF, :mesprit)", :mesprit]] },
  :PG_LAKE_AZELF   => { :rows => [[:PG_LAKES, "quest_step(:SELF) == :lakes && !quest_flag(:SELF, :azelf)", :azelf]] },
  #--- T1-6 Project NULL, Unmasked: the Black Site (699) ------------------------------------------
  :PG_BLACK_SITE_DOOR => { :rows => [
    [:PG_TYPENULL, "quest_state(:SELF) == :available", :offer],
    [:PG_TYPENULL, "quest_step(:SELF) == :raid", :raid],
    [:PG_TYPENULL, "quest_step(:SELF) == :out", :out]],
    :idle => "A blast door with a sunburst on it. The lock wants a key you don't have." },
  :PG_NULL_CRADLE  => { :rows => [[:PG_TYPENULL, "quest_step(:SELF) == :null", :cradle]] },
  :PG_NULL_ARCHIVE => { :rows => [[:PG_TYPENULL, "quest_step(:SELF) == :genesect", :archive]] },
  #--- T1-7 The Pit-Dojo Scrolls: the Iron Pit (263) ----------------------------------------------
  :PG_KAITO_PIT => { :rows => [
    [:PG_KUBFU, "quest_state(:SELF) == :available", :offer],
    [:PG_KUBFU, "quest_step(:SELF) == :pit", :pit]] }
})
