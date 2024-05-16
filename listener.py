import os
import sys

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
        __import__(dependency)
    except ImportError:
        print(f"Installing {dependencies[dependency]}")
        os.system(f"pip3 install {dependencies[dependency]}")

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 2
RESPEAKER_WIDTH = 2

RESPEAKER_INDEX = 1
CHUNK = 1024

p = pyaudio.PyAudio()

stream = p.open(
    rate=RESPEAKER_RATE,
    format=p.get_format_from_width(RESPEAKER_WIDTH),
    channels=RESPEAKER_CHANNELS,
    input=True,
    input_device_index=RESPEAKER_INDEX,
    frames_per_buffer=CHUNK,
)

r = speech_recognition.Recognizer()

while True:
    data = stream.read(CHUNK)
    try:
        text = r.recognize_google(data, language="en-US")
        print(text)
    except Exception as e:
        print(e)

        stream.stop_stream()
        stream.close()
        p.terminate()