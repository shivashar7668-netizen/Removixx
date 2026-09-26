"""
Removix UI - Base Layout Wrapper
--------------------------------
Shared HTML document wrapper with top bar, sidebar, glassmorphic card styles,
animations, footer, and theme variables.
"""

from ui.sidebar import SIDEBAR_CSS, render_top_bar_html, render_sidebar_html, SIDEBAR_JS

BASE_CSS = r"""
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
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

a { color: inherit; text-decoration: none; }

/* ---------- Brand Badge on Nav ---------- */
.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 0px;
  background: #ffffff;
  padding: 6px 18px 6px 14px;
  border-radius: 9999px;
  border: 1px solid rgba(226, 232, 240, 0.9);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
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
.brand-icon svg { width: 100%; height: 100%; display: block; }
.brand-name {
  font-size: 21.5px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--ink);
  line-height: 1;
}

/* ---------- Hero Section ---------- */
.hero {
  max-width: 920px;
  margin: 32px auto 0;
  text-align: center;
  padding: 0 24px;
  box-sizing: border-box;
}
.hero h1 {
  font-size: clamp(32px, 4.8vw, 54px);
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: var(--ink);
  margin-bottom: 14px;
}
.hero-sub {
  font-size: 16.5px;
  line-height: 1.6;
  color: var(--ink-muted);
  max-width: 720px;
  margin: 0 auto 32px;
}
.hero-sub strong { color: var(--ink); font-weight: 600; }

/* ---------- Main Tool Card ---------- */
.tool-container {
  max-width: 1140px;
  width: 100%;
  margin: 0 auto;
  padding: 0 32px;
  box-sizing: border-box;
  flex: 1;
}
.main-tool-card {
  background: var(--card-bg);
  border: 1px solid rgba(226, 232, 240, 0.9);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: 32px;
  position: relative;
  overflow: hidden;
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
  .hero {
    margin: 20px auto 0;
    padding: 0 16px;
  }
  .hero-sub {
    font-size: 14.5px;
    margin-bottom: 22px;
  }
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

/* ---------- 3D Floating Folder Dropzone (Removix Sky Blue Edition) ---------- */
#dropzone,
.dropzone-box,
[id^="dropzone"] {
  border: 2px dashed #0ea5e9;
  background: #f8fafc;
  border-radius: 20px;
  padding: 34px 24px 26px;
  text-align: center;
  cursor: pointer;
  display: block;
  transition: all 0.25s ease;
  user-select: none;
  -webkit-user-select: none;
  outline: none;
  position: relative;
}

#dropzone:hover,
#dropzone.hover,
#dropzone.dragover,
.dropzone-box:hover,
.dropzone-box.hover,
.dropzone-box.dragover,
[id^="dropzone"]:hover,
[id^="dropzone"].hover,
[id^="dropzone"].dragover {
  border-color: #0284c7;
  background: #f0f9ff;
  transform: scale(1.004);
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
.dropzone-box:hover .folder,
[id^="dropzone"]:hover .folder,
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
.dropzone-box:hover .back-side::before,
[id^="dropzone"]:hover .back-side::before,
.folder-container:hover .back-side::before {
  transform: rotateX(-5deg) skewX(5deg);
}

#dropzone:hover .back-side::after,
.dropzone-box:hover .back-side::after,
[id^="dropzone"]:hover .back-side::after,
.folder-container:hover .back-side::after {
  transform: rotateX(-15deg) skewX(12deg);
}

.folder .front-side {
  z-index: 1;
}

#dropzone:hover .front-side,
.dropzone-box:hover .front-side,
[id^="dropzone"]:hover .front-side,
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
.dropzone-box:hover .custom-file-upload,
[id^="dropzone"]:hover .custom-file-upload,
.folder-container:hover .custom-file-upload,
.custom-file-upload:hover {
  background: rgba(255, 255, 255, 0.4);
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-16px); }
  100% { transform: translateY(0px); }
}

.drop-primary {
  font-size: 18px;
  font-weight: 700;
  color: var(--ink);
  margin-top: 14px;
  margin-bottom: 6px;
}

.drop-secondary {
  font-size: 13.5px;
  color: var(--ink-muted);
}

input[type="file"] { display: none; }

/* Target Zone Pills */
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
  font-size: 12.5px;
  font-weight: 600;
  padding: 6px 16px;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
  outline: none;
}
.zone-pill.active {
  background: #0284c7;
  color: #ffffff;
  border-color: #0284c7;
  box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
}

/* Feature Boxes */
.section-features {
  max-width: 1140px;
  margin: 60px auto 0;
  padding: 0 32px;
  text-align: center;
  box-sizing: border-box;
}
.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}
@media (max-width: 1200px) {
  .section-features {
    padding: 0 28px;
  }
}
@media (max-width: 1024px) {
  .section-features {
    padding: 0 24px;
  }
}
@media (max-width: 768px) {
  .section-features {
    padding: 0 14px;
    margin: 36px auto 0;
  }
  .features-grid {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 480px) {
  .section-features {
    padding: 0 10px;
  }
}
.feature-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: var(--radius-md);
  padding: 24px;
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
  margin-bottom: 18px;
}
.feature-icon-pill {
  width: 42px;
  height: 42px;
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
  font-size: 16.5px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 8px;
}
.feature-box p {
  font-size: 13px;
  color: var(--ink-muted);
  line-height: 1.6;
}

/* Primary Action Buttons */
.btn-primary {
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
  color: #ffffff;
  border: none;
  font-size: 14.5px;
  font-weight: 700;
  padding: 12px 28px;
  border-radius: 9999px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 16px rgba(2, 132, 199, 0.35);
  transition: all 0.2s ease;
  outline: none;
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45);
}

.btn-secondary {
  background: #f1f5f9;
  color: #334155;
  border: 1px solid #e2e8f0;
  font-size: 13.5px;
  font-weight: 600;
  padding: 10px 22px;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-secondary:hover {
  background: #e2e8f0;
  color: #0f172a;
}

/* ---------- Animated Download & Reset Action Buttons (Uiverse) ---------- */
.result-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.result-actions .container {
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
  width: 165px;
  height: 57px;
  cursor: pointer;
  transition: all 0.4s ease;
  padding: 5px;
  position: relative;
  user-select: none;
  -webkit-user-select: none;
  box-sizing: border-box;
}

.label:hover {
  box-shadow: 0 8px 24px rgba(91, 91, 240, 0.35);
  transform: translateY(-1px);
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
  font-size: 15px;
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
  white-space: nowrap;
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
  width: 57px !important;
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
  font-size: 15px;
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
  text-decoration: none;
}
.btn-reset:hover {
  background: #f8fafc;
  border-color: #94a3b8;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  color: var(--ink);
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

/* Progress and Status Elements */
.progress-bar-wrap {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 9999px;
  overflow: hidden;
  margin: 18px 0;
}
.progress-bar-fill {
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, #38bdf8 0%, #0284c7 100%);
  border-radius: 9999px;
  transition: width 0.3s ease;
}

/* Checkerboard pattern for showing transparent cutouts */
.checkerboard-bg {
  background-color: #ffffff;
  background-image: linear-gradient(45deg, #f1f5f9 25%, transparent 25%),
                    linear-gradient(-45deg, #f1f5f9 25%, transparent 25%),
                    linear-gradient(45deg, transparent 75%, #f1f5f9 75%),
                    linear-gradient(-45deg, transparent 75%, #f1f5f9 75%);
  background-size: 20px 20px;
  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
}

/* ---------- Dynamic Processing View Component ---------- */
.processing {
  display: none;
  width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
}
.processing.active, .processing[style*="display: block"] {
  animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

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
  }
}

.lottie-scan-stage {
  position: relative;
  width: 90%;
  max-width: 380px;
  margin: 0 auto;
  box-sizing: border-box;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.7);
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
  width: 14px;
  height: 14px;
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

.radar-scan-svg {
  animation: radarSpin 4s linear infinite;
}
@keyframes radarSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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
@keyframes pulseDot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.8); }
}

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
  transition: all 0.25s ease;
}
.chip-indicator {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1.5px solid var(--line);
  background: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: var(--ink-faint);
  transition: all 0.25s ease;
  flex-shrink: 0;
}
.step-chip-row.active {
  color: var(--primary);
  font-weight: 700;
}
.step-chip-row.active .chip-indicator {
  border-color: var(--primary);
  background: var(--sky-soft);
  color: var(--primary);
  transform: scale(1.08);
}
.step-chip-row.done {
  color: var(--ink);
}
.step-chip-row.done .chip-indicator {
  border-color: #10b981;
  background: #10b981;
  color: #fff;
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

/* 5. Tool Config Cards, Trays, Confirmation Panels Across All Tools */
html.dark-mode [id$="-config-card"],
html.dark-mode [id$="-file-config"],
html.dark-mode [id*="config"],
html.dark-mode #images-tray,
html.dark-mode #collage-tray,
html.dark-mode .config-panel,
html.dark-mode .file-item-row,
body.dark-mode [id$="-config-card"],
body.dark-mode [id$="-file-config"],
body.dark-mode [id*="config"],
body.dark-mode #images-tray,
body.dark-mode #collage-tray,
body.dark-mode .config-panel,
body.dark-mode .file-item-row {
  background: #111827 !important;
  border-color: #1e293b !important;
  color: #f8fafc !important;
}

/* Model download banner */
html.dark-mode #model-download-card,
body.dark-mode #model-download-card {
  background: #111827 !important;
  border-color: #1e293b !important;
}
html.dark-mode #model-download-card span,
body.dark-mode #model-download-card span {
  color: #93c5fd !important;
}
html.dark-mode #model-download-card p,
body.dark-mode #model-download-card p {
  color: #60a5fa !important;
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
html.dark-mode #bg-result-card > div,
html.dark-mode .result-card,
html.dark-mode #pdf-result-card,
html.dark-mode .checkerboard-bg,
body.dark-mode #bg-result-card > div,
body.dark-mode .result-card,
body.dark-mode #pdf-result-card,
body.dark-mode .checkerboard-bg {
  background: #111827 !important;
  border-color: #1e293b !important;
}
html.dark-mode #pdf-result-card h3,
body.dark-mode #pdf-result-card h3 {
  color: #4ade80 !important;
}
html.dark-mode #pdf-result-card p,
body.dark-mode #pdf-result-card p {
  color: #86efac !important;
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

/* 11. Overriding Inline Styles In Tool Views */
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
"""

