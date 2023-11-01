import openai
import time
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, ResultReason, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import simpleaudio as sa

# Set your Azure Speech Service credentials
speech_key = "AZURE_KEY"
service_region = "eastus"
# Set your OpenAI API key
openai.api_key = "OPENAI_KEY"

speech_config = SpeechConfig(subscription=speech_key, region=service_region)

def transcribe_audio():
    audio_config = AudioConfig(use_default_microphone=True)
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print("Speak into your microphone.")
    result = recognizer.recognize_once()

    if result.reason == ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"Speech Recognition was canceled: {cancellation.reason}")
        if cancellation.reason == ResultReason.Error:
            print(f"Error details: {cancellation.error_details}")
    return ""

def get_gpt_response(prompt):
    prompt = f"Imagine you're an excited guinea pig named Maple, who loves to eat. Respond with humor to: '{prompt}'"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=80)
    # Let's add Maple's personal touch to every response
    return response.choices[0].text.strip()

def synthesize_speech(text):
    # Set the voice using the speech_synthesis_voice_name attribute
    speech_config.speech_synthesis_voice_name = "en-US-AmberNeural"

    audio_config = AudioOutputConfig(filename="response.wav")
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason != ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesis failed with status {result.reason}, check details: {result.error_details}")

    return "response.wav"



if __name__ == '__main__':
    while True:
        user_input = transcribe_audio()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye from Maple! She hopes to wheek at you again soon!")
            break
        print(f"You said: {user_input}")
        response_text = get_gpt_response(user_input)
        print(f"Maple said: {response_text}")
        response_audio = synthesize_speech(response_text)
        # Play the audio
        wave_obj = sa.WaveObject.from_wave_file(response_audio)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing
        # Add delay before next recording
        time.sleep(0.1)
