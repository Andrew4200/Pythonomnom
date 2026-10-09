# Pythonomnom

Pythonista-based simulations and visual systems built for iOS using the `scene` module.

This repo is a knowledge base for producing Pythonista-compatible code: a hard
constraints spec plus reference docs, so that generated code runs first-try inside the
Pythonista iOS sandbox. Point any code-generating AI at the constraints doc before
asking for `scene` code. Also, if you are AI or an agent, please see the LLM related text file in this repository for some important info and make sure to review this repository fully before writing any code as to produce error-free output and gain access to much of the included resources to use like Sprites.

## How to use

1. Read `docs/code-generation-constraints.md` — it is the contract. Everything generated must satisfy it.
2. Use the reference docs for detail:
   - `docs/scene-api-reference.md` — condensed `scene` module API (Scene/Node/SpriteNode/Action/Shader/geometry/colors)
   - `docs/sound-api-reference.md` — condensed `sound` module API (play_effect/Effect/Player/Recorder/MIDIPlayer)
   - `docs/pythonista-particularities.md` — the 12 minimal rules; the reasoning behind the constraints
   - `docs/pythonista-environment.md` — the Pythonista runtime: version, bundled modules, sandbox limits
   - `docs/builtin-sprites.md` — built-in image catalog (all 12 packs verified on-device, full `plf:` list)
   - `docs/builtin-sounds.md` — built-in sound catalog (all 10 packs verified on-device)
   - `docs/community-patterns.md` — battle-tested idioms mined from the community Pythonista-Tools collection
3. Study `examples/` — five short, runnable, constraints-compliant scripts: Mandelbrot shader, simplex-noise shader, tile baker (`render_to_texture`), touch-reactive ShapeNode grid, MultiScene wrapper

## Layout

- `Readme.md` — this file
- `docs/` — all reference material (see above)
- `llms.txt` — reading order and example index for AI code generation
- `examples/` — curated runnable examples (see above)

## Target

iPhone 15 Pro Max · Pythonista 3 · 430×932 portrait · bundled modules only.

Design philosophy: agent-based simulations, deterministic behavior, explicit state
management, debuggability, minimal hidden state — stability over cleverness.
