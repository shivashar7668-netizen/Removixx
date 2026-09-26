"""
Removix UI - Image to Text (OCR) View
-------------------------------------
Extracts selectable text from documents, screenshots, receipts, photos, and PDFs.
Supports: English (eng), Hindi (hin), and Bilingual (eng+hin).

Dedicated processing UI:
- Badge: "TEXT EXTRACTOR"
- Steps: "Reading file" → "Enhancing image quality" → "Detecting text" → "Extracting text" → "Done"
"""

from ui.layout import render_layout, render_processing_component

OCR_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg>"""


def render_ocr_page() -> str:
    """Renders the Image to Text (OCR) interface."""
    processing_card = render_processing_component(
        component_id="ocr-proc",
        badge_text="TEXT EXTRACTOR",
        badge_icon_svg=OCR_BADGE_SVG,
        title_text="Extracting Text...",
        subtitle_text="Enhancing quality, correcting skew, and extracting bilingual text.",
        steps=[
            "Reading file",
            "Enhancing image quality",
            "Detecting text",
            "Extracting text",
            "Done",
        ],
    )

    main_card_html = f"""
    <!-- Language Selection Pills -->
    <div class="zone-pills-bar" id="ocr-lang-bar" style="margin-bottom:18px;">
      <span class="zone-label">Language:</span>
      <button type="button" class="zone-pill active" id="btn-lang-enghin" onclick="setOcrLang('eng+hin')">English + Hindi (Bilingual)</button>
      <button type="button" class="zone-pill" id="btn-lang-eng" onclick="setOcrLang('eng')">English Only</button>
      <button type="button" class="zone-pill" id="btn-lang-hin" onclick="setOcrLang('hin')">Hindi Only (हिंदी)</button>
    </div>

    <!-- Dropzone View -->
    <div id="dropzone-ocr" class="dropzone-box" onclick="document.getElementById('file-input-ocr').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose File</span>
      </div>
      <p class="drop-primary">Drop image or PDF here, or browse</p>
      <p class="drop-secondary">Supports PNG, JPG, JPEG, WEBP, PDF (Up to 20 pages) • Hindi & English</p>
    </div>
    <input type="file" id="file-input-ocr" accept=".png,.jpg,.jpeg,.webp,.bmp,.tiff,.pdf" onchange="handleOcrFile(this.files[0])">

    <!-- Selected File Confirmation Card -->
    <div id="ocr-config-card" style="display:none; margin-top:20px; padding:18px 22px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:16px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:12px; overflow:hidden;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg>
          </div>
          <div style="overflow:hidden;">
            <p id="ocr-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap; max-width:380px;">screenshot.png</p>
            <p id="ocr-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready for extraction</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetOcrView()">Change File</button>
      </div>

      <div style="margin-top:20px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-ocr" onclick="executeOcrExtraction()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg>
          <span id="btn-start-ocr-text">Extract Text</span>
        </button>
      </div>
    </div>

    <!-- Dedicated Processing View (Custom OCR UI) -->
    {processing_card}

    <!-- Result / Output Card -->
    <div id="ocr-result-wrap" style="display:none; margin-top:24px;">
      <!-- Truncation / Page Limit Notice Banner -->
      <div id="ocr-limit-notice" style="display:none; margin-bottom:14px; padding:12px 16px; background:#fffbeb; border:1px solid #fde68a; border-left:4px solid #f59e0b; border-radius:12px; color:#92400e; font-size:13.5px; font-weight:600; line-height:1.5;">
        Only 20 pages can be processed at a time. The first 20 pages have been extracted.
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <h3 style="font-size:15px; font-weight:700; color:var(--ink); display:flex; align-items:center; gap:8px;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
          Extracted Text Result
        </h3>
        <button type="button" class="btn-secondary" id="btn-copy-ocr" onclick="copyOcrText()" style="padding:7px 16px; font-size:13px; font-weight:600; display:inline-flex; align-items:center; gap:6px;">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          <span id="btn-copy-text">Copy to Clipboard</span>
        </button>
      </div>

      <textarea id="ocr-output-box" rows="12" style="width:100%; border:1.5px solid #cbd5e1; border-radius:14px; padding:16px; font-size:14.5px; line-height:1.6; font-family:'Inter', sans-serif; color:var(--ink); background:#ffffff; outline:none; resize:vertical; box-sizing:border-box; box-shadow:0 2px 10px rgba(15,23,42,0.03);"></textarea>

      <div class="result-actions" style="margin-top:22px;">
        <div class="container">
          <label class="label" id="dl-label-ocr" style="width: 195px;">
            <input type="checkbox" class="input" id="dl-checkbox-ocr" />
            <span class="circle">
              <svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"></path>
              </svg>
              <div class="square"></div>
            </span>
            <p class="title">Download Text</p>
            <p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetOcrView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Extract Another File
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Hindi & English Recognition</h3>
          <p>Optimized bilingual recognition engine for both English and Devanagari Hindi text.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Images & Multi-Page PDF</h3>
          <p>Extracts formatted text from photos, book scans, and multi-page PDFs up to 20 pages at 300 DPI.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Quality Enhancement & Deskew</h3>
          <p>Automatically enhances blurry text, removes sensor noise, and straightens tilted scans before extraction.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let selectedOcrLang = 'eng+hin';
    let currentOcrFile = null;
    let ocrTimer1 = null;
    let ocrTimer2 = null;
    let ocrTimer3 = null;

    // Drag and Drop listeners
    const dropzoneOcr = document.getElementById('dropzone-ocr');
    if (dropzoneOcr) {
      ['dragenter', 'dragover'].forEach(evt => {
        dropzoneOcr.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneOcr.classList.add('dragover');
        });
      });
      ['dragleave', 'drop'].forEach(evt => {
        dropzoneOcr.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneOcr.classList.remove('dragover');
        });
      });
      dropzoneOcr.addEventListener('drop', e => {
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          handleOcrFile(e.dataTransfer.files[0]);
        }
      });
    }

    function setOcrLang(lang) {
      selectedOcrLang = lang;
      document.getElementById('btn-lang-enghin').classList.toggle('active', lang === 'eng+hin');
      document.getElementById('btn-lang-eng').classList.toggle('active', lang === 'eng');
      document.getElementById('btn-lang-hin').classList.toggle('active', lang === 'hin');
    }

    let currentOcrBlobUrl = '';
    let currentOcrFileName = '';
    let isOcrDownloadComplete = false;

    function triggerOcrDownload() {
      if (!currentOcrBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentOcrBlobUrl;
      a.download = currentOcrFileName || 'removix_extracted_text.txt';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxOcr = document.getElementById('dl-checkbox-ocr');
    const dlLabelOcr = document.getElementById('dl-label-ocr');
    if (dlCheckboxOcr) {
      dlCheckboxOcr.addEventListener('change', () => {
        if (dlCheckboxOcr.checked) {
          if (dlLabelOcr) dlLabelOcr.classList.add('is-checked');
          triggerOcrDownload();
          setTimeout(() => {
            isOcrDownloadComplete = true;
          }, 2350);
        }
      });
      dlCheckboxOcr.addEventListener('click', (e) => {
        if (isOcrDownloadComplete) {
          e.preventDefault();
          triggerOcrDownload();
        }
      });
    }

    function resetOcrView() {
      currentOcrFile = null;
      if (ocrTimer1) clearTimeout(ocrTimer1);
      if (ocrTimer2) clearTimeout(ocrTimer2);
      if (ocrTimer3) clearTimeout(ocrTimer3);
      document.getElementById('ocr-result-wrap').style.display = 'none';
      document.getElementById('ocr-proc').style.display = 'none';
      document.getElementById('ocr-config-card').style.display = 'none';
      const notice = document.getElementById('ocr-limit-notice');
      if (notice) notice.style.display = 'none';
      document.getElementById('dropzone-ocr').style.display = '';
      const inputEl = document.getElementById('file-input-ocr');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxOcr) dlCheckboxOcr.checked = false;
      if (dlLabelOcr) dlLabelOcr.classList.remove('is-checked');
      isOcrDownloadComplete = false;
      if (currentOcrBlobUrl) {
        URL.revokeObjectURL(currentOcrBlobUrl);
        currentOcrBlobUrl = '';
      }
    }

    function handleOcrFile(file) {
      if (!file) return;
      currentOcrFile = file;

      const isPdf = file.name.toLowerCase().endsWith('.pdf') || file.type === 'application/pdf';
      document.getElementById('dropzone-ocr').style.display = 'none';
      document.getElementById('ocr-doc-name').textContent = file.name;
      const sizeKb = (file.size / 1024).toFixed(0);
      document.getElementById('ocr-doc-size').textContent = `${sizeKb} KB • ${isPdf ? 'PDF Document ready' : 'Image ready'}`;
      
      const btnText = document.getElementById('btn-start-ocr-text');
      if (btnText) {
        btnText.textContent = isPdf ? 'Extract Text from PDF' : 'Extract Text from Image';
      }

      document.getElementById('ocr-config-card').style.display = 'block';
    }

    function setOcrProgress(stepIdx, pct, title) {
      const compId = 'ocr-proc';
      const bar = document.getElementById(`${compId}-bar`);
      const pctEl = document.getElementById(`${compId}-pct`);
      const stageTitle = document.getElementById(`${compId}-stage-title`);

      if (bar) bar.style.width = pct + '%';
      if (pctEl) pctEl.textContent = Math.round(pct) + '%';
      if (stageTitle && title) stageTitle.textContent = title + '...';

      for (let i = 1; i <= 5; i++) {
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

    function executeOcrExtraction() {
      if (!currentOcrFile) return;

      const formData = new FormData();
      formData.append('file', currentOcrFile);
      formData.append('image', currentOcrFile);
      formData.append('lang', selectedOcrLang);

      document.getElementById('ocr-config-card').style.display = 'none';
      const procEl = document.getElementById('ocr-proc');
      procEl.style.display = 'block';

      // Step 1: Reading file
      setOcrProgress(1, 15, 'Reading file');

      ocrTimer1 = setTimeout(() => {
        // Step 2: Enhancing image quality
        setOcrProgress(2, 38, 'Enhancing image quality');
      }, 600);

      ocrTimer2 = setTimeout(() => {
        // Step 3: Detecting text
        setOcrProgress(3, 62, 'Detecting text');
      }, 1200);

      ocrTimer3 = setTimeout(() => {
        // Step 4: Extracting text
        setOcrProgress(4, 85, 'Extracting text');
      }, 1800);

      fetch('/api/ocr', {
        method: 'POST',
        body: formData
      })
      .then(res => {
        if (ocrTimer1) clearTimeout(ocrTimer1);
        if (ocrTimer2) clearTimeout(ocrTimer2);
        if (ocrTimer3) clearTimeout(ocrTimer3);
        if (!res.ok) {
          return res.json().then(e => { throw new Error(e.error || 'Text extraction failed'); });
        }
        return res.json();
      })
      .then(data => {
        // Step 5: Done
        setOcrProgress(5, 100, 'Done');
        setTimeout(() => {
          procEl.style.display = 'none';

          // Check if no readable text found
          if (data.status === 'empty' || !data.text || !data.text.trim()) {
            alert('No readable text was found in this image.');
            resetOcrView();
            return;
          }

          document.getElementById('ocr-result-wrap').style.display = 'block';
          
          if (dlCheckboxOcr) dlCheckboxOcr.checked = false;
          if (dlLabelOcr) dlLabelOcr.classList.remove('is-checked');
          isOcrDownloadComplete = false;

          // Check 20-page limit truncation
          const notice = document.getElementById('ocr-limit-notice');
          if (data.truncated) {
            if (notice) notice.style.display = 'block';
            alert('Only 20 pages can be processed at a time. The first 20 pages have been extracted.');
          } else {
            if (notice) notice.style.display = 'none';
          }

          const txtBox = document.getElementById('ocr-output-box');
          txtBox.value = data.text;

          const blob = new Blob([data.text], { type: 'text/plain;charset=utf-8' });
          currentOcrBlobUrl = URL.createObjectURL(blob);
          currentOcrFileName = 'removix_extracted_text.txt';
        }, 300);
      })
      .catch(err => {
        if (ocrTimer1) clearTimeout(ocrTimer1);
        if (ocrTimer2) clearTimeout(ocrTimer2);
        if (ocrTimer3) clearTimeout(ocrTimer3);
        const msg = err.message || '';
        if (msg.includes('This PDF file could not be processed')) {
          alert('This PDF file could not be processed. Please try a different file.');
        } else if (msg.includes('No readable text was found')) {
          alert('No readable text was found in this image.');
        } else {
          alert('Something went wrong, please try again.');
        }
        resetOcrView();
      });
    }

    function copyOcrText() {
      const txtBox = document.getElementById('ocr-output-box');
      txtBox.select();
      navigator.clipboard.writeText(txtBox.value).then(() => {
        const copyTextEl = document.getElementById('btn-copy-text');
        copyTextEl.textContent = 'Copied! ✓';
        setTimeout(() => {
          copyTextEl.textContent = 'Copy to Clipboard';
        }, 2000);
      });
    }
    """

    return render_layout(
        title="Image to Text (OCR)",
        active_tool="image-to-text",
        hero_title="Image & PDF to Text (OCR)",
        hero_sub="Extract selectable, editable text from screenshots, photos, and PDF documents with <strong>Hindi & English</strong> bilingual recognition.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
