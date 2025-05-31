# app.py
import os
import time
import threading
from flask import Flask, send_from_directory

UPLOAD_DIR = "downloads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)

@app.route("/file/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)

# Delete files older than 24 hours
def cleanup():
    while True:
        now = time.time()
        for file in os.listdir(UPLOAD_DIR):
            path = os.path.join(UPLOAD_DIR, file)
            if os.path.isfile(path) and (now - os.path.getmtime(path)) > 86400:
                os.remove(path)
        time.sleep(3600)

threading.Thread(target=cleanup, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
