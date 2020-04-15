import mido
import signal
import random
import itertools
import time
import datetime
from collections import deque
import asyncio
import config
import record
import midi
import jobs


async def record_job(job_todo):
    wav_filename = "-".join([
            datetime.datetime.utcnow().isoformat()[0:10],
            config.KITTY_NAME,
            str(job_todo["_id"]),

        ]) + ".wav"
    new_recording = record.LoserRecording(wav_filename)
    new_recording.record()
    await midi.output_midi(job_todo["events"])
    await new_recording.schedule_stop()
    print("done")


def signal_handler(signal, frame):
    loop.stop()
    client.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    print("starting")
    while True:
        print("trying")
        job_todo = jobs.get_owned_job()
        if job_todo is None:
            job_todo = jobs.get_oldest_job()

        if job_todo:
            confirmation = jobs.take_job(job_todo)
            if confirmation:
                asyncio.run(record_job(job_todo))
                jobs.finish_job(job_todo)

        time.sleep(3)


if __name__ == "__main__":
    main()
