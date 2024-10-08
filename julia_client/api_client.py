import wave
from io import BytesIO

import pyaudio
import webrtcvad
import requests
from pydub import AudioSegment
from pydub.playback import play

from julia_client.microphone import MicrophoneStream


SAMPLE_RATE = 16000
FRAME_LENGTH = 512


def play_wav(audio: bytes):
    segment = AudioSegment.from_file(BytesIO(audio), format="wav")
    play(segment)


def extent_bytes(first, second):
    arr = bytearray()
    arr.extend(first)
    arr.extend(second)

    return bytes(arr)


vad = webrtcvad.Vad()
vad.set_mode(3)
speech = b''
speech_ctr = 0
speaking = False
while True:
    with MicrophoneStream(sample_rate=SAMPLE_RATE, frame_length=FRAME_LENGTH) as stream:
        for chunk in stream.generator():
            speech_chunk = chunk[:960]
            is_speech = vad.is_speech(speech_chunk, SAMPLE_RATE)
            if is_speech:
                speech_ctr = 0
                speaking = True
                speech = extent_bytes(speech, chunk)
                print("Speech")
            else:
                speech_ctr += 1
                speech = extent_bytes(speech, chunk)
                print("Not speech")
                print(speech_ctr)

            if speaking and speech_ctr >= 30:
                speaking = False
                break

        response = requests.post('http://127.0.0.1:5000/request', data=speech)
        wf = wave.open("hey_julia.wav", 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(stream._audio_interface.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(speech)
        wf.close()
        if response.content:
            play_wav(response.content)
        speech = b''
        speech_ctr = 0
