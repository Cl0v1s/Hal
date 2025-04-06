import gc
import pyaudio
from transformers import pipeline, MarianTokenizer, MarianMTModel
import sounddevice as sd
import torch
import numpy as np
import whisper
import os
from eff_word_net.streams import SimpleMicStream
from eff_word_net.engine import HotwordDetector

from eff_word_net.audio_processing import Resnet50_Arc_loss

from eff_word_net import samples_loc


device = sd.default.device[0]

def listen(record_secs = 3):
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 16000
    chunk = 1024

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
    return frames

# Load model in memory so it's always ready
whisper_model = whisper.load_model("small")
def understand(buffer):
    w = np.frombuffer(b''.join(buffer), np.int16).flatten().astype(np.float32) / 32768.0 
    result = whisper_model.transcribe(w, language="fr")
    print("Transcription: {0}".format(result["text"]))
    return result["text"]

base_model = Resnet50_Arc_loss()
name_files = os.listdir("name")
reference_file = [name for name in name_files if name.endswith("_ref.json")]
if(len(reference_file) == 0):
    raise Exception("You must train this system with a hotword, please run 'invoke learnName <name>'")
reference_file = reference_file[0]
def wait_for_call():
    mycroft_hw = HotwordDetector(
        hotword=reference_file.replace('_ref.json', ''),
        model = base_model,
        reference_file=os.path.join("name", reference_file),
        threshold=0.7,
        relaxation_time=2
    )
    mic_stream = SimpleMicStream(
        window_length_secs=1.5,
        sliding_window_secs=0.75,
    )
    mic_stream.start_stream()
    called = False
    while called == False:
        frame = mic_stream.getFrame()
        result = mycroft_hw.scoreFrame(frame)
        print(result)
        if(result != None and result["match"]):
            print("Wakeword uttered",result["confidence"])
            called = True
    mic_stream.close_stream()


def translate(request):
    tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
    model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
    translated = model.generate(**tokenizer([request], return_tensors="pt", padding=True))
    request=tokenizer.decode(translated[0], skip_special_tokens=True)
    del model
    gc.collect()
    return request

def get_emotion(request):
    emotion_detector = pipeline("text-classification", model="gokuls/BERT-tiny-emotion-intent", device="cpu", torch_dtype=torch.float16)
    emotion = emotion_detector(request)
    del emotion_detector
    gc.collect()
    return emotion

def get_intent(request):
    intent_detector = pipeline("text-classification", model="./tinybert_finetuned", device="cpu", torch_dtype=torch.float16)
    intent = intent_detector(request)
    del intent_detector
    gc.collect()
    return intent

def think(question, context):
    thinker = pipeline("question-answering", model="dewdev/dynamic_tinybert", device="cpu", torch_dtype=torch.float16)
    answer = thinker(question=question, context=context)
    del thinker
    gc.collect()
    return answer

def get_syntax(request):
    syntaxer = pipeline(model="vblagoje/bert-english-uncased-finetuned-pos", aggregation_strategy="simple", device="cpu", torch_dtype=torch.float16)
    tokens=syntaxer(request)
    del syntaxer
    gc.collect()
    return tokens