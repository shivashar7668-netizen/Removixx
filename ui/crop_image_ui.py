"""
Removix UI - Crop Image View with Live Interactive Crop & Handles
"""
from ui.layout import render_layout, render_processing_component

BADGE_SVG = r"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/></svg>"""

def render_crop_image_page() -> str:
    processing_card = render_processing_component(
        component_id="proc-crop-image",
        badge_text="IMAGE CROPPING",
        badge_icon_svg=BADGE_SVG,
        title_text="Cropping Image...",
        subtitle_text="Calculating boundaries and extracting pixel region.",
        steps=['Reading image', 'Calculating bounds', 'Cropping area', 'Finalizing file'],
    )

    main_card_html = f"""
    <style>
      .crop-workspace {{
        display: grid;
        grid-template-columns: 1fr 340px;
        gap: 24px;
        margin-top: 20px;
        align-items: start;
      }}
      @media (max-width: 900px) {{
        .crop-workspace {{
          grid-template-columns: 1fr;
        }}
      }}
      .crop-editor-panel, .crop-preview-panel {{
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 18px;
        position: relative;
      }}
      .crop-panel-title {{
        font-size: 13.5px;
        font-weight: 700;
        color: var(--ink);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
      }}
      .crop-stage-container {{
        width: 100%;
        min-height: 280px;
        max-height: 480px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(0, 0, 0, 0.04);
        border-radius: 12px;
        overflow: hidden;
        position: relative;
        user-select: none;
        touch-action: none;
      }}
      body.dark-mode .crop-stage-container {{
        background: rgba(0, 0, 0, 0.35);
      }}
      .crop-stage-inner {{
        position: relative;
        display: inline-block;
        line-height: 0;
        max-width: 100%;
        max-height: 460px;
      }}
      #crop-source-img {{
        max-width: 100%;
        max-height: 460px;
        display: block;
        object-fit: contain;
        pointer-events: none;
      }}
      .crop-overlay-dim {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        pointer-events: none;
      }}
      .crop-box {{
        position: absolute;
        border: 2px solid #0284c7;
        box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.55), 0 0 10px rgba(2, 132, 199, 0.4);
        cursor: move;
        box-sizing: border-box;
        touch-action: none;
      }}
      .crop-grid-lines {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        pointer-events: none;
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr;
      }}
      .crop-grid-lines > div {{
        border: 1px dashed rgba(255, 255, 255, 0.35);
      }}
      .crop-handle {{
        position: absolute;
        width: 11px;
        height: 11px;
        background: #ffffff;
        border: 2px solid #0284c7;
        border-radius: 2px;
        box-sizing: border-box;
        z-index: 5;
        touch-action: none;
      }}
      .crop-handle.handle-tl {{ top: -6px; left: -6px; cursor: nwse-resize; }}
      .crop-handle.handle-tr {{ top: -6px; right: -6px; cursor: nesw-resize; }}
      .crop-handle.handle-bl {{ bottom: -6px; left: -6px; cursor: nesw-resize; }}
      .crop-handle.handle-br {{ bottom: -6px; right: -6px; cursor: nwse-resize; }}
      .crop-handle.handle-t  {{ top: -6px; left: calc(50% - 5px); cursor: ns-resize; }}
      .crop-handle.handle-b  {{ bottom: -6px; left: calc(50% - 5px); cursor: ns-resize; }}
      .crop-handle.handle-l  {{ left: -6px; top: calc(50% - 5px); cursor: ew-resize; }}
      .crop-handle.handle-r  {{ right: -6px; top: calc(50% - 5px); cursor: ew-resize; }}
      
      .crop-preview-box {{
        width: 100%;
        min-height: 240px;
        max-height: 280px;
        background: rgba(0, 0, 0, 0.04);
        border: 1px dashed var(--line);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        position: relative;
        margin-bottom: 16px;
      }}
      body.dark-mode .crop-preview-box {{
        background: rgba(0, 0, 0, 0.35);
      }}
      #crop-live-canvas {{
        max-width: 100%;
        max-height: 260px;
        display: block;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      }}
      .crop-dim-badge {{
        display: inline-block;
        padding: 3px 8px;
        background: var(--bg-page);
        border: 1px solid var(--line);
        border-radius: 6px;
        font-size: 11.5px;
        font-weight: 700;
        color: var(--primary);
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
    <div id="dropzone-crop_image" class="dropzone-box" onclick="document.getElementById('file-input-crop_image').click()">
      <div class="folder-container">
        <div class="folder"><div class="front-side"><div class="tip"></div><div class="cover"></div></div><div class="back-side cover"></div></div>
        <span class="custom-file-upload">Choose Image</span>
      </div>
      <p class="drop-primary">Drop your image here, or browse</p>
      <p class="drop-secondary">Crop to 1:1, 16:9, 4:3, 9:16 or interactive drag selection</p>
    </div>
    <input type="file" id="file-input-crop_image" accept=".png,.jpg,.jpeg,.webp" onchange="handleCropImageUpload(this.files[0])">

    <!-- Active Workspace -->
    <div id="crop_image-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/></svg>
          </div>
          <div>
            <p id="crop_image-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">image.jpg</p>
            <p id="crop_image-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetCropImageView()">Change File</button>
      </div>

      <!-- Ratio Control Buttons -->
      <div style="margin-top:18px;">
        <label style="display:block; font-size:12.5px; font-weight:700; color:var(--ink); margin-bottom:8px;">Crop Aspect Ratio:</label>
        <div class="zone-pills-bar" style="justify-content:flex-start; flex-wrap:wrap; gap:8px;">
          <button type="button" class="zone-pill active" id="btn-crop-11" onclick="setCropRatio('1:1')">1:1 Square</button>
          <button type="button" class="zone-pill" id="btn-crop-169" onclick="setCropRatio('16:9')">16:9 Widescreen</button>
          <button type="button" class="zone-pill" id="btn-crop-43" onclick="setCropRatio('4:3')">4:3 Standard</button>
          <button type="button" class="zone-pill" id="btn-crop-916" onclick="setCropRatio('9:16')">9:16 Portrait / Story</button>
          <button type="button" class="zone-pill" id="btn-crop-free" onclick="setCropRatio('free')">Freeform</button>
        </div>
      </div>

      <!-- Split Interactive Workspace -->
      <div class="crop-workspace">
        <!-- Left: Interactive Crop Area -->
        <div class="crop-editor-panel">
          <div class="crop-panel-title">
            <span>Crop Area Selection</span>
            <span style="font-size:11.5px; font-weight:500; color:var(--ink-muted);">Drag corners or box to resize</span>
          </div>
          <div class="crop-stage-container" id="crop-stage-wrap">
            <div class="crop-stage-inner" id="crop-stage-inner">
              <img id="crop-source-img" alt="Source Image">
              <div class="crop-box" id="crop-box">
                <div class="crop-grid-lines">
                  <div></div><div></div><div></div>
                  <div></div><div></div><div></div>
                  <div></div><div></div><div></div>
                </div>
                <div class="crop-handle handle-tl" data-handle="tl"></div>
                <div class="crop-handle handle-tr" data-handle="tr"></div>
                <div class="crop-handle handle-bl" data-handle="bl"></div>
                <div class="crop-handle handle-br" data-handle="br"></div>
                <div class="crop-handle handle-t"  data-handle="t"></div>
                <div class="crop-handle handle-b"  data-handle="b"></div>
                <div class="crop-handle handle-l"  data-handle="l"></div>
                <div class="crop-handle handle-r"  data-handle="r"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Live Result Preview & Actions -->
        <div class="crop-preview-panel">
          <div class="crop-panel-title">
            <span>Live Result Preview</span>
            <span class="crop-dim-badge" id="crop-live-dims">0 × 0 px</span>
          </div>
          <div class="crop-preview-box">
            <canvas id="crop-live-canvas"></canvas>
          </div>
          <button type="button" class="btn-primary" id="btn-start-crop_image" style="width:100%; justify-content:center; padding:12px 18px; font-size:14px;" onclick="executeCropImage()">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/></svg>
            Crop Image
          </button>
        </div>
      </div>
    </div>

    {processing_card}

    <!-- Result Card -->
    <div id="crop_image-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Process Complete!</h3>
      <p id="crop_image-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your cropped image is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-crop_image" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-crop_image" />
            <span class="circle"><svg class="icon" viewBox="0 0 24 24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"/></svg><div class="square"></div></span>
            <p class="title">Download File</p><p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetCropImageView()">
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
    let currentCropImageFile = null;
    let currentCropImageBlobUrl = '';
    let isCropImageDlDone = false;
    let selectedCropRatio = '1:1';

    // Interactive Crop State
    let cropBoxState = { x: 0, y: 0, w: 100, h: 100 };
    let isDraggingCropBox = false;
    let isResizingHandle = null;
    let dragStartPos = { x: 0, y: 0 };
    let cropInitialBox = { x: 0, y: 0, w: 0, h: 0 };

    const cropSourceImg = document.getElementById('crop-source-img');
    const cropBoxEl = document.getElementById('crop-box');
    const cropStageInner = document.getElementById('crop-stage-inner');
    const cropLiveCanvas = document.getElementById('crop-live-canvas');
    const cropLiveDims = document.getElementById('crop-live-dims');

    function handleCropImageUpload(file) {
      if (!file) return;
      currentCropImageFile = file;
      document.getElementById('dropzone-crop_image').style.display = 'none';
      document.getElementById('crop_image-doc-name').textContent = file.name;
      document.getElementById('crop_image-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('crop_image-file-config').style.display = 'block';

      const reader = new FileReader();
      reader.onload = function(e) {
        cropSourceImg.onload = function() {
          initCropBox();
        };
        cropSourceImg.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    function initCropBox() {
      const imgW = cropSourceImg.clientWidth;
      const imgH = cropSourceImg.clientHeight;
      if (!imgW || !imgH) return;

      applyRatioToBox(selectedCropRatio, imgW, imgH);
      updateCropDisplay();
    }

    function applyRatioToBox(ratio, imgW, imgH) {
      imgW = imgW || cropSourceImg.clientWidth;
      imgH = imgH || cropSourceImg.clientHeight;
      if (!imgW || !imgH) return;

      let targetW, targetH;
      if (ratio === '1:1') {
        const side = Math.min(imgW, imgH) * 0.75;
        targetW = side;
        targetH = side;
      } else if (ratio === '16:9') {
        targetW = imgW * 0.85;
        targetH = targetW * (9 / 16);
        if (targetH > imgH) {
          targetH = imgH * 0.85;
          targetW = targetH * (16 / 9);
        }
      } else if (ratio === '4:3') {
        targetW = imgW * 0.85;
        targetH = targetW * (3 / 4);
        if (targetH > imgH) {
          targetH = imgH * 0.85;
          targetW = targetH * (4 / 3);
        }
      } else if (ratio === '9:16') {
        targetH = imgH * 0.85;
        targetW = targetH * (9 / 16);
        if (targetW > imgW) {
          targetW = imgW * 0.85;
          targetH = targetW * (16 / 9);
        }
      } else {
        targetW = imgW * 0.75;
        targetH = imgH * 0.75;
      }

      cropBoxState.w = Math.max(30, Math.round(targetW));
      cropBoxState.h = Math.max(30, Math.round(targetH));
      cropBoxState.x = Math.max(0, Math.round((imgW - cropBoxState.w) / 2));
      cropBoxState.y = Math.max(0, Math.round((imgH - cropBoxState.h) / 2));
    }

    function setCropRatio(r) {
      selectedCropRatio = r;
      ['1:1', '16:9', '4:3', '9:16', 'free'].forEach(x => {
        const id = 'btn-crop-' + x.replace(':', '');
        const el = document.getElementById(id);
        if (el) el.classList.toggle('active', x === r);
      });
      applyRatioToBox(r);
      updateCropDisplay();
    }

    function updateCropDisplay() {
      const imgW = cropSourceImg.clientWidth;
      const imgH = cropSourceImg.clientHeight;
      if (!imgW || !imgH) return;

      // Constrain box
      cropBoxState.w = Math.min(cropBoxState.w, imgW);
      cropBoxState.h = Math.min(cropBoxState.h, imgH);
      cropBoxState.x = Math.max(0, Math.min(cropBoxState.x, imgW - cropBoxState.w));
      cropBoxState.y = Math.max(0, Math.min(cropBoxState.y, imgH - cropBoxState.h));

      cropBoxEl.style.left = cropBoxState.x + 'px';
      cropBoxEl.style.top = cropBoxState.y + 'px';
      cropBoxEl.style.width = cropBoxState.w + 'px';
      cropBoxEl.style.height = cropBoxState.h + 'px';

      renderLiveCropPreview();
    }

    function renderLiveCropPreview() {
      if (!cropSourceImg.naturalWidth) return;
      const scaleX = cropSourceImg.naturalWidth / cropSourceImg.clientWidth;
      const scaleY = cropSourceImg.naturalHeight / cropSourceImg.clientHeight;

      const natX = Math.round(cropBoxState.x * scaleX);
      const natY = Math.round(cropBoxState.y * scaleY);
      const natW = Math.round(cropBoxState.w * scaleX);
      const natH = Math.round(cropBoxState.h * scaleY);

      cropLiveDims.textContent = `${natW} × ${natH} px`;

      // Draw onto canvas
      const maxDim = 320;
      let drawW = natW;
      let drawH = natH;
      if (drawW > maxDim || drawH > maxDim) {
        if (drawW > drawH) {
          drawH = Math.round((drawH * maxDim) / drawW);
          drawW = maxDim;
        } else {
          drawW = Math.round((drawW * maxDim) / drawH);
          drawH = maxDim;
        }
      }

      cropLiveCanvas.width = Math.max(1, drawW);
      cropLiveCanvas.height = Math.max(1, drawH);
      const ctx = cropLiveCanvas.getContext('2d');
      ctx.imageSmoothingQuality = 'high';
      ctx.clearRect(0, 0, drawW, drawH);
      try {
        ctx.drawImage(cropSourceImg, natX, natY, natW, natH, 0, 0, drawW, drawH);
      } catch (err) {}
    }

    // Pointer Events for Dragging and Resizing
    function getEventPos(e) {
      if (e.touches && e.touches.length > 0) {
        return { x: e.touches[0].clientX, y: e.touches[0].clientY };
      }
      return { x: e.clientX, y: e.clientY };
    }

    // Handles mousedown / touchstart
    cropBoxEl.addEventListener('mousedown', startCropInteraction);
    cropBoxEl.addEventListener('touchstart', startCropInteraction, { passive: false });

    function startCropInteraction(e) {
      const handleEl = e.target.closest('.crop-handle');
      const pos = getEventPos(e);
      dragStartPos = pos;
      cropInitialBox = { ...cropBoxState };

      if (handleEl) {
        isResizingHandle = handleEl.getAttribute('data-handle');
        isDraggingCropBox = false;
      } else {
        isDraggingCropBox = true;
        isResizingHandle = null;
      }
      e.preventDefault();
      e.stopPropagation();

      window.addEventListener('mousemove', onCropPointerMove);
      window.addEventListener('touchmove', onCropPointerMove, { passive: false });
      window.addEventListener('mouseup', endCropInteraction);
      window.addEventListener('touchend', endCropInteraction);
    }

    function onCropPointerMove(e) {
      if (!isDraggingCropBox && !isResizingHandle) return;
      e.preventDefault();
      const pos = getEventPos(e);
      const dx = pos.x - dragStartPos.x;
      const dy = pos.y - dragStartPos.y;

      const imgW = cropSourceImg.clientWidth;
      const imgH = cropSourceImg.clientHeight;

      if (isDraggingCropBox) {
        cropBoxState.x = Math.max(0, Math.min(imgW - cropInitialBox.w, cropInitialBox.x + dx));
        cropBoxState.y = Math.max(0, Math.min(imgH - cropInitialBox.h, cropInitialBox.y + dy));
      } else if (isResizingHandle) {
        let newX = cropInitialBox.x;
        let newY = cropInitialBox.y;
        let newW = cropInitialBox.w;
        let newH = cropInitialBox.h;

        const h = isResizingHandle;
        if (h.includes('r')) newW = cropInitialBox.w + dx;
        if (h.includes('l')) { newW = cropInitialBox.w - dx; newX = cropInitialBox.x + dx; }
        if (h.includes('b')) newH = cropInitialBox.h + dy;
        if (h.includes('t')) { newH = cropInitialBox.h - dy; newY = cropInitialBox.y + dy; }

        // If aspect ratio is locked
        if (selectedCropRatio !== 'free') {
          let targetRatio = 1;
          if (selectedCropRatio === '16:9') targetRatio = 16 / 9;
          else if (selectedCropRatio === '4:3') targetRatio = 4 / 3;
          else if (selectedCropRatio === '9:16') targetRatio = 9 / 16;

          if (h.includes('r') || h.includes('l')) {
            newH = newW / targetRatio;
          } else {
            newW = newH * targetRatio;
          }
        }

        if (newW >= 30 && newH >= 30 && newX >= 0 && (newX + newW) <= imgW && newY >= 0 && (newY + newH) <= imgH) {
          cropBoxState.x = newX;
          cropBoxState.y = newY;
          cropBoxState.w = newW;
          cropBoxState.h = newH;
        }
      }
      updateCropDisplay();
    }

    function endCropInteraction() {
      isDraggingCropBox = false;
      isResizingHandle = null;
      window.removeEventListener('mousemove', onCropPointerMove);
      window.removeEventListener('touchmove', onCropPointerMove);
      window.removeEventListener('mouseup', endCropInteraction);
      window.removeEventListener('touchend', endCropInteraction);
    }

    window.addEventListener('resize', () => {
      if (currentCropImageFile && cropSourceImg.naturalWidth) {
        updateCropDisplay();
      }
    });

    function triggerCropImageDownload() {
      if (!currentCropImageBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentCropImageBlobUrl;
      a.download = 'removix_cropped_' + (currentCropImageFile ? currentCropImageFile.name : 'image.png');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxCropImage = document.getElementById('dl-checkbox-crop_image');
    const dlLabelCropImage = document.getElementById('dl-label-crop_image');
    if (dlCheckboxCropImage) {
      dlCheckboxCropImage.addEventListener('change', () => {
        if (dlCheckboxCropImage.checked) {
          if (dlLabelCropImage) dlLabelCropImage.classList.add('is-checked');
          triggerCropImageDownload();
          setTimeout(() => { isCropImageDlDone = true; }, 2350);
        }
      });
      dlCheckboxCropImage.addEventListener('click', (e) => {
        if (isCropImageDlDone) { e.preventDefault(); triggerCropImageDownload(); }
      });
    }

    function resetCropImageView() {
      currentCropImageFile = null;
      document.getElementById('crop_image-result-card').style.display = 'none';
      document.getElementById('proc-crop-image').style.display = 'none';
      document.getElementById('crop_image-file-config').style.display = 'none';
      document.getElementById('dropzone-crop_image').style.display = '';
      const inputEl = document.getElementById('file-input-crop_image');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxCropImage) dlCheckboxCropImage.checked = false;
      if (dlLabelCropImage) dlLabelCropImage.classList.remove('is-checked');
      isCropImageDlDone = false;
      if (currentCropImageBlobUrl) { URL.revokeObjectURL(currentCropImageBlobUrl); currentCropImageBlobUrl = ''; }
      cropSourceImg.src = '';
    }

    function executeCropImage() {
      if (!currentCropImageFile || !cropSourceImg.naturalWidth) return;

      const scaleX = cropSourceImg.naturalWidth / cropSourceImg.clientWidth;
      const scaleY = cropSourceImg.naturalHeight / cropSourceImg.clientHeight;

      const natX = Math.round(cropBoxState.x * scaleX);
      const natY = Math.round(cropBoxState.y * scaleY);
      const natW = Math.round(cropBoxState.w * scaleX);
      const natH = Math.round(cropBoxState.h * scaleY);

      const formData = new FormData();
      formData.append('file', currentCropImageFile);
      formData.append('ratio', selectedCropRatio);
      formData.append('left', natX);
      formData.append('top', natY);
      formData.append('right', natX + natW);
      formData.append('bottom', natY + natH);

      document.getElementById('crop_image-file-config').style.display = 'none';
      const procEl = document.getElementById('proc-crop-image');
      procEl.style.display = 'block';

      fetch('/api/crop-image', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Crop failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('crop_image-result-card').style.display = 'block';
        currentCropImageBlobUrl = URL.createObjectURL(blob);
        document.getElementById('crop_image-result-sub').textContent = `Cropped to ${natW} × ${natH} px (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetCropImageView();
      });
    }
    """

    return render_layout(
        title="Crop Image",
        active_tool="image-tools",
        hero_title="Crop Image",
        hero_sub="Trim photos to <strong>standard aspect ratios or custom dimensions</strong> in seconds.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
