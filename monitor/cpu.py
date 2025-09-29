import psutil

def get_cpu_usage():
    """Devuelve el uso actual de CPU en porcentaje."""
    return psutil.cpu_percent(interval=1)
