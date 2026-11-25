#===============================================================================
# Prismfall Cutscenes - 014 Portraits: face windows and speech bubbles
# (SPINE Revision 22; the bubble is Revision 7's)
#-------------------------------------------------------------------------------
# Three ways a line can look:
#   FACE   (the default for the story cast, once they have portrait art): a
#          framed 96x96 face beside the message box, on its left, Desolation
#          style. The frame is cut from the message box's own windowskin.
#   BUBBLE (opt-in, rare: comic relief, dramatic beats): a round portrait with a
#          speech tail pointing at the speaker on the map, plus emotes.
#   PLAIN  (everyone else, and cast without art yet): the normal message box;
#          the "Name: " label stays in the text.
#
#   Script:    pf_say(:JUNO, :happy, "Hi!")                         face
#              pf_say(:LARCH, :angry, "IT LIVES IN A TREE.", bubble: true, emote: :anger)
#   Show Text: \pf[JUNO,happy]Juno: Hi!                              face
#              \pfb[LARCH,angry,anger]Larch: IT LIVES IN A TREE.     bubble
#              \pfb[MARTIN,shocked,sweat+exclaim,12]Martin: WHAT.    (emotes, event id)
#              [portrait: JUNO, happy] / [bubble: LARCH, angry, anger]  (story-bible tags)
# In face mode the emotes and event fields are ignored. Within one conversation
# a cast member's later name-only lines ("Juno: ...") keep their face with the
# last expression, so scripts only tag first lines and expression changes.
#
# Expressions: any name works for faces (it picks the file); bubbles know
#              neutral happy smug angry crying shocked deadpan panic sad blush surprised
# Emotes:      sweat shock anger sparkle gloom question exclaim tears blush dots
# Portrait art: Graphics/Portraits/ID_expression.png, then ID.png (96x96).
# :PLAYER uses PLAYER_A or PLAYER_B, by the look chosen (pbChangePlayer 1/2).
# Bubbles without art fall back to a round crop of the trainer front sprite's
# head, then a silhouette. See design/CUTSCENES.md section 6.
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
    # Face mode (Desolation's FaceWindowVX: a 128x128 window holding a 96x96 face,
    # set on the message box's left edge, above it, or below it when the box is at the top)
    FACE_SIZE   = 96
    FACE_EDGE   = 16         # frame thickness around the face
    FACE_FRAME  = FACE_SIZE + (FACE_EDGE * 2)
    FACE_POP    = 0.16       # new speaker: rises 8 px out of the box and fades in
    FACE_SWAP   = 0.10       # same speaker, new expression: a 2 px nudge
    FACE_LINGER = 0.35       # a face closed this recently is still "on screen" for the next line
    FACE_SKIN   = "Graphics/Windowskins/speech hgss 1"   # when the message box has no skin to copy
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
      :blush   => { :bg => [255, 192, 208], :emotes => [], :face => [:blush] },
      # every cast pack ships ID_surprised.png; milder than :shocked (one mark, no shock lines)
      :surprised => { :bg => [255, 240, 176], :emotes => [:exclaim], :jolt => true }
    }

    # Optional per-character data: Prismfall::Portrait.register(:MARTIN,
    #   name: "Martin", trainer: :LEADER_MARTIN, event: "Martin", color: [r, g, b],
    #   crop: [x, y, size])   # head square on the trainer sprite, when the default misses
    @people = {}
    @current = nil
    @scene_faces = {}     # "juno" => [:JUNO, :happy]: who has shown a face in this conversation
    @last_face = nil      # [id, file, closed_at] of the last face window

    # Portrait use (SPINE Rev 22). Only the story cast gets a face (once their
    # art exists) or, when a line asks for one, a bubble. Anyone else tagged with
    # \pf[...] or pf_say gets the plain message box with their "Name: " label.
    # Add a character with `Portrait.register(:ID, cast: true)` or by listing them here.
    # See story/13_CUTSCENES.md, "Portrait use".
    ONLY_CAST = true
    CAST = %i[
      PLAYER
      KESTREL JUNO
      VOSS VALEN MOURNER ROWAN
      LARCH EDDA WICK CALLA
      DORIAN TAMSIN MARISOL ROOK SAHAR CORVIN BRANN KAITO ANJA
      ODESSA ILSA BASTIAN YSOLDE MAGNUS NYX CELESTINE SIGRUN
      HESPER TEO THISTLE SABLE KROLL QUENT MARCHETTI HOLLIS PIP MAUD DEX MORWEN
      MAELIS DASK EIRIK HROTHGAR KASSAN RENATA SALLOW GUTTER OKORO DELPHINE
      VESPER WENNA MARTIN WENLOW
      AURELIUS COLL REFLECTION ZARA
      VENAM SHELLY GARRET MELIA ALEXANDRA AMARIA TITANIA SHIV LIN NOVA
      ASHE ASHKAAR_OFFICER ISENMAR_OFFICER MERIDIAN_ADMIN MERIDIAN_ASHE OCTAVE_SINGER
    ]

    class << self
      attr_reader :current

      def register(id, **data); @people[id.to_s.upcase.to_sym] = data; end
      def person(id); return @people[id.to_s.upcase.to_sym] || {}; end

      # true when this speaker may get a face or a bubble
      def cast?(id)
        return true if !ONLY_CAST
        key = id.to_s.upcase.to_sym
        base = key.to_s.sub(/_[AB]\z/, "").to_sym   # PLAYER_A / PLAYER_B
        return true if CAST.include?(key) || CAST.include?(base)
        return person(key)[:cast] == true
      end

      def display_name(id)
        return person(id)[:name] || id.to_s.split("_").map(&:capitalize).join(" ")
      end

      # Pulls a portrait tag out of message text. Returns [clean_text, spec or nil].
      # \pf[...] and [portrait: ...] ask for the face; \pfb[...] and [bubble: ...] for the bubble.
      def extract(message)
        text = message.to_s
        spec = nil
        text = text.sub(/\\pf(b?)\[([^\]]*)\]/i) do
          spec = parse($2, !$1.empty?)
          ""
        end
        if !spec
          text = text.sub(/\[(portrait|bubble):\s*([^\]]*)\]\s*/i) do
            spec = parse($2, $1.downcase == "bubble")
            ""
          end
        end
        text = text.gsub(/\\pfb?\[[^\]]*\]/i, "").gsub(/\[(?:portrait|bubble):[^\]]*\]\s*/i, "") if spec
        return text, spec
      end

      def parse(fields, bubble = false)
        parts = fields.split(",").map(&:strip)
        return nil if parts.empty? || parts[0].to_s.empty?
        expr = (parts[1] && !parts[1].empty?) ? parts[1].downcase.to_sym : :neutral
        emotes = (parts[2].to_s.empty?) ? nil : parts[2].downcase.split(/[+\s|]+/).map(&:to_sym)
        event = (parts[3].to_s.empty?) ? nil : (parts[3] =~ /\A-?\d+\z/ ? parts[3].to_i : parts[3])
        return { :id => parts[0].upcase.to_sym, :expression => expr, :emotes => emotes, :event => event, :bubble => bubble }
      end

      # The art file id: :PLAYER is PLAYER_A or PLAYER_B, by the look picked at the
      # start (pbChangePlayer(1) / (2)); register(:ID, art: :OTHER) borrows another's.
      def art_id(id)
        key = id.to_s.upcase.to_sym
        return person(key)[:art].to_s.upcase.to_sym if person(key)[:art]
        return key if key != :PLAYER
        look = ($player.character_ID rescue 1) if defined?($player) && $player
        return (look == 2) ? :PLAYER_B : :PLAYER_A
      end

      # Graphics/Portraits/ID_expression.png, else ID.png, else nil (no art yet).
      def face_file(id, expression)
        aid = art_id(id)
        ["#{FOLDER}#{aid}_#{expression.to_s.downcase}", "#{FOLDER}#{aid}"].each do |path|
          file = C::Gfx.resolve(path)
          return file if file
        end
        return nil
      end

      # -> :face, :bubble or :plain
      def mode_for(spec)
        return :plain if !spec || !cast?(spec[:id])
        return :bubble if spec[:bubble]
        return :face if face_file(spec[:id], spec[:expression])
        return :plain
      end

      # "Juno" in "Juno: Hi" (after any leading control codes), or nil.
      def label_of(text)
        t = text.to_s.sub(/\A(?:\\[A-Za-z]+(?:\[[^\]]*\])?|\s)+/, "")
        m = t.match(/\A([^:\n\\\[\]]{1,32}):\s/)
        return (m) ? m[1].strip.downcase : nil
      end

      # A cast member's name-only line ("Juno: ...") after one of their tagged lines in
      # the same conversation keeps their face, with the last expression.
      def carry(text)
        return nil if @scene_faces.empty?
        return nil if defined?($game_temp) && $game_temp && $game_temp.respond_to?(:in_battle) && $game_temp.in_battle
        label = label_of(text)
        hit = label && @scene_faces[label]
        return nil if !hit
        return { :id => hit[0], :expression => hit[1], :emotes => nil, :event => nil, :bubble => false, :carried => true }
      end

      def remember(spec, text)
        [label_of(text), display_name(spec[:id]).downcase].compact.uniq.each do |label|
          @scene_faces[label] = [spec[:id], spec[:expression]]
        end
      end

      # A new conversation: the main map interpreter set up an event (see the hook below).
      def new_conversation
        @scene_faces.clear
      end

      # How a face window enters: :pop (new speaker), :swap (new expression) or :none.
      def face_entry(id, file)
        last = @last_face
        return :pop if !last || last[0] != id || C::Util.now - last[2] > FACE_LINGER
        return (last[1] == file) ? :none : :swap
      end

      def face_closed(id, file)
        @last_face = [id, file, C::Util.now]
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

      # mode :face or :bubble (default: what the spec asks for)
      def open(spec, msgwindow = nil, mode = nil)
        close
        mode ||= (spec[:bubble]) ? :bubble : :face
        @current = (mode == :bubble) ? Bubble.new(spec, msgwindow) : FaceBox.new(spec, msgwindow)
        return @current
      rescue StandardError => e
        C::Util.log("portrait #{mode} failed: #{e.class}: #{e.message}")
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
        aid = Portrait.art_id(id)
        src = C::Gfx.load_bitmap("#{FOLDER}#{aid}_#{expression}")
        kind = :expression
        if !src
          src = C::Gfx.load_bitmap("#{FOLDER}#{aid}")
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
    # Face mode: the frame is cut from the message box's own windowskin, so it
    # matches whichever speech frame the player picked in Options.
    #---------------------------------------------------------------------------
    module Frame
      module_function

      # -> FACE_FRAME square bitmap: the skin's left corners and edge (mirrored for the
      # right side, so the frame is symmetric) around a panel of the skin's body colour.
      def build(msgwindow = nil)
        out = Bitmap.new(FACE_FRAME, FACE_FRAME)
        skin, own = skin_for(msgwindow)
        src = (skin) ? region(skin, msgwindow) : nil
        if src
          cut(out, skin, *src)
        else
          drawn(out)
        end
        skin.dispose if own && skin && !skin.disposed?
        return out
      end

      # The message box's skin (it may have been changed with \w[...]), else the
      # speech frame from Options, else the stock HGSS frame. -> [bitmap, loaded_here]
      def skin_for(msgwindow)
        if msgwindow && msgwindow.respond_to?(:windowskin)
          s = msgwindow.windowskin
          return s, false if s.is_a?(Bitmap) && !s.disposed?
        end
        path = (defined?(MessageConfig) && MessageConfig.respond_to?(:pbGetSpeechFrame)) ? MessageConfig.pbGetSpeechFrame : nil
        bmp = (path && !path.to_s.empty?) ? C::Gfx.load_bitmap(path) : nil
        bmp ||= C::Gfx.load_bitmap(FACE_SKIN)
        return bmp, true
      rescue StandardError
        return nil, false
      end

      # -> [x, y, w, h of the frame part, body colour x, y, corner size, back rect or nil]
      def region(skin, msgwindow)
        w = skin.width
        h = skin.height
        return [128, 0, 64, 64, 64, 64, 16, [0, 0, 128, 128]] if w == 192 && h == 128   # RPG Maker XP skin
        return [64, 0, 64, 64, 32, 32, 16, [0, 0, 64, 64]] if w == 128 && h == 128      # RPG Maker VX skin
        c = [FACE_EDGE, w / 3, h / 3].min
        return nil if c < 4
        r = (msgwindow.respond_to?(:skinrect)) ? msgwindow.skinrect : nil
        if r.is_a?(Rect) && r.width > 0 && r.height > 0 && r.x + r.width <= w && r.y + r.height <= h
          bx = r.x + (r.width / 2)
          by = r.y + (r.height / 2)
        elsif h == 48 && (w == 96 || w == 80)          # Essentials' speech frames (body 32,16,16,16)
          bx, by = 40, 24
        else
          bx, by = w / 2, h / 2
        end
        return [0, 0, w, h, bx, by, c, nil]
      end

      def cut(out, skin, ox, oy, w, h, bx, by, c, back)
        f = FACE_FRAME
        mid = f - (c * 2)
        if back
          out.stretch_blt(Rect.new(2, 2, f - 4, f - 4), skin, Rect.new(*back))
        else
          out.stretch_blt(Rect.new(c, c, mid, mid), skin, Rect.new(bx, by, 1, 1))
        end
        c.times do |i|
          [i, f - 1 - i].each do |dx|                    # a left column, and its mirror on the right
            out.blt(dx, 0, skin, Rect.new(ox + i, oy, 1, c))
            out.blt(dx, f - c, skin, Rect.new(ox + i, oy + h - c, 1, c))
            out.stretch_blt(Rect.new(dx, c, 1, mid), skin, Rect.new(ox + i, oy + c, 1, h - (c * 2)))
          end
        end
        out.stretch_blt(Rect.new(c, 0, mid, c), skin, Rect.new(ox + c - 1, oy, 1, c))
        out.stretch_blt(Rect.new(c, f - c, mid, c), skin, Rect.new(ox + c - 1, oy + h - c, 1, c))
      end

      # No skin at all: a plain dark-rimmed box.
      def drawn(out)
        f = FACE_FRAME
        e = FACE_EDGE
        out.fill_rect(4, 2, f - 8, f - 4, Color.new(72, 64, 72))
        out.fill_rect(2, 4, f - 4, f - 8, Color.new(72, 64, 72))
        out.fill_rect(6, 4, f - 12, f - 8, Color.new(100, 100, 112))
        out.fill_rect(4, 6, f - 8, f - 12, Color.new(100, 100, 112))
        out.fill_rect(e, e, f - (e * 2), f - (e * 2), Color.new(248, 248, 248))
      end
    end

    #---------------------------------------------------------------------------
    # Face mode: a framed face beside the message box (Desolation's face window).
    #---------------------------------------------------------------------------
    class FaceBox
      attr_reader :spec, :file, :entry, :rect

      def initialize(spec, msgwindow = nil)
        @spec = spec
        @msg = msgwindow
        @id = spec[:id]
        @file = Portrait.face_file(@id, spec[:expression])
        @entry = Portrait.face_entry(@id, @file)
        @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
        @viewport.z = VIEWPORT_Z
        @frame_bmp = Frame.build(msgwindow)
        @face_bmp = load_face
        @frame = Sprite.new(@viewport)
        @frame.bitmap = @frame_bmp
        @face = Sprite.new(@viewport)
        @face.bitmap = @face_bmp
        @face.z = 1
        @start = C::Util.now
        @first = true
        @rect = [0, 0, FACE_FRAME, FACE_FRAME]
        update
      end

      # The art as a FACE_SIZE square (other square sizes are scaled to it).
      def load_face
        out = Bitmap.new(FACE_SIZE, FACE_SIZE)
        src = (@file) ? C::Gfx.load_bitmap(@file) : nil
        return out if !src
        size = [src.width, src.height].min
        sx = (src.width - size) / 2
        if size == FACE_SIZE
          out.blt(0, 0, src, Rect.new(sx, 0, size, size))
        else
          out.stretch_blt(Rect.new(0, 0, FACE_SIZE, FACE_SIZE), src, Rect.new(sx, 0, size, size))
        end
        src.dispose
        return out
      end

      # pbPositionNearMsgWindow(face, msg, :left): on the box's left edge, above it,
      # or below it when there is no room above (the box at the top).
      def place
        mx = 0
        mh = 96
        my = Graphics.height - mh
        if @msg && @msg.respond_to?(:y) && @msg.respond_to?(:height)
          mx = @msg.x.to_i if @msg.respond_to?(:x)
          mh = @msg.height.to_i
          my = (@first) ? predicted_y(mh) : @msg.y.to_i
        end
        y = my - FACE_FRAME
        below = y < 0
        y = my + mh if below
        return mx, y, below
      end

      # The face opens before the core places the box for this message: guess the
      # place the same way pbRepositionMessageWindow will (later frames use the real one).
      def predicted_y(mh)
        pos = ($game_system.message_position rescue 2) if defined?($game_system) && $game_system
        return 0 if pos == 0
        return (Graphics.height - mh) / 2 if pos == 1
        return Graphics.height - mh
      end

      def update
        return if @disposed
        x, y, below = place
        @first = false
        t = C::Util.now - @start
        dy = 0                   # frame and face
        op = 255
        fdy = 0                  # face only
        fop = 255
        if @entry == :pop && t < FACE_POP
          k = C::Ease.apply(:out, t / FACE_POP)
          dy = ((1 - k) * 4).round * 2                   # 8 px, in 2 px steps, out of the box
          dy = -dy if below
          op = (255 * k).round
          fop = op
        elsif @entry == :swap && t < FACE_SWAP
          fdy = (t < FACE_SWAP / 2) ? ((below) ? -2 : 2) : 0
          fop = (160 + (95 * t / FACE_SWAP)).round
        end
        @frame.x = x
        @frame.y = y + dy
        @frame.opacity = op
        @face.x = x + FACE_EDGE
        @face.y = y + FACE_EDGE + dy + fdy
        @face.opacity = fop
        @rect = [x, y, FACE_FRAME, FACE_FRAME]
      end

      def dispose
        return if @disposed
        @disposed = true
        Portrait.face_closed(@id, @file)
        [@frame, @face].each { |s| s.dispose if s && !s.disposed? }
        [@frame_bmp, @face_bmp].each { |b| b.dispose if b && !b.disposed? }
        @viewport.dispose
      end
    end

    #---------------------------------------------------------------------------
    # Bubble mode (opt-in): round portrait, speech tail, emotes.
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
        @art, @art_kind = Art.load(@id, spec[:expression] || @expr)   # the file goes by the name asked for
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
# Message hook: a \pf[...] / \pfb[...] (or [portrait: ...] / [bubble: ...]) tag in
# any Show Text / pbMessage shows that message with a face or a bubble. A cast
# member's untagged "Name: ..." line keeps the face they showed earlier in the
# same conversation. Alias-chained; the core method gets the text without the tag.
#-------------------------------------------------------------------------------
if defined?(pbMessageDisplay) && !defined?(prismfall_portrait_pbMessageDisplay)
  alias prismfall_portrait_pbMessageDisplay pbMessageDisplay

  def pbMessageDisplay(msgwindow, message, letterbyletter = true, commandProc = nil, &block)
    pf = Prismfall::Portrait
    text, spec = pf.extract(message)
    spec ||= pf.carry(text)
    mode = pf.mode_for(spec)
    pf.remember(spec, text) if mode != :plain && !spec[:carried]
    # No tag, not story cast, or no art yet (and no bubble asked for): the plain box,
    # tag stripped (the "Name: " label stays).
    return prismfall_portrait_pbMessageDisplay(msgwindow, text, letterbyletter, commandProc, &block) if mode == :plain
    view = pf.open(spec, msgwindow, mode)
    begin
      return prismfall_portrait_pbMessageDisplay(msgwindow, text, letterbyletter, commandProc) do
        view&.update
        block&.call
      end
    ensure
      pf.close
    end
  end
