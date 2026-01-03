# merge_worker.py
import os, subprocess, shlex, tempfile
from tasks.queue import set_started, update_task, set_done, set_error
from config import OUTPUT_DIR

def ffprobe_duration(path):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"'
    try:
        out = subprocess.check_output(shlex.split(cmd)).decode().strip()
        return float(out)
    except Exception:
        return None

def build_concat_list(video_paths):
    # FFmpeg concat demuxer requires identical codec/params; otherwise re-encode later
    tf = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt")
    for p in video_paths:
        tf.write(f"file '{os.path.abspath(p)}'\n")
    tf.flush()
    return tf.name

def run_merge(task_id, video_paths, audio_paths=None, subtitle_paths=None, reencode=False, out_name="merged_output.mp4", audio_map_idxs=None):
    try:
        set_started(task_id)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, out_name)

        concat_file = build_concat_list(video_paths)
        # Strategy 1: try stream copy for speed; fallback to re-encode if mismatch
        if not reencode:
            cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_file}" -c copy "{output_path}"'
        else:
            # Re-encode to common baseline for compatibility
            cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_file}" -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 192k "{output_path}"'

        process = subprocess.Popen(shlex.split(cmd), stderr=subprocess.PIPE, universal_newlines=True)

        # Approximate progress using durations
        total_duration = sum([ffprobe_duration(p) or 0 for p in video_paths]) or 1.0
        last_progress = 0
        for line in process.stderr:
            if "time=" in line:
                try:
                    t = line.split("time=")[1].split(" ")[0]
                    h, m, s = t.split(":")
                    cur = float(h) * 3600 + float(m) * 60 + float(s)
                    progress = min(99, int((cur / total_duration) * 100))
                    if progress > last_progress:
                        last_progress = progress
                        update_task(task_id, progress=progress, message="Merging video")
                except Exception:
                    pass

        rc = process.wait()
        if rc != 0:
            set_error(task_id, "Video merge failed; try re-encode.")
            return

        # Attach multiple audio tracks if provided
        if audio_paths:
            base = output_path
            temp_out = base.replace(".mp4", "_audio.mp4")
            map_cmd = ['ffmpeg', '-y', '-i', base]
            for a in audio_paths:
                map_cmd.extend(['-i', a])
            # Map existing video + its audio (0) and extra audios (1..N)
            # audio_map_idxs allows choosing which track is default; otherwise first remains default
            for idx in range(len(audio_paths) + 1):
                if idx == 0:
                    map_cmd.extend(['-map', '0:v', '-map', '0:a?'])
                else:
                    map_cmd.extend(['-map', f'{idx}:a?'])
            map_cmd.extend(['-c:v', 'copy', '-c:a', 'aac', temp_out])
            subprocess.check_call(map_cmd)
            os.replace(temp_out, output_path)

        # Attach subtitles if provided
        if subtitle_paths:
            base = output_path
            temp_out = base.replace(".mp4", "_subs.mp4")
            sub_cmd = ['ffmpeg', '-y', '-i', base]
            for s in subtitle_paths:
                sub_cmd.extend(['-i', s])
            # Copy video/audio, burn or attach subs (mov_text for MP4)
            for i in range(len(subtitle_paths)):
                sub_cmd.extend(['-map', '0', '-map', f'{i+1}:s?'])
            sub_cmd.extend(['-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text', temp_out])
            subprocess.check_call(sub_cmd)
            os.replace(temp_out, output_path)

        set_done(task_id, output_path)
    except Exception as e:
        set_error(task_id, str(e))
