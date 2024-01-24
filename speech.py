
from gtts import gTTS
from io import BytesIO
import pygame

class Speech():

    @classmethod
    def speak(cls, text):
        mp3_file_object = BytesIO()
        tts = gTTS(text, lang='en')
        tts.write_to_fp(mp3_file_object)
        tts.save("test_audio")

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file_object, 'mp3')
        pygame.mixer.music.play()
