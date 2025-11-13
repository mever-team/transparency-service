import platform, subprocess, psutil
import types
import inspect

def human_readable_time(seconds: float) -> str:
    if seconds < 1e-3:  # less than 1 millisecond
        return f"{seconds * 1e6:.2f}µs"
    elif seconds < 1:  # less than 1 second
        return f"{seconds * 1e3:.2f}ms"
    elif seconds < 60:  # less than 1 minute
        return f"{seconds:.2f}s"
    elif seconds < 3600:  # less than 1 hour
        minutes = int(seconds // 60)
        sec = seconds % 60
        return f"{minutes}min {sec:.2f}s"
    else:  # 1 hour or more
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        sec = seconds % 60
        return f"{hours}h {minutes}min {sec:.2f}s"

def get_hardware_info():
    cpu_info = "Not found"
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    cpu_info = line.strip().split(":")[1].strip()
    except FileNotFoundError:
        cpu_info = platform.processor() or platform.machine()

    ram_bytes = psutil.virtual_memory().total
    ram_gb = round(ram_bytes / (1024 ** 3), 2)
    cuda_version = "Not found"
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "CUDA Version" in line:
                    cuda_version = line.strip()
                    break
    except FileNotFoundError:
        pass
    if cuda_version == "Not found":
        try:
            result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "release" in line:
                        cuda_version = line.strip()
                        break
        except FileNotFoundError:
            pass

    return f"CPU: {cpu_info}, RAM: {ram_gb} GB, CUDA: {cuda_version}"


def get_callable_source(obj):
    if isinstance(obj, (types.FunctionType, types.MethodType, types.BuiltinFunctionType)):
        return inspect.getsource(obj)

    if callable(obj):
        return inspect.getsource(obj.__call__)

    return ''