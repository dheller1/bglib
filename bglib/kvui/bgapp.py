from kivy.app import App
from kivy.core.window import Window
from bglib.kvui.rootwidget import RootWidget


class BgApp(App):
    WindowSize = (1280, 800)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = BgApp.WindowSize
        self.rootwidget = RootWidget(size=BgApp.WindowSize)

    def build(self):
        return self.rootwidget
