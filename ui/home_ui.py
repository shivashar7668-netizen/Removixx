"""
Removix UI - Home Page View
---------------------------
Completely redesigned home page matching Image 1 and Image 2:
- Full-width hero banner with Welcome badge and 3D floating tool illustration
- Popular Tools horizontal scroll cards (8 tools)
- Recent Files real-time database-backed table
- Your Activity 2x2 statistics dashboard with real-time period selector (This Week, This Month, All Time)
"""

from ui.sidebar import SIDEBAR_CSS, render_top_bar_html, render_sidebar_html, SIDEBAR_JS
from ui.components.hero_illustration import render_hero_illustration, HERO_ILLUSTRATION_CSS
from ui.components.premium_laptop import render_premium_laptop_svg_node
from ui.layout import FOOTER_HTML, FOOTER_CSS

HOME_PAGE_CSS = r"""
/* ========== HOME PAGE STYLES ========== */
.home-layout-container {
  display: flex;
  flex-direction: column;
  gap: 28px;
  width: 100%;
}

/* 1. Hero Banner */
.home-banner-card {
  width: 100%;
  border-radius: var(--radius-xl);
  background: var(--banner-grad);
  border: 1px solid var(--line);
  padding: 36px 44px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px -4px rgba(2, 132, 199, 0.08);
}

.banner-left {
  flex: 1;
  max-width: 580px;
  z-index: 2;
}

.banner-welcome-pill {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 9999px;
  background: #ffffff;
  color: #0284c7;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 16px;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.10);
  border: 1px solid rgba(14, 165, 233, 0.2);
}

body.dark-mode .banner-welcome-pill {
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  border-color: rgba(56, 189, 248, 0.3);
}

.banner-heading {
  font-size: clamp(30px, 3.4vw, 44px);
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: var(--ink);
  margin-bottom: 12px;
}

.banner-heading-highlight {
  color: #0284c7;
  background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

body.dark-mode .banner-heading-highlight {
  background: linear-gradient(135deg, #38bdf8 0%, #60a5fa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.banner-subtext {
  font-size: 15px;
  line-height: 1.6;
  color: var(--ink-muted);
}

/* 2. Popular Tools Section */
.popular-tools-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.section-heading-group h2 {
  font-size: 21px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--ink);
  margin-bottom: 2px;
}

.section-heading-group p {
  font-size: 13.5px;
  color: var(--ink-muted);
}

.btn-view-all-link {
  font-size: 13.5px;
  font-weight: 700;
  color: #0284c7;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: gap 0.2s ease;
}

body.dark-mode .btn-view-all-link {
  color: #38bdf8;
}

.btn-view-all-link:hover {
  gap: 8px;
}

.popular-tools-row {
  display: grid;
  grid-template-columns: repeat(8, minmax(135px, 1fr));
  gap: 14px;
  overflow-x: auto;
  padding-bottom: 6px;
  scrollbar-width: thin;
}

@media (max-width: 1400px) {
  .popular-tools-row {
    grid-template-columns: repeat(4, 1fr);
  }
}
@media (max-width: 900px) {
  .popular-tools-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

.popular-tool-card {
  background: var(--card-bg);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  padding: 20px 16px 18px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-decoration: none;
  transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: var(--shadow-sm);
  min-height: 145px;
}

.popular-tool-card:hover {
  transform: translateY(-4px);
  border-color: #93c5fd;
  box-shadow: var(--shadow-md);
}

body.dark-mode .popular-tool-card:hover {
  border-color: #38bdf8;
}

.tool-card-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
  background: var(--icon-bg);
  transition: background-color 0.2s ease;
}

html.dark-mode .tool-card-icon-box,
body.dark-mode .tool-card-icon-box,
[data-theme="dark"] .tool-card-icon-box {
  background: var(--icon-dark-bg) !important;
}

.tool-card-icon-box svg {
  width: 22px;
  height: 22px;
}

.tool-card-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 4px;
  line-height: 1.3;
}

.tool-card-desc {
  font-size: 11.5px;
  color: var(--ink-muted);
  line-height: 1.4;
}

/* 3. Bottom Dashboard Section (Two Columns) */
.home-bottom-dashboard {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 24px;
}

@media (max-width: 1100px) {
  .home-bottom-dashboard {
    grid-template-columns: 1fr;
  }
}

/* Left Column: Recent Files */
.dashboard-card-panel {
  background: var(--card-bg);
  border: 1px solid var(--line);
  border-radius: var(--radius-xl);
  padding: 24px 26px;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
}

.panel-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.panel-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.panel-header-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: var(--primary-light);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.panel-header-icon svg {
  width: 20px;
  height: 20px;
}

.panel-title-text h3 {
  font-size: 17px;
  font-weight: 800;
  color: var(--ink);
  letter-spacing: -0.01em;
}

.panel-title-text p {
  font-size: 12px;
  color: var(--ink-muted);
}

/* Recent Files Table */
.recent-table-wrap {
  width: 100%;
  overflow-x: auto;
}

.recent-files-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.recent-files-table th {
  padding: 10px 12px;
  font-size: 11.5px;
  font-weight: 700;
  color: var(--ink-faint);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid var(--line);
}

.recent-files-table td {
  padding: 12px 12px;
  font-size: 13px;
  color: var(--ink-secondary);
  border-bottom: 1px solid var(--line-subtle);
  vertical-align: middle;
}

.recent-files-table tr:last-child td {
  border-bottom: none;
}

.recent-files-table tr:hover td {
  background: var(--line-subtle);
}

.file-cell-name {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: var(--ink);
}

.file-row-thumb {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
  background: var(--line-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-file-type {
  display: inline-block;
  padding: 3px 9px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 700;
}

.badge-type-image {
  background: #e0f2fe;
  color: #0284c7;
}

.badge-type-pdf {
  background: #fee2e2;
  color: #dc2626;
}

.badge-type-video {
  background: #f3e8ff;
  color: #9333ea;
}

body.dark-mode .badge-type-image {
  background: rgba(2, 132, 199, 0.25);
  color: #38bdf8;
}

body.dark-mode .badge-type-pdf {
  background: rgba(220, 38, 38, 0.25);
  color: #f87171;
}

body.dark-mode .badge-type-video {
  background: rgba(147, 51, 234, 0.25);
  color: #c084fc;
}

.table-action-btn {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--ink-muted);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.table-action-btn:hover {
  background: var(--line-subtle);
  color: var(--primary);
}

.empty-state-notice {
  padding: 36px 20px;
  text-align: center;
  color: var(--ink-muted);
  font-size: 13.5px;
}

/* Right Column: Your Activity */
.period-select-btn {
  padding: 6px 12px;
  border-radius: 9999px;
  background: var(--bg-page);
  border: 1px solid var(--line);
  color: var(--ink);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  outline: none;
  font-family: inherit;
}

.period-select-btn:hover {
  border-color: var(--primary);
}

.activity-stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.stat-item-box {
  background: var(--bg-page);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  padding: 16px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  position: relative;
}

.stat-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-icon-circle {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-circle svg {
  width: 17px;
  height: 17px;
}

.stat-label-text {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--ink-muted);
}

.stat-value-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-top: 4px;
}

.stat-number-big {
  font-size: 22px;
  font-weight: 800;
  color: var(--ink);
  letter-spacing: -0.02em;
}

.stat-change-pill {
  font-size: 10.5px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 9999px;
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.pill-change-up {
  background: var(--badge-green-bg);
  color: var(--badge-green-text);
}

.pill-change-down {
  background: #fee2e2;
  color: #dc2626;
}

.pill-change-neutral {
  background: var(--line);
  color: var(--ink-muted);
}

body.dark-mode .pill-change-neutral {
  background: rgba(255, 255, 255, 0.08);
  color: var(--ink-muted);
}

.empty-recent-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
  gap: 8px;
  text-align: center;
}

.empty-recent-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 1px dashed var(--line);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ink-muted);
  opacity: 0.7;
  margin-bottom: 2px;
}

.empty-recent-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--ink);
}

.empty-recent-subtitle {
  font-size: 12.5px;
  color: var(--ink-muted);
  max-width: 300px;
}

/* Storage Bar */
.storage-progress-bg {
  width: 100%;
  height: 6px;
  border-radius: 9999px;
  background: var(--line);
  overflow: hidden;
  margin-top: 8px;
}

.storage-progress-fill {
  height: 100%;
  border-radius: 9999px;
  background: #0284c7;
  transition: width 0.4s ease;
}

.storage-sub-info {
  font-size: 10.5px;
  color: var(--ink-faint);
  margin-top: 4px;
}
"""

