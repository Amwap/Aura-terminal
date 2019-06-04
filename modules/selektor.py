# coding: utf-8

from modules.module import Module

from extensions.JsonClient import JC
j = JC()

from os import startfile, listdir
from random import choice


class Selektor(Module):
    def __init__(self):
        Module.__init__(self)
        self.module_name = 'Module: Selektor'
        self.box_name    = 'In box: Directories'
        self.box_content = 'Not found'
        self.aura_says   = 'Selektor connected, commands available.'

        self.commands_list_bot = {
            'add':'add [name] <path/to/dir>',
            'del':'del <name> or <number>',
            'dir':'dir <name selekt> - to open dirrectory',
            'ignore':'ignore - show ignore list'}

        self.commands_list_middle = {
            "tg":"tg <search tag 1 > <search tag 2> ...",
            "nm":"nm <part of the name>",
            "add":"add <tag 1> <tag 2> ...",
            "del":"del <tag 1> <tag 2> ...",
            "tags":"tags - show tags for this selekt",
            "new":"new - show raw files",
            "r":"r - open random file", }

        self.commands_list_ignore = {
            "add":"add <ignor word>",
            "del":"del <ignore word> or <number>"}

        self.commands_list = self.commands_list_bot
        
        self._selektor = j.j_move(name='SELEKTOR')
        self._tags = j.j_move(name='TAGS')
        self._ignorelist = j.j_move(name='IGNORE')
        self._taglist = set()

        self.set_box(list(self._selektor))
        self.set_box_string()
        self._scene = 'bot'

        self._files = []
        self._dirs = {}
        self._names = {}
        self._selekt_name = None
        self._active_file = None 
        self._active_file_name = None
        self._last_message = None



    def module_request(self, message):
        self._last_message = message
        if self._scene == 'bot':
            if   message.command == 'add': self._add(message)
            elif message.command == 'del': self._del(message.args)
            elif message.command == 'dir': self._dir(message.args)
            elif message.command == 'ignore': 
                self.commands_list = self.commands_list_ignore
                self._ignore()
            else: 
                self._set_selekt(message.command)

        elif self._scene == 'ignore':
            if   message.command == 'add': self._ignore_add(message.args[1:])
            elif message.command == 'del': self._ignore_del(message.args[1:])

        else: 
            if message.command == 'tg': self._search_tg(message.args)
            elif message.command == 'nm': self._search_nm(message)
            elif message.command == 'add': self._tg_add(message.args[1:])
            elif message.command == 'del': self._tg_del(message.args[1:])
            elif message.command == 'tags': self._set_tags()
            elif message.command == 'new': self._set_new()
            elif message.command == 'random': self._open_random()
            
            else:
                self._set_active_file(message.string)
                self._start(self._active_file, message.string)     



    def _set_selekt(self, selekt_name):
        try:
            self._selekt_name = selekt_name
            self._taglist = set()
            self._files = []
            self._dirs = {}
            self._names = {}
            self._mapping(self._selektor[selekt_name])
            self.set_box(self._files)
            self._scene = 'middle'
            self.box_name = f'In box: {selekt_name}'
            self.aura_says = f'Selekt "{selekt_name}" has been set.'
            self.commands_list = self.commands_list_middle

        except KeyError: self.aura_says = f'Selekt "{selekt_name}" not found.'



    def back(self): 
        if self._scene == 'top':
            self._set_selekt(self._selekt_name)
            # self._scene = "middle"
            # self.set_box(self._files)
            # self.box_name = f'In box: {self._selekt_name}'
            # self.aura_says = f'Files "{self._selekt_name}" was loaded in box.'
            return False
            
        elif self._scene == 'ignore': return 'reload'
        elif self._scene == 'middle': return 'reload'
        elif self._scene == 'bot':return 'main'




    def _set_new(self):
        new_file = []
        for f in self._files:
            if f not in self._tags[self._selekt_name]: 
                new_file.append(f)
        
        self._scene = 'top'
        self.set_box(new_file)
        self.box_name = f'In box: New files'
        self.aura_says = 'New files for this selekt was loaded in box.'
        


    def _global_search(self):
        if self._search_tg(self._last_message.args) == True:
            if self._search_nm(self._last_message) == True:
                self.aura_says = f'Nothing was found for this request'



    def _search_nm(self, message):
        new_file = []
        for f in self._files:
            if f.lower().find(message.string.lower()) != -1: 
                new_file.append(f)
        
        if new_file == []:
            return True

        else:
            self._scene = 'top'
            self.set_box(new_file)
            self.box_name = 'In box: Search by name'
            self.aura_says = 'Search by name is done. Results uploaded to box.'
            return False



    def _open_random(self):
        f = choice(self._files)
        self._set_active_file(f)
        self._start(self._active_file, f)



    def _ignore(self):
        self._scene = 'ignore'
        self.set_box(self._ignorelist)
        self.box_name = 'In box: Ignore'
        self.aura_says = 'Ignore list showed in box.'
        


    def _ignore_add(self, arguments):
        self._ignorelist += arguments
        j.j_move(name='IGNORE', var=self._ignorelist)
        self.set_box(self._ignorelist)
        self.aura_says = '{} append to ignore list.'.format(", ".join(arguments))



    def _ignore_del(self, arguments):
        for x in arguments:
            del self._ignorelist[self._ignorelist.index(x)]

        j.j_move(name='IGNORE', var=self._ignorelist)
        self.set_box(self._ignorelist)
        self.aura_says = '{} deleted'.format(", ".join(arguments))


    def _search_tg(self, args):
        new_file = []
        args_set = set([x.lower() for x in args])
        for f in self._files:
            tags_file = self._tags[self._selekt_name].get(f)
            if tags_file == None: tags_file = []
            if list(set(tags_file) & args_set) != []: 
                new_file.append(f)

        if new_file == []:
            return True

        else:
            self._scene = 'top'
            self.set_box(new_file)
            self.box_name = 'In box: Search by tags'
            arg_string = ', '.join(args)
            self.aura_says = f'Files with tags: {arg_string} for this selekt was loaded in box.'
            return False



    def _set_tags(self):
        self.set_box(list(self._taglist))
        self._scene = 'top'
        self.box_name = f'In box: Tags'
        self.aura_says = 'Tags for this selekt was loaded in box'



    def _tg_add(self, args):
        if self._active_file_name in self._tags[self._selekt_name]:
            self._tags[self._selekt_name][self._active_file_name] += [x.lower() for x in args]

        elif self._active_file_name not in self._tags:
            self._tags[self._selekt_name][self._active_file_name] = [x.lower() for x in args]

        tag_string = ', '.join(args)
        self.aura_says = f'For {self._active_file_name} append tags: {tag_string}'
        j.j_move(name='TAGS', var=self._tags)



    def _tg_del(self, args):        
        if args[0] == 'all':
            self._tags[self._selekt_name].pop(self._active_file_name)
            self.aura_says = f'All tags deleted for {self._active_file_name}'

        else:
            selected_file = self._tags[self._selekt_name][self._active_file_name]
            for arg in args:
                if arg in selected_file:
                    del selected_file[selected_file.index(arg)]
            say_string = ', '.join(args)
            self.aura_says = f'For {self._active_file_name} deleted tags: {say_string}'

        if self._tags[self._selekt_name][self._active_file_name] == []:
            self._tags[self._selekt_name].pop(self._active_file_name)
        j.j_move(name='TAGS', var=self._tags)


                
    def _set_active_file(self, command):
        change = False
        for name in self._dirs:
            if command in self._dirs[name]:
                self._active_file = f'{name}\\{command}'
                self._active_file_name = command
                change = True

        if change == False: 
            self._active_file_name = None
            self._active_file = None



    def _start(self, path, name):
        try:
            startfile(path)
            tags = '\n'
            if name in self._tags[self._selekt_name]:
                for tg in self._tags[self._selekt_name][name]:
                    tags += f'{tg}\n'

            else: tags = 'Not found'

            self.aura_says = f'File "{name}" has been started.\n\nTags: {tags}'
        
        except TypeError: self._global_search()



    def _mapping(self, path):
        name = path.split('\\')[-1]
        self._names[name] = path
        self._dirs[path] = []
        for stuff in listdir(path):
            strike = False
            for ignor in self._ignorelist:
                if stuff.lower().find(ignor.lower()) != -1:
                    strike = True

            if stuff.find('.') == -1 and strike != True:                    
                self._mapping(f'{path}\\{stuff}')

            elif stuff.find('.') != -1 and strike != True:
                self._dirs[path].append(stuff)
                self._files.append(stuff)
                try:self._taglist |= set(self._tags[self._selekt_name][stuff])
                except KeyError: pass



    def _add(self,message):
        if len(message.args) < 2:
            self.aura_says = "Broken command."
            return
        
        if message.name == None:
            self.aura_says = "You did not indicate the path."
            return

        name = message.name
        self._selektor[name] = message.link

        self._selekt_name = name
        self._tags[name] = {}
        j.j_move(name='TAGS', var=self._tags)
        j.j_move(name='SELEKTOR', var=self._selektor)
        self.set_box(list(self._selektor))



    def _del(self, arguments):
        if len(arguments) < 2:
            self.aura_says = "Broken command."
            return
        try:
            del self._selektor[arguments[1]]
            j.j_move(name='SELEKTOR', var=self._selektor)
            self.set_box(list(self._selektor))
        except KeyError:
            self.aura_says = "Selekt not found."
    
    
    
    def _dir(self, args):
        print(self._selektor[args])
        if args in self._true_box:
            startfile(self._selektor[args]) 
            self.aura_says = f"Directory {args} has been open"

        else:
            self.aura_says = f"Directory {args} not found."


    def open_item(self, message):
        if message.args[1] in self._true_box:
            self._dir(message.args[1])
            return True