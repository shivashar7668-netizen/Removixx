"""
Removix UI Template Module
--------------------------
Separated frontend layout to keep app.py lightweight and maintainable.
"""

from ui.sidebar import SIDEBAR_CSS, render_top_bar_html, render_sidebar_html, SIDEBAR_JS

TOP_BAR_HTML = render_top_bar_html()
SIDEBAR_HTML = render_sidebar_html(active_tool="video-tools")

_RAW_PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
  (function() {
    try {
      var saved = localStorage.getItem('removix_theme');
      var isDark = saved === 'dark' || (!saved && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
      if (isDark) {
        document.documentElement.classList.add('dark-mode');
        document.documentElement.setAttribute('data-theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark-mode');
        document.documentElement.setAttribute('data-theme', 'light');
      }
    } catch(e) {}
  })();
</script>
<style id="fouc-prevention-style">
  html.dark-mode { background-color: #0b0f19 !important; color: #f8fafc !important; }
  html.dark-mode body { background-color: #0b0f19 !important; color: #f8fafc !important; }
  [data-theme="dark"] { background-color: #0b0f19 !important; color: #f8fafc !important; }
  [data-theme="dark"] body { background-color: #0b0f19 !important; color: #f8fafc !important; }

  /* Anti-Flash Rules for Cards, Icons, and Containers */
  html.dark-mode .feature-card,
  html.dark-mode .privacy-card,
  [data-theme="dark"] .feature-card,
  [data-theme="dark"] .privacy-card {
    background: #1e293b !important;
    border-color: #334155 !important;
  }
  html.dark-mode .feature-icon-pill,
  [data-theme="dark"] .feature-icon-pill {
    background: rgba(56, 189, 248, 0.12) !important;
    color: #38bdf8 !important;
  }
  html.dark-mode .privacy-icon-box,
  [data-theme="dark"] .privacy-icon-box {
    background: rgba(16, 185, 129, 0.16) !important;
    color: #34d399 !important;
  }
</style>
<title>Removix — AI Video & Image Watermark Remover</title>
<link rel="icon" type="image/png" href="/static/removix.png?v=3">
<link rel="shortcut icon" href="/favicon.ico?v=3">
<link rel="apple-touch-icon" href="/static/removix.png?v=3">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="/lottie.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script>
  if (!window.lottie) {
    var s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js';
    document.head.appendChild(s);
  }
</script>
<style>
  :root {
    --primary: #0284c7;
    --primary-hover: #0369a1;
    --sky: #0ea5e9;
    --sky-light: #e0f2fe;
    --sky-soft: #f0f9ff;
    --ink: #0f172a;
    --ink-muted: #475569;
    --ink-faint: #94a3b8;
    --bg-page: #f8fafc;
    --card-bg: #ffffff;
    --line: #e2e8f0;
    --line-subtle: #f1f5f9;
    --green-badge: #16a34a;
    --green-badge-bg: #dcfce7;
    --radius-lg: 24px;
    --radius-md: 16px;
    --radius-sm: 10px;
    --shadow-card: 0 20px 45px -12px rgba(15, 23, 42, 0.08), 0 4px 16px -2px rgba(15, 23, 42, 0.03);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body {
    background-color: var(--bg-page);
    background-image: radial-gradient(1200px 600px at 50% -80px, #e0f2fe 0%, rgba(240, 249, 255, 0.4) 45%, rgba(248, 250, 252, 0) 100%);
    background-repeat: no-repeat;
    color: var(--ink);
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }

  a { color: inherit; text-decoration: none; }

  /* ---------- Clean Top Header (Removix) ---------- */
  .top-header {
    padding: 32px 20px 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .brand-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0px;
    background: #ffffff;
    padding: 6px 20px 6px 16px;
    border-radius: 9999px;
    border: 1px solid rgba(226, 232, 240, 0.9);
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
  }
  .brand-icon {
    width: 27px;
    height: 27px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: visible;
    flex-shrink: 0;
  }
  .brand-icon img, .brand-logo-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
  }
  .brand-icon svg { width: 100%; height: 100%; display: block; }
  .brand-name {
    font-size: 21.5px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--ink);
    line-height: 1;
    margin-left: 0px;
  }
  .brand-name span { color: var(--sky); }

  /* ---------- Hero Section ---------- */
  .hero {
    max-width: 820px;
    margin: 40px auto 0;
    text-align: center;
    padding: 0 20px;
  }
  .badge-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #0284c7;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 6px 16px;
    border-radius: 9999px;
    margin-bottom: 20px;
  }
  .hero h1 {
    font-size: clamp(34px, 5.2vw, 56px);
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -0.03em;
    color: var(--ink);
    margin-bottom: 16px;
  }
  .hero-sub {
    font-size: 17px;
    line-height: 1.6;
    color: var(--ink-muted);
    max-width: 720px;
    margin: 0 auto 36px;
  }
  .hero-sub strong { color: var(--ink); font-weight: 600; }

  /* ---------- Tool Card (Hero Main Box) ---------- */
  .tool-container {
    max-width: 1140px;
    width: 100%;
    margin: 0 auto;
    padding: 0 32px;
    box-sizing: border-box;
    overflow-x: hidden;
  }
  .main-tool-card {
    background: var(--card-bg);
    border: 1px solid rgba(226, 232, 240, 0.9);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    padding: 32px;
    position: relative;
    overflow: hidden;
    overflow-x: hidden;
    width: 100%;
    box-sizing: border-box;
  }

  @media (max-width: 1200px) {
    .tool-container {
      max-width: 100%;
      padding: 0 28px;
    }
  }

  @media (max-width: 1024px) {
    .tool-container {
      padding: 0 24px;
    }
    .main-tool-card {
      padding: 26px 20px;
    }
  }

  @media (max-width: 768px) {
    .tool-container {
      padding: 0 14px;
    }
    .main-tool-card {
      padding: 18px 14px;
      border-radius: 16px;
    }
  }

  @media (max-width: 480px) {
    .tool-container {
      padding: 0 10px;
    }
    .main-tool-card {
      padding: 14px 10px;
      border-radius: 12px;
    }
  }

  /* Mode Switcher tabs */
  .tool-tabs {
    display: none !important;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 24px;
  }
  .tool-tab {
    padding: 9px 22px;
    border-radius: 9999px;
    font-size: 13.5px;
    font-weight: 600;
    color: var(--ink-muted);
    background: #f1f5f9;
    border: 1px solid transparent;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
  }
  .tool-tab.active {
    background: #eff6ff;
    color: #0284c7;
    border-color: #bae6fd;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.12);
  }
  .tool-tab:hover:not(.active) {
    background: #e2e8f0;
  }

  /* Watermark Detection Zone Pills */
  .zone-pills-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin: 0 auto 20px;
    flex-wrap: wrap;
  }
  .zone-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--ink-muted);
  }
  .zone-pill {
    background: #f1f5f9;
    border: 1px solid var(--line);
    color: var(--ink-muted);
    font-size: 12px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 9999px;
    cursor: pointer;
    transition: all 0.2s ease;
    outline: none;
    font-family: inherit;
  }
  .zone-pill:hover {
    background: #e2e8f0;
    color: var(--ink);
  }
  .zone-pill.active {
    background: #0284c7;
    color: #ffffff;
    border-color: #0284c7;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
  }

  /* Dropzone */
  #dropzone {
    border: 2px dashed #bae6fd;
    background: #f8fafc;
    border-radius: var(--radius-md);
    padding: 34px 24px 26px;
    text-align: center;
    cursor: pointer;
    display: block;
    transition: all 0.25s ease;
    user-select: none;
    -webkit-user-select: none;
  }
  #dropzone:hover, #dropzone.hover {
    border-color: var(--sky);
    background: var(--sky-soft);
  }

  /* From Uiverse.io by 3bdel3ziz-T — Removix Sky Blue Edition */
  .folder-container {
    --transition: 350ms;
    --folder-W: 120px;
    --folder-H: 80px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    padding: 10px;
    background: linear-gradient(135deg, #38bdf8, #0284c7);
    border-radius: 18px;
    box-shadow: 0 15px 30px rgba(2, 132, 199, 0.28);
    height: calc(var(--folder-H) * 1.7);
    width: 210px;
    margin: 14px auto 20px;
    position: relative;
    perspective: 600px;
  }

  .folder {
    position: absolute;
    top: -20px;
    left: calc(50% - 60px);
    animation: float 2.5s infinite ease-in-out;
    transition: transform var(--transition) ease;
  }

  #dropzone:hover .folder,
  .folder-container:hover .folder {
    transform: scale(1.06);
  }

  .folder .front-side,
  .folder .back-side {
    position: absolute;
    transition: transform var(--transition);
    transform-origin: bottom center;
  }

  .folder .back-side::before,
  .folder .back-side::after {
    content: "";
    display: block;
    background-color: white;
    opacity: 0.6;
    z-index: 0;
    width: var(--folder-W);
    height: var(--folder-H);
    position: absolute;
    transform-origin: bottom center;
    border-radius: 12px;
    transition: transform 350ms;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  }

  #dropzone:hover .back-side::before,
  .folder-container:hover .back-side::before {
    transform: rotateX(-5deg) skewX(5deg);
  }
  #dropzone:hover .back-side::after,
  .folder-container:hover .back-side::after {
    transform: rotateX(-15deg) skewX(12deg);
  }

  .folder .front-side {
    z-index: 1;
  }

  #dropzone:hover .front-side,
  .folder-container:hover .front-side {
    transform: rotateX(-40deg) skewX(15deg);
  }

  .folder .tip {
    background: linear-gradient(135deg, #ff9a56, #ff6f56);
    width: 80px;
    height: 20px;
    border-radius: 12px 12px 0 0;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
    position: absolute;
    top: -10px;
    z-index: 2;
  }

  .folder .cover {
    background: linear-gradient(135deg, #ffe563, #ffc663);
    width: var(--folder-W);
    height: var(--folder-H);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.22);
    border-radius: 10px;
  }

  .custom-file-upload {
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
    text-align: center;
    background: rgba(255, 255, 255, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.35);
    border-radius: 10px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
    cursor: pointer;
    transition: background var(--transition) ease, transform 0.2s ease;
    display: block;
    width: 100%;
    padding: 9px 18px;
    position: relative;
    z-index: 5;
    pointer-events: auto;
    text-decoration: none;
    letter-spacing: 0.01em;
  }

  #dropzone:hover .custom-file-upload,
  .custom-file-upload:hover {
    background: rgba(255, 255, 255, 0.4);
  }

  @keyframes float {
    0% {
      transform: translateY(0px);
    }
    50% {
      transform: translateY(-16px);
    }
    100% {
      transform: translateY(0px);
    }
  }

  .drop-primary {
    font-size: 18px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 6px;
  }
  .drop-secondary {
    font-size: 13px;
    color: var(--ink-muted);
  }
  input[type=file] { display: none; }

  /* ---------- Processing View ---------- */
  .processing {
    display: none;
    width: 100%;
    box-sizing: border-box;
    overflow-x: hidden;
  }
  .processing.active {
    display: block;
    animation: fadeIn 0.3s ease;
  }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

  .processing-layout {
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 24px;
    align-items: center;
    width: 100%;
    box-sizing: border-box;
    overflow-x: hidden;
  }
  @media (max-width: 768px) {
    .processing-layout {
      grid-template-columns: 1fr;
      justify-items: center;
      gap: 20px;
      overflow-x: hidden;
    }
  }

  /* Left: Lottie Scanner Stage with Blurred Media Preview */
  .lottie-scan-stage {
    position: relative;
    width: 90%;
    max-width: 380px;
    margin: 0 auto;
    box-sizing: border-box;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1.5px solid #bae6fd;
    padding: 24px 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 16px 36px -12px rgba(14, 165, 233, 0.12);
    min-height: 330px;
    text-align: center;
    overflow: hidden;
  }
  .scan-bg-preview {
    position: absolute;
    inset: -12px;
    background-size: cover;
    background-position: center;
    filter: blur(10px) brightness(0.96) saturate(1.1);
    transform: scale(1.12);
    opacity: 0;
    transition: opacity 0.5s ease;
    z-index: 0;
    pointer-events: none;
  }
  .scan-bg-preview.has-image {
    opacity: 0.6;
  }
  .scan-bg-overlay {
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    z-index: 1;
    pointer-events: none;
  }
  .scan-badge {
    position: relative;
    z-index: 2;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #0284c7;
    background: rgba(224, 242, 254, 0.92);
    backdrop-filter: blur(8px);
    padding: 5px 13px;
    border-radius: 9999px;
    margin-bottom: 8px;
    border: 1px solid rgba(186, 230, 253, 0.7);
    box-shadow: 0 2px 8px rgba(14, 165, 233, 0.15);
  }
  .scan-badge svg {
    width: 13px;
    height: 13px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2.2;
  }
  .lottie-container {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 250px;
    height: 140px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    box-sizing: border-box;
  }
  .lottie-container svg {
    width: 100% !important;
    height: 100% !important;
    max-width: 100%;
  }
  .stage-title {
    position: relative;
    z-index: 2;
    color: var(--ink);
    font-size: 16px;
    font-weight: 700;
    margin-top: 6px;
    margin-bottom: 3px;
    word-break: break-word;
    max-width: 100%;
    box-sizing: border-box;
  }
  .stage-sub {
    position: relative;
    z-index: 2;
    color: var(--ink-muted);
    font-size: 12.5px;
    max-width: 320px;
    width: 100%;
    margin: 0 auto 14px;
    line-height: 1.4;
    word-break: break-word;
    box-sizing: border-box;
  }
  .scan-progress-box {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 320px;
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(226, 232, 240, 0.95);
    border-radius: 12px;
    padding: 10px 14px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
    box-sizing: border-box;
  }
  .scan-progress-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
    color: var(--ink-muted);
    margin-bottom: 7px;
  }
  .scan-pct-value {
    font-size: 13px;
    font-weight: 800;
    color: var(--primary);
    font-variant-numeric: tabular-nums;
  }
  .scan-progress-track {
    width: 100%;
    height: 7px;
    background: #e2e8f0;
    border-radius: 999px;
    overflow: hidden;
  }
  .scan-progress-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #0ea5e9 0%, #0284c7 100%);
    border-radius: 999px;
    transition: width 0.35s ease;
  }

  /* Right Side: Details & Progress Chips */
  .processing-details {
    padding: 10px;
    text-align: left;
  }
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #0284c7;
    background: #e0f2fe;
    padding: 5px 12px;
    border-radius: 9999px;
    margin-bottom: 12px;
  }
  .status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #0284c7;
    animation: pulseDot 1.4s infinite;
  }
  @keyframes pulseDot { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.8); } }

  .details-title {
    font-size: 21px;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.25;
    margin-bottom: 8px;
  }
  .details-sub {
    font-size: 13.5px;
    color: var(--ink-muted);
    line-height: 1.55;
    margin-bottom: 22px;
  }

  /* Step track */
  .step-track {
    display: flex;
    flex-direction: column;
    gap: 9px;
  }
  .step-chip-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    font-weight: 600;
    color: var(--ink-faint);
  }
  .chip-indicator {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 1.5px solid var(--line);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 700;
    background: #fff;
    color: var(--ink-faint);
    transition: all 0.2s ease;
  }
  .step-chip-row.active {
    color: var(--primary);
  }
  .step-chip-row.active .chip-indicator {
    border-color: var(--primary);
    background: var(--sky-soft);
    color: var(--primary);
  }
  .step-chip-row.done {
    color: var(--ink);
  }
  .step-chip-row.done .chip-indicator {
    border-color: #10b981;
    background: #10b981;
    color: #fff;
  }

  /* Mobile Responsiveness for Processing UI Box (320px - 540px) */
  @media (max-width: 540px) {
    .tool-container {
      padding: 0 12px;
    }
    .main-tool-card {
      padding: 20px 12px;
      border-radius: 18px;
    }
    .lottie-scan-stage {
      width: 90%;
      max-width: 380px;
      margin: 0 auto;
      padding: 20px 12px;
    }
    .processing-details {
      width: 90%;
      max-width: 380px;
      margin: 16px auto 0;
      padding: 4px;
    }
  }

  @media (max-width: 375px) {
    .tool-container {
      padding: 0 6px;
    }
    .main-tool-card {
      padding: 14px 6px;
      border-radius: 14px;
    }
    .lottie-scan-stage {
      width: 90%;
      max-width: 380px;
      margin: 0 auto;
      padding: 16px 8px;
    }
    .scan-progress-box {
      padding: 8px 10px;
    }
    .processing-details {
      width: 90%;
      max-width: 380px;
      margin: 12px auto 0;
    }
  }

  @media (max-width: 330px) {
    .tool-container {
      padding: 0 4px;
    }
    .main-tool-card {
      padding: 12px 4px;
    }
    .lottie-scan-stage {
      width: 92%;
      padding: 14px 6px;
    }
  }

  /* ---------- Result View ---------- */
  .result {
    display: none;
    text-align: center;
    padding: 24px 0;
  }
  .result.active {
    display: block;
    animation: fadeIn 0.3s ease;
  }
  .result-icon-circle {
    width: 68px;
    height: 68px;
    background: #dcfce7;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    color: #16a34a;
  }
  .result-icon-circle svg { width: 34px; height: 34px; fill: none; stroke: currentColor; stroke-width: 2.5; }
  .result h3 {
    font-size: 23px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 6px;
  }
  .result p {
    font-size: 14.5px;
    color: var(--ink-muted);
    margin-bottom: 24px;
  }
  .result-actions {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 14px;
  }
  /* From Uiverse.io by nazar-gavrylyk */ 
  .container {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .label {
    background-color: #0f172a;
    border: 2px solid rgb(91, 91, 240);
    display: flex;
    align-items: center;
    border-radius: 50px;
    width: 160px;
    height: 57px;
    cursor: pointer;
    transition: all 0.4s ease;
    padding: 5px;
    position: relative;
    user-select: none;
    -webkit-user-select: none;
    box-sizing: border-box;
  }

  .label::before {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #fff;
    width: 8px;
    height: 8px;
    transition: all 0.4s ease;
    border-radius: 100%;
    margin: auto;
    opacity: 0;
    visibility: hidden;
  }

  .label .input {
    display: none;
  }

  .label .title {
    font-size: 16px;
    font-weight: 700;
    color: #fff;
    transition: all 0.4s ease;
    position: absolute;
    right: 18px;
    top: 50%;
    transform: translateY(-50%);
    text-align: center;
    margin: 0;
    line-height: 1;
  }

  .label .title:last-child {
    opacity: 0;
    visibility: hidden;
  }

  .label .circle {
    height: 45px;
    width: 45px;
    border-radius: 50%;
    background-color: rgb(91, 91, 240);
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.4s ease;
    position: relative;
    box-shadow: 0 0 0 0 rgb(255, 255, 255);
    overflow: hidden;
    flex-shrink: 0;
  }

  .label .circle .icon {
    color: #fff;
    width: 26px;
    height: 26px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    transition: all 0.4s ease;
  }

  .label .circle .square {
    aspect-ratio: 1;
    width: 15px;
    border-radius: 2px;
    background-color: #fff;
    opacity: 0;
    visibility: hidden;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    transition: all 0.4s ease;
  }

  .label .circle::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    background-color: #3333a8;
    width: 100%;
    height: 0;
    transition: all 0.4s ease;
  }

  .label:has(.input:checked),
  .label.is-checked {
    width: 57px;
    animation: installed 0.35s ease 2s forwards;
  }

  .label:has(.input:checked)::before,
  .label.is-checked::before {
    animation: rotate 1.8s ease-in-out 0.2s forwards;
  }

  .label .input:checked + .circle,
  .label.is-checked .circle {
    animation:
      pulse 0.8s forwards,
      circleDelete 0.2s ease 2s forwards;
    rotate: 180deg;
  }

  .label .input:checked + .circle::before,
  .label.is-checked .circle::before {
    animation: installing 1.8s ease-in-out forwards;
  }

  .label .input:checked + .circle .icon,
  .label.is-checked .circle .icon {
    opacity: 0;
    visibility: hidden;
  }

  .label .input:checked ~ .circle .square,
  .label.is-checked ~ .circle .square {
    opacity: 1;
    visibility: visible;
  }

  .label .input:checked ~ .title,
  .label.is-checked ~ .title {
    opacity: 0;
    visibility: hidden;
  }

  .label .input:checked ~ .title:last-child,
  .label.is-checked ~ .title:last-child {
    animation: showInstalledMessage 0.35s ease 2s forwards;
  }

  @keyframes pulse {
    0% {
      scale: 0.95;
      box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7);
    }
    70% {
      scale: 1;
      box-shadow: 0 0 0 16px rgba(255, 255, 255, 0);
    }
    100% {
      scale: 0.95;
      box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
    }
  }

  @keyframes installing {
    from {
      height: 0;
    }
    to {
      height: 100%;
    }
  }

  @keyframes rotate {
    0% {
      transform: rotate(-90deg) translate(27px) rotate(0);
      opacity: 1;
      visibility: visible;
    }
    99% {
      transform: rotate(270deg) translate(27px) rotate(270deg);
      opacity: 1;
      visibility: visible;
    }
    100% {
      opacity: 0;
      visibility: hidden;
    }
  }

  @keyframes installed {
    100% {
      width: 150px;
      border-color: rgb(35, 174, 35);
    }
  }

  @keyframes circleDelete {
    100% {
      opacity: 0;
      visibility: hidden;
    }
  }

  @keyframes showInstalledMessage {
    100% {
      opacity: 1;
      visibility: visible;
      right: 56px;
    }
  }
  .btn-reset {
    background: #ffffff;
    color: var(--ink);
    border: 2px solid #cbd5e1;
    font-size: 15.5px;
    font-weight: 700;
    height: 57px;
    padding: 0 28px;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.25s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    box-sizing: border-box;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    line-height: 1;
    margin: 0;
  }
  .btn-reset:hover {
    background: #f8fafc;
    border-color: #94a3b8;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  }
  .btn-reset svg {
    width: 17px;
    height: 17px;
    stroke: currentColor;
    fill: none;
    stroke-width: 2.2;
    transition: transform 0.3s ease;
  }
  .btn-reset:hover svg {
    transform: rotate(-45deg);
  }

  /* Error Box */
  .error-box {
    display: none;
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    font-size: 14px;
    text-align: left;
    margin-top: 20px;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .error-box.active { display: block; }

  /* ---------- Feature Cards (Image 4) ---------- */
  .section-features {
    max-width: 980px;
    margin: 80px auto 0;
    padding: 0 20px;
    text-align: center;
  }
  .features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 24px;
  }
  @media (max-width: 768px) {
    .features-grid { grid-template-columns: 1fr; }
  }
  .feature-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: var(--radius-md);
    padding: 26px;
    text-align: left;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .feature-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
  }
  .feature-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  .feature-icon-pill {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: #f0f9ff;
    color: #0284c7;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .feature-icon-pill svg { width: 22px; height: 22px; stroke: currentColor; fill: none; stroke-width: 2; }

  .free-badge {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: var(--green-badge);
    background: var(--green-badge-bg);
    padding: 4px 10px;
    border-radius: 9999px;
    text-transform: uppercase;
  }
  .feature-box h3 {
    font-size: 17px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 8px;
  }
  .feature-box p {
    font-size: 13.5px;
    color: var(--ink-muted);
    line-height: 1.6;
  }
  .features-footer-caption {
    font-size: 13.5px;
    color: var(--ink-muted);
    margin-top: 14px;
  }

  /* ---------- Before & After Section (Image 5) ---------- */
  .section-comparison {
    max-width: 980px;
    margin: 90px auto 0;
    padding: 0 20px;
  }
  .comparison-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: center;
  }
  @media (max-width: 800px) {
    .comparison-grid { grid-template-columns: 1fr; gap: 32px; }
  }
  .comp-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #4f46e5;
    margin-bottom: 12px;
    display: inline-block;
  }
  .comp-title {
    font-size: clamp(28px, 3.6vw, 40px);
    font-weight: 800;
    color: var(--ink);
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin-bottom: 18px;
  }
  .comp-desc {
    font-size: 15px;
    color: var(--ink-muted);
    line-height: 1.65;
    margin-bottom: 28px;
  }
  .comp-desc strong {
    color: var(--ink);
  }
  .comp-stats {
    display: flex;
    gap: 28px;
    flex-wrap: wrap;
    padding-top: 18px;
    border-top: 1px solid var(--line);
  }
  .comp-stat-item h4 {
    font-size: 16px;
    font-weight: 800;
    color: #4f46e5;
    margin-bottom: 2px;
  }
  .comp-stat-item p {
    font-size: 12px;
    color: var(--ink-muted);
  }

  /* Comparison Visual Interactive Split Slider */
  .comp-visuals-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 0;
    margin: 0;
  }

  /* ---------- Interactive Split Curtain Comparison Slider ---------- */
  .split-slider-container {
    position: relative;
    width: 100%;
    margin: 0 auto;
    padding: 0;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 16px 38px -8px rgba(15, 23, 42, 0.18), 0 0 0 1px rgba(226, 232, 240, 0.9);
    user-select: none;
    -webkit-user-select: none;
    touch-action: none;
    cursor: ew-resize;
    background: transparent !important;
  }
  #homepage-split-slider {
    width: 100%;
    max-width: 440px;
    aspect-ratio: 4 / 5;
    padding: 0;
    margin: 0 auto;
    overflow: hidden;
    background: transparent !important;
  }
  #user-split-slider {
    width: 100%;
    max-width: 620px;
    padding: 0;
    margin: 0 auto;
    overflow: hidden;
    background: transparent !important;
  }

  /* Result Mode Switcher (Compare Slider vs Box Eraser) */
  .result-mode-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin: 0 auto 16px;
    flex-wrap: wrap;
  }
  .mode-btn {
    padding: 8px 20px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 700;
    color: var(--ink-muted);
    background: #f1f5f9;
    border: 1px solid var(--line);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 7px;
    transition: all 0.2s ease;
    font-family: inherit;
    outline: none;
  }
  .mode-btn:hover {
    background: #e2e8f0;
    color: var(--ink);
  }
  .mode-btn.active {
    background: #0284c7;
    color: #ffffff;
    border-color: #0284c7;
    box-shadow: 0 2px 10px rgba(2, 132, 199, 0.28);
  }
  .mode-btn svg {
    width: 15px;
    height: 15px;
    stroke: currentColor;
    fill: none;
  }

  /* Interactive Box Eraser Overlay */
  .box-draw-overlay {
    position: absolute;
    inset: 0;
    z-index: 30;
    cursor: crosshair;
    user-select: none;
    -webkit-user-select: none;
  }
  .box-selection-rect {
    position: absolute;
    border: 2px dashed #0284c7;
    background: rgba(14, 165, 233, 0.22);
    border-radius: 5px;
    pointer-events: none;
    box-shadow: 0 0 12px rgba(2, 132, 199, 0.4);
    box-sizing: border-box;
  }
  .box-floating-bar {
    position: absolute;
    display: flex;
    align-items: center;
    gap: 6px;
    background: #0f172a;
    border: 1px solid rgba(255, 255, 255, 0.18);
    color: #ffffff;
    padding: 4px 6px;
    border-radius: 8px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    font-size: 12px;
    font-weight: 600;
    z-index: 50;
    white-space: nowrap;
    box-sizing: border-box;
    cursor: grab;
    user-select: none;
    -webkit-user-select: none;
    touch-action: none;
  }
  .box-floating-bar:active {
    cursor: grabbing;
  }
  .removix-toast {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%) translateY(30px);
    background: #0f172a;
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.4);
    padding: 11px 24px;
    border-radius: 9999px;
    font-size: 13.5px;
    font-weight: 700;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    opacity: 0;
    pointer-events: none;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 99999;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .removix-toast.show {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  .btn-box-erase {
    background: #0284c7;
    color: #ffffff;
    border: none;
    padding: 5px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 700;
    transition: background 0.15s ease;
    font-family: inherit;
  }
  .btn-box-erase:hover {
    background: #0369a1;
  }
  .btn-box-cancel {
    background: transparent;
    color: #94a3b8;
    border: none;
    cursor: pointer;
    font-size: 15px;
    padding: 0 4px;
    line-height: 1;
  }
  .btn-box-cancel:hover {
    color: #ffffff;
  }
  .box-hint-badge {
    position: absolute;
    top: 14px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(6px);
    color: #ffffff;
    font-size: 12.5px;
    font-weight: 600;
    padding: 5px 16px;
    border-radius: 9999px;
    pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    z-index: 40;
  }
  .split-layer {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    padding: 0;
    margin: 0;
    background: transparent !important;
  }
  .split-slider-container img,
  .split-layer img,
  .split-img {
    position: absolute;
    inset: 0;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: center !important;
    display: block;
    pointer-events: none;
    background: transparent !important;
  }
  #homepage-split-slider img,
  #homepage-split-slider .split-img {
    object-position: center 80% !important;
  }
  .split-before {
    clip-path: polygon(0 0, 50% 0, 50% 100%, 0 100%);
    z-index: 2;
  }
  .split-after {
    clip-path: polygon(50% 0, 100% 0, 100% 100%, 50% 100%);
    z-index: 2;
  }
  .split-handle {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    pointer-events: none;
    z-index: 5;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .split-line {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 2.5px;
    background: #ffffff;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);
  }
  .split-knob {
    width: 38px;
    height: 38px;
    background: #ffffff;
    border-radius: 50%;
    box-shadow: 0 4px 16px rgba(2, 132, 199, 0.4), 0 0 0 2px #0ea5e9;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #0284c7;
    z-index: 6;
  }
  .split-knob svg {
    width: 18px;
    height: 18px;
    stroke: currentColor;
    stroke-width: 2.5;
    fill: none;
  }
  .split-label {
    position: absolute;
    bottom: 12px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.03em;
    pointer-events: none;
    backdrop-filter: blur(8px);
    z-index: 4;
  }
  .before-label {
    left: 12px;
    background: rgba(15, 23, 42, 0.75);
    color: #f8fafc;
    border: 1px solid rgba(255, 255, 255, 0.15);
  }
  .after-label {
    right: 12px;
    background: rgba(2, 132, 199, 0.85);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.25);
  }
  .split-range {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: ew-resize;
    z-index: 10;
    margin: 0;
    padding: 0;
    pointer-events: none;
  }

  /* Result-specific slider wrap */
  .result-slider-container {
    margin: 18px auto 20px;
    max-width: 620px;
  }

  /* Removix Deep Clean Audit Card */
  .audit-card {
    max-width: 520px;
    margin: 18px auto 20px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 16px 18px;
    text-align: left;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03);
  }
  .audit-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e2e8f0;
  }
  .audit-badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 700;
    color: #0369a1;
  }
  .audit-badge-pill svg {
    width: 16px;
    height: 16px;
    stroke: currentColor;
    stroke-width: 2.2;
    fill: none;
  }
  .audit-status-tag {
    font-size: 11.5px;
    font-weight: 700;
    color: #15803d;
    background: #dcfce7;
    padding: 3px 8px;
    border-radius: 999px;
  }
  .audit-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  @media (max-width: 540px) {
    .audit-grid { grid-template-columns: 1fr; }
  }
  .audit-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
  }
  .audit-check {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #0284c7;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    flex-shrink: 0;
    margin-top: 1px;
  }
  .audit-item strong {
    display: block;
    font-size: 12px;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.25;
  }
  .audit-item small {
    display: block;
    font-size: 11px;
    color: var(--ink-muted);
    line-height: 1.3;
    margin-top: 2px;
  }

  /* ---------- Privacy / Local Processing Section (Image 2) ---------- */
  .section-privacy {
    max-width: 980px;
    margin: 100px auto 0;
    padding: 0 20px;
    text-align: center;
  }
  .privacy-title {
    font-size: clamp(28px, 4vw, 42px);
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--ink);
    margin-bottom: 40px;
  }
  .privacy-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    text-align: left;
  }
  @media (max-width: 768px) {
    .privacy-grid { grid-template-columns: 1fr; }
  }
  .privacy-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: var(--radius-md);
    padding: 30px 26px;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .privacy-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
  }
  .privacy-icon-box {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: #ecfdf5;
    color: #10b981;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
  }
  .privacy-icon-box svg { width: 22px; height: 22px; stroke: currentColor; fill: none; stroke-width: 2; }
  .privacy-card h3 {
    font-size: 17px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 10px;
  }
  .privacy-card p {
    font-size: 13.5px;
    color: var(--ink-muted);
    line-height: 1.6;
  }

  /* ---------- Modern Rounded Removix Footer ---------- */
  .app-footer-wrap {
    max-width: 980px;
    width: 100%;
    margin: 70px auto 40px;
    padding: 0 20px;
    box-sizing: border-box;
    clear: both;
  }

  .app-footer-card {
    background: var(--card-bg, #ffffff);
    border: 1px solid rgba(226, 232, 240, 0.95);
    border-radius: var(--radius-lg, 24px);
    box-shadow: 0 20px 45px -12px rgba(15, 23, 42, 0.08), 0 4px 16px -2px rgba(15, 23, 42, 0.03);
    padding: 38px 40px 28px;
    position: relative;
    overflow: hidden;
    box-sizing: border-box;
  }

  .footer-glow-bar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3.5px;
    background: linear-gradient(90deg, #38bdf8 0%, #0284c7 45%, #0ea5e9 75%, #38bdf8 100%);
  }

  .footer-main-grid {
    display: grid;
    grid-template-columns: 1.4fr 1fr 1fr;
    gap: 36px;
    align-items: start;
    text-align: left;
  }

  @media (max-width: 820px) {
    .app-footer-card {
      padding: 28px 24px 22px;
    }
    .footer-main-grid {
      grid-template-columns: 1fr;
      gap: 28px;
    }
  }

  .footer-brand-col {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .footer-brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
  }

  .footer-brand-icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    color: #0284c7;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.15);
  }

  .footer-brand-icon svg {
    width: 18px;
    height: 18px;
  }

  .footer-brand-title {
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--ink, #0f172a);
  }

  .footer-badge-pro {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #0284c7;
    background: #e0f2fe;
    padding: 3px 9px;
    border-radius: 9999px;
    border: 1px solid #bae6fd;
  }

  .footer-brand-desc {
    font-size: 13.5px;
    color: var(--ink-muted, #475569);
    line-height: 1.6;
    margin: 0;
    max-width: 380px;
  }

  .footer-pill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 4px;
  }

  .footer-pill-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11.5px;
    font-weight: 600;
    color: var(--ink, #0f172a);
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 5px 12px;
    border-radius: 9999px;
    transition: all 0.2s ease;
  }

  .footer-pill-tag:hover {
    background: #f0f9ff;
    border-color: #bae6fd;
  }

  .footer-nav-col {
    display: flex;
    flex-direction: column;
  }

  .footer-col-heading {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--ink, #0f172a);
    margin-bottom: 14px;
  }

  .footer-links-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .footer-nav-link {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    font-size: 13.5px;
    font-weight: 500;
    color: var(--ink-muted, #475569);
    text-decoration: none;
    transition: all 0.2s ease;
    padding: 2px 0;
  }

  .footer-nav-link svg {
    width: 15px;
    height: 15px;
    stroke: #94a3b8;
    fill: none;
    stroke-width: 2;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .footer-nav-link:hover {
    color: #0284c7;
    transform: translateX(3px);
  }

  .footer-nav-link:hover svg {
    stroke: #0284c7;
  }

  .footer-divider {
    height: 1px;
    background: #f1f5f9;
    margin: 30px 0 20px;
    width: 100%;
  }

  .footer-bottom-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 14px;
  }

  .footer-copy-wrap {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--ink-muted, #64748b);
    flex-wrap: wrap;
  }

  .footer-copy-wrap strong {
    color: var(--ink, #0f172a);
  }

  .footer-dot-sep {
    color: #cbd5e1;
  }

  .footer-copy-sub {
    color: var(--ink-faint, #94a3b8);
    font-size: 12.5px;
  }

  .footer-developer-card {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }

  .footer-dev-label {
    font-size: 13px;
    font-weight: 500;
    color: var(--ink-muted, #64748b);
  }

  .dev-link-modern {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border: 1px solid #bae6fd;
    color: #0284c7;
    font-size: 13px;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 9999px;
    text-decoration: none;
    box-shadow: 0 2px 6px rgba(2, 132, 199, 0.08);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .dev-link-modern svg {
    width: 13px;
    height: 13px;
    stroke: currentColor;
    fill: none;
    stroke-width: 2.3;
    transition: transform 0.2s ease;
  }

  .dev-link-modern:hover {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
    border-color: #0284c7;
    color: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(2, 132, 199, 0.28);
  }

  .dev-link-modern:hover svg {
    transform: translate(2px, -2px);
  }

/* ========== COMPREHENSIVE DARK MODE SYSTEM ========== */
html.dark-mode,
body.dark-mode,
html.dark-mode body {
  --primary: #38bdf8;
  --primary-hover: #0ea5e9;
  --primary-light: rgba(56, 189, 248, 0.16);
  --sky: #38bdf8;
  --sky-light: rgba(56, 189, 248, 0.16);
  --sky-soft: #162032;
  --ink: #f8fafc;
  --ink-secondary: #e2e8f0;
  --ink-muted: #94a3b8;
  --ink-faint: #64748b;
  --bg-page: #0b0f19;
  --card-bg: #162032;
  --line: #1e293b;
  --line-subtle: #1e293b;
  --green-badge: #4ade80;
  --green-badge-bg: rgba(22, 163, 74, 0.2);
  --shadow-card: 0 20px 45px -12px rgba(0, 0, 0, 0.6), 0 4px 16px -2px rgba(0, 0, 0, 0.4);
}

html.dark-mode body,
body.dark-mode {
  background-color: #0b0f19 !important;
  background-image: radial-gradient(1200px 600px at 50% -80px, rgba(14, 165, 233, 0.12) 0%, rgba(15, 23, 42, 0.35) 45%, rgba(11, 15, 25, 0) 100%) !important;
  color: #f8fafc !important;
}

/* 1. Main Tool Card & Hero */
html.dark-mode .hero h1,
body.dark-mode .hero h1 {
  color: #f8fafc !important;
}
html.dark-mode .hero-sub,
body.dark-mode .hero-sub {
  color: #94a3b8 !important;
}
html.dark-mode .hero-sub strong,
body.dark-mode .hero-sub strong {
  color: #f8fafc !important;
}
html.dark-mode .main-tool-card,
body.dark-mode .main-tool-card {
  background: #162032 !important;
  border-color: #1e293b !important;
  box-shadow: 0 20px 45px -12px rgba(0, 0, 0, 0.6) !important;
}

/* 2. Dropzone Box & Text */
html.dark-mode #dropzone,
html.dark-mode .dropzone-box,
html.dark-mode [id^="dropzone"],
body.dark-mode #dropzone,
body.dark-mode .dropzone-box,
body.dark-mode [id^="dropzone"] {
  background: #111827 !important;
  border-color: #0284c7 !important;
}
html.dark-mode #dropzone:hover,
html.dark-mode #dropzone.hover,
html.dark-mode .dropzone-box:hover,
html.dark-mode .dropzone-box.hover,
html.dark-mode [id^="dropzone"]:hover,
body.dark-mode #dropzone:hover,
body.dark-mode #dropzone.hover,
body.dark-mode .dropzone-box:hover,
body.dark-mode .dropzone-box.hover,
body.dark-mode [id^="dropzone"]:hover {
  background: #1e293b !important;
  border-color: #38bdf8 !important;
}
html.dark-mode .drop-primary,
body.dark-mode .drop-primary {
  color: #f8fafc !important;
}
html.dark-mode .drop-secondary,
body.dark-mode .drop-secondary {
  color: #94a3b8 !important;
}

/* 3. Feature Cards */
html.dark-mode .feature-box,
body.dark-mode .feature-box {
  background: #162032 !important;
  border-color: #1e293b !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35) !important;
}
html.dark-mode .feature-box:hover,
body.dark-mode .feature-box:hover {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.55) !important;
  border-color: #334155 !important;
}
html.dark-mode .feature-box h3,
body.dark-mode .feature-box h3 {
  color: #f8fafc !important;
}
html.dark-mode .feature-box p,
body.dark-mode .feature-box p {
  color: #94a3b8 !important;
}
html.dark-mode .feature-icon-pill,
body.dark-mode .feature-icon-pill,
[data-theme="dark"] .feature-icon-pill {
  background: rgba(56, 189, 248, 0.12) !important;
  color: #38bdf8 !important;
}
html.dark-mode .privacy-icon-box,
body.dark-mode .privacy-icon-box,
[data-theme="dark"] .privacy-icon-box {
  background: rgba(16, 185, 129, 0.16) !important;
  color: #34d399 !important;
}
html.dark-mode .result-icon-circle,
body.dark-mode .result-icon-circle,
[data-theme="dark"] .result-icon-circle {
  background: rgba(22, 163, 74, 0.18) !important;
  color: #4ade80 !important;
}

/* 4. Zone Pills & Mode Switchers */
html.dark-mode .zone-label,
body.dark-mode .zone-label {
  color: #94a3b8 !important;
}
html.dark-mode .zone-pill,
body.dark-mode .zone-pill {
  background: #1e293b !important;
  border-color: #334155 !important;
  color: #cbd5e1 !important;
}
html.dark-mode .zone-pill:hover,
body.dark-mode .zone-pill:hover {
  background: #334155 !important;
  color: #ffffff !important;
}
html.dark-mode .zone-pill.active,
body.dark-mode .zone-pill.active {
  background: #0284c7 !important;
  border-color: #0284c7 !important;
  color: #ffffff !important;
  box-shadow: 0 2px 10px rgba(2, 132, 199, 0.4) !important;
}

/* 5. Tool Config Cards, Trays, Audit Cards Across All Tools */
html.dark-mode [id$="-config-card"],
html.dark-mode [id$="-file-config"],
html.dark-mode [id*="config"],
html.dark-mode #images-tray,
html.dark-mode #collage-tray,
html.dark-mode .config-panel,
html.dark-mode .file-item-row,
html.dark-mode .audit-card,
body.dark-mode [id$="-config-card"],
body.dark-mode [id$="-file-config"],
body.dark-mode [id*="config"],
body.dark-mode #images-tray,
body.dark-mode #collage-tray,
body.dark-mode .config-panel,
body.dark-mode .file-item-row,
body.dark-mode .audit-card {
  background: #111827 !important;
  border-color: #1e293b !important;
  color: #f8fafc !important;
}

html.dark-mode .audit-header,
body.dark-mode .audit-header {
  border-color: #1e293b !important;
}
html.dark-mode .audit-badge-pill,
body.dark-mode .audit-badge-pill {
  color: #38bdf8 !important;
}
html.dark-mode .audit-item strong,
body.dark-mode .audit-item strong {
  color: #f8fafc !important;
}
html.dark-mode .audit-item small,
body.dark-mode .audit-item small {
  color: #94a3b8 !important;
}

/* 6. Form Controls: Selects, Inputs, Textareas */
html.dark-mode select,
html.dark-mode input[type="text"],
html.dark-mode input[type="number"],
html.dark-mode input[type="password"],
html.dark-mode textarea,
body.dark-mode select,
body.dark-mode input[type="text"],
body.dark-mode input[type="number"],
body.dark-mode input[type="password"],
body.dark-mode textarea {
  background: #162032 !important;
  border-color: #334155 !important;
  color: #f8fafc !important;
}
html.dark-mode select:focus,
html.dark-mode input:focus,
html.dark-mode textarea:focus,
body.dark-mode select:focus,
body.dark-mode input:focus,
body.dark-mode textarea:focus {
  border-color: #38bdf8 !important;
  outline: none !important;
}
html.dark-mode input::placeholder,
html.dark-mode textarea::placeholder,
body.dark-mode input::placeholder,
body.dark-mode textarea::placeholder {
  color: #64748b !important;
}

/* 7. Action Buttons (Secondary & Reset Buttons) */
html.dark-mode .btn-secondary,
body.dark-mode .btn-secondary {
  background: #1e293b !important;
  color: #e2e8f0 !important;
  border-color: #334155 !important;
}
html.dark-mode .btn-secondary:hover,
body.dark-mode .btn-secondary:hover {
  background: #334155 !important;
  color: #ffffff !important;
  border-color: #475569 !important;
}
html.dark-mode .btn-reset,
body.dark-mode .btn-reset {
  background: #162032 !important;
  color: #f8fafc !important;
  border-color: #334155 !important;
}
html.dark-mode .btn-reset:hover,
body.dark-mode .btn-reset:hover {
  background: #1e293b !important;
  border-color: #475569 !important;
  color: #ffffff !important;
}

/* 8. Result Cards & Preview Containers */
html.dark-mode .result h3,
body.dark-mode .result h3 {
  color: #f8fafc !important;
}
html.dark-mode .result p,
body.dark-mode .result p {
  color: #94a3b8 !important;
}

/* 9. Processing Lottie Scanner Stage Component */
html.dark-mode .lottie-scan-stage,
body.dark-mode .lottie-scan-stage {
  background: rgba(17, 24, 39, 0.75) !important;
  border-color: #1e293b !important;
}
html.dark-mode .scan-bg-overlay,
body.dark-mode .scan-bg-overlay {
  background: rgba(11, 15, 25, 0.75) !important;
}
html.dark-mode .scan-badge,
body.dark-mode .scan-badge {
  background: rgba(14, 165, 233, 0.2) !important;
  border-color: rgba(56, 189, 248, 0.35) !important;
  color: #38bdf8 !important;
}
html.dark-mode .stage-title,
html.dark-mode .details-title,
body.dark-mode .stage-title,
body.dark-mode .details-title {
  color: #f8fafc !important;
}
html.dark-mode .stage-sub,
html.dark-mode .details-sub,
body.dark-mode .stage-sub,
body.dark-mode .details-sub {
  color: #94a3b8 !important;
}
html.dark-mode .step-chip-row,
body.dark-mode .step-chip-row {
  color: #94a3b8 !important;
}
html.dark-mode .step-chip-row .chip-indicator,
body.dark-mode .step-chip-row .chip-indicator {
  background: #1e293b !important;
  border-color: #334155 !important;
  color: #cbd5e1 !important;
}
html.dark-mode .step-chip-row.active,
body.dark-mode .step-chip-row.active {
  color: #38bdf8 !important;
}
html.dark-mode .step-chip-row.active .chip-indicator,
body.dark-mode .step-chip-row.active .chip-indicator {
  background: rgba(56, 189, 248, 0.16) !important;
  border-color: #38bdf8 !important;
  color: #38bdf8 !important;
}
html.dark-mode .step-chip-row.done,
body.dark-mode .step-chip-row.done {
  color: #f1f5f9 !important;
}
html.dark-mode .step-chip-row.done .chip-indicator,
body.dark-mode .step-chip-row.done .chip-indicator {
  background: #10b981 !important;
  border-color: #10b981 !important;
  color: #ffffff !important;
}
html.dark-mode .status-badge,
body.dark-mode .status-badge {
  background: rgba(14, 165, 233, 0.15) !important;
  border-color: rgba(56, 189, 248, 0.3) !important;
  color: #38bdf8 !important;
}
html.dark-mode .scan-progress-box,
body.dark-mode .scan-progress-box {
  background: rgba(17, 24, 39, 0.85) !important;
  border-color: #1e293b !important;
}
html.dark-mode .scan-progress-track,
body.dark-mode .scan-progress-track {
  background: #1e293b !important;
}

/* 10. Footer Dark Theme */
html.dark-mode .app-footer-card,
body.dark-mode .app-footer-card {
  background: #111827 !important;
  border-color: #1e293b !important;
  box-shadow: 0 20px 45px -12px rgba(0, 0, 0, 0.6) !important;
}
html.dark-mode .footer-divider,
body.dark-mode .footer-divider {
  background: #1e293b !important;
}
html.dark-mode .footer-brand-title,
html.dark-mode .footer-col-heading,
body.dark-mode .footer-brand-title,
body.dark-mode .footer-col-heading {
  color: #f8fafc !important;
}
html.dark-mode .footer-brand-desc,
html.dark-mode .footer-nav-link,
html.dark-mode .footer-dev-label,
html.dark-mode .footer-copy-wrap,
body.dark-mode .footer-brand-desc,
body.dark-mode .footer-nav-link,
body.dark-mode .footer-dev-label,
body.dark-mode .footer-copy-wrap {
  color: #94a3b8 !important;
}
html.dark-mode .footer-nav-link:hover,
body.dark-mode .footer-nav-link:hover {
  color: #38bdf8 !important;
}
html.dark-mode .footer-pill-tag,
body.dark-mode .footer-pill-tag {
  background: #1e293b !important;
  border-color: #334155 !important;
  color: #cbd5e1 !important;
}
html.dark-mode .footer-pill-tag:hover,
body.dark-mode .footer-pill-tag:hover {
  background: #334155 !important;
  border-color: #475569 !important;
}
html.dark-mode .dev-link-modern,
body.dark-mode .dev-link-modern {
  background: rgba(56, 189, 248, 0.12) !important;
  border-color: rgba(56, 189, 248, 0.3) !important;
  color: #38bdf8 !important;
}
html.dark-mode .dev-link-modern:hover,
body.dark-mode .dev-link-modern:hover {
  background: #0284c7 !important;
  border-color: #0284c7 !important;
  color: #ffffff !important;
}

/* 11. Comparison Section (Video/Image Watermark Tools) */
html.dark-mode .section-comparison,
body.dark-mode .section-comparison {
  color: #f8fafc !important;
}
html.dark-mode .comp-title,
body.dark-mode .comp-title {
  color: #f8fafc !important;
}
html.dark-mode .comp-desc,
body.dark-mode .comp-desc {
  color: #94a3b8 !important;
}
html.dark-mode .comp-desc strong,
body.dark-mode .comp-desc strong {
  color: #f8fafc !important;
}
html.dark-mode .comp-stats,
body.dark-mode .comp-stats {
  border-color: #1e293b !important;
}
html.dark-mode .comp-stat-item p,
body.dark-mode .comp-stat-item p {
  color: #94a3b8 !important;
}
html.dark-mode .features-footer-caption,
body.dark-mode .features-footer-caption {
  color: #94a3b8 !important;
}

/* 12. Overriding Inline Styles In Tool Views */
html.dark-mode [style*="background:#f8fafc"],
html.dark-mode [style*="background: #f8fafc"],
html.dark-mode [style*="background:#ffffff"],
html.dark-mode [style*="background: #ffffff"],
html.dark-mode [style*="background:#f1f5f9"],
html.dark-mode [style*="background: #f1f5f9"],
body.dark-mode [style*="background:#f8fafc"],
body.dark-mode [style*="background: #f8fafc"],
body.dark-mode [style*="background:#ffffff"],
body.dark-mode [style*="background: #ffffff"],
body.dark-mode [style*="background:#f1f5f9"],
body.dark-mode [style*="background: #f1f5f9"] {
  background: #111827 !important;
  border-color: #1e293b !important;
}

html.dark-mode [style*="color:#0f172a"],
html.dark-mode [style*="color: #0f172a"],
html.dark-mode [style*="color:#1e293b"],
html.dark-mode [style*="color: #1e293b"],
body.dark-mode [style*="color:#0f172a"],
body.dark-mode [style*="color: #0f172a"],
body.dark-mode [style*="color:#1e293b"],
body.dark-mode [style*="color: #1e293b"] {
  color: #f8fafc !important;
}

html.dark-mode [style*="color:#475569"],
html.dark-mode [style*="color: #475569"],
html.dark-mode [style*="color:#64748b"],
html.dark-mode [style*="color: #64748b"],
body.dark-mode [style*="color:#475569"],
body.dark-mode [style*="color: #475569"],
body.dark-mode [style*="color:#64748b"],
body.dark-mode [style*="color: #64748b"] {
  color: #94a3b8 !important;
}

/* --- Injected Sidebar CSS --- */
{{SIDEBAR_CSS}}
</style>
</head>
<body class="removix-body">
<script>
  (function() {
    if (document.documentElement.classList.contains('dark-mode') || document.documentElement.getAttribute('data-theme') === 'dark') {
      document.body.classList.add('dark-mode');
      document.body.setAttribute('data-theme', 'dark');
    }
  })();
</script>
{{TOP_BAR_HTML}}

<div class="app-layout-shell">
  {{SIDEBAR_HTML}}
  <div class="sidebar-backdrop" id="sidebarBackdrop" onclick="toggleSidebarMenu()"></div>

  <main class="app-main-content-area" id="mainContentArea">
    <!-- Hero Section -->
<section class="hero">

  <h1>Removix Watermark Remover</h1>
  <p class="hero-sub">
    Drop any AI <strong>video or image</strong> and the watermark is gone in seconds — every frame, original quality, ready to post.
  </p>
</section>

<!-- Interactive Tool Container -->
<section class="tool-container" id="tool-section">
  <div class="main-tool-card">

    <!-- Mode Selector Tabs -->
    <div class="tool-tabs" id="tool-tabs">
      <button class="tool-tab active" id="tab-video" onclick="setMode('video')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg>
        Video Remover
      </button>
      <button class="tool-tab" id="tab-image" onclick="setMode('image')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
        Image Remover
      </button>
    </div>

    <!-- Watermark Target Zone Selector -->
    <div class="zone-pills-bar" id="zone-pills-bar">
      <span class="zone-label">Target Area:</span>
      <button type="button" class="zone-pill active" id="pill-auto" onclick="setZone('auto')">Auto AI Detect (All Tools)</button>
      <button type="button" class="zone-pill" id="pill-br" onclick="setZone('bottom-right')">Bottom-Right Corner</button>
      <button type="button" class="zone-pill" id="pill-bl" onclick="setZone('bottom-left')">Bottom-Left Corner</button>
    </div>

    <!-- Dropzone View (3D Floating Folder Animation by 3bdel3ziz-T) -->
    <div id="dropzone" tabindex="0">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side">
            <div class="tip"></div>
            <div class="cover"></div>
          </div>
          <div class="back-side cover"></div>
        </div>
        <label class="custom-file-upload" for="file">
          Choose a file
        </label>
      </div>
      <p class="drop-primary" id="drop-primary-text">Drop your video or image here, or browse</p>
      <p class="drop-secondary" id="drop-secondary-text">Supports MP4, MOV, WebM, MKV, PNG, JPG, WEBP • Max 4K resolution</p>
    </div>
    <input type="file" id="file" accept=".mp4,.mov,.m4v,.webm,.mkv,.avi,.flv,.png,.jpg,.jpeg,.webp">

    <!-- Processing View -->
    <div class="processing" id="processing">
      <div class="processing-layout">
        <!-- Lottie AI Scanner Stage -->
        <div class="lottie-scan-stage" id="lottie-scan-stage">
          <div class="scan-bg-preview" id="scan-bg-preview"></div>
          <div class="scan-bg-overlay"></div>
          <div class="scan-badge">
            <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            AI Frame Matrix Scanner
          </div>
          <div class="lottie-container" id="lottie-container"></div>
          <div class="stage-title" id="stage-title">Analyzing and detecting...</div>
          <p class="stage-sub" id="stage-sub">Reconstructing background and removing watermark cleanly</p>
          <div class="scan-progress-box">
            <div class="scan-progress-header">
              <span id="scan-file-label">Restoration progress</span>
              <span class="scan-pct-value" id="ring-pct">0%</span>
            </div>
            <div class="scan-progress-track">
              <div class="scan-progress-bar" id="player-progress-fill"></div>
            </div>
          </div>
        </div>

        <!-- Right Side: Details & Progress Chips -->
        <div class="processing-details">
          <div class="status-badge">
            <span class="status-dot"></span>
            PROCESSING
          </div>
          <h2 class="details-title" id="details-title">Restoring background with AI...</h2>
          <p class="details-sub">Analyzing pixels and reconstructing original background. One moment.</p>

          <div class="step-track">
            <div class="step-chip-row" id="chip-queued">
              <div class="chip-indicator">1</div>
              <span>Upload to server</span>
            </div>
            <div class="step-chip-row" id="chip-scanning">
              <div class="chip-indicator">2</div>
              <span>Scan frames & detect watermark</span>
            </div>
            <div class="step-chip-row" id="chip-removing">
              <div class="chip-indicator">3</div>
              <span>Intelligent background reconstruction</span>
            </div>
            <div class="step-chip-row" id="chip-finalizing">
              <div class="chip-indicator">4</div>
              <span>Finalizing clean stream</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Result View -->
    <div class="result" id="result">
      <div class="result-icon-circle">
        <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3>Watermark Removed — Clean & Seamless</h3>
      <p>Smart AI reconstruction. Original texture and detail preserved.</p>

      <!-- Interactive Mode Bar: Compare vs Box Eraser -->
      <div class="result-mode-bar" id="result-mode-bar" style="display:none;">
        <button type="button" class="mode-btn active" id="btn-mode-slider" onclick="setResultMode('slider')">
          <svg viewBox="0 0 24 24"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/><line x1="12" y1="3" x2="12" y2="21"/></svg>
          Compare Slider
        </button>
        <button type="button" class="mode-btn" id="btn-mode-eraser" onclick="setResultMode('eraser')">
          <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" stroke-dasharray="3 3"/><path d="M7 17l10-10"/></svg>
          Select & Erase Watermark
        </button>
      </div>

      <!-- Live Interactive Comparison Slider for User Upload -->
      <div class="result-slider-container" id="user-split-wrap" style="display:none;">
        <div class="split-slider-container" id="user-split-slider">
          <div class="split-layer split-before">
            <img src="" id="user-img-before" alt="Original" class="split-img">
            <span class="split-label before-label">Original</span>
          </div>
          <div class="split-layer split-after" id="user-split-after">
            <img src="" id="user-img-after" alt="Cleaned image" class="split-img">
            <span class="split-label after-label" id="after-layer-label">Watermark Removed</span>
          </div>
          <div class="split-handle" id="user-split-handle">
            <div class="split-line"></div>
            <div class="split-knob">
              <svg viewBox="0 0 24 24"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/></svg>
            </div>
          </div>
          <input type="range" min="0" max="100" value="50" class="split-range" id="user-range" aria-label="Compare Original and Cleaned">

          <!-- Interactive Box Eraser Overlay -->
          <div class="box-draw-overlay" id="box-draw-overlay" style="display:none;">
            <div class="box-selection-rect" id="box-selection-rect" style="display:none;"></div>
            <div class="box-floating-bar" id="box-floating-bar" style="display:none;" title="Drag anywhere to move bar">
              <button type="button" class="btn-box-erase" id="btn-box-erase" onclick="submitBoxErase()">⚡ Erase with AI</button>
              <button type="button" class="btn-box-cancel" onclick="cancelBoxSelection()" title="Cancel">✕</button>
            </div>
            <div class="box-hint-badge" id="box-hint-badge">Drag mouse over watermark to select & erase</div>
          </div>
        </div>
      </div>

      <!-- Removix AI Provenance Audit Badge -->
      <div class="audit-card">
        <div class="audit-header">
          <div class="audit-badge-pill">
            <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span>Removix Deep Clean Audit</span>
          </div>
          <span class="audit-status-tag">✓ 100% Seamlessly Restored</span>
        </div>
        <div class="audit-grid">
          <div class="audit-item">
            <div class="audit-check">✓</div>
            <div>
              <strong>Visible AI Watermark</strong>
              <small>Seamless AI reconstruction</small>
            </div>
          </div>
          <div class="audit-item">
            <div class="audit-check">✓</div>
            <div>
              <strong>Zero Smudge Guarantee</strong>
              <small>Original texture & grain preserved</small>
            </div>
          </div>
          <div class="audit-item">
            <div class="audit-check">✓</div>
            <div>
              <strong>AI Provenance & Metadata</strong>
              <small>Generative markers removed</small>
            </div>
          </div>
          <div class="audit-item">
            <div class="audit-check">✓</div>
            <div>
              <strong>Lossless Dimensions</strong>
              <small>Byte-identical pixels outside watermark</small>
            </div>
          </div>
        </div>
      </div>
      <div class="result-actions">
        <!-- From Uiverse.io by nazar-gavrylyk --> 
        <div class="container">
          <label class="label" id="dl-label">
            <input type="checkbox" class="input" id="dl-checkbox" />
            <span class="circle">
              <svg
                class="icon"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M12 19V5m0 14-4-4m4 4 4-4"
                ></path>
              </svg>
              <div class="square"></div>
            </span>
            <p class="title">Download</p>
            <p class="title">Open</p>
          </label>
        </div>
        <button class="btn-reset" id="reset-btn">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Clean Another File
        </button>
      </div>
    </div>

    <!-- Error Box -->
    <div class="error-box" id="error-box"></div>

  </div>
</section>

<!-- Feature Cards Section (Image 4) -->
<section class="section-features">
  <div class="features-grid">
    <!-- Card 1 -->
    <div class="feature-box">
      <div class="feature-top">
        <div class="feature-icon-pill">
          <svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg>
        </div>
        <span class="free-badge">FREE</span>
      </div>
      <h3>Visible logo, lifted</h3>
      <p>The AI watermark sparkle is tracked and removed frame-to-frame without annoying blurs or corner crops.</p>
    </div>

    <!-- Card 2 -->
    <div class="feature-box">
      <div class="feature-top">
        <div class="feature-icon-pill">
          <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
        </div>
        <span class="free-badge">FREE</span>
      </div>
      <h3>Every frame, clean</h3>
      <p>The logo is removed across the whole clip, no flicker, no smear. Frame coherence is preserved 100%.</p>
    </div>

    <!-- Card 3 -->
    <div class="feature-box">
      <div class="feature-top">
        <div class="feature-icon-pill">
          <svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        </div>
        <span class="free-badge">FREE</span>
      </div>
      <h3>Pixel-perfect quality</h3>
      <p>Resolution, frame rate, and bitrate stay exactly as rendered. Audio stream passes untouched.</p>
    </div>
  </div>

  <p class="features-footer-caption">
    No re-encode penalty, resolution, frame rate, and bitrate stay exactly as originally rendered.
  </p>
</section>

<!-- Before & After Comparison Section (Image 5) -->
<section class="section-comparison">
  <div class="comparison-grid">
    <div class="comp-text-col">
      <span class="comp-label">Removix Image & Video Engine</span>
      <h2 class="comp-title">How to remove the watermark from an image</h2>
      <p class="comp-desc">
        Switch to the Image tab, drop in any Gemini, Imagen or AI picture, and the <strong>Removix image watermark remover</strong> lifts the sparkle logo automatically at the original resolution. Intelligent background reconstruction restores the watermark area with seamless precision. Outside the watermark zone, every pixel is byte-identical to the original. No compression. No artifacts. No quality loss.
      </p>

      <div class="comp-stats">
        <div class="comp-stat-item">
          <h4>byte-identical</h4>
          <p>Outside watermark</p>
        </div>
        <div class="comp-stat-item">
          <h4>unchanged</h4>
          <p>Dimensions</p>
        </div>
        <div class="comp-stat-item">
          <h4>none</h4>
          <p>Re-compression</p>
        </div>
      </div>
    </div>

    <!-- Interactive Split Curtain Comparison Slider -->
    <div class="comp-visuals-wrapper">
      <div class="split-slider-container" id="homepage-split-slider">
        <div class="split-layer split-before">
          <img src="/static/before.webp?v=8" onerror="if(this.src.indexOf('/before.webp')===-1)this.src='/before.webp'" width="1684" height="2528" alt="Original" class="split-img" loading="eager">
          <span class="split-label before-label">Original</span>
        </div>
        <div class="split-layer split-after" id="homepage-split-after">
          <img src="/static/after.webp?v=8" onerror="if(this.src.indexOf('/after.webp')===-1)this.src='/after.webp'" width="1684" height="2528" alt="Watermark Removed" class="split-img" loading="eager">
          <span class="split-label after-label">Watermark Removed</span>
        </div>
        <div class="split-handle" id="homepage-split-handle">
          <div class="split-line"></div>
          <div class="split-knob">
            <svg viewBox="0 0 24 24"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/></svg>
          </div>
        </div>
        <input type="range" min="0" max="100" value="50" class="split-range" id="homepage-range" aria-label="Compare Before and After">
      </div>
    </div>
  </div>
</section>

<!-- "Your images never leave your device" Privacy Section (Image 2) -->
<section class="section-privacy">
  <h2 class="privacy-title">Your images never leave your device</h2>

  <div class="privacy-grid">
    <!-- Card 1 -->
    <div class="privacy-card">
      <div class="privacy-icon-box">
        <svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
      </div>
      <h3>Local processing</h3>
      <p>Everything runs directly on your machine. Your images are never uploaded to external servers. We never see them. We never store them.</p>
    </div>

    <!-- Card 2 -->
    <div class="privacy-card">
      <div class="privacy-icon-box">
        <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3>Personal & commercial use</h3>
      <p>Use the cleaned images for client work, social posts, marketing campaigns, presentations, anything you'd use a regular photo for.</p>
    </div>

    <!-- Card 3 -->
    <div class="privacy-card">
      <div class="privacy-icon-box">
        <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      </div>
      <h3>Regulated industries</h3>
      <p>Healthcare, legal, and finance: your images stay on your device. No data leakage. No compliance risk. No third-party transmission.</p>
    </div>
  </div>
</section>

<!-- Modern Rounded Removix Footer -->
<footer class="app-footer-wrap">
  <div class="app-footer-card">
    <div class="footer-glow-bar"></div>

    <div class="footer-main-grid">
      <!-- Left Column: Brand & Security Badges -->
      <div class="footer-brand-col">
        <div class="footer-brand-badge">
          <div class="footer-brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <span class="footer-brand-title">Removix</span>
        </div>
        <p class="footer-brand-desc">
          Universal on-device AI media suite. Built for creators, photographers, and developers with 100% offline privacy and zero cloud transmission.
        </p>
        <div class="footer-pill-tags">
          <span class="footer-pill-tag">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="#16a34a" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            100% Local &amp; Private
          </span>
          <span class="footer-pill-tag">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="#0284c7" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            Hardware Accelerated
          </span>
          <span class="footer-pill-tag">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="#6366f1" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
            Zero-Latency
          </span>
        </div>
      </div>

      <!-- Right Column 1: AI Media Tools -->
      <div class="footer-nav-col">
        <h4 class="footer-col-heading">AI Media Tools</h4>
        <ul class="footer-links-list">
          <li><a href="/" class="footer-nav-link"><svg viewBox="0 0 24 24"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg> Video Watermark</a></li>
          <li><a href="/image-watermark" class="footer-nav-link"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg> Image Watermark</a></li>
          <li><a href="/bg-remove" class="footer-nav-link"><svg viewBox="0 0 24 24"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12"/></svg> Background Remover</a></li>
          <li><a href="/image-to-text" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg> Image to Text (OCR)</a></li>
        </ul>
      </div>

      <!-- Right Column 2: Document & Converter Tools -->
      <div class="footer-nav-col">
        <h4 class="footer-col-heading">Converters &amp; Utilities</h4>
        <ul class="footer-links-list">
          <li><a href="/image-to-pdf" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M9 15h6M9 11h2M9 19h6"/></svg> Image to PDF</a></li>
          <li><a href="/pdf-to-image" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><circle cx="10" cy="13" r="2"/></svg> PDF to Image</a></li>
          <li><a href="/format-convert" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M7 16l-4-4m0 0l4-4m-4 4h18M17 8l4 4m0 0l-4 4m4-4H3"/></svg> Format Convert</a></li>
          <li><a href="/qr-code" class="footer-nav-link"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg> QR Generator</a></li>
        </ul>
      </div>
    </div>

    <!-- Divider Bar -->
    <div class="footer-divider"></div>

    <!-- Bottom Attribution Row -->
    <div class="footer-bottom-row">
      <div class="footer-copy-wrap">
        <span>Copyright &copy; 2026 <strong>Removix</strong>. All rights reserved.</span>
        <span class="footer-dot-sep">•</span>
        <span class="footer-copy-sub">Offline Precision Engine</span>
      </div>

      <div class="footer-developer-card">
        <span class="footer-dev-label">Developed by</span>
        <a href="https://shivankthakur.com/" target="_blank" rel="noopener noreferrer" class="dev-link-modern" title="Visit Shivank Thakur Portfolio">
          <span>Shivank Thakur</span>
          <svg viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>
  </main>
</div>

<script>
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file');
const processingEl = document.getElementById('processing');
const resultEl = document.getElementById('result');
const errorBox = document.getElementById('error-box');
const ringPct = document.getElementById('ring-pct');
const stageTitle = document.getElementById('stage-title');
const stageSub = document.getElementById('stage-sub');
const playerProgressFill = document.getElementById('player-progress-fill');
const scanFileLabel = document.getElementById('scan-file-label');
const dlCheckbox = document.getElementById('dl-checkbox');
const dlLabel = document.getElementById('dl-label');
const resetBtn = document.getElementById('reset-btn');

let currentMode = 'video';
let currentZone = 'auto';
let currentResultMode = 'slider';
let currentJobId = '';
let currentJobFilename = '';
let isDrawingBox = false;
let boxStartX = 0, boxStartY = 0;
let activeBox = null;
let pollTimer = null;
let lottieAnim = null;
let currentDownloadUrl = '';
let currentDownloadFilename = '';
let isDownloadComplete = false;

function setZone(zone) {
  currentZone = zone;
  document.querySelectorAll('.zone-pill').forEach(p => p.classList.remove('active'));
  const idMap = { 'auto': 'pill-auto', 'bottom-right': 'pill-br', 'bottom-left': 'pill-bl' };
  const btn = document.getElementById(idMap[zone]);
  if (btn) btn.classList.add('active');
}

function showToast(msg) {
  // Toast notifications disabled per user request
}

function triggerDownload() {
  if (!currentJobId) return;

  const isDesktop = !!(window.pywebview || window.__removix_desktop);

  fetch('/api/save_to_downloads/' + currentJobId, { method: 'POST' })
    .then(r => r.json())
    .then(data => {
      if (data && data.status === 'ok') {
        if (!isDesktop) {
          fallbackBrowserDownload();
        }
      } else {
        fallbackBrowserDownload();
      }
    })
    .catch(() => {
      fallbackBrowserDownload();
    });
}

function fallbackBrowserDownload() {
  if (!currentDownloadUrl) return;
  const a = document.createElement('a');
  a.href = currentDownloadUrl;
  a.download = currentDownloadFilename || 'removix_clean_file';
  document.body.appendChild(a);
  a.click();
  a.remove();
}

if (dlCheckbox) {
  dlCheckbox.addEventListener('change', () => {
    if (dlCheckbox.checked) {
      if (dlLabel) dlLabel.classList.add('is-checked');
      triggerDownload();
      setTimeout(() => {
        isDownloadComplete = true;
      }, 2350);
    }
  });

  dlCheckbox.addEventListener('click', (e) => {
    if (isDownloadComplete) {
      e.preventDefault();
      triggerDownload();
    }
  });
}

function initLottie() {
  if (lottieAnim) return;
  const container = document.getElementById('lottie-container');
  if (!container || !window.lottie) return;
  try {
    lottieAnim = window.lottie.loadAnimation({
      container: container,
      renderer: 'svg',
      loop: true,
      autoplay: true,
      path: '/api/animation.json'
    });
  } catch (e) {
    console.warn('Lottie failed to load', e);
  }
}

// Preload Lottie animation on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initLottie);
} else {
  initLottie();
}

const STAGES = {
  queued:     { title: 'Uploading file...',            sub: 'Preparing media and initializing AI restoration engine.' },
  scanning:   { title: 'Analyzing and detecting...',   sub: 'Detecting watermark coordinates with intelligent precision.' },
  removing:   { title: 'Reconstructing with AI...',    sub: 'Intelligent background reconstruction in progress.' },
  finalizing: { title: 'Finalizing clean output...',   sub: 'Saving the clean, restored file with zero quality loss.' },
};
const stageOrder = ['queued', 'scanning', 'removing', 'finalizing', 'done'];

function setMode(mode) {
  currentMode = mode;
  document.getElementById('tab-video').classList.toggle('active', mode === 'video');
  document.getElementById('tab-image').classList.toggle('active', mode === 'image');
  if (mode === 'video') {
    fileInput.accept = ".mp4,.mov,.m4v,.webm,.mkv,.avi,.flv";
    document.getElementById('drop-primary-text').textContent = "Drop your video here, or browse";
    document.getElementById('drop-secondary-text').textContent = "Supports MP4, MOV, WebM, MKV • Up to 4K resolution";
  } else {
    fileInput.accept = ".png,.jpg,.jpeg,.webp";
    document.getElementById('drop-primary-text').textContent = "Drop your image here, or browse";
    document.getElementById('drop-secondary-text').textContent = "Supports PNG, JPG, JPEG, WEBP • Lossless quality";
  }
}

['dragenter','dragover'].forEach(evt =>
  dropzone.addEventListener(evt, e => { e.preventDefault(); dropzone.classList.add('hover'); }));
['dragleave','drop'].forEach(evt =>
  dropzone.addEventListener(evt, e => { e.preventDefault(); dropzone.classList.remove('hover'); }));
dropzone.addEventListener('drop', e => { const f = e.dataTransfer.files[0]; if (f) startJob(f); });
dropzone.addEventListener('click', e => {
  if (e.target !== fileInput && !e.target.closest('label[for="file"]')) {
    fileInput.click();
  }
});
dropzone.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') fileInput.click(); });
fileInput.addEventListener('change', e => { if (e.target.files[0]) startJob(e.target.files[0]); });
resetBtn.addEventListener('click', resetUI);

let maxProgressSeen = 0;
function setProgress(percent, msg) {
  let p = Math.max(0, Math.min(100, (percent !== null && percent !== undefined) ? percent : 0));
  if (p < maxProgressSeen && p > 0 && maxProgressSeen < 100) {
    p = maxProgressSeen;
  } else {
    maxProgressSeen = p;
  }
  if (ringPct) ringPct.textContent = Math.round(p) + '%';
  if (playerProgressFill) playerProgressFill.style.width = p + '%';
  if (msg && stageSub) {
    stageSub.textContent = msg;
    stageSub.setAttribute('data-custom', '1');
  } else if (!msg && stageSub) {
    stageSub.removeAttribute('data-custom');
  }
}

function resetUI() {
  maxProgressSeen = 0;
  cleanupStream();
  processingEl.classList.remove('active');
  resultEl.classList.remove('active');
  errorBox.classList.remove('active');
  dropzone.style.display = '';
  document.getElementById('tool-tabs').style.display = 'flex';
  const zoneBar = document.getElementById('zone-pills-bar');
  if (zoneBar) zoneBar.style.display = 'flex';
  setZone('auto');
  const bgPreview = document.getElementById('scan-bg-preview');
  if (bgPreview) {
    bgPreview.style.backgroundImage = '';
    bgPreview.classList.remove('has-image');
  }
  if (ringPct) ringPct.textContent = '0%';
  if (playerProgressFill) playerProgressFill.style.width = '0%';
  if (stageSub) stageSub.removeAttribute('data-custom');
  document.querySelectorAll('.step-chip-row').forEach(c => c.classList.remove('active','done'));
  if (lottieAnim) {
    lottieAnim.pause();
  }
  if (dlCheckbox) dlCheckbox.checked = false;
  if (dlLabel) dlLabel.classList.remove('is-checked');
  isDownloadComplete = false;
  currentDownloadUrl = '';
  currentDownloadFilename = '';
  fileInput.value = '';
  const userWrap = document.getElementById('user-split-wrap');
  if (userWrap) userWrap.style.display = 'none';
  const modeBar = document.getElementById('result-mode-bar');
  if (modeBar) modeBar.style.display = 'none';
  cancelBoxSelection();
  setResultMode('slider');
  currentJobId = '';
  const beforeImg = document.getElementById('user-img-before');
  const afterImg = document.getElementById('user-img-after');
  if (beforeImg) beforeImg.src = '';
  if (afterImg) afterImg.src = '';
}

function setResultMode(mode) {
  currentResultMode = mode;
  const btnSlider = document.getElementById('btn-mode-slider');
  const btnEraser = document.getElementById('btn-mode-eraser');
  const overlay = document.getElementById('box-draw-overlay');
  const userRange = document.getElementById('user-range');
  const userHandle = document.getElementById('user-split-handle');
  const beforeLayer = document.querySelector('#user-split-slider .split-before');
  const afterLayer = document.querySelector('#user-split-slider .split-after');
  const afterLabel = document.getElementById('after-layer-label');

  if (mode === 'slider') {
    if (btnSlider) btnSlider.classList.add('active');
    if (btnEraser) btnEraser.classList.remove('active');
    if (overlay) overlay.style.display = 'none';
    if (userRange) userRange.style.display = 'block';
    if (userHandle) userHandle.style.display = 'flex';
    if (afterLabel) afterLabel.textContent = 'Watermark Removed';
    cancelBoxSelection();
    const val = userRange ? userRange.value : 50;
    if (beforeLayer) beforeLayer.style.clipPath = `polygon(0 0, ${val}% 0, ${val}% 100%, 0 100%)`;
    if (afterLayer) afterLayer.style.clipPath = `polygon(${val}% 0, 100% 0, 100% 100%, ${val}% 100%)`;
    if (userHandle) userHandle.style.left = val + '%';
  } else {
    if (btnEraser) btnEraser.classList.add('active');
    if (btnSlider) btnSlider.classList.remove('active');
    if (userRange) userRange.style.display = 'none';
    if (userHandle) userHandle.style.display = 'none';
    if (beforeLayer) beforeLayer.style.clipPath = 'polygon(0 0, 0 0, 0 100%, 0 100%)';
    if (afterLayer) afterLayer.style.clipPath = 'polygon(0 0, 100% 0, 100% 100%, 0 100%)';
    if (afterLabel) afterLabel.textContent = 'Select Area to Erase';
    if (overlay) overlay.style.display = 'block';
    cancelBoxSelection();
  }
}

function cancelBoxSelection() {
  activeBox = null;
  const rectEl = document.getElementById('box-selection-rect');
  const floatBar = document.getElementById('box-floating-bar');
  if (rectEl) {
    rectEl.style.display = 'none';
    rectEl.style.transition = 'none';
  }
  if (floatBar) floatBar.style.display = 'none';
}

function positionFloatBar() {
  const overlay = document.getElementById('box-draw-overlay');
  const floatBar = document.getElementById('box-floating-bar');
  if (!overlay || !floatBar || !activeBox) return;

  floatBar.style.display = 'flex';
  const barWidth = floatBar.offsetWidth || 140;
  const barHeight = floatBar.offsetHeight || 32;
  const pad = 8;
  const ovW = overlay.clientWidth;
  const ovH = overlay.clientHeight;

  // Decide whether to place above or below the box
  let barTop;
  const spaceBelow = ovH - (activeBox.y + activeBox.h);
  const spaceAbove = activeBox.y;

  if (spaceBelow < barHeight + pad + 6 && spaceAbove >= barHeight + pad) {
    // Not enough room below -> Place ABOVE the box
    barTop = activeBox.y - barHeight - 8;
  } else if (spaceBelow >= barHeight + pad + 6) {
    // Plenty of room below -> Place BELOW the box
    barTop = activeBox.y + activeBox.h + 8;
  } else {
    // Box covers most of vertical space, clamp inside
    barTop = Math.max(pad, Math.min(ovH - barHeight - pad, activeBox.y + activeBox.h - barHeight - 8));
  }

  // Strictly clamp inside overlay vertical boundaries
  barTop = Math.max(pad, Math.min(ovH - barHeight - pad, barTop));

  // Horizontal position:
  // Align with activeBox.x, but ensure it NEVER overflows right or left
  let barLeft = activeBox.x;
  if (barLeft + barWidth > ovW - pad) {
    barLeft = ovW - barWidth - pad;
  }
  barLeft = Math.max(pad, barLeft);

  floatBar.style.top = Math.round(barTop) + 'px';
  floatBar.style.left = Math.round(barLeft) + 'px';
}

let isDraggingBar = false;
let barDragStartX = 0, barDragStartY = 0;
let barInitialLeft = 0, barInitialTop = 0;

function initFloatBarDraggable() {
  const floatBar = document.getElementById('box-floating-bar');
  const overlay = document.getElementById('box-draw-overlay');
  if (!floatBar || !overlay || floatBar._hasDragInit) return;
  floatBar._hasDragInit = true;

  floatBar.addEventListener('pointerdown', (e) => {
    if (e.target.closest('button')) return;
    isDraggingBar = true;
    barDragStartX = e.clientX;
    barDragStartY = e.clientY;
    barInitialLeft = parseFloat(floatBar.style.left) || 0;
    barInitialTop = parseFloat(floatBar.style.top) || 0;
    try { floatBar.setPointerCapture(e.pointerId); } catch(err) {}
    e.stopPropagation();
  });

  floatBar.addEventListener('pointermove', (e) => {
    if (!isDraggingBar) return;
    const dx = e.clientX - barDragStartX;
    const dy = e.clientY - barDragStartY;
    const maxLeft = Math.max(6, overlay.clientWidth - floatBar.offsetWidth - 6);
    const maxTop = Math.max(6, overlay.clientHeight - floatBar.offsetHeight - 6);
    const newLeft = Math.max(6, Math.min(maxLeft, barInitialLeft + dx));
    const newTop = Math.max(6, Math.min(maxTop, barInitialTop + dy));
    floatBar.style.left = Math.round(newLeft) + 'px';
    floatBar.style.top = Math.round(newTop) + 'px';
    e.stopPropagation();
  });

  const stopBarDrag = (e) => {
    if (isDraggingBar) {
      isDraggingBar = false;
      try { floatBar.releasePointerCapture(e.pointerId); } catch(err) {}
      e.stopPropagation();
    }
  };

  floatBar.addEventListener('pointerup', stopBarDrag);
  floatBar.addEventListener('pointercancel', stopBarDrag);
}

function initBoxEraserEvents() {
  const overlay = document.getElementById('box-draw-overlay');
  const rectEl = document.getElementById('box-selection-rect');
  const floatBar = document.getElementById('box-floating-bar');
  if (!overlay || !rectEl || !floatBar) return;

  initFloatBarDraggable();

  const onDown = (e) => {
    if (e.target.closest('#box-floating-bar')) return;
    const r = overlay.getBoundingClientRect();
    boxStartX = e.clientX - r.left;
    boxStartY = e.clientY - r.top;
    isDrawingBox = true;
    activeBox = null;
    floatBar.style.display = 'none';
    rectEl.style.display = 'block';
    rectEl.style.transition = 'none';
    rectEl.style.left = boxStartX + 'px';
    rectEl.style.top = boxStartY + 'px';
    rectEl.style.width = '0px';
    rectEl.style.height = '0px';
    try { overlay.setPointerCapture(e.pointerId); } catch(err) {}
  };

  const onMove = (e) => {
    if (!isDrawingBox) return;
    const r = overlay.getBoundingClientRect();
    const curX = Math.max(0, Math.min(r.width, e.clientX - r.left));
    const curY = Math.max(0, Math.min(r.height, e.clientY - r.top));
    const x = Math.min(boxStartX, curX);
    const y = Math.min(boxStartY, curY);
    const w = Math.abs(curX - boxStartX);
    const h = Math.abs(curY - boxStartY);
    rectEl.style.left = x + 'px';
    rectEl.style.top = y + 'px';
    rectEl.style.width = w + 'px';
    rectEl.style.height = h + 'px';
    activeBox = { x, y, w, h };
  };

  const onUp = (e) => {
    if (!isDrawingBox) return;
    isDrawingBox = false;
    try { overlay.releasePointerCapture(e.pointerId); } catch(err) {}
    if (!activeBox || activeBox.w < 6 || activeBox.h < 6) {
      cancelBoxSelection();
      return;
    }
    positionFloatBar();
  };

  overlay.addEventListener('pointerdown', onDown);
  overlay.addEventListener('pointermove', onMove);
  overlay.addEventListener('pointerup', onUp);
  overlay.addEventListener('pointercancel', () => { isDrawingBox = false; cancelBoxSelection(); });
  window.addEventListener('resize', () => { if (activeBox) positionFloatBar(); });
}

function submitBoxErase() {
  if (!activeBox || !currentJobId) return;
  const afterImg = document.getElementById('user-img-after');
  const overlay = document.getElementById('box-draw-overlay');
  if (!afterImg || !overlay) return;

  const r = overlay.getBoundingClientRect();
  if (r.width <= 0 || r.height <= 0) return;
  const naturalW = afterImg.naturalWidth || r.width;
  const naturalH = afterImg.naturalHeight || r.height;
  const scaleX = naturalW / r.width;
  const scaleY = naturalH / r.height;
  const imgX = Math.max(0, Math.round(activeBox.x * scaleX));
  const imgY = Math.max(0, Math.round(activeBox.y * scaleY));
  const imgW = Math.min(naturalW - imgX, Math.round(activeBox.w * scaleX));
  const imgH = Math.min(naturalH - imgY, Math.round(activeBox.h * scaleY));

  if (imgW < 4 || imgH < 4) {
    alert('Selected area is too small. Please drag a box over the watermark.');
    return;
  }

  const eraseBtn = document.getElementById('btn-box-erase');
  if (eraseBtn) {
    eraseBtn.disabled = true;
    eraseBtn.textContent = 'Erasing with AI...';
  }

  fetch('/api/reclean/' + currentJobId, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ box: [imgX, imgY, imgW, imgH] })
  })
  .then(res => res.json())
  .then(data => {
    if (eraseBtn) {
      eraseBtn.disabled = false;
      eraseBtn.textContent = '⚡ Erase with AI';
    }
    if (data.output_url) {
      const bustUrl = data.output_url + (data.output_url.indexOf('?') === -1 ? '?' : '&') + '_t=' + Date.now();
      const freshImg = new Image();
      freshImg.onload = () => {
        afterImg.src = bustUrl;
        setupSplitSlider('user-split-slider');
        cancelBoxSelection();
        setResultMode('slider');
      };
      freshImg.onerror = () => {
        afterImg.src = bustUrl;
        cancelBoxSelection();
        setResultMode('slider');
      };
      freshImg.src = bustUrl;
    } else if (data.job_id) {
      cancelBoxSelection();
      setResultMode('slider');
      resultEl.classList.remove('active');
      processingEl.classList.add('active');
      setStage('scanning');
      setProgress(5, 'Re-restoring video with selected area...');
      poll(data.job_id, currentJobFilename || 'video');
    } else if (data.error) {
      alert('Could not erase: ' + data.error);
    }
  })
  .catch(err => {
    if (eraseBtn) {
      eraseBtn.disabled = false;
      eraseBtn.textContent = '⚡ Erase with AI';
    }
    console.error('Erase error:', err);
    alert('Could not erase selected area. Please try again.');
  });
}

