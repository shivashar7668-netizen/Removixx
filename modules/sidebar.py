"""
Removix Modular Sidebar Navigation & Multi-Tool UI Component
-----------------------------------------------------------
Implements:
1. Top bar with Hamburger menu (☰) + Removix Logo
2. Smooth sliding left drawer navigation with 6 tools:
   - Video Watermark Remove (Active)
   - Image Watermark Remove
   - Background Remove
   - Image to PDF
   - PDF to Image
   - Format Convert
3. Interactive tool view switcher with smooth transitions
"""

SIDEBAR_CSS = r"""
/* ========== REMOVIX MODULAR SIDEBAR & TOP BAR STYLES ========== */

/* Top Navigation Bar */
.removix-top-nav {
  width: 100%;
  padding: 24px 32px 0;
  display: flex !important;
  align-items: center;
  justify-content: flex-start;
  gap: 14px;
  position: relative;
  z-index: 50;
  box-sizing: border-box;
}

.hamburger-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.9);
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
  display: flex !important;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  color: #0284c7;
  padding: 0;
  outline: none;
  flex-shrink: 0;
}

.hamburger-btn:hover {
  background: #f0f9ff;
  border-color: #bae6fd;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(2, 132, 199, 0.12);
}

.hamburger-btn svg {
  width: 22px;
  height: 22px;
  stroke: #0284c7;
  stroke-width: 2.5;
  fill: none;
}

.top-brand-wrap {
  display: inline-flex;
  align-items: center;
  gap: 1px;
  background: #ffffff;
  padding: 6px 18px 6px 14px;
  border-radius: 9999px;
  border: 1px solid rgba(226, 232, 240, 0.9);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
  user-select: none;
}

/* Sidebar Drawer Backdrop Overlay */
.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.28);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  z-index: 998;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.28s ease;
}

.sidebar-backdrop.active {
  opacity: 1;
  pointer-events: auto;
}

/* Left Sidebar Drawer */
.removix-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 290px;
  max-width: 85vw;
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  box-shadow: 6px 0 32px rgba(15, 23, 42, 0.10);
  z-index: 999;
  display: flex;
  flex-direction: column;
  transform: translateX(-100%);
  transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1);
  box-sizing: border-box;
  user-select: none;
}

.removix-sidebar.open {
  transform: translateX(0);
}

/* Sidebar Header (Logo + Close ✕) */
.sidebar-header {
  padding: 22px 20px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #f1f5f9;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0px;
}

.sidebar-close-btn {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  border: none;
  background: transparent;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.18s ease;
  outline: none;
}

.sidebar-close-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.sidebar-close-btn svg {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  stroke-width: 2.2;
  fill: none;
}

/* Sidebar Navigation Items */
.sidebar-nav {
  padding: 16px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  flex: 1;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 12px 14px;
  border-radius: 14px;
  background: transparent;
  border: 1px solid transparent;
  color: #334155;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  text-align: left;
  outline: none;
  width: 100%;
  box-sizing: border-box;
}

.sidebar-item:hover:not(.active) {
  background: #f8fafc;
  color: #0f172a;
  border-color: #f1f5f9;
}

.sidebar-item.active {
  background: #e0f2fe;
  color: #0284c7;
  border-color: #bae6fd;
  box-shadow: 0 2px 10px rgba(2, 132, 199, 0.10);
  font-weight: 700;
}

.sidebar-icon-box {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: #f1f5f9;
  color: #0284c7;
  transition: all 0.2s ease;
}

.sidebar-item.active .sidebar-icon-box {
  background: #0284c7;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
}

.sidebar-icon-box svg {
  width: 19px;
  height: 19px;
  stroke: currentColor;
  stroke-width: 2;
  fill: none;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid #f1f5f9;
  font-size: 12px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-version-pill {
  background: #f1f5f9;
  color: #475569;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 9999px;
}

/* Tool View Transition Animations */
.tool-fade-in {
  animation: toolFadeIn 0.26s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes toolFadeIn {
  from {
    opacity: 0.3;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
"""