PREMIUM_BANNER_CSS = r"""
/* ========== GET MORE WITH PREMIUM BANNER ========== */
.premium-banner-section {
  width: 100%;
  margin-top: 6px;
}

.premium-banner-card {
  width: 100%;
  border-radius: var(--radius-xl, 24px);
  background: linear-gradient(135deg, #0284c7 0%, #1e40af 52%, #172554 100%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  padding: 42px 48px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 36px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 16px 36px -10px rgba(30, 64, 175, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
}

body.dark-mode .premium-banner-card,
[data-theme="dark"] .premium-banner-card {
  background: linear-gradient(135deg, #0369a1 0%, #1e3a8a 55%, #0f172a 100%) !important;
  border-color: rgba(56, 189, 248, 0.25) !important;
  box-shadow: 0 18px 40px -10px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.08) inset !important;
}

.premium-ambient-glow {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(50px);
}

.glow-1 {
  top: -60px;
  right: -40px;
  width: 320px;
  height: 320px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.3) 0%, rgba(56, 189, 248, 0) 70%);
}

.glow-2 {
  bottom: -60px;
  left: 30%;
  width: 280px;
  height: 280px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(99, 102, 241, 0) 70%);
}

.premium-banner-left {
  flex: 1.1;
  max-width: 550px;
  z-index: 2;
  position: relative;
}

.premium-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 5px 14px;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.16);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.28);
  color: #ffffff;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}

.premium-banner-heading {
  font-size: clamp(28px, 3.2vw, 38px);
  font-weight: 800;
  line-height: 1.18;
  letter-spacing: -0.025em;
  color: #ffffff;
  margin-bottom: 14px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.18);
}

.premium-banner-desc {
  font-size: 15px;
  line-height: 1.65;
  color: rgba(241, 245, 249, 0.92);
  margin-bottom: 22px;
  max-width: 500px;
}

.premium-features-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  margin-bottom: 28px;
}

.premium-feature-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255, 255, 255, 0.24);
  padding: 7px 15px;
  border-radius: 9999px;
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.premium-feature-icon {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #38bdf8;
}

.premium-cta-wrap {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-premium-get-started {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: #ffffff;
  color: #1e40af;
  font-size: 15px;
  font-weight: 800;
  padding: 13px 32px;
  border-radius: 9999px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2), 0 2px 4px rgba(0, 0, 0, 0.08);
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.btn-premium-get-started:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.28);
  background: #f8fafc;
  color: #1d4ed8;
}

.btn-premium-get-started:active {
  transform: translateY(0);
}

.premium-banner-right {
  flex: 1;
  max-width: 480px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 2;
}

.premium-illustration-container {
  width: 100%;
  max-width: 480px;
  height: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.premium-illustration-svg {
  width: 100%;
  height: auto;
  overflow: visible;
  display: block;
}

/* Floating animation keyframes */
@keyframes floatBadgeA {
  0%, 100% { transform: translate(60px, 45px) rotate(-1deg); }
  50% { transform: translate(60px, 37px) rotate(1deg); }
}
@keyframes floatBadgeB {
  0%, 100% { transform: translate(180px, 15px) rotate(1deg); }
  50% { transform: translate(180px, 7px) rotate(-1deg); }
}
@keyframes floatBadgeC {
  0%, 100% { transform: translate(305px, 35px) rotate(-1.5deg); }
  50% { transform: translate(305px, 28px) rotate(0.5deg); }
}
@keyframes floatBadgeD {
  0%, 100% { transform: translate(415px, 80px) rotate(1.5deg); }
  50% { transform: translate(415px, 72px) rotate(-1deg); }
}

.float-badge-1 { animation: floatBadgeA 4.8s ease-in-out infinite; }
.float-badge-2 { animation: floatBadgeB 5.4s ease-in-out infinite 0.4s; }
.float-badge-3 { animation: floatBadgeC 4.6s ease-in-out infinite 0.8s; }
.float-badge-4 { animation: floatBadgeD 5.2s ease-in-out infinite 1.2s; }

@media (max-width: 1000px) {
  .premium-banner-card {
    flex-direction: column;
    padding: 34px 28px;
    text-align: center;
    gap: 28px;
  }
  .premium-banner-left {
    max-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .premium-banner-desc {
    margin-left: auto;
    margin-right: auto;
  }
  .premium-features-row {
    justify-content: center;
  }
  .premium-banner-right {
    max-width: 380px;
  }
}

@media (max-width: 540px) {
  .premium-banner-card {
    padding: 26px 18px;
    border-radius: 18px;
  }
  .premium-features-row {
    flex-direction: column;
    width: 100%;
    gap: 8px;
  }
  .premium-feature-pill {
    width: 100%;
    justify-content: center;
  }
  .btn-premium-get-started {
    width: 100%;
  }
  .premium-banner-right {
    max-width: 300px;
  }
}
"""

