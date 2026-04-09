from fastapi import FastAPI
from monitor import metrics, monitor_services
import statistics
from monitor.monitor import monitor_services, metrics
import threading
import statistics

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Monitoring Service Running "}
@app.on_event("startup")
def start_monitor():
    thread = threading.Thread(target=monitor_services)
    thread.daemon = True
    thread.start()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def start_monitor():
    thread = threading.Thread(target=monitor_services, daemon=True)
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
        uptime = (data["uptime"] / total * 100) if total > 0 else 0
        avg_latency = statistics.mean(data["latencies"]) if data["latencies"] else 0

        result[service] = {
            "uptime_percentage": round(uptime, 2),
            "avg_latency": round(avg_latency, 3),
            "errors": data["errors"]
        }

    return result
