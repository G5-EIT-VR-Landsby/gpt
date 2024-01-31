import os
from pathlib import Path
from openai import OpenAI
from env import Env

speech_file_path = Path(__file__).parent / "speech.mp3"

client = OpenAI(
    organization=Env.organization,
    api_key=Env.api_key

)

stream = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ],
    max_tokens=50,
    stream=True
)

not_allowd_speach = [",", ".", " ", "\n", ", ", ". ", "  ", "\n "]
# Print out response while straming from OpenAI
i = 0
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
 
        word = chunk.choices[0].delta.content
        if word not in not_allowd_speach:
            print(i,len(word), word)
            i += 1
            # Speech.speak(word)


