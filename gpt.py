from queue import Queue
from openai import OpenAI
from env import Env
import base64

IMAGE_PRE_PROMPT = """
Answer this by creating a short text prompt for generating a realistic picture\
of a single example of an event or an object that can be used as input text for\
DALL·E 2 API. Do not start the prompt with the word "generate" only the description\
of the picture.
"""
IMAGE_ROLE_PROMPT = """\
You are a realisitc image creator, you only make realsitic drawings unless explicitly\
told otherwise.
"""

PROMPT_CONTEXTS = {
    "fagomraade": {"1": "You are a math teacher", "2": "You are a history teacher", "3": "You are a biology teacher"},
    "nivaa": {"1": ", in elementary school.", "2": ", in secondary school.", "3": ", in high school."},
    "svarlengde": {"1": "Give short answers of a maximum of 50 words", "2": "Give medium-long answers of a maximum of 100 words", "3": "Give long answers of a maximum of 200 words"}
}

class GPT:

    def __init__(self, organization, api_key) -> None:
        self.client = OpenAI(organization=organization, api_key=api_key)

        self.stream_queue = Queue()
        self.prompt_context = {
            "fagomraade": "1",
            "nivaa": "1",
            "svarlengde": "1"
        }

    # [start 1 2 3]
    def set_prompt_context(self, context_list):
        # print(context)
        # if context is None:
        #     return
        # if all(key in PROMPT_CONTEXTS for key in context):
        #     self.prompt_context = context
        if context_list is None:
            return
        
        self.prompt_context['fagomraade'] = context_list[0]
        self.prompt_context['nivaa'] = context_list[1]
        self.prompt_context['svarlengde'] = context_list[2]
        print(f"[set_prompt_context] new prompt_context: {self.prompt_context}")
        return


    def get_prompt_context(self):
        fagomraade = self.prompt_context["fagomraade"]
        nivaa = self.prompt_context["nivaa"]
        svarlengde = self.prompt_context["svarlengde"]
        return PROMPT_CONTEXTS["fagomraade"][fagomraade] + PROMPT_CONTEXTS["nivaa"][nivaa] + PROMPT_CONTEXTS["svarlengde"][svarlengde]

    def get_queue(self):
        return self.stream_queue.get()

    def get_text(self, role_prompt, text_prompt, stream=False):
        print("[gpt]: prompting.")
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": text_prompt},
            ],
            # max_tokens=60,
            stream=stream,
        )

        return response

    def generate_image(self, text_prompt):
        # print("IMAGE", text_prompt)

        gpt_image_text_response = self.get_text(
            text_prompt=text_prompt + IMAGE_PRE_PROMPT, role_prompt=IMAGE_ROLE_PROMPT
        )

        img_prompt = gpt_image_text_response.choices[0].message.content

        print("[GPT IMAGE]: IMAGE PROMPT:", img_prompt)

        response = self.client.images.generate(
            model="dall-e-3",
            prompt=img_prompt,
            size="1024x1024",
            quality="standard",
            response_format="b64_json",
            style="natural",
            n=1,
        )

        image_data = response.data[0].b64_json

        with open("images/image.png", "wb") as fh:
            fh.write(base64.b64decode(image_data))

        print("[gpt IMAGE]: Image has been saved.")

    # need a stream object from get_prompt
    def stream(self, role_prompt, text_prompt):
        stream = self.get_text(role_prompt, text_prompt, stream=True)

        temp_msg_list = []
        stream_list_queue = []
        queue_index = 0

        # Print out response while streaming from OpenAI
        print("[gpt]: starting stream: ")
        for chunk in stream:
            word = chunk.choices[0].delta.content
            if word is not None:
                temp_msg_list.append(word)

            # When we have collected a sentence from the stream, save it to response_msg.
            if len(temp_msg_list) > 0 and "." in temp_msg_list[-1]:
                stream_list_queue.append("".join(temp_msg_list))

                temp_msg_list.clear()

                # print(queue_index, stream_list_queue[queue_index])

                print("[gpt]: ", stream_list_queue[queue_index])
                # Add sentence to queue
                self.stream_queue.put(stream_list_queue[queue_index])

                queue_index += 1

        print(f"[GPT]: gpt request finished, sentences: {len(stream_list_queue)}")


if __name__ == "__main__":
    gpt = GPT(Env.gpt_organization, Env.gpt_api_key)
    
    # NOTE: in main these two functions run in seprate threads.
    gpt.stream("du er en historie lærer", "Hvem vant 2 verdenskrig?")
    gpt.generate_image("kan du fortelle meg lit tom 2 verdenskrig?")
