import psutil
import threading
import time
import platform
from collections import deque


class SystemMonitor:
    def __init__(self, interval=1, bucket_size=60, window=1440, logger=None):
        # 1 second * 60 seconds per tracking instance * 1440 minutes per day = one day of tracking
        self.interval = interval
        self.running = False
        self.thread = None
        self.last_cpu_usage = 0
        self.last_ram_usage = 0
        self.last_disk_usage = 0
        self.bucket_progress = 0
        self.bucket_size = bucket_size
        self.cpu_usage = deque(maxlen=window)
        self.ram_usage = deque(maxlen=window)
        self.disk_usage = deque(maxlen=window)
        self.lock = threading.Lock()
        self.logger = logger
        self.disk_path = '/' if platform.system() != 'Windows' else 'C:\\'
        self.ram_total_gb = round(psutil.virtual_memory().total/(1024**3), 2)
        self.track_once() # first timestamp on creation
        self.accumulate()

    def accumulate(self):
        with self.lock:
            self.cpu_usage.append(self.last_cpu_usage)
            self.ram_usage.append(self.last_ram_usage)
            self.disk_usage.append(self.last_disk_usage)
            # No need to manually trim - deque handles it automatically
            self.last_cpu_usage = 0
            self.last_ram_usage = 0
            self.last_disk_usage = 0
            self.bucket_progress = 0

    def track_once(self):
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage(self.disk_path).percent
        with self.lock:
            self.last_cpu_usage = max(cpu, self.last_cpu_usage)
            self.last_ram_usage = max(ram, self.last_ram_usage)
            self.last_disk_usage = max(disk, self.last_disk_usage)
            self.bucket_progress += 1
        if self.bucket_progress >= self.bucket_size:
            self.accumulate()

    def __call__(self):
        if self.logger:
            self.logger.info("System monitoring started")
        psutil.cpu_percent(interval=None)
        psutil.disk_usage(self.disk_path)
        self.running = True
        while self.running:
            self.track_once()
            time.sleep(self.interval)

    def unsafe_status(self):
        # usage pattern should be like this:
        # with monitor.lock: return monitor.unsafe_status()
        return {
            "cpu": list(self.cpu_usage),
            "ram": list(self.ram_usage),
            "disk": list(self.disk_usage),
            "ram_total_gb": self.ram_total_gb
        }