HOME_PAGE_CSS = HOME_PAGE_CSS + "\n" + HERO_ILLUSTRATION_CSS + "\n" + FOOTER_CSS + "\n" + PREMIUM_BANNER_CSS

HOME_PAGE_JS = r"""
// ==================== REAL-TIME ACTIVITY & DASHBOARD LOGIC ====================
let currentPeriod = 'month';

function getFileIconSvg(type) {
  if (type === 'PDF') {
    return `<div class="file-row-thumb" style="color:#dc2626; background:#fee2e2;">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/></svg>
    </div>`;
  } else if (type === 'Video') {
    return `<div class="file-row-thumb" style="color:#9333ea; background:#f3e8ff;">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
    </div>`;
  } else {
    return `<div class="file-row-thumb" style="color:#0284c7; background:#e0f2fe;">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/></svg>
    </div>`;
  }
}

function fetchRecentFiles() {
  fetch('/api/activity/recent')
    .then(r => r.json())
    .then(data => {
      const tbody = document.getElementById('recentFilesTableBody');
      if (!tbody) return;
      if (!data || data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="empty-state-notice" style="padding:0; border:none;">
          <div class="empty-recent-wrapper">
            <div class="empty-recent-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><polyline points="9 15 12 12 15 15"/></svg>
            </div>
            <div class="empty-recent-title">No recent activity yet</div>
            <div class="empty-recent-subtitle">Process an image, PDF, or video using any tool to see your history here.</div>
          </div>
        </td></tr>`;
        return;
      }
      tbody.innerHTML = data.map(item => {
        const typeClass = item.type === 'PDF' ? 'badge-type-pdf' : (item.type === 'Video' ? 'badge-type-video' : 'badge-type-image');
        return `
          <tr>
            <td>
              <div class="file-cell-name">
                ${getFileIconSvg(item.type)}
                <span>${item.name}</span>
              </div>
            </td>
            <td><span class="badge-file-type ${typeClass}">${item.type}</span></td>
            <td>${item.size}</td>
            <td>${item.date}</td>
            <td style="text-align:right;">
              <button class="table-action-btn" title="Download" onclick="downloadRecentFile(${item.id}, '${item.name}')">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              </button>
              <button class="table-action-btn" title="Delete record" onclick="deleteRecentRecord(${item.id})">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg>
              </button>
            </td>
          </tr>
        `;
      }).join('');
    })
    .catch(() => {});
}

function fetchActivityStats(period) {
  fetch('/api/activity/stats?period=' + (period || currentPeriod))
    .then(r => r.json())
    .then(stats => {
      if (!stats) return;
      const statFiles = document.getElementById('statFilesProcessed');
      if (statFiles) statFiles.textContent = stats.files_processed || 0;
      const fChange = document.getElementById('statFilesChange');
      if (fChange) {
        if (stats.files_change > 0) {
          fChange.textContent = '↑ ' + stats.files_change + '%';
          fChange.className = 'stat-change-pill pill-change-up';
        } else if (stats.files_change < 0) {
          fChange.textContent = '↓ ' + Math.abs(stats.files_change) + '%';
          fChange.className = 'stat-change-pill pill-change-down';
        } else {
          fChange.textContent = '0%';
          fChange.className = 'stat-change-pill pill-change-neutral';
        }
      }

      const statStorage = document.getElementById('statStorageUsed');
      if (statStorage) statStorage.textContent = (stats.storage_used_mb || 0) + ' MB';
      const statBar = document.getElementById('statStorageBar');
      if (statBar) statBar.style.width = (stats.storage_pct || 0) + '%';
      const statSub = document.getElementById('statStorageSub');
      if (statSub) statSub.textContent = (stats.storage_pct || 0) + '% of ' + (stats.storage_quota_mb || 500) + ' MB';

      const statImgs = document.getElementById('statImagesProcessed');
      if (statImgs) statImgs.textContent = stats.images_processed || 0;
      const iChange = document.getElementById('statImagesChange');
      if (iChange) {
        if (stats.images_change > 0) {
          iChange.textContent = '↑ ' + stats.images_change + '%';
          iChange.className = 'stat-change-pill pill-change-up';
        } else if (stats.images_change < 0) {
          iChange.textContent = '↓ ' + Math.abs(stats.images_change) + '%';
          iChange.className = 'stat-change-pill pill-change-down';
        } else {
          iChange.textContent = '0%';
          iChange.className = 'stat-change-pill pill-change-neutral';
        }
      }

      const statPdfs = document.getElementById('statPdfFiles');
      if (statPdfs) statPdfs.textContent = stats.pdf_files || 0;
      const pChange = document.getElementById('statPdfChange');
      if (pChange) {
        if (stats.pdf_change > 0) {
          pChange.textContent = '↑ ' + stats.pdf_change + '%';
          pChange.className = 'stat-change-pill pill-change-up';
        } else if (stats.pdf_change < 0) {
          pChange.textContent = '↓ ' + Math.abs(stats.pdf_change) + '%';
          pChange.className = 'stat-change-pill pill-change-down';
        } else {
          pChange.textContent = '0%';
          pChange.className = 'stat-change-pill pill-change-neutral';
        }
      }
    })
    .catch(() => {});
}

function changeActivityPeriod(val) {
  currentPeriod = val;
  fetchActivityStats(val);
}

function refreshRecentFilesList() {
  fetchRecentFiles();
  fetchActivityStats(currentPeriod);
  showRemovixToast('Activity synced with local database.');
}

function downloadRecentFile(fileId, fileName) {
  window.location.href = '/api/activity/download/' + fileId;
}

function deleteRecentRecord(fileId) {
  if (!confirm('Remove this file entry from your history?')) return;
  fetch('/api/activity/delete/' + fileId, { method: 'DELETE' })
    .then(r => r.json())
    .then(() => {
      fetchRecentFiles();
      fetchActivityStats(currentPeriod);
      showRemovixToast('Entry removed from history.');
    });
}

// Initial fetch and 30-second background polling
document.addEventListener('DOMContentLoaded', () => {
  fetchRecentFiles();
  fetchActivityStats(currentPeriod);
  setInterval(() => {
    fetchRecentFiles();
    fetchActivityStats(currentPeriod);
  }, 30000);
});
if (document.readyState !== 'loading') {
  fetchRecentFiles();
  fetchActivityStats(currentPeriod);
}
"""

