import os
from pymongo import MongoClient
import pymongo
import datetime
import config

mc = MongoClient(
    "mongodb+srv://{}:{}@{}/test?retryWrites=true".format(
        config.MONGO_USER, config.MONGO_PW, config.MONGO_HOST
    )
)

MONGO_JOBS = mc.loser.jobs

def get_oldest_job():
    job = MONGO_JOBS.find_one(
        {"status": "available"}, sort=[("submit_dt", pymongo.ASCENDING)]
    )
    return job


def get_owned_job():
    job = MONGO_JOBS.find_one(
        {"status": "running", "kitty_name": config.KITTY_NAME},
        sort=[("submit_dt", pymongo.ASCENDING)],
    )
    return job


def take_job(mongo_job):
    MONGO_JOBS.update_one(
        {"_id": mongo_job["_id"]},
        {"$set": {"status": "running", "kitty_name": config.KITTY_NAME}},
        upsert=False,
    )
    taken = MONGO_JOBS.find_one({"_id": mongo_job["_id"]})
    return config.KITTY_NAME == taken["kitty_name"]


def finish_job(mongo_job):
    # check if still saying running and kitty_name matches, then
    MONGO_JOBS.update_one(
        {"_id": mongo_job["_id"]},
        {
            "$set": {
                "status": "completed",
                "complete_dt": datetime.datetime.utcnow(),
                "kitty_name": config.KITTY_NAME,
            }
        },
        upsert=False,
    )
