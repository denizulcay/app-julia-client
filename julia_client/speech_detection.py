from typing import Iterable, Self

import webrtcvad

from julia_client.utils import extent_bytes


class SpeechDetectionClient:
    def __init__(self: Self, mode: int = 3, frame_length: int = 480):
        self._client = webrtcvad.Vad()
        self._client.set_mode(mode)
        self._frame_length = frame_length

    def get_speech(
            self: Self,
            stream_gen: Iterable[bytes],
            sample_rate: int,
            silence_length: int = 15
    ) -> bytes:
        speech, silence_ctr, speaking = b'', 0, False
        for chunk in stream_gen:
            # Speech can only process 160, 320, 480 frames
            speech_chunk = chunk[:self._frame_length * 2]
            is_speech = self._client.is_speech(speech_chunk, sample_rate)
            if is_speech:
                silence_ctr = 0
                speaking = True
                speech = extent_bytes(speech, chunk)
                print("Speech")
            elif speaking and silence_ctr >= silence_length:
                return speech
            elif speaking:
                silence_ctr += 1
                speech = extent_bytes(speech, chunk)
                print(silence_ctr)
