# A grid of ShapeNode cells that heat up where you touch, then cool down.
# Demonstrates subclassing ShapeNode (passing parent= through kwargs) and a
# distance-falloff touch effect. Drag a finger across the screen.
# Source: community Pythonista-Tools collection (Andrew4200/Pythonista).
from scene import *
from ui import Path
from colorsys import hsv_to_rgb

CELL = 48
COOL_HUE = 2 / 3  # blue
HOT_HUE = 1 / 6   # yellow


class Cell(ShapeNode):
    def __init__(self, i, j, **kwargs):
        self.heat = 0.0
        super().__init__(Path.rect(0, 0, CELL, CELL), 'white',
                         position=(i * CELL, j * CELL), **kwargs)

    def refresh(self):
        k = min(1.0, self.heat)
        self.fill_color = hsv_to_rgb(k * HOT_HUE + (1 - k) * COOL_HUE, 1, 1)


class TouchGrid(Scene):
    def setup(self):
        self.background_color = 'black'
        cols = int(self.size.w // CELL) + 1
        rows = int(self.size.h // CELL) + 1
        self.cells = [Cell(c, r, parent=self)
                      for r in range(rows) for c in range(cols)]

    def update(self):
        for cell in self.cells:
            if cell.heat > 0:
                cell.heat *= 0.96
                cell.refresh()

    def touch_began(self, touch):
        self._heat(touch.location)

    def touch_moved(self, touch):
        self._heat(touch.location)

    def _heat(self, loc):
        for cell in self.cells:
            d = abs(cell.frame.center() - loc)
            if d < CELL * 3:
                cell.heat += CELL / max(d * d, 1)
                cell.refresh()


run(TouchGrid())
