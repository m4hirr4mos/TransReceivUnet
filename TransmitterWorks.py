#!/usr/bin/env python3
import sounddevice as sd
import numpy as np
import wavio
import subprocess
from unetpy import UnetSocket

# Define the recording parameters
sample_rate = 48000
duration = None
recording = False
audio_data = []

def toggle_recording():
    global recording
    if recording:
        recording = False
        print("Recording stopped.")
    else:
        recording = True
        print("Recording...")

def audio_callback(indata, frames, time, status):
    if recording:
        audio_data.append(indata.copy())

# Start the audio stream
with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
    print("Press Enter to toggle recording (start/stop).")
    while True:
        try:
            key = input()
            if key == '':
                toggle_recording()
        except KeyboardInterrupt:
            break

# Save the recorded audio to a WAV file
if audio_data:
    wavio.write("/home/vboxuser/recorded_audio.wav", np.vstack(audio_data), sample_rate, sampwidth=2)
    print("Recording saved as '/home/vboxuser/recorded_audio.wav'")

# Encode the audio
def encode_audio(input_path, encoded_path):
    try:
        subprocess.run(["bazel-bin/lyra/cli_example/encoder_main", f"--input_path={input_path}", f"--output_dir={encoded_path}", "--bitrate=3200"], check=True)
        print(f"Audio encoded and saved as '{encoded_path}'.")
    except subprocess.CalledProcessError:
        print("Error while encoding the audio.")

# Transmit the encoded data in chunks
def transmit_lyra_file(file_path, chunk_size=400):
    s = UnetSocket('localhost', 1101)

    try:
        lyra_data = open(file_path, "rb").read()

        # Transmit data in chunks
        for i in range(0, len(lyra_data), chunk_size):
            chunk = lyra_data[i:i + chunk_size]
            s.send(chunk, 0)
            print(f"Transmitted chunk {i // chunk_size + 1}")
        s.send("Transmission Complete",0)
        print("Transmission complete")
    finally:
        s.close()

if __name__ == "__main__":
    input_audio_path = "/home/vboxuser/recorded_audio.wav"
    encoded_audio_output = "/home/vboxuser/Lyra_Encode"

    # Encode the recorded audio
    encode_audio(input_audio_path, encoded_audio_output)

    # Transmit the encoded data in chunks
    transmit_lyra_file(f"{encoded_audio_output}/recorded_audio.lyra", chunk_size=400)