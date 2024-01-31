
import boto3
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import io
import pyaudio
from env import Env

client = OpenAI( 
    organization=Env.organization,
    api_key=Env.api_key

)
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Du er en norsk lærer som underviser i økonomi"},
    {"role": "user", "content": "Forklar meg hva sharpe-ratio er med tre setninger"}
  ]
)

print(completion.choices[0].message)

"""speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1-hd",
  voice="onyx",
  input=completion.choices[0].message.content
)

response.stream_to_file(speech_file_path)"""

# Replace 'your_access_key_id' and 'your_secret_access_key' with your actual AWS credentials
aws_access_key_id = 'AKIA6GBMHZV5KLEXLHXV'
aws_secret_access_key = '4ypAIaMN0mBCqZKgRSp4AeY6g4VllLhPUFIJCJyt'
region_name = 'eu-central-1'  # e.g., 'us-east-1'

"""# Initialize the Polly client
polly_client = boto3.client('polly', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Specify the text you want to convert to speech
text_to_speak = completion.choices[0].message.content

# Specify the voice you want to use
voice_id = 'Ida'  # You can find a list of available voices here: https://docs.aws.amazon.com/polly/latest/dg/voicelist.html

# Use the Polly client to synthesize speech
response = polly_client.synthesize_speech(Text=text_to_speak, VoiceId=voice_id, OutputFormat='mp3', Engine='neural')

# Save the audio stream to a file
with open('output.mp3', 'wb') as file:
    file.write(response['AudioStream'].read())"""

def stream_audio_from_polly(text_to_speak, voice_id='Ida', region_name='eu-central-1'):
    # Initialize Polly client
    polly_client = boto3.client('polly', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Configure audio format and parameters
    output_format = 'mp3'
    sample_rate = 16000

    # Split the text into smaller chunks (adjust as needed)
    chunk_size = 30
    text_chunks = [text_to_speak[i:i + chunk_size] for i in range(0, len(text_to_speak), chunk_size)]


    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Iterate over text chunks and stream audio
    for text_chunk in text_chunks:
        # Synthesize speech using Polly
        response = polly_client.synthesize_speech(Text=text_chunk, VoiceId=voice_id, OutputFormat=output_format,
                                                  SampleRate=str(sample_rate), Engine='neural')

        # Load the audio stream with pydub
        audio_stream = AudioSegment.from_mp3(io.BytesIO(response['AudioStream'].read()))

        # Play the audio using pydub's playback module
        play(audio_stream)

    # Clean up resources
    p.terminate()

if __name__ == "__main__":
    # Replace 'your_aws_region' with your actual AWS region
    aws_region = 'eu-central-1'

    # Specify the text you want to synthesize and stream
    text_to_speak = completion.choices[0].message.content

    # Optional: Specify the desired Polly voice (default is Joanna)
    polly_voice = 'Ida'

    # Stream audio from Polly
    stream_audio_from_polly(text_to_speak, voice_id=polly_voice, region_name=aws_region)





   