FOOTER_CSS = r"""
/* ---------- TinyWow-style Full-Width Footer ---------- */
.app-footer-wrap {
  width: 100%;
  max-width: 100%;
  margin: 56px 0 0 0;
  padding: 0;
  box-sizing: border-box;
  clear: both;
  position: relative;
}

.app-footer-card {
  width: 100%;
  max-width: 100%;
  background: transparent;
  border-top: 1px solid var(--line, #e2e8f0);
  border-left: none;
  border-right: none;
  border-bottom: none;
  border-radius: 0;
  box-shadow: none;
  padding: 48px 4px 28px;
  position: relative;
  box-sizing: border-box;
}

.footer-glow-bar {
  position: absolute;
  top: -1px;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #38bdf8 0%, #0284c7 45%, #0ea5e9 75%, #38bdf8 100%);
  border-radius: 3px;
}

.footer-main-grid {
  display: grid;
  grid-template-columns: 1.8fr repeat(4, 1fr);
  gap: clamp(24px, 3.2vw, 56px);
  align-items: start;
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 1200px) {
  .footer-main-grid {
    grid-template-columns: 1.5fr repeat(4, 1fr);
    gap: 24px;
  }
}

@media (max-width: 1024px) {
  .footer-main-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 28px;
  }
  .footer-brand-col {
    grid-column: span 4;
    max-width: 600px;
    margin-bottom: 6px;
  }
}

@media (max-width: 768px) {
  .app-footer-card {
    padding: 36px 0 22px;
  }
  .footer-main-grid {
    grid-template-columns: 1fr 1fr;
    gap: 28px 20px;
  }
  .footer-brand-col {
    grid-column: span 2;
    margin-bottom: 4px;
  }
  .footer-bottom-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }
}

@media (max-width: 480px) {
  .app-footer-card {
    padding: 28px 0 20px;
  }
  .footer-main-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  .footer-brand-col {
    grid-column: span 1;
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

.footer-brand-desc {
  font-size: 13.5px;
  color: var(--ink-muted, #475569);
  line-height: 1.6;
  margin: 0;
  max-width: 460px;
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

/* Footer Dark Mode */
html.dark-mode .app-footer-card,
body.dark-mode .app-footer-card {
  background: transparent !important;
  border-top-color: #1e293b !important;
  box-shadow: none !important;
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
"""

