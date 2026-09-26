"""
Removix UI - PDF Tools Views with Live Previews & Drag-to-Reorder
-----------------------------------------------------------------
1. Image to PDF View (Multi-image thumbnails, drag-to-reorder, merge to PDF)
2. PDF to Image View (Left thumbnail strip, large viewer, format PNG/JPG, ZIP download)
"""

from ui.layout import render_layout, render_processing_component

PDF_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>"""


def render_image_to_pdf_page() -> str:
    """Renders the Image to PDF converter view with thumbnail drag-to-reorder."""
    processing_card = render_processing_component(
        component_id="i2p-proc",
        badge_text="PDF CONVERTER",
        badge_icon_svg=PDF_BADGE_SVG,
        title_text="Generating PDF Document...",
        subtitle_text="Combining pages with original resolution and crystal clarity.",
        steps=[
            "Reading images",
            "Arranging pages",
            "Generating PDF",
            "Finalizing file",
        ],
    )

    main_card_html = f"""
    <style>
      .i2p-grid-tray {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 16px;
        margin-top: 14px;
        max-height: 480px;
        overflow-y: auto;
        padding: 4px;
      }}
      .i2p-card-item {{
        background: var(--bg-card);
        border: 2px solid var(--line);
        border-radius: 12px;
        padding: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        cursor: grab;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        user-select: none;
      }}
      .i2p-card-item:active {{
        cursor: grabbing;
      }}
      .i2p-card-item.dragging {{
        opacity: 0.4;
        transform: scale(0.95);
      }}
      .i2p-card-item.drag-over {{
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.3);
      }}
      .i2p-order-badge {{
        position: absolute;
        top: 8px;
        left: 8px;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: var(--primary);
        color: #ffffff;
        font-size: 11px;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 5;
      }}
      .btn-i2p-remove {{
        position: absolute;
        top: 8px;
        right: 8px;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: rgba(239, 68, 68, 0.12);
        color: #ef4444;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 800;
        z-index: 5;
        transition: all 0.15s ease;
      }}
      .btn-i2p-remove:hover {{
        background: #ef4444;
        color: #ffffff;
      }}
      .i2p-thumb-wrap {{
        width: 100%;
        height: 140px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border-radius: 6px;
        background: rgba(0, 0, 0, 0.03);
        margin-top: 14px;
      }}
      body.dark-mode .i2p-thumb-wrap {{
        background: rgba(0, 0, 0, 0.3);
      }}
      .i2p-thumb-wrap img {{
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
      }}
      .i2p-doc-info {{
        width: 100%;
        margin-top: 8px;
        text-align: center;
      }}
      .i2p-doc-name {{
        font-size: 12px;
        font-weight: 700;
        color: var(--ink);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: block;
      }}
      .i2p-card-arrows {{
        display: flex;
        gap: 6px;
        margin-top: 8px;
        width: 100%;
        justify-content: center;
      }}
      .btn-nudge {{
        padding: 2px 8px;
        font-size: 11px;
        border: 1px solid var(--line);
        border-radius: 4px;
        background: var(--bg-page);
        color: var(--ink);
        cursor: pointer;
      }}
      .btn-nudge:hover {{
        border-color: var(--primary);
        color: var(--primary);
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
    <div id="dropzone-i2p" class="dropzone-box" onclick="document.getElementById('file-input-pdf').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose Images</span>
      </div>
      <p class="drop-primary">Drop images here to combine into PDF, or browse</p>
      <p class="drop-secondary">Supports PNG, JPG, JPEG, WEBP • Drag thumbnails to rearrange order</p>
    </div>
    <input type="file" id="file-input-pdf" multiple accept=".png,.jpg,.jpeg,.webp" onchange="handleImageSelection(this.files)">

    <!-- Selected Images Reorder Tray -->
    <div id="images-tray" style="display:none; margin-top:24px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding-bottom:12px; border-bottom:1px solid var(--line);">
        <h3 style="font-size:15px; font-weight:700; color:var(--ink);">
          Selected Images (<span id="img-count" style="color:var(--primary);">0</span>)
          <span style="font-size:12px; font-weight:500; color:var(--ink-muted); margin-left:8px;">Drag thumbnails to change page sequence</span>
        </h3>
        <div style="display:flex; gap:8px;">
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="document.getElementById('file-input-pdf').click()">+ Add More</button>
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px; color:#dc2626;" onclick="clearImages()">Clear All</button>
        </div>
      </div>
      
      <div class="i2p-grid-tray" id="images-list"></div>
      
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-convert-pdf" style="padding:12px 28px; font-size:14px;" onclick="startImageToPdfConversion()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
          <span id="btn-convert-text">Convert & Merge to PDF</span>
        </button>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card -->
    <div id="pdf-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">PDF Ready for Download!</h3>
      <p id="pdf-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">All images combined with original resolution and crystal clarity.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-pdf" style="width: 195px;">
            <input type="checkbox" class="input" id="dl-checkbox-pdf" />
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
        <button type="button" class="btn-reset" onclick="resetPdfView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Create Another PDF
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Visual Reordering</h3>
          <p>Drag and drop image thumbnail cards to arrange the exact page sequence you want.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Lossless DPI Quality</h3>
          <p>Images are preserved at full camera resolution with zero downscaling artifacts.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>100% Private</h3>
          <p>Images compile straight into PDF on your local system with zero third-party cloud uploads.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let selectedImageFiles = [];
    let i2pDragSourceIdx = null;

    function handleImageSelection(files) {
      if (!files || files.length === 0) return;
      for (let i = 0; i < files.length; i++) {
        if (files[i].type.startsWith('image/')) {
          selectedImageFiles.push(files[i]);
        }
      }
      renderImageTray();
    }

    function renderImageTray() {
      const tray = document.getElementById('images-tray');
      const list = document.getElementById('images-list');
      const countEl = document.getElementById('img-count');
      const dropzone = document.getElementById('dropzone-i2p');

      if (selectedImageFiles.length === 0) {
        tray.style.display = 'none';
        dropzone.style.display = '';
        return;
      }

      dropzone.style.display = 'none';
      tray.style.display = 'block';
      countEl.textContent = selectedImageFiles.length;
      list.innerHTML = '';

      selectedImageFiles.forEach((file, idx) => {
        const item = document.createElement('div');
        item.className = 'i2p-card-item';
        item.draggable = true;
        item.dataset.index = idx;

        // Drag handlers
        item.addEventListener('dragstart', (e) => {
          i2pDragSourceIdx = idx;
          item.classList.add('dragging');
          e.dataTransfer.effectAllowed = 'move';
        });
        item.addEventListener('dragend', () => {
          item.classList.remove('dragging');
          document.querySelectorAll('.i2p-card-item').forEach(el => el.classList.remove('drag-over'));
        });
        item.addEventListener('dragover', (e) => {
          e.preventDefault();
          e.dataTransfer.dropEffect = 'move';
          item.classList.add('drag-over');
        });
        item.addEventListener('dragleave', () => {
          item.classList.remove('drag-over');
        });
        item.addEventListener('drop', (e) => {
          e.preventDefault();
          item.classList.remove('drag-over');
          if (i2pDragSourceIdx !== null && i2pDragSourceIdx !== idx) {
            const moved = selectedImageFiles.splice(i2pDragSourceIdx, 1)[0];
            selectedImageFiles.splice(idx, 0, moved);
            renderImageTray();
          }
        });

        const badge = document.createElement('div');
        badge.className = 'i2p-order-badge';
        badge.textContent = idx + 1;

        const rmBtn = document.createElement('button');
        rmBtn.type = 'button';
        rmBtn.className = 'btn-i2p-remove';
        rmBtn.innerHTML = '✕';
        rmBtn.title = 'Remove Image';
        rmBtn.onclick = (e) => { e.stopPropagation(); removeImage(idx); };

        const thumbWrap = document.createElement('div');
        thumbWrap.className = 'i2p-thumb-wrap';
        const img = document.createElement('img');
        const reader = new FileReader();
        reader.onload = (e) => { img.src = e.target.result; };
        reader.readAsDataURL(file);
        thumbWrap.appendChild(img);

        const info = document.createElement('div');
        info.className = 'i2p-doc-info';
        const nameSpan = document.createElement('span');
        nameSpan.className = 'i2p-doc-name';
        nameSpan.textContent = file.name;
        nameSpan.title = file.name;
        info.appendChild(nameSpan);

        const arrows = document.createElement('div');
        arrows.className = 'i2p-card-arrows';
        if (idx > 0) {
          const lBtn = document.createElement('button');
          lBtn.type = 'button';
          lBtn.className = 'btn-nudge';
          lBtn.innerHTML = '←';
          lBtn.onclick = (e) => { e.stopPropagation(); moveImage(idx, -1); };
          arrows.appendChild(lBtn);
        }
        if (idx < selectedImageFiles.length - 1) {
          const rBtn = document.createElement('button');
          rBtn.type = 'button';
          rBtn.className = 'btn-nudge';
          rBtn.innerHTML = '→';
          rBtn.onclick = (e) => { e.stopPropagation(); moveImage(idx, 1); };
          arrows.appendChild(rBtn);
        }

        item.appendChild(badge);
        item.appendChild(rmBtn);
        item.appendChild(thumbWrap);
        item.appendChild(info);
        item.appendChild(arrows);
        list.appendChild(item);
      });
    }

    function moveImage(idx, delta) {
      const target = idx + delta;
      if (target < 0 || target >= selectedImageFiles.length) return;
      const tmp = selectedImageFiles[idx];
      selectedImageFiles[idx] = selectedImageFiles[target];
      selectedImageFiles[target] = tmp;
      renderImageTray();
    }

    function removeImage(idx) {
      selectedImageFiles.splice(idx, 1);
      renderImageTray();
    }

    function clearImages() {
      selectedImageFiles = [];
      renderImageTray();
    }

    let currentPdfBlobUrl = '';
    let isPdfDownloadComplete = false;

    function triggerPdfDownload() {
      if (!currentPdfBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentPdfBlobUrl;
      a.download = 'removix_document.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxPdf = document.getElementById('dl-checkbox-pdf');
    const dlLabelPdf = document.getElementById('dl-label-pdf');
    if (dlCheckboxPdf) {
      dlCheckboxPdf.addEventListener('change', () => {
        if (dlCheckboxPdf.checked) {
          if (dlLabelPdf) dlLabelPdf.classList.add('is-checked');
          triggerPdfDownload();
          setTimeout(() => { isPdfDownloadComplete = true; }, 2350);
        }
      });
      dlCheckboxPdf.addEventListener('click', (e) => {
        if (isPdfDownloadComplete) { e.preventDefault(); triggerPdfDownload(); }
      });
    }

    function resetPdfView() {
      clearImages();
      document.getElementById('pdf-result-card').style.display = 'none';
      document.getElementById('i2p-proc').style.display = 'none';
      document.getElementById('dropzone-i2p').style.display = '';
      if (dlCheckboxPdf) dlCheckboxPdf.checked = false;
      if (dlLabelPdf) dlLabelPdf.classList.remove('is-checked');
      isPdfDownloadComplete = false;
      if (currentPdfBlobUrl) { URL.revokeObjectURL(currentPdfBlobUrl); currentPdfBlobUrl = ''; }
    }

    function startImageToPdfConversion() {
      if (selectedImageFiles.length === 0) {
        alert('Please select at least one image.');
        return;
      }
      
      const formData = new FormData();
      selectedImageFiles.forEach(f => formData.append('images', f));

      document.getElementById('images-tray').style.display = 'none';
      const procEl = document.getElementById('i2p-proc');
      procEl.style.display = 'block';

      fetch('/api/image-to-pdf', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'PDF generation failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('pdf-result-card').style.display = 'block';
        currentPdfBlobUrl = URL.createObjectURL(blob);
        document.getElementById('pdf-result-sub').textContent = `Combined ${selectedImageFiles.length} images into multi-page PDF (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetPdfView();
      });
    }
    """

    return render_layout(
        title="Image to PDF Converter",
        active_tool="image-to-pdf",
        hero_title="Image to PDF Converter",
        hero_sub="Combine photos into a high-quality PDF with <strong>interactive drag-to-reorder thumbnails</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )


def render_pdf_to_image_page() -> str:
    """Renders the PDF to Image extractor view with live thumbnail preview and page selection."""
    processing_card = render_processing_component(
        component_id="p2i-proc",
        badge_text="PDF CONVERTER",
        badge_icon_svg=PDF_BADGE_SVG,
        title_text="Extracting High-Res Images...",
        subtitle_text="Rendering vector pages at crisp 300 DPI print quality.",
        steps=[
            "Reading PDF",
            "Rendering pages",
            "Exporting images",
            "Packaging ZIP",
        ],
    )

    main_card_html = f"""
    <style>
      .pdf-preview-layout {{
        display: grid;
        grid-template-columns: 240px 1fr;
        gap: 20px;
        margin-top: 20px;
        align-items: stretch;
        min-height: 480px;
      }}
      @media (max-width: 800px) {{
        .pdf-preview-layout {{
          grid-template-columns: 1fr;
        }}
      }}
      .pdf-thumb-strip {{
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 14px;
        max-height: 520px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 14px;
      }}
      .pdf-thumb-card {{
        background: var(--bg-page);
        border: 2px solid var(--line);
        border-radius: 10px;
        padding: 8px;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        transition: all 0.15s ease;
        position: relative;
        overflow: hidden;
      }}
      .pdf-thumb-card:hover {{
        border-color: var(--primary);
      }}
      .pdf-thumb-card.active {{
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.25);
      }}
      .pdf-thumb-card.selected-page {{
        border-color: var(--primary);
        background: rgba(2, 132, 199, 0.05);
      }}
      .thumb-checkbox {{
        position: absolute;
        top: 8px;
        left: 8px;
        width: 18px;
        height: 18px;
        accent-color: var(--primary);
        cursor: pointer;
        z-index: 5;
      }}
      .pdf-thumb-canvas-wrap {{
        width: 100%;
        height: 140px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border-radius: 6px;
        background: #ffffff;
      }}
      body.dark-mode .pdf-thumb-canvas-wrap {{
        background: #1e293b;
      }}
      .pdf-thumb-canvas-wrap canvas {{
        max-width: 100%;
        max-height: 100%;
      }}
      .pdf-thumb-badge {{
        font-size: 11px;
        font-weight: 700;
        color: var(--ink-muted);
        margin-top: 6px;
      }}

      /* Large Viewer */
      .pdf-main-viewer {{
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
      }}
      .pdf-viewer-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--line);
        margin-bottom: 14px;
      }}
      .pdf-viewer-canvas-stage {{
        height: 480px;
        min-height: 480px;
        max-height: 480px;
        width: 100%;
        background: rgba(0, 0, 0, 0.04);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden !important;
        position: relative;
        padding: 0;
        user-select: none;
        -webkit-user-select: none;
        touch-action: none;
      }}
      body.dark-mode .pdf-viewer-canvas-stage {{
        background: rgba(0, 0, 0, 0.35);
      }}
      .pdf-canvas-pan-wrap {{
        display: flex;
        align-items: center;
        justify-content: center;
        transform-origin: center center;
        will-change: transform;
        transition: transform 0.1s ease-out;
        pointer-events: auto;
      }}
      .pdf-canvas-pan-wrap.is-dragging {{
        transition: none !important;
      }}
      #p2i-large-canvas {{
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        border-radius: 4px;
        display: block;
        transform-origin: center center;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        pointer-events: none;
      }}
      @media (max-width: 768px) {{
        .pdf-viewer-canvas-stage {{
          height: 380px;
          min-height: 380px;
          max-height: 380px;
        }}
      }}
      .btn-rot-mini {{
        padding: 4px 10px;
        font-size: 11.5px;
        font-weight: 700;
        border: 1px solid var(--line);
        border-radius: 6px;
        background: var(--bg-card);
        color: var(--ink);
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 4px;
      }}
      .btn-rot-mini:hover {{
        background: var(--line-subtle);
        border-color: var(--primary);
        color: var(--primary);
      }}
    </style>
    
    <!-- Back to PDF Tools Link -->
    <div style="margin-bottom: 20px;">
      <a href="/pdf-tools" class="btn-secondary" style="display:inline-flex; align-items:center; gap:8px; padding:8px 18px; font-size:13px; text-decoration:none; font-weight:600;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        Back to PDF Tools
      </a>
    </div>

    <!-- Output Format: PNG / JPG -->
    <div class="zone-pills-bar" id="pdf-format-pills" style="margin-bottom:18px;">
      <span class="zone-label">Output Format:</span>
      <button type="button" class="zone-pill active" id="btn-fmt-png" onclick="setPdfOutputFmt('PNG')">PNG (Ultra HD 300 DPI)</button>
      <button type="button" class="zone-pill" id="btn-fmt-jpg" onclick="setPdfOutputFmt('JPG')">JPG (Ultra HD 300 DPI)</button>
    </div>

    <!-- Dropzone View -->
    <div id="dropzone-p2i" class="dropzone-box" onclick="document.getElementById('file-input-p2i').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose PDF File</span>
      </div>
      <p class="drop-primary">Drop your PDF document here, or browse</p>
      <p class="drop-secondary">Extract pages into high-resolution PNG or JPG with live preview</p>
    </div>
    <input type="file" id="file-input-p2i" accept=".pdf,application/pdf" onchange="handlePdfUpload(this.files[0])">

    <!-- Active PDF to Image Workspace -->
    <div id="p2i-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:40px; height:40px; border-radius:10px; background:#fee2e2; color:#dc2626; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          </div>
          <div>
            <p id="p2i-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">Document.pdf</p>
            <p id="p2i-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <div style="display:flex; gap:8px;">
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="selectAllP2iPages(true)">Select All</button>
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="selectAllP2iPages(false)">Clear</button>
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetP2iView()">Change File</button>
        </div>
      </div>

      <!-- Counter bar -->
      <div style="margin-top:14px; display:flex; align-items:center; justify-content:space-between;">
        <span id="p2i-selected-count" style="font-size:12px; font-weight:700; color:var(--primary); background:var(--sky-light); padding:4px 10px; border-radius:9999px;">0 pages selected</span>
      </div>

      <!-- PDF Preview Component: Left Thumbnails + Right Large Viewer -->
      <div class="pdf-preview-layout">
        <!-- Left: Thumbnail Strip -->
        <div class="pdf-thumb-strip" id="p2i-thumb-strip">
          <!-- Thumbnails rendered dynamically -->
        </div>

        <!-- Right: Large Viewer -->
        <div class="pdf-main-viewer">
          <div class="pdf-viewer-bar">
            <div>
              <span id="p2i-page-indicator" style="font-size:13px; font-weight:700; color:var(--ink);">Page 1 of 1</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <button type="button" id="btn-toggle-p2i-curr" class="btn-rot-mini" onclick="toggleCurrentP2iSelect()">
                Toggle Select
              </button>
              <div style="width:1px; height:18px; background:var(--line); margin:0 4px;"></div>
              <button type="button" class="btn-rot-mini" onclick="zoomP2i(-0.25)">−</button>
              <span id="p2i-zoom-label" style="font-size:11.5px; font-weight:700; color:var(--ink-muted); min-width:38px; text-align:center;">100%</span>
              <button type="button" class="btn-rot-mini" onclick="zoomP2i(0.25)">+</button>
            </div>
          </div>
          <div class="pdf-viewer-canvas-stage" id="p2i-viewer-canvas-stage" title="Double click to reset zoom">
            <div class="pdf-canvas-pan-wrap" id="p2i-canvas-pan-wrap">
              <canvas id="p2i-large-canvas"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-p2i" style="padding:12px 28px; font-size:14px;" onclick="executePdfExtraction()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="14" height="14" rx="2"/><path d="M7 21h12a2 2 0 0 0 2-2V7"/><circle cx="8" cy="8" r="1" fill="currentColor"/><path d="M17 13l-3.5-3.5L7 16"/></svg>
          Convert to Images (ZIP)
        </button>
      </div>
    </div>

    <!-- Dedicated Processing View -->
    {processing_card}

    <!-- Result View -->
    <div id="p2i-result" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Extraction Complete!</h3>
      <p id="p2i-summary-msg" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">All selected pages rendered at crisp 300 DPI print quality.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-p2i" style="width: 230px;">
            <input type="checkbox" class="input" id="dl-checkbox-p2i" />
            <span class="circle">
              <svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"></path>
              </svg>
              <div class="square"></div>
            </span>
            <p class="title" id="p2i-dl-text">Download Images (ZIP)</p>
            <p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetP2iView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Convert Another PDF
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Ultra HD 300 DPI</h3>
          <p>Vector rendering engine renders text, diagrams, and photos in razor-sharp print quality.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polyline points="21 8 21 21 3 21 3 8"/><rect x="1" y="3" width="22" height="5"/><line x1="10" y1="12" x2="14" y2="12"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>1-Click ZIP Package</h3>
          <p>Multi-page PDFs are automatically structured into an easy-to-extract ZIP archive.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Total Privacy</h3>
          <p>Documents never touch third-party servers. All page rasterization happens right on your device.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let selectedPdfFmt = 'PNG';
    let currentPdfFile = null;
    let p2iDoc = null;
    let totalP2iPages = 0;
    let activeP2iPage = 1;
    let selectedP2iPages = new Set();
    let p2iZoom = 1.0;
    let currentP2iBlobUrl = '';
    let isP2iDownloadComplete = false;
    let p2iRenderTask = null;

    let p2iPanX = 0, p2iPanY = 0;
    let isP2iDragging = false, p2iDragStartX = 0, p2iDragStartY = 0;
    let p2iTouchStartX = 0, p2iTouchStartY = 0;
    let p2iInitialPinchDist = 0, p2iPinchStartZoom = 1.0;
    let isP2iTouching = false;

    const p2iThumbStrip = document.getElementById('p2i-thumb-strip');
    const p2iPageIndicator = document.getElementById('p2i-page-indicator');
    const p2iZoomLabel = document.getElementById('p2i-zoom-label');
    const p2iLargeCanvas = document.getElementById('p2i-large-canvas');
    const p2iStage = document.getElementById('p2i-viewer-canvas-stage');
    const p2iPanWrap = document.getElementById('p2i-canvas-pan-wrap');
    const p2iSelectedCount = document.getElementById('p2i-selected-count');
    const btnToggleP2iCurr = document.getElementById('btn-toggle-p2i-curr');

    function setPdfOutputFmt(fmt) {
      selectedPdfFmt = fmt;
      document.getElementById('btn-fmt-png').classList.toggle('active', fmt === 'PNG');
      document.getElementById('btn-fmt-jpg').classList.toggle('active', fmt === 'JPG');
    }

    function handlePdfUpload(file) {
      if (!file) return;
      if (!file.name.toLowerCase().endsWith('.pdf')) {
        alert('Please choose a valid PDF file.');
        return;
      }
      currentPdfFile = file;
      document.getElementById('dropzone-p2i').style.display = 'none';
      document.getElementById('p2i-doc-name').textContent = file.name;
      document.getElementById('p2i-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('p2i-file-config').style.display = 'block';

      loadPdfForP2i(file);
    }

    function loadPdfForP2i(file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const typedArray = new Uint8Array(e.target.result);
        if (window.pdfjsLib) {
          pdfjsLib.getDocument({ data: typedArray }).promise.then(function(doc) {
            p2iDoc = doc;
            totalP2iPages = doc.numPages;
            selectedP2iPages.clear();
            for (let i = 1; i <= totalP2iPages; i++) selectedP2iPages.add(i);
            renderP2iThumbnails();
            showP2iLargePage(1);
            updateP2iSelectedUI();
          }).catch(function(err) {
            alert('This file could not be opened. Please try another PDF file.');
            resetP2iView();
          });
        }
      };
      reader.readAsArrayBuffer(file);
    }

    function renderP2iThumbnails() {
      p2iThumbStrip.innerHTML = '';
      for (let p = 1; p <= totalP2iPages; p++) {
        (function(pageNum) {
          const card = document.createElement('div');
          card.className = 'pdf-thumb-card' + (pageNum === activeP2iPage ? ' active' : '') + (selectedP2iPages.has(pageNum) ? ' selected-page' : '');
          card.id = 'p2i-card-' + pageNum;
          card.onclick = function(e) {
            if (e.target.classList.contains('thumb-checkbox')) return;
            showP2iLargePage(pageNum);
          };

          const chk = document.createElement('input');
          chk.type = 'checkbox';
          chk.className = 'thumb-checkbox';
          chk.checked = selectedP2iPages.has(pageNum);
          chk.onclick = function(e) {
            e.stopPropagation();
            toggleP2iPageSelect(pageNum, chk.checked);
          };

          const canvasWrap = document.createElement('div');
          canvasWrap.className = 'pdf-thumb-canvas-wrap';

          const canvas = document.createElement('canvas');
          canvasWrap.appendChild(canvas);

          const badge = document.createElement('div');
          badge.className = 'pdf-thumb-badge';
          badge.textContent = `Page ${pageNum}`;

          card.appendChild(chk);
          card.appendChild(canvasWrap);
          card.appendChild(badge);
          p2iThumbStrip.appendChild(card);

          p2iDoc.getPage(pageNum).then(function(page) {
            const viewport = page.getViewport({ scale: 0.25 });
            canvas.width = viewport.width;
            canvas.height = viewport.height;
            const ctx = canvas.getContext('2d');
            page.render({ canvasContext: ctx, viewport: viewport });
          });
        })(p);
      }
    }

    function toggleP2iPageSelect(pageNum, isSel) {
      if (isSel) selectedP2iPages.add(pageNum);
      else selectedP2iPages.delete(pageNum);
      const card = document.getElementById('p2i-card-' + pageNum);
      if (card) card.classList.toggle('selected-page', isSel);
      updateP2iSelectedUI();
    }

    function toggleCurrentP2iSelect() {
      const isSel = selectedP2iPages.has(activeP2iPage);
      toggleP2iPageSelect(activeP2iPage, !isSel);
      const card = document.getElementById('p2i-card-' + activeP2iPage);
      if (card) {
        const chk = card.querySelector('.thumb-checkbox');
        if (chk) chk.checked = !isSel;
      }
    }

    function selectAllP2iPages(select) {
      selectedP2iPages.clear();
      if (select) {
        for (let i = 1; i <= totalP2iPages; i++) selectedP2iPages.add(i);
      }
      for (let p = 1; p <= totalP2iPages; p++) {
        const card = document.getElementById('p2i-card-' + p);
        if (card) {
          card.classList.toggle('selected-page', select);
          const chk = card.querySelector('.thumb-checkbox');
          if (chk) chk.checked = select;
        }
      }
      updateP2iSelectedUI();
    }

    function updateP2iSelectedUI() {
      const count = selectedP2iPages.size;
      p2iSelectedCount.textContent = `${count} of ${totalP2iPages} pages selected`;
      if (btnToggleP2iCurr) {
        btnToggleP2iCurr.textContent = selectedP2iPages.has(activeP2iPage) ? '✓ Deselect Page' : '+ Select Page';
      }
    }

    function updateP2iZoomUI() {
      if (p2iZoomLabel) {
        p2iZoomLabel.textContent = Math.round(p2iZoom * 100) + '%';
      }
      if (p2iZoom <= 1.0) {
        p2iPanX = 0;
        p2iPanY = 0;
      } else if (p2iStage && p2iLargeCanvas) {
        const curW = (p2iLargeCanvas.offsetWidth || 300) * p2iZoom;
        const curH = (p2iLargeCanvas.offsetHeight || 400) * p2iZoom;
        const stW = p2iStage.clientWidth || 600;
        const stH = p2iStage.clientHeight || 480;
        const maxPanX = Math.max(0, (curW - stW) / 2 + 80);
        const maxPanY = Math.max(0, (curH - stH) / 2 + 80);
        p2iPanX = Math.max(-maxPanX, Math.min(maxPanX, p2iPanX));
        p2iPanY = Math.max(-maxPanY, Math.min(maxPanY, p2iPanY));
      }
      if (p2iPanWrap) {
        p2iPanWrap.style.transform = `translate(${p2iPanX}px, ${p2iPanY}px) scale(${p2iZoom})`;
      }
      if (p2iStage) {
        p2iStage.style.cursor = p2iZoom > 1.0 ? (isP2iDragging ? 'grabbing' : 'grab') : 'default';
      }
    }

    function zoomP2i(delta) {
      p2iZoom = Math.max(0.5, Math.min(2.5, +(p2iZoom + delta).toFixed(2)));
      updateP2iZoomUI();
    }

    function resetP2iZoomAndPan() {
      p2iZoom = 1.0;
      p2iPanX = 0;
      p2iPanY = 0;
      updateP2iZoomUI();
    }

    function showP2iLargePage(pageNum) {
      if (!p2iDoc || pageNum < 1 || pageNum > totalP2iPages) return;
      activeP2iPage = pageNum;
      resetP2iZoomAndPan();
      p2iPageIndicator.textContent = `Page ${pageNum} of ${totalP2iPages}`;

      document.querySelectorAll('#p2i-thumb-strip .pdf-thumb-card').forEach((el, idx) => {
        el.classList.toggle('active', (idx + 1) === pageNum);
      });

      if (btnToggleP2iCurr) {
        btnToggleP2iCurr.textContent = selectedP2iPages.has(activeP2iPage) ? '✓ Deselect Page' : '+ Select Page';
      }

      if (p2iRenderTask) {
        p2iRenderTask.cancel();
        p2iRenderTask = null;
      }

      p2iDoc.getPage(pageNum).then(function(page) {
        const stageH = p2iStage ? p2iStage.clientHeight : 480;
        const stageW = p2iStage ? p2iStage.clientWidth : 600;
        const maxFitH = Math.max(260, stageH - 40);
        const maxFitW = Math.max(260, stageW - 40);

        const baseViewport = page.getViewport({ scale: 1.0 });
        const fitScale = Math.min(maxFitW / baseViewport.width, maxFitH / baseViewport.height);
        const dpr = Math.max(window.devicePixelRatio || 1, 2);
        const renderViewport = page.getViewport({ scale: fitScale * dpr });

        p2iLargeCanvas.width = renderViewport.width;
        p2iLargeCanvas.height = renderViewport.height;
        p2iLargeCanvas.style.width = Math.round(baseViewport.width * fitScale) + 'px';
        p2iLargeCanvas.style.height = Math.round(baseViewport.height * fitScale) + 'px';

        const ctx = p2iLargeCanvas.getContext('2d');
        p2iRenderTask = page.render({ canvasContext: ctx, viewport: renderViewport });
        p2iRenderTask.promise.then(function() {
          p2iRenderTask = null;
          updateP2iZoomUI();
        }).catch(function(err) {
          if (err && err.name !== 'RenderingCancelledException') {
            console.error('Render error:', err);
          }
        });
      });
    }

    if (p2iStage) {
      p2iStage.addEventListener('dblclick', function(e) {
        e.preventDefault();
        resetP2iZoomAndPan();
      });

      p2iStage.addEventListener('mousedown', function(e) {
        if (e.button !== 0 || p2iZoom <= 1.0) return;
        isP2iDragging = true;
        p2iDragStartX = e.clientX - p2iPanX;
        p2iDragStartY = e.clientY - p2iPanY;
        if (p2iPanWrap) p2iPanWrap.classList.add('is-dragging');
        p2iStage.style.cursor = 'grabbing';
        e.preventDefault();
      });

      window.addEventListener('mousemove', function(e) {
        if (!isP2iDragging) return;
        p2iPanX = e.clientX - p2iDragStartX;
        p2iPanY = e.clientY - p2iDragStartY;
        updateP2iZoomUI();
      });

      window.addEventListener('mouseup', function() {
        if (!isP2iDragging) return;
        isP2iDragging = false;
        if (p2iPanWrap) p2iPanWrap.classList.remove('is-dragging');
        if (p2iStage) p2iStage.style.cursor = p2iZoom > 1.0 ? 'grab' : 'default';
      });

      p2iStage.addEventListener('touchstart', function(e) {
        if (e.touches.length === 1) {
          if (p2iZoom > 1.0) {
            isP2iTouching = true;
            p2iTouchStartX = e.touches[0].clientX - p2iPanX;
            p2iTouchStartY = e.touches[0].clientY - p2iPanY;
            if (p2iPanWrap) p2iPanWrap.classList.add('is-dragging');
          }
        } else if (e.touches.length === 2) {
          isP2iTouching = false;
          if (p2iPanWrap) p2iPanWrap.classList.add('is-dragging');
          p2iInitialPinchDist = Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
          );
          p2iPinchStartZoom = p2iZoom;
        }
      }, { passive: false });

      p2iStage.addEventListener('touchmove', function(e) {
        if (e.touches.length === 1 && isP2iTouching && p2iZoom > 1.0) {
          p2iPanX = e.touches[0].clientX - p2iTouchStartX;
          p2iPanY = e.touches[0].clientY - p2iTouchStartY;
          updateP2iZoomUI();
          e.preventDefault();
        } else if (e.touches.length === 2 && p2iInitialPinchDist > 0) {
          const currentDist = Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
          );
          const zoomFactor = currentDist / p2iInitialPinchDist;
          p2iZoom = Math.max(0.5, Math.min(2.5, +(p2iPinchStartZoom * zoomFactor).toFixed(2)));
          updateP2iZoomUI();
          e.preventDefault();
        }
      }, { passive: false });

      p2iStage.addEventListener('touchend', function(e) {
        if (e.touches.length === 0) {
          isP2iTouching = false;
          p2iInitialPinchDist = 0;
          if (p2iPanWrap) p2iPanWrap.classList.remove('is-dragging');
        } else if (e.touches.length === 1) {
          p2iInitialPinchDist = 0;
          if (p2iZoom > 1.0) {
            isP2iTouching = true;
            touchStartX = e.touches[0].clientX - p2iPanX;
            touchStartY = e.touches[0].clientY - p2iPanY;
          }
        }
      });

      p2iStage.addEventListener('wheel', function(e) {
        if (e.ctrlKey) {
          e.preventDefault();
          const delta = e.deltaY < 0 ? 0.25 : -0.25;
          zoomP2i(delta);
        }
      }, { passive: false });
    }

    function triggerP2iDownload() {
      if (!currentP2iBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentP2iBlobUrl;
      a.download = 'removix_extracted_images.zip';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxP2i = document.getElementById('dl-checkbox-p2i');
    const dlLabelP2i = document.getElementById('dl-label-p2i');
    if (dlCheckboxP2i) {
      dlCheckboxP2i.addEventListener('change', () => {
        if (dlCheckboxP2i.checked) {
          if (dlLabelP2i) dlLabelP2i.classList.add('is-checked');
          triggerP2iDownload();
          setTimeout(() => { isP2iDownloadComplete = true; }, 2350);
        }
      });
      dlCheckboxP2i.addEventListener('click', (e) => {
        if (isP2iDownloadComplete) { e.preventDefault(); triggerP2iDownload(); }
      });
    }

    function resetP2iView() {
      currentPdfFile = null;
      p2iDoc = null;
      selectedP2iPages.clear();
      resetP2iZoomAndPan();
      document.getElementById('p2i-result').style.display = 'none';
      document.getElementById('p2i-proc').style.display = 'none';
      document.getElementById('p2i-file-config').style.display = 'none';
      document.getElementById('dropzone-p2i').style.display = '';
      const inputEl = document.getElementById('file-input-p2i');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxP2i) dlCheckboxP2i.checked = false;
      if (dlLabelP2i) dlLabelP2i.classList.remove('is-checked');
      isP2iDownloadComplete = false;
      if (currentP2iBlobUrl) { URL.revokeObjectURL(currentP2iBlobUrl); currentP2iBlobUrl = ''; }
      p2iThumbStrip.innerHTML = '';
    }

    function executePdfExtraction() {
      if (!currentPdfFile) return;

      if (selectedP2iPages.size === 0) {
        alert('Please select at least one page to convert.');
        return;
      }

      const formData = new FormData();
      formData.append('pdf', currentPdfFile);
      formData.append('format', selectedPdfFmt);
      formData.append('pages', Array.from(selectedP2iPages).sort((a,b)=>a-b).join(','));

      document.getElementById('p2i-file-config').style.display = 'none';
      const procEl = document.getElementById('p2i-proc');
      procEl.style.display = 'block';

      fetch('/api/pdf-to-image', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Extraction failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('p2i-result').style.display = 'block';
        currentP2iBlobUrl = URL.createObjectURL(blob);
        document.getElementById('p2i-summary-msg').textContent = `Extracted ${selectedP2iPages.size} pages at 300 DPI as ${selectedPdfFmt} archive (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetP2iView();
      });
    }
    """

    return render_layout(
        title="PDF to Image Converter",
        active_tool="pdf-to-image",
        hero_title="PDF to Image Converter",
        hero_sub="Extract all pages from any PDF document into <strong>crystal-clear 300 DPI individual images</strong> with live preview.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
