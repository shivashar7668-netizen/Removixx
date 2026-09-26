"""
Removix UI - Compress Image View with Before/After Comparison & Live Estimation
"""
from ui.layout import render_layout, render_processing_component

BADGE_SVG = r"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/></svg>"""

def render_compress_image_page() -> str:
    processing_card = render_processing_component(
        component_id="proc-compress-image",
        badge_text="IMAGE COMPRESSION",
        badge_icon_svg=BADGE_SVG,
        title_text="Compressing File...",
        subtitle_text="Stripping redundant metadata and quantizing color tables.",
        steps=['Reading file', 'Analyzing pixels', 'Applying compression', 'Finalizing file'],
    )

    main_card_html = f"""
    <style>
      .comp-comparison-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 20px;
      }}
      @media (max-width: 768px) {{
        .comp-comparison-grid {{
          grid-template-columns: 1fr;
        }}
      }}
      .comp-card-box {{
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
      }}
      .comp-card-header {{
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
      }}
      .comp-badge-pill {{
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 3px 8px;
        border-radius: 6px;
      }}
      .comp-badge-orig {{
        background: var(--line-subtle);
        color: var(--ink-secondary);
      }}
      .comp-badge-after {{
        background: var(--primary-light);
        color: var(--primary);
      }}
      .comp-img-wrapper {{
        width: 100%;
        height: 240px;
        border-radius: 10px;
        overflow: hidden;
        background: rgba(0, 0, 0, 0.03);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
      }}
      body.dark-mode .comp-img-wrapper {{
        background: rgba(0, 0, 0, 0.3);
      }}
      .comp-img-wrapper img {{
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        display: block;
      }}
      .savings-pill {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 10px;
        border-radius: 9999px;
        background: var(--badge-green-bg);
        color: var(--badge-green-text);
        font-size: 11.5px;
        font-weight: 700;
        margin-top: 10px;
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
    <div id="dropzone-compress_image" class="dropzone-box" onclick="document.getElementById('file-input-compress_image').click()">
      <div class="folder-container">
        <div class="folder"><div class="front-side"><div class="tip"></div><div class="cover"></div></div><div class="back-side cover"></div></div>
        <span class="custom-file-upload">Choose Image</span>
      </div>
      <p class="drop-primary">Drop your image here, or browse</p>
      <p class="drop-secondary">Supports PNG, JPG, JPEG, WEBP • Up to 80% file size reduction with Before/After preview</p>
    </div>
    <input type="file" id="file-input-compress_image" accept=".png,.jpg,.jpeg,.webp" onchange="handleCompressImageUpload(this.files[0])">

    <!-- Active Compression Workspace -->
    <div id="compress_image-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
          </div>
          <div>
            <p id="compress_image-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">image.jpg</p>
            <p id="compress_image-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetCompressImageView()">Change File</button>
      </div>

      <!-- Compression Level Buttons -->
      <div style="margin-top:20px;">
        <label style="display:block; font-size:12.5px; font-weight:700; color:var(--ink); margin-bottom:8px;">Compression Level:</label>
        <div class="zone-pills-bar" style="justify-content:flex-start; flex-wrap:wrap; gap:10px;">
          <button type="button" class="zone-pill" id="btn-comp-60" onclick="setCompressLevel(60)">High (60% Maximum Savings)</button>
          <button type="button" class="zone-pill active" id="btn-comp-75" onclick="setCompressLevel(75)">Recommended (75% Balanced)</button>
          <button type="button" class="zone-pill" id="btn-comp-85" onclick="setCompressLevel(85)">Light (85% Maximum Quality)</button>
        </div>
      </div>

      <!-- Before / After Live Comparison -->
      <div class="comp-comparison-grid">
        <!-- Before: Original -->
        <div class="comp-card-box">
          <div class="comp-card-header">
            <span class="comp-badge-pill comp-badge-orig">BEFORE (ORIGINAL)</span>
            <span id="comp-orig-size" style="font-size:12px; font-weight:700; color:var(--ink-muted);">0 KB</span>
          </div>
          <div class="comp-img-wrapper">
            <img id="comp-img-before" alt="Original Image">
          </div>
        </div>

        <!-- After: Live Preview -->
        <div class="comp-card-box">
          <div class="comp-card-header">
            <span class="comp-badge-pill comp-badge-after">AFTER (ESTIMATED)</span>
            <span id="comp-after-size" style="font-size:12px; font-weight:700; color:var(--primary);">Estimating...</span>
          </div>
          <div class="comp-img-wrapper">
            <img id="comp-img-after" alt="Compressed Preview">
          </div>
          <div class="savings-pill" id="comp-savings-badge">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <span id="comp-savings-text">~45% Estimated Size Reduction</span>
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-compress_image" style="padding:12px 28px; font-size:14px;" onclick="executeCompressImage()">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
          Compress Image
        </button>
      </div>
    </div>

    {processing_card}

    <!-- Result Card -->
    <div id="compress_image-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Process Complete!</h3>
      <p id="compress_image-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your compressed image is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-compress_image" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-compress_image" />
            <span class="circle"><svg class="icon" viewBox="0 0 24 24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"/></svg><div class="square"></div></span>
            <p class="title">Download File</p><p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetCompressImageView()">
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
    let currentCompressImageFile = null;
    let currentCompressImageBlobUrl = '';
    let isCompressImageDlDone = false;
    let selectedQuality = 75;
    let liveEstimatedBlobUrl = '';

    const compImgBefore = document.getElementById('comp-img-before');
    const compImgAfter = document.getElementById('comp-img-after');
    const compOrigSize = document.getElementById('comp-orig-size');
    const compAfterSize = document.getElementById('comp-after-size');
    const compSavingsText = document.getElementById('comp-savings-text');

    function handleCompressImageUpload(file) {
      if (!file) return;
      currentCompressImageFile = file;
      document.getElementById('dropzone-compress_image').style.display = 'none';
      document.getElementById('compress_image-doc-name').textContent = file.name;
      const sizeKb = (file.size / 1024).toFixed(0);
      document.getElementById('compress_image-doc-size').textContent = sizeKb + ' KB • Ready';
      compOrigSize.textContent = sizeKb + ' KB';
      document.getElementById('compress_image-file-config').style.display = 'block';

      const reader = new FileReader();
      reader.onload = function(e) {
        compImgBefore.src = e.target.result;
        updateLiveCompressionPreview();
      };
      reader.readAsDataURL(file);
    }

    function setCompressLevel(lvl) {
      selectedQuality = lvl;
      ['60', '75', '85'].forEach(x => {
        const el = document.getElementById('btn-comp-' + x);
        if (el) el.classList.toggle('active', parseInt(x) === lvl);
      });
      updateLiveCompressionPreview();
    }

    function updateLiveCompressionPreview() {
      if (!currentCompressImageFile || !compImgBefore.src) return;

      const img = new Image();
      img.onload = function() {
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth || img.width;
        canvas.height = img.naturalHeight || img.height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);

        const q = selectedQuality / 100;
        const mime = currentCompressImageFile.type === 'image/png' ? 'image/webp' : 'image/jpeg';
        canvas.toBlob(function(blob) {
          if (!blob) return;
          if (liveEstimatedBlobUrl) URL.revokeObjectURL(liveEstimatedBlobUrl);
          liveEstimatedBlobUrl = URL.createObjectURL(blob);
          compImgAfter.src = liveEstimatedBlobUrl;

          const estKb = (blob.size / 1024).toFixed(0);
          compAfterSize.textContent = `${estKb} KB`;

          const origBytes = currentCompressImageFile.size;
          const diffPct = Math.max(0, Math.round(((origBytes - blob.size) / origBytes) * 100));
          compSavingsText.textContent = `~${diffPct}% Estimated Size Reduction`;
        }, mime, q);
      };
      img.src = compImgBefore.src;
    }

    function triggerCompressImageDownload() {
      if (!currentCompressImageBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentCompressImageBlobUrl;
      a.download = 'removix_compressed_' + (currentCompressImageFile ? currentCompressImageFile.name : 'image.jpg');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxCompressImage = document.getElementById('dl-checkbox-compress_image');
    const dlLabelCompressImage = document.getElementById('dl-label-compress_image');
    if (dlCheckboxCompressImage) {
      dlCheckboxCompressImage.addEventListener('change', () => {
        if (dlCheckboxCompressImage.checked) {
          if (dlLabelCompressImage) dlLabelCompressImage.classList.add('is-checked');
          triggerCompressImageDownload();
          setTimeout(() => { isCompressImageDlDone = true; }, 2350);
        }
      });
      dlCheckboxCompressImage.addEventListener('click', (e) => {
        if (isCompressImageDlDone) { e.preventDefault(); triggerCompressImageDownload(); }
      });
    }

    function resetCompressImageView() {
      currentCompressImageFile = null;
      document.getElementById('compress_image-result-card').style.display = 'none';
      document.getElementById('proc-compress-image').style.display = 'none';
      document.getElementById('compress_image-file-config').style.display = 'none';
      document.getElementById('dropzone-compress_image').style.display = '';
      const inputEl = document.getElementById('file-input-compress_image');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxCompressImage) dlCheckboxCompressImage.checked = false;
      if (dlLabelCompressImage) dlLabelCompressImage.classList.remove('is-checked');
      isCompressImageDlDone = false;
      if (currentCompressImageBlobUrl) { URL.revokeObjectURL(currentCompressImageBlobUrl); currentCompressImageBlobUrl = ''; }
      if (liveEstimatedBlobUrl) { URL.revokeObjectURL(liveEstimatedBlobUrl); liveEstimatedBlobUrl = ''; }
      compImgBefore.src = '';
      compImgAfter.src = '';
    }

    function executeCompressImage() {
      if (!currentCompressImageFile) return;
      const formData = new FormData();
      formData.append('file', currentCompressImageFile);
      formData.append('quality', selectedQuality);

      document.getElementById('compress_image-file-config').style.display = 'none';
      const procEl = document.getElementById('proc-compress-image');
      procEl.style.display = 'block';

      fetch('/api/compress-image', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Compression failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('compress_image-result-card').style.display = 'block';
        currentCompressImageBlobUrl = URL.createObjectURL(blob);
        const origSizeKb = (currentCompressImageFile.size / 1024).toFixed(0);
        const newSizeKb = (blob.size / 1024).toFixed(0);
        const savedPct = Math.max(0, Math.round(((currentCompressImageFile.size - blob.size) / currentCompressImageFile.size) * 100));
        document.getElementById('compress_image-result-sub').textContent = `Compressed from ${origSizeKb} KB to ${newSizeKb} KB (${savedPct}% reduction).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetCompressImageView();
      });
    }
    """

    return render_layout(
        title="Compress Image",
        active_tool="image-tools",
        hero_title="Compress Image",
        hero_sub="Shrink image file size by up to <strong>80% while retaining high visual fidelity</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
