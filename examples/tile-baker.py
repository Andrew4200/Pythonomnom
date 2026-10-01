# Bake a composed ShapeNode group into ONE texture, then stamp it many times.
# Every sprite below shares a single texture: O(1) texture memory for O(N) tiles.
# (Community-measured cost of the naive one-texture-per-tile way: ~280 KB each,
# ~235 MB for a 29x29 map.)
# Source: technique from the Pythonista-Tools collection (Andrew4200/Pythonista).
from scene import *
import ui

TILE = 96


def make_tile_texture():
    tile = Node()  # compose off-screen...
    s = TILE / 2
    base = ui.Path()  # diamond base
    base.move_to(0, -s)
    base.line_to(s, 0)
    base.line_to(0, s)
    base.line_to(-s, 0)
    base.close()
    ShapeNode(base, fill_color=(0.18, 0.55, 0.34), parent=tile)
    q = s * 0.55  # inset diamond
    inner = ui.Path()
    inner.move_to(0, -q)
    inner.line_to(q, 0)
    inner.line_to(0, q)
    inner.line_to(-q, 0)
    inner.close()
    ShapeNode(inner, fill_color=(0.25, 0.70, 0.42), parent=tile)
    rivet = ui.Path.oval(-8, -8, 16, 16)
    ShapeNode(rivet, fill_color=(1.0, 0.84, 0.0), parent=tile)
    return tile.render_to_texture()  # ...bake once


class TileField(Scene):
    def setup(self):
        self.background_color = (0.10, 0.10, 0.18)
        texture = make_tile_texture()
        cols = int(self.size.w // TILE) + 2
        rows = int(self.size.h // (TILE * 0.75)) + 2
        for r in range(rows):
            for c in range(cols):
                x = c * TILE + (TILE / 2 if r % 2 else 0)
                y = r * TILE * 0.75
                SpriteNode(texture=texture, position=(x, y), parent=self)


run(TileField())
