// static/js/ui.js
const form = document.getElementById('uploadForm');
const statusEl = document.getElementById('status');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  const videos = form.querySelector('input[name="videos"]').files;
  if (!videos.length) {
    statusEl.textContent = 'Please select at least one video.';
    statusEl.classList.remove('hidden');
    return;
  }
  statusEl.textContent = 'Uploading...';
  statusEl.classList.remove('hidden');

  const res = await fetch('/upload', { method: 'POST', body: fd });
  const data = await res.json();
  if (res.ok) {
    window.location.href = data.redirect;
  } else {
    statusEl.textContent = data.error || 'Upload failed.';
  }
});
