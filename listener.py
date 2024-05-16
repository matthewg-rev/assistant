import os
import sys
import importlib

dependencies = {
    "pyaudio": "pyaudio",
    "speech_recognition": "speechrecognition",
    "vosk": "vosk",
}

model_options = {
    "vosk-model-small-en-us-0.15": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
}

# check if we are ran in sudo
if os.geteuid() != 0:
    print("Please run this script as sudo.")
    sys.exit()

# check if dependencies are installed
for dependency in dependencies:
    try:
        globals()[dependency] = importlib.import_module(dependency)
    except ImportError:
        print(f"Installing {dependencies[dependency]}")
        result = os.system(f"pip3 install {dependencies[dependency]}")
        if result != 0:
            print(f"Failed to install {dependencies[dependency]}.")
            sys.exit()

# all models are downloaded to \models
if not os.path.isdir("models"):
    os.mkdir("models")

# check if there's any models downloaded
if len(os.listdir("models")) == 0:
    print("No models found. Downloading models.")
    for model in model_options:
        print(f"Downloading {model}")
        result = os.system(f"wget {model_options[model]} -O models/{model}.zip")
        if result != 0:
            print(f"Failed to download {model}.")
            sys.exit()
        result = os.system(f"unzip models/{model}.zip -d models/")
        if result != 0:
            print(f"Failed to unzip {model}.")
            sys.exit()


RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 2
RESPEAKER_WIDTH = 2

RESPEAKER_INDEX = 1
CHUNK = 1024

p = pyaudio.PyAudio()