from flask import Flask, request
from flask_uploads import UploadSet, IMAGES, AUDIO, configure_uploads
from flask_socketio import SocketIO, join_room, emit, send
import speech_recognition
from utils.uploader import *
from utils.speech import *

path_to_images = r'./tests/responses'
path_to_audios = r'./tests/responses'

app = Flask(__name__)
app.config["UPLOADED_IMAGES_DEST"] = path_to_images
app.config["UPLOADED_AUDIOS_DEST"] = path_to_audios
app.secret_key = b'gOdSAvetHeroMaNOV\n\xec]/'

socketio = SocketIO(app)

images = UploadSet('images', IMAGES)
audios = UploadSet('audios', AUDIO)
configure_uploads(app, (images, audios,))

files_to_handlers = \
    {
        'image': images,
        'audio': audios
    }

recognizer = speech_recognition.Recognizer()


def upload(file_type: str):
    if file_type in request.files:
        files_to_handlers[file_type].save(request.files[file_type])
        return "Good"
    return "Bad"


@app.route('/')
def hello_world():
    return 'Hello, World!'


@socketio.on("connect")
def connect():
    return True


@app.route('/upload_image', methods=['POST'])
def upload_image():
    return upload("image")


@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    return upload("audio")


@socketio.on('test')
def test(data):
    return data


@socketio.on('upload_image')
def upload_image(image):
    return upload("image")


@socketio.on("upload_audio")
def upload_audio(audio):
    return upload("audio")


@socketio.on("give_answer")
def get_answer(data):
    question = audio_to_text(bytearray.fromhex(data['audio']))
    answer = question_to_answer(question)

    if data['return_type'] == "text":
        return answer

    elif data['return_type'] == "audio":
        audio = text_to_audio(answer)
        return bytearray.hex(audio)
    else:
        return None


@socketio.on("audio_to_text")
def convert(audio):
    text = audio_to_text(bytearray.fromhex(audio))
    return text


@socketio.on("text_to_audio")
def convert(text):
    audio = text_to_audio(text)
    return bytes.hex(audio)


if __name__ == '__main__':
    socketio.run(host='0.0.0.0', port=5000)
