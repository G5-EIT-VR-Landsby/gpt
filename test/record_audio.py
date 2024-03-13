import pyaudio
import wave
from pydub import AudioSegment
from pynput import keyboard
from io import BytesIO

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORDING_FLAG = False

AUDIO_FILE_PATH = "recording/"


# keboard callback fucntion
def on_release(key):
    global RECORDING_FLAG
    try:
        if key.char == "v":
            RECORDING_FLAG = False if RECORDING_FLAG else True
    
    except AttributeError:
        pass



def start_recording():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open the audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []

    print("start recording")
    # Record audio until stop flag is received
    while RECORDING_FLAG:
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    buffer = BytesIO()
    wf = wave.open(buffer, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Use pydub to convert audio to MP3
    filename = AUDIO_FILE_PATH + "recording.mp3"
    audio_segment = AudioSegment.from_wav(buffer)
    audio_segment.export(filename, format="mp3", bitrate="192k")

if __name__ == '__main__':
    listener = keyboard.Listener(
    on_release=on_release)
    listener.start()

    while True:
        if RECORDING_FLAG:
            start_recording()


    
