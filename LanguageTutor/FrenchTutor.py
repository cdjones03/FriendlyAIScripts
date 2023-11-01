import time
import requests
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, ResultReason, SpeechSynthesizer

# Set your Azure Speech Service and Translator Text API credentials
speech_key = "2fb333d7da0844438808efaff644188c"
service_region = "eastus"
translator_key = "97ff78b9f6f24d519cb5c2e9a7ff85a2"
translator_endpoint = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"

speech_config = SpeechConfig(subscription=speech_key, region=service_region)
speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)


def translate_text(text, from_lang, to_lang):
    headers = {"Ocp-Apim-Subscription-Key": translator_key, "Content-type": "application/json", "Ocp-Apim-Subscription-Region": service_region}
    body = [{"text": text}]
    url = translator_endpoint + "&from=" + from_lang + "&to=" + to_lang
    request = requests.post(url, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']

def transcribe_audio():
    audio_config = AudioConfig(use_default_microphone=True)
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print("Speak into your microphone.")
    result = recognizer.recognize_once()
    if result.reason == ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason in [ResultReason.NoMatch, ResultReason.Canceled]:
        print("Something went wrong. Let's try again.")
        return transcribe_audio()

def pronounce_text(text):
    ssml_string = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="fr-FR"><voice name="Microsoft Server Speech Text to Speech Voice (fr-BE, CharlineNeural)">{text}</voice></speak>'
    result = speech_synthesizer.speak_ssml_async(ssml_string).get()
    if result.reason != ResultReason.SynthesizingAudioCompleted:
        print(f"Text synthesis failed: {result.reason}")

if __name__ == '__main__':
    print("Bonjour! Welcome to the French language assistant.")
    
    while True:
        user_input = transcribe_audio()
        if user_input.lower() in ["exit", "quit"]:
            print("Au revoir! Hope to speak with you again soon!")
            break

        translated_input = translate_text(user_input, 'en', 'fr')
        print(f"You said: {user_input}")
        print(f"This means in French: {translated_input}")
        print("Here's how you say it:")
        pronounce_text(translated_input)
        time.sleep(0.1)
