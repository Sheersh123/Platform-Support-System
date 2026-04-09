import json
import datetime
LOG_FILE = "../logs/logs.json"
def log_event(service, level, message):
    log = {
        "timestamp": str(datetime.datetime.now()),
        "service": service,
        "level": level,
        "message": message
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")