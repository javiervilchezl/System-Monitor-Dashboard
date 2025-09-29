import tkinter as tk
from tkinter import ttk
import psutil

class DashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Monitor Dashboard")
        self.geometry("500x350")
        self.configure(bg="#1e1e1e")  # Dark theme

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TProgressbar", thickness=25, troughcolor="#333333", background="#4caf50")
        style.configure("TButton", font=("Arial", 12), padding=6)

        # CPU
        self.cpu_label = tk.Label(self, text="CPU", font=("Arial", 14), bg="#1e1e1e", fg="white")
        self.cpu_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.cpu_bar = ttk.Progressbar(self, length=300, maximum=100, style="TProgressbar")
        self.cpu_bar.grid(row=0, column=1, padx=10, pady=10)
        self.cpu_value = tk.Label(self, text="0%", font=("Arial", 14), bg="#1e1e1e", fg="white")
        self.cpu_value.grid(row=0, column=2, padx=10, pady=10)

        # RAM
        self.ram_label = tk.Label(self, text="RAM", font=("Arial", 14), bg="#1e1e1e", fg="white")
        self.ram_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.ram_bar = ttk.Progressbar(self, length=300, maximum=100, style="TProgressbar")
        self.ram_bar.grid(row=1, column=1, padx=10, pady=10)
        self.ram_value = tk.Label(self, text="0%", font=("Arial", 14), bg="#1e1e1e", fg="white")
        self.ram_value.grid(row=1, column=2, padx=10, pady=10)

        # DISK
        self.disk_label = tk.Label(self, text="Disco", font=("Arial", 14), bg="#1e1e1e", fg="white")
        self.disk_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.disk_bar = ttk.Progressbar(self, length=300, maximum=100, style="TProgressbar")
        self.disk_bar.grid(row=2, column=1, padx=10, pady=10)
        self.disk_value = tk.Label(self, text="0%", font=("Arial", 14), bg="#1e1e1e", fg="white")
        self.disk_value.grid(row=2, column=2, padx=10, pady=10)

        # NETWORK
        self.net_label = tk.Label(self, text="Red", font=("Arial", 14), bg="#1e1e1e", fg="white")
        self.net_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.net_bar = ttk.Progressbar(self, length=300, maximum=100, style="TProgressbar")
        self.net_bar.grid(row=3, column=1, padx=10, pady=10)
        self.net_value = tk.Label(self, text="0 KB/s", font=("Arial", 14), bg="#1e1e1e", fg="white")
        self.net_value.grid(row=3, column=2, padx=10, pady=10)

        # BOTÓN DE CERRAR
        self.close_button = ttk.Button(self, text="Cerrar App", command=self.destroy)
        self.close_button.grid(row=4, column=0, columnspan=3, pady=20)

        # Actualización periódica
        self.last_net = psutil.net_io_counters()
        self.update_metrics()

    def update_metrics(self):
        # CPU
        cpu = psutil.cpu_percent()
        self.cpu_bar["value"] = cpu
        self.cpu_value.config(text=f"{cpu:.1f}%")

        # RAM
        ram = psutil.virtual_memory().percent
        self.ram_bar["value"] = ram
        self.ram_value.config(text=f"{ram:.1f}%")

        # Disco (usar raíz del sistema)
        disk = psutil.disk_usage("/").percent
        self.disk_bar["value"] = disk
        self.disk_value.config(text=f"{disk:.1f}%")

        # Red (velocidad)
        new_net = psutil.net_io_counters()
        sent_speed = (new_net.bytes_sent - self.last_net.bytes_sent) / 1024
        recv_speed = (new_net.bytes_recv - self.last_net.bytes_recv) / 1024
        total_speed = sent_speed + recv_speed
        usage = min(total_speed / 1024 * 100, 100)  # escala simple máx 100
        self.net_bar["value"] = usage
        self.net_value.config(text=f"{total_speed:.1f} KB/s")
        self.last_net = new_net

        # Refrescar cada segundo
        self.after(1000, self.update_metrics)
