import psutil
import platform
import socket
from datetime import datetime, timedelta


def get_system_health():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    disk = psutil.disk_usage("C:\\")

    return {
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "os": platform.platform(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": disk.percent,
        "disk_free_gb": round(disk.free / (1024 ** 3), 2),
        "uptime": str(timedelta(seconds=int(uptime.total_seconds()))),
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def get_top_processes(limit=8):
    processes = []

    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
        try:
            info = proc.info
            memory_mb = info["memory_info"].rss / (1024 * 1024)
            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "cpu_percent": info["cpu_percent"],
                "memory_mb": round(memory_mb, 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    processes = sorted(processes, key=lambda p: p["memory_mb"], reverse=True)
    return processes[:limit]


def calculate_health_score(health, logs):
    score = 100

    if health["cpu_percent"] > 85:
        score -= 15
    if health["memory_percent"] > 80:
        score -= 15
    if health["disk_percent"] > 85:
        score -= 20
    if logs["failed_logins"] > 5:
        score -= 10
    if logs["critical_errors"] > 0:
        score -= 15
    if logs["warnings"] > 5:
        score -= 5

    return max(score, 0)
