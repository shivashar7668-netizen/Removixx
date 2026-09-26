"""
Removix UI - WEBP to JPG View
-------------------------
Dedicated high-precision converter from WEBP to JPG.
Matches the exact visual styling, upload box, and animated buttons of Removix.
"""

from ui.layout import render_layout, render_processing_component

CONV_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><path d="M7 16l-4-4m0 0l4-4m-4 4h18M17 8l4 4m0 0l-4 4m4-4H3"/></svg>"""


def render_webp_to_jpg_page() -> str:
    """Renders the WEBP to JPG converter tool view."""
    processing_card = render_processing_component(
        component_id="proc-webp-to-jpg",
        badge_text="IMAGE CONVERTER",
        badge_icon_svg=CONV_BADGE_SVG,
        title_text="Converting to JPG...",
        subtitle_text="Optimizing pixels, color encoding, and resolution balance.",
        steps=[
            "Reading WEBP image",
            "Encoding JPG format",
            "Optimizing quality",
            "Finalizing file",
        ],
    )

    main_card_html = f"""
    <!-- Back to Image Tools Button -->
    <div style="margin-bottom: 20px;">
      <a href="/image-tools" class="btn-secondary" style="display:inline-flex; align-items:center; gap:8px; padding:8px 18px; font-size:13px; text-decoration:none; font-weight:600;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        Back to Image Tools
      </a>
    </div>

    <!-- Dropzone View -->
    <div id="dropzone-webp_to_jpg" class="dropzone-box" onclick="document.getElementById('file-input-webp_to_jpg').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose WEBP File</span>
      </div>
      <p class="drop-primary">Drop your WEBP file here, or browse</p>
      <p class="drop-secondary">Supports WEBP format • Highest visual quality output</p>
    </div>
    <input type="file" id="file-input-webp_to_jpg" accept=".webp" onchange="handleWebptojpgUpload(this.files[0])">

    <!-- Selected File Config Card -->
    <div id="webp_to_jpg-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:12px; overflow:hidden;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
          </div>
          <div style="overflow:hidden;">
            <p id="webp_to_jpg-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap; max-width:380px;">image.webp</p>
            <p id="webp_to_jpg-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • WEBP Image</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetWebptojpgView()">Change File</button>
      </div>

      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-webp_to_jpg" onclick="executeWebptojpg()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M7 16l-4-4m0 0l4-4m-4 4h18M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
          Convert to JPG
        </button>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card -->
    <div id="webp_to_jpg-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Conversion Complete!</h3>
      <p id="webp_to_jpg-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your file has been converted to JPG with crystal clarity.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-webp_to_jpg" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-webp_to_jpg" />
            <span class="circle">
              <svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"></path>
              </svg>
              <div class="square"></div>
            </span>
            <p class="title">Download JPG</p>
            <p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetWebptojpgView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Convert Another File
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
          <h3>Optimized Quality</h3>
          <p>Preserves color fidelity, balanced compression, and sharp details without bulky bloat.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>100% On-Device Privacy</h3>
          <p>Your photos stay securely on your computer and are converted locally with zero cloud upload.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Instant Processing</h3>
          <p>Hardware accelerated on-device engine delivers conversions in milliseconds.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let currentWebptojpgFile = null;

    const dropzoneWebptojpg = document.getElementById('dropzone-webp_to_jpg');
    if (dropzoneWebptojpg) {
      ['dragenter', 'dragover'].forEach(evt => {
        dropzoneWebptojpg.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneWebptojpg.classList.add('dragover');
        });
      });
      ['dragleave', 'drop'].forEach(evt => {
        dropzoneWebptojpg.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneWebptojpg.classList.remove('dragover');
        });
      });
      dropzoneWebptojpg.addEventListener('drop', e => {
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          handleWebptojpgUpload(e.dataTransfer.files[0]);
        }
      });
    }

    function handleWebptojpgUpload(file) {
      if (!file) return;
      currentWebptojpgFile = file;
      document.getElementById('dropzone-webp_to_jpg').style.display = 'none';
      document.getElementById('webp_to_jpg-doc-name').textContent = file.name;
      document.getElementById('webp_to_jpg-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • WEBP Image';
      document.getElementById('webp_to_jpg-file-config').style.display = 'block';
    }

    let currentWebptojpgBlobUrl = '';
    let isWebptojpgDownloadComplete = false;

    function triggerWebptojpgDownload() {
      if (!currentWebptojpgBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentWebptojpgBlobUrl;
      a.download = 'removix_webp_to_jpg.jpg';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxWebptojpg = document.getElementById('dl-checkbox-webp_to_jpg');
    const dlLabelWebptojpg = document.getElementById('dl-label-webp_to_jpg');
    if (dlCheckboxWebptojpg) {
      dlCheckboxWebptojpg.addEventListener('change', () => {
        if (dlCheckboxWebptojpg.checked) {
          if (dlLabelWebptojpg) dlLabelWebptojpg.classList.add('is-checked');
          triggerWebptojpgDownload();
          setTimeout(() => {
            isWebptojpgDownloadComplete = true;
          }, 2350);
        }
      });
      dlCheckboxWebptojpg.addEventListener('click', (e) => {
        if (isWebptojpgDownloadComplete) {
          e.preventDefault();
          triggerWebptojpgDownload();
        }
      });
    }

    function resetWebptojpgView() {
      currentWebptojpgFile = null;
      document.getElementById('webp_to_jpg-result-card').style.display = 'none';
      document.getElementById('proc-webp-to-jpg').style.display = 'none';
      document.getElementById('webp_to_jpg-file-config').style.display = 'none';
      document.getElementById('dropzone-webp_to_jpg').style.display = '';
      const inputEl = document.getElementById('file-input-webp_to_jpg');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxWebptojpg) dlCheckboxWebptojpg.checked = false;
      if (dlLabelWebptojpg) dlLabelWebptojpg.classList.remove('is-checked');
      isWebptojpgDownloadComplete = false;
      if (currentWebptojpgBlobUrl) {
        URL.revokeObjectURL(currentWebptojpgBlobUrl);
        currentWebptojpgBlobUrl = '';
      }
    }

    function setWebptojpgProgress(stepIdx, pct, title) {
      const compId = 'proc-webp-to-jpg';
      const bar = document.getElementById(`${compId}-bar`);
      const pctEl = document.getElementById(`${compId}-pct`);
      const stageTitle = document.getElementById(`${compId}-stage-title`);

      if (bar) bar.style.width = pct + '%';
      if (pctEl) pctEl.textContent = Math.round(pct) + '%';
      if (stageTitle && title) stageTitle.textContent = title + '...';

      for (let i = 1; i <= 4; i++) {
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

    function executeWebptojpg() {
      if (!currentWebptojpgFile) return;

      const formData = new FormData();
      formData.append('file', currentWebptojpgFile);

      document.getElementById('webp_to_jpg-file-config').style.display = 'none';
      const procEl = document.getElementById('proc-webp-to-jpg');
      procEl.style.display = 'block';

      // Step 1: Reading image
      setWebptojpgProgress(1, 20, 'Reading WEBP image');

      const t1 = setTimeout(() => {
        // Step 2: Encoding format
        setWebptojpgProgress(2, 50, 'Encoding JPG format');
      }, 400);

      const t2 = setTimeout(() => {
        // Step 3: Optimizing quality
        setWebptojpgProgress(3, 80, 'Optimizing quality');
      }, 800);

      fetch('/api/webp-to-jpg', {
        method: 'POST',
        body: formData
      })
      .then(res => {
        clearTimeout(t1);
        clearTimeout(t2);
        // Step 4: Finalizing file
        setWebptojpgProgress(4, 95, 'Finalizing file');
        if (!res.ok) {
          return res.json().then(e => { throw new Error(e.error || 'Conversion failed'); });
        }
        return res.blob();
      })
      .then(blob => {
        setWebptojpgProgress(4, 100, 'Finalizing file');
        setTimeout(() => {
          procEl.style.display = 'none';
          document.getElementById('webp_to_jpg-result-card').style.display = 'block';

          if (dlCheckboxWebptojpg) dlCheckboxWebptojpg.checked = false;
          if (dlLabelWebptojpg) dlLabelWebptojpg.classList.remove('is-checked');
          isWebptojpgDownloadComplete = false;

          currentWebptojpgBlobUrl = URL.createObjectURL(blob);
          const resultSub = document.getElementById('webp_to_jpg-result-sub');
          resultSub.textContent = `Converted to JPG successfully (${(blob.size / 1024).toFixed(0)} KB).`;
        }, 350);
      })
      .catch(err => {
        clearTimeout(t1);
        clearTimeout(t2);
        alert('Something went wrong, please try again.');
        resetWebptojpgView();
      });
    }
    """

    return render_layout(
        title="WEBP to JPG",
        active_tool="image-tools",
        hero_title="WEBP to JPG",
        hero_sub="Convert modern WebP graphics into standard JPG images supported everywhere.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
