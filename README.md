# MergeLab — Fast animated video merging (Flask)

A full-stack video merging web app built by **Nathesh**, final year CSE and freelance web-developer. Frontend is UI/UX-heavy with dark/light mode and animated interactions; backend uses Flask + FFmpeg for fast merges, multi-audio, and subtitle support. Live progress appears on a dashboard, and the final result is downloadable to your PC.

## Features
- Dark/light theme with animated transitions
- Hover-animated buttons and smooth page entrance effects
- Fast video concatenation with stream copy; fallback re-encode for mismatched codecs
- Attach multiple audio tracks and optional subtitles (SRT/ASS/VTT)
- Live dashboard with progress and stages
- Download final merged file

## Tech stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- Media engine: FFmpeg

## Project structure
See `/video-merge-app` tree in this repo.

## Setup
1. Install Python 3.10+ and FFmpeg (ensure `ffmpeg`/`ffprobe` on PATH).
2. `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
3. `pip install -r requirements.txt`
4. `python app.py` (development)

## Usage
- Open `http://localhost:5000`
- Upload videos (same codec for fastest merging), optional audios/subtitles
- Toggle "Force re-encode" if inputs differ
- Watch progress on the dashboard; download when complete

## Notes
- Fastest results when all input videos share the same codec/parameters (e.g., H.264 + AAC, same resolution).
- Subtitles stored in MP4 as `mov_text`; for MKV, adjust commands to `-c:s copy`.
- For production, use Gunicorn + Nginx and a worker queue (Celery/RQ).

## License
MIT License — see `LICENSE`. © Nathesh

