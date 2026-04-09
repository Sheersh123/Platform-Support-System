import random

recovery_stats = {
    "attempts": 0,
    "success": 0,
    "failure": 0
}
def recover(service, issue):
    recovery_stats["attempts"] += 1
    print(f" Attempting recovery for {service} due to {issue}")
    if random.random() > 0.3:
        recovery_stats["success"] += 1
        print(f"Recovery successful for {service}")
        return True
    else:
        recovery_stats["failure"] += 1
        print(f" Recovery failed for {service}")
        return False