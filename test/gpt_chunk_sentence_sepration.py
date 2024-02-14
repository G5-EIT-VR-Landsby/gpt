from openai import OpenAI
from env import Env
import boto3
from pydub import AudioSegment
from pydub.playback import play
import io
import pyaudio


# OpenAI client connection
client = OpenAI(
    organization=Env.organization,
    api_key=Env.api_key
)

# Test Prompts
test_prompt = "Hva er ost?"
test_role_prompt = "Du er en hisorielærer som underviser om andre verdenskrig. "

def get_prompt(client, role_prompt, text_prompt): 
    stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": role_prompt},
        {"role": "user", "content": text_prompt}
    ],
        # max_tokens=60,
        stream=True
    )
    return stream


def stream_gpt():

    stream = get_prompt(client, test_role_prompt, test_prompt)
    
    temp_msg_list = []
    response_msg = []
    response_index = 0

    # Print out response while streaming from OpenAI
    for chunk in stream:
        word = chunk.choices[0].delta.content
        if word is not None:
            temp_msg_list.append(word)
                
        # When we have collected a sentence from the stream, save it to response_msg.
        if len(temp_msg_list) > 0 and "." in temp_msg_list[-1]:
            response_msg.append("".join(temp_msg_list))

            temp_msg_list.clear()

            # print(response_index, response_msg[response_index])

            # if len(response_msg) > 0:
            #     response_msg.pop(0)

            response_index += 1

    print(f"[Info]: gpt request finished, sentences: {len(response_msg)}")

if __name__ == "__main__":
    stream_gpt()


