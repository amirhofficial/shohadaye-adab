"""Read-only career guidance content migrated from the new-chat source."""
import json
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data.json"

@lru_cache(maxsize=1)
def get_data():
    with DATA_FILE.open(encoding="utf-8") as f:
        return json.load(f)

def field_by_id(field_id):
    return next((x for x in get_data()["FIELDS"] if x["id"] == field_id), None)

def major_by_id(major_id):
    return next((x for x in get_data()["MAJORS"] if x["id"] == major_id), None)

def job_by_id(job_id):
    return next((x for x in get_data()["JOBS"] if x["id"] == job_id), None)
