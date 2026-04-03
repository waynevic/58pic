const navButtons = document.querySelectorAll('.chapter-nav button');
const chapters = document.querySelectorAll('.chapter');

navButtons.forEach((btn) => {
  btn.addEventListener('click', () => {
    navButtons.forEach((b) => b.classList.remove('active'));
    chapters.forEach((c) => c.classList.remove('active'));

    btn.classList.add('active');
    const target = document.getElementById(btn.dataset.target);
    if (target) {
      target.classList.add('active');
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

const copyBtn = document.getElementById('copyBtn');
const promptTemplate = document.getElementById('promptTemplate');

if (copyBtn && promptTemplate) {
  copyBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(promptTemplate.innerText);
      copyBtn.textContent = '已复制 ✅';
      setTimeout(() => {
        copyBtn.textContent = '复制模板';
      }, 1500);
    } catch {
      copyBtn.textContent = '复制失败，请手动复制';
    }
  });
}
