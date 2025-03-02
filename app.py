from flask import Flask, request, jsonify, send_file, render_template, Response, send_from_directory
from flask_cors import CORS
import yt_dlp
import os
import subprocess
import socket
import time
import re
import time


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
tor_process = None  # Store the Tor process

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Global variable to track progress
download_progress = {"percent": 0}


def download_progress_hook(d):
    """Hook to update download progress, stripping ANSI codes."""
    if d['status'] == 'downloading':
        raw_percent = d.get('_percent_str', '0').strip()
        # Remove ANSI escape sequences
        clean_percent = re.sub(r'\x1b\[[0-9;]*m', '', raw_percent)
        try:
            percent = float(clean_percent.replace('%', '').strip())
            download_progress['percent'] = percent
            print(f"Downloading: {percent}%")
        except ValueError:
            print(f"Failed to parse progress: {raw_percent}")




@app.route("/")
def index():
    return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")


QUALITY_OPTIONS = {
    "4k": "bv*[height=2160]+ba/b[height=2160]",
    "1440p": "bv*[height=1440]+ba/b[height=1440]",
    "1080p": "bv*[height=1080][vcodec^=avc1]+ba[acodec^=mp4a]/b[height=1080]",
    "720p": "bv*[height=720][vcodec^=avc1]+ba[acodec^=mp4a]/b[height=720]",
    "480p": "bv*[height=480][vcodec^=avc1]+ba[acodec^=mp4a]/b[height=480]",
    "360p": "bv*[height=360][vcodec^=avc1]+ba[acodec^=mp4a]/b[height=360]",
}


def get_local_ip():
    """Get local network IP."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


@app.route("/download", methods=["POST"])
def download_video():
    global download_progress
    download_progress = {"percent": 0}  # Reset progress at the start

    data = request.get_json()
    url = data.get("url")
    quality = data.get("quality", "1080p")

    if not url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    if quality not in QUALITY_OPTIONS:
        return jsonify({"success": False, "error": "Invalid quality option"}), 400

    try:
        ydl_opts = {
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "format": QUALITY_OPTIONS[quality],
            "merge_output_format": "mp4",
            "progress_hooks": [download_progress_hook],
            "proxy": "socks5h://127.0.0.1:9050"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict).replace(".webm", ".mp4").replace(".mkv", ".mp4")

        local_ip = get_local_ip()
        download_link = f"http://{local_ip}:10000/downloaded/{os.path.basename(filename)}"

        return jsonify({"success": True, "download_link": download_link})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@app.route("/progress")
def progress_stream():
    def generate():
        last_percent = -1
        while download_progress['percent'] < 100:
            current_percent = int(download_progress['percent'])
            if current_percent != last_percent:
                yield f"data: {current_percent}\n\n"  # Double newlines for SSE
                last_percent = current_percent
            time.sleep(0.5)  # Keep this for smooth updates
        yield "data: 100\n\n"  # Complete the progress

    return Response(generate(), mimetype='text/event-stream')





@app.route("/downloaded/<filename>")
def serve_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"success": False, "error": "File not found"}), 404


@app.route("/start-tor")
def start_tor():
    global tor_process
    if tor_process is None:
        tor_process = subprocess.Popen(["tor"])
        return jsonify({"message": "Tor is Enabled!"})
    return jsonify({"message": "Tor is Already Running"})


@app.route("/stop-tor")
def stop_tor():
    global tor_process
    if tor_process:
        tor_process.terminate()
        tor_process = None
        return jsonify({"message": "Tor is Disabled!"})
    return jsonify({"message": "Tor is Already Stopped"})


@app.route("/tor-status")
def tor_status():
    global tor_process
    if tor_process:
        return jsonify({"status": "ON"})
    return jsonify({"status": "OFF"})

@app.route("/check-tor-ip")
def check_tor_ip():
    try:
        proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050"
        }
        response = requests.get("https://api64.ipify.org?format=json", proxies=proxies)
        return jsonify({"tor_ip": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
