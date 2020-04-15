import datetime
import random
import itertools
import os
from pymongo import MongoClient
import config
import jobs
mc = MongoClient(
    "mongodb+srv://{}:{}@{}/test?retryWrites=true".format(
        config.MONGO_USER, config.MONGO_PW, config.MONGO_HOST
    )
)
hz = 200
dur = 1000 / hz

def noteandoff(i):
    note = random.randint(0, 127)
    return [
            {"ts": ((2 * i) + 0) * dur , "type": "key_down", "note": note, "velocity": 60},
            {"ts": ((2 * i) + 1) * dur , "type": "key_up", "note": note, "velocity": 60},
            ]

def new_job():
    events = itertools.chain.from_iterable(noteandoff(i) for i in range(int(4000 / dur)))
    return {
        "submit_dt": datetime.datetime.now(),
        "status": "available",
        "events": list(events)
    }

ok = new_job()
mc.loser.jobs.insert_one(ok)
print(ok)

# import pyaudio
# p = pyaudio.PyAudio()
# for ii in range(p.get_device_count()):
#     print(f"{ii} - {p.get_device_info_by_index(ii).get('name')}")

# job
# _id : ObjectId
# submit_dt : IsoDate
# complete_dt : None or IsoDate
# status : "available" "running" "completed" "failed"
# kitty_name : string
# events : Array[event]

# event
# ts : what time into song. in ms (?)
# type : key_down key_up pedal
# note : pitch if key_down or key_up
# velocity : if pitch
# pedal_no : if pedal
# pedal_value : if pedal




