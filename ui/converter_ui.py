"""
Removix UI - Universal Format Converter View
--------------------------------------------
Interactive converter interface for:
- Images: JPG ↔ PNG ↔ WEBP ↔ SVG ↔ ICO ↔ PDF ↔ BMP
- Videos: MP4 ↔ MOV ↔ WEBM ↔ MKV ↔ GIF ↔ MP3 ↔ WAV
- Audios: MP3 ↔ WAV ↔ AAC ↔ FLAC

Dedicated processing UI:
- Badge: "FORMAT CONVERTER"
- Steps: "Reading file" → "Converting format" → "Optimizing output" → "Finalizing file"
- Dynamic target format selection (pills + dropdown) strictly separated by media category.
"""

from ui.layout import render_layout, render_processing_component

CONVERTER_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><path d="M7 16l-4-4m0 0l4-4m-4 4h18M17 8l4 4m0 0l-4 4m4-4H3"/></svg>"""


def render_converter_page() -> str:
    """Renders the Universal Format Converter interface."""
    processing_card = render_processing_component(
        component_id="conv-proc",
        badge_text="FORMAT CONVERTER",
        badge_icon_svg=CONVERTER_BADGE_SVG,
        title_text="Converting Media Format...",
        subtitle_text="Transcoding with high bitrate and hardware acceleration.",
        steps=[
            "Reading file",
            "Converting format",
            "Optimizing output",
            "Finalizing file",
        ],
    )

    main_card_html = f"""
    <!-- Dropzone View -->
    <div id="dropzone-convert" class="dropzone-box" onclick="document.getElementById('file-input-convert').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose Media File</span>
      </div>
      <p class="drop-primary" id="convert-drop-title">Drop your image, video, or audio file here, or browse</p>
      <p class="drop-secondary">Supports PNG, JPG, WEBP, SVG, PDF, MP4, MOV, WebM, MKV, MP3, WAV</p>
    </div>
    <input type="file" id="file-input-convert" accept=".png,.jpg,.jpeg,.webp,.svg,.bmp,.ico,.pdf,.mp4,.mov,.webm,.mkv,.avi,.flv,.gif,.mp3,.wav,.aac,.flac,.m4a" onchange="handleConvertFileSelection(this.files[0])">

    <!-- Selected File & Target Format Config Card -->
    <div id="convert-config" style="display:none; margin-top:24px; padding:24px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
        <div style="display:flex; align-items:center; gap:12px; overflow:hidden;">
          <div id="convert-file-icon" style="width:42px; height:42px; border-radius:12px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          </div>
          <div style="overflow:hidden;">
            <p id="convert-filename" style="font-size:15px; font-weight:700; color:var(--ink); margin-bottom:2px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap; max-width:380px;">file.png</p>
            <p id="convert-filesize" style="font-size:12px; color:var(--ink-muted);">0 MB • PNG File</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetConvertView()">Change File</button>
      </div>

      <!-- Target Format Selector Section -->
      <div style="margin-top:16px; border-top:1px solid #e2e8f0; padding-top:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
          <div>
            <span style="font-size:13.5px; font-weight:700; color:var(--ink);">Select Target Format:</span>
            <span id="convert-category-badge" style="margin-left:8px; font-size:11px; font-weight:700; color:#0284c7; background:#e0f2fe; padding:2px 8px; border-radius:999px;">IMAGE</span>
          </div>

          <!-- Format Dropdown Option -->
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:12px; color:var(--ink-muted);">Dropdown:</span>
            <select id="target-format-select" onchange="onFormatDropdownChange(this.value)" style="background:#ffffff; border:1px solid #cbd5e1; border-radius:8px; padding:5px 12px; font-size:13px; font-weight:600; color:var(--ink); outline:none; cursor:pointer;">
            </select>
          </div>
        </div>

        <!-- Format Buttons Tray -->
        <div id="target-formats-tray" style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:16px;"></div>

        <!-- Conversion Transformation Indicator -->
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:12px 16px; display:flex; align-items:center; justify-content:center; gap:12px; font-size:13.5px;">
          <span id="label-source-fmt" style="font-weight:700; color:var(--ink);">PNG</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          <span id="label-target-fmt" style="font-weight:800; color:var(--primary); background:#e0f2fe; padding:3px 10px; border-radius:6px;">WEBP</span>
        </div>
      </div>

      <div style="margin-top:22px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-start-convert" onclick="executeConversion()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M7 16l-4-4m0 0l4-4m-4 4h18M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
          <span id="btn-convert-label">Convert to WEBP</span>
        </button>
      </div>
    </div>

    <!-- Processing View (Custom Format Converter UI) -->
    {processing_card}

    <!-- Result / Download State -->
    <div id="convert-result" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Conversion Successful!</h3>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-convert" style="width: 200px;">
            <input type="checkbox" class="input" id="dl-checkbox-convert" />
            <span class="circle">
              <svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19V5m0 14-4-4m4 4 4-4"></path>
              </svg>
              <div class="square"></div>
            </span>
            <p class="title" id="btn-download-label">Download File</p>
            <p class="title">Open</p>
          </label>
        </div>
        <button type="button" class="btn-reset" onclick="resetConvertView()">
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
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M7 16l-4-4m0 0l4-4m-4 4h18M17 8l4 4m0 0l-4 4m4-4H3"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Universal Conversion</h3>
          <p>Seamlessly convert between JPG, PNG, WEBP, SVG, MP4, MOV, WebM, MP3, and animated GIFs.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Lossless Fidelity</h3>
          <p>WebP lossless encoding, full RGB color profiles, and 320kbps audio preserves maximum sharpness.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Hardware Speed</h3>
          <p>Powered locally by Removix high-speed processing engine with zero cloud lag.</p>
        </div>
      </div>
    </section>
    """

    client_js = r"""
    let convertSourceFile = null;
    let selectedTargetFmt = null;
    let currentChoices = [];

    // Distinct format presets for each media type
    const FORMAT_PRESETS = {
      image: ['PNG', 'JPG', 'WEBP', 'SVG', 'PDF', 'ICO', 'BMP'],
      video: ['MP4', 'MOV', 'WEBM', 'MKV', 'GIF', 'MP3', 'WAV'],
      audio: ['MP3', 'WAV', 'AAC', 'FLAC']
    };

    // Drag and Drop listeners on dropzone
    const dropzoneConv = document.getElementById('dropzone-convert');
    if (dropzoneConv) {
      ['dragenter', 'dragover'].forEach(evt => {
        dropzoneConv.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneConv.classList.add('dragover');
        });
      });
      ['dragleave', 'drop'].forEach(evt => {
        dropzoneConv.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneConv.classList.remove('dragover');
        });
      });
      dropzoneConv.addEventListener('drop', e => {
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          handleConvertFileSelection(e.dataTransfer.files[0]);
        }
      });
    }

    function handleConvertFileSelection(file) {
      if (!file) return;
      convertSourceFile = file;

      const ext = '.' + file.name.split('.').pop().toLowerCase();
      const isImg = ['.png','.jpg','.jpeg','.webp','.svg','.bmp','.ico','.tiff','.pdf'].includes(ext);
      const isVid = ['.mp4','.mov','.webm','.mkv','.avi','.flv','.m4v'].includes(ext);
      const isAud = ['.mp3','.wav','.m4a','.aac','.flac','.ogg'].includes(ext);

      document.getElementById('convert-filename').textContent = file.name;
      document.getElementById('convert-filesize').textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB • ' + ext.toUpperCase().replace('.', '') + ' file';
      document.getElementById('label-source-fmt').textContent = ext.toUpperCase().replace('.', '');

      const badgeEl = document.getElementById('convert-category-badge');
      if (ext === '.pdf') badgeEl.textContent = 'DOCUMENT';
      else if (isImg) badgeEl.textContent = 'IMAGE';
      else if (isVid) badgeEl.textContent = 'VIDEO';
      else if (isAud) badgeEl.textContent = 'AUDIO';
      else badgeEl.textContent = 'MEDIA';

      // Pick choices based strictly on media category
      let rawChoices = [];
      if (isImg) rawChoices = [...FORMAT_PRESETS.image];
      else if (isVid) rawChoices = [...FORMAT_PRESETS.video];
      else if (isAud) rawChoices = [...FORMAT_PRESETS.audio];
      else rawChoices = ['PNG', 'JPG', 'WEBP', 'MP4', 'MP3'];

      // Exclude current file format
      const curUpper = ext.replace('.', '').toUpperCase();
      currentChoices = rawChoices.filter(c => {
        if (c === curUpper) return false;
        if (curUpper === 'JPEG' && c === 'JPG') return false;
        if (curUpper === 'JPG' && c === 'JPEG') return false;
        return true;
      });

      selectedTargetFmt = currentChoices[0] || 'PNG';

      // Populate Button Pills and Dropdown
      renderFormatSelectors();

      document.getElementById('dropzone-convert').style.display = 'none';
      document.getElementById('convert-config').style.display = 'block';
    }

    function renderFormatSelectors() {
      const tray = document.getElementById('target-formats-tray');
      const selectEl = document.getElementById('target-format-select');
      tray.innerHTML = '';
      selectEl.innerHTML = '';

      currentChoices.forEach(fmt => {
        // Pill Button
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'zone-pill' + (fmt === selectedTargetFmt ? ' active' : '');
        btn.textContent = fmt;
        btn.onclick = () => selectTargetFormat(fmt);
        tray.appendChild(btn);

        // Select Option
        const opt = document.createElement('option');
        opt.value = fmt;
        opt.textContent = fmt;
        if (fmt === selectedTargetFmt) opt.selected = true;
        selectEl.appendChild(opt);
      });

      updateSelectedLabels();
    }

    function selectTargetFormat(fmt) {
      selectedTargetFmt = fmt;
      
      // Update pills active state
      document.querySelectorAll('#target-formats-tray .zone-pill').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.trim() === fmt);
      });

      // Update dropdown value
      const selectEl = document.getElementById('target-format-select');
      if (selectEl) selectEl.value = fmt;

      updateSelectedLabels();
    }

    function onFormatDropdownChange(val) {
      selectTargetFormat(val);
    }

    function updateSelectedLabels() {
      const lblTarget = document.getElementById('label-target-fmt');
      const btnLabel = document.getElementById('btn-convert-label');
      if (lblTarget) lblTarget.textContent = selectedTargetFmt;
      if (btnLabel) btnLabel.textContent = `Convert to ${selectedTargetFmt}`;
    }

    let currentConvBlobUrl = '';
    let currentConvFileName = '';
    let isConvDownloadComplete = false;

    function triggerConvDownload() {
      if (!currentConvBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentConvBlobUrl;
      a.download = currentConvFileName || 'removix_converted';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxConv = document.getElementById('dl-checkbox-convert');
    const dlLabelConv = document.getElementById('dl-label-convert');
    if (dlCheckboxConv) {
      dlCheckboxConv.addEventListener('change', () => {
        if (dlCheckboxConv.checked) {
          if (dlLabelConv) dlLabelConv.classList.add('is-checked');
          triggerConvDownload();
          setTimeout(() => {
            isConvDownloadComplete = true;
          }, 2350);
        }
      });
      dlCheckboxConv.addEventListener('click', (e) => {
        if (isConvDownloadComplete) {
          e.preventDefault();
          triggerConvDownload();
        }
      });
    }

    function resetConvertView() {
      convertSourceFile = null;
      document.getElementById('convert-result').style.display = 'none';
      document.getElementById('conv-proc').style.display = 'none';
      document.getElementById('convert-config').style.display = 'none';
      document.getElementById('dropzone-convert').style.display = '';
      const inputEl = document.getElementById('file-input-convert');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxConv) dlCheckboxConv.checked = false;
      if (dlLabelConv) dlLabelConv.classList.remove('is-checked');
      isConvDownloadComplete = false;
      if (currentConvBlobUrl) {
        URL.revokeObjectURL(currentConvBlobUrl);
        currentConvBlobUrl = '';
      }
    }

    function setConvProgress(stepIdx, pct, title) {
      const compId = 'conv-proc';
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

    function executeConversion() {
      if (!convertSourceFile || !selectedTargetFmt) return;

      const formData = new FormData();
      formData.append('file', convertSourceFile);
      formData.append('target_format', selectedTargetFmt);

      document.getElementById('convert-config').style.display = 'none';
      const procEl = document.getElementById('conv-proc');
      procEl.style.display = 'block';

      // Step 1: Reading file
      setConvProgress(1, 18, 'Reading file');

      const t1 = setTimeout(() => {
        // Step 2: Converting format
        setConvProgress(2, 50, 'Converting format');
      }, 500);

      const t2 = setTimeout(() => {
        // Step 3: Optimizing output
        setConvProgress(3, 80, 'Optimizing output');
      }, 1100);

      fetch('/api/format-convert', {
        method: 'POST',
        body: formData
      })
      .then(res => {
        clearTimeout(t1);
        clearTimeout(t2);
        // Step 4: Finalizing file
        setConvProgress(4, 95, 'Finalizing file');
        if (!res.ok) {
          return res.json().then(e => { throw new Error(e.error || 'Conversion failed'); });
        }
        return res.blob();
      })
      .then(blob => {
        setConvProgress(4, 100, 'Finalizing file');
        setTimeout(() => {
          procEl.style.display = 'none';
          document.getElementById('convert-result').style.display = 'block';
          
          if (dlCheckboxConv) dlCheckboxConv.checked = false;
          if (dlLabelConv) dlLabelConv.classList.remove('is-checked');
          isConvDownloadComplete = false;

          const dlLabel = document.getElementById('btn-download-label');
          const successInfo = document.getElementById('convert-success-info');
          
          currentConvBlobUrl = URL.createObjectURL(blob);
          const outExt = selectedTargetFmt.toLowerCase();
          currentConvFileName = `removix_converted.${outExt}`;
          if (dlLabel) dlLabel.textContent = `Download ${selectedTargetFmt.toUpperCase()}`;
          if (dlLabelConv) dlLabelConv.style.width = '205px';
          successInfo.textContent = `File successfully converted to ${selectedTargetFmt} with maximum fidelity.`;
        }, 350);
      })
      .catch(err => {
        clearTimeout(t1);
        clearTimeout(t2);
        alert('Something went wrong, please try again.');
        resetConvertView();
      });
    }
    """

    return render_layout(
        title="Universal Format Converter",
        active_tool="format-convert",
        hero_title="Universal Format Converter",
        hero_sub="Convert between images, videos, and audio formats with <strong>zero quality loss</strong> and hardware acceleration.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_js=client_js,
    )
