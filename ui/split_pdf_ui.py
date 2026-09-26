"""
Removix UI - Split PDF View with Thumbnail Strip, Checkboxes & Large Viewer
"""
from ui.layout import render_layout, render_processing_component

PDF_SPLIT_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/></svg>"""

def render_split_pdf_page() -> str:
    """Renders the Split PDF tool view."""
    processing_card = render_processing_component(
        component_id="split-proc",
        badge_text="PDF SPLITTER",
        badge_icon_svg=PDF_SPLIT_BADGE_SVG,
        title_text="Splitting PDF Document...",
        subtitle_text="Extracting document pages while preserving original quality and structure.",
        steps=[
            "Reading document",
            "Analyzing pages",
            "Extracting selection",
            "Packaging output",
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
      #split-large-canvas {{
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
    <div id="dropzone-split" class="dropzone-box" onclick="document.getElementById('file-input-split').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose PDF File</span>
      </div>
      <p class="drop-primary">Drop your PDF document here, or browse</p>
      <p class="drop-secondary">Extract specific pages with visual checkbox selection or page range input</p>
    </div>
    <input type="file" id="file-input-split" accept=".pdf,application/pdf" onchange="handleSplitUpload(this.files[0])">

    <!-- Active PDF Split Workspace -->
    <div id="split-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/></svg>
          </div>
          <div>
            <p id="split-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">Document.pdf</p>
            <p id="split-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <div style="display:flex; gap:10px;">
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="selectAllPages(true)">Select All</button>
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="selectAllPages(false)">Clear Selection</button>
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetSplitView()">Change File</button>
        </div>
      </div>

      <!-- Range Input & Counter Bar -->
      <div style="margin-top:16px; padding:12px 16px; background:var(--bg-page); border:1px solid var(--line); border-radius:12px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:10px; flex:1; min-width:240px;">
          <label style="font-size:12.5px; font-weight:700; color:var(--ink); white-space:nowrap;">Page Range:</label>
          <input type="text" id="split-range-input" placeholder="e.g. 1-3, 5" style="flex:1; padding:7px 12px; border:1px solid var(--line); border-radius:8px; font-size:13px; background:var(--bg-card); color:var(--ink); outline:none;" oninput="onRangeInputManual(this.value)">
        </div>
        <span id="split-selected-count" style="font-size:12px; font-weight:700; color:var(--primary); background:var(--sky-light); padding:4px 10px; border-radius:9999px;">0 pages selected</span>
      </div>

      <!-- PDF Preview Component: Left Thumbnails + Right Large Viewer -->
      <div class="pdf-preview-layout">
        <!-- Left: Thumbnail Strip -->
        <div class="pdf-thumb-strip" id="split-thumb-strip">
          <!-- Thumbnails rendered dynamically -->
        </div>

        <!-- Right: Large Viewer -->
        <div class="pdf-main-viewer">
          <div class="pdf-viewer-bar">
            <div>
              <span id="split-page-indicator" style="font-size:13px; font-weight:700; color:var(--ink);">Page 1 of 1</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <button type="button" id="btn-toggle-select-curr" class="btn-rot-mini" onclick="toggleCurrentPageSelect()">
                Toggle Select
              </button>
              <div style="width:1px; height:18px; background:var(--line); margin:0 4px;"></div>
              <button type="button" class="btn-rot-mini" onclick="zoomPdf(-0.25)">−</button>
              <span id="split-zoom-label" style="font-size:11.5px; font-weight:700; color:var(--ink-muted); min-width:38px; text-align:center;">100%</span>
              <button type="button" class="btn-rot-mini" onclick="zoomPdf(0.25)">+</button>
            </div>
          </div>
          <div class="pdf-viewer-canvas-stage" id="split-viewer-canvas-stage" title="Double click to reset zoom">
            <div class="pdf-canvas-pan-wrap" id="split-canvas-pan-wrap">
              <canvas id="split-large-canvas"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-split" style="padding:12px 28px; font-size:14px;" onclick="executePdfSplit()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/></svg>
          Split PDF
        </button>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card -->
    <div id="split-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Pages Extracted Successfully!</h3>
      <p id="split-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your split document files are ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-split" style="width: 215px;">
            <input type="checkbox" class="input" id="dl-checkbox-split" />
            <span class="circle">
              <svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"></path>
              </svg>
              <div class="square"></div>
            </span>
            <p class="title">Download Split Files</p>
            <p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetSplitView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Split Another PDF
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Checkbox Selection</h3>
          <p>Click checkboxes directly on each thumbnail to extract only the exact pages you need.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>100% Private</h3>
          <p>Pages render locally in your browser so confidential files never leave your device.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Lightning Fast</h3>
          <p>Instant page extraction and ZIP packaging completed in your browser session.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let currentSplitFile = null;
    let splitPdfDoc = null;
    let totalSplitPages = 0;
    let activeSplitPage = 1;
    let selectedSplitPages = new Set();
    let splitZoom = 1.0;
    let currentSplitBlobUrl = '';
    let isSplitDownloadComplete = false;
    let splitRenderTask = null;

    let splitPanX = 0, splitPanY = 0;
    let isSplitDragging = false, splitDragStartX = 0, splitDragStartY = 0;
    let splitTouchStartX = 0, splitTouchStartY = 0;
    let splitInitialPinchDist = 0, splitPinchStartZoom = 1.0;
    let isSplitTouching = false;

    const splitThumbStrip = document.getElementById('split-thumb-strip');
    const splitPageIndicator = document.getElementById('split-page-indicator');
    const splitZoomLabel = document.getElementById('split-zoom-label');
    const splitLargeCanvas = document.getElementById('split-large-canvas');
    const splitStage = document.getElementById('split-viewer-canvas-stage');
    const splitPanWrap = document.getElementById('split-canvas-pan-wrap');
    const splitSelectedCount = document.getElementById('split-selected-count');
    const splitRangeInput = document.getElementById('split-range-input');
    const btnToggleSelectCurr = document.getElementById('btn-toggle-select-curr');

    function handleSplitUpload(file) {
      if (!file) return;
      currentSplitFile = file;
      document.getElementById('dropzone-split').style.display = 'none';
      document.getElementById('split-doc-name').textContent = file.name;
      document.getElementById('split-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('split-file-config').style.display = 'block';

      loadPdfForSplit(file);
    }

    function loadPdfForSplit(file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const typedArray = new Uint8Array(e.target.result);
        if (window.pdfjsLib) {
          pdfjsLib.getDocument({ data: typedArray }).promise.then(function(doc) {
            splitPdfDoc = doc;
            totalSplitPages = doc.numPages;
            selectedSplitPages.clear();
            for (let i = 1; i <= totalSplitPages; i++) {
              selectedSplitPages.add(i);
            }
            renderSplitThumbnails();
            showSplitLargePage(1);
            updateSelectedUI();
          }).catch(function(err) {
            alert('This file could not be opened. Please try another PDF file.');
            resetSplitView();
          });
        }
      };
      reader.readAsArrayBuffer(file);
    }

    function renderSplitThumbnails() {
      splitThumbStrip.innerHTML = '';
      for (let p = 1; p <= totalSplitPages; p++) {
        (function(pageNum) {
          const card = document.createElement('div');
          card.className = 'pdf-thumb-card' + (pageNum === activeSplitPage ? ' active' : '') + (selectedSplitPages.has(pageNum) ? ' selected-page' : '');
          card.id = 'split-card-' + pageNum;
          card.onclick = function(e) {
            if (e.target.classList.contains('thumb-checkbox')) return;
            showSplitLargePage(pageNum);
          };

          const chk = document.createElement('input');
          chk.type = 'checkbox';
          chk.className = 'thumb-checkbox';
          chk.id = 'split-chk-' + pageNum;
          chk.checked = selectedSplitPages.has(pageNum);
          chk.onclick = function(e) {
            e.stopPropagation();
            togglePageSelection(pageNum, chk.checked);
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
          splitThumbStrip.appendChild(card);

          // Render thumbnail
          splitPdfDoc.getPage(pageNum).then(function(page) {
            const viewport = page.getViewport({ scale: 0.25 });
            canvas.width = viewport.width;
            canvas.height = viewport.height;
            const ctx = canvas.getContext('2d');
            page.render({ canvasContext: ctx, viewport: viewport });
          });
        })(p);
      }
    }

    function togglePageSelection(pageNum, isSelected) {
      if (isSelected) {
        selectedSplitPages.add(pageNum);
      } else {
        selectedSplitPages.delete(pageNum);
      }
      const card = document.getElementById('split-card-' + pageNum);
      if (card) {
        card.classList.toggle('selected-page', isSelected);
      }
      updateSelectedUI();
    }

    function toggleCurrentPageSelect() {
      const isSel = selectedSplitPages.has(activeSplitPage);
      togglePageSelection(activeSplitPage, !isSel);
      const chk = document.getElementById('split-chk-' + activeSplitPage);
      if (chk) chk.checked = !isSel;
    }

    function selectAllPages(select) {
      selectedSplitPages.clear();
      if (select) {
        for (let i = 1; i <= totalSplitPages; i++) selectedSplitPages.add(i);
      }
      for (let p = 1; p <= totalSplitPages; p++) {
        const card = document.getElementById('split-card-' + p);
        const chk = document.getElementById('split-chk-' + p);
        if (card) card.classList.toggle('selected-page', select);
        if (chk) chk.checked = select;
      }
      updateSelectedUI();
    }

    function updateSelectedUI() {
      const count = selectedSplitPages.size;
      splitSelectedCount.textContent = `${count} page${count === 1 ? '' : 's'} selected`;

      // Update range input text
      const sorted = Array.from(selectedSplitPages).sort((a,b)=>a-b);
      splitRangeInput.value = formatRanges(sorted);

      if (btnToggleSelectCurr) {
        btnToggleSelectCurr.textContent = selectedSplitPages.has(activeSplitPage) ? '✓ Deselect Page' : '+ Select Page';
      }
    }

    function formatRanges(pages) {
      if (!pages.length) return '';
      let ranges = [];
      let start = pages[0], end = pages[0];
      for (let i = 1; i < pages.length; i++) {
        if (pages[i] === end + 1) {
          end = pages[i];
        } else {
          ranges.push(start === end ? `${start}` : `${start}-${end}`);
          start = end = pages[i];
        }
      }
      ranges.push(start === end ? `${start}` : `${start}-${end}`);
      return ranges.join(', ');
    }

    function onRangeInputManual(str) {
      if (!totalSplitPages) return;
      selectedSplitPages.clear();
      const parts = str.split(',');
      parts.forEach(pt => {
        pt = pt.trim();
        if (pt.includes('-')) {
          const b = pt.split('-');
          if (b.length === 2 && !isNaN(b[0]) && !isNaN(b[1])) {
            const s = Math.max(1, parseInt(b[0]));
            const e = Math.min(totalSplitPages, parseInt(b[1]));
            for (let i = s; i <= e; i++) selectedSplitPages.add(i);
          }
        } else if (!isNaN(pt) && pt !== '') {
          const v = parseInt(pt);
          if (v >= 1 && v <= totalSplitPages) selectedSplitPages.add(v);
        }
      });

      for (let p = 1; p <= totalSplitPages; p++) {
        const isSel = selectedSplitPages.has(p);
        const card = document.getElementById('split-card-' + p);
        const chk = document.getElementById('split-chk-' + p);
        if (card) card.classList.toggle('selected-page', isSel);
        if (chk) chk.checked = isSel;
      }
      splitSelectedCount.textContent = `${selectedSplitPages.size} page${selectedSplitPages.size === 1 ? '' : 's'} selected`;
    }

    function updateSplitZoomUI() {
      if (splitZoomLabel) {
        splitZoomLabel.textContent = Math.round(splitZoom * 100) + '%';
      }
      if (splitZoom <= 1.0) {
        splitPanX = 0;
        splitPanY = 0;
      } else if (splitStage && splitLargeCanvas) {
        const curW = (splitLargeCanvas.offsetWidth || 300) * splitZoom;
        const curH = (splitLargeCanvas.offsetHeight || 400) * splitZoom;
        const stW = splitStage.clientWidth || 600;
        const stH = splitStage.clientHeight || 480;
        const maxPanX = Math.max(0, (curW - stW) / 2 + 80);
        const maxPanY = Math.max(0, (curH - stH) / 2 + 80);
        splitPanX = Math.max(-maxPanX, Math.min(maxPanX, splitPanX));
        splitPanY = Math.max(-maxPanY, Math.min(maxPanY, splitPanY));
      }
      if (splitPanWrap) {
        splitPanWrap.style.transform = `translate(${splitPanX}px, ${splitPanY}px) scale(${splitZoom})`;
      }
      if (splitStage) {
        splitStage.style.cursor = splitZoom > 1.0 ? (isSplitDragging ? 'grabbing' : 'grab') : 'default';
      }
    }

    function zoomPdf(delta) {
      splitZoom = Math.max(0.5, Math.min(2.5, +(splitZoom + delta).toFixed(2)));
      updateSplitZoomUI();
    }

    function resetSplitZoomAndPan() {
      splitZoom = 1.0;
      splitPanX = 0;
      splitPanY = 0;
      updateSplitZoomUI();
    }

    function showSplitLargePage(pageNum) {
      if (!splitPdfDoc || pageNum < 1 || pageNum > totalSplitPages) return;
      activeSplitPage = pageNum;
      resetSplitZoomAndPan();
      splitPageIndicator.textContent = `Page ${pageNum} of ${totalSplitPages}`;

      document.querySelectorAll('#split-thumb-strip .pdf-thumb-card').forEach((el, idx) => {
        el.classList.toggle('active', (idx + 1) === pageNum);
      });

      if (btnToggleSelectCurr) {
        btnToggleSelectCurr.textContent = selectedSplitPages.has(activeSplitPage) ? '✓ Deselect Page' : '+ Select Page';
      }

      if (splitRenderTask) {
        splitRenderTask.cancel();
        splitRenderTask = null;
      }

      splitPdfDoc.getPage(pageNum).then(function(page) {
        const stageH = splitStage ? splitStage.clientHeight : 480;
        const stageW = splitStage ? splitStage.clientWidth : 600;
        const maxFitH = Math.max(260, stageH - 40);
        const maxFitW = Math.max(260, stageW - 40);

        const baseViewport = page.getViewport({ scale: 1.0 });
        const fitScale = Math.min(maxFitW / baseViewport.width, maxFitH / baseViewport.height);
        const dpr = Math.max(window.devicePixelRatio || 1, 2);
        const renderViewport = page.getViewport({ scale: fitScale * dpr });

        splitLargeCanvas.width = renderViewport.width;
        splitLargeCanvas.height = renderViewport.height;
        splitLargeCanvas.style.width = Math.round(baseViewport.width * fitScale) + 'px';
        splitLargeCanvas.style.height = Math.round(baseViewport.height * fitScale) + 'px';

        const ctx = splitLargeCanvas.getContext('2d');
        splitRenderTask = page.render({ canvasContext: ctx, viewport: renderViewport });
        splitRenderTask.promise.then(function() {
          splitRenderTask = null;
          updateSplitZoomUI();
        }).catch(function(err) {
          if (err && err.name !== 'RenderingCancelledException') {
            console.error('Render error:', err);
          }
        });
      });
    }

    if (splitStage) {
      splitStage.addEventListener('dblclick', function(e) {
        e.preventDefault();
        resetSplitZoomAndPan();
      });

      splitStage.addEventListener('mousedown', function(e) {
        if (e.button !== 0 || splitZoom <= 1.0) return;
        isSplitDragging = true;
        splitDragStartX = e.clientX - splitPanX;
        splitDragStartY = e.clientY - splitPanY;
        if (splitPanWrap) splitPanWrap.classList.add('is-dragging');
        splitStage.style.cursor = 'grabbing';
        e.preventDefault();
      });

      window.addEventListener('mousemove', function(e) {
        if (!isSplitDragging) return;
        splitPanX = e.clientX - splitDragStartX;
        splitPanY = e.clientY - splitDragStartY;
        updateSplitZoomUI();
      });

      window.addEventListener('mouseup', function() {
        if (!isSplitDragging) return;
        isSplitDragging = false;
        if (splitPanWrap) splitPanWrap.classList.remove('is-dragging');
        if (splitStage) splitStage.style.cursor = splitZoom > 1.0 ? 'grab' : 'default';
      });

      splitStage.addEventListener('touchstart', function(e) {
        if (e.touches.length === 1) {
          if (splitZoom > 1.0) {
            isSplitTouching = true;
            splitTouchStartX = e.touches[0].clientX - splitPanX;
            splitTouchStartY = e.touches[0].clientY - splitPanY;
            if (splitPanWrap) splitPanWrap.classList.add('is-dragging');
          }
        } else if (e.touches.length === 2) {
          isSplitTouching = false;
          if (splitPanWrap) splitPanWrap.classList.add('is-dragging');
          splitInitialPinchDist = Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
          );
          splitPinchStartZoom = splitZoom;
        }
      }, { passive: false });

      splitStage.addEventListener('touchmove', function(e) {
        if (e.touches.length === 1 && isSplitTouching && splitZoom > 1.0) {
          splitPanX = e.touches[0].clientX - splitTouchStartX;
          splitPanY = e.touches[0].clientY - splitTouchStartY;
          updateSplitZoomUI();
          e.preventDefault();
        } else if (e.touches.length === 2 && splitInitialPinchDist > 0) {
          const currentDist = Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
          );
          const zoomFactor = currentDist / splitInitialPinchDist;
          splitZoom = Math.max(0.5, Math.min(2.5, +(splitPinchStartZoom * zoomFactor).toFixed(2)));
          updateSplitZoomUI();
          e.preventDefault();
        }
      }, { passive: false });

      splitStage.addEventListener('touchend', function(e) {
        if (e.touches.length === 0) {
          isSplitTouching = false;
          splitInitialPinchDist = 0;
          if (splitPanWrap) splitPanWrap.classList.remove('is-dragging');
        } else if (e.touches.length === 1) {
          splitInitialPinchDist = 0;
          if (splitZoom > 1.0) {
            isSplitTouching = true;
            touchStartX = e.touches[0].clientX - splitPanX;
            touchStartY = e.touches[0].clientY - splitPanY;
          }
        }
      });

      splitStage.addEventListener('wheel', function(e) {
        if (e.ctrlKey) {
          e.preventDefault();
          const delta = e.deltaY < 0 ? 0.25 : -0.25;
          zoomPdf(delta);
        }
      }, { passive: false });
    }

    function triggerSplitDownload() {
      if (!currentSplitBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentSplitBlobUrl;
      a.download = 'removix_split_' + (currentSplitFile ? currentSplitFile.name : 'doc.zip');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxSplit = document.getElementById('dl-checkbox-split');
    const dlLabelSplit = document.getElementById('dl-label-split');
    if (dlCheckboxSplit) {
      dlCheckboxSplit.addEventListener('change', () => {
        if (dlCheckboxSplit.checked) {
          if (dlLabelSplit) dlLabelSplit.classList.add('is-checked');
          triggerSplitDownload();
          setTimeout(() => { isSplitDownloadComplete = true; }, 2350);
        }
      });
      dlCheckboxSplit.addEventListener('click', (e) => {
        if (isSplitDownloadComplete) { e.preventDefault(); triggerSplitDownload(); }
      });
    }

    function resetSplitView() {
      currentSplitFile = null;
      splitPdfDoc = null;
      selectedSplitPages.clear();
      resetSplitZoomAndPan();
      document.getElementById('split-result-card').style.display = 'none';
      document.getElementById('split-proc').style.display = 'none';
      document.getElementById('split-file-config').style.display = 'none';
      document.getElementById('dropzone-split').style.display = '';
      const inputEl = document.getElementById('file-input-split');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxSplit) dlCheckboxSplit.checked = false;
      if (dlLabelSplit) dlLabelSplit.classList.remove('is-checked');
      isSplitDownloadComplete = false;
      if (currentSplitBlobUrl) { URL.revokeObjectURL(currentSplitBlobUrl); currentSplitBlobUrl = ''; }
      splitThumbStrip.innerHTML = '';
    }

    function executePdfSplit() {
      if (!currentSplitFile) return;

      if (selectedSplitPages.size === 0) {
        alert('Please select at least one page to extract.');
        return;
      }

      const isAll = selectedSplitPages.size === totalSplitPages;
      const rangeVal = formatRanges(Array.from(selectedSplitPages).sort((a,b)=>a-b));

      const formData = new FormData();
      formData.append('pdf', currentSplitFile);
      formData.append('mode', isAll ? 'all' : 'range');
      if (!isAll) {
        formData.append('range', rangeVal);
      }

      document.getElementById('split-file-config').style.display = 'none';
      const procEl = document.getElementById('split-proc');
      procEl.style.display = 'block';

      fetch('/api/split-pdf', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Splitting failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('split-result-card').style.display = 'block';
        currentSplitBlobUrl = URL.createObjectURL(blob);
        document.getElementById('split-result-sub').textContent = `Extraction complete (${(blob.size / 1024).toFixed(0)} KB). Selected pages: ${rangeVal}`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetSplitView();
      });
    }
    """

    return render_layout(
        title="Split PDF",
        active_tool="pdf-tools",
        hero_title="Split PDF Document",
        hero_sub="Separate PDF pages with <strong>visual thumbnail checkboxes and custom page range extraction</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
