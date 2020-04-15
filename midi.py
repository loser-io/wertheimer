import time
import asyncio
import mido
import logging
async def output_midi(events):
    job_start_time = time.time() * 1000
    logging.debug(f"playing events")
    with mido.open_output(mido.get_output_names()[0]) as outport:
        for next_event in events:
            time_into_job = time.time() * 1000  - job_start_time
            ms_until_next = next_event["ts"] - time_into_job
            await asyncio.sleep(max(ms_until_next / 1000, 0))

            if next_event["type"] == "key_down":
                mido_msg = mido.Message("note_on",
                    note=next_event["note"],
                    velocity=next_event["velocity"])
                outport.send(mido_msg)
            elif next_event["type"] == "key_up":
                mido_msg = mido.Message("note_off", note=next_event["note"])
                outport.send(mido_msg)