"""
Removix UI - Collage Maker View
"""
from ui.layout import render_layout, render_processing_component

COLLAGE_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/></svg>"""

def render_collage_maker_page() -> str:
    processing_card = render_processing_component(
        component_id="proc-collage",
        badge_text="COLLAGE MAKER",
        badge_icon_svg=COLLAGE_BADGE_SVG,
        title_text="Building Collage...",
        subtitle_text="Arranging photos into a balanced grid with white border spacing.",
        steps=["Reading images", "Balancing dimensions", "Stitching canvas", "Finalizing file"],
    )

    main_card_html = f"""
    <!-- Back to Image Tools Link -->
    <div style="margin-bottom: 20px;">
      <a href="/image-tools" class="btn-secondary" style="display:inline-flex; align-items:center; gap:8px; padding:8px 18px; font-size:13px; text-decoration:none; font-weight:600;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        Back to Image Tools
      </a>
    </div>

    <div id="dropzone-collage" class="dropzone-box" onclick="document.getElementById('file-input-collage').click()">
      <div class="folder-container">
        <div class="folder"><div class="front-side"><div class="tip"></div><div class="cover"></div></div><div class="back-side cover"></div></div>
        <span class="custom-file-upload">Choose Photos</span>
      </div>
      <p class="drop-primary">Drop 2 to 6 photos here, or browse</p>
      <p class="drop-secondary">Select multiple images to combine into a photo collage</p>
    </div>
    <input type="file" id="file-input-collage" multiple accept=".png,.jpg,.jpeg,.webp" onchange="handleCollageSelection(this.files)">

    <div id="collage-tray" style="display:none; margin-top:20px; padding:22px 24px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <h4 style="font-size:14.5px; font-weight:700; color:var(--ink);">Selected Photos (<span id="collage-count" style="color:var(--primary);">0</span>)</h4>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px; color:#dc2626;" onclick="clearCollageList()">Clear All</button>
      </div>

      <div id="collage-thumbs" style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:16px;"></div>

      <div style="margin-top:16px;">
        <label style="display:block; font-size:12.5px; font-weight:700; color:var(--ink); margin-bottom:8px;">Collage Layout:</label>
        <div class="zone-pills-bar" style="justify-content:flex-start;">
          <button type="button" class="zone-pill active" id="btn-col-grid" onclick="setCollageLayout('grid')">2x2 Grid</button>
          <button type="button" class="zone-pill" id="btn-col-horiz" onclick="setCollageLayout('horizontal')">Horizontal Strip</button>
          <button type="button" class="zone-pill" id="btn-col-vert" onclick="setCollageLayout('vertical')">Vertical Strip</button>
        </div>
      </div>

      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-collage" onclick="executeCollage()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/></svg>
          Generate Collage
        </button>
      </div>
    </div>

    {processing_card}

    <div id="collage-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Collage Ready!</h3>
      <p id="collage-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your stitched photo collage is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-collage" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-collage" />
            <span class="circle"><svg class="icon" viewBox="0 0 24 24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"/></svg><div class="square"></div></span>
            <p class="title">Download JPG</p><p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetCollageView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Make Another Collage
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top"><div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div><span class="free-badge">FREE</span></div>
          <h3>Smart Alignment</h3>
          <p>Centers and resizes images into uniform proportional cells with clean margins.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top"><div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div><span class="free-badge">FREE</span></div>
          <h3>100% Private</h3>
          <p>Collage generation executes on your computer with complete data privacy.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top"><div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div><span class="free-badge">FREE</span></div>
          <h3>Print Ready</h3>
          <p>Compiles at high resolution suitable for scrapbooking, framing, or sharing.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let selectedCollageFiles = [];
    let selectedCollageLayout = 'grid';

    function setCollageLayout(l) {
      selectedCollageLayout = l;
      document.getElementById('btn-col-grid').classList.toggle('active', l === 'grid');
      document.getElementById('btn-col-horiz').classList.toggle('active', l === 'horizontal');
      document.getElementById('btn-col-vert').classList.toggle('active', l === 'vertical');
    }

    function handleCollageSelection(files) {
      if (!files || files.length === 0) return;
      for (let i = 0; i < files.length; i++) {
        if (selectedCollageFiles.length < 6) selectedCollageFiles.push(files[i]);
      }
      renderCollageTray();
    }

    function renderCollageTray() {
      const tray = document.getElementById('collage-tray');
      const countEl = document.getElementById('collage-count');
      const thumbs = document.getElementById('collage-thumbs');
      const dropzone = document.getElementById('dropzone-collage');

      countEl.textContent = selectedCollageFiles.length;
      if (selectedCollageFiles.length > 0) {
        tray.style.display = 'block';
        dropzone.style.padding = '22px 20px';
      } else {
        tray.style.display = 'none';
        dropzone.style.padding = '34px 24px 26px';
        return;
      }

      thumbs.innerHTML = '';
      selectedCollageFiles.forEach((file, idx) => {
        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        img.style.cssText = 'width:64px; height:64px; object-fit:cover; border-radius:10px; border:1px solid #cbd5e1;';
        thumbs.appendChild(img);
      });
    }

    function clearCollageList() {
      selectedCollageFiles = [];
      renderCollageTray();
    }

    let currentCollageBlobUrl = '';
    let isCollageDlDone = false;

    function triggerCollageDownload() {
      if (!currentCollageBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentCollageBlobUrl;
      a.download = 'removix_collage.jpg';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxCollage = document.getElementById('dl-checkbox-collage');
    const dlLabelCollage = document.getElementById('dl-label-collage');
    if (dlCheckboxCollage) {
      dlCheckboxCollage.addEventListener('change', () => {
        if (dlCheckboxCollage.checked) {
          if (dlLabelCollage) dlLabelCollage.classList.add('is-checked');
          triggerCollageDownload();
          setTimeout(() => { isCollageDlDone = true; }, 2350);
        }
      });
      dlCheckboxCollage.addEventListener('click', (e) => {
        if (isCollageDlDone) { e.preventDefault(); triggerCollageDownload(); }
      });
    }

    function resetCollageView() {
      clearCollageList();
      document.getElementById('collage-result-card').style.display = 'none';
      document.getElementById('proc-collage').style.display = 'none';
      document.getElementById('collage-tray').style.display = 'none';
      document.getElementById('dropzone-collage').style.display = '';
      const inputEl = document.getElementById('file-input-collage');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxCollage) dlCheckboxCollage.checked = false;
      if (dlLabelCollage) dlLabelCollage.classList.remove('is-checked');
      isCollageDlDone = false;
      if (currentCollageBlobUrl) { URL.revokeObjectURL(currentCollageBlobUrl); currentCollageBlobUrl = ''; }
    }

    function executeCollage() {
      if (selectedCollageFiles.length < 2) {
        alert('Please choose at least 2 images to create a collage.');
        return;
      }
      const formData = new FormData();
      selectedCollageFiles.forEach(f => formData.append('files', f));
      formData.append('layout', selectedCollageLayout);

      document.getElementById('collage-tray').style.display = 'none';
      const procEl = document.getElementById('proc-collage');
      procEl.style.display = 'block';

      fetch('/api/collage-maker', { method: 'POST', body: formData })
      .then(res => {
        if (!res.ok) return res.json().then(e => { throw new Error(e.error || 'Failed to make collage'); });
        return res.blob();
      })
      .then(blob => {
        procEl.style.display = 'none';
        document.getElementById('collage-result-card').style.display = 'block';
        currentCollageBlobUrl = URL.createObjectURL(blob);
        document.getElementById('collage-result-sub').textContent = `Collage generated with ${selectedCollageFiles.length} photos (${(blob.size / 1024).toFixed(0)} KB).`;
      })
      .catch(err => {
        alert('Something went wrong, please try again.');
        resetCollageView();
      });
    }
    """

    return render_layout(
        title="Collage Maker",
        active_tool="image-tools",
        hero_title="Photo Collage Maker",
        hero_sub="Stitch multiple photos into a <strong>clean, balanced photo collage</strong> with white borders.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
