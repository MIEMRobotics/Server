from flask import Flask, request
from flask_uploads import UploadSet, IMAGES, AUDIO, configure_uploads

path_to_images = r'./tests/responses'
path_to_audios = r'./tests/responses'

app = Flask(__name__)
app.config["UPLOADED_IMAGES_DEST"] = path_to_images
app.config["UPLOADED_AUDIOS_DEST"] = path_to_audios
app.secret_key = b'gOdSAvetHeroMaNOV\n\xec]/'

images = UploadSet('images', IMAGES)
audios = UploadSet('audios', AUDIO)
configure_uploads(app, (images, audios,))

files_to_handlers = \
    {
        'image': images,
        'audio': audios
    }


def upload(file_type: str):
    if file_type in request.files:
        files_to_handlers[file_type].save(request.files[file_type])
        return "Good"
    return "Bad"


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/upload_image', methods=['POST'])
def upload_image():
    return upload("image")


@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    return upload("audio")
