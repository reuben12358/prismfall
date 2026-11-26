#===============================================================================
# Prismfall Cutscenes - 017 AdvancedAnimations: in-engine cutscenes on the live map
#-------------------------------------------------------------------------------
# Gemini's engine and scenes (gemini_recommends/2026-11-24_rejuv-advanced-animations-engine §6 + §12,
# 2026-11-24_rejuv-cutscenes-rethink-and-expanded-slate), modelled on Rejuvenation V14's
# Scripts/AdvancedAnimations.rb + Scripts/Camera: map actors on arbitrary-grid acting sheets with
# per-frame ticks, pixel VFX locked to map tiles, a snapshot zoom, letterbox, ramped flashes,
# 90-degree cut plates and a portrait box. No movies; everything plays on the real tilemap.
#
# Which version of each scene is installed (the newest one Gemini shipped):
#   Ch2 pageant, Ch5 Shatter DC, Ch8 caldera, Ch10 Bride Grove, Ch11 rethink, Ch16 Wenlow,
#   Ruin R7 Aurelius v2 ............ PROPOSAL.md §6
#   Ch9 unmasking v4 ............... ch9_v4_scene.rb (replaces §6's v3)
#   Ch19 WAR-1, Ch15 Glassfall, Ch21 Arceus ... wave3_ready_scenes.rb (replace §6's first versions)
#   Ch13 Glass Court, Ch17 Sun Court .......... ch13_ch17_scenes_final.rb
# §6's first Ch5 / Ch11 / Ch19 / Ch15 / Ch21 scenes and Ch9 v3 are not installed.
#
# Claude's integration changes (2026-11-25), each marked "[PF]" in the code:
#   - session: the engine remembers the player's map, tile, facing, screen tone and BGM when it starts
#     and puts them back in dispose (the scenes move $game_map / $game_player freely); followers hidden.
#   - say: waits for USE / BACK in real play (capture runs and AdvancedAnimations.auto_advance keep the
#     timed hold); long lines page at 3 rows; names come from Prismfall::Portrait; the player speaks
#     under their own name, sheet and portrait.
#   - audio: BGM / SE tags resolve through Prismfall::Cutscene.scene_bgm / scene_se (016_Movies.rb);
#     a tag with no file stays silent.
#   - photosensitive mode (Prismfall::Cutscene.photosensitive?): besides Gemini's guards on flash,
#     flash_ramp, impact_beat and shake, additive VFX are dimmed and actor colour flashes capped.
#   - transfer_map raises SceneUnavailable for a map that isn't built; captures only write inside the
#     game folder; sheets are also looked up in this plugin's own Graphics folder (the pfw_* war art);
#     §12's two engine patches (foot pads, zoom overscan clamp) are applied.
#   - Ch5: lowlight: false leaves out the Lowlight cutaway (story/24: "no streets shown"); lines as the
#     script. Ruin R7: the King is AURELIUS and speaks story/42's lines.
# Map events call pfm_cutscene(:ID) (016_Movies.rb), which checks the maps before playing.
#===============================================================================

