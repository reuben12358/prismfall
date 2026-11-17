#===============================================================================
# Prismfall Cutscenes - 004 Graphics loading and actors
#-------------------------------------------------------------------------------
# Actors come from Pokemon battler sprites (EBDX animated strips or single
# frames), trainer front sprites, overworld charsets, Pokemon icons, any image,
# or small procedural props. A missing graphic never stops a scene: a
# code-drawn placeholder stands in.
#===============================================================================
module Prismfall
  module Cutscene
    module Gfx
      # mode: :single, :strip (bitmap = current frame, strip = source sheet),
      #       :charset (4x4), :icon (frames side by side)
      Data = Struct.new(:bitmap, :fw, :fh, :frames, :mode, :px, :strip, :placeholder)
      DIR_ROWS = { :down => 0, :left => 1, :right => 2, :up => 3 }

      module_function

      # Art shipped with this plugin (Graphics/ inside the plugin folder) is found
      # when the game's own Graphics folder has no file of that name.
      PLUGIN_ROOT = "Plugins/Prismfall Cutscenes/"

      def resolve(path)
        return nil if path.nil? || path == ""
        [path, PLUGIN_ROOT + path].each do |p|
          found = if defined?(pbResolveBitmap) then pbResolveBitmap(p)
                  elsif File.file?(p) then p
                  elsif File.file?(p + ".png") then p + ".png"
                  end
          return found if found
          break if path.start_with?("/")
        end
        return nil
      rescue StandardError
        return nil
      end

      def load_bitmap(path)
        file = resolve(path)
        return nil if !file
        return Bitmap.new(file)
      rescue StandardError => e
        Util.log("could not load #{path}: #{e.message}")
        return nil
      end

      def native_px(height); return (height <= NATIVE_SPRITE_MAX_HEIGHT) ? 2 : 1; end

      # Square-frame horizontal strips (EBDX) are animated; anything else is one frame.
      def from_sheet(bmp)
        if bmp.width > bmp.height && (bmp.width % bmp.height) == 0
          size = bmp.height
          frame = Bitmap.new(size, size)
          frame.blt(0, 0, bmp, Rect.new(0, 0, size, size))
          return Data.new(frame, size, size, bmp.width / size, :strip, native_px(size), bmp, false)
        end
        return Data.new(bmp, bmp.width, bmp.height, 1, :single, native_px(bmp.height), nil, false)
      end

      def pokemon(species, back: false, shiny: false, form: 0, gender: 0)
        file = nil
        if defined?(GameData::Species)
          begin
            file = (back) ? GameData::Species.back_sprite_filename(species, form, gender, shiny) :
                            GameData::Species.front_sprite_filename(species, form, gender, shiny)
          rescue StandardError
            file = nil
          end
        end
        bmp = load_bitmap(file)
        return from_sheet(bmp) if bmp
        return creature(Util.palette(Util.type_palette(species, :steel)))
      end

      def trainer(type)
        file = nil
        if defined?(GameData::TrainerType) && type.is_a?(Symbol)
          file = (GameData::TrainerType.front_sprite_filename(type) rescue nil)
        end
        file ||= "Graphics/Trainers/#{type}"
        bmp = load_bitmap(file)
        bmp ||= load_bitmap("Graphics/Trainers/#{STAND_INS[type]}") if STAND_INS[type]
        return from_sheet(bmp) if bmp
        return person(person_color(type), 2, 3)
      end

      # name: a Graphics/Characters file name, or a trainer type id.
      def charset(name, color = nil)
        file = nil
        if name.is_a?(Symbol) && defined?(GameData::TrainerType)
          file = (GameData::TrainerType.charset_filename(name) rescue nil)
        elsif name.is_a?(String)
          file = "Graphics/Characters/#{name}"
        end
        bmp = load_bitmap(file)
        bmp ||= load_bitmap("Graphics/Characters/trainer_#{STAND_INS[name]}") if name.is_a?(Symbol) && STAND_INS[name]
        return Data.new(bmp, bmp.width / 4, bmp.height / 4, 4, :charset, 1, nil, false) if bmp
        return placeholder_charset(color || person_color(name))
      end

      def player_charset
        name = ($game_player.character_name rescue nil)
        return charset(name.to_s) if name && name != ""
        return placeholder_charset([232, 232, 240])
      end

      def icon(species, shiny: false, form: 0)
        file = nil
        if defined?(GameData::Species)
          file = (GameData::Species.icon_filename(species, form, 0, shiny) rescue nil)
        end
        bmp = load_bitmap(file)
        if bmp
          n = [bmp.width / [bmp.height, 1].max, 1].max
          return Data.new(bmp, bmp.width / n, bmp.height, n, :icon, 1, nil, false)
        end
        return placeholder_icon(Util.palette(Util.type_palette(species, :steel)))
      end

      def image(path)
        bmp = load_bitmap(path)
        return Data.new(bmp, bmp.width, bmp.height, 1, :single, 1, nil, false) if bmp
        return creature(Util.palette(:steel))
      end

      # Stable colour for an unknown person, from the id's letters.
      def person_color(id)
        s = id.to_s
        return [200, 72, 48]  if s.include?("ASHKAAR")
        return [72, 136, 208] if s.include?("ISENMAR")
        h = s.sum
        return [80 + (h * 37 % 150), 80 + (h * 59 % 150), 80 + (h * 83 % 150)]
      end

      #-------------------------------------------------------------------------
      # Placeholders and props (drawn at art-pixel size, shown at 2x)
      #-------------------------------------------------------------------------
      def creature(pal)
        b = Bitmap.new(40, 40)
        dark = Color.new(24, 24, 32)
        Pix.disc(b, 20, 26, 14, dark)
        Pix.disc(b, 20, 12, 10, dark)
        Pix.disc(b, 20, 26, 13, pal.outer)
        Pix.disc(b, 20, 12, 9, pal.outer)
        Pix.disc(b, 20, 28, 8, pal.inner)
        Pix.rect(b, 15, 10, 2, 3, dark)
        Pix.rect(b, 23, 10, 2, 3, dark)
        Pix.rect(b, 15, 10, 1, 1, pal.core)
        Pix.rect(b, 23, 10, 1, 1, pal.core)
        return Data.new(b, 40, 40, 1, :single, 2, nil, true)
      end

      def draw_person(b, x, y, col, step = 0, scale = 1)
        dark = Color.new(24, 24, 32)
        skin = Color.new(240, 200, 160)
        body = Util.color(col)
        shade = Util.color(Util.mix(col, [0, 0, 0], 0.35))
        s = scale
        Pix.rect(b, x + (4 * s), y, 8 * s, 8 * s, dark)
        Pix.rect(b, x + (5 * s), y + (1 * s), 6 * s, 6 * s, skin)
        Pix.rect(b, x + (5 * s), y + (1 * s), 6 * s, 2 * s, shade)
        Pix.rect(b, x + (3 * s), y + (8 * s), 10 * s, 9 * s, dark)
        Pix.rect(b, x + (4 * s), y + (8 * s), 8 * s, 8 * s, body)
        Pix.rect(b, x + (4 * s), y + (13 * s), 8 * s, 3 * s, shade)
        lx = (step == 1) ? 1 : 0
        rx = (step == 3) ? 1 : 0
        Pix.rect(b, x + (5 * s), y + (17 * s), 2 * s, (6 - lx) * s, dark)
        Pix.rect(b, x + (9 * s), y + (17 * s), 2 * s, (6 - rx) * s, dark)
      end

      def person(col, px = 2, scale = 3)
        b = Bitmap.new(16 * scale, 24 * scale)
        draw_person(b, 0, 0, col, 0, scale)
        return Data.new(b, b.width, b.height, 1, :single, px, nil, true)
      end

      def placeholder_charset(col)
        @charsets ||= {}
        key = col[0, 3]
        cached = @charsets[key]
        return cached if cached && !cached.bitmap.disposed?
        b = Bitmap.new(64, 96)
        4.times { |row| 4.times { |c| draw_person(b, c * 16, row * 24, col, c) } }
        @charsets[key] = Data.new(b, 16, 24, 4, :charset, 2, nil, true)
        return @charsets[key]
      end

      def placeholder_cache_size
        return (@charsets || {}).count { |_, d| !d.bitmap.disposed? }
      end

      def placeholder_icon(pal)
        b = Bitmap.new(64, 32)
        dark = Color.new(24, 24, 32)
        2.times do |i|
          cx = 16 + (i * 32)
          cy = 18 - i
          Pix.disc(b, cx, cy, 10, dark)
          Pix.disc(b, cx, cy, 9, pal.outer)
          Pix.disc(b, cx, cy + 2, 5, pal.inner)
          Pix.rect(b, cx - 4, cy - 3, 2, 2, dark)
          Pix.rect(b, cx + 3, cy - 3, 2, 2, dark)
        end
        return Data.new(b, 32, 32, 2, :icon, 2, nil, true)
      end

      # Procedural props: :ship (sled-ship), :banner, :stone, :tripod.
      def prop(kind, col = nil)
        col ||= [120, 136, 160]
        c = Util.color(col)
        shade = Util.color(Util.mix(col, [0, 0, 0], 0.4))
        light = Util.color(Util.mix(col, [255, 255, 255], 0.5))
        dark = Color.new(24, 24, 32)
        case kind
        when :ship
          b = Bitmap.new(56, 40)
          Pix.rect(b, 27, 2, 2, 28, dark)
          14.times { |i| Pix.rect(b, 29, 4 + i, 16 - i, 1, (i < 3) ? light : c) }
          8.times { |i| Pix.rect(b, 4 + i, 28 + i, 48 - (i * 2), 1, (i == 0) ? light : shade) }
          Pix.rect(b, 2, 36, 52, 2, dark)
          Pix.rect(b, 0, 34, 4, 2, dark)
        when :banner
          b = Bitmap.new(16, 32)
          Pix.rect(b, 2, 0, 2, 32, dark)
          Pix.rect(b, 4, 2, 10, 12, c)
          Pix.rect(b, 4, 2, 10, 2, light)
          Pix.rect(b, 4, 12, 10, 2, shade)
          Pix.rect(b, 10, 14, 4, 2, c)
        when :tripod
          b = Bitmap.new(16, 24)
          Pix.rect(b, 5, 2, 6, 5, c)
          Pix.rect(b, 6, 3, 2, 2, light)
          Pix.line(b, 8, 7, 3, 23, dark)
          Pix.line(b, 8, 7, 13, 23, dark)
          Pix.rect(b, 7, 7, 2, 16, dark)
        else   # :stone
          b = Bitmap.new(12, 12)
          Pix.disc(b, 6, 6, 5, dark)
          Pix.disc(b, 6, 6, 4, c)
          Pix.rect(b, 4, 3, 2, 2, light)
        end
        return Data.new(b, b.width, b.height, 1, :single, 2, nil, true)
      end

      # o: the options of an `actor` command.
      def for_actor(o)
        if o[:species]   then return pokemon(o[:species], back: o[:back] || false, shiny: o[:shiny] || false,
                                              form: o[:form] || 0, gender: o[:gender] || 0)
        elsif o[:trainer] then return trainer(o[:trainer])
        elsif o[:player]  then return player_charset
        elsif o[:charset] then return charset(o[:charset], o[:color])
        elsif o[:icon]    then return icon(o[:icon], shiny: o[:shiny] || false, form: o[:form] || 0)
        elsif o[:image]   then return image(o[:image])
        elsif o[:prop]    then return prop(o[:prop], o[:color])
        end
        return placeholder_charset(o[:color] || [200, 200, 208])
      end

      def dispose(data)
        return if !data
        return if data.mode == :charset && data.placeholder   # shared cache
        data.bitmap.dispose if data.bitmap && !data.bitmap.disposed?
        data.strip.dispose if data.strip && !data.strip.disposed?
      end
    end

    #---------------------------------------------------------------------------
    # Actor: one sprite in world space, anchored at its feet (bottom centre).
    #---------------------------------------------------------------------------
    class Actor
      attr_accessor :x, :y, :scale, :angle, :opacity, :flip, :off_x, :off_y, :z, :walking, :dir, :tint, :mouth
      attr_reader :id, :sprite, :gfx

      def initialize(scene, id, o)
        @id      = id
        @gfx     = Gfx.for_actor(o)
        @x, @y   = (o[:at] || [scene.w / 2, scene.h / 2]).map(&:to_f)
        @scale   = (o[:scale] || 1).to_f
        @angle   = (o[:angle] || 0).to_f
        @opacity = (o[:opacity] || 255).to_f
        @flip    = o[:flip] || false
        @z       = o[:z]
        @dir     = o[:dir] || :down
        @walking = o[:walk] || false
        @animate = o[:animate] != false
        @mouth   = o[:mouth]
        @submerge = (o[:submerge] || 0).to_i
        @tint    = [0.0, 0.0, 0.0, 0.0]
        sil = o[:silhouette]
        sil = [16, 16, 24] if sil == true
        @tint = Util.rgb(sil)[0, 3].map(&:to_f) + [255.0] if sil
        if o[:tint]
          c = Util.rgb(o[:tint])
          @tint = [c[0].to_f, c[1].to_f, c[2].to_f, (c[3] || 128).to_f]
        end
        @off_x = @off_y = 0.0
        @time  = Util.hash01(id.to_s.sum) * 3
        @frame = -1
        @color = Color.new(0, 0, 0, 0)
        @sprite = Sprite.new(scene.viewport)
        @sprite.bitmap = @gfx.bitmap
        @sprite.ox = @gfx.fw / 2
        @sprite.oy = @gfx.fh - @submerge
        @sprite.src_rect.set(0, 0, @gfx.fw, @gfx.fh - @submerge) if @submerge > 0
        update(scene, 0)
      end

      def width;  return @gfx.fw * @gfx.px * @scale; end
      def height; return (@gfx.fh - @submerge) * @gfx.px * @scale; end
      def pos;    return [@x, @y]; end
      def center; return [@x, @y - (height / 2)]; end
      def top;    return [@x, @y - height]; end

      # Where beams leave from: mouth: [dx, dy] from the feet (dx mirrors with
      # flip), default a little above the centre.
      def mouth_point
        return [@x, @y - (height * 0.58)] if !@mouth
        return [@x + ((@flip) ? -@mouth[0] : @mouth[0]), @y + @mouth[1]]
      end

      def update(scene, dt)
        @time += dt
        case @gfx.mode
        when :strip
          f = (@animate) ? (@time * POKEMON_ANIM_FPS).to_i % @gfx.frames : 0
          if f != @frame
            @frame = f
            @gfx.bitmap.clear
            @gfx.bitmap.blt(0, 0, @gfx.strip, Rect.new(f * @gfx.fw, 0, @gfx.fw, @gfx.fh))
          end
        when :charset
          col = (@walking) ? (@time * 6).to_i % 4 : 0
          @sprite.src_rect.set(col * @gfx.fw, (Gfx::DIR_ROWS[@dir] || 0) * @gfx.fh, @gfx.fw, @gfx.fh - @submerge)
        when :icon
          col = (@animate) ? (@time * 4).to_i % @gfx.frames : 0
          @sprite.src_rect.set(col * @gfx.fw, 0, @gfx.fw, @gfx.fh)
        end
        cam = scene.camera
        sx, sy = cam.to_screen(@x + @off_x, @y + @off_y, 1.0)
        if cam.zoom == 1.0
          sx = Util.snap(sx)
          sy = Util.snap(sy)
        end
        @sprite.x = sx.round
        @sprite.y = sy.round
        @sprite.zoom_x = @sprite.zoom_y = @gfx.px * @scale * cam.zoom
        @sprite.angle = @angle
        @sprite.mirror = @flip
        @sprite.opacity = @opacity.round
        @sprite.z = @z || (500 + @y.round)
        sil = scene.silhouette_rgb
        if sil then @color.set(sil[0], sil[1], sil[2], 255)
        else @color.set(@tint[0], @tint[1], @tint[2], @tint[3])
        end
        @sprite.color = @color
        update_rim(scene) if @rim
      end

      def dispose
        dispose_rim if @rim
        @sprite.dispose if @sprite && !@sprite.disposed?
        Gfx.dispose(@gfx)
      end
    end
  end
end
