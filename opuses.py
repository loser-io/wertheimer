import requests
import os
import logging
from dotenv import load_dotenv
import operator

load_dotenv(override=True)


def gould(method, route):
    return operator.methodcaller(
        method,
        os.getenv("GOULD_HOST") + "/api/as/performer/" + route,
        headers={"Authorization": "Bearer " + os.getenv("GOULD_API_KEY")},
    )(requests)


def get_assigned():
    res = gould("get", "assigned")
    if res.status_code == 422:
        return None
    else:
        return res.json()


def get_presigned_url():
    res = gould("get", "destination")
    if res.status_code == 422:
        raise ValueError  # uh idk what happened

    presigned_url = res.text
    return presigned_url


def upload_opus(opus):
    presigned_url = get_presigned_url()

    opus_filename = opus["_id"] + ".wav"
    with open(opus_filename, "rb") as f:
        logging.debug(f"uploading {opus_filename} to {presigned_url}")
        res = requests.put(
            presigned_url,
            headers={"Content-Type": "audio/wav"},
            data=f.read()
            # files={"file": (opus_filename, f)},
        )
        logging.debug(f"upload attempt res code {str(res)}")

    res = gould("post", "confirmation")
    if res.text != "OK":
        raise ValueError  # wtf
    print(res.text)

