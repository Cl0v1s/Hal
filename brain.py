###
# Nick Bild
# February 2024
# https://github.com/nickbild/local_llm_assistant
#
# Be sure to start the LLM before running this script, e.g.:
# ./TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile
###

import gc
import pyaudio
import wave
from transformers import pipeline, MarianTokenizer, MarianMTModel, WhisperForConditionalGeneration
import sounddevice as sd
import torch
import numpy as np
import soundfile as sf
import torchaudio
import io
import whisper
from silero_vad import load_silero_vad, read_audio, get_speech_timestamps, VADIterator

device = sd.default.device[0]

def listen(record_secs = 3):
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 16000
    chunk = 1024
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
    return b''.join(frames)

# Load model in memory so it's always ready
whisper_model = whisper.load_model("small")
def understand(buffer):
    w=np.frombuffer(buffer, np.int16).flatten().astype(np.float32) / 32768.0 
    result = whisper_model.transcribe(w, language="fr")
    print("Transcription: {0}".format(result["text"]))
    return result["text"]

silvero = load_silero_vad()
def wait_for_call(name):
    was_called = False
    while was_called == False:
        buffer = listen(1.5)
        wav = torch.tensor(np.frombuffer(buffer, dtype=np.int16))
        speech_timestamps = get_speech_timestamps(
            wav,
            silvero,
            return_seconds=True,
        )
        if(len(speech_timestamps) > 0):
            if((speech_timestamps[0]["end"] - speech_timestamps[0]["start"]) <= 1):
                request = understand(buffer)
                was_called = (name.lower() in request.lower())

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

def get_syntax(request):
    syntaxer = pipeline(model="vblagoje/bert-english-uncased-finetuned-pos", aggregation_strategy="simple", device="cpu", torch_dtype=torch.float16)
    tokens=syntaxer(request)
    del syntaxer
    gc.collect()
    return tokens