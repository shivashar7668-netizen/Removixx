"""
Removix UI - Make Round Image View with Live Circular Preview & Background Switcher
"""
from ui.layout import render_layout, render_processing_component

BADGE_SVG = r"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/></svg>"""

def render_make_round_image_page() -> str:
    processing_card = render_processing_component(
        component_id="proc-make-round-image",
        badge_text="AVATAR CREATOR",
        badge_icon_svg=BADGE_SVG,
        title_text="Creating Round Image...",
        subtitle_text="Square center cropping and applying supersampled circular mask.",
        steps=['Reading image', 'Calculating center', 'Applying circular mask', 'Finalizing file'],
    )

    main_card_html = f"""
    <style>
      .round-preview-stage {{
        margin-top: 20px;
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 24px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        min-height: 320px;
      }}
      .round-outer-canvas-wrap {{
        width: 260px;
        height: 260px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border: 1px dashed var(--line);
        transition: background 0.2s ease;
      }}
      .bg-checkered {{
        background-color: #f1f5f9;
        background-image: linear-gradient(45deg, #cbd5e1 25%, transparent 25%), 
                          linear-gradient(-45deg, #cbd5e1 25%, transparent 25%), 
                          linear-gradient(45deg, transparent 75%, #cbd5e1 75%), 
                          linear-gradient(-45deg, transparent 75%, #cbd5e1 75%);
        background-size: 16px 16px;
        background-position: 0 0, 0 8px, 8px -8px, -8px 0px;
      }}
      body.dark-mode .bg-checkered {{
        background-color: #0f172a;
        background-image: linear-gradient(45deg, #1e293b 25%, transparent 25%), 
                          linear-gradient(-45deg, #1e293b 25%, transparent 25%), 
                          linear-gradient(45deg, transparent 75%, #1e293b 75%), 
                          linear-gradient(-45deg, transparent 75%, #1e293b 75%);
      }}
      .round-circle-mask {{
        width: 240px;
        height: 240px;
        border-radius: 50%;
        overflow: hidden;
        position: relative;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
      }}
      #round-live-img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
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
    <div id="dropzone-make_round_image" class="dropzone-box" onclick="document.getElementById('file-input-make_round_image').click()">
      <div class="folder-container">
        <div class="folder"><div class="front-side"><div class="tip"></div><div class="cover"></div></div><div class="back-side cover"></div></div>
        <span class="custom-file-upload">Choose Image</span>
      </div>
      <p class="drop-primary">Drop your image here, or browse</p>
      <p class="drop-secondary">Make circular profile photos and round avatars with live background options</p>
    </div>
    <input type="file" id="file-input-make_round_image" accept=".png,.jpg,.jpeg,.webp" onchange="handleMakeRoundImageUpload(this.files[0])">

    <!-- Active Round Image Workspace -->
    <div id="make_round_image-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/></svg>
          </div>
          <div>
            <p id="make_round_image-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">image.jpg</p>
            <p id="make_round_image-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetMakeRoundImageView()">Change File</button>
      </div>

      <!-- Background Options: Transparent (default), White, Custom color -->
      <div style="margin-top:20px;">
        <label style="display:block; font-size:12.5px; font-weight:700; color:var(--ink); margin-bottom:8px;">Outer Background Style:</label>
        <div class="zone-pills-bar" style="justify-content:flex-start; flex-wrap:wrap; gap:10px;">
          <button type="button" class="zone-pill active" id="btn-bg-trans" onclick="setRoundBg('transparent')">Transparent (Default)</button>
          <button type="button" class="zone-pill" id="btn-bg-white" onclick="setRoundBg('white')">Pure White</button>
          <button type="button" class="zone-pill" id="btn-bg-custom" onclick="setRoundBg('custom')">Custom Color</button>
          <div id="round-color-picker-wrap" style="display:none; align-items:center; gap:6px;">
            <input type="color" id="round-custom-color" value="#0284c7" style="width:36px; height:32px; padding:0; border:1px solid var(--line); border-radius:6px; cursor:pointer; background:none;" oninput="onRoundCustomColorChange(this.value)">
          </div>
        </div>
      </div>

      <!-- Live Circular Preview Stage -->
      <div class="round-preview-stage">
        <div style="font-size:11.5px; font-weight:700; color:var(--ink-muted); margin-bottom:12px;">
          LIVE CIRCULAR AVATAR PREVIEW
        </div>
        <div class="round-outer-canvas-wrap bg-checkered" id="round-outer-canvas">
          <div class="round-circle-mask">
            <img id="round-live-img" alt="Circular Profile Avatar">
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-make_round_image" style="padding:12px 28px; font-size:14px;" onclick="executeMakeRoundImage()">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/></svg>
          Make Round Image
        </button>
      </div>
    </div>

    {processing_card}

    <!-- Result Card -->
    <div id="make_round_image-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Process Complete!</h3>
      <p id="make_round_image-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your circular image is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-make_round_image" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-make_round_image" />
            <span class="circle"><svg class="icon" viewBox="0 0 24 24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"/></svg><div class="square"></div></span>
            <p class="title">Download File</p><p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetMakeRoundImageView()">
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
    let currentMakeRoundImageFile = null;
    let currentMakeRoundImageBlobUrl = '';
    let isMakeRoundImageDlDone = false;
    let selectedRoundBg = 'transparent';

    const roundLiveImg = document.getElementById('round-live-img');
    const roundOuterCanvas = document.getElementById('round-outer-canvas');
    const roundColorPickerWrap = document.getElementById('round-color-picker-wrap');
    const roundCustomColor = document.getElementById('round-custom-color');

    function handleMakeRoundImageUpload(file) {
      if (!file) return;
      currentMakeRoundImageFile = file;
      document.getElementById('dropzone-make_round_image').style.display = 'none';
      document.getElementById('make_round_image-doc-name').textContent = file.name;
      document.getElementById('make_round_image-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('make_round_image-file-config').style.display = 'block';

      const reader = new FileReader();
      reader.onload = function(e) {
        roundLiveImg.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    function setRoundBg(mode) {
      selectedRoundBg = mode;
      document.getElementById('btn-bg-trans').classList.toggle('active', mode === 'transparent');
      document.getElementById('btn-bg-white').classList.toggle('active', mode === 'white');
      document.getElementById('btn-bg-custom').classList.toggle('active', mode === 'custom');

      if (mode === 'transparent') {
        roundColorPickerWrap.style.display = 'none';
        roundOuterCanvas.className = 'round-outer-canvas-wrap bg-checkered';
        roundOuterCanvas.style.backgroundColor = '';
      } else if (mode === 'white') {
        roundColorPickerWrap.style.display = 'none';
        roundOuterCanvas.className = 'round-outer-canvas-wrap';
        roundOuterCanvas.style.backgroundColor = '#ffffff';
      } else {
        roundColorPickerWrap.style.display = 'inline-flex';
        roundOuterCanvas.className = 'round-outer-canvas-wrap';
        roundOuterCanvas.style.backgroundColor = roundCustomColor.value;
      }
    }

    function onRoundCustomColorChange(val) {
      if (selectedRoundBg === 'custom') {
        roundOuterCanvas.style.backgroundColor = val;
      }
    }

    function triggerMakeRoundImageDownload() {
      if (!currentMakeRoundImageBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentMakeRoundImageBlobUrl;
      a.download = 'removix_round_avatar.png';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxMakeRoundImage = document.getElementById('dl-checkbox-make_round_image');
    const dlLabelMakeRoundImage = document.getElementById('dl-label-make_round_image');
    if (dlCheckboxMakeRoundImage) {
      dlCheckboxMakeRoundImage.addEventListener('change', () => {
        if (dlCheckboxMakeRoundImage.checked) {
          if (dlLabelMakeRoundImage) dlLabelMakeRoundImage.classList.add('is-checked');
          triggerMakeRoundImageDownload();
          setTimeout(() => { isMakeRoundImageDlDone = true; }, 2350);
        }
      });
      dlCheckboxMakeRoundImage.addEventListener('click', (e) => {
        if (isMakeRoundImageDlDone) { e.preventDefault(); triggerMakeRoundImageDownload(); }
      });
    }

    function resetMakeRoundImageView() {
      currentMakeRoundImageFile = null;
      document.getElementById('make_round_image-result-card').style.display = 'none';
      document.getElementById('proc-make-round-image').style.display = 'none';
      document.getElementById('make_round_image-file-config').style.display = 'none';
      document.getElementById('dropzone-make_round_image').style.display = '';
      const inputEl = document.getElementById('file-input-make_round_image');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxMakeRoundImage) dlCheckboxMakeRoundImage.checked = false;
      if (dlLabelMakeRoundImage) dlLabelMakeRoundImage.classList.remove('is-checked');
      isMakeRoundImageDlDone = false;
      if (currentMakeRoundImageBlobUrl) { URL.revokeObjectURL(currentMakeRoundImageBlobUrl); currentMakeRoundImageBlobUrl = ''; }
      roundLiveImg.src = '';
      setRoundBg('transparent');
    }

    function executeMakeRoundImage() {
      if (!currentMakeRoundImageFile) return;
      const formData = new FormData();
      formData.append('file', currentMakeRoundImageFile);
      const bgVal = selectedRoundBg === 'custom' ? roundCustomColor.value : selectedRoundBg;
      formData.append('bg_color', bgVal);

      document.getElementById('make_round_image-file-config').style.display = 'none';
      const procEl = document.getElementById('proc-make-round-image');
      procEl.style.display = 'block';

      fetch('/api/make-round-image', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Round image creation failed'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('make_round_image-result-card').style.display = 'block';
        currentMakeRoundImageBlobUrl = URL.createObjectURL(blob);
        document.getElementById('make_round_image-result-sub').textContent = `Circular PNG created (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetMakeRoundImageView();
      });
    }
    """

    return render_layout(
        title="Make Round Image",
        active_tool="image-tools",
        hero_title="Make Round Image",
        hero_sub="Create circular profile photos and round avatars with <strong>transparent or custom borders</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
