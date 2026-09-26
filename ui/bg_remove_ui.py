"""
Removix UI - Background Remover View
------------------------------------
Interactive interface for AI background removal & matting.
Options:
- Fast Mode (1024px) vs HD Mode (2048px)
- Transparent PNG output with checkerboard pattern preview
- First-run model download progress handling
- Dedicated processing steps: "Loading model" → "Analyzing image" → "Removing background" → "Refining edges" → "Done"
"""

from ui.layout import render_layout, render_processing_component

BG_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12" stroke-linecap="round" stroke-linejoin="round"/></svg>"""


def render_bg_remove_page() -> str:
    """Renders the AI Background Remover page."""
    processing_card = render_processing_component(
        component_id="bg-proc",
        badge_text="BACKGROUND REMOVER",
        badge_icon_svg=BG_BADGE_SVG,
        title_text="Extracting Transparent Subject...",
        subtitle_text="Segmenting fine hair, edges, and complex backgrounds cleanly with AI.",
        steps=[
            "Initializing engine",
            "Analyzing image",
            "Removing background",
            "Refining edges",
            "Done",
        ],
    )

    main_card_html = f"""
    <!-- Mode Selection Pills (Fast 1024px vs HD 2048px) -->
    <div class="zone-pills-bar" id="bg-mode-bar" style="margin-bottom:18px;">
      <span class="zone-label">Resolution Mode:</span>
      <button type="button" class="zone-pill active" id="btn-mode-fast" onclick="setBgMode('fast')">Fast Mode (1024px • Instant)</button>
      <button type="button" class="zone-pill" id="btn-mode-hd" onclick="setBgMode('hd')">HD Mode (2048px • Maximum Detail)</button>
    </div>

    <!-- Model Download Progress Banner (Shown if model not ready) -->
    <div id="model-download-card" style="display:none; margin-bottom:20px; padding:18px 20px; background:#eff6ff; border:1px solid #bfdbfe; border-radius:16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span style="font-size:13.5px; font-weight:700; color:#1e40af;">First-Run: Preparing AI Removal Engine</span>
        <span id="model-dl-pct" style="font-size:13px; font-weight:800; color:#1d4ed8;">0%</span>
      </div>
      <div class="progress-bar-wrap" style="margin:8px 0;"><div class="progress-bar-fill" id="model-dl-bar" style="width:0%;"></div></div>
      <p id="model-dl-info" style="font-size:12px; color:#3b82f6;">Downloading AI components... (One-time setup)</p>
    </div>

    <!-- Dropzone View -->
    <div id="dropzone-bg" class="dropzone-box" onclick="document.getElementById('file-input-bg').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose Photo</span>
      </div>
      <p class="drop-primary">Drop portrait, product, or photo here, or browse</p>
      <p class="drop-secondary">Supports PNG, JPG, JPEG, WEBP • Auto transparent cutout</p>
    </div>
    <input type="file" id="file-input-bg" accept=".png,.jpg,.jpeg,.webp" onchange="handleBgFile(this.files[0])">

    <!-- Selected Image Confirmation & Action Card -->
    <div id="bg-config-card" style="display:none; margin-top:20px; padding:20px 22px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:14px; overflow:hidden;">
          <img id="bg-thumb-preview" src="" style="width:52px; height:52px; object-fit:cover; border-radius:10px; border:1px solid #cbd5e1; background:#ffffff; flex-shrink:0;">
          <div style="overflow:hidden;">
            <p id="bg-doc-name" style="font-size:15px; font-weight:700; color:var(--ink); margin-bottom:3px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap; max-width:380px;">photo.jpg</p>
            <p id="bg-doc-info" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready for cutout</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetBgView()">Change Image</button>
      </div>

      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-bg" onclick="executeBgRemoval()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12"/></svg>
          <span id="btn-bg-label">Remove Background (Fast Mode)</span>
        </button>
      </div>
    </div>

    <!-- Dedicated Processing View (Custom Background Remover UI) -->
    {processing_card}

    <!-- Result View with Transparent Checkerboard Preview -->
    <div id="bg-result-card" style="display:none; margin-top:24px; text-align:center;">
      <div style="display:inline-block; position:relative; padding:16px; background:#ffffff; border:1px solid #e2e8f0; border-radius:20px; box-shadow:0 10px 32px rgba(15,23,42,0.08); margin-bottom:20px; max-width:100%; box-sizing:border-box;">
        <!-- Checkerboard container for showing transparency -->
        <div class="checkerboard-bg" style="border-radius:12px; overflow:hidden; display:flex; align-items:center; justify-content:center; padding:12px; min-height:220px; border:1px solid #e2e8f0;">
          <img id="bg-result-img" src="" alt="Transparent Cutout" style="max-width:100%; max-height:420px; width:auto; height:auto; display:block; object-fit:contain;">
        </div>
      </div>

      <div>
        <div class="result-actions">
          <div class="container">
            <label class="label" id="dl-label-bg" style="width: 235px;">
              <input type="checkbox" class="input" id="dl-checkbox-bg" />
              <span class="circle">
                <svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"></path>
                </svg>
                <div class="square"></div>
              </span>
              <p class="title">Download Transparent PNG</p>
              <p class="title">Open</p>
            </label>
          </div>
          <button type="button" class="btn-reset" onclick="resetBgView()">
            <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
            Remove Another Background
          </button>
        </div>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Neural Edge Matting</h3>
          <p>Intelligent neural network cleanly isolates intricate strands of hair, fur, and complex edges.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>HD 2048px Resolution</h3>
          <p>Preserves pristine edges on high-megapixel e-commerce photos and professional studio portraits.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>100% Offline Processing</h3>
          <p>Runs 100% locally on your device with zero cloud data transfer for total privacy.</p>
        </div>
      </div>
    </section>
    """

    extra_css = r"""
    .checkerboard-bg {
      background-color: #ffffff;
      background-image:
        linear-gradient(45deg, #e2e8f0 25%, transparent 25%),
        linear-gradient(-45deg, #e2e8f0 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #e2e8f0 75%),
        linear-gradient(-45deg, transparent 75%, #e2e8f0 75%);
      background-size: 20px 20px;
      background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
    }
    html.dark-mode .checkerboard-bg,
    body.dark-mode .checkerboard-bg {
      background-color: #0f172a !important;
      background-image:
        linear-gradient(45deg, #1e293b 25%, transparent 25%),
        linear-gradient(-45deg, #1e293b 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #1e293b 75%),
        linear-gradient(-45deg, transparent 75%, #1e293b 75%) !important;
    }
    """

    client_js = r"""
    let currentBgMode = 'fast';
    let currentBgFile = null;
    let modelPollTimer = null;

    // Check model status on page load
    checkModelStatus();

    function checkModelStatus() {
      fetch('/api/bg-remove/model-status')
        .then(r => r.json())
        .then(data => {
          const card = document.getElementById('model-download-card');
          if (!data.ready) {
            card.style.display = 'block';
            document.getElementById('model-dl-pct').textContent = Math.round(data.percent) + '%';
            document.getElementById('model-dl-bar').style.width = data.percent + '%';
            if (data.is_downloading) {
              const mb = (data.downloaded_bytes / (1024 * 1024)).toFixed(1);
              const totalMb = (data.total_bytes / (1024 * 1024)).toFixed(1);
              document.getElementById('model-dl-info').textContent = `Downloading AI components (${mb} MB / ${totalMb} MB)...`;
              if (!modelPollTimer) {
                modelPollTimer = setInterval(checkModelStatus, 1500);
              }
            } else {
              document.getElementById('model-dl-info').textContent = 'AI engine will initialize automatically when you click Remove Background.';
              if (modelPollTimer) { clearInterval(modelPollTimer); modelPollTimer = null; }
            }
          } else {
            card.style.display = 'none';
            if (modelPollTimer) { clearInterval(modelPollTimer); modelPollTimer = null; }
          }
        })
        .catch(() => {});
    }

    // Drag and Drop listeners
    const dropzoneBg = document.getElementById('dropzone-bg');
    if (dropzoneBg) {
      ['dragenter', 'dragover'].forEach(evt => {
        dropzoneBg.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneBg.classList.add('dragover');
        });
      });
      ['dragleave', 'drop'].forEach(evt => {
        dropzoneBg.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneBg.classList.remove('dragover');
        });
      });
      dropzoneBg.addEventListener('drop', e => {
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          handleBgFile(e.dataTransfer.files[0]);
        }
      });
    }

    function setBgMode(mode) {
      currentBgMode = mode;
      document.getElementById('btn-mode-fast').classList.toggle('active', mode === 'fast');
      document.getElementById('btn-mode-hd').classList.toggle('active', mode === 'hd');
      const label = document.getElementById('btn-bg-label');
      if (label) {
        label.textContent = `Remove Background (${mode === 'hd' ? 'HD 2048px' : 'Fast 1024px'})`;
      }
    }

    let currentBgBlobUrl = '';
    let currentBgFileName = '';
    let isBgDownloadComplete = false;

    function triggerBgDownload() {
      if (!currentBgBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentBgBlobUrl;
      a.download = currentBgFileName || 'removix_transparent.png';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxBg = document.getElementById('dl-checkbox-bg');
    const dlLabelBg = document.getElementById('dl-label-bg');
    if (dlCheckboxBg) {
      dlCheckboxBg.addEventListener('change', () => {
        if (dlCheckboxBg.checked) {
          if (dlLabelBg) dlLabelBg.classList.add('is-checked');
          triggerBgDownload();
          setTimeout(() => {
            isBgDownloadComplete = true;
          }, 2350);
        }
      });
      dlCheckboxBg.addEventListener('click', (e) => {
        if (isBgDownloadComplete) {
          e.preventDefault();
          triggerBgDownload();
        }
      });
    }

    function resetBgView() {
      currentBgFile = null;
      document.getElementById('bg-result-card').style.display = 'none';
      document.getElementById('bg-proc').style.display = 'none';
      document.getElementById('bg-config-card').style.display = 'none';
      document.getElementById('dropzone-bg').style.display = '';
      const inputEl = document.getElementById('file-input-bg');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxBg) dlCheckboxBg.checked = false;
      if (dlLabelBg) dlLabelBg.classList.remove('is-checked');
      isBgDownloadComplete = false;
      if (currentBgBlobUrl) {
        URL.revokeObjectURL(currentBgBlobUrl);
        currentBgBlobUrl = '';
      }
    }

    function handleBgFile(file) {
      if (!file) return;
      currentBgFile = file;

      document.getElementById('dropzone-bg').style.display = 'none';
      document.getElementById('bg-doc-name').textContent = file.name;
      document.getElementById('bg-doc-info').textContent = `${(file.size / 1024).toFixed(0)} KB • Ready for cutout`;
      document.getElementById('bg-thumb-preview').src = URL.createObjectURL(file);
      document.getElementById('bg-config-card').style.display = 'block';
    }

    function setBgProgress(stepIdx, pct, title) {
      const compId = 'bg-proc';
      const bar = document.getElementById(`${compId}-bar`);
      const pctEl = document.getElementById(`${compId}-pct`);
      const stageTitle = document.getElementById(`${compId}-stage-title`);

      if (bar) bar.style.width = pct + '%';
      if (pctEl) pctEl.textContent = Math.round(pct) + '%';
      if (stageTitle && title) stageTitle.textContent = title + '...';

      for (let i = 1; i <= 5; i++) {
        const stepRow = document.getElementById(`${compId}-step-${i}`);
        if (!stepRow) continue;
        stepRow.classList.remove('active', 'done');
        if (i < stepIdx) {
          stepRow.classList.add('done');
        } else if (i === stepIdx) {
          stepRow.classList.add('active');
        }
      }
    }

    function executeBgRemoval() {
      if (!currentBgFile) return;

      const formData = new FormData();
      formData.append('image', currentBgFile);
      formData.append('mode', currentBgMode);

      document.getElementById('bg-config-card').style.display = 'none';
      const procEl = document.getElementById('bg-proc');
      procEl.style.display = 'block';

      // Step 1: Loading model
      setBgProgress(1, 15, 'Loading model');

      const t1 = setTimeout(() => {
        // Step 2: Analyzing image
        setBgProgress(2, 40, 'Analyzing image');
      }, 700);

      const t2 = setTimeout(() => {
        // Step 3: Removing background
        setBgProgress(3, 70, 'Removing background');
      }, 1500);

      const t3 = setTimeout(() => {
        // Step 4: Refining edges
        setBgProgress(4, 90, 'Refining edges');
      }, 2400);

      fetch('/api/bg-remove', {
        method: 'POST',
        body: formData
      })
      .then(res => {
        clearTimeout(t1);
        clearTimeout(t2);
        clearTimeout(t3);
        setBgProgress(5, 98, 'Done');
        if (!res.ok) {
          return res.json().then(e => { throw new Error(e.error || 'Background removal failed'); });
        }
        return res.blob();
      })
      .then(blob => {
        setBgProgress(5, 100, 'Done');
        setTimeout(() => {
          procEl.style.display = 'none';
          document.getElementById('bg-result-card').style.display = 'block';
          
          if (dlCheckboxBg) dlCheckboxBg.checked = false;
          if (dlLabelBg) dlLabelBg.classList.remove('is-checked');
          isBgDownloadComplete = false;

          const resultImg = document.getElementById('bg-result-img');
          currentBgBlobUrl = URL.createObjectURL(blob);
          resultImg.src = currentBgBlobUrl;
          const stem = currentBgFile.name.replace(/\.[^/.]+$/, "");
          currentBgFileName = `removix_transparent.png`;

          document.getElementById('bg-result-meta').textContent = `Transparent cutout ready (${(blob.size / 1024).toFixed(0)} KB) • Mode: ${currentBgMode.toUpperCase()}`;
        }, 300);
      })
      .catch(err => {
        clearTimeout(t1);
        clearTimeout(t2);
        clearTimeout(t3);
        alert('Something went wrong, please try again.');
        resetBgView();
      });
    }
    """

    return render_layout(
        title="AI Background Remover",
        active_tool="bg-remove",
        hero_title="AI Background Remover",
        hero_sub="Extract portraits, people, and products with <strong>1-click transparent background</strong> cutout and razor-sharp edge matting.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_css=extra_css,
        extra_js=client_js,
    )
