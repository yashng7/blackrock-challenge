import psutil
import threading

_last_request_time = 0.0


def set_request_time(duration: float):
    global _last_request_time
    _last_request_time = duration


def get_performance_metrics() -> dict:
    elapsed = _last_request_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = elapsed % 60
    seconds_int = int(seconds)
    milliseconds = int((seconds - seconds_int) * 1000)
    time_str = f"{hours:02d}:{minutes:02d}:{seconds_int:02d}.{milliseconds:03d}"

    process = psutil.Process()
    memory_mb = process.memory_info().rss / (1024 * 1024)
    memory_str = f"{memory_mb:.2f} MB"

    return {
        "time": time_str,
        "memory": memory_str,
        "threads": threading.active_count(),
    }