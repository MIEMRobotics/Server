from scipy.io import wavfile
import cv2


def upload_audio(path, audio):
    wavfile.write(path, 3, audio)


def upload_image(path, image):
    cv2.imwrite(path, image)