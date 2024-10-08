import asyncio
import socket
from io import BytesIO

import pyaudio
from pydub import AudioSegment
from pydub.playback import play

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512

# Server settings
SERVER_IP = '192.168.1.30'  # Replace with your server's IP
SERVER_PORT = 5001


def play_wav(audio_data: bytes):
    segment = AudioSegment.from_file(BytesIO(audio_data), format="wav")
    play(segment)


class AsyncTcpClient:
    def __init__(self, ip, port, chunk):
        self.ip = ip
        self.port = port
        self.chunk = chunk

    async def start_stream(self):
        self._reader, self._writer = await asyncio.open_connection(self.ip, self.port)

    async def write_stream(self, data):
        self._writer.write(data)
        await self._writer.drain()

    async def read_stream(self):
        data = await self._reader.read()

        return data

    async def stop_stream(self):
        self._writer.close()
        await self._writer.wait_closed()


async def send_audio(stream: pyaudio.Stream, client: AsyncTcpClient):
    while True:
        # Read audio data from microphone
        data = stream.read(CHUNK, exception_on_overflow=False)
        # Send data to server
        await client.write_stream(data)


async def receive_audio(client: AsyncTcpClient):
    while True:
        data = await client.read_stream()
        print(data)
        play_wav(data)


async def main():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=512)
    client = AsyncTcpClient(SERVER_IP, SERVER_PORT, CHUNK)
    try:
        await client.start_stream()
        send = send_audio(stream, client)
        receive = receive_audio(client)
        await asyncio.gather(send, receive)
    except KeyboardInterrupt:
        print("Closing connection...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


asyncio.run(main())
