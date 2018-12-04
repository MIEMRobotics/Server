from flask import Flask, request
from flask_uploads import UploadSet, IMAGES, AUDIO, configure_uploads
from flask_socketio import SocketIO, join_room, emit
import speech_recognition

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


def classify_image(image):
    return image


def detect_image(image):
    return image


def audio_to_text(audio):
    text = recognizer.recognize_google(audio)
    return text


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/upload_image', methods=['POST'])
def upload_image():
    return upload("image")


@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    return upload("audio")


@socketio.on("detect")
def detect(data):
    image = data['image']
    detected = detect_image(image)
    emit('detected', {'image': detected})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
