import tkinter as tk
from tkinter import ttk
import psutil
from datetime import datetime

BG = "#07111f"
CARD = "#0d1b2a"
TEXT = "#e8f1f8"
GREEN = "#00d084"
YELLOW = "#ffc857"
RED = "#ff4d6d"
BLUE = "#4dabf7"

root = tk.Tk()
root.title("Digital Embedded Immune System")
root.geometry("1100x700")
root.configure(bg=BG)

title = tk.Label(root, text="🛡 DIGITAL EMBEDDED IMMUNE SYSTEM",
                 font=("Arial", 24, "bold"), bg=BG, fg=TEXT)
title.pack(pady=15)

subtitle = tk.Label(root,
    text="LIVE DEVICE MONITOR • DETECT • DIAGNOSE • PROTECT • RECOVER",
    font=("Arial", 11), bg=BG, fg=BLUE)
subtitle.pack()

status = tk.Label(root, text="SYSTEM INITIALIZING...",
                  font=("Arial", 18, "bold"), bg=BG, fg=GREEN)
status.pack(pady=12)

cards = tk.Frame(root, bg=BG)
cards.pack(fill="x", padx=20)

labels = {}
for name in ["CPU", "RAM", "BATTERY", "NETWORK"]:
    f = tk.Frame(cards, bg=CARD, padx=25, pady=15)
    f.pack(side="left", expand=True, fill="x", padx=5)
    tk.Label(f, text=name, font=("Arial", 11, "bold"),
             bg=CARD, fg=TEXT).pack()
    labels[name] = tk.Label(f, text="--", font=("Arial", 22, "bold"),
                            bg=CARD, fg=GREEN)
    labels[name].pack()

info = tk.Label(root, text="Analyzing device...",
                font=("Arial", 12), bg=BG, fg=TEXT)
info.pack(pady=12)

tk.Label(root, text="LIVE RESOURCE CONSUMERS",
         font=("Arial", 15, "bold"), bg=BG, fg=TEXT).pack()

columns = ("Process", "CPU %", "RAM MB", "Impact")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

for c in columns:
    tree.heading(c, text=c)
    tree.column(c, width=200)

tree.pack(fill="both", expand=True, padx=25, pady=10)

alert = tk.Label(root, text="IMMUNE SYSTEM: MONITORING",
                 font=("Arial", 13, "bold"), bg=CARD, fg=GREEN)
alert.pack(fill="x", padx=25, pady=10)

previous_battery = None

def update():
    global previous_battery

    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent

    battery_obj = psutil.sensors_battery()
    battery = battery_obj.percent if battery_obj else 0

    net = psutil.net_io_counters()
    network = (net.bytes_sent + net.bytes_recv) / (1024 * 1024)

    labels["CPU"].config(text=f"{cpu:.1f}%")
    labels["RAM"].config(text=f"{ram:.1f}%")
    labels["BATTERY"].config(text=f"{battery:.0f}%")
    labels["NETWORK"].config(text=f"{network:.1f} MB")

    for item in tree.get_children():
        tree.delete(item)

    processes = []

    for p in psutil.process_iter(["name", "memory_info"]):
        try:
            name = p.info["name"] or "Unknown"
            mem = p.info["memory_info"].rss / (1024 * 1024)
            pcpu = p.cpu_percent(None)
            processes.append((pcpu, mem, name))
        except:
            pass

    processes.sort(reverse=True)

    for pcpu, mem, name in processes[:10]:
        impact = "HIGH" if pcpu > 30 or mem > 500 else "NORMAL"
        tree.insert("", "end",
                    values=(name, f"{pcpu:.1f}", f"{mem:.1f}", impact))

    if battery_obj and not battery_obj.power_plugged and battery <= 20:
        state = "LOW POWER WARNING"
        color = RED
        message = "⚠ Battery low — power saving recommended"
    elif cpu >= 80 or ram >= 85:
        state = "THREAT DETECTED"
        color = RED
        message = "⚠ High resource usage detected"
    elif cpu >= 60 or ram >= 70:
        state = "WARNING"
        color = YELLOW
        message = "⚠ Increasing resource load detected"
    else:
        state = "SECURE"
        color = GREEN
        message = "✓ Device operating normally"

    status.config(text=f"● {state}", fg=color)
    alert.config(text=f"IMMUNE RESPONSE: {message}", fg=color)

    if previous_battery is not None and battery < previous_battery - 2:
        info.config(text="Battery level decreased — monitoring power condition...",
                    fg=YELLOW)
    else:
        info.config(text=f"Last scan: {datetime.now().strftime('%H:%M:%S')} | "
                         "Automatic monitoring active",
                    fg=TEXT)

    previous_battery = battery
    root.after(1500, update)

update()
root.mainloop()
