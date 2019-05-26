# coding: utf-8

class Message():
    def __init__(self, string):
        self.name = None
        self.args = None
        self.link = None
        self.command = None
        self.string = string
        self._autoset(string, string.split(" "))


    def _autoset(self, string, string_list):
        if "http" in string:
            if len(string_list) == 3:
                self.command = string_list[0]
                self.name = string_list[1].replace(" ", "_")
                self.link = string_list[2]

            if len(string_list) == 2:
                self.command = string_list[0]
                self.name = string_list[1].split("/")[-1].replace(" ", "_")
                self.link = string_list[1]

        elif "C:\\" in string or "E:\\" in string:
            self.command = string_list[0]
            if string_list[1].startswith("C:") or string_list[1].startswith("E:"):
                self.link = "".join(self.string[1:])
                self.name = self.link.split("\\")[-1].replace(" ", "_")

            else:
                self.name = string_list[1].replace(" ", "_")
                self.link = " ".join(string_list[2:])


        
        else: 
            self.command = string_list[0]
            self.args = string_list






# https://vk.com/project.aura

# C:\MY DATA\DEVELOPING\Python\My scripts