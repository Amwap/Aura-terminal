#coding: utf-8

from datetime import datetime
from os import path, remove
from random import randint
from re import compile
from time import sleep

import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

from extensions.JsonClient import JC

j = JC()


def sound_output(answer):
    mixer.init()
    mp3_name = "tts.mp3"

    split_regex = compile(r'[.|!|?|^]')
    sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(answer)])

    for text in sentences:
        if text != "":
            print(text)
            tts = gTTS(text=text, lang='en')  
            try: tts.save(j.path["DATA"]+mp3_name)  
            except:    pass

            mixer.music.load(j.path["DATA"]+mp3_name)
            mixer.music.play()
            
            while mixer.music.get_busy():
                sleep(0.1)
        
    mixer.music.load(j.path["DATA"]+'\\stub.mp3')
    mixer.stop
    mixer.quit
    
    if path.exists(j.path["DATA"]+mp3_name):
        try:
            remove(j.path["DATA"]+mp3_name)
        except PermissionError:
            pass

    return 



def sound_input(): # Внимание! в питоне 3.7 не работает.
    r = sr.Recognizer()
    
    with sr.Microphone() as source:                    
        print("Aura listen to you")
        audio = r.listen(source)

    try:
        message = r.recognize_google(audio, language="ru-RU")
        message.lower()
        print(message)
            
    except:
        print("exception")

    return message
