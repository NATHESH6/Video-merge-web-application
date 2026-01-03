# tasks/queue.py
import uuid, time
from threading import Lock

_tasks = {}
_lock = Lock()

def create_task():
    tid = str(uuid.uuid4())
    with _lock:
        _tasks[tid] = {"status": "queued", "progress": 0, "message": "Waiting", "result": None, "error": None, "started_at": None}
    return tid

def update_task(tid, **kwargs):
    with _lock:
        if tid in _tasks:
            _tasks[tid].update(kwargs)

def get_task(tid):
    with _lock:
        return _tasks.get(tid)

def set_started(tid):
    update_task(tid, status="running", started_at=time.time(), message="Starting merge")

def set_done(tid, result_path):
    update_task(tid, status="done", progress=100, result=result_path, message="Completed")

def set_error(tid, msg):
    update_task(tid, status="error", error=msg, message="Failed")