SIDEBAR_HTML = r"""
<!-- Sidebar Backdrop Overlay -->
<div class="sidebar-backdrop" id="sidebarBackdrop" onclick="toggleSidebar(false)"></div>

<!-- Left Sidebar Navigation Drawer -->
<aside class="removix-sidebar" id="removixSidebar" aria-label="Tool Navigation">
  <div class="sidebar-header">
    <div class="sidebar-brand">
      <div class="brand-icon">
        <svg class="brand-logo-img" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Removix Logo">
          <path d="m56.693 463.048c-12.974-15.793-15.047-37.869-5.237-55.796 7.387-13.498 13.718-28.467 18.996-44.911 9.16-28.554 16.229-57.886 21.215-87.986 4.976-30.102 8.16-59.045 9.561-86.829 1.391-27.786 2.091-50.94 2.091-69.463v-17.945h-23.568c-25.597 0-46.348-20.733-46.348-46.309 0-25.576 20.751-46.309 46.348-46.309h365.69c18.311 0 33.156 14.832 33.156 33.128v219.107c0 19.264-15.63 34.88-34.91 34.88h-1.594c-26.693 0-52.23-9.646-73.216-26.128-5.323-4.181-11.823-6.868-18.916-6.868-10.513 0-18.432 9.689-16.181 19.95 1.927 8.786 4.385 17.186 7.375 25.201 5.172 13.893 11.448 26.827 18.824 38.783 7.367 11.967 15.433 22.776 24.201 32.417 8.759 9.65 17.527 18.333 26.294 26.049 5.929 5.303 12.022 10.337 18.278 15.102 23.655 18.016 25.408 52.931 3.447 72.974-16.147 14.737-40.248 16.513-58.465 4.422-14.352-9.525-27.302-19.711-38.853-30.56-19.719-18.524-36.452-37.916-50.195-58.176-13.745-20.26-24.706-40.808-32.867-61.648-8.17-20.84-14.342-40.809-18.526-59.913-4.182-19.101-6.974-36.557-8.364-52.386-1.401-15.82-2.093-29.133-2.093-39.942 0-3.853 0-7.326 0-10.42 0-3.084.196-5.589.599-7.524 0-2.316.195-4.432.597-6.368h124.194c19.198 0 34.761-15.55 34.761-34.732 0-19.182-15.563-34.732-34.761-34.732h-111.621c-19.401 0-35.047 15.868-34.757 35.25l.07 4.69c0 33.575-1.494 64.643-4.482 93.197-2.988 28.563-6.871 54.901-11.652 79.014-4.781 24.123-10.158 45.93-16.134 65.412-5.976 19.491-12.158 36.757-18.526 51.807-3.388 8.158-6.881 15.979-10.478 23.464-15.872 33.026-60.69 38.415-83.953 10.098z" fill="#0ea5e9"/>
        </svg>
      </div>
      <span class="brand-name">emovix</span>
    </div>
    <button class="sidebar-close-btn" onclick="toggleSidebar(false)" aria-label="Close sidebar">
      <svg viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>
  </div>

  <nav class="sidebar-nav">
    <!-- 1. Video Watermark Remove (Default Active) -->
    <a href="/video-watermark" class="sidebar-item active" data-tool="video-watermark">
      <div class="sidebar-icon-box">
        <svg viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="3" stroke-linecap="round"/><path d="M7 4v16M17 4v16M2 12h20M2 8h5M2 16h5M17 8h5M17 16h5" stroke-linecap="round"/></svg>
      </div>
      <span>Video Watermark Remove</span>
    </a>

    <!-- 2. Image Watermark Remove -->
    <a href="/image-watermark" class="sidebar-item" data-tool="image-watermark">
      <div class="sidebar-icon-box">
        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="3" stroke-linecap="round"/><circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"/><path d="M21 15l-5-5L5 21" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <span>Image Watermark Remove</span>
    </a>

    <!-- 3. Background Remove -->
    <a href="/bg-remove" class="sidebar-item" data-tool="bg-remove">
      <div class="sidebar-icon-box">
        <svg viewBox="0 0 24 24"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <span>Background Remove</span>
    </a>

    <!-- 4. Image to Text (OCR) -->
    <a href="/image-to-text" class="sidebar-item" data-tool="image-to-text">
      <div class="sidebar-icon-box">
        <svg viewBox="0 0 24 24"><path d="M4 7V4h16v3M9 20h6M12 4v16" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <span>Image to Text (OCR)</span>
    </a>

    <!-- 5. QR Code Generator -->
    <a href="/qr-code" class="sidebar-item" data-tool="qr-code">
      <div class="sidebar-icon-box">
        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="7" y="7" width="1" height="1"/><rect x="7" y="16" width="1" height="1"/><rect x="16" y="7" width="1" height="1"/><rect x="16" y="16" width="1" height="1"/></svg>
      </div>
      <span>QR Code Generator</span>
    </a>

    <!-- 6. Image to PDF -->
    <a href="/image-to-pdf" class="sidebar-item" data-tool="image-to-pdf">
      <div class="sidebar-icon-box">
        <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke-linecap="round"/><polyline points="14 2 14 8 20 8"/><path d="M9 15h6M9 11h2M9 19h6" stroke-linecap="round"/></svg>
      </div>
      <span>Image to PDF</span>
    </a>

    <!-- 5. PDF to Image -->
    <a href="/pdf-to-image" class="sidebar-item" data-tool="pdf-to-image">
      <div class="sidebar-icon-box">
        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="14" height="14" rx="2" stroke-linecap="round"/><path d="M7 21h12a2 2 0 0 0 2-2V7" stroke-linecap="round"/><circle cx="8" cy="8" r="1" fill="currentColor"/><path d="M17 13l-3.5-3.5L7 16" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <span>PDF to Image</span>
    </a>

    <!-- 6. Format Convert -->
    <a href="/format-convert" class="sidebar-item" data-tool="format-convert">
      <div class="sidebar-icon-box">
        <svg viewBox="0 0 24 24"><path d="M7 16l-4-4m0 0l4-4m-4 4h18M17 8l4 4m0 0l-4 4m4-4H3" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <span>Format Convert</span>
    </a>
  </nav>

  <div class="sidebar-footer">
    <span>Removix</span>
    <span class="sidebar-version-pill">v1.0 Pro</span>
  </div>
</aside>
"""

