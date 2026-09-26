"""
Removix UI - Black & White View with Before/After Comparison & Live Intensity Slider
"""
from ui.layout import render_layout, render_processing_component

BADGE_SVG = r"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>"""

def render_black_white_page() -> str:
    processing_card = render_processing_component(
        component_id="proc-black-white",
        badge_text="IMAGE MONOCHROME",
        badge_icon_svg=BADGE_SVG,
        title_text="Converting to Black & White...",
        subtitle_text="Calculating luminous weighting and enhancing tonal contrast.",
        steps=['Reading image', 'Converting channels', 'Enhancing contrast', 'Finalizing file'],
    )

    main_card_html = f"""
    <style>
      .bw-comparison-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 20px;
      }}
      @media (max-width: 768px) {{
        .bw-comparison-grid {{
          grid-template-columns: 1fr;
        }}
      }}
      .bw-card-box {{
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
      }}
      .bw-card-header {{
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
      }}
      .bw-badge-pill {{
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 3px 8px;
        border-radius: 6px;
      }}
      .bw-badge-orig {{
        background: var(--line-subtle);
        color: var(--ink-secondary);
      }}
      .bw-badge-after {{
        background: #f3e8ff;
        color: #9333ea;
      }}
      body.dark-mode .bw-badge-after {{
        background: rgba(147, 51, 234, 0.25);
        color: #c084fc;
      }}
      .bw-img-wrapper {{
        width: 100%;
        height: 250px;
        border-radius: 10px;
        overflow: hidden;
        background: rgba(0, 0, 0, 0.03);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
      }}
      body.dark-mode .bw-img-wrapper {{
        background: rgba(0, 0, 0, 0.3);
      }}
      .bw-img-wrapper img {{
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        display: block;
        transition: filter 0.15s ease-out;
      }}
    </style>
    
    <!-- Back to Image Tools Link -->
    <div style="margin-bottom: 20px;">
      <a href="/image-tools" class="btn-secondary" style="display:inline-flex; align-items:center; gap:8px; padding:8px 18px; font-size:13px; text-decoration:none; font-weight:600;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        Back to Image Tools
      </a>
    </div>

    <!-- Dropzone View -->
    <div id="dropzone-black_white" class="dropzone-box" onclick="document.getElementById('file-input-black_white').click()">
      <div class="folder-container">
        <div class="folder"><div class="front-side"><div class="tip"></div><div class="cover"></div></div><div class="back-side cover"></div></div>
        <span class="custom-file-upload">Choose Image</span>
      </div>
      <p class="drop-primary">Drop your image here, or browse</p>
      <p class="drop-secondary">Transform color photos into classic monochrome with live intensity slider</p>
    </div>
    <input type="file" id="file-input-black_white" accept=".png,.jpg,.jpeg,.webp" onchange="handleBlackWhiteUpload(this.files[0])">

    <!-- Active Black & White Workspace -->
    <div id="black_white-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>
          </div>
          <div>
            <p id="black_white-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">image.jpg</p>
            <p id="black_white-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetBlackWhiteView()">Change File</button>
      </div>

      <!-- Monochrome Intensity Slider (0-100, default 100) -->
      <div style="margin-top:20px; padding:16px 18px; background:var(--bg-page); border:1px solid var(--line); border-radius:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <label style="font-size:13px; font-weight:700; color:var(--ink);">Monochrome Intensity:</label>
          <span id="bw-intensity-val" style="font-size:12.5px; font-weight:800; color:var(--primary);">100% (Full B&W)</span>
        </div>
        <input type="range" id="bw-intensity-slider" min="0" max="100" value="100" style="width:100%; height:32px; cursor:pointer;" oninput="updateBwLivePreview(this.value)">
      </div>

      <!-- Before / After Side by Side -->
      <div class="bw-comparison-grid">
        <!-- Before: Original Color -->
        <div class="bw-card-box">
          <div class="bw-card-header">
            <span class="bw-badge-pill bw-badge-orig">BEFORE (ORIGINAL)</span>
            <span style="font-size:11.5px; color:var(--ink-muted);">Full Color</span>
          </div>
          <div class="bw-img-wrapper">
            <img id="bw-img-before" alt="Original Color">
          </div>
        </div>

        <!-- After: Monochrome Live Preview -->
        <div class="bw-card-box">
          <div class="bw-card-header">
            <span class="bw-badge-pill bw-badge-after">AFTER (LIVE MONOCHROME)</span>
            <span id="bw-contrast-pill" style="font-size:11.5px; font-weight:700; color:var(--primary);">High Tonal Contrast</span>
          </div>
          <div class="bw-img-wrapper">
            <img id="bw-img-after" alt="Black and White Preview">
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-black_white" style="padding:12px 28px; font-size:14px;" onclick="executeBlackWhite()">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>
          Convert to B&W
        </button>
      </div>
    </div>

    {processing_card}

    <!-- Result Card -->
    <div id="black_white-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Process Complete!</h3>
      <p id="black_white-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your black & white image is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-black_white" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-black_white" />
            <span class="circle"><svg class="icon" viewBox="0 0 24 24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"/></svg><div class="square"></div></span>
            <p class="title">Download File</p><p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetBlackWhiteView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Try Another Image
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top"><div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div><span class="free-badge">FREE</span></div>
          <h3>Maximum Precision</h3>
          <p>Engineered for high fidelity color rendering and optimal output quality.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top"><div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div><span class="free-badge">FREE</span></div>
          <h3>100% Private</h3>
          <p>Files stay entirely on your local machine with zero third-party cloud uploads.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top"><div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div><span class="free-badge">FREE</span></div>
          <h3>Lightning Fast</h3>
          <p>Instant processing completed locally in your browser session.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let currentBlackWhiteFile = null;
    let currentBlackWhiteBlobUrl = '';
    let isBlackWhiteDlDone = false;
    let currentIntensity = 100;

    const bwImgBefore = document.getElementById('bw-img-before');
    const bwImgAfter = document.getElementById('bw-img-after');
    const bwIntensityVal = document.getElementById('bw-intensity-val');
    const bwIntensitySlider = document.getElementById('bw-intensity-slider');

    function handleBlackWhiteUpload(file) {
      if (!file) return;
      currentBlackWhiteFile = file;
      document.getElementById('dropzone-black_white').style.display = 'none';
      document.getElementById('black_white-doc-name').textContent = file.name;
      document.getElementById('black_white-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('black_white-file-config').style.display = 'block';

      const reader = new FileReader();
      reader.onload = function(e) {
        bwImgBefore.src = e.target.result;
        bwImgAfter.src = e.target.result;
        updateBwLivePreview(100);
      };
      reader.readAsDataURL(file);
    }

    function updateBwLivePreview(val) {
      currentIntensity = parseInt(val) || 100;
      bwIntensityVal.textContent = currentIntensity + '% ' + (currentIntensity === 100 ? '(Full B&W)' : currentIntensity === 0 ? '(Color)' : '(Muted)');
      
      const grayPct = currentIntensity;
      const contrast = 1 + (currentIntensity / 100) * 0.25;
      bwImgAfter.style.filter = `grayscale(${grayPct}%) contrast(${contrast})`;
    }

    function triggerBlackWhiteDownload() {
      if (!currentBlackWhiteBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentBlackWhiteBlobUrl;
      a.download = 'removix_bw_' + (currentBlackWhiteFile ? currentBlackWhiteFile.name : 'image.jpg');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxBlackWhite = document.getElementById('dl-checkbox-black_white');
    const dlLabelBlackWhite = document.getElementById('dl-label-black_white');
    if (dlCheckboxBlackWhite) {
      dlCheckboxBlackWhite.addEventListener('change', () => {
        if (dlCheckboxBlackWhite.checked) {
          if (dlLabelBlackWhite) dlLabelBlackWhite.classList.add('is-checked');
          triggerBlackWhiteDownload();
          setTimeout(() => { isBlackWhiteDlDone = true; }, 2350);
        }
      });
      dlCheckboxBlackWhite.addEventListener('click', (e) => {
        if (isBlackWhiteDlDone) { e.preventDefault(); triggerBlackWhiteDownload(); }
      });
    }

    function resetBlackWhiteView() {
      currentBlackWhiteFile = null;
      document.getElementById('black_white-result-card').style.display = 'none';
      document.getElementById('proc-black-white').style.display = 'none';
      document.getElementById('black_white-file-config').style.display = 'none';
      document.getElementById('dropzone-black_white').style.display = '';
      const inputEl = document.getElementById('file-input-black_white');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxBlackWhite) dlCheckboxBlackWhite.checked = false;
      if (dlLabelBlackWhite) dlLabelBlackWhite.classList.remove('is-checked');
      isBlackWhiteDlDone = false;
      if (currentBlackWhiteBlobUrl) { URL.revokeObjectURL(currentBlackWhiteBlobUrl); currentBlackWhiteBlobUrl = ''; }
      bwImgBefore.src = '';
      bwImgAfter.src = '';
      bwImgAfter.style.filter = '';
      bwIntensitySlider.value = 100;
    }

    function executeBlackWhite() {
      if (!currentBlackWhiteFile) return;
      const formData = new FormData();
      formData.append('file', currentBlackWhiteFile);

      document.getElementById('black_white-file-config').style.display = 'none';
      const procEl = document.getElementById('proc-black-white');
      procEl.style.display = 'block';

      fetch('/api/black-white', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Conversion failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('black_white-result-card').style.display = 'block';
        currentBlackWhiteBlobUrl = URL.createObjectURL(blob);
        document.getElementById('black_white-result-sub').textContent = `Monochrome contrast applied (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetBlackWhiteView();
      });
    }
    """

    return render_layout(
        title="Black & White Image",
        active_tool="image-tools",
        hero_title="Black & White Image",
        hero_sub="Convert photos to <strong>fine art monochrome with rich tonal contrast</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