function setupSplitSlider(sliderContainerId) {
  const container = document.getElementById(sliderContainerId);
  if (!container) return;
  const range = container.querySelector('.split-range');
  const beforeLayer = container.querySelector('.split-before');
  const afterLayer = container.querySelector('.split-after');
  const handle = container.querySelector('.split-handle');
  if (!range || !afterLayer || !handle) return;

  function update() {
    if (sliderContainerId === 'user-split-slider' && currentResultMode !== 'slider') return;
    const val = parseFloat(range.value);
    if (beforeLayer) {
      beforeLayer.style.clipPath = `polygon(0 0, ${val}% 0, ${val}% 100%, 0 100%)`;
    }
    afterLayer.style.clipPath = `polygon(${val}% 0, 100% 0, 100% 100%, ${val}% 100%)`;
    handle.style.left = val + '%';
  }

  // Adjust container aspect ratio to match natural image dimensions for user-uploaded images
  if (sliderContainerId !== 'homepage-split-slider') {
    const img = container.querySelector('.split-before img');
    if (img) {
      const adjust = () => {
        if (img.naturalWidth && img.naturalHeight) {
          container.style.aspectRatio = `${img.naturalWidth} / ${img.naturalHeight}`;
        }
        update();
      };
      if (img.complete && img.naturalWidth) {
        adjust();
      } else {
        img.addEventListener('load', adjust, { once: true });
      }
    }
  }

  function setPosFromClientX(clientX) {
    const rect = container.getBoundingClientRect();
    if (!rect.width) return;
    let pct = ((clientX - rect.left) / rect.width) * 100;
    pct = Math.max(0, Math.min(100, pct));
    range.value = pct;
    update();
  }

  if (!container._hasSliderEvents) {
    container._hasSliderEvents = true;

    let isDragging = false;

    container.addEventListener('pointerdown', (e) => {
      if (sliderContainerId === 'user-split-slider' && currentResultMode !== 'slider') return;
      isDragging = true;
      try { container.setPointerCapture(e.pointerId); } catch(err) {}
      setPosFromClientX(e.clientX);
    });

    container.addEventListener('pointermove', (e) => {
      if (!isDragging) return;
      setPosFromClientX(e.clientX);
    });

    const stopDragging = (e) => {
      if (isDragging) {
        isDragging = false;
        try { container.releasePointerCapture(e.pointerId); } catch(err) {}
      }
    };

    container.addEventListener('pointerup', stopDragging);
    container.addEventListener('pointercancel', stopDragging);

    range.addEventListener('input', update);
    range.addEventListener('change', update);
  }

  update();
}

