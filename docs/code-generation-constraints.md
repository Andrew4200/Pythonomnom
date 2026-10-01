Pythonomnom

Pythonista-based simulations and visual systems built for iOS using the scene module.

This document defines the hard constraints, environment assumptions, and error-avoidance rules required for generating compatible code. It is written to maximize first-run success inside the Pythonista iOS sandbox.

⸻

1. Target Environment

Platform
	•	iOS
•	iPhone 15 Pro Max
	•	Pythonista 3
	•	Sandboxed runtime
	•	No arbitrary pip installs

Python Version
	•	Python 3.x (bundled interpreter inside Pythonista)

Primary Framework
	•	scene module
	•	ui (only when necessary)

Only bundled modules may be used. No external dependencies.

⸻

2. Target Device Dimensions

Assume portrait orientation.

Logical resolution:

Size(430.00, 932.00)

	•	Width: 430
	•	Height: 932
	•	Origin: bottom-left
	•	Y-axis increases upward

All layout and UI elements must respect these bounds.

Avoid placing interactive UI within ~40px of the top edge.

Prefer relative positioning:

x = self.size.w * 0.5
y = self.size.h * 0.9


⸻

3. Scene Lifecycle Rules (Critical)
	•	Scene.update(self) takes no parameters
	•	Use self.dt for delta time
	•	Always initialize all critical attributes inside setup()
	•	update() may execute before all nodes are fully constructed
	•	If a Scene subclass defines __init__, it must call super().__init__() —
	  otherwise Scene never sets up internal state (e.g. fixed_time_step) and
	  the runtime crashes with AttributeError inside scene._draw.

Safe pattern:

def setup(self):
    self.node = None
    self.build_scene()

def update(self):
    if self.node:
        ...

Never rely on construction order guarantees.

⸻

4. Color System Rules (Critical)

ShapeNode / UI
	•	NEVER pass scene.Color into ShapeNode
	•	ALWAYS use tuples: (r, g, b) or (r, g, b, a)
	•	Color errors often surface at draw-time via ui.set_color

Correct:

node.fill_color = (1, 0, 0, 1)

Incorrect:

node.fill_color = Color(1, 0, 0)

Background

Scene.background_color may accept:
	•	Tuple
	•	scene.Color

Prefer tuples for consistency.

⸻

5. Vector Math Rules

scene.Vector2 methods are unreliable.

Do NOT use:
	•	.length()
	•	.normalized()

Always implement explicit math helpers:

import math

def mag(x, y):
    return math.sqrt(x*x + y*y)

def normalize(x, y):
    m = mag(x, y)
    return (x/m, y/m) if m else (0, 0)

Prefer explicit x/y arithmetic over undocumented behavior.

⸻

6. ShapeNode Constraints
	•	line_width cannot be passed in the constructor
	•	Must set after initialization

Correct:

n = ShapeNode(path)
n.line_width = 2

Prefer SpriteNode over ShapeNode when possible for stability.

⸻

7. UI and Drawing Stability
	•	Avoid heavy redraw loops using canvas
	•	Prefer SpriteNode or ShapeNode
	•	ui.Path does not store color — color belongs to ShapeNode
	•	Reassigning alpha repeatedly overrides previous values silently

Canvas is fragile and should be a last resort.

⸻

8. Known Error Corrections

scene.text()

Correct signature:

text(string, x, y, alignment=...)

Never pass alignment positionally.

⸻

update(self, dt)

Incorrect:

def update(self, dt):
    ...

Correct:

def update(self):
    dt = self.dt


⸻

AttributeError Race Conditions

Always initialize attributes in setup() before referencing them in update().

Example:

def setup(self):
    self.needle = None

Guard usage:

if self.needle:
    ...


⸻

scene.Color in ShapeNode

Replace with tuple color.

⸻

Vector2.length()

Replace with explicit math helper functions.

⸻

9. Coordinate System
	•	Child nodes use local coordinates relative to parent
	•	World → local conversions must be explicit
	•	No implicit coordinate transforms occur