FOOTER_HTML = r"""
<footer class="app-footer-wrap">
  <div class="app-footer-card">
    <div class="footer-glow-bar"></div>

    <div class="footer-main-grid">
      <!-- 1. Left Column: Brand & Security Badges -->
      <div class="footer-brand-col">
        <a href="/" class="footer-brand-badge" style="text-decoration:none;">
          <div class="footer-brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <span class="footer-brand-title">Removix</span>
        </a>
        <p class="footer-brand-desc">
          Universal on-device AI media and document utility suite. Edit, convert, and enhance files with 100% privacy and zero cloud retention.
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

      <!-- 2. Column: Navigate -->
      <div class="footer-nav-col">
        <h4 class="footer-col-heading">Navigate</h4>
        <ul class="footer-links-list">
          <li><a href="/" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg> Home</a></li>
          <li><a href="/privacy-policy" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> Privacy Policy</a></li>
          <li><a href="/faq" class="footer-nav-link"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> FAQ</a></li>
          <li><a href="/contact" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg> Contact</a></li>
          <li><a href="/about" class="footer-nav-link"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg> About</a></li>
        </ul>
      </div>

      <!-- 3. Column: Image Tools -->
      <div class="footer-nav-col">
        <h4 class="footer-col-heading">Image Tools</h4>
        <ul class="footer-links-list">
          <li><a href="/bg-remove" class="footer-nav-link"><svg viewBox="0 0 24 24"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12"/></svg> Remove Background</a></li>
          <li><a href="/compress-image" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/></svg> Compress Image</a></li>
          <li><a href="/resize-image" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></svg> Resize Image</a></li>
          <li><a href="/crop-image" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/></svg> Crop Image</a></li>
          <li><a href="/image-tools" class="footer-nav-link" style="color:var(--primary); font-weight:700;"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg> All Image Tools &rarr;</a></li>
        </ul>
      </div>

      <!-- 4. Column: PDF Tools -->
      <div class="footer-nav-col">
        <h4 class="footer-col-heading">PDF Tools</h4>
        <ul class="footer-links-list">
          <li><a href="/pdf-to-image" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> PDF to Image</a></li>
          <li><a href="/image-to-pdf" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><polyline points="9 15 12 12 15 15"/></svg> Image to PDF</a></li>
          <li><a href="/merge-pdf" class="footer-nav-link"><svg viewBox="0 0 24 24"><rect x="8" y="2" width="13" height="15" rx="2"/><rect x="3" y="7" width="13" height="15" rx="2"/></svg> Merge PDF</a></li>
          <li><a href="/split-pdf" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><line x1="12" y1="11" x2="12" y2="17"/><line x1="9" y1="14" x2="15" y2="14"/></svg> Split PDF</a></li>
          <li><a href="/word-to-pdf" class="footer-nav-link"><svg viewBox="0 0 24 24"><rect x="3" y="2" width="18" height="20" rx="2"/><line x1="8" y1="8" x2="16" y2="8"/><line x1="8" y1="12" x2="16" y2="12"/></svg> Word to PDF</a></li>
          <li><a href="/pdf-tools" class="footer-nav-link" style="color:var(--primary); font-weight:700;"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M9 15h6M9 11h2M9 19h6"/></svg> All PDF Tools &rarr;</a></li>
        </ul>
      </div>

      <!-- 5. Column: Video & AI Tools -->
      <div class="footer-nav-col">
        <h4 class="footer-col-heading">Video &amp; AI Tools</h4>
        <ul class="footer-links-list">
          <li><a href="/video-watermark" class="footer-nav-link"><svg viewBox="0 0 24 24"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg> Video Watermark</a></li>
          <li><a href="/image-watermark" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> AI Eraser</a></li>
          <li><a href="/image-to-text" class="footer-nav-link"><svg viewBox="0 0 24 24"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg> Image to Text (OCR)</a></li>
          <li><a href="/upscale-image" class="footer-nav-link"><svg viewBox="0 0 24 24"><polyline points="17 11 12 6 7 11"/><polyline points="17 18 12 13 7 18"/></svg> Upscale Image</a></li>
          <li><a href="/qr-code" class="footer-nav-link"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg> QR Generator</a></li>
          <li><a href="/more-tools" class="footer-nav-link" style="color:var(--primary); font-weight:700;"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/></svg> More Tools Hub &rarr;</a></li>
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
        <span class="footer-copy-sub">Universal On-Device Engine</span>
      </div>

      <div class="footer-developer-card">
        <span class="footer-dev-label">Developed by</span>
        <a href="https://shivankthakur.com/" target="_blank" rel="noopener noreferrer" class="dev-link-modern" title="Visit Shivank Thakur Portfolio">
          <span>Shivank Thakur</span>
          <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>
"""

