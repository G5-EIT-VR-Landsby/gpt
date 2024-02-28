from queue import Queue
from openai import OpenAI
from env import Env
# import boto3
# from pydub import AudioSegment
# from pydub.playback import play
# import io
# import pyaudio
from threading import Lock

class GPT:

    def __init__(self, organization, api_key) -> None:
        self.client = OpenAI(
            organization=organization,
            api_key=api_key)

        self.stream_queue = Queue()

        
    def get_queue(self):
        return self.stream_queue.get()
        

    def prompt(self, role_prompt, text_prompt): 
        #Fagområde_dict = {"1": "Du er en mattelærer", "2": "Du er en geografilærer", "3": "Du er en fysikklærer"}
        #Nivå_dict = {"1": ", på barneskolenivå.", "2": ", på ungdomsskolenivå.", "3": ", på videregåendenivå."}
        #Svarlengde_dict = {"1": "Gi korte svar på maks 50 ord", "2": "Gi medium lange svar på maks 100 ord", "3": "Gi langde svar på maks 200 ord"}
        stream = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        #    {"role": "system", "content": Fagområde_dict[role_prompt[0]]+ Nivå_dict[role_prompt[1]]+ Svarlengde_dict[role_prompt[2]]},
            {"role": "system", "content": role_prompt},         
            {"role": "user", "content": text_prompt}
        ],
            # max_tokens=60,
            stream=True
        )

        return stream

    # need a stream object from get_prompt
    def stream(self, role_prompt, text_prompt):

        stream = self.prompt(role_prompt, text_prompt)
        
        temp_msg_list = []
        stream_list_queue = []
        queue_index = 0

        # Print out response while streaming from OpenAI
        for chunk in stream:
            word = chunk.choices[0].delta.content
            if word is not None:
                temp_msg_list.append(word)
                    
            # When we have collected a sentence from the stream, save it to response_msg.
            if len(temp_msg_list) > 0 and "." in temp_msg_list[-1]:
                stream_list_queue.append("".join(temp_msg_list))

                temp_msg_list.clear()

                # print(queue_index, stream_list_queue[queue_index])

                # Add sentence to queue
                self.stream_queue.put(stream_list_queue[queue_index])

                queue_index += 1

        print(f"[GPT]: gpt request finished, sentences: {len(stream_list_queue)}")

        # return stream_list_queue
    
    

if __name__ == "__main__":
    gpt = GPT()

    stream = gpt.stream("du er en historie lærer", "Hvem vant 2 verdenskrig?")