function setStage(stage) {
  const idx = stageOrder.indexOf(stage);
  ['queued','scanning','removing','finalizing'].forEach((key, keyIdx) => {
    const chip = document.getElementById('chip-' + key);
    if (chip) {
      chip.classList.toggle('done', keyIdx < idx);
      chip.classList.toggle('active', keyIdx === idx);
    }
  });
  const info = STAGES[stage];
  if (info) {
    stageTitle.textContent = info.title;
    if (!stageSub.getAttribute('data-custom')) {
      stageSub.textContent = info.sub;
    }
  }
}

function startJob(file) {
  dropzone.style.display = 'none';
  document.getElementById('tool-tabs').style.display = 'none';
  const zoneBar = document.getElementById('zone-pills-bar');
  if (zoneBar) zoneBar.style.display = 'none';
  processingEl.classList.add('active');
  errorBox.classList.remove('active');
  resultEl.classList.remove('active');
  setStage('queued');
  setProgress(0);

  if (scanFileLabel) {
    const fn = file.name || 'File';
    scanFileLabel.textContent = fn.length > 24 ? fn.slice(0, 22) + '...' : fn;
  }

  const bgPreview = document.getElementById('scan-bg-preview');
  if (bgPreview && file) {
    if (file.type && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        bgPreview.style.backgroundImage = `url(${e.target.result})`;
        bgPreview.classList.add('has-image');
      };
      reader.readAsDataURL(file);
    } else if (file.type && file.type.startsWith('video/')) {
      const v = document.createElement('video');
      v.preload = 'metadata';
      v.muted = true;
      v.playsInline = true;
      const vUrl = URL.createObjectURL(file);
      v.src = vUrl;
      v.onloadeddata = () => {
        v.currentTime = 0.1;
      };
      v.onseeked = () => {
        try {
          const c = document.createElement('canvas');
          c.width = v.videoWidth || 320;
          c.height = v.videoHeight || 240;
          const ctx = c.getContext('2d');
          ctx.drawImage(v, 0, 0, c.width, c.height);
          bgPreview.style.backgroundImage = `url(${c.toDataURL()})`;
          bgPreview.classList.add('has-image');
        } catch (err) {}
        URL.revokeObjectURL(vUrl);
      };
    }
  }

  initLottie();
  if (lottieAnim) {
    lottieAnim.play();
  }

  const fd = new FormData();
  fd.append('file', file);
  fd.append('corner', currentZone);

  fetch('/api/upload', { method: 'POST', body: fd })
    .then(r => r.json().then(j => ({ ok: r.ok, body: j })))
    .then(({ ok, body }) => {
      if (!ok) throw new Error(body.error || 'Upload failed.');
      poll(body.job_id, file.name);
    })
    .catch(err => showError(err.message));
}

