from time import sleep

import requests

from julia_client.microphone_stream import MicrophoneStream
from julia_client.speech_detection import SpeechDetectionClient
from julia_client.utils import play_wav

SAMPLE_RATE = 16000
FRAME_LENGTH = 512
SERVER_IP = '192.168.1.30'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

detect_client = SpeechDetectionClient()

with MicrophoneStream(sample_rate=SAMPLE_RATE, frame_length=FRAME_LENGTH) as stream:
    while True:
        payload = detect_client.get_speech(stream.generator(), sample_rate=SAMPLE_RATE)
        response = requests.post(f'http://{SERVER_IP}:{SERVER_PORT}/request', data=payload)
        if response.status_code == 200:
            play_wav(response.content)
            sleep(1)