def render_premium_banner_html() -> str:
    """Renders the Premium banner section with animated laptop SVG illustration."""
    laptop_node = render_premium_laptop_svg_node()
    return f"""
      <!-- 4. Get more with Premium Banner Section -->
      <section class="premium-banner-section">
        <div class="premium-banner-card">
          <!-- Ambient lighting effects -->
          <div class="premium-ambient-glow glow-1"></div>
          <div class="premium-ambient-glow glow-2"></div>

          <!-- Left Column: Value Proposition & Features -->
          <div class="premium-banner-left">
            <div class="premium-badge-pill">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              <span>Get more with Premium</span>
            </div>
            <h2 class="premium-banner-heading">Get more with Premium</h2>
            <p class="premium-banner-desc">
              Take your projects further with premium tools and advanced features. Edit, convert, and enhance high-resolution files with zero waiting and full priority access.
            </p>

            <!-- 3 Benefit points with icons -->
            <div class="premium-features-row">
              <div class="premium-feature-pill">
                <div class="premium-feature-icon">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M4.93 4.93l14.14 14.14"/></svg>
                </div>
                <span>Ad-free</span>
              </div>
              <div class="premium-feature-pill">
                <div class="premium-feature-icon">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                </div>
                <span>Unlimited usage</span>
              </div>
              <div class="premium-feature-pill">
                <div class="premium-feature-icon">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <span>Faster processing</span>
              </div>
            </div>

            <!-- Get Started Button (Non-functional as requested) -->
            <div class="premium-cta-wrap">
              <a href="javascript:void(0)" class="btn-premium-get-started" onclick="event.preventDefault()">
                <span>Get started</span>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </a>
            </div>
          </div>

          <!-- Right Column: Screen / Laptop Illustration with Floating Tool Icons -->
          <div class="premium-banner-right">
            <div class="premium-illustration-container">
              <svg class="premium-illustration-svg" viewBox="0 0 520 380" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <linearGradient id="premImgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#38bdf8" />
                    <stop offset="100%" stop-color="#0284c7" />
                  </linearGradient>
                  <linearGradient id="premPdfGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#f87171" />
                    <stop offset="100%" stop-color="#dc2626" />
                  </linearGradient>
                  <linearGradient id="premVidGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#c084fc" />
                    <stop offset="100%" stop-color="#7c3aed" />
                  </linearGradient>
                  <linearGradient id="premOcrGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#34d399" />
                    <stop offset="100%" stop-color="#059669" />
                  </linearGradient>
                  <linearGradient id="premSwooshGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.2" />
                    <stop offset="50%" stop-color="#60a5fa" stop-opacity="0.8" />
                    <stop offset="100%" stop-color="#93c5fd" stop-opacity="0.3" />
                  </linearGradient>
                  <filter id="premDropShadow" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#020617" flood-opacity="0.35" />
                  </filter>
                  <filter id="premGlow" x="-30%" y="-30%" width="160%" height="160%">
                    <feGaussianBlur stdDeviation="8" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                  </filter>
                </defs>

                <!-- Ambient Glow Behind Laptop -->
                <circle cx="270" cy="220" r="160" fill="url(#premImgGrad)" opacity="0.18" filter="url(#premGlow)" />

                <!-- Curved Energy Trajectory Swoosh -->
                <path d="M 120 270 Q 230 180 320 80 Q 380 40 460 70" stroke="url(#premSwooshGrad)" stroke-width="4" stroke-linecap="round" fill="none" />
                <circle cx="210" cy="215" r="4" fill="#67e8f9" filter="url(#premGlow)" />
                <circle cx="280" cy="140" r="5" fill="#93c5fd" filter="url(#premGlow)" />
                <circle cx="370" cy="70" r="4" fill="#a7f3d0" filter="url(#premGlow)" />

                <!-- Animated Laptop SVG Illustration Component -->
                {laptop_node}

                <!-- 1. Floating Card: Image (Top-Left) -->
                <g class="float-badge-1" transform="translate(60, 45)" filter="url(#premDropShadow)">
                  <rect width="84" height="84" rx="20" fill="url(#premImgGrad)" />
                  <rect x="1" y="1" width="82" height="82" rx="19" stroke="#ffffff" stroke-opacity="0.3" stroke-width="1.5" fill="none" />
                  <g transform="translate(24, 20)">
                    <rect x="0" y="0" width="36" height="28" rx="5" stroke="#ffffff" stroke-width="2.4" fill="none" />
                    <circle cx="10" cy="9" r="3" fill="#ffffff" />
                    <path d="M 3 24 L 14 13 L 23 21 L 28 17 L 33 24" stroke="#ffffff" stroke-width="2.4" stroke-linejoin="round" fill="none" />
                  </g>
                  <text x="42" y="68" text-anchor="middle" font-size="11" font-weight="800" fill="#ffffff" font-family="'Plus Jakarta Sans',sans-serif" letter-spacing="0.5">IMAGE</text>
                </g>

                <!-- 2. Floating Card: PDF (Top-Center) -->
                <g class="float-badge-2" transform="translate(180, 15)" filter="url(#premDropShadow)">
                  <rect width="88" height="88" rx="20" fill="url(#premPdfGrad)" />
                  <rect x="1" y="1" width="86" height="86" rx="19" stroke="#ffffff" stroke-opacity="0.35" stroke-width="1.5" fill="none" />
                  <g transform="translate(27, 18)">
                    <path d="M 6 0 L 22 0 L 32 10 L 32 30 C 32 32 30 34 28 34 L 6 34 C 4 34 2 32 2 30 L 2 4 C 2 2 4 0 6 0 Z" stroke="#ffffff" stroke-width="2.4" fill="none" stroke-linejoin="round" />
                    <polyline points="22,0 22,10 32,10" stroke="#ffffff" stroke-width="2.4" fill="none" />
                    <line x1="8" y1="20" x2="26" y2="20" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
                    <line x1="8" y1="26" x2="20" y2="26" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
                  </g>
                  <text x="44" y="72" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff" font-family="'Plus Jakarta Sans',sans-serif" letter-spacing="0.5">PDF</text>
                </g>

                <!-- 3. Floating Card: Video (Top-Right) -->
                <g class="float-badge-3" transform="translate(305, 35)" filter="url(#premDropShadow)">
                  <rect width="84" height="84" rx="20" fill="url(#premVidGrad)" />
                  <rect x="1" y="1" width="82" height="82" rx="19" stroke="#ffffff" stroke-opacity="0.3" stroke-width="1.5" fill="none" />
                  <g transform="translate(24, 18)">
                    <rect x="0" y="2" width="24" height="26" rx="4" stroke="#ffffff" stroke-width="2.4" fill="none" />
                    <polygon points="24,10 36,4 36,26 24,20" stroke="#ffffff" stroke-width="2.4" stroke-linejoin="round" fill="none" />
                    <polygon points="9,10 17,15 9,20" fill="#ffffff" />
                  </g>
                  <text x="42" y="68" text-anchor="middle" font-size="11" font-weight="800" fill="#ffffff" font-family="'Plus Jakarta Sans',sans-serif" letter-spacing="0.5">VIDEO</text>
                </g>

                <!-- 4. Floating Card: AI / OCR Sparkles (Far-Right) -->
                <g class="float-badge-4" transform="translate(415, 80)" filter="url(#premDropShadow)">
                  <rect width="82" height="82" rx="20" fill="url(#premOcrGrad)" />
                  <rect x="1" y="1" width="80" height="80" rx="19" stroke="#ffffff" stroke-opacity="0.3" stroke-width="1.5" fill="none" />
                  <g transform="translate(24, 16)">
                    <path d="M 16 0 Q 16 14 30 14 Q 16 14 16 28 Q 16 14 2 14 Q 16 14 16 0 Z" fill="#ffffff" />
                    <path d="M 27 22 Q 27 26 33 26 Q 27 26 27 30 Q 27 26 23 26 Q 27 26 27 22 Z" fill="#ffffff" opacity="0.85" />
                  </g>
                  <text x="41" y="66" text-anchor="middle" font-size="11" font-weight="800" fill="#ffffff" font-family="'Plus Jakarta Sans',sans-serif" letter-spacing="0.5">AI / OCR</text>
                </g>
              </svg>
            </div>
          </div>
        </div>
      </section>
"""

