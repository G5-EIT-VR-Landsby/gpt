from openai import OpenAI
from env import Env
# import boto3
# from pydub import AudioSegment
# from pydub.playback import play
# import io
# import pyaudio
# from threading import Lock
from queue import Queue

class GPT:
    def __init__(self) -> None:
        self.client = OpenAI(
            organization=Env.organization,
            api_key=Env.api_key)

        self.stream_list_queue = []
        self.sentence_queue = Queue()
        
    def get_queue(self):
        return self.sentence_queue.get()
    
    def get_prompt(self, role_prompt, text_prompt): 
        stream = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": text_prompt}
        ],
            # max_tokens=60,
            stream=True
        )

        return stream

    # need a stream object from get_prompt
    def stream(self, stream):
        
        temp_msg_list = []
        self.stream_list_queue = []
        response_index = 0

        # Print out response while streaming from OpenAI
        for chunk in stream:
            word = chunk.choices[0].delta.content
            if word is not None:
                temp_msg_list.append(word)
                    
            # When we have collected a sentence from the stream, save it to response_msg.
            if len(temp_msg_list) > 0 and "." in temp_msg_list[-1]:
                self.stream_list_queue.append("".join(temp_msg_list))

                temp_msg_list.clear()

                # print(response_index, response_msg[response_index])

                # if len(response_msg) > 0:
                #     response_msg.pop(0)

                response_index += 1

        print(f"[GPT]: gpt request finished, sentences: {len(self.stream_list_queue)}")

        return self.stream_list_queue
    
    

if __name__ == "__main__":
    gpt = GPT()

    stream = gpt.get_prompt("du er en historie lærer", "Hvem vant 2 verdenskrig?")
    msg_list = gpt.stream(stream)
    print(gpt.stream_list_queue)