let streamSource = null;

function cleanupStream() {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
  if (streamSource) {
    streamSource.close();
    streamSource = null;
  }
}

function handleJob(job, jobId, filename) {
  if (!job) return;
  if (job.stage) {
    setStage(job.stage);
  }
  if (job.percent !== null && job.percent !== undefined) {
    setProgress(job.percent, job.message);
  }
  if (job.stage === 'error') {
    cleanupStream();
    showError(job.error || 'Processing failed.');
    return;
  }
  if (job.stage === 'done') {
    cleanupStream();
    setProgress(100);
    setTimeout(() => {
      processingEl.classList.remove('active');
      resultEl.classList.add('active');
      currentDownloadUrl = '/api/download/' + jobId;
      currentDownloadFilename = 'removix_' + filename;
      currentJobId = jobId;
      currentJobFilename = filename;
      if (dlCheckbox) dlCheckbox.checked = false;
      if (dlLabel) dlLabel.classList.remove('is-checked');
      isDownloadComplete = false;

      // Live interactive split comparison for user upload
      const userWrap = document.getElementById('user-split-wrap');
      const modeBar = document.getElementById('result-mode-bar');
      const inUrl = job.input_url || ('/api/preview/' + jobId + '/input');
      const outUrl = job.output_url || ('/api/preview/' + jobId + '/output');
      if (userWrap) {
        const beforeImg = document.getElementById('user-img-before');
        const afterImg = document.getElementById('user-img-after');
        if (beforeImg && afterImg) {
          const cacheBust = '?t=' + Date.now();
          beforeImg.src = inUrl + cacheBust;
          afterImg.src = outUrl + cacheBust;
          afterImg.onerror = () => {
            setTimeout(() => { afterImg.src = outUrl + '?retry=1&t=' + Date.now(); }, 600);
          };
          const userRange = document.getElementById('user-range');
          if (userRange) userRange.value = 50;
          userWrap.style.display = 'block';
          if (modeBar) modeBar.style.display = 'flex';
          setResultMode('slider');
          setupSplitSlider('user-split-slider');
        }
      } else {
        if (userWrap) userWrap.style.display = 'none';
        if (modeBar) modeBar.style.display = 'none';
      }
    }, 450);
  }
}

