from flask import Flask, send_file, send_from_directory
import os

app = Flask(__name__)


@app.route("/")
def serve_index():
    return send_file("../../example/build/index.html")


@app.route("/<path:filename>")
def serve_static_content(filename):
    return send_from_directory("../../example/build/", filename)
