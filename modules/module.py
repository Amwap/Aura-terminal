# coding: utf-8


from extensions.JsonClient import JC
j = JC()

class Module():
    def __init__(self):
        self.module_name = "Module: Name"
        self.box_name = "In box: Name"
        self.box_content = "Not found"
        self.aura_says = "Something"
        self.user_hint = ""
        self.commands_list = {}
        
        self._true_box = []
        self._num_box = dict(enumerate([]))
        self._standart_box_id = 21 # minus itself
        self._box_id = self._standart_box_id  
        self._box_lines = self._standart_box_id 
        self._box_width = 23
        self.input_list_id = 0
        self.command_list_id = 0
        self.insert_list = [""]



    def request(self, message):
        self.command_list_id = 0
        self.module_request(message)



    def module_request(self,message):
        pass



    def back(self):
        return "main"



    def set_box(self, massive=None, nonnumerate=False):
        if massive!=None:
            m = massive.copy()
            m.reverse()
            self._true_box = m
        
        self._num_box = dict(enumerate(self._true_box))
        self.set_box_string(self._true_box, nonnumerate)



    def set_box_string(self, massive=None, nonnumerate=False):
        
        if massive == None:
            massive = self._true_box

        self.box_content = ""

        def add_line(i):
            if nonnumerate == True: num = ""
            else: num = f"{i%len(massive)} "
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

        