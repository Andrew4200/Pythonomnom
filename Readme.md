Pythonomnom

Pythonista-based simulations and visual systems built for iOS using the scene module.

This document defines the hard constraints, environment assumptions, and error-avoidance rules required for generating compatible code. It is written to maximize first-run success inside the Pythonista iOS sandbox.

⸻

1. Target Environment

Platform
	•	iOS
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