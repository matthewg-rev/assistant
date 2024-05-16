import pyaudio
import speech_recognition
import wave

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