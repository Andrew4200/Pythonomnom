# MultiScene: one Scene that hosts swappable sub-scenes (menu -> game -> over).
# Forwards draw/update/touches/dt so sub-scenes behave like real scenes.
# Source: community Pythonista-Tools collection (Andrew4200/Pythonista).
from scene import *


class MultiScene(Scene):
    def __init__(self, start_scene):
        self.active_scene = start_scene

    def switch_scene(self, new_scene):
        self.active_scene = new_scene
        self._sync(new_scene)
        new_scene.setup()

    def _sync(self, sc):
        sc.size = self.size
        sc.bounds = self.bounds

    def setup(self):
        self._sync(self.active_scene)
        self.active_scene.setup()

    def draw(self):
        self.active_scene.touches = self.touches
        self.active_scene.draw()

    def update(self):
        sc = self.active_scene
        sc.dt = self.dt
        if hasattr(sc, 'update'):
            sc.update()

    def touch_began(self, touch):
        self._forward('touch_began', touch)

    def touch_moved(self, touch):
        self._forward('touch_moved', touch)

    def touch_ended(self, touch):
        self._forward('touch_ended', touch)

    def _forward(self, name, touch):
        handler = getattr(self.active_scene, name, None)
        if handler is not None:
            handler(touch)


class Menu(Scene):
    def setup(self):
        self.background_color = (0.06, 0.20, 0.38)
        LabelNode('Tap to play', font=('Helvetica', 36),
                  position=self.size / 2, parent=self)

    def touch_ended(self, touch):
        main_scene.switch_scene(Game())


class Game(Scene):
    def setup(self):
        self.background_color = (0.09, 0.13, 0.24)
        self.t = 0.0
        self.label = LabelNode('Playing... tap to finish', font=('Helvetica', 28),
                               position=self.size / 2, parent=self)

    def update(self):
        self.t += self.dt
        self.label.text = 'Playing... {:.1f}s (tap to finish)'.format(self.t)

    def touch_ended(self, touch):
        main_scene.switch_scene(Menu())


main_scene = MultiScene(Menu())
run(main_scene)
