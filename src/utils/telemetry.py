"""System telemetry, memory, and performance monitoring."""

import os
import time
from typing import Dict, Any


class SystemTelemetry:
    """Collects runtime memory usage, uptime, and hardware telemetry."""

    def __init__(self):
        self._start_time = time.time()

    def get_metrics(self) -> Dict[str, Any]:
        """Collect current process runtime telemetry."""
        uptime = time.time() - self._start_time
        pid = os.getpid()

        mem_info = {"rss_mb": 0.0}
        try:
            import psutil
            proc = psutil.Process(pid)
            mem_info["rss_mb"] = round(proc.memory_info().rss / (1024 * 1024), 2)
            mem_info["cpu_pct"] = proc.cpu_percent(interval=None)
        except ImportError:
            pass

        return {
            "uptime_seconds": round(uptime, 2),
            "pid": pid,
            "memory": mem_info,
        }
