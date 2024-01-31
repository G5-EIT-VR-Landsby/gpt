from openai import OpenAI
from openai.resources.audio import audio, speech
from env import Env
from pathlib import Path
from threading import Thread, Lock
import boto3
from pydub import AudioSegment
from pydub.playback import play
import io
from pydub.playback import play
import pyaudio

queue_lock = Lock()
speech_lock = Lock()
# start by acquire to get text before audio
speech_lock.acquire()

speech_file_path = Path(__file__).parent / "speech.mp3"

aws_access_key_id = 'AKIA6GBMHZV5KLEXLHXV'
aws_secret_access_key = '4ypAIaMN0mBCqZKgRSp4AeY6g4VllLhPUFIJCJyt'
region_name = 'eu-central-1'  # e.g., 'us-east-1'

client = OpenAI(
    organization=Env.organization,
    api_key=Env.api_key

)
test_prompt = "Lag et kort dikt som handler om hvordan andre verdenskrig ustplillte seg."


response_msg = []
def get_text(text_prompt):

    stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Du er en hisorielærer som underviser om andre verdenskrig. "},
        {"role": "user", "content": text_prompt}
    ],
        max_tokens=50,
        stream=True
    )
    
    temp_msg_list = []

    # Print out response while straming from OpenAI
    for chunk in stream:
        word = chunk.choices[0].delta.content
        if word is not None:
            temp_msg_list.append(word)
        
        # Divide text into chunks
        if len(temp_msg_list) > 5:
            response_msg.append("".join(temp_msg_list))

            temp_msg_list.clear()

            # print(response_msg)
            # speech_lock.release()

    print(response_msg)


def stream_audio_from_polly(voice_id='Ida', region_name='eu-central-1'):
    # Initialize Polly client
    polly_client = boto3.client('polly', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Configure audio format and parameters
    output_format = 'mp3'
    sample_rate = 16000

    # Split the text into smaller chunks (adjust as needed)
    # chunk_size = 30
    # text_chunks = [text_to_speak[i:i + chunk_size] for i in range(0, len(text_to_speak), chunk_size)]


    # Initialize PyAudio
    # p = pyaudio.PyAudio()

    # Iterate over text chunks and stream audio
    speech_lock.acquire()

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    while len(response_msg) > 0:    
        response = polly_client.synthesize_speech(Text=response_msg[0], VoiceId=voice_id, OutputFormat=output_format,
                                                  SampleRate=str(sample_rate), Engine='neural')

        
        # Load the audio stream with pydub
        audio_stream = AudioSegment.from_mp3(io.BytesIO(response['AudioStream'].read()))

        play(audio_stream)

        response_msg.remove(0)

    p.terminate()

if __name__ == '__main__':
    gpt_thread = Thread(target = get_text, args=(test_prompt, ))
    # speech_thread = Thread(target=stream_audio_from_polly)

    gpt_thread.start()
    # speech_thread.start()
    # speech_thread.join()
    gpt_thread.join()

