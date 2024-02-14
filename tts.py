from env import Env
import boto3
from pydub import AudioSegment
from pydub.playback import play
import io
# import pyaudio


class TTS:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name="eu-central-1", voice_id="Ida") -> None:
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.voice_id = voice_id

        # Initialize Polly client
        self.polly_client = boto3.client('polly', 
                                         region_name=region_name, 
                                         aws_access_key_id=aws_access_key_id, 
                                         aws_secret_access_key=aws_secret_access_key)


    def text_to_speach(self, text, output_format="mp3", sample_rate=16000):

        response = self.polly_client.synthesize_speech(Text=text, 
                                                       VoiceId=self.voice_id, 
                                                       OutputFormat=output_format,
                                                       SampleRate=str(sample_rate), 
                                                       Engine='neural')

        # Read audio raw from io object
        audio_stream = AudioSegment.from_mp3(io.BytesIO(response['AudioStream'].read()))
        return audio_stream
    
    @staticmethod
    def audio_to_file(audio_stream, filename):
        audio_stream.export(filename)

    @staticmethod
    def play_audio(audio_stream):
        play(audio_stream)

if __name__ == "__main__":
    tts = TTS(Env.aws_access_key_id, Env.aws_secret_access_key)
    test_text = "halla, dette er en test."
    audio_stream = tts.text_to_speach(test_text)
    tts.play_audio(audio_stream)


