#===============================================================================
# Prismfall Trials - 150 Talk routing: one script call per map event
#-------------------------------------------------------------------------------
# A map event only needs   Script: pf_trial_talk(:KEY)
# The first row of TALK[:KEY] whose condition is true runs its quest scene;
# if none does, the event opens its Trial board / keeper, or says its idle line.
# A quest taken from a board (flag :from_board) still plays its giver's :offer
# scene once when you next talk to the giver (Rejuvenation Help Center style).
# Rows: [quest_id, "condition", scene]   (":SELF" in the condition = that quest)
# Visibility of objects that come and go (the Nickit, lanterns, the Ralts...)
# is the map event's own "Condition:" comment (010); TRIAL_EVENTS.yaml lists both.
#===============================================================================
module Prismfall
  module Trials
    TALK = {
      #--- Ferrow's Landing (100) and interiors ------------------------------------
      :TEASEL => { :board => :ELOWEN, :rows => [
        [:EL_FIRST_LESSON, "quest_state(:SELF) == :available", :offer],
        [:EL_FIRST_LESSON, "quest_active(:SELF)", :return],
        [:EL_GLASS_FOAL, "quest_state(:SELF) == :available", :offer]] },
      :WAYSHRINE_ROPE => { :board => :ELOWEN, :rows => [] },
      :WENNA => { :rows => [
        [:EL_TART_THIEF, "quest_state(:SELF) == :available", :offer],
        [:EL_TART_THIEF, "quest_step(:SELF) == :return", :return],
        [:EL_SCARECROW, "quest_step(:SELF) == :bottle", :bottle]] },
      :TART_STALL => { :rows => [[:EL_TART_THIEF, "quest_step(:SELF) == :ask", :sighting]] },
      :NICKIT_SIGHTING => { :rows => [[:EL_TART_THIEF, "quest_step(:SELF) == :chase && chase(:SELF) >= 1 && chase(:SELF) <= 3", :sighting]] },
      :LOFT_NICKIT => { :rows => [[:EL_TART_THIEF, "quest_step(:SELF) == :loft", :loft]] },
      :DEED_WASHING => { :rows => [[:EL_FIRST_LESSON, "!deed(:fl_washing)", :deed_washing]], :idle => "The washing flaps on the line." },
      :DEED_ROPE    => { :rows => [[:EL_FIRST_LESSON, "!deed(:fl_rope)", :deed_rope]] },
      :DEED_SAILOR  => { :rows => [[:EL_FIRST_LESSON, "!deed(:fl_sailor)", :deed_sailor]] },
      :DEED_KELP    => { :rows => [[:EL_FIRST_LESSON, "!deed(:fl_kelp)", :deed_kelp]], :idle => "The kelp is drying nicely." },
      :BERTH_TIMBURR => { :rows => [
        [:EL_LAST_PLANK, "quest_state(:SELF) == :available", :berth],
        [:EL_LAST_PLANK, "quest_step(:SELF) == :finish", :finish]],
        :idle => "The Timburr hammers a plank into the berth, steps back, and stares at the sea." },
      :BOATYARD_PLANK => { :rows => [[:EL_LAST_PLANK, "quest_step(:SELF) == :planks", :plank]] },
      :DOCKMASTER => { :rows => [
        [:EL_MASTER_OF_NOTHING, "quest_state(:SELF) == :available", :offer],
        [:EL_MASTER_OF_NOTHING, "quest_step(:SELF) == :ledger", :ledger],
        [:ZE_FORM_7B, "quest_step(:SELF) == :stamps && !quest_flag(:SELF, :dock)", :stamp_dock]] },
      :DOVETAIL_NEST => { :rows => [[:EL_MASTER_OF_NOTHING, "quest_step(:SELF) == :ask", :rigging]],
                          :idle => "The Wattrel is asleep in its nest of tarred rope, waiting for a ship." },
      :LARCH => { :rows => [[:ZE_FORM_7B, "quest_step(:SELF) == :stamps && !quest_flag(:SELF, :larch)", :stamp_larch]] },
      :HESPER => { :rows => [[:ZE_FORM_7B, "quest_step(:SELF) == :warm", :warm]] },
      :KIOSK_PENNY => { :board => :ZENITH, :rows => [
        [:ZE_FORM_7B, "quest_state(:SELF) == :available", :offer],
        [:ZE_FIELD_SURVEY, "quest_active(:SELF)", :report]] },
      :CUSTOMS_OFFICER => { :rows => [[:ZE_FORM_7B, "quest_step(:SELF) == :stamps && !quest_flag(:SELF, :customs)", :stamp_customs]] },
      #--- Windfall Row (521), Hale Farmhouse (523), the Glassed Orchard (522) -------
      :COLL => { :rows => [[:EL_SCARECROW, "quest_state(:SELF) == :available", :offer]] },
      :SCARECROW => { :rows => [
        [:EL_SCARECROW, "quest_step(:SELF) == :ask", :watch],
        [:EL_SCARECROW, "quest_step(:SELF) == :water", :water],
        [:EL_SCARECROW, "quest_done(:SELF) && badges >= 2 && event_mon(:EL_SUDOWOODO) != :caught", :rematch]],
        :idle => "It's a scarecrow. Probably." },
      :ORCHARD_HOOFPRINT => { :rows => [[:EL_GLASS_FOAL, "quest_active(:SELF) && chase(:SELF) <= 2 && quest_step(:SELF) != :foal", :hoofprint]] },
      :GLASS_FOAL => { :rows => [[:EL_GLASS_FOAL, "quest_step(:SELF) == :foal", :foal]] },
      #--- The Strand Road: Lacecliff Walk (527) ----------------------------------------
      :DOBBS => { :rows => [[:EL_TIDE_POOL_FEUD, "quest_state(:SELF) == :available", :offer]],
                  :idle => "Dobbs is up to her knees in a rock pool, humming." },
      :TIDE_POOL => { :rows => [[:EL_TIDE_POOL_FEUD, "quest_active(:SELF)", :pool]] },
      #--- Saltmere (140, 143, 145, 146, 147) --------------------------------------------
      :HOLLIN => { :board => :ELOWEN, :rows => [
        [:EL_LANTERNS, "quest_state(:SELF) == :available", :offer],
        [:EL_LANTERNS, "quest_step(:SELF) == :return", :return],
        [:EL_SOUND_OF_SALTMERE, "quest_state(:SELF) == :available", :offer]] },
      :PROP_LANTERN => { :rows => [[:EL_LANTERNS, "quest_step(:SELF) == :search && !quest_flag(:SELF, :prop_room)", :prop_room]] },
      :CARAMEL_SELLER => { :rows => [
        [:EL_LANTERNS, "quest_step(:SELF) == :search && !quest_flag(:SELF, :stall)", :stall],
        [:EL_SOUND_OF_SALTMERE, "quest_step(:SELF) == :ask && night", :silence_stall]] },
      :BOAT_LANTERN => { :rows => [[:EL_LANTERNS, "quest_step(:SELF) == :search && !quest_flag(:SELF, :boat)", :boat]] },
      :ROPEWALK_LANTERN => { :rows => [[:EL_LANTERNS, "quest_step(:SELF) == :search && !quest_flag(:SELF, :ropewalk)", :ropewalk]] },
      :STAGEHAND => { :rows => [[:EL_LANTERNS, "quest_step(:SELF) == :search && !quest_flag(:SELF, :stagehand)", :stagehand]],
                      :idle => "Ottilie is running lines to an empty theatre. She waves without stopping." },
      :SILENCE_STAGE    => { :rows => [[:EL_SOUND_OF_SALTMERE, "quest_step(:SELF) == :ask", :silence_stage]] },
      :SILENCE_ROPEWALK => { :rows => [[:EL_SOUND_OF_SALTMERE, "quest_step(:SELF) == :ask", :silence_ropewalk]] },
      :BREAKWATER_END => { :rows => [[:EL_SOUND_OF_SALTMERE, "quest_step(:SELF) == :breakwater", :breakwater]],
                           :idle => "The end of the breakwater. Fog, and the sea breathing." },
      :FANE => { :rows => [[:EL_PAINT_LOFT, "quest_state(:SELF) == :available", :offer]],
                 :idle => "Marguerite Fane is painting a sky. It is going well. She would like you to stop watching." },
      :BRAKKA => { :board => :ASHKAAR, :rows => [
        [:AS_LITTLE_CRUCIBLE, "quest_state(:SELF) == :available", :offer],
        [:AS_LITTLE_CRUCIBLE, "quest_step(:SELF) == :mascot", :mascot],
        [:AS_LITTLE_CRUCIBLE, "quest_step(:SELF) == :ask", :bouts]] },
      :KIOSK_PENNY_SALTMERE => { :board => :ZENITH, :rows => [[:ZE_FIELD_SURVEY, "quest_active(:SELF)", :report]] },
      #--- The Weavers' Road and Briarwick (552, 524, 525, 120, 123) --------------------
      :ALDRETH => { :board => :ELOWEN, :rows => [
        [:EL_THREE_KNOTS, "quest_state(:SELF) == :available", :offer],
        [:EL_THREE_KNOTS, "quest_step(:SELF) == :return", :return]] },
      :SHRINE_FORD   => { :rows => [[:EL_THREE_KNOTS, "quest_active(:SELF) && !quest_flag(:SELF, :river)", :shrine_river]] },
      :SHRINE_WOOD   => { :rows => [[:EL_THREE_KNOTS, "quest_active(:SELF) && !quest_flag(:SELF, :wood)", :shrine_wood]] },
      :SHRINE_SQUARE => { :rows => [[:EL_THREE_KNOTS, "quest_active(:SELF) && !quest_flag(:SELF, :square)", :shrine_square]] },
      :SAP_TREE => { :rows => [[:EL_HORN_AND_PINCER, "badges >= 2 && !quest_done(:SELF)", :tree]] },
      :HETT => { :rows => [
        [:EL_SILKTHIEF, "quest_state(:SELF) == :available", :offer],
        [:EL_SILKTHIEF, "quest_step(:SELF) == :report", :report]] },
      :MOTH_NESTS => { :rows => [[:EL_SILKTHIEF, "quest_active(:SELF) && quest_step(:SELF) != :report", :nest]],
                       :idle => "The old moth nests hang like paper lanterns, wrapped warm in Briarwick silk." },
      #--- Frostwick (573), the Rimewood (562), Halvard's (576), Gullcry (561), Ebbmouth (160/167), the Rehearsal (568)
      :INGRITH => { :board => :ISENMAR, :rows => [[:IS_OATH_PARCEL, "quest_state(:SELF) == :available", :offer]] },
      :MAELON  => { :board => :ELOWEN,  :rows => [[:EL_REHEARSAL, "quest_state(:SELF) == :available", :offer]] },
      :BRENNA_SIGVALD => { :rows => [
        [:IS_TWO_HEARTHS, "quest_state(:SELF) == :available", :offer],
        [:IS_TWO_HEARTHS, "quest_step(:SELF) == :cook", :cook]] },
      :RIMEWOOD_HIVE => { :rows => [[:IS_TWO_HEARTHS, "quest_step(:SELF) == :ask", :hive]], :idle => "The hive hums." },
      :HALVARD => { :rows => [[:IS_TWO_HEARTHS, "quest_step(:SELF) == :ask", :smokehouse]] },
      :PARCEL_RATTLE => { :rows => [[:IS_OATH_PARCEL, "quest_step(:SELF) == :carry && !quest_flag(:SELF, :rattled)", :rattle]] },
      :EBB_MAST => { :rows => [[:EL_MASTER_OF_NOTHING, "quest_done(:SELF) && badges >= 3 && event_mon(:EL_WATTREL) != :gifted", :homecoming]],
                     :idle => "Gulls on the harbour mast. One of them crackles." },
      :ASTA => { :rows => [
        [:IS_EGG_THIEF, "quest_state(:SELF) == :available", :offer],
        [:IS_EGG_THIEF, "quest_step(:SELF) == :report", :report]] },
      :EGG_LEDGE => { :rows => [[:IS_EGG_THIEF, "quest_step(:SELF) == :ask", :ledge]] },
      :BERSI => { :board => :ISENMAR, :rows => [
        [:IS_OATH_PARCEL, "quest_active(:SELF)", :deliver],
        [:IS_SKALDS_SAGA, "quest_state(:SELF) == :available", :offer],
        [:IS_SKALDS_SAGA, "quest_step(:SELF) == :feast", :feast]] },
      :GORM => { :rows => [[:IS_SKALDS_SAGA, "quest_step(:SELF) == :ask && quest_flag(:SELF, :deed) == :bully", :gorm]],
                 :idle => "Gorm: Toll's ten. Unless you're the one who flattened me. Then it's free. Don't tell anyone." },
      :KIOSK_PENNY_EBB => { :board => :ZENITH, :rows => [
        [:ZE_LATTICE_HUM, "quest_state(:SELF) == :available", :offer],
        [:ZE_LATTICE_HUM, "quest_step(:SELF) == :choose", :choose],
        [:ZE_FIELD_SURVEY, "quest_active(:SELF)", :report]] },
      :WHEEL_UPPER => { :rows => [[:ZE_LATTICE_HUM, "quest_step(:SELF) == :ask", :wheel_upper]] },
      :WHEEL_GUILD => { :rows => [[:ZE_LATTICE_HUM, "quest_step(:SELF) == :ask", :wheel_guild]] },
      :WHEEL_QUAY  => { :rows => [[:ZE_LATTICE_HUM, "quest_step(:SELF) == :ask", :wheel_quay]] },
      :REHEARSAL_LOOP => { :rows => [[:EL_REHEARSAL, "quest_active(:SELF) && quest_step(:SELF) != :finish", :watch]],
                           :idle => "The wagon tips. The horse screams. Five seconds. Again." },
      :REHEARSAL_GIRL => { :rows => [[:EL_REHEARSAL, "quest_step(:SELF) == :finish", :finish]] }
    }

    # True if a TALK row would run a quest scene now. For existing story NPCs:
    #   if: 'pf_trial_ready?(:WENNA)'  then: [{script: 'pf_trial_talk(:WENNA)'}]  else: [their own lines]
    def self.talk_ready?(key)
      t = TALK[key.to_sym]
      return false if !t
      return t[:rows].any? do |qid, c, scene|
        next false if get(qid).nil? || get(qid)[:stub]
        (scene == :offer && active?(qid) && flag(qid, :from_board)) || cond(c, qid)
      end
    end

    def self.talk(key)
      t = TALK[key.to_sym]
      raise ArgumentError, "No TALK entry #{key.inspect}" if !t
      t[:rows].each do |qid, c, scene|
        next if get(qid).nil? || get(qid)[:stub]
        # A quest taken from a board still gets its giver's briefing once.
        briefing = (scene == :offer && active?(qid) && flag(qid, :from_board))
        next if !briefing && !cond(c, qid)
        set_flag(qid, :from_board, false) if briefing
        return Script.run_scene(qid, scene)
      end
      return board(t[:board]) if t[:board]
      pbMessage(_INTL(t[:idle])) if t[:idle]
      return false
    end
  end
end

# Event usage: Script: pf_trial_talk(:WENNA)
def pf_trial_talk(key);   return Prismfall::Trials.talk(key);        end
def pf_trial_ready?(key); return Prismfall::Trials.talk_ready?(key); end
