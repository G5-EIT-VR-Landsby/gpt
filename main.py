from gpt import GPT
from tts import TTS
from stt_sim import STT_sim
import threading
from env import Env
import os

from STT.whisper_live.client import TranscriptionClient

# if debug we simulate 
DEBUG = 1

gpt = GPT(Env.gpt_organization, Env.gpt_api_key)
tts = TTS(Env.aws_access_key_id, Env.aws_secret_access_key)

stt_client = TranscriptionClient(
        "localhost",
        9090,
        is_multilingual=True,
        # lang="en",
        translate=False,
        model="small"
    )

# Simluate prompt generation
stt_sim = STT_sim()

def stt_sim_target():
    while True:
        stt_sim.get_text()

# gpt thread target
def gpt_target():
    while True:
        query_prompt = stt_client.client.get_prompt()
        if query_prompt:
            print(query_prompt)
            prompt_context = "du er en historielærer"
            gpt.stream(prompt_context, query_prompt)

# tts thread target
def tts_target():
    filname_index = 0

    while True:
        sentence_to_text = gpt.get_queue()
        audio_stream = tts.text_to_speach(sentence_to_text)
        tmp_filename = "audio_files/tmp" + str(filname_index) + ".mp3"
        filname_finished = "audio_files/" + str(filname_index) + "_done" + ".mp3"

        # play audio
        tts.play_audio(audio_stream=audio_stream)

        audio_stream.export(tmp_filename)
        os.rename(tmp_filename, filname_finished)
        
        filname_index += 1


# sst_client thread gpt_target
def stt_target():
    if DEBUG:
        stt_sim_target()
    else:
        stt_client()


if __name__ == "__main__":

    thread_functions = [stt_target, gpt_target, tts_target]


    threads = []
    for func in thread_functions:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()
    # join
    for th in threads:
        th.join()

