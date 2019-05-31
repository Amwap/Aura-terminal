# coding: utf-8

from extensions.Overvew import overview_save

from modules.aura import Aura
from modules.conductor import Conductor
from modules.main import Main
from modules.notebook import Notebook
from modules.selektor import Selektor

from program.message import Message


overview_save("launches", 1)

class Distributor():
    def __init__(self):
        self._module_name = "main"

        self.module_base = {
            "main": Main(),
            "aura": Aura(),
            "path": Conductor(),
            "note": Notebook(),
            "slk":  Selektor(),
            "game": None, # TODO
            "tool": None, # TODO
            } 

        self.module_base["main"].module_base = self.module_base

        self.active_module = self.module_base["main"]

    def order(self, string):
        if string == "":
            return False
        repl_list = []
        for word in string.split():
            try: repl = self.active_module._num_box[int(word)]
            except: repl = word
            repl_list.append(repl)

            
        message = Message(" ".join(repl_list))

        if self._module_name == "main" and  message.command in self.module_base:
            self.active_module = self.module_base[message.command]
            overview_save(message.command, 1)
            
        
        elif message.command == "module":
            self.active_module = self.module_base[message.arguments]
            overview_save(message.command, 1)

        else:
            self.active_module.request(message)
