import requests
import time
from .incident_engine import detect_incidents
from .alert import send_alert
from .recovery import recover
from .logger import log_event

SERVICES = {
    "self_check": "https://platform-support-system.onrender.com/health"
}

metrics = {
    "self_check": {
        "uptime": 0,
        "total": 0,
        "errors": 0,
        "latencies": []
    }
}

def monitor_services():
    while True:
        try:
            for name, url in SERVICES.items():
                start = time.time()

                try:
                    response = requests.get(url, timeout=2)
                    latency = time.time() - start

                    metrics[name]["total"] += 1
                    metrics[name]["latencies"].append(latency)

                    # prevent memory leak
                    if len(metrics[name]["latencies"]) > 100:
                        metrics[name]["latencies"].pop(0)

                    if response.status_code == 200:
                        metrics[name]["uptime"] += 1
                    else:
                        metrics[name]["errors"] += 1
                        log_event(name, "ERROR", f"Bad response: {response.status_code}")

                        incident = detect_incidents(name, metrics[name])
                        if incident:
                            send_alert(name, incident)
                            recover(name)

                except requests.exceptions.RequestException as e:
                    metrics[name]["total"] += 1
                    metrics[name]["errors"] += 1

                    log_event(name, "CRITICAL", f"Service unreachable: {str(e)}")

                    incident = detect_incidents(name, metrics[name])
                    if incident:
                        send_alert(name, incident)
                        recover(name)

            time.sleep(5)

        except Exception as e:
            print("Monitor loop error:", str(e))
            time.sleep(5)
