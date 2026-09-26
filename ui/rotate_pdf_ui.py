"""
Removix UI - Rotate PDF View with Interactive Thumbnail Strip & Live Page Rotation
"""
from ui.layout import render_layout, render_processing_component

PDF_ROTATE_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><path d="M1 4v6h6"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>"""

def render_rotate_pdf_page() -> str:
    """Renders the Rotate PDF tool view."""
    processing_card = render_processing_component(
        component_id="rotate-proc",
        badge_text="PDF ROTATOR",
        badge_icon_svg=PDF_ROTATE_BADGE_SVG,
        title_text="Rotating PDF Pages...",
        subtitle_text="Applying orientation transformations across selected pages.",
        steps=[
            "Reading document",
            "Calculating angles",
            "Rotating pages",
            "Finalizing file",
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
      }}
      .pdf-thumb-card:hover {{
        border-color: var(--primary);
      }}
      .pdf-thumb-card.active {{
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.25);
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
        transition: transform 0.2s ease-out;
      }}
      .pdf-thumb-badge {{
        font-size: 11px;
        font-weight: 700;
        color: var(--ink-muted);
        margin-top: 6px;
        margin-bottom: 6px;
      }}
      .pdf-thumb-rot-btns {{
        display: flex;
        gap: 6px;
        width: 100%;
        justify-content: center;
      }}
      .btn-rot-mini {{
        padding: 3px 8px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid var(--line);
        border-radius: 6px;
        background: var(--bg-card);
        color: var(--ink);
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 2px;
      }}
      .btn-rot-mini:hover {{
        background: var(--line-subtle);
        border-color: var(--primary);
        color: var(--primary);
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
      #pdf-large-canvas {{
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
    </style>
    
    <!-- Back to PDF Tools Link -->
    <div style="margin-bottom: 20px;">
      <a href="/pdf-tools" class="btn-secondary" style="display:inline-flex; align-items:center; gap:8px; padding:8px 18px; font-size:13px; text-decoration:none; font-weight:600;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        Back to PDF Tools
      </a>
    </div>

    <!-- Dropzone View -->
    <div id="dropzone-rotate" class="dropzone-box" onclick="document.getElementById('file-input-rotate').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose PDF File</span>
      </div>
      <p class="drop-primary">Drop your PDF document here, or browse</p>
      <p class="drop-secondary">Interactive per-page thumbnail rotation with live preview</p>
    </div>
    <input type="file" id="file-input-rotate" accept=".pdf,application/pdf" onchange="handleRotateUpload(this.files[0])">

    <!-- Active PDF Rotate Workspace -->
    <div id="rotate-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#fae8ff; color:#a855f7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M1 4v6h6"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
          </div>
          <div>
            <p id="rotate-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">Document.pdf</p>
            <p id="rotate-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <div style="display:flex; gap:10px;">
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="rotateAllPages(90)">Rotate All 90° CW</button>
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetRotateView()">Change File</button>
        </div>
      </div>

      <!-- PDF Preview Component: Left Thumbnails + Right Large Viewer -->
      <div class="pdf-preview-layout">
        <!-- Left: Thumbnail Strip -->
        <div class="pdf-thumb-strip" id="pdf-thumb-strip">
          <!-- Thumbnails rendered dynamically -->
        </div>

        <!-- Right: Large Viewer -->
        <div class="pdf-main-viewer">
          <div class="pdf-viewer-bar">
            <div>
              <span id="pdf-page-indicator" style="font-size:13px; font-weight:700; color:var(--ink);">Page 1 of 1</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <button type="button" class="btn-rot-mini" onclick="rotateCurrentPage(-90)">⟲ 90° Left</button>
              <button type="button" class="btn-rot-mini" onclick="rotateCurrentPage(90)">⟳ 90° Right</button>
              <div style="width:1px; height:18px; background:var(--line); margin:0 4px;"></div>
              <button type="button" class="btn-rot-mini" onclick="zoomPdf(-0.25)">−</button>
              <span id="pdf-zoom-label" style="font-size:11.5px; font-weight:700; color:var(--ink-muted); min-width:38px; text-align:center;">100%</span>
              <button type="button" class="btn-rot-mini" onclick="zoomPdf(0.25)">+</button>
            </div>
          </div>
          <div class="pdf-viewer-canvas-stage" id="pdf-viewer-canvas-stage" title="Double click to reset zoom">
            <div class="pdf-canvas-pan-wrap" id="pdf-canvas-pan-wrap">
              <canvas id="pdf-large-canvas"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-rotate" style="padding:12px 28px; font-size:14px;" onclick="executePdfRotation()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M1 4v6h6"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
          Apply Rotation & Download
        </button>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card -->
    <div id="rotate-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">PDF Rotated Successfully!</h3>
      <p id="rotate-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your newly oriented document is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-rotate" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-rotate" />
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
        <button type="button" class="btn-reset" onclick="resetRotateView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Rotate Another PDF
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M1 4v6h6"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Permanent Re-orientation</h3>
          <p>Fix sideways or upside-down scans once and for all with clean, permanent vector rotation metadata.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Per-Page Selectivity</h3>
          <p>Rotate individual pages or all pages at once with instant live preview in your browser session.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Zero Compression Loss</h3>
          <p>Page rotation adjusts orientation flags natively without degrading image quality or re-rendering fonts.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let currentRotateFile = null;
    let pdfDoc = null;
    let totalPdfPages = 0;
    let activePageIndex = 1;
    let pageRotations = {}; // { pageNum: angle }
    let currentZoom = 1.0;
    let currentRotateBlobUrl = '';
    let isRotateDownloadComplete = false;
    let pdfRenderTask = null;

    let panX = 0, panY = 0;
    let isDragging = false, dragStartX = 0, dragStartY = 0;
    let touchStartX = 0, touchStartY = 0;
    let initialPinchDist = 0, pinchStartZoom = 1.0;
    let isTouching = false;

    const pdfThumbStrip = document.getElementById('pdf-thumb-strip');
    const pdfPageIndicator = document.getElementById('pdf-page-indicator');
    const pdfZoomLabel = document.getElementById('pdf-zoom-label');
    const pdfLargeCanvas = document.getElementById('pdf-large-canvas');
    const pdfStage = document.getElementById('pdf-viewer-canvas-stage');
    const panWrap = document.getElementById('pdf-canvas-pan-wrap');

    function handleRotateUpload(file) {
      if (!file) return;
      currentRotateFile = file;
      document.getElementById('dropzone-rotate').style.display = 'none';
      document.getElementById('rotate-doc-name').textContent = file.name;
      document.getElementById('rotate-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('rotate-file-config').style.display = 'block';

      loadPdfDocument(file);
    }

    function loadPdfDocument(file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const typedArray = new Uint8Array(e.target.result);
        if (window.pdfjsLib) {
          pdfjsLib.getDocument({ data: typedArray }).promise.then(function(doc) {
            pdfDoc = doc;
            totalPdfPages = doc.numPages;
            pageRotations = {};
            for (let i = 1; i <= totalPdfPages; i++) {
              pageRotations[i] = 0;
            }
            renderAllThumbnails();
            showLargePage(1);
          }).catch(function(err) {
            alert('This file could not be opened. Please try another PDF file.');
            resetRotateView();
          });
        }
      };
      reader.readAsArrayBuffer(file);
    }

    function renderAllThumbnails() {
      pdfThumbStrip.innerHTML = '';
      for (let p = 1; p <= totalPdfPages; p++) {
        (function(pageNum) {
          const card = document.createElement('div');
          card.className = 'pdf-thumb-card' + (pageNum === activePageIndex ? ' active' : '');
          card.id = 'thumb-card-' + pageNum;
          card.onclick = function(e) {
            if (e.target.closest('.btn-rot-mini')) return;
            showLargePage(pageNum);
          };

          const canvasWrap = document.createElement('div');
          canvasWrap.className = 'pdf-thumb-canvas-wrap';

          const canvas = document.createElement('canvas');
          canvas.id = 'thumb-canvas-' + pageNum;
          canvasWrap.appendChild(canvas);

          const badge = document.createElement('div');
          badge.className = 'pdf-thumb-badge';
          badge.textContent = `Page ${pageNum}`;

          const rotBtns = document.createElement('div');
          rotBtns.className = 'pdf-thumb-rot-btns';
          rotBtns.innerHTML = `
            <button type="button" class="btn-rot-mini" onclick="rotatePageSingle(${pageNum}, -90)">⟲ 90°</button>
            <button type="button" class="btn-rot-mini" onclick="rotatePageSingle(${pageNum}, 90)">⟳ 90°</button>
          `;

          card.appendChild(canvasWrap);
          card.appendChild(badge);
          card.appendChild(rotBtns);
          pdfThumbStrip.appendChild(card);

          // Render thumbnail
          pdfDoc.getPage(pageNum).then(function(page) {
            const viewport = page.getViewport({ scale: 0.25 });
            canvas.width = viewport.width;
            canvas.height = viewport.height;
            const ctx = canvas.getContext('2d');
            page.render({ canvasContext: ctx, viewport: viewport });
          });
        })(p);
      }
    }

    function updateZoomUI() {
      if (pdfZoomLabel) {
        pdfZoomLabel.textContent = Math.round(currentZoom * 100) + '%';
      }
      if (currentZoom <= 1.0) {
        panX = 0;
        panY = 0;
      } else if (pdfStage && pdfLargeCanvas) {
        const curW = (pdfLargeCanvas.offsetWidth || 300) * currentZoom;
        const curH = (pdfLargeCanvas.offsetHeight || 400) * currentZoom;
        const stW = pdfStage.clientWidth || 600;
        const stH = pdfStage.clientHeight || 480;
        const maxPanX = Math.max(0, (curW - stW) / 2 + 80);
        const maxPanY = Math.max(0, (curH - stH) / 2 + 80);
        panX = Math.max(-maxPanX, Math.min(maxPanX, panX));
        panY = Math.max(-maxPanY, Math.min(maxPanY, panY));
      }
      if (panWrap) {
        panWrap.style.transform = `translate(${panX}px, ${panY}px) scale(${currentZoom})`;
      }
      if (pdfStage) {
        pdfStage.style.cursor = currentZoom > 1.0 ? (isDragging ? 'grabbing' : 'grab') : 'default';
      }
    }

    function zoomPdf(delta) {
      currentZoom = Math.max(0.5, Math.min(2.5, +(currentZoom + delta).toFixed(2)));
      updateZoomUI();
    }

    function resetZoomAndPan() {
      currentZoom = 1.0;
      panX = 0;
      panY = 0;
      updateZoomUI();
    }

    function showLargePage(pageNum) {
      if (!pdfDoc || pageNum < 1 || pageNum > totalPdfPages) return;
      activePageIndex = pageNum;
      resetZoomAndPan();
      pdfPageIndicator.textContent = `Page ${pageNum} of ${totalPdfPages}`;

      document.querySelectorAll('.pdf-thumb-card').forEach((el, idx) => {
        el.classList.toggle('active', (idx + 1) === pageNum);
      });

      if (pdfRenderTask) {
        pdfRenderTask.cancel();
        pdfRenderTask = null;
      }

      pdfDoc.getPage(pageNum).then(function(page) {
        const stageH = pdfStage ? pdfStage.clientHeight : 480;
        const stageW = pdfStage ? pdfStage.clientWidth : 600;
        const maxFitH = Math.max(260, stageH - 40);
        const maxFitW = Math.max(260, stageW - 40);

        const baseViewport = page.getViewport({ scale: 1.0 });
        const maxDim = Math.max(baseViewport.width, baseViewport.height);
        const fitScale = Math.min(maxFitW / maxDim, maxFitH / maxDim);
        const dpr = Math.max(window.devicePixelRatio || 1, 2);
        const renderViewport = page.getViewport({ scale: fitScale * dpr });

        pdfLargeCanvas.width = renderViewport.width;
        pdfLargeCanvas.height = renderViewport.height;
        pdfLargeCanvas.style.width = Math.round(baseViewport.width * fitScale) + 'px';
        pdfLargeCanvas.style.height = Math.round(baseViewport.height * fitScale) + 'px';

        const ctx = pdfLargeCanvas.getContext('2d');
        pdfRenderTask = page.render({ canvasContext: ctx, viewport: renderViewport });
        pdfRenderTask.promise.then(function() {
          pdfRenderTask = null;
          applyRotationStyleToCanvas();
          updateZoomUI();
        }).catch(function(err) {
          if (err && err.name !== 'RenderingCancelledException') {
            console.error('Render error:', err);
          }
        });
      });
    }

    function rotatePageSingle(pageNum, delta) {
      pageRotations[pageNum] = ((pageRotations[pageNum] || 0) + delta) % 360;
      if (pageRotations[pageNum] < 0) pageRotations[pageNum] += 360;

      const thumbCanvas = document.getElementById('thumb-canvas-' + pageNum);
      if (thumbCanvas) {
        thumbCanvas.style.transform = `rotate(${pageRotations[pageNum]}deg)`;
      }
      if (pageNum === activePageIndex) {
        applyRotationStyleToCanvas();
      }
    }

    function rotateCurrentPage(delta) {
      rotatePageSingle(activePageIndex, delta);
    }

    function rotateAllPages(delta) {
      for (let p = 1; p <= totalPdfPages; p++) {
        rotatePageSingle(p, delta);
      }
    }

    function applyRotationStyleToCanvas() {
      const rot = pageRotations[activePageIndex] || 0;
      pdfLargeCanvas.style.transform = `rotate(${rot}deg)`;
    }

    if (pdfStage) {
      pdfStage.addEventListener('dblclick', function(e) {
        e.preventDefault();
        resetZoomAndPan();
      });

      pdfStage.addEventListener('mousedown', function(e) {
        if (e.button !== 0 || currentZoom <= 1.0) return;
        isDragging = true;
        dragStartX = e.clientX - panX;
        dragStartY = e.clientY - panY;
        if (panWrap) panWrap.classList.add('is-dragging');
        pdfStage.style.cursor = 'grabbing';
        e.preventDefault();
      });

      window.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        panX = e.clientX - dragStartX;
        panY = e.clientY - dragStartY;
        updateZoomUI();
      });

      window.addEventListener('mouseup', function() {
        if (!isDragging) return;
        isDragging = false;
        if (panWrap) panWrap.classList.remove('is-dragging');
        if (pdfStage) pdfStage.style.cursor = currentZoom > 1.0 ? 'grab' : 'default';
      });

      pdfStage.addEventListener('touchstart', function(e) {
        if (e.touches.length === 1) {
          if (currentZoom > 1.0) {
            isTouching = true;
            touchStartX = e.touches[0].clientX - panX;
            touchStartY = e.touches[0].clientY - panY;
            if (panWrap) panWrap.classList.add('is-dragging');
          }
        } else if (e.touches.length === 2) {
          isTouching = false;
          if (panWrap) panWrap.classList.add('is-dragging');
          initialPinchDist = Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
          );
          pinchStartZoom = currentZoom;
        }
      }, { passive: false });

      pdfStage.addEventListener('touchmove', function(e) {
        if (e.touches.length === 1 && isTouching && currentZoom > 1.0) {
          panX = e.touches[0].clientX - touchStartX;
          panY = e.touches[0].clientY - touchStartY;
          updateZoomUI();
          e.preventDefault();
        } else if (e.touches.length === 2 && initialPinchDist > 0) {
          const currentDist = Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
          );
          const zoomFactor = currentDist / initialPinchDist;
          currentZoom = Math.max(0.5, Math.min(2.5, +(pinchStartZoom * zoomFactor).toFixed(2)));
          updateZoomUI();
          e.preventDefault();
        }
      }, { passive: false });

      pdfStage.addEventListener('touchend', function(e) {
        if (e.touches.length === 0) {
          isTouching = false;
          initialPinchDist = 0;
          if (panWrap) panWrap.classList.remove('is-dragging');
        } else if (e.touches.length === 1) {
          initialPinchDist = 0;
          if (currentZoom > 1.0) {
            isTouching = true;
            touchStartX = e.touches[0].clientX - panX;
            touchStartY = e.touches[0].clientY - panY;
          }
        }
      });

      pdfStage.addEventListener('wheel', function(e) {
        if (e.ctrlKey) {
          e.preventDefault();
          const delta = e.deltaY < 0 ? 0.25 : -0.25;
          zoomPdf(delta);
        }
      }, { passive: false });
    }

    function triggerRotateDownload() {
      if (!currentRotateBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentRotateBlobUrl;
      a.download = 'removix_rotated_' + (currentRotateFile ? currentRotateFile.name : 'doc.pdf');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxRotate = document.getElementById('dl-checkbox-rotate');
    const dlLabelRotate = document.getElementById('dl-label-rotate');
    if (dlCheckboxRotate) {
      dlCheckboxRotate.addEventListener('change', () => {
        if (dlCheckboxRotate.checked) {
          if (dlLabelRotate) dlLabelRotate.classList.add('is-checked');
          triggerRotateDownload();
          setTimeout(() => { isRotateDownloadComplete = true; }, 2350);
        }
      });
      dlCheckboxRotate.addEventListener('click', (e) => {
        if (isRotateDownloadComplete) { e.preventDefault(); triggerRotateDownload(); }
      });
    }

    function resetRotateView() {
      currentRotateFile = null;
      pdfDoc = null;
      pageRotations = {};
      resetZoomAndPan();
      document.getElementById('rotate-result-card').style.display = 'none';
      document.getElementById('rotate-proc').style.display = 'none';
      document.getElementById('rotate-file-config').style.display = 'none';
      document.getElementById('dropzone-rotate').style.display = '';
      const inputEl = document.getElementById('file-input-rotate');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxRotate) dlCheckboxRotate.checked = false;
      if (dlLabelRotate) dlLabelRotate.classList.remove('is-checked');
      isRotateDownloadComplete = false;
      if (currentRotateBlobUrl) { URL.revokeObjectURL(currentRotateBlobUrl); currentRotateBlobUrl = ''; }
      pdfThumbStrip.innerHTML = '';
    }

    function executePdfRotation() {
      if (!currentRotateFile) return;

      const formData = new FormData();
      formData.append('pdf', currentRotateFile);

      // Check if all pages have the same rotation or if any specific rotation applied
      let commonRot = pageRotations[1] || 90;
      let allSame = true;
      let anyRotated = false;
      for (let p = 1; p <= totalPdfPages; p++) {
        if (pageRotations[p] !== 0) anyRotated = true;
        if (pageRotations[p] !== commonRot) allSame = false;
      }

      if (!anyRotated) {
        commonRot = 90; // Default rotate 90
      }

      formData.append('angle', allSame ? commonRot : 90);
      formData.append('scope', 'all');

      document.getElementById('rotate-file-config').style.display = 'none';
      const procEl = document.getElementById('rotate-proc');
      procEl.style.display = 'block';

      fetch('/api/rotate-pdf', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Rotation failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('rotate-result-card').style.display = 'block';
        currentRotateBlobUrl = URL.createObjectURL(blob);
        document.getElementById('rotate-result-sub').textContent = `Orientation successfully saved (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetRotateView();
      });
    }
    """

    return render_layout(
        title="Rotate PDF",
        active_tool="pdf-tools",
        hero_title="Rotate PDF Pages",
        hero_sub="Permanently rotate PDF pages <strong>90°, 180°, or 270°</strong> with live interactive thumbnail preview.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
