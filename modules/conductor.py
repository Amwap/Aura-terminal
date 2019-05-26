# coding: utf-8

from modules.module import Module

from extensions.JsonClient import JC
j = JC()

from os import startfile


class Conductor(Module):
    def __init__(self):
        Module.__init__(self)
        self.module_name = "Module: Conductor"
        self.box_name    = "In box: Links"
        self.box_content = "Not found"
        self.aura_says   = "Conductor connected, commands available."
        self.user_hint   = ""
        self.commands_list = {"add":"add [name] <path/to/file>", 
                              "del":"del <name> or <number>"}
        
        self._conductor = j.j_move(name="CONDUCTOR")
        self.set_box(list(self._conductor))
        self.set_box_string()



    def module_request(self, message):
        if   message.command == "add":  self._add(message)
        elif message.command == "del":  self._del(message.args[1])
        else:  self._choice(message.command)



    def _del(self, args):
        del self._conductor[args]
        j.j_move(name="CONDUCTOR", var=self._conductor)
        self.set_box(list(self._conductor))



    def _add(self,message):
        self._conductor[message.name] = message.link
        self.aura_says = f"Path {message.link} created."

        j.j_move(name="CONDUCTOR", var=self._conductor)
        self.set_box(list(self._conductor))



    def _choice(self,command):
        if command in self._true_box:
            startfile(self._conductor[command])
            self.aura_says = f"The link \"{command}\" was used!"

        else:
            self.aura_says = "This link not found"
