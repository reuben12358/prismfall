#===============================================================================
# Prismfall Cutscenes - 018 Expressive conversations
# (Gemini spec 2026-11-24_expressive-conversations-system, v2 "natural restraint";
#  reviewed and reworked on install, see gemini_recommends/REVIEW.md)
#-------------------------------------------------------------------------------
# Adds three things to ordinary [portrait: NAME, expr] / \pf[...] conversations.
# Nothing here moves a portrait: faces fade, cross-fade and dim, and that is all.
#
#   A. Two-speaker stage. In face mode the speaker's face stays where 014 puts it
#      (left of the box); when someone else answers, their face fades in on the
#      right and the one who just spoke stays, dimmed. Each speaker keeps a side
#      for the whole conversation. A third speaker takes the side of whoever
#      spoke longest ago. The listener is only kept through an unbroken exchange:
#      after narration, a walk, a battle or any pause the stage starts again with
#      just the speaker. No sprite outlives its message box.
#
#   B. Emote balloons over the map sprite (Graphics/Animations/pf_emote_balloons,
#      10 rows x 4 frames of 32x32). Only where a line asks:
#        \pfe[dots]  \pfe[exclaim,KESTREL]  \pfe[question,12]   (kind, target)
#        [emote: dots]  [emote: exclaim, Kestrel]               (story-bible form)
#        pf_emote(:KESTREL, :dots)                              (script)
#      At most MAX_EMOTES a conversation; more are dropped (and logged).
#      Kinds: exclaim double_exclaim question dots anger sweat heart idea music jolt
#
#   C. Overworld acting, opt-in and small:
#        \pfp[crossed] / [pose: crossed]     a stance from Graphics/Characters/pose_NAME
#        \pfa[nod]     / [act: nod]          nod step_back lean_in turn_away headshake return face
#        pf_nod pf_step_back pf_lean_in pf_turn_away pf_turn_toward pf_face_each_other
#        pf_headshake pf_step_return pf_pose pf_pose_reset pf_stage_clear
#      Pose sheets come in two layouts: a 128x48 strip of four poses (the first
#      six cast), or 128x192 with a pose in each ROW that plays its four frames
#      once and holds the last (everyone else: crossed / point / brace / shrug).
#      Pose art faces the camera, so the automatic stances (auto_poses) are only
#      used for a speaker who is standing still and facing down.
#
# Switches (Prismfall::Expressive.dual_stage = false, ...):
#   enabled      true         false: everything below is off, 014 behaves as before
#   dual_stage   true         false: 014's single face window
#   auto_poses   :restrained  false: stances only where a line or script asks
#   auto_face    false        true: speaker and previous speaker turn to each other
#                             (off: most lines are said to the silent player, and
#                             map events already stage who faces whom)
#   auto_emote   false        true: a balloon on shocked / panic (rarely wanted)
#===============================================================================
module Prismfall
  module Expressive
    C  = Prismfall::Cutscene
    P  = Prismfall::Portrait
    PX = C::PX

    FADE_IN_TIME   = 0.10        # a face arriving: alpha only
    CROSSFADE_TIME = 0.10        # same speaker, new expression: old face out, new face in
    DIM_TIME       = 0.12        # speaker <-> listener
    LINGER         = P::FACE_LINGER   # two face lines closer than this are one exchange
    LISTENER_TONE  = [-42, -42, -42, 35]

    EMOTE_SHEET    = "Graphics/Animations/pf_emote_balloons"
    EMOTE_CELL     = 32
    EMOTE_TIME     = 0.92
    EMOTE_Z        = P::VIEWPORT_Z - 5
    MAX_EMOTES     = 3           # balloons per conversation (creator directive)
    POSE_FRAME     = 0.09        # seconds a frame of a 4-frame pose row shows
    POSE_MIN_HOLD  = 1.25        # automatic stances do not change faster than this

    EMOTE_ROWS = {
      :exclaim => 0, :double_exclaim => 1, :question => 2, :dots => 3, :anger => 4,
      :sweat => 5, :heart => 6, :idea => 7, :music => 8, :jolt => 9
    }
    EMOTE_ALIASES = {
      :alert => :exclaim, :shock => :double_exclaim, :horror => :double_exclaim,
      :confused => :question, :curious => :question,
      :ellipsis => :dots, :gloom => :dots, :silent => :dots,
      :angry => :anger, :furious => :anger, :nervous => :sweat, :tears => :sweat,
      :blush => :heart, :warm => :heart, :sparkle => :idea, :realize => :idea,
      :note => :music, :cheerful => :music, :dread => :jolt, :wince => :jolt, :tension => :jolt
    }
    AUTO_EMOTES = { :shocked => :exclaim, :panic => :double_exclaim }   # only with auto_emote
    EMOTE_SE    = { :exclaim => "Exclaim", :double_exclaim => "Exclaim" }   # silent when the file is absent

    # Pose names. The strip sheets have their own; a 4-row sheet uses ROW_POSES.
    POSE_NAMES = {
      :JUNO     => { :clasped => 0, :flinch => 1, :worried => 2, :resolute => 3 },
      :KESTREL  => { :crossed => 0, :scoff => 1, :lean_angry => 2, :guarded => 3 },
      :LARCH    => { :ponder => 0, :glasses => 1, :explain => 2, :sheepish => 3 },
      :PLAYER_A => { :determined => 0, :recoil => 1, :thoughtful => 2, :reach => 3 },
      :PLAYER_B => { :determined => 0, :recoil => 1, :thoughtful => 2, :reach => 3 },
      :VOSS     => { :behind_back => 0, :open_palm => 1, :collar => 2, :shock => 3 }
    }
    ROW_POSES = { :crossed => 0, :akimbo => 0, :point => 1, :gesture => 1, :brace => 2, :shrug => 3, :open => 3 }

    # Automatic stances (auto_poses == :restrained): expression -> pose, for the
    # six strip sheets only. :neutral always goes back to the walking sprite.
    RESTRAINED_POSES = {
      :JUNO     => { :happy => 0, :blush => 0, :shocked => 1, :panic => 1, :sad => 2, :crying => 2, :angry => 3 },
      :KESTREL  => { :deadpan => 0, :smug => 0, :angry => 2, :sad => 3, :crying => 3 },
      :LARCH    => { :deadpan => 0, :smug => 1, :happy => 2, :sad => 3, :blush => 3 },
      :PLAYER_A => { :angry => 0, :shocked => 1, :panic => 1, :sad => 3 },
      :PLAYER_B => { :angry => 0, :shocked => 1, :panic => 1, :sad => 3 },
      :VOSS     => { :deadpan => 0, :smug => 2, :angry => 2, :shocked => 3, :panic => 3 }
    }
    ACTS = %i[nod step_back lean_in turn_away headshake return face shudder hop]

    @enabled    = true
    @dual_stage = true
    @auto_poses = :restrained
    @auto_face  = false
    @auto_emote = false
    @scene = { :emotes => 0, :speakers => [], :expr => {}, :pose_at => {} }
    @dirty = false

    class << self
      attr_accessor :enabled, :dual_stage, :auto_poses, :auto_face, :auto_emote

      def stage?; return @enabled && @dual_stage; end
      def stage;  return @stage ||= Stage.new; end
      def emotes; return @emotes ||= EmoteManager.new; end

      # On the map, out of battle: the only place overworld acting happens.
      def on_map?
        return false if !defined?(Scene_Map) || !defined?($scene) || !$scene.is_a?(Scene_Map)
        return false if defined?($game_temp) && $game_temp && $game_temp.respond_to?(:in_battle) && $game_temp.in_battle
        return true
      end

      def active?
        return @dirty || (@emotes && @emotes.active?) || (@stage && @stage.remembers?) ? true : false
      end

      def emotes_shown; return @scene[:emotes]; end

      def resolve_emote(kind)
        key = kind.to_s.downcase.strip.to_sym
        key = EMOTE_ALIASES[key] || key
        return (EMOTE_ROWS.has_key?(key)) ? key : nil
      end

      # Pulls the acting tags out of a message. -> [clean text, { emotes:, pose:, act: }]
      def extract_inline_tags(message)
        text = message.to_s.dup
        dirs = { :emotes => [], :pose => nil, :act => nil }
        take = lambda do |fields|
          parts = fields.split(",").map(&:strip)
          (parts[0].to_s.empty?) ? nil : parts
        end
        text.gsub!(/\\pfe\[([^\]]*)\]|\[emote:\s*([^\]]*)\]\s?/i) do
          parts = take.call($1 || $2)
          dirs[:emotes].push({ :kind => parts[0], :target => parts[1] }) if parts
          ""
        end
        text.gsub!(/\\pfp\[([^\]]*)\]|\[pose:\s*([^\]]*)\]\s?/i) do
          parts = take.call($1 || $2)
          dirs[:pose] = { :pose => parts[0], :target => parts[1] } if parts
          ""
        end
        text.gsub!(/\\pfa\[([^\]]*)\]|\[act:\s*([^\]]*)\]\s?/i) do
          parts = take.call($1 || $2)
          dirs[:act] = { :kind => parts[0], :target => parts[1] } if parts
          ""
        end
        return text, dirs
      end

      def tags?(dirs); return !dirs[:emotes].empty? || !dirs[:pose].nil? || !dirs[:act].nil?; end

      #-------------------------------------------------------------------------
      # Who a tag or a helper means
      #-------------------------------------------------------------------------
      # A map event whose name is the id, or starts with it ("Kestrel K1",
      # "Juno (lab yard)" - but not "Juno's seed packets"); a shown one first,
      # then the nearest to the player.
      def named_event(name)
        return nil if !defined?($game_map) || !$game_map || !$game_map.respond_to?(:events)
        want = name.to_s.downcase.tr("_", " ").strip
        return nil if want.empty?
        re = /\A#{Regexp.escape(want)}(?:\z|[\s(\[,:;.-])/
        hits = $game_map.events.values.select { |e| e.respond_to?(:name) && e.name.to_s.downcase =~ re }
        return nil if hits.empty?
        shown = hits.reject { |e| hidden?(e) }
        hits = shown if !shown.empty?
        exact = hits.select { |e| e.name.to_s.downcase == want }
        hits = exact if !exact.empty?
        return hits[0] if hits.length == 1 || !defined?($game_player) || !$game_player.respond_to?(:x)
        return hits.min_by { |e| ((e.x - $game_player.x).abs + (e.y - $game_player.y).abs rescue 0) }
      rescue StandardError
        return nil
      end

      def hidden?(char)
        return true if char.respond_to?(:character_name) && char.character_name.to_s.empty? &&
                       (!char.respond_to?(:tile_id) || char.tile_id.to_i == 0)
        return true if char.respond_to?(:transparent) && char.transparent
        return char.instance_variable_get(:@erased) ? true : false
      end

      def self_event
        interp = (defined?(pbMapInterpreter)) ? pbMapInterpreter : nil
        ev = (interp && interp.respond_to?(:get_self)) ? interp.get_self : nil
        return (ev && !hidden?(ev)) ? ev : nil
      rescue StandardError
        return nil
      end

      def follower(name)
        return nil if !defined?($game_temp) || !$game_temp || !$game_temp.respond_to?(:followers)
        f = $game_temp.followers.get_follower_by_name(name.to_s.split("_").map(&:capitalize).join(" "))
        return (f && !hidden?(f)) ? f : nil
      rescue StandardError
        return nil
      end

      # target: a character, an event id, 0 / :PLAYER, or a name.
      def resolve_character(target)
        return nil if target.nil?
        return target if defined?(Game_Character) && target.is_a?(Game_Character)
        return target if target.respond_to?(:screen_x) && !target.is_a?(String) && !target.is_a?(Symbol) && !target.is_a?(Integer)
        text = target.to_s.strip
        return $game_player if target == 0 || text.upcase == "PLAYER" || text =~ /\APLAYER_[AB]\z/i
        if target.is_a?(Integer) || text =~ /\A\d+\z/
          return nil if !defined?($game_map) || !$game_map || !$game_map.respond_to?(:events)
          return $game_map.events[text.to_i]
        end
        ev_name = P.person(text)[:event]
        return resolve_character(ev_name) if ev_name && ev_name.to_s.downcase != text.downcase
        return named_event(text) || follower(text)
      rescue StandardError
        return nil
      end

      # The map character saying a line. A cast member must be on the map under
      # their own name (or be the follower); for anyone else it is the event
      # running the text, when that event can be seen.
      def speaker_for(spec, plain = false)
        return self_event if !spec
        return $game_player if spec[:id] == :PLAYER
        return resolve_character(spec[:event]) if spec[:event]
        found = resolve_character(spec[:id])
        return found if found
        return (plain) ? self_event : nil
      rescue StandardError
        return nil
      end

      def pose_sheet_for(id)
        aid = P.art_id(id)
        return nil if !C::Gfx.resolve("Graphics/Characters/pose_#{aid}")
        return "pose_#{aid}", aid
      end

      def pose_index(aid, pose)
        text = pose.to_s.downcase.strip
        return text.to_i if pose.is_a?(Integer) || text =~ /\A\d+\z/
        return (POSE_NAMES[aid] || ROW_POSES)[text.to_sym] || ROW_POSES[text.to_sym]
      end

      #-------------------------------------------------------------------------
      # A line of dialogue
      #-------------------------------------------------------------------------
      # spec: the portrait spec of the line (nil for an untagged line);
      # plain: no face or bubble is shown for it.
      def trigger_acting(spec, dirs, plain = false)
        return if !@enabled || !on_map?
        return if !spec && !tags?(dirs)
        sc = @scene
        spk = speaker_for(spec, plain)
        id = (spec) ? spec[:id] : nil
        expr = (spec && spec[:expression]) ? spec[:expression].to_sym : :neutral
        now = C::Util.now
        changed = id && sc[:expr][id] != expr
        sc[:expr][id] = expr if id
        @dirty = true if spk || tags?(dirs)

        if @auto_face && spk && !plain
          prev = sc[:speakers].reverse.find { |c| c && c != spk }
          if prev
            turn_toward(spk, prev)
            turn_toward(prev, spk)
          end
        end
        if spk
          sc[:speakers].delete(spk)
          sc[:speakers].push(spk)
          sc[:speakers].shift if sc[:speakers].length > 4
        end

        dirs[:emotes].each do |em|
          t = (em[:target]) ? resolve_character(em[:target]) : spk
          spawn_emote(t, em[:kind])
        end
        if @auto_emote && dirs[:emotes].empty? && spk && changed && AUTO_EMOTES[expr]
          spawn_emote(spk, AUTO_EMOTES[expr])
        end

        if dirs[:pose]
          t = (dirs[:pose][:target]) ? resolve_character(dirs[:pose][:target]) : spk
          apply_pose(t, dirs[:pose][:target] || id, dirs[:pose][:pose])
          sc[:pose_at][id] = now if id
        elsif @auto_poses == :restrained && spk && id && changed && !spec[:carried] && !plain
          auto_pose(spk, id, expr, now)
        end

        if dirs[:act]
          t = (dirs[:act][:target]) ? resolve_character(dirs[:act][:target]) : spk
          run_act(t, dirs[:act][:kind], sc[:speakers].reverse.find { |c| c && c != t })
        end
      rescue StandardError => e
        C::Util.log("expressive acting failed: #{e.class}: #{e.message}")
        raise if C.raise_errors
      end

      def spawn_emote(char, kind, force = false)
        return nil if !char || !on_map?
        key = resolve_emote(kind)
        if !key
          C::Util.log("expressive: unknown emote #{kind.inspect}")
          return nil
        end
        if !force && @scene[:emotes] >= MAX_EMOTES
          C::Util.log("expressive: emote #{key} dropped (#{MAX_EMOTES} a conversation)")
          return nil
        end
        b = emotes.spawn(char, key)
        return nil if !b
        @scene[:emotes] += 1
        @dirty = true
        return b
      end

      def auto_pose(char, id, expr, now)
        return if !char.respond_to?(:pf_set_pose)
        if expr == :neutral
          char.pf_clear_pose if char.pf_pose_auto
          return
        end
        return if now - (@scene[:pose_at][id] || -999.0) < POSE_MIN_HOLD
        return if char.respond_to?(:direction) && char.direction != 2          # the art faces the camera
        return if (char.respond_to?(:moving?) && char.moving?) || (char.respond_to?(:move_route_forcing) && char.move_route_forcing)
        sheet, aid = pose_sheet_for(id)
        idx = sheet && RESTRAINED_POSES[aid] && RESTRAINED_POSES[aid][expr]
        return if !idx
        char.pf_set_pose(sheet, idx, true)
        @scene[:pose_at][id] = now
      end

      # id: whose sheet (a name, or nil to go by the character's own charset).
      def apply_pose(char, id, pose)
        return false if !char || !char.respond_to?(:pf_set_pose)
        text = pose.to_s.downcase.strip
        if ["reset", "none", "idle", "off"].include?(text)
          char.pf_clear_pose
          return true
        end
        id = :PLAYER if defined?($game_player) && char == $game_player
        id ||= char.character_name.to_s.sub(/\Apose_/i, "") if char.respond_to?(:character_name)
        sheet, aid = pose_sheet_for(id)
        idx = (sheet) ? pose_index(aid, pose) : nil
        if !idx
          C::Util.log("expressive: no pose #{pose.inspect} for #{id.inspect}")
          return false
        end
        char.pf_set_pose(sheet, C::Util.clamp(idx, 0, 3))
        @dirty = true
        return true
      end

      def run_act(char, kind, other = nil)
        return false if !char || !char.respond_to?(:pf_start_act)
        key = kind.to_s.downcase.strip.to_sym
        return false if !ACTS.include?(key)
        @dirty = true
        case key
        when :turn_away then turn_away(char, other)
        when :face      then turn_toward(char, other || $game_player)
        when :step_back, :lean_in then char.pf_start_act(key, 4)
        else char.pf_start_act(key)
        end
        return true
      end

      def facing(from, to)
        dx = to.x - from.x
        dy = to.y - from.y
        return nil if dx == 0 && dy == 0
        return (dx > 0) ? 6 : 4 if dx.abs >= dy.abs
        return (dy > 0) ? 2 : 8
      end

      # Turns only someone standing free: not walking, not on a forced route, not
      # already walked into place by this event (pf_staged), within 6 tiles.
      def turn_toward(char, target)
        return false if !char || !target || char == target || !char.respond_to?(:pf_set_facing)
        return false if !char.respond_to?(:x) || !target.respond_to?(:x)
        return false if char.respond_to?(:pf_staged) && char.pf_staged
        return false if ((target.x - char.x).abs + (target.y - char.y).abs) > 6
        dir = facing(char, target)
        return (dir) ? char.pf_set_facing(dir) : false
      end

      def turn_away(char, from = nil)
        return false if !char || !char.respond_to?(:pf_set_facing)
        dir = (from && from.respond_to?(:x) && char.respond_to?(:x)) ? facing(from, char) : nil
        dir ||= { 2 => 4, 4 => 8, 6 => 8, 8 => 4 }[char.direction]
        return char.pf_set_facing(dir || 4)
      end

      #-------------------------------------------------------------------------
      # Clean-up
      #-------------------------------------------------------------------------
      def reset_all_actors
        chars = []
        chars.push($game_player) if defined?($game_player) && $game_player
        chars.concat($game_map.events.values) if defined?($game_map) && $game_map && $game_map.respond_to?(:events)
        if defined?($game_temp) && $game_temp && $game_temp.respond_to?(:followers) && $game_temp.followers.respond_to?(:each_follower)
          $game_temp.followers.each_follower { |f, _| chars.push(f) }
        end
        chars.each { |c| c.pf_reset_acting if c.respond_to?(:pf_reset_acting) }
      rescue StandardError
        nil
      end

      # The conversation is over (the event ended, a new one began, the map changed).
      def clear_all
        @stage.forget if @stage
        @emotes.clear if @emotes
        @scene = { :emotes => 0, :speakers => [], :expr => {}, :pose_at => {} }
        reset_all_actors if @dirty
        @dirty = false
      end

      # Leaving the map screen (a battle, a menu scene): balloons cannot be updated there.
      def leave_map
        @emotes.clear if @emotes
      end
    end

    #===========================================================================
    # A. The two-speaker stage
    #===========================================================================
    # One framed face: the frame, the face, and the old face during a cross-fade.
    class Panel
      attr_reader :id, :file, :side

      # entry: :pop (fade in), :swap (cross-fade from prev_file), :none
      # dim_from / dim_to: 0.0 bright .. 1.0 listener
      def initialize(viewport, side, id, file, frame_bmp, entry, prev_file, dim_from, dim_to, start)
        @side = side
        @id = id
        @file = file
        @entry = entry
        @dim_from = dim_from
        @dim_to = dim_to
        @start = start
        @face_bmp = Panel.face_bitmap(file)
        @frame = Sprite.new(viewport)
        @frame.bitmap = frame_bmp
        @frame.z = (dim_to > 0) ? 10 : 20
        @face = Sprite.new(viewport)
        @face.bitmap = @face_bmp
        @face.z = @frame.z + 2
        if entry == :swap && prev_file
          @prev_bmp = Panel.face_bitmap(prev_file)
          @prev = Sprite.new(viewport)
          @prev.bitmap = @prev_bmp
          @prev.z = @frame.z + 1
        end
        @tone = Tone.new(0, 0, 0, 0)
      end

      # The art as a FACE_SIZE square (as FaceBox#load_face).
      def self.face_bitmap(file)
        size = P::FACE_SIZE
        out = Bitmap.new(size, size)
        src = (file) ? C::Gfx.load_bitmap(file) : nil
        return out if !src
        s = [src.width, src.height].min
        sx = (src.width - s) / 2
        if s == size
          out.blt(0, 0, src, Rect.new(sx, 0, s, s))
        else
          out.stretch_blt(Rect.new(0, 0, size, size), src, Rect.new(sx, 0, s, s))
        end
        src.dispose
        return out
      end

      def update(x, y, now)
        t = now - @start
        op = 255
        op = (255 * C::Ease.apply(:out, C::Util.clamp(t / FADE_IN_TIME, 0.0, 1.0))).round if @entry == :pop && t < FADE_IN_TIME
        k = C::Util.clamp(t / DIM_TIME, 0.0, 1.0)
        dim = @dim_from + ((@dim_to - @dim_from) * k)
        @tone.set(*LISTENER_TONE.map { |v| (v * dim).round })
        fop = op
        if @prev
          if t < CROSSFADE_TIME
            xk = C::Util.clamp(t / CROSSFADE_TIME, 0.0, 1.0)
            @prev.opacity = (255 * (1.0 - xk)).round
            fop = (255 * xk).round
          else
            @prev.visible = false
          end
        end
        @frame.x = x
        @frame.y = y
        @frame.opacity = op
        @frame.tone = @tone
        [@face, @prev].compact.each do |s|
          s.x = x + P::FACE_EDGE
          s.y = y + P::FACE_EDGE
          s.tone = @tone
        end
        @face.opacity = fop
      end

      def sprites; return [@frame, @face, @prev].compact; end
      def dim; return @dim_to; end

      def dispose
        sprites.each { |s| s.dispose if !s.disposed? }
        [@face_bmp, @prev_bmp].compact.each { |b| b.dispose if !b.disposed? }
      end
    end

    # What Portrait.open returns for a face line while the stage is on. It is a
    # FaceBox to the rest of the code (spec / file / entry / rect / update / dispose).
    class StageView < P::FaceBox
      attr_reader :side, :panels

      # listener: nil or { :id, :file, :side, :dim_from }
      def initialize(stage, spec, msgwindow, side, entry, prev_file, dim_from, listener)
        @stage = stage
        @spec = spec
        @msg = msgwindow
        @id = spec[:id]
        @side = side
        @entry = entry
        @file = P.face_file(@id, spec[:expression])
        @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @viewport.z = P::VIEWPORT_Z
        @frame_bmp = P::Frame.build(msgwindow)
        @start = C::Util.now
        @panels = [Panel.new(@viewport, side, @id, @file, @frame_bmp, entry, prev_file, dim_from, 0.0, @start)]
        if listener
          @panels.push(Panel.new(@viewport, listener[:side], listener[:id], listener[:file], @frame_bmp,
                                 :none, nil, listener[:dim_from], 1.0, @start))
        end
        @first = true
        @rect = [0, 0, P::FACE_FRAME, P::FACE_FRAME]
        update
      end

      def listener; return @panels[1]; end

      # Left: where 014 puts its face. Right: the same, on the box's other end.
      def anchor(side, x, y)
        return x, y if side == :left
        mw = (@msg && @msg.respond_to?(:width)) ? @msg.width.to_i : 0
        mw = Graphics.width - x if mw <= 0
        return x + mw - P::FACE_FRAME, y
      end

      def update
        return if @disposed
        x, y, = place
        @first = false
        now = C::Util.now
        @panels.each do |pn|
          px, py = anchor(pn.side, x, y)
          pn.update(px, py, now)
          @rect = [px, py, P::FACE_FRAME, P::FACE_FRAME] if pn.equal?(@panels[0])
        end
      end

      def dispose
        return if @disposed
        @disposed = true
        P.face_closed(@id, @file)
        @stage.closed(self)
        @panels.each(&:dispose)
        @frame_bmp.dispose if !@frame_bmp.disposed?
        @viewport.dispose
      end
    end

    # Remembers who stands where between message boxes; owns no sprites itself.
    class Stage
      def initialize; forget; end

      def forget
        @sides = {}          # id => :left / :right, for the conversation
        @used = {}           # id => time of their last line
        @last = nil          # { :at, :speaker => {id, file, side}, :listener => {..} or nil } of the last face line
      end

      def remembers?; return !@sides.empty?; end
      def side_of(id); return @sides[id]; end

      def take_side(id)
        return @sides[id] if @sides[id]
        taken = @sides.values
        side = ([:left, :right] - taken).first
        if !side                                         # both taken: whoever spoke longest ago gives theirs up
          old = @sides.keys.min_by { |k| @used[k] || 0.0 }
          side = @sides.delete(old)
          @used.delete(old)
        end
        @sides[id] = side
        return side
      end

      def open_line(spec, msgwindow)
        id = spec[:id]
        now = C::Util.now
        file = P.face_file(id, spec[:expression])
        last = (@last && now - @last[:at] <= LINGER) ? @last : nil
        was = (last) ? [last[:speaker], last[:listener]].compact.find { |h| h[:id] == id } : nil
        side = take_side(id)
        @used[id] = now
        entry = :pop
        prev_file = nil
        dim_from = 0.0
        if was && was[:side] == side
          entry = (was[:file] == file) ? :none : :swap
          prev_file = was[:file]
          dim_from = was[:dim]
        end
        listener = nil
        if last
          other = [last[:speaker], last[:listener]].compact.find { |h| h[:id] != id && h[:side] != side && @sides[h[:id]] == h[:side] }
          listener = { :id => other[:id], :file => other[:file], :side => other[:side], :dim_from => other[:dim] } if other
        end
        return StageView.new(self, spec, msgwindow, side, entry, prev_file, dim_from, listener)
      end

      def closed(view)
        pn = view.panels[0]
        ls = view.listener
        @last = { :at => C::Util.now,
                  :speaker => { :id => pn.id, :file => pn.file, :side => pn.side, :dim => 0.0 },
                  :listener => (ls) ? { :id => ls.id, :file => ls.file, :side => ls.side, :dim => 1.0 } : nil }
      end
    end

    #===========================================================================
    # B. Emote balloons
    #===========================================================================
    class EmoteBalloon
      attr_reader :char, :kind

      def initialize(viewport, bitmap, char, kind)
        @char = char
        @kind = kind
        @row = EMOTE_ROWS[kind]
        @start = C::Util.now
        @sprite = Sprite.new(viewport)
        @sprite.bitmap = bitmap
        @sprite.ox = EMOTE_CELL / 2
        @sprite.oy = EMOTE_CELL
        @sprite.z = 500
        @done = false
        update
      end

      def done?; return @done; end
      def frame; return @frame; end
      def sprite; return @sprite; end

      # -> true when finished
      def update
        return true if @done
        lt = C::Util.now - @start
        if lt >= EMOTE_TIME || !@char.respond_to?(:screen_x)
          dispose
          return true
        end
        @frame = (lt < 0.10) ? 0 : ((lt < 0.28) ? 1 : ((lt < 0.56) ? 2 : 3))      # pop in, peak, hold, settle
        @sprite.src_rect.set(@frame * EMOTE_CELL, @row * EMOTE_CELL, EMOTE_CELL, EMOTE_CELL)
        ox = (@char.respond_to?(:pf_visual_ox)) ? @char.pf_visual_ox : 0
        oy = (@char.respond_to?(:pf_visual_oy)) ? @char.pf_visual_oy : 0
        @sprite.x = C::Util.snap(@char.screen_x + ox)
        @sprite.y = C::Util.snap(@char.screen_y - 46 + oy)
        @sprite.opacity = (lt > 0.74) ? (255 * (1.0 - ((lt - 0.74) / (EMOTE_TIME - 0.74)))).round : 255
        return false
      end

      def dispose
        return if @done
        @done = true
        @sprite.dispose if !@sprite.disposed?
      end
    end

    class EmoteManager
      def initialize
        @active = []
      end

      def active?; return !@active.empty?; end
      def count; return @active.length; end

      def spawn(char, kind)
        return nil if !EMOTE_ROWS[kind]
        if !@bitmap || @bitmap.disposed?
          @bitmap = C::Gfx.load_bitmap(EMOTE_SHEET)
          return nil if !@bitmap
        end
        if !@viewport || @viewport.disposed?
          @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
          @viewport.z = EMOTE_Z
        end
        @active.reject! { |b| b.char == char && (b.dispose || true) }      # one balloon a head
        b = EmoteBalloon.new(@viewport, @bitmap, char, kind)
        @active.push(b)
        C::Sound.play(:se, EMOTE_SE[kind], 60, 100) if EMOTE_SE[kind]
        return b
      end

      def update
        return if @active.empty?
        @active.reject!(&:update)
        release if @active.empty?
      end

      def clear
        @active.each(&:dispose)
        @active.clear
        release
      end

      def release
        @bitmap.dispose if @bitmap && !@bitmap.disposed?
        @bitmap = nil
        @viewport.dispose if @viewport && !@viewport.disposed?
        @viewport = nil
      end
    end
  end
