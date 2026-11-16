#===============================================================================
# Prismfall Cutscenes - 013 Portrait speech bubbles (SPINE Revision 7)
#-------------------------------------------------------------------------------
# A round portrait with a white ring and a speech tail pointing at the speaker
# on the map, popping in above the normal message box, with code-drawn emotes.
#
#   Script:    pf_say(:MARTIN, :crying, "I LEFT THE OVEN ON!")
#              pf_say(:MARTIN, :smug, "Obviously.", emote: :sparkle, event: 12)
#   Show Text: \pf[MARTIN,crying]MARTIN: I LEFT THE OVEN ON!
#              \pf[MARTIN,shocked,sweat+exclaim]      (third field: emotes)
#              \pf[MARTIN,angry,,12]                  (fourth field: event id)
#              [portrait: MARTIN, crying] MARTIN: ...  (story-bible tag, same thing)
#
# Expressions: neutral happy smug angry crying shocked deadpan panic sad blush
# Emotes:      sweat shock anger sparkle gloom question exclaim tears blush dots
# Portrait art (optional): Graphics/Portraits/NAME_expression.png, then
# Graphics/Portraits/NAME.png, then a round crop of the trainer front sprite's
# head, then a silhouette with the name's initial. See design/CUTSCENES.md.
#===============================================================================
module Prismfall
  module Portrait
    C  = Prismfall::Cutscene
    PX = C::PX
    FOLDER   = "Graphics/Portraits/"
    DIAMETER = 96            # screen pixels of portrait art shown inside the ring
    RADIUS   = DIAMETER / 2 / PX    # art pixels
    CANVAS   = 92            # art-pixel canvas for ring, tail and emotes
    MID      = CANVAS / 2
    TAIL     = 12            # art pixels beyond the ring
    VIEWPORT_Z = 99_999
    POP_TIME = 0.28
    EMOTE_FPS = 8
    EMOTES = [:sweat, :shock, :anger, :sparkle, :gloom, :question, :exclaim, :tears, :blush, :dots]

    # bg: backdrop colour behind the face; emotes: drawn around the ring;
    # face: drawn over the face, only when no art exists for that expression;
    # shake: bubble jitter in art pixels; jolt: extra pop on entry.
    EXPRESSIONS = {
      :neutral => { :bg => [200, 208, 224], :emotes => [] },
      :happy   => { :bg => [255, 224, 136], :emotes => [:sparkle] },
      :smug    => { :bg => [216, 184, 240], :emotes => [:sparkle] },
      :angry   => { :bg => [240, 104, 88],  :emotes => [:anger], :shake => 1 },
      :crying  => { :bg => [136, 184, 240], :emotes => [:sweat], :face => [:tears], :shake => 1 },
      :shocked => { :bg => [255, 248, 176], :emotes => [:shock, :exclaim], :jolt => true },
      :deadpan => { :bg => [168, 168, 176], :emotes => [:dots] },
      :panic   => { :bg => [176, 216, 248], :emotes => [:sweat, :shock], :shake => 2 },
      :sad     => { :bg => [112, 128, 184], :emotes => [], :face => [:gloom] },
      :blush   => { :bg => [255, 192, 208], :emotes => [], :face => [:blush] }
    }

    # Optional per-character data: Prismfall::Portrait.register(:MARTIN,
    #   name: "Martin", trainer: :LEADER_MARTIN, event: "Martin", color: [r, g, b],
    #   crop: [x, y, size])   # head square on the trainer sprite, when the default misses
    @people = {}
    @current = nil

    class << self
      attr_reader :current

      def register(id, **data); @people[id.to_s.upcase.to_sym] = data; end
      def person(id); return @people[id.to_s.upcase.to_sym] || {}; end

      def display_name(id)
        return person(id)[:name] || id.to_s.split("_").map(&:capitalize).join(" ")
      end

      # Pulls a portrait tag out of message text. Returns [clean_text, spec or nil].
      def extract(message)
        text = message.to_s
        spec = nil
        text = text.sub(/\\pf\[([^\]]*)\]/i) do
          spec = parse($1)
          ""
        end
        if !spec
          text = text.sub(/\[portrait:\s*([^\]]*)\]\s*/i) do
            spec = parse($1)
            ""
          end
        end
        text = text.gsub(/\\pf\[[^\]]*\]/i, "").gsub(/\[portrait:[^\]]*\]\s*/i, "") if spec
        return text, spec
      end

      def parse(fields)
        parts = fields.split(",").map(&:strip)
        return nil if parts.empty? || parts[0].to_s.empty?
        expr = (parts[1] && !parts[1].empty?) ? parts[1].downcase.to_sym : :neutral
        emotes = (parts[2].to_s.empty?) ? nil : parts[2].downcase.split(/[+\s|]+/).map(&:to_sym)
        event = (parts[3].to_s.empty?) ? nil : (parts[3] =~ /\A-?\d+\z/ ? parts[3].to_i : parts[3])
        return { :id => parts[0].upcase.to_sym, :expression => expr, :emotes => emotes, :event => event }
      end

      # The map character a bubble points at: an explicit event id / name, the
      # registered or same-named event, :PLAYER, else the event running the text.
      def speaker(spec)
        return nil if !$game_map || !$game_map.respond_to?(:events)
        target = spec[:event] || person(spec[:id])[:event]
        return $game_player if spec[:id] == :PLAYER || target == 0 || target.to_s.upcase == "PLAYER"
        events = $game_map.events
        return events[target] if target.is_a?(Integer) && events[target]
        want = (target || spec[:id]).to_s.downcase
        found = events.values.find { |e| e.respond_to?(:name) && e.name.to_s.downcase == want }
        return found if found
        return nil if target
        interp = (defined?(pbMapInterpreter)) ? pbMapInterpreter : nil
        return interp.get_self if interp && interp.respond_to?(:get_self)
        return nil
      rescue StandardError
        return nil
      end

      def open(spec, msgwindow = nil)
        close
        @current = Bubble.new(spec, msgwindow)
        return @current
      rescue StandardError => e
        C::Util.log("portrait bubble failed: #{e.class}: #{e.message}")
        raise if C.raise_errors
        @current = nil
        return nil
      end

      def close
        @current.dispose if @current
        @current = nil
      end
    end

    #---------------------------------------------------------------------------
    # Portrait art (with fallbacks)
    #---------------------------------------------------------------------------
    module Art
      module_function

      # -> [bitmap (DIAMETER x DIAMETER, round), kind] where kind is
      # :expression, :base, :sprite or :silhouette.
      def load(id, expression)
        src = C::Gfx.load_bitmap("#{FOLDER}#{id}_#{expression}")
        kind = :expression
        if !src
          src = C::Gfx.load_bitmap("#{FOLDER}#{id}")
          kind = :base
        end
        if src
          out = round_copy(src, 0, 0, [src.width, src.height].min)
          src.dispose
          return out, kind
        end
        out = from_trainer(id)
        return out, :sprite if out
        return silhouette(id), :silhouette
      end

      # Copies a square of `size` source pixels into a round DIAMETER bitmap:
      # one scaled copy (integer scale when the source divides DIAMETER), then
      # a row-by-row circular mask.
      def round_copy(src, sx, sy, size)
        d = DIAMETER
        square = Bitmap.new(d, d)
        square.stretch_blt(Rect.new(0, 0, d, d), src, Rect.new(sx, sy, size, size))
        out = Bitmap.new(d, d)
        r = d / 2.0
        d.times do |y|
          half = Math.sqrt([(r * r) - ((y + 0.5 - r)**2), 0].max).floor
          next if half <= 0
          out.blt((r - half).round, y, square, Rect.new((r - half).round, y, half * 2, 1))
        end
        square.dispose
        return out
      end

      # Head region of the trainer front sprite: top-centre square.
      def from_trainer(id)
        return nil if !defined?(GameData::TrainerType)
        type = Portrait.person(id)[:trainer]
        candidates = [type, id, :"LEADER_#{id}", :"RIVAL_#{id}", :"CHAMPION_#{id}"].compact
        file = nil
        candidates.each do |t|
          file = (GameData::TrainerType.front_sprite_filename(t) rescue nil)
          break if file
        end
        src = C::Gfx.load_bitmap(file)
        return nil if !src
        frame = [src.height, src.width].min                 # first frame of a strip
        size = DIAMETER / C::Gfx.native_px(frame)           # keeps integer scaling
        size = [size, frame].min
        sx = (frame - size) / 2
        sy = [(frame * 0.04).round, frame - size].min
        crop = Portrait.person(id)[:crop]              # optional [x, y, size] in sprite pixels
        sx, sy, size = crop if crop
        out = round_copy(src, sx, sy, size)
        src.dispose
        return out
      end

      def silhouette(id)
        d = DIAMETER
        out = Bitmap.new(d, d)
        col = Portrait.person(id)[:color] || C::Gfx.person_color(id)
        dark = C::Util.color(C::Util.mix(col, [0, 0, 0], 0.55))
        C::Pix.disc(out, d / 2, 38, 20, dark)                 # head
        C::Pix.disc(out, d / 2, 104, 40, dark, 36)            # shoulders
        C::TextDraw.font(out, 34)
        C::TextDraw.outline(out, 0, 22, d, 34, id.to_s[0, 1].upcase, Color.new(255, 255, 255), Color.new(24, 24, 32), 1)
        masked = round_copy(out, 0, 0, d)
        out.dispose
        return masked
      end
    end

    #---------------------------------------------------------------------------
    # Emotes, drawn on an art-pixel canvas centred on the bubble
    #---------------------------------------------------------------------------
    module Emote
      DARK = [24, 24, 40]

      module_function

      def col(rgb); return C::Util.color(rgb); end

      def outlined_line(b, x0, y0, x1, y1, rgb)
        C::Pix.line(b, x0, y0 + 1, x1, y1 + 1, col(DARK), 2)
        C::Pix.line(b, x0, y0, x1, y1, col(rgb), 1)
      end

      def polar(ang, r)
        a = ang * Math::PI / 180
        return (MID + (Math.cos(a) * r)).round, (MID + (Math.sin(a) * r)).round
      end

      def draw(b, kind, f)
        case kind
        when :sweat
          3.times do |i|
            x, y = polar(-38 + (i * 26), RADIUS + 9 + (i.odd? ? 3 : 0))
            y += (f + (i * 2)) % 6
            C::Pix.disc(b, x, y + 2, 3, col(DARK))
            C::Pix.rect(b, x - 1, y - 3, 3, 3, col(DARK))
            C::Pix.disc(b, x, y + 2, 2, col([120, 200, 255]))
            C::Pix.rect(b, x, y - 2, 1, 3, col([120, 200, 255]))
            C::Pix.rect(b, x - 1, y + 1, 1, 1, col([255, 255, 255]))
          end
        when :shock
          7.times do |i|
            ang = -160 + (i * 23)
            len = ((i + f).odd?) ? 12 : 7
            x0, y0 = polar(ang, RADIUS + 6)
            x1, y1 = polar(ang + ((i.odd?) ? 5 : -5), RADIUS + 6 + (len / 2))
            x2, y2 = polar(ang, RADIUS + 6 + len)
            outlined_line(b, x0, y0, x1, y1, [255, 240, 96])
            outlined_line(b, x1, y1, x2, y2, [255, 240, 96])
          end
        when :anger
          x, y = polar(-42, RADIUS + 9)
          s = 4 + (f % 2)
          red = col([240, 56, 48])
          C::Pix.rect(b, x - s - 1, y - s - 1, (s * 2) + 4, (s * 2) + 4, col(DARK))
          [[-1, -1], [1, -1], [-1, 1], [1, 1]].each do |dx, dy|
            C::Pix.rect(b, x + ((dx < 0) ? -s : 2), y + (dy * 2), s - 1, 2, red)
            C::Pix.rect(b, x + (dx * 2), y + ((dy < 0) ? -s : 2), 2, s - 1, red)
          end
        when :sparkle
          [[-140, 8, 0], [-48, 10, 2], [20, 7, 4]].each do |ang, r, ph|
            x, y = polar(ang, RADIUS + r)
            len = [1, 3, 5, 3][(f + ph) % 4]
            C::Pix.rect(b, x - len - 1, y - 1, (len * 2) + 3, 3, col(DARK))
            C::Pix.rect(b, x - 1, y - len - 1, 3, (len * 2) + 3, col(DARK))
            C::Pix.rect(b, x - len, y, (len * 2) + 1, 1, col([255, 248, 160]))
            C::Pix.rect(b, x, y - len, 1, (len * 2) + 1, col([255, 248, 160]))
            C::Pix.rect(b, x, y, 1, 1, col([255, 255, 255]))
          end
        when :gloom
          9.times do |i|
            x = MID - 16 + (i * 4)
            half = Math.sqrt([(RADIUS * RADIUS) - ((x - MID)**2), 0].max).floor
            len = 6 + ((C::Util.hash01(i, 3) * 12).round) + ((f + i) % 3)
            C::Pix.rect(b, x, MID - half + 1, 1, [len, half].min, col([72, 64, 136]))
          end
        when :question, :exclaim
          x, y = polar(-45, RADIUS + 11)
          y -= [0, 1, 2, 1][f % 4]
          white = col([255, 255, 255])
          C::Pix.rect(b, x - 3, y - 8, 8, 15, col(DARK))
          if kind == :exclaim
            C::Pix.rect(b, x, y - 7, 2, 8, col([255, 96, 72]))
            C::Pix.rect(b, x, y + 3, 2, 2, col([255, 96, 72]))
          else
            C::Pix.rect(b, x - 1, y - 7, 4, 2, white)
            C::Pix.rect(b, x + 2, y - 6, 2, 4, white)
            C::Pix.rect(b, x, y - 2, 2, 3, white)
            C::Pix.rect(b, x, y + 3, 2, 2, white)
          end
        when :tears
          [-1, 1].each do |side|
            x = MID + (side * 9)
            blue = col([120, 200, 255])
            C::Pix.rect(b, x - 1, MID - 4, 3, 18, blue)
            C::Pix.rect(b, x, MID - 4 + ((f * 3) % 16), 1, 3, col([255, 255, 255]))
            dx = side * (4 + ((f * 2) % 8))                    # drops flying off
            C::Pix.rect(b, x + dx, MID + 6 - ((f % 4) * 2), 2, 2, blue)
          end
        when :blush
          [-1, 1].each do |side|
            3.times do |i|
              x = MID + (side * 12) + ((i - 1) * 3)
              C::Pix.line(b, x, MID + 7, x + 1, MID + 4, col([255, 104, 136]))
            end
          end
        when :dots
          x, y = polar(-40, RADIUS + 10)
          n = 1 + (f / 2 % 3)
          C::Pix.rect(b, x - 5, y - 2, 15, 6, col(DARK))
          n.times { |i| C::Pix.rect(b, x - 3 + (i * 4), y, 2, 2, col([255, 255, 255])) }
        end
      end
    end

    #---------------------------------------------------------------------------
    class Bubble
      attr_reader :spec, :art_kind, :emotes, :center

      def initialize(spec, msgwindow = nil)
        @spec = spec
        @msg = msgwindow
        @id = spec[:id]
        @expr = (EXPRESSIONS.has_key?(spec[:expression])) ? spec[:expression] : :neutral
        @cfg = EXPRESSIONS[@expr]
        @speaker = Portrait.speaker(spec)
        @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @viewport.z = VIEWPORT_Z
        @art, @art_kind = Art.load(@id, @expr)
        @emotes = (spec[:emotes] || @cfg[:emotes]).select { |e| EMOTES.include?(e) }
        @emotes += (@cfg[:face] || []) if @art_kind != :expression && !spec[:emotes]
        @base_bmp = Bitmap.new(CANVAS, CANVAS)
        @emote_bmp = Bitmap.new(CANVAS, CANVAS)
        @base = sprite(@base_bmp, PX, CANVAS / 2, 0)
        @face = sprite(@art, 1, DIAMETER / 2, 1)
        @over = sprite(@emote_bmp, PX, CANVAS / 2, 2)
        @start = C::Util.now
        @tail_key = nil
        @frame = -1
        @center = [0, 0]
        update
      end

      def sprite(bmp, zoom, origin, z)
        s = Sprite.new(@viewport)
        s.bitmap = bmp
        s.ox = s.oy = origin
        s.zoom_x = s.zoom_y = zoom
        s.z = z
        return s
      end

      # Head of the speaker on screen, or nil.
      def head_point
        return nil if !@speaker || !@speaker.respond_to?(:screen_x)
        x = @speaker.screen_x
        y = @speaker.screen_y - 40
        return nil if x < -32 || x > Graphics.width + 32 || y < -64 || y > Graphics.height + 32
        return [x, y]
      rescue StandardError
        return nil
      end

      def place(head)
        w = Graphics.width
        h = Graphics.height
        r = (RADIUS + 3) * PX
        top = 8 + r
        bottom = h - 8 - r
        if @msg && @msg.respond_to?(:y) && @msg.respond_to?(:height)
          if @msg.y <= 0 then top = @msg.height + 8 + r
          else bottom = @msg.y - 8 - r
          end
        end
        bottom = top if bottom < top
        if head
          x = head[0]
          y = head[1] - r - (TAIL * PX)
        else
          x = r + 24
          y = bottom
        end
        x = C::Util.clamp(x, r + 8, w - r - 8)
        y = C::Util.clamp(y, top, bottom)
        if head && ((x - head[0])**2) + ((y - head[1])**2) < (r + 12)**2   # would cover the speaker
          x += (head[0] < w / 2) ? r + 40 : -(r + 40)
          x = C::Util.clamp(x, r + 8, w - r - 8)
        end
        return [C::Util.snap(x), C::Util.snap(y)]
      end

      def draw_base(dir)
        b = @base_bmp
        b.clear
        dark = C::Util.color([24, 24, 40])
        white = Color.new(255, 255, 255)
        if dir                                           # speech tail
          ux, uy = dir
          px = -uy
          py = ux
          tip = [MID + (ux * (RADIUS + 3 + TAIL)), MID + (uy * (RADIUS + 3 + TAIL))]
          (-6..6).each do |i|
            bx = MID + (ux * (RADIUS - 2)) + (px * i)
            by = MID + (uy * (RADIUS - 2)) + (py * i)
            C::Pix.line(b, bx, by, tip[0], tip[1], dark, 3) if i.abs == 6
          end
          (-5..5).each do |i|
            bx = MID + (ux * (RADIUS - 2)) + (px * i)
            by = MID + (uy * (RADIUS - 2)) + (py * i)
            C::Pix.line(b, bx, by, tip[0], tip[1], white, 2)
          end
        end
        C::Pix.disc(b, MID, MID, RADIUS + 3, dark)
        C::Pix.disc(b, MID, MID, RADIUS + 2, white)
        C::Pix.disc(b, MID, MID, RADIUS, C::Util.color(@cfg[:bg]))
        if dir                                           # the tail joins the ring
          ux, uy = dir
          (-4..4).each do |i|
            C::Pix.rect(b, MID + (ux * (RADIUS + 2)) + (-uy * i) - 1, MID + (uy * (RADIUS + 2)) + (ux * i) - 1, 2, 2, white)
          end
        end
      end

      def update
        return if @disposed
        lt = C::Util.now - @start
        head = head_point
        cx, cy = place(head)
        @center = [cx, cy]
        dir = nil
        key = :none
        if head
          dx = head[0] - cx
          dy = head[1] - cy
          len = Math.sqrt((dx * dx) + (dy * dy))
          if len > 4
            step = (Math.atan2(dy, dx) / (Math::PI / 12)).round     # 24 tail directions
            key = step
            dir = [Math.cos(step * Math::PI / 12), Math.sin(step * Math::PI / 12)]
          end
        elsif @msg                                           # no speaker on screen: point at the box
          key = :down
          dir = [0.0, (@msg.respond_to?(:y) && @msg.y <= 0) ? -1.0 : 1.0]
        end
        if key != @tail_key
          @tail_key = key
          draw_base(dir)
        end
        f = (lt * EMOTE_FPS).to_i
        if f != @frame
          @frame = f
          @emote_bmp.clear
          @emotes.each { |e| Emote.draw(@emote_bmp, e, f) }
        end
        # pop in with a small bounce; scale steps keep the pixels square
        k = C::Ease.apply(:out_back, lt / POP_TIME)
        k = 1.0 if lt >= POP_TIME
        k *= 1.0 + (0.12 * Math.sin(Math::PI * C::Util.clamp(lt / 0.4, 0, 1))) if @cfg[:jolt]
        k = (k * 8).round / 8.0
        sx = sy = 0
        if @cfg[:shake] && lt >= POP_TIME
          sx = (((f * 2) % 3) - 1) * @cfg[:shake] * PX
          sy = (f.odd?) ? PX : 0 if @cfg[:shake] > 1
        end
        [[@base, PX], [@face, 1], [@over, PX]].each do |s, z|
          s.x = cx + sx
          s.y = cy + sy
          s.zoom_x = s.zoom_y = z * k
          s.visible = k > 0
        end
      end

      def dispose
        return if @disposed
        @disposed = true
        [@base, @face, @over].each { |s| s.dispose if s && !s.disposed? }
        [@base_bmp, @emote_bmp, @art].each { |b| b.dispose if b && !b.disposed? }
        @viewport.dispose
      end
    end
  end
