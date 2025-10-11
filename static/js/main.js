const form = document.getElementById('upload-form');
const videosInput = document.getElementById('videos');
const statusBlock = document.getElementById('status');
const resultBlock = document.getElementById('result');
const resultCount = document.getElementById('result-count');
const downloadLink = document.getElementById('download-link');

function toggle(element, show) {
  element.toggleAttribute('hidden', !show);
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const files = videosInput.files;
  if (!files || !files.length) {
    alert('Select at least one video to get started.');
    return;
  }

  const formData = new FormData();
  Array.from(files).forEach((file) => formData.append('videos', file));
  const mode = form.querySelector('input[name="mode"]:checked')?.value ?? 'blur';
  formData.append('mode', mode);

  toggle(form, false);
  toggle(statusBlock, true);
  toggle(resultBlock, false);

  try {
    const response = await fetch('/process', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const { error } = await response.json().catch(() => ({ error: 'Upload failed.' }));
      throw new Error(error || 'Upload failed.');
    }

    const payload = await response.json();
    resultCount.textContent = `Generated ${payload.fileCount} files.`;
    downloadLink.href = payload.downloadUrl;

    toggle(resultBlock, true);
  } catch (error) {
    alert(error.message || 'Something went wrong.');
  } finally {
    toggle(statusBlock, false);
    toggle(form, true);
  }
});

const dropzone = document.querySelector('.uploader');

['dragenter', 'dragover'].forEach((eventName) => {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.add('is-dragging');
  });
});

['dragleave', 'drop'].forEach((eventName) => {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.remove('is-dragging');
  });
});

dropzone.addEventListener('drop', (event) => {
  const items = event.dataTransfer.files;
  if (!items?.length) return;
  const transfer = new DataTransfer();
  Array.from(items).forEach((file) => transfer.items.add(file));
  videosInput.files = transfer.files;
});