end

# A new event on the main map interpreter starts a new conversation (faces are
# not carried over from the last one). Parallel and child interpreters don't count.
if defined?(Interpreter) && !Interpreter.method_defined?(:prismfall_portrait_setup)
  class Interpreter
    alias prismfall_portrait_setup setup

    def setup(*args)
      Prismfall::Portrait.new_conversation if @main
      return prismfall_portrait_setup(*args)
    end
  end
end

# pf_say(:JUNO, :happy, "text")  - "Juno: text" with Juno's face beside the box
# (or the plain box until she has art). bubble: true - the speech bubble instead
# (the rare comic/dramatic beat); then emote: :sweat or [:sweat, :shock] and
# event: id or name (who the tail points at) apply. name: false (no "Name: "
# prefix) or a String; commands:/cancel: as pbMessage takes them.
def pf_say(id, expression = :neutral, text = "", emote: nil, event: nil, name: nil, commands: nil, cancel: 0, bubble: false)
  emotes = Array(emote).compact.join("+")
  label = (name == false) ? "" : "#{name || Prismfall::Portrait.display_name(id)}: "
  tag = (bubble) ? "pfb" : "pf"
  message = "\\#{tag}[#{id},#{expression},#{emotes},#{event}]#{label}#{text}"
  return pbMessage(message, commands, cancel)
