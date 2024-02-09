from unetpy import UnetSocket
import subprocess

def receive_lyra_and_decode(output_dir):
    s = UnetSocket('localhost', 1102)
    lyra_data_in_list = []
    try:
        rx = s.receive()
        print("Receiving")
        lyra_data = rx.data
        print("Happend")
        lyra_data_bytes = ''.join(chr(byte % 256) for byte in rx.data)
        lyra_data_bytes_1 =  lyra_data_bytes.encode('latin-1')
        lyra_data_in_list.append(lyra_data_bytes_1)
        lyra_official = b''.join(lyra_data_in_list)
        # lyra_data_bytes = bytes([byte % 256 for byte in lyra_data])
        print("Received and converted")
        lyra_file_path = f"/home/vboxuser/Lyra_Encode1/recorded_audio.lyra"
        with open(lyra_file_path, "wb") as lyra_file:
            lyra_file.write(lyra_official)

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
