# coding utf-8

from datetime import timedelta, datetime
from time import clock, ctime

import kivy
# kivy.require('1.10.1')
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from extensions.JsonClient import JC
j = JC()

from program.program import Program
program = Program()



class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        print(touch.pos)



class MyKeyboardListener(Widget):
    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        from kivy.core.window import Window
        self._keyboard = Window.request_keyboard(self, 'text')
        self._keyboard.bind(on_key_up=self.key_up)
        self._keyboard.bind(on_key_down=self.key_down)

    def key_down(self, keyboard, keycode, text, modifiers):
        program.set_key("down", *keycode)
        return True

    def key_up(self, *args):
        program.set_key("up", *args[1])
        return True



class Application(App):
    title = 'Aura Terminal'
    icon = 'Images\Aura.ico'

    Config.set("graphics", "resizable", 0)
    Config.set("graphics", "width", 600)
    Config.set("graphics", "height", 360)



    def build(self):
        self.text = "123"

        pack = FloatLayout()
        interface = Image(source="Images\Interface.png")
        pack.add_widget(interface)


        self.time = Label(
            text=f'date \ntime ', 
            pos=(41, -136),
            font_size="15",
            font_name=j.path["FONT"]+"\\10651.otf",
            text_size=(100, 15),
            valign="top",
        )
        pack.add_widget(self.time)

        self.date = Label(
            text=f'date \ntime ', 
            pos=(-150, -136),
            font_size="15",
            font_name=j.path["FONT"]+"\\10651.otf",
            text_size=(150, 15),
            valign="top",
        )
        pack.add_widget(self.date)

        self.language = Label(
            text=f'En', 
            pos=(-221, -137),
            font_size="14",
            font_name=j.path["FONT"]+"\\10651.otf",
            text_size=(100, 15),
            valign="top",
        )
        pack.add_widget(self.language)

        self.version = Label(
            text=f'version: Aura Terminal 000\nrelease: 00 00 2019 by Amwap',
            pos=(-150, 154),
            font_size="15",
            font_name = j.path["FONT"]+"\\10651.otf",
            text_size=(200, 30),
            valign="top",
        )
        pack.add_widget(self.version)

        self.module = Label(
            text=f'Module: Main',
            pos=(182, 153),
            font_size="12",
            font_name = j.path["FONT"]+"\\consolai.ttf",
            text_size=(190, 15),
            valign="top",
        )
        pack.add_widget(self.module)

        self.inbox = Label(
            text=f'In box: Commands',
            pos=(182, 130),
            font_size="12",
            font_name = j.path["FONT"]+"\\consolai.ttf",
            text_size=(190, 15),
            valign="top",
        )
        pack.add_widget(self.inbox)

        self.box = Label(
            text=f'• 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 '*30,
            pos=(182, -25),
            font_size="12",
            font_name=j.path["FONT"]+"\\consolai.ttf",
            #wraplength=False,
            text_size=(190, 280),
            valign="top",
        )
        pack.add_widget(self.box)

        self.aura_place = Label(
            text=f'Welcome to Aura Terminal',
            pos=(-170, 21),
            font_size="12",
            font_name=j.path["FONT"]+"\\consolai.ttf",
            text_size=(230, 220),
            valign="top",
        )
        pack.add_widget(self.aura_place)

        self.hint_place = Label(
            text=program.user_says[-100:],
            pos=(-105, -156),
            font_size="13",
            font_name = j.path["FONT"]+"\\consolai.ttf",
            text_size=(334, 15),
            color=[150, 150, 150, 2],
            valign="top",
        )
        pack.add_widget(self.hint_place)

        self.user_place = Label(
            text=program.user_says[-100:],
            pos=(-105, -156),
            font_size="13",
            font_name = j.path["FONT"]+"\\consolai.ttf",
            text_size=(334, 15),
            valign="top",
        ) 
        pack.add_widget(self.user_place)

        self.invitation = Label(
            text=">>",
            pos=(-120, -156),
            font_size="13",
            font_name = j.path["FONT"]+"\\consola.ttf",
            text_size=(335, 15),
            valign="top",
        ) 
        pack.add_widget(self.invitation)



        pack.add_widget(MyPaintWidget())
        pack.add_widget(MyKeyboardListener())

        Clock.schedule_interval(self._timer_loop, 0.1)
        Clock.schedule_interval(self._data_set, 0.1)
        Clock.schedule_interval(self._stub_set, 0.3)
        Clock.schedule_interval(self._voice_ping, 1)
        self.stub = " "
        return pack



    def _voice_ping(self, dt):
        program.last_signal = datetime.now()

    
    def _timer_loop(self, dt):
        now_time = ctime()
        session_time = str(timedelta(seconds=clock()))[:-7]

        self.time.text = f"{session_time}"
        self.date.text = f"{now_time}"



    def _stub_set(self, dt):
        if self.stub != "_":
            self.stub = "_"
        elif self.stub != " ":
            self.stub = " "



    def hinting(self, text):
        string = text.split(" ")
        if string[0] in program.active_module.commands_list:
            # return text.replace(string[0], f"[/b][color=ff0000]{string[0]}[/color][/b]")
            return text
        else:
            return text



    def _data_set(self, dt):
        self.module.text = program.get_module_name()
        self.inbox.text = program.get_box_name()
        self.box.text = program.get_box_content()   
        self.aura_place.text = program.get_aura_says()

        text = self.hinting(program.get_user_says()) 
        if len(text) > 47:
            text = self.hinting(program.get_user_says())[-47:-1]

        if program.active_module.commands_list.get(program.user_says) != None:
            self.hint_place.text = program.active_module.commands_list.get(program.user_says)
        else: self.hint_place.text = program.user_hint

        self.user_place.text = text + self.stub 
        self.language.text = program._language
        



