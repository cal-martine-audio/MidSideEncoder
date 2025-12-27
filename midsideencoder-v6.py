# Mid-Side Encoder Version 6.0
# By Cal Martine
import os
import time
from pydub import AudioSegment


# CHANGE THESE TWO VARIABLES TO REFLECT YOUR FILE PATH (ex. Users/[YOUR USERNAME]/Desktop/MidSideEncoder/Input)
output_folder = "/PATH/TO/MidSideEncoder/Output"
input_folder = "PATH/TO/MidSideEncoder/Input"
# ________________________________________________


def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# List all files in the input folder
files = list_files(input_folder)

print(files)

for file in files:
    if file.lower().endswith(('.wav', '.mp3', '.aiff', '.tiff')):
        input_file = os.path.join(input_folder, file)

        try:
            # Load the input audio file
            audio = AudioSegment.from_file(input_file)

            # Create a mono bounce (sum of left and right channels)
            mono_bounce = audio.set_channels(1)
            mono_bounce.export(output_folder + "/" + file.split('.')[0] + "_MID.wav", format="wav")

            # Create a side plus bounce (left channel + inverted right channel)
            side_bounce = audio.split_to_mono()[0].overlay(audio.split_to_mono()[1].invert_phase())
            side_bounce.export(output_folder + "/" + file.split('.')[0] + "_SIDE_PLUS.wav", format="wav")

            # Create a side minus bounce (right channel + inverted left channel)
            side_minus_bounce = audio.split_to_mono()[1].overlay(audio.split_to_mono()[0].invert_phase())
            side_minus_bounce.export(output_folder + "/" + file.split('.')[0] + "_SIDE_MINUS.wav", format="wav")
            print("success: " + file)
            time.sleep(1)
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
