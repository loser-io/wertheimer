import os
import pyaudio
MONGO_PW = os.environ["MONGO_PW"]
MONGO_USER = os.environ["MONGO_USER"]
MONGO_HOST = os.environ["MONGO_HOST"]
KITTY_NAME = "mbp00000000"

SAMPLE_RATE = 44100 # 44.1kHz sampling rate
FORM_ONE = pyaudio.paInt16 # 16-bit resolution
CHANNEL_COUNT = 1 # 1 channel
CHUNK_SIZE = 4096 # 2^12 samples for buffer
DEVICE_INDEX = 0
STOP_TIMEOUT = 60
STOP_DB_FLOOR = 10
