import mido
import requests
import signal
import random
import itertools
import time
import datetime
from collections import deque
import asyncio

import record
import midi
# import jobs
import opuses
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.DEBUG)


async def record_job(opus):
    wav_filename = "-".join([
            # datetime.datetime.utcnow().isoformat()[0:10],
            # config.KITTY_NAME,
            str(opus["_id"]),
        ]) + ".wav"

    new_recording = record.LoserRecording(wav_filename)
    new_recording.record()
    await midi.output_midi(opus["events"])
    await new_recording.schedule_stop()

def signal_handler(signal, frame):
    loop.stop()
    client.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

def main():
    print("starting")
    while True:
        assigned_opus = opuses.get_assigned()
        if assigned_opus:
            asyncio.run(record_job(assigned_opus))
            opuses.upload_opus(assigned_opus)
        else:
            time.sleep(3)

if __name__ == "__main__":
    main()
