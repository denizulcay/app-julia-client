import queue

import pyaudio


class MicrophoneStream:
    def __init__(self, sample_rate: int, frame_length: int):
        self._sample_rate = sample_rate
        self._frame_length = frame_length
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._sample_rate,
            input=True,
            frames_per_buffer=self._frame_length,
            stream_callback=self._fill_buffer,
        )
        self.closed = False

        return self

    def __exit__(
        self,
        type: object,
        value: object,
        traceback: object,
    ):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(
        self,
        in_data: object,
        frame_count: int,
        time_info: object,
        status_flags: object,
    ):
        self._buff.put(in_data)

        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)
