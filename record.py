from math import log10
import audioop
import pyaudio
import logging
import wave
import sys
import time
import asyncio

FORM_ONE = pyaudio.paInt16 # 16-bit resolution
SAMPLE_RATE = 44100 # 44.1kHz sampling rate
CHANNEL_COUNT = 1 # 1 channel
CHUNK_SIZE = 4096 # 2^12 samples for buffer
DEVICE_INDEX = 0
STOP_TIMEOUT = 30
STOP_DB_FLOOR = 20

def audio_list_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,numdevices):
        if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
            logging.debug(f"Input Device id {i} - {p.get_device_info_by_host_api_device_index(0,i).get('name')}")

        if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
            logging.debug(f"Output Device id {i} - {p.get_device_info_by_host_api_device_index(0,i).get('name')}")

    devinfo = p.get_device_info_by_index(DEVICE_INDEX)
    logging.debug(f"Selected device is {devinfo.get('name')}" )
    p.terminate()

class LoserRecording():
    def __init__(self, outname):
        self.should_record = False
        self.should_log_db = False
        self.outname = outname
        self.audio = pyaudio.PyAudio()
        self.wavefile = wave.open(self.outname, 'wb')
        self.stream = None
        self.db = 0

    def record(self):
        logging.debug(f"recording to filename: {self.outname}")
        audio_list_devices()

        self.should_record = True

        self.wavefile.setnchannels(CHANNEL_COUNT)
        self.wavefile.setsampwidth(self.audio.get_sample_size(FORM_ONE))
        self.wavefile.setframerate(SAMPLE_RATE)

        def stream_callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            self.db = 20 * log10(audioop.rms(in_data, 2) + sys.float_info.epsilon)

            return (None, pyaudio.paContinue)

        self.stream = self.audio.open(
                    format = FORM_ONE,
                    rate = SAMPLE_RATE,
                    channels = CHANNEL_COUNT,
                    input_device_index = DEVICE_INDEX,
                    output=False,
                    input = True,
                    frames_per_buffer=CHUNK_SIZE,
                    stream_callback=stream_callback
                )
        print("recording")
        self.stream.start_stream()

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.wavefile.close()
        self.audio.terminate()

    async def schedule_stop(self):
        print("stopping recording")
        wanted_stop = time.time()
        logging.debug(f"db: {self.db}")
        while self.db > STOP_DB_FLOOR and (time.time() - wanted_stop) < STOP_TIMEOUT:
            logging.debug(f"db: {self.db}")
            await asyncio.sleep(0.1)
        logging.debug(f"db: {self.db}")
        self.stop_recording()
