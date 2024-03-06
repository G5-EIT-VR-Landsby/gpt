from queue import Queue
from openai import OpenAI
from env import Env
from threading import Lock
import base64


class GPT:

    def __init__(self, organization, api_key) -> None:
        self.client = OpenAI(organization=organization, api_key=api_key)

        self.stream_queue = Queue()
        self.prompt_context = ""


    def get_queue(self):
        return self.stream_queue.get()

    def prompt(self, role_prompt, text_prompt):
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": text_prompt},
            ],
            # max_tokens=60,
            stream=True,
        )

        return stream

    def image(self, text_prompt):
        print("IMAGE", text_prompt)
        specific_prompt = '\n Answer this by creating a short text prompt for generating a realistic picture of a single example of an event or an object that can be used as input text for DALL·E 2 API. Do not start< the prompt with the word "generate" only the description of the pictureæ'
        full_prompt = text_prompt + specific_prompt

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": full_prompt},
            ],
            # max_tokens=60,
        )

        img_prompt = response.choices[0].message.content

        print("IMAGE PROMPT:", img_prompt)

        response = self.client.images.generate(
            model="dall-e-3",
            prompt=img_prompt,
            size="1024x1024",
            quality="standard",
            response_format="b64_json",
            style="natural",
            n=1
            )

        image_data = response.data[0].b64_json

        with open("images/image.png", "wb") as fh:
            fh.write(base64.b64decode(image_data))

        print("Image has been saved.")

        

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

if __name__ == "__main__":
    gpt = GPT(Env.gpt_organization, Env.gpt_api_key)

    stream = gpt.stream("du er en historie lærer", "Hvem vant 2 verdenskrig?")
