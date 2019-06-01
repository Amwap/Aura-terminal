import json
from os import getcwd

class JC():
    def __init__(self):
        MAIN_DIR = getcwd()
        MAIN_DIR = "C:\MY DATA\DEVELOPING\Aura Project\Aura Terminal\IN PROGRESS\Aura-Terminal"
        self.path = {
                    "":"", # есть, значит так надо.
                    "CASPER": f"{MAIN_DIR}\data\casper.json",
                    "CONDUCTOR": f"{MAIN_DIR}\data\conductor.json",
                    "SELEKTOR": f"{MAIN_DIR}\data\\selektor\\selektor.json",
                    "TAGS": f"{MAIN_DIR}\data\\selektor\\tags.json",
                    "IGNORE": f"{MAIN_DIR}\data\\selektor\\ignore.json",
                    "STATS": f"{MAIN_DIR}\data\\stats.json",
                    "NOTEBOOK": f"{MAIN_DIR}\data\\notebook",
                    "DATA": f"{MAIN_DIR}\data",
                    "FONT": f"{MAIN_DIR}\\application",
                    "MANUAL": f"{MAIN_DIR}\data\\manual.txt",
                    "CONFIG": f"{MAIN_DIR}\data\\config.json",
                    "IMAGES": f"{MAIN_DIR}\images"
                    }


    def j_move(self,name="", path="", var=None):
        paths = path + self.path[name]
        if var == None: return self.j_load(paths)
        elif var != None: self.j_save(paths, var)
    

    def j_load(self, path):
        with open(path, mode="r",encoding='utf8') as json_file:
            variable = json.load(json_file)
        return(variable)


    def j_save(self, path, var):
        with open(path, 'w', encoding='utf8') as json_file:
            json.dump(var, json_file, ensure_ascii=False)