end

#===============================================================================
# 014's face line becomes a stage line; a new conversation clears the stage.
#===============================================================================
module Prismfall
  module Portrait
    class << self
      if !method_defined?(:prismfall_expressive_open)
        alias prismfall_expressive_open open
        alias prismfall_expressive_new_conversation new_conversation
      end

      def open(spec, msgwindow = nil, mode = nil)
        mode ||= (spec[:bubble]) ? :bubble : :face
        return prismfall_expressive_open(spec, msgwindow, mode) if mode != :face || !Prismfall::Expressive.stage?
        close
        @current = Prismfall::Expressive.stage.open_line(spec, msgwindow)
        return @current
      rescue StandardError => e
        C::Util.log("portrait stage failed: #{e.class}: #{e.message}")
        raise if C.raise_errors
        @current = nil
        return nil
      end

      def new_conversation
        Prismfall::Expressive.clear_all
        prismfall_expressive_new_conversation
      end
    end
  end
end

#===============================================================================
# C. Overworld acting on map characters
#===============================================================================
if defined?(Game_Character) && !Game_Character.method_defined?(:pf_update_expressive)
  class Game_Character
    attr_reader :pf_pose_sheet, :pf_pose_index, :pf_pose_at, :pf_pose_auto, :pf_staged

    def pf_visual_ox; return @pf_ox.to_i; end
    def pf_visual_oy; return @pf_oy.to_i; end

    # A turn on the spot. Not for a character that is walking or keeps its direction.
    def pf_set_facing(dir)
      return false if ![2, 4, 6, 8].include?(dir) || @direction_fix
      return false if moving? || jumping? || @move_route_forcing
      @direction = dir
      @stop_count = 0 if @stop_count
      return true
    end

    def pf_set_pose(sheet, index = 0, auto = false)
      @pf_pose_sheet = sheet
      @pf_pose_index = [[index.to_i, 0].max, 3].min
      @pf_pose_at = Prismfall::Cutscene::Util.now
      @pf_pose_auto = auto
      @pf_pose_dir = @direction
    end

    def pf_clear_pose
      @pf_pose_sheet = nil
      @pf_pose_index = 0
      @pf_pose_auto = false
    end

    def pf_reset_acting
      pf_clear_pose
      @pf_act = nil
      @pf_ox = @pf_oy = @pf_hold_ox = @pf_hold_oy = 0
      @pf_staged = false
    end

    def pf_acting?; return !@pf_act.nil?; end

    # kind: :nod :step_back :lean_in :return :headshake, and for the rare loud beat :shudder :hop
    def pf_start_act(kind, dist = 4)
      @pf_act = { :kind => kind.to_sym, :start => Prismfall::Cutscene::Util.now, :dist => dist.to_i, :dir => @direction,
                  :ox => @pf_hold_ox.to_i, :oy => @pf_hold_oy.to_i }
      pf_update_expressive
    end

    def pf_update_expressive
      # a stance is for standing: walking off (or, for an automatic one, turning) ends it
      if @pf_pose_sheet && (moving? || jumping? || (@pf_pose_auto && @direction != @pf_pose_dir))
        pf_clear_pose
      end
      @pf_hold_ox ||= 0
      @pf_hold_oy ||= 0
      act = @pf_act
      if !act
        @pf_ox = @pf_hold_ox
        @pf_oy = @pf_hold_oy
        return
      end
      cs = Prismfall::Cutscene
      lt = cs::Util.now - act[:start]
      vx, vy = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }[act[:dir]] || [0, 1]
      ox = @pf_hold_ox
      oy = @pf_hold_oy
      done = false
      case act[:kind]
      when :nod                                  # one small dip
        done = lt >= 0.22
        oy += cs::Util.snap(Math.sin(cs::Util.clamp(lt / 0.22, 0.0, 1.0) * Math::PI) * 2) if !done
      when :step_back, :lean_in                  # a few pixels, eased, and held until :return
        k = cs::Ease.apply(:out, cs::Util.clamp(lt / 0.20, 0.0, 1.0))
        sign = (act[:kind] == :lean_in) ? 1 : -1
        ox = @pf_hold_ox = act[:ox] + cs::Util.snap(sign * vx * act[:dist] * k)
        oy = @pf_hold_oy = act[:oy] + cs::Util.snap(sign * vy * (act[:dist] / 2.0) * k)
        done = lt >= 0.20
      when :return
        k = 1.0 - cs::Ease.apply(:out, cs::Util.clamp(lt / 0.18, 0.0, 1.0))
        ox = @pf_hold_ox = cs::Util.snap(act[:ox] * k)
        oy = @pf_hold_oy = cs::Util.snap(act[:oy] * k)
        done = lt >= 0.18
      when :headshake                            # a look left, a look right, back
        step = (lt / 0.14).to_i
        if !@direction_fix
          @direction = (step == 0) ? ((act[:dir] == 4 || act[:dir] == 6) ? 2 : 4) : ((step == 1) ? ((act[:dir] == 4 || act[:dir] == 6) ? 8 : 6) : act[:dir])
        end
        done = step >= 2
      when :shudder
        done = lt >= 0.28
        amp = (cs.photosensitive?) ? 0 : cs::PX
        ox += (((lt * 24).to_i.even?) ? -amp : amp) if !done
      when :hop
        done = lt >= 0.22
        oy -= cs::Util.snap(Math.sin(cs::Util.clamp(lt / 0.22, 0.0, 1.0) * Math::PI) * 4) if !done
      else
        done = true
      end
      @pf_ox = ox
      @pf_oy = oy
      @pf_act = nil if done
    end

    alias prismfall_expr_char_update update
    def update
      prismfall_expr_char_update
      pf_update_expressive
    end

    # Walked somewhere by its event: leave its facing to the event from here on.
    alias prismfall_expr_force_move_route force_move_route
    def force_move_route(*args)
      @pf_staged = true
      prismfall_expr_force_move_route(*args)
    end
  end
