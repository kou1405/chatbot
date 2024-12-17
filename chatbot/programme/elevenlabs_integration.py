from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, play, stream

def generate_and_stream_audio(text, api_key="baaf0ae7108c8b16ebab470efaa9e4cb", model="eleven_multilingual_v2"):
    client = ElevenLabs(api_key=api_key)
    audio_stream = client.generate(text=text, stream=True, model=model)
    stream(audio_stream)

if __name__ == "__main__":
    generate_and_stream_audio("Bonjour, comment puis-je vous aider ?")
