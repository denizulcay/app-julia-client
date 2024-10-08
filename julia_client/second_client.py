import numpy as np
import socket
import pyaudio

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000
CHUNK = 512

# Server settings
SERVER_IP = '192.168.1.30'
SERVER_PORT = 5001

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))


p = pyaudio.PyAudio()

# Open the input stream
input_stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)

# Open the output stream
output_stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       output=True,
                       frames_per_buffer=CHUNK)

print("Streaming audio...")

input_stream.start_stream()
output_stream.start_stream()

print("Sending audio...")

try:
    while True:
        # Read audio data from microphone
        data = input_stream.read(CHUNK, exception_on_overflow=False)
        # Send data to server
        client_socket.sendall(data)
        response = client_socket.recv(CHUNK)
        output_stream.write(response, CHUNK)

except KeyboardInterrupt:
    print("Closing connection...")
finally:
    client_socket.close()
    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()
