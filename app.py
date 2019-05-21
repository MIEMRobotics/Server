from flask import Flask, request
from flask_uploads import UploadSet, IMAGES, AUDIO, configure_uploads
from flask_socketio import SocketIO, join_room, emit, send
from utils.speech import *
from types import FunctionType


class ServerApp:
    """
    Basic class from you can inherit from or use functional API to extend it
    """

    def __init__(self, secret_key=b'1'):
        """
        Initialize app

        :param secret_key: Secret key for your app
        :type secret_key: bytearray
        """

        self._flask_app = Flask(__name__)
        self._flask_app.secret_key = secret_key

        self._socket_app = SocketIO(self._flask_app)

        @self._socket_app.on('test')
        def get_response():
            """
            Test function

            :return: "Hello, World"
            :rtype: str
            """
            return "Hello, World!"

    def run(self, host, port):
        """
        Runs the server

        :param host: ip of your server. Use 0.0.0.0 to open to outer connection
        :type host: str
        :param port: port of your server. Must be open.
        :type port: int
        :return: None
        :rtype: None
        """

        self._socket_app.run(host=host, port=port, app=self._flask_app)

    def add_socket_function(self, func, message):
        """
        Adds socket based function to your API.

        :param func: function object
        :type func: FunctionType
        :param message: signal that trigger function
        :type message: str

        :return: None
        :rtype: None

        Example::

            def get_up_text(text: str):
                return text.upper()

            app = ServerApp()
            app.add_socket_function(get_some_text, 'up')
        """

        @self._socket_app.on(message)
        def new_func(*args):
            return func(*args)
        new_func.__name__ = func.__name__

    def add_route_function(self, func, route):
        """
        Adds http requests based function to your API.

        :param func: function object
        :type func: FunctionType
        :param route: route that trigger function
        :type route: str

        :return: None
        :rtype: None

        Example::

            def get_up_text(text: str):
                return text.upper()

            app = ServerApp()
            app.add_route_function(get_some_text, 'up')
        """
        @self._flask_app.route(route)
        def new_func(*args):
            return func(*args)
        new_func.__name__ = func.__name__


class DialogApp(ServerApp):

    def __init__(self):

        super().__init__()

        @self._socket_app.on("give_answer")
        def get_answer(data):
            """
            Answers the question using DialogFlow API

            :param data: dict with 2 fields - 'audio' and 'return_type'.
             'audio' is wav file, coded as hex  string.
             'return_type' is 'text' or 'audio'

            :return: audio file, coded as hex string if 'return_type' is 'audio'.
              text string if 'return_type' is 'text'
            :rtype: str
            """
            question = audio_to_text(bytearray.fromhex(data['audio']))
            answer = question_to_answer(question)

            if data['return_type'] == "text":
                return answer

            elif data['return_type'] == "audio":
                audio = text_to_audio(answer)
                return bytearray.hex(audio)
            else:
                return None

        @self._socket_app.on("audio_to_text")
        def convert_audio(audio):
            """
            Maket audio to text transform and returns it as callback

            :param audio: audio file in wav format, coded as hex string
            :type audio: str

            :return: Text in the recording
            :rtype: str
            """
            text = audio_to_text(bytearray.fromhex(audio))
            return text

        @self._socket_app.on("text_to_audio")
        def convert_text(text):
            """
            Make text to audio transform and returns as callback

            :param text: text request
            :type text: str

            :return: audio file in .wav format, coded as hex string
            :rtype: str
            """
            audio = text_to_audio(text)
            return bytes.hex(audio)


def get_some_text(text):
    return text


def get_up_text(text: str):
    return text.upper()


if __name__ == '__main__':

    app = DialogApp()
    app.add_socket_function(get_some_text, 'text')
    app.add_socket_function(get_some_text, 'up')

    app.run('127.0.0.1', 5000)
