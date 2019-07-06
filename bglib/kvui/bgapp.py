from kivy.app import App
from bglib.kvui.rootwidget import RootWidget


class BgApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rootwidget = RootWidget()

    def build(self):
        return self.rootwidget