module Prismfall
  module AdvancedAnimations
    TICK = 0.05   # Rejuvenation / Reborn standard event tick (1/20 s = 2 frames @ 40fps)
    TILE = 32
    SUB  = defined?(Game_Map::REAL_RES_X) ? Game_Map::REAL_RES_X : 128

    # [PF] a scene asked for a map that isn't built (pfm_cutscene logs it and returns false)
    class SceneUnavailable < StandardError; end

    @auto_advance = false
    class << self
      # [PF] true = say() keeps its timed hold instead of waiting for a key (harnesses, attract loops)
      attr_accessor :auto_advance

      def map_built?(map_id)
        file = format("Data/Map%03d.rxdata", map_id)
        return pbRgssExists?(file) if defined?(pbRgssExists?)
        return File.exist?(file)
      end

      # [PF] :PLAYER_A or :PLAYER_B, whoever the player chose
      def player_key
        tt = ($player.trainer_type rescue nil).to_s
        return (tt == "PLAYER_B") ? :PLAYER_B : :PLAYER_A
      end

      def player_key?(sym)
        return [:PLAYER, :PLAYER_A, :PLAYER_B].include?(sym)
      end

      # [PF] the scenes name the protagonist's sheet "PLAYER_A"; show the player's own
      def cast_sheet(name)
        return name if name != "PLAYER_A" && name != "PLAYER_B"
        return player_key.to_s
      end

      # [PF] capture frames may only be written inside the game folder
      def safe_capture_dir(dir)
        return nil if dir.nil?
        d = dir.to_s
        if d.empty? || d.start_with?("/", "\\", "~") || d =~ /\A[A-Za-z]:/ || d.split(/[\/\\]/).include?("..")
          PBDebug.log("[AdvancedAnimations] capture_dir #{d.inspect} is outside the game folder; not capturing") if defined?(PBDebug)
          return nil
        end
        return d
      end
    end

    module Ease
      module_function
      def apply(kind, t)
        t = 0.0 if t < 0.0
        t = 1.0 if t > 1.0
        case kind
        when :linear    then t
        when :in        then t * t
        when :out       then 1.0 - ((1.0 - t) * (1.0 - t))
        when :in_out    then t < 0.5 ? (2.0 * t * t) : (1.0 - ((-2.0 * t + 2.0) ** 2) / 2.0)
        when :out_cubic then 1.0 - ((1.0 - t) ** 3)
        when :in_cubic  then t * t * t
        else t
        end
      end
    end

    #===========================================================================
    # World-space Map Actor (charset walking OR arbitrary-grid ActingClip sheet)
    # Foot-anchored at bottom-center of exact map tile (tx, ty) with real Y-sort!
    #===========================================================================
    class MapActor
      attr_reader :id, :tx, :ty, :dir, :sprite
      attr_accessor :visible, :opacity, :off_x, :off_y, :mirror, :scale

      EMOTE_ROWS = {
        :exclaim => 0, :alert => 0,
        :double_exclaim => 1, :shock => 1, :horror => 1, :panic => 1,
        :question => 2, :confused => 2,
        :dots => 3, :ellipsis => 3, :silent => 3,
        :anger => 4, :angry => 4,
        :sweat => 5, :nervous => 5, :tears => 5,
        :heart => 6, :blush => 6,
        :idea => 7, :sparkle => 7,
        :music => 8, :note => 8,
        :jolt => 9, :dread => 9
      }.freeze

      def initialize(engine, id, sheet:, tx:, ty:, dir: :down, grid: [4, 4],
                     is_charset: true, z_bias: 0, scale: 1.0, folder: "Graphics/Characters/")
        @engine     = engine
        @id         = id
        @tx         = tx.to_f
        @ty         = ty.to_f
        @dir        = dir
        @folder     = folder
        @is_charset = is_charset
        @z_bias     = z_bias
        @scale      = scale.to_f
        @off_x      = 0.0
        @off_y      = 0.0
        @visible    = true
        @opacity    = 255
        @mirror     = false
        @walk_phase = 0.0
        @walking    = false
        @move_task  = nil
        @hop_task   = nil
        @tremble_task = nil
        @crouch_task  = nil
        @clip       = nil
        @emote      = nil
        @color_flash = nil
        @sprite     = Sprite.new(engine.actor_vp)
        load_sheet(sheet, grid, is_charset)
        sync_screen_pos
      end

      def load_sheet(name, grid = [4, 4], is_charset = false)
        name = Prismfall::AdvancedAnimations.cast_sheet(name)   # [PF]
        path = name.start_with?("Graphics/") ? name : (@folder + name)
        @bmp = @engine.cached_bitmap(path)
        @cols, @rows = grid
        @is_charset = is_charset
        @cw = @bmp.width / @cols
        @ch = @bmp.height / @rows
        @sprite.bitmap = @bmp
        @sprite.ox = @cw / 2
        foot_pad = if name.include?("act_ch5_mourner") then 8
                   elsif name.include?("act_ch9_mourner_dive_side") then 8
                   elsif name.include?("act_ch9_mourner_throw") then 6
                   elsif name.include?("act_ch9_trevenant") then 1
                   elsif name.include?("act_war1_primal_kyogre") then 8
                   elsif name.include?("act_war1_reshiram") then 8
                   elsif name.include?("act_ch21_arceus") then 12
                   elsif name.include?("act_ch11_anja") || name.include?("act_ch11_juno") ||
                         name.include?("act_ch5_dex") || name.include?("act_ch2_dorian") ||
                         name.include?("act_ch19_valen") || name.include?("act_ch19_kestrel") ||
                         name.include?("act_ch15_glassfall") || name.include?("act_ch21_valen") ||
                         name.include?("act_ch13_kroll") || name.include?("act_ch17_voss") then 2   # §12 patch 1
                   elsif name.include?("pfw_banner") then 2
                   else 4
                   end
        @sprite.oy = @ch - foot_pad
        if @is_charset
          set_charset_frame(@dir, 0)
        else
          set_cell(0)
        end
      end

      def set_dir(dir)
        @dir = dir
        set_charset_frame(@dir, 0) if @is_charset && !@clip
      end

      def set_charset_frame(dir, pat)
        row = { :down => 0, :left => 1, :right => 2, :up => 3 }[dir] || 0
        @sprite.src_rect.set((pat % @cols) * @cw, row * @ch, @cw, @ch)
      end

      def set_cell(cell)
        col = cell % @cols
        row = (cell / @cols) % @rows
        @sprite.src_rect.set(col * @cw, row * @ch, @cw, @ch)
      end

      # Instant swap to a 4-pose B2W2 acting strip (pose_JUNO.png, pose_PLAYER_A.png)
      def set_pose(sheet, pose_idx)
        @clip = nil
        @walking = false
        load_sheet(sheet, [4, 1], false)
        set_cell(pose_idx.to_i)
      end

      # Restore standard 4x4 walking charset seamlessly at identical foot baseline
      def restore_charset(sheet, dir: nil)
        @clip = nil
        @dir = dir if dir
        load_sheet(sheet, [4, 4], true)
      end

      def move_to(tx2, ty2, duration:, walk: true, dir: nil, ease: :linear, arc_h: 0.0)
        dx = tx2 - @tx
        dy = ty2 - @ty
        if dir
          @dir = dir
        elsif dx.abs > dy.abs
          @dir = dx >= 0 ? :right : :left
        elsif dy.abs > 0.01
          @dir = dy >= 0 ? :down : :up
        end
        @walking = walk
        @move_task = {
          :x0 => @tx, :y0 => @ty, :x1 => tx2.to_f, :y1 => ty2.to_f,
          :t => 0.0, :dur => [duration.to_f, 0.001].max, :ease => ease, :arc_h => arc_h.to_f
        }
      end

      def hop(height: 14, duration: 0.28)
        @hop_task = { :h => height.to_f, :t => 0.0, :dur => [duration.to_f, 0.001].max }
      end

      def tremble(duration: 0.65, amp: 2.0, freq: 44.0)
        @tremble_task = { :t => 0.0, :dur => [duration.to_f, 0.01].max, :amp => amp.to_f, :freq => freq.to_f }
      end

      def crouch_to(target_off_y, duration: 0.25)
        @crouch_task = { :y0 => @off_y.to_f, :y1 => target_off_y.to_f, :t => 0.0, :dur => [duration.to_f, 0.01].max }
      end

      # Rejuvenation V14 AdvancedAnimations variable-tick frameData playback!
      def play_clip(sheet:, grid: [4, 4], frames: nil, ticks: nil, holds: nil,
                    se: {}, cry: {}, shake: {}, flash: {}, hitstop: {}, on_frame: {},
                    loops: 1, stay: true)
        load_sheet(sheet, grid, false)
        list = (frames || (0...(grid[0] * grid[1]))).to_a
        if holds
          h_arr = Array(holds).map(&:to_f)
        elsif ticks
          h_arr = Array(ticks).map { |tk| tk.to_f * TICK }
        else
          h_arr = [0.10]
        end
        dur_list = list.each_index.map { |i| h_arr[[i, h_arr.length - 1].min] }
        @clip = {
          :frames => list, :holds => dur_list, :idx => -1, :t => 0.0,
          :loop => 0, :loops => loops, :stay => stay,
          :se => se || {}, :cry => cry || {}, :shake => shake || {},
          :flash => flash || {}, :hitstop => hitstop || {}, :on_frame => on_frame || {},
          :done => false
        }
        advance_clip_to(0)
      end

      def clip_done?; !@clip || @clip[:done]; end
      def moving?; !@move_task.nil?; end

      def show_emote(kind = :exclaim, duration: 0.65)
        dispose_emote
        sym = kind.to_sym
        sp = Sprite.new(@engine.vfx_vp)
        sp.z = 950
        sheet_path = "Graphics/Animations/pf_emote_balloons.png"
        if File.exist?(sheet_path)
          bmp = @engine.cached_bitmap(sheet_path)
          row = EMOTE_ROWS[sym] || 0
          sp.bitmap = bmp
          sp.src_rect.set(0, row * 32, 32, 32)
          sp.ox = 16
          sp.oy = 32
          @emote = { :sp => sp, :t => 0.0, :dur => duration.to_f, :sheet => true, :row => row, :kind => sym, :owned_bmp => false }
        else
          bmp = Bitmap.new(24, 28)
          bg = Color.new(255, 255, 255)
          ol = Color.new(24, 24, 32)
          ac = (sym == :shock || sym == :double_exclaim) ? Color.new(236, 48, 64) : Color.new(236, 64, 56)
          bmp.fill_rect(2, 2, 20, 18, ol)
          bmp.fill_rect(4, 4, 16, 14, bg)
          bmp.fill_rect(8, 20, 8, 4, ol)
          bmp.fill_rect(10, 18, 4, 4, bg)
          bmp.fill_rect(10, 24, 4, 2, ol)
          bmp.fill_rect(10, 6, 4, 6, ac)
          bmp.fill_rect(10, 14, 4, 2, ac)
          sp.bitmap = bmp
          sp.ox = 12
          sp.oy = 28
          @emote = { :sp => sp, :t => 0.0, :dur => duration.to_f, :sheet => false, :owned_bmp => true }
        end
        sx, sy = screen_pos
        sp.x = sx.round
        sp.y = [(sy - (44.0 * @scale)).round, 66].max
      end

      def dispose_emote
        return if !@emote
        sp = @emote[:sp]
        if sp && !sp.disposed?
          sp.bitmap.dispose if @emote[:owned_bmp] && sp.bitmap && !sp.bitmap.disposed?
          sp.dispose
        end
        @emote = nil
      end

      def screen_pos
        sx, sy = @engine.tile_to_screen(@tx, @ty)
        hop_y = 0.0
        if @hop_task
          u = @hop_task[:t] / @hop_task[:dur]
          hop_y = -Math.sin(u * Math::PI) * @hop_task[:h]
        end
        arc_y = 0.0
        if @move_task && @move_task[:arc_h] > 0.0
          u = @move_task[:t] / @move_task[:dur]
          arc_y = -Math.sin(u * Math::PI) * @move_task[:arc_h]
        end
        tremble_x = 0.0
        if @tremble_task
          raw = Math.sin(@tremble_task[:t] * @tremble_task[:freq]) * @tremble_task[:amp]
          tremble_x = (raw / 2.0).round * 2.0
        end
        return sx + @off_x + tremble_x, sy + @off_y + hop_y + arc_y
      end

      def update(dt)
        if @move_task
          @move_task[:t] += dt
          u = [@move_task[:t] / @move_task[:dur], 1.0].min
          k = Ease.apply(@move_task[:ease], u)
          @tx = @move_task[:x0] + (@move_task[:x1] - @move_task[:x0]) * k
          @ty = @move_task[:y0] + (@move_task[:y1] - @move_task[:y0]) * k
          if @walking && @is_charset && !@clip
            @walk_phase += dt * 7.5
            set_charset_frame(@dir, @walk_phase.to_i % @cols)
          end
          if u >= 1.0
            @tx = @move_task[:x1]
            @ty = @move_task[:y1]
            @move_task = nil
            @walking = false
            set_charset_frame(@dir, 0) if @is_charset && !@clip
          end
        end

        if @hop_task
          @hop_task[:t] += dt
          @hop_task = nil if @hop_task[:t] >= @hop_task[:dur]
        end

        if @tremble_task
          @tremble_task[:t] += dt
          @tremble_task = nil if @tremble_task[:t] >= @tremble_task[:dur]
        end

        if @crouch_task
          @crouch_task[:t] += dt
          u = [@crouch_task[:t] / @crouch_task[:dur], 1.0].min
          @off_y = @crouch_task[:y0] + (@crouch_task[:y1] - @crouch_task[:y0]) * Ease.apply(:out, u)
          @crouch_task = nil if u >= 1.0
        end

        if @clip && !@clip[:done]
          @clip[:t] += dt
          cur_h = @clip[:holds][@clip[:idx]]
          while @clip[:t] >= cur_h && !@clip[:done]
            @clip[:t] -= cur_h
            nxt = @clip[:idx] + 1
            if nxt >= @clip[:frames].length
              @clip[:loop] += 1
              if @clip[:loops] == :forever || @clip[:loop] < @clip[:loops]
                advance_clip_to(0)
                cur_h = @clip[:holds][0]
              else
                @clip[:done] = true
                @clip = nil if !@clip[:stay]
                break
              end
            else
              advance_clip_to(nxt)
              cur_h = @clip[:holds][nxt]
            end
          end
        end

        if @color_flash
          @color_flash[:t] += dt
          if @color_flash[:t] >= @color_flash[:dur]
            @sprite.color.set(0, 0, 0, 0)
            @color_flash = nil
          else
            u = 1.0 - (@color_flash[:t] / @color_flash[:dur])
            c = @color_flash[:col]
            @sprite.color.set(c[0], c[1], c[2], (c[3] * u).round)
          end
        end

        sync_screen_pos

        if @emote
          @emote[:t] += dt
          if @emote[:t] >= @emote[:dur]
            dispose_emote
          else
            if @emote[:sheet]
              t_e = @emote[:t]
              col = if @emote[:kind] == :dots || @emote[:kind] == :ellipsis || @emote[:kind] == :silent
                      step = [@emote[:dur] * 0.22, 0.14].min
                      [(t_e / step).to_i, 3].min
                    else
                      t_e < 0.06 ? 0 : (t_e < 0.14 ? 1 : (t_e < 0.28 ? 2 : 3))
                    end
              @emote[:sp].src_rect.set(col * 32, @emote[:row] * 32, 32, 32)
            end
            sx, sy = screen_pos
            pop = @emote[:t] < 0.08 ? ((1.0 - @emote[:t] / 0.08) * 6.0) : 0.0
            @emote[:sp].x = sx.round
            @emote[:sp].y = [(sy - (44.0 * @scale) + pop).round, 66].max
          end
        end
      end

      def flash_color(r, g, b, a = 180, duration: 0.16)
        a = [a, 70].min if @engine.photosensitive?   # [PF]
        @color_flash = { :col => [r, g, b, a], :t => 0.0, :dur => [duration.to_f, 0.01].max }
        @sprite.color.set(r, g, b, a)
      end

      def sync_screen_pos
        sx, sy = screen_pos
        @sprite.x = sx.round
        @sprite.y = sy.round
        @sprite.z = sy.round + @z_bias
        @sprite.visible = @visible
        @sprite.opacity = @opacity.round
        @sprite.mirror  = @mirror
        @sprite.zoom_x  = @scale
        @sprite.zoom_y  = @scale
      end

      def dispose
        dispose_emote
        @sprite.dispose if @sprite && !@sprite.disposed?
      end

      private

      def advance_clip_to(i)
        @clip[:idx] = i
        cell = @clip[:frames][i]
        set_cell(cell)
        @engine.play_se(@clip[:se][i]) if @clip[:se][i]
        @engine.play_cry(@clip[:cry][i]) if @clip[:cry][i]
        if (sh = @clip[:shake][i])
          @engine.shake(power: sh[0], duration: sh[1] || 0.25)
        end
        if (fl = @clip[:flash][i])
          @engine.flash(color: fl[0], power: fl[1] || 180, duration: fl[2] || 0.16)
        end
        if (hs = @clip[:hitstop][i])
          @engine.trigger_hitstop(hs)
        end
        @clip[:on_frame][i].call(@engine, self, i) if @clip[:on_frame][i]
      end
    end

    #===========================================================================
    # World-space Crisp Pixel VFX Sprite (locked to live map tile coordinates!)
    #===========================================================================
    class MapVfx
      attr_reader :id, :done

      def initialize(engine, id, sheet:, tx:, ty:, grid: [4, 1], frames: nil,
                     ticks: nil, holds: nil, hold: 0.06, blend: :add,
                     scale: 1.0, grow: nil, loops: 1, stay: 0.0, fade: 0.0,
                     move_to: nil, arc_h: 0.0, drift: nil, gravity: 0.0, spin: 0.0,
                     offset: [0, 0], z_layer: :above, opacity: 255, untoned: nil,
                     origin: :center, mirror: false)
        @engine  = engine
        @id      = id
        @tx      = tx.to_f
        @ty      = ty.to_f
        @tx0     = @tx
        @ty0     = @ty
        @cols, @rows = grid
        @frames  = (frames || (0...(@cols * @rows))).to_a
        if holds
          h_arr = Array(holds).map(&:to_f)
        elsif ticks
          h_arr = Array(ticks).map { |tk| tk.to_f * TICK }
        else
          h_arr = [hold.to_f]
        end
        @holds   = @frames.each_index.map { |i| h_arr[[i, h_arr.length - 1].min] }
        @total   = [@holds.sum, 0.001].max
        @loops   = loops
        @stay    = stay
        @fade    = fade.to_f
        @scale   = scale.to_f
        @scale_x = nil
        @scale_y = nil
        @grow    = grow
        @move_to = move_to   # [tx2, ty2, dur]
        @arc_h   = arc_h.to_f
        @drift   = drift     # [vx_px, vy_px]
        @gravity = gravity.to_f
        @spin    = spin.to_f
        @offset  = offset
        @z_layer = z_layer
        @opacity = opacity.to_f
        @opacity *= 0.5 if blend == :add && engine.photosensitive?   # [PF] dim strobing additive sheets
        @origin_mode = origin
        @t       = 0.0
        @done    = false

        use_vfx_vp = if z_layer == :floor
                       false
                     else
                       untoned.nil? ? (blend == :add) : untoned
                     end
        vp = use_vfx_vp ? engine.vfx_vp : engine.actor_vp
        path = sheet.start_with?("Graphics/") ? sheet : ("Graphics/Animations/" + sheet)
        @bmp = engine.cached_bitmap(path)
        @cw = @bmp.width / @cols
        @ch = @bmp.height / @rows
        @sprite = Sprite.new(vp)
        @sprite.bitmap = @bmp
        case origin
        when :foot
          @sprite.ox = @cw / 2
          @sprite.oy = @ch - 8
        when :left
          @sprite.ox = 0
          @sprite.oy = @ch / 2
        when :right
          @sprite.ox = @cw
          @sprite.oy = @ch / 2
        else
          @sprite.ox = @cw / 2
          @sprite.oy = @ch / 2
        end
        @sprite.blend_type = { :add => 1, :sub => 2, :normal => 0 }[blend] || 0
        @sprite.mirror = mirror
        update(0.0)
      end

      def stop!; @done = true; end

      def set_tile(tx, ty)
        @tx = tx.to_f
        @ty = ty.to_f
      end

      def set_scale(sx, sy = nil)
        @scale_x = sx.to_f
        @scale_y = (sy || sx).to_f
      end

      def update(dt)
        return true if @done
        @t += dt
        life = (@loops == :forever || @stay == :forever) ? nil : (@total * @loops) + @stay.to_f
        if life && @t >= life
          @done = true
          return true
        end

        # Frame selection
        if @loops != :forever && @t >= @total * @loops
          i = @frames.length - 1
        else
          tm = @t % @total
          i = 0
          acc = 0.0
          while i < @frames.length - 1 && tm >= (acc += @holds[i])
            i += 1
          end
        end
        cell = @frames[i]
        @sprite.src_rect.set((cell % @cols) * @cw, (cell / @cols) * @ch, @cw, @ch)

        # Tile movement / parabolic arc
        arc_y = 0.0
        if @move_to
          u = [@t / [@move_to[2].to_f, 0.001].max, 1.0].min
          @tx = @tx0 + (@move_to[0] - @tx0) * u
          @ty = @ty0 + (@move_to[1] - @ty0) * u
          arc_y = -Math.sin(u * Math::PI) * @arc_h if @arc_h > 0.0
        end

        sx, sy = @engine.tile_to_screen(@tx, @ty)
        # tile_to_screen returns foot anchor; center/left/right anchored VFX sit at tile center (sy - 16)
        base_y = (@origin_mode == :foot) ? sy : (sy - 16)
        px = sx + @offset[0]
        py = base_y + @offset[1] + arc_y
        if @drift
          px += @drift[0] * @t
          py += (@drift[1] * @t) + (0.5 * @gravity * @t * @t)
        end

        @sprite.x = px.round
        @sprite.y = py.round
        @sprite.z = case @z_layer
                    when :floor then 5
                    when :mid   then sy.round + 2
                    else             700 + sy.round / 4
                    end

        sc = @scale
        if @grow
          u = [@t / [@grow[2].to_f, 0.001].max, 1.0].min
          sc *= @grow[0] + (@grow[1] - @grow[0]) * Ease.apply(:out, u)
        end
        @sprite.zoom_x = @scale_x ? @scale_x : sc
        @sprite.zoom_y = @scale_y ? @scale_y : sc
        @sprite.angle  = @spin * @t

        op = @opacity
        if @fade > 0.0 && life && (life - @t) < @fade
          op *= [(life - @t) / @fade, 0.0].max
        end
        @sprite.opacity = op.round
        return false
      end

      def dispose
        @sprite.dispose if @sprite && !@sprite.disposed?
      end
    end

    #===========================================================================
    # Crisp In-Engine Portrait Dialogue Overlay (Desolation/Rejuv FaceWindowVX)
    # Keeps live map, lighting, roots, smoke, and camera running underneath!
    #===========================================================================
    class PortraitBox
      MAX_LINES = 3            # [PF] rows that fit the box; the rest is handed back as overflow
      attr_reader :overflow

      # [PF] the name Prismfall's own dialogue shows for this speaker
      def self.display_name(sym)
        return "" if sym.nil?
        if defined?(Prismfall::Portrait) && Prismfall::Portrait.respond_to?(:display_name)
          n = (Prismfall::Portrait.display_name(sym) rescue nil)
          return n.to_s if n && !n.to_s.empty?
        end
        return sym.to_s.capitalize
      end

      def initialize(ui_vp, speaker_sym, expression, text, engine, name: nil)
        @engine = engine
        @vp = ui_vp
        @sprites = []
        @text = text.to_s
        @name = (name || PortraitBox.display_name(speaker_sym)).to_s
        @chars_shown = 0.0
        @done_typing = false

        box_y = Graphics.height - 98
        box_h = 86

        # 1. Optional Portrait Frame (omitted cleanly for disembodied/plain speakers like Radio or Lieutenant)
        p_bmp = speaker_sym ? load_portrait(speaker_sym, expression) : nil
        if p_bmp
          face_x = 12
          face_y = box_y - 18
          @face_bg = Sprite.new(@vp)
          @face_bg.z = 9500
          fb = Bitmap.new(104, 104)
          fb.fill_rect(0, 0, 104, 104, Color.new(18, 22, 34, 240))
          fb.fill_rect(2, 2, 100, 100, Color.new(210, 218, 236, 255))
          fb.fill_rect(4, 4, 96, 96, Color.new(26, 30, 44, 255))
          @face_bg.bitmap = fb
          @face_bg.x = face_x
          @face_bg.y = face_y
          @sprites << @face_bg

          @face_sp = Sprite.new(@vp)
          @face_sp.bitmap = p_bmp
          @face_sp.z = 9505
          @face_sp.x = face_x + 4 + (96 - p_bmp.width) / 2
          @face_sp.y = face_y + 4 + (96 - p_bmp.height) / 2
          @sprites << @face_sp
        end

        # 2. Message Frame (clean dark-slate Rejuv/Desolation style with crisp border)
        msg_x = p_bmp ? 122 : 12
        msg_w = Graphics.width - msg_x - 12
        @box = Sprite.new(@vp)
        @box.z = 9500
        bb = Bitmap.new(msg_w, box_h)
        bb.fill_rect(0, 0, msg_w, box_h, Color.new(16, 20, 30, 238))
        bb.fill_rect(2, 2, msg_w - 4, box_h - 4, Color.new(208, 216, 234, 255))
        bb.fill_rect(4, 4, msg_w - 8, box_h - 8, Color.new(22, 26, 38, 244))
        @box.bitmap = bb
        @box.x = msg_x
        @box.y = box_y
        @sprites << @box

        # 3. Speaker Nameplate Tab (auto-sized for sovereign titles like "Gilded King Aurelius")
        if !@name.empty?
          @name_sp = Sprite.new(@vp)
          @name_sp.z = 9510
          nw = @name.length > 18 ? 248 : (@name.length > 14 ? 214 : (@name.length > 10 ? 184 : 136))
          nb = Bitmap.new(nw, 28)
          nb.fill_rect(0, 0, nw, 28, Color.new(16, 20, 30, 248))
          nb.fill_rect(2, 2, nw - 4, 24, Color.new(208, 216, 234, 255))
          nb.fill_rect(4, 4, nw - 8, 20, Color.new(34, 40, 58, 255))
          set_font(nb, 18, true)
          nb.font.color = Color.new(255, 236, 176)
          nb.draw_text(8, 2, nw - 16, 24, @name, 0)
          @name_sp.bitmap = nb
          @name_sp.x = msg_x + 6
          @name_sp.y = box_y - 22
          @sprites << @name_sp
        end

        # 4. Crisp Text Bitmap
        @txt_sp = Sprite.new(@vp)
        @txt_sp.z = 9515
        @txt_bmp = Bitmap.new(msg_w - 22, box_h - 14)
        set_font(@txt_bmp, 20, false)
        @txt_sp.bitmap = @txt_bmp
        @txt_sp.x = msg_x + 12
        @txt_sp.y = box_y + 10
        @sprites << @txt_sp

        @wrapped = wrap_lines(@text, @txt_bmp, msg_w - 26)
        @overflow = (@wrapped.length > MAX_LINES) ? @wrapped[MAX_LINES..-1].join(" ") : nil   # [PF]
        @wrapped = @wrapped[0, MAX_LINES]
        @total_chars = @wrapped.join.length
        @last_drawn = -1

        # [PF] "press to go on" arrow, shown while say() waits for a key
        @prompt_sp = Sprite.new(@vp)
        @prompt_sp.z = 9520
        pb = Bitmap.new(12, 6)
        6.times { |r| pb.fill_rect(r, r, 12 - (r * 2), 1, Color.new(244, 248, 255)) }
        @prompt_sp.bitmap = pb
        @prompt_sp.x = msg_x + msg_w - 24
        @prompt_sp.y = box_y + box_h - 16
        @prompt_sp.visible = false
        @prompt = false
        @prompt_t = 0.0
        @sprites << @prompt_sp
      end

      # [PF] show the whole line now (a key press while it types)
      def finish!
        @chars_shown = @total_chars.to_f
      end

      def prompt=(on)
        @prompt = on
        @prompt_t = 0.0
        @prompt_sp.visible = on if @prompt_sp && !@prompt_sp.disposed?
      end

      def load_portrait(sym, expr)
        return nil if sym.nil?
        sym = Prismfall::AdvancedAnimations.player_key if Prismfall::AdvancedAnimations.player_key?(sym)   # [PF]
        base = "Graphics/Portraits/#{sym.to_s.upcase}"
        ["#{base}_#{expr}.png", "#{base}.png"].each do |p|
          return Bitmap.new(p) if File.exist?(p)
        end
        return nil
      end

      def set_font(bmp, size, bold)
        bmp.font.name = ["Power Clear", "Liberation Sans", "DejaVu Sans"]
        bmp.font.size = size
        bmp.font.bold = bold
      end

      def wrap_lines(str, bmp, max_w)
        lines = []
        cur = ""
        str.split(" ").each do |w|
          cand = cur.empty? ? w : "#{cur} #{w}"
          if bmp.text_size(cand).width > max_w && !cur.empty?
            lines << cur
            cur = w
          else
            cur = cand
          end
        end
        lines << cur if !cur.empty?
        lines
      end

      def update(dt)
        if @prompt && @prompt_sp && !@prompt_sp.disposed?
          @prompt_t += dt
          @prompt_sp.visible = ((@prompt_t * 2.0).to_i.even?)
        end
        @chars_shown = [@chars_shown + dt * 44.0, @total_chars.to_f].min
        n = @chars_shown.to_i
        @done_typing = (n >= @total_chars)
        return if n == @last_drawn
        @last_drawn = n
        @txt_bmp.clear
        rem = n
        @wrapped.each_with_index do |line, li|
          break if rem <= 0
          sub = line[0, [rem, line.length].min]
          rem -= line.length
          # Crisp 1px shadow + white text
          @txt_bmp.font.color = Color.new(10, 12, 18)
          @txt_bmp.draw_text(1, li * 23 + 1, @txt_bmp.width, 26, sub, 0)
          @txt_bmp.font.color = Color.new(244, 248, 255)
          @txt_bmp.draw_text(0, li * 23, @txt_bmp.width, 26, sub, 0)
        end
      end

      def done_typing?; @done_typing; end

      def dispose
        @sprites.each do |s|
          next if !s || s.disposed?
          s.bitmap.dispose if s.bitmap && !s.bitmap.disposed?
          s.dispose
        end
        @sprites.clear
      end
    end

    #===========================================================================
    # Master Rejuvenation V14 Live-Map Choreography Engine
    #===========================================================================
    class Engine
      attr_reader :actor_vp, :vfx_vp, :ui_vp, :time, :cues, :frames_captured

      def initialize(capture_dir: nil, capture_fps: 30)
        capture_dir  = Prismfall::AdvancedAnimations.safe_capture_dir(capture_dir)   # [PF]
        @capture_dir = capture_dir
        @session     = snapshot_session                                               # [PF]
        @capture_fps = capture_fps
        @fixed_dt    = capture_dir ? (1.0 / capture_fps.to_f) : nil
        @frames_captured = 0
        @time        = 0.0
        @cues        = []
        @bmp_cache   = {}
        @actors      = {}
        @vfxs        = []

        # 4-viewport layered pipeline!
        @actor_vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @actor_vp.z = 350

        # Optional 90-degree side-view cinematic backdrop in @actor_vp (z=1 below all actors!)
        @backdrop_sp = Sprite.new(@actor_vp)
        @backdrop_sp.z = 1
        @backdrop_sp.visible = false

        @vfx_vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @vfx_vp.z = 420

        @zoom_vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @zoom_vp.z = 89_000
        @zoom_sp = Sprite.new(@zoom_vp)
        @zoom_sp.visible = false

        @ui_vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @ui_vp.z = 90_000

        # Cinema widescreen bars
        @bar_h = 0.0
        @bar_task = nil
        @bar_top = Sprite.new(@ui_vp)
        @bar_top.bitmap = Bitmap.new(Graphics.width, 4)
        @bar_top.bitmap.fill_rect(0, 0, Graphics.width, 4, Color.new(0, 0, 0))
        @bar_top.z = 9100
        @bar_top.visible = false

        @bar_bot = Sprite.new(@ui_vp)
        @bar_bot.bitmap = @bar_top.bitmap
        @bar_bot.z = 9100
        @bar_bot.visible = false

        # Screen flash / impact silhouette overlay
        @flash_sp = Sprite.new(@ui_vp)
        @flash_sp.bitmap = Bitmap.new(Graphics.width, Graphics.height)
        @flash_sp.z = 9200
        @flash_sp.opacity = 0
        @flash_task = nil

        # Red emergency vignette / edge glow sprite
        @vig_sp = Sprite.new(@ui_vp)
        @vig_sp.bitmap = Bitmap.new(Graphics.width, Graphics.height)
        @vig_sp.z = 9050
        @vig_sp.opacity = 0
        @vig_pulse = nil

        # Camera state (pbZoomMap + smooth tile scroll + shake)
        @zoom       = 1.0
        @zoom_focus = nil   # :player, actor_id, or [tx, ty]
        @zoom_task  = nil
        @cam_tx     = nil
        @cam_ty     = nil
        @cam_task   = nil
        @shake_task = nil
        @shake_x    = 0.0
        @shake_y    = 0.0
        @tone       = [0.0, 0.0, 0.0, 0.0]
        @tone_task  = nil
        @hitstop    = 0.0
        @dialogue   = nil
        @last_tick  = System.uptime
      end

      def photosensitive?
        Prismfall::Cutscene.photosensitive? rescue false
      end

      def cached_bitmap(path)
        p = path.end_with?(".png") ? path : "#{path}.png"
        bmp = @bmp_cache[p]
        return bmp if bmp && !bmp.disposed?
        file = p
        overlay = "Plugins/Prismfall Cutscenes/" + p          # [PF] the plugin's own art (the pfw_* war sheets)
        file = overlay if !File.exist?(p) && File.exist?(overlay)
        bmp = Bitmap.new(file)
        @bmp_cache[p] = bmp
        bmp
      end

      def log_cue(kind, detail = {})
        @cues << { "t" => @time.round(4), "kind" => kind.to_s }.merge(detail)
      end

      #-------------------------------------------------------------------------
      # Audio Cues (played live in-engine AND logged frame-exact for video mux!)
      #-------------------------------------------------------------------------
      def play_bgm(name, volume: 85, tag: nil)
        log_cue("bgm", "name" => name.to_s, "volume" => volume, "tag" => (tag || name).to_s)
        file = scene_audio(:scene_bgm, (tag || name).to_s, name.to_s)   # [PF] tag -> a file that exists, or nil
        pbBGMPlay(file, volume) if file
      rescue StandardError
        nil
      end

      def bgm_cut
        log_cue("bgm_cut")
        Audio.bgm_stop rescue nil
      end

      def bgm_fade(sec = 0.8)
        log_cue("bgm_fade", "sec" => sec)
        Audio.bgm_fade((sec * 1000).round) rescue nil
      end

      def play_se(name, volume: 90, pitch: 100)
        log_cue("se", "name" => name.to_s, "volume" => volume, "pitch" => pitch)
        file = scene_audio(:scene_se, name.to_s, name.to_s)             # [PF]
        pbSEPlay(file, volume, pitch) if file
      rescue StandardError
        nil
      end

      # [PF] the Cutscenes plugin's tag tables (016_Movies.rb); without them the name is used as given
      def scene_audio(kind, tag, name)
        return name if !defined?(Prismfall::Cutscene) || !Prismfall::Cutscene.respond_to?(kind)
        return Prismfall::Cutscene.send(kind, tag)
      end

      def play_cry(species, volume: 95)
        log_cue("cry", "species" => species.to_s, "volume" => volume)
        GameData::Species.play_cry_from_species(species, 0, volume) rescue (pbSEPlay("Cries/#{species}", volume) rescue nil)
      end

      #-------------------------------------------------------------------------
      # Map & Camera Controls (pbCameraScrollTo, pbZoomMap, tone, shake, bars)
      #-------------------------------------------------------------------------
      def tile_to_screen(tx, ty)
        sx = ((tx * SUB - $game_map.display_x + 3) / 4.0) + 16.0
        sy = ((ty * SUB - $game_map.display_y + 3) / 4.0) + 32.0
        return sx, sy
      end

      def screen_to_tile(sx, sy)
        tx = (((sx.to_f - 16.0) * 4.0) + $game_map.display_x - 3.0) / SUB.to_f
        ty = (((sy.to_f - 32.0) * 4.0) + $game_map.display_y - 3.0) / SUB.to_f
        return tx, ty
      end

      def set_backdrop(name, z: 1)
        path = name.start_with?("Graphics/") ? name : ("Graphics/Animations/" + name)
        @backdrop_sp.bitmap = cached_bitmap(path)
        @backdrop_sp.x = 0
        @backdrop_sp.y = 0
        @backdrop_sp.z = z
        @backdrop_sp.visible = true
      end

      def clear_backdrop
        @backdrop_sp.visible = false
        @backdrop_sp.bitmap = nil
      end

      def set_camera_tile(tx, ty)
        @cam_tx = tx.to_f
        @cam_ty = ty.to_f
        apply_camera_display
      end

      def pan_camera_to(tx, ty, duration: 0.6, ease: :in_out)
        @cam_tx ||= (($game_map.display_x / 4.0) + Graphics.width / 2.0 - 16.0) / 32.0
        @cam_ty ||= (($game_map.display_y / 4.0) + Graphics.height / 2.0 - 16.0) / 32.0
        @cam_task = {
          :x0 => @cam_tx, :y0 => @cam_ty, :x1 => tx.to_f, :y1 => ty.to_f,
          :t => 0.0, :dur => [duration.to_f, 0.001].max, :ease => ease
        }
      end

      def zoom_map(goal, duration: 0.45, focus: nil, ease: :in_out)
        @zoom_focus = focus if !focus.nil?
        if duration <= 0.001
          @zoom = goal.to_f
          @zoom_task = nil
        else
          @zoom_task = {
            :z0 => @zoom, :z1 => goal.to_f,
            :t => 0.0, :dur => duration.to_f, :ease => ease
          }
        end
      end

      def set_tone(r, g, b, gray = 0, duration: 0.5)
        target = [r.to_f, g.to_f, b.to_f, gray.to_f]
        if duration <= 0.001
          @tone = target
          @tone_task = nil
          apply_tone
        else
          @tone_task = { :from => @tone.dup, :to => target, :t => 0.0, :dur => duration.to_f }
        end
      end

      def set_emergency_vignette(rgb = [210, 28, 36], max_alpha: 72, pulse_hz: 1.1)
        b = @vig_sp.bitmap
        b.clear
        w, h = b.width, b.height
        # Crisp stepped pixel-art dithered edge border glow (never muddy blur!)
        [24, 14, 6].each_with_index do |band, bi|
          alpha = [55, 110, 175][bi]
          col = Color.new(rgb[0], rgb[1], rgb[2], alpha)
          b.fill_rect(0, 0, w, band, col)
          b.fill_rect(0, h - band, w, band, col)
          b.fill_rect(0, band, band, h - band * 2, col)
          b.fill_rect(w - band, band, band, h - band * 2, col)
        end
        @vig_pulse = { :max => max_alpha.to_f, :hz => pulse_hz.to_f, :t => 0.0 }
      end

      def clear_vignette
        @vig_pulse = nil
        @vig_sp.opacity = 0
      end

      def letterbox(on, height: 32, duration: 0.35)
        goal = on ? height.to_f : 0.0
        if duration <= 0.001
          @bar_h = goal
          @bar_task = nil
          sync_bars
        else
          @bar_task = { :from => @bar_h, :to => goal, :t => 0.0, :dur => duration.to_f }
        end
      end

      def shake(power: 5, duration: 0.35, decay: true)
        p = photosensitive? ? (power.to_f * 0.2) : power.to_f
        @shake_task = { :p => p, :t => 0.0, :dur => [duration.to_f, 0.001].max, :decay => decay }
      end

      def flash(color: [255, 255, 255], power: 220, duration: 0.25)
        p = photosensitive? ? [power, 64].min : power
        @flash_sp.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(color[0], color[1], color[2]))
        @flash_sp.opacity = p
        @flash_task = { :mode => :fade, :p => p.to_f, :t => 0.0, :dur => [duration.to_f, 0.001].max }
      end

      # 0-frame hard cut to solid pure #000000 black (above letterbox bars & actors!)
      def set_blackout(on)
        if on
          @flash_sp.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(0, 0, 0))
          @flash_sp.opacity = 255
          @flash_task = nil
        else
          @flash_sp.opacity = 0
          @flash_task = nil
        end
      end

      # Reborn/Rejuvenation ramped flash: 17 -> 51 -> 136 -> 221 -> 255 -> hold -> fade
      def flash_ramp(color: [255, 255, 255], steps: [17, 51, 136, 221, 255],
                     step_dur: 0.035, hold_dur: 0.14, fade_dur: 0.35)
        @flash_sp.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(color[0], color[1], color[2]))
        if photosensitive?
          steps = steps.map { |v| [v / 4, 60].min }
          hold_dur = 0.04
        end
        @flash_task = {
          :mode => :ramp, :steps => steps, :step_dur => step_dur,
          :hold_dur => hold_dur, :fade_dur => fade_dur, :t => 0.0
        }
      end

      # Classic 2-frame high-contrast B&W impact beat + real-clock hitstop!
      def impact_beat(hitstop_sec: 0.14, color_a: [255, 255, 255], color_b: [16, 12, 24])
        if !photosensitive?
          @flash_sp.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(*color_a))
          @flash_sp.opacity = 235
          step_frame(true)
          @flash_sp.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(*color_b))
          @flash_sp.opacity = 210
          step_frame(true)
          @flash_sp.opacity = 0
        end
        trigger_hitstop(hitstop_sec) if hitstop_sec > 0.0
      end

      def trigger_hitstop(sec)
        @hitstop = [@hitstop, sec.to_f].max
      end

      #-------------------------------------------------------------------------
      # Actor & VFX Spawning
      #-------------------------------------------------------------------------
      def spawn_actor(id, **opts)
        remove_actor(id)
        @actors[id] = MapActor.new(self, id, **opts)
      end

      def actor(id); @actors[id]; end

      def remove_actor(id)
        a = @actors.delete(id)
        a.dispose if a
      end

      def clear_actors
        @actors.each_value(&:dispose)
        @actors.clear
      end

      def spawn_vfx(id = nil, **opts)
        v = MapVfx.new(self, id, **opts)
        @vfxs << v
        v
      end

      def stop_vfx(id)
        @vfxs.each { |v| v.stop! if v.id == id }
      end

      def clear_vfxs
        @vfxs.each(&:dispose)
        @vfxs.clear
      end

      #-------------------------------------------------------------------------
      # Dialogue + Timeline Wait Helpers
      #-------------------------------------------------------------------------
      # [PF] In real play the box waits for USE / BACK (a press while it types shows the whole line);
      # capture runs and auto_advance keep Gemini's timed hold. A line longer than the box pages.
      def say(speaker_sym, expr, text, hold: 1.55, name: nil, interactive: nil)
        interactive = interactive? if interactive.nil?
        if Prismfall::AdvancedAnimations.player_key?(speaker_sym)
          name = ($player.name rescue name)
        end
        rest = text.to_s
        while rest
          @dialogue.dispose if @dialogue
          @dialogue = PortraitBox.new(@ui_vp, speaker_sym, expr, rest, self, name: name)
          rest = @dialogue.overflow
          if interactive
            until @dialogue.done_typing?
              step_frame
              @dialogue.finish! if advance_pressed?
            end
            @dialogue.prompt = true
            step_frame
            step_frame until advance_pressed?
          else
            step_frame until @dialogue.done_typing?
            wait(hold)
          end
          @dialogue.dispose
          @dialogue = nil
        end
      end

      def interactive?
        return false if @capture_dir
        return !Prismfall::AdvancedAnimations.auto_advance
      end

      def advance_pressed?
        return Input.trigger?(Input::USE) || Input.trigger?(Input::BACK)
      end

      def wait(seconds)
        target = @time + seconds.to_f
        step_frame while @time < target
      end

      def wait_for_clip(actor_id)
        a = @actors[actor_id]
        return if !a
        step_frame until a.clip_done?
      end

      def wait_for_move(actor_id)
        a = @actors[actor_id]
        return if !a
        step_frame until !a.moving?
      end

      # Seamless live map transfer (B2W2 / Rejuv V14 cross-cut!)
      def transfer_map(map_id, cam_tx, cam_ty, hide_player: true)
        if !Prismfall::AdvancedAnimations.map_built?(map_id)                 # [PF]
          raise SceneUnavailable, "map #{map_id} is not built"
        end
        begin_session_travel                                                  # [PF]
        clear_actors
        clear_vfxs
        @zoom = 1.0
        @zoom_task = nil
        @zoom_sp.visible = false
        $game_temp.player_transferring = false
        $game_map.setup(map_id)
        $game_player.moveto(cam_tx.round, cam_ty.round)
        $game_player.transparent = hide_player
        $scene.disposeSpritesets if $scene.respond_to?(:disposeSpritesets)
        $scene.createSpritesets  if $scene.respond_to?(:createSpritesets)
        set_camera_tile(cam_tx, cam_ty)
        apply_tone
        # Force 1 silent update so Spriteset_Map refreshes cleanly before next capture
        $game_map.update
        $scene.miniupdate if $scene.respond_to?(:miniupdate)
      end

      #-------------------------------------------------------------------------
      # Frame Update + Unified pbZoomMap Snap + Lossless Capture
      #-------------------------------------------------------------------------
      def step_frame(ignore_hitstop = false)
        dt = @fixed_dt || begin
          now = System.uptime
          d = [[now - @last_tick, 0.001].max, 0.05].min
          @last_tick = now
          d
        end
        @time += dt

        # Hitstop freezes actor/VFX motion while camera shake & audio keep living!
        world_dt = (!ignore_hitstop && @hitstop > 0.0) ? 0.0 : dt
        if !ignore_hitstop && @hitstop > 0.0
          @hitstop = [@hitstop - dt, 0.0].max
        end

        update_camera(dt)
        update_tone(dt)
        update_bars(dt)
        update_flash(dt)
        update_vignette(dt)

        # Keep real RPG Maker XP map events & autotiles alive underneath!
        if world_dt > 0.0
          $game_map.update
          apply_camera_display
          $scene.miniupdate if $scene.respond_to?(:miniupdate)
        end

        @actors.each_value { |a| a.update(world_dt) }
        @vfxs.reject! do |v|
          finished = v.update(world_dt)
          v.dispose if finished
          finished
        end
        @dialogue.update(dt) if @dialogue

        # Apply shake directly to world viewports when not zoomed
        if @zoom <= 1.001
          @actor_vp.ox = -@shake_x.round
          @actor_vp.oy = -@shake_y.round
          @vfx_vp.ox   = -@shake_x.round
          @vfx_vp.oy   = -@shake_y.round
          @zoom_sp.visible = false
        else
          @actor_vp.ox = 0
          @actor_vp.oy = 0
          @vfx_vp.ox   = 0
          @vfx_vp.oy   = 0
          render_zoom_snapshot
        end

        Graphics.update
        Input.update if !@fixed_dt

        if @capture_dir
          Graphics.screenshot(format("%s/f%05d.png", @capture_dir, @frames_captured))
          @frames_captured += 1
        end
      end

      def dispose
        @dialogue.dispose if @dialogue
        clear_actors
        clear_vfxs
        @backdrop_sp.dispose if @backdrop_sp && !@backdrop_sp.disposed?
        if @zoom_sp && !@zoom_sp.disposed?
          @zoom_sp.bitmap.dispose if @zoom_sp.bitmap && !@zoom_sp.bitmap.disposed?
          @zoom_sp.dispose
        end
        [@bar_bot, @bar_top, @flash_sp, @vig_sp].each do |s|
          next if !s || s.disposed?
          s.bitmap.dispose if s.bitmap && !s.bitmap.disposed? && s != @bar_bot
          s.dispose
        end
        @bmp_cache.each_value { |b| b.dispose if b && !b.disposed? }
        @bmp_cache.clear
        [@actor_vp, @vfx_vp, @zoom_vp, @ui_vp].each { |v| v.dispose if v && !v.disposed? }
        restore_session                                                       # [PF] was: tone.set(0, 0, 0, 0)
      end

      private

      #-------------------------------------------------------------------------
      # [PF] Session: what the game gets back when the scene ends
      #-------------------------------------------------------------------------
      def snapshot_session
        return nil if !$game_map || !$game_player
        t = ($game_screen) ? $game_screen.tone : nil
        return {
          :map_id => $game_map.map_id, :x => $game_player.x, :y => $game_player.y,
          :dir => $game_player.direction, :transparent => $game_player.transparent,
          :display_x => $game_map.display_x, :display_y => $game_map.display_y,
          :tone => (t ? [t.red, t.green, t.blue, t.gray] : [0, 0, 0, 0]),
          :bgm => (($game_system.getPlayingBGM rescue nil)),
          :travelled => false, :followers => []
        }
      end

      # first transfer_map of a scene: from here on the real map and player are props
      def begin_session_travel
        return if !@session || @session[:travelled]
        @session[:travelled] = true
        return if !$game_temp || !$game_temp.respond_to?(:followers)
        $game_temp.followers.each_follower do |event, _data|
          @session[:followers] << [event, event.transparent]
          event.transparent = true
        end
      rescue StandardError
        nil
      end

      def restore_session
        s = @session
        @session = nil
        return if !s
        if s[:travelled] && $game_map && $game_player
          $game_temp.player_transferring = false if $game_temp
          $game_map.setup(s[:map_id])
          $game_player.moveto(s[:x], s[:y])
          case s[:dir]
          when 2 then $game_player.turn_down
          when 4 then $game_player.turn_left
          when 6 then $game_player.turn_right
          when 8 then $game_player.turn_up
          end
          $game_player.transparent = s[:transparent]
          s[:followers].each { |event, was| event.transparent = was }
          if $scene.respond_to?(:createSpritesets)
            $scene.disposeSpritesets if $scene.respond_to?(:disposeSpritesets)
            $scene.createSpritesets
          end
          $game_map.display_x = s[:display_x]
          $game_map.display_y = s[:display_y]
          $game_map.need_refresh = true
          $game_map.update
        end
        $game_screen.tone.set(*s[:tone]) if $game_screen
        if $game_system
          if s[:bgm]
            pbBGMPlay(s[:bgm])
          else
            pbBGMFade(0.8)
          end
        end
      rescue StandardError => e
        PBDebug.log("[AdvancedAnimations] restore_session: #{e.class}: #{e.message}") if defined?(PBDebug)
      end

      def apply_camera_display
        return if @cam_tx.nil? || @cam_ty.nil?
        max_x = [($game_map.width - Graphics.width / 32.0) * SUB, 0].max
        max_y = [($game_map.height - Graphics.height / 32.0) * SUB, 0].max
        dx = (@cam_tx * SUB) - ((Graphics.width / 2.0 - 16.0) * 4.0)
        dy = (@cam_ty * SUB) - ((Graphics.height / 2.0 - 16.0) * 4.0)
        $game_map.display_x = [[dx, 0.0].max, max_x].min.round
        $game_map.display_y = [[dy, 0.0].max, max_y].min.round
      end

      def update_camera(dt)
        if @cam_task
          @cam_task[:t] += dt
          u = [@cam_task[:t] / @cam_task[:dur], 1.0].min
          k = Ease.apply(@cam_task[:ease], u)
          @cam_tx = @cam_task[:x0] + (@cam_task[:x1] - @cam_task[:x0]) * k
          @cam_ty = @cam_task[:y0] + (@cam_task[:y1] - @cam_task[:y0]) * k
          @cam_task = nil if u >= 1.0
          apply_camera_display
        end

        if @zoom_task
          @zoom_task[:t] += dt
          u = [@zoom_task[:t] / @zoom_task[:dur], 1.0].min
          k = Ease.apply(@zoom_task[:ease], u)
          @zoom = @zoom_task[:z0] + (@zoom_task[:z1] - @zoom_task[:z0]) * k
          @zoom_task = nil if u >= 1.0
        end

        if @shake_task
          @shake_task[:t] += dt
          if @shake_task[:t] >= @shake_task[:dur]
            @shake_task = nil
            @shake_x = @shake_y = 0.0
          else
            u = @shake_task[:t] / @shake_task[:dur]
            amp = @shake_task[:decay] ? (@shake_task[:p] * (1.0 - u)) : @shake_task[:p]
            ph = @shake_task[:t] * 58.0
            @shake_x = Math.sin(ph) * amp
            @shake_y = Math.cos(ph * 1.37) * amp * 0.65
          end
        else
          @shake_x = @shake_y = 0.0
        end
      end

      def focus_screen_point
        case @zoom_focus
        when Array
          sx, sy = tile_to_screen(@zoom_focus[0], @zoom_focus[1])
          return sx, sy - 16.0
        when Symbol
          if @actors[@zoom_focus]
            a = @actors[@zoom_focus]
            sx, sy = a.screen_pos
            y_off = @backdrop_sp && @backdrop_sp.visible ? 52.0 : (20.0 * a.scale)
            return sx, sy - y_off
          end
        end
        return Graphics.width / 2.0, Graphics.height / 2.0
      end

      # Rejuvenation V14 Scripts/Camera/pbZoomMap unified snapshot zoom!
      def render_zoom_snapshot
        @zoom_vp.visible = false
        @ui_vp.visible   = false
        snap = Graphics.snap_to_bitmap
        @ui_vp.visible   = true
        @zoom_vp.visible = true

        old = @zoom_sp.bitmap
        @zoom_sp.bitmap = snap
        old.dispose if old && !old.disposed?

        # §12 patch 2: exact integer overscan clamp (no peel-away at the screen edges)
        fx, fy = focus_screen_point
        w = Graphics.width.to_f
        h = Graphics.height.to_f
        z = [@zoom.to_f, 1.001].max
        sx = (w / 2.0 + @shake_x).round
        sy = (h / 2.0 + @shake_y).round
        min_fx = (sx / z).ceil
        max_fx = (w - (w - sx) / z).floor
        min_fy = (sy / z).ceil
        max_fy = (h - (h - sy) / z).floor
        @zoom_sp.ox = (min_fx <= max_fx) ? [[fx.round, min_fx].max, max_fx].min : (w / 2.0).round
        @zoom_sp.oy = (min_fy <= max_fy) ? [[fy.round, min_fy].max, max_fy].min : (h / 2.0).round
        @zoom_sp.x  = sx
        @zoom_sp.y  = sy
        @zoom_sp.zoom_x = @zoom
        @zoom_sp.zoom_y = @zoom
        @zoom_sp.visible = true
      end

      def update_tone(dt)
        return if !@tone_task
        @tone_task[:t] += dt
        u = [@tone_task[:t] / @tone_task[:dur], 1.0].min
        4.times { |i| @tone[i] = @tone_task[:from][i] + (@tone_task[:to][i] - @tone_task[:from][i]) * u }
        @tone_task = nil if u >= 1.0
        apply_tone
      end

      def apply_tone
        t = Tone.new(@tone[0].round, @tone[1].round, @tone[2].round, @tone[3].round)
        $game_screen.tone.set(t.red, t.green, t.blue, t.gray) if $game_screen
        @actor_vp.tone.set(t.red, t.green, t.blue, t.gray)
      end

      def update_bars(dt)
        return if !@bar_task
        @bar_task[:t] += dt
        u = [@bar_task[:t] / @bar_task[:dur], 1.0].min
        @bar_h = @bar_task[:from] + (@bar_task[:to] - @bar_task[:from]) * Ease.apply(:out, u)
        @bar_task = nil if u >= 1.0
        sync_bars
      end

      def sync_bars
        h = @bar_h.round
        if h <= 0
          @bar_top.visible = @bar_bot.visible = false
        else
          @bar_top.visible = @bar_bot.visible = true
          @bar_top.x = 0; @bar_top.y = 0; @bar_top.zoom_y = h / 4.0
          @bar_bot.x = 0; @bar_bot.y = Graphics.height - h; @bar_bot.zoom_y = h / 4.0
        end
      end

      def update_flash(dt)
        return if !@flash_task
        @flash_task[:t] += dt
        if @flash_task[:mode] == :fade
          u = @flash_task[:t] / @flash_task[:dur]
          if u >= 1.0
            @flash_sp.opacity = 0
            @flash_task = nil
          else
            @flash_sp.opacity = (@flash_task[:p] * (1.0 - u)).round
          end
        else # :ramp
          steps = @flash_task[:steps]
          ramp_total = steps.length * @flash_task[:step_dur]
          hold_end   = ramp_total + @flash_task[:hold_dur]
          fade_end   = hold_end + @flash_task[:fade_dur]
          t = @flash_task[:t]
          if t < ramp_total
            idx = [(t / @flash_task[:step_dur]).to_i, steps.length - 1].min
            @flash_sp.opacity = steps[idx]
          elsif t < hold_end
            @flash_sp.opacity = steps.last
          elsif t < fade_end
            u = (t - hold_end) / [@flash_task[:fade_dur], 0.001].max
            @flash_sp.opacity = (steps.last * (1.0 - u)).round
          else
            @flash_sp.opacity = 0
            @flash_task = nil
          end
        end
      end

      def update_vignette(dt)
        return if !@vig_pulse
        @vig_pulse[:t] += dt
        wave = 0.5 + 0.5 * Math.sin(@vig_pulse[:t] * Math::PI * 2.0 * @vig_pulse[:hz])
        @vig_sp.opacity = (@vig_pulse[:max] * (0.35 + 0.65 * wave)).round
      end
    end

    #===========================================================================
    # Engine Extension: Crisp 512x384 exact2x=True 90° Banquet-Style Apex Plate
    #---------------------------------------------------------------------------
    # Renders the plate inside dedicated untoned @plate_vp at z=390 (ABOVE all
    # toned overworld actors at z=350, BELOW untoned @vfx_vp live pixel rain/motes
    # at z=420, BELOW @ui_vp letterbox & PortraitBox at z=90000!) while safely
    # suspending/restoring any active pbZoomMap snapshot and guaranteeing 100%
    # edge-to-edge coverage during pan + zoom + shake!
    #===========================================================================
    module CutPlateExtension
      def show_cut_plate(path_or_name, fade_in: 0.20, hold: 4.0, fade_out: 0.30,
                         pan: nil, zoom: [1.0, 1.06], shake: 0, &block)
        path = path_or_name.start_with?("Graphics/") ? path_or_name : "Graphics/Pictures/#{path_or_name}"
        file_p = path.end_with?(".png") ? path : "#{path}.png"
        return false unless File.exist?(file_p)

        ensure_cut_plate_sprite
        bmp = cached_bitmap(path)
        @cut_plate_sp.bitmap  = bmp
        @cut_plate_sp.ox      = bmp.width / 2
        @cut_plate_sp.oy      = bmp.height / 2
        @cut_plate_sp.z       = 1000
        @cut_plate_sp.visible = true
        @cut_plate_bg.visible = true

        # Suspend any active pbZoomMap snapshot so the 90° plate renders at true 1:1 native scale!
        @cut_plate_saved_zoom = [@zoom, @zoom_focus, @zoom_task]
        @zoom = 1.0
        @zoom_task = nil
        @zoom_sp.visible = false if @zoom_sp && !@zoom_sp.disposed?

        p0, p1 = parse_pan_spec(pan)
        z0, z1 = Array(zoom).length >= 2 ? [zoom[0].to_f, zoom[1].to_f] : [1.0, 1.05]
        sh = photosensitive? ? (shake.to_f * 0.2) : shake.to_f

        # Guarantee 100% edge-to-edge coverage with smooth monotonic zoom (zero map peek-through!)
        hw = [bmp.width / 2.0, 1.0].max
        hh = [bmp.height / 2.0, 1.0].max
        req_z0 = [1.0, 1.0 + (p0[0].abs + sh + 1.0) / hw, 1.0 + (p0[1].abs + sh + 1.0) / hh].max
        req_z1 = [1.0, 1.0 + (p1[0].abs + sh + 1.0) / hw, 1.0 + (p1[1].abs + sh + 1.0) / hh].max
        z0 = [z0, req_z0].max
        z1 = [z1, req_z1, z0 + 0.04].max

        total_motion = [fade_in.to_f + hold.to_f + fade_out.to_f, 0.5].max

        @cut_plate_task = {
          :t => 0.0, :dur => total_motion,
          :p0 => p0, :p1 => p1, :z0 => z0, :z1 => z1,
          :shake => sh
        }
        apply_cut_plate_transform(0.0)

        # Fade-in ramp
        if fade_in.to_f > 0.001
          t_start = @time
          while (@time - t_start) < fade_in.to_f
            u = [(@time - t_start) / fade_in.to_f, 1.0].min
            op = (255.0 * Ease.apply(:out, u)).round
            @cut_plate_sp.opacity = op
            @cut_plate_bg.opacity = op
            step_frame
          end
        end
        @cut_plate_sp.opacity = 255
        @cut_plate_bg.opacity = 255

        # Active hold or custom choreographed block (e.g., silent beat + PortraitBox dialogue!)
        if block_given?
          block.call(self)
        else
          wait(hold.to_f)
        end

        # Fade-out ramp
        if fade_out.to_f > 0.001
          t_start = @time
          while (@time - t_start) < fade_out.to_f
            u = [(@time - t_start) / fade_out.to_f, 1.0].min
            op = (255.0 * (1.0 - Ease.apply(:in, u))).round
            @cut_plate_sp.opacity = op
            @cut_plate_bg.opacity = op
            step_frame
          end
        end

        clear_cut_plate
        true
      end

      def clear_cut_plate
        @cut_plate_task = nil
        if @cut_plate_sp && !@cut_plate_sp.disposed?
          @cut_plate_sp.visible = false
          @cut_plate_sp.opacity = 0
          @cut_plate_sp.bitmap  = nil
        end
        if @cut_plate_bg && !@cut_plate_bg.disposed?
          @cut_plate_bg.visible = false
          @cut_plate_bg.opacity = 0
        end
        if @cut_plate_saved_zoom
          @zoom, @zoom_focus, @zoom_task = @cut_plate_saved_zoom
          @cut_plate_saved_zoom = nil
        end
      end

      def step_frame(ignore_hitstop = false)
        if @cut_plate_task && @cut_plate_sp && !@cut_plate_sp.disposed? && @cut_plate_sp.visible
          dt = @fixed_dt || 0.0333
          @cut_plate_task[:t] += dt
          u = [@cut_plate_task[:t] / @cut_plate_task[:dur], 1.0].min
          apply_cut_plate_transform(u)
        end
        super(ignore_hitstop)
      end

      def dispose
        clear_cut_plate
        if @cut_plate_sp && !@cut_plate_sp.disposed?
          @cut_plate_sp.dispose
        end
        @cut_plate_sp = nil
        if @cut_plate_bg && !@cut_plate_bg.disposed?
          @cut_plate_bg.bitmap.dispose if @cut_plate_bg.bitmap && !@cut_plate_bg.bitmap.disposed?
          @cut_plate_bg.dispose
        end
        @cut_plate_bg = nil
        if @plate_vp && !@plate_vp.disposed?
          @plate_vp.dispose
        end
        @plate_vp = nil
        super
      end

      private

      def ensure_cut_plate_sprite
        return if @cut_plate_sp && !@cut_plate_sp.disposed?
        @plate_vp = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @plate_vp.z = 390
        @cut_plate_bg = Sprite.new(@plate_vp)
        @cut_plate_bg.bitmap = Bitmap.new(Graphics.width, Graphics.height)
        @cut_plate_bg.bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(0, 0, 0, 255))
        @cut_plate_bg.z = 999
        @cut_plate_bg.visible = false
        @cut_plate_bg.opacity = 0
        @cut_plate_sp = Sprite.new(@plate_vp)
        @cut_plate_sp.z = 1000
        @cut_plate_sp.visible = false
        @cut_plate_sp.opacity = 0
      end

      def parse_pan_spec(pan)
        if pan.is_a?(Hash) && !pan.empty?
          k, v = pan.first
          return [k[0].to_f, k[1].to_f], [v[0].to_f, v[1].to_f]
        elsif pan.is_a?(Array) && pan.length == 2 && pan[0].is_a?(Array)
          return [pan[0][0].to_f, pan[0][1].to_f], [pan[1][0].to_f, pan[1][1].to_f]
        end
        return [0.0, 0.0], [0.0, 0.0]
      end

      def apply_cut_plate_transform(u)
        task = @cut_plate_task
        return unless task && @cut_plate_sp && !@cut_plate_sp.disposed?
        k = Ease.apply(:in_out, u)
        px = task[:p0][0] + (task[:p1][0] - task[:p0][0]) * k
        py = task[:p0][1] + (task[:p1][1] - task[:p0][1]) * k
        sc = task[:z0] + (task[:z1] - task[:z0]) * k
        sh_x = task[:shake] > 0.0 ? Math.sin(task[:t] * 48.0) * task[:shake] : 0.0
        sh_y = task[:shake] > 0.0 ? Math.cos(task[:t] * 61.0) * task[:shake] * 0.65 : 0.0
        @cut_plate_sp.x      = (Graphics.width / 2.0 + px + sh_x).round
        @cut_plate_sp.y      = (Graphics.height / 2.0 + py + sh_y).round
        @cut_plate_sp.zoom_x = sc
        @cut_plate_sp.zoom_y = sc
      end
    end

    Engine.prepend(CutPlateExtension)

    #===========================================================================
    # SCENES (the latest version of each; see the header of this file)
    #===========================================================================
    class << self
      #=========================================================================
      # SCENE 0 (LIVE DIRECTOR'S CUT) — Ch2: "Dorian's Stage & The Lantern Pageant"
      # Target Duration: ~28.0s (~840 frames @ 30fps)
      # Live Map: Map 145 (Lantern Theatre — stage x=11..26 y=3..9, stalls y=13..23)
      # Uses act_ch2_dorian_stage + Followers/MELOETTA + <= 3 emotes!
      #=========================================================================
      def play_ch2_lantern_pageant_dc(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # ACT I (0.0–8.5s) — Warm Theatrical Wonder: Dorian's Spotlight & Meloetta Dance!
          eng.transfer_map(145, 18.5, 9.5, hide_player: true)
          # Hide static Pageant & Ottilie stage NPCs so Dorian, Meloetta & Mourner own the wide stage cleanly!
          $game_map.events.each_value do |ev|
            ev.transparent = true if ["Pageant", "Ottilie"].include?(ev.name)
          end

          eng.set_tone(12, 4, -10, 0, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch2_dorian_stage", volume: 82, tag: "ch2_dorian_stage")

          # Dorian center-stage on polished boards (18.5, 7.6), Meloetta at (16.5, 7.6)
          # Juno & PC standing calmly in front center aisle (17.6, 13.8) & (18.8, 13.8)
          eng.spawn_actor(:dorian,   sheet: "act_ch2_dorian_stage", tx: 18.5, ty: 7.6, grid: [4, 4], is_charset: false)
          eng.spawn_actor(:meloetta, sheet: "Followers/MELOETTA",   tx: 16.5, ty: 7.6, dir: :down, grid: [4, 4], is_charset: true)
          eng.spawn_actor(:juno,     sheet: "JUNO",                 tx: 17.6, ty: 13.8, dir: :up, is_charset: true)
          eng.spawn_actor(:pc,       sheet: "PLAYER_A",             tx: 18.8, ty: 13.8, dir: :up, is_charset: true)

          # Dorian theatrical top-hat tip & sweeping velvet cape flourish (frames 0..7)!
          eng.actor(:dorian).play_clip(
            sheet: "act_ch2_dorian_stage", grid: [4, 4], frames: [0, 1, 2, 3, 4, 5, 6, 7],
            ticks: [8, 7, 8, 10, 7, 12, 10, 10], loops: 1, stay: true
          )
          eng.actor(:meloetta).move_to(20.5, 7.6, duration: 1.8, walk: true, dir: :right, arc_h: 8.0)
          eng.play_cry(:MELOETTA, volume: 84)
          eng.wait(2.2)

          eng.say(:DORIAN, :happy, "Enter, stage left, our brave challenger! To thunderous applause!", hold: 1.25)
          eng.wait(0.35)
          eng.say(:JUNO, :happy, "It IS salt. It's still beautiful. I hate that it's still beautiful.", hold: 1.25)

          # ACT II (8.5–15.5s) — Stage Lights Snap Cool Twilight-Grey & The Mourner Steps From Canvas!
          eng.bgm_cut
          eng.play_se("Door slide", volume: 86, pitch: 72)
          # Readable eerie desaturated twilight-slate (keeps stage wood, footlights & velvet seats crisp!)
          eng.set_tone(-34, -36, -24, 68, duration: 0.25)
          eng.actor(:dorian).play_clip(
            sheet: "act_ch2_dorian_stage", grid: [4, 4], frames: [8, 9, 10, 11],
            ticks: [8, 6, 8, 24], loops: 1, stay: true
          )
          # Dorian recoils cleanly stage-left while Meloetta turns in alarm toward center stage!
          eng.actor(:dorian).move_to(16.0, 8.0, duration: 0.50, walk: false, ease: :out)
          eng.actor(:meloetta).set_dir(:left)
          eng.actor(:meloetta).move_to(21.1, 7.9, duration: 0.45, walk: false, arc_h: 6.0, ease: :out)
          # Emote #1 of 3 (restrained!): Dorian jolts spinning toward torn painted canvas!
          eng.actor(:dorian).show_emote(:exclaim, duration: 0.65)
          eng.wait(0.55)

          # The Mourner steps straight through the torn center backdrop at (18.5, 5.0)!
          eng.play_bgm("ch2_mourner_sermon", volume: 84, tag: "ch2_mourner_sermon")
          eng.spawn_actor(:mourner, sheet: "MOURNER", tx: 18.5, ty: 5.0, dir: :down, is_charset: true)
          eng.actor(:mourner).move_to(18.5, 6.9, duration: 1.25, walk: true, dir: :down)
          eng.zoom_map(1.28, duration: 1.15, focus: :mourner, ease: :in_out)
          eng.wait(1.30)

          eng.say(:MOURNER, :neutral, "Three hundred years of pageantry. Ask your Warden why nothing in Verdance ever rots.", hold: 1.45)

          # Emote #2 of 3 (restrained!): Grounded UP-facing Juno shudders looking at the stage!
          eng.actor(:juno).tremble(duration: 0.55, amp: 1.5, freq: 42.0)
          eng.actor(:juno).show_emote(:double_exclaim, duration: 0.65)
          eng.wait(0.45)
          eng.say(:MOURNER, :sad, "Let the land grieve.", hold: 1.05)

          # ACT III (15.5–21.5s) — Canvas Tear & Dorian Commands the House Lights!
          eng.zoom_map(1.0, duration: 0.35, ease: :out)
          eng.play_se("Cut", volume: 96, pitch: 112)
          eng.shake(power: 5, duration: 0.38)

          # Dorian steps to the front-left apron with sweeping cape command pose (ZERO floating rail box!)
          eng.actor(:dorian).move_to(15.8, 8.4, duration: 0.35, walk: false, ease: :out)
          eng.actor(:dorian).play_clip(
            sheet: "act_ch2_dorian_stage", grid: [4, 4], frames: [4, 5, 6, 7],
            ticks: [6, 10, 10, 24], loops: 1, stay: true
          )
          plate_shown = eng.show_cut_plate(
            "Graphics/Pictures/cut_ch2_pageant_tear_90deg",
            fade_in: 0.18, hold: 5.8, fade_out: 0.30,
            pan: { [-6, 4] => [8, -4] }, zoom: [1.0, 1.06], shake: 2
          ) do |e|
            e.wait(2.40)
            e.say(:DORIAN, :angry, "House lights! HOUSE LIGHTS! Everybody walk, nobody run!", hold: 1.35)
            e.wait(0.55)
          end
          unless plate_shown
            # House lights surge partially back up on Dorian's shout!
            eng.set_tone(-14, -14, -12, 34, duration: 0.35)
            eng.zoom_map(1.22, duration: 0.55, focus: :dorian, ease: :out)
            eng.say(:DORIAN, :angry, "House lights! HOUSE LIGHTS! Everybody walk, nobody run!", hold: 1.35)
            eng.zoom_map(1.0, duration: 0.45, ease: :out)
          end

          # ACT IV (21.5–28.0s) — 60-Frame Freeze "...You." & Organic Cotton Spore Vanish!
          # Calm, grounded vertical step forward up the center aisle (zero fast diagonal darting!)
          eng.actor(:pc).move_to(18.8, 12.2, duration: 1.15, walk: true, dir: :up)
          eng.pan_camera_to(18.5, 8.8, duration: 0.85, ease: :in_out)
          eng.wait(1.20)

          # Emote #3 of 3 (restrained!): Mourner sees the PC and freezes for 60 full frames!
          eng.bgm_cut
          eng.actor(:mourner).show_emote(:dots, duration: 1.10)
          eng.zoom_map(1.36, duration: 1.25, focus: :mourner, ease: :in_out)
          eng.wait(1.50)

          eng.say(:MOURNER, :shocked, "...You.", hold: 1.10)

          # Soft organic swirling white Cotton Spore vanish + drifting silver spore motes!
          eng.play_se("Anim/Silverwind", volume: 88, pitch: 118)
          eng.flash(color: [248, 250, 255], power: 195, duration: 0.36)
          [
            [-0.45, -0.30, 0.90, [0, 1, 2, 3], [-14, -18]],
            [ 0.50, -0.20, 0.85, [1, 2, 3, 0], [ 16, -20]],
            [-0.25,  0.25, 1.05, [2, 3, 0, 1], [-10, -10]],
            [ 0.35,  0.30, 0.80, [3, 0, 1, 2], [ 12, -12]],
            [ 0.00, -0.10, 1.15, [0, 1, 2, 3], [  0, -24]],
          ].each do |dx, dy, sc, fr, dr|
            eng.spawn_vfx(nil, sheet: "pf_vfx_smoke_and_motes", tx: 18.5 + dx, ty: 6.9 + dy,
                          grid: [4, 2], frames: fr, ticks: [4, 5, 5, 6],
                          blend: :add, opacity: 190, scale: sc, drift: dr, fade: 0.45, z_layer: :above)
          end
          6.times do |mi|
            ang = (mi / 6.0) * Math::PI * 2.0 + 0.3
            eng.spawn_vfx(nil, sheet: "pf_vfx_smoke_and_motes", tx: 18.5 + Math.cos(ang) * 0.4, ty: 6.8 + Math.sin(ang) * 0.3,
                          grid: [4, 2], frames: [7], hold: 1.35, blend: :add, opacity: 220, scale: 0.95,
                          drift: [Math.cos(ang) * 26, Math.sin(ang) * 14 - 22], fade: 0.55, z_layer: :above)
          end
          eng.remove_actor(:mourner)
          eng.zoom_map(1.0, duration: 0.65, ease: :out)
          eng.wait(1.00)

          eng.say(:JUNO, :sad, "He sounded sad. Isn't that weird? I thought he'd sound evil.", hold: 1.45)

          eng.wait(0.80)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.45)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE 1 (DIRECTOR'S CUT) — Ch5: "The Spire Shatter"
      # Target Duration: ~34.0s (~1,020 frames @ 30fps)
      # Live Maps: Sculpted Octagonal Map 952 -> Map 608 (Dex) -> Scarred Map 952!
      # ZERO MS-Paint geometry | ZERO pit-walking | <= 3 emotes | 90° Dex Plate!
      #=========================================================================
      # [PF] lowlight: false leaves out ACT III (the live Lowlight cutaway, the Dex plate and Rook's "Turn it
      # off" line). story/24_SCRIPT_CH5.md keeps all three for map 608 after the boss ("no streets shown").
      def play_ch5_spire_shatter_dc(capture_dir: nil, capture_fps: 30, lowlight: true)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I (0.0–8.5s) — Sculpted Octagonal Map 952 (Plate Vault Catwalk!)
          #   Walkable geometry strictly honored:
          #     - Elevated Marble Plate Dais: x=9..15, y=5..10 (Cradle at 12,7)
          #     - Steel-Grate Catwalk Bridge: x=11..13, y=10..15 (over abyssal PIT!)
          #     - South Vestibule -> Service Door: x=6..19, y=15..17 (Door at 18,17)
          #---------------------------------------------------------------------
          eng.transfer_map(952, 12.0, 11.2, hide_player: true)
          ev_mourner = $game_map.events.values.find { |e| e.name == "Mourner" }
          ev_mourner.transparent = true if ev_mourner

          eng.set_tone(-32, -36, -14, 28, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch5_girei_intro", volume: 82, tag: "ch5_girei_intro")

          # Cast positioned strictly on the catwalk bridge & elevated marble dais!
          eng.spawn_actor(:pc,      sheet: "PLAYER_A", tx: 11.7, ty: 15.8, dir: :up, is_charset: true)
          eng.spawn_actor(:rook,    sheet: "ROOK",     tx: 11.0, ty: 16.4, dir: :up, is_charset: true)
          eng.spawn_actor(:mourner, sheet: "act_ch5_mourner_reach", tx: 12.0, ty: 8.35, grid: [4, 4], is_charset: false)
          eng.spawn_actor(:sable,   sheet: "SABLE",    tx: 13.3, ty: 8.10, dir: :left, is_charset: true)

          # Subtle ambient Zap Plate sparks (zero giant geometric octagon seal!)
          eng.spawn_vfx(:plate_hum, sheet: "pf_vfx_prism_lightning", tx: 12.0, ty: 7.0,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [9, 9, 9, 9], loops: :forever,
                        blend: :add, opacity: 165, scale: 0.52, z_layer: :above, offset: [0, -6])

          # PC & Rook ascend the steel catwalk across the abyssal reactor shaft toward the dais!
          eng.actor(:pc).move_to(11.7, 11.4,   duration: 1.55, walk: true, dir: :up)
          eng.actor(:rook).move_to(11.0, 12.3, duration: 1.65, walk: true, dir: :up)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch5_mourner_reach", grid: [4, 4], frames: 0..7,
            ticks: [12, 8, 8, 10, 10, 8, 8, 10], loops: 1, stay: true
          )
          eng.pan_camera_to(12.0, 8.8, duration: 1.70, ease: :in_out)
          eng.wait(1.75)

          eng.say(:MOURNER, :neutral, "Gently. We lift it out gently, and we carry it out of here, and we give this city back its river and its dark.", hold: 1.35)
          eng.say(:MOURNER, :neutral, "That's all. That's all tonight is.", hold: 1.00)
          eng.wait(0.35)
          eng.say(:SABLE, :happy, "Mm-hm. Gently.", hold: 0.90)

          # Sable steps to the cradle, clamps the blinking brass Splitter & skips along the dais!
          eng.actor(:sable).move_to(12.85, 7.35, duration: 0.30, walk: true, dir: :left)
          eng.wait_for_move(:sable)
          eng.play_se("Battle catch click", volume: 100)
          eng.spawn_vfx(:splitter, sheet: "pf_vfx_splitter_beacon", tx: 12.35, ty: 7.05,
                        grid: [4, 1], frames: [0, 1, 0, 1], ticks: [6, 6, 4, 4],
                        loops: :forever, blend: :normal, untoned: true, z_layer: :above)

          # Emote #1 of 3 (restrained!): Mourner jolts seeing the Splitter clamp!
          eng.actor(:mourner).show_emote(:exclaim, duration: 0.60)
          eng.play_se("Exclaim", volume: 88)
          eng.actor(:sable).hop(height: 10, duration: 0.22)
          # Sable stays strictly on marble dais (14.2, 9.2) before fleeing down east catwalk lane!
          eng.actor(:sable).move_to(14.2, 9.2, duration: 0.48, walk: true, dir: :down)
          eng.wait(0.45)

          eng.say(:MOURNER, :shocked, "What is that? What have you put on—", hold: 0.95)
          eng.say(:SABLE, :happy, "Light for everyone.", hold: 0.85)

          # Sable exits legally via marble steps -> east catwalk handrail lane (13.2) -> East Service Door!
          eng.actor(:sable).move_to(13.2, 10.6, duration: 0.32, walk: true, dir: :down)
          eng.wait_for_move(:sable)
          eng.actor(:sable).move_to(13.2, 15.6, duration: 0.55, walk: true, dir: :down)
          eng.wait(0.30)

          #---------------------------------------------------------------------
          # ACT II (8.5–15.5s) — Conduit Overload, Barehanded Lunge & THE SHATTER!
          #---------------------------------------------------------------------
          eng.remove_actor(:sable)
          eng.set_tone(-78, -84, -52, 70, duration: 0.95)
          eng.zoom_map(1.46, duration: 1.20, focus: [12.0, 7.6], ease: :in_out)
          eng.stop_vfx(:plate_hum)
          eng.stop_vfx(:splitter)
          eng.spawn_vfx(:splitter_hot, sheet: "pf_vfx_splitter_beacon", tx: 12.35, ty: 7.05,
                        grid: [4, 1], frames: [1, 2, 2, 3], ticks: [4, 3, 2, 2],
                        loops: :forever, blend: :add, untoned: true, z_layer: :above)
          eng.play_se("Anim/Saint7", volume: 92)

          # Crackling violet-gold conduit lightning arcing across the marble sanctum!
          [[12.0, 7.2], [10.6, 7.8], [13.4, 7.8], [12.0, 9.4]].each_with_index do |(lx, ly), li|
            eng.spawn_vfx(nil, sheet: "pf_vfx_prism_lightning", tx: lx, ty: ly,
                          grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2],
                          blend: :add, scale: 0.92, z_layer: :above)
            eng.play_se("Anim/Thunder1", volume: 74) if li == 1
            eng.wait(0.24)
          end

          # LAW 2: 0.42s DEAD-SILENCE AUDIO VACUUM!
          eng.bgm_cut
          eng.play_se("Battle catch click", volume: 100, pitch: 128)
          eng.wait(0.42)

          # Mourner lunges barehanded into the Zap Plate flash while PC holds steady on the catwalk!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch5_mourner_reach", grid: [4, 4], frames: 8..15,
            ticks: [5, 3, 2, 2, 2, 3, 4, 5],
            se: { 2 => "Anim/Thunder9" },
            shake: { 4 => [4, 0.25] }
          )
          eng.wait(0.60)

          # THE SHATTER!! (ZERO geometric shockwave circle — pure ballistic crystal shards + lightning!)
          eng.play_se("Anim/Explosion7", volume: 100)
          eng.play_se("Anim/Ice8", volume: 96)
          eng.play_se("Anim/HealBell", volume: 88, pitch: 72)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.play_bgm("ch5_vogel_climax", volume: 92, tag: "ch5_vogel_climax")
          eng.flash_ramp(color: [248, 224, 255], steps: [51, 136, 221, 255],
                         step_dur: 0.03, hold_dur: 0.12, fade_dur: 0.44)
          eng.shake(power: 7, duration: 0.65, decay: true)
          eng.zoom_map(1.04, duration: 0.45, focus: [12.0, 8.2], ease: :out_cubic)
          eng.stop_vfx(:splitter_hot)

          # 16 crisp radial pixel crystal shards exploding outward from the Zap Plate!
          16.times do |si|
            ang = (si / 16.0) * Math::PI * 2.0 + 0.15
            spd = 138 + (si % 3) * 44
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: 12.0, ty: 7.4,
                          grid: [4, 2], frames: [si % 4, (si + 1) % 4, (si + 2) % 4, (si + 3) % 4],
                          hold: 0.07, loops: 3, blend: :add,
                          drift: [Math.cos(ang) * spd, Math.sin(ang) * spd - 52],
                          gravity: 240, spin: (si.even? ? 240 : -240), fade: 0.22, z_layer: :above)
          end

          # Conduit lightning racing south down the steel catwalk bridge!
          [[10.2, 9.2], [13.8, 9.2], [12.0, 10.4], [11.2, 12.2], [12.8, 12.2], [12.0, 14.0]].each_with_index do |(lx, ly), i|
            eng.spawn_vfx(nil, sheet: "pf_vfx_prism_lightning", tx: lx, ty: ly,
                          grid: [4, 2], frames: (i.even? ? (4..7) : (0..3)), ticks: [2, 2, 2, 2],
                          blend: :add, scale: 1.05, z_layer: :above)
            eng.wait(0.08)
          end
          eng.wait(0.85)

          #---------------------------------------------------------------------
          # ACT III (15.5–25.0s) — LIVE MAP 608 SHATTERED LOWLIGHT + 90° DEX PLATE!
          #   Canon location: NW Lowlight landing around Dex (4.5, 7.5) & Spark (5.5, 7.6)!
          #---------------------------------------------------------------------
          if !lowlight   # [PF] script beat 4: the ring of light runs out through the rock, then silence
            eng.bgm_fade(0.7)
            eng.wait(1.10)
          end
          if lowlight
          eng.flash(color: [244, 224, 255], power: 255, duration: 0.36)
          eng.transfer_map(608, 8.0, 7.4, hide_player: true)
          # Hide static post-shatter crowd events on NW landing so Dex & Spark own the beat cleanly!
          $game_map.events.each_value do |ev|
            ev.transparent = true if ev.x <= 12 && ev.y <= 12
          end
          eng.set_tone(-36, -42, -16, 48, duration: 0.0)

          # 11-year-old Dex waving happily beside his Fizzbolt soda crate + Spark the Pichu!
          eng.spawn_actor(:dex,    sheet: "act_ch5_dex_freeze", tx: 4.5, ty: 7.5, grid: [4, 4], is_charset: false)
          eng.spawn_actor(:pichu,  sheet: "Followers/PICHU",    tx: 5.5, ty: 7.6, dir: :left, grid: [4, 4], is_charset: true)
          eng.actor(:dex).play_clip(
            sheet: "act_ch5_dex_freeze", grid: [4, 4], frames: [0, 1, 2, 3, 2, 4, 5],
            ticks: [5, 5, 6, 6, 5, 7, 8], loops: 1, stay: true
          )
          eng.zoom_map(1.30, duration: 1.35, focus: :dex, ease: :in_out)
          eng.wait(1.30)

          # Violet Bleed frost veins sweep from the Spire across Lowlight cobblestones!
          eng.play_se("Anim/Ice8", volume: 88, pitch: 86)
          eng.play_cry(:PICHU, volume: 78)
          eng.actor(:pichu).tremble(duration: 1.8, amp: 2.0, freq: 48.0)
          [[7.5, 6.2], [6.2, 6.8], [5.2, 7.8], [3.6, 8.2]].each_with_index do |(gx, gy), gi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_frost", tx: gx, ty: gy,
                          grid: [4, 2], frames: 0..3, ticks: [3, 3, 3, 4],
                          stay: 4.0, fade: 0.3, blend: :normal, opacity: 145, scale: 0.85, z_layer: :floor)
            eng.wait(0.08)
          end

          # Dex crystallizes progressively mid-wave (frames 6 -> 10) -> hard bgm_cut -> 90° HEARTBREAK PLATE!
          eng.actor(:dex).play_clip(
            sheet: "act_ch5_dex_freeze", grid: [4, 4], frames: [6, 7, 8, 9, 10],
            ticks: [5, 5, 5, 6, 7], loops: 1, stay: true
          )
          eng.wait(1.25)

          eng.bgm_cut
          eng.play_se("Anim/HealBell", volume: 82, pitch: 112)
          eng.wait(0.35)

          # Floating translucent glass-dust motes drifting slowly OVER the 90° Dex plate!
          eng.play_bgm("ch5_lowlight_grief", volume: 82, tag: "ch5_lowlight_grief")
          8.times do |mi|
            eng.spawn_vfx(:"dex_mote_#{mi}", sheet: "pf_vfx_smoke_and_motes",
                          tx: 2.0 + mi * 1.4, ty: 9.2 - (mi % 3) * 1.2,
                          grid: [4, 2], frames: [7], hold: 8.0, blend: :add,
                          drift: [4 - (mi % 3) * 3, -16 - (mi % 4) * 4], fade: 0.8, z_layer: :above)
          end

          # 90° STREET-LEVEL HEARTBREAK APEX CUT: cut_ch5_dex_freeze_90deg.png (512x384 exact2x!)
          eng.show_cut_plate(
            "Graphics/Pictures/cut_ch5_dex_freeze_90deg",
            fade_in: 0.22, hold: 5.8, fade_out: 0.35,
            pan: { [-6, 0] => [10, -4] }, zoom: [1.0, 1.07], shake: 0
          ) do |e|
            # Hold 3.6s completely silent of text — let 11yo Dex & trembling Spark break your heart!
            e.wait(3.60)
            e.say(:ROOK, :sad, "...Turn it off. Rotom. Turn it off.", hold: 1.55)
            e.wait(0.55)
          end

          # Brief quiet hold back on live Map 608 showing Dex's settled shimmering crystal statue!
          eng.actor(:dex).play_clip(
            sheet: "act_ch5_dex_freeze", grid: [4, 4], frames: [12, 13, 14, 15],
            ticks: [8, 8, 8, 20], loops: 1, stay: true
          )
          eng.wait(1.35)
          end   # if lowlight

          #---------------------------------------------------------------------
          # ACT IV (25.0–34.0s) — Scarred Octagonal Map 952: Smoking Glove & Electivire!
          #---------------------------------------------------------------------
          eng.flash(color: [236, 224, 248], power: 205, duration: 0.38)
          eng.transfer_map(952, 12.0, 9.2, hide_player: true)
          ev_mourner = $game_map.events.values.find { |e| e.name == "Mourner" }
          ev_mourner.transparent = true if ev_mourner
          ev_cradle  = $game_map.events.values.find { |e| e.name == "Cradle" }
          if ev_cradle   # [PF] the cracked tile comes from the event's own "cracked" page
            cracked = (ev_cradle.instance_variable_get(:@event).pages[1].graphic.tile_id rescue 0)
            ev_cradle.instance_variable_set(:@tile_id, (cracked > 0) ? cracked : 25947)
          end
          eng.set_tone(-46, -50, -30, 52, duration: 0.0)

          # PC & Rook on the west side of the 3-tile catwalk so Mourner exits cleanly down east lane 13.2!
          eng.spawn_actor(:pc,      sheet: "PLAYER_A", tx: 11.7, ty: 11.4, dir: :up, is_charset: true)
          eng.spawn_actor(:rook,    sheet: "ROOK",     tx: 11.0, ty: 12.3, dir: :up, is_charset: true)
          eng.spawn_actor(:mourner, sheet: "act_ch5_mourner_burn", tx: 12.0, ty: 8.45, grid: [4, 4], is_charset: false)

          # Smoking right glove wisps + stuttering weak sparks strictly on the cracked Zap Plate!
          eng.spawn_vfx(:smoke, sheet: "pf_vfx_smoke_and_motes", tx: 12.45, ty: 8.2,
                        grid: [4, 2], frames: 0..3, ticks: [5, 5, 5, 5], loops: :forever,
                        blend: :normal, untoned: false, drift: [2, -8], z_layer: :above, offset: [0, -14])
          eng.spawn_vfx(:spark_cradle, sheet: "pf_vfx_prism_lightning", tx: 12.0, ty: 6.9,
                        grid: [4, 2], frames: [3, 2, 3], ticks: [12, 3, 16], loops: :forever,
                        blend: :add, scale: 0.48, z_layer: :above, offset: [0, -6])

          eng.actor(:mourner).play_clip(
            sheet: "act_ch5_mourner_burn", grid: [4, 4], frames: 0..11,
            ticks: [10, 10, 10, 10, 10, 10, 10, 10, 8, 8, 10, 12], loops: 1, stay: true
          )
          eng.wait(1.15)

          eng.say(:MOURNER, :shocked, "No — no — what did you DO?", hold: 1.05)
          eng.wait(0.45)
          eng.say(:MOURNER, :sad, "...You. Not you. Not here. Get out of here, child. Get OUT—", hold: 1.45)

          # Mourner flees cleanly down east catwalk lane (13.2) -> south vestibule -> East Service Door (ZERO pit-walk, ZERO PC brushing!)
          eng.stop_vfx(:smoke)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch5_mourner_burn", grid: [4, 4], frames: 12..15,
            ticks: [4, 4, 4, 4], loops: :forever
          )
          eng.actor(:mourner).move_to(13.2, 10.6, duration: 0.35, walk: false)
          eng.wait_for_move(:mourner)
          eng.actor(:pc).set_dir(:right)
          eng.actor(:mourner).move_to(13.2, 15.8, duration: 0.65, walk: false)
          eng.wait_for_move(:mourner)
          eng.actor(:pc).set_dir(:up)
          eng.actor(:mourner).move_to(18.0, 16.8, duration: 0.55, walk: false)
          eng.wait(0.55)
          eng.remove_actor(:mourner)
          eng.play_se("Door exit", volume: 80)

          # Overcharged Electivire leaps from behind the cracked cradle!
          eng.play_se("Anim/Thunder9", volume: 96)
          eng.spawn_actor(:electivire, sheet: "Followers/ELECTIVIRE", tx: 12.0, ty: 6.2,
                          dir: :down, grid: [4, 4], is_charset: true)
          eng.actor(:electivire).move_to(12.0, 8.4, duration: 0.38, walk: true, dir: :down, arc_h: 22.0)
          eng.spawn_vfx(nil, sheet: "pf_vfx_prism_lightning", tx: 12.0, ty: 8.3,
                        grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2],
                        blend: :add, scale: 1.25, z_layer: :above)
          eng.shake(power: 5, duration: 0.42)
          eng.play_cry(:ELECTIVIRE, volume: 100)

          # Emote #2 of 3 (restrained!): Grounded PC holds steady facing Electivire on the catwalk!
          eng.actor(:pc).show_emote(:double_exclaim, duration: 0.65)
          eng.zoom_map(1.30, duration: 0.60, focus: :electivire, ease: :out_cubic)
          eng.wait(0.75)

          eng.say(:ROOK, :shocked, "That's it. That's the Zap Plate. That's — it's broken. It's BROKEN.", hold: 1.00)
          # Emote #3 of 3 (restrained!): Rook glances nervously toward the vault guard
          eng.actor(:rook).show_emote(:dots, duration: 0.70)
          eng.wait(0.35)
          eng.say(:ROOK, :panic, "That's the vault guard! That's Meridian's — look at it, it's drunk on the — get BACK—", hold: 1.25)

          eng.zoom_map(1.0, duration: 0.45, ease: :out)
          eng.letterbox(false, duration: 0.40)
          eng.wait(0.45)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE F (LIVE DIRECTOR'S CUT) — Ch8: "Five Bells" Caldera Crisis & Light Stone
      # Target Duration: ~34.5s (~1,035 frames @ 30fps)
      # Live Maps: Canon Built Map 255 (Cindervault Tap Chamber) -> Map 928
      #            (Midnight Hearthguild Hall stand-in; swaps 928->244)!
      # Canon: story/29_SCRIPT_CH8.md ("Five Bells", "Three Doctors", "Whose Is It")
      # Restraint: <= 3 emotes | 0px static portraits | grounded PC | 0 MS-Paint shapes!
      #=========================================================================
      def play_ch8_caldera(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I (0.0–17.5s) — "FIVE BELLS" & TAP SEVEN CRISIS (Canon Map 255!)
          #---------------------------------------------------------------------
          eng.transfer_map(255, 13.0, 12.2, hide_player: true)
          # Hide static NPC events (4..9); KEEP ev[10] Gauge ring & ev[11] Emergency lever!
          [4, 5, 6, 7, 8, 9].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(-14, -30, -44, 14, duration: 0.0)
          eng.set_emergency_vignette([218, 62, 22], max_alpha: 46, pulse_hz: 0.85)
          eng.letterbox(true, height: 32, duration: 0.0)

          # Three Doctors + Hammer Bomber + Litwick cleanly staged on Map 255 steel catwalks!
          eng.spawn_actor(:wick,    sheet: "WICK",    tx: 8.6,  ty: 13.0, dir: :right, is_charset: true)
          eng.spawn_actor(:quent,   sheet: "QUENT",   tx: 18.0, ty: 13.0, dir: :left,  is_charset: true)
          eng.spawn_actor(:dir1,    sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 17.8, ty: 10.0, dir: :down, is_charset: true)
          eng.spawn_actor(:dir2,    sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 19.0, ty: 10.0, dir: :down, is_charset: true)
          eng.spawn_actor(:bomber,  sheet: "trainer_HOLLOW_ADMIN",         tx: 13.0, ty: 8.2,  dir: :down, is_charset: true)
          eng.spawn_actor(:litwick, sheet: "Followers/LITWICK",            tx: 10.2, ty: 15.6, dir: :up,   is_charset: true)

          # Blinking brass Splitter strapped to Tap Seven collar + rising volcanic embers & steam!
          eng.spawn_vfx(:tap_splitter, sheet: "pf_vfx_splitter_beacon", tx: 13.0, ty: 8.9,
                        grid: [4, 1], frames: [0, 1, 2, 1], ticks: [6, 6, 6, 6], loops: :forever,
                        blend: :add, opacity: 220, scale: 0.78, z_layer: :above)
          [[11.4, 10.6, 0], [14.6, 10.6, 2], [13.0, 9.8, 1]].each_with_index do |(ex, ey, ph), ei|
            eng.spawn_vfx(:"caldera_ember_#{ei}", sheet: "pf_vfx_ch8_caldera_fx", tx: ex, ty: ey,
                          grid: [4, 2], frames: [ph % 4, (ph + 1) % 4, (ph + 2) % 4, (ph + 3) % 4],
                          ticks: [8, 8, 8, 8], loops: :forever,
                          blend: :add, opacity: 155, scale: 1.05, z_layer: :above)
          end

          # Brann, Sigrun, grounded PC, and Larch hurry up from the south service stair!
          eng.spawn_actor(:brann,  sheet: "BRANN",    tx: 11.4, ty: 16.4, dir: :up, is_charset: true)
          eng.spawn_actor(:sigrun, sheet: "SIGRUN",   tx: 12.6, ty: 16.6, dir: :up, is_charset: true)
          eng.spawn_actor(:pc,     sheet: "PLAYER_A", tx: 13.8, ty: 16.8, dir: :up, is_charset: true)
          eng.spawn_actor(:larch,  sheet: "LARCH",    tx: 15.0, ty: 16.6, dir: :up, is_charset: true)

          # THE FIVE BELLS: 1... 2... 3... 4... [0.90s dread pause] ...5!
          4.times do |bi|
            eng.play_se("ch8_foundry_bell", volume: 86, pitch: 100)
            eng.shake(power: 2, duration: 0.16)
            eng.wait(0.42)
          end
          eng.wait(0.68)
          eng.play_se("ch8_foundry_bell", volume: 100, pitch: 90)
          eng.shake(power: 5, duration: 0.36)
          eng.flash(color: [255, 168, 88], power: 110, duration: 0.24)

          eng.play_bgm("ch8_caldera_crisis", volume: 82, tag: "ch8_caldera_crisis")
          eng.actor(:brann).move_to(11.4, 14.2,  duration: 0.90, walk: true, dir: :up)
          eng.actor(:sigrun).move_to(12.6, 14.2, duration: 0.95, walk: true, dir: :up)
          eng.actor(:pc).move_to(13.8, 14.2,     duration: 1.00, walk: true, dir: :up)
          eng.actor(:larch).move_to(15.0, 14.2,  duration: 0.95, walk: true, dir: :up)
          eng.wait(0.45)

          eng.say(nil, :neutral, "FIVE! Off the mountain! FIVE!", hold: 0.65, name: "Bell-Ringer")

          # Emote #1 of 3: Larch alarmed checking the pressure gauge ring!
          eng.actor(:larch).show_emote(:exclaim, duration: 0.55)
          eng.play_se("Exclaim", volume: 78)
          eng.say(:BRANN, :angry, "That's the tap! Imelda, the gauge—what's it say?", hold: 0.72)
          eng.say(:LARCH, :shocked, "It's in the red and still climbing. Under an hour.", hold: 0.75)
          eng.say(:BRANN, :sad, "To the mountain doing what mountains do.", hold: 0.75)

          # Zoom up toward the steaming magma core & Hammer Bomber strapping the Splitter to Tap Seven!
          eng.zoom_map(1.26, duration: 0.85, focus: [13.0, 10.6], ease: :in_out)
          eng.wait(0.40)
          eng.say(nil, :neutral, "They'll cover up a fever. They can't cover up a mountain! There were families in the Lowlight!", hold: 0.95, name: "Hammer Bomber")

          eng.zoom_map(1.0, duration: 0.45, ease: :out)
          eng.say(:BRANN, :angry, "TAP SEVEN. DESTINATION: RIMEHOLT. Our fire, piped over the mountains—and none of us was asked!", hold: 0.95)

          # Grounded PC takes ONE calm half-step to the rail; magma pressure surges -> ALL-CLEAR SINGLE BELL!
          eng.actor(:pc).move_to(13.8, 13.7, duration: 0.45, walk: true, dir: :up)
          eng.wait(0.50)
          eng.bgm_cut
          eng.play_se("ch8_foundry_bell", volume: 92, pitch: 112)
          eng.flash(color: [16, 14, 18], power: 240, duration: 0.55)
          eng.wait(0.45)

          #---------------------------------------------------------------------
          # ACT II–III (17.5–34.8s) — MIDNIGHT HEARTHGUILD HALL: "WHOSE IS IT"
          #   Live Map 928 (dark central basalt table stand-in; swaps 928->244)
          #---------------------------------------------------------------------
          eng.clear_vignette
          eng.transfer_map(928, 11.5, 10.4, hide_player: true)
          $game_map.events.each do |eid, ev|
            ev.transparent = true if eid >= 3
          end
          # Legible dark-stone midnight tone (keeps crimson banners, lanterns, floor masonry & dark basalt table crisp!)
          eng.set_tone(-10, -14, -12, 16, duration: 0.0)

          # Envoy Haskar & 2 Ashkaar oath-guards caught beside the dark basalt table lifting the Light Stone!
          eng.spawn_actor(:haskar, sheet: "NPC 05",              tx: 11.5, ty: 7.4, dir: :down, is_charset: true)
          eng.spawn_actor(:guard1, sheet: "pfw_soldier_ashkaar", tx: 9.8,  ty: 7.6, dir: :down, is_charset: true)
          eng.spawn_actor(:guard2, sheet: "pfw_soldier_ashkaar", tx: 13.2, ty: 7.6, dir: :down, is_charset: true)

          # Pure-pixel faceted cold-white Light Stone glowing upward from the dark basalt table!
          eng.spawn_vfx(:light_stone, sheet: "pf_vfx_ch8_caldera_fx", tx: 11.5, ty: 9.1,
                        grid: [4, 2], frames: [4, 5, 6, 7], ticks: [9, 9, 9, 9], loops: :forever,
                        blend: :add, opacity: 225, scale: 0.95, z_layer: :above)

          eng.flash(color: [0, 0, 0], power: 220, duration: 0.50)
          eng.wait(0.55)
          eng.say(nil, :neutral, "The Warden was occupied. The city was in danger. The Stone was safest with—", hold: 0.72, name: "Envoy Haskar")

          # Guttural Salamence growl from the dark yard door! Sigrun steps in backlit by caldera embers!
          eng.play_cry(:SALAMENCE, volume: 96)
          eng.shake(power: 4, duration: 0.30)
          eng.spawn_vfx(:door_embers, sheet: "pf_vfx_ch8_caldera_fx", tx: 11.5, ty: 13.4,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [9, 9, 9, 9], loops: :forever,
                        blend: :add, opacity: 145, scale: 1.0, z_layer: :above)
          eng.spawn_actor(:sigrun,    sheet: "SIGRUN",              tx: 11.5, ty: 14.4, dir: :up, is_charset: true)
          eng.spawn_actor(:salamence, sheet: "Followers/SALAMENCE", tx: 13.4, ty: 14.6, dir: :up, is_charset: true)
          eng.spawn_actor(:pc,        sheet: "PLAYER_A",            tx: 10.2, ty: 14.4, dir: :up, is_charset: true)

          eng.actor(:sigrun).move_to(11.5, 12.2,    duration: 0.75, walk: true, dir: :up)
          eng.actor(:salamence).move_to(13.4, 12.6, duration: 0.85, walk: true, dir: :up)
          eng.actor(:pc).move_to(10.2, 12.6,        duration: 0.85, walk: true, dir: :up)
          eng.wait(0.85)
          eng.actor(:sigrun).set_pose("act_ch8_sigrun_brann", 0) # Commanding doorway stance!

          # Emote #2 of 3: Envoy Haskar jolts caught red-handed!
          eng.actor(:haskar).show_emote(:exclaim, duration: 0.55)
          eng.play_se("Exclaim", volume: 82)
          eng.wait(0.30)

          eng.say(:SIGRUN, :angry, "Say true, Haskar.", hold: 0.75)
          eng.say(nil, :neutral, "...The Dominar told me to take it while everyone was looking at the mountain.", hold: 0.90, name: "Envoy Haskar")
          eng.say(:SIGRUN, :neutral, "Thank you. Put it down.", hold: 0.72)

          # Light Stone settles cleanly on the basalt table; exhausted Brann enters under solitary burden theme!
          eng.play_se("Anim/HealBell", volume: 78, pitch: 128)
          eng.flash(color: [220, 240, 255], power: 115, duration: 0.35)
          eng.play_bgm("ch8_lightstone_burden", volume: 80, tag: "ch8_lightstone_burden")

          eng.spawn_actor(:brann, sheet: "BRANN", tx: 7.4, ty: 11.4, dir: :right, is_charset: true)
          eng.actor(:brann).move_to(8.8, 10.8, duration: 0.85, walk: true, dir: :right)
          eng.wait_for_move(:brann)
          eng.actor(:brann).play_clip(
            sheet: "act_ch8_sigrun_brann", grid: [4, 1], frames: [2, 3],
            ticks: [16, 40], loops: 1, stay: true
          )
          # Emote #3 of 3: Brann's quiet exhausted grief beside the glowing stone
          eng.actor(:brann).show_emote(:dots, duration: 0.85)
          eng.zoom_map(1.26, duration: 1.00, focus: [11.0, 10.6], ease: :in_out)
          eng.wait(0.95)

          eng.say(:BRANN, :sad, "Thirty years it's been on that wall. I was carrying a woman's grandmother up four hundred steps.", hold: 1.00)

          eng.actor(:sigrun).set_pose("act_ch8_sigrun_brann", 1) # Turns calmly toward grounded PC!
          eng.say(:SIGRUN, :neutral, "My father will send another envoy, and one day a legion. Say it. Who should keep it?", hold: 1.15)

          eng.wait(0.65)
          eng.zoom_map(1.0, duration: 0.45, ease: :out)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.45)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #-------------------------------------------------------------------------
      # SCENE 2 — Ch9 Peak #2 (DIRECTOR'S CUT v4 — TRUE 10/10 CINEMA):
      # "Trevenant's Ingrain, The 3-Wave Breach, 90° Unmasking & Arrival Epilogue"
      # Live Map 295 (Gen 5 B2W2 Crimson Emergency Reliquary; Wednesday swaps
      # map_id: 295 -> 264) + 90-degree Banquet-style Side-View Cathedral Cut!
      # ZERO Protagonist during Acts I-VI (pure 4-cast cinema: Mourner, Trevenant,
      # Juno, Nell); Protagonist walks naturally in from the south entrance ONLY
      # in Act VII after the unmasking reveal!
      #-------------------------------------------------------------------------
      def play_ch9_trevenant_unmasking(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          # Helper lambdas for exact pixel staging during the 90-degree side-view cut
          s2t_foot = proc { |sx, sy| eng.screen_to_tile(sx, sy) }
          s2t_ctr  = proc { |sx, sy| eng.screen_to_tile(sx, sy + 16) }

          #=====================================================================
          # ACT I — Reliquary Sabotage & Juno's Heroic Leap to Shield Nell!
          #         (ZERO Protagonist! $game_player.transparent = true)
          #=====================================================================
          eng.transfer_map(295, 15.0, 11.4, hide_player: true)
          eng.set_tone(-28, -86, -78, 42, duration: 0.0)
          eng.set_emergency_vignette([216, 28, 38], max_alpha: 74, pulse_hz: 1.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch9_tension", volume: 80, tag: "ch9_tension")

          # Tactical vertical aisle layout (NORTH -> SOUTH, 100% spatial continuity):
          #   Reliquary Plinth (15.0, 10.4) — fires crimson crystal spears SOUTHWARD
          #   5-Tile Ingrain Root Wall (y = 14.65) — erupts NORTH of Trevenant!
          #   Trevenant (15.0, 16.35) — 100% Row 3 UP-facing (NORTH) back view on all 16 frames!
          #   Mourner (15.0, 18.02) — dives in front of Juno & Nell, spins NORTH, throws UPWARD!
          #   Nell starts exposed in center aisle (15.0, 19.55); Juno leaps from (13.5, 19.80)
          #   right in front of Nell (15.0, 19.12) to shield her with her body!
          eng.spawn_vfx(:reliquary, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [0, 1], ticks: [10, 10], loops: :forever,
                        blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          eng.spawn_actor(:mourner, sheet: "act_ch9_mourner_throw_up", tx: 15.0, ty: 11.7,
                          grid: [4, 4], is_charset: false)
          eng.spawn_actor(:juno, sheet: "JUNO",   tx: 13.5, ty: 19.80, dir: :up, is_charset: true)
          eng.spawn_actor(:nell, sheet: "NPC 02", tx: 15.0, ty: 19.55, dir: :up, is_charset: true)

          # Mourner frantically pulling Splitter wires off the Fist Plate Reliquary!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [0, 1, 0, 1],
            ticks: [7, 7, 6, 6], loops: 1, stay: true
          )
          eng.zoom_map(1.44, duration: 1.0, focus: [15.0, 10.9], ease: :in_out)
          eng.wait(1.08)

          # Audio Vacuum #1: dry CLICK on the last Splitter -> Emote #1 (!) on Mourner ONLY!
          eng.bgm_cut
          eng.stop_vfx(:reliquary)
          eng.spawn_vfx(:reliquary_arm, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [2], hold: 0.65, stay: :forever,
                        blend: :normal, untoned: true, z_layer: :mid, origin: :foot)
          eng.play_se("Battle catch click", volume: 100, pitch: 130)
          eng.actor(:mourner).show_emote(:exclaim, duration: 0.55)
          eng.wait(0.42)

          # Partial Fist Plate Shatter! Bell chime + crimson shockwave ring!
          eng.stop_vfx(:reliquary_arm)
          eng.spawn_vfx(:reliquary_crack, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [3, 4, 5, 6, 7], ticks: [4, 6, 6, 6, 6],
                        loops: :forever, blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          eng.play_se("Anim/HealBell", volume: 95, pitch: 72)
          eng.play_se("Anim/Ice8", volume: 95)
          eng.play_bgm("ch9_tension", volume: 86, tag: "ch9_tension")
          eng.flash_ramp(color: [255, 196, 208], steps: [51, 136, 221, 255], step_dur: 0.03, hold_dur: 0.10, fade_dur: 0.35)
          eng.shake(power: 5, duration: 0.45)
          eng.spawn_vfx(nil, sheet: "pf_vfx_shockwave_ring", tx: 15.0, ty: 10.6,
                        grid: [4, 2], frames: 4..7, ticks: [3, 3, 4, 4],
                        blend: :add, scale: 1.0, grow: [0.6, 3.2, 0.7], fade: 0.25, z_layer: :above)
          eng.zoom_map(1.0, duration: 0.42, ease: :out)
          eng.wait(0.42)

          # Crimson glass frost races SOUTH down the central carpet toward exposed Nell!
          eng.pan_camera_to(15.0, 15.9, duration: 1.05, ease: :in_out)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [2, 3], ticks: [4, 6]
          )
          [11.9, 13.0, 14.1, 15.2, 16.3].each_with_index do |gy, gi|
            [-1.1, 0.0, 1.1].each do |gx|
              eng.spawn_vfx(nil, sheet: "pf_vfx_glass_frost", tx: 15.0 + gx, ty: gy,
                            grid: [4, 2], frames: 4..7, ticks: [2, 2, 3, 3],
                            stay: :forever, blend: :normal, opacity: 140, scale: 0.88, z_layer: :floor)
            end
            if gi == 3
              # Exposed Nell freezes trembling in the center aisle!
              eng.actor(:nell).tremble(duration: 1.35, amp: 2.0, freq: 48.0)
            end
            eng.play_se("Anim/Ice2", volume: 70, pitch: 95 + gi * 6) if gi.even?
            eng.wait(0.15)
          end

          # Multi-Box Sabotage & Shielding Beat:
          # Box 1 (Juno, shocked): "Wait—the glass—"
          eng.say(:JUNO, :shocked, "Wait—the glass—", hold: 0.58)
          eng.wait(0.14)

          # Juno spots Nell exposed in the center aisle (Emote #2 !!), sprints & LEAPS right in front of Nell!
          eng.actor(:juno).show_emote(:double_exclaim, duration: 0.75)
          eng.play_se("Exclaim", volume: 95)
          eng.actor(:juno).set_dir(:right)
          eng.wait(0.14)
          eng.actor(:juno).move_to(14.15, 19.55, duration: 0.16, walk: true, dir: :right)
          eng.wait_for_move(:juno)

          # HEROIC JUMP ARC: Juno physically leaps across flagstones directly in front of Nell!
          eng.play_se("Player jump", volume: 92)
          eng.actor(:juno).move_to(15.0, 19.12, duration: 0.34, walk: false, dir: :right, arc_h: 24.0, ease: :out_cubic)
          eng.actor(:nell).move_to(14.85, 19.82, duration: 0.24, walk: true, dir: :up)
          eng.actor(:nell).crouch_to(3, duration: 0.20)
          eng.actor(:nell).tremble(duration: 0.90, amp: 2.0, freq: 46.0)
          eng.wait_for_move(:juno)

          # Juno lands shielding Nell with her body (pose_JUNO :flinch + protective crouch)!
          eng.play_se("Player bump", volume: 78, pitch: 90)
          eng.shake(power: 2, duration: 0.12)
          eng.actor(:juno).set_pose("pose_JUNO", 1)
          eng.actor(:juno).crouch_to(4, duration: 0.12)

          # Box 2 (Juno, panic): "NELL!!"
          eng.say(:JUNO, :panic, "NELL!!", hold: 0.45)
          eng.wait(0.12)
          # Box 3 (Juno, panic): "Get down—!!"
          eng.say(:JUNO, :panic, "Get down—!!", hold: 0.58)

          #=====================================================================
          # ACT II — Mourner's Dive South, Spin-Turn NORTH & UPWARD Dusk Ball Throw!
          #=====================================================================
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [3, 4, 4, 5],
            ticks: [3, 4, 4, 5], se: { 1 => "Fly" }
          )
          eng.actor(:mourner).move_to(15.0, 18.02, duration: 0.56, walk: false, arc_h: 24.0, ease: :out_cubic)
          eng.wait_for_move(:mourner)
          eng.shake(power: 3, duration: 0.18)
          eng.actor(:juno).restore_charset("JUNO", dir: :up)
          eng.wait(0.16)

          # Mourner faces UP (NORTH) & whips arm UPWARD launching Dusk Ball NORTHWARD!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [6, 7, 8, 9],
            ticks: [5, 7, 3, 7],
            se: { 2 => "Battle throw" }
          )
          eng.wait(0.60) # Launch ball right on frame 8 upward whip smear!
          eng.spawn_vfx(nil, sheet: "pf_vfx_duskball_release", tx: 15.0, ty: 17.9,
                        grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: 3,
                        blend: :normal, untoned: true, move_to: [15.0, 16.35, 0.42],
                        arc_h: 36.0, z_layer: :above)
          eng.wait(0.42)

          # Dusk Ball pops open at vanguard tile (15.0, 16.35) -> UP-FACING TREVENANT MATERIALIZES!
          eng.play_se("Battle ball drop", volume: 90)
          eng.play_se("Anim/Darkness6", volume: 88, pitch: 115)
          eng.spawn_vfx(nil, sheet: "pf_vfx_duskball_release", tx: 15.0, ty: 16.35,
                        grid: [4, 2], frames: 4..7, ticks: [2, 3, 3, 3],
                        blend: :add, scale: 1.4, z_layer: :above)
          eng.spawn_actor(:trevenant, sheet: "act_ch9_trevenant_ingrain_up", tx: 15.0, ty: 16.35,
                          grid: [4, 4], is_charset: false, z_bias: 8)
          eng.play_cry(:TREVENANT, volume: 100)

          #=====================================================================
          # ACT III — UP-FACING TREVENANT INGRAIN SLAM & 5-TILE NORTH ROOT WALL!
          #=====================================================================
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: 0..8,
            ticks: [4, 4, 5, 7, 10, 2, 6, 6, 6],
            se: { 6 => "Anim/Earth4", 7 => "Anim/LeechSeedPlanted" },
            shake: { 6 => [6, 0.45] },
            flash: { 6 => [[168, 255, 176], 125, 0.22] },
            on_frame: {
              6 => proc do |e, _a, _fi|
                # 5-tile gnarled emerald Ingrain Root Wall erupts NORTH of Trevenant (y = 14.65)!
                [15.0, 14.0, 16.0, 13.0, 17.0].each_with_index do |rx, ri|
                  e.spawn_vfx(:"root_#{ri}", sheet: "pf_vfx_ingrain_roots", tx: rx, ty: 14.65,
                              grid: [4, 2], frames: [0, 1, 2, 3, 4],
                              ticks: [2 + ri, 3, 3, 4, 8], stay: :forever,
                              blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
                end
              end
            }
          )
          # Mourner spreads both arms wide facing NORTH shielding Juno & Nell behind him!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [10], ticks: [20], stay: true
          )
          eng.wait_for_clip(:trevenant)
          eng.wait(0.24)

          #=====================================================================
          # ACT IV — 3 ESCALATING BARRAGE WAVES (TIGHT 4-CAST DRAMA, ZERO SPAM!)
          #=====================================================================

          # --- WAVE 1: HOLD! (Two-volley 6 crimson spears -> emerald deflects) ---
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [8, 9, 8, 9, 8, 9, 8],
            ticks: [7, 6, 7, 6, 7, 6, 14], stay: true
          )
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [10, 11, 10, 11],
            ticks: [10, 12, 10, 20], stay: true
          )
          w1_pairs = [
            [13.0, 3], [17.0, 4], [15.0, 0],
            [14.0, 1], [16.0, 2], [15.0, 0]
          ]
          w1_pairs.each_with_index do |(sx, ri), si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: sx, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.15, move_to: [sx, 14.15, 0.28], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 78, pitch: 106 + si * 4) if si.even?
            eng.wait(0.22)
            eng.stop_vfx(:"root_#{ri}")
            eng.stop_vfx(:"root_w1_#{ri}")
            eng.spawn_vfx(:"root_w1_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: sx, ty: 14.65,
                          grid: [4, 2], frames: [0], hold: 0.45, stay: :forever,
                          blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: sx, ty: 14.05,
                          grid: [4, 2], frames: [7], hold: 0.14, blend: :add, scale: 0.72, z_layer: :above)
            if si == 2 || si == 5
              eng.shake(power: 4, duration: 0.28)
              eng.play_se("Anim/hit", volume: 88, pitch: 112 + si * 2)
              eng.flash(color: [164, 255, 184], power: 82, duration: 0.16)
              eng.actor(:nell).tremble(duration: 0.35, amp: 2.0)
            end
            eng.wait(0.12) if si == 2
          end
          eng.play_se("Anim/Ice8", volume: 76, pitch: 120)
          eng.zoom_map(1.15, duration: 0.75, focus: [15.0, 15.7], ease: :in_out)
          eng.wait(0.80)

          # --- WAVE 2: OVERWHELMING! (Cracks spread -> splinters -> Multi-Box!) ---
          eng.set_tone(-42, -96, -84, 52, duration: 0.85)
          eng.set_emergency_vignette([232, 24, 38], max_alpha: 92, pulse_hz: 2.0)
          eng.play_se("Anim/Earth1", volume: 84, pitch: 88)
          eng.wait(0.24)

          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [10, 11, 10, 11, 10, 11, 10, 11],
            ticks: [6, 6, 6, 6, 6, 6, 6, 10], stay: true
          )
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [11, 12, 11, 12, 11, 12],
            ticks: [7, 7, 7, 7, 7, 14], stay: true
          )

          w2_specs_a = [
            [14.8, 13.0], [15.2, 17.0], [14.6, 14.0], [15.4, 16.0],
            [15.0, 15.0], [14.2, 13.4], [15.8, 16.6], [15.0, 15.0]
          ]
          w2_specs_a.each_with_index do |(x0, x1), si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: x0, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.24, move_to: [x1, 14.15, 0.24], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 84, pitch: 102 + si * 4) if si.even?
            if si == 3
              # Glowing crimson stress cracks spread across the emerald barrier!
              5.times { |ri| eng.stop_vfx(:"root_w1_#{ri}"); eng.stop_vfx(:"root_#{ri}") }
              [15.0, 14.0, 16.0, 13.0, 17.0].each_with_index do |rx, ri|
                eng.spawn_vfx(:"root_w2_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.65,
                              grid: [4, 2], frames: [1], hold: 0.4, stay: :forever,
                              blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
              end
              eng.shake(power: 5, duration: 0.34)
              eng.play_se("Anim/Ice8", volume: 82, pitch: 106)
              eng.actor(:trevenant).flash_color(255, 110, 140, 170, duration: 0.20)
            elsif si == 7
              # Center tiles crack deep crimson + emerald bark splinters shower south!
              [0, 1, 2].each { |ri| eng.stop_vfx(:"root_w2_#{ri}") }
              [15.0, 14.0, 16.0].each_with_index do |rx, ri|
                eng.spawn_vfx(:"root_w2b_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.65,
                              grid: [4, 2], frames: [2], hold: 0.4, stay: :forever,
                              blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
                eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.8,
                              grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                              scale: 0.56, drift: [(ri - 1) * 34, 68], gravity: 110, z_layer: :above)
              end
              eng.play_se("Anim/Ice8", volume: 92, pitch: 90)
              eng.play_cry(:TREVENANT, volume: 84)
              eng.shake(power: 6, duration: 0.42)
              eng.actor(:trevenant).flash_color(255, 180, 200, 200, duration: 0.24)
              # Juno ducks tighter shielding Nell (pose_JUNO :flinch + crouch):
              eng.actor(:juno).set_pose("pose_JUNO", 1)
              eng.actor(:juno).crouch_to(5, duration: 0.12)
            end
            eng.wait(0.17)
          end
          eng.wait(0.24)

          # Wave 2 Multi-Box Dialogue Beat:
          # Box 4 (Juno, panic): "The roots—they're splintering!!"
          eng.say(:JUNO, :panic, "The roots—they're splintering!!", hold: 0.72)

          # Wave 2 SLAMS HARDER between boxes!
          [[14.0, 14.0], [16.0, 16.0], [14.8, 14.8], [15.2, 15.2]].each_with_index do |(x0, x1), si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: x0, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.32, move_to: [x1, 14.15, 0.21], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 88, pitch: 112 + si * 6) if si.even?
            if si == 2
              eng.play_se("Anim/Ice8", volume: 92, pitch: 86)
              eng.shake(power: 6, duration: 0.36)
              eng.actor(:trevenant).flash_color(255, 196, 210, 210, duration: 0.22)
              eng.actor(:nell).tremble(duration: 0.65, amp: 2.0)
            end
            eng.wait(0.14)
          end
          eng.actor(:juno).restore_charset("JUNO", dir: :up)
          eng.wait(0.14)

          # Box 5 (Juno, shocked): "Hold on! Please, hold on—"
          eng.say(:JUNO, :shocked, "Hold on! Please, hold on—", hold: 0.72)

          # --- WAVE 3: PENETRATION!! Center root wall BLOWS OPEN! ---
          eng.zoom_map(1.28, duration: 0.70, focus: [15.0, 15.9], ease: :in_out)
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [11, 10, 12, 13],
            ticks: [6, 6, 10, 18], stay: true
          )
          w3_xs = [14.0, 16.0, 14.6, 15.4, 15.0, 14.8, 15.2, 15.0]
          w3_xs.each_with_index do |sx, si|
            eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: sx, ty: 10.5,
                          grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                          blend: :add, scale: 1.32, move_to: [sx, 14.2, 0.21], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 88, pitch: 116 + si * 4) if si.even?
            if si == 4
              eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: 15.0, ty: 14.7,
                            grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                            scale: 0.62, drift: [10, 75], gravity: 115, z_layer: :above)
              eng.shake(power: 5, duration: 0.25)
            end
            eng.wait(0.13)
          end
          eng.wait(0.12)

          # BLOWN-OPEN JAGGED BREACH GAP IN CENTER ROOT WALL (x = 15.0)!!
          eng.stop_vfx(:root_w2b_0)
          eng.spawn_vfx(:root_breach_center, sheet: "pf_vfx_ingrain_roots_breach", tx: 15.0, ty: 14.65,
                        grid: [4, 2], frames: [3], hold: 1.0, stay: :forever,
                        blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
          3.times do |bi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: 14.6 + bi * 0.4, ty: 14.8,
                          grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                          scale: 0.70, drift: [(bi - 1) * 48, 88], gravity: 130, z_layer: :above)
          end
          eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: 15.0, ty: 14.4,
                        grid: [4, 2], frames: [7], hold: 0.22, blend: :add, scale: 0.95, z_layer: :above)
          eng.play_se("Anim/Explosion2", volume: 96)
          eng.play_se("Anim/Ice8", volume: 98, pitch: 84)
          eng.play_cry(:TREVENANT, volume: 92)
          eng.flash(color: [255, 196, 212], power: 190, duration: 0.22)
          eng.shake(power: 7, duration: 0.48)
          eng.actor(:trevenant).flash_color(255, 220, 232, 220, duration: 0.24)
          eng.wait(0.42) # Horror beat letting the smoking breached center gap register!

          # Stray spear + FATAL JAGGED SPEAR punching STRAIGHT THROUGH THE BREACH toward Juno & Nell!
          eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: 14.7, ty: 13.8,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 3,
                        blend: :add, scale: 1.25, move_to: [14.2, 18.4, 0.28], z_layer: :above)
          eng.play_se("Anim/Slash9", volume: 86, pitch: 115)
          eng.wait(0.18)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_throw_up", grid: [4, 4], frames: [12, 14, 15],
            ticks: [3, 3, 4], stay: true
          )
          # Juno throws arms over Nell!
          eng.actor(:juno).set_pose("pose_JUNO", 1)
          eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: 15.0, ty: 13.6,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [2, 2, 2], loops: 4,
                        blend: :add, scale: 1.45, move_to: [15.0, 18.6, 0.36], z_layer: :above)
          eng.play_se("Anim/Ice2", volume: 96, pitch: 132)
          eng.wait(0.28)

          #=====================================================================
          # ACT V — 90-DEGREE BANQUET SIDE-VIEW CATHEDRAL CUT!
          #   - PURE 4-CAST CINEMA (ZERO Protagonist!):
          #       LEFT:  Vertical Ingrain Wall (sx=78) + LEFT-facing Trevenant (sx=152)
          #       MID:   Diving Mourner (sx=356 -> 274 -> 302)
          #       RIGHT: Shielding Juno (sx=388) + clearly visible trembling Nell (sx=444)
          #   - ZERO emote balloon clutter — pure physical acting & cinema!
          #   - ZERO DOUBLE-MASK: ONLY the single mask on Mourner's own face
          #     shatters at 1.55x pbZoomMap with crisp face-matched shards!
          #=====================================================================
          eng.flash(color: [255, 224, 236], power: 195, duration: 0.12)
          eng.clear_actors
          eng.clear_vfxs
          eng.zoom_map(1.0, duration: 0.0)
          eng.set_tone(0, 0, 0, 0, duration: 0.0)
          eng.set_backdrop("pf_vfx_ch9_sideview_hall", z: 1)

          # LEFT (sx = 78): Vertical side-profile Ingrain Root Wall cracking -> blowing open!
          wx, wy = s2t_foot.call(78, 318)
          eng.spawn_vfx(:side_wall, sheet: "pf_vfx_ingrain_wall_side", tx: wx, ty: wy,
                        grid: [4, 1], frames: [1, 2], ticks: [10, 10], stay: :forever,
                        blend: :normal, untoned: false, scale: 1.15, z_layer: :mid, origin: :foot)

          # LEFT-MID (sx = 152): Side-profile Trevenant (Row 1 LEFT) bracing against the storm!
          ttx, tty = s2t_foot.call(152, 312)
          eng.spawn_actor(:side_trev, sheet: "Followers/TREVENANT", tx: ttx, ty: tty,
                          dir: :left, grid: [4, 4], is_charset: true, scale: 2.0, z_bias: 20)

          # RIGHT-MID (sx = 388): Juno crouched physically shielding right in front of Nell!
          jtx, jty = s2t_foot.call(388, 314)
          eng.spawn_actor(:side_juno, sheet: "JUNO", tx: jtx, ty: jty,
                          dir: :left, grid: [4, 4], is_charset: true, scale: 2.0, z_bias: 26)
          eng.actor(:side_juno).off_y = 6.0

          # RIGHT (sx = 444): Nell clearly visible crouched & trembling right behind Juno!
          ntx, nty = s2t_foot.call(444, 310)
          eng.spawn_actor(:side_nell, sheet: "NPC 02", tx: ntx, ty: nty,
                          dir: :left, grid: [4, 4], is_charset: true, scale: 2.0, z_bias: 18)
          eng.actor(:side_nell).off_y = 6.0
          eng.actor(:side_nell).tremble(duration: 2.2, amp: 2.0, freq: 44.0)

          # Establish clean 4-character 90-deg cathedral as 3 horizontal spears hammer left wall!
          [[14, 206, 78, 212, 0.24], [8, 256, 80, 254, 0.24], [10, 238, 86, 240, 0.23]].each_with_index do |(x0, y0, x1, y1, dur), si|
            stx0, sty0 = s2t_ctr.call(x0, y0)
            stx1, sty1 = s2t_ctr.call(x1, y1)
            eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: stx0, ty: sty0,
                          grid: [4, 2], frames: [6], hold: dur, blend: :add, scale: 1.08,
                          move_to: [stx1, sty1, dur], z_layer: :above)
            eng.play_se("Anim/Ice2", volume: 88, pitch: 114 + si * 8)
            eng.shake(power: 4, duration: 0.18) if si == 1
            eng.wait(0.26)
          end

          # Side-profile vertical root wall BLOWS OPEN into Frame 3 jagged chest-height breach gap!
          eng.stop_vfx(:side_wall)
          eng.spawn_vfx(:side_wall_breach, sheet: "pf_vfx_ingrain_wall_side", tx: wx, ty: wy,
                        grid: [4, 1], frames: [3], hold: 1.0, stay: :forever,
                        blend: :normal, untoned: false, scale: 1.15, z_layer: :mid, origin: :foot)
          sp_x, sp_y = s2t_ctr.call(110, 240)
          eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: sp_x, ty: sp_y,
                        grid: [4, 2], frames: [4, 5], ticks: [3, 4], blend: :normal, untoned: true,
                        scale: 0.85, drift: [95, -18], gravity: 110, z_layer: :above)
          eng.play_se("Anim/Ice8", volume: 96, pitch: 88)
          eng.shake(power: 6, duration: 0.30)
          eng.actor(:side_trev).flash_color(255, 190, 210, 200, duration: 0.22)
          eng.actor(:side_trev).tremble(duration: 0.28, amp: 2.0, freq: 42.0)
          eng.wait(0.26)

          # ====================================================================
          # DEAD SILENCE (bgm_cut!) + FATAL SPEAR + SAKUGA SLOW-MO DIVE!!
          # ====================================================================
          eng.bgm_cut
          eng.play_se("Fly", volume: 90, pitch: 82)

          # Fatal horizontal blazing crimson spear rockets straight out of the breach!
          fsx0, fsy0 = s2t_ctr.call(90, 250)
          fsx1, fsy1 = s2t_ctr.call(264, 250)
          eng.spawn_vfx(:fatal_spear, sheet: "pf_vfx_ingrain_roots_breach", tx: fsx0, ty: fsy0,
                        grid: [4, 2], frames: [6], hold: 0.78, blend: :add, scale: 1.28,
                        move_to: [fsx1, fsy1, 0.74], z_layer: :above)

          # MOURNER LEAPS HORIZONTALLY INTO FRAME shielding BOTH Juno and Nell!
          mtx0, mty0 = s2t_foot.call(356, 312)
          mtx1, mty1 = s2t_foot.call(274, 312)
          eng.spawn_actor(:side_mourner, sheet: "act_ch9_mourner_dive_side", tx: mtx0, ty: mty0,
                          grid: [4, 2], is_charset: false, scale: 1.0, z_bias: 45)
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [0, 1, 2],
            ticks: [4, 6, 10], stay: true
          )
          eng.actor(:side_mourner).move_to(mtx1, mty1, duration: 0.76, walk: false, arc_h: 38.0, ease: :out_cubic)
          # Smooth 1.55x pbZoomMap centered directly onto Mourner's face for single-mask impact!
          eng.zoom_map(1.55, duration: 0.74, focus: :side_mourner, ease: :out_cubic)
          eng.wait(0.74)

          # 2-FRAME HIGH-CONTRAST B&W SILHOUETTE IMPACT + 0.25s HITSTOP FREEZE RIGHT ON HIS FACE!!
          eng.stop_vfx(:fatal_spear)
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [3], ticks: [20], stay: true
          )
          ix, iy = s2t_ctr.call(262, 254)
          eng.spawn_vfx(nil, sheet: "pf_vfx_ingrain_roots_breach", tx: ix, ty: iy,
                        grid: [4, 2], frames: [7], hold: 0.24, blend: :add, scale: 1.05, z_layer: :above)
          eng.play_se("Cut", volume: 100, pitch: 78)
          eng.play_se("Anim/Ice8", volume: 96, pitch: 118)
          eng.impact_beat(hitstop_sec: 0.25)
          eng.flash(color: [255, 242, 248], power: 235, duration: 0.22)
          eng.shake(power: 7, duration: 0.34)

          # SINGLE-MASK SLOW-MO SHATTER DIRECTLY OFF MOURNER'S FACE (ZERO DUPLICATE GIANT MASK!)
          eng.clear_vignette
          eng.set_tone(-44, -52, -40, 88, duration: 0.75)

          # Frame 4: Spiderweb crack right across the ONE mask on Mourner's own face!
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [4], ticks: [20], stay: true
          )
          mtx_c, mty_c = s2t_foot.call(282, 312)
          eng.actor(:side_mourner).move_to(mtx_c, mty_c, duration: 0.65, walk: false, ease: :out)
          eng.wait(0.32)
          eng.play_se("Anim/Ice2", volume: 84, pitch: 140) # Crisp porcelain crack in dead silence!
          gx, gy = s2t_ctr.call(266, 254)
          eng.spawn_vfx(nil, sheet: "pf_vfx_glass_shards", tx: gx, ty: gy,
                        grid: [4, 2], frames: [7], hold: 0.16, blend: :add, scale: 0.45, z_layer: :above)
          eng.wait(0.33)

          # Frame 5: Mask shears directly off Mourner's face exposing Rowan's bare eyes!
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [5], ticks: [16], stay: true
          )
          mtx_s, mty_s = s2t_foot.call(290, 312)
          eng.actor(:side_mourner).move_to(mtx_s, mty_s, duration: 0.55, walk: false, ease: :out)
          eng.wait(0.55)

          # Frame 6 -> Frame 7: Unmasked Rowan tumbles & drops to one knee!
          # Spawn ONLY crisp face-matched (scale 0.26) porcelain halves & lily petals flying OFF his face!
          eng.actor(:side_mourner).play_clip(
            sheet: "act_ch9_mourner_dive_side", grid: [4, 2], frames: [6, 7],
            ticks: [12, 40], stay: true
          )
          mtx2, mty2 = s2t_foot.call(302, 312)
          eng.actor(:side_mourner).move_to(mtx2, mty2, duration: 0.95, walk: false, ease: :out)

          # Spawn mask halves directly from Frame 5's sheared mask position (left of Rowan's bare face!)
          shx_l, shy_l = s2t_ctr.call(248, 254)
          shx_r, shy_r = s2t_ctr.call(262, 252)
          eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: shx_l, ty: shy_l,
                        grid: [4, 2], frames: [4], hold: 1.55, blend: :normal, untoned: true,
                        scale: 0.26, drift: [-58, -18], gravity: 58, spin: -115, fade: 0.28, z_layer: :above)
          eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: shx_r, ty: shy_r,
                        grid: [4, 2], frames: [5], hold: 1.55, blend: :normal, untoned: true,
                        scale: 0.26, drift: [26, -38], gravity: 54, spin: 96, fade: 0.28, z_layer: :above)
          [[244, 244, 6, -24, -12], [268, 240, 7, 22, -16], [254, 258, 6, -12, -4]].each_with_index do |(px, py, fr, vx, vy), pi|
            ptx, pty = s2t_ctr.call(px, py)
            eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: ptx, ty: pty,
                          grid: [4, 2], frames: [fr], hold: 1.75, blend: :normal, untoned: true,
                          scale: 0.28 + (pi % 2) * 0.04, drift: [vx, vy], gravity: 14,
                          spin: (pi.even? ? 28 : -24), fade: 0.35, z_layer: :above)
          end
          # Smoothly ease zoom back 1.55x -> 1.12x framing LEFT-facing Trevenant, kneeling Rowan, Juno & Nell!
          eng.zoom_map(1.12, duration: 1.15, focus: :side_mourner, ease: :out)
          eng.wait(1.40)

          #=====================================================================
          # ACT VI — Cut Back to Top-Down Map 295 & Intimate Unmasking Reveal!
          #          (STILL ZERO Protagonist — strictly Juno, Nell, Rowan & Trevenant!)
          #=====================================================================
          eng.clear_backdrop
          eng.clear_actors
          eng.clear_vfxs
          eng.set_camera_tile(15.0, 16.5)
          eng.set_tone(-34, -56, -48, 86, duration: 0.0) # Dying crimson fading to cool twilight!
          eng.zoom_map(1.34, duration: 0.0, focus: [15.0, 18.2])

          # Restore live scarred Map 295 aftermath: cracked Reliquary, floor frost, breached root wall!
          eng.spawn_vfx(:reliquary_after, sheet: "pf_vfx_fist_reliquary", tx: 15.0, ty: 10.4,
                        grid: [4, 2], frames: [5, 6, 7], ticks: [10, 10, 10], loops: :forever,
                        blend: :normal, untoned: false, z_layer: :mid, origin: :foot)
          [11.9, 13.0, 14.1, 15.2, 16.3].each do |gy|
            [-1.1, 0.0, 1.1].each do |gx|
              eng.spawn_vfx(nil, sheet: "pf_vfx_glass_frost", tx: 15.0 + gx, ty: gy,
                            grid: [4, 2], frames: [7], hold: 1.0, stay: :forever,
                            blend: :normal, opacity: 120, scale: 0.88, z_layer: :floor)
            end
          end
          [[13.0, 1], [14.0, 2], [15.0, 3], [16.0, 2], [17.0, 1]].each_with_index do |(rx, fr), ri|
            eng.spawn_vfx(:"root_after_#{ri}", sheet: "pf_vfx_ingrain_roots_breach", tx: rx, ty: 14.65,
                          grid: [4, 2], frames: [fr], hold: 1.0, stay: :forever,
                          blend: :normal, untoned: false, scale: 0.65, z_layer: :mid, origin: :foot)
          end

          # Scarred Trevenant remaining rooted facing NORTH toward the breached wall (100% Row 3 back view!)
          eng.spawn_actor(:trevenant, sheet: "act_ch9_trevenant_ingrain_up", tx: 15.0, ty: 16.35,
                          grid: [4, 4], is_charset: false, z_bias: 6)
          eng.actor(:trevenant).play_clip(
            sheet: "act_ch9_trevenant_ingrain_up", grid: [4, 4], frames: [14, 14, 15],
            ticks: [18, 18, 80], stay: true
          )

          # Juno & Nell matching exact side-view continuity (ZERO Protagonist!)
          eng.spawn_actor(:juno, sheet: "JUNO",   tx: 15.0,  ty: 19.35, dir: :up, is_charset: true)
          eng.actor(:juno).off_y = 4.0
          eng.spawn_actor(:nell, sheet: "NPC 02", tx: 14.55, ty: 19.85, dir: :up, is_charset: true)
          eng.actor(:nell).off_y = 3.0

          # Unmasked Rowan collapsing to his knees with head bowed deep (Frame 13)!
          eng.spawn_actor(:mourner, sheet: "act_ch9_mourner_unmask", tx: 15.0, ty: 18.0,
                          grid: [4, 4], is_charset: false, z_bias: 10)
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [9, 10, 13],
            ticks: [10, 12, 90], stay: true
          )

          # Broken porcelain mask half tumbles & CLATTERS clearly beside Rowan at (15.75, 18.42)!
          eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: 15.10, ty: 17.85,
                        grid: [4, 2], frames: [4], hold: 0.36, blend: :normal, untoned: true,
                        scale: 0.30, move_to: [15.75, 18.42, 0.36], arc_h: 18.0, spin: 180, z_layer: :above)
          eng.set_tone(-26, -30, -14, 112, duration: 2.1)
          eng.wait(0.36)

          # Dry ceramic clink as broken mask hits stone -> unobstructed split mask & white lily!
          eng.play_se("Anim/Ice8", volume: 74, pitch: 134)
          eng.spawn_vfx(:mask_floor, sheet: "pf_vfx_smoke_and_motes", tx: 15.75, ty: 18.42,
                        grid: [4, 2], frames: [6], hold: 1.0, stay: :forever,
                        blend: :normal, untoned: false, z_layer: :mid)

          # Subtle perimeter motes & drifting white lily petals (Rowan & lily 100% unobstructed!)
          6.times do |mi|
            mx = mi < 3 ? (12.2 + mi * 0.7) : (16.4 + (mi - 3) * 0.7)
            eng.spawn_vfx(nil, sheet: "pf_vfx_smoke_and_motes", tx: mx, ty: 19.2 - (mi % 3) * 0.9,
                          grid: [4, 2], frames: [7], hold: 16.0, blend: :add,
                          drift: [3 - (mi % 3) * 3, -10 - (mi % 4) * 2], fade: 1.4, z_layer: :above)
          end
          [[12.6, 16.5, 6], [16.9, 16.8, 7], [17.4, 18.4, 6]].each_with_index do |(px, py, fr), pi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: px, ty: py,
                          grid: [4, 2], frames: [fr], hold: 16.0, blend: :normal, untoned: true,
                          scale: 0.28, drift: [4 - pi * 3, 7], gravity: 1.2,
                          spin: (pi.even? ? 16 : -14), fade: 1.4, z_layer: :above)
          end

          # Nell uncrouches and peeks out trembling beside Juno in stunned silence!
          eng.wait(0.45)
          eng.actor(:nell).crouch_to(0, duration: 0.35)
          eng.actor(:nell).move_to(14.20, 19.65, duration: 0.42, walk: true, dir: :up)
          eng.actor(:nell).tremble(duration: 0.75, amp: 2.0, freq: 38.0)

          # Complete the 1.45s pure dead-silence hold after mask clatter!
          eng.wait(1.00)

          # Juno slowly rises from her crouch with Emote #3 (ONE quiet '...' balloon)!
          eng.actor(:juno).crouch_to(0, duration: 0.42)
          eng.actor(:juno).move_to(15.0, 19.18, duration: 0.42, walk: true, dir: :up)
          eng.actor(:juno).show_emote(:dots, duration: 0.95)
          eng.wait(0.45)

          # === INTIMATE 6-BOX EMOTIONAL REVEAL (Juno, Nell & Uncle Rowan) ===
          # Box 6 (Juno, shocked): "...Wait." (0.75s silent beat!)
          eng.say(:JUNO, :shocked, "...Wait.", hold: 0.80)
          eng.wait(0.75)

          # Box 7 (Juno, crying): "...That voice..."
          eng.say(:JUNO, :crying, "...That voice...", hold: 0.90)

          # Rowan slowly lifts his bare face; Never Meant to Belong solo violin softly enters!
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [13, 14, 15, 12],
            ticks: [5, 9, 10, 140], stay: true
          )
          eng.play_bgm("ch9_never_meant", volume: 82, tag: "ch9_never_meant")
          eng.wait(0.55)

          # Box 8 (Juno, crying): "...Uncle Rowan?"
          eng.say(:JUNO, :crying, "...Uncle Rowan?", hold: 1.05)

          # Quiet violin pause — Nell shifts softly in disbelief (zero balloons, zero alert ping!)
          eng.actor(:nell).hop(height: 5, duration: 0.18)
          eng.wait(0.75)

          # Box 9 (Rowan, sad): "Juno..." (0.55s pause)
          eng.say(:ROWAN, :sad, "Juno...", hold: 0.75)
          eng.wait(0.55)

          # Box 10 (Rowan, sad): "Don't look at me like that."
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [15], ticks: [80], stay: true
          )
          eng.say(:ROWAN, :sad, "Don't look at me like that.", hold: 1.02)

          # Fresh delicate white lily petals drift across the twilight hall
          [[13.4, 16.8, 6], [16.5, 17.2, 7], [15.9, 18.2, 6]].each_with_index do |(px, py, fr), pi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_mask_shatter_side", tx: px, ty: py,
                          grid: [4, 2], frames: [fr], hold: 10.0, blend: :normal, untoned: true,
                          scale: 0.28, drift: [3 - pi * 2, 7], gravity: 1.0,
                          spin: (pi.even? ? 14 : -12), fade: 1.2, z_layer: :above)
          end
          eng.wait(0.55)

          # Box 11 (Rowan, neutral): "Look at the flowers."
          eng.actor(:mourner).play_clip(
            sheet: "act_ch9_mourner_unmask", grid: [4, 4], frames: [12], ticks: [200], stay: true
          )
          eng.say(:ROWAN, :neutral, "Look at the flowers.", hold: 1.25)

          #=====================================================================
          # ACT VII — POST-UNMASKING ARRIVAL EPILOGUE!
          #           Camera pulls back to reveal the south entrance;
          #           Protagonist walks naturally into the shattered clearing
          #           AFTER the event, teeing up post-cutscene gameplay!
          #=====================================================================
          eng.zoom_map(1.0, duration: 1.05, focus: [15.0, 18.5], ease: :in_out)
          eng.pan_camera_to(15.0, 19.2, duration: 1.05, ease: :in_out)
          eng.wait(1.35)

          # Protagonist enters naturally from offscreen south entrance (crisp B2W2 walk stride!)
          eng.spawn_actor(:pc, sheet: "PLAYER_A", tx: 15.35, ty: 25.0, dir: :up, is_charset: true)
          eng.actor(:pc).move_to(15.35, 20.65, duration: 2.05, walk: true, dir: :up, ease: :linear)
          eng.wait(1.15)
          # Hearing footsteps, Juno turns south (keeping close to Nell), then Nell turns too!
          eng.actor(:juno).set_dir(:down)
          eng.wait(0.18)
          eng.actor(:nell).set_dir(:down)
          eng.wait_for_move(:pc)
          eng.wait(0.35)

          # Box 12 (Juno, crying): "...You made it."
          eng.say(:JUNO, :crying, "...You made it.", hold: 0.95)
          eng.actor(:juno).set_dir(:up)
          eng.wait(0.24)
          eng.actor(:nell).set_dir(:up)
          eng.wait(0.12)

          # Box 13 (Juno, sad): "Look — his mask... it broke."
          eng.say(:JUNO, :sad, "Look — his mask... it broke.", hold: 1.15)

          # Quiet resignation hold — Rowan meets your eyes beside the broken mask & white lily
          eng.bgm_fade(1.4)
          eng.wait(1.35)
          eng.letterbox(false, duration: 0.50)
          eng.wait(0.45)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE G (LIVE DIRECTOR'S CUT) — Ch10: "Bride Grove — The Plate Accepts Juno"
      # Target Duration: ~37.5s (~1,125 frames @ 30fps)
      # Live Map: Map 525 SE Sacred Ring-of-Stones Hollow (swaps 525->708)!
      # Canon: story/28_SCRIPT_CH10.md ("The Ogre", "The Loyal Three", "The Plate Accepts Her")
      # Restraint: <= 3 emotes | 0px static portraits | grounded PC | 0 MS-Paint shapes!
      #=========================================================================
      def play_ch10_bride_grove(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I (0.0–9.8s) — "The Ogre" & Juno's Quiet Path Under the Bride Tree
          #---------------------------------------------------------------------
          eng.transfer_map(525, 35.8, 30.8, hide_player: true)
          # Hide static SE Map 525 trainers/logs so the sacred stone-circle clearing is pristine!
          [13, 23, 24].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(-30, -24, -22, 42, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch10_veil_hollow", volume: 80, tag: "ch10_veil_hollow")

          # Pulsing pure-pixel emerald Meadow Plate nestled inside the mossy stone ring (36.5, 31.6)!
          eng.spawn_vfx(:meadow_plate, sheet: "pf_vfx_ch10_meadow_fx", tx: 36.5, ty: 31.7,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 195, scale: 0.92, z_layer: :floor)

          # Ogerpon guarding the Meadow Plate fiercely in the worn stone ring!
          eng.spawn_actor(:ogerpon, sheet: "Followers/OGERPON", tx: 36.6, ty: 30.8, dir: :left, is_charset: true)

          # Grounded PC leads Juno calmly down the quiet NW forest path, then steps respectfully back!
          eng.spawn_actor(:pc,   sheet: "PLAYER_A", tx: 33.4, ty: 26.8, dir: :down, is_charset: true)
          eng.spawn_actor(:juno, sheet: "JUNO",     tx: 33.4, ty: 25.6, dir: :down, is_charset: true)
          eng.actor(:pc).move_to(33.8, 29.4,   duration: 1.15, walk: true, dir: :down)
          eng.actor(:juno).move_to(34.6, 31.1, duration: 1.75, walk: true, dir: :down)
          eng.wait(1.20)
          eng.actor(:pc).set_dir(:right)
          eng.wait_for_move(:juno)
          eng.actor(:juno).set_dir(:right)

          # Ogerpon recognizes Juno, lowers its club & takes one gentle step forward!
          eng.play_cry(:OGERPON, volume: 88)
          eng.actor(:ogerpon).move_to(35.9, 31.0, duration: 0.65, walk: true, dir: :left)
          eng.wait(0.75)

          eng.say(:JUNO, :shocked, "...It knows me. I used to leave biscuits by the stair. Uncle Rowan said it was the badgers.", hold: 0.95)

          #---------------------------------------------------------------------
          # ACT II (9.8–19.2s) — Sweet Peach Fog: The Loyal Three Kneel in Unison!
          #---------------------------------------------------------------------
          eng.set_tone(-10, -34, -18, 24, duration: 0.70)
          eng.spawn_actor(:okidogi,     sheet: "Followers/OKIDOGI",     tx: 34.8, ty: 35.6, dir: :up, is_charset: true)
          eng.spawn_actor(:munkidori,   sheet: "Followers/MUNKIDORI",   tx: 36.5, ty: 35.8, dir: :up, is_charset: true)
          eng.spawn_actor(:fezandipiti, sheet: "Followers/FEZANDIPITI", tx: 38.2, ty: 35.6, dir: :up, is_charset: true)

          eng.actor(:okidogi).move_to(34.8, 33.5,     duration: 0.90, walk: true, dir: :up)
          eng.actor(:munkidori).move_to(36.5, 33.7,   duration: 0.95, walk: true, dir: :up)
          eng.actor(:fezandipiti).move_to(38.2, 33.5, duration: 0.90, walk: true, dir: :up)
          eng.wait(1.00)

          # All three kneel simultaneously in theatrical Saltmere pageant reverence!
          [:okidogi, :munkidori, :fezandipiti].each { |id| eng.actor(id).crouch_to(8, duration: 0.35) }
          eng.actor(:juno).set_dir(:down)
          # Emote #1 of 3: Juno stunned seeing the "heroes" from the pageant!
          eng.actor(:juno).show_emote(:exclaim, duration: 0.65)
          eng.play_se("Exclaim", volume: 80)
          eng.wait(0.95)

          eng.say(:JUNO, :happy, "It's them! The Loyal Three—from the pageant! They've come to help!", hold: 0.95)

          # Ogerpon roars desperately slamming its club into the roots; the Three rise blazing!
          eng.play_cry(:OGERPON, volume: 96)
          eng.actor(:ogerpon).hop(height: 12, duration: 0.28)
          eng.shake(power: 5, duration: 0.35)
          [:okidogi, :munkidori, :fezandipiti].each { |id| eng.actor(id).crouch_to(0, duration: 0.22) }
          eng.play_cry(:OKIDOGI, volume: 82)
          eng.wait(0.45)

          eng.say(:JUNO, :panic, "Wait— which— who do we—", hold: 0.60)

          # Grounded PC steps ONE calm, decisive pace down beside Ogerpon -> collars crack & Three flee!
          eng.actor(:pc).move_to(34.8, 30.2, duration: 0.55, walk: true, dir: :down)
          eng.wait_for_move(:pc)
          eng.bgm_cut
          eng.play_se("Anim/Ice8", volume: 90, pitch: 112)
          eng.flash(color: [248, 224, 240], power: 190, duration: 0.36)
          eng.set_tone(-22, -18, -16, 26, duration: 0.50)

          eng.actor(:okidogi).move_to(34.8, 37.0,     duration: 0.75, walk: true, dir: :down)
          eng.actor(:munkidori).move_to(36.5, 37.2,   duration: 0.80, walk: true, dir: :down)
          eng.actor(:fezandipiti).move_to(38.2, 37.0, duration: 0.75, walk: true, dir: :down)
          eng.wait(0.95)
          [:okidogi, :munkidori, :fezandipiti].each { |id| eng.remove_actor(id) }

          #---------------------------------------------------------------------
          # ACT III (20.2–31.0s) — Ogerpon's Tears & THE MEADOW PLATE ACCEPTS JUNO!
          #---------------------------------------------------------------------
          eng.play_bgm("ch10_bride_tree_grace", volume: 82, tag: "ch10_bride_tree_grace")
          # Ogerpon sits hard in petals & lifts its carved teal mask off to wipe its tearful eye!
          eng.actor(:ogerpon).move_to(37.4, 31.1, duration: 0.45, walk: true, dir: :right)
          eng.wait_for_move(:ogerpon)
          eng.actor(:ogerpon).set_pose("act_ch10_juno_ogerpon", 2)
          # Emote #2 of 3: quiet shared grief & recognition
          eng.actor(:ogerpon).show_emote(:dots, duration: 1.05)
          eng.actor(:juno).set_dir(:right)
          eng.wait(1.25)

          eng.say(:JUNO, :crying, "You were down here the whole time. Twelve years, by yourself... every single biscuit.", hold: 1.05)

          # Ogerpon puts its teal mask back on & stays faithfully at Juno's side!
          eng.actor(:ogerpon).set_pose("act_ch10_juno_ogerpon", 3)
          eng.wait(0.35)

          # Juno steps into the stone ring & kneels bare-handed over the glowing emerald Meadow Plate!
          eng.actor(:juno).move_to(36.3, 31.6, duration: 0.75, walk: true, dir: :right)
          eng.wait_for_move(:juno)
          eng.actor(:juno).set_pose("act_ch10_juno_ogerpon", 0)
          eng.wait(0.65)

          # THE GROVE BREATHES OUT: Grey twilight transforms to radiant sunlit meadow GOLD + falling petals!
          eng.play_se("Anim/HealBell", volume: 90, pitch: 106)
          eng.play_se("Anim/Saint7", volume: 84, pitch: 112)
          eng.flash(color: [236, 255, 198], power: 205, duration: 0.60)
          eng.set_tone(26, 18, -24, 0, duration: 1.25)
          eng.actor(:juno).set_pose("act_ch10_juno_ogerpon", 1) # Kneeling awestruck in golden pollen!

          # Lush pure-pixel swirling pink/ivory Bride Tree petals & golden pollen sweeping across the grove!
          [[33.6, 29.6, 0], [36.5, 30.8, 1], [39.2, 30.2, 2], [35.4, 32.8, 3]].each_with_index do |(px, py, ph), pi|
            eng.spawn_vfx(:"bride_petals_#{pi}", sheet: "pf_vfx_ch10_meadow_fx", tx: px, ty: py,
                          grid: [4, 2], frames: [4 + (ph % 4), 4 + ((ph + 1) % 4), 4 + ((ph + 2) % 4), 4 + ((ph + 3) % 4)],
                          ticks: [8, 8, 8, 8], loops: :forever,
                          blend: :add, opacity: 220, scale: 1.25, z_layer: :above)
          end

          # Unhurried silent golden-petal awe hold as the Veil lifts across the whole hollow!
          eng.zoom_map(1.30, duration: 1.35, focus: [36.4, 31.3], ease: :in_out)
          eng.wait(1.90)

          eng.say(:JUNO, :crying, "Oh, it's heavy. Nobody said it was heavy. It's like holding the whole hill.", hold: 1.00)
          eng.say(:JUNO, :sad, "He held this for twenty-four years... and I never once asked him if it hurt.", hold: 1.05)

          #---------------------------------------------------------------------
          # ACT IV (31.0–37.5s) — Valen & Tamsin at the Pathhead: "Now You've Seen."
          #---------------------------------------------------------------------
          eng.zoom_map(1.0, duration: 0.60, ease: :out)
          eng.pan_camera_to(35.0, 29.8, duration: 0.80, ease: :in_out)
          eng.spawn_actor(:valen,  sheet: "VALEN",  tx: 32.8, ty: 26.2, dir: :down, is_charset: true)
          eng.spawn_actor(:tamsin, sheet: "TAMSIN", tx: 34.0, ty: 26.2, dir: :down, is_charset: true)
          eng.actor(:valen).move_to(33.2, 28.2,  duration: 0.85, walk: true, dir: :down)
          eng.actor(:tamsin).move_to(34.2, 28.4, duration: 0.85, walk: true, dir: :down)
          eng.wait(0.95)
          eng.actor(:pc).set_dir(:up)

          # Emote #3 of 3: Valen's grave quiet gaze on the new Warden
          eng.actor(:valen).show_emote(:dots, duration: 0.80)
          eng.say(:VALEN, :neutral, "Warden Hale.", hold: 0.85)

          # Tamsin hurries down to Juno while Valen speaks quietly to the grounded PC!
          eng.actor(:tamsin).move_to(35.3, 31.4, duration: 0.95, walk: true, dir: :down)
          eng.wait(0.35)
          eng.say(:VALEN, :neutral, "Every seat takes the person who sits in it a little at a time, and gives back a city.", hold: 0.95)
          eng.actor(:tamsin).set_dir(:right)
          eng.say(:VALEN, :sad, "I asked you to come and see what it costs. Now you've seen.", hold: 1.25)

          eng.wait(1.15)
          eng.letterbox(false, duration: 0.50)
          eng.wait(0.50)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE 3 (RETHINK) — Ch11: "The Lake Breathes" (Kyogre Awakens)
      # Target Duration: ~36.0s (~1,080 frames @ 30fps)
      # Live Map: Map 563 (Rimewood Glade frozen lake; swaps 563 -> 309/300)
      # ZERO MS-Paint geometry | <= 3 restrained emotes | 90° Pier Apex Plate!
      #=========================================================================
      def play_ch11_kyogre_rethink(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I (0.0–5.5s) — Wet Midnight Ice, Emerald Aurora & Rising Gale
          #---------------------------------------------------------------------
          eng.transfer_map(563, 18.0, 14.8, hide_player: true)
          [1, 5, 7].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(-56, -46, -14, 32, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch11_ominous", volume: 80, tag: "ch11_ominous")
          eng.play_se("Anim/Whirlwind", volume: 58, pitch: 82)

          # NEW pure pixel-art emerald aurora ribbons (staged pf_vfx_deluge_rain Row 1)
          [[13.6, 9.6, 0], [18.0, 9.3, 1], [22.4, 9.6, 2]].each_with_index do |(ax, ay, ph), ai|
            eng.spawn_vfx(:"aurora_#{ai}", sheet: "pf_vfx_deluge_rain", tx: ax, ty: ay,
                          grid: [4, 2], frames: [4 + (ph % 4), 4 + ((ph + 1) % 4), 4 + ((ph + 2) % 4), 4 + ((ph + 3) % 4)],
                          ticks: [8, 8, 8, 8], loops: :forever,
                          blend: :add, opacity: 185, scale: 1.15, z_layer: :above)
          end

          # Cast walking onto the open south snow shore looking north across Lake Rime
          eng.spawn_actor(:anja, sheet: "ANJA",     tx: 15.8, ty: 19.2, dir: :up, is_charset: true)
          eng.spawn_actor(:pc,   sheet: "PLAYER_A", tx: 18.0, ty: 19.6, dir: :up, is_charset: true)
          eng.spawn_actor(:juno, sheet: "JUNO",     tx: 20.2, ty: 19.2, dir: :up, is_charset: true)

          eng.actor(:anja).move_to(15.8, 17.8, duration: 1.45, walk: true, dir: :up)
          eng.actor(:pc).move_to(18.0, 18.1,   duration: 1.55, walk: true, dir: :up)
          eng.actor(:juno).move_to(20.2, 17.8, duration: 1.50, walk: true, dir: :up)
          eng.pan_camera_to(18.0, 15.2, duration: 1.65, ease: :in_out)
          eng.wait(1.65)

          # Gale wind strikes! Anja leans in (scarf whipping), Juno grips blossom wreath!
          eng.actor(:anja).play_clip(
            sheet: "act_ch11_anja_brace", grid: [4, 4], frames: [0, 1, 2, 3],
            ticks: [8, 8, 8, 12], loops: 1, stay: true
          )
          eng.actor(:juno).play_clip(
            sheet: "act_ch11_juno_pier", grid: [4, 4], frames: [0, 1, 2, 3],
            ticks: [8, 8, 8, 12], loops: 1, stay: true
          )
          eng.wait(1.10)

          # Box 1 — Canon alarm beat (story/30_SCRIPT_CH11.md line 231)
          eng.say(:JUNO, :panic, "The lamps on the towers— they've gone from red to white!", hold: 1.25)
          eng.wait(0.35)

          #---------------------------------------------------------------------
          # ACT II (5.5–12.0s) — The Ice Tears Like a Page & Juno Stumbles!
          #---------------------------------------------------------------------
          eng.pan_camera_to(18.0, 14.0, duration: 0.70, ease: :in_out)
          eng.play_se("Anim/Earth3", volume: 86, pitch: 88)
          eng.shake(power: 3, duration: 1.10, decay: false)

          # Staggered NEW organic black-blue sea-ice fissures (pf_vfx_ice_fissure Row 0 — ZERO zigzags!)
          [[14.4, 13.4], [18.0, 13.0], [21.6, 13.4]].each_with_index do |(fx, fy), fi|
            eng.spawn_vfx(:"fissure_#{fi}", sheet: "pf_vfx_ice_fissure", tx: fx, ty: fy,
                          grid: [4, 2], frames: 0..3, ticks: [5, 5, 6, 10],
                          stay: :forever, blend: :normal, untoned: false,
                          scale: 1.18, z_layer: :floor)
            eng.play_se(fi == 1 ? "Anim/Ice5" : "Anim/Ice2", volume: 84, pitch: 90 + fi * 8)
            eng.wait(0.34)
          end

          # Emote #1 of 3 (restrained!): Juno jolts as tidal spray hits shore & stumbles back!
          eng.pan_camera_to(18.0, 15.6, duration: 0.55, ease: :out)
          eng.actor(:juno).show_emote(:exclaim, duration: 0.65)
          eng.play_se("Exclaim", volume: 84)
          eng.play_se("Anim/Water2", volume: 78, pitch: 108)
          eng.actor(:juno).play_clip(
            sheet: "act_ch11_juno_pier", grid: [4, 4], frames: [4, 5, 6, 7],
            ticks: [6, 7, 8, 14], stay: true
          )
          eng.actor(:juno).move_to(20.5, 18.4, duration: 0.52, walk: false, arc_h: 8.0, ease: :out)
          # Grounded, natural Protagonist reaction: turns calmly to check on Juno, then back north
          eng.wait(0.24)
          eng.actor(:pc).set_dir(:right)
          eng.wait(0.70)
          eng.actor(:pc).set_dir(:up)

          # Multi-box canon reaction with breathing pause!
          eng.say(:JUNO, :shocked, "The ice isn't cracking— it's tearing like a page!", hold: 1.10)
          eng.wait(0.45)
          eng.say(:JUNO, :panic, "The lanterns on Net Row are sliding into black water!", hold: 1.15)
          eng.wait(0.35)

          #---------------------------------------------------------------------
          # ACT IIIA (12.0–20.5s) — "The Lake Breathes" & Anja's Evacuation Order
          #---------------------------------------------------------------------
          # Dead stillness: BGM drops to eerie sub-bass water sigh as the whole harbour inhales!
          eng.bgm_fade(0.45)
          eng.pan_camera_to(18.0, 13.4, duration: 0.75, ease: :in_out)
          eng.set_tone(-84, -74, -26, 54, duration: 1.15)
          eng.play_se("Anim/Water2", volume: 82, pitch: 66)

          # Slow chest-filling inhale zoom (1.0 -> 1.36 -> 1.24 exhale sway!)
          eng.zoom_map(1.36, duration: 1.45, focus: [18.0, 13.2], ease: :in_out)
          # Submerged Leviathan beneath drifting ice floes (staged pf_vfx_ice_fissure Row 1: frames 4->5->6, ZERO oval eye!)
          eng.spawn_vfx(:submerged_abyss, sheet: "pf_vfx_ice_fissure", tx: 18.0, ty: 13.0,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [14, 16, 40],
                        stay: :forever, blend: :normal, untoned: false,
                        scale: 1.45, z_layer: :floor)
          eng.wait(1.50)
          eng.zoom_map(1.24, duration: 0.90, focus: [18.0, 13.6], ease: :in_out)
          eng.play_se("Anim/Earth4", volume: 72, pitch: 72)

          # Grounded Protagonist takes one measured half-step north; colorless scar hums -> Emote #2 of 3!
          eng.actor(:pc).move_to(18.0, 17.6, duration: 0.75, walk: true, dir: :up)
          eng.wait(0.55)
          eng.actor(:pc).show_emote(:double_exclaim, duration: 0.70)
          eng.play_se("Anim/HealBell", volume: 64, pitch: 136)
          eng.flash(color: [240, 248, 255], power: 92, duration: 0.16)
          eng.wait(0.75)

          # Anja recoils, pivots right pointing urgently toward Tower 4, shouting!
          eng.zoom_map(1.0, duration: 0.50, ease: :out)
          eng.pan_camera_to(18.0, 15.8, duration: 0.50, ease: :out)
          eng.actor(:anja).play_clip(
            sheet: "act_ch11_anja_brace", grid: [4, 4], frames: [4, 5, 6, 7],
            ticks: [6, 6, 10, 14], stay: true
          )
          eng.actor(:pc).set_dir(:left)
          eng.wait(0.55)

          eng.say(:ANJA, :panic, "That's not a Pokémon— that's WEATHER!", hold: 1.00)
          eng.wait(0.35)
          eng.say(:ANJA, :angry, "TOWERS! EVERYBODY TO THE TOWERS!", hold: 1.05)

          # Physical Rescue Acting: Anja & Juno brace firmly on snow shore (railing-free rows 0-1!); PC faces lake!
          eng.actor(:anja).move_to(16.2, 17.6, duration: 0.45, walk: false)
          eng.actor(:anja).play_clip(
            sheet: "act_ch11_anja_brace", grid: [4, 4], frames: [0, 1, 2, 3],
            ticks: [7, 7, 8, 16], stay: true
          )
          eng.actor(:juno).move_to(19.6, 17.8, duration: 0.52, walk: false, arc_h: 8.0)
          eng.actor(:juno).play_clip(
            sheet: "act_ch11_juno_pier", grid: [4, 4], frames: [0, 1, 2, 3],
            ticks: [7, 7, 8, 16], stay: true
          )
          eng.actor(:pc).set_dir(:up)
          eng.wait(0.55)

          # Crater flares blinding cyan-white (frame 7) + LAW 2 0.42s DEAD-SILENCE VACUUM!
          eng.stop_vfx(:submerged_abyss)
          eng.spawn_vfx(:crater_burst, sheet: "pf_vfx_ice_fissure", tx: 18.0, ty: 13.0,
                        grid: [4, 2], frames: [7], hold: 0.55, stay: :forever,
                        blend: :add, opacity: 235, scale: 1.52, z_layer: :above)
          eng.bgm_cut
          eng.play_se("Anim/Ice8", volume: 100, pitch: 86)
          eng.wait(0.42)

          #---------------------------------------------------------------------
          # ACT IIIB (20.5–28.5s) — 90° BANQUET-STYLE APEX CUT: cut_ch11_kyogre_90deg!
          #   Crisp 512x384 exact2x=True pier illustration + live @vfx_vp diagonal
          #   rain + Primal Kyogre cry + Kevin Penkin orchestral swell!
          #---------------------------------------------------------------------
          eng.stop_vfx(:crater_burst)
          3.times { |ai| eng.stop_vfx(:"aurora_#{ai}") }
          eng.play_cry(:KYOGRE_1, volume: 100)
          eng.play_se("Anim/Water5", volume: 96)
          eng.play_bgm("ch11_kyogre_thaw", volume: 92, tag: "ch11_kyogre_thaw")
          eng.flash(color: [198, 242, 255], power: 220, duration: 0.28)

          # Spawn crisp live diagonal pixel rain across full 512x384 @vfx_vp (balanced opacity 72 over plate!)
          [12.0, 16.0, 20.0, 24.0].each_with_index do |rx, xi|
            [10.5, 14.5, 18.5].each_with_index do |ry, yi|
              ph = (xi + yi) % 4
              eng.spawn_vfx(:"plate_rain_#{xi}_#{yi}", sheet: "pf_vfx_deluge_rain", tx: rx, ty: ry,
                            grid: [4, 2], frames: [ph, (ph + 1) % 4, (ph + 2) % 4, (ph + 3) % 4],
                            ticks: [2, 2, 2, 2], loops: :forever,
                            blend: :add, opacity: 72, scale: 1.05, z_layer: :above)
            end
          end

          eng.show_cut_plate(
            "Graphics/Pictures/cut_ch11_kyogre_90deg",
            fade_in: 0.18, hold: 7.4, fade_out: 0.30,
            pan: { [4, 0] => [-12, -4] }, zoom: [1.0, 1.07], shake: 2
          ) do |e|
            # Hold 3.1s completely text-free so the colossal tidal wall & Kyogre register!
            e.wait(3.10)
            e.say(:JUNO, :shocked, "It's bigger than the harbour...", hold: 1.05)
            e.wait(0.45)
            e.say(:JUNO, :panic, "...the whole sea stood up!", hold: 1.15)
            e.wait(0.65)
          end

          #---------------------------------------------------------------------
          # ACT IV (28.5–36.0s) — Return to Deluge Lake Rime: Primal Breach & Warm Rain!
          #---------------------------------------------------------------------
          eng.flash_ramp(color: [190, 242, 255], steps: [48, 132, 220, 255],
                         step_dur: 0.025, hold_dur: 0.08, fade_dur: 0.36)
          eng.set_tone(-44, -22, 18, 20, duration: 0.0)
          eng.pan_camera_to(18.0, 14.5, duration: 0.0)
          eng.play_se("Anim/Explosion7", volume: 92)
          eng.play_se("Anim/Water3", volume: 96)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.shake(power: 6, duration: 0.55, decay: true)

          # Metal-Slug-tier curling sea-foam ocean geysers flanking Primal Kyogre (staged pf_vfx_origin_pulse Row 1!)
          [[14.6, 14.3, 1.15], [18.0, 14.6, 1.32], [21.4, 14.3, 1.15]].each do |gx, gy, gsc|
            eng.spawn_vfx(nil, sheet: "pf_vfx_origin_pulse", tx: gx, ty: gy,
                          grid: [4, 2], frames: 4..7, ticks: [4, 4, 5, 6],
                          blend: :add, scale: gsc, z_layer: :above, origin: :foot)
          end

          # Primal Kyogre breaches vertically out of Lake Rime!
          eng.spawn_actor(:kyogre, sheet: "act_war1_primal_kyogre", tx: 18.0, ty: 15.1,
                          grid: [4, 2], is_charset: false, z_bias: 20)
          eng.actor(:kyogre).play_clip(
            sheet: "act_war1_primal_kyogre", grid: [4, 2], frames: [0, 1, 2, 3, 4, 5, 3],
            ticks: [5, 5, 6, 10, 6, 8, 28], loops: 1, stay: true
          )
          eng.wait(0.25)

          # Swirling anime-pixel Origin Pulse plasma orbs framing Kyogre cleanly (staged pf_vfx_origin_pulse Row 0!)
          [[14.6, 11.4], [21.4, 11.4], [18.0, 10.4]].each_with_index do |(ox, oy), oi|
            eng.spawn_vfx(nil, sheet: "pf_vfx_origin_pulse", tx: ox, ty: oy,
                          grid: [4, 2], frames: 0..3, ticks: [4, 4, 4, 5],
                          blend: :add, scale: 0.92, z_layer: :above)
            eng.wait(0.10) if oi < 2
          end

          # Anja & Juno brace against shockwave on open snow shore (railing-free rows 0-1!) into warm midnight rain!
          eng.actor(:anja).play_clip(
            sheet: "act_ch11_anja_brace", grid: [4, 4], frames: [4, 5, 3, 2, 1, 0],
            ticks: [7, 8, 10, 12, 14, 30], stay: true
          )
          eng.actor(:juno).play_clip(
            sheet: "act_ch11_juno_pier", grid: [4, 4], frames: [4, 5, 2, 1, 0],
            ticks: [7, 8, 12, 14, 30], stay: true
          )
          eng.actor(:pc).set_dir(:up)
          eng.wait(1.35)

          # Emote #3 of 3 (restrained!): quiet (...) on Anja feeling warm tropical rain on frozen sea!
          eng.play_se("Anim/Water1", volume: 78)
          eng.actor(:anja).show_emote(:dots, duration: 0.90)
          eng.wait(0.65)

          eng.say(:ANJA, :shocked, "Warm rain... at midnight on a frozen sea.", hold: 1.25)
          eng.wait(0.55)
          eng.say(:ANJA, :neutral, "Hold the platform— the Deep is awake!", hold: 1.35)

          # Long quiet aftermath hold under pouring warm rain before boss battle handoff
          eng.wait(1.30)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.45)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE H (#7) — Ch13 Glass Court: Sable Unmasked, Voss's Broadcast &
      #                The Fault (:CH13_FAULT, ~39s)
      # Live Maps: Map 287 (Glass Court Tribunal) -> cut_ch13_voss_broadcast_90deg
      #            -> Map 287 (Evening Fault) -> cut_ch13_fault_90deg
      #            -> Map 174 (Flooded Undercroft Pool)
      # Emote Count: STRICTLY 3 (:exclaim Juno, :exclaim Valen, :ellipsis PC)
      #=========================================================================
      def pf_play_ch13_glass_court_fault(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Glass Court Tribunal & Sable Unmasked (Map 287, ~0.0s..14.0s)
          #---------------------------------------------------------------------
          eng.transfer_map(287, 13.0, 14.5, hide_player: true)
          $game_map.events.each_value { |ev| ev.transparent = true }

          eng.set_tone(-6, -4, 6, 10, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch13_predators", volume: 82, tag: "ch13_predators")

          # North Dais: Sovereign Valen at white chair, Provost Ilsa beside him, chained Rowan in left dock
          eng.spawn_actor(:valen,     sheet: "VALEN",                  tx: 13.0, ty: 10.1, dir: :down,  is_charset: true)
          eng.spawn_actor(:ilsa,      sheet: "ILSA",                   tx: 15.0, ty: 10.7, dir: :down,  is_charset: true)
          eng.spawn_actor(:rowan,     sheet: "ROWAN",                  tx: 10.6, ty: 11.4, dir: :right, is_charset: true)

          # Accord Court Guards flanking the glass well
          eng.spawn_actor(:guard_l,   sheet: "trainer_THORNGUARD",     tx: 10.6, ty: 13.8, dir: :right, is_charset: true)
          eng.spawn_actor(:guard_r,   sheet: "trainer_THORNGUARD",     tx: 15.6, ty: 13.8, dir: :left,  is_charset: true)

          # Left Wardens' Row (benches): Juno, Kaito, Celestine
          eng.spawn_actor(:juno,      sheet: "JUNO",                   tx: 8.4,  ty: 14.4, dir: :right, is_charset: true)
          eng.spawn_actor(:kaito,     sheet: "KAITO",                  tx: 8.4,  ty: 16.4, dir: :right, is_charset: true)
          eng.spawn_actor(:celestine, sheet: "CELESTINE",              tx: 8.4,  ty: 18.4, dir: :right, is_charset: true)

          # Right Public Gallery: civilians + 3rd row Sabine Kroll disguised in her grey hat!
          eng.spawn_actor(:spec1,     sheet: "NPC 04",                 tx: 17.6, ty: 14.4, dir: :left,  is_charset: true)
          eng.spawn_actor(:spec2,     sheet: "NPC 11",                 tx: 17.6, ty: 18.4, dir: :left,  is_charset: true)
          eng.spawn_actor(:kroll,     sheet: "act_ch13_kroll_vault",   tx: 17.6, ty: 16.4, grid: [4, 4], is_charset: false, z_bias: 8)
          eng.actor(:kroll).set_cell(0)

          # Calm, grounded Protagonist standing steadily at the central witness rail
          eng.spawn_actor(:pc,        sheet: "PLAYER_A",               tx: 13.0, ty: 16.4, dir: :up,    is_charset: true)

          eng.wait(0.85)
          eng.zoom_map(1.16, duration: 0.90, focus: [14.0, 12.6], ease: :in_out)
          eng.play_se("Anim/HealBell", volume: 72, pitch: 118)
          eng.wait(0.65)

          eng.say(:ILSA, :neutral, "Someone in this room recognises that Meridian box.", hold: 0.95)
          eng.wait(0.24)
          eng.say(:ILSA, :angry, "Public gallery. Third row. Grey hat. Sabine Kroll.", hold: 1.05)

          # EMOTE #1 (Earned!): Juno recoils in the Wardens' row as Kroll stands, tosses her grey hat & vaults!
          eng.actor(:juno).show_emote(:exclaim, duration: 0.60)
          eng.play_se("Exclaim", volume: 88)
          eng.zoom_map(1.18, duration: 0.65, focus: [15.4, 15.6], ease: :in_out)
          eng.actor(:kroll).play_clip(
            sheet: "act_ch13_kroll_vault", grid: [4, 4],
            frames: [1, 2, 3], ticks: [7, 8, 7], stay: true
          )
          eng.wait(0.80)

          eng.say(:KROLL, :happy, "Light for everyone, right? ...You're no fun any more, Provost.", hold: 1.00)

          # Fluid athletic vault over the gallery rail into the courtroom well + Sharpedo release!
          eng.play_se("Player jump", volume: 92)
          eng.actor(:kroll).play_clip(
            sheet: "act_ch13_kroll_vault", grid: [4, 4],
            frames: [4, 5, 6, 7], ticks: [4, 5, 4, 8], stay: true
          )
          eng.actor(:kroll).move_to(14.6, 15.1, duration: 0.42, walk: false, arc_h: 24.0, ease: :out_cubic)
          eng.wait(0.55)

          eng.play_se("Battle throw", volume: 92)
          eng.actor(:kroll).play_clip(
            sheet: "act_ch13_kroll_vault", grid: [4, 4],
            frames: [8, 9], ticks: [6, 14], stay: true
          )
          eng.wait(0.22)
          eng.flash(color: [220, 245, 255], power: 165, duration: 0.20)
          eng.spawn_actor(:sharpedo, sheet: "Followers/SHARPEDO", tx: 14.0, ty: 13.6, dir: :up, grid: [4, 4], is_charset: true, z_bias: 6)
          eng.play_cry(:SHARPEDO, volume: 96)
          eng.shake(power: 3, duration: 0.30)
          eng.wait(0.85)

          eng.say(:KROLL, :smug, "Inquiry. There'll be an inquiry. You'll see.", hold: 0.90)

          # Smoke pellet drop -> vanishes leaving ONLY her discarded grey hat on the glass well floor!
          eng.actor(:kroll).play_clip(
            sheet: "act_ch13_kroll_vault", grid: [4, 4],
            frames: [10, 11, 12, 13, 14, 15], ticks: [4, 4, 5, 5, 6, 18],
            se: { 1 => "Anim/fog2" }, stay: true
          )
          eng.wait(0.45)
          eng.remove_actor(:sharpedo)
          eng.wait(0.95)

          #---------------------------------------------------------------------
          # ACT II — Voss On Every Screen (cut_ch13_voss_broadcast_90deg.png)
          # (~14.2s .. 22.0s | ZERO Protagonist! Ice-cold Meridian Spin!)
          #---------------------------------------------------------------------
          eng.flash(color: [168, 232, 255], power: 210, duration: 0.22)
          eng.play_bgm("ch13_voss_spin", volume: 82, tag: "ch13_voss_spin")
          eng.play_se("Anim/Thunder4", volume: 68, pitch: 130)
          eng.show_cut_plate(
            "cut_ch13_voss_broadcast_90deg",
            fade_in: 0.18, hold: 7.5, fade_out: 0.26,
            pan: { [0, 6] => [0, -6] }, zoom: [1.02, 1.07], shake: 0
          ) do |e|
            e.wait(1.65)
            e.say(:VOSS, :sad, "If any Meridian contractor acted outside the law, they acted alone.", hold: 1.00)
            e.wait(0.24)
            e.say(:VOSS, :sad, "I am appalled. I've ordered a full inquiry.", hold: 0.95)
            e.wait(0.26)
            e.say(:VOSS, :deadpan, "MERIDIAN APPROVAL +4  —  'DIRECTOR'S CANDOUR PRAISED'", hold: 1.15, name: "Lucent Broadcast")
          end

          #---------------------------------------------------------------------
          # ACT III — Evening Session Fault Tremor, 0.42s bgm_cut &
          #           90° Collapsing Dome Fault Apex Plate (~22.0s .. 32.8s)
          #---------------------------------------------------------------------
          # Return to dusk/evening Glass Court on Map 287 (hat & Kroll gone; tension heavy!)
          eng.remove_actor(:kroll)
          eng.zoom_map(1.0, duration: 0.0)
          eng.pan_camera_to(13.0, 14.5, duration: 0.0)
          eng.set_tone(-48, -42, -16, 44, duration: 0.0)
          eng.wait(0.65)

          # Deep bedrock Arbiter Engine test-fire tremor! Floor splits with glowing cyan fissures!
          eng.play_se("Anim/Earth4", volume: 96)
          eng.shake(power: 5, duration: 1.35, decay: false)
          eng.spawn_vfx(:fiss1, sheet: "pf_vfx_ch13_fault_vfx", tx: 13.0, ty: 14.8,
                        grid: [4, 2], frames: [4, 5], ticks: [7, 16], stay: :forever,
                        blend: :normal, untoned: false, scale: 0.92, z_layer: :floor)
          eng.spawn_vfx(:fiss2, sheet: "pf_vfx_ch13_fault_vfx", tx: 13.0, ty: 12.6,
                        grid: [4, 2], frames: [4, 5], ticks: [8, 16], stay: :forever,
                        blend: :normal, untoned: false, scale: 0.84, z_layer: :floor)
          # EMOTE #2 (Earned!): Valen snaps upright as the stained-glass dome splits!
          eng.actor(:valen).show_emote(:exclaim, duration: 0.60)
          eng.play_se("Anim/Ice5", volume: 88)
          eng.spawn_vfx(:shards_top, sheet: "pf_vfx_ch13_fault_vfx", tx: 13.0, ty: 13.6,
                        grid: [4, 2], frames: 0..3, ticks: [4, 4, 4, 5], loops: 2,
                        blend: :add, scale: 1.18, z_layer: :above)
          eng.wait(1.05)

          # LAW 2: 0.42s DIGITAL-ZERO AUDIO VACUUM + SHATTERING GLASS DOME CRACK!
          eng.bgm_cut
          eng.play_se("Anim/Ice8", volume: 100, pitch: 86)
          eng.play_se("Anim/Crash", volume: 92)
          eng.wait(0.42)

          # 90° BANQUET-STYLE APEX PLATE: Collapsing Dome, Chained Rowan vs Pinned Marchetti!
          eng.impact_beat(hitstop_sec: 0.12)
          eng.flash(color: [198, 244, 255], power: 220, duration: 0.25)
          eng.play_bgm("ch13_fault_dread", volume: 88, tag: "ch13_fault_dread")
          eng.play_se("Anim/Water5", volume: 96)
          eng.play_cry(:MANECTRIC, volume: 90)
          eng.show_cut_plate(
            "cut_ch13_fault_90deg",
            fade_in: 0.20, hold: 8.6, fade_out: 0.30,
            pan: { [-8, 5] => [8, -4] }, zoom: [1.02, 1.08], shake: 1.8
          ) do |e|
            # Live glittering stained-glass shards drifting cleanly over the 90° collapse plate!
            e.spawn_vfx(:p13_shards, sheet: "pf_vfx_ch13_fault_vfx", tx: 13.0, ty: 13.6,
                        grid: [4, 2], frames: [2, 3, 2, 3], ticks: [6, 6, 6, 6], loops: :forever,
                        blend: :add, opacity: 120, scale: 0.88, z_layer: :above)
            # 3.6s PURE SILENT TEXT-FREE CONTEMPLATION letting the vertical horror land!
            e.wait(3.60)
            e.say(:ROWAN, :angry, "Forget the chain— the water's coming up from the undercroft!!", hold: 1.10)
            e.wait(0.28)
            e.say(:MARCHETTI, :panic, "The orrery ring— it's pinned my waist—!", hold: 1.05)
            e.stop_vfx(:p13_shards)
          end

          #---------------------------------------------------------------------
          # ACT IV — Flooded Undercroft Pool Moral Choice (Map 174, ~32.8s..40.0s)
          #---------------------------------------------------------------------
          eng.transfer_map(174, 10.0, 11.4, hide_player: true)
          $game_map.events.each_value { |ev| ev.transparent = true }
          eng.set_tone(-44, -38, -14, 42, duration: 0.0)

          # Left half-submerged stone island: Rowan chained cleanly beside rope coil; Wick on far left pier!
          eng.spawn_actor(:rowan_u,   sheet: "ROWAN",               tx: 5.5,  ty: 10.8, dir: :right, is_charset: true, z_bias: 6)
          eng.spawn_actor(:wick_u,    sheet: "WICK",                tx: 3.1,  ty: 10.4, dir: :right, is_charset: true, z_bias: 6)
          # Right stone dock pier (100% clear of the white rowboat!): Marchetti pinned with barking Manectric!
          eng.spawn_actor(:march_u,   sheet: "MARCHETTI",           tx: 15.2, ty: 14.0, dir: :left,  is_charset: true, z_bias: 6)
          eng.spawn_actor(:manectric, sheet: "Followers/MANECTRIC", tx: 14.1, ty: 14.0, dir: :left,  grid: [4, 4], is_charset: true, z_bias: 6)
          # Center stone stair: Calm grounded Protagonist forced to choose!
          eng.spawn_actor(:pc_u,      sheet: "PLAYER_A",            tx: 10.0, ty: 11.5, dir: :left,  is_charset: true, z_bias: 6)

          # Surging dark floodwater splash crests placed cleanly in OPEN water channels (ZERO actor overlap!)
          eng.spawn_vfx(:wave_l, sheet: "pf_vfx_ch13_fault_vfx", tx: 7.4, ty: 11.0,
                        grid: [4, 2], frames: [6, 7], ticks: [9, 9], loops: :forever,
                        blend: :normal, untoned: false, opacity: 155, scale: 0.44, z_layer: :floor)
          eng.spawn_vfx(:wave_r, sheet: "pf_vfx_ch13_fault_vfx", tx: 15.8, ty: 11.4,
                        grid: [4, 2], frames: [7, 6], ticks: [9, 9], loops: :forever,
                        blend: :normal, untoned: false, opacity: 155, scale: 0.44, z_layer: :floor)

          eng.play_se("Anim/Water2", volume: 86, pitch: 82)
          eng.play_se("Anim/metal", volume: 84, pitch: 90)
          eng.shake(power: 3, duration: 0.45)
          eng.wait(0.85)

          eng.say(:WICK, :panic, "The dock's going under! Break Rowan's chain— please!", hold: 1.05, name: "Brother Wick")
          eng.actor(:pc_u).set_dir(:right)
          eng.play_cry(:MANECTRIC, volume: 88)
          eng.wait(0.32)
          eng.say(:MARCHETTI, :sad, "I can't lift this brass... you can only reach one of us.", hold: 1.15)

          # EMOTE #3 (Restrained heavy choice silence!): Calm Protagonist turns north-center facing the rising flood
          eng.actor(:pc_u).set_dir(:down)
          eng.actor(:pc_u).show_emote(:ellipsis, duration: 0.95)
          eng.wait(1.05)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.50)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE I (#10) — Ch17 Drowned Aurelia Sun Court: The Missing Piece &
      #                 Voss's Torch Breach (:CH17_SUN_COURT, ~38s)
      # Live Map: Map 186 (Gilded Sun Court Vault) -> cut_ch17_voss_breach_90deg
      #           -> Map 186 (Breached Vault & Voss's Open Palm Offer)
      # Emote Count: STRICTLY 3 (:exclaim Nyx, :exclaim Sahar, :ellipsis PC)
      #=========================================================================
      def pf_play_ch17_sun_court_breach(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Sunken Sun Court & Eighteen Awakening Colors (Map 186, ~0.0s..11.8s)
          #---------------------------------------------------------------------
          eng.transfer_map(186, 13.5, 13.2, hide_player: true)
          $game_map.events.each_value { |ev| ev.transparent = true }

          # Deep 300-year-old sunken lapis-and-gold vault gloom so prismatic light shafts, 18 colors & torch breach POP!
          eng.set_tone(-44, -48, -16, 26, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch17_murals", volume: 82, tag: "ch17_murals")

          # Door-sized Broken Golden Hand Keystone Cradle resting squarely on the circular sun medallion!
          eng.spawn_vfx(:golden_hand, sheet: "pf_vfx_ch17_golden_hand", tx: 13.5, ty: 12.8,
                        grid: [4, 2], frames: [0], ticks: [30], loops: :forever,
                        blend: :normal, untoned: false, scale: 0.82, z_layer: :mid)

          # Ethereal slanting golden-prismatic sunken temple light shafts cutting through the gloom
          eng.spawn_vfx(:shaft_l, sheet: "pf_vfx_ch17_sun_court", tx: 10.4, ty: 11.4,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 165, scale: 1.05, z_layer: :above)
          eng.spawn_vfx(:shaft_r, sheet: "pf_vfx_ch17_sun_court", tx: 16.6, ty: 11.4,
                        grid: [4, 2], frames: [2, 3, 0, 1], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 165, scale: 1.05, z_layer: :above)

          # Cast: Sahar studying inscription beside cradle, Nyx descending marble stair, calm PC approaching!
          eng.spawn_actor(:sahar, sheet: "SAHAR",    tx: 11.3, ty: 13.4, dir: :right, is_charset: true)
          eng.spawn_actor(:nyx,   sheet: "NYX",      tx: 15.6, ty: 10.8, dir: :down,  is_charset: true)
          eng.spawn_actor(:pc,    sheet: "PLAYER_A", tx: 13.5, ty: 16.4, dir: :up,    is_charset: true)

          # Calm, natural walk up to the giant broken golden hand (clean breathing room below plinth!)
          eng.wait(0.65)
          eng.actor(:pc).move_to(13.5, 15.0, duration: 1.25, walk: true, dir: :up)
          eng.wait(1.35)

          # THE EIGHTEEN COLORS KINDLE ONE BY ONE AROUND THE GOLDEN MEDALLION!!
          eng.play_se("Anim/Shiny sparkle", volume: 90, pitch: 96)
          eng.play_se("Anim/Saint7", volume: 86, pitch: 108)
          eng.flash(color: [255, 250, 224], power: 165, duration: 0.30)

          # Broken Golden Hand awakens through frames 1 -> 2 -> 3 (colorless fingertips -> radiant prismatic halo!)
          eng.stop_vfx(:golden_hand)
          eng.spawn_vfx(:golden_hand, sheet: "pf_vfx_ch17_golden_hand", tx: 13.5, ty: 12.8,
                        grid: [4, 2], frames: [1, 2, 3], ticks: [10, 12, 30], stay: :forever,
                        blend: :normal, untoned: true, scale: 0.82, z_layer: :mid)

          # Staggered 18-color prismatic sanctuary rings kindling vividly around the circular sun court!
          [
            [11.0, 11.6], [16.0, 11.6], [11.0, 14.9], [16.0, 14.9]
          ].each_with_index do |(mx, my), mi|
            eng.spawn_vfx(:"prism_#{mi}", sheet: "pf_vfx_ch17_golden_hand", tx: mx, ty: my,
                          grid: [4, 2], frames: [4, 5, 6, 7], ticks: [8, 8, 8, 8], loops: :forever,
                          blend: :add, opacity: 225, scale: 0.84, z_layer: :floor)
            eng.play_se("Anim/HealBell", volume: 68, pitch: 96 + mi * 8) if mi.even?
            eng.wait(0.32)
          end

          #---------------------------------------------------------------------
          # ACT II — "You're The Missing Piece" & PC's 4th Authored Line (~11.8s..20.4s)
          #---------------------------------------------------------------------
          eng.zoom_map(1.18, duration: 0.90, focus: [13.5, 13.4], ease: :in_out)
          # EMOTE #1 (Earned!): Nyx gasps stepping softly down beside the glowing medallion
          eng.actor(:nyx).show_emote(:exclaim, duration: 0.65)
          eng.actor(:nyx).move_to(15.5, 12.6, duration: 0.70, walk: true, dir: :left)
          eng.wait(0.80)

          eng.say(:NYX, :shocked, "Oh...", hold: 0.65)
          eng.wait(0.22)
          eng.say(:NYX, :sad, "Oh, darling. You're the missing piece.", hold: 1.05)
          eng.wait(0.28)
          eng.say(:SAHAR, :neutral, "'Here rests the One that is every color and none.'", hold: 1.05)
          eng.wait(0.26)
          eng.say(:SAHAR, :sad, "It's the Legend Plate. You're carrying what was torn from this hand.", hold: 1.10)
          eng.wait(0.36)
          # Protagonist's canonical fourth authored line!
          eng.say(:PLAYER_A, :neutral, "...I know. I think I always knew. I just didn't have the word.", hold: 1.25)
          eng.wait(0.35)

          #---------------------------------------------------------------------
          # ACT III — 0.42s bgm_cut -> PLASMA TORCH BREACH -> 90° VOSS BREACH PLATE!
          # (~20.4s .. 31.6s | 3.6s Pure Silent Text-Free Contemplation!)
          #---------------------------------------------------------------------
          eng.zoom_map(1.0, duration: 0.40, ease: :out)
          # LAW 2: 0.42s DIGITAL-ZERO AUDIO VACUUM + RAZOR PLASMA TORCH IGNITION!
          eng.bgm_cut
          eng.play_se("Anim/Slash1", volume: 96, pitch: 125)
          eng.play_se("Anim/Fire6", volume: 94, pitch: 112)
          eng.wait(0.42)

          # Blinding white-hot plasma cutting-torch arc slices through the dark eastern golden wall!
          eng.impact_beat(hitstop_sec: 0.12)
          eng.flash(color: [255, 224, 148], power: 215, duration: 0.24)
          eng.shake(power: 5, duration: 0.65)
          eng.play_se("Anim/Explosion7", volume: 90, pitch: 108)
          eng.play_se("Anim/Fire4", volume: 88)
          eng.spawn_vfx(:torch_arc, sheet: "pf_vfx_ch17_sun_court", tx: 18.2, ty: 12.6,
                        grid: [4, 2], frames: [4, 5, 4, 5], ticks: [5, 6, 5, 6],
                        blend: :add, scale: 1.25, z_layer: :above)
          eng.spawn_vfx(:breach_sparks, sheet: "pf_vfx_ch17_sun_court", tx: 18.2, ty: 13.0,
                        grid: [4, 2], frames: [6, 7], ticks: [5, 5], loops: :forever,
                        blend: :add, opacity: 235, scale: 1.02, z_layer: :above)

          # EMOTE #2 (Earned!): Sahar & PC spin right toward the blazing molten wall breach!
          eng.actor(:sahar).show_emote(:exclaim, duration: 0.60)
          eng.actor(:pc).set_dir(:right)
          eng.actor(:nyx).set_dir(:right)
          eng.wait(1.05)

          # Clear all untoned @vfx_vp map VFX before cutting to 90° plate so ZERO top-down sprites bleed onto plate!
          eng.stop_vfx(:golden_hand)
          eng.stop_vfx(:shaft_l)
          eng.stop_vfx(:shaft_r)
          eng.stop_vfx(:breach_sparks)

          # 90° BANQUET-STYLE APEX PLATE: Voss stepping through molten breach extending bare open palm!
          eng.play_bgm("ch17_voss_treachery", volume: 84, tag: "ch17_voss_treachery")
          eng.show_cut_plate(
            "cut_ch17_voss_breach_90deg",
            fade_in: 0.22, hold: 8.8, fade_out: 0.30,
            pan: { [8, 4] => [-8, -3] }, zoom: [1.02, 1.08], shake: 0.6
          ) do |e|
            # Subtle molten spark shower drifting cleanly on the far right breach edge without blocking Voss or Hand!
            e.spawn_vfx(:p17_sparks, sheet: "pf_vfx_ch17_sun_court", tx: 18.8, ty: 12.6,
                        grid: [4, 2], frames: [6, 7], ticks: [6, 6], loops: :forever,
                        blend: :add, opacity: 80, scale: 0.66, z_layer: :above)
            # 3.6s PURE SILENT TEXT-FREE HOLD letting the double-open-palm visual rhyme land!
            e.wait(3.60)
            e.say(:VOSS, :happy, "Oh, look at that. Ten years of telemetry... nothing compares to seeing it live.", hold: 1.15)
            e.wait(0.28)
            e.say(:VOSS, :neutral, "Gods are absentee landlords. I'm making sure we never need one again.", hold: 1.15)
            e.stop_vfx(:p17_sparks)
          end

          #---------------------------------------------------------------------
          # ACT IV — Breached Sun Court & Voss's Open Palm Offer (~31.6s..39.0s)
          #---------------------------------------------------------------------
          eng.set_tone(-38, -42, -14, 24, duration: 0.65)
          # Cleanly restore the awakened Broken Golden Hand, sunken light shafts & molten breach embers!
          eng.spawn_vfx(:golden_hand, sheet: "pf_vfx_ch17_golden_hand", tx: 13.5, ty: 12.8,
                        grid: [4, 2], frames: [3], ticks: [30], loops: :forever,
                        blend: :normal, untoned: true, scale: 0.82, z_layer: :mid)
          eng.spawn_vfx(:shaft_l, sheet: "pf_vfx_ch17_sun_court", tx: 10.4, ty: 11.4,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 145, scale: 1.05, z_layer: :above)
          eng.spawn_vfx(:shaft_r, sheet: "pf_vfx_ch17_sun_court", tx: 16.6, ty: 11.4,
                        grid: [4, 2], frames: [2, 3, 0, 1], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :add, opacity: 145, scale: 1.05, z_layer: :above)
          eng.spawn_vfx(:breach_embers, sheet: "pf_vfx_ch17_sun_court", tx: 18.2, ty: 12.8,
                        grid: [4, 2], frames: [6, 7], ticks: [7, 7], loops: :forever,
                        blend: :add, opacity: 185, scale: 0.85, z_layer: :above)

          # Voss steps smoothly into the Sun Court flanked by two Meridian salvage divers!
          eng.spawn_actor(:voss,   sheet: "act_ch17_voss_palm",           tx: 17.2, ty: 14.4, grid: [4, 4], is_charset: false, z_bias: 8)
          eng.spawn_actor(:crew_1, sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 18.2, ty: 12.6, dir: :left, is_charset: true)
          eng.spawn_actor(:crew_2, sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 18.2, ty: 15.0, dir: :left, is_charset: true)
          eng.actor(:voss).set_cell(3)

          eng.actor(:voss).play_clip(
            sheet: "act_ch17_voss_palm", grid: [4, 4],
            frames: [3, 4, 5, 7], ticks: [7, 7, 7, 8], stay: true
          )
          eng.actor(:voss).move_to(15.6, 14.7, duration: 0.95, walk: false, ease: :out_cubic)
          eng.actor(:nyx).move_to(15.2, 11.4, duration: 0.65, walk: true, dir: :down)
          eng.zoom_map(1.14, duration: 0.90, focus: [14.5, 13.8], ease: :in_out)
          eng.wait(1.05)

          # Voss smoothly extends his bare right palm open — echoing the Broken Golden Hand directly beside him!
          eng.play_se("Anim/HealBell", volume: 74, pitch: 90)
          eng.actor(:voss).play_clip(
            sheet: "act_ch17_voss_palm", grid: [4, 4],
            frames: [8, 9, 10, 11, 12], ticks: [6, 7, 8, 12, 24], stay: true
          )
          eng.wait(0.85)

          eng.say(:VOSS, :neutral, "Stand with me at the Festival. No child in Velmora will ever be Fixed again.", hold: 1.15)
          eng.wait(0.30)
          eng.say(:VOSS, :sad, "Your mother wilted in exile because of a broken god. I can fix the god.", hold: 1.30)

          # EMOTE #3 (Quiet stunned weight!): Calm Protagonist stares at Voss's open palm
          eng.actor(:pc).show_emote(:ellipsis, duration: 0.95)
          eng.wait(1.10)
          eng.zoom_map(1.0, duration: 0.65, ease: :out)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.55)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE D (LIVE DIRECTOR'S CUT) — Ch16: "Clear Air — Wenlow's Stand"
      # Target Duration: ~34.5s (~1,035 frames @ 30fps)
      # Live Maps: Map 104 (Mirefen Infirmary stand-in) -> 0-frame #000000 Black
      #            (1 dry gunshot SE + 120f unbroken dead silence) -> Map 544 (Cragholm)!
      # Canon: story/35_SCRIPT_CH16.md (Interlude IV) + REVIEW.md #20 dead-silence rule!
      # Restraint: <= 3 emotes | 0px static portraits | grounded PC | 0 MS-Paint shapes!
      #=========================================================================
      def play_ch16_wenlow(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I (0.0–12.5s) — Evening Rounds & Radio Warning (Mirefen Infirmary)
          #---------------------------------------------------------------------
          eng.transfer_map(104, 10.5, 10.4, hide_player: true)
          # Hide static Tidewater Inn NPCs so Wenlow & patients own the Infirmary cleanly
          [2, 3, 4].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(-14, -18, -8, 12, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch16_wenlow_warm", volume: 82, tag: "ch16_wenlow_warm")

          # Sleeping Quiet Ward patients behind the bead curtain + left-bed patient
          eng.spawn_actor(:pat_left,  sheet: "NPC 06", tx: 4.5,  ty: 11.4, dir: :down, is_charset: true)
          eng.spawn_actor(:pat_ward1, sheet: "NPC 02", tx: 15.5, ty: 9.6,  dir: :down, is_charset: true)
          eng.spawn_actor(:pat_ward2, sheet: "NPC 04", tx: 15.5, ty: 12.6, dir: :down, is_charset: true)

          # Delicate pure-pixel glass-bead curtain framing the Quiet Ward doorway (Y-sorted behind Wenlow!)
          eng.spawn_vfx(:beads_ward, sheet: "pf_vfx_ch16_ward_fx", tx: 14.4, ty: 10.8,
                        grid: [4, 2], frames: [0, 1, 2, 3], ticks: [10, 10, 10, 10], loops: :forever,
                        blend: :normal, untoned: false, opacity: 195, scale: 0.62, z_layer: :mid)

          # 17-year-old Wenlow doing warm evening rounds beside the left patient cot
          eng.spawn_actor(:wenlow, sheet: "WENLOW", tx: 6.4, ty: 11.4, dir: :left, is_charset: true)
          eng.wait(0.55)
          eng.actor(:wenlow).move_to(6.4, 12.0, duration: 0.40, walk: true, dir: :down)
          eng.wait_for_move(:wenlow)
          eng.actor(:wenlow).move_to(12.6, 12.0, duration: 1.15, walk: true, dir: :right)
          eng.wait(0.65)

          eng.say(:WENLOW, :happy, "Right! Evening rounds! Mrs. Pell, water. Old Fisk, the green one, not the brown one—yes, that one.", hold: 1.00)

          eng.wait_for_move(:wenlow)
          eng.actor(:wenlow).move_to(12.8, 9.6, duration: 0.75, walk: true, dir: :up)
          eng.wait_for_move(:wenlow)

          # Radio crackles from the east stilt-walks! Emote #1 of 3!
          eng.play_se("Battle catch click", volume: 84, pitch: 122)
          eng.actor(:wenlow).show_emote(:exclaim, duration: 0.60)
          eng.play_se("Exclaim", volume: 78)
          eng.wait(0.55)

          eng.say(nil, :neutral, "Infirmary? Grey coats at the east walks. Lots. They've got the Sweetrot list.", hold: 1.05, name: "Radio")

          # Wenlow steadies himself, walks calmly to the Quiet Ward threshold in front of the bead curtain
          eng.set_tone(-26, -28, -14, 28, duration: 0.75)
          eng.wait(0.30)
          eng.actor(:wenlow).move_to(13.5, 11.4, duration: 0.80, walk: true, dir: :down)
          eng.wait_for_move(:wenlow)
          eng.actor(:wenlow).set_dir(:right)
          eng.wait(0.30)

          eng.say(:WENLOW, :neutral, "...Okay. Okay. I've read the book twice. Nobody ever looks at the glass ones.", hold: 1.00)

          #---------------------------------------------------------------------
          # ACT II (12.5–21.5s) — MANDATORY HARD bgm_cut TOTAL DEAD SILENCE!
          #   Canon REVIEW.md #20: silence from the Ward doorway through the shot!
          #---------------------------------------------------------------------
          eng.bgm_cut
          eng.set_tone(-38, -40, -24, 46, duration: 0.55)
          # Wenlow turns to face the doorway in his pure-pixel acting sheet (frame 0: steady, left-facing)
          eng.actor(:wenlow).set_pose("act_ch16_wenlow_stand", 0)
          eng.pan_camera_to(10.8, 10.9, duration: 0.65, ease: :in_out)
          eng.wait(0.35)

          # Front Infirmary door swings open; Directorate squad enters silently into open lower corridor!
          eng.play_se("Door enter", volume: 88, pitch: 86)
          eng.spawn_actor(:lt,   sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 10.0, ty: 14.0, dir: :up, is_charset: true)
          eng.spawn_actor(:off1, sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 9.2,  ty: 14.3, dir: :up, is_charset: true)
          eng.spawn_actor(:off2, sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 10.8, ty: 14.3, dir: :up, is_charset: true)
          eng.spawn_actor(:off3, sheet: "trainer_MERIDIAN_DIRECTORATE", tx: 10.0, ty: 14.7, dir: :up, is_charset: true)

          eng.actor(:lt).move_to(10.6, 11.4, duration: 0.85, walk: true, dir: :up)
          eng.actor(:off1).move_to(9.2, 11.0, duration: 0.90, walk: true, dir: :up)
          eng.actor(:off2).move_to(9.6, 12.3, duration: 0.80, walk: true, dir: :up)
          eng.actor(:off3).move_to(8.4, 11.8, duration: 0.95, walk: true, dir: :up)
          eng.wait(0.95)
          [:lt, :off1, :off2, :off3].each { |id| eng.actor(id).set_dir(:right) }

          # Mirrored Bayer-dithered Directorate lantern beam projecting from Lieutenant rightward onto Wenlow!
          eng.spawn_vfx(:lantern_cone, sheet: "pf_vfx_ch16_ward_fx", tx: 12.2, ty: 11.4,
                        grid: [4, 2], frames: [4, 5, 6, 7], ticks: [9, 9, 9, 9], loops: :forever,
                        blend: :add, mirror: true, opacity: 105, scale: 0.82, z_layer: :above)
          eng.wait(0.35)

          eng.say(nil, :neutral, "Medical facility. We have reason to believe Sweetrot users are being harboured on these premises.", hold: 1.15, name: "Lieutenant")

          # Intimate zoom framing Lieutenant & Wenlow raising both open palms in front of the bead curtain
          eng.zoom_map(1.30, duration: 1.10, focus: [12.0, 11.1], ease: :in_out)
          eng.actor(:wenlow).play_clip(
            sheet: "act_ch16_wenlow_stand", grid: [4, 1], frames: [0, 1, 2, 3],
            ticks: [10, 10, 10, 30], loops: 1, stay: true
          )
          # Emote #2 of 3: quiet resolve before speaking
          eng.actor(:wenlow).show_emote(:dots, duration: 0.65)
          eng.wait(1.15)

          eng.say(:WENLOW, :neutral, "This is a hospital.", hold: 1.05)

          # Lieutenant steps half a pace closer; Wenlow begins his final sentence — cut off at 0 frames!
          eng.actor(:lt).move_to(11.1, 11.4, duration: 0.45, walk: true, dir: :right)
          eng.wait(0.50)
          eng.say(:WENLOW, :neutral, "You have to —", hold: 0.25)

          #---------------------------------------------------------------------
          # ACT III (21.5–25.6s) — 0-FRAME HARD CUT TO PURE #000000 BLACK
          #   ONE SINGLE DRY GUNSHOT SE — 120 FULL FRAMES (4.00s) DEAD SILENCE!
          #---------------------------------------------------------------------
          eng.set_blackout(true)
          eng.wait(0.06)
          eng.play_se("ch16_gunshot", volume: 100)
          eng.wait(4.00)

          #---------------------------------------------------------------------
          # ACT IV (25.6–34.5s) — Cragholm Deep Seams Aftermath (Map 544 -> 363)
          #   Solo violin enters STRICTLY here, after the full 4.0s silent black!
          #---------------------------------------------------------------------
          eng.transfer_map(544, 14.5, 30.2, hide_player: true)
          [14, 15].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end
          eng.set_tone(-34, -36, -28, 38, duration: 0.0)

          # Motionless Corvin beside the pit-prop; Pip & Bastian in doorway; grounded PC cleanly framed!
          eng.spawn_actor(:corvin,  sheet: "CORVIN",   tx: 16.4, ty: 29.5, dir: :down,  is_charset: true)
          eng.spawn_actor(:pip,     sheet: "PIP",      tx: 11.6, ty: 32.5, dir: :up,    is_charset: true)
          eng.spawn_actor(:bastian, sheet: "BASTIAN",  tx: 10.8, ty: 32.8, dir: :up,    is_charset: true)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A", tx: 10.2, ty: 32.2, dir: :right, is_charset: true)

          eng.play_bgm("ch16_aftermath_violin", volume: 78, tag: "ch16_aftermath_violin")
          eng.flash(color: [0, 0, 0], power: 255, duration: 1.35)
          eng.wait(1.45)

          eng.play_se("Battle catch click", volume: 70, pitch: 90)
          eng.say(nil, :neutral, "...Infirmary to Cragholm. Infirmary to — (static) — is anyone — the boy, Doctor. The boy.", hold: 1.40, name: "Radio")

          # Corvin never moves. Pip takes a step in; Bastian calmly steps up behind her and stops her.
          eng.zoom_map(1.22, duration: 1.30, focus: [14.4, 30.5], ease: :in_out)
          eng.actor(:pip).move_to(12.8, 31.2, duration: 0.85, walk: true, dir: :right)
          eng.wait(0.30)
          eng.actor(:bastian).move_to(11.9, 31.4, duration: 0.75, walk: true, dir: :right)
          eng.wait_for_move(:bastian)
          eng.actor(:pip).set_dir(:left)
          eng.wait(0.45)
          eng.actor(:pip).set_dir(:right)

          # Emote #3 of 3: unbroken stillness over Corvin
          eng.actor(:corvin).show_emote(:dots, duration: 1.10)
          eng.wait(1.50)

          eng.zoom_map(1.0, duration: 0.50, ease: :out)
          eng.letterbox(false, duration: 0.50)
          eng.wait(0.50)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # WAVE-3 SCENE 1 — Ch19 WAR-1 Rethink (~42s, Live Map 926 The Glass Dunes)
      # "Origin Pulse vs Blue Flare — Valen's Command, Kestrel's Intercept &
      #  The 90° Panoramic Glass Dunes Apex Plate"
      #-------------------------------------------------------------------------
      # Emote Count: STRICTLY 2 (:exclaim on Kestrel spotting blast, :ellipsis
      #              on Anja surveying the vitrified desert).
      # Protagonist: Grounded & natural (calm observational footing -> single
      #              steady defensive step back behind Kestrel's shield cover).
      # Pure-Pixel VFX: pf_vfx_w3_origin_beam, pf_vfx_w3_blue_flare,
      #                 pf_vfx_w3_clash_core, pf_vfx_w3_glass_curtain.
      # Acting Sheets:  act_ch19_valen_command, act_ch19_kestrel_shield,
      #                 act_war1_primal_kyogre, act_war1_reshiram.
      # 90° Apex Plate: cut_ch19_war1_90deg.png (3.1s silent text-free hold!).
      #=========================================================================
      def pf_play_ch19_war1_rethink(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Dawn Frontline, Primal Kyogre & Reshiram Summons, Valen's Vigil
          # (~0.0s .. 11.2s)
          #---------------------------------------------------------------------
          eng.transfer_map(926, 25.8, 8.6, hide_player: true)
          (3..10).each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(12, 2, -10, 8, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch19_dynast", volume: 82, tag: "ch19_dynast")

          # Isenmar Host (West / Left)
          eng.spawn_actor(:eirik, sheet: "EIRIK", tx: 23.5, ty: 11.3, dir: :right, is_charset: true)
          eng.spawn_actor(:is_s1, sheet: "pfw_soldier_isenmar", tx: 22.4, ty: 9.8,  dir: :right, is_charset: true)
          eng.spawn_actor(:is_s2, sheet: "pfw_soldier_isenmar", tx: 22.4, ty: 11.8, dir: :right, is_charset: true)
          eng.spawn_actor(:is_s3, sheet: "pfw_soldier_isenmar", tx: 23.9, ty: 12.4, dir: :right, is_charset: true)
          eng.spawn_actor(:is_b1, sheet: "pfw_banner_isenmar",  tx: 21.8, ty: 8.6,  grid: [1, 1], is_charset: false)
          eng.spawn_actor(:is_b2, sheet: "pfw_banner_isenmar",  tx: 21.7, ty: 12.1, grid: [1, 1], is_charset: false)

          # Ashkaar Host (East / Right)
          eng.spawn_actor(:hrothgar, sheet: "HROTHGAR", tx: 36.5, ty: 11.3, dir: :left, is_charset: true)
          eng.spawn_actor(:as_s1, sheet: "pfw_soldier_ashkaar", tx: 37.6, ty: 9.8,  dir: :left, is_charset: true)
          eng.spawn_actor(:as_s2, sheet: "pfw_soldier_ashkaar", tx: 37.6, ty: 11.8, dir: :left, is_charset: true)
          eng.spawn_actor(:as_s3, sheet: "pfw_soldier_ashkaar", tx: 36.1, ty: 12.4, dir: :left, is_charset: true)
          eng.spawn_actor(:as_b1, sheet: "pfw_banner_ashkaar",  tx: 38.2, ty: 8.6,  grid: [1, 1], is_charset: false)
          eng.spawn_actor(:as_b2, sheet: "pfw_banner_ashkaar",  tx: 38.3, ty: 12.1, grid: [1, 1], is_charset: false)

          # Southern Dune Ridge — Valen commanding forward; Kestrel, grounded PC, Anja & Sigrun below
          eng.spawn_actor(:valen,   sheet: "act_ch19_valen_command",  tx: 30.0, ty: 11.3, grid: [4, 4], is_charset: false, z_bias: 4)
          eng.spawn_actor(:kestrel, sheet: "act_ch19_kestrel_shield", tx: 28.1, ty: 12.5, grid: [4, 4], is_charset: false, z_bias: 4)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A",                tx: 30.0, ty: 12.6, dir: :up, is_charset: true)
          eng.spawn_actor(:anja,    sheet: "ANJA",                    tx: 26.8, ty: 12.7, dir: :up, is_charset: true)
          eng.spawn_actor(:sigrun,  sheet: "SIGRUN",                  tx: 32.2, ty: 12.7, dir: :up, is_charset: true)
          eng.actor(:valen).set_cell(0)
          eng.actor(:kestrel).set_cell(14)

          # Beat 1: Primal Kyogre breaches on Isenmar flank inside pure-pixel hydro vortex!
          eng.play_se("Anim/Water5", volume: 95)
          eng.shake(power: 4, duration: 0.45)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_origin_beam", tx: 25.3, ty: 9.8,
                        grid: [4, 2], frames: 4..7, ticks: [3, 4, 4, 5],
                        blend: :add, scale: 1.18, z_layer: :above, origin: :foot)
          eng.spawn_actor(:kyogre, sheet: "act_war1_primal_kyogre", tx: 25.3, ty: 9.8,
                          grid: [4, 2], is_charset: false, z_bias: 20)
          eng.actor(:kyogre).play_clip(
            sheet: "act_war1_primal_kyogre", grid: [4, 2], frames: [0, 1, 2, 3],
            ticks: [4, 4, 5, 14], stay: true
          )
          eng.play_cry(:KYOGRE_1, volume: 100)
          eng.wait(1.35)
          eng.say(:EIRIK, :angry, "Isenmar! Look to the crest!", hold: 0.95, name: "Thane Eirik")
          eng.wait(0.28)
          eng.say(:EIRIK, :angry, "The sea has come to the sand!", hold: 1.10, name: "Thane Eirik")

          # Beat 2: Wide pan east to Ashkaar flank -> Reshiram unfolds in cobalt turbine inferno!
          eng.pan_camera_to(34.2, 8.6, duration: 1.00, ease: :in_out)
          eng.wait(1.05)
          eng.flash(color: [255, 226, 178], power: 195, duration: 0.28)
          eng.play_se("Anim/Fire4", volume: 95)
          eng.shake(power: 4, duration: 0.45)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_blue_flare", tx: 34.7, ty: 9.8,
                        grid: [4, 2], frames: 4..7, ticks: [3, 3, 4, 4],
                        blend: :add, scale: 1.15, z_layer: :above, origin: :foot)
          eng.spawn_actor(:reshiram, sheet: "act_war1_reshiram", tx: 34.7, ty: 9.8,
                          grid: [4, 2], is_charset: false, z_bias: 20)
          eng.actor(:reshiram).play_clip(
            sheet: "act_war1_reshiram", grid: [4, 2], frames: [0, 1, 2, 3],
            ticks: [5, 4, 5, 14], stay: true
          )
          eng.play_cry(:RESHIRAM, volume: 100)
          eng.wait(1.15)
          eng.say(:HROTHGAR, :angry, "Then let it remember fire.", hold: 1.25, name: "Dominar Hrothgar")

          #---------------------------------------------------------------------
          # ACT II — Valen's Command, Pure-Pixel Beam Launch & Tug-of-War
          # (~11.8s .. 22.8s)
          #---------------------------------------------------------------------
          eng.pan_camera_to(30.0, 8.8, duration: 0.85, ease: :in_out)
          eng.set_tone(-72, -74, -52, 62, duration: 0.85)
          eng.play_bgm("ch19_war_clash", volume: 90, tag: "ch19_war_clash")

          # Valen braces into rising dune gale and raises gauntleted command hand!
          eng.actor(:valen).play_clip(
            sheet: "act_ch19_valen_command", grid: [4, 4],
            frames: [1, 2, 4, 5, 6, 7], ticks: [6, 6, 5, 5, 10, 8], stay: true
          )
          eng.wait(1.05)
          eng.say(:VALEN, :angry, "Hold the southern ridge!", hold: 0.85)
          eng.wait(0.24)
          eng.say(:VALEN, :shocked, "Nobody crosses that seam— BRACE!!", hold: 0.95)

          # Both titans enter charge poses (frame 4) with pure-pixel swirling muzzle vortices!
          eng.actor(:valen).play_clip(
            sheet: "act_ch19_valen_command", grid: [4, 4], frames: [8, 9], ticks: [8, 12], stay: true
          )
          eng.actor(:kyogre).set_cell(4)
          eng.actor(:reshiram).set_cell(4)
          eng.play_se("Anim/Charge_Beam", volume: 95)
          eng.play_se("Anim/Fire5", volume: 82)
          eng.spawn_vfx(:muzzle_l, sheet: "pf_vfx_w3_origin_beam", tx: 26.75, ty: 9.8,
                        grid: [4, 2], frames: 4..7, ticks: [3, 3, 3, 3], loops: :forever,
                        blend: :add, scale: 0.78, offset: [0, -47], z_layer: :above)
          eng.spawn_vfx(:muzzle_r, sheet: "pf_vfx_w3_blue_flare", tx: 33.45, ty: 9.8,
                        grid: [4, 2], frames: [4, 5, 6, 5], ticks: [3, 3, 3, 3], loops: :forever,
                        blend: :add, scale: 0.78, offset: [0, -47], z_layer: :above)
          eng.zoom_map(1.18, duration: 0.95, focus: [30.0, 8.6], ease: :in_out)
          eng.wait(1.05)

          # ORIGIN PULSE vs BLUE FLARE LAUNCH!
          eng.actor(:kyogre).set_cell(5)
          eng.actor(:reshiram).set_cell(5)
          eng.actor(:valen).set_cell(10)
          eng.play_se("Anim/HyperBeam", volume: 100)
          eng.play_se("Anim/Fire6", volume: 95)
          eng.impact_beat(hitstop_sec: 0.12)

          mouth_l = 26.75
          mouth_r = 33.45
          # Center-anchored pure-pixel beams (invariant under mirror: true!) bridging mouth -> clash point!
          beam_l = eng.spawn_vfx(:beam_l, sheet: "pf_vfx_w3_origin_beam", tx: mouth_l + 0.3, ty: 9.8,
                                 grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: :forever,
                                 blend: :add, origin: :center, offset: [0, -47], z_layer: :above)
          beam_r = eng.spawn_vfx(:beam_r, sheet: "pf_vfx_w3_blue_flare", tx: mouth_r - 0.3, ty: 9.8,
                                 grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: :forever,
                                 blend: :add, mirror: true, origin: :center, offset: [0, -47], z_layer: :above)

          # 10-frame (0.33s) crisp beam extension to dead-center tx = 30.0!
          10.times do |fi|
            u = (fi + 1) / 10.0
            tip_l = mouth_l + (30.0 - mouth_l) * u
            tip_r = mouth_r - (mouth_r - 30.0) * u
            beam_l.set_tile((mouth_l + tip_l) * 0.5, 9.8)
            beam_r.set_tile((mouth_r + tip_r) * 0.5, 9.8)
            beam_l.set_scale([((tip_l - mouth_l) * 32.0) / 118.0, 0.12].max, 0.88)
            beam_r.set_scale([((mouth_r - tip_r) * 32.0) / 118.0, 0.12].max, 0.88)
            eng.step_frame
          end

          # DEAD-CENTER PURE-PIXEL CLASH COLLISION!
          eng.play_se("Anim/Explosion7", volume: 100)
          eng.play_se("Anim/Ice8", volume: 88)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash_ramp(color: [224, 248, 255], steps: [51, 136, 221, 255],
                         step_dur: 0.025, hold_dur: 0.08, fade_dur: 0.25)
          core = eng.spawn_vfx(:clash_core, sheet: "pf_vfx_w3_clash_core", tx: 30.0, ty: 9.8,
                               grid: [4, 2], frames: 0..3, ticks: [2, 2, 2, 2], loops: :forever,
                               blend: :add, scale: 1.28, offset: [0, -47], z_layer: :above)

          # Sustained 3.0s (90 frames) live beam tug-of-war as emerald Trinitite heat builds beneath!
          eng.shake(power: 6, duration: 3.05, decay: false)
          eng.zoom_map(1.32, duration: 0.85, focus: [30.0, 8.6], ease: :in_out)

          90.times do |fi|
            u = fi / 90.0
            cx = 30.0 + Math.sin(u * 13.0) * 0.86 * (1.0 - 0.28 * u)
            core.set_tile(cx, 9.8)
            pulse_y = 0.88 + 0.14 * Math.sin(fi * 0.85).abs
            beam_l.set_tile((mouth_l + cx) * 0.5, 9.8)
            beam_r.set_tile((mouth_r + cx) * 0.5, 9.8)
            beam_l.set_scale(((cx - mouth_l) * 32.0) / 116.0, pulse_y)
            beam_r.set_scale(((mouth_r - cx) * 32.0) / 116.0, pulse_y)

            if fi == 26
              eng.zoom_map(1.10, duration: 0.90, focus: [30.0, 8.6], ease: :in_out)
              eng.flash(color: [215, 246, 255], power: 135, duration: 0.12)
              eng.play_se("Anim/Ice2", volume: 82)
              eng.actor(:valen).set_cell(11)
              eng.spawn_vfx(nil, sheet: "pf_vfx_w3_glass_curtain", tx: 30.0, ty: 9.4,
                            grid: [4, 2], frames: [4, 5], ticks: [5, 14], stay: :forever,
                            blend: :normal, untoned: false, opacity: 155, scale: 0.52, z_layer: :floor)
            elsif fi == 56
              eng.flash(color: [255, 234, 200], power: 145, duration: 0.12)
              eng.play_se("Anim/Fire5", volume: 85)
            elsif fi == 78
              eng.flash(color: [216, 255, 236], power: 175, duration: 0.14)
              eng.play_se("Anim/Saint7", volume: 88, pitch: 112)
            end
            eng.step_frame
          end

          #---------------------------------------------------------------------
          # ACT III — 90° BANQUET-STYLE APEX PLATE (cut_ch19_war1_90deg.png)
          # (~22.8s .. 30.4s | 3.6s Pure Silent Text-Free Panoramic Hold!)
          #---------------------------------------------------------------------
          eng.flash(color: [232, 252, 255], power: 220, duration: 0.24)
          eng.show_cut_plate(
            "cut_ch19_war1_90deg",
            fade_in: 0.22, hold: 7.2, fade_out: 0.28,
            pan: { [-10, 4] => [10, -4] }, zoom: [1.02, 1.09], shake: 1.5
          ) do |e|
            # Subtle live pure-pixel spark shimmer along the clash seam without washing out the 90° art!
            e.spawn_vfx(:p19_sparks, sheet: "pf_vfx_w3_clash_core", tx: 30.0, ty: 8.6,
                        grid: [4, 2], frames: [2, 3, 2, 3], ticks: [4, 4, 4, 4], loops: :forever,
                        blend: :add, opacity: 52, scale: 0.55, z_layer: :above)
            # 3.6s PURE SILENT TEXT-FREE CONTEMPLATION of Kyogre vs Reshiram side-view!
            e.wait(3.60)
            e.say(:VALEN, :shocked, "Sea and fire... the sand is melting straight to glass!", hold: 1.25)
            e.wait(0.28)
            e.say(:KESTREL, :angry, "Look out— the seam's about to blow!!", hold: 1.05)
            e.stop_vfx(:p19_sparks)
          end

          #---------------------------------------------------------------------
          # ACT IV — 0.42s DEAD-SILENCE bgm_cut -> TRINITITE SHOCKWAVE &
          #          KESTREL'S AIRBORNE SHIELD INTERCEPT! (~30.4s .. 35.4s)
          #---------------------------------------------------------------------
          eng.stop_vfx(:beam_l)
          eng.stop_vfx(:beam_r)
          eng.stop_vfx(:muzzle_l)
          eng.stop_vfx(:muzzle_r)
          eng.stop_vfx(:clash_core)

          # LAW 2: 0.42s DIGITAL-ZERO AUDIO VACUUM + SINGLE CHILLING BELL!
          eng.bgm_cut
          eng.play_se("Anim/HealBell", volume: 96, pitch: 118)
          eng.wait(0.42)

          # MASSIVE EMERALD TRINITITE ERUPTION ACROSS MAP 926!
          eng.play_se("Anim/Ice8", volume: 100, pitch: 78)
          eng.play_se("Anim/Explosion7", volume: 96)
          eng.play_se("Anim/Saint7", volume: 88, pitch: 90)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash_ramp(color: [188, 255, 224], steps: [64, 152, 232, 255],
                         step_dur: 0.025, hold_dur: 0.12, fade_dur: 0.45)
          eng.shake(power: 7, duration: 0.72, decay: true)
          eng.zoom_map(1.0, duration: 0.65, ease: :out_cubic)
          eng.pan_camera_to(30.0, 9.6, duration: 0.55, ease: :out_cubic)

          # Single heroic central emerald Trinitite spire between the two titans (clean desert breathing room!)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_clash_core", tx: 30.0, ty: 9.4,
                        grid: [4, 2], frames: 4..7, ticks: [3, 4, 5, 16], stay: :forever,
                        blend: :normal, untoned: false, scale: 0.72, z_layer: :mid, origin: :foot)

          # Valen recoils backward shielding brow with sand kick!
          eng.actor(:valen).play_clip(
            sheet: "act_ch19_valen_command", grid: [4, 4],
            frames: [12, 13], ticks: [6, 16], stay: true
          )
          eng.actor(:valen).move_to(30.0, 11.75, duration: 0.34, walk: false, ease: :out)

          # EMOTE #1 (Earned!): Kestrel spots the emerald shockwave racing south -> SPRINT & AIRBORNE LEAP!
          eng.actor(:kestrel).show_emote(:exclaim, duration: 0.55)
          eng.play_se("Exclaim", volume: 92)
          eng.actor(:kestrel).play_clip(
            sheet: "act_ch19_kestrel_shield", grid: [4, 4],
            frames: [1, 2, 3], ticks: [3, 3, 4], stay: true
          )
          eng.actor(:kestrel).move_to(29.0, 12.25, duration: 0.28, walk: false, ease: :out)

          # Crisp, well-spaced perimeter vitrified glass shards so the Glass Dunes floor stays open & readable!
          [
            [[27.2, 9.2], [32.8, 9.2]],
            [[25.2, 10.9], [34.8, 10.9]],
            []
          ].each_with_index do |pair, pi|
            pair.each do |gx, gy|
              eng.spawn_vfx(nil, sheet: "pf_vfx_w3_glass_curtain", tx: gx, ty: gy,
                            grid: [4, 2], frames: 4..7, ticks: [3, 4, 5, 14], stay: :forever,
                            blend: :normal, untoned: false, opacity: 178, scale: 0.36, z_layer: :floor)
            end
            eng.play_se("Anim/Ice2", volume: 74, pitch: 88 + pi * 10)
            if pi == 1
              # Kestrel launches sideways airborne dive-leap directly in front of grounded PC!
              eng.play_se("Player jump", volume: 90)
              eng.actor(:kestrel).play_clip(
                sheet: "act_ch19_kestrel_shield", grid: [4, 4],
                frames: [4, 5, 6, 7], ticks: [4, 5, 4, 12], stay: true
              )
              eng.actor(:kestrel).move_to(30.0, 12.15, duration: 0.36, walk: false, arc_h: 22.0, ease: :out_cubic)
              # Grounded, natural Protagonist takes ONE calm steady defensive step back (ZERO jerky fidgeting!)
              eng.actor(:pc).move_to(30.0, 13.05, duration: 0.32, walk: true, dir: :up)
            end
            eng.wait(0.28)
          end

          # Kestrel absorbs shockwave crouch with emerald rim flash -> eases upright!
          eng.play_se("Player bump", volume: 76, pitch: 90)
          eng.actor(:kestrel).play_clip(
            sheet: "act_ch19_kestrel_shield", grid: [4, 4],
            frames: [8, 9, 10, 11], ticks: [5, 6, 7, 8], stay: true
          )
          eng.actor(:kyogre).play_clip(
            sheet: "act_war1_primal_kyogre", grid: [4, 2], frames: [6, 7], ticks: [12, 24], stay: true
          )
          eng.actor(:reshiram).play_clip(
            sheet: "act_war1_reshiram", grid: [4, 2], frames: [6, 7], ticks: [12, 24], stay: true
          )
          eng.wait(1.15)

          #---------------------------------------------------------------------
          # ACT V — Vitrified Silence, Truce & Larch's Radio Verdict (~35.4s .. 42.3s)
          #---------------------------------------------------------------------
          eng.set_tone(-16, 6, -4, 62, duration: 1.35)
          eng.play_bgm("ch19_aftermath", volume: 78, tag: "ch19_aftermath")

          # Valen recovers composed; Kestrel checks calmly on PC; Anja & Sigrun step onto vitrified glass
          eng.actor(:valen).play_clip(
            sheet: "act_ch19_valen_command", grid: [4, 4], frames: [14, 15], ticks: [10, 16], stay: true
          )
          eng.actor(:kestrel).play_clip(
            sheet: "act_ch19_kestrel_shield", grid: [4, 4], frames: [12, 13, 14, 15], ticks: [8, 10, 8, 16], stay: true
          )
          eng.actor(:anja).move_to(28.4, 11.5, duration: 0.95, walk: true, dir: :up)
          eng.actor(:sigrun).move_to(31.6, 11.5, duration: 0.95, walk: true, dir: :up)
          eng.wait(1.10)

          # EMOTE #2 (Restrained quiet grief!): Anja gazes across the glassed desert
          eng.actor(:anja).show_emote(:ellipsis, duration: 0.85)
          eng.wait(0.55)

          eng.say(:SIGRUN, :neutral, "Father. Enough.", hold: 0.78)
          eng.wait(0.24)
          eng.say(:SIGRUN, :sad, "Nobody won this morning that the dead would agree with.", hold: 1.15)
          eng.wait(0.26)
          eng.say(:ANJA, :sad, "Eirik... the glass stops here. The Boon will settle it.", hold: 1.15)
          eng.wait(0.30)
          eng.say(:LARCH, :neutral, "That wasn't a battle to them.", hold: 0.82, name: "Larch (Radio)")
          eng.wait(0.28)
          eng.say(:LARCH, :deadpan, "That was a reading.", hold: 1.15, name: "Larch (Radio)")

          eng.wait(0.85)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.55)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # WAVE-3 SCENE 2 — Ch15 CE-1 Glassfall Rethink (~36s, Map 295 -> AF 290 -> 295)
      # "Through Her Eyes — AF 290 Sanctuary Fracture & 90° Cathedral Apex Plate"
      #-------------------------------------------------------------------------
      # DIRECTOR'S NOTE STRICTLY ENFORCED:
      #   - ZERO Protagonist inside the AF 290 historical flashback!
      #   - Grounded, calm Protagonist appears ONLY in present-day framing
      #     before and after the historical vision.
      # Emote Count: STRICTLY 2 (:exclaim on Young Voss when sky cracks,
      #              :ellipsis on present-day Kestrel when Echo Morwen turns).
      # Pure-Pixel VFX: pf_vfx_w3_glass_curtain, pf_vfx_w3_prism_light.
      # Acting Sheet:   act_ch15_glassfall_brace (JUNO.png anchored).
      # 90° Apex Plate: cut_ch15_glassfall_90deg.png (3.8s silent text-free hold!).
      #=========================================================================
      def pf_play_ch15_glassfall_rethink(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Present-Day Hollow Cathedral Framing (~0.0s .. 6.8s)
          #---------------------------------------------------------------------
          eng.transfer_map(295, 15.0, 14.0, hide_player: true)
          ev_prior = $game_map.events[2]
          ev_prior.transparent = true if ev_prior

          eng.set_tone(-46, -42, -18, 38, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch15_ominous", volume: 80, tag: "ch15_ominous")

          # Present-day party standing calmly and naturally (ZERO jerky movement!)
          eng.spawn_actor(:kestrel, sheet: "KESTREL",                 tx: 15.0, ty: 11.4, dir: :down, is_charset: true)
          eng.spawn_actor(:ysolde,  sheet: "YSOLDE",                  tx: 12.8, ty: 14.4, dir: :up,   is_charset: true)
          eng.spawn_actor(:juno,    sheet: "act_ch15_glassfall_brace", tx: 17.2, ty: 14.4, grid: [4, 4], is_charset: false)
          eng.spawn_actor(:pc,      sheet: "PLAYER_A",                tx: 15.0, ty: 15.8, dir: :up,   is_charset: true)
          eng.actor(:juno).set_cell(15)

          eng.wait(1.05)
          eng.play_se("Anim/HealBell", volume: 90, pitch: 112)
          eng.play_se("Anim/Saint7", volume: 84)
          eng.flash(color: [228, 244, 255], power: 175, duration: 0.25)
          eng.shake(power: 3, duration: 0.30)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_prism_light", tx: 15.0, ty: 11.4,
                        grid: [4, 2], frames: [4, 5, 4, 5], ticks: [4, 4, 4, 4],
                        blend: :add, scale: 0.95, z_layer: :above)
          eng.wait(0.85)

          eng.say(:KESTREL, :angry, "Ten years, Ysolde. 'When he's ready.'", hold: 0.95)
          eng.wait(0.28)
          eng.say(:KESTREL, :angry, "I'm ready. Watch what really happened.", hold: 1.15)
          eng.wait(0.35)

          #---------------------------------------------------------------------
          # ACT II — AF 290 HISTORICAL VISION (STRICTLY ZERO PROTAGONIST!!)
          # (~6.8s .. 21.0s)
          #---------------------------------------------------------------------
          eng.flash_ramp(color: [255, 240, 206], steps: [44, 128, 214, 255],
                         step_dur: 0.03, hold_dur: 0.12, fade_dur: 0.40)
          eng.wait(0.45)
          eng.clear_actors
          eng.clear_vfxs
          # Iconic warm AF 290 sepia memory tone
          eng.set_tone(28, 12, -26, 95, duration: 0.0)

          # Historical AF 290 Sanctuary Cast — ZERO PLAYER_A ANYWHERE IN THIS VISION!
          eng.spawn_actor(:valen,   sheet: "VALEN",                   tx: 15.0, ty: 10.6, dir: :down, is_charset: true)
          eng.spawn_actor(:ines,    sheet: "trainer_LADY",            tx: 13.6, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:ch1,     sheet: "trainer_LASS",            tx: 12.2, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:ch2,     sheet: "NPC 04",                  tx: 16.4, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:ch3,     sheet: "NPC 11",                  tx: 17.8, ty: 11.5, dir: :down, is_charset: true)
          eng.spawn_actor(:voss,    sheet: "VOSS",                    tx: 19.4, ty: 11.1, dir: :left, is_charset: true)
          eng.spawn_actor(:obs,     sheet: "trainer_SCIENTIST",       tx: 20.6, ty: 11.3, dir: :left, is_charset: true)
          eng.spawn_actor(:child,   sheet: "NPC 02",                  tx: 15.0, ty: 14.5, dir: :up,   is_charset: true)
          eng.spawn_actor(:morwen,  sheet: "MORWEN",                  tx: 10.8, ty: 14.9, dir: :right, is_charset: true)
          # Archivist Witness bracing across the nave using our bespoke 4x4 brace sheet!
          eng.spawn_actor(:witness, sheet: "act_ch15_glassfall_brace", tx: 18.2, ty: 14.6, grid: [4, 4], is_charset: false)
          eng.actor(:witness).set_cell(0)

          # Soft luminous memory motes drifting slowly through the AF 290 nave
          [[11.5, 12.2], [15.0, 12.6], [18.5, 12.2]].each_with_index do |(mx, my), mi|
            eng.spawn_vfx(:"mote_#{mi}", sheet: "pf_vfx_w3_prism_light", tx: mx, ty: my,
                          grid: [4, 2], frames: [4, 5], ticks: [10, 10], loops: :forever,
                          blend: :add, opacity: 125, scale: 0.72, z_layer: :above)
          end

          eng.zoom_map(1.22, duration: 1.35, focus: [17.4, 11.4], ease: :in_out)
          eng.wait(1.55)
          eng.say(:VOSS, :neutral, "The Choir's note is climbing.", hold: 0.90, name: "Young Voss")
          eng.wait(0.28)
          eng.say(:VOSS, :neutral, "Hold the Crown steady— eighteen Plates, one reading.", hold: 1.15, name: "Young Voss")

          # Pressure drops -> witness's veil lifts -> sky cracks cleanly overhead!
          eng.zoom_map(1.26, duration: 0.90, focus: [15.0, 12.2], ease: :in_out)
          eng.actor(:witness).play_clip(
            sheet: "act_ch15_glassfall_brace", grid: [4, 4],
            frames: [1, 2, 3], ticks: [7, 8, 8], stay: true
          )
          # EMOTE #1 (Earned!): Young Voss snaps up as the harmonic overloads!
          eng.actor(:voss).show_emote(:exclaim, duration: 0.65)
          eng.play_se("Anim/Saint7", volume: 88, pitch: 118)
          eng.play_se("Anim/Ice5", volume: 84)
          eng.spawn_vfx(:fracture_hi, sheet: "pf_vfx_w3_glass_curtain", tx: 15.0, ty: 9.2,
                        grid: [4, 2], frames: [4, 5, 6], ticks: [4, 4, 8], stay: 0.65,
                        blend: :add, opacity: 195, scale: 0.85, z_layer: :above)
          eng.wait(1.05)

          # LAW 2: 0.40s DIGITAL-ZERO DEAD-SILENCE VACUUM + CRACKING BELL!
          eng.bgm_cut
          eng.play_se("Anim/HealBell", volume: 100, pitch: 70)
          eng.play_se("Anim/Ice8", volume: 92, pitch: 112)
          eng.wait(0.40)

          # THE GLASSFALL SHARD CURTAIN DROPS!!
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash(color: [224, 255, 240], power: 235, duration: 0.28)
          eng.shake(power: 6, duration: 0.70)
          eng.play_bgm("ch15_decretum", volume: 88, tag: "ch15_decretum")
          eng.zoom_map(1.0, duration: 0.55, ease: :out_cubic)

          # Witness drops into crisp high-contrast eye-shield forearm crouch (frames 4..7)!
          eng.actor(:witness).play_clip(
            sheet: "act_ch15_glassfall_brace", grid: [4, 4],
            frames: [4, 5, 6, 7, 9, 10], ticks: [6, 7, 7, 8, 8, 8], stay: true
          )
          # Morwen dashes to shield the 5-year-old child!
          eng.actor(:morwen).move_to(14.3, 14.6, duration: 0.60, walk: true, dir: :right)

          # Pure-pixel diagonal emerald shard curtain raining across pews & creeping vitrified floor cracks!
          [[11.0, 11.4], [15.0, 11.6], [19.0, 11.4], [12.8, 15.0], [17.4, 15.0]].each_with_index do |(rx, ry), ri|
            eng.spawn_vfx(nil, sheet: "pf_vfx_w3_glass_curtain", tx: rx, ty: ry,
                          grid: [4, 2], frames: 0..3, ticks: [3, 3, 4, 4], loops: 2,
                          blend: :add, scale: 1.15, z_layer: :above)
            eng.wait(0.14) if ri.even?
          end
          eng.play_se("Anim/Ice8", volume: 94, pitch: 86)

          [[10.4, 13.6], [19.6, 13.6], [10.6, 16.2], [19.4, 16.2]].each_with_index do |(cx, cy), ci|
            eng.spawn_vfx(:"gspire_#{ci}", sheet: "pf_vfx_w3_glass_curtain", tx: cx, ty: cy,
                          grid: [4, 2], frames: 4..7, ticks: [4, 4, 5, 14], stay: :forever,
                          blend: :normal, untoned: false, scale: 0.90, z_layer: :mid, origin: :foot)
            eng.play_se("Anim/Ice2", volume: 72, pitch: 92 + ci * 8) if ci.even?
            eng.wait(0.28)
          end

          # Morwen's Mismagius rises calmly over the shielded child
          eng.spawn_actor(:mismagius, sheet: "Followers/MISMAGIUS", tx: 15.9, ty: 14.4,
                          dir: :left, grid: [4, 4], is_charset: true)
          eng.actor(:mismagius).opacity = 225
          eng.play_cry(:MISMAGIUS, volume: 82)
          eng.wait(1.35)

          #---------------------------------------------------------------------
          # ACT III — 90° BANQUET-STYLE APEX PLATE (cut_ch15_glassfall_90deg.png)
          # (~21.0s .. 30.2s | 3.8s Pure Silent Text-Free Contemplation!)
          #---------------------------------------------------------------------
          eng.show_cut_plate(
            "cut_ch15_glassfall_90deg",
            fade_in: 0.25, hold: 9.0, fade_out: 0.30,
            pan: { [0, 6] => [0, -6] }, zoom: [1.02, 1.08], shake: 0
          ) do |e|
            # Live pure-pixel falling prism motes drifting gently over the cathedral arches!
            e.spawn_vfx(:p15_motes, sheet: "pf_vfx_w3_prism_light", tx: 15.0, ty: 12.8,
                        grid: [4, 2], frames: [4, 5, 4, 5], ticks: [8, 8, 8, 8], loops: :forever,
                        blend: :add, opacity: 120, scale: 1.05, z_layer: :above)
            # 3.8s PURE SILENT TEXT-FREE HOLD letting Decretum & Morwen's embrace breathe!
            e.wait(3.80)
            e.say(:VALEN, :angry, "Find the child. Whatever it costs.", hold: 1.15)
            e.wait(0.32)
            e.say(:MORWEN, :sad, "Take them to Edda's boat at midnight.", hold: 1.05)
            e.wait(0.28)
            e.say(:MORWEN, :crying, "I'll carry the name... Kestrel, I'm sorry.", hold: 1.30)
            e.wait(0.40)
            e.stop_vfx(:p15_motes)
          end

          #---------------------------------------------------------------------
          # ACT IV — RETURN TO PRESENT-DAY CATHEDRAL (Grounded PC & Echo Morwen)
          # (~30.2s .. 36.2s)
          #---------------------------------------------------------------------
          eng.flash(color: [192, 224, 255], power: 185, duration: 0.42)
          eng.clear_actors
          eng.clear_vfxs
          eng.set_tone(-38, -28, 4, 62, duration: 0.90)
          eng.pan_camera_to(15.0, 14.8, duration: 0.65, ease: :in_out)

          # Present-day Protagonist stands calmly and naturally beside Kestrel, Ysolde & grieving Juno!
          eng.spawn_actor(:pc,          sheet: "PLAYER_A",                 tx: 15.0, ty: 16.4, dir: :up,   is_charset: true)
          eng.spawn_actor(:kestrel,     sheet: "KESTREL",                  tx: 12.6, ty: 13.0, dir: :down, is_charset: true)
          eng.spawn_actor(:ysolde,      sheet: "YSOLDE",                   tx: 17.4, ty: 13.0, dir: :down, is_charset: true)
          eng.spawn_actor(:juno,        sheet: "act_ch15_glassfall_brace", tx: 17.2, ty: 15.8, grid: [4, 4], is_charset: false)
          eng.spawn_actor(:echo_morwen, sheet: "trainer_ECHO_MORWEN",      tx: 15.0, ty: 13.8, dir: :up,   is_charset: true)
          eng.actor(:juno).play_clip(
            sheet: "act_ch15_glassfall_brace", grid: [4, 4], frames: [15, 14, 15], ticks: [10, 12, 20], stay: true
          )
          eng.actor(:echo_morwen).opacity = 205
          # Render spectral halo BEHIND Echo Morwen (:floor) so her face & 10-year turn read razor clear!
          eng.spawn_vfx(:echo_halo, sheet: "pf_vfx_w3_prism_light", tx: 15.0, ty: 13.8,
                        grid: [4, 2], frames: [4, 5], ticks: [8, 8], loops: :forever,
                        blend: :add, opacity: 145, scale: 0.66, z_layer: :floor)
          eng.wait(1.25)

          # Impossibly across ten years, Echo Morwen turns straight :down at the Protagonist!
          eng.actor(:echo_morwen).set_dir(:down)
          # EMOTE #2 (Quiet stunned hush!): Kestrel freezes witnessing the impossible turn
          eng.actor(:kestrel).show_emote(:ellipsis, duration: 0.90)
          eng.play_se("Anim/HealBell", volume: 84, pitch: 105)
          eng.zoom_map(1.26, duration: 0.95, focus: :echo_morwen, ease: :in_out)
          eng.wait(1.10)

          eng.say(:MORWEN, :neutral, "Little one. You came back.", hold: 1.05, name: "Echo Morwen")
          eng.wait(0.32)
          eng.say(:MORWEN, :sad, "I told her not to let you.", hold: 1.35, name: "Echo Morwen")

          # Echo Morwen dissolves softly into pure-pixel golden-silver motes
          eng.stop_vfx(:echo_halo)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_prism_light", tx: 15.0, ty: 13.8,
                        grid: [4, 2], frames: [5, 4, 5], ticks: [6, 6, 8], fade: 0.45,
                        blend: :add, scale: 0.85, z_layer: :above)
          24.times do |fi|
            eng.actor(:echo_morwen).opacity = (205 * (1.0 - (fi + 1) / 24.0)).round
            eng.step_frame
          end
          eng.remove_actor(:echo_morwen)
          eng.actor(:juno).set_cell(15)
          eng.zoom_map(1.0, duration: 0.70, ease: :out)
          eng.wait(0.55)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.55)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # WAVE-3 SCENE 3 — Ch21 Arceus Finale Rethink (~44s, Map 285 Summit Terrace)
      # "The Ring, The Kneel & The Dawn — 18 Golden Astral Locks, Valen's
      #  Sacrifice & 90° Crownhaven Apex Plate"
      #-------------------------------------------------------------------------
      # Emote Count: STRICTLY 2 (:exclaim on Voss when Lock #18 shatters,
      #              :ellipsis on Ilsa gazing at Valen's empty cracked Crown).
      # Protagonist: Completely grounded & natural (steady observational stance,
      #              single calm purposeful step forward when Lock #18 opens).
      # Pure-Pixel VFX: pf_vfx_w3_arceus_locks, pf_vfx_w3_prism_light.
      # Acting Sheets:  act_ch21_valen_kneel, act_ch21_arceus_bound.
      # 90° Apex Plate: cut_ch21_valen_90deg.png (4.2s silent text-free hold!).
      #=========================================================================
      def pf_play_ch21_arceus_rethink(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I — Bound Creator & Ornate Golden Astral Locks (~0.0s .. 8.8s)
          #---------------------------------------------------------------------
          eng.transfer_map(285, 48.5, 22.8, hide_player: true)
          [1, 2].each do |eid|
            ev = $game_map.events[eid]
            ev.transparent = true if ev
          end

          eng.set_tone(-48, -64, -18, 46, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ch21_arceus_bound", volume: 84, tag: "ch21_arceus_bound")

          # Cast staged cleanly on Map 285 white-stone summit terrace (PC balanced right, clear view of Valen & Crown!)
          eng.spawn_actor(:valen,     sheet: "act_ch21_valen_kneel", tx: 48.5, ty: 24.4, grid: [4, 4], is_charset: false, z_bias: 6)
          eng.spawn_actor(:ilsa,      sheet: "ILSA",                 tx: 47.1, ty: 24.8, dir: :up, is_charset: true)
          eng.spawn_actor(:voss,      sheet: "VOSS",                 tx: 51.8, ty: 23.8, dir: :up, is_charset: true)
          eng.spawn_actor(:pc,        sheet: "PLAYER_A",             tx: 49.5, ty: 26.2, dir: :up, is_charset: true)
          eng.spawn_actor(:celestine, sheet: "CELESTINE",            tx: 44.6, ty: 25.4, dir: :up, is_charset: true)
          eng.spawn_actor(:kestrel,   sheet: "KESTREL",              tx: 52.4, ty: 25.4, dir: :up, is_charset: true)
          eng.actor(:valen).set_cell(0)

          # Bound Arceus suspended high above terrace framed by pure-pixel Golden Astral Rune Seals!
          eng.spawn_actor(:arceus, sheet: "act_ch21_arceus_bound", tx: 48.5, ty: 21.0,
                          grid: [4, 2], is_charset: false, z_bias: 35)
          eng.actor(:arceus).play_clip(
            sheet: "act_ch21_arceus_bound", grid: [4, 2], frames: [0, 1, 0, 1],
            ticks: [10, 10, 10, 10], loops: :forever
          )
          eng.spawn_vfx(:locks_main, sheet: "pf_vfx_w3_arceus_locks", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [0, 1], ticks: [9, 9], loops: :forever,
                        blend: :add, scale: 1.04, z_layer: :above)
          eng.spawn_vfx(:lock_l, sheet: "pf_vfx_w3_arceus_locks", tx: 46.2, ty: 20.4,
                        grid: [4, 2], frames: [0, 1], ticks: [11, 11], loops: :forever,
                        blend: :add, opacity: 175, scale: 0.56, z_layer: :above)
          eng.spawn_vfx(:lock_r, sheet: "pf_vfx_w3_arceus_locks", tx: 50.8, ty: 20.4,
                        grid: [4, 2], frames: [1, 0], ticks: [11, 11], loops: :forever,
                        blend: :add, opacity: 175, scale: 0.56, z_layer: :above)

          eng.play_cry(:ARCEUS, volume: 100)
          eng.shake(power: 4, duration: 0.55)
          eng.zoom_map(1.24, duration: 1.25, focus: [48.5, 20.5], ease: :in_out)
          eng.wait(1.85)
          eng.zoom_map(1.0, duration: 0.55, ease: :out)
          eng.pan_camera_to(48.5, 22.9, duration: 0.55, ease: :in_out)
          eng.wait(0.75)

          eng.say(:VOSS, :shocked, "Eighteen Plates. Eighteen golden locks.", hold: 1.05)
          eng.wait(0.32)
          eng.say(:VOSS, :happy, "Look at it— it's magnificent!", hold: 1.15)

          #---------------------------------------------------------------------
          # ACT II — Holding the Door & Pure-Pixel Dawn Pillar Shattering Lock #18
          # (~8.8s .. 20.2s)
          #---------------------------------------------------------------------
          eng.zoom_map(1.16, duration: 0.80, focus: [48.5, 23.8], ease: :in_out)
          eng.play_se("Anim/Saint7", volume: 84)
          # Valen spreads both hands wide gripping the Concordance Ring pylons!
          eng.actor(:valen).play_clip(
            sheet: "act_ch21_valen_kneel", grid: [4, 4],
            frames: [1, 2, 3, 2], ticks: [8, 8, 8, 8], loops: :forever
          )
          eng.wait(1.05)

          eng.say(:ILSA, :neutral, "I've got you, Father. Little owl's got you.", hold: 1.25)
          eng.wait(0.34)
          eng.say(:VALEN, :neutral, "Go. Free it.", hold: 0.85)
          eng.wait(0.28)
          eng.say(:VALEN, :neutral, "I'll hold the door. I've had thirty years of practice.", hold: 1.35)
          eng.wait(0.40)

          # Grounded, calm Protagonist takes ONE steady purposeful step forward (unobstructed center view!)
          eng.actor(:pc).move_to(49.5, 25.5, duration: 0.65, walk: true, dir: :up)
          eng.pan_camera_to(48.5, 22.4, duration: 0.60, ease: :in_out)
          eng.zoom_map(1.0, duration: 0.55, ease: :out)
          eng.set_tone(-74, -76, -44, 62, duration: 0.65)

          # Lock #18 overheats white-gold as pure-pixel divine prism pillar ascends!
          eng.stop_vfx(:locks_main)
          eng.stop_vfx(:lock_l)
          eng.stop_vfx(:lock_r)
          eng.spawn_vfx(:lock_overheat, sheet: "pf_vfx_w3_arceus_locks", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [2, 3], ticks: [10, 12], stay: :forever,
                        blend: :add, scale: 1.12, z_layer: :above)
          eng.actor(:arceus).play_clip(
            sheet: "act_ch21_arceus_bound", grid: [4, 2], frames: [2, 3], ticks: [14, 16], stay: true
          )

          # Continuous spiraling pure-pixel divine light pillar (ZERO flat pink rectangle!)
          eng.play_se("Anim/Charge_Beam", volume: 95)
          eng.play_se("Anim/HyperBeam", volume: 88, pitch: 112)
          eng.shake(power: 5, duration: 1.65, decay: false)
          eng.spawn_vfx(:pillar_bot, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 23.6,
                        grid: [4, 2], frames: 0..3, ticks: [3, 3, 3, 3], loops: :forever,
                        blend: :add, scale: 1.05, z_layer: :above)
          eng.spawn_vfx(:pillar_top, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 20.2,
                        grid: [4, 2], frames: [2, 3, 0, 1], ticks: [3, 3, 3, 3], loops: :forever,
                        blend: :add, scale: 1.05, z_layer: :above)
          eng.zoom_map(1.22, duration: 1.35, focus: [48.5, 20.8], ease: :in_out)
          eng.wait(1.75)

          # LOCK #18 SHATTERS!! Chain explosion + flying golden lock fragments + radiant starburst!
          eng.stop_vfx(:lock_overheat)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_arceus_locks", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [4, 5, 6, 7], ticks: [4, 5, 5, 6],
                        blend: :add, scale: 1.35, z_layer: :above)
          eng.spawn_vfx(nil, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 19.6,
                        grid: [4, 2], frames: [6, 7], ticks: [5, 7],
                        blend: :add, scale: 1.0, grow: [0.85, 2.35, 0.55], fade: 0.25, z_layer: :above)
          # EMOTE #1 (Earned!): Voss reels in shock as all eighteen golden locks burst!
          eng.actor(:voss).show_emote(:exclaim, duration: 0.65)
          eng.play_se("Anim/Explosion7", volume: 96)
          eng.play_se("Anim/Ice8", volume: 94, pitch: 115)
          eng.impact_beat(hitstop_sec: 0.14)
          eng.flash_ramp(color: [255, 248, 224], steps: [64, 152, 232, 255],
                         step_dur: 0.025, hold_dur: 0.10, fade_dur: 0.35)
          eng.wait(0.65)

          #---------------------------------------------------------------------
          # ACT III — 0.45s DEAD-SILENCE VACUUM -> VALEN DROPS TO ONE KNEE!
          # (~20.2s .. 28.4s)
          #---------------------------------------------------------------------
          eng.stop_vfx(:pillar_bot)
          eng.stop_vfx(:pillar_top)

          # LAW 2: 0.45s DIGITAL-ZERO AUDIO VACUUM + SOLITARY CHIME!
          eng.bgm_cut
          eng.play_se("Anim/HealBell", volume: 98, pitch: 100)
          eng.wait(0.45)

          # T-KT enters warmly as dawn tone washes across Briar Hall summit!
          eng.play_bgm("ch21_tkt", volume: 88, tag: "ch21_tkt")
          eng.set_tone(12, 8, -4, 16, duration: 1.25)
          eng.zoom_map(1.14, duration: 1.05, focus: [48.5, 23.4], ease: :in_out)

          # Valen recoils -> Crown slips off brow -> drops to ONE KNEE -> Crown clatters on marble -> looks UP in peace!
          eng.actor(:valen).play_clip(
            sheet: "act_ch21_valen_kneel", grid: [4, 4],
            frames: [4, 5, 6, 7, 8, 9, 10],
            ticks: [5, 7, 6, 8, 12, 12, 18],
            se: { 3 => "Anim/HealBell" },
            stay: true
          )
          eng.spawn_vfx(:valen_motes, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 24.2,
                        grid: [4, 2], frames: [4, 5], ticks: [9, 9], loops: :forever,
                        blend: :add, opacity: 145, scale: 0.78, z_layer: :floor)
          eng.wait(3.15)

          eng.say(:VALEN, :happy, "Little owl...", hold: 0.95)
          eng.wait(0.38)
          eng.say(:VALEN, :happy, "Velmora is free.", hold: 1.25)
          eng.wait(0.40)

          #---------------------------------------------------------------------
          # ACT IV — 90° BANQUET-STYLE APEX PLATE (cut_ch21_valen_90deg.png)
          # (~28.4s .. 35.8s | 4.2s Pure Silent Text-Free Emotional Peak!)
          #---------------------------------------------------------------------
          eng.show_cut_plate(
            "cut_ch21_valen_90deg",
            fade_in: 0.28, hold: 7.4, fade_out: 0.35,
            pan: { [-8, 4] => [8, -4] }, zoom: [1.02, 1.08], shake: 0
          ) do |e|
            # Live falling golden dawn motes floating over Ilsa, Valen, cracked Crown & Arceus!
            e.spawn_vfx(:p21_motes, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 22.8,
                        grid: [4, 2], frames: [4, 5, 4, 5], ticks: [9, 9, 9, 9], loops: :forever,
                        blend: :add, opacity: 120, scale: 0.96, z_layer: :above)
            # 4.2s COMPLETELY SILENT, TEXT-FREE CONTEMPLATION at T-KT's soaring peak!
            e.wait(4.20)
            e.say(:ILSA, :crying, "...Father.", hold: 1.55)
            e.wait(0.55)
            e.stop_vfx(:p21_motes)
          end

          #---------------------------------------------------------------------
          # ACT V — EMPTY CRACKED CROWN, FREED ARCEUS & GOLDEN DAWN (~35.8s .. 44.3s)
          #---------------------------------------------------------------------
          eng.set_tone(24, 18, 4, 6, duration: 1.25)
          eng.zoom_map(1.0, duration: 0.85, ease: :out_cubic)
          eng.pan_camera_to(48.5, 22.9, duration: 0.85, ease: :in_out)

          # Valen ascends gently into sunlit golden motes -> ONLY the empty cracked Crown stays on the stone (frame 15)!
          eng.actor(:valen).play_clip(
            sheet: "act_ch21_valen_kneel", grid: [4, 4],
            frames: [11, 12, 13, 14, 15],
            ticks: [8, 9, 9, 10, 24],
            se: { 4 => "Anim/HealBell" },
            stay: true
          )
          eng.actor(:ilsa).move_to(47.4, 24.9, duration: 0.70, walk: true, dir: :right)
          eng.wait(1.95)
          eng.stop_vfx(:valen_motes)

          # EMOTE #2 (Quiet reverent grief!): Ilsa pauses beside the empty cracked Sovereign Crown
          eng.actor(:ilsa).show_emote(:ellipsis, duration: 0.95)
          eng.wait(0.85)

          # Freed Radiant Arceus descends serenely IN FRONT OF pure-pixel golden starburst (:floor z=5 BEHIND Arceus!)
          eng.actor(:arceus).play_clip(
            sheet: "act_ch21_arceus_bound", grid: [4, 2], frames: [4, 5, 6, 7],
            ticks: [7, 8, 10, 24], stay: true
          )
          eng.actor(:arceus).move_to(48.5, 21.8, duration: 1.40, walk: false, ease: :out_cubic)
          eng.spawn_vfx(:arceus_dawn, sheet: "pf_vfx_w3_prism_light", tx: 48.5, ty: 20.6,
                        grid: [4, 2], frames: [6, 7], ticks: [10, 10], loops: :forever,
                        blend: :add, opacity: 150, scale: 1.18, spin: 12.0, z_layer: :floor)
          eng.wait(1.45)

          eng.play_cry(:ARCEUS, volume: 95)
          eng.play_se("Anim/Saint7", volume: 90, pitch: 108)
          eng.flash(color: [255, 248, 214], power: 185, duration: 0.36)
          eng.spawn_vfx(:dawn_spark_l, sheet: "pf_vfx_w3_prism_light", tx: 46.6, ty: 23.0,
                        grid: [4, 2], frames: [4, 5], ticks: [9, 9], loops: :forever,
                        blend: :add, opacity: 145, scale: 0.72, z_layer: :above)
          eng.spawn_vfx(:dawn_spark_r, sheet: "pf_vfx_w3_prism_light", tx: 50.4, ty: 23.0,
                        grid: [4, 2], frames: [5, 4], ticks: [9, 9], loops: :forever,
                        blend: :add, opacity: 145, scale: 0.72, z_layer: :above)
          eng.wait(1.10)

          eng.say(:ILSA, :crying, "Little light. You have carried me far.", hold: 1.25, name: "Arceus (via Ilsa)")
          eng.wait(0.36)
          eng.say(:ILSA, :happy, "I will not take what is not given.", hold: 1.45, name: "Arceus (via Ilsa)")

          eng.wait(1.15)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.65)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end

      #=========================================================================
      # SCENE E (LIVE DIRECTOR'S CUT v2) — Ruin R7: "Gilded King Aurelius"
      # Target Duration: ~36.2s (~1,086 frames @ 30fps)
      # Live Map: NEW Sculpted Map 186 (Grand Meridian Ballroom — 5x5 Golden
      #           Sunburst Medallion & Elevated Crimson Royal Dais; swaps 186->491)
      # Canon: story/42_SCRIPT_RUIN_KING.md (R7 "The mirror breach" -> "The challenge").
      # [PF] The King's lines below are the script's, word for word (2c3c22b); his ids are AURELIUS.
      #      In the script the Kneel / Refuse choice and :ruin_voss fall between ACT III and ACT IV:
      #      split this scene there when it is staged on map 491.
      # CRITICAL GUARDRAIL (Reuben): personality only, never Fate powers!
      #   ZERO Gate of Babylon portals | ZERO floating swords/spears/halberds |
      #   ZERO Enkidu-from-portals whips | ONE single gilded Poke Ball | <= 3 emotes!
      #=========================================================================
      def play_ruin_aurelius_dc(capture_dir: nil, capture_fps: 30)
        eng = Engine.new(capture_dir: capture_dir, capture_fps: capture_fps)
        begin
          #---------------------------------------------------------------------
          # ACT I (0.0–6.0s) — The Mirror Breach & Slow Sovereign Descent
          #---------------------------------------------------------------------
          eng.transfer_map(186, 13.5, 11.4, hide_player: true)
          # Hide static Gala guests; KEEP ev[3] ("Replica" golden keystone cradle on crimson dais!)
          $game_map.events.each do |eid, ev|
            ev.transparent = true if eid >= 4
          end

          eng.set_tone(-44, -44, -30, 48, duration: 0.0)
          eng.letterbox(true, height: 32, duration: 0.0)
          eng.play_bgm("ruin_intro_organ", volume: 82, tag: "ruin_intro_organ")

          # Cast positioned strictly on NEW Map 186 sculpted marble & crimson runner (zero furniture clip!)
          eng.spawn_actor(:valen, sheet: "VALEN",    tx: 9.8,  ty: 12.6, dir: :right, is_charset: true)
          eng.spawn_actor(:pc,    sheet: "PLAYER_A", tx: 13.5, ty: 16.4, dir: :up,    is_charset: true)
          eng.spawn_actor(:voss,  sheet: "VOSS",     tx: 14.8, ty: 17.8, dir: :up,    is_charset: true)

          # Camera tilts up to the elevated crimson dais as the Keystone Cradle flares rich antique gold!
          eng.pan_camera_to(13.5, 8.6, duration: 0.75, ease: :in_out)
          eng.wait(0.60)
          eng.play_se("Anim/HealBell", volume: 88, pitch: 118)
          eng.play_se("Anim/Saint7", volume: 86, pitch: 96)
          eng.flash(color: [255, 224, 132], power: 195, duration: 0.45)
          # Rich antique-gold cathedral tone over NEW cream-stone ballroom & 5x5 golden sunburst medallion!
          eng.set_tone(-18, -24, -46, 12, duration: 0.85)

          # Pure-pixel Aureate cathedral light shafts & drifting gold leaf (ZERO portals/swords!)
          [[11.2, 8.5, 0], [13.5, 7.6, 1], [15.8, 8.5, 2]].each_with_index do |(sx, sy, ph), si|
            eng.spawn_vfx(:"gold_shaft_#{si}", sheet: "pf_vfx_ruin_gold_aura", tx: sx, ty: sy,
                          grid: [4, 2], frames: [ph % 4, (ph + 1) % 4, (ph + 2) % 4, (ph + 3) % 4],
                          ticks: [12, 12, 12, 12], loops: :forever,
                          blend: :add, opacity: 96, scale: 1.30, z_layer: :above)
          end
          [[10.6, 11.4, 0], [16.4, 11.4, 2], [13.5, 13.0, 1]].each_with_index do |(mx, my, ph), mi|
            eng.spawn_vfx(:"gold_leaf_#{mi}", sheet: "pf_vfx_ruin_gold_aura", tx: mx, ty: my,
                          grid: [4, 2], frames: [4 + (ph % 4), 4 + ((ph + 1) % 4), 4 + ((ph + 2) % 4), 4 + ((ph + 3) % 4)],
                          ticks: [10, 10, 10, 10], loops: :forever,
                          blend: :add, opacity: 165, scale: 0.96, z_layer: :above)
          end

          # Gilded King Aurelius manifests atop the crimson dais and descends slowly down the grand marble stairs!
          eng.spawn_actor(:aurelius, sheet: "AURELIUS", tx: 13.5, ty: 6.2, dir: :down, is_charset: true)
          eng.wait(0.40)
          eng.actor(:aurelius).move_to(13.5, 10.6, duration: 2.15, walk: true, dir: :down)
          eng.actor(:voss).move_to(15.2, 11.4, duration: 1.75, walk: true, dir: :up)
          eng.pan_camera_to(13.5, 11.8, duration: 2.05, ease: :in_out)
          eng.wait(2.15)
          eng.actor(:voss).set_dir(:left)

          eng.say(:VOSS, :happy, "Your Majesty! Look at what House Aurel built for you! Eighteen locks, calibrated to the splinter. No crude iron: pure current! The god will have nowhere left to—", hold: 0.85)

          #---------------------------------------------------------------------
          # ACT II (6.0–17.2s) — Contempt, Cosmic Air Drop & Physical Voss Toss!
          #   Proposal §3.4: NO Enkidu chains/portals — pure physical gauntlet flick!
          #---------------------------------------------------------------------
          eng.bgm_cut
          eng.actor(:aurelius).set_pose("act_ruin_aurelius_pose", 0) # Arms crossed, imperious royal stance
          eng.play_se("Anim/metal", volume: 82, pitch: 122)          # Hollow tinny knuckle tap on Voss's harness
          eng.wait(0.35)

          # [PF] PROVISIONAL: the King's theme is on hold (Reuben). The tag is Gemini's; 016_Movies.rb maps it
          # to a stand-in until the pick is made.
          eng.play_bgm("ruin_cosmic_air", volume: 86, tag: "ruin_cosmic_air")
          eng.zoom_map(1.24, duration: 0.80, focus: :aurelius, ease: :in_out)
          eng.wait(0.40)

          eng.say(:AURELIUS, :smug, "...That's it?", hold: 0.92)
          eng.say(:AURELIUS, :deadpan, "Three hundred years, and this tin-plated parlour trick is what House Aurel calls ambition?", hold: 0.92)

          # Emote #1 of 3: Voss jolts in shocked disbelief
          eng.actor(:voss).show_emote(:exclaim, duration: 0.50)
          eng.play_se("Exclaim", volume: 80)
          eng.wait(0.25)
          eng.say(:VOSS, :shocked, "My lord? It draws on all eighteen Imprints. I spent thirty years—", hold: 0.72)

          eng.say(:AURELIUS, :angry, "You built a shopkeeper's tower on my drowned roof, wired a clerk's harness out of scraps from my sewers, and crawled to my glass on your knees!", hold: 0.92)
          eng.say(:AURELIUS, :smug, "And they named you for me. \"Aurelian\": heir of Aurelius. A copper coin stamped with the sovereign's face.", hold: 0.92)
          eng.say(:AURELIUS, :neutral, "Know your place, mongrel.", hold: 0.92)

          # Physical gauntlet flick tosses Voss cleanly onto open east marble floor (ZERO portals/chains!)
          eng.zoom_map(1.04, duration: 0.25, ease: :out)
          eng.actor(:aurelius).set_pose("act_ruin_aurelius_pose", 1) # Contemptuous right gauntlet flick
          eng.play_se("Anim/hit", volume: 96, pitch: 88)
          eng.shake(power: 5, duration: 0.30)
          eng.flash(color: [255, 224, 124], power: 130, duration: 0.16)
          eng.actor(:voss).move_to(17.2, 13.4, duration: 0.48, walk: false, arc_h: 20.0, ease: :out)
          eng.wait_for_move(:voss)
          eng.play_se("Anim/Earth3", volume: 78, pitch: 112)
          eng.shake(power: 3, duration: 0.20)
          eng.actor(:voss).tremble(duration: 0.50, amp: 1.5, freq: 44.0)
          eng.wait(0.30)

          eng.say(:VOSS, :panic, "No, Your Majesty, I'm your heir—!", hold: 0.70)
          eng.say(:AURELIUS, :deadpan, "A king has no heirs while he is standing in the room.", hold: 0.85)

          #---------------------------------------------------------------------
          # ACT III (17.2–25.8s) — Sovereign Audience Atop the 5x5 Golden Sunburst!
          #---------------------------------------------------------------------
          eng.actor(:aurelius).restore_charset("AURELIUS", dir: :down)
          eng.actor(:aurelius).move_to(13.5, 13.0, duration: 0.95, walk: true, dir: :down)
          eng.pan_camera_to(13.5, 13.2, duration: 0.95, ease: :in_out)
          eng.wait_for_move(:aurelius)

          # Open gauntleted hand extended directly over the 5x5 golden sunburst medallion!
          eng.actor(:aurelius).set_pose("act_ruin_aurelius_pose", 2)
          eng.zoom_map(1.26, duration: 0.85, focus: [13.5, 13.7], ease: :in_out)
          eng.wait(0.35)

          eng.say(:AURELIUS, :smug, "Now, then. The clerk is out of the way, and the sky is already listening.", hold: 0.92)
          eng.say(:AURELIUS, :neutral, "Every Plate, every crown, every worthy specimen in this land was mine before your grandparents learned to breathe. I am merely collecting interest.", hold: 0.92)
          eng.say(:AURELIUS, :smug, "You walked through twenty-three graves to open my door. A finer errand than any servant I left in the salt.", hold: 0.92)
          eng.wait(0.20)
          eng.say(:AURELIUS, :smug, "Kneel, mongrel. Set that little hoop at my feet, and I will be generous. I am always generous to things that know their station.", hold: 0.92)

          # Grounded Protagonist refusal: calm steady silence, ONE deliberate step onto sunburst rim!
          eng.wait(0.40)
          eng.actor(:pc).move_to(13.5, 15.3, duration: 0.60, walk: true, dir: :up)
          eng.wait_for_move(:pc)
          eng.play_se("Anim/metal", volume: 80, pitch: 134)

          # Emote #2 of 3: Aurelius pauses a heartbeat in genuine surprise before laughing!
          eng.actor(:aurelius).show_emote(:dots, duration: 0.60)
          eng.wait(0.55)

          #---------------------------------------------------------------------
          # ACT IV (25.8–36.2s) — Earned Amusement, Single Gilded Poke Ball & Challenge!
          #   Proposal §3.6: ZERO Gate of Babylon portals/swords — ONE gilded Poke Ball!
          #---------------------------------------------------------------------
          eng.say(:AURELIUS, :happy, "Ha! Look at those eyes. Not a shred of fear, not a whisper of devotion!", hold: 0.85)

          # Aurelius raises ONE single gilded Poke Ball atop the 5x5 sunburst as the hall inverts royal gold!
          eng.actor(:aurelius).set_pose("act_ruin_aurelius_pose", 3)
          eng.play_se("Anim/Saint7", volume: 94, pitch: 108)
          eng.flash(color: [255, 224, 120], power: 185, duration: 0.38)
          eng.shake(power: 4, duration: 0.34)
          eng.set_tone(-22, -34, -58, 22, duration: 0.65)

          # Extra pure-pixel gold-leaf flakes drifting gently around the golden sunburst (ZERO portals/blades!)
          [[11.8, 12.6, 0], [15.2, 12.6, 1], [12.4, 14.3, 2], [14.6, 14.3, 3]].each_with_index do |(gx, gy, ph), gi|
            eng.spawn_vfx(:"gold_invert_#{gi}", sheet: "pf_vfx_ruin_gold_aura", tx: gx, ty: gy,
                          grid: [4, 2], frames: [4 + (ph % 4), 4 + ((ph + 1) % 4), 4 + ((ph + 2) % 4), 4 + ((ph + 3) % 4)],
                          ticks: [8, 8, 8, 8], loops: :forever,
                          blend: :add, opacity: 195, scale: 1.0, z_layer: :above)
          end

          # Emote #3 of 3: Grounded PC holds rock-steady facing the First Sovereign!
          eng.actor(:pc).show_emote(:double_exclaim, duration: 0.60)
          eng.zoom_map(1.34, duration: 0.80, focus: :aurelius, ease: :in_out)
          eng.wait(0.60)

          eng.say(:AURELIUS, :smug, "Look up, mongrel. Let us see what three hundred years of mortal mediocrity has produced.", hold: 0.82)
          eng.say(:AURELIUS, :neutral, "You mean to unmake the sky? To erase the eighteen Plates I spent a kingdom's blood to claim?", hold: 0.82)
          eng.say(:AURELIUS, :happy, "Hahaha! Audacious! Unforgivable! Utterly magnificent!", hold: 0.82)
          eng.say(:AURELIUS, :angry, "Stand your ground, insolent mongrel! Face the First Sovereign of Aurelia and prove you have the spine to look heaven in the eye!", hold: 1.15)

          eng.wait(0.65)
          eng.zoom_map(1.0, duration: 0.45, ease: :out)
          eng.letterbox(false, duration: 0.45)
          eng.wait(0.45)
        ensure
          cues = eng.cues.dup
          fc   = eng.frames_captured
          eng.dispose
        end
        return { :cues => cues, :frames => fc }
      end
    end
  end
end

#===============================================================================
# Gemini's shorthand: plays a scene by id, with no checks (returns the scene's { :cues, :frames }, or nil
# for an unknown id). Map events should call pfm_cutscene(:ID) instead (016_Movies.rb): it knows which
# scenes' maps are built, restores the game afterwards and never raises.
#===============================================================================
def pbRejuvCutscene(id, **opts)
  aa = Prismfall::AdvancedAnimations
  case id.to_s.upcase.to_sym
  when :CH2_PAGEANT, :CH2_PAGEANT_DC, :CH2_DC            then aa.play_ch2_lantern_pageant_dc(**opts)
  when :CH5_DC, :CH5_SHATTER_DC, :SH1_DC, :CH5_SHATTER   then aa.play_ch5_spire_shatter_dc(**opts)
  when :CH8_CALDERA, :CH8_FIVE_BELLS, :CH8_DC            then aa.play_ch8_caldera(**opts)
  when :CH9_UNMASK, :IR1                                 then aa.play_ch9_trevenant_unmasking(**opts)
  when :CH10_BRIDE_GROVE, :CH10_JUNO, :CH10_DC           then aa.play_ch10_bride_grove(**opts)
  when :CH11_RETHINK, :CH11_KYOGRE_RETHINK, :CH11_THAW_DC, :CH11_DC, :CH11_KYOGRE, :CH11_THAW, :KYOGRE
    aa.play_ch11_kyogre_rethink(**opts)
  when :CH13_FAULT, :CH13_GLASS_COURT, :CH13_DC          then aa.pf_play_ch13_glass_court_fault(**opts)
  when :CH15_GLASSFALL, :CE1, :GLASSFALL                 then aa.pf_play_ch15_glassfall_rethink(**opts)
  when :CH16_WENLOW, :CH16_PURGE, :CH16_DC               then aa.play_ch16_wenlow(**opts)
  when :CH17_SUN_COURT, :CH17_BREACH, :CH17_DC           then aa.pf_play_ch17_sun_court_breach(**opts)
  when :CH19_WAR, :WAR_CLIMAX, :WAR1                     then aa.pf_play_ch19_war1_rethink(**opts)
  when :CH21_ARCEUS, :CH21_FINALE, :THE_LIGHT            then aa.pf_play_ch21_arceus_rethink(**opts)
  when :RUIN_AURELIUS_DC, :RUIN_R7_AURELIUS, :RUIN_AURELIUS
    aa.play_ruin_aurelius_dc(**opts)
  else
    PBDebug.log("[AdvancedAnimations] Unknown scene #{id.inspect}") if defined?(PBDebug)
    nil
  end
end
