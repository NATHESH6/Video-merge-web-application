# config.py
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "merged")
MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024  # 2 GB
ALLOWED_VIDEO = {"mp4", "mov", "mkv", "webm"}
ALLOWED_AUDIO = {"aac", "mp3", "wav", "m4a", "flac"}
ALLOWED_SUBS = {"srt", "ass", "vtt"}
POLL_INTERVAL_MS = 800
