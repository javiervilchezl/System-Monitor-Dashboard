import psutil

def get_network_usage():
    """Devuelve bytes enviados y recibidos desde el arranque."""
    net_io = psutil.net_io_counters()
    return {
        "sent": net_io.bytes_sent,
        "recv": net_io.bytes_recv
    }
