# MergeLab — Fast animated video merging (Flask)

## 🎬 Video Merge Web Application
📌 Project Purpose
This project is a video merge web application designed to simplify the process of combining multiple video files into one. It allows users to upload videos, add extra audio tracks and subtitles, monitor the merging process in real time, and download the final output directly to their PC.


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
```
video-merge-app/
├── app.py
├── requirements.txt
├── config.py
├── merge_worker.py
├── tasks/
│   └── queue.py
├── static/
│   ├── css/
│   │   ├── main.css
│   │   └── themes.css
│   ├── js/
│   │   ├── ui.js
│   │   ├── dashboard.js
│   │   └── theme.js
│   └── assets/
│       └── icons/
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   └── download.html
├── uploads/
│   ├── videos/
│   ├── audio/
│   └── subs/
├── outputs/
│   └── merged/
├── README.md
└── LICENSE
```

## 🛠️ How to Use
1 Run the application locally
```
python app.py
```
Then open http://localhost:5000 in your browser.
2 Upload files
   - Select one or more video files.
   - Optionally upload audio tracks and subtitle files.
   - Enter a custom output filename if desired.
   - Use the “Force re-encode” option if the input videos have mismatched codecs.
3 Monitor progress
    - A dashboard displays the merge status with a progress bar and stage indicators (Queued → Merging → Completed).
    - Updates are shown live until the process finishes.

4 Download result
    - Once merging is complete, click the Download Video button to save the merged file to your PC.
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
MIT License — see `LICENSE`. © Nathesh<br>
Copyright (c) 2026 Nathesh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
`
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.`


