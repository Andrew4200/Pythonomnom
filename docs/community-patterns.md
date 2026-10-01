# Community Patterns

Battle-tested idioms mined from the Pythonista-Tools script collection
(`Andrew4200/Pythonista`: ~130 topic folders of community scripts). Surveyed
`scenes/`, `games/`, and `shader/`; file names below are paths in that repo.

**Heads-up:** much of the collection predates the Node/Action rewrite and even
Python 3. Patterns are split into *portable* (use freely) and *legacy* (do not
use in new code) — check which side you're on before copying.

## Portable patterns

### Entity objects: `update(dt)` + `draw()` + `bbox()`

The clean structure, seen in `games/Breakout_Clone.py` and `games/SpaceShooter.py`:

```python
class Ball:
    def update(self, dt): ...
    def draw(self): ...
    def bbox(self): return Rect(...)

class Game(Scene):
    def setup(self):
        self.ball = Ball()
    def draw(self):
        self.ball.update(self.dt)
        self.ball.draw()
```

The anti-pattern is `games/Pong.py`: module-level `global` state mutated from
`draw()`. Prefer entities owned by the scene.

### Removal sets — never mutate a list mid-iteration

Collect the dead, remove after the loop (`games/SpaceShooter.py`,
`games/Breakout_Clone.py`, `scenes/a-Particollision.py`):

```python
removed = set()
for bullet in self.bullets:
    bullet.update()
    if bullet.y > self.size.h:
        removed.add(bullet)
for bullet in removed:
    self.bullets.remove(bullet)
```

### Object pooling for particles

`scenes/confetti.py` recycles dead particles instead of constructing new ones —
exactly the "reuse objects" rule from `pythonista-particularities.md`:

```python
def touch_moved(self, touch):
    if self.dead:
        particle = self.dead.pop()
        particle.__init__(touch.location)   # re-init in place
    else:
        particle = Particle(touch.location)
        self.particles.append(particle)
```

### Scene switching: the MultiScene wrapper

`scenes/Multi-Scene.py` — a `Scene` subclass that forwards everything to an
active sub-scene. Gives you menu → game → game-over without modal complexity:

```python
class MultiScene(Scene):
    def __init__(self, start_scene):
        self.active_scene = start_scene
    def switch_scene(self, new_scene):
        self.active_scene = new_scene
        new_scene.setup()
    def draw(self):
        self.active_scene.draw()
    def touch_began(self, touch):
        self.active_scene.touch_began(touch)
    # ... forward touch_moved / touch_ended the same way

main_scene = MultiScene(Scene1())
run(main_scene)
```

`games/Breakout_Clone.py` extends this by also forwarding `dt` and `touches`
to the active scene each frame — needed once sub-scenes use `update()`.

### Modal overlays for menus

`scenes/SceneTransition.py` — the built-in way, no wrapper needed:

```python
self.present_modal_scene(OverlayScene())  # overlay gets all touches
# inside the overlay:
self.dismiss_modal_scene()
```

### Multitouch state keyed by `touch_id`

`scenes/Touch Colors.py` — the canonical pattern, with cleanup:

```python
def setup(self):
    self.touch_colors = {}
def touch_began(self, touch):
    self.touch_colors[touch.touch_id] = hsv_to_rgb(random(), 1, 1)
def touch_ended(self, touch):
    del self.touch_colors[touch.touch_id]
def draw(self):
    for touch in self.touches.values():
        r, g, b = self.touch_colors[touch.touch_id]
        ...
```

Related: `touch.prev_location` gives drag deltas for paddle-style dragging
(`games/Pong.py`).

### Collision: `Rect.intersects()` + side sub-rects

`games/Breakout_Clone.py` builds thin rects for each block edge
(`self.left`, `self.right`, `self.top`, `self.bottom`) and tests them in order
to get bounce direction right — cheaper and more robust than corner math.
For point tests: `Point(x, y) in rect` (`games/SpaceShooter.py`).

