import pyaudio
import wave
import time

import pyaudio
p = pyaudio.PyAudio()
for ii in range(p.get_device_count()):
    print(f"{ii} - {p.get_device_info_by_index(ii).get('name')}")
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 3 # seconds to record
dev_index = 0 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(
    format = form_1,
    rate = samp_rate,
    channels = chans,
    input_device_index = dev_index,
    input = True,
    frames_per_buffer=chunk
    )
print("recording")
frames = []

sample_midi = [
{"ts": 0, "type": "note_on", "value_0": 60, "value_1": 120},
{"ts": 500, "type": "note_on", "value_0": 60, "value_1": 120},
{"ts": 1000, "type": "note_on", "value_0": 60, "value_1": 120},
{"ts": 15000, "type": "note_on", "value_0": 60, "value_1": 120},
]

start = time.time() * 1000
for msg in sample_midi:
    noww = (time.time() * 1000) - start



# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk) * record_secs)):
    data = stream.read(chunk)
    frames.append(data)



print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()