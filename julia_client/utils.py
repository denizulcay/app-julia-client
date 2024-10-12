from io import BytesIO

from pydub import AudioSegment
from pydub.playback import play


def play_wav(audio: bytes):
    segment = AudioSegment.from_file(BytesIO(audio), format="wav")
    play(segment)


def extent_bytes(first, second):
    arr = bytearray()
    arr.extend(first)
    arr.extend(second)

    return bytes(arr)
