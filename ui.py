import tkinter as tk
from tkinter import ttk
import psutil
import platform

class DashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Monitor Dashboard")
        self.geometry("550x400")
        self.configure(bg="#1e1e1e")

        # Estilos 
        style = ttk.Style(self)
        style.theme_use("clam")

        # Barras dinámicas
        style.configure("Green.Horizontal.TProgressbar", thickness=25, troughcolor="#333", background="#4caf50")
        style.configure("Yellow.Horizontal.TProgressbar", thickness=25, troughcolor="#333", background="#ffb300")
        style.configure("Red.Horizontal.TProgressbar", thickness=25, troughcolor="#333", background="#e53935")

        style.configure("TButton", font=("Arial", 12), padding=6)

        # Widgets
        self._create_row(0, "CPU")
        self._create_row(1, "RAM")
        self._create_row(2, "Disco")
        self._create_row(3, "Red")

        # Botón de cierre
        self.close_button = ttk.Button(self, text="Cerrar App", command=self.destroy)
        self.close_button.grid(row=4, column=0, columnspan=3, pady=20)

        # Detectar disco principal (multiplataforma)
        self.disk_mount = self._detect_main_disk()

        # Guardar estado de red
        self.last_net = psutil.net_io_counters()

        # Arrancar actualización
        self.update_metrics()

    # Crear fila
    def _create_row(self, row, label):
        lbl = tk.Label(self, text=label, font=("Arial", 14), bg="#1e1e1e", fg="white")
        lbl.grid(row=row, column=0, padx=10, pady=10, sticky="w")

        bar = ttk.Progressbar(self, length=300, maximum=100, style="Green.Horizontal.TProgressbar")
        bar.grid(row=row, column=1, padx=10, pady=10)

        val = tk.Label(self, text="0%", font=("Arial", 14), bg="#1e1e1e", fg="white")
        val.grid(row=row, column=2, padx=10, pady=10)

        if label == "CPU":
            self.cpu_bar, self.cpu_value = bar, val
        elif label == "RAM":
            self.ram_bar, self.ram_value = bar, val
        elif label == "Disco":
            self.disk_bar, self.disk_value = bar, val
        elif label == "Red":
            self.net_bar, self.net_value = bar, val

    # Elegir estilo por valor
    def style_for_value(self, val):
        if val < 70:
            return "Green.Horizontal.TProgressbar"
        elif val < 90:
            return "Yellow.Horizontal.TProgressbar"
        else:
            return "Red.Horizontal.TProgressbar"

    # Formato humano para red
    def human_readable(self, bytes_per_s):
        if bytes_per_s > 1024**2:
            return f"{bytes_per_s/1024**2:.2f} MB/s"
        if bytes_per_s > 1024:
            return f"{bytes_per_s/1024:.1f} KB/s"
        return f"{bytes_per_s:.0f} B/s"

    # Detectar disco principal 
    def _detect_main_disk(self):
        system = platform.system()
        if system == "Windows":
            return "C:\\"
        for part in psutil.disk_partitions():
            if "rw" in part.opts or part.mountpoint == "/":
                return part.mountpoint
        return "/"  # fallback

    # Actualizar métricas
    def update_metrics(self):
        # CPU
        cpu = psutil.cpu_percent()
        self.cpu_bar["value"] = cpu
        self.cpu_bar["style"] = self.style_for_value(cpu)
        self.cpu_value.config(text=f"{cpu:.1f}%")

        # RAM
        ram = psutil.virtual_memory().percent
        self.ram_bar["value"] = ram
        self.ram_bar["style"] = self.style_for_value(ram)
        self.ram_value.config(text=f"{ram:.1f}%")

        # Disco
        disk = psutil.disk_usage(self.disk_mount).percent
        self.disk_bar["value"] = disk
        self.disk_bar["style"] = self.style_for_value(disk)
        self.disk_value.config(text=f"{disk:.1f}%")

        # Red
        new_net = psutil.net_io_counters()
        sent_speed_b = new_net.bytes_sent - self.last_net.bytes_sent
        recv_speed_b = new_net.bytes_recv - self.last_net.bytes_recv
        total_speed_b = sent_speed_b + recv_speed_b

        # Barra arbitraria: escala simple (100% = 10MB/s)
        usage = min(total_speed_b / (10 * 1024**2) * 100, 100)

        self.net_bar["value"] = usage
        self.net_bar["style"] = self.style_for_value(usage)
        self.net_value.config(text=self.human_readable(total_speed_b))

        self.last_net = new_net

        # Volver a llamar en 1s
        self.after(1000, self.update_metrics)
