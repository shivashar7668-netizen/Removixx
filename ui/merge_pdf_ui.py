"""
Removix UI - Merge PDF View with Visual Thumbnails & Drag-to-Reorder Grid
"""
from ui.layout import render_layout, render_processing_component

PDF_MERGE_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>"""

def render_merge_pdf_page() -> str:
    """Renders the Merge PDF tool page."""
    processing_card = render_processing_component(
        component_id="merge-proc",
        badge_text="PDF MERGER",
        badge_icon_svg=PDF_MERGE_BADGE_SVG,
        title_text="Merging PDF Documents...",
        subtitle_text="Combining pages, bookmarks, and vectors into a unified document.",
        steps=[
            "Reading documents",
            "Validating structure",
            "Merging pages",
            "Finalizing file",
        ],
    )

    main_card_html = f"""
    <style>
      .merge-grid-tray {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        gap: 16px;
        margin-top: 14px;
        max-height: 480px;
        overflow-y: auto;
        padding: 4px;
      }}
      .merge-card-item {{
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
      .merge-card-item:active {{
        cursor: grabbing;
      }}
      .merge-card-item.dragging {{
        opacity: 0.4;
        transform: scale(0.95);
      }}
      .merge-card-item.drag-over {{
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.3);
      }}
      .merge-order-badge {{
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
      .btn-merge-remove {{
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
      .btn-merge-remove:hover {{
        background: #ef4444;
        color: #ffffff;
      }}
      .merge-canvas-wrap {{
        width: 100%;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border-radius: 6px;
        background: #ffffff;
        margin-top: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
      }}
      body.dark-mode .merge-canvas-wrap {{
        background: #1e293b;
      }}
      .merge-canvas-wrap canvas {{
        max-width: 100%;
        max-height: 100%;
      }}
      .merge-doc-info {{
        width: 100%;
        margin-top: 8px;
        text-align: center;
      }}
      .merge-doc-name {{
        font-size: 12px;
        font-weight: 700;
        color: var(--ink);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: block;
      }}
      .merge-doc-meta {{
        font-size: 10.5px;
        color: var(--ink-muted);
        margin-top: 2px;
      }}
      .merge-card-arrows {{
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
    <div id="dropzone-merge" class="dropzone-box" onclick="document.getElementById('file-input-merge').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose PDF Files</span>
      </div>
      <p class="drop-primary">Drop PDF files here to merge, or browse</p>
      <p class="drop-secondary">Select multiple PDFs • Drag thumbnails to rearrange sequence</p>
    </div>
    <input type="file" id="file-input-merge" multiple accept=".pdf,application/pdf" onchange="handlePdfSelection(this.files)">

    <!-- Selected Files Reorder Tray -->
    <div id="merge-tray" style="display:none; margin-top:24px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding-bottom:12px; border-bottom:1px solid var(--line);">
        <h3 style="font-size:15px; font-weight:700; color:var(--ink);">
          Selected PDFs (<span id="pdf-count" style="color:var(--primary);">0</span>)
          <span style="font-size:12px; font-weight:500; color:var(--ink-muted); margin-left:8px;">Drag cards or use arrows to reorder</span>
        </h3>
        <div style="display:flex; gap:8px;">
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="document.getElementById('file-input-merge').click()">+ Add More</button>
          <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px; color:#dc2626;" onclick="clearMergeList()">Clear All</button>
        </div>
      </div>

      <div class="merge-grid-tray" id="merge-list"></div>

      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-merge-action" style="padding:12px 28px; font-size:14px;" onclick="executePdfMerge()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
          <span id="btn-merge-text">Merge PDFs</span>
        </button>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card -->
    <div id="merge-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">PDFs Merged Successfully!</h3>
      <p id="merge-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">All selected documents combined in your designated order.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-merge" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-merge" />
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
        <button type="button" class="btn-reset" onclick="resetMergeView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Merge Another PDF
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
          <p>Drag and drop document thumbnail cards to easily organize your final reading sequence.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>100% Private</h3>
          <p>Page thumbnails generate locally on your machine with zero server roundtrips.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Lossless Merging</h3>
          <p>Fonts, outlines, and embedded assets are merged natively with zero loss in resolution.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let selectedPdfMergeFiles = [];
    let dragSourceIndex = null;

    function handlePdfSelection(files) {
      if (!files || files.length === 0) return;
      for (let i = 0; i < files.length; i++) {
        if (files[i].type === 'application/pdf' || files[i].name.toLowerCase().endsWith('.pdf')) {
          selectedPdfMergeFiles.push(files[i]);
        }
      }
      renderMergeTray();
    }

    function renderMergeTray() {
      const tray = document.getElementById('merge-tray');
      const list = document.getElementById('merge-list');
      const countEl = document.getElementById('pdf-count');
      const dropzone = document.getElementById('dropzone-merge');

      if (selectedPdfMergeFiles.length === 0) {
        tray.style.display = 'none';
        dropzone.style.display = '';
        return;
      }

      dropzone.style.display = 'none';
      tray.style.display = 'block';
      countEl.textContent = selectedPdfMergeFiles.length;
      list.innerHTML = '';

      selectedPdfMergeFiles.forEach((file, idx) => {
        const item = document.createElement('div');
        item.className = 'merge-card-item';
        item.draggable = true;
        item.dataset.index = idx;

        // Drag events
        item.addEventListener('dragstart', (e) => {
          dragSourceIndex = idx;
          item.classList.add('dragging');
          e.dataTransfer.effectAllowed = 'move';
        });
        item.addEventListener('dragend', () => {
          item.classList.remove('dragging');
          document.querySelectorAll('.merge-card-item').forEach(el => el.classList.remove('drag-over'));
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
          if (dragSourceIndex !== null && dragSourceIndex !== idx) {
            const moved = selectedPdfMergeFiles.splice(dragSourceIndex, 1)[0];
            selectedPdfMergeFiles.splice(idx, 0, moved);
            renderMergeTray();
          }
        });

        // Order badge
        const badge = document.createElement('div');
        badge.className = 'merge-order-badge';
        badge.textContent = idx + 1;

        // Remove button
        const rmBtn = document.createElement('button');
        rmBtn.type = 'button';
        rmBtn.className = 'btn-merge-remove';
        rmBtn.innerHTML = '✕';
        rmBtn.title = 'Remove PDF';
        rmBtn.onclick = (e) => { e.stopPropagation(); removeMergePdf(idx); };

        // Canvas wrap
        const canvasWrap = document.createElement('div');
        canvasWrap.className = 'merge-canvas-wrap';
        const canvas = document.createElement('canvas');
        canvas.id = 'merge-thumb-' + idx;
        canvasWrap.appendChild(canvas);

        // Doc Info
        const info = document.createElement('div');
        info.className = 'merge-doc-info';
        const nameSpan = document.createElement('span');
        nameSpan.className = 'merge-doc-name';
        nameSpan.textContent = file.name;
        nameSpan.title = file.name;

        const metaSpan = document.createElement('div');
        metaSpan.className = 'merge-doc-meta';
        metaSpan.textContent = (file.size / 1024).toFixed(0) + ' KB';

        info.appendChild(nameSpan);
        info.appendChild(metaSpan);

        // Nudge arrows
        const arrows = document.createElement('div');
        arrows.className = 'merge-card-arrows';
        if (idx > 0) {
          const leftBtn = document.createElement('button');
          leftBtn.type = 'button';
          leftBtn.className = 'btn-nudge';
          leftBtn.innerHTML = '←';
          leftBtn.title = 'Move Left';
          leftBtn.onclick = (e) => { e.stopPropagation(); moveMergePdf(idx, -1); };
          arrows.appendChild(leftBtn);
        }
        if (idx < selectedPdfMergeFiles.length - 1) {
          const rightBtn = document.createElement('button');
          rightBtn.type = 'button';
          rightBtn.className = 'btn-nudge';
          rightBtn.innerHTML = '→';
          rightBtn.title = 'Move Right';
          rightBtn.onclick = (e) => { e.stopPropagation(); moveMergePdf(idx, 1); };
          arrows.appendChild(rightBtn);
        }

        item.appendChild(badge);
        item.appendChild(rmBtn);
        item.appendChild(canvasWrap);
        item.appendChild(info);
        item.appendChild(arrows);
        list.appendChild(item);

        // Render first page thumbnail via PDF.js
        renderFirstPageThumbnail(file, canvas, metaSpan);
      });
    }

    function renderFirstPageThumbnail(file, canvas, metaSpan) {
      const reader = new FileReader();
      reader.onload = function(e) {
        if (window.pdfjsLib) {
          const typedArray = new Uint8Array(e.target.result);
          pdfjsLib.getDocument({ data: typedArray }).promise.then(function(doc) {
            metaSpan.textContent = `${doc.numPages} pg • ${(file.size / 1024).toFixed(0)} KB`;
            doc.getPage(1).then(function(page) {
              const viewport = page.getViewport({ scale: 0.25 });
              canvas.width = viewport.width;
              canvas.height = viewport.height;
              const ctx = canvas.getContext('2d');
              page.render({ canvasContext: ctx, viewport: viewport });
            });
          }).catch(function(err) {});
        }
      };
      reader.readAsArrayBuffer(file);
    }

    function moveMergePdf(idx, delta) {
      const target = idx + delta;
      if (target < 0 || target >= selectedPdfMergeFiles.length) return;
      const tmp = selectedPdfMergeFiles[idx];
      selectedPdfMergeFiles[idx] = selectedPdfMergeFiles[target];
      selectedPdfMergeFiles[target] = tmp;
      renderMergeTray();
    }

    function removeMergePdf(idx) {
      selectedPdfMergeFiles.splice(idx, 1);
      renderMergeTray();
    }

    function clearMergeList() {
      selectedPdfMergeFiles = [];
      renderMergeTray();
    }

    let currentMergedPdfBlobUrl = '';
    let isMergeDownloadComplete = false;

    function triggerMergeDownload() {
      if (!currentMergedPdfBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentMergedPdfBlobUrl;
      a.download = 'removix_merged.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxMerge = document.getElementById('dl-checkbox-merge');
    const dlLabelMerge = document.getElementById('dl-label-merge');
    if (dlCheckboxMerge) {
      dlCheckboxMerge.addEventListener('change', () => {
        if (dlCheckboxMerge.checked) {
          if (dlLabelMerge) dlLabelMerge.classList.add('is-checked');
          triggerMergeDownload();
          setTimeout(() => { isMergeDownloadComplete = true; }, 2350);
        }
      });
      dlCheckboxMerge.addEventListener('click', (e) => {
        if (isMergeDownloadComplete) { e.preventDefault(); triggerMergeDownload(); }
      });
    }

    function resetMergeView() {
      clearMergeList();
      document.getElementById('merge-result-card').style.display = 'none';
      document.getElementById('merge-proc').style.display = 'none';
      document.getElementById('dropzone-merge').style.display = '';
      if (dlCheckboxMerge) dlCheckboxMerge.checked = false;
      if (dlLabelMerge) dlLabelMerge.classList.remove('is-checked');
      isMergeDownloadComplete = false;
      if (currentMergedPdfBlobUrl) { URL.revokeObjectURL(currentMergedPdfBlobUrl); currentMergedPdfBlobUrl = ''; }
    }

    function executePdfMerge() {
      if (selectedPdfMergeFiles.length < 2) {
        alert('Please select at least 2 PDF files to merge.');
        return;
      }

      const formData = new FormData();
      selectedPdfMergeFiles.forEach(file => {
        formData.append('files', file);
      });

      document.getElementById('merge-tray').style.display = 'none';
      const procEl = document.getElementById('merge-proc');
      procEl.style.display = 'block';

      fetch('/api/merge-pdf', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Merge failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('merge-result-card').style.display = 'block';
        currentMergedPdfBlobUrl = URL.createObjectURL(blob);
        document.getElementById('merge-result-sub').textContent = `Combined ${selectedPdfMergeFiles.length} files successfully (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetMergeView();
      });
    }
    """

    return render_layout(
        title="Merge PDF",
        active_tool="pdf-tools",
        hero_title="Merge PDF Files",
        hero_sub="Combine multiple PDF documents with <strong>interactive drag-to-reorder thumbnails</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
