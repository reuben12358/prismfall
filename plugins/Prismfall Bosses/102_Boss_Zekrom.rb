#===============================================================================
# Zekrom - Zenith, Chapter 16 "Clear Air", the Cogsworth Engine core
# (story/07_ACT_IV.md). Each bar breaks a containment cable: the player is
# freeing it, not beating it. The second break wrecks the foundry
# (:FACTORY -> :SCRAPYARD). Its last bar ends with Zekrom tearing free (no faint).
#   Conditional Branch > Script: Prismfall::Bosses.wild_battle(:ZEKROM_ENGINE)
#     (result :freed -> ZEKROM_FREED story beat)
#===============================================================================
Prismfall::Bosses.register(:ZEKROM_ENGINE, {
  :species       => :ZEKROM,
  :level         => 72,
  :ability       => :TERAVOLT,
  :nature        => :ADAMANT,
  :ivs           => 31,
  # Balance 2026-11-23 (cell BZEK): typical parties won 0% (Hone Claws + +1 Attack every break). Bulk for speed,
  # and each break hardens instead of sharpening.
  :evs           => { :HP => 252, :ATTACK => 4, :SPEED => 252 },
  :moves         => [:FUSIONBOLT, :DRAGONCLAW, :CRUNCH, :HONECLAWS],
  :bars          => { :CASUAL => 2, :STANDARD => 3, :HARD => 4 },
  :stat_mults    => { :CASUAL => { :HP => 0.85, :ATTACK => 0.75 }, :STANDARD => { :ATTACK => 0.9 },
                      :HARD => { :DEFENSE => 1.15, :SPECIAL_DEFENSE => 1.15 } },
  :field         => :FACTORY,
  :catch         => false,
  :intro         => ["Zekrom strains against the golden cables of the Engine core!"],
  :break_message => "A containment cable around {1} snapped!",
  :on_break      => { :messages => ["{1} roars as the Engine's grip weakens!"], :cure_status => true,
                      :stats => { :DEFENSE => 1 } },
  :breaks        => {
    2 => { :field => :SCRAPYARD, :field_message => "The Engine core buckles! The foundry floor collapses into scrap!",
           :learn => { 0 => :BOLTSTRIKE }, :clear_hazards => true }
  },
  :ai_script     => { 1 => [:HONECLAWS] },
  :on_defeat     => [
    { :messages => ["The last cable tore loose!", "{1} broke free of the Engine core and burst through the roof!"],
      :end_battle => 1, :result => :freed }
  ]
})
