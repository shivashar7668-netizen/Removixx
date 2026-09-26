"""
Removix UI - Word to PDF View
-----------------------------
Converts Microsoft Word documents (.docx, .doc) to high-quality PDF.
Uses high-precision document formatting with native vector typography engine.
"""

from ui.layout import render_layout, render_processing_component

WORD_TO_PDF_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><rect x="3" y="2" width="18" height="20" rx="2" stroke-width="2"/><line x1="8" y1="8" x2="16" y2="8"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="8" y1="16" x2="12" y2="16"/></svg>"""


def render_word_to_pdf_page() -> str:
    """Renders the Word to PDF converter tool view."""
    processing_card = render_processing_component(
        component_id="w2p-proc",
        badge_text="DOCUMENT CONVERTER",
        badge_icon_svg=WORD_TO_PDF_BADGE_SVG,
        title_text="Converting Word Document...",
        subtitle_text="Rendering typography, tables, and layouts into standard PDF format.",
        steps=[
            "Reading document",
            "Converting to PDF",
            "Finalizing file",
        ],
    )

    main_card_html = f"""
    <!-- Dropzone View -->
    <div id="dropzone-w2p" class="dropzone-box" onclick="document.getElementById('file-input-w2p').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose Word Document</span>
      </div>
      <p class="drop-primary">Drop Word document here, or browse</p>
      <p class="drop-secondary">Supports DOCX and DOC • Converts with precise formatting and styling</p>
    </div>
    <input type="file" id="file-input-w2p" accept=".docx,.doc,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword" onchange="handleWordUpload(this.files[0])">

    <!-- Selected Word Document Config Card -->
    <div id="w2p-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card, #f8fafc); border:1px solid var(--line, #e2e8f0); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:12px; overflow:hidden;">
          <div style="width:42px; height:42px; border-radius:10px; background:rgba(37,99,235,0.1); color:#2563eb; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect x="3" y="2" width="18" height="20" rx="2" stroke="#2563eb" stroke-width="2"/><text x="12" y="15" text-anchor="middle" font-size="9" font-weight="800" fill="#2563eb" font-family="Arial,sans-serif">W</text></svg>
          </div>
          <div style="overflow:hidden;">
            <p id="w2p-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap; max-width:380px;">Document.docx</p>
            <p id="w2p-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Word Document</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetWordView()">Change File</button>
      </div>

      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-w2p" onclick="executeWordToPdf()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
          Convert Word to PDF
        </button>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card with Converted PDF First Page Preview -->
    <div id="w2p-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:var(--bg-card); border:1px solid rgba(22,163,74,0.3); border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:rgba(22,163,74,0.12); color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:var(--ink); margin-bottom:6px;">Conversion Complete!</h3>
      <p id="w2p-result-sub" style="font-size:13.5px; color:var(--ink-muted); margin-bottom:20px;">Your Word document has been compiled into a high-quality PDF.</p>

      <!-- Live First Page Preview of Converted PDF -->
      <div id="w2p-preview-box" style="margin: 0 auto 24px; max-width: 340px; border-radius: 12px; overflow: hidden; border: 1px solid var(--line); box-shadow: 0 6px 20px rgba(0,0,0,0.08); background: var(--bg-card);">
        <div style="font-size: 11px; font-weight: 700; color: var(--ink-muted); text-transform: uppercase; letter-spacing: 0.5px; padding: 8px 12px; background: rgba(0,0,0,0.03); border-bottom: 1px solid var(--line); display: flex; justify-content: space-between; align-items: center;">
          <span>First Page Preview</span>
          <span id="w2p-pages-pill" style="font-size: 11px; font-weight: 700; background: rgba(37,99,235,0.1); color: #2563eb; padding: 2px 8px; border-radius: 20px;">PDF Ready</span>
        </div>
        <div style="background: #3a3f47; padding: 12px; display: flex; align-items: center; justify-content: center; min-height: 220px;">
          <canvas id="w2p-preview-canvas" style="max-width: 100%; height: auto; border-radius: 3px; box-shadow: 0 4px 12px rgba(0,0,0,0.35); display: block;"></canvas>
        </div>
      </div>

      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-w2p" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-w2p" />
            <span class="circle">
              <svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"></path>
              </svg>
              <div class="square"></div>
            </span>
            <p class="title">Download PDF</p>
            <p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetWordView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Convert Another File
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18"/><path d="M14 9h4"/><path d="M14 15h4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Accurate Formatting</h3>
          <p>Preserves typography, line heights, bold/italic text, tables, bullet points, and headers flawlessly.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Universal Compatibility</h3>
          <p>Produces standard PDF documents compatible with Adobe Acrobat, modern browsers, and mobile viewers.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Secure & Offline</h3>
          <p>Your confidential proposals, essays, and legal agreements are converted locally with 100% data privacy.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let currentWordFile = null;

    const dropzoneW2p = document.getElementById('dropzone-w2p');
    if (dropzoneW2p) {
      ['dragenter', 'dragover'].forEach(evt => {
        dropzoneW2p.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneW2p.classList.add('dragover');
        });
      });
      ['dragleave', 'drop'].forEach(evt => {
        dropzoneW2p.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneW2p.classList.remove('dragover');
        });
      });
      dropzoneW2p.addEventListener('drop', e => {
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          handleWordUpload(e.dataTransfer.files[0]);
        }
      });
    }

    function handleWordUpload(file) {
      if (!file) return;
      const lower = file.name.toLowerCase();
      if (!lower.endsWith('.docx') && !lower.endsWith('.doc')) {
        alert('Please choose a valid Word document (.docx or .doc).');
        return;
      }
      currentWordFile = file;
      document.getElementById('dropzone-w2p').style.display = 'none';
      document.getElementById('w2p-doc-name').textContent = file.name;
      document.getElementById('w2p-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Word Document';
      document.getElementById('w2p-file-config').style.display = 'block';
    }

    let currentW2pBlobUrl = '';
    let isW2pDownloadComplete = false;

    function triggerW2pDownload() {
      if (!currentW2pBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentW2pBlobUrl;
      a.download = 'removix_converted.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxW2p = document.getElementById('dl-checkbox-w2p');
    const dlLabelW2p = document.getElementById('dl-label-w2p');
    if (dlCheckboxW2p) {
      dlCheckboxW2p.addEventListener('change', () => {
        if (dlCheckboxW2p.checked) {
          if (dlLabelW2p) dlLabelW2p.classList.add('is-checked');
          triggerW2pDownload();
          setTimeout(() => {
            isW2pDownloadComplete = true;
          }, 2350);
        }
      });
      dlCheckboxW2p.addEventListener('click', (e) => {
        if (isW2pDownloadComplete) {
          e.preventDefault();
          triggerW2pDownload();
        }
      });
    }

    function resetWordView() {
      currentWordFile = null;
      document.getElementById('w2p-result-card').style.display = 'none';
      document.getElementById('w2p-proc').style.display = 'none';
      document.getElementById('w2p-file-config').style.display = 'none';
      document.getElementById('dropzone-w2p').style.display = '';
      const inputEl = document.getElementById('file-input-w2p');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxW2p) dlCheckboxW2p.checked = false;
      if (dlLabelW2p) dlLabelW2p.classList.remove('is-checked');
      isW2pDownloadComplete = false;
      if (currentW2pBlobUrl) {
        URL.revokeObjectURL(currentW2pBlobUrl);
        currentW2pBlobUrl = '';
      }
      const pCanvas = document.getElementById('w2p-preview-canvas');
      if (pCanvas) {
        const ctx = pCanvas.getContext('2d');
        if (ctx) ctx.clearRect(0, 0, pCanvas.width, pCanvas.height);
      }
    }

    function setW2pProgress(stepIdx, pct, title) {
      const compId = 'w2p-proc';
      const bar = document.getElementById(`${compId}-bar`);
      const pctEl = document.getElementById(`${compId}-pct`);
      const stageTitle = document.getElementById(`${compId}-stage-title`);

      if (bar) bar.style.width = pct + '%';
      if (pctEl) pctEl.textContent = Math.round(pct) + '%';
      if (stageTitle && title) stageTitle.textContent = title + '...';

      for (let i = 1; i <= 3; i++) {
        const stepRow = document.getElementById(`${compId}-step-${i}`);
        if (!stepRow) continue;
        stepRow.classList.remove('active', 'done');
        if (i < stepIdx) {
          stepRow.classList.add('done');
        } else if (i === stepIdx) {
          stepRow.classList.add('active');
        }
      }
    }

    function executeWordToPdf() {
      if (!currentWordFile) return;

      const formData = new FormData();
      formData.append('file', currentWordFile);

      document.getElementById('w2p-file-config').style.display = 'none';
      const procEl = document.getElementById('w2p-proc');
      procEl.style.display = 'block';

      // Step 1: Reading document
      setW2pProgress(1, 25, 'Reading document');

      const t1 = setTimeout(() => {
        // Step 2: Converting to PDF
        setW2pProgress(2, 65, 'Converting to PDF');
      }, 500);

      fetch('/api/word-to-pdf', {
        method: 'POST',
        body: formData
      })
      .then(res => {
        clearTimeout(t1);
        // Step 3: Finalizing file
        setW2pProgress(3, 95, 'Finalizing file');
        if (!res.ok) {
          return res.json().then(e => { throw new Error(e.error || 'Conversion failed'); });
        }
        return res.blob();
      })
      .then(async blob => {
        setW2pProgress(3, 100, 'Finalizing file');

        // Render first page preview with PDF.js
        try {
          if (window.pdfjsLib) {
            const buf = await blob.arrayBuffer();
            const pdfDoc = await pdfjsLib.getDocument({ data: buf }).promise;
            const pill = document.getElementById('w2p-pages-pill');
            if (pill) pill.textContent = `${pdfDoc.numPages} Page${pdfDoc.numPages > 1 ? 's' : ''}`;
            const page = await pdfDoc.getPage(1);
            const canvas = document.getElementById('w2p-preview-canvas');
            if (canvas) {
              const viewport = page.getViewport({ scale: 1.0 });
              const scale = Math.min(300 / viewport.width, 1.5);
              const scaledViewport = page.getViewport({ scale: scale });
              canvas.width = scaledViewport.width;
              canvas.height = scaledViewport.height;
              const ctx = canvas.getContext('2d');
              await page.render({ canvasContext: ctx, viewport: scaledViewport }).promise;
            }
          }
        } catch (e) {
          console.warn('PDF preview error:', e);
        }

        setTimeout(() => {
          procEl.style.display = 'none';
          document.getElementById('w2p-result-card').style.display = 'block';

          if (dlCheckboxW2p) dlCheckboxW2p.checked = false;
          if (dlLabelW2p) dlLabelW2p.classList.remove('is-checked');
          isW2pDownloadComplete = false;

          currentW2pBlobUrl = URL.createObjectURL(blob);
          const resultSub = document.getElementById('w2p-result-sub');
          resultSub.textContent = `Word document converted into PDF (${(blob.size / 1024).toFixed(0)} KB).`;
        }, 350);
      })
      .catch(err => {
        clearTimeout(t1);
        alert('Something went wrong, please try again.');
        resetWordView();
      });
    }
    """

    return render_layout(
        title="Word to PDF",
        active_tool="pdf-tools",
        hero_title="Word to PDF Converter",
        hero_sub="Convert Word documents (<strong>DOCX & DOC</strong>) into professional, print-ready PDF files.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
