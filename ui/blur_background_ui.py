"""
Removix UI - Blur Background View with Before/After Comparison & Intensity Slider
"""
from ui.layout import render_layout, render_processing_component

BADGE_SVG = r"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/></svg>"""

def render_blur_background_page() -> str:
    processing_card = render_processing_component(
        component_id="proc-blur-background",
        badge_text="PORTRAIT BLUR",
        badge_icon_svg=BADGE_SVG,
        title_text="Applying Portrait Blur...",
        subtitle_text="Segmenting foreground subject and softly blurring background.",
        steps=['Detecting subject', 'Blurring background', 'Saving result'],
    )

    main_card_html = f"""
    <style>
      .blur-comparison-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 20px;
      }}
      @media (max-width: 768px) {{
        .blur-comparison-grid {{
          grid-template-columns: 1fr;
        }}
      }}
      .blur-card-box {{
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
      }}
      .blur-card-header {{
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
      }}
      .blur-badge-pill {{
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 3px 8px;
        border-radius: 6px;
      }}
      .blur-badge-orig {{
        background: var(--line-subtle);
        color: var(--ink-secondary);
      }}
      .blur-badge-after {{
        background: var(--primary-light);
        color: var(--primary);
      }}
      .blur-img-wrapper {{
        width: 100%;
        height: 250px;
        border-radius: 10px;
        overflow: hidden;
        background: rgba(0, 0, 0, 0.03);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
      }}
      body.dark-mode .blur-img-wrapper {{
        background: rgba(0, 0, 0, 0.3);
      }}
      .blur-img-wrapper img {{
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        display: block;
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
    <div id="dropzone-blur_background" class="dropzone-box" onclick="document.getElementById('file-input-blur_background').click()">
      <div class="folder-container">
        <div class="folder"><div class="front-side"><div class="tip"></div><div class="cover"></div></div><div class="back-side cover"></div></div>
        <span class="custom-file-upload">Choose Image</span>
      </div>
      <p class="drop-primary">Drop your image here, or browse</p>
      <p class="drop-secondary">Keep the subject crisp while creating a cinematic portrait blur</p>
    </div>
    <input type="file" id="file-input-blur_background" accept=".png,.jpg,.jpeg,.webp" onchange="handleBlurBackgroundUpload(this.files[0])">

    <!-- Active Configuration View -->
    <div id="blur_background-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/></svg>
          </div>
          <div>
            <p id="blur_background-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">image.jpg</p>
            <p id="blur_background-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetBlurBackgroundView()">Change File</button>
      </div>

      <!-- Blur Intensity Slider (1-10, default 5) -->
      <div style="margin-top:20px; padding:16px 18px; background:var(--bg-page); border:1px solid var(--line); border-radius:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <label style="font-size:13px; font-weight:700; color:var(--ink);">Blur Intensity (1 - 10):</label>
          <span id="blur-intensity-val" style="font-size:12.5px; font-weight:800; color:var(--primary);">Level 5 (Medium / Cinematic)</span>
        </div>
        <input type="range" id="blur-intensity-slider" min="1" max="10" value="5" style="width:100%; height:32px; cursor:pointer;" oninput="onBlurSliderChange(this.value)">
      </div>

      <!-- Action Button -->
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-blur_background" style="padding:12px 28px; font-size:14px;" onclick="executeBlurBackground()">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/></svg>
          Blur Background
        </button>
      </div>
    </div>

    {processing_card}

    <!-- Result Card with Before/After Comparison -->
    <div id="blur_background-result-card" style="display:none; margin-top:24px; padding:24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
        <div>
          <h3 style="font-size:18px; font-weight:800; color:var(--ink); margin-bottom:4px;">Portrait Blur Applied</h3>
          <p id="blur_background-result-sub" style="font-size:13px; color:var(--ink-muted);">Cinematic background blur generated successfully.</p>
        </div>
        <div style="display:flex; gap:10px;">
          <button type="button" class="btn-secondary" style="padding:8px 16px; font-size:12.5px;" onclick="changeBlurIntensityAgain()">
            Adjust Blur
          </button>
        </div>
      </div>

      <!-- Before / After Grid -->
      <div class="blur-comparison-grid">
        <!-- Before: Original Sharp -->
        <div class="blur-card-box">
          <div class="blur-card-header">
            <span class="blur-badge-pill blur-badge-orig">BEFORE (ORIGINAL)</span>
            <span style="font-size:11.5px; color:var(--ink-muted);">Sharp Background</span>
          </div>
          <div class="blur-img-wrapper">
            <img id="blur-img-before" alt="Original Photo">
          </div>
        </div>

        <!-- After: Portrait Blur -->
        <div class="blur-card-box">
          <div class="blur-card-header">
            <span class="blur-badge-pill blur-badge-after">AFTER (PORTRAIT BLUR)</span>
            <span id="blur-level-badge" style="font-size:11.5px; font-weight:700; color:var(--primary);">Level 5</span>
          </div>
          <div class="blur-img-wrapper">
            <img id="blur-img-after" alt="Blurred Background Result">
          </div>
        </div>
      </div>

      <!-- Result Actions -->
      <div class="result-actions" style="margin-top:24px; justify-content:center;">
        <div class="container">
          <label class="label" id="dl-label-blur_background" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-blur_background" />
            <span class="circle"><svg class="icon" viewBox="0 0 24 24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"/></svg><div class="square"></div></span>
            <p class="title">Download File</p><p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetBlurBackgroundView()">
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
    let currentBlurBackgroundFile = null;
    let currentBlurBackgroundBlobUrl = '';
    let isBlurBackgroundDlDone = false;
    let currentBlurLevel = 5;

    const blurImgBefore = document.getElementById('blur-img-before');
    const blurImgAfter = document.getElementById('blur-img-after');
    const blurIntensitySlider = document.getElementById('blur-intensity-slider');
    const blurIntensityVal = document.getElementById('blur-intensity-val');
    const blurLevelBadge = document.getElementById('blur-level-badge');

    function handleBlurBackgroundUpload(file) {
      if (!file) return;
      currentBlurBackgroundFile = file;
      document.getElementById('dropzone-blur_background').style.display = 'none';
      document.getElementById('blur_background-doc-name').textContent = file.name;
      document.getElementById('blur_background-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('blur_background-file-config').style.display = 'block';

      const reader = new FileReader();
      reader.onload = function(e) {
        blurImgBefore.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    function onBlurSliderChange(val) {
      currentBlurLevel = parseInt(val) || 5;
      let label = 'Medium (Cinematic)';
      if (currentBlurLevel <= 3) label = 'Light / Subtle';
      else if (currentBlurLevel >= 8) label = 'Heavy Bokeh';
      blurIntensityVal.textContent = `Level ${currentBlurLevel} (${label})`;
    }

    function changeBlurIntensityAgain() {
      document.getElementById('blur_background-result-card').style.display = 'none';
      document.getElementById('blur_background-file-config').style.display = 'block';
    }

    function triggerBlurBackgroundDownload() {
      if (!currentBlurBackgroundBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentBlurBackgroundBlobUrl;
      a.download = 'removix_portrait_blur_' + (currentBlurBackgroundFile ? currentBlurBackgroundFile.name : 'image.png');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxBlurBackground = document.getElementById('dl-checkbox-blur_background');
    const dlLabelBlurBackground = document.getElementById('dl-label-blur_background');
    if (dlCheckboxBlurBackground) {
      dlCheckboxBlurBackground.addEventListener('change', () => {
        if (dlCheckboxBlurBackground.checked) {
          if (dlLabelBlurBackground) dlLabelBlurBackground.classList.add('is-checked');
          triggerBlurBackgroundDownload();
          setTimeout(() => { isBlurBackgroundDlDone = true; }, 2350);
        }
      });
      dlCheckboxBlurBackground.addEventListener('click', (e) => {
        if (isBlurBackgroundDlDone) { e.preventDefault(); triggerBlurBackgroundDownload(); }
      });
    }

    function resetBlurBackgroundView() {
      currentBlurBackgroundFile = null;
      document.getElementById('blur_background-result-card').style.display = 'none';
      document.getElementById('proc-blur-background').style.display = 'none';
      document.getElementById('blur_background-file-config').style.display = 'none';
      document.getElementById('dropzone-blur_background').style.display = '';
      const inputEl = document.getElementById('file-input-blur_background');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxBlurBackground) dlCheckboxBlurBackground.checked = false;
      if (dlLabelBlurBackground) dlLabelBlurBackground.classList.remove('is-checked');
      isBlurBackgroundDlDone = false;
      if (currentBlurBackgroundBlobUrl) { URL.revokeObjectURL(currentBlurBackgroundBlobUrl); currentBlurBackgroundBlobUrl = ''; }
      blurImgBefore.src = '';
      blurImgAfter.src = '';
      blurIntensitySlider.value = 5;
      onBlurSliderChange(5);
    }

    function executeBlurBackground() {
      if (!currentBlurBackgroundFile) return;
      const formData = new FormData();
      formData.append('file', currentBlurBackgroundFile);
      // Map 1-10 to radius pixels (e.g. level 5 -> 20px)
      const radiusPx = currentBlurLevel * 4;
      formData.append('radius', radiusPx);

      document.getElementById('blur_background-file-config').style.display = 'none';
      const procEl = document.getElementById('proc-blur-background');
      procEl.style.display = 'block';

      fetch('/api/blur-background', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Blur processing failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('blur_background-result-card').style.display = 'block';
        currentBlurBackgroundBlobUrl = URL.createObjectURL(blob);
        blurImgAfter.src = currentBlurBackgroundBlobUrl;
        blurLevelBadge.textContent = `Level ${currentBlurLevel}`;
        document.getElementById('blur_background-result-sub').textContent = `Portrait background softly blurred (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetBlurBackgroundView();
      });
    }
    """

    return render_layout(
        title="Blur Background",
        active_tool="image-tools",
        hero_title="Blur Background",
        hero_sub="Keep the subject in focus while creating a <strong>soft cinematic portrait background</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