end

#-------------------------------------------------------------------------------
# Message hook: a \pf[...] or [portrait: ...] tag in any Show Text / pbMessage
# opens the bubble for that message. Alias-chained; the core method is called
# with the tag removed.
#-------------------------------------------------------------------------------
if defined?(pbMessageDisplay) && !defined?(prismfall_portrait_pbMessageDisplay)
  alias prismfall_portrait_pbMessageDisplay pbMessageDisplay

  def pbMessageDisplay(msgwindow, message, letterbyletter = true, commandProc = nil, &block)
    text, spec = Prismfall::Portrait.extract(message)
    return prismfall_portrait_pbMessageDisplay(msgwindow, message, letterbyletter, commandProc, &block) if !spec
    bubble = Prismfall::Portrait.open(spec, msgwindow)
    begin
      return prismfall_portrait_pbMessageDisplay(msgwindow, text, letterbyletter, commandProc) do
        bubble&.update
        block&.call
      end
    ensure
      Prismfall::Portrait.close
    end
  end
end

# pf_say(:MARTIN, :crying, "text")  - shows "Martin: text" under a portrait bubble.
# Options: emote: :sweat or [:sweat, :shock], event: id or name, name: false (no
# "Name: " prefix) or a String, plus anything pbMessage takes as commands.
def pf_say(id, expression = :neutral, text = "", emote: nil, event: nil, name: nil, commands: nil, cancel: 0)
  emotes = Array(emote).compact.join("+")
  label = (name == false) ? "" : "#{name || Prismfall::Portrait.display_name(id)}: "
  message = "\\pf[#{id},#{expression},#{emotes},#{event}]#{label}#{text}"
  return pbMessage(message, commands, cancel)
end
