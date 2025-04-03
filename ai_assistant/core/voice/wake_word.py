import pvporcupine
import pyaudio
import struct
import logging

class WakeWordDetector:
    def __init__(self, wake_word="jarvis"):
        self.wake_word = wake_word.lower()
        self.access_key = "xCnfSx/RWQuZ5Li7xfLpWjPlRsJvazt2DmH1LdUpN19df1w+tsmGDA=="  # REPLACE WITH YOUR KEY
        self.porcupine = None
        self.audio = None
        self.stream = None
        
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keywords=[self.wake_word]
            )
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length,
                input_device_index=None  # Use default microphone
            )
            logging.info(f"Wake word detector ready for '{self.wake_word}'")
        except Exception as e:
            logging.error(f"Wake word init failed: {str(e)}")
            raise

    def listen_for_wake_word(self):
        try:
            while True:
                pcm = self.stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                if self.porcupine.process(pcm) >= 0:
                    return True
        except KeyboardInterrupt:
            return False
        except Exception as e:
            logging.error(f"Wake word detection error: {str(e)}")
            raise

    def cleanup(self):
        if hasattr(self, 'stream') and self.stream:
            self.stream.close()
        if hasattr(self, 'audio') and self.audio:
            self.audio.terminate()
        if hasattr(self, 'porcupine') and self.porcupine:
            self.porcupine.delete()
        logging.info("Wake word resources released")