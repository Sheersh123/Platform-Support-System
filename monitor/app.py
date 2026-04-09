from fastapi import FastAPI
from monitor import metrics, monitor_services
import statistics
import threading
app = FastAPI()
@app.on_event("startup")
def start_monitor():
    thread = threading.Thread(target=monitor_services)
    thread.daemon = True
    thread.start()
@app.get("/metrics")
def get_metrics():
    result = {}
    for service, data in metrics.items():
        total = data["total"]
        uptime = (data["uptime"] / total * 100) if total else 0
        error_rate = (data["errors"] / total * 100) if total else 0
        avg_latency = (
            statistics.mean(data["latencies"])
            if data["latencies"]
            else 0
        )
        result[service] = {
            "uptime": f"{uptime:.2f}%",
            "error_rate": f"{error_rate:.2f}%",
            "avg_latency": f"{avg_latency:.2f}s"
        }
    return result