PREMIUM_BANNER_HTML = render_premium_banner_html()

def render_home_page() -> str:
    """Renders the complete Removix Home Page View."""
    top_bar = render_top_bar_html()
    sidebar = render_sidebar_html(active_tool="home")

    # Render Hero Animated SVG Illustration Component
    hero_illustration = render_hero_illustration()
    hero_illustration_html = hero_illustration["html"]

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

  /* Critical Anti-Flash Rules */
  html.dark-mode .popular-tool-card,
  [data-theme="dark"] .popular-tool-card {{
    background: #162032 !important;
    border-color: #1e293b !important;
  }}
  html.dark-mode .tool-card-icon-box,
  [data-theme="dark"] .tool-card-icon-box {{
    background: var(--icon-dark-bg, rgba(255, 255, 255, 0.08)) !important;
  }}
</style>
<title>Removix — Edit, Convert & Enhance Your Files</title>
<link rel="icon" type="image/png" href="/static/removix.png?v=4">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  background: var(--bg-page);
  color: var(--ink);
  font-family: 'Plus Jakarta Sans', sans-serif;
  overflow-x: hidden;
  transition: background-color 0.25s ease, color 0.25s ease;
}}
{SIDEBAR_CSS}
{HOME_PAGE_CSS}
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

  <main class="app-main-content-area">
    <div class="home-layout-container">

      <!-- 1. Full-width Hero Banner -->
      <section class="home-banner-card">
        <div class="banner-left">
          <span class="banner-welcome-pill">WELCOME TO REMOVIX</span>
          <h1 class="banner-heading">
            Edit, Convert &amp; Enhance<br>
            Your Files <span class="banner-heading-highlight">in Seconds</span>
          </h1>
          <p class="banner-subtext">Powerful and easy-to-use tools for images, PDFs, videos and more.</p>
        </div>

        {hero_illustration_html}
      </section>

      <!-- 2. Popular Tools Section -->
      <section class="popular-tools-section">
        <div class="section-title-row">
          <div class="section-heading-group">
            <h2>Popular Tools</h2>
            <p>Most used tools, ready for you.</p>
          </div>
          <a href="/image-tools" class="btn-view-all-link">View All Tools &rarr;</a>
        </div>

        <div class="popular-tools-row">
          <!-- 1. Remove Background -->
          <a href="/bg-remove" class="popular-tool-card">
            <div class="tool-card-icon-box" style="--icon-bg:#e0f2fe; --icon-dark-bg:rgba(2, 132, 199, 0.18); color:#0284c7;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12"/></svg>
            </div>
            <h4 class="tool-card-name">Remove Background</h4>
            <p class="tool-card-desc">Remove image backgrounds instantly.</p>
          </a>

          <!-- 2. Compress Image -->
          <a href="/compress-image" class="popular-tool-card">
            <div class="tool-card-icon-box" style="--icon-bg:#f3e8ff; --icon-dark-bg:rgba(147, 51, 234, 0.18); color:#9333ea;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
            </div>
            <h4 class="tool-card-name">Compress Image</h4>
            <p class="tool-card-desc">Reduce file size without losing quality.</p>
          </a>

          <!-- 3. Resize Image -->
          <a href="/resize-image" class="popular-tool-card">
            <div class="tool-card-icon-box" style="--icon-bg:#dcfce7; --icon-dark-bg:rgba(22, 163, 74, 0.18); color:#16a34a;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></svg>
            </div>
            <h4 class="tool-card-name">Resize Image</h4>
            <p class="tool-card-desc">Resize images to any dimension quickly.</p>
          </a>

          <!-- 4. PDF to Image -->
          <a href="/pdf-to-image" class="popular-tool-card">
            <div class="tool-card-icon-box" style="--icon-bg:#fee2e2; --icon-dark-bg:rgba(220, 38, 38, 0.18); color:#dc2626;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            </div>
            <h4 class="tool-card-name">PDF to Image</h4>
            <p class="tool-card-desc">Convert PDF pages to high-quality images.</p>
          </a>

          <!-- 5. Merge PDF -->
          <a href="/merge-pdf" class="popular-tool-card">
            <div class="tool-card-icon-box" style="--icon-bg:#ffedd5; --icon-dark-bg:rgba(234, 88, 12, 0.18); color:#ea580c;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="8" y="2" width="13" height="15" rx="2"/><rect x="3" y="7" width="13" height="15" rx="2"/></svg>
            </div>
            <h4 class="tool-card-name">Merge PDF</h4>
            <p class="tool-card-desc">Combine multiple PDF files into one.</p>
          </a>

          <!-- 6. Video Compressor -->
          <a href="/video-watermark" class="popular-tool-card">
            <div class="tool-card-icon-box" style="--icon-bg:#ede9fe; --icon-dark-bg:rgba(124, 58, 237, 0.18); color:#7c3aed;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
            </div>
            <h4 class="tool-card-name">Video Compressor</h4>
            <p class="tool-card-desc">Compress video files without quality loss.</p>
          </a>

          <!-- 7. AI Eraser -->
          <a href="/image-watermark" class="popular-tool-card">
            <div class="tool-card-icon-box" style="--icon-bg:#ccfbf1; --icon-dark-bg:rgba(13, 148, 136, 0.18); color:#0d9488;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            </div>
            <h4 class="tool-card-name">AI Eraser</h4>
            <p class="tool-card-desc">Remove unwanted objects with AI.</p>
          </a>

          <!-- 8. Image to PDF -->
          <a href="/image-to-pdf" class="popular-tool-card">
            <div class="tool-card-icon-box" style="--icon-bg:#e0f2fe; --icon-dark-bg:rgba(2, 132, 199, 0.18); color:#0284c7;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><polyline points="9 15 12 12 15 15"/></svg>
            </div>
            <h4 class="tool-card-name">Image to PDF</h4>
            <p class="tool-card-desc">Convert multiple images into a single PDF.</p>
          </a>
        </div>
      </section>

      <!-- 3. Bottom Dashboard (Two Columns) -->
      <section class="home-bottom-dashboard">

        <!-- Left Column: Recent Files -->
        <div class="dashboard-card-panel" id="recent-files">
          <div class="panel-header-row">
            <div class="panel-header-left">
              <div class="panel-header-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              </div>
              <div class="panel-title-text">
                <h3>Recent Files</h3>
                <p>Your recently processed files.</p>
              </div>
            </div>
            <a href="javascript:void(0)" class="btn-view-all-link" onclick="refreshRecentFilesList()">Refresh &circlearrowright;</a>
          </div>

          <div class="recent-table-wrap">
            <table class="recent-files-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Size</th>
                  <th>Date</th>
                  <th style="text-align:right;">Actions</th>
                </tr>
              </thead>
              <tbody id="recentFilesTableBody">
                <tr><td colspan="5" class="empty-state-notice" style="padding:0; border:none;">
                  <div class="empty-recent-wrapper">
                    <div class="empty-recent-icon">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><polyline points="9 15 12 12 15 15"/></svg>
                    </div>
                    <div class="empty-recent-title">No recent activity yet</div>
                    <div class="empty-recent-subtitle">Process an image, PDF, or video using any tool to see your history here.</div>
                  </div>
                </td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Right Column: Your Activity -->
        <div class="dashboard-card-panel">
          <div class="panel-header-row">
            <div class="panel-header-left">
              <div class="panel-header-icon" style="background:#e0f2fe; color:#0284c7;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
              </div>
              <div class="panel-title-text">
                <h3>Your Activity</h3>
                <p>Track your usage and storage.</p>
              </div>
            </div>

            <!-- Period Select Dropdown -->
            <select id="activityPeriodSelect" class="period-select-btn" onchange="changeActivityPeriod(this.value)">
              <option value="month" selected>This Month</option>
              <option value="week">This Week</option>
              <option value="all">All Time</option>
            </select>
          </div>

          <div class="activity-stats-grid">
            <!-- 1. Files Processed -->
            <div class="stat-item-box">
              <div class="stat-top-row">
                <span class="stat-label-text">Files Processed</span>
                <div class="stat-icon-circle" style="background:#e0f2fe; color:#0284c7;">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                </div>
              </div>
              <div class="stat-value-row">
                <span class="stat-number-big" id="statFilesProcessed">0</span>
                <span class="stat-change-pill pill-change-neutral" id="statFilesChange">0%</span>
              </div>
            </div>

            <!-- 2. Storage Used -->
            <div class="stat-item-box">
              <div class="stat-top-row">
                <span class="stat-label-text">Storage Used</span>
                <div class="stat-icon-circle" style="background:#e0f2fe; color:#0284c7;">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
                </div>
              </div>
              <div class="stat-value-row">
                <span class="stat-number-big" id="statStorageUsed">0 MB</span>
              </div>
              <div class="storage-progress-bg">
                <div class="storage-progress-fill" id="statStorageBar" style="width: 0%;"></div>
              </div>
              <p class="storage-sub-info" id="statStorageSub">0% of 500 MB</p>
            </div>

            <!-- 3. Images Processed -->
            <div class="stat-item-box">
              <div class="stat-top-row">
                <span class="stat-label-text">Images Processed</span>
                <div class="stat-icon-circle" style="background:#f3e8ff; color:#9333ea;">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                </div>
              </div>
              <div class="stat-value-row">
                <span class="stat-number-big" id="statImagesProcessed">0</span>
                <span class="stat-change-pill pill-change-neutral" id="statImagesChange">0%</span>
              </div>
            </div>

            <!-- 4. PDF Files -->
            <div class="stat-item-box">
              <div class="stat-top-row">
                <span class="stat-label-text">PDF Files</span>
                <div class="stat-icon-circle" style="background:#fee2e2; color:#dc2626;">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                </div>
              </div>
              <div class="stat-value-row">
                <span class="stat-number-big" id="statPdfFiles">0</span>
                <span class="stat-change-pill pill-change-neutral" id="statPdfChange">0%</span>
              </div>
            </div>
          </div>
        </div>

      </section>

      {PREMIUM_BANNER_HTML}

      {FOOTER_HTML}

    </div>
  </main>
</div>

<script>
{SIDEBAR_JS}
{HOME_PAGE_JS}
</script>
</body>
</html>
"""