end

# The Gilded King (Gemini rework 2026-11-23, Path B; ids and art renamed from THEODRIC 2026-11-24) is shown as
# "Gilded King Aurelius": [portrait: AURELIUS, smug] in scripts.
Prismfall::Portrait.register(:AURELIUS, name: "Gilded King Aurelius", trainer: :GILDED_AURELIUS, cast: true)
# Script tags that differ from the art prefix (Gemini wiring audit 2026-11-24): Ch16 writes [portrait: SALLOW, ...]
# and Ch5 [portrait: RENATA, ...] for the same Councillor; the Envoy's files are OKORO_* (her tag in Ch20), and her
# first name works too; the Spin Doctor's single class portrait is MERIDIAN_ASHE.
Prismfall::Portrait.register(:RENATA,   name: "Councillor Sallow",  cast: true)
Prismfall::Portrait.register(:SALLOW,   name: "Councillor Sallow",  art: :RENATA, cast: true)
Prismfall::Portrait.register(:OKORO,    name: "Envoy Okoro",        cast: true)
Prismfall::Portrait.register(:DELPHINE, name: "Envoy Okoro",        art: :OKORO, cast: true)
Prismfall::Portrait.register(:ASHE,     name: "Ashe",               art: :MERIDIAN_ASHE, trainer: :MERIDIAN_ASHE, cast: true)
Prismfall::Portrait.register(:MAUD,     name: "Hierophant Ellery",  cast: true)
Prismfall::Portrait.register(:GUTTER,   name: "Mother Gutter",      trainer: :SUMP_BARON, cast: true)
Prismfall::Portrait.register(:EIRIK,    name: "Thane Eirik",        cast: true)
Prismfall::Portrait.register(:HROTHGAR, name: "Dominar Hrothgar",   cast: true)
Prismfall::Portrait.register(:KASSAN,   name: "Prince-Elector Kassan", cast: true)
Prismfall::Portrait.register(:REFLECTION, name: "Reflection",       trainer: :REFLECTION, cast: true)
Prismfall::Portrait.register(:ZARA,     name: "Zara",               trainer: :PUNK_ZARA, cast: true)
# Sister-game cameos (design/CAMEOS.md): home-game looks, 12 expressions each
{ :VENAM => :FESTIVAL_VENAM, :SHELLY => :FESTIVAL_SHELLY, :GARRET => :FESTIVAL_GARRET, :MELIA => :FESTIVAL_MELIA,
  :ALEXANDRA => :FESTIVAL_ALEXANDRA, :AMARIA => :FESTIVAL_AMARIA, :TITANIA => :FESTIVAL_TITANIA,
  :SHIV => :FESTIVAL_SHIV, :LIN => :FESTIVAL_LIN, :NOVA => :FESTIVAL_NOVA }.each do |id, type|
  Prismfall::Portrait.register(id, trainer: type, cast: true)
end
