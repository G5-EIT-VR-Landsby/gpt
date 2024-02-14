from env import Env
import boto3
from pydub import AudioSegment
from pydub.playback import play
import io
import pyaudio

# boto3 variables
aws_access_key_id = 'AKIA6GBMHZV5KLEXLHXV'
aws_secret_access_key = '4ypAIaMN0mBCqZKgRSp4AeY6g4VllLhPUFIJCJyt'

region_name = 'eu-central-1'  # e.g., 'us-east-1'
voice_id = "Ida"

# Initialize Polly client
polly_client = boto3.client('polly', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Configure audio format and parameters
output_format = 'mp3'
sample_rate = 16000

# Initialize PyAudio
# p = pyaudio.PyAudio()

text_prompt_to_translate = "hei dette er en test."

response = polly_client.synthesize_speech(Text=text_prompt_to_translate, VoiceId=voice_id, OutputFormat=output_format,
                                        SampleRate=str(sample_rate), Engine='neural')


# Read audio raw from io object
audio_stream = AudioSegment.from_mp3(io.BytesIO(response['AudioStream'].read()))
# Play audio from audio_stream
play(audio_stream)

audio_stream.export("test.mp3", format="mp3")


