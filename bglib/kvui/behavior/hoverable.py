from kivy.core.window import Window
from kivy.properties import BooleanProperty


class HoverableBehavior:
    """
    :Properties:
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """
    is_hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return  # nothing to do if not on screen
        pos = args[1]
        # to_widget ensures compatibility with relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.is_hovered == inside:
            return  # no change
        self.is_hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass
