from enum import auto
from openai import OpenAI
from openai.resources.beta.threads.messages import messages
from env import Env
from pathlib import Path
import os


speech_file_path = Path(__file__).parent / "speech.mp3"

client = OpenAI(
)


stream = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ],
    max_tokens=50,
    stream=False
)
# print while straming from OpenAI
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")
#
message = stream.choices[0].message

print(message.content)

audio = client.audio.speech.create(
    input=str(message.content),
    voice="shimmer",
    response_format="mp3",
    model="tts-1"
)
print("trying to write to file: ", speech_file_path)
audio.stream_to_file(speech_file_path)

