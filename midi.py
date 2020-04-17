import time
import asyncio
import mido
import logging
async def output_midi(events):
    job_start_time = time.time() * 1000
    logging.debug(f"playing events")
    logging.debug(f"using midi outport {mido.get_output_names()[0]}")

    with mido.open_output(mido.get_output_names()[0]) as outport:
        for next_event in events:
            time_into_job = time.time() * 1000  - job_start_time
            ms_until_next = next_event["ts"] - time_into_job
            await asyncio.sleep(max(ms_until_next / 1000, 0))
            logging.debug(f"next_event: {str(next_event)}")
            if next_event["type"] == "KEY_DOWN":
                mido_msg = mido.Message("note_on",
                    note=next_event["note"],
                    velocity=next_event["velocity"])
                logging.debug(f"sending: {str(mido_msg)}")
                outport.send(mido_msg)

            elif next_event["type"] == "KEY_UP":
                mido_msg = mido.Message("note_off", note=next_event["note"])
                logging.debug(f"sending: {str(mido_msg)}")
                outport.send(mido_msg)
            # ignores pedals lol

    await asyncio.sleep(3) # hack in case person forgot to end w key up
