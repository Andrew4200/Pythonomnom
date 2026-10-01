# scene Module API Reference

Condensed from the Pythonista 3.4 `scene` module documentation. Companion to
`../Readme.md` (hard constraints) and `pythonista-particularities.md` (design rules).

## Quick start

```python
from scene import *

class MyScene(Scene):
    def setup(self):
        self.background_color = 'midnightblue'
        self.ship = SpriteNode('spc:PlayerShip1Orange')
        self.ship.position = self.size / 2
        self.add_child(self.ship)

run(MyScene())
```

- Every scene subclasses `Scene`, which is itself a `Node`. Nodes form a scene graph.
- `run(MyScene())` presents fullscreen. `run(MyScene(), PORTRAIT)` locks orientation.
- SpriteNode image names can be built-in images (browse with the `[+]` button in the editor).

## Frame loop order

Each frame the scene processes, in order:

1. `update()` is called
2. Actions on children are evaluated
3. `did_evaluate_actions()` is called
4. All nodes are rendered

## Scene methods

| Method | Notes |
|---|---|
| `setup()` | Called once, just before the scene is presented. `size`/`bounds` are valid here. |
| `update()` | Called 60×/sec while presented. **Takes no parameters** — use `self.dt`. |
| `draw()` | Classic render-loop mode only (see below). |
| `touch_began(touch)` / `touch_moved(touch)` / `touch_ended(touch)` | Touch events. `touch.location` is in scene coordinates; `touch.touch_id` distinguishes simultaneous touches. |
| `did_change_size()` | Called on rotation; `size` already holds the new value. Reposition content here. |
| `did_evaluate_actions()` | Called after children's actions finish each frame. |
| `pause()` / `resume()` / `stop()` | Auto-called on home button / resume / close ("×"). Override to save state. |
| `should_rotate()` | Called to decide auto-rotation; return `False` to lock orientation. |
| `present_modal_scene(other)` | Overlay a scene (menus). It receives all touches. |
| `dismiss_modal_scene()` | Close a modally presented scene. |
| `controller_changed(key, value)` | MFi controller events, e.g. `'button_a'` → bool, `'thumbstick_left'` → Point(-1..1). |

## Scene attributes

| Attribute | Notes |
|---|---|
| `dt` | Seconds since last `update()`. Drive custom animation with this. |
| `t` | Seconds since the scene started. |
| `size` | Drawable area dimensions (read-only). |
| `bounds` | `Rect` with origin (0,0) and the drawable size. |
| `touches` | Dict of active touches, keyed by `touch_id`. |
| `background_color` | Accepts tuple, `scene.Color`, hex string, or CSS name. Default dark gray. |
| `view` | The presenting view (read-only, may be `None`). |
| `presented_scene` / `presenting_scene` | Modal scene relationships. |

## Node

The fundamental building block. The base `Node` draws nothing; subclasses do.

```python
Node(position=(0, 0), z_position=0.0, scale=1.0, x_scale=1.0, y_scale=1.0,
     alpha=1.0, speed=1.0, parent=None)
```

| Method | Notes |
|---|---|
| `add_child(node)` | Appends to the child list. |
| `remove_from_parent()` | Detaches the node. |
| `run_action(action[, key])` | Starts an action. Same `key` replaces a running action. |
| `remove_action(key)` / `remove_all_actions()` | Stops actions; prior changes are **not** reverted. |
| `render_to_texture([crop_rect])` | Snapshot of the node + children as a `Texture`. |
| `point_to_scene(point)` / `point_from_scene(point)` | Convert between node-local and scene coordinates. Raises `ValueError` if the node isn't in a scene. |

