import requests
import time
from .incident_engine import detect_incidents
from .alert import send_alert
from recovery import recover
from logger import log_event
SERVICES = {
    "service_a": "http://localhost:8001/health",
    "service_b": "http://localhost:8002/health",
    "service_c": "http://localhost:8003/health"
}
metrics = {
    "service_a": {"uptime": 0, "total": 0, "errors": 0, "latencies": []},
    "service_b": {"uptime": 0, "total": 0, "errors": 0, "latencies": []},
    "service_c": {"uptime": 0, "total": 0, "errors": 0, "latencies": []}
}
def monitor_services():
    while True:
        for name, url in SERVICES.items():
            start = time.time()
            try:
                response = requests.get(url, timeout=2)
                latency = time.time() - start
                metrics[name]["total"] += 1
                metrics[name]["latencies"].append(latency)
                if response.status_code == 200:
                    metrics[name]["uptime"] += 1
                else:
                    metrics[name]["errors"] += 1
            except Exception as e:
                metrics[name]["total"] += 1
                metrics[name]["errors"] += 1
                log_event(name, "CRITICAL", f"Service unreachable: {str(e)}")
