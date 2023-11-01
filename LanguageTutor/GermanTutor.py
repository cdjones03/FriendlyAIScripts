import openai
import time
import azure.cognitiveservices.speech as speechsdk
import os
import uuid
import requests

API_KEY_TRANSLATOR = "97ff78b9f6f24d519cb5c2e9a7ff85a2"
REGION_TRANSLATOR = "eastus"
API_KEY_SPEECH = "2fb333d7da0844438808efaff644188c"
REGION_SPEECH = "eastus"
YOUR_OPENAI_API_KEY = "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"

openai.api_key = YOUR_OPENAI_API_KEY

def text_to_speech(text, language):
    speech_config = speechsdk.SpeechConfig(subscription=API_KEY_SPEECH, region=REGION_SPEECH)
    speech_config.speech_synthesis_language = language
    speech_config.speech_synthesis_voice_name = "de-DE-ConradNeural"  # specify voice here
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    print(f'Speech to be synthesized for: {text}, language: {language}')  # print before speech synthesis
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print('Speech synthesis completed.')
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f'Speech synthesis canceled: {cancellation_details.reason}')

def speech_to_text(language):
    speech_config = speechsdk.SpeechConfig(subscription=API_KEY_SPEECH, region=REGION_SPEECH)
    speech_config.speech_recognition_language = language
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        print(f'No speech could be recognized: {result.reason}')

def translate_text(text, to_language, from_language="en"):
    endpoint = f"https://api.cognitive.microsofttranslator.com"
    path = "/translate"
    constructed_url = endpoint + path

    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY_TRANSLATOR,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4())
    }

    params = {
        "api-version": "3.0",
        "from": from_language,
        "to": to_language
    }

    body = [{"text": text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response.raise_for_status()

    return response.json()[0]['translations'][0]['text']

def generate_responses(prompt, language):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60,
        n=3  # Number of responses
    )
    generated_responses = [choice.text.strip() for choice in response.choices]

    return generated_responses

def main():
    initial_prompt = "Hello, how are you?"
    language = "de"
    while True:
        translated_prompt = translate_text(initial_prompt, to_language=language)
        text_to_speech(translated_prompt, language)
        print(f"Initial Prompt: {initial_prompt}")

        responses = generate_responses(translated_prompt, language)
        translated_responses = [translate_text(response, to_language="en", from_language=language)
                                for response in responses]

        for i, (response, translated_response) in enumerate(zip(responses, translated_responses), 1):
            print(f"\nResponse {i}: {response} - Press {i} to listen")
            print(f"Translated Response {i}: {translated_response}")

        # User can listen to each response before choosing one to speak
        while True:
            choice = input("\nEnter a number to listen or press Enter to speak: ")
            if choice in ['1', '2', '3']:
                text_to_speech(responses[int(choice) - 1], language)
            else:
                break

        user_speech = speech_to_text(language)
        initial_prompt = translate_text(user_speech, to_language="en", from_language=language)

if __name__ == "__main__":
    main()
