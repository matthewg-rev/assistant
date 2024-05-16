import os
import sys
import importlib

dependencies = {
    "pyaudio": "pyaudio",
    "speech_recognition": "speechrecognition",
    "vosk": "vosk",
}

# check if we are ran in sudo
if os.geteuid() != 0:
    print("Please run this script as sudo.")
    sys.exit()

# check if dependencies are installed
for dependency in dependencies:
    try:
        importlib.import_module(dependency)
    except ImportError:
        print(f"Installing {dependencies[dependency]}")
        os.system(f"pip3 install {dependencies[dependency]}")

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 2
RESPEAKER_WIDTH = 2

RESPEAKER_INDEX = 1
CHUNK = 1024

p = pyaudio.PyAudio()