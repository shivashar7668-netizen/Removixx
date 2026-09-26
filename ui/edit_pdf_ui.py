"""
Removix UI - Edit PDF View
--------------------------
Comprehensive document editor with 7 specialized sub-tools:
1. Add Text & Watermarks
2. Edit / Replace Existing Text
3. Add Images & Stamps
4. Add Shapes (Rectangles, Circles, Lines)
5. Annotations (Highlight, Underline, Strikeout)
6. Add Digital Signature (Canvas drawing or image upload)
7. Redact Content (Permanent blackout redaction)
"""

from ui.layout import render_layout, render_processing_component

PDF_EDIT_BADGE_SVG = r"""<svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>"""


def render_edit_pdf_page() -> str:
    """Renders the comprehensive Edit PDF tool view."""
    processing_card = render_processing_component(
        component_id="edit-proc",
        badge_text="PDF EDITOR",
        badge_icon_svg=PDF_EDIT_BADGE_SVG,
        title_text="Applying Document Modifications...",
        subtitle_text="Rendering vector additions, annotations, and redactions into the PDF.",
        steps=[
            "Reading document",
            "Validating edits",
            "Applying modifications",
            "Finalizing file",
        ],
    )

    main_card_html = f"""
    <!-- Dropzone View -->
    <div id="dropzone-edit" class="dropzone-box" onclick="document.getElementById('file-input-edit').click()">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side"><div class="tip"></div><div class="cover"></div></div>
          <div class="back-side cover"></div>
        </div>
        <span class="custom-file-upload">Choose PDF to Edit</span>
      </div>
      <p class="drop-primary">Drop your PDF document here, or browse</p>
      <p class="drop-secondary">Add text, images, shapes, signatures, annotations, or redact sensitive data</p>
    </div>
    <input type="file" id="file-input-edit" accept=".pdf,application/pdf" onchange="handleEditUpload(this.files[0])">

    <!-- Active PDF File & Sub-Tool Workspace -->
    <div id="edit-file-workspace" style="display:none; margin-top:20px;">
      <!-- Document Header Bar -->
      <div style="display:flex; justify-content:space-between; align-items:center; padding:16px 20px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:16px; margin-bottom:18px;">
        <div style="display:flex; align-items:center; gap:12px; overflow:hidden;">
          <div style="width:38px; height:38px; border-radius:10px; background:#e0f2fe; color:#0284c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          </div>
          <div style="overflow:hidden;">
            <p id="edit-doc-name" style="font-size:14px; font-weight:700; color:var(--ink); margin-bottom:2px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap; max-width:380px;">Document.pdf</p>
            <p id="edit-doc-size" style="font-size:11.5px; color:var(--ink-muted);">0 KB • Ready to edit</p>
          </div>
        </div>
        <button type="button" class="btn-secondary" style="padding:6px 14px; font-size:12px;" onclick="resetEditView()">Change File</button>
      </div>

      <!-- 7 Sub-Tool Tabs -->
      <div class="zone-pills-bar" id="edit-tool-tabs" style="margin-bottom:16px; justify-content:center; gap:6px;">
        <button type="button" class="zone-pill active" id="tab-text" onclick="switchEditSubTool('text')">Add Text</button>
        <button type="button" class="zone-pill" id="tab-replace" onclick="switchEditSubTool('replace')">Edit Text</button>
        <button type="button" class="zone-pill" id="tab-image" onclick="switchEditSubTool('image')">Add Image</button>
        <button type="button" class="zone-pill" id="tab-shape" onclick="switchEditSubTool('shape')">Add Shapes</button>
        <button type="button" class="zone-pill" id="tab-annotate" onclick="switchEditSubTool('annotate')">Annotate</button>
        <button type="button" class="zone-pill" id="tab-signature" onclick="switchEditSubTool('signature')">Signature</button>
        <button type="button" class="zone-pill" id="tab-redact" onclick="switchEditSubTool('redact')">Redact</button>
      </div>

      <!-- Sub-Tool Panel 1: Add Text -->
      <div id="subtool-panel-text" class="edit-subtool-card">
        <h4 style="font-size:15px; font-weight:700; color:var(--ink); margin-bottom:12px;">Add Custom Text</h4>
        <div style="display:grid; grid-template-columns:2fr 1fr 1fr; gap:12px; margin-bottom:12px;">
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Text to Add:</label>
            <input type="text" id="add-text-content" placeholder="Enter text here" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Page Number:</label>
            <input type="number" id="add-text-page" value="1" min="1" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Font Size:</label>
            <input type="number" id="add-text-size" value="14" min="8" max="72" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px;">
          </div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px;">
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">X Position (px):</label>
            <input type="number" id="add-text-x" value="54" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Y Position (px):</label>
            <input type="number" id="add-text-y" value="100" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Text Color:</label>
            <input type="color" id="add-text-color" value="#0f172a" style="width:100%; height:38px; border:1px solid #cbd5e1; border-radius:9px; cursor:pointer; padding:2px;">
          </div>
        </div>
      </div>

      <!-- Sub-Tool Panel 2: Edit / Replace Text -->
      <div id="subtool-panel-replace" class="edit-subtool-card" style="display:none;">
        <h4 style="font-size:15px; font-weight:700; color:var(--ink); margin-bottom:12px;">Find & Replace Existing Text</h4>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;">
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Find Text:</label>
            <input type="text" id="find-text-val" placeholder="Original phrase to replace" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Replace With:</label>
            <input type="text" id="replace-text-val" placeholder="New replacement text" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px;">
          </div>
        </div>
        <p style="font-size:12px; color:#64748b;">Replaces all occurrences across the document while matching original layout.</p>
      </div>

      <!-- Sub-Tool Panel 3: Add Image -->
      <div id="subtool-panel-image" class="edit-subtool-card" style="display:none;">
        <h4 style="font-size:15px; font-weight:700; color:var(--ink); margin-bottom:12px;">Add Image or Stamp</h4>
        <div style="margin-bottom:12px;">
          <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Choose Image (PNG, JPG):</label>
          <input type="file" id="edit-stamp-file" accept=".png,.jpg,.jpeg,.webp" style="display:block; width:100%; font-size:12.5px;">
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:10px;">
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Page #:</label>
            <input type="number" id="stamp-page" value="1" min="1" style="width:100%; box-sizing:border-box; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">X (px):</label>
            <input type="number" id="stamp-x" value="50" style="width:100%; box-sizing:border-box; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Y (px):</label>
            <input type="number" id="stamp-y" value="100" style="width:100%; box-sizing:border-box; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Width (px):</label>
            <input type="number" id="stamp-w" value="150" style="width:100%; box-sizing:border-box; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;">
          </div>
        </div>
      </div>

      <!-- Sub-Tool Panel 4: Add Shapes -->
      <div id="subtool-panel-shape" class="edit-subtool-card" style="display:none;">
        <h4 style="font-size:15px; font-weight:700; color:var(--ink); margin-bottom:12px;">Add Shape</h4>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-bottom:12px;">
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Shape Type:</label>
            <select id="shape-type" style="width:100%; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px; background:#fff;">
              <option value="rect">Rectangle / Box</option>
              <option value="circle">Circle / Oval</option>
              <option value="line">Line</option>
            </select>
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Stroke Color:</label>
            <input type="color" id="shape-stroke" value="#0284c7" style="width:100%; height:38px; border:1px solid #cbd5e1; border-radius:9px; cursor:pointer;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Page Number:</label>
            <input type="number" id="shape-page" value="1" min="1" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px;">
          </div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:10px;">
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">Left (X1):</label><input type="number" id="shape-x1" value="50" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">Top (Y1):</label><input type="number" id="shape-y1" value="50" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">Right (X2):</label><input type="number" id="shape-x2" value="250" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">Bottom (Y2):</label><input type="number" id="shape-y2" value="150" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
        </div>
      </div>

      <!-- Sub-Tool Panel 5: Annotate -->
      <div id="subtool-panel-annotate" class="edit-subtool-card" style="display:none;">
        <h4 style="font-size:15px; font-weight:700; color:var(--ink); margin-bottom:12px;">Highlight or Underline Text</h4>
        <div style="display:grid; grid-template-columns:2fr 1fr 1fr; gap:12px;">
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Text to Annotate:</label>
            <input type="text" id="annot-text" placeholder="Phrase to highlight" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Type:</label>
            <select id="annot-type" style="width:100%; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px; background:#fff;">
              <option value="highlight">Highlight</option>
              <option value="underline">Underline</option>
              <option value="strikeout">Strikeout</option>
            </select>
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:var(--ink-muted); margin-bottom:4px;">Page #:</label>
            <input type="number" id="annot-page" value="1" min="1" style="width:100%; box-sizing:border-box; padding:9px 12px; border:1px solid #cbd5e1; border-radius:9px; font-size:13px;">
          </div>
        </div>
      </div>

      <!-- Sub-Tool Panel 6: Signature -->
      <div id="subtool-panel-signature" class="edit-subtool-card" style="display:none;">
        <h4 style="font-size:15px; font-weight:700; color:var(--ink); margin-bottom:12px;">Digital Signature</h4>
        <p style="font-size:12.5px; color:var(--ink-muted); margin-bottom:10px;">Draw your signature directly below:</p>
        <div style="border:1.5px dashed #cbd5e1; border-radius:12px; background:#fff; margin-bottom:10px; position:relative;">
          <canvas id="sig-canvas" width="450" height="130" style="display:block; margin:0 auto; cursor:crosshair;"></canvas>
          <button type="button" onclick="clearSignatureCanvas()" style="position:absolute; top:8px; right:8px; padding:4px 10px; font-size:11px; border:1px solid #cbd5e1; background:#f8fafc; border-radius:6px; cursor:pointer;">Clear</button>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px;">
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">Page #:</label><input type="number" id="sig-page" value="1" min="1" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">X (px):</label><input type="number" id="sig-x" value="350" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">Y (px):</label><input type="number" id="sig-y" value="650" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
        </div>
      </div>

      <!-- Sub-Tool Panel 7: Redact -->
      <div id="subtool-panel-redact" class="edit-subtool-card" style="display:none;">
        <h4 style="font-size:15px; font-weight:700; color:var(--ink); margin-bottom:12px;">Permanent Redaction</h4>
        <p style="font-size:12.5px; color:#dc2626; margin-bottom:12px;">Warning: Redacted areas and underlying text are irreversibly erased.</p>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr 1fr; gap:10px;">
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">Page #:</label><input type="number" id="redact-page" value="1" min="1" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">X1 (px):</label><input type="number" id="redact-x1" value="50" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">Y1 (px):</label><input type="number" id="redact-y1" value="100" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">X2 (px):</label><input type="number" id="redact-x2" value="300" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
          <div><label style="display:block; font-size:12px; color:var(--ink-muted);">Y2 (px):</label><input type="number" id="redact-y2" value="140" style="width:100%; padding:8px; border:1px solid #cbd5e1; border-radius:8px; font-size:12.5px;"></div>
        </div>
      </div>

      <!-- Action Button -->
      <div style="margin-top:24px; text-align:center;">
        <button type="button" class="btn-primary" id="btn-save-edits" onclick="executePdfEdit()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
          Apply Edits & Save PDF
        </button>
      </div>
    </div>

    <!-- Processing View -->
    {processing_card}

    <!-- Result / Download Card -->
    <div id="edit-result-card" style="display:none; margin-top:24px; padding:28px 24px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:18px; text-align:center;">
      <div style="width:52px; height:52px; border-radius:50%; background:#dcfce7; color:#16a34a; display:inline-flex; align-items:center; justify-content:center; margin-bottom:14px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3 style="font-size:19px; font-weight:800; color:#166534; margin-bottom:6px;">Edits Saved Successfully!</h3>
      <p id="edit-result-sub" style="font-size:13.5px; color:#15803d; margin-bottom:20px;">Your edited PDF document is ready for download.</p>
      <div class="result-actions">
        <div class="container">
          <label class="label" id="dl-label-edit" style="width: 205px;">
            <input type="checkbox" class="input" id="dl-checkbox-edit" />
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
        <button type="button" class="btn-reset" onclick="resetEditView()">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Edit Another PDF
        </button>
      </div>
    </div>
    """

    feature_cards_html = r"""
    <section class="section-features">
      <div class="features-grid">
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>7 Integrated Editing Tools</h3>
          <p>Full-featured suite to add text, insert graphics, draw vector shapes, add notes, and sign forms easily.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>Permanent Redaction</h3>
          <p>Blackout confidential numbers and sensitive lines irreversibly without leaking underlying text layers.</p>
        </div>
        <div class="feature-box">
          <div class="feature-top">
            <div class="feature-icon-pill"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
            <span class="free-badge">FREE</span>
          </div>
          <h3>100% Vector Quality</h3>
          <p>Edits are inserted as sharp vector objects preserving crisp typography and infinite print scalability.</p>
        </div>
      </div>
    </section>
    """

    extra_css = r"""
    .edit-subtool-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      padding: 20px;
      margin-top: 10px;
      box-shadow: 0 1px 4px rgba(15,23,42,0.03);
    }
    """

    client_js = r"""
    let currentEditFile = null;
    let activeSubTool = 'text';

    const dropzoneEdit = document.getElementById('dropzone-edit');
    if (dropzoneEdit) {
      ['dragenter', 'dragover'].forEach(evt => {
        dropzoneEdit.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneEdit.classList.add('dragover');
        });
      });
      ['dragleave', 'drop'].forEach(evt => {
        dropzoneEdit.addEventListener(evt, e => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneEdit.classList.remove('dragover');
        });
      });
      dropzoneEdit.addEventListener('drop', e => {
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          handleEditUpload(e.dataTransfer.files[0]);
        }
      });
    }

    function handleEditUpload(file) {
      if (!file) return;
      if (!file.name.toLowerCase().endsWith('.pdf')) {
        alert('Please choose a valid PDF file.');
        return;
      }
      currentEditFile = file;
      document.getElementById('dropzone-edit').style.display = 'none';
      document.getElementById('edit-doc-name').textContent = file.name;
      document.getElementById('edit-doc-size').textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB • PDF Document';
      document.getElementById('edit-file-workspace').style.display = 'block';
      initSignatureCanvas();
    }

    function switchEditSubTool(toolName) {
      activeSubTool = toolName;
      const tabs = ['text', 'replace', 'image', 'shape', 'annotate', 'signature', 'redact'];
      tabs.forEach(t => {
        const tabEl = document.getElementById('tab-' + t);
        const panelEl = document.getElementById('subtool-panel-' + t);
        if (tabEl) tabEl.classList.toggle('active', t === toolName);
        if (panelEl) panelEl.style.display = (t === toolName) ? 'block' : 'none';
      });
    }

    // Signature Canvas Drawing
    let sigCanvas, sigCtx, isDrawing = false;
    function initSignatureCanvas() {
      sigCanvas = document.getElementById('sig-canvas');
      if (!sigCanvas) return;
      sigCtx = sigCanvas.getContext('2d');
      sigCtx.lineWidth = 2.5;
      sigCtx.lineCap = 'round';
      sigCtx.strokeStyle = '#0f172a';

      sigCanvas.onmousedown = (e) => {
        isDrawing = true;
        const rect = sigCanvas.getBoundingClientRect();
        sigCtx.beginPath();
        sigCtx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
      };
      sigCanvas.onmousemove = (e) => {
        if (!isDrawing) return;
        const rect = sigCanvas.getBoundingClientRect();
        sigCtx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
        sigCtx.stroke();
      };
      window.onmouseup = () => { isDrawing = false; };
    }

    function clearSignatureCanvas() {
      if (!sigCanvas || !sigCtx) return;
      sigCtx.clearRect(0, 0, sigCanvas.width, sigCanvas.height);
    }

    let currentEditBlobUrl = '';
    let isEditDownloadComplete = false;

    function triggerEditDownload() {
      if (!currentEditBlobUrl) return;
      const a = document.createElement('a');
      a.href = currentEditBlobUrl;
      a.download = 'removix_edited.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const dlCheckboxEdit = document.getElementById('dl-checkbox-edit');
    const dlLabelEdit = document.getElementById('dl-label-edit');
    if (dlCheckboxEdit) {
      dlCheckboxEdit.addEventListener('change', () => {
        if (dlCheckboxEdit.checked) {
          if (dlLabelEdit) dlLabelEdit.classList.add('is-checked');
          triggerEditDownload();
          setTimeout(() => {
            isEditDownloadComplete = true;
          }, 2350);
        }
      });
      dlCheckboxEdit.addEventListener('click', (e) => {
        if (isEditDownloadComplete) {
          e.preventDefault();
          triggerEditDownload();
        }
      });
    }

    function resetEditView() {
      currentEditFile = null;
      document.getElementById('edit-result-card').style.display = 'none';
      document.getElementById('edit-proc').style.display = 'none';
      document.getElementById('edit-file-workspace').style.display = 'none';
      document.getElementById('dropzone-edit').style.display = '';
      const inputEl = document.getElementById('file-input-edit');
      if (inputEl) inputEl.value = '';
      if (dlCheckboxEdit) dlCheckboxEdit.checked = false;
      if (dlLabelEdit) dlLabelEdit.classList.remove('is-checked');
      isEditDownloadComplete = false;
      if (currentEditBlobUrl) {
        URL.revokeObjectURL(currentEditBlobUrl);
        currentEditBlobUrl = '';
      }
    }

    function setEditProgress(stepIdx, pct, title) {
      const compId = 'edit-proc';
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

    function executePdfEdit() {
      if (!currentEditFile) return;

      const formData = new FormData();
      formData.append('pdf', currentEditFile);
      formData.append('tool', activeSubTool);

      if (activeSubTool === 'text') {
        const textVal = document.getElementById('add-text-content').value;
        if (!textVal) { alert('Please enter text to add.'); return; }
        formData.append('text', textVal);
        formData.append('page', document.getElementById('add-text-page').value);
        formData.append('fontsize', document.getElementById('add-text-size').value);
        formData.append('x', document.getElementById('add-text-x').value);
        formData.append('y', document.getElementById('add-text-y').value);
        formData.append('color', document.getElementById('add-text-color').value);
      } else if (activeSubTool === 'replace') {
        const findVal = document.getElementById('find-text-val').value;
        const repVal = document.getElementById('replace-text-val').value;
        if (!findVal) { alert('Please enter text to find.'); return; }
        formData.append('search_text', findVal);
        formData.append('replace_text', repVal);
      } else if (activeSubTool === 'image') {
        const imgInput = document.getElementById('edit-stamp-file');
        if (!imgInput.files || imgInput.files.length === 0) { alert('Please choose an image file.'); return; }
        formData.append('image', imgInput.files[0]);
        formData.append('page', document.getElementById('stamp-page').value);
        formData.append('x', document.getElementById('stamp-x').value);
        formData.append('y', document.getElementById('stamp-y').value);
        formData.append('width', document.getElementById('stamp-w').value);
      } else if (activeSubTool === 'shape') {
        formData.append('shape', document.getElementById('shape-type').value);
        formData.append('stroke', document.getElementById('shape-stroke').value);
        formData.append('page', document.getElementById('shape-page').value);
        formData.append('x1', document.getElementById('shape-x1').value);
        formData.append('y1', document.getElementById('shape-y1').value);
        formData.append('x2', document.getElementById('shape-x2').value);
        formData.append('y2', document.getElementById('shape-y2').value);
      } else if (activeSubTool === 'annotate') {
        const annotText = document.getElementById('annot-text').value;
        if (!annotText) { alert('Please enter text to annotate.'); return; }
        formData.append('search_text', annotText);
        formData.append('annot_type', document.getElementById('annot-type').value);
        formData.append('page', document.getElementById('annot-page').value);
      } else if (activeSubTool === 'signature') {
        const dataUrl = sigCanvas.toDataURL('image/png');
        formData.append('signature_data', dataUrl);
        formData.append('page', document.getElementById('sig-page').value);
        formData.append('x', document.getElementById('sig-x').value);
        formData.append('y', document.getElementById('sig-y').value);
      } else if (activeSubTool === 'redact') {
        formData.append('page', document.getElementById('redact-page').value);
        formData.append('x1', document.getElementById('redact-x1').value);
        formData.append('y1', document.getElementById('redact-y1').value);
        formData.append('x2', document.getElementById('redact-x2').value);
        formData.append('y2', document.getElementById('redact-y2').value);
      }

      document.getElementById('edit-file-workspace').style.display = 'none';
      const procEl = document.getElementById('edit-proc');
      procEl.style.display = 'block';

      // Step 1: Reading document
      setEditProgress(1, 20, 'Reading document');

      const t1 = setTimeout(() => {
        // Step 2: Validating edits
        setEditProgress(2, 50, 'Validating edits');
      }, 500);

      const t2 = setTimeout(() => {
        // Step 3: Applying modifications
        setEditProgress(3, 75, 'Applying modifications');
      }, 1000);

      fetch('/api/edit-pdf', {
        method: 'POST',
        body: formData
      })
      .then(res => {
        clearTimeout(t1);
        clearTimeout(t2);
        // Step 4: Finalizing file
        setEditProgress(4, 95, 'Finalizing file');
        if (!res.ok) {
          return res.json().then(e => { throw new Error(e.error || 'Edit failed'); });
        }
        return res.blob();
      })
      .then(blob => {
        setEditProgress(4, 100, 'Finalizing file');
        setTimeout(() => {
          procEl.style.display = 'none';
          document.getElementById('edit-result-card').style.display = 'block';

          if (dlCheckboxEdit) dlCheckboxEdit.checked = false;
          if (dlLabelEdit) dlLabelEdit.classList.remove('is-checked');
          isEditDownloadComplete = false;

          currentEditBlobUrl = URL.createObjectURL(blob);
          const resultSub = document.getElementById('edit-result-sub');
          resultSub.textContent = `Document modifications applied successfully (${(blob.size / 1024).toFixed(0)} KB).`;
        }, 350);
      })
      .catch(err => {
        clearTimeout(t1);
        clearTimeout(t2);
        alert('Something went wrong, please try again.');
        resetEditView();
      });
    }
    """

    return render_layout(
        title="Edit PDF",
        active_tool="pdf-tools",
        hero_title="Edit PDF Document",
        hero_sub="Add text, images, shapes, annotations, signatures, or <strong>redact sensitive data</strong>.",
        main_card_html=main_card_html,
        feature_cards_html=feature_cards_html,
        extra_css=extra_css,
        extra_js=client_js,
    )
