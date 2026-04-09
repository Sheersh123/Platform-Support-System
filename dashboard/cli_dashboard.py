import requests
import time
import os

METRICS_URL = "http://127.0.0.1:9000/metrics"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def get_status(error_rate):
    error = float(error_rate.replace("%", ""))

    if error > 80:
        return "🔴 CRITICAL"
    elif error > 40:
        return "🟠 WARNING"
    else:
        return "🟢 HEALTHY"

def show_dashboard():
    while True:
        try:
            data = requests.get(METRICS_URL).json()

            clear()
            print("=" * 50)
            print("PLATFORM SUPPORT DASHBOARD")
            print("=" * 50)

            for service, metrics in data.items():
                status = get_status(metrics["error_rate"])

                print(f"\n🔹 {service.upper()}")
                print(f"   Status        : {status}")
                print(f"   Uptime        : {metrics['uptime']}")
                print(f"   Error Rate    : {metrics['error_rate']}")
                print(f"   Avg Latency   : {metrics['avg_latency']}")
                print("-" * 50)

        except Exception as e:
            print("Error fetching metrics:", e)

        time.sleep(5)

if __name__ == "__main__":
    show_dashboard()