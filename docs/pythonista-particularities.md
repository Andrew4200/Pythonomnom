# Pythonista Particularities

The 12 minimal rules for building stable visual systems in Pythonista 3.
Companion to `../Readme.md`: the Readme is the enforceable contract for generated code;
this is the reasoning behind it.

## 1. Respect the engine (don't fight it)

Pythonista is not a game engine. It's a constrained renderer.

- No external libs, no advanced rendering, no safety nets
- Anything "clever" usually breaks or stutters

**Rule:** If there's a built-in way → use it. If not → simplify the idea, don't emulate complexity.

## 2. Prefer stable primitives

Rendering stability hierarchy:

```
SpriteNode > ShapeNode > ui.Path > canvas
```

- `SpriteNode` is safest (texture-based)
- `ShapeNode` is acceptable
- `ui.Path` = structure only (no color)
- `canvas` = last resort, crash-prone

**Rule:** Default to `SpriteNode` unless you have a clear reason not to.

## 3. State must exist before use (lifecycle rule)

Scene lifecycle is non-deterministic early on.

- `update()` may run before `setup()` completes
- Missing attributes = crash

**Rule:** Everything used in `update()` must be initialized first (in `setup()`).

## 4. Be explicit with math (never trust helpers)

`Vector2` is unreliable.

**Rule:** Always do manual math:

```python
mag = (v.x * v.x + v.y * v.y) ** 0.5
nx, ny = (v.x / mag, v.y / mag) if mag else (0, 0)
```

No hidden helpers. No assumptions.

## 5. Node hierarchy is absolute

Positions are relative, not global.

- Child position ≠ world position
- Must convert manually

**Rule:**

```python
local = world - parent.position
```

(`Node.point_to_scene()` / `point_from_scene()` also exist — see `scene-api-reference.md`.)

Skip this and layout bugs will be subtle and persistent.

## 6. Use the engine's animation system

Manual animation loops = jitter + complexity.

- Use `Action` for movement, fade, removal

**Rule:** If something changes over time → it should probably be an `Action`.

## 7. Colors and rendering are strict

Rendering errors often appear later, not at assignment.

- Use tuples `(r, g, b[, a])`
- Never color `ui.Path`
- Alpha overwrites silently

**Rule:** Treat rendering like a strict type system.

## 8. Minimize dynamic complexity

Pythonista breaks under:

- frequent UI updates
- many ShapeNodes
- constant creation/destruction

**Rule:**

- Reuse objects (pooling)
- Separate static vs dynamic elements
- Avoid "live UI" (health bars, etc.)

## 9. Design for frame-based reality

There is:

- no tweening system
- no animation chaining
- no high-level timing model

**Rule:** Everything is:

```python
state += velocity * dt
```

If you need easing → implement it manually or fake it with `Action`s.

## 10. Avoid known footguns

These cause disproportionate bugs:

- naming an attribute `size`
- passing alignment positionally to `text()`
- assuming `ShapeNode` constructor args (e.g. `line_width`)
- relying on `Vector2` methods

**Rule:** Assume API inconsistencies unless proven otherwise.

## 11. Single-script mental model

- No modular architecture
- No imports beyond the sandbox

**Rule:** Flatten complexity:

- fewer abstractions
- clearer flow
- explicit ownership of state

## 12. When in doubt: reduce

Most failures come from overbuilding.

If something feels dynamic, reactive, UI-heavy, or "engine-like" → it's probably a bad idea in this environment.

## The core meta-rule

If you compress everything into one line: **stability over cleverness.** Every shortcut the
engine offers exists because the manual alternative has already broken someone's scene.
