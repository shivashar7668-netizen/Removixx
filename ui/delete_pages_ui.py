"""
Removix UI - Delete Pages View with Thumbnail Strip & Red Delete Overlay
"""
from ui.layout import render_layout, render_processing_component

PDF_DELETE_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>"""

def render_delete_pages_page() -> str:
    """Renders the Delete Pages tool view."""
    processing_card = render_processing_component(
        component_id="delete-proc",
        badge_text="PAGE REMOVER",
        badge_icon_svg=PDF_DELETE_BADGE_SVG,
        title_text="Removing Selected Pages...",
        subtitle_text="Stripping unwanted pages and compiling a clean new document.",
        steps=[
            "Reading document",
            "Identifying target pages",
            "Pruning pages",
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
        overflow: hidden;
      }}
      .pdf-thumb-card:hover {{
        border-color: var(--primary);
      }}
      .pdf-thumb-card.active {{
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.25);
      }}
      .pdf-thumb-card.marked-delete {{
        border-color: #ef4444 !important;
        background: rgba(239, 68, 68, 0.05);
      }}
      .thumb-delete-overlay {{
        display: none;
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(239, 68, 68, 0.25);
        backdrop-filter: blur(1px);
        align-items: center;
        justify-content: center;
        z-index: 4;
        pointer-events: none;
      }}
      .pdf-thumb-card.marked-delete .thumb-delete-overlay {{
        display: flex;
      }}
      .thumb-delete-badge {{
        background: #ef4444;
        color: #ffffff;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 9999px;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
      }}
      .btn-thumb-x {{
        position: absolute;
        top: 6px;
        right: 6px;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: rgba(239, 68, 68, 0.12);
        color: #ef4444;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 5;
        font-size: 13px;
        font-weight: 800;
        transition: all 0.15s ease;
      }}
      .btn-thumb-x:hover {{
        background: #ef4444;
        color: #ffffff;
      }}
      .pdf-thumb-card.marked-delete .btn-thumb-x {{
        background: #ef4444;
        color: #ffffff;
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
      #delete-large-canvas {{
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

    <!-- Dropzone View -->
    <div id="dropzone-delete" class="dropzone-box" onclick="document.getElementById('file-input-delete').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose PDF File</span>
      </div>
      <p class="drop-primary">Drop your PDF document here, or browse</p>
      <p class="drop-secondary">Click ❌ on any page thumbnail to mark for instant deletion</p>
    </div>
    <input type="file" id="file-input-delete" accept=".pdf,application/pdf" onchange="handleDeleteUpload(this.files[0])">

    <!-- Active PDF Delete Workspace -->
    <div id="delete-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#fee2e2; color:#dc2626; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
          </div>
          <div>
            <p id="delete-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">Document.pdf</p>
            <p id="delete-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
          <span id="delete-marked-count" style="font-size:12px; font-weight:700; color:#ef4444; background:rgba(239,68,68,0.1); padding:5px 12px; border-radius:9999px;">0 pages marked</span>
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetDeleteView()">Change File</button>
        </div>
      </div>

      <!-- PDF Preview Component: Left Thumbnails + Right Large Viewer -->
      <div class="pdf-preview-layout">
        <!-- Left: Thumbnail Strip -->
        <div class="pdf-thumb-strip" id="delete-thumb-strip">
          <!-- Thumbnails rendered dynamically -->
        </div>

        <!-- Right: Large Viewer -->
        <div class="pdf-main-viewer">
          <div class="pdf-viewer-bar">
            <div>
              <span id="delete-page-indicator" style="font-size:13px; font-weight:700; color:var(--ink);">Page 1 of 1</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <button type="button" id="btn-toggle-del-curr" class="btn-rot-mini" style="color:#ef4444;" onclick="toggleCurrentPageDelete()">
                ❌ Mark for Deletion
              </button>
              <div style="width:1px; height:18px; background:var(--line); margin:0 4px;"></div>
              <button type="button" class="btn-rot-mini" onclick="zoomPdf(-0.25)">−</button>
              <span id="delete-zoom-label" style="font-size:11.5px; font-weight:700; color:var(--ink-muted); min-width:38px; text-align:center;">100%</span>
              <button type="button" class="btn-rot-mini" onclick="zoomPdf(0.25)">+</button>
            </div>
          </div>
          <div class="pdf-viewer-canvas-stage" id="delete-viewer-canvas-stage" title="Double click to reset zoom">
            <div class="pdf-canvas-pan-wrap" id="delete-canvas-pan-wrap">
              <canvas id="delete-large-canvas"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-delete" style="padding:12px 28px; font-size:14px; background:#dc2626;" onclick="executePdfDelete()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
          Delete Selected Pages
        </button>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card -->
    <div id="delete-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Pages Removed Successfully!</h3>
      <p id="delete-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your cleaned PDF is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-delete" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-delete" />
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
        <button type="button" class="btn-reset" onclick="resetDeleteView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Delete More Pages
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Visual Selection</h3>
          <p>Click the ❌ on any page thumbnail to mark unwanted sheets with an instant visual indicator.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>100% Private</h3>
          <p>Thumbnails render directly in your browser without uploading your sensitive documents to any cloud.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Lossless Output</h3>
          <p>Remaining pages retain original vector typography, embedded images, and annotations perfectly.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let currentDeleteFile = null;
    let deletePdfDoc = null;
    let totalDeletePages = 0;
    let activeDeletePage = 1;
    let markedDeletePages = new Set();
    let deleteZoom = 1.0;
    let currentDeleteBlobUrl = '';
    let isDeleteDownloadComplete = false;
    let deleteRenderTask = null;

    let deletePanX = 0, deletePanY = 0;
    let isDeleteDragging = false, deleteDragStartX = 0, deleteDragStartY = 0;
    let deleteTouchStartX = 0, deleteTouchStartY = 0;
    let deleteInitialPinchDist = 0, deletePinchStartZoom = 1.0;
    let isDeleteTouching = false;

    const deleteThumbStrip = document.getElementById('delete-thumb-strip');
    const deletePageIndicator = document.getElementById('delete-page-indicator');
    const deleteZoomLabel = document.getElementById('delete-zoom-label');
    const deleteLargeCanvas = document.getElementById('delete-large-canvas');
    const deleteStage = document.getElementById('delete-viewer-canvas-stage');
    const deletePanWrap = document.getElementById('delete-canvas-pan-wrap');
    const deleteMarkedCount = document.getElementById('delete-marked-count');
    const btnToggleDelCurr = document.getElementById('btn-toggle-del-curr');

    function handleDeleteUpload(file) {
      if (!file) return;
      currentDeleteFile = file;
      document.getElementById('dropzone-delete').style.display = 'none';
      document.getElementById('delete-doc-name').textContent = file.name;
      document.getElementById('delete-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('delete-file-config').style.display = 'block';

      loadPdfForDelete(file);
    }

    function loadPdfForDelete(file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const typedArray = new Uint8Array(e.target.result);
        if (window.pdfjsLib) {
          pdfjsLib.getDocument({ data: typedArray }).promise.then(function(doc) {
            deletePdfDoc = doc;
            totalDeletePages = doc.numPages;
            markedDeletePages.clear();
            renderDeleteThumbnails();
            showDeleteLargePage(1);
            updateMarkedCount();
          }).catch(function(err) {
            alert('This file could not be opened. Please try another PDF file.');
            resetDeleteView();
          });
        }
      };
      reader.readAsArrayBuffer(file);
    }

    function renderDeleteThumbnails() {
      deleteThumbStrip.innerHTML = '';
      for (let p = 1; p <= totalDeletePages; p++) {
        (function(pageNum) {
          const card = document.createElement('div');
          card.className = 'pdf-thumb-card' + (pageNum === activeDeletePage ? ' active' : '') + (markedDeletePages.has(pageNum) ? ' marked-delete' : '');
          card.id = 'del-card-' + pageNum;
          card.onclick = function(e) {
            if (e.target.closest('.btn-thumb-x')) return;
            showDeleteLargePage(pageNum);
          };

          const xBtn = document.createElement('button');
          xBtn.type = 'button';
          xBtn.className = 'btn-thumb-x';
          xBtn.innerHTML = '✕';
          xBtn.title = 'Mark for deletion';
          xBtn.onclick = function(e) {
            e.stopPropagation();
            togglePageDeleteMark(pageNum);
          };

          const overlay = document.createElement('div');
          overlay.className = 'thumb-delete-overlay';
          overlay.innerHTML = '<span class="thumb-delete-badge">DELETE</span>';

          const canvasWrap = document.createElement('div');
          canvasWrap.className = 'pdf-thumb-canvas-wrap';

          const canvas = document.createElement('canvas');
          canvasWrap.appendChild(canvas);

          const badge = document.createElement('div');
          badge.className = 'pdf-thumb-badge';
          badge.textContent = `Page ${pageNum}`;

          card.appendChild(xBtn);
          card.appendChild(overlay);
          card.appendChild(canvasWrap);
          card.appendChild(badge);
          deleteThumbStrip.appendChild(card);

          // Render thumbnail
          deletePdfDoc.getPage(pageNum).then(function(page) {
            const viewport = page.getViewport({ scale: 0.25 });
            canvas.width = viewport.width;
            canvas.height = viewport.height;
            const ctx = canvas.getContext('2d');
            page.render({ canvasContext: ctx, viewport: viewport });
          });
        })(p);
      }
    }

    function togglePageDeleteMark(pageNum) {
      if (markedDeletePages.has(pageNum)) {
        markedDeletePages.delete(pageNum);
      } else {
        if (markedDeletePages.size >= totalDeletePages - 1) {
          alert('Cannot delete all pages in the PDF.');
          return;
        }
        markedDeletePages.add(pageNum);
      }
      const card = document.getElementById('del-card-' + pageNum);
      if (card) {
        card.classList.toggle('marked-delete', markedDeletePages.has(pageNum));
      }
      updateMarkedCount();
      updateCurrentPageDeleteBtn();
    }

    function toggleCurrentPageDelete() {
      togglePageDeleteMark(activeDeletePage);
    }

    function updateMarkedCount() {
      const count = markedDeletePages.size;
      deleteMarkedCount.textContent = `${count} page${count === 1 ? '' : 's'} marked for deletion`;
    }

    function updateCurrentPageDeleteBtn() {
      if (markedDeletePages.has(activeDeletePage)) {
        btnToggleDelCurr.innerHTML = '✓ Keep Page';
        btnToggleDelCurr.style.color = '#10b981';
      } else {
        btnToggleDelCurr.innerHTML = '❌ Mark for Deletion';
        btnToggleDelCurr.style.color = '#ef4444';
      }
    }

    function updateDeleteZoomUI() {
      if (deleteZoomLabel) {
        deleteZoomLabel.textContent = Math.round(deleteZoom * 100) + '%';
      }
      if (deleteZoom <= 1.0) {
        deletePanX = 0;
        deletePanY = 0;
      } else if (deleteStage && deleteLargeCanvas) {
        const curW = (deleteLargeCanvas.offsetWidth || 300) * deleteZoom;
        const curH = (deleteLargeCanvas.offsetHeight || 400) * deleteZoom;
        const stW = deleteStage.clientWidth || 600;
        const stH = deleteStage.clientHeight || 480;
        const maxPanX = Math.max(0, (curW - stW) / 2 + 80);
        const maxPanY = Math.max(0, (curH - stH) / 2 + 80);
        deletePanX = Math.max(-maxPanX, Math.min(maxPanX, deletePanX));
        deletePanY = Math.max(-maxPanY, Math.min(maxPanY, deletePanY));
      }
      if (deletePanWrap) {
        deletePanWrap.style.transform = `translate(${deletePanX}px, ${deletePanY}px) scale(${deleteZoom})`;
      }
      if (deleteStage) {
        deleteStage.style.cursor = deleteZoom > 1.0 ? (isDeleteDragging ? 'grabbing' : 'grab') : 'default';
      }
    }

    function zoomPdf(delta) {
      deleteZoom = Math.max(0.5, Math.min(2.5, +(deleteZoom + delta).toFixed(2)));
      updateDeleteZoomUI();
    }

    function resetDeleteZoomAndPan() {
      deleteZoom = 1.0;
      deletePanX = 0;
      deletePanY = 0;
      updateDeleteZoomUI();
    }

    function showDeleteLargePage(pageNum) {
      if (!deletePdfDoc || pageNum < 1 || pageNum > totalDeletePages) return;
      activeDeletePage = pageNum;
      resetDeleteZoomAndPan();
      deletePageIndicator.textContent = `Page ${pageNum} of ${totalDeletePages}`;

      document.querySelectorAll('#delete-thumb-strip .pdf-thumb-card').forEach((el, idx) => {
        el.classList.toggle('active', (idx + 1) === pageNum);
      });

      updateCurrentPageDeleteBtn();

      if (deleteRenderTask) {
        deleteRenderTask.cancel();
        deleteRenderTask = null;
      }

      deletePdfDoc.getPage(pageNum).then(function(page) {
        const stageH = deleteStage ? deleteStage.clientHeight : 480;
        const stageW = deleteStage ? deleteStage.clientWidth : 600;
        const maxFitH = Math.max(260, stageH - 40);
        const maxFitW = Math.max(260, stageW - 40);

        const baseViewport = page.getViewport({ scale: 1.0 });
        const fitScale = Math.min(maxFitW / baseViewport.width, maxFitH / baseViewport.height);
        const dpr = Math.max(window.devicePixelRatio || 1, 2);
        const renderViewport = page.getViewport({ scale: fitScale * dpr });

        deleteLargeCanvas.width = renderViewport.width;
        deleteLargeCanvas.height = renderViewport.height;
        deleteLargeCanvas.style.width = Math.round(baseViewport.width * fitScale) + 'px';
        deleteLargeCanvas.style.height = Math.round(baseViewport.height * fitScale) + 'px';

        const ctx = deleteLargeCanvas.getContext('2d');
        deleteRenderTask = page.render({ canvasContext: ctx, viewport: renderViewport });
        deleteRenderTask.promise.then(function() {
          deleteRenderTask = null;
          updateDeleteZoomUI();
        }).catch(function(err) {
          if (err && err.name !== 'RenderingCancelledException') {
            console.error('Render error:', err);
          }
        });
      });
    }

    if (deleteStage) {
      deleteStage.addEventListener('dblclick', function(e) {
        e.preventDefault();
        resetDeleteZoomAndPan();
      });

      deleteStage.addEventListener('mousedown', function(e) {
        if (e.button !== 0 || deleteZoom <= 1.0) return;
        isDeleteDragging = true;
        deleteDragStartX = e.clientX - deletePanX;
        deleteDragStartY = e.clientY - deletePanY;
        if (deletePanWrap) deletePanWrap.classList.add('is-dragging');
        deleteStage.style.cursor = 'grabbing';
        e.preventDefault();
      });

      window.addEventListener('mousemove', function(e) {
        if (!isDeleteDragging) return;
        deletePanX = e.clientX - deleteDragStartX;
        deletePanY = e.clientY - deleteDragStartY;
        updateDeleteZoomUI();
      });

      window.addEventListener('mouseup', function() {
        if (!isDeleteDragging) return;
        isDeleteDragging = false;
        if (deletePanWrap) deletePanWrap.classList.remove('is-dragging');
        if (deleteStage) deleteStage.style.cursor = deleteZoom > 1.0 ? 'grab' : 'default';
      });

      deleteStage.addEventListener('touchstart', function(e) {
        if (e.touches.length === 1) {
          if (deleteZoom > 1.0) {
            isDeleteTouching = true;
            deleteTouchStartX = e.touches[0].clientX - deletePanX;
            deleteTouchStartY = e.touches[0].clientY - deletePanY;
            if (deletePanWrap) deletePanWrap.classList.add('is-dragging');
          }
        } else if (e.touches.length === 2) {
          isDeleteTouching = false;
          if (deletePanWrap) deletePanWrap.classList.add('is-dragging');
          deleteInitialPinchDist = Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
          );
          deletePinchStartZoom = deleteZoom;
        }
      }, { passive: false });

      deleteStage.addEventListener('touchmove', function(e) {
        if (e.touches.length === 1 && isDeleteTouching && deleteZoom > 1.0) {
          deletePanX = e.touches[0].clientX - deleteTouchStartX;
          deletePanY = e.touches[0].clientY - deleteTouchStartY;
          updateDeleteZoomUI();
          e.preventDefault();
        } else if (e.touches.length === 2 && deleteInitialPinchDist > 0) {
          const currentDist = Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
          );
          const zoomFactor = currentDist / deleteInitialPinchDist;
          deleteZoom = Math.max(0.5, Math.min(2.5, +(deletePinchStartZoom * zoomFactor).toFixed(2)));
          updateDeleteZoomUI();
          e.preventDefault();
        }
      }, { passive: false });

      deleteStage.addEventListener('touchend', function(e) {
        if (e.touches.length === 0) {
          isDeleteTouching = false;
          deleteInitialPinchDist = 0;
          if (deletePanWrap) deletePanWrap.classList.remove('is-dragging');
        } else if (e.touches.length === 1) {
          deleteInitialPinchDist = 0;
          if (deleteZoom > 1.0) {
            isDeleteTouching = true;
            deleteTouchStartX = e.touches[0].clientX - deletePanX;
            deleteTouchStartY = e.touches[0].clientY - deletePanY;
          }
        }
      });

      deleteStage.addEventListener('wheel', function(e) {
        if (e.ctrlKey) {
          e.preventDefault();
          const delta = e.deltaY < 0 ? 0.25 : -0.25;
          zoomPdf(delta);
        }
      }, { passive: false });
    }

    function triggerDeleteDownload() {
      if (!currentDeleteBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentDeleteBlobUrl;
      a.download = 'removix_cleaned_' + (currentDeleteFile ? currentDeleteFile.name : 'doc.pdf');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxDelete = document.getElementById('dl-checkbox-delete');
    const dlLabelDelete = document.getElementById('dl-label-delete');
    if (dlCheckboxDelete) {
      dlCheckboxDelete.addEventListener('change', () => {
        if (dlCheckboxDelete.checked) {
          if (dlLabelDelete) dlLabelDelete.classList.add('is-checked');
          triggerDeleteDownload();
          setTimeout(() => { isDeleteDownloadComplete = true; }, 2350);
        }
      });
      dlCheckboxDelete.addEventListener('click', (e) => {
        if (isDeleteDownloadComplete) { e.preventDefault(); triggerDeleteDownload(); }
      });
    }

    function resetDeleteView() {
      currentDeleteFile = null;
      deletePdfDoc = null;
      markedDeletePages.clear();
      resetDeleteZoomAndPan();
      document.getElementById('delete-result-card').style.display = 'none';
      document.getElementById('delete-proc').style.display = 'none';
      document.getElementById('delete-file-config').style.display = 'none';
      document.getElementById('dropzone-delete').style.display = '';
      const inputEl = document.getElementById('file-input-delete');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxDelete) dlCheckboxDelete.checked = false;
      if (dlLabelDelete) dlLabelDelete.classList.remove('is-checked');
      isDeleteDownloadComplete = false;
      if (currentDeleteBlobUrl) { URL.revokeObjectURL(currentDeleteBlobUrl); currentDeleteBlobUrl = ''; }
      deleteThumbStrip.innerHTML = '';
    }

    function executePdfDelete() {
      if (!currentDeleteFile) return;

      if (markedDeletePages.size === 0) {
        alert('Please mark at least one page for deletion by clicking its ❌ button.');
        return;
      }

      const pagesStr = Array.from(markedDeletePages).sort((a,b)=>a-b).join(', ');

      const formData = new FormData();
      formData.append('pdf', currentDeleteFile);
      formData.append('pages', pagesStr);

      document.getElementById('delete-file-config').style.display = 'none';
      const procEl = document.getElementById('delete-proc');
      procEl.style.display = 'block';

      fetch('/api/delete-pages', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Deletion failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('delete-result-card').style.display = 'block';
        currentDeleteBlobUrl = URL.createObjectURL(blob);
        document.getElementById('delete-result-sub').textContent = `Cleaned PDF ready (${(blob.size / 1024).toFixed(0)} KB). Removed pages: ${pagesStr}`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetDeleteView();
      });
    }
    """

    return render_layout(
        title="Delete PDF Pages",
        active_tool="pdf-tools",
        hero_title="Delete PDF Pages",
        hero_sub="Remove unwanted pages from PDF files with <strong>visual thumbnail selection and instant deletion</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
