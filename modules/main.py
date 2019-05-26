# coding: utf-8

from modules.module import Module



class Main(Module):
    def __init__(self):
        Module.__init__(self)
        self.module_name = "Module: Main"
        self.box_name    = "In box: Commands"
        self.box_content = "Not found"
        self.aura_says   = "Welcome to Aura Terminal!"
        self.user_hint   = ""
        self.commands_list = {}

        self._true_box = [
            "aura",
            "path",
            "note",
            "slk",
            "tool",
            "game",
            "overview",
            "manual",
            "commands",
            "theme",
        ]

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

Information:
7  Overview
8  Manual
9  Commands

Configuration:
10  Theme

"""

        
        
    def module_request(self, message):
        if message.command == "manual": pass
        elif message.command == "theme": pass
        elif message.command == "overview": pass
        elif message.command == "commands": pass
        elif message.command == " ": pass