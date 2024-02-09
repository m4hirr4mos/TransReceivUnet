#!/usr/bin/env python3

from unetpy import UnetSocket
import subprocess

def receive_lyra_and_decode(output_dir, chunk_size=400):
    s = UnetSocket('localhost', 1102)

    try:
        rx = s.receive()
        print("Receiving")

        lyra_chunks = []

        while True:
            rx = s.receive()
            if not rx.data:
                print("No more data. Exiting loop.")
                break

            # Convert byte values to valid characters and handle non-ASCII characters
            try:
                chunk_str = ''.join(chr(byte % 256) for byte in rx.data)
                chunk_bytes = chunk_str.encode('latin-1')[:chunk_size]
            except UnicodeEncodeError:
                print("Warning: Non-ASCII characters detected. Ignoring.")
                chunk_bytes = b''

            lyra_chunks.append(chunk_bytes)
            rx.data = rx.data[chunk_size:]
            print("Receiving chunk")

            if len(chunk_bytes) < chunk_size:
                print("Received data less than 400 bytes. Exiting loop.")
                break

        # Combine chunks into the complete Lyra-encoded data
        lyra_data = b''.join(lyra_chunks)

        # Check if there is any data to decode
        if lyra_data:
            lyra_file_path = f"{output_dir}/recorded_audio.lyra"
            with open(lyra_file_path, "wb") as lyra_file:
                lyra_file.write(lyra_data)

            # Decode the received Lyra file
            try:
                subprocess.run(["bazel-bin/lyra/cli_example/decoder_main", f"--encoded_path={lyra_file_path}", f"--output_dir={output_dir}", "--bitrate=3200"], check=True)
                print(f"Audio decoded and saved in '{output_dir}'.")
            except subprocess.CalledProcessError:
                print("Error while decoding the audio.")

            # Play the decoded audio
            try:
                subprocess.run(["aplay", f"{output_dir}/recorded_audio_decoded.wav"], check=True)
                print("Audio played.")
            except subprocess.CalledProcessError:
                print("Error while playing the audio.")

    finally:
        s.close()

if __name__ == "__main__":
    decoded_audio_output = "/home/vboxuser/Lyra_Decode"
    receive_lyra_and_decode(decoded_audio_output)