def render_processing_component(
    component_id: str,
    badge_text: str,
    badge_icon_svg: str,
    title_text: str,
    subtitle_text: str,
    steps: list,
) -> str:
    """Renders the standard Removix high-tech processing card component."""
    steps_html = ""
    for idx, step in enumerate(steps):
        active_cls = " active" if idx == 0 else ""
        steps_html += f"""
        <div class="step-chip-row{active_cls}" id="{component_id}-step-{idx + 1}">
          <div class="chip-indicator" id="{component_id}-ind-{idx + 1}">{idx + 1}</div>
          <span>{step}</span>
        </div>
        """

    return f"""
    <!-- Dedicated Dynamic Processing Component -->
    <div class="processing" id="{component_id}" style="display:none;">
      <div class="processing-layout">
        <!-- Left Stage: Scanner Track & Animation -->
        <div class="lottie-scan-stage">
          <div class="scan-bg-preview" id="{component_id}-bg-preview"></div>
          <div class="scan-bg-overlay"></div>
          <div class="scan-badge">
            {badge_icon_svg}
            {badge_text}
          </div>
          <div class="lottie-container" id="{component_id}-lottie">
            <svg class="radar-scan-svg" viewBox="0 0 100 100" style="width:85px; height:85px; stroke:#0284c7; fill:none;">
              <circle cx="50" cy="50" r="42" stroke-width="2" stroke-dasharray="6 4" opacity="0.35"/>
              <circle cx="50" cy="50" r="28" stroke-width="2.5" stroke="#38bdf8" opacity="0.6"/>
              <circle cx="50" cy="50" r="14" stroke-width="3" stroke="#0284c7"/>
              <circle cx="50" cy="50" r="5" fill="#0284c7"/>
            </svg>
          </div>
          <div class="stage-title" id="{component_id}-stage-title">{steps[0]}...</div>
          <p class="stage-sub" id="{component_id}-stage-sub">{subtitle_text}</p>
          <div class="scan-progress-box">
            <div class="scan-progress-header">
              <span id="{component_id}-progress-label">Conversion progress</span>
              <span class="scan-pct-value" id="{component_id}-pct">0%</span>
            </div>
            <div class="scan-progress-track">
              <div class="scan-progress-bar" id="{component_id}-bar"></div>
            </div>
          </div>
        </div>

        <!-- Right Side: Status Badge, Title & Step Chips -->
        <div class="processing-details">
          <div class="status-badge">
            <span class="status-dot"></span>
            PROCESSING
          </div>
          <h2 class="details-title" id="{component_id}-details-title">{title_text}</h2>
          <p class="details-sub" id="{component_id}-details-sub">{subtitle_text}</p>

          <div class="step-track">
            {steps_html}
          </div>
        </div>
      </div>
    </div>
    """

