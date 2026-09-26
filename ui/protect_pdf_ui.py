"""
Removix UI - Protect PDF View with First Page Preview & Encryption Form
"""
from ui.layout import render_layout, render_processing_component

PDF_PROTECT_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>"""

def render_protect_pdf_page() -> str:
    """Renders the Protect PDF tool view with first-page preview."""
    processing_card = render_processing_component(
        component_id="protect-proc",
        badge_text="SECURITY ENGINE",
        badge_icon_svg=PDF_PROTECT_BADGE_SVG,
        title_text="Encrypting Document...",
        subtitle_text="Applying AES-256 encryption keys to lock the PDF securely.",
        steps=[
            "Reading document",
            "Generating encryption keys",
            "Encrypting pages",
            "Finalizing secured file",
        ],
    )

    main_card_html = f"""
    <style>
      .protect-workspace {{
        display: grid;
        grid-template-columns: 280px 1fr;
        gap: 24px;
        margin-top: 20px;
        align-items: start;
      }}
      @media (max-width: 800px) {{
        .protect-workspace {{
          grid-template-columns: 1fr;
        }}
      }}
      .protect-preview-box {{
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
      }}
      .protect-canvas-wrap {{
        width: 100%;
        height: 280px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border-radius: 8px;
        background: #ffffff;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
      }}
      body.dark-mode .protect-canvas-wrap {{
        background: #1e293b;
      }}
      .protect-canvas-wrap canvas {{
        max-width: 100%;
        max-height: 100%;
      }}
      .protect-form-box {{
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 20px;
        display: flex;
        flex-direction: column;
      }}
    </style>
    
    <!-- Back to PDF Tools Link -->
    <div style="margin-bottom: 20px;">
      <a href="/pdf-tools" class="btn-secondary" style="display:inline-flex; align-items:center; gap:8px; padding:8px 18px; font-size:13px; text-decoration:none; font-weight:600;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        Back to PDF Tools
      </a>
    </div>

    <!-- Dropzone View -->
    <div id="dropzone-protect" class="dropzone-box" onclick="document.getElementById('file-input-protect').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose PDF File</span>
      </div>
      <p class="drop-primary">Drop your PDF document here, or browse</p>
      <p class="drop-secondary">Protect confidential files with military-grade 256-bit encryption</p>
    </div>
    <input type="file" id="file-input-protect" accept=".pdf,application/pdf" onchange="handleProtectUpload(this.files[0])">

    <!-- Active PDF Protect Workspace -->
    <div id="protect-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding-bottom:14px; border-bottom:1px solid var(--line);">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#fef9c3; color:#ca8a04; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          </div>
          <div>
            <p id="protect-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">Document.pdf</p>
            <p id="protect-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetProtectView()">Change File</button>
      </div>

      <div class="protect-workspace">
        <!-- Left: First Page Preview -->
        <div class="protect-preview-box">
          <div style="font-size:12px; font-weight:700; color:var(--ink); margin-bottom:10px; align-self:flex-start;">
            FIRST PAGE PREVIEW
          </div>
          <div class="protect-canvas-wrap">
            <canvas id="protect-first-page-canvas"></canvas>
          </div>
          <div id="protect-page-meta" style="font-size:11.5px; color:var(--ink-muted); margin-top:10px;">
            1 of 1 pages
          </div>
        </div>

        <!-- Right: Password Fields -->
        <div class="protect-form-box">
          <div style="margin-bottom:16px;">
            <label style="display:block; font-size:13px; font-weight:700; color:var(--ink); margin-bottom:6px;">Set Password:</label>
            <input type="password" id="protect-pw" placeholder="Enter password to encrypt file..." style="width:100%; box-sizing:border-box; padding:11px 14px; border:1px solid var(--line); border-radius:10px; font-size:14px; outline:none; background:var(--bg-page); color:var(--ink);">
          </div>
          <div style="margin-bottom:20px;">
            <label style="display:block; font-size:13px; font-weight:700; color:var(--ink); margin-bottom:6px;">Confirm Password:</label>
            <input type="password" id="protect-pw-confirm" placeholder="Confirm password..." style="width:100%; box-sizing:border-box; padding:11px 14px; border:1px solid var(--line); border-radius:10px; font-size:14px; outline:none; background:var(--bg-page); color:var(--ink);">
          </div>

          <button type="button" class="btn-primary" id="btn-start-protect" style="width:100%; justify-content:center; padding:12px 20px; font-size:14px;" onclick="executePdfProtect()">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            Protect PDF
          </button>
        </div>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card -->
    <div id="protect-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Document Secured!</h3>
      <p id="protect-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your password-protected PDF is ready for safe distribution.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-protect" style="width: 215px;">
            <input type="checkbox" class="input" id="dl-checkbox-protect" />
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
        <button type="button" class="btn-reset" onclick="resetProtectView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Protect Another PDF
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>AES-256 Encryption</h3>
          <p>Bank-grade encryption prevents unauthorized viewing, extraction, or copying of sensitive content.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>First Page Preview</h3>
          <p>Verify document contents visually before sealing it behind cryptographic encryption.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>100% Private</h3>
          <p>Password encryption runs directly on your local system with zero third-party transmission.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let currentProtectFile = null;
    let currentProtectBlobUrl = '';
    let isProtectDownloadComplete = false;

    const protectFirstPageCanvas = document.getElementById('protect-first-page-canvas');
    const protectPageMeta = document.getElementById('protect-page-meta');

    function handleProtectUpload(file) {
      if (!file) return;
      currentProtectFile = file;
      document.getElementById('dropzone-protect').style.display = 'none';
      document.getElementById('protect-doc-name').textContent = file.name;
      document.getElementById('protect-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('protect-file-config').style.display = 'block';

      renderProtectFirstPage(file);
    }

    function renderProtectFirstPage(file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        if (window.pdfjsLib) {
          const typedArray = new Uint8Array(e.target.result);
          pdfjsLib.getDocument({ data: typedArray }).promise.then(function(doc) {
            protectPageMeta.textContent = `Total pages: ${doc.numPages}`;
            doc.getPage(1).then(function(page) {
              const baseViewport = page.getViewport({ scale: 1.0 });
              const scale = 260 / baseViewport.height;
              const viewport = page.getViewport({ scale: Math.max(0.3, scale) });
              protectFirstPageCanvas.width = viewport.width;
              protectFirstPageCanvas.height = viewport.height;
              const ctx = protectFirstPageCanvas.getContext('2d');
              page.render({ canvasContext: ctx, viewport: viewport });
            });
          }).catch(function(err) {});
        }
      };
      reader.readAsArrayBuffer(file);
    }

    function triggerProtectDownload() {
      if (!currentProtectBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentProtectBlobUrl;
      a.download = 'removix_protected.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxProtect = document.getElementById('dl-checkbox-protect');
    const dlLabelProtect = document.getElementById('dl-label-protect');
    if (dlCheckboxProtect) {
      dlCheckboxProtect.addEventListener('change', () => {
        if (dlCheckboxProtect.checked) {
          if (dlLabelProtect) dlLabelProtect.classList.add('is-checked');
          triggerProtectDownload();
          setTimeout(() => { isProtectDownloadComplete = true; }, 2350);
        }
      });
      dlCheckboxProtect.addEventListener('click', (e) => {
        if (isProtectDownloadComplete) { e.preventDefault(); triggerProtectDownload(); }
      });
    }

    function resetProtectView() {
      currentProtectFile = null;
      document.getElementById('protect-result-card').style.display = 'none';
      document.getElementById('protect-proc').style.display = 'none';
      document.getElementById('protect-file-config').style.display = 'none';
      document.getElementById('dropzone-protect').style.display = '';
      const inputEl = document.getElementById('file-input-protect');
      if (inputEl) inputEl.value = '';
      document.getElementById('protect-pw').value = '';
      document.getElementById('protect-pw-confirm').value = '';
      if (dlCheckboxProtect) dlCheckboxProtect.checked = false;
      if (dlLabelProtect) dlLabelProtect.classList.remove('is-checked');
      isProtectDownloadComplete = false;
      if (currentProtectBlobUrl) { URL.revokeObjectURL(currentProtectBlobUrl); currentProtectBlobUrl = ''; }
    }

    function executePdfProtect() {
      if (!currentProtectFile) return;

      const pw = document.getElementById('protect-pw').value;
      const pwConfirm = document.getElementById('protect-pw-confirm').value;

      if (!pw) {
        alert('Please enter a password.');
        return;
      }
      if (pw !== pwConfirm) {
        alert('Passwords do not match. Please re-enter.');
        return;
      }

      const formData = new FormData();
      formData.append('pdf', currentProtectFile);
      formData.append('password', pw);

      document.getElementById('protect-file-config').style.display = 'none';
      const procEl = document.getElementById('protect-proc');
      procEl.style.display = 'block';

      fetch('/api/protect-pdf', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Encryption failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('protect-result-card').style.display = 'block';
        currentProtectBlobUrl = URL.createObjectURL(blob);
        document.getElementById('protect-result-sub').textContent = `Encrypted with AES-256 (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetProtectView();
      });
    }
    """

    return render_layout(
        title="Protect PDF",
        active_tool="pdf-tools",
        hero_title="Protect PDF Document",
        hero_sub="Encrypt PDF documents with <strong>first page preview and 256-bit password protection</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