function startPolling(jobId, filename) {
  if (pollTimer) clearInterval(pollTimer);
  const checkStatus = () => {
    fetch('/api/status/' + jobId)
      .then(r => r.json())
      .then(job => handleJob(job, jobId, filename))
      .catch(() => {});
  };
  checkStatus();
  pollTimer = setInterval(checkStatus, 200);
}

function poll(jobId, filename) {
  cleanupStream();
  startPolling(jobId, filename);
}

function showError(msg) {
  cleanupStream();
  processingEl.classList.remove('active');
  errorBox.textContent = msg;
  errorBox.classList.add('active');
  dropzone.style.display = '';
  document.getElementById('tool-tabs').style.display = 'flex';
}

function initApp() {
  initLottie();
  initBoxEraserEvents();
  setupSplitSlider('homepage-split-slider');
}

initApp();
document.addEventListener('DOMContentLoaded', initApp);

{{SIDEBAR_JS}}
</script>
</body>
</html>
"""

PAGE = (_RAW_PAGE
    .replace("{{SIDEBAR_CSS}}", SIDEBAR_CSS)
    .replace("{{SIDEBAR_HTML}}", SIDEBAR_HTML)
    .replace("{{TOP_BAR_HTML}}", TOP_BAR_HTML)
    .replace("{{SIDEBAR_JS}}", SIDEBAR_JS)
)
