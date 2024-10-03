import socket
import pyaudio

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512

# Server settings
SERVER_IP = '192.168.1.30'  # Replace with your server's IP
SERVER_PORT = 5001

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open microphone stream
stream = audio.open(format=pyaudio.paInt16, channels=1,
                    rate=16000, input=True,
                    frames_per_buffer=512)

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

print("Sending audio...")

try:
    while True:
        # Read audio data from microphone
        data = stream.read(CHUNK, exception_on_overflow=False)
        # Send data to server
        client_socket.sendall(data)

except KeyboardInterrupt:
    print("Closing connection...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    client_socket.close()
