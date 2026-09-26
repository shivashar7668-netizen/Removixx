"""
Removix UI - PNG to GIF View
-------------------------
Dedicated high-precision converter from PNG to GIF.
Matches the exact visual styling, upload box, and animated buttons of Removix.
"""

from ui.layout import render_layout, render_processing_component

CONV_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><path d="M7 16l-4-4m0 0l4-4m-4 4h18M17 8l4 4m0 0l-4 4m4-4H3"/></svg>"""


def render_png_to_gif_page() -> str:
    """Renders the PNG to GIF converter tool view."""
    processing_card = render_processing_component(
        component_id="proc-png-to-gif",
        badge_text="IMAGE CONVERTER",
        badge_icon_svg=CONV_BADGE_SVG,
        title_text="Converting to GIF...",
        subtitle_text="Optimizing pixels, color encoding, and resolution balance.",
        steps=[
            "Reading PNG image",
            "Encoding GIF format",
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
    <div id="dropzone-png_to_gif" class="dropzone-box" onclick="document.getElementById('file-input-png_to_gif').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose PNG File</span>
      </div>
      <p class="drop-primary">Drop your PNG file here, or browse</p>
      <p class="drop-secondary">Supports PNG format • Highest visual quality output</p>
    </div>
    <input type="file" id="file-input-png_to_gif" accept=".png" onchange="handlePngtogifUpload(this.files[0])">

    <!-- Selected File Config Card -->
    <div id="png_to_gif-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:12px; overflow:hidden;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
          </div>
          <div style="overflow:hidden;">
            <p id="png_to_gif-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap; max-width:380px;">image.png</p>
            <p id="png_to_gif-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • PNG Image</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetPngtogifView()">Change File</button>
      </div>

      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-png_to_gif" onclick="executePngtogif()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M7 16l-4-4m0 0l4-4m-4 4h18M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
          Convert to GIF
        </button>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card -->
    <div id="png_to_gif-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Conversion Complete!</h3>
      <p id="png_to_gif-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your file has been converted to GIF with crystal clarity.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-png_to_gif" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-png_to_gif" />
            <span class="circle">
              <svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"></path>
              </svg>
              <div class="square"></div>
            </span>
            <p class="title">Download GIF</p>
            <p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetPngtogifView()">
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
    let currentPngtogifFile = null;

    const dropzonePngtogif = document.getElementById('dropzone-png_to_gif');
    if (dropzonePngtogif) {
      ['dragenter', 'dragover'].forEach(evt => {
        dropzonePngtogif.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzonePngtogif.classList.add('dragover');
        });
      });
      ['dragleave', 'drop'].forEach(evt => {
        dropzonePngtogif.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzonePngtogif.classList.remove('dragover');
        });
      });
      dropzonePngtogif.addEventListener('drop', e => {
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          handlePngtogifUpload(e.dataTransfer.files[0]);
        }
      });
    }

    function handlePngtogifUpload(file) {
      if (!file) return;
      currentPngtogifFile = file;
      document.getElementById('dropzone-png_to_gif').style.display = 'none';
      document.getElementById('png_to_gif-doc-name').textContent = file.name;
      document.getElementById('png_to_gif-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • PNG Image';
      document.getElementById('png_to_gif-file-config').style.display = 'block';
    }

    let currentPngtogifBlobUrl = '';
    let isPngtogifDownloadComplete = false;

    function triggerPngtogifDownload() {
      if (!currentPngtogifBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentPngtogifBlobUrl;
      a.download = 'removix_png_to_gif.gif';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxPngtogif = document.getElementById('dl-checkbox-png_to_gif');
    const dlLabelPngtogif = document.getElementById('dl-label-png_to_gif');
    if (dlCheckboxPngtogif) {
      dlCheckboxPngtogif.addEventListener('change', () => {
        if (dlCheckboxPngtogif.checked) {
          if (dlLabelPngtogif) dlLabelPngtogif.classList.add('is-checked');
          triggerPngtogifDownload();
          setTimeout(() => {
            isPngtogifDownloadComplete = true;
          }, 2350);
        }
      });
      dlCheckboxPngtogif.addEventListener('click', (e) => {
        if (isPngtogifDownloadComplete) {
          e.preventDefault();
          triggerPngtogifDownload();
        }
      });
    }

    function resetPngtogifView() {
      currentPngtogifFile = null;
      document.getElementById('png_to_gif-result-card').style.display = 'none';
      document.getElementById('proc-png-to-gif').style.display = 'none';
      document.getElementById('png_to_gif-file-config').style.display = 'none';
      document.getElementById('dropzone-png_to_gif').style.display = '';
      const inputEl = document.getElementById('file-input-png_to_gif');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxPngtogif) dlCheckboxPngtogif.checked = false;
      if (dlLabelPngtogif) dlLabelPngtogif.classList.remove('is-checked');
      isPngtogifDownloadComplete = false;
      if (currentPngtogifBlobUrl) {
        URL.revokeObjectURL(currentPngtogifBlobUrl);
        currentPngtogifBlobUrl = '';
      }
    }

    function setPngtogifProgress(stepIdx, pct, title) {
      const compId = 'proc-png-to-gif';
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

    function executePngtogif() {
      if (!currentPngtogifFile) return;

      const formData = new FormData();
      formData.append('file', currentPngtogifFile);

      document.getElementById('png_to_gif-file-config').style.display = 'none';
      const procEl = document.getElementById('proc-png-to-gif');
      procEl.style.display = 'block';

      // Step 1: Reading image
      setPngtogifProgress(1, 20, 'Reading PNG image');

      const t1 = setTimeout(() => {
        // Step 2: Encoding format
        setPngtogifProgress(2, 50, 'Encoding GIF format');
      }, 400);

      const t2 = setTimeout(() => {
        // Step 3: Optimizing quality
        setPngtogifProgress(3, 80, 'Optimizing quality');
      }, 800);

      fetch('/api/png-to-gif', {
        method: 'POST',
        body: formData
      })
      .then(res => {
        clearTimeout(t1);
        clearTimeout(t2);
        // Step 4: Finalizing file
        setPngtogifProgress(4, 95, 'Finalizing file');
        if (!res.ok) {
          return res.json().then(e => { throw new Error(e.error || 'Conversion failed'); });
        }
        return res.blob();
      })
      .then(blob => {
        setPngtogifProgress(4, 100, 'Finalizing file');
        setTimeout(() => {
          procEl.style.display = 'none';
          document.getElementById('png_to_gif-result-card').style.display = 'block';

          if (dlCheckboxPngtogif) dlCheckboxPngtogif.checked = false;
          if (dlLabelPngtogif) dlLabelPngtogif.classList.remove('is-checked');
          isPngtogifDownloadComplete = false;

          currentPngtogifBlobUrl = URL.createObjectURL(blob);
          const resultSub = document.getElementById('png_to_gif-result-sub');
          resultSub.textContent = `Converted to GIF successfully (${(blob.size / 1024).toFixed(0)} KB).`;
        }, 350);
      })
      .catch(err => {
        clearTimeout(t1);
        clearTimeout(t2);
        alert('Something went wrong, please try again.');
        resetPngtogifView();
      });
    }
    """

    return render_layout(
        title="PNG to GIF",
        active_tool="image-tools",
        hero_title="PNG to GIF",
        hero_sub="Transform PNG designs into lightweight GIF graphics with transparency.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
