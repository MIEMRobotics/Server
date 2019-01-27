import apiai
import json
import speech_recognition as sr
from speech_recognition import Recognizer
from google.cloud import texttospeech
from functools import partial
from tempfile import mkstemp
from utils.api_keys import dialog_flow_key

_recognize = partial(Recognizer().recognize_google, language="ru-RU")
_text_to_speech_client = texttospeech.TextToSpeechClient()


def audio_to_text(audio):
    _, name = mkstemp()

    with open(name, 'w+b') as temp:
        temp.write(audio)

        with sr.WavFile(name) as f:
            audio_data = sr.Recognizer().record(f)
            return _recognize_wav(audio_data)


def text_to_audio(text):

    input = texttospeech.types.module.SynthesisInput(text=text)
    voice = texttospeech.types.module.VoiceSelectionParams(language_code='ru-RU',
                                                           ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    audio_config = texttospeech.types.module.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

    response = _text_to_speech_client.synthesize_speech(input, voice, audio_config)

    return response.audio_content


def question_to_answer(question):
    answer = _dialog_flow_response(question)
    if answer:
        return answer
    else:
        return "I don't get it"


def _dialog_flow_response(text):
    request = apiai.ApiAI(dialog_flow_key).text_request()
    request.lang = 'ru'
    request.session_id = 'MIEMRobot'
    request.query = text

    response = request.getresponse().read().decode('utf-8')
    response_json = json.loads(response)
    response_text = response_json['result']['fulfillment']['speech']

    if response_text:
        return response_text
    else:
        return None


def _recognize_wav(audio_data):
    try:
        text = _recognize(audio_data)
        return text
    except Exception as e:
        print(e)
        return None
