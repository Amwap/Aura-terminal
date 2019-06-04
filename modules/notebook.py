#codinf: utf-8

from modules.module import Module

from extensions.JsonClient import JC
j = JC()

from os import listdir, startfile, remove

class Notebook(Module):
    def __init__(self):
        Module.__init__(self)
        self.module_name = "Module: Notebook"
        self.box_name    = "In box: Lists"
        self.box_content = "Not found"
        self.aura_says   = "Did you call me?"
        self.user_hint   = ""
        self.commands_list = {"add":"add <note name>",
                              "del":"del <note name> or <number>",
                              "print":"print is not released", 
                              "archive":"archive is not released"}

        self.set_box(listdir(j.path["NOTEBOOK"]))
        self.NOTEBOOK = j.path["NOTEBOOK"]



    def module_request(self, message):
        if message.command == "add":       self._add(message.args[1])
        elif message.command == "del":     self._del(message.args[1])
        elif message.command == "print":   pass
        elif message.command == "archive": pass
        else: self._read(message.command)



    def _read(self, command):
        print(command)
        if f"{command}.txt" in listdir(self.NOTEBOOK):
            startfile(f"{self.NOTEBOOK}\\{command}.txt")
            self.aura_says = f"Note \"{command}\" open for read and write."
        else:
            self.aura_says = f"Note \"{command}\" is not found."
        


    def _add(self, arguments):
        f = open(f"{self.NOTEBOOK}\\{arguments}.txt", "w")
        f.close()
        startfile(f"{self.NOTEBOOK}\\{arguments}.txt")
        self.set_box(listdir(self.NOTEBOOK))



    def _del(self, arguments):
        if f"{arguments}.txt" in listdir(self.NOTEBOOK):
            remove(f"{self.NOTEBOOK}\\{arguments}.txt")
            self.set_box(listdir(self.NOTEBOOK))
        else:
            self.aura_says = f"Note \"{arguments}\" is not found."



    def open_item(self, message):
        if message.args[1]+".txt" in self._true_box:
            self._read(message.args[1])
            return True

    
