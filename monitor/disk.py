import psutil

def get_disk_usage():
    """Devuelve un diccionario con el uso de cada partición."""
    usage = {}
    for part in psutil.disk_partitions():
        try:
            usage[part.device] = psutil.disk_usage(part.mountpoint).percent
        except PermissionError:
            continue
    return usage