def render_layout(
    title: str,
    active_tool: str,
    hero_title: str,
    hero_sub: str,
    main_card_html: str,
    feature_cards_html: str = "",
    extra_css: str = "",
    extra_js: str = "",
) -> str:
    """Wraps any tool view into the full Removix web layout."""
    top_bar = render_top_bar_html()
    sidebar = render_sidebar_html(active_tool=active_tool)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
  (function() {{
    try {{
      var saved = localStorage.getItem('removix_theme');
      var isDark = saved === 'dark' || (!saved && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
      if (isDark) {{
        document.documentElement.classList.add('dark-mode');
        document.documentElement.setAttribute('data-theme', 'dark');
      }} else {{
        document.documentElement.classList.remove('dark-mode');
        document.documentElement.setAttribute('data-theme', 'light');
      }}
    }} catch(e) {{}}
  }})();
</script>
<style id="fouc-prevention-style">
  html.dark-mode {{ background-color: #0b0f19 !important; color: #f8fafc !important; }}
  html.dark-mode body {{ background-color: #0b0f19 !important; color: #f8fafc !important; }}
  [data-theme="dark"] {{ background-color: #0b0f19 !important; color: #f8fafc !important; }}
  [data-theme="dark"] body {{ background-color: #0b0f19 !important; color: #f8fafc !important; }}

  /* Critical Anti-Flash Rules for Cards and Grid Icons */
  html.dark-mode .image-tool-card,
  html.dark-mode .pdf-tool-card,
  html.dark-mode .popular-tool-card,
  html.dark-mode .more-tool-card,
  [data-theme="dark"] .image-tool-card,
  [data-theme="dark"] .pdf-tool-card,
  [data-theme="dark"] .popular-tool-card,
  [data-theme="dark"] .more-tool-card {{
    background: #1e293b !important;
    border-color: #334155 !important;
  }}
  html.dark-mode .image-tool-icon,
  html.dark-mode .pdf-tool-icon,
  html.dark-mode .tool-card-icon-box,
  html.dark-mode .more-tool-icon,
  [data-theme="dark"] .image-tool-icon,
  [data-theme="dark"] .pdf-tool-icon,
  [data-theme="dark"] .tool-card-icon-box,
  [data-theme="dark"] .more-tool-icon {{
    background: var(--icon-dark-bg, rgba(255, 255, 255, 0.08)) !important;
  }}
  html.dark-mode .image-tool-name,
  html.dark-mode .pdf-tool-name,
  html.dark-mode .tool-card-name,
  html.dark-mode .more-tool-name,
  [data-theme="dark"] .image-tool-name,
  [data-theme="dark"] .pdf-tool-name,
  [data-theme="dark"] .tool-card-name,
  [data-theme="dark"] .more-tool-name {{
    color: #f1f5f9 !important;
  }}
  html.dark-mode .image-tool-desc,
  html.dark-mode .pdf-tool-desc,
  html.dark-mode .tool-card-desc,
  html.dark-mode .more-tool-desc,
  [data-theme="dark"] .image-tool-desc,
  [data-theme="dark"] .pdf-tool-desc,
  [data-theme="dark"] .tool-card-desc,
  [data-theme="dark"] .more-tool-desc {{
    color: #94a3b8 !important;
  }}
  html.dark-mode .image-tool-arrow,
  html.dark-mode .pdf-tool-arrow,
  html.dark-mode .more-tool-arrow,
  [data-theme="dark"] .image-tool-arrow,
  [data-theme="dark"] .pdf-tool-arrow,
  [data-theme="dark"] .more-tool-arrow {{
    background: #0f172a !important;
    border-color: #334155 !important;
    color: #64748b !important;
  }}
</style>
<title>{title} — Removix</title>
<link rel="icon" type="image/png" href="/static/removix.png?v=3">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="/lottie.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script>
  if (window.pdfjsLib) {{
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }}
  if (!window.lottie) {{
    var s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js';
    document.head.appendChild(s);
  }}
</script>
<style>
{BASE_CSS}
{SIDEBAR_CSS}
{FOOTER_CSS}
{extra_css}
</style>
</head>
<body class="removix-body">
<script>
  (function() {{
    if (document.documentElement.classList.contains('dark-mode') || document.documentElement.getAttribute('data-theme') === 'dark') {{
      document.body.classList.add('dark-mode');
      document.body.setAttribute('data-theme', 'dark');
    }}
  }})();
</script>
{top_bar}

<div class="app-layout-shell">
  {sidebar}
  <div class="sidebar-backdrop" id="sidebarBackdrop" onclick="toggleSidebarMenu()"></div>

  <main class="app-main-content-area" id="mainContentArea">
    <section class="hero">
      <h1>{hero_title}</h1>
      <p class="hero-sub">{hero_sub}</p>
    </section>

    <section class="tool-container">
      <div class="main-tool-card">
        {main_card_html}
      </div>
    </section>

    {feature_cards_html}

    {FOOTER_HTML}
  </main>
</div>

<script>
{SIDEBAR_JS}
{extra_js}
</script>
</body>
</html>
"""
