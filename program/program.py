# coding: utf-8

from program.insert import Insert

class Program(Insert):
    def __init__(self):
        Insert.__init__(self)

    def set_key(self, move, code, key):
        self.key_set(move, code, key)

    def get_user_says(self):
        return self.user_says

    def get_module_name(self):
        return self.active_module.module_name

    def get_box_name(self):
        return self.active_module.box_name

    def get_box_content(self):
        return self.active_module.box_content

    def get_aura_says(self):
        return self.active_module.aura_says
    
    def get_user_hint(self):
        return self.active_module.user_hint
