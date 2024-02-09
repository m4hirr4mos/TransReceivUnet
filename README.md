#Cloning the Lyra Repository
To get started with Lyra, clone the repository using the following command in your Linux terminal:
git clone https://github.com/google/lyra.git


#Building Lyra with Bazel
Navigate to the Lyra directory and build Lyra using Bazel with the following command:
cd lyra
bazel build -c opt lyra/cli_example:encoder_main
 
#Encoding Speech with Lyra
After building Lyra, you can proceed with encoding speech. Use the following command format:

bazel-bin/lyra/cli_example/encoder_main \
--input_path=/path/to/input.wav \
--output_dir=/path/to/output \
--bitrate=3200

•	input_path: Directory of the input WAV file.
•	output_dir: Directory where the compressed output file will be placed.
•	bitrate: Bitrate for compressing the voice.

#Decoding Compressed Speech
To decode the compressed speech, use the following command:
bazel-bin/lyra/cli_example/decoder_main \
--input_path=/path/to/compressed.lyra \
--output_path=/path/to/output.wav

•	input_path: Location of the encoded speech file.
•	output_path: Location to save the decoded WAV file.

#Setting up UnetStack
1.	Download UnetStack Community from https://unetstack.net/#downloads and extract the files/unzip it.
   
#Transmitting and Receiving Audio via UnetStack
1.	Navigate to the Lyra directory.
2.	Save the transmitter and receiver scripts.
3.	Open three separate terminals.


#Setting Up Nodes and recording,encoding and decoding Audio
1.	Run the following command on your Linux Terminal in the repository when UnetStack is installed  to set up a 2-node network:

bin/unet samples/2-node-network.groovy

3.	Open command shells for both Nodes A and B and type "subscribe phy" into each terminal.
4.	Run the Receiver Script in one terminal in the lyra directory.
5.	In the other terminal, run the transmitter script in the lyra directory.
6.	Press Enter to start recording, press Enter again to stop recording.
7.	Press Ctrl + C and check the decoding and playing of the audio on the receiver terminal.

