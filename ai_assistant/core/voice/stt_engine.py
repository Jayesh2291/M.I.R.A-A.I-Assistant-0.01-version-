from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os

# Initialize model (update path in config.json)
model_path = os.path.join(os.path.dirname(__file__), "../../models/en-us")
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

def listen():
    mic = pyaudio.PyAudio().open(
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=8192
    )
    
    print("Speak now...")
    while True:
        data = mic.read(4096)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            return result.get("text", "").strip()