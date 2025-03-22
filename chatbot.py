###
# Nick Bild
# February 2024
# https://github.com/nickbild/local_llm_assistant
#
# Be sure to start the LLM before running this script, e.g.:
# ./TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile
###

import gc
from openai import OpenAI
import pyaudio
import wave
import whisper
from transformers import pipeline, BertForTokenClassification, AutoTokenizer, MarianTokenizer, MarianMTModel
import sounddevice as sd

device = sd.default.device[0]

def record_wav():
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 16000
    chunk = 1024
    record_secs = 3
    wav_output_filename = 'input.wav'

    audio = pyaudio.PyAudio()

    # Create pyaudio stream.
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = device,input = True, \
                        frames_per_buffer=chunk)
    print("recording")
    frames = []
    # Loop through stream and append audio chunks to frame array.
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)
    print("finished recording")
    # Stop the stream, close it, and terminate the pyaudio instantiation.
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # Save the audio frames as .wav file.
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    return

def getCurrentMemoryUsage():
    ''' Memory usage in kB '''

    with open('/proc/self/status') as f:
        memusage = f.read().split('VmRSS:')[1].split('\n')[0]
    return memusage.strip()

def listen():
    model = whisper.load_model("base")
    record_wav()
    result = model.transcribe("input.wav")
    print("Transcription: {0}".format(result["text"]))
    del model
    gc.collect()
    return result["text"]

def translate(request):
    tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
    model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
    translated = model.generate(**tokenizer([request], return_tensors="pt", padding=True))
    request=tokenizer.decode(translated[0], skip_special_tokens=True)
    del model
    gc.collect()
    return request

def get_emotion(request):
    emotion_detector = pipeline("text-classification", model="gokuls/BERT-tiny-emotion-intent", device="cpu")
    emotion = emotion_detector(request)
    del emotion_detector
    gc.collect()
    return emotion

def get_intent(request):
    intent_detector = pipeline("text-classification", model="./tinybert_finetuned", device="cpu")
    intent = intent_detector(request)
    del intent_detector
    gc.collect()
    return intent

def get_syntax(request):
    syntaxer = pipeline(model="vblagoje/bert-english-uncased-finetuned-pos", aggregation_strategy="simple", device="cpu")
    tokens=syntaxer(request)
    del syntaxer
    gc.collect()
    return tokens

def main():
    request = listen()
    request = translate(request)

    print(request)
    print(get_emotion(request))
    print(get_intent(request))
    print(get_syntax(request))

if __name__ == "__main__":
    print("Ready...")
    while(True):
        input("Press enter to start")
        # if GPIO.input(BUTTON) == GPIO.LOW:
        main()