### Bake ShapeNode groups with `render_to_texture()`

From the forum thread embedded in
`scenes/2-problems-with-shape-nodes-and-sprite-nodes.py`: composing each tile
from ShapeNodes and baking each to its own texture cost ~280 KB/tile →
~235 MB for a 29×29 map. The fix:

```python
tile = Node(position=position)          # compose faces as children...
left = ShapeNode(left_path, fill_color='#3fb427', parent=tile)
# ...
sprite = SpriteNode(texture=tile.render_to_texture())  # ...bake once
```

And reuse: identical pieces share one texture instead of one texture per tile.

### Pre-bake animation frames; never decode per frame

`scenes/animating-gifs-in-pythonista-scene.py` decodes a GIF frame and writes
`tmp.png` to disk **every frame** — the slow way. Pre-render frames to
`Texture` objects in `setup()` and swap `sprite.texture` in `update()`.

### Subclassing ShapeNode

`shader/shader.py` (a ShapeNode grid, despite the folder name):

```python
class Cell(ShapeNode):
    def __init__(self, i, j, **kwargs):
        super().__init__(Path.rect(0, 0, S, S), 'white',
                         position=(i * S, j * S), **kwargs)
# parent= passes through kwargs:
Cell(i, j, parent=self)
```

Touch falloff trick from the same file: `S / abs(cell.frame.center() - touch.location) ** 2`.

### Draw-mode state discipline

- `tint(...)` persists — always reset with `tint(1, 1, 1)` / `no_tint()` after
  tinted drawing (`games/SpaceShooter.py`).
- `push_matrix()` / `translate()` / `rotate()` / `pop_matrix()` for rotated
  sprites and shapes (`scenes/confetti.py`, `games/SpaceShooter.py`).

### Tilt control

`gravity().x * k`, clamped to screen bounds — paddle in
`games/Breakout_Clone.py`, ship in `games/SpaceShooter.py`:

```python
self.rect.x += gravity().x * 50
self.rect.x = min(self.size.w - 100, max(0, self.rect.x))
```

### Fire-rate limiting

`if self.frame_count % 12 == 0: self.fire()` (`games/SpaceShooter.py`) —
simple frame-counter gating, no timers needed.

### Perf debugging

`run(MyScene(), show_fps=True)` appears across the collection; the `SceneView`
equivalent is `shows_fps`. Use it before optimizing.

### Never hardcode the screen size

`games/Pong.py` hardcodes `Size(768, 1024)` — breaks on any other device.
`games/Breakout_Clone.py` does it right: `screen_size = self.size` in `setup()`,
then relative layout everywhere. This matches the constraints doc.

## Performance numbers (community-measured)

- ~3,000 nodes ran at roughly 40 fps on an iPad Air 2
  (`scenes/2-problems-with-shape-nodes-and-sprite-nodes.py` thread). Keep node
  counts modest; bake and reuse textures.
- ~50 particles with Python-level O(n²) circle hit-testing visibly lagged
  (`scenes/a-Particollision.py`). Beyond that, use spatial partitioning or move
  collision to fewer, coarser checks.

## Legacy — do not use in new code

- **`Layer`, `TextLayer`, `layer.animate(...)`, `curve_*`** (`games/SpaceShooter.py`
  is full of these). Superseded by Node/Action; kept only for backwards
  compatibility.
- **`should_rotate()`** — old API; rotation/orientation is handled via `run()`
  arguments and `did_change_size()` now.
- **Python 2-isms** (`xrange`, unparenthesized `print`) — many scripts predate
  Python 3. Modernize on sight.
- **`self.delay(seconds, fn)`** with `functools.partial` (`games/SpaceShooter.py`)
  is handy for timed callbacks, but confirm it exists in your Pythonista build
  before using — it comes from the older API surface.
- Heavy **draw-mode** games (Pong, Breakout, SpaceShooter, the particle demos)
  predate the Node rewrite. Draw mode is still legitimate for simple sketches,
  but node-based scenes perform significantly better.
