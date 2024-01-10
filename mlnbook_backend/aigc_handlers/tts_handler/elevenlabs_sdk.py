from elevenlabs import set_api_key
from elevenlabs import generate, play, Voice, VoiceSettings

set_api_key("xxx")
audio = generate(
    text="Hello! My name is Bella.",
    voice=Voice(
        voice_id='jBpfuIE2acCO8z3wKNLl',
        settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
    )
)

play(audio)
