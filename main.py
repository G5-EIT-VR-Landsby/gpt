from gpt import GPT
from tts import TTS
from stt_sim import STT
import threading
# import time
from env import Env


gpt = GPT(Env.organization, Env.api_key)
tts = TTS(Env.aws_access_key_id, Env.aws_secret_access_key)

# TODO:
stt = STT()

def sst_target():
    while True:
        stt.get_text()

def gpt_target():
    while True:
        query_prompt = stt.get_queue()
        gpt.stream("du er en historielærer", query_prompt)


def tts_target():
    filname_index = 0

    while True:
        sentence_to_text = gpt.get_queue()
        audio_stream = tts.text_to_speach(sentence_to_text)
        filename = "audio_files/audio" + str(filname_index) + ".mp3"

        # play audio
        tts.play_audio(audio_stream=audio_stream)

        audio_stream.export(filename)
        filname_index += 1

if __name__ == "__main__":

    thread_functions = [sst_target, gpt_target, tts_target]


    threads = []
    for func in thread_functions:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()
    # join
    for th in threads:
        th.join()

        
    

