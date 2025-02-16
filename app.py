from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask import Flask, render_template
from flask import send_from_directory
import yt_dlp
import os
import subprocess


app = Flask(__name__)
CORS(app)
DOWNLOADS_DIR = "static/downloads"
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")  # Ensure 'index.html' exists in 'templates' folder

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")


# Updated quality options (VP9 for 4K & 1440p, AVC for others)
QUALITY_OPTIONS = {
    "4k": "bv*[height=2160]+ba/b[height=2160]",
    "1440p": "bv*[height=1440]+ba/b[height=1440]",
    "1080p": "bv*[height=1080][vcodec^=avc1]+ba[acodec^=mp4a]/b[height=1080]",
    "720p": "bv*[height=720][vcodec^=avc1]+ba[acodec^=mp4a]/b[height=720]",
    "480p": "bv*[height=480][vcodec^=avc1]+ba[acodec^=mp4a]/b[height=480]",
    "360p": "bv*[height=360][vcodec^=avc1]+ba[acodec^=mp4a]/b[height=360]",
}

def convert_to_h264(input_file, output_file):
    """Converts VP9 videos to H.264 to prevent playback issues."""
    try:
        command = [
            "ffmpeg", "-y", "-i", input_file, "-c:v", "libx264", "-preset", "slow",
            "-crf", "23", "-c:a", "aac", "-b:a", "192k", output_file
        ]
        subprocess.run(command, check=True)
        os.remove(input_file)  # Remove original VP9 file
        return output_file
    except Exception as e:
        print("FFmpeg Error:", e)
        return None

@app.route("/download", methods=["POST"])
def download_video():
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
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict).replace(".webm", ".mp4").replace(".mkv", ".mp4")
        
        # Convert only if it's 4K or 1440p (VP9 format)
        if quality in ["4k", "1440p"]:
            output_file = filename.replace(".mp4", "_converted.mp4")
            converted_file = convert_to_h264(filename, output_file)
            if converted_file:
                filename = converted_file

        return jsonify({"success": True, "download_link": f"http://127.0.0.1:10000/downloaded/{os.path.basename(filename)}" })


    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/downloaded/<filename>")
def serve_file(filename):
    """Serve the downloaded video so the phone can download it directly."""
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)  # ✅ Forces download on mobile
    return jsonify({"success": False, "error": "File not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Get port from Render
    app.run(debug=True, host="0.0.0.0", port=5000)
