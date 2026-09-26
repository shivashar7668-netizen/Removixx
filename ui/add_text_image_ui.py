"""
Removix UI - Add Text to Image View with Real-time Typography Overlay
"""
from ui.layout import render_layout, render_processing_component

BADGE_SVG = r"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 7V4h16v3"/><line x1="12" y1="4" x2="12" y2="20"/><line x1="8" y1="20" x2="16" y2="20"/></svg>"""

def render_add_text_image_page() -> str:
    processing_card = render_processing_component(
        component_id="proc-add-text-image",
        badge_text="IMAGE TYPOGRAPHY",
        badge_icon_svg=BADGE_SVG,
        title_text="Rendering Text...",
        subtitle_text="Calculating font layout, drop shadow, and alpha overlay.",
        steps=['Reading image', 'Positioning text', 'Rendering typography', 'Finalizing file'],
    )

    main_card_html = f"""
    <style>
      .text-preview-stage {{
        margin-top: 20px;
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        min-height: 320px;
      }}
      .text-img-container {{
        max-width: 100%;
        max-height: 420px;
        display: inline-block;
        position: relative;
        overflow: hidden;
        border-radius: 10px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
      }}
      #text-base-img {{
        max-width: 100%;
        max-height: 400px;
        display: block;
        object-fit: contain;
      }}
      #text-live-overlay {{
        position: absolute;
        pointer-events: none;
        user-select: none;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 700;
        white-space: pre-wrap;
        line-height: 1.25;
        text-shadow: 0 2px 5px rgba(0,0,0,0.65), 0 0 2px rgba(0,0,0,0.8);
        padding: 8px 12px;
        max-width: 90%;
        box-sizing: border-box;
      }}
      .text-controls-grid {{
        display: grid;
        grid-template-columns: 2fr 1fr 1fr;
        gap: 14px;
        margin-top: 14px;
      }}
      @media (max-width: 768px) {{
        .text-controls-grid {{
          grid-template-columns: 1fr;
        }}
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
    <div id="dropzone-add_text_image" class="dropzone-box" onclick="document.getElementById('file-input-add_text_image').click()">
      <div class="folder-container">
        <div class="folder"><div class="front-side"><div class="tip"></div><div class="cover"></div></div><div class="back-side cover"></div></div>
        <span class="custom-file-upload">Choose Image</span>
      </div>
      <p class="drop-primary">Drop your image here, or browse</p>
      <p class="drop-secondary">Add custom typography, watermarks, or captions with instant live preview</p>
    </div>
    <input type="file" id="file-input-add_text_image" accept=".png,.jpg,.jpeg,.webp" onchange="handleAddTextImageUpload(this.files[0])">

    <!-- Active Text Workspace -->
    <div id="add_text_image-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 7V4h16v3"/><line x1="12" y1="4" x2="12" y2="20"/><line x1="8" y1="20" x2="16" y2="20"/></svg>
          </div>
          <div>
            <p id="add_text_image-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">image.jpg</p>
            <p id="add_text_image-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetAddTextImageView()">Change File</button>
      </div>

      <!-- Controls Form -->
      <div style="margin-top:18px;">
        <label style="display:block; font-size:12.5px; font-weight:700; color:var(--ink); margin-bottom:6px;">Text Caption:</label>
        <input type="text" id="text-input-val" value="Removix Preview" placeholder="Type your text or watermark here..." style="width:100%; box-sizing:border-box; padding:10px 14px; border:1px solid var(--line); border-radius:10px; font-size:14px; outline:none; background:var(--bg-page); color:var(--ink);" oninput="updateLiveTextOverlay()">
      </div>

      <div class="text-controls-grid">
        <!-- 7 Position Options -->
        <div>
          <label style="display:block; font-size:12px; font-weight:700; color:var(--ink); margin-bottom:6px;">Position (7 Options):</label>
          <select id="text-placement" style="width:100%; padding:9px 12px; border:1px solid var(--line); border-radius:8px; font-size:13px; background:var(--bg-page); color:var(--ink); outline:none;" onchange="updateLiveTextOverlay()">
            <option value="bottom_center" selected>Bottom Center (Default)</option>
            <option value="top_left">Top Left</option>
            <option value="top_center">Top Center</option>
            <option value="top_right">Top Right</option>
            <option value="center">Center</option>
            <option value="bottom_left">Bottom Left</option>
            <option value="bottom_right">Bottom Right</option>
          </select>
        </div>

        <!-- Font Size -->
        <div>
          <label style="display:flex; justify-content:space-between; font-size:12px; font-weight:700; color:var(--ink); margin-bottom:6px;">
            <span>Font Size:</span>
            <span id="text-font-size-label" style="color:var(--primary);">36px</span>
          </label>
          <input type="range" id="text-font-size" min="14" max="96" value="36" style="width:100%; height:34px; cursor:pointer;" oninput="updateLiveTextOverlay()">
        </div>

        <!-- Color Picker -->
        <div>
          <label style="display:block; font-size:12px; font-weight:700; color:var(--ink); margin-bottom:6px;">Text Color:</label>
          <div style="display:flex; align-items:center; gap:8px;">
            <input type="color" id="text-color" value="#ffffff" style="width:42px; height:34px; padding:0; border:1px solid var(--line); border-radius:8px; cursor:pointer; background:none;" oninput="updateLiveTextOverlay()">
            <input type="text" id="text-color-hex" value="#FFFFFF" style="width:70px; padding:6px 8px; border:1px solid var(--line); border-radius:8px; font-size:12px; text-transform:uppercase; background:var(--bg-page); color:var(--ink);" oninput="onHexColorInput(this.value)">
          </div>
        </div>
      </div>

      <!-- Live Preview Canvas Stage -->
      <div class="text-preview-stage">
        <div style="font-size:11.5px; font-weight:700; color:var(--ink-muted); margin-bottom:10px; align-self:flex-start;">
          LIVE PREVIEW (REAL-TIME OVERLAY)
        </div>
        <div class="text-img-container" id="text-img-container">
          <img id="text-base-img" alt="Base Image">
          <div id="text-live-overlay">Removix Preview</div>
        </div>
      </div>

      <!-- Action Button -->
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-add_text_image" style="padding:12px 28px; font-size:14px;" onclick="executeAddTextImage()">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 7V4h16v3"/><line x1="12" y1="4" x2="12" y2="20"/><line x1="8" y1="20" x2="16" y2="20"/></svg>
          Add Text to Image
        </button>
      </div>
    </div>

    {processing_card}

    <!-- Result Card -->
    <div id="add_text_image-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Process Complete!</h3>
      <p id="add_text_image-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your image with custom typography is ready.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-add_text_image" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-add_text_image" />
            <span class="circle"><svg class="icon" viewBox="0 0 24 24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"/></svg><div class="square"></div></span>
            <p class="title">Download File</p><p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetAddTextImageView()">
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
    let currentAddTextImageFile = null;
    let currentAddTextImageBlobUrl = '';
    let isAddTextImageDlDone = false;

    const textBaseImg = document.getElementById('text-base-img');
    const textLiveOverlay = document.getElementById('text-live-overlay');
    const textInputVal = document.getElementById('text-input-val');
    const textPlacement = document.getElementById('text-placement');
    const textFontSize = document.getElementById('text-font-size');
    const textFontSizeLabel = document.getElementById('text-font-size-label');
    const textColor = document.getElementById('text-color');
    const textColorHex = document.getElementById('text-color-hex');

    function handleAddTextImageUpload(file) {
      if (!file) return;
      currentAddTextImageFile = file;
      document.getElementById('dropzone-add_text_image').style.display = 'none';
      document.getElementById('add_text_image-doc-name').textContent = file.name;
      document.getElementById('add_text_image-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('add_text_image-file-config').style.display = 'block';

      const reader = new FileReader();
      reader.onload = function(e) {
        textBaseImg.onload = function() {
          updateLiveTextOverlay();
        };
        textBaseImg.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    function onHexColorInput(hex) {
      if (/^#[0-9A-Fa-f]{6}$/.test(hex)) {
        textColor.value = hex;
        updateLiveTextOverlay();
      }
    }

    function updateLiveTextOverlay() {
      const val = textInputVal.value;
      textLiveOverlay.textContent = val;
      const size = parseInt(textFontSize.value) || 36;
      textFontSizeLabel.textContent = size + 'px';
      
      const col = textColor.value;
      textColorHex.value = col.toUpperCase();
      textLiveOverlay.style.color = col;

      // Responsive preview font size scaled to displayed image size
      const scale = textBaseImg.clientWidth && textBaseImg.naturalWidth ? (textBaseImg.clientWidth / textBaseImg.naturalWidth) : 1;
      const previewPx = Math.max(12, Math.round(size * Math.max(0.4, scale)));
      textLiveOverlay.style.fontSize = previewPx + 'px';

      // Reset positions
      textLiveOverlay.style.top = '';
      textLiveOverlay.style.bottom = '';
      textLiveOverlay.style.left = '';
      textLiveOverlay.style.right = '';
      textLiveOverlay.style.transform = '';
      textLiveOverlay.style.textAlign = 'left';

      const pos = textPlacement.value;
      if (pos === 'top_left') {
        textLiveOverlay.style.top = '12px';
        textLiveOverlay.style.left = '14px';
      } else if (pos === 'top_center') {
        textLiveOverlay.style.top = '12px';
        textLiveOverlay.style.left = '50%';
        textLiveOverlay.style.transform = 'translateX(-50%)';
        textLiveOverlay.style.textAlign = 'center';
      } else if (pos === 'top_right') {
        textLiveOverlay.style.top = '12px';
        textLiveOverlay.style.right = '14px';
        textLiveOverlay.style.textAlign = 'right';
      } else if (pos === 'center') {
        textLiveOverlay.style.top = '50%';
        textLiveOverlay.style.left = '50%';
        textLiveOverlay.style.transform = 'translate(-50%, -50%)';
        textLiveOverlay.style.textAlign = 'center';
      } else if (pos === 'bottom_left') {
        textLiveOverlay.style.bottom = '12px';
        textLiveOverlay.style.left = '14px';
      } else if (pos === 'bottom_right') {
        textLiveOverlay.style.bottom = '12px';
        textLiveOverlay.style.right = '14px';
        textLiveOverlay.style.textAlign = 'right';
      } else { // bottom_center (default)
        textLiveOverlay.style.bottom = '12px';
        textLiveOverlay.style.left = '50%';
        textLiveOverlay.style.transform = 'translateX(-50%)';
        textLiveOverlay.style.textAlign = 'center';
      }
    }

    function triggerAddTextImageDownload() {
      if (!currentAddTextImageBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentAddTextImageBlobUrl;
      a.download = 'removix_text_' + (currentAddTextImageFile ? currentAddTextImageFile.name : 'image.png');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxAddTextImage = document.getElementById('dl-checkbox-add_text_image');
    const dlLabelAddTextImage = document.getElementById('dl-label-add_text_image');
    if (dlCheckboxAddTextImage) {
      dlCheckboxAddTextImage.addEventListener('change', () => {
        if (dlCheckboxAddTextImage.checked) {
          if (dlLabelAddTextImage) dlLabelAddTextImage.classList.add('is-checked');
          triggerAddTextImageDownload();
          setTimeout(() => { isAddTextImageDlDone = true; }, 2350);
        }
      });
      dlCheckboxAddTextImage.addEventListener('click', (e) => {
        if (isAddTextImageDlDone) { e.preventDefault(); triggerAddTextImageDownload(); }
      });
    }

    function resetAddTextImageView() {
      currentAddTextImageFile = null;
      document.getElementById('add_text_image-result-card').style.display = 'none';
      document.getElementById('proc-add-text-image').style.display = 'none';
      document.getElementById('add_text_image-file-config').style.display = 'none';
      document.getElementById('dropzone-add_text_image').style.display = '';
      const inputEl = document.getElementById('file-input-add_text_image');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxAddTextImage) dlCheckboxAddTextImage.checked = false;
      if (dlLabelAddTextImage) dlLabelAddTextImage.classList.remove('is-checked');
      isAddTextImageDlDone = false;
      if (currentAddTextImageBlobUrl) { URL.revokeObjectURL(currentAddTextImageBlobUrl); currentAddTextImageBlobUrl = ''; }
      textBaseImg.src = '';
    }

    function executeAddTextImage() {
      if (!currentAddTextImageFile) return;
      const textVal = textInputVal.value.trim();
      if (!textVal) {
        alert('Please enter a caption or watermark text.');
        return;
      }

      const formData = new FormData();
      formData.append('file', currentAddTextImageFile);
      formData.append('text', textVal);
      formData.append('placement', textPlacement.value);
      formData.append('font_size', textFontSize.value);
      formData.append('color', textColor.value);

      document.getElementById('add_text_image-file-config').style.display = 'none';
      const procEl = document.getElementById('proc-add-text-image');
      procEl.style.display = 'block';

      fetch('/api/add-text-image', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Text rendering failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('add_text_image-result-card').style.display = 'block';
        currentAddTextImageBlobUrl = URL.createObjectURL(blob);
        document.getElementById('add_text_image-result-sub').textContent = `Typography added successfully (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetAddTextImageView();
      });
    }
    """

    return render_layout(
        title="Add Text to Image",
        active_tool="image-tools",
        hero_title="Add Text to Image",
        hero_sub="Overlay custom <strong>captions, typography, or watermarks</strong> in seconds.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