TOP_BAR_HTML = r"""
<!-- Clean Top Header with Hamburger and Logo -->
<header class="removix-top-nav">
  <button class="hamburger-btn" id="hamburgerBtn" onclick="toggleSidebar(true)" aria-label="Open tool menu" title="Open tools menu">
    <svg viewBox="0 0 24 24" width="22" height="22" stroke="#0284c7" stroke-width="2.4" fill="none">
      <line x1="3" y1="6" x2="21" y2="6" stroke-linecap="round"></line>
      <line x1="3" y1="12" x2="21" y2="12" stroke-linecap="round"></line>
      <line x1="3" y1="18" x2="21" y2="18" stroke-linecap="round"></line>
    </svg>
  </button>
  <div class="brand-badge">
    <div class="brand-icon">
      <svg class="brand-logo-img" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Removix Logo">
        <path d="m56.693 463.048c-12.974-15.793-15.047-37.869-5.237-55.796 7.387-13.498 13.718-28.467 18.996-44.911 9.16-28.554 16.229-57.886 21.215-87.986 4.976-30.102 8.16-59.045 9.561-86.829 1.391-27.786 2.091-50.94 2.091-69.463v-17.945h-23.568c-25.597 0-46.348-20.733-46.348-46.309 0-25.576 20.751-46.309 46.348-46.309h365.69c18.311 0 33.156 14.832 33.156 33.128v219.107c0 19.264-15.63 34.88-34.91 34.88h-1.594c-26.693 0-52.23-9.646-73.216-26.128-5.323-4.181-11.823-6.868-18.916-6.868-10.513 0-18.432 9.689-16.181 19.95 1.927 8.786 4.385 17.186 7.375 25.201 5.172 13.893 11.448 26.827 18.824 38.783 7.367 11.967 15.433 22.776 24.201 32.417 8.759 9.65 17.527 18.333 26.294 26.049 5.929 5.303 12.022 10.337 18.278 15.102 23.655 18.016 25.408 52.931 3.447 72.974-16.147 14.737-40.248 16.513-58.465 4.422-14.352-9.525-27.302-19.711-38.853-30.56-19.719-18.524-36.452-37.916-50.195-58.176-13.745-20.26-24.706-40.808-32.867-61.648-8.17-20.84-14.342-40.809-18.526-59.913-4.182-19.101-6.974-36.557-8.364-52.386-1.401-15.82-2.093-29.133-2.093-39.942 0-3.853 0-7.326 0-10.42 0-3.084.196-5.589.599-7.524 0-2.316.195-4.432.597-6.368h124.194c19.198 0 34.761-15.55 34.761-34.732 0-19.182-15.563-34.732-34.732-34.732h-111.621c-19.401 0-35.047 15.868-34.757 35.25l.07 4.69c0 33.575-1.494 64.643-4.482 93.197-2.988 28.563-6.871 54.901-11.652 79.014-4.781 24.123-10.158 45.93-16.134 65.412-5.976 19.491-12.158 36.757-18.526 51.807-3.388 8.158-6.881 15.979-10.478 23.464-15.872 33.026-60.69 38.415-83.953 10.098z" fill="#0ea5e9"/>
      </svg>
    </div>
    <span class="brand-name">emovix</span>
  </div>
</header>
"""

