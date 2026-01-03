# app.py
import os
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from config import UPLOAD_DIR, OUTPUT_DIR, ALLOWED_VIDEO, ALLOWED_AUDIO, ALLOWED_SUBS
from tasks.queue import create_task, get_task
from merge_worker import run_merge
import threading
import sys
print(sys.path)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024 * 1024

def allowed(filename, allowed_set):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in allowed_set)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard/<task_id>')
def dashboard(task_id):
    return render_template('dashboard.html', task_id=task_id)

@app.route('/upload', methods=['POST'])
def upload():
    videos = request.files.getlist('videos')
    audios = request.files.getlist('audios')
    subs = request.files.getlist('subs')
    reencode = request.form.get('reencode') == 'on'
    out_name = secure_filename(request.form.get('out_name') or 'merged_output.mp4')

    if not videos or len(videos) < 1:
        return jsonify({'error': 'Please upload at least one video.'}), 400

    os.makedirs(os.path.join(UPLOAD_DIR, "videos"), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_DIR, "audio"), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_DIR, "subs"), exist_ok=True)

    video_paths, audio_paths, sub_paths = [], [], []

    for v in videos:
        if not allowed(v.filename, ALLOWED_VIDEO):
            return jsonify({'error': f'Invalid video type: {v.filename}'}), 400
        path = os.path.join(UPLOAD_DIR, "videos", secure_filename(v.filename))
        v.save(path)
        video_paths.append(path)

    for a in audios or []:
        if a and a.filename and allowed(a.filename, ALLOWED_AUDIO):
            path = os.path.join(UPLOAD_DIR, "audio", secure_filename(a.filename))
            a.save(path)
            audio_paths.append(path)

    for s in subs or []:
        if s and s.filename and allowed(s.filename, ALLOWED_SUBS):
            path = os.path.join(UPLOAD_DIR, "subs", secure_filename(s.filename))
            s.save(path)
            sub_paths.append(path)

    task_id = create_task()
    t = threading.Thread(target=run_merge, args=(task_id, video_paths, audio_paths, sub_paths, reencode, out_name))
    t.daemon = True
    t.start()

    return jsonify({'task_id': task_id, 'redirect': url_for('dashboard', task_id=task_id)}), 200

@app.route('/progress/<task_id>')
def progress(task_id):
    task = get_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

@app.route('/download/<task_id>')
def download(task_id):
    task = get_task(task_id)
    if not task or task.get('status') != 'done':
        return jsonify({'error': 'Not ready'}), 400
    path = task.get('result')
    return send_file(path, as_attachment=True, download_name=os.path.basename(path))

if __name__ == '__main__':
    app.run(debug=True)
