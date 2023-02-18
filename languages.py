import speech_recognition as sr

def speak(r : sr.Recognizer, source: sr.Microphone, lang: str):
    command = ''
    r.adjust_for_ambient_noise(source,duration=1)
    audio = r.listen(source)
    try:
        match lang:
            case 'esp':
                command = r.recognize_google(audio, language = 'es-ES')
                match command.lower():
                    case "inglés" | 'cambia a inglés' | 'idioma inglés':
                        print("Cambiando a Inglés")
                        lang = 'eng'
                
                    case "japonés":
                        print("Cambiando a Japonés")
                        lang = 'jap'
                    case _:
                        print(command)
                
            case  'default' |'eng':
                command = r.recognize_google(audio, language = 'en-UK')
                match command.lower():
                    case "spanish" | 'change to spanish' | 'go to spanish':
                        print("Going to Spanish")
                        lang = 'esp'
                    case "japanese":
                        print("Going to Japanese")
                        lang = 'jap'
                    case _:
                        print(command)
            case 'jap':
                command = r.recognize_google(audio, language = 'ja')
                match command:
                    case "スペイン語" | 'スペイン語へ変更' | '変更スペイン語':
                        print("スペイン語へ変更中。。。")
                        lang = 'esp'
                    case "英語":
                        print("英語へ変更中。。。")
                        lang = 'eng'
                    case _:
                        print(command)
                
            case _:
                print(command)
    except sr.UnknownValueError:
        print('no entendí')
                    
    except sr.RequestError:
        print('el servicio no funciona')
    return command, lang