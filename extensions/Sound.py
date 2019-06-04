#coding: utf-8

import speech_recognition as sr
import pyttsx3


speak_engine = pyttsx3.init()
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[2].id)

def sound_output(answer):
    speak_engine.say(answer)
    speak_engine.runAndWait()
    speak_engine.stop()



def sound_input(lang): 
    if lang == "en": lang = "en-EN"
    if lang == "ru": lang = "ru-RU"

    r = sr.Recognizer()
    
    with sr.Microphone() as source:                    
        audio = r.listen(source)
    try:
        message = r.recognize_google(audio, language=lang)
        return message
        
    except: 
        return ""


# from datetime import datetime
# from os import path, remove
# from random import randint
# from re import compile
# from time import sleep
# from threading import Thread
# from gtts import gTTS
# from pygame import mixer
# from extensions.JsonClient import JC
# j = JC()


# def sound_output(answer):
#     mixer.init()
#     mp3_name = "tts.mp3"

#     split_regex = compile(r'[.|!|?|^]')
#     sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(answer)])

#     for text in sentences:
#         if text != "":
#             print(text)
#             tts = gTTS(text=text, lang='en')  
#             try: tts.save(j.path["DATA"]+mp3_name)  
#             except:    pass

#             mixer.music.load(j.path["DATA"]+mp3_name)
#             mixer.music.play()
            
#             while mixer.music.get_busy():
#                 sleep(0.1)
        
#     mixer.music.load(j.path["DATA"]+'\\stub.mp3')
#     mixer.stop
#     mixer.quit
    
#     if path.exists(j.path["DATA"]+mp3_name):
#         try:
#             remove(j.path["DATA"]+mp3_name)
#         except PermissionError:
#             pass

#     return 





    

