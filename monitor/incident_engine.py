def detect_incidents(metrics):
    incidents = []
    for service, data in metrics.items():
        total = data["total"]
        if total == 0:
            continue
        error_rate = data["errors"] / total
        avg_latency = (
            sum(data["latencies"]) / len(data["latencies"])
            if data["latencies"] else 0
        )
        if error_rate == 1:
            incidents.append((service, "Service Down", "CRITICAL"))
        elif error_rate > 0.5:
            incidents.append((service, "High Error Rate", "HIGH"))
        elif avg_latency > 1:
            incidents.append((service, "High Latency", "MEDIUM"))
    return incidents