#===============================================================================
# Prismfall Cutscenes - 003 Scene definitions and the authoring DSL
#-------------------------------------------------------------------------------
#   Prismfall::Cutscene.define(:MY_SCENE) do
#     background :sky, palette: :dusk
#     actor :hero, species: :LUCARIO, at: [140, 300], flip: true
#     text "It began at dusk."
#     beam from: :hero, to: [420, 200], color: :fighting
#   end
#   Prismfall::Cutscene.play(:MY_SCENE)
#
# Timing model: a time cursor runs through the block.
#   * "Showpiece" commands (text, say, title, beam, beam_clash, charge_up,
#     volley, clash_armies, lunge, faint, fade_out/in, vs_card) take their
#     duration from the cursor: the next command starts when they end.
#   * Tweens (move, pan, zoom, fade, tint, scale, rotate, shake, flash, tone,
#     march, overlay, letterbox, emit...) start at the cursor and do NOT move
#     it, so several can run under the next showpiece. Add `wait: true` to
#     block, or `wait: false` to make a showpiece run in the background.
#   * wait(n) moves the cursor; together { } starts everything inside at the
#     same time; sequence { } is a normal run nested in a together; at(t) { }
#     places commands at an absolute time.
#===============================================================================
module Prismfall
  module Cutscene
    Event = Struct.new(:t, :dur, :op, :args, :seq)

    class Definition
      attr_reader :id, :events, :options
      attr_accessor :length

      def initialize(id, options = {})
        @id      = id
        @options = options
        @events  = []
        @length  = 0.0
      end

      def finish!
        @events = @events.sort_by { |e| [e.t, e.seq] }
        return self
      end

      def uses?(op); return @events.any? { |e| e.op == op }; end
    end

    class Builder
      attr_reader :definition, :vars

      def initialize(id, options = {}, vars = {})
        @definition = Definition.new(id, options)
        @vars  = vars
        @t     = 0.0
        @mode  = :seq
        @par_max = 0.0
        @seq   = 0
        @ids   = {}
      end

      # Scene variable (variant switches etc.) passed to Cutscene.play/build.
      def var(key, default = nil)
        return (@vars.has_key?(key)) ? @vars[key] : default
      end

      def now; return @t; end

      #-------------------------------------------------------------------------
      # Flow
      #-------------------------------------------------------------------------
      def wait(seconds)
        @t += seconds.to_f
        @par_max = [@par_max, @t].max if @mode == :par
        @definition.length = [@definition.length, @t].max
      end

      def together(&block)
        saved = [@mode, @par_max]
        start = @t
        @mode = :par
        @par_max = start
        run(&block)
        finish = [@par_max, @t].max
        @mode, @par_max = saved
        @t = start
        block_end(finish)
      end

      def sequence(&block)
        saved = [@mode, @par_max]
        start = @t
        @mode = :seq
        run(&block)
        finish = @t
        @mode, @par_max = saved
        @t = start
        block_end(finish)
      end

      def at(time, &block)
        saved = [@mode, @par_max, @t]
        @mode = :seq
        @t = time.to_f
        run(&block)
        @mode, @par_max, @t = saved
      end

      # Runs a Ruby block against the live scene (escape hatch).
      def call(always: false, &block); add(:call, { :proc => block, :always => always }); end

      # Inlines another defined scene at the cursor.
      def include_scene(id, **vars)
        blk = Cutscene.block_for(id)
        raise ArgumentError, "Unknown cutscene #{id.inspect}" if !blk
        saved = @vars
        @vars = @vars.merge(vars)
        run(&blk)
        @vars = saved
      end

      #-------------------------------------------------------------------------
      # Stage: backgrounds, actors
      #-------------------------------------------------------------------------
      def background(kind = nil, **o)
        kind ||= (o[:image]) ? :image : :color
        add(:background, o.merge(:kind => kind))
      end

      def clear_backgrounds; add(:clear_backgrounds, {}); end

      def actor(id, **o)
        @ids[id] = :actor
        add(:actor, o.merge(:id => id))
      end

      def remove(id, **o);  add(:remove, o.merge(:id => ref(id)), 0.0); end
      def clear_actors;     add(:clear_actors, {}); end   # ids may be declared again afterwards
      def move(id, **o);    tween(:move, id, o, 0.6); end
      def scale(id, **o);   tween(:scale, id, o, 0.4); end
      def rotate(id, **o);  tween(:rotate, id, o, 0.4); end
      def fade(id, **o);    tween(:fade, id, o, 0.4); end
      def tint(id, **o);    tween(:tint, id, o, 0.3); end
      def flip(id, value = nil); add(:flip, { :id => ref(id), :value => value }); end
      def face(id, dir);    add(:face, { :id => ref(id), :dir => dir }); end
      def hop(id, **o);     tween(:hop, id, o, 0.35); end
      def tremble(id, **o); tween(:tremble, id, o, 0.5); end
      def lunge(id, **o);   add(:lunge, o.merge(:id => ref(id)), o[:duration] || 0.4, true); end
      def hit(id, **o);     add(:hit, o.merge(:id => ref(id)), o[:duration] || 0.35); end
      def faint(id, **o);   add(:faint, o.merge(:id => ref(id)), o[:duration] || 0.8, true); end
      def hp_bar(id, **o);  tween(:hp_bar, id, o, 0.6); end

      #-------------------------------------------------------------------------
      # Camera and screen
      #-------------------------------------------------------------------------
      def camera(**o);  add(:camera, check_points(o)); end
      def cut(**o);     add(:cut, check_points(o), o[:duration] || 0.0); end
      def pan(**o);     add(:pan, check_points(o), o[:duration] || 1.0); end
      def zoom(**o);    add(:zoom, o, o[:duration] || 0.6); end
      def shake(**o);   add(:shake, o, o[:duration] || 0.4); end
      def flash(**o);   add(:flash, o, o[:duration] || 0.3); end
      def tone(**o);    add(:tone, o, o[:duration] || 0.5); end
      def fade_out(**o); add(:fade_out, o, o[:duration] || 0.5, true); end
      def fade_in(**o);  add(:fade_in, o, o[:duration] || 0.5, true); end

      def letterbox(on = true, **o)
        add(:letterbox, o.merge(:on => on), o[:duration] || 0.5)
      end

      #-------------------------------------------------------------------------
      # Particles and overlays
      #-------------------------------------------------------------------------
      def emit(kind, **o);  add(:emit, check_points(o).merge(:kind => kind), 0.0); end
      def stop_emit(id = nil); add(:stop_emit, { :id => id }); end
      def burst(kind, **o); add(:burst, check_points(o).merge(:kind => kind)); end
      def overlay(kind, **o); add(:overlay, o.merge(:kind => kind), o[:duration] || 1.0); end
      def dome(**o);        add(:dome, check_points(o), o[:duration] || 2.0); end

      #-------------------------------------------------------------------------
      # Text
      #-------------------------------------------------------------------------
      def text(str, **o)
        add(:text, o.merge(:text => str), o[:duration] || Builder.read_time(str), true)
      end

      def say(speaker, str, **o)
        add(:text, o.merge(:text => str, :speaker => speaker), o[:duration] || Builder.read_time(str), true)
      end

      def title(str, **o)
        add(:title, o.merge(:text => str), o[:duration] || 2.5, true)
      end

      def vs_card(**o); add(:vs_card, o, o[:duration] || 4.0, true); end

      def self.read_time(str)
        return Util.clamp(1.3 + (str.to_s.length * 0.05), 1.8, 6.0)
      end

      #-------------------------------------------------------------------------
      # Audio
      #-------------------------------------------------------------------------
      def bgm(name, **o); add(:bgm, o.merge(:name => name)); end
      def bgs(name, **o); add(:bgs, o.merge(:name => name)); end
      def se(name, **o);  add(:se, o.merge(:name => name)); end
      def me(name, **o);  add(:me, o.merge(:name => name)); end
      def cry(species, **o); add(:cry, o.merge(:species => species)); end
      def bgm_fade(seconds = 1.0); add(:bgm_fade, { :seconds => seconds }); end
      def bgs_fade(seconds = 1.0); add(:bgs_fade, { :seconds => seconds }); end

      #-------------------------------------------------------------------------
      # Beams
      #-------------------------------------------------------------------------
      def charge_up(**o); add(:charge_up, check_points(o), o[:duration] || 1.0, true); end
      def beam(**o);      add(:beam, check_points(o), o[:duration] || 1.2, true); end
      def impact(**o);    add(:impact, check_points(o), o[:duration] || 0.5); end
      def ring(**o);      add(:ring, check_points(o), o[:duration] || 0.6); end

      # a: / b: are { from:, color:, width: } (or just an actor id / point).
      def beam_clash(**o)
        [:a, :b].each do |k|
          raise ArgumentError, "beam_clash needs #{k}:" if !o[k]
          o[k] = { :from => o[k] } if !o[k].is_a?(Hash)
          check_point(o[k][:from])
        end
        w = o[:winner] || :both
        raise ArgumentError, "beam_clash winner: must be :a, :b, :both, :fizzle or :mash" if ![:a, :b, :both, :fizzle, :mash].include?(w)
        add(:beam_clash, o, o[:duration] || 6.0, true)
      end

      # Changes a running clash (id:) - white: 0..1 desaturates both beams.
      def clash_mod(id, **o); add(:clash_mod, o.merge(:id => id), o[:duration] || 1.0); end

      #-------------------------------------------------------------------------
      # Armies
      #-------------------------------------------------------------------------
      def army(id, **o)
        @ids[id] = :army
        add(:army, o.merge(:id => id))
      end

      def march(id, **o);  add(:march, o.merge(:id => ref(id, :army)), o[:duration] || 2.0); end
      def rout(id, **o);   add(:rout, o.merge(:id => ref(id, :army)), o[:duration] || 2.0); end
      def army_tint(id, **o); add(:army_tint, o.merge(:id => ref(id, :army)), o[:duration] || 1.0); end
      def army_fall(id, **o); add(:army_fall, o.merge(:id => ref(id, :army)), o[:duration] || 0.8); end

      def clash_armies(a, b, **o)
        add(:clash_armies, o.merge(:a => ref(a, :army), :b => ref(b, :army)), o[:duration] || 4.0, true)
      end

      def volley(**o); add(:volley, check_points(o), o[:duration] || 1.6, true); end

      private

      def run(&block)
        if block.arity == 1 then block.call(self)
        else instance_eval(&block)
        end
      end

      def block_end(finish)
        @definition.length = [@definition.length, finish].max
        if @mode == :par then @par_max = [@par_max, finish].max
        else @t = finish
        end
      end

      def add(op, args, dur = 0.0, blocking = false)
        args = args.dup
        blocking = args.delete(:wait) if args.has_key?(:wait)
        dur = dur.to_f
        @seq += 1
        @definition.events.push(Event.new(@t, dur, op, args, @seq))
        @definition.length = [@definition.length, @t + dur].max
        block_end(@t + dur) if blocking
        return nil
      end

      def tween(op, id, o, default)
        add(op, check_points(o).merge(:id => ref(id)), o[:duration] || default)
      end

      # Authoring check: ids must be declared before they are used.
      def ref(id, kind = nil)
        found = @ids[id]
        if !found || (kind && found != kind)
          raise ArgumentError, "Cutscene #{@definition.id.inspect}: unknown #{kind || 'actor'} #{id.inspect} (declare it first)"
        end
        return id
      end

      def check_point(spec)
        ref(spec) if spec.is_a?(Symbol)
        ref(spec[:actor]) if spec.is_a?(Hash) && spec[:actor]
        return spec
      end

      def check_points(o)
        [:to, :from, :at, :toward, :target].each { |k| check_point(o[k]) if o[k] }
        return o
      end
    end

    #---------------------------------------------------------------------------
    # Registry
    #---------------------------------------------------------------------------
    @blocks   = {}
    @options  = {}
    @playing  = false
    @skipped  = false
    @last_results = {}

    class << self
      attr_reader :last_results, :current     # current = the Scene being played, or nil

      # Registers a scene. options: skippable: (true), restore_bgm: (true),
      # vars: a proc returning default variables (evaluated at play time).
      # The block is built once now (with default vars) to catch mistakes early,
      # and again each time the scene plays.
      def define(id, **options, &block)
        raise ArgumentError, "Cutscene.define needs a block" if !block
        @blocks[id]  = block
        @options[id] = options
        build(id, **(options[:check_vars] || {})) if options[:check] != false
        return id
      end

      def block_for(id); return @blocks[id]; end
      def exists?(id);   return @blocks.has_key?(id); end
      def ids;           return @blocks.keys; end

      # Builds a Definition. With a block: an anonymous scene (id = label).
      def build(id = :ANONYMOUS, **vars, &block)
        blk = block || @blocks[id]
        raise ArgumentError, "Unknown cutscene #{id.inspect}" if !blk
        opts = (block) ? {} : (@options[id] || {})
        b = Builder.new(id, opts, vars)
        (blk.arity == 1) ? blk.call(b) : b.instance_eval(&blk)
        return b.definition.finish!
      end

      # Plays a scene (id or Definition). Returns true when it ran to the end,
      # false when it was skipped or could not run. Never softlocks an event:
      # outside Debug mode errors are logged and the scene ends.
      def play(id, **vars)
        return false if @playing
        @playing = true
        @skipped = false
        begin
          if id.is_a?(Definition)
            defn = id
          else
            raise ArgumentError, "Unknown cutscene #{id.inspect}" if !exists?(id)
            dv = @options[id][:vars]
            vars = dv.call.merge(vars) if dv
            defn = build(id, **vars)
          end
          scene = Scene.new(defn)
          @current = scene
          status = scene.play
          @last_results = scene.results
          @skipped = (status == :skipped)
          Scene.fade_back
          return !@skipped
        rescue StandardError => e
          Util.log("#{id.is_a?(Definition) ? id.id : id}: #{e.class}: #{e.message}\n#{(e.backtrace || [])[0, 6].join("\n")}")
          raise if $DEBUG || @raise_errors
          return false
        ensure
          @playing = false
          @current = nil
        end
      end

      attr_accessor :raise_errors

      def playing?;    return @playing; end
      def skipped?;    return @skipped; end
      def result(key); return @last_results[key]; end
    end
  end
end

# Short form for event Script commands.
def pbCutscene(id, **vars)
  return Prismfall::Cutscene.play(id, **vars)
end
