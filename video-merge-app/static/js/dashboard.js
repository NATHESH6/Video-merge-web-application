// static/js/dashboard.js
const progressInner = document.getElementById('progressInner');
const progressText = document.getElementById('progressText');
const dl = document.getElementById('downloadLink');

function updateStages(status) {
  document.getElementById('stage-queue').classList.toggle('active', status === 'queued');
  document.getElementById('stage-run').classList.toggle('active', status === 'running');
  document.getElementById('stage-done').classList.toggle('active', status === 'done');
}

async function poll() {
  const res = await fetch(`/progress/${taskId}`);
  if (!res.ok) return;
  const data = await res.json();

  progressInner.style.width = `${data.progress || 0}%`;
  progressText.textContent = data.message || '...';
  updateStages(data.status);

  if (data.status === 'done') {
    dl.classList.remove('hidden');
    dl.href = `/download/${taskId}`;
    return; // stop polling
  }
  if (data.status === 'error') {
    progressText.textContent = data.error || 'Something went wrong.';
    return;
  }
  setTimeout(poll, 800);
}
poll();
