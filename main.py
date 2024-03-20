from gpt import GPT
from tts import TTS

from stt import STT
import threading
from env import Env
import os
from udp_server import Server
from gpt_stt import STT
from pynput import keyboard

# Config variables
DEBUG = 1
audio_file_dir_path = "audio_files/"

# Ai model objects
gpt = GPT(Env.gpt_organization, Env.gpt_api_key)
tts = TTS(Env.aws_access_key_id, Env.aws_secret_access_key)
# stt = STT(DEBUG)
stt = STT(Env.gpt_organization, Env.gpt_api_key)
udp_server = Server()


# gpt thread target
def gpt_target():
    while True:
        query_prompt = (
            stt.get_prompt()
        )  # this will wait untiil we have a prompt in sst.Queue
        print("[gpt]: got prompt")
        gpt.set_prompt_context(udp_server.global_context)
        prompt_context = gpt.get_prompt_context()
        gpt.stream(prompt_context, query_prompt)
        print("[gpt]: got through stream")

        # Create image from context.
        img_thread = threading.Thread(target=gpt.generate_image, args=(query_prompt,))
        img_thread.start()
        # stream_thread.start()


# tts thread target
def tts_target():
    filname_index = 1

    while True:
        sentence_to_text = gpt.get_queue()
        audio_stream = tts.text_to_speach(sentence_to_text)

        # audio file name, FIXME: make function in tts?
        tmp_filename = audio_file_dir_path + "tmp" + str(filname_index) + ".mp3"
        filname_finished = audio_file_dir_path + str(filname_index) + "_done" + ".mp3"

        audio_stream.export(tmp_filename, format="mp3")
        # rename after exported
        os.rename(tmp_filename, filname_finished)

        # play audio
        tts.play_audio(audio_stream=audio_stream)
        filname_index += 1


# stt thread target (this is stt client side)
def stt_target():
    listener = keyboard.Listener(on_release=stt.on_release)
    listener.start()
    stt.start()


#  Udp server
def udp_server_target():
    udp_server.start()


if __name__ == "__main__":
    thread_functions = [stt_target, gpt_target, tts_target, udp_server_target]

    threads = []
    for func in thread_functions:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()

    # join
    for th in threads:
        th.join()
