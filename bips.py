import pyaudio
import wave
import eyes
import random
import re

import os 

def say(text):
    eyes.get_instance().anim_laugh()
    eyes.get_instance().write(re.sub(r'<.+?/?>', '', text).encode("utf-8"))
    os.system('espeak -v en+f4 -m -p 10 -s 150 "{0}" 2>/dev/null'.format(text))

def play(filename):
    chunk = 1024 
    file = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(file.getsampwidth()),
                    channels = file.getnchannels(),
                    rate = file.getframerate(),
                    output = True)
    data = file.readframes(chunk)
    while data != b'':
        stream.write(data)
        data = file.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()

def playGonk():
    v = random.randint(1, 2)
    play("fx/gonk"+ str(v) + ".wav")

def playListen():
    play("fx/listen.wav")

def playError():
    play("fx/error.wav")

def playOk():
    play("fx/ok.wav")

def playSad():
    play("fx/sad.wav")

if __name__ == "__main__":
    say("Temperature: <prosody pitch='120'>10</prosody>; Wind: <prosody pitch='120'>10 kilometer per hour</prosody>")