Key attributes: `position` (in **parent's** coordinates), `z_position` (draw order; larger = front),
`scale` / `x_scale` / `y_scale`, `alpha` (multiplies down the subtree), `rotation` (radians, CCW),
`speed` (action speed multiplier), `paused`, `parent` (read-only), `children` (read-only list —
mutating it does nothing), `scene` (read-only), `frame` (read-only content rect in parent
coordinates), `bbox` (content + descendants rect in parent coordinates).

## SpriteNode

```python
SpriteNode(texture, position=(0, 0), z_position=0.0, scale=1.0, x_scale=1.0,
           y_scale=1.0, alpha=1.0, speed=1.0, parent=None, size=None,
           color='white', blend_mode=0)
```

- `texture`: a `Texture`, a built-in image name (`'spc:PlayerShip1Orange'`), or a file path.
  `None` → drawn as a colored rectangle using `color`.
- `color`: tints the texture. **Use tuples** — never `scene.Color` on nodes (see Readme).
- `anchor_point`: which point of the sprite sits at `position`, in unit space. Default `(0.5, 0.5)` = centered.
- `size`: auto-set from the texture when assigned.
- `blend_mode`: `BLEND_NORMAL` (default), `BLEND_ADD`, `BLEND_MULTIPLY`.
- `shader`: attach a `Shader` for custom GPU rendering.

## EffectNode

Post-processing for its children: renders them to a private framebuffer, then blends it back.

- `crop_rect`: region of children to render. Auto-derived by default; set explicitly if children change size often or go off-screen (perf).
- `blend_mode`, `shader`: as SpriteNode.
- `effects_enabled`: `False` → renders as a plain `Node`. Default `True`, except `Scene` sets it `False`.

## LabelNode

```python
LabelNode(text, font=('Helvetica', 20), *args, **kwargs)
```

A `SpriteNode` that rasterizes a string. Setting `text` or `font` regenerates the texture
automatically. Text is centered on `position` by default; adjust `anchor_point` to change that.

## ShapeNode

```python
ShapeNode(path=None, fill_color='white', stroke_color='clear', shadow=None, *args, **kwargs)
```

Renders a `ui.Path`. Attributes: `path`, `fill_color`, `stroke_color`,
`shadow` as `(color, x_offset, y_offset, radius)` or `None`.

**Repo gotchas** (enforced by `../Readme.md`):
- `line_width` lives on `ui.Path` and **cannot** be passed to the constructor — set it after init.
- Colors must be tuples, never `scene.Color`.

## SceneView

Subclass of `ui.View` that hosts a scene and runs the render loop. `run()` creates one implicitly.

- `scene`: the presented scene. Empty view until set.
- `paused`: pause the loop.
- `frame_interval`: `1` = 60 fps (default); `2` = 30 fps. Passable to `run()` too.
- `anti_alias`: 4× multisampling. Real perf cost; off by default.
- `shows_fps`: debug framerate overlay.
- Shows stdout/exceptions in a status line at the bottom — `print()` debugging works fullscreen.

## Action

High-level animation API. Prefer over manual per-frame animation.

```python
move = Action.move_to(x, y, 0.7, TIMING_SINODIAL)
self.ship.run_action(move)

laser.run_action(Action.sequence(Action.move_by(0, 1000), Action.remove()))
```

- Factories: `move_to`, `move_by`, plus rotate/scale/fade variants; `sequence(...)`, `group(...)`, `repeat(action)`; `remove()` (removes the node — not an animation, but sequencable).
- Timing modes: `TIMING_LINEAR` (default), `TIMING_SINODIAL`, `TIMING_EASE_IN_OUT`, etc.

## Shader

Custom GLSL fragment shader for `SpriteNode`/`EffectNode`.

Automatically provided (declare them to use them):

| Name | Type | Meaning |
|---|---|---|
| `u_time` | float | Scene animation timestamp |
| `u_sprite_size` | vec2 | Sprite size in points |
| `u_scale` | float | Screen scale (retina ≈ 2.0) |
| `u_texture` | sampler2D | Sprite texture (children render for EffectNode) |
| `u_tint_color` | vec4 | Premultiplied sprite color |
| `u_fill_color` | vec4 | Used when the sprite has no texture |
| `v_tex_coord` | vec2 (varying) | Current UV coordinates |

- `Shader.set_uniform(name, value)`: float/vec2/vec3/vec4 or `Texture` for samplers.
- `Shader.get_uniform(name)`: float/vector uniforms only; `None` for bad names.

Minimal example (ripple around touch):

```python
ripple = '''
precision highp float;
varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
void main(void) {
    vec2 p = -1.0 + 2.0 * v_tex_coord + (u_offset / u_sprite_size * 2.0);
    float len = length(p);
    vec2 uv = v_tex_coord + (p/len) * 1.5 * cos(len*50.0 - u_time*10.0) * 0.03;
    gl_FragColor = texture2D(u_texture, uv);
}
'''
sprite.shader = Shader(ripple)
# later: sprite.shader.set_uniform('u_offset', (dx, dy))
```

## Geometry

- Origin `(0, 0)` is the **bottom-left**; y increases upward.
- `Vector2`, `Point`, `Size` support `+ - * /` (scalar or component-wise). Assigning any 2-sequence works where a Point/Size is expected.
- `point[0]` / `point.x` both work.
- Hit-testing: `point in rect`; `Rect.intersects(other)`; `Rect.intersection(other)`.
- **Repo rule:** don't rely on `Vector2.length()` / `.normalized()` — write explicit helpers.

## Colors

Accepted forms: `'#ff0000'`, `'green'` (CSS names), `(r, g, b[, a])` floats 0–1 (alpha defaults 1.0),
or a single 0–1 float for grayscale. Reading any color attribute back always yields a 4-tuple.

## Module functions

| Function | Returns |
|---|---|
| `gravity()` | `(x, y, z)` device orientation |
| `get_screen_size()` | `Size` |
| `get_screen_scale()` | scale factor |
| `get_image_path(name)` | path to a built-in image |
| `get_controllers()` | list of connected controller states |

## Constants

- Orientations: `DEFAULT_ORIENTATION`, `PORTRAIT`, `LANDSCAPE`
- Blend modes: `BLEND_NORMAL`, `BLEND_ADD`, `BLEND_MULTIPLY`
- Filtering: `FILTERING_LINEAR`, `FILTERING_NEAREST`
- Timing: `TIMING_LINEAR`, `TIMING_SINODIAL`, `TIMING_EASE_IN_OUT`, …

## ui integration

- Build a `SceneView` explicitly, set its `.scene`, and embed it in a `ui` hierarchy for non-fullscreen scenes.
- A presented scene's auto-created view is available as `scene.view` — add `ui` controls (e.g. text fields) to it.
- `Texture` can be built from a `ui.Image` (typically rendered via `ui.ImageContext`) — this is how `ShapeNode`/`LabelNode` rasterize.

## Classic render loop

Override `draw()` instead of using nodes; called every frame, starting from a blank screen each time:

```python
class MyScene(Scene):
    def draw(self):
        background('gray')
        fill('red')
        rect(-50, -50, 100, 100)

run(MyScene())
```

Uses `scene_drawing` functions (`background`, `fill`, `rect`, `translate`, `rotate`, …).
Node-based scenes perform significantly better; the classic loop suits Processing-style sketches.
