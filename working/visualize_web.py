import io, json, time
from flask import Flask, Response
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

THREAT_JSON = "../analysis_output/threat_ip.json"

app = Flask(__name__)

def load_stats():
    try:
        with open(THREAT_JSON, "r") as f:
            data = json.load(f)
        return data.get("stats", {})
    except Exception:
        return {}

@app.get("/")
def index():
    # cache-bust so browser reloads image every time
    return f"""
    <html>
      <head><meta http-equiv="refresh" content="5"></head>
      <body>
        <h3>SSH Threat Dashboard (refresh 5s)</h3>
        <img src="/plot.png?t={int(time.time())}" />
      </body>
    </html>
    """

@app.get("/plot.png")
def plot_png():
    stats = load_stats()
    labels = ["brute_force", "lockout", "pam_failure", "other_failed"]
    values = [int(stats.get(k, 0)) for k in labels]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color=["red", "orange", "blue", "green"])
    ax.set_title("SSH Threats")
    ax.set_ylabel("Count")
    ax.grid(True, axis="y", alpha=0.3)

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype="image/png")

if __name__ == "__main__":
    try :
        app.run(host="0.0.0.0", port=8080)
        print("Check the dashboard at http://localhost:8080")
    except KeyboardInterrupt as error :
        print("Thanks for using \n follow me on Linkedin to Stay Secured ")
    except Exception as error :
        print(f"Error: {error}")
        print("Do you install the required dependencies? If not, run 'pip install -r requirements.txt' to install them.")