import requests


def post(file_type: str, path_to_file: str):
    url = "http://127.0.0.1:5000/upload_" + file_type
    file = {file_type: open(path_to_file, 'rb')}
    response = requests.post(url, files=file)
    print(file_type + ": " + response.text)


path_to_image = r'1.jpeg'
path_to_audio = r'1.mp3'

post("image", path_to_image)
post("audio", path_to_audio)