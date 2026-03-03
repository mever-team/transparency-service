import psutil
import threading
import time
import platform


class SystemMonitor:
    def __init__(self, interval=1, logger=None):
        self.interval = interval
        self.running = False
        self.thread = None
        self.cpu_usage = []
        self.ram_usage = []  # Percentage
        self.disk_usage = []  # Percentage
        self.lock = threading.Lock()
        self.logger = logger
        self.disk_path = '/' if platform.system() != 'Windows' else 'C:\\'
        self.ram_total_gb = round(psutil.virtual_memory().total/(1024**3), 2)
        self.track_once() # first timestamp on creation

    def track_once(self):
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage(self.disk_path).percent
        with self.lock:
            self.cpu_usage.append(cpu)
            self.ram_usage.append(ram)
            self.disk_usage.append(disk)

    def __call__(self):
        if self.logger: self.logger.info("System monitoring started")
        psutil.cpu_percent(interval=None)
        psutil.disk_usage(self.disk_path)
        self.running = True
        while self.running:
            self.track_once()
            time.sleep(self.interval)

    def unsafe_status(self):
        # usage pattern should be like this:
        # with monitor.lock: return monitor.unsafe_status()
        return {"cpu": self.cpu_usage, "ram": self.ram_usage, "disk": self.disk_usage, "ram_total_gb": self.ram_total_gb}
