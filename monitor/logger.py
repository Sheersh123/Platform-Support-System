<<<<<<< HEAD
import json
from datetime import datetime

LOG_FILE = "logs.json"

def log_event(service, level, message):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "service": service,
        "level": level,
        "message": message
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")
=======
def log_event(service, level, message):
    print(f"[{level}] [{service}] {message}")
>>>>>>> ee85057b8f0633b77ec646cf03c5bb5302420425
