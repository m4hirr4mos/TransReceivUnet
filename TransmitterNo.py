import sounddevice as sd
import numpy as np
import wavio
import subprocess
from unetpy import UnetSocket

# Define the recording parameters
sample_rate = 16000
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
    wavio.write("recorded_audio.wav", np.vstack(audio_data), sample_rate, sampwidth=2)
    print("Recording saved as 'recorded_audio.wav'")

# Encode the audio
def encode_audio(input_path, encoded_path):
    try:
        subprocess.run(["bazel-bin/lyra/cli_example/encoder_main", f"--input_path={input_path}", f"--output_dir={encoded_path}", "--bitrate=3200"], check=True)
        print(f"Audio encoded and saved as '{encoded_path}'.")
    except subprocess.CalledProcessError:
        print("Error while encoding the audio.")

# Define paths for your audio and encoded output
input_audio_path = "recorded_audio.wav"
encoded_audio_output = "Lyra_Encode"

# Encode the recorded audio
encode_audio(input_audio_path, encoded_audio_output)

# Transmit the encoded data
s = UnetSocket('localhost', 1101)
try:
    encoded_data = open(f"{encoded_audio_output}/recorded_audio.lyra", "rb").read()
    x = s.send(encoded_data, 0)
    print(x)
finally:
    s.close()
