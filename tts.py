import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 125)

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id) # female voice (1)

    def convert(self, text:str, filename: str="hello.mp3"):
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()

        print(f"Saved audio to {filename}")

if __name__ == "__main__":
    tts = TextToSpeech()
    tts.convert(text='The quick brown fox jumps over the lazy dog.', filename='hello.mp3')