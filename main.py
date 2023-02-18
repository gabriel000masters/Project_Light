from languages import *
from actions import *
import speech_recognition as sr
import time

def main():
    current_lang = 'default'
    command = ''
    print('habla')
    time.sleep(1)
    while 1:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            command, current_lang = speak(r, source, current_lang)
            read_action(r, source, command, current_lang)

if __name__ == "__main__":
    main()