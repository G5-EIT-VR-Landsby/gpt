from queue import Queue
from env import Env


class STT_sim:

    def __init__(self) -> None:
        self.queue = Queue()

    def get_queue(self):
        return self.queue.get()
    
    def get_text(self):
        text_to_prompt = input("prompt: ")
        self.queue.put(text_to_prompt)

        



