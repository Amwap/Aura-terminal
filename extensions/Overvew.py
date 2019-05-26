# coding: utf-8

from extensions.JsonClient import JC
j = JC()

from os import listdir

def overview_save(place, integer):
    stats = j.j_move(name="STATS")
    stats[place] += integer
    j.j_move(name="STATS", var=stats)


def overview_show():
    stats = j.j_move(name="STATS")
    statistics = ["Enter in modul",
                  "• Main:      " + str(stats["main"]),
                  "• Aura:      " + str(stats["aura"]),
                  "• Notebook:  " + str(stats["note"]),
                  "• Selector:  " + str(stats["selector"]),
                  "• Conductor: " + str(stats["path"]),
                  " ",
                  "Data size:",
                  "• Aura:      " + str(len(j.j_move(name="CASPER"))),
                  "• Notebook:  " + str(len(listdir(j.path["NOTEBOOK"]))),
                  #f"• Selector:  " + str(len(j.j_load(SELECTS))),
                  "• Conductor: " + str(len(j.j_move(name="CONDUCTOR"))),
                ]

    return(statistics)
