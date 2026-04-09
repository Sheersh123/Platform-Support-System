from fastapi import FastAPI
<<<<<<< HEAD
from monitor import metrics, monitor_services
import statistics
=======
from monitor.monitor import monitor_services, metrics
>>>>>>> ee85057b8f0633b77ec646cf03c5bb5302420425
import threading
import statistics

app = FastAPI()
<<<<<<< HEAD
@app.get("/")
def home():
    return {"message": "Monitoring Service Running "}
@app.on_event("startup")
def start_monitor():
    thread = threading.Thread(target=monitor_services)
    thread.daemon = True
    thread.start()
=======

@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def start_monitor():
    thread = threading.Thread(target=monitor_services, daemon=True)
    thread.start()

>>>>>>> ee85057b8f0633b77ec646cf03c5bb5302420425
@app.get("/metrics")
def get_metrics():
    result = {}
    for service, data in metrics.items():
        total = data["total"]
<<<<<<< HEAD

        uptime = (data["uptime"] / total * 100) if total else 0
        error_rate = (data["errors"] / total * 100) if total else 0
        avg_latency = (
            statistics.mean(data["latencies"])
            if data["latencies"]
            else 0
        )
=======
        uptime = (data["uptime"] / total * 100) if total > 0 else 0
        avg_latency = statistics.mean(data["latencies"]) if data["latencies"] else 0

>>>>>>> ee85057b8f0633b77ec646cf03c5bb5302420425
        result[service] = {
            "uptime_percentage": round(uptime, 2),
            "avg_latency": round(avg_latency, 3),
            "errors": data["errors"]
        }

    return result
