import speech_recognition as sr
import os
import webbrowser
import playsound
import subprocess
import time
import random
from gtts import gTTS
from time import ctime

r = sr.Recognizer()


def record_audio():
    with sr.Microphone() as source:
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, my speech service is down')
        return voice_data


def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 100000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(f"Bleh: {audio_string}")
    os.remove(audio_file)


def respond(voice_data):
    if 'what is your name' in voice_data:
        print('My name is Bleh')
    if 'search' in voice_data:
        if 'YouTube' in voice_data:
            search_term = voice_data.split("for")[-1]
            speak('Searching YouTube')
            url = f"https://www.youtube.com/results?search_query={search_term}"
        else:
            search_term = voice_data.split("for")[-1]
            speak('Searching Google')
            url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
    if 'open' in voice_data:
        app = voice_data.split("open ")[-1]
        app = app.title()
        speak('Opening {}'.format(app))
        os.system("""osascript -e 'tell application "{}" to activate'""".format(app))
    if 'close' in voice_data:
        app = voice_data.split("close ")[-1]
        app = app.title()
        speak('Closing {}'.format(app))
        os.system("pkill {}".format(app))
    if 'time' in voice_data:
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        speak(time)
    if 'exit' in voice_data:
        speak('Exiting')
        exit()


time.sleep(1)
speak('Hello i am Bleh. How,can i help you ?')
while 1:
    voice_data = record_audio()
    print(voice_data)
    respond(voice_data)
