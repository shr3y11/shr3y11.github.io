const menuButton = document.querySelector('.menu-button');
const navigation = document.querySelector('.site-nav');

menuButton?.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  navigation?.classList.toggle('is-open', !isOpen);
});

navigation?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    menuButton?.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
  });
});

document.querySelector('#year').textContent = new Date().getFullYear();

const resumeDialog = document.querySelector('#resume-dialog');
const certificateDialog = document.querySelector('#certificate-dialog');
let dialogOpener = null;
let resumeLoad = null;

async function renderResume(url) {
  const status = document.querySelector('#resume-status');
  status.textContent = 'Loading résumé PDF.';
  try {
    const pdfjs = await import('./assets/vendor/pdfjs/pdf.mjs');
    pdfjs.GlobalWorkerOptions.workerSrc = new URL('./assets/vendor/pdfjs/pdf.worker.mjs', document.baseURI).href;
    const pdf = await pdfjs.getDocument({
      url,
      standardFontDataUrl: new URL('./assets/vendor/pdfjs/standard_fonts/', document.baseURI).href,
      isEvalSupported: false,
    }).promise;
    const pages = document.querySelector('#resume-pages');
    const rendered = document.createDocumentFragment();
    for (let number = 1; number <= pdf.numPages; number += 1) {
      const page = await pdf.getPage(number);
      const viewport = page.getViewport({ scale: 2.5 });
      const canvas = document.createElement('canvas');
      canvas.width = Math.ceil(viewport.width);
      canvas.height = Math.ceil(viewport.height);
      canvas.setAttribute('role', 'img');
      canvas.setAttribute('aria-label', `Shreeyash Wale’s résumé, page ${number}. A selectable-text PDF is available from Open PDF.`);
      await page.render({ canvasContext: canvas.getContext('2d'), viewport }).promise;
      rendered.append(canvas);
    }
    pages.replaceChildren(rendered);
    pages.hidden = false;
    document.querySelector('#resume-image').hidden = true;
    status.textContent = `Résumé loaded. ${pdf.numPages} page${pdf.numPages === 1 ? '' : 's'}.`;
  } catch {
    // The exact pre-rendered PDF page remains visible if the browser cannot run PDF.js.
    status.textContent = 'Showing a résumé preview. The PDF is available from Open PDF or Download PDF.';
    resumeLoad = null;
  }
}

function openDialog(dialog, opener) {
  if (!dialog || typeof dialog.showModal !== 'function') return false;
  dialogOpener = opener;
  dialog.classList.remove('is-closing');
  dialog.showModal();
  document.body.classList.add('has-dialog');
  return true;
}

function closeDialog(dialog) {
  if (!dialog.open || dialog.classList.contains('is-closing')) return;
  const finish = () => {
    dialog.close();
    dialog.classList.remove('is-closing');
    document.body.classList.remove('has-dialog');
    dialogOpener?.focus({ preventScroll: true });
    if (dialog === certificateDialog) document.querySelector('#certificate-full').removeAttribute('src');
  };
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return finish();
  dialog.classList.add('is-closing');
  window.setTimeout(finish, 200);
}

document.querySelectorAll('[data-resume]').forEach((link) => {
  link.addEventListener('click', (event) => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (openDialog(resumeDialog, link)) {
      event.preventDefault();
      if (!resumeLoad) resumeLoad = renderResume(link.href);
    }
  });
});

document.querySelector('#resume-zoom')?.addEventListener('click', (event) => {
  const button = event.currentTarget;
  const zoomed = button.getAttribute('aria-pressed') !== 'true';
  button.setAttribute('aria-pressed', String(zoomed));
  button.textContent = zoomed ? 'Fit page' : 'Zoom in';
  document.querySelector('.resume-preview').classList.toggle('is-zoomed', zoomed);
});

document.querySelectorAll('[data-certificate]').forEach((link) => {
  link.addEventListener('click', (event) => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    document.querySelector('#certificate-dialog-title').textContent = link.dataset.certificate;
    const fullImage = document.querySelector('#certificate-full');
    fullImage.src = link.href;
    fullImage.alt = `${link.dataset.certificate} certificate awarded to Shreeyash Wale`;
    document.querySelector('#certificate-original').href = link.href;
    if (openDialog(certificateDialog, link)) event.preventDefault();
  });
});

document.querySelectorAll('.document-dialog').forEach((dialog) => {
  dialog.querySelector('[data-close-dialog]').addEventListener('click', () => closeDialog(dialog));
  dialog.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeDialog(dialog);
  });
  // A backdrop click closes the viewer; clicks inside its content do not.
  let pressedBackdrop = false;
  dialog.addEventListener('pointerdown', (event) => { pressedBackdrop = event.target === dialog; });
  dialog.addEventListener('click', (event) => {
    if (pressedBackdrop && event.target === dialog) closeDialog(dialog);
    pressedBackdrop = false;
  });
});
