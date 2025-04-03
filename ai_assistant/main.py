import json
import os
import time
from core.voice.wake_word import WakeWordDetector
from core.voice.stt_engine import listen
from core.voice.tts_engine import speak
from core.brain.processor import process_command
from core.brain.memory import Memory
from utils.logger import setup_logger

class AIAssistant:
    def __init__(self):
        # Load configuration
        with open("config.json") as f:
            self.config = json.load(f)
        
        # Initialize components
        self.logger = setup_logger(self.config["log_file"])
        self.memory = Memory(self.config["memory_file"])
        self.wake_detector = WakeWordDetector(self.config["wake_word"])
        
        # Ensure backup directory exists
        os.makedirs(self.config["backup_path"], exist_ok=True)

    def run(self):
        try:
            self.logger.info("AI Assistant starting up")
            speak("Assistant initialized. Ready for commands.")
            
            while True:
                try:
                    # Wait for wake word
                    print(f"\n🔊 Listening for wake word '{self.config['wake_word']}'...")
                    if not self.wake_detector.listen_for_wake_word():
                        break  # Exit if interrupted
                    
                    # Process command
                    speak("Yes? How can I help?")
                    print("[Listening for command...]")
                    command = listen()
                    
                    if command:
                        self.logger.info(f"Command received: {command}")
                        response = process_command(command, self.memory)
                        self.memory.save(command, response)
                        speak(response)
                    else:
                        speak("I didn't catch that. Please try again.")
                        
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    self.logger.error(f"Command processing error: {str(e)}")
                    speak("Sorry, I encountered an error. Please try again.")
                    time.sleep(1)  # Prevent rapid error looping

        except KeyboardInterrupt:
            self.logger.info("Assistant shutting down by user request")
            speak("Goodbye!")
        except Exception as e:
            self.logger.critical(f"Fatal error: {str(e)}")
            speak("Critical error! Assistant is shutting down.")
        finally:
            self.wake_detector.cleanup()
            self.logger.info("Assistant shutdown complete")

if __name__ == "__main__":
    assistant = AIAssistant()
    assistant.run()