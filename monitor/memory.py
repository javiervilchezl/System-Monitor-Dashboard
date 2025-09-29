import psutil

def get_memory_usage():
    """Devuelve el porcentaje de uso de RAM."""
    return psutil.virtual_memory().percent
