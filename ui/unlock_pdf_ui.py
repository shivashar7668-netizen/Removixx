"""
Removix UI - Unlock PDF View with Password Protected Indicator & Success Preview
"""
from ui.layout import render_layout, render_processing_component

PDF_UNLOCK_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>"""

def render_unlock_pdf_page() -> str:
    """Renders the Unlock PDF tool view."""
    processing_card = render_processing_component(
        component_id="unlock-proc",
        badge_text="SECURITY ENGINE",
        badge_icon_svg=PDF_UNLOCK_BADGE_SVG,
        title_text="Decrypting Document...",
        subtitle_text="Authenticating password credentials and stripping encryption layers.",
        steps=[
            "Reading secured file",
            "Authenticating credentials",
            "Removing encryption",
            "Finalizing unrestricted PDF",
        ],
    )

    main_card_html = f"""
    <style>
      .unlock-card-panel {{
        margin-top: 20px;
        padding: 24px;
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 18px;
      }}
      .unlock-status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        background: #fef2f2;
        color: #ef4444;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid #fecaca;
      }}
      body.dark-mode .unlock-status-pill {{
        background: rgba(239, 68, 68, 0.15);
        border-color: rgba(239, 68, 68, 0.3);
      }}
      .unlocked-preview-container {{
        width: 100%;
        max-width: 320px;
        margin: 16px auto;
        height: 240px;
        border-radius: 10px;
        overflow: hidden;
        background: #ffffff;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      body.dark-mode .unlocked-preview-container {{
        background: #1e293b;
      }}
      #unlocked-preview-canvas {{
        max-width: 100%;
        max-height: 100%;
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
    <div id="dropzone-unlock" class="dropzone-box" onclick="document.getElementById('file-input-unlock').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose Protected PDF</span>
      </div>
      <p class="drop-primary">Drop your locked PDF document here, or browse</p>
      <p class="drop-secondary">Permanently remove password barriers and permission restrictions</p>
    </div>
    <input type="file" id="file-input-unlock" accept=".pdf,application/pdf" onchange="handleUnlockUpload(this.files[0])">

    <!-- Active PDF Unlock Workspace -->
    <div id="unlock-file-config" class="unlock-card-panel" style="display:none;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding-bottom:14px; border-bottom:1px solid var(--line);">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#d1fae5; color:#059669; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>
          </div>
          <div>
            <div style="display:flex; align-items:center; gap:8px;">
              <p id="unlock-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">Document.pdf</p>
              <span class="unlock-status-pill">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                Password Protected
              </span>
            </div>
            <p id="unlock-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetUnlockView()">Change File</button>
      </div>

      <!-- Password Input -->
      <div style="margin-top:20px; max-width:440px;">
        <label style="display:block; font-size:13px; font-weight:700; color:var(--ink); margin-bottom:6px;">Document Password:</label>
        <input type="password" id="unlock-pw" placeholder="Enter current document password..." style="width:100%; box-sizing:border-box; padding:11px 14px; border:1px solid var(--line); border-radius:10px; font-size:14px; outline:none; background:var(--bg-page); color:var(--ink);">
        <p style="font-size:11.5px; color:var(--ink-muted); margin-top:6px;">Enter the password once to decrypt and view document preview.</p>
      </div>

      <div style="margin-top:22px; text-align:left;">
        <button type="button" class="btn-primary" id="btn-start-unlock" style="padding:12px 28px; font-size:14px;" onclick="executePdfUnlock()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>
          Unlock PDF
        </button>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card with Unlocked Preview -->
    <div id="unlock-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Document Unlocked!</h3>
      <p id="unlock-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:14px;">Password removed successfully. Verified preview below:</p>

      <!-- Unlocked Live Preview Canvas -->
      <div class="unlocked-preview-container">
        <canvas id="unlocked-preview-canvas"></canvas>
      </div>

      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-unlock" style="width: 215px;">
            <input type="checkbox" class="input" id="dl-checkbox-unlock" />
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
        <button type="button" class="btn-reset" onclick="resetUnlockView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Unlock Another PDF
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Restriction Stripping</h3>
          <p>Permanently eliminates printing, copying, and modification password blocks.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Verified Preview</h3>
          <p>Preview unlocked document pages immediately after successful password removal.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>100% Private</h3>
          <p>Passwords are never sent to external servers or logged in plain text.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let currentUnlockFile = null;
    let currentUnlockBlobUrl = '';
    let isUnlockDownloadComplete = false;

    const unlockedPreviewCanvas = document.getElementById('unlocked-preview-canvas');

    function handleUnlockUpload(file) {
      if (!file) return;
      currentUnlockFile = file;
      document.getElementById('dropzone-unlock').style.display = 'none';
      document.getElementById('unlock-doc-name').textContent = file.name;
      document.getElementById('unlock-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('unlock-file-config').style.display = 'block';
    }

    function renderUnlockedPreview(blob) {
      const reader = new FileReader();
      reader.onload = function(e) {
        if (window.pdfjsLib) {
          const typedArray = new Uint8Array(e.target.result);
          pdfjsLib.getDocument({ data: typedArray }).promise.then(function(doc) {
            doc.getPage(1).then(function(page) {
              const baseViewport = page.getViewport({ scale: 1.0 });
              const scale = 220 / baseViewport.height;
              const viewport = page.getViewport({ scale: Math.max(0.3, scale) });
              unlockedPreviewCanvas.width = viewport.width;
              unlockedPreviewCanvas.height = viewport.height;
              const ctx = unlockedPreviewCanvas.getContext('2d');
              page.render({ canvasContext: ctx, viewport: viewport });
            });
          }).catch(function(err) {});
        }
      };
      reader.readAsArrayBuffer(blob);
    }

    function triggerUnlockDownload() {
      if (!currentUnlockBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentUnlockBlobUrl;
      a.download = 'removix_unlocked.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxUnlock = document.getElementById('dl-checkbox-unlock');
    const dlLabelUnlock = document.getElementById('dl-label-unlock');
    if (dlCheckboxUnlock) {
      dlCheckboxUnlock.addEventListener('change', () => {
        if (dlCheckboxUnlock.checked) {
          if (dlLabelUnlock) dlLabelUnlock.classList.add('is-checked');
          triggerUnlockDownload();
          setTimeout(() => { isUnlockDownloadComplete = true; }, 2350);
        }
      });
      dlCheckboxUnlock.addEventListener('click', (e) => {
        if (isUnlockDownloadComplete) { e.preventDefault(); triggerUnlockDownload(); }
      });
    }

    function resetUnlockView() {
      currentUnlockFile = null;
      document.getElementById('unlock-result-card').style.display = 'none';
      document.getElementById('unlock-proc').style.display = 'none';
      document.getElementById('unlock-file-config').style.display = 'none';
      document.getElementById('dropzone-unlock').style.display = '';
      const inputEl = document.getElementById('file-input-unlock');
      if (inputEl) inputEl.value = '';
      document.getElementById('unlock-pw').value = '';
      if (dlCheckboxUnlock) dlCheckboxUnlock.checked = false;
      if (dlLabelUnlock) dlLabelUnlock.classList.remove('is-checked');
      isUnlockDownloadComplete = false;
      if (currentUnlockBlobUrl) { URL.revokeObjectURL(currentUnlockBlobUrl); currentUnlockBlobUrl = ''; }
    }

    function executePdfUnlock() {
      if (!currentUnlockFile) return;

      const pw = document.getElementById('unlock-pw').value;
      if (!pw) {
        alert('Please enter the document password.');
        return;
      }

      const formData = new FormData();
      formData.append('pdf', currentUnlockFile);
      formData.append('password', pw);

      document.getElementById('unlock-file-config').style.display = 'none';
      const procEl = document.getElementById('unlock-proc');
      procEl.style.display = 'block';

      fetch('/api/unlock-pdf', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Incorrect password or unlock failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('unlock-result-card').style.display = 'block';
        currentUnlockBlobUrl = URL.createObjectURL(blob);
        document.getElementById('unlock-result-sub').textContent = `Document unlocked (${(blob.size / 1024).toFixed(0)} KB).`;
        renderUnlockedPreview(blob);
      })
      .catch(err => {
        alert(err.message || 'Incorrect password. Please try again.');
        document.getElementById('unlock-proc').style.display = 'none';
        document.getElementById('unlock-file-config').style.display = 'block';
      });
    }
    """

    return render_layout(
        title="Unlock PDF",
        active_tool="pdf-tools",
        hero_title="Unlock PDF Document",
        hero_sub="Remove password security with <strong>password indicator and post-unlock preview</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
