import cv2
from scipy.io import wavfile


def upload_audio(path, audio):
    wavfile.write(path, 3, audio)


def upload_image(path, image):
    cv2.imwrite(path, image)