# MultiScene: one Scene that hosts swappable sub-scenes.
#
# Menu -> Game -> Menu
#
# Pythonista scene-module safe version:
#   - Does NOT call child.draw()
#   - Uses the normal Node rendering system
#   - Does NOT assign Scene.bounds (read-only)
#   - Forwards update/touch events
#   - Keeps the active scene's nodes under the host scene

from scene import *


class MultiScene(Scene):

    def __init__(self, start_scene):
        super().__init__()
        self.active_scene = None
        self.active_nodes = []
        self.switch_scene(start_scene)

    def setup(self):
        # setup() may be called after __init__, so make sure the
        # currently active scene has the correct size.
        if self.active_scene is not None:
            self._sync(self.active_scene)

    def _sync(self, sc):
        sc.size = self.size
        # Do NOT assign sc.bounds.
        # bounds is read-only and derived from size.

    def switch_scene(self, new_scene):

        # Remove the previous scene's nodes from the host.
        for node in self.active_nodes:
            node.remove_from_parent()

        self.active_nodes = []
        self.active_scene = new_scene

        # Give the new scene the host's dimensions.
        self._sync(new_scene)

        # Build the new scene's contents.
        new_scene.setup()

        # Move its nodes into the actual scene being rendered.
        for node in list(new_scene.children):
            node.remove_from_parent()
            self.add_child(node)
            self.active_nodes.append(node)

        # The host scene controls the actual background.
        self.background_color = new_scene.background_color

    def update(self):
        sc = self.active_scene

        if sc is None:
            return

        # Forward the host's frame timing.
        sc.dt = self.dt

        # Forward update logic.
        sc.update()

    def touch_began(self, touch):
        self._forward('touch_began', touch)

    def touch_moved(self, touch):
        self._forward('touch_moved', touch)

    def touch_ended(self, touch):
        self._forward('touch_ended', touch)

    def _forward(self, name, touch):
        sc = self.active_scene

        if sc is None:
            return

        handler = getattr(sc, name, None)

        if handler is not None:
            handler(touch)


class Menu(Scene):

    def setup(self):
        self.background_color = (0.06, 0.20, 0.38)

        LabelNode(
            'Tap to play',
            font=('Helvetica', 36),
            position=self.size / 2,
            parent=self
        )

    def touch_ended(self, touch):
        main_scene.switch_scene(Game())


class Game(Scene):

    def setup(self):
        self.background_color = (0.09, 0.13, 0.24)

        self.t = 0.0

        self.label = LabelNode(
            'Playing... tap to finish',
            font=('Helvetica', 28),
            position=self.size / 2,
            parent=self
        )

    def update(self):
        self.t += self.dt

        self.label.text = (
            'Playing... {:.1f}s (tap to finish)'
            .format(self.t)
        )

    def touch_ended(self, touch):
        main_scene.switch_scene(Menu())


main_scene = MultiScene(Menu())

run(main_scene)