end

# The map sprite: shows the pose cell instead of the walking frame, and the
# few-pixel acting offset.
if defined?(Sprite_Character) && !Sprite_Character.method_defined?(:prismfall_expr_sprite_update)
  class Sprite_Character
    alias prismfall_expr_sprite_update update
    alias prismfall_expr_sprite_dispose dispose

    def update
      prismfall_expr_sprite_update
      ch = @character
      return if !ch || disposed? || !ch.respond_to?(:pf_pose_sheet)
      sheet = ch.pf_pose_sheet
      sheet = nil if sheet && (sheet.empty? || (ch.respond_to?(:bush_depth) && ch.bush_depth.to_i > 0))
      if sheet
        if @pf_pose_name != sheet
          @pf_pose_bmp&.dispose
          @pf_pose_bmp = (AnimatedBitmap.new("Graphics/Characters/#{sheet}") rescue nil)
          @pf_pose_name = sheet
        end
        bmp = (@pf_pose_bmp) ? @pf_pose_bmp.bitmap : nil
        if bmp && !bmp.disposed?
          cw = bmp.width / 4
          rows = (bmp.height >= cw * 4) ? 4 : 1
          chh = bmp.height / rows
          idx = ch.pf_pose_index.to_i
          if rows == 1                                   # a strip of four poses
            sx = idx * cw
            sy = 0
          else                                           # a pose a row: play its four frames once, hold the last
            lt = Prismfall::Cutscene::Util.now - (ch.pf_pose_at || 0.0)
            f = (lt / Prismfall::Expressive::POSE_FRAME).to_i
            sx = [[f, 0].max, 3].min * cw
            sy = idx * chh
          end
          self.bitmap = bmp
          self.src_rect.set(sx, sy, cw, chh)
          self.ox = cw / 2
          self.oy = chh
        end
      elsif @pf_pose_name
        @pf_pose_bmp&.dispose
        @pf_pose_bmp = nil
        @pf_pose_name = nil
        self.ox = @cw / 2 if @cw && @cw > 0
      end
      ox = ch.pf_visual_ox
      oy = ch.pf_visual_oy
      self.x += ox if ox != 0
      self.y += oy if oy != 0
    end

    def dispose
      @pf_pose_bmp&.dispose
      @pf_pose_bmp = nil
      prismfall_expr_sprite_dispose
    end
  end
