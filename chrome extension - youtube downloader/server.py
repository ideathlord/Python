#!/usr/bin/env python3
"""
Local Download Server
----------------------
A small local HTTP server that the Chrome extension talks to. It reuses the
same yt-dlp download logic as yt_downloader.py, but exposes it over
http://127.0.0.1:5005 so the browser extension (which can't run Python or
ffmpeg itself) can trigger downloads.

This is meant to run on YOUR machine only, for YOUR own personal use.
It is not meant to be exposed to the internet or other devices.

IMPORTANT: Only download content you own, that is public domain, licensed
under Creative Commons, or that you otherwise have permission to download.

Setup:
    pip install yt-dlp flask

Run:
    python server.py

Leave this running in a terminal while you use the Chrome extension.
"""

import os
import threading
import uuid
from pathlib import Path

from flask import Flask, jsonify, request

try:
    import yt_dlp
except ImportError:
    print("Missing dependency. Install it with:\n    pip install yt-dlp")
    raise SystemExit(1)

app = Flask(__name__)

# Where downloads get saved. Change this if you'd like a different folder.
DOWNLOAD_DIR = str(Path.home() / "Downloads" / "yt-downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

PLAYER_CLIENTS = ["tv", "web", "default", "android_vr"]

# In-memory job tracking so the popup can poll for progress.
# job_id -> {"status": "downloading"|"done"|"error", "percent": str, "title": str, "error": str}
jobs = {}


def _cors(resp):
    """Allow the extension's origin to call this local server."""
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.after_request
def add_cors_headers(resp):
    return _cors(resp)


@app.route("/download", methods=["OPTIONS"])
@app.route("/status/<job_id>", methods=["OPTIONS"])
def preflight(job_id=None):
    return _cors(app.make_default_options_response())


def build_options(job_id, audio_only, quality, player_client):
    outtmpl = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    def progress_hook(d):
        if d["status"] == "downloading":
            jobs[job_id]["percent"] = d.get("_percent_str", "").strip()
        elif d["status"] == "finished":
            jobs[job_id]["percent"] = "100%"

    if audio_only:
        format_spec = "bestaudio/best"
        postprocessors = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ]
        merge_output_format = None
    else:
        max_height = quality or 1080
        format_spec = (
            f"bestvideo[vcodec^=avc1][height<={max_height}]+bestaudio[acodec^=mp4a]"
            f"/best[vcodec^=avc1][ext=mp4][height<={max_height}]"
            f"/bestvideo[ext=mp4][height<={max_height}]+bestaudio[ext=m4a]"
            f"/best[ext=mp4][height<={max_height}]"
        )
        postprocessors = [{"key": "FFmpegVideoRemuxer", "preferedformat": "mp4"}]
        merge_output_format = "mp4"

    opts = {
        "format": format_spec,
        "outtmpl": outtmpl,
        "postprocessors": postprocessors,
        "progress_hooks": [progress_hook],
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {"youtube": {"player_client": [player_client]}},
    }
    if merge_output_format:
        opts["merge_output_format"] = merge_output_format
    return opts


def run_download(job_id, url, audio_only, quality):
    last_error = None
    for client in PLAYER_CLIENTS:
        opts = build_options(job_id, audio_only, quality, client)
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                jobs[job_id]["title"] = info.get("title", "Unknown title")
                ydl.download([url])
                jobs[job_id]["status"] = "done"
                return
        except yt_dlp.utils.DownloadError as e:
            last_error = str(e)
            continue

    jobs[job_id]["status"] = "error"
    jobs[job_id]["error"] = last_error or "Unknown error"


@app.route("/download", methods=["POST"])
def start_download():
    data = request.get_json(force=True)
    url = (data.get("url") or "").strip()
    audio_only = bool(data.get("audio_only", False))
    quality = data.get("quality")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "downloading", "percent": "0%", "title": "", "error": ""}

    thread = threading.Thread(
        target=run_download, args=(job_id, url, audio_only, quality), daemon=True
    )
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/status/<job_id>", methods=["GET"])
def get_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Unknown job"}), 404
    return jsonify(job)


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"ok": True})


if __name__ == "__main__":
    print(f"Downloads will be saved to: {DOWNLOAD_DIR}")
    print("Server running at http://127.0.0.1:5005")
    print("Leave this window open while using the extension. Press Ctrl+C to stop.")
    app.run(host="127.0.0.1", port=5005)
