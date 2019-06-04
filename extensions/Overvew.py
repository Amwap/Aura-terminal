# coding: utf-8

from os import listdir
from datetime import timedelta
from extensions.JsonClient import JC

j = JC()


def overview_save(place, integer):
    stats = j.j_move(name="STATS")
    stats[place] += integer
    j.j_move(name="STATS", var=stats)



def time_save(time):
    stats = j.j_move(name="TIMEWORK")
    stats += time
    j.j_move(name="TIMEWORK", var=stats)



casper = j.j_move(name="CASPER")
selektor = j.j_move(name="SELEKTOR")
tags = j.j_move(name="TAGS")

questions = len(casper)
answers = 0
for x in casper:
    for i in casper[x]:
        answers += 1

casper = None


files = 0

for x in tags:
    files += len(tags[x])


def get_overview():
    stats = j.j_move(name="STATS")
    time = j.j_move(name="TIMEWORK")
    statistics = [
        "General",
        "• Starts program:  " + str(stats["launches"]),
        "• Requests:        " + str(stats["requests"]),
        "• Time work:  " + str(timedelta(seconds=int(time))),
        "",
        "Module Aura",
        "• Connects:        " + str(stats["aura"]),
        "• Questions:       " + str(questions),
        "• Answers:         " + str(answers),
        "• Messages:        " + str(stats["messages"]),
        "",
        "Module Path",
        "• Connects:        " + str(stats["path"]),
        "• Shortcuts:       " + str(len(j.j_move(name="CONDUCTOR"))),
        "",
        "Module Note",
        "• Connects:        " + str(stats["note"]),
        "• Notes:           " + str(len(listdir(j.path["NOTEBOOK"]))),
        "",
        "Module Slk",
        "• Connects:        " + str(stats["slk"]),
        "• Selekts:         " + str(len(selektor)),
        "• Files:           " + str(files),
        ""]
        
    statistics.reverse()
    return(statistics)