SIDEBAR_JS = r"""
// ========== SIDEBAR & MULTI-TOOL INTERACTION SYSTEM ==========
const TOOL_CONFIGS = {
  'video-watermark': {
    title: 'Removix Watermark Remover',
    subtitle: 'Drop any AI <strong>video</strong> or <strong>image</strong> and the watermark is gone in seconds — every frame, original quality, ready to post.',
    dropPrimary: 'Drop your video here, or browse',
    dropSecondary: 'Supports MP4, MOV, WebM, MKV • Up to 4K resolution',
    accept: '.mp4,.mov,.m4v,.webm,.mkv,.avi,.flv',
    mode: 'video',
    feature1: { title: 'Visible logo, lifted', desc: 'The AI watermark sparkle is tracked and removed automatically.' },
    feature2: { title: 'Every frame, clean', desc: 'The logo is removed across the whole video, not just one frame.' },
    feature3: { title: 'Pixel-perfect quality', desc: 'Resolution, frame rate, and bitrate stay the same.' }
  },
  'image-watermark': {
    title: 'Image Watermark Remover',
    subtitle: 'Drop any AI generated <strong>image</strong> and remove watermarks instantly with deep neural LaMa reconstruction.',
    dropPrimary: 'Drop your image here, or browse',
    dropSecondary: 'Supports PNG, JPG, JPEG, WEBP • Lossless quality',
    accept: '.png,.jpg,.jpeg,.webp',
    mode: 'image',
    feature1: { title: 'Deep Neural Inpainting', desc: 'Reconstructs complex textures behind watermarks with pixel accuracy.' },
    feature2: { title: 'C2PA Provenance Stripped', desc: 'Cleans metadata and invisible provenance markers automatically.' },
    feature3: { title: 'Original Resolution', desc: 'Maintains 100% original sharpness and color fidelity.' }
  },
  'bg-remove': {
    title: 'AI Background Remover',
    subtitle: 'Extract subjects, portraits, and product photos with <strong>1-click transparent background</strong> cutout.',
    dropPrimary: 'Drop your photo here to remove background',
    dropSecondary: 'Supports PNG, JPG, WEBP • Auto Subject Isolation',
    accept: '.png,.jpg,.jpeg,.webp',
    mode: 'image',
    feature1: { title: 'Instant Alpha Cutout', desc: 'Crisp subject segmentation with transparent background export.' },
    feature2: { title: 'Hair & Edge Precision', desc: 'Feathered edge blending for natural looking subject extraction.' },
    feature3: { title: 'E-Commerce Ready', desc: 'Clean transparent PNGs ready for Amazon, Shopify, or ads.' }
  },
  'image-to-pdf': {
    title: 'Image to PDF Converter',
    subtitle: 'Combine single or multiple images into a single <strong>clean, high-resolution PDF document</strong> instantly.',
    dropPrimary: 'Drop images here to combine into PDF',
    dropSecondary: 'Supports PNG, JPG, JPEG, WEBP • Multi-page Merge',
    accept: '.png,.jpg,.jpeg,.webp',
    mode: 'image',
    feature1: { title: 'Zero Quality Compression', desc: 'Embeds full resolution images directly into PDF container.' },
    feature2: { title: 'Multi-Image Merge', desc: 'Drop multiple photos to combine them into an ordered PDF.' },
    feature3: { title: 'Instant Download', desc: 'Lightweight, standard PDF ready for email and print.' }
  },
  'pdf-to-image': {
    title: 'PDF to Image Converter',
    subtitle: 'Extract all pages from any PDF document into <strong>crystal-clear individual images</strong> in seconds.',
    dropPrimary: 'Drop PDF document here to extract images',
    dropSecondary: 'Supports PDF Files • High 300 DPI Rendering',
    accept: '.pdf',
    mode: 'image',
    feature1: { title: 'High DPI Extraction', desc: 'Renders pages at crisp print-grade resolution (PNG/JPG).' },
    feature2: { title: 'Full Document Batch', desc: 'Extracts every page into neatly organized high-res images.' },
    feature3: { title: 'Fast & Private', desc: 'Processes locally on your computer with 100% data privacy.' }
  },
  'format-convert': {
    title: 'Media Format Converter',
    subtitle: 'Convert between popular video, audio, and image formats with <strong>zero quality loss</strong> and hardware acceleration.',
    dropPrimary: 'Drop media file here to convert format',
    dropSecondary: 'Supports MP4, MOV, WebM, MKV, MP3, GIF, PNG, JPG',
    accept: '.mp4,.mov,.webm,.mkv,.avi,.flv,.png,.jpg,.jpeg,.webp,.gif,.mp3,.wav',
    mode: 'video',
    feature1: { title: 'Hardware Accelerated', desc: 'Blazing fast conversions powered by local GPU encoders.' },
    feature2: { title: 'Lossless Audio & Video', desc: 'Preserves high bitrate streams and audio synchronization.' },
    feature3: { title: 'Web & Social Presets', desc: 'Optimized profiles for Instagram, YouTube, TikTok, and web.' }
  }
};

let currentToolId = 'video-watermark';

function toggleSidebar(open) {
  const sidebar = document.getElementById('removixSidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  if (!sidebar) return;

  const shouldOpen = (open !== undefined) ? open : !sidebar.classList.contains('open');
  if (shouldOpen) {
    sidebar.classList.add('open');
    if (backdrop) backdrop.classList.add('active');
  } else {
    sidebar.classList.remove('open');
    if (backdrop) backdrop.classList.remove('active');
  }
}

// Close sidebar on Escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    toggleSidebar(false);
  }
});

function switchSidebarTool(toolId) {
  const routes = {
    'video-watermark': '/video-watermark',
    'image-watermark': '/image-watermark',
    'bg-remove': '/bg-remove',
    'image-to-text': '/image-to-text',
    'ocr': '/image-to-text',
    'qr-code': '/qr-code',
    'qr-generator': '/qr-code',
    'image-to-pdf': '/image-to-pdf',
    'pdf-to-image': '/pdf-to-image',
    'format-convert': '/format-convert',
  };
  if (routes[toolId] && window.location.pathname !== routes[toolId]) {
    window.location.href = routes[toolId];
    return;
  }
  if (!TOOL_CONFIGS[toolId]) return;
  currentToolId = toolId;

  // 1. Update active item in sidebar
  document.querySelectorAll('.sidebar-item').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-tool') === toolId);
  });

  const cfg = TOOL_CONFIGS[toolId];

  // 2. Animate and update Hero Titles
  const heroTitle = document.querySelector('.hero h1');
  const heroSub = document.querySelector('.hero-sub');

  if (heroTitle) {
    heroTitle.innerHTML = cfg.title;
    heroTitle.classList.remove('tool-fade-in');
    void heroTitle.offsetWidth; // trigger reflow
    heroTitle.classList.add('tool-fade-in');
  }

  if (heroSub) {
    heroSub.innerHTML = cfg.subtitle;
    heroSub.classList.remove('tool-fade-in');
    void heroSub.offsetWidth;
    heroSub.classList.add('tool-fade-in');
  }

  // 3. Update Dropzone hints and accepted types
  const dropPrimary = document.getElementById('drop-primary-text');
  const dropSecondary = document.getElementById('drop-secondary-text');
  const fileInput = document.getElementById('file');

  if (dropPrimary) dropPrimary.textContent = cfg.dropPrimary;
  if (dropSecondary) dropSecondary.textContent = cfg.dropSecondary;
  if (fileInput && cfg.accept) fileInput.setAttribute('accept', cfg.accept);

  // Sync mode if setMode is defined
  if (typeof setMode === 'function' && cfg.mode) {
    try { setMode(cfg.mode); } catch(e){}
    // Restore custom text if setMode overwrote it
    if (dropPrimary) dropPrimary.textContent = cfg.dropPrimary;
    if (dropSecondary) dropSecondary.textContent = cfg.dropSecondary;
  }

  // 4. Update Feature cards below
  const featBoxes = document.querySelectorAll('.feature-box');
  if (featBoxes.length >= 3) {
    const f1 = featBoxes[0];
    const f2 = featBoxes[1];
    const f3 = featBoxes[2];

    if (f1) {
      const h3 = f1.querySelector('h3');
      const p = f1.querySelector('p');
      if (h3) h3.textContent = cfg.feature1.title;
      if (p) p.textContent = cfg.feature1.desc;
    }
    if (f2) {
      const h3 = f2.querySelector('h3');
      const p = f2.querySelector('p');
      if (h3) h3.textContent = cfg.feature2.title;
      if (p) p.textContent = cfg.feature2.desc;
    }
    if (f3) {
      const h3 = f3.querySelector('h3');
      const p = f3.querySelector('p');
      if (h3) h3.textContent = cfg.feature3.title;
      if (p) p.textContent = cfg.feature3.desc;
    }
  }

  // 5. Update Target Area pills visibility
  const zoneBar = document.getElementById('zone-pills-bar') || document.querySelector('.zone-pills-bar');
  if (zoneBar) {
    if (toolId === 'video-watermark' || toolId === 'image-watermark') {
      zoneBar.style.display = 'flex';
    } else {
      zoneBar.style.display = 'none';
    }
  }

  // 6. Smoothly close sidebar on smaller viewports
  if (window.innerWidth < 1024) {
    setTimeout(() => toggleSidebar(false), 240);
  }
}
"""
