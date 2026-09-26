"""
Removix UI - QR Code Generator View
-----------------------------------
Interactive interface to create custom-colored, high-resolution QR codes
for links, text, Wi-Fi credentials, and contact cards.
Badge: "QR GENERATOR" (Instant feedback spinner)
"""

from ui.layout import render_layout

QR_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="7" y="7" width="1" height="1"/><rect x="7" y="16" width="1" height="1"/><rect x="16" y="7" width="1" height="1"/><rect x="16" y="16" width="1" height="1"/></svg>"""


def render_qr_page() -> str:
    """Renders the QR Code Generator page."""
    main_card_html = r"""
    <!-- QR Input & Config Form -->
    <div id="qr-form-wrap">
      <div style="margin-bottom:20px;">
        <label style="display:block; font-size:14px; font-weight:700; color:var(--ink); margin-bottom:8px;">Enter Website URL or Text:</label>
        <textarea id="qr-input-text" rows="3" placeholder="https://example.com or any text to encode..." style="width:100%; border:1.5px solid #cbd5e1; border-radius:14px; padding:14px 16px; font-size:14.5px; font-family:inherit; color:var(--ink); outline:none; transition:border-color 0.2s; resize:vertical; box-sizing:border-box;"></textarea>
      </div>

      <!-- Customization Controls: Colors and Size -->
      <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:16px; padding:18px 20px; margin-bottom:24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
          <h3 style="font-size:14px; font-weight:700; color:var(--ink);">Design Customization</h3>
          <div class="scan-badge" style="margin:0; padding:3px 10px; font-size:10.5px;">
            <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            QR GENERATOR
          </div>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:18px;">
          <!-- QR Color (Foreground) -->
          <div>
            <label style="display:block; font-size:12.5px; font-weight:600; color:var(--ink-muted); margin-bottom:6px;">QR Pattern Color:</label>
            <div style="display:flex; align-items:center; gap:8px;">
              <input type="color" id="qr-fill-color" value="#0f172a" style="width:38px; height:38px; border:none; border-radius:8px; cursor:pointer; background:transparent;">
              <input type="text" id="qr-fill-hex" value="#0f172a" style="width:85px; padding:6px 10px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px; font-family:monospace; color:var(--ink);" oninput="document.getElementById('qr-fill-color').value=this.value">
            </div>
            <!-- Color Presets -->
            <div style="display:flex; gap:6px; margin-top:8px;">
              <div onclick="setFgColor('#0f172a')" style="width:20px; height:20px; border-radius:50%; background:#0f172a; cursor:pointer; border:1px solid #cbd5e1;" title="Classic Black"></div>
              <div onclick="setFgColor('#0284c7')" style="width:20px; height:20px; border-radius:50%; background:#0284c7; cursor:pointer; border:1px solid #cbd5e1;" title="Sky Blue"></div>
              <div onclick="setFgColor('#4f46e5')" style="width:20px; height:20px; border-radius:50%; background:#4f46e5; cursor:pointer; border:1px solid #cbd5e1;" title="Indigo"></div>
              <div onclick="setFgColor('#16a34a')" style="width:20px; height:20px; border-radius:50%; background:#16a34a; cursor:pointer; border:1px solid #cbd5e1;" title="Emerald"></div>
              <div onclick="setFgColor('#dc2626')" style="width:20px; height:20px; border-radius:50%; background:#dc2626; cursor:pointer; border:1px solid #cbd5e1;" title="Crimson"></div>
            </div>
          </div>

          <!-- Background Color -->
          <div>
            <label style="display:block; font-size:12.5px; font-weight:600; color:var(--ink-muted); margin-bottom:6px;">Background Color:</label>
            <div style="display:flex; align-items:center; gap:8px;">
              <input type="color" id="qr-back-color" value="#ffffff" style="width:38px; height:38px; border:none; border-radius:8px; cursor:pointer; background:transparent;">
              <input type="text" id="qr-back-hex" value="#ffffff" style="width:85px; padding:6px 10px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px; font-family:monospace; color:var(--ink);" oninput="document.getElementById('qr-back-color').value=this.value">
            </div>
            <!-- Background Presets -->
            <div style="display:flex; gap:6px; margin-top:8px;">
              <div onclick="setBgColor('#ffffff')" style="width:20px; height:20px; border-radius:50%; background:#ffffff; cursor:pointer; border:1px solid #cbd5e1;" title="Pure White"></div>
              <div onclick="setBgColor('#f8fafc')" style="width:20px; height:20px; border-radius:50%; background:#f8fafc; cursor:pointer; border:1px solid #cbd5e1;" title="Snow Slate"></div>
              <div onclick="setBgColor('#f0f9ff')" style="width:20px; height:20px; border-radius:50%; background:#f0f9ff; cursor:pointer; border:1px solid #cbd5e1;" title="Sky Soft"></div>
              <div onclick="setBgColor('#fef3c7')" style="width:20px; height:20px; border-radius:50%; background:#fef3c7; cursor:pointer; border:1px solid #cbd5e1;" title="Warm Amber"></div>
            </div>
          </div>
        </div>

        <!-- Format Selector (PNG, JPG, SVG) -->
        <div style="margin-top:16px; border-top:1px solid #e2e8f0; padding-top:14px;">
          <label style="display:block; font-size:12.5px; font-weight:600; color:var(--ink-muted); margin-bottom:8px;">Export Format:</label>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button type="button" class="zone-pill active" id="pill-fmt-png" onclick="setQrFormat('PNG')">PNG</button>
            <button type="button" class="zone-pill" id="pill-fmt-jpg" onclick="setQrFormat('JPG')">JPG</button>
            <button type="button" class="zone-pill" id="pill-fmt-svg" onclick="setQrFormat('SVG')">SVG</button>
          </div>
        </div>
      </div>

      <div style="text-align:center;">
        <button type="button" class="btn-primary" id="btn-gen-qr" onclick="generateQrCode()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          <span id="btn-gen-text">Generate QR Code</span>
        </button>
      </div>
    </div>

    <!-- Generating Loading Spinner -->
    <div id="qr-loading" style="display:none; text-align:center; padding:32px 0;">
      <div style="width:40px; height:40px; border:3px solid #e0f2fe; border-top-color:#0284c7; border-radius:50%; animation:qrSpin 0.8s linear infinite; margin:0 auto 12px;"></div>
      <p style="font-size:14.5px; font-weight:600; color:var(--ink);">Generating vector QR code...</p>
    </div>
    <style>@keyframes qrSpin { to { transform: rotate(360deg); } }</style>

    <!-- QR Result & Preview Card -->
    <div id="qr-result-wrap" style="display:none; margin-top:24px; text-align:center;">
      <div style="display:inline-block; padding:18px; background:#ffffff; border:1px solid #e2e8f0; border-radius:20px; box-shadow:0 8px 30px rgba(15,23,42,0.06); margin-bottom:20px;">
        <img id="qr-preview-img" src="" alt="Generated QR Code" style="max-width:280px; width:100%; height:auto; display:block; border-radius:8px;">
      </div>
      
      <div>
        <p id="qr-meta-text" style="font-size:13px; color:var(--ink-muted); margin-bottom:16px;">PNG Image • Lossless Master Clarity</p>
        <div class="result-actions">
          <div class="container">
            <label class="label" id="dl-label-qr" style="width: 205px;">
              <input type="checkbox" class="input" id="dl-checkbox-qr" />
              <span class="circle">
                <svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"></path>
                </svg>
                <div class="square"></div>
              </span>
              <p class="title" id="btn-download-qr-text">Download QR</p>
              <p class="title">Open</p>
            </label>
          </div>
          <button type="button" class="btn-reset" onclick="resetQrView()">
            <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
            Generate Another QR
          </button>
        </div>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Custom Brand Colors</h3>
          <p>Style your QR code with your company colors and high contrast for guaranteed scanner readability.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Mathematical Vector SVG</h3>
          <p>Export true mathematical vector SVG with resolution-independent geometry that never loses sharpness at any scale.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Permanent & Static</h3>
          <p>Generated QR codes never expire. No external redirect servers, 100% private and offline.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let currentQrFormat = 'PNG';

    // Sync color inputs
    const fgColor = document.getElementById('qr-fill-color');
    const fgHex = document.getElementById('qr-fill-hex');
    const bgColor = document.getElementById('qr-back-color');
    const bgHex = document.getElementById('qr-back-hex');

    if (fgColor && fgHex) {
      fgColor.addEventListener('input', () => fgHex.value = fgColor.value);
    }
    if (bgColor && bgHex) {
      bgColor.addEventListener('input', () => bgHex.value = bgColor.value);
    }

    function setFgColor(col) {
      if (fgColor) fgColor.value = col;
      if (fgHex) fgHex.value = col;
    }

    function setBgColor(col) {
      if (bgColor) bgColor.value = col;
      if (bgHex) bgHex.value = col;
    }

    function setQrFormat(fmt) {
      currentQrFormat = fmt.toUpperCase();
      ['PNG', 'JPG', 'SVG'].forEach(f => {
        const p = document.getElementById('pill-fmt-' + f.toLowerCase());
        if (p) p.classList.toggle('active', f === currentQrFormat);
      });
    }

    let currentQrDataUrl = '';
    let currentQrFileName = '';
    let isQrDownloadComplete = false;

    function triggerQrDownload() {
      if (!currentQrDataUrl) return;
      const a = document.createElement('a');
      a.href = currentQrDataUrl;
      a.download = currentQrFileName || 'removix_qrcode.png';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxQr = document.getElementById('dl-checkbox-qr');
    const dlLabelQr = document.getElementById('dl-label-qr');
    if (dlCheckboxQr) {
      dlCheckboxQr.addEventListener('change', () => {
        if (dlCheckboxQr.checked) {
          if (dlLabelQr) dlLabelQr.classList.add('is-checked');
          triggerQrDownload();
          setTimeout(() => {
            isQrDownloadComplete = true;
          }, 2350);
        }
      });
      dlCheckboxQr.addEventListener('click', (e) => {
        if (isQrDownloadComplete) {
          e.preventDefault();
          triggerQrDownload();
        }
      });
    }

    function resetQrView() {
      document.getElementById('qr-result-wrap').style.display = 'none';
      document.getElementById('qr-loading').style.display = 'none';
      document.getElementById('qr-form-wrap').style.display = 'block';
      if (dlCheckboxQr) dlCheckboxQr.checked = false;
      if (dlLabelQr) dlLabelQr.classList.remove('is-checked');
      isQrDownloadComplete = false;
      currentQrDataUrl = '';
    }

    function generateQrCode() {
      const text = document.getElementById('qr-input-text').value.trim();
      if (!text) {
        alert('Please enter a website link or text to generate a QR code.');
        document.getElementById('qr-input-text').focus();
        return;
      }

      const fill = document.getElementById('qr-fill-hex').value.trim() || '#0f172a';
      const back = document.getElementById('qr-back-hex').value.trim() || '#ffffff';

      document.getElementById('qr-form-wrap').style.display = 'none';
      document.getElementById('qr-loading').style.display = 'block';

      fetch('/api/qr-generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          fill_color: fill,
          back_color: back,
          format: currentQrFormat
        })
      })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Failed to generate QR code'); });
        return res.json();
      })
      .then(data => {
        document.getElementById('qr-loading').style.display = 'none';
        const resultWrap = document.getElementById('qr-result-wrap');
        const img = document.getElementById('qr-preview-img');
        const dlBtnText = document.getElementById('btn-download-qr-text');

        if (dlCheckboxQr) dlCheckboxQr.checked = false;
        if (dlLabelQr) dlLabelQr.classList.remove('is-checked');
        isQrDownloadComplete = false;

        img.src = data.data_url;
        currentQrDataUrl = data.data_url;
        const ext = (data.format || 'png').toLowerCase();
        currentQrFileName = `removix_qrcode.${ext}`;
        if (dlBtnText) {
          dlBtnText.textContent = `Download QR (${ext.toUpperCase()})`;
        }

        let desc = '';
        if (ext === 'svg') {
          desc = 'SVG Mathematical Vector • Resolution-Independent (No quality loss when scaled) • 100% Vector Path';
        } else if (ext === 'jpg') {
          desc = `JPG Image • Size: ${data.dimensions} • 100% Quality Chroma 4:4:4 • High Error Correction`;
        } else {
          desc = `PNG Image • Size: ${data.dimensions} • Lossless Master Clarity • High Error Correction`;
        }
        document.getElementById('qr-meta-text').textContent = desc;
        resultWrap.style.display = 'block';
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetQrView();
      });
    }
    """

    return render_layout(
        title="QR Code Generator",
        active_tool="qr-code",
        hero_title="Instant QR Code Generator",
        hero_sub="Create beautiful, customized <strong>high-resolution QR codes</strong> for links, contacts, and text in milliseconds.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
