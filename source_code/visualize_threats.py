import json
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
THREAT_JSON = Path(__file__).with_name("threat_ip.json")
def load_attack_counts():
    with THREAT_JSON.open("r", encoding="utf-8") as file:
        data = json.load(file)
    attack_details = data.get("attack_details", {})
    return {name: details.get("failed_attempts", 0) for name, details in attack_details.items()}
fig, ax = plt.subplots(figsize=(8, 5))
def update(frame):
    counts = load_attack_counts()
    labels = list(counts.keys())
    values = [counts[label] for label in labels]
    ax.clear()
    bars = ax.bar(labels, values, color=["#e74c3c", "#f39c12", "#3498db", "#2ecc71"])
    ax.set_title("Attack Type Counts from threat_ip.json")
    ax.set_xlabel("Attack Type")
    ax.set_ylabel("Failed Attempts")
    ax.set_ylim(0, max(values + [1]) * 1.1)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 1, str(value), ha="center", va="bottom", fontsize=10)
    plt.tight_layout()
animation = FuncAnimation(fig, update, interval=5000)
try:
    plt.show()
except KeyboardInterrupt as error :
    print("Thanks for using \n follow me on Linkedin to Stay Secured ")
