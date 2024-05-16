import os
import sys
import importlib

from queue import Queue
from threading import Thread

dependencies = {
    "pyaudio": "pyaudio",
    "speech_recognition": "speechrecognition",
}

non_imported_dependencies = [
    "SpeechRecognition[whisper-local]"
]

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

# check if non-imported dependencies are installed
for dependency in non_imported_dependencies:
    if not importlib.util.find_spec(dependency):
        print(f"Installing {dependency}")
        result = os.system(f"pip3 -m install {dependency}")
        if result != 0:
            print(f"Failed to install {dependency}.")
            sys.exit()

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 2
RESPEAKER_WIDTH = 2

RESPEAKER_INDEX = 1
CHUNK = 1024

r = speech_recognition.Recognizer()
queue = Queue()

def listening_worker():
    while True:
        audio = queue.get()
        if audio is None:
            break

        try:
            text = r.recognize_whisper(audio, language="english")
            print(text)
        except speech_recognition.UnknownValueError:
            print("Could not understand audio")
        except speech_recognition.RequestError as e:
            print(f"Could not request results; {e}")


listening_thread = Thread(target=listening_worker)
listening_thread.daemon = True
listening_thread.start()
with sr.Microphone() as source:
    try:
        while True:
            queue.put(r.listen(source))
    except KeyboardInterrupt:
        pass

queue.join()
queue.put(None)
listening_thread.join()