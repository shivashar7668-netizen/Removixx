"""
Removix UI - Flip Image View with Instant Live Center Preview
"""
from ui.layout import render_layout, render_processing_component

BADGE_SVG = r"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2v20"/><polyline points="4 8 8 12 4 16"/><polyline points="20 8 16 12 20 16"/></svg>"""

def render_flip_image_page() -> str:
    processing_card = render_processing_component(
        component_id="proc-flip-image",
        badge_text="IMAGE FLIPPER",
        badge_icon_svg=BADGE_SVG,
        title_text="Flipping Image...",
        subtitle_text="Inverting pixel matrix along selected axis.",
        steps=['Reading image', 'Mirroring coordinates', 'Encoding output', 'Finalizing file'],
    )

    main_card_html = f"""
    <style>
      .flip-preview-stage {{
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
        min-height: 340px;
        perspective: 1200px;
        overflow: hidden;
      }}
      .flip-img-wrap {{
        max-width: 100%;
        max-height: 420px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        perspective: 1200px;
        transform-style: preserve-3d;
      }}
      #flip-live-img {{
        max-width: 100%;
        max-height: 400px;
        object-fit: contain;
        display: block;
        border-radius: 10px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        transform-style: preserve-3d;
        backface-visibility: visible;
        will-change: transform;
      }}
      @keyframes liveSmoothFlipH {{
        0% {{
          transform: perspective(1200px) rotateY(0deg) scale(1);
        }}
        50% {{
          transform: perspective(1200px) rotateY(90deg) scale(0.92);
        }}
        100% {{
          transform: perspective(1200px) rotateY(180deg) scale(1);
        }}
      }}
      @keyframes liveSmoothFlipV {{
        0% {{
          transform: perspective(1200px) rotateX(0deg) scale(1);
        }}
        50% {{
          transform: perspective(1200px) rotateX(90deg) scale(0.92);
        }}
        100% {{
          transform: perspective(1200px) rotateX(180deg) scale(1);
        }}
      }}
      .flip-anim-h {{
        animation: liveSmoothFlipH 0.72s cubic-bezier(0.4, 0.0, 0.2, 1) forwards;
      }}
      .flip-anim-v {{
        animation: liveSmoothFlipV 0.72s cubic-bezier(0.4, 0.0, 0.2, 1) forwards;
      }}
      .flip-dir-pills-bar {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--bg-page);
        padding: 4px;
        border-radius: 9999px;
        border: 1px solid var(--line);
      }}
      .flip-dir-pill {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 6px 16px;
        font-size: 13px;
        font-weight: 600;
        color: var(--ink-muted);
        background: transparent;
        border: 1px solid transparent;
        border-radius: 9999px;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        outline: none;
      }}
      .flip-dir-pill:hover {{
        color: var(--ink);
      }}
      .flip-dir-pill.active {{
        background: #0284c7;
        color: #ffffff;
        border-color: #0284c7;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.28);
      }}
      html.dark-mode .flip-dir-pill.active,
      body.dark-mode .flip-dir-pill.active {{
        background: #0ea5e9;
        border-color: #0ea5e9;
        color: #ffffff;
        box-shadow: 0 2px 10px rgba(14, 165, 233, 0.35);
      }}
      .flip-status-badge {{
        position: absolute;
        top: 14px;
        right: 16px;
        background: var(--bg-page);
        border: 1px solid var(--line);
        color: var(--ink);
        font-size: 12px;
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        z-index: 10;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
      }}
      @keyframes flipSpin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
      }}
      .flip-spinner {{
        animation: flipSpin 0.8s linear infinite;
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
    <div id="dropzone-flip_image" class="dropzone-box" onclick="document.getElementById('file-input-flip_image').click()">
      <div class="folder-container">
        <div class="folder"><div class="front-side"><div class="tip"></div><div class="cover"></div></div><div class="back-side cover"></div></div>
        <span class="custom-file-upload">Choose Image</span>
      </div>
      <p class="drop-primary">Drop your image here, or browse</p>
      <p class="drop-secondary">Flip horizontally (mirror) or vertically (upside-down)</p>
    </div>
    <input type="file" id="file-input-flip_image" accept=".png,.jpg,.jpeg,.webp" onchange="handleFlipImageUpload(this.files[0])">

    <!-- Active Flip Workspace -->
    <div id="flip_image-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:var(--bg-card); border:1px solid var(--line); border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2v20"/><polyline points="4 8 8 12 4 16"/><polyline points="20 8 16 12 20 16"/></svg>
          </div>
          <div>
            <p id="flip_image-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:2px;">image.jpg</p>
            <p id="flip_image-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetFlipImageView()">Change File</button>
      </div>

      <!-- Controls: Flip Direction -->
      <div style="margin-top:20px; display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
        <span style="font-size:13px; font-weight:700; color:var(--ink);">Flip Direction:</span>
        <div class="flip-dir-pills-bar">
          <button type="button" class="flip-dir-pill active" id="btn-flip-h" onclick="setFlipDir('horizontal')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M8 7l-5 5 5 5"/><path d="M16 7l5 5-5 5"/><line x1="12" y1="3" x2="12" y2="21"/></svg>
            Horizontal
          </button>
          <button type="button" class="flip-dir-pill" id="btn-flip-v" onclick="setFlipDir('vertical')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M7 8l5-5 5 5"/><path d="M7 16l5 5 5-5"/><line x1="3" y1="12" x2="21" y2="12"/></svg>
            Vertical
          </button>
        </div>
      </div>

      <!-- Live Center Preview Stage -->
      <div class="flip-preview-stage">
        <div class="flip-status-badge" id="flip-status-pill">
          <span style="display:inline-block; width:7px; height:7px; border-radius:50%; background:#0284c7;" id="flip-status-dot"></span>
          <span id="flip-status-text">Ready to Flip (Horizontal)</span>
        </div>
        <div class="flip-img-wrap">
          <img id="flip-live-img" alt="Flip Image Preview">
        </div>
      </div>

      <!-- Action Buttons -->
      <div id="flip-action-pre" style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-flip_image" style="padding:12px 28px; font-size:14px; display:inline-flex; align-items:center; gap:8px;" onclick="executeFlipImage()">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2v20"/><polyline points="4 8 8 12 4 16"/><polyline points="20 8 16 12 20 16"/></svg>
          Flip Image
        </button>
      </div>

      <div id="flip-action-post" style="display:none; margin-top:22px; text-align:center; justify-content:center; align-items:center; gap:12px; flex-wrap:wrap;">
        <button type="button" class="btn-primary" id="btn-download-flipped" style="background:#16a34a; border-color:#16a34a; padding:12px 28px; font-size:14px; display:inline-flex; align-items:center; gap:8px;" onclick="triggerFlipImageDownload()">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Download Flipped Image
        </button>
        <button type="button" class="btn-secondary" style="padding:12px 20px; font-size:14px; display:inline-flex; align-items:center; gap:8px;" onclick="resetFlipToOriginal()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Flip Again
        </button>
      </div>
    </div>

    {processing_card}

    <!-- Result Card (Kept for compatibility) -->
    <div id="flip_image-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Process Complete!</h3>
      <p id="flip_image-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your mirrored image is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-flip_image" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-flip_image" />
            <span class="circle"><svg class="icon" viewBox="0 0 24 24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"/></svg><div class="square"></div></span>
            <p class="title">Download File</p><p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetFlipImageView()">
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
    let currentFlipImageFile = null;
    let originalImageDataUrl = '';
    let currentFlipImageBlobUrl = '';
    let isFlipImageDlDone = false;
    let selectedFlipDir = 'horizontal';
    let isFlipping = false;

    const flipLiveImg = document.getElementById('flip-live-img');
    const flipStatusText = document.getElementById('flip-status-text');
    const flipStatusDot = document.getElementById('flip-status-dot');

    function handleFlipImageUpload(file) {
      if (!file) return;
      currentFlipImageFile = file;
      document.getElementById('dropzone-flip_image').style.display = 'none';
      document.getElementById('flip_image-doc-name').textContent = file.name;
      document.getElementById('flip_image-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Ready';
      document.getElementById('flip_image-file-config').style.display = 'block';

      const reader = new FileReader();
      reader.onload = function(e) {
        originalImageDataUrl = e.target.result;
        resetFlipToOriginal();
      };
      reader.readAsDataURL(file);
    }

    function setFlipDir(dir) {
      selectedFlipDir = dir;
      document.getElementById('btn-flip-h').classList.toggle('active', dir === 'horizontal');
      document.getElementById('btn-flip-v').classList.toggle('active', dir === 'vertical');
      
      const postActions = document.getElementById('flip-action-post');
      if (postActions && postActions.style.display === 'flex') {
        resetFlipToOriginal();
      } else {
        updateReadyBadge();
      }
    }

    function updateReadyBadge() {
      if (flipStatusDot) flipStatusDot.style.background = '#0284c7';
      if (flipStatusText) {
        flipStatusText.textContent = selectedFlipDir === 'horizontal' ? 'Ready to Flip (Horizontal)' : 'Ready to Flip (Vertical)';
      }
    }

    function resetFlipToOriginal() {
      if (!originalImageDataUrl) return;
      if (currentFlipImageBlobUrl) {
        URL.revokeObjectURL(currentFlipImageBlobUrl);
        currentFlipImageBlobUrl = '';
      }
      flipLiveImg.classList.remove('flip-anim-h', 'flip-anim-v');
      flipLiveImg.style.transform = 'none';
      flipLiveImg.src = originalImageDataUrl;
      
      updateReadyBadge();
      
      const btnStart = document.getElementById('btn-start-flip_image');
      if (btnStart) {
        btnStart.disabled = false;
        btnStart.style.opacity = '1';
        btnStart.style.cursor = 'pointer';
        btnStart.innerHTML = `
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2v20"/><polyline points="4 8 8 12 4 16"/><polyline points="20 8 16 12 20 16"/></svg>
          Flip Image
        `;
      }
      document.getElementById('flip-action-pre').style.display = 'block';
      const postActions = document.getElementById('flip-action-post');
      if (postActions) postActions.style.display = 'none';
      isFlipping = false;
    }

    function triggerFlipImageDownload() {
      if (!currentFlipImageBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentFlipImageBlobUrl;
      a.download = 'removix_flipped_' + (currentFlipImageFile ? currentFlipImageFile.name : 'image.png');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxFlipImage = document.getElementById('dl-checkbox-flip_image');
    const dlLabelFlipImage = document.getElementById('dl-label-flip_image');
    if (dlCheckboxFlipImage) {
      dlCheckboxFlipImage.addEventListener('change', () => {
        if (dlCheckboxFlipImage.checked) {
          if (dlLabelFlipImage) dlLabelFlipImage.classList.add('is-checked');
          triggerFlipImageDownload();
          setTimeout(() => { isFlipImageDlDone = true; }, 2350);
        }
      });
      dlCheckboxFlipImage.addEventListener('click', (e) => {
        if (isFlipImageDlDone) { e.preventDefault(); triggerFlipImageDownload(); }
      });
    }

    function resetFlipImageView() {
      currentFlipImageFile = null;
      originalImageDataUrl = '';
      if (currentFlipImageBlobUrl) {
        URL.revokeObjectURL(currentFlipImageBlobUrl);
        currentFlipImageBlobUrl = '';
      }
      isFlipping = false;
      document.getElementById('flip_image-file-config').style.display = 'none';
      document.getElementById('dropzone-flip_image').style.display = '';
      const inputEl = document.getElementById('file-input-flip_image');
      if (inputEl) inputEl.value = '';
      
      flipLiveImg.src = '';
      flipLiveImg.className = '';
      flipLiveImg.style.transform = 'none';
      
      selectedFlipDir = 'horizontal';
      document.getElementById('btn-flip-h').classList.add('active');
      document.getElementById('btn-flip-v').classList.remove('active');
      document.getElementById('flip-action-pre').style.display = 'block';
      const postActions = document.getElementById('flip-action-post');
      if (postActions) postActions.style.display = 'none';
    }

    function executeFlipImage() {
      if (!currentFlipImageFile || isFlipping) return;
      isFlipping = true;

      const btnStart = document.getElementById('btn-start-flip_image');
      if (btnStart) {
        btnStart.disabled = true;
        btnStart.style.opacity = '0.75';
        btnStart.style.cursor = 'not-allowed';
        btnStart.innerHTML = `
          <svg class="flip-spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
            <path d="M12 2a10 10 0 0 1 10 10"></path>
          </svg>
          Flipping...
        `;
      }

      if (flipStatusDot) flipStatusDot.style.background = '#f59e0b';
      if (flipStatusText) flipStatusText.textContent = `Flipping ${selectedFlipDir}...`;

      // Trigger smooth 3D CSS animation
      flipLiveImg.classList.remove('flip-anim-h', 'flip-anim-v');
      void flipLiveImg.offsetWidth;
      if (selectedFlipDir === 'horizontal') {
        flipLiveImg.classList.add('flip-anim-h');
      } else {
        flipLiveImg.classList.add('flip-anim-v');
      }

      const formData = new FormData();
      formData.append('file', currentFlipImageFile);
      formData.append('direction', selectedFlipDir);

      const animDuration = 720;
      const animTimer = new Promise(resolve => setTimeout(resolve, animDuration));
      const fetchRequest = fetch('/api/flip-image', { method: 'POST', body: formData })
        .then(res => {
          if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Flip failed'); });
          return res.blob();
        });

      Promise.all([fetchRequest, animTimer])
        .then(([blob]) => {
          if (currentFlipImageBlobUrl) URL.revokeObjectURL(currentFlipImageBlobUrl);
          currentFlipImageBlobUrl = URL.createObjectURL(blob);

          const preloadedImg = new Image();
          preloadedImg.onload = function() {
            // Swap src and clean up animation class without visible jump
            flipLiveImg.classList.remove('flip-anim-h', 'flip-anim-v');
            flipLiveImg.style.transform = 'none';
            flipLiveImg.src = currentFlipImageBlobUrl;

            // Update badge
            if (flipStatusDot) flipStatusDot.style.background = '#10b981';
            if (flipStatusText) {
              flipStatusText.textContent = `✓ Flipped ${selectedFlipDir === 'horizontal' ? 'Horizontally' : 'Vertically'}`;
            }

            // Show post-flip actions
            document.getElementById('flip-action-pre').style.display = 'none';
            const postActions = document.getElementById('flip-action-post');
            if (postActions) postActions.style.display = 'flex';

            isFlipping = false;
          };
          preloadedImg.src = currentFlipImageBlobUrl;
        })
        .catch(err => {
          console.error(err);
          isFlipping = false;
          flipLiveImg.classList.remove('flip-anim-h', 'flip-anim-v');
          flipLiveImg.style.transform = 'none';
          if (btnStart) {
            btnStart.disabled = false;
            btnStart.style.opacity = '1';
            btnStart.style.cursor = 'pointer';
            btnStart.innerHTML = `
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2v20"/><polyline points="4 8 8 12 4 16"/><polyline points="20 8 16 12 20 16"/></svg>
              Flip Image
            `;
          }
          updateReadyBadge();
          alert('Something went wrong during flip, please try again.');
        });
    }
    """

    return render_layout(
        title="Flip Image",
        active_tool="image-tools",
        hero_title="Flip Image",
        hero_sub="Mirror photos <strong>horizontally or invert vertically</strong> in one click.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
