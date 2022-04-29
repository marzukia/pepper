import threading
from flask import Flask, send_file, send_from_directory

from pepper.server.watcher import run_watcher

app = Flask(__name__)

PROJECT_PATH = "../example/"


@app.route("/")
def serve_index():
    return send_file(f"{PROJECT_PATH}build/index.html")


@app.route("/<path:filename>")
def serve_static_content(filename):
    return send_from_directory(f"{PROJECT_PATH}build/", filename)


if __name__ == "__main__":
    watcher_thread = threading.Thread(target=run_watcher)
    watcher_thread.start()
    # app.run(debug=True)
    watcher_thread.join()
