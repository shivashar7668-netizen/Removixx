"""
Removix UI - Resize Image View with Aspect Ratio Lock & Live Dimension Comparison
"""
from ui.layout import render_layout, render_processing_component

BADGE_SVG = r"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></svg>"""

def render_resize_image_page() -> str:
    processing_card = render_processing_component(
        component_id="proc-resize-image",
        badge_text="IMAGE RESIZING",
        badge_icon_svg=BADGE_SVG,
        title_text="Resizing Image...",
        subtitle_text="Resampling pixel grid with high-fidelity Lanczos interpolation.",
        steps=['Reading image', 'Calculating scale', 'Interpolating pixels', 'Finalizing file'],
    )

    main_card_html = f"""
    <style>
      .resize-workspace {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 20px;
      }}
      @media (max-width: 800px) {{
        .resize-workspace {{
          grid-template-columns: 1fr;
        }}
      }}
      .resize-card-box {{
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 18px;
        position: relative;
        display: flex;
        flex-direction: column;
      }}
      .resize-compare-bar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 14px;
        background: var(--bg-page);
        border: 1px solid var(--line);
        border-radius: 10px;
        margin-top: 14px;
        font-size: 12.5px;
      }}
      .resize-preview-img-wrap {{
        width: 100%;
        height: 250px;
        border-radius: 10px;
        overflow: hidden;
        background: rgba(0, 0, 0, 0.03);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        margin-top: 14px;
      }}
      body.dark-mode .resize-preview-img-wrap {{
        background: rgba(0, 0, 0, 0.3);
      }}
      #resize-live-img {{
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        display: block;
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
    <div id="dropzone-resize_image" class="dropzone-box" onclick="document.getElementById('file-input-resize_image').click()">
      <div class="folder-container">
        <div class="folder"><div class="front-side"><div class="tip"></div><div class="cover"></div></div><div class="back-side cover"></div></div>
        <span class="custom-file-upload">Choose Image</span>
      </div>
      <p class="drop-primary">Drop your image here, or browse</p>
      <p class="drop-secondary">Scale width and height with aspect ratio lock and live preview</p>
    </div>
    <input type="file" id="file-input-resize_image" accept=".png,.jpg,.jpeg,.webp" onchange="handleResizeImageUpload(this.files[0])">

    <!-- Active Resize Workspace -->
    <div id="resize_image-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></svg>
          </div>
          <div>
            <p id="resize_image-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">image.jpg</p>
            <p id="resize_image-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetResizeImageView()">Change File</button>
      </div>

      <div class="resize-workspace">
        <!-- Left: Dimension Controls & Presets -->
        <div class="resize-card-box">
          <label style="display:block; font-size:13px; font-weight:700; color:var(--ink); margin-bottom:12px;">Custom Dimensions (Pixels):</label>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
            <div>
              <label style="display:block; font-size:12px; font-weight:700; color:var(--ink-muted); margin-bottom:5px;">Width (px):</label>
              <input type="number" id="resize-w" min="1" max="10000" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid var(--line); border-radius:8px; font-size:13.5px; background:var(--bg-page); color:var(--ink);" oninput="onResizeDimChange('w')">
            </div>
            <div>
              <label style="display:block; font-size:12px; font-weight:700; color:var(--ink-muted); margin-bottom:5px;">Height (px):</label>
              <input type="number" id="resize-h" min="1" max="10000" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid var(--line); border-radius:8px; font-size:13.5px; background:var(--bg-page); color:var(--ink);" oninput="onResizeDimChange('h')">
            </div>
          </div>

          <!-- Lock Aspect Ratio (default on) -->
          <div style="margin-top:14px;">
            <label style="display:inline-flex; align-items:center; gap:8px; font-size:12.5px; font-weight:700; color:var(--ink); cursor:pointer;">
              <input type="checkbox" id="resize-aspect" checked style="accent-color:var(--primary); width:16px; height:16px;">
              <span>Lock Aspect Ratio</span>
            </label>
          </div>

          <!-- Quick Scale Presets -->
          <div style="margin-top:16px;">
            <label style="display:block; font-size:12px; font-weight:700; color:var(--ink-muted); margin-bottom:6px;">Quick Presets:</label>
            <div style="display:flex; flex-wrap:wrap; gap:6px;">
              <button type="button" class="btn-secondary" style="padding:5px 10px; font-size:11.5px;" onclick="applyResizeScale(25)">25%</button>
              <button type="button" class="btn-secondary" style="padding:5px 10px; font-size:11.5px;" onclick="applyResizeScale(50)">50%</button>
              <button type="button" class="btn-secondary" style="padding:5px 10px; font-size:11.5px;" onclick="applyResizeScale(75)">75%</button>
              <button type="button" class="btn-secondary" style="padding:5px 10px; font-size:11.5px;" onclick="applyResizeScale(150)">150%</button>
              <button type="button" class="btn-secondary" style="padding:5px 10px; font-size:11.5px;" onclick="applyResizeScale(200)">200%</button>
            </div>
          </div>

          <!-- Dimension Comparison Bar -->
          <div class="resize-compare-bar">
            <div>
              <span style="color:var(--ink-muted); font-size:11.5px;">Original:</span>
              <strong id="resize-orig-dim" style="color:var(--ink); margin-left:4px;">0 × 0 px</strong>
            </div>
            <div>
              <span style="color:var(--ink-muted); font-size:11.5px;">New:</span>
              <strong id="resize-new-dim" style="color:var(--primary); margin-left:4px;">0 × 0 px</strong>
            </div>
          </div>
        </div>

        <!-- Right: Live Preview -->
        <div class="resize-card-box">
          <div style="font-size:12.5px; font-weight:700; color:var(--ink); display:flex; justify-content:space-between; align-items:center;">
            <span>Preview</span>
            <span id="resize-scale-pct" style="font-size:11.5px; font-weight:700; color:var(--primary);">100% Scale</span>
          </div>
          <div class="resize-preview-img-wrap">
            <img id="resize-live-img" alt="Resized Preview">
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-resize_image" style="padding:12px 28px; font-size:14px;" onclick="executeResizeImage()">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></svg>
          Resize Image
        </button>
      </div>
    </div>

    {processing_card}

    <!-- Result Card -->
    <div id="resize_image-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Process Complete!</h3>
      <p id="resize_image-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your resized image is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-resize_image" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-resize_image" />
            <span class="circle"><svg class="icon" viewBox="0 0 24 24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"/></svg><div class="square"></div></span>
            <p class="title">Download File</p><p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetResizeImageView()">
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
    let currentResizeImageFile = null;
    let currentResizeImageBlobUrl = '';
    let isResizeImageDlDone = false;
    let origWidth = 0;
    let origHeight = 0;

    const resizeWInput = document.getElementById('resize-w');
    const resizeHInput = document.getElementById('resize-h');
    const resizeAspectCheck = document.getElementById('resize-aspect');
    const resizeOrigDim = document.getElementById('resize-orig-dim');
    const resizeNewDim = document.getElementById('resize-new-dim');
    const resizeScalePct = document.getElementById('resize-scale-pct');
    const resizeLiveImg = document.getElementById('resize-live-img');

    function handleResizeImageUpload(file) {
      if (!file) return;
      currentResizeImageFile = file;
      document.getElementById('dropzone-resize_image').style.display = 'none';
      document.getElementById('resize_image-doc-name').textContent = file.name;
      document.getElementById('resize_image-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('resize_image-file-config').style.display = 'block';

      const reader = new FileReader();
      reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
          origWidth = img.naturalWidth;
          origHeight = img.naturalHeight;
          resizeWInput.value = origWidth;
          resizeHInput.value = origHeight;
          resizeOrigDim.textContent = `${origWidth} × ${origHeight} px`;
          resizeNewDim.textContent = `${origWidth} × ${origHeight} px`;
          resizeScalePct.textContent = '100% Scale';
          resizeLiveImg.src = e.target.result;
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    function onResizeDimChange(changed) {
      if (!origWidth || !origHeight) return;
      let w = parseInt(resizeWInput.value) || 1;
      let h = parseInt(resizeHInput.value) || 1;

      if (resizeAspectCheck.checked) {
        const ratio = origWidth / origHeight;
        if (changed === 'w') {
          h = Math.max(1, Math.round(w / ratio));
          resizeHInput.value = h;
        } else {
          w = Math.max(1, Math.round(h * ratio));
          resizeWInput.value = w;
        }
      }
      updateComparisonDisplay(w, h);
    }

    function applyResizeScale(pct) {
      if (!origWidth || !origHeight) return;
      const factor = pct / 100;
      const w = Math.max(1, Math.round(origWidth * factor));
      const h = Math.max(1, Math.round(origHeight * factor));
      resizeWInput.value = w;
      resizeHInput.value = h;
      updateComparisonDisplay(w, h);
    }

    function updateComparisonDisplay(w, h) {
      resizeNewDim.textContent = `${w} × ${h} px`;
      const pctW = Math.round((w / origWidth) * 100);
      resizeScalePct.textContent = `${pctW}% Scale`;
    }

    function triggerResizeImageDownload() {
      if (!currentResizeImageBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentResizeImageBlobUrl;
      a.download = 'removix_resized_' + (currentResizeImageFile ? currentResizeImageFile.name : 'image.png');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxResizeImage = document.getElementById('dl-checkbox-resize_image');
    const dlLabelResizeImage = document.getElementById('dl-label-resize_image');
    if (dlCheckboxResizeImage) {
      dlCheckboxResizeImage.addEventListener('change', () => {
        if (dlCheckboxResizeImage.checked) {
          if (dlLabelResizeImage) dlLabelResizeImage.classList.add('is-checked');
          triggerResizeImageDownload();
          setTimeout(() => { isResizeImageDlDone = true; }, 2350);
        }
      });
      dlCheckboxResizeImage.addEventListener('click', (e) => {
        if (isResizeImageDlDone) { e.preventDefault(); triggerResizeImageDownload(); }
      });
    }

    function resetResizeImageView() {
      currentResizeImageFile = null;
      document.getElementById('resize_image-result-card').style.display = 'none';
      document.getElementById('proc-resize-image').style.display = 'none';
      document.getElementById('resize_image-file-config').style.display = 'none';
      document.getElementById('dropzone-resize_image').style.display = '';
      const inputEl = document.getElementById('file-input-resize_image');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxResizeImage) dlCheckboxResizeImage.checked = false;
      if (dlLabelResizeImage) dlLabelResizeImage.classList.remove('is-checked');
      isResizeImageDlDone = false;
      if (currentResizeImageBlobUrl) { URL.revokeObjectURL(currentResizeImageBlobUrl); currentResizeImageBlobUrl = ''; }
      resizeLiveImg.src = '';
      origWidth = 0;
      origHeight = 0;
    }

    function executeResizeImage() {
      if (!currentResizeImageFile) return;
      const w = parseInt(resizeWInput.value);
      const h = parseInt(resizeHInput.value);
      if (!w || !h || w < 1 || h < 1) {
        alert('Please specify valid positive dimensions.');
        return;
      }

      const formData = new FormData();
      formData.append('file', currentResizeImageFile);
      formData.append('width', w);
      formData.append('height', h);
      formData.append('unit', 'px');

      document.getElementById('resize_image-file-config').style.display = 'none';
      const procEl = document.getElementById('proc-resize-image');
      procEl.style.display = 'block';

      fetch('/api/resize-image', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Resize failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('resize_image-result-card').style.display = 'block';
        currentResizeImageBlobUrl = URL.createObjectURL(blob);
        document.getElementById('resize_image-result-sub').textContent = `Scaled to ${w} × ${h} px (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetResizeImageView();
      });
    }
    """

    return render_layout(
        title="Resize Image",
        active_tool="image-tools",
        hero_title="Resize Image",
        hero_sub="Scale width and height in pixels or percentage with <strong>aspect ratio lock</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
