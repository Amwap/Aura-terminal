from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
import time
from kivy.uix.popup import Popup

theRoot = Builder.load_string('''
<CustomPopup>:
    active: switch_id_popup.active
    StackLayout:
        Switch:
            id: switch_id_popup
            size_hint: .5, .5
        Button:
            text: 'Close'
            on_release: root.dismiss() 
            size_hint: .5, .5

StackLayout:
    active: switch_id.active
    orientation: 'lr-tb'
    padding: 10
    spacing: 5
    Label:
        text: "Zone 1 Valve"
        size_hint: .25, .1
    Switch:
        id: switch_id
        size_hint: .25, .1
    Button:
        text: "Program 1"
        on_press: app.open_popup()
        size_hint: .5,.1

''')

class CustomPopup(Popup):
    pass


class TheApp(App):
    def build(self):
        self.the_popup = CustomPopup()
        Clock.schedule_interval(self.timer_loop, 2)
        return theRoot

    def timer_loop(self, dt):  
        if self.root.active and self.the_popup.active:
            print("Do something")
        else:
            print("Do nothing")

    def open_popup(self):
        self.the_popup.open()


if __name__ == '__main__':
    TheApp().run()