end

#===============================================================================
# Message hook (outside 014's): strips the acting tags, starts the acting for the
# line, and keeps the balloons moving while the box is up. Faces are still 014's
# job (its open now builds the stage view above).
#===============================================================================
if defined?(pbMessageDisplay) && !defined?(prismfall_expressive_pbMessageDisplay)
  alias prismfall_expressive_pbMessageDisplay pbMessageDisplay

  def pbMessageDisplay(msgwindow, message, letterbyletter = true, commandProc = nil, &block)
    ex = Prismfall::Expressive
    return prismfall_expressive_pbMessageDisplay(msgwindow, message, letterbyletter, commandProc, &block) if !ex.enabled
    text, dirs = ex.extract_inline_tags(message)
    if ex.on_map?
      pf = Prismfall::Portrait
      clean, spec = pf.extract(text)
      spec ||= pf.carry(clean)
      ex.trigger_acting(spec, dirs, pf.mode_for(spec) == :plain)
    end
    return prismfall_expressive_pbMessageDisplay(msgwindow, text, letterbyletter, commandProc, &block) if !ex.emotes.active?
    return prismfall_expressive_pbMessageDisplay(msgwindow, text, letterbyletter, commandProc) do
      ex.emotes.update
      block&.call
    end
  end
end

# A new event on the main interpreter: nobody has been staged by it yet. (014's
# hook on the same method calls Portrait.new_conversation, which clears the rest.)
if defined?(Interpreter) && !Interpreter.method_defined?(:prismfall_expressive_setup)
  class Interpreter
    alias prismfall_expressive_setup setup

    def setup(*args)
      Prismfall::Expressive.clear_all if @main && Prismfall::Expressive.active?
      return prismfall_expressive_setup(*args)
    end
  end
