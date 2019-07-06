from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from bglib.flow.decision import Decision


class DecisionOptionButton(Button):
    def __init__(self, decision_option, **kwargs):
        super().__init__(**kwargs)
        self.decision_option = decision_option
        self.text = decision_option.text

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.on_option_chosen(self.decision_option)
        super().on_touch_down(touch)


class DecisionWidget(BoxLayout):
    def __init__(self, decision, **kwargs):
        super().__init__(**kwargs)
        self.decision = decision
        self.orientation = 'vertical'

        labeltext = f'{self.decision.owner}: {self.decision.text}'
        self.add_widget(Label(text=labeltext, size_hint_x=1))
        for opt in self.decision.options:
            self.add_widget(DecisionOptionButton(opt))

    def on_option_chosen(self, option):
        self.decision.choose(option)
        if self.parent:
            self.parent.remove_widget(self)