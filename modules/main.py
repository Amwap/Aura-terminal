# coding: utf-8

from modules.module import Module
from os import startfile
from extensions.Overvew import get_overview
from extensions.JsonClient import JC
j = JC()



class Main(Module):
    def __init__(self):
        Module.__init__(self)
        
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
            "assistant":"assistant - voice assistant", # other module
            #"voice off":"voice off - turn off voice input", # other module
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
8 assistant

Information:
9  View
10  Manual

Configuration:
11  Theme

"""

    def back(self):
        return "reload"
        


    def module_request(self, message):
        if message.command == "manual": self._open_manual()
        elif message.command == "theme": self._set_theme(message)
        elif message.command == "view": self._load_view()
        elif message.command == "open": self._open_item(message)
        else: self.aura_says, _ = self.module_base["aura"]._search_answer(message.string)



    def _open_item(self, message):
        for module in self.module_base:
            if module == "main": continue
            if self.module_base[module].open_item(message) == True: 
                self.aura_says = f"{message.args[1]} open through the module {module}"
                break
            else:
                self.aura_says = "Nothing not found"




    def _load_view(self):
        self.set_box(massive=get_overview(), nonnumerate=True)
        self.aura_says = "Statistis has been load in box."



    def _set_theme(self, message):
        if len(message.args) == 1:
            self.set_box(massive=[x for x in self.theme_list.keys()],nonnumerate=False)
            self.aura_says = "Theme list has been load in box"

        elif message.args[1] in self.theme_list:
            self.theme_list["theme"] = message.args[1]
            j.j_move(name="CONFIG", var=self.theme_list)
            self.theme_active = "{0}\\{1}.png".format(j.path["IMAGES"], self.theme_list["theme"])
            self.aura_says = f"The {message.args[1]} theme was been set. Pleace restart the program."



    def _open_manual(self):
        startfile(j.path["MANUAL"])
        self.aura_says = "Manual is open for reading"



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