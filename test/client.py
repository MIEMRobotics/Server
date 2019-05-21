from socketIO_client import SocketIO

temp_audio_source_path = "data/source.wav"
temp_audio_answer_path = "data/answer.wav"


def on_connect(is_connected):
    if is_connected:
        print("Connection successful")
    else:
        print("Connection forbidden")


def on_audio(audio):
    with open(temp_audio_answer_path, 'wb') as f:
        f.write(bytearray.fromhex(audio))


def on_text(text):
    print(text)


def get_audio_data():
    with open(temp_audio_source_path, 'rb') as f:
        audio_data = f.read()

    if audio_data:
        return audio_data


def get_text_data():
    return "Люблю грозу в начале мая! Как долбанёт и нет сарая!"


if __name__ == '__main__':

    with SocketIO("127.0.0.1", 5000) as client:

        client.emit("text_to_audio", get_text_data(), on_audio)
        client.wait_for_callbacks(2)

        client.emit('audio_to_text', get_audio_data().hex(), on_text)
        client.wait_for_callbacks(2)

        client.emit("give_answer", {'audio': get_audio_data().hex(), 'return_type': "text"}, on_text)
        client.wait_for_callbacks(2)

