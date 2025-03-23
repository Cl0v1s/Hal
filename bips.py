import pyaudio
import wave

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

def playListen():
    play("fx/listen.wav")

def playError():
    play("fx/error.wav")

def playOk():
    play("fx/ok.wav")

def playSad():
    play("fx/sad.wav")