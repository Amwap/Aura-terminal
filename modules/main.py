# coding: utf-8

from modules.module import Module
from os import startfile
from extensions.Overvew import get_overview
from extensions.JsonClient import JC
j = JC()



class Main(Module):
    def __init__(self):
        Module.__init__(self)
        self.module_base = None
        self.module_name = "Module: Main"
        self.box_name    = "In box: Commands"
        self.box_content = "Not found"
        self.aura_says   = "Welcome to Aura Terminal!"
        self.user_hint   = ""

        self.theme_list = j.j_move(name="CONFIG")
        self.theme_active = "{0}\\{1}.png".format(j.path["IMAGES"], self.theme_list["theme"])
        


        self.commands_list = {
            "aura":"aura - conversation module", # other module
            "path":"path - shortcut access module", # other module
            "note":"note - module for notes", # other module
            "slk":"slk - file manager", # other module
            "tool":"tool - module useful scripts", # other module
            "game":"game - pseudographic games", # other module
            "open":"open <name item in aura scope>",
            "play":"play <selekt name>",
            "voice on":"voice on - connect voice input", # other module
            "voice off":"voice off - turn off voice input", # other module
            "view":"view - program statistics",
            "manual":"manual - open full manual about program",
            "theme":"theme - switch theme",
            }

        self._true_box = self.commands_list.keys()

        self.set_box()
        self.box_content = """Modules:
0  Aura
1  Path
2  Note
3  Slk
4  Tool
5  Game

Commands:
6 open
7 play
8 voice on
9 voice off

Information:
10  View
11  Manual

Configuration:
12  Theme

"""

    def back(self):
        return "reload"
        

    def module_request(self, message):
        if message.command == "manual": 
            startfile(j.path["MANUAL"])
            self.aura_says = "Manual is open for reading"
            
        elif message.command == "theme":
            if len(message.args) == 1:
                self.set_box(massive=[x for x in self.theme_list.keys()],nonnumerate=False)

            elif message.args[1] in self.theme_list:
                self.theme_list["theme"] = message.args[1]
                j.j_move(name="CONFIG", var=self.theme_list)
                self.theme_active = "{0}\\{1}.png".format(j.path["IMAGES"], self.theme_list["theme"])


        elif message.command == "view":
            self.set_box(massive=get_overview(), nonnumerate=True)

        elif message.command == "open": pass

        else:
            self.aura_says, _ = self.module_base["aura"]._search_answer(message.string)


    def set_box_string(self, massive=None, nonnumerate=True):
        
        if massive == None:
            massive = self._true_box

        self.box_content = ""

        def add_line(i):
            num = ""
            cont = str(num + f"{self._num_box[i%len(massive)]}")
            if len(cont)>= self._box_width:
                cont = num + f"{self._num_box[i%len(massive)]}"[:self._box_width]
            self.box_content += cont + "\n"


        if len(massive) == 0:
            self.box_content = "Not found."

        elif type(massive) == list:
            for i in range(self._box_id - self._box_lines, self._box_id):
                try:
                    self._num_box[i]
                    add_line(i)
                except KeyError:
                    if len(self._true_box) > 19:
                        add_line(i)
                    else:
                        pass

        elif type(massive) == str:
            pass  # TODO text box