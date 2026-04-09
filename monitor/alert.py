import datetime
def send_alert(service, issue, severity):
    alert = {
        "service": service,
        "issue": issue,
        "severity": severity,
        "timestamp": str(datetime.datetime.now())
    }
    print(f"ALERT → {alert}")