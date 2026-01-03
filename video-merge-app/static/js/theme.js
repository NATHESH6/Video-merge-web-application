// static/js/theme.js
const toggle = document.getElementById('themeToggle');
function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}
toggle?.addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-theme') || 'dark';
  setTheme(cur === 'dark' ? 'light' : 'dark');
});
const saved = localStorage.getItem('theme');
if (saved) setTheme(saved);
