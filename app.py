import tkinter as tk
from tkinter import ttk
import psutil
import time
from collections import deque

BG = "#07111F"
CARD = "#0E1C2D"
TEXT = "#EAF2F8"
GREEN = "#20D080"
YELLOW = "#FFC857"
RED = "#FF4D6D"
BLUE = "#4DA3FF"

root = tk.Tk()
root.title("Digital Embedded Immune System")
root.geometry("1200x760")
root.configure(bg=BG)

# ---------- DATA ----------
cpu_history = deque(maxlen=60)
ram_history = deque(maxlen=60)
battery_history = deque(maxlen=60)

last_net = psutil.net_io_counters()
last_time = time.time()

# ---------- HEADER ----------
tk.Label(
    root,
    text="🛡 DIGITAL EMBEDDED IMMUNE SYSTEM",
    font=("Arial", 25, "bold"),
    bg=BG,
    fg=TEXT
).pack(pady=(15, 2))

tk.Label(
    root,
    text="LIVE MONITORING • DETECTION • DIAGNOSIS • IMMUNE RESPONSE • RECOVERY",
    font=("Arial", 11),
    bg=BG,
    fg=BLUE
).pack()

status = tk.Label(
    root,
    text="● SYSTEM INITIALIZING",
    font=("Arial", 17, "bold"),
    bg=BG,
    fg=GREEN
)
status.pack(pady=10)

# ---------- CARDS ----------
card_frame = tk.Frame(root, bg=BG)
card_frame.pack(fill="x", padx=20)

values = {}

for name in ["CPU", "RAM", "BATTERY", "NETWORK"]:
    box = tk.Frame(card_frame, bg=CARD)
    box.pack(side="left", expand=True, fill="x", padx=5)

    tk.Label(
        box, text=name,
        font=("Arial", 11, "bold"),
        bg=CARD, fg=TEXT
    ).pack(pady=(12, 2))

    values[name] = tk.Label(
        box, text="--",
        font=("Arial", 23, "bold"),
        bg=CARD, fg=GREEN
    )
    values[name].pack(pady=(0, 12))

# ---------- NOTE ----------
message = tk.Label(
    root,
    text="Automatic immune monitoring active...",
    font=("Arial", 12, "bold"),
    bg=BG,
    fg=TEXT
)
message.pack(pady=8)

# ---------- NOTEBOOK ----------
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True, padx=20, pady=10)

monitor_tab = tk.Frame(tabs, bg=BG)
diagnosis_tab = tk.Frame(tabs, bg=BG)
analytics_tab = tk.Frame(tabs, bg=BG)

tabs.add(monitor_tab, text=" LIVE RESOURCE MONITOR ")
tabs.add(diagnosis_tab, text=" FAULT DIAGNOSIS ")
tabs.add(analytics_tab, text=" LIVE ANALYTICS ")

# ---------- PROCESS TABLE ----------
tk.Label(
    monitor_tab,
    text="TOP RESOURCE-CONSUMING PROCESSES",
    font=("Arial", 15, "bold"),
    bg=BG, fg=TEXT
).pack(pady=8)

columns = ("Process", "CPU %", "RAM MB", "Resource Impact")

tree = ttk.Treeview(
    monitor_tab,
    columns=columns,
    show="headings",
    height=14
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=220)

tree.pack(fill="both", expand=True, padx=10, pady=5)

# ---------- DIAGNOSIS ----------
diagnosis = tk.Label(
    diagnosis_tab,
    text="SYSTEM DIAGNOSIS\n\nAnalyzing live device conditions...",
    font=("Arial", 16, "bold"),
    bg=CARD,
    fg=TEXT,
    justify="left",
    anchor="nw",
    padx=25,
    pady=25
)
diagnosis.pack(fill="both", expand=True, padx=20, pady=20)

# ---------- ANALYTICS ----------
canvas = tk.Canvas(
    analytics_tab,
    bg=CARD,
    highlightthickness=0
)
canvas.pack(fill="both", expand=True, padx=20, pady=20)

def draw_graph():
    canvas.delete("all")

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    if w < 100 or h < 100:
        return

    canvas.create_text(
        20, 20,
        text="LIVE SYSTEM LOAD HISTORY",
        anchor="nw",
        fill=TEXT,
        font=("Arial", 15, "bold")
    )

    def graph(data, y_offset, title, color):
        if len(data) < 2:
            return

        points = []
        max_value = 100

        for i, value in enumerate(data):
            x = 40 + (i / max(1, len(data)-1)) * (w-70)
            y = y_offset + 80 - (value / max_value) * 70
            points.extend([x, y])

        canvas.create_text(
            40, y_offset,
            text=title,
            anchor="w",
            fill=color,
            font=("Arial", 10, "bold")
        )

        canvas.create_line(
            *points,
            fill=color,
            width=2
        )

    graph(cpu_history, 60, "CPU", BLUE)
    graph(ram_history, 170, "RAM", GREEN)
    graph(battery_history, 280, "BATTERY", YELLOW)

