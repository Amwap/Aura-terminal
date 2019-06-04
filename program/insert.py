# coding: utf-8

from datetime import datetime
from threading import Thread

from pyperclip import paste

from extensions.Overvew import overview_save
from extensions.Sound import *
from program.distributor import Distributor


class Insert(Distributor):
    def __init__(self):
        Distributor.__init__(self)
        self.user_says = ''
        self.user_hint = ''
        self._shift = False
        self._language = "en"
        self._assistant = False
        self._module_init = False

        self.last_signal = datetime.now()



    def __recognition(self):
        while self._assistant:
            td = datetime.now() - self.last_signal
            if td.seconds > 5:
                self._assistant = True
            
            self.user_hint = sound_input(lang=self._language)
            if self.user_hint != "": self._enter(self.user_hint)
            print(self.user_hint)
        return



    def key_set(self, move, code, key):
        if move == "down":
            self._key_down(code, key)

        elif move == "up":
            self._key_up(code, key)



    def _input_spin(self, vector):
        if vector == "right":  self.active_module.input_list_id += 1
        elif vector == "left": self.active_module.input_list_id -= 1
        self.user_says = self.active_module.insert_list[self.active_module.input_list_id % len(self.active_module.insert_list)]



    def _box_spin(self, vector):
        if len(self.active_module._true_box) > 19:
            if vector == "pagedown":   self.active_module._box_id +=1
            elif vector == "pageup":   self.active_module._box_id  -=1
            self.active_module.set_box()



    def _command_spin(self, vector):
        if vector == "down":  self.active_module.command_list_id += 1
        elif vector == "up": self.active_module.command_list_id -= 1
        commands_list = list(self.active_module.commands_list.keys())
        self.user_says = commands_list[self.active_module.command_list_id % len(commands_list)]



    def _enter(self, string):
        overview_save("requests", 1)

        repl_list = []
        for word in string.split():
            try: repl = self.active_module._num_box[int(word)]
            except: repl = word
            repl_list.append(repl)
        string = " ".join(repl_list)

        if string.lower().startswith("assistant") and self._assistant == False:
            self._assistant = True
            Thread(target=self.__recognition).start()
            self.user_says = ""
            self.active_module.aura_says = "Voice assistant Aura activated"
            return

        elif string.lower().startswith("assistant") and self._assistant == True:
            self._assistant = False
            self.user_says = ""
            self.active_module.aura_says = "Voice assistant Aura deactivated"
            return

            

        self.order(string)
        self.user_says = ""
        
        #self.active_module._box_id = self.active_module._standart_box_id

        if self.active_module.module_name == "Module: Aura":
            self.active_module.set_box()

        if self._assistant == True:
            sound_output(self.active_module.aura_says)



    def _delete(self):
        self.active_module.insert_list[-1] = ""
        self.user_says = ""

    

    def translate(self, code, key):
        liter = {"97":"ф", "98":"и", "99":"с", "100":"в","101":"у", "102":"а", "103":"п", "104":"р",
                "105":"ш", "106":"о", "107":"л", "108":"д", "111":"щ", "112":"з", "113":"й", "114":"к",
                "115":"ы", "116":"е", "117":"г", "118":"м", "119":"ц", "120":"ч", "121":"н", "122":"я",
                "109":"ь", "1073":"б", "1102":"ю", "1078":"ж","1101":"э", "1093":"х", "1098":"ъ", "1105":"ё",
                "110":"т"}.get(str(code))
                
        if liter == None:
            return key
        else:
            return liter



    def _key_up(self, code, key):
        if key == "shift": self._shift = False



    def _key_down(self, code, key):
        if   key == "shift":     self._shift = True
        elif key == "delete":    self._delete()
        elif key == "spacebar":  self.user_says += " "
        elif key == "backspace": self.user_says = self.user_says[:-1]
        elif key == "enter":     self._enter(self.user_says)
        elif key == "left":      self._input_spin("left")
        elif key == "right":     self._input_spin("right")
        elif key == "up":        self._command_spin("up")
        elif key == "down":      self._command_spin("down")
        elif key == "pageup":    self._box_spin("pageup")
        elif key == "pagedown":  self._box_spin("pagedown")
        elif key == "insert":    self.user_says += f"{paste()} "
        elif key == "tab":       self._language = "ru" if self._language == "en" else "en"
        elif key == "lctrl":     pass
        elif key == "escape":
            move = self.active_module.back()
            if move == 'reload' :
                self.active_module.__init__()
                self.active_module.module_base = self.module_base

            elif move == 'main':
                self.active_module = self.module_base["main"]

        else:    
            if self._shift == True:
                symbols_array = {"1":"!", "2":"@", "3":"#", "4":"$", "5":"%", 
                                 "6":"^", "7":"&","8":"*","9":"(", "0":")", "/":","}
                try:  
                    self.user_says += symbols_array[key]

                except KeyError:
                    if self._language == "ru":
                        key = self.translate(code, key) 
                        
                    self.user_says += key.capitalize()

            elif self._shift == False:  
                if self._language == "ru":
                        key = self.translate(code, key) 
                self.user_says += key

            self.active_module.insert_list[-1] = self.user_says
            self.active_module.input_list_id = len(self.active_module.insert_list)
