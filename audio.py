import pyaudio

FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 0.1

# start Recording
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
stream.start_stream()