Be careful when nesting nodes.

⸻

10. Performance Guidelines
	•	Limit total node count
	•	Avoid creating objects inside update()
	•	Prefer mutation over re-instantiation
	•	Avoid large texture generation loops
	•	Keep systems deterministic
	•	Avoid timing-dependent race bugs
	•	Avoid hidden state

⸻

11. File Requirements

All returned scripts must:
	•	Run immediately when pasted into Pythonista
	•	Contain all helper functions
	•	Avoid undefined globals
	•	Avoid unused variables
	•	Avoid shadowing built-ins (e.g., size)
	•	Contain no missing references
	•	Be self-contained

No partial snippets unless explicitly requested.

⸻

12. Sandbox Constraints
	•	No pip installs
	•	Only bundled modules allowed
	•	No filesystem assumptions outside app sandbox
	•	Avoid background threads unless essential
	•	No external network dependency unless explicitly required

⸻

13. Preferred Visual Stack (Priority Order)
	1.	SpriteNode
	2.	ShapeNode
	3.	ui (only when required)
	4.	canvas (last resort)

⸻

14. Pre-Return Stability Checklist

Before finalizing any script:
	•	No scene.Color used in ShapeNode
	•	update() has no parameters
	•	All attributes initialized before use
	•	No reliance on Vector2 methods
	•	No constructor line_width usage
	•	No missing helper functions
	•	Script runs standalone
	•	Layout fits 430x932 portrait bounds

⸻

15. Design Philosophy

This repository prioritizes:
	•	Agent-based simulations
	•	Visual systems
	•	Deterministic behavior
	•	Explicit state management
	•	Debuggability
	•	Minimal hidden state
	•	Stability over cleverness

All generated code must optimize for reliability and first-run correctness within the Pythonista iOS environment.

⸻

16. Anti-patterns (wrong → failure → right)

Each pair below is a real bug class. Prefer the RIGHT form every time.

**update() with a parameter**
```python
# WRONG — TypeError: update() takes 2 positional arguments (scene calls it with none)
def update(self, dt):
    self.position += self.velocity * dt
# RIGHT — frame delta lives on self.dt
def update(self):
    self.position += self.velocity * self.dt
```

**Scene subclass __init__ without super().__init__()**
```python
# WRONG — AttributeError: 'MultiScene' object has no attribute 'fixed_time_step'
# (crashed on-device; Scene.__init__ sets up fixed_time_step, view, etc.)
class MultiScene(Scene):
    def __init__(self, start_scene):
        self.active_scene = start_scene
# RIGHT
class MultiScene(Scene):
    def __init__(self, start_scene):
        super().__init__()
        self.active_scene = start_scene
```

**Vector2 convenience methods**
```python
# WRONG — Vector2.length() / .normalized() are unreliable in Pythonista's scene
speed = v.length()
direction = v.normalized()
# RIGHT — explicit math
import math
speed = math.hypot(v.x, v.y)
direction = Vector2(v.x / speed, v.y / speed) if speed else Vector2(0, 0)
```

**scene.Color for node colors**
```python
# WRONG
node.color = scene.Color(1, 0, 0, 1)
# RIGHT — plain tuples
node.color = (1, 0, 0, 1)
```

**ShapeNode line_width in the constructor**
```python
# WRONG — silently ignored / unstable
node = ShapeNode(path, fill_color=(1, 1, 1, 1), line_width=3)
# RIGHT — set after initialization
node = ShapeNode(path, fill_color=(1, 1, 1, 1))
node.line_width = 3
```

**Guessing APIs from desktop Python or memory**
```python
# WRONG — NameError at runtime (triangle() does not exist in scene)
triangle(...)
# RIGHT — only call what the API references document; when unsure, check
# docs/scene-api-reference.md and docs/sound-api-reference.md first
```

**Reaching for pip / installs**
```python
# WRONG — any install step (pip, StaSh, manual download) in generated code
# RIGHT — bundled modules only; the script must be paste-and-run as a single file
```
