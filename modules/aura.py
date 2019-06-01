#coding: utf-8

import random
import re
import threading
from difflib import SequenceMatcher
from os import path, remove
from random import choice, randint
from re import compile

import gtts
from pygame import mixer

from extensions.JsonClient import JC
from extensions.Overvew import overview_save
from extensions.Sound import sound_output
from modules.module import Module

j = JC()


class Aura(Module):
    def __init__(self):
        Module.__init__(self)
        self.module_name = "Module: Aura"
        self.box_name = "In box: History"
        self.box_content = "Not found"
        self.aura_says = "Did you call me?"
        self.user_hint = ""
        self.commands_list = {"add": "add <question> = <answer 1> = <answer 2> ...",
                              "del": "del - delete last answer",
                              "say": "say <message for dubbing>",}

        self._true_box = []
        self._num_box = dict(enumerate(self._true_box))

        self._casper_main = j.j_move(name="CASPER")
        self._casper = self._casper_main.copy()

        self._history = [""]
        #self._history = [""] + ["123"]*22 # lengh test
        self._last_question = None

        self.last_add = None
        self.treads = []
        


    def _add(self, text):
        text_list = [ x.rstrip().lstrip() for x in text.split("=")]
        if len(text_list) < 2:
            self.aura_says = "Мistake command"
            return
        
        for msg in text_list[0].split("/"):
            question = " ".join(self._text_filter(msg))
            if question in self._casper_main:
                self._casper_main[question] += text_list[1:]
                self._casper[question] += text_list[1:]

            else:
                self._casper_main[question] = text_list[1:]
                self._casper[question] = text_list[1:]

        j.j_move(name="CASPER", var=self._casper_main)
        string = ", ".join(text_list[1:])

        self.aura_says = f'for "{text_list[0]}" added answer: {string}'



    def _del(self):
        try:
            if self.aura_says in self._casper_main[self._last_question]:
                self._casper_main[self._last_question].remove(self.aura_says)
                if self._casper_main[self._last_question] == []:
                    self._casper_main.pop(self._last_question)
                j.j_move(name="CASPER", var=self._casper_main)

                self.aura_says = "Delet complite."


            else:
                self.aura_says = "I can not do this because the answer belongs to another question."

        except KeyError:
            self.aura_says = "Failed to delete non-existent object."

    def __say(self):
        sound_output(self.aura_says)
        return



    def module_request(self, message): 
        if self.insert_list[-1] != message.string: self.insert_list.append(message.string)
        self.insert_list.append("")
        self._box_id = self._standart_box_id
        
        if message.command == "add": self._add(message.string[4:])
        elif message.command == "del": self._del()
        elif message.command == "say": 
            self.aura_says = message.string[4:]
            t = threading.Thread(target=self.__say)
            t.start()

        else: 
            self.aura_says, self._last_question = self._search_answer(message.string, self._casper)

        
        self._reload_history(message.string, self.aura_says)



    def _text_filter(self, text):
        split_regex = compile(r'[.|!|?|^|@|#|$|%|&|*| |)|(|:|,]')
        sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(text)])
        word_list = [x.lower() for x in sentences]
        if "?" in text:
            word_list.append("?")

        return word_list



    def _search_answer(self, string, massive=None):
        overview_save("messages", 1)
        if massive == None:
            massive = self._casper

        def selection( string, massive ):
            max_coincidence = 0
            list_coincidence = []
            for key in massive: 
                s = SequenceMatcher(lambda x: x==" ", self._text_filter(key), self._text_filter(string)) 
                coincidence = s.ratio()
                if coincidence == max_coincidence and coincidence > 0:
                    list_coincidence.append(key)


                elif coincidence > max_coincidence:
                    max_coincidence = coincidence
                    list_coincidence.clear()
                    list_coincidence.append(key)

            return (list_coincidence, max_coincidence)



        def check(list_coincidence, max_coincidence):                        
            if max_coincidence < 0.5:
                separator = randint(0,2)
                if separator == 0:
                    hint = ''
                    answer = choice(massive[hint])
                
                elif separator == 1:
                    hint = ''
                    answer = choice(massive[hint])

                elif separator == 2:
                    hint = ''
                    answer = choice(massive[hint])

            else:
                stub = ""
                if max_coincidence < 0.8:
                    stub = " " + choice(massive[""])

                
                hint = choice(list_coincidence)
                try:
                    answer = choice(massive[hint]) + stub
                except IndexError:
                    answer = "Something went wrong"

            return answer, hint



        answer, hint = check(*selection(string, massive))
        answer = answer.replace("%USERNAME%", "User")

        try: 
            if massive[hint] == []: massive.pop(hint)
        except KeyError as e: print(e)
        
        return answer, hint

    def _reload_history(self, user_says, aura_says):
        self._history.append(f"U>>{user_says}")
        self._history.append(f"A>>{aura_says}")
        self.set_box(massive=self._history, nonnumerate=True)



    def set_box(self, massive=None, nonnumerate=True):
        if massive!=None:
            m = massive.copy()
            m.reverse()
            self._true_box = m

        self._num_box = dict(enumerate(self._true_box))
        self.set_box_string(self._true_box, nonnumerate)
