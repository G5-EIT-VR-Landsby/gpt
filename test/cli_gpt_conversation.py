from openai import OpenAI
from env import Env
import boto3
from pydub import AudioSegment
from pydub.playback import play
import io
import pyaudio

# boto3 env variables
aws_access_key_id = 'AKIA6GBMHZV5KLEXLHXV'
aws_secret_access_key = '4ypAIaMN0mBCqZKgRSp4AeY6g4VllLhPUFIJCJyt'
region_name = 'eu-central-1'  # e.g., 'us-east-1'

client = OpenAI(
    organization=Env.organization,
    api_key=Env.api_key

)

# Initialize Polly client
polly_client = boto3.client('polly', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Configure audio format and parameters
output_format = 'mp3'
sample_rate = 16000

# Initialize PyAudio
p = pyaudio.PyAudio()

def main(text_prompt, voice_id='Ida', region_name='eu-central-1'):


    stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Du er en hisorielærer som underviser om andre verdenskrig. "},
        {"role": "user", "content": text_prompt}
    ],
        max_tokens=60,
        stream=True
    )
    
    temp_msg_list = []
    response_msg = []
    response_index = 0

    # Print out response while straming from OpenAI
    for chunk in stream:
        word = chunk.choices[0].delta.content
        if word is not None:
            temp_msg_list.append(word)
                
        if len(temp_msg_list) > 0 and "." in temp_msg_list[-1]:
            response_msg.append("".join(temp_msg_list))

            temp_msg_list.clear()

            print(response_msg[response_index])
            # made chunk in response msg
            response = polly_client.synthesize_speech(Text=response_msg[0], VoiceId=voice_id, OutputFormat=output_format,
                                                    SampleRate=str(sample_rate), Engine='neural')

            
            # Load the audio stream with pydub
            audio_stream = AudioSegment.from_mp3(io.BytesIO(response['AudioStream'].read()))
 
            play(audio_stream)

            # if len(response_msg) > 0:
            #     response_msg.pop(0)

            response_index += 1


if __name__ == "__main__":
    inp = ""

    while inp != "exit":
        inp = input("> ")
        main(inp)

    p.terminate()

