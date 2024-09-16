from google.cloud import texttospeech
from google.cloud import speech

def synthesize_speech(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content



def transcribe_audio(audio_file):
    client = speech.SpeechClient()
    with open(audio_file, 'rb') as audio:
        audio_content = audio.read()
    audio = speech.RecognitionAudio(content=audio_content)
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Ensure correct encoding
        sample_rate_hertz=16000,  # Set the correct sample rate
        language_code="en-US"
    )
    
    response = client.recognize(config=config, audio=audio)
    
    # Check if results are available
    if not response.results:
        return "No speech recognized."
    
    return response.results[0].alternatives[0].transcript



output = transcribe_audio("output.mp3")
print(output)