from fastapi import FastAPI
from monitor import metrics, monitor_services
import statistics
import threading
from prometheus_client import start_http_server, Gauge
app = FastAPI()
uptime_gauge = Gauge("service_uptime", "Service uptime percentage", ["service"])
error_gauge = Gauge("service_error_rate", "Service error rate", ["service"])
latency_gauge = Gauge("service_latency", "Service latency", ["service"])
@app.on_event("startup")
def start_monitor():
    thread = threading.Thread(target=monitor_services)
    thread.daemon = True
    thread.start()
    start_http_server(9100)
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
        uptime_gauge.labels(service=service).set(uptime)
        error_gauge.labels(service=service).set(error_rate)
        latency_gauge.labels(service=service).set(avg_latency)
        result[service] = {
            "uptime": f"{uptime:.2f}%",
            "error_rate": f"{error_rate:.2f}%",
            "avg_latency": f"{avg_latency:.2f}s"
        }
    return result