def diagnose(cpu, ram, battery, plugged):
    problems = []
    actions = []

    if cpu >= 85:
        problems.append("Very high CPU load")
        actions.append("Check top CPU-consuming process")

    elif cpu >= 65:
        problems.append("Increasing CPU load")
        actions.append("Monitor heavy applications")

    if ram >= 90:
        problems.append("Very high memory usage")
        actions.append("Close unnecessary applications")

    elif ram >= 75:
        problems.append("High memory usage")
        actions.append("Monitor memory-consuming processes")

    if battery >= 0 and battery <= 20 and not plugged:
        problems.append("LOW POWER CONDITION")
        actions.append("Connect charger / enable power saving")

    if not problems:
        return (
            "SYSTEM STATUS: SECURE\n\n"
            "✓ CPU within normal range\n"
            "✓ Memory within normal range\n"
            "✓ Power condition normal\n\n"
            "IMMUNE RESPONSE:\n"
            "Continuous monitoring active."
        )

    text = "SYSTEM STATUS: THREAT / WARNING\n\n"

    for p in problems:
        text += "⚠ " + p + "\n"

    text += "\nRECOMMENDED IMMUNE RESPONSE:\n"

    for a in actions:
        text += "→ " + a + "\n"

    text += "\nRecovery monitoring: ACTIVE"

    return text

def update():
    global last_net, last_time

    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent

    battery_obj = psutil.sensors_battery()

    if battery_obj:
        battery = battery_obj.percent
        plugged = battery_obj.power_plugged
    else:
        battery = 100
        plugged = True

    # Network speed
    now = time.time()
    current_net = psutil.net_io_counters()

    elapsed = max(now - last_time, 0.1)

    sent = current_net.bytes_sent - last_net.bytes_sent
    recv = current_net.bytes_recv - last_net.bytes_recv

    network_speed = (sent + recv) / elapsed / 1024

    last_net = current_net
    last_time = now

    # Update cards
    values["CPU"].config(text=f"{cpu:.1f}%")
    values["RAM"].config(text=f"{ram:.1f}%")
    values["BATTERY"].config(text=f"{battery:.0f}%")

    if network_speed > 1024:
        values["NETWORK"].config(
            text=f"{network_speed/1024:.1f} MB/s"
        )
    else:
        values["NETWORK"].config(
            text=f"{network_speed:.0f} KB/s"
        )

    # History
    cpu_history.append(cpu)
    ram_history.append(ram)
    battery_history.append(battery)

    # Process list
    for item in tree.get_children():
        tree.delete(item)

    processes = []

    for p in psutil.process_iter(
        ["name", "memory_info", "cpu_percent"]
    ):
        try:
            name = p.info["name"] or "Unknown"
            mem = p.info["memory_info"].rss / (1024 * 1024)
            pcpu = p.info["cpu_percent"] or 0

            # Estimated resource impact
            impact_score = pcpu * 0.7 + min(mem / 10, 30)

            processes.append(
                (impact_score, pcpu, mem, name)
            )

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    processes.sort(reverse=True)

    for score, pcpu, mem, name in processes[:12]:

        if score >= 50:
            impact = "HIGH"
        elif score >= 20:
            impact = "MEDIUM"
        else:
            impact = "LOW"

        tree.insert(
            "",
            "end",
            values=(
                name,
                f"{pcpu:.1f}",
                f"{mem:.1f}",
                impact
            )
        )

    # Status
    if battery <= 20 and not plugged:
        status.config(
            text="● LOW POWER WARNING",
            fg=RED
        )

        message.config(
            text="⚠ Battery low — power saving recommended",
            fg=RED
        )

    elif cpu >= 85 or ram >= 90:
        status.config(
            text="● CRITICAL THREAT DETECTED",
            fg=RED
        )

        message.config(
            text="⚠ High resource usage detected — immune response active",
            fg=RED
        )

    elif cpu >= 65 or ram >= 75:
        status.config(
            text="● WARNING",
            fg=YELLOW
        )

        message.config(
            text="⚠ Increasing resource load detected",
            fg=YELLOW
        )

    else:
        status.config(
            text="● SYSTEM SECURE",
            fg=GREEN
        )

        message.config(
            text="✓ Device operating normally — continuous protection active",
            fg=GREEN
        )

    # Diagnosis
    diagnosis.config(
        text=diagnose(cpu, ram, battery, plugged)
    )

    # Graph
    draw_graph()

    # Automatic refresh
    root.after(1500, update)

update()

root.mainloop()