end

if defined?(Scene_Map) && !Scene_Map.method_defined?(:prismfall_expressive_update)
  class Scene_Map
    alias prismfall_expressive_update update
    alias prismfall_expressive_transfer transfer_player
    alias prismfall_expressive_dispose_spritesets disposeSpritesets

    def update
      prismfall_expressive_update
      ex = Prismfall::Expressive
      return if !ex.active?
      ex.emotes.update
      ex.clear_all if !pbMapInterpreterRunning? && !ex.emotes.active?
    end

    def transfer_player(*args)
      Prismfall::Expressive.clear_all if Prismfall::Expressive.active?
      return prismfall_expressive_transfer(*args)
    end

    # the map screen is going away (a battle, another scene): no balloon is left hanging
    def disposeSpritesets(*args)
      Prismfall::Expressive.leave_map
      return prismfall_expressive_dispose_spritesets(*args)
    end
  end
end

#===============================================================================
# Script helpers for events. target: :JUNO / "Juno" (the map event of that name,
# or the follower), an event id, :PLAYER or 0, or a character.
#===============================================================================
# One balloon. wait: true holds the event until it has gone. Counts toward the
# three a conversation unless force: true.
def pf_emote(target, kind, wait: false, force: false)
  ex = Prismfall::Expressive
  b = ex.spawn_emote(ex.resolve_character(target), kind, force)
  return nil if !b
  if wait
    limit = Prismfall::Cutscene::Util.now + Prismfall::Expressive::EMOTE_TIME + 0.5
    until b.done? || Prismfall::Cutscene::Util.now > limit
      Graphics.update
      Input.update
      pbUpdateSceneMap if defined?(pbUpdateSceneMap)
      ex.emotes.update
    end
  end
  return b
