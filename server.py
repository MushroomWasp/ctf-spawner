#!/usr/bin/env python3
import subprocess
import random
import string
import threading
import time
from flask import Flask, request, jsonify

# =========================
# CONFIGURATION CONSTANTS
# =========================
INSTANCE_LIFETIME = 300          # seconds before instance stops
PORT_RANGE = (20000, 30000)      # range of random ports
SERVER_IP = "138.68.65.113"      # public server IP

# Team tokens (example)
TOKENS = {
    "team1token": False,
    "team2token": False,
    "team3token": False
}

# =========================
# GLOBAL STATE
# =========================
app = Flask(__name__)
instances = {}  # {token: {"name": str, "port": int}}

# =========================
# UTILS
# =========================
def random_name(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def stop_instance(token):
    """Stop instance for a token."""
    if token not in instances:
        return

    name = instances[token]["name"]
    port = instances[token]["port"]

    with open("/dev/null", "w") as devnull:
        subprocess.Popen(
            ["./script.sh", "STOP", name],
            stdout=devnull,
            stderr=devnull
        )

    print(f"[INFO] Stopped instance {name} (token={token}) on port {port}")
    instances.pop(token, None)
    TOKENS[token] = False  # mark as off

def start_instance(token):
    """Start a new instance for a token (replaces old one if needed)."""
    # If instance exists, stop it first
    if token in instances:
        stop_instance(token)

    port = random.randint(*PORT_RANGE)
    name = random_name()

    with open("/dev/null", "w") as devnull:
        subprocess.Popen(
            ["./script.sh", "START", str(port), name],
            stdout=devnull,
            stderr=devnull
        )

    print(f"[INFO] Started instance {name} (token={token}) on port {port}")

    # Track instance
    instances[token] = {"name": name, "port": port}
    TOKENS[token] = True  # mark as on

    # Build URL
    url = f"http://{SERVER_IP}:{port}/"
    print(f"[LINK] {url}")

    # Schedule automatic stop
    def delayed_stop():
        time.sleep(INSTANCE_LIFETIME)
        stop_instance(token)

    threading.Thread(target=delayed_stop, daemon=True).start()

    return {"url": url, "name": name}

# =========================
# ROUTES
# =========================
@app.route("/spawn", methods=["POST"])
def spawn():
    data = request.get_json(force=True)
    token = data.get("token")

    if token not in TOKENS:
        return jsonify({"error": "Invalid token"}), 403

    result = start_instance(token)
    return jsonify(result)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8484)
