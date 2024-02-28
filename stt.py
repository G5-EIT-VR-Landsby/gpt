from queue import Queue
from STT.whisper_live.client import TranscriptionClient


class STT:

    def __init__(self, debug) -> None:
        self.debug = debug
        self.client = TranscriptionClient(
                "localhost",
                9090,
                is_multilingual=True,
                # lang="en",
                translate=False,
                model="small"
            )
        self.sim_queue = Queue()

    def start(self):
        if self.debug:
            self.start_sim()
        else:
            # self.client = TranscriptionClient(
            #     "localhost",
            #     9090,
            #     is_multilingual=True,
            #     # lang="en",
            #     translate=False,
            #     model="small"
            # )
            self.client()


    def get_prompt(self):
        if self.debug:
            return self.sim_queue.get()
        
        return self.client.client.get_prompt()
    

    def start_sim(self):
        while True:
            self.sim_get_text()

    def sim_get_text(self):
        text_to_prompt = input("prompt: ")
        self.sim_queue.put(text_to_prompt)



