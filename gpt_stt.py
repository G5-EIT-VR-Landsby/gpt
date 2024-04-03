from queue import Queue
from openai import OpenAI
from env import Env

import pyaudio
import wave
from pydub import AudioSegment
from pynput.keyboard import Key
# from pynput import keyboard
from io import BytesIO

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORDING_FLAG = False
AUDIO_FILE_PATH = "recording/"
FILENAME = AUDIO_FILE_PATH + "recording.mp3"

class STT:
    def __init__(self, organization, api_key) -> None:
        self.queue = Queue()
        self.client = OpenAI(organization=organization, api_key=api_key)
        self.recording = False


    def getTextFromAudio(self, audio_file):
        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="no"
        )
        transcription = response.text
        return transcription

    # This is for pynput (mabye get this flag otherwise? )
    def on_release(self, key):
        try:
            if key.char == "v":
                self.recording = False if self.recording else True
        
        except AttributeError:
            pass

    def record_audio(self):
        # Initialize PyAudio
        audio = pyaudio.PyAudio()

        # Open the audio stream
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        frames = []

        print("start recording")
        # Record audio until stop flag is received
        while self.recording:
            data = stream.read(CHUNK)
            frames.append(data)

        print("Recording finished.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        wave_buffer = BytesIO()
        wf = wave.open(wave_buffer, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        wave_audio_segment = AudioSegment.from_wav(wave_buffer)
        wave_audio_segment.export(FILENAME, format="mp3")
        return FILENAME

    def get_prompt(self):
        return self.queue.get()

    def start(self):

        while True:
            if self.recording:
                filename = self.record_audio()
                # TODO: fix buffer sending or save as file and then upload.
                audio_file = open(filename, "rb")
                text = self.getTextFromAudio(audio_file)
                audio_file.close()
                print("[stt]: got text from gpt: ", text)
                self.queue.put(text)

if __name__ == "__main__":
    stt = STT(Env.gpt_organization, Env.gpt_api_key)
    
    stt.start()

