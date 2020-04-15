from math import log10
import audioop
import pyaudio
import wave
import sys
import config
import time
import asyncio


class LoserRecording():
    def __init__(self, outname):
        self.should_record = False
        self.outname = outname
        self.audio = pyaudio.PyAudio()
        self.wavefile = wave.open(self.outname, 'wb')
        self.stream = None
        self.db = 0

    def record(self):
        self.should_record = True

        self.wavefile.setnchannels(config.CHANNEL_COUNT)
        self.wavefile.setsampwidth(self.audio.get_sample_size(config.FORM_ONE))
        self.wavefile.setframerate(config.SAMPLE_RATE)

        def stream_callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            self.db = 20 * log10(audioop.rms(in_data, 2) + sys.float_info.epsilon)
            return (None, pyaudio.paContinue)

        self.stream = self.audio.open(
                    format = config.FORM_ONE,
                    rate = config.SAMPLE_RATE,
                    channels = config.CHANNEL_COUNT,
                    input_device_index = config.DEVICE_INDEX,
                    output=False,
                    input = True,
                    frames_per_buffer=config.CHUNK_SIZE,
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
        while self.db > config.STOP_DB_FLOOR and (time.time() - wanted_stop) < config.STOP_TIMEOUT:
            await asyncio.sleep(0.1)
        self.stop_recording()
