"""
Removix UI - Upscale Image View
"""
from ui.layout import render_layout, render_processing_component

UPSCALE_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/><path d="M21 14v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5"/></svg>"""

def render_upscale_image_page() -> str:
    processing_card = render_processing_component(
        component_id="proc-upscale",
        badge_text="IMAGE ENHANCER",
        badge_icon_svg=UPSCALE_BADGE_SVG,
        title_text="Enhancing Resolution...",
        subtitle_text="Reconstructing micro-details and doubling pixel resolution.",
        steps=["Reading image", "Enhancing resolution", "Saving result"],
    )

    main_card_html = f"""
    <!-- Back to Image Tools Link -->
    <div style="margin-bottom: 20px;">
      <a href="/image-tools" class="btn-secondary" style="display:inline-flex; align-items:center; gap:8px; padding:8px 18px; font-size:13px; text-decoration:none; font-weight:600;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        Back to Image Tools
      </a>
    </div>

    <div id="dropzone-upscale" class="dropzone-box" onclick="document.getElementById('file-input-upscale').click()">
      <div class="folder-container">
        <div class="folder"><div class="front-side"><div class="tip"></div><div class="cover"></div></div><div class="back-side cover"></div></div>
        <span class="custom-file-upload">Choose Image</span>
      </div>
      <p class="drop-primary">Drop your image here, or browse</p>
      <p class="drop-secondary">Supports JPG, PNG, WEBP • Max 1MB file size • 2x Resolution Boost</p>
    </div>
    <input type="file" id="file-input-upscale" accept=".png,.jpg,.jpeg,.webp" onchange="handleUpscaleUpload(this.files[0])">

    <div id="upscale-file-config" style="display:none; margin-top:20px; padding:22px 24px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:42px; height:42px; border-radius:10px; background:#fef9c3; color:#ca8a04; display:flex; align-items:center; justify-content:center;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          </div>
          <div>
            <p id="upscale-doc-name" style="font-size:14.5px; font-weight:700; color:var(--ink);">image.jpg</p>
            <p id="upscale-doc-size" style="font-size:12px; color:var(--ink-muted);">0 KB • Ready to upscale</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetUpscaleView()">Change File</button>
      </div>

      <div style="margin-top:16px; padding:12px 16px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; font-size:12.5px; color:#166534;">
        Target output: <strong>2x Higher Resolution</strong> with enhanced sharpness and reduced compression artifacts.
      </div>

      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-upscale" onclick="executeUpscale()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          Upscale Image 2x
        </button>
      </div>
    </div>

    {processing_card}

    <div id="upscale-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Image Upscaled 2x!</h3>
      <p id="upscale-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your 2x resolution enhanced image is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-upscale" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-upscale" />
            <span class="circle"><svg class="icon" viewBox="0 0 24 24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"/></svg><div class="square"></div></span>
            <p class="title">Download Image</p><p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetUpscaleView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Upscale Another Image
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top"><div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div><span class="free-badge">FREE</span></div>
          <h3>2x Ultra Clarity</h3>
          <p>Reconstructs fine textures and cleans jagged edges for twice the pixel resolution.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top"><div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div><span class="free-badge">FREE</span></div>
          <h3>100% Private</h3>
          <p>Your photos stay securely on your computer and are enhanced locally without cloud storage.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top"><div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div><span class="free-badge">FREE</span></div>
          <h3>Optimized Speed</h3>
          <p>Hardware accelerated processing delivers upscale results in seconds.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let currentUpscaleFile = null;

    function handleUpscaleUpload(file) {
      if (!file) return;
      if (file.size > 1024 * 1024) {
        alert('Please upload an image smaller than 1MB for best results.');
        return;
      }
      currentUpscaleFile = file;
      document.getElementById('dropzone-upscale').style.display = 'none';
      document.getElementById('upscale-doc-name').textContent = file.name;
      document.getElementById('upscale-doc-size').textContent = (file.size / 1024).toFixed(0) + ' KB • Max 1MB';
      document.getElementById('upscale-file-config').style.display = 'block';
    }

    let currentUpscaleBlobUrl = '';
    let isUpscaleDlDone = false;

    function triggerUpscaleDownload() {
      if (!currentUpscaleBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentUpscaleBlobUrl;
      a.download = 'removix_upscaled.png';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxUpscale = document.getElementById('dl-checkbox-upscale');
    const dlLabelUpscale = document.getElementById('dl-label-upscale');
    if (dlCheckboxUpscale) {
      dlCheckboxUpscale.addEventListener('change', () => {
        if (dlCheckboxUpscale.checked) {
          if (dlLabelUpscale) dlLabelUpscale.classList.add('is-checked');
          triggerUpscaleDownload();
          setTimeout(() => { isUpscaleDlDone = true; }, 2350);
        }
      });
      dlCheckboxUpscale.addEventListener('click', (e) => {
        if (isUpscaleDlDone) { e.preventDefault(); triggerUpscaleDownload(); }
      });
    }

    function resetUpscaleView() {
      currentUpscaleFile = null;
      document.getElementById('upscale-result-card').style.display = 'none';
      document.getElementById('proc-upscale').style.display = 'none';
      document.getElementById('upscale-file-config').style.display = 'none';
      document.getElementById('dropzone-upscale').style.display = '';
      const inputEl = document.getElementById('file-input-upscale');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxUpscale) dlCheckboxUpscale.checked = false;
      if (dlLabelUpscale) dlLabelUpscale.classList.remove('is-checked');
      isUpscaleDlDone = false;
      if (currentUpscaleBlobUrl) { URL.revokeObjectURL(currentUpscaleBlobUrl); currentUpscaleBlobUrl = ''; }
    }

    function executeUpscale() {
      if (!currentUpscaleFile) return;
      if (currentUpscaleFile.size > 1024 * 1024) {
        alert('Please upload an image smaller than 1MB for best results.');
        return;
      }
      const formData = new FormData();
      formData.append('file', currentUpscaleFile);

      document.getElementById('upscale-file-config').style.display = 'none';
      const procEl = document.getElementById('proc-upscale');
      procEl.style.display = 'block';

      fetch('/api/upscale-image', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Could not enhance this image. Please try a different file.'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('upscale-result-card').style.display = 'block';
        currentUpscaleBlobUrl = URL.createObjectURL(blob);
        document.getElementById('upscale-result-sub').textContent = `Image upscaled 2x (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert(err.message || 'Could not enhance this image. Please try a different file.');
        resetUpscaleView();
      });
    }
    """

    return render_layout(
        title="Upscale Image",
        active_tool="image-tools",
        hero_title="Upscale Image 2x",
        hero_sub="Double your image resolution with <strong>clarity enhancement and detail reconstruction</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
