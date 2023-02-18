import os
import re
import shutil
import urllib.request
import webbrowser
from urllib.parse import quote

import bs4 as bs
import requests
import win32api

from languages import *

def read_action(r : sr.Recognizer, source: sr.Microphone, action: str, language: str):
    extensions = ['.exe', '.txt', '.mp3', '.wav', '.mp4', '.html', '.png', '.jpg', '.jpeg','.docx', '.csv', '.lxml', '.ppt']
    match action.lower():
                case 'read wikipedia' | 'leer wikipedia' | 'wikipedia':
                    text = speak(r, source, language)
                    scrape_from_wikipedia(text, language)
                case 'youtube':
                    text = speak(r, source, language)
                    process_video_youtube(text, language)
                case 'open':
                    print('folder name?')
                    folder_name = speak(r, source, language)
                    print('file name?')
                    filename = speak(r, source, language)
                    process_file(r, source, language, filename=filename, folder_name=folder_name, command='open', ext=extensions)
                case 'delete':
                    process_file(r, source, language, 'boom','Accel World', 'delete', ext=extensions)
                case 'rename':
                    process_file(r, source, language, 'hola','Accel World', 'rename', ext=extensions)
                case 'move':
                    move_file(extension=extensions)
                                  
def scrape_from_wikipedia(topic : str, p_lang : str):
    source = ''
    match p_lang:
        case 'eng' | 'default':
            source = urllib.request.urlopen(f'https://en.wikipedia.org/wiki/{quote(topic[0])}').read()
        case 'esp':
            source = urllib.request.urlopen(f'https://es.wikipedia.org/wiki/{quote(topic[0])}').read()
        case 'jap':
            topic_encoded = str(topic[0])
            source = urllib.request.urlopen(f'https://ja.wikipedia.org/wiki/{quote(topic_encoded)}').read()
    soup = bs.BeautifulSoup(source, 'lxml')
    [[print(str(paragraph.text))] for paragraph in soup.find_all(['h1','h2','h3','p'])]

def process_video_youtube(name: str, lang: str):
    name = list(name)
    name[0] = name[0].replace(' ', '+')
    name[0] = name[0].replace("%E3%80%80", '')
    match lang:
        case 'jap':
            base_search_link = f'https://www.youtube.com/results?search_query={quote(str(name[0]))}'
        case _:
            base_search_link = f'https://www.youtube.com/results?search_query={name[0]}'
            
    url = urllib.request.urlopen(base_search_link)
    vid_ids = re.findall(r"watch\?v=(\S{11})", url.read().decode())
    open_youtube_vid(vid_ids, index = 0) 

def open_youtube_vid(vid_ids, index = 0):
    webbrowser.open_new_tab(f"https://www.youtube.com/watch?v={vid_ids[index]}")

def process_file(r : sr.Recognizer, source: sr.Microphone, language: str, filename: str, folder_name: str, command: str, ext):
    rex = re.compile(f'{folder_name}')
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        route = find_filepath(drive, rex)
        if filename and command != 'move':
                boot = f'{route}//{filename}'
                work_with_file(r= r,  source= source, language= language, file= boot, extension= ext, action= command, base_route= route, old_name= filename) 
    return f'{route}//{filename}'

def find_filepath(root_folder: str, rex):
    for root, dirs, files in os.walk(root_folder):
        folder = rex.search(root)
        if folder:
            folder = root
            return str(folder)
    return str(root)

def work_with_file(r : sr.Recognizer, source: sr.Microphone, language: str, file: str, extension: str, action: str = '', new_name: str = '', old_name: str = '', base_route: str = ''):
    match action:
        case 'open':
            for ext in extension:
                if os.path.exists(f'{file}{ext}'):
                    file = file + ext
                    os.startfile(file)
        case 'delete':
            for ext in extension:
                if os.path.exists(f'{file}{ext}'):
                    file = file + ext
                    os.remove(file)
        case 'rename':
            for ext in extension:
                if os.path.exists(f'{file}{ext}'):
                    old_name = old_name + ext
                    print('new name?')
                    new_name = f'{speak(r, source, language)[0]}{ext}'
                    os.rename(f'{base_route}//{old_name}', f'{base_route}//{new_name}')

def move_file(extension: list):
    origin = process_file('Dog','Accel World', 'move',ext=extension)
    destination = process_file('Dog','anime', 'move', ext=extension)
    for ext in extension:
        if os.path.exists(f'{origin}{ext}'):
            origin = f'{origin}{ext}'
            destination = f'{destination}{ext}'
            shutil.move(origin, destination)
            print(f'origin: {origin}')
            print(f'destination: {destination}')