end

def pf_act(target, kind, other = nil)
  ex = Prismfall::Expressive
  return ex.run_act(ex.resolve_character(target), kind, (other) ? ex.resolve_character(other) : nil)
end

def pf_nod(target);                 return pf_act(target, :nod);                 end
def pf_headshake(target);           return pf_act(target, :headshake);           end
def pf_step_return(target);         return pf_act(target, :return);              end
def pf_turn_away(target, from = nil); return pf_act(target, :turn_away, from);   end

def pf_step_back(target, dist: 4)
  ev = Prismfall::Expressive.resolve_character(target)
  return false if !ev || !ev.respond_to?(:pf_start_act)
  ev.pf_start_act(:step_back, dist)
  return true
end

def pf_lean_in(target, dist: 4)
  ev = Prismfall::Expressive.resolve_character(target)
  return false if !ev || !ev.respond_to?(:pf_start_act)
  ev.pf_start_act(:lean_in, dist)
  return true
end

def pf_turn_toward(target, other)
  ex = Prismfall::Expressive
  return ex.turn_toward(ex.resolve_character(target), ex.resolve_character(other))
end

def pf_face_each_other(a, b)
  ex = Prismfall::Expressive
  ea = ex.resolve_character(a)
  eb = ex.resolve_character(b)
  r = ex.turn_toward(ea, eb)
  return ex.turn_toward(eb, ea) || r
end

# pf_pose(:LARCH, :glasses)   pf_pose(12, :crossed, :BRANN)   pf_pose(:JUNO, :reset)
def pf_pose(target, pose, sheet_id = nil)
  ex = Prismfall::Expressive
  id = sheet_id || ((target.is_a?(Symbol) || target.is_a?(String)) && target.to_s !~ /\A\d+\z/ ? target : nil)
  return ex.apply_pose(ex.resolve_character(target), id, pose)
end

def pf_pose_reset(target = nil)
  ex = Prismfall::Expressive
  return ex.reset_all_actors if target.nil?
  ev = ex.resolve_character(target)
  ev.pf_reset_acting if ev && ev.respond_to?(:pf_reset_acting)
  return true
end

def pf_stage_clear
  Prismfall::Expressive.clear_all
  return true
end
