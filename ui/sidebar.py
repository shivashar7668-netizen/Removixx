"""
Removix UI - Top Bar & Sidebar Navigation
-----------------------------------------
Shared top navigation bar, collapsible left sidebar, dark/light mode toggle,
search with Ctrl+K, Google login modal, and Upgrade to Pro card.
"""

SIDEBAR_CSS = r"""
/* ========== THEME VARIABLES ========== */
:root {
  --primary: #0284c7;
  --primary-hover: #0369a1;
  --primary-light: #e0f2fe;
  --sky: #0ea5e9;
  --sky-soft: #f0f9ff;
  --bg-page: #f8fafc;
  --card-bg: #ffffff;
  --sidebar-bg: #ffffff;
  --topbar-bg: #ffffff;
  --ink: #0f172a;
  --ink-secondary: #334155;
  --ink-muted: #64748b;
  --ink-faint: #94a3b8;
  --line: #e2e8f0;
  --line-subtle: #f1f5f9;
  --radius-xl: 24px;
  --radius-lg: 18px;
  --radius-md: 14px;
  --radius-sm: 10px;
  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05);
  --shadow-md: 0 4px 14px -2px rgba(15, 23, 42, 0.07);
  --shadow-lg: 0 16px 36px -8px rgba(15, 23, 42, 0.09);
  --banner-grad: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 55%, #e0f2fe 100%);
  --badge-green-bg: #dcfce7;
  --badge-green-text: #16a34a;
}

html.dark-mode,
body.dark-mode,
html.dark-mode body {
  --primary: #38bdf8;
  --primary-hover: #0ea5e9;
  --primary-light: rgba(56, 189, 248, 0.16);
  --sky-soft: #162032;
  --bg-page: #0b0f19;
  --card-bg: #162032;
  --sidebar-bg: #111827;
  --topbar-bg: #111827;
  --ink: #f8fafc;
  --ink-secondary: #e2e8f0;
  --ink-muted: #94a3b8;
  --ink-faint: #64748b;
  --line: #1e293b;
  --line-subtle: #1e293b;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 14px -2px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 16px 36px -8px rgba(0, 0, 0, 0.6);
  --banner-grad: linear-gradient(135deg, #162032 0%, #1e293b 55%, #162032 100%);
  --badge-green-bg: rgba(22, 163, 74, 0.2);
  --badge-green-text: #4ade80;
}

/* ========== TOP NAVIGATION BAR ========== */
.removix-top-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  width: 100%;
  height: 68px;
  background: var(--topbar-bg);
  border-bottom: 1px solid var(--line);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-sizing: border-box;
  transition: background-color 0.25s ease, border-color 0.25s ease;
}

.nav-left-group {
  display: flex;
  align-items: center;
  gap: 16px;
}

.hamburger-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: transparent;
  border: 1px solid var(--line);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--ink);
  transition: all 0.2s ease;
}

.hamburger-btn:hover {
  background: var(--line-subtle);
  border-color: var(--primary);
  color: var(--primary);
}

.nav-brand-link {
  display: flex;
  align-items: center;
  gap: 3px;
  text-decoration: none;
}

.nav-brand-logo-img {
  width: 30px;
  height: 30px;
  flex-shrink: 0;
}

.nav-brand-text {
  font-size: 21px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--ink);
}

/* Center Search Bar */
.nav-search-bar {
  flex: 1;
  max-width: 520px;
  margin: 0 28px;
  position: relative;
  display: flex;
  align-items: center;
}

.search-input-wrapper {
  width: 100%;
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon-left {
  position: absolute;
  left: 14px;
  color: var(--ink-faint);
  pointer-events: none;
  display: flex;
  align-items: center;
}

.nav-search-input {
  width: 100%;
  height: 40px;
  padding: 0 85px 0 42px;
  border-radius: 20px;
  background: var(--bg-page);
  border: 1px solid var(--line);
  color: var(--ink);
  font-size: 13.5px;
  font-family: inherit;
  outline: none;
  transition: all 0.2s ease;
}

.nav-search-input:focus {
  background: var(--card-bg);
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.nav-search-input::placeholder {
  color: var(--ink-faint);
}

.search-ctrl-badge {
  position: absolute;
  right: 12px;
  background: var(--card-bg);
  border: 1px solid var(--line);
  color: var(--ink-faint);
  font-size: 11px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 6px;
  pointer-events: none;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

/* Nav Right Section */
.nav-right-group {
  display: flex;
  align-items: center;
  gap: 14px;
}

.theme-toggle-btn {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: transparent;
  border: 1px solid transparent;
  color: var(--ink-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-toggle-btn:hover {
  background: var(--line-subtle);
  color: var(--primary);
}

.nav-divider {
  width: 1px;
  height: 24px;
  background: var(--line);
}

.btn-nav-login {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 16px;
  border-radius: 9999px;
  background: var(--primary);
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
}

.btn-nav-login:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
}

.nav-user-container {
  position: relative;
  display: none;
}

.nav-avatar-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 3px 6px;
  border-radius: 20px;
  transition: background 0.15s ease;
}

.nav-avatar-btn:hover {
  background: var(--line-subtle);
}

.avatar-circle {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #0284c7;
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
}

.avatar-chevron {
  color: var(--ink-muted);
  width: 14px;
  height: 14px;
  transition: transform 0.2s ease;
}

/* User Dropdown Menu */
.user-dropdown-menu {
  position: absolute;
  top: 60px;
  right: 24px;
  width: 210px;
  background: var(--card-bg);
  border: 1px solid var(--line);
  border-radius: 14px;
  box-shadow: var(--shadow-lg);
  padding: 8px;
  display: none;
  flex-direction: column;
  z-index: 200;
}

.user-dropdown-menu.show {
  display: flex;
}

.dropdown-user-info {
  padding: 10px 12px 8px;
  border-bottom: 1px solid var(--line-subtle);
  margin-bottom: 6px;
}

.dropdown-user-name {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--ink);
}

.dropdown-user-email {
  font-size: 11.5px;
  color: var(--ink-muted);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
  text-decoration: none;
  cursor: pointer;
  border: none;
  background: transparent;
  width: 100%;
  text-align: left;
  transition: background 0.15s ease;
}

.dropdown-item:hover {
  background: var(--primary-light);
  color: var(--primary);
}

/* ========== APP BODY & SIDEBAR LAYOUT ========== */
.app-layout-shell {
  display: flex;
  width: 100%;
  min-height: 100vh;
  position: relative;
  box-sizing: border-box;
}

/* Left Sidebar: ALWAYS FIXED AT THE LEFT FROM THE TOP OF THE VIEWPORT */
.removix-main-sidebar {
  position: fixed;
  top: 68px;
  left: 0;
  bottom: 0;
  width: 250px;
  height: calc(100vh - 68px);
  background: var(--sidebar-bg);
  border-right: 1px solid var(--line);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px 14px 20px 16px;
  box-sizing: border-box;
  overflow-y: auto;
  overflow-x: hidden;
  transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 900;
}

.removix-main-sidebar.collapsed {
  transform: translateX(-100%);
}

.sidebar-items-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sidebar-nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 12px;
  color: var(--ink-muted);
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.18s ease;
  position: relative;
}

.sidebar-nav-link svg {
  width: 20px;
  height: 20px;
  stroke-width: 2;
  stroke: currentColor;
  fill: none;
  flex-shrink: 0;
}

.sidebar-nav-link:hover {
  background: var(--line-subtle);
  color: var(--ink);
}

.sidebar-nav-link.active {
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 700;
}

.sidebar-nav-link.active svg {
  stroke: var(--primary);
}

.sidebar-badge-soon {
  margin-left: auto;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 9999px;
  background: #f1f5f9;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

body.dark-mode .sidebar-badge-soon {
  background: #1e293b;
  color: #94a3b8;
}

/* Bottom "Upgrade to Pro" Card (Image 2) */
.sidebar-pro-card {
  margin-top: auto;
  padding: 14px 14px 14px 14px;
  border-radius: 16px;
  background: #f0f7ff;
  border: 1px solid #dbeafe;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

body.dark-mode .sidebar-pro-card {
  background: #1e293b;
  border-color: #334155;
}

.sidebar-pro-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.15);
  border-color: #93c5fd;
}

.pro-card-left {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.pro-crown-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  color: #0284c7;
  margin-top: 1px;
}

.pro-card-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #0284c7;
  line-height: 1.25;
  margin-bottom: 3px;
}

.pro-card-sub {
  font-size: 11.5px;
  color: var(--ink-muted);
  line-height: 1.35;
}

.pro-chevron-icon {
  width: 16px;
  height: 16px;
  color: var(--ink-muted);
  flex-shrink: 0;
}

/* Center Content Container: positioned cleanly beside the fixed sidebar */
.app-main-content-area {
  margin-top: 68px;
  margin-left: 250px;
  width: calc(100% - 250px);
  min-height: calc(100vh - 68px);
  padding: 24px 32px 60px;
  box-sizing: border-box;
  transition: margin-left 0.28s cubic-bezier(0.16, 1, 0.3, 1), width 0.28s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
}

body.sidebar-collapsed .app-main-content-area,
.removix-main-sidebar.collapsed ~ .app-main-content-area,
.app-layout-shell.sidebar-collapsed .app-main-content-area {
  margin-left: 0 !important;
  width: 100% !important;
}

@media (max-width: 1024px) {
  .removix-main-sidebar {
    position: fixed;
    top: 68px;
    bottom: 0;
    left: 0;
    transform: translateX(-100%);
    box-shadow: var(--shadow-lg);
    z-index: 1100;
  }
  .removix-main-sidebar.mobile-open {
    transform: translateX(0);
  }
  .app-main-content-area {
    margin-left: 0 !important;
    width: 100% !important;
    padding: 20px 18px 48px;
  }
}

/* Backdrop for Mobile Sidebar */
.sidebar-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  top: 68px;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(2px);
  z-index: 1050;
}

.sidebar-backdrop.active {
  display: block;
}

/* ========== MODALS & TOAST NOTIFICATIONS ========== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 1000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
  overflow-y: auto;
  overflow-x: hidden;
  box-sizing: border-box;
  -webkit-overflow-scrolling: touch;
}

.modal-overlay.active {
  display: flex;
}

.modal-card {
  background: var(--card-bg);
  border: 1px solid var(--line);
  border-radius: 20px;
  width: 100%;
  max-width: 440px;
  padding: 32px 28px;
  box-shadow: var(--shadow-lg);
  position: relative;
  text-align: center;
  animation: modalPop 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  box-sizing: border-box;
  margin: auto;
}

@keyframes modalPop {
  0% { transform: scale(0.94); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

.modal-close-btn {
  position: absolute;
  top: 18px;
  right: 18px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--line-subtle);
  border: none;
  color: var(--ink-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.modal-close-btn:hover {
  background: var(--line);
  color: var(--ink);
}

.btn-google-sign-in {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  padding: 11px 18px;
  border-radius: 10px;
  background: var(--card-bg);
  border: 1px solid var(--line);
  color: var(--ink);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.btn-google-sign-in:hover {
  background: var(--line-subtle);
  border-color: #cbd5e1;
  transform: translateY(-1px);
}

body.dark-mode .btn-google-sign-in {
  background: #111827;
  border-color: #1e293b;
  color: #f8fafc;
}

body.dark-mode .btn-google-sign-in:hover {
  background: #1f2937;
  border-color: #38bdf8;
}

/* Auth Modal Styles */
.auth-modal-card {
  max-width: 420px;
  width: 100%;
  padding: 30px 26px;
  text-align: left;
  border-radius: 20px;
  box-sizing: border-box;
  max-height: calc(100vh - 40px);
  max-height: calc(100dvh - 40px);
  overflow-y: auto;
  margin: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--line) transparent;
}

.auth-modal-card::-webkit-scrollbar {
  width: 5px;
}
.auth-modal-card::-webkit-scrollbar-thumb {
  background: var(--line);
  border-radius: 9999px;
}

.auth-header-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: #e0f2fe;
  color: #0284c7;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
}

body.dark-mode .auth-header-icon {
  background: rgba(14, 165, 233, 0.15);
  color: #38bdf8;
}

.auth-title {
  font-size: 20px;
  font-weight: 800;
  color: var(--ink);
  margin-bottom: 4px;
  letter-spacing: -0.02em;
}

.auth-subtitle {
  font-size: 13px;
  color: var(--ink-muted);
  line-height: 1.4;
  margin-bottom: 16px;
}

.auth-tabs-row {
  display: flex;
  background: var(--line-subtle);
  border-radius: 10px;
  padding: 3px;
  margin-bottom: 16px;
  gap: 4px;
}

body.dark-mode .auth-tabs-row {
  background: #0f172a;
}

.auth-tab-btn {
  flex: 1;
  padding: 8px 12px;
  border-radius: 8px;
  background: transparent;
  border: none;
  font-size: 13px;
  font-weight: 700;
  color: var(--ink-muted);
  cursor: pointer;
  transition: all 0.18s ease;
  text-align: center;
}

.auth-tab-btn.active {
  background: var(--card-bg);
  color: var(--primary);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

body.dark-mode .auth-tab-btn.active {
  background: #1e293b;
  color: #38bdf8;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.auth-field-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.auth-field-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--ink);
}

.auth-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.auth-input-icon {
  position: absolute;
  left: 12px;
  color: var(--ink-faint);
  display: flex;
  align-items: center;
  pointer-events: none;
}

.auth-input {
  width: 100%;
  padding: 10px 38px 10px 36px;
  border-radius: 10px;
  background: var(--bg-page);
  border: 1px solid var(--line);
  color: var(--ink);
  font-size: 13.5px;
  font-family: inherit;
  outline: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.auth-input:focus {
  background: var(--card-bg);
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}

body.dark-mode .auth-input {
  background: #0f172a;
  border-color: #1e293b;
  color: #f8fafc;
}

body.dark-mode .auth-input:focus {
  background: #111827;
  border-color: #38bdf8;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
}

.auth-toggle-pwd {
  position: absolute;
  right: 10px;
  background: transparent;
  border: none;
  color: var(--ink-muted);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
}

.btn-auth-submit {
  width: 100%;
  padding: 11px 16px;
  border-radius: 10px;
  background: var(--primary);
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 4px;
}

.btn-auth-submit:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
}

.btn-auth-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.auth-divider-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 12px 0 10px;
}

.auth-divider-line {
  flex: 1;
  height: 1px;
  background: var(--line);
}

.auth-divider-text {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--ink-faint);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.auth-alert {
  padding: 9px 12px;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 600;
  display: none;
  align-items: center;
  gap: 8px;
  line-height: 1.4;
  margin-bottom: 6px;
}

.auth-alert.error {
  display: flex;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
}

body.dark-mode .auth-alert.error {
  background: rgba(220, 38, 38, 0.15);
  border-color: rgba(220, 38, 38, 0.3);
  color: #f87171;
}

.auth-alert.success {
  display: flex;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #16a34a;
}

body.dark-mode .auth-alert.success {
  background: rgba(22, 163, 74, 0.15);
  border-color: rgba(22, 163, 74, 0.3);
  color: #4ade80;
}

.auth-alert.info {
  display: flex;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #2563eb;
}

body.dark-mode .auth-alert.info {
  background: rgba(37, 99, 235, 0.15);
  border-color: rgba(37, 99, 235, 0.3);
  color: #60a5fa;
}

.auth-bottom-switch {
  text-align: center;
  margin-top: 14px;
  font-size: 12.5px;
  color: var(--ink-muted);
}

.auth-bottom-switch a {
  color: var(--primary);
  font-weight: 700;
  text-decoration: none;
  cursor: pointer;
  margin-left: 4px;
}

.auth-bottom-switch a:hover {
  text-decoration: underline;
}

/* Responsive adjustments for Auth Modal (Tablet) */
@media (max-width: 768px) {
  .modal-overlay {
    padding: 16px;
  }
  .auth-modal-card {
    max-width: 400px;
    padding: 24px 22px;
    max-height: calc(100vh - 32px);
    max-height: calc(100dvh - 32px);
  }
  .auth-header-icon {
    width: 44px;
    height: 44px;
    margin-bottom: 12px;
  }
  .auth-title {
    font-size: 19px;
  }
  .auth-tabs-row {
    margin-bottom: 14px;
  }
  .auth-tab-btn {
    padding: 7.5px 10px;
    font-size: 12.5px;
  }
  .btn-google-sign-in {
    padding: 10px 14px;
    font-size: 13.5px;
  }
  .auth-form {
    gap: 11px;
  }
  .btn-auth-submit {
    padding: 10.5px 14px;
    font-size: 13.5px;
  }
}

/* Responsive adjustments for Auth Modal (Mobile) */
@media (max-width: 480px) {
  .modal-overlay {
    padding: 12px;
  }
  .auth-modal-card {
    max-width: 100%;
    width: 100%;
    padding: 22px 18px 20px;
    border-radius: 18px;
    max-height: calc(100vh - 24px);
    max-height: calc(100dvh - 24px);
  }
  .modal-close-btn {
    top: 12px;
    right: 12px;
    width: 28px;
    height: 28px;
  }
  .auth-header-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    margin-bottom: 10px;
  }
  .auth-header-icon svg {
    width: 19px;
    height: 19px;
  }
  .auth-title {
    font-size: 17.5px;
  }
  .auth-subtitle {
    font-size: 12px;
    margin-bottom: 12px;
    line-height: 1.35;
  }
  .auth-tabs-row {
    margin-bottom: 12px;
    padding: 2.5px;
  }
  .auth-tab-btn {
    padding: 7px 8px;
    font-size: 12px;
  }
  .btn-google-sign-in {
    padding: 9.5px 12px;
    font-size: 13px;
    gap: 10px;
  }
  .btn-google-sign-in svg {
    width: 17px;
    height: 17px;
  }
  .auth-divider-row {
    margin: 10px 0 8px;
    gap: 10px;
  }
  .auth-divider-text {
    font-size: 11px;
  }
  .auth-form {
    gap: 10px;
  }
  .auth-field-label {
    font-size: 11.5px;
  }
  .auth-input {
    padding: 8.5px 34px 8.5px 32px;
    font-size: 13px;
    border-radius: 8px;
  }
  .auth-input-icon {
    left: 10px;
  }
  .auth-toggle-pwd {
    right: 8px;
  }
  .btn-auth-submit {
    padding: 9.5px 14px;
    font-size: 13px;
    border-radius: 8px;
  }
  .auth-bottom-switch {
    margin-top: 12px;
    font-size: 12px;
  }
}

/* Landscape Mobile or Very Short Screens (max-height: 560px) */
@media (max-height: 560px) {
  .modal-overlay {
    padding: 8px;
    align-items: flex-start;
  }
  .auth-modal-card {
    padding: 16px 18px;
    margin: 8px auto;
  }
  .auth-header-icon {
    display: none;
  }
  .auth-subtitle {
    display: none;
  }
  .auth-title {
    font-size: 16px;
    margin-bottom: 6px;
  }
  .auth-tabs-row {
    margin-bottom: 8px;
  }
  .auth-divider-row {
    margin: 6px 0;
  }
  .auth-form {
    gap: 7px;
  }
}

/* Quick Search Palette (Ctrl+K) */
.search-palette-modal {
  max-width: 580px;
  padding: 18px;
  text-align: left;
}

.palette-input {
  width: 100%;
  padding: 12px 16px 12px 42px;
  border-radius: 12px;
  background: var(--bg-page);
  border: 1px solid var(--line);
  color: var(--ink);
  font-size: 15px;
  outline: none;
  font-family: inherit;
  box-sizing: border-box;
}

.palette-results-list {
  max-height: 340px;
  overflow-y: auto;
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.palette-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-radius: 10px;
  color: var(--ink);
  text-decoration: none;
  font-size: 13.5px;
  font-weight: 600;
  transition: background 0.15s ease;
}

.palette-item:hover {
  background: var(--primary-light);
  color: var(--primary);
}

.palette-item-tag {
  font-size: 11px;
  font-weight: 600;
  color: var(--ink-faint);
  background: var(--line-subtle);
  padding: 2px 8px;
  border-radius: 9999px;
}

/* Sleek Toast Notification */
.removix-toast {
  position: fixed;
  bottom: 28px;
  right: 28px;
  background: var(--ink);
  color: var(--card-bg);
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 13.5px;
  font-weight: 600;
  box-shadow: var(--shadow-lg);
  z-index: 2000;
  display: flex;
  align-items: center;
  gap: 10px;
  transform: translateY(120%);
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  pointer-events: none;
}

.removix-toast.show {
  transform: translateY(0);
  opacity: 1;
  pointer-events: auto;
}
"""

def render_top_bar_html() -> str:
    """Renders the top navigation bar with Supabase Auth state integration."""
    import json
    from modules.auth_config import get_supabase_config
    cfg = get_supabase_config()
    cfg_json = json.dumps(cfg)

    return f"""
<script id="removix-auth-config" type="application/json">{cfg_json}</script>
<header class="removix-top-nav">
  <!-- Left: Hamburger + Logo -->
  <div class="nav-left-group">
    <button class="hamburger-btn" id="hamburgerBtn" onclick="toggleSidebarMenu()" aria-label="Toggle Menu" title="Toggle navigation menu">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>
    <a href="/" class="nav-brand-link">
      <svg class="nav-brand-logo-img" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Removix Logo">
        <path d="m56.693 463.048c-12.974-15.793-15.047-37.869-5.237-55.796 7.387-13.498 13.718-28.467 18.996-44.911 9.16-28.554 16.229-57.886 21.215-87.986 4.976-30.102 8.16-59.045 9.561-86.829 1.391-27.786 2.091-50.94 2.091-69.463v-17.945h-23.568c-25.597 0-46.348-20.733-46.348-46.309 0-25.576 20.751-46.309 46.348-46.309h365.69c18.311 0 33.156 14.832 33.156 33.128v219.107c0 19.264-15.63 34.88-34.91 34.88h-1.594c-26.693 0-52.23-9.646-73.216-26.128-5.323-4.181-11.823-6.868-18.916-6.868-10.513 0-18.432 9.689-16.181 19.95 1.927 8.786 4.385 17.186 7.375 25.201 5.172 13.893 11.448 26.827 18.824 38.783 7.367 11.967 15.433 22.776 24.201 32.417 8.759 9.65 17.527 18.333 26.294 26.049 5.929 5.303 12.022 10.337 18.278 15.102 23.655 18.016 25.408 52.931 3.447 72.974-16.147 14.737-40.248 16.513-58.465 4.422-14.352-9.525-27.302-19.711-38.853-30.56-19.719-18.524-36.452-37.916-50.195-58.176-13.745-20.26-24.706-40.808-32.867-61.648-8.17-20.84-14.342-40.809-18.526-59.913-4.182-19.101-6.974-36.557-8.364-52.386-1.401-15.82-2.093-29.133-2.093-39.942 0-3.853 0-7.326 0-10.42 0-3.084.196-5.589.599-7.524 0-2.316.195-4.432.597-6.368h124.194c19.198 0 34.761-15.55 34.761-34.732 0-19.182-15.563-34.732-34.732-34.732h-111.621c-19.401 0-35.047 15.868-34.757 35.25l.07 4.69c0 33.575-1.494 64.643-4.482 93.197-2.988 28.563-6.871 54.901-11.652 79.014-4.781 24.123-10.158 45.93-16.134 65.412-5.976 19.491-12.158 36.757-18.526 51.807-3.388 8.158-6.881 15.979-10.478 23.464-15.872 33.026-60.69 38.415-83.953 10.098z" fill="#0284c7"/>
      </svg>
      <span class="nav-brand-text">emovix</span>
    </a>
  </div>

  <!-- Center: Search Input with Ctrl K -->
  <div class="nav-search-bar" onclick="openSearchPalette()">
    <div class="search-input-wrapper">
      <div class="search-icon-left">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </div>
      <input type="text" class="nav-search-input" placeholder="Search tools, files or features..." readonly>
      <span class="search-ctrl-badge">Ctrl K</span>
    </div>
  </div>

  <!-- Right: Moon/Sun toggle, Divider, Login, Avatar -->
  <div class="nav-right-group">
    <!-- Dark/Light Mode Moon Button -->
    <button class="theme-toggle-btn" id="themeToggleBtn" onclick="toggleThemeMode()" title="Toggle Dark/Light theme" aria-label="Toggle Theme">
      <svg class="moon-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      </svg>
    </button>

    <div class="nav-divider"></div>

    <!-- Login Button (Shown when logged out) -->
    <button class="btn-nav-login" id="navLoginBtn" onclick="openLoginModal()">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
      Login
    </button>

    <!-- User Avatar & Dropdown Chevron (Shown when logged in) -->
    <div class="nav-user-container" id="navUserContainer">
      <button class="nav-avatar-btn" id="navAvatarBtn" onclick="toggleUserDropdown(event)" aria-label="User profile">
        <div class="avatar-circle" id="navAvatarCircle">U</div>
        <svg class="avatar-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
      </button>

      <!-- Dropdown Popup (Real User Email, Profile and Logout ONLY) -->
      <div class="user-dropdown-menu" id="userDropdownMenu">
        <div class="dropdown-user-info">
          <p class="dropdown-user-name">Signed in as</p>
          <p class="dropdown-user-email" id="dropdownUserEmail">—</p>
        </div>
        <a href="/profile" class="dropdown-item" onclick="toggleUserDropdown();">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Profile
        </a>
        <button type="button" class="dropdown-item" style="color:#ef4444;" onclick="handleSupabaseSignOut(); toggleUserDropdown();">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          Logout
        </button>
      </div>
    </div>
  </div>
</header>
"""

def render_sidebar_html(active_tool="home") -> str:
    """Renders the left navigation sidebar matching Image 1 & Image 2."""
    def is_act(tool):
        return "active" if tool == active_tool else ""

    return f"""
<aside class="removix-main-sidebar" id="removixSidebar" aria-label="Tool Navigation">
  <div class="sidebar-items-list">
    <!-- 1. Home -->
    <a href="/" class="sidebar-nav-link {is_act('home')}" data-tool="home">
      <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      <span>Home</span>
    </a>

    <!-- 2. Image Tools -->
    <a href="/image-tools" class="sidebar-nav-link {is_act('image-tools')}" data-tool="image-tools">
      <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
      <span>Image Tools</span>
    </a>

    <!-- 3. PDF Tools -->
    <a href="/pdf-tools" class="sidebar-nav-link {is_act('pdf-tools')}" data-tool="pdf-tools">
      <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
      <span>PDF Tools</span>
    </a>

    <!-- 4. Video Tools -->
    <a href="/video-watermark" class="sidebar-nav-link {is_act('video-tools')}" data-tool="video-tools">
      <svg viewBox="0 0 24 24"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
      <span>Video Tools</span>
    </a>

    <!-- 5. More Tools -->
    <a href="/more-tools" class="sidebar-nav-link {is_act('more-tools')}" data-tool="more-tools">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/>
      </svg>
      <span>More Tools</span>
    </a>

  </div>

  <!-- Bottom: Upgrade to Pro Card (Image 2) -->
  <a href="javascript:void(0)" class="sidebar-pro-card" onclick="showRemovixToast('Removix Pro upgrade coming soon!')">
    <div class="pro-card-left">
      <svg class="pro-crown-icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M2 19h20v2H2v-2zm1.2-12l4.8 5.4 4-8.4 4 8.4 4.8-5.4L21 16H3l.2-9z"/>
      </svg>
      <div>
        <p class="pro-card-title">Upgrade to Pro</p>
        <p class="pro-card-sub">Get unlimited access to all tools.</p>
      </div>
    </div>
    <svg class="pro-chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="9 18 15 12 9 6"></polyline>
    </svg>
  </a>
</aside>

<!-- Supabase Auth Modal Dialog (Sign In / Sign Up) -->
<div class="modal-overlay" id="loginModalOverlay" onclick="handleModalOverlayClick(event)">
  <div class="modal-card auth-modal-card">
    <button class="modal-close-btn" onclick="closeLoginModal()" aria-label="Close modal">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>

    <div class="auth-header-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
    </div>

    <h3 class="auth-title" id="authModalTitle">Sign in to Removix</h3>
    <p class="auth-subtitle" id="authModalSubtitle">Access your tools, batch processing, and synced settings.</p>

    <!-- Tabs: Sign In / Create Account -->
    <div class="auth-tabs-row">
      <button type="button" class="auth-tab-btn active" id="tabSignIn" onclick="switchAuthTab('signin')">Sign In</button>
      <button type="button" class="auth-tab-btn" id="tabSignUp" onclick="switchAuthTab('signup')">Create Account</button>
    </div>

    <!-- Google Sign-In Button -->
    <button type="button" class="btn-google-sign-in" onclick="handleGoogleSignIn()">
      <svg width="18" height="18" viewBox="0 0 24 24">
        <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.15z"/>
        <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"/>
        <path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.98 0 12s.45 3.82 1.25 5.42l4.03-3.15z"/>
        <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/>
      </svg>
      Continue with Google
    </button>

    <div class="auth-divider-row">
      <div class="auth-divider-line"></div>
      <span class="auth-divider-text">or with email</span>
      <div class="auth-divider-line"></div>
    </div>

    <!-- Alert / Status Notice -->
    <div class="auth-alert" id="authAlertBox"></div>

    <!-- Email/Password Form -->
    <form class="auth-form" id="authForm" onsubmit="handleAuthFormSubmit(event)">
      <div class="auth-field-group">
        <label class="auth-field-label" for="authEmailInput">Email address</label>
        <div class="auth-input-wrapper">
          <span class="auth-input-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          </span>
          <input type="email" id="authEmailInput" class="auth-input" placeholder="name@example.com" required autocomplete="email">
        </div>
      </div>

      <div class="auth-field-group">
        <label class="auth-field-label" for="authPasswordInput">Password</label>
        <div class="auth-input-wrapper">
          <span class="auth-input-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          </span>
          <input type="password" id="authPasswordInput" class="auth-input" placeholder="At least 6 characters" required autocomplete="current-password" minlength="6">
          <button type="button" class="auth-toggle-pwd" onclick="togglePasswordVisibility('authPasswordInput')" title="Toggle password visibility">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          </button>
        </div>
      </div>

      <!-- Confirm Password (Only on Sign Up tab) -->
      <div class="auth-field-group" id="confirmPasswordGroup" style="display:none;">
        <label class="auth-field-label" for="authConfirmPasswordInput">Confirm Password</label>
        <div class="auth-input-wrapper">
          <span class="auth-input-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          </span>
          <input type="password" id="authConfirmPasswordInput" class="auth-input" placeholder="Repeat password" minlength="6">
        </div>
      </div>

      <button type="submit" class="btn-auth-submit" id="authSubmitBtn">
        <span id="authSubmitText">Sign In</span>
      </button>
    </form>

    <div class="auth-bottom-switch">
      <span id="authSwitchPrompt">Don't have an account?</span>
      <a id="authSwitchLink" onclick="toggleAuthMode()">Create account</a>
    </div>
  </div>
</div>

<!-- Search Palette Modal (Ctrl+K) -->
<div class="modal-overlay" id="searchPaletteOverlay" onclick="handleSearchOverlayClick(event)">
  <div class="modal-card search-palette-modal">
    <div style="position:relative;">
      <div class="search-icon-left" style="left:14px; top:14px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </div>
      <input type="text" id="paletteSearchInput" class="palette-input" placeholder="Type to search tools (e.g. compress, pdf, watermark, resize)..." oninput="filterSearchPalette(this.value)">
    </div>

    <div class="palette-results-list" id="paletteResults">
      <!-- Generated via JS -->
    </div>
  </div>
</div>

<!-- Floating Toast Notification -->
<div class="removix-toast" id="removixToast">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
  <span id="toastMessage">Notice</span>
</div>
"""

SIDEBAR_JS = r"""
// ==================== SIDEBAR & THEME SCRIPT ====================

// 1. Sidebar Toggle
function toggleSidebarMenu() {
  const sidebar = document.getElementById('removixSidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  if (!sidebar) return;
  const isMobile = window.innerWidth <= 1024;
  if (isMobile) {
    const isOpen = sidebar.classList.toggle('mobile-open');
    if (backdrop) {
      backdrop.classList.toggle('active', isOpen);
    }
  } else {
    sidebar.classList.toggle('collapsed');
    document.body.classList.toggle('sidebar-collapsed');
  }
}

function closeMobileSidebar() {
  const sidebar = document.getElementById('removixSidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  if (sidebar) sidebar.classList.remove('mobile-open');
  if (backdrop) backdrop.classList.remove('active');
}

// 2. Dark/Light Theme Switching with Storage Sync
function initThemeMode() {
  const saved = localStorage.getItem('removix_theme');
  const isDark = (saved === 'dark') || (!saved && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  if (isDark) {
    document.documentElement.classList.add('dark-mode');
    document.documentElement.setAttribute('data-theme', 'dark');
    document.body.classList.add('dark-mode');
    document.body.setAttribute('data-theme', 'dark');
    updateThemeIcon(true);
  } else {
    document.documentElement.classList.remove('dark-mode');
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.classList.remove('dark-mode');
    document.body.setAttribute('data-theme', 'light');
    updateThemeIcon(false);
  }
}

function updateThemeIcon(isDark) {
  const btn = document.getElementById('themeToggleBtn');
  if (!btn) return;
  if (isDark) {
    btn.innerHTML = `<svg class="sun-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`;
  } else {
    btn.innerHTML = `<svg class="moon-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
  }
}

function toggleThemeMode() {
  const isDark = !document.documentElement.classList.contains('dark-mode');
  if (isDark) {
    document.documentElement.classList.add('dark-mode');
    document.documentElement.setAttribute('data-theme', 'dark');
    document.body.classList.add('dark-mode');
    document.body.setAttribute('data-theme', 'dark');
  } else {
    document.documentElement.classList.remove('dark-mode');
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.classList.remove('dark-mode');
    document.body.setAttribute('data-theme', 'light');
  }
  const themeStr = isDark ? 'dark' : 'light';
  localStorage.setItem('removix_theme', themeStr);
  updateThemeIcon(isDark);
  
  // Persist to backend settings
  fetch('/api/settings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ theme: themeStr })
  }).catch(() => {});
}

// 3. Supabase Authentication System
let _currentAuthMode = 'signin';
let _removixSession = null;
let _supabaseClient = null;
let _authListeners = [];

window.removixGetSession = function() {
  return _removixSession;
};

function dispatchAuthEvent(session) {
  _removixSession = session;
  const evt = new CustomEvent('removix:auth-changed', { detail: { session: session } });
  document.dispatchEvent(evt);
  window.dispatchEvent(evt);
}

function getAuthConfig() {
  try {
    const el = document.getElementById('removix-auth-config');
    if (el) return JSON.parse(el.textContent);
  } catch (e) {}
  return { supabase_url: '', supabase_anon_key: '', configured: false };
}

function createFallbackSupabaseClient(url, key) {
  const STORAGE_KEY = 'removix_supabase_session';

  function saveSession(sess) {
    if (sess) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sess));
    } else {
      localStorage.removeItem(STORAGE_KEY);
    }
  }

  function getSavedSession() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch(e) {
      return null;
    }
  }

  return {
    auth: {
      getSession: async function() {
        const sess = getSavedSession();
        return { data: { session: sess }, error: null };
      },
      signUp: async function(creds) {
        if (!url || !key || url.includes('your-project-id')) {
          throw new Error('Authentication service is currently unavailable. Please try again later.');
        }
        const resp = await fetch(url.replace(/\/$/, '') + '/auth/v1/signup', {
          method: 'POST',
          headers: {
            'apikey': key,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email: creds.email, password: creds.password })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.msg || data.message || data.error_description || 'Signup failed');
        const session = data.access_token ? {
          access_token: data.access_token,
          user: data.user || { id: data.id, email: creds.email }
        } : null;
        if (session) saveSession(session);
        return { data: { session: session, user: data.user || data }, error: null };
      },
      signInWithPassword: async function(creds) {
        if (!url || !key || url.includes('your-project-id')) {
          throw new Error('Authentication service is currently unavailable. Please try again later.');
        }
        const resp = await fetch(url.replace(/\/$/, '') + '/auth/v1/token?grant_type=password', {
          method: 'POST',
          headers: {
            'apikey': key,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email: creds.email, password: creds.password })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.msg || data.error_description || data.message || 'Invalid email or password');
        const session = {
          access_token: data.access_token,
          user: data.user
        };
        saveSession(session);
        return { data: { session: session, user: data.user }, error: null };
      },
      signInWithOAuth: async function(opts) {
        if (!url || !key || url.includes('your-project-id')) {
          throw new Error('Google Sign-In is currently unavailable. Please try again later.');
        }
        const provider = opts.provider || 'google';
        const redirect = (opts.options && opts.options.redirectTo) || window.location.origin;
        window.location.href = url.replace(/\/$/, '') + '/auth/v1/authorize?provider=' + encodeURIComponent(provider) + '&redirect_to=' + encodeURIComponent(redirect);
        return { data: null, error: null };
      },
      signOut: async function() {
        const sess = getSavedSession();
        if (sess && sess.access_token && url && key && !url.includes('your-project-id')) {
          fetch(url.replace(/\/$/, '') + '/auth/v1/logout', {
            method: 'POST',
            headers: {
              'apikey': key,
              'Authorization': 'Bearer ' + sess.access_token
            }
          }).catch(() => {});
        }
        saveSession(null);
        return { error: null };
      },
      onAuthStateChange: function(callback) {
        _authListeners.push(callback);
        return {
          data: {
            subscription: {
              unsubscribe: () => {
                _authListeners = _authListeners.filter(cb => cb !== callback);
              }
            }
          }
        };
      }
    }
  };
}

function initSupabase() {
  const cfg = getAuthConfig();

  if (window.supabase && typeof window.supabase.createClient === 'function' && cfg.configured) {
    try {
      _supabaseClient = window.supabase.createClient(cfg.supabase_url, cfg.supabase_anon_key);
    } catch(e) {
      _supabaseClient = createFallbackSupabaseClient(cfg.supabase_url, cfg.supabase_anon_key);
    }
  } else {
    _supabaseClient = createFallbackSupabaseClient(cfg.supabase_url, cfg.supabase_anon_key);
  }

  if (_supabaseClient && _supabaseClient.auth) {
    _supabaseClient.auth.onAuthStateChange(function(event, session) {
      updateAuthUI(session);
      dispatchAuthEvent(session);
    });

    _supabaseClient.auth.getSession().then(function(res) {
      const sess = res && res.data ? res.data.session : null;
      updateAuthUI(sess);
      dispatchAuthEvent(sess);
    }).catch(function() {
      updateAuthUI(null);
      dispatchAuthEvent(null);
    });
  }

  handleOAuthRedirect();
}

function handleOAuthRedirect() {
  if (window.location.hash && window.location.hash.includes('access_token=')) {
    try {
      const params = new URLSearchParams(window.location.hash.substring(1));
      const accessToken = params.get('access_token');
      const refreshToken = params.get('refresh_token');
      if (accessToken) {
        const cfg = getAuthConfig();
        if (cfg.supabase_url && !cfg.supabase_url.includes('your-project-id')) {
          fetch(cfg.supabase_url.replace(/\/$/, '') + '/auth/v1/user', {
            headers: {
              'apikey': cfg.supabase_anon_key,
              'Authorization': 'Bearer ' + accessToken
            }
          })
          .then(r => r.json())
          .then(user => {
            if (user && user.id) {
              const session = { access_token: accessToken, refresh_token: refreshToken, user: user };
              localStorage.setItem('removix_supabase_session', JSON.stringify(session));
              updateAuthUI(session);
              dispatchAuthEvent(session);
              showRemovixToast('Signed in successfully with Google!');
              history.replaceState(null, '', window.location.pathname + window.location.search);
            }
          })
          .catch(() => {});
        }
      }
    } catch(e) {}
  }
}

function updateAuthUI(session) {
  _removixSession = session;
  const loginBtn = document.getElementById('navLoginBtn');
  const userContainer = document.getElementById('navUserContainer');
  const avatarCircle = document.getElementById('navAvatarCircle');
  const dropdownEmail = document.getElementById('dropdownUserEmail');

  if (session && session.user) {
    const email = session.user.email || 'User';
    const initial = email.charAt(0).toUpperCase();

    if (loginBtn) loginBtn.style.display = 'none';
    if (userContainer) userContainer.style.display = 'block';
    if (avatarCircle) avatarCircle.textContent = initial;
    if (dropdownEmail) dropdownEmail.textContent = email;
  } else {
    if (loginBtn) loginBtn.style.display = 'inline-flex';
    if (userContainer) userContainer.style.display = 'none';
    if (dropdownEmail) dropdownEmail.textContent = '—';
  }
}

function openLoginModal() {
  const el = document.getElementById('loginModalOverlay');
  if (el) el.classList.add('active');
  const alertBox = document.getElementById('authAlertBox');
  if (alertBox) alertBox.style.display = 'none';
}

function closeLoginModal() {
  const el = document.getElementById('loginModalOverlay');
  if (el) el.classList.remove('active');
}

function handleModalOverlayClick(e) {
  if (e.target.id === 'loginModalOverlay') {
    closeLoginModal();
  }
}

function switchAuthTab(mode) {
  _currentAuthMode = mode;
  const tabIn = document.getElementById('tabSignIn');
  const tabUp = document.getElementById('tabSignUp');
  const confirmGroup = document.getElementById('confirmPasswordGroup');
  const submitText = document.getElementById('authSubmitText');
  const promptText = document.getElementById('authSwitchPrompt');
  const linkText = document.getElementById('authSwitchLink');
  const title = document.getElementById('authModalTitle');
  const subtitle = document.getElementById('authModalSubtitle');
  const alertBox = document.getElementById('authAlertBox');
  if (alertBox) { alertBox.style.display = 'none'; alertBox.className = 'auth-alert'; }

  if (mode === 'signup') {
    if (tabIn) tabIn.classList.remove('active');
    if (tabUp) tabUp.classList.add('active');
    if (confirmGroup) confirmGroup.style.display = 'flex';
    if (submitText) submitText.textContent = 'Create Account';
    if (promptText) promptText.textContent = 'Already have an account?';
    if (linkText) linkText.textContent = 'Sign In';
    if (title) title.textContent = 'Create your Account';
    if (subtitle) subtitle.textContent = 'Join Removix to unlock all features and sync across devices.';
  } else {
    if (tabUp) tabUp.classList.remove('active');
    if (tabIn) tabIn.classList.add('active');
    if (confirmGroup) confirmGroup.style.display = 'none';
    if (submitText) submitText.textContent = 'Sign In';
    if (promptText) promptText.textContent = "Don't have an account?";
    if (linkText) linkText.textContent = 'Create account';
    if (title) title.textContent = 'Sign in to Removix';
    if (subtitle) subtitle.textContent = 'Access your tools, batch processing, and synced settings.';
  }
}

function toggleAuthMode() {
  switchAuthTab(_currentAuthMode === 'signin' ? 'signup' : 'signin');
}

function showAuthAlert(msg, type) {
  const box = document.getElementById('authAlertBox');
  if (!box) return;
  box.textContent = msg;
  box.className = 'auth-alert ' + (type || 'error');
  box.style.display = 'flex';
}

function togglePasswordVisibility(inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  input.type = input.type === 'password' ? 'text' : 'password';
}

async function handleAuthFormSubmit(e) {
  e.preventDefault();
  const emailInput = document.getElementById('authEmailInput');
  const passInput = document.getElementById('authPasswordInput');
  const confirmInput = document.getElementById('authConfirmPasswordInput');
  const submitBtn = document.getElementById('authSubmitBtn');
  const submitText = document.getElementById('authSubmitText');

  const email = emailInput ? emailInput.value.trim() : '';
  const password = passInput ? passInput.value : '';
  const confirm = confirmInput ? confirmInput.value : '';

  if (!email || !password) {
    showAuthAlert('Please enter both email and password.', 'error');
    return;
  }

  if (_currentAuthMode === 'signup') {
    if (password.length < 6) {
      showAuthAlert('Password must be at least 6 characters long.', 'error');
      return;
    }
    if (password !== confirm) {
      showAuthAlert('Passwords do not match. Please re-check.', 'error');
      return;
    }
  }

  if (submitBtn) submitBtn.disabled = true;
  if (submitText) submitText.textContent = _currentAuthMode === 'signup' ? 'Creating account...' : 'Signing in...';

  try {
    if (_currentAuthMode === 'signup') {
      const res = await _supabaseClient.auth.signUp({ email: email, password: password });
      if (res.error) throw res.error;

      if (res.data && res.data.session) {
        updateAuthUI(res.data.session);
        dispatchAuthEvent(res.data.session);
        closeLoginModal();
        showRemovixToast('Account created and signed in successfully!');
      } else {
        showAuthAlert('Account created! Please check your email for confirmation or sign in.', 'success');
      }
    } else {
      const res = await _supabaseClient.auth.signInWithPassword({ email: email, password: password });
      if (res.error) throw res.error;

      if (res.data && res.data.session) {
        updateAuthUI(res.data.session);
        dispatchAuthEvent(res.data.session);
        closeLoginModal();
        showRemovixToast('Signed in successfully as ' + email);
      }
    }
  } catch (err) {
    let msg = err.message || 'Authentication error. Please try again.';
    showAuthAlert(msg, 'error');
  } finally {
    if (submitBtn) submitBtn.disabled = false;
    if (submitText) submitText.textContent = _currentAuthMode === 'signup' ? 'Create Account' : 'Sign In';
  }
}

async function handleGoogleSignIn() {
  try {
    await _supabaseClient.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: window.location.origin + window.location.pathname
      }
    });
  } catch (err) {
    let msg = err.message || 'Google sign in failed.';
    showAuthAlert(msg, 'error');
  }
}

async function handleSupabaseSignOut() {
  try {
    if (_supabaseClient && _supabaseClient.auth) {
      await _supabaseClient.auth.signOut();
    }
  } catch (e) {}
  updateAuthUI(null);
  dispatchAuthEvent(null);
  showRemovixToast('Signed out successfully.');
}


// 4. User Dropdown
function toggleUserDropdown(e) {
  if (e) e.stopPropagation();
  const menu = document.getElementById('userDropdownMenu');
  if (menu) menu.classList.toggle('show');
}

document.addEventListener('click', function() {
  const menu = document.getElementById('userDropdownMenu');
  if (menu && menu.classList.contains('show')) menu.classList.remove('show');
});

// 5. Toast Notifications
let toastTimeout = null;
function showRemovixToast(msg) {
  const toast = document.getElementById('removixToast');
  const msgEl = document.getElementById('toastMessage');
  if (!toast || !msgEl) return;
  msgEl.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove('show');
  }, 2800);
}

// 6. Search Palette (Ctrl+K)
const REMOVIX_SEARCH_TOOLS = [
  { name: 'Remove Background', url: '/bg-remove', tag: 'AI Image' },
  { name: 'Compress Image', url: '/compress-image', tag: 'Image Tool' },
  { name: 'Resize Image', url: '/resize-image', tag: 'Image Tool' },
  { name: 'Crop Image', url: '/crop-image', tag: 'Image Tool' },
  { name: 'PDF to Image', url: '/pdf-to-image', tag: 'PDF Tool' },
  { name: 'Image to PDF', url: '/image-to-pdf', tag: 'PDF Tool' },
  { name: 'Merge PDF', url: '/merge-pdf', tag: 'PDF Tool' },
  { name: 'Split PDF', url: '/split-pdf', tag: 'PDF Tool' },
  { name: 'Rotate PDF', url: '/rotate-pdf', tag: 'PDF Tool' },
  { name: 'Delete PDF Pages', url: '/delete-pages', tag: 'PDF Tool' },
  { name: 'Protect PDF', url: '/protect-pdf', tag: 'PDF Tool' },
  { name: 'Unlock PDF', url: '/unlock-pdf', tag: 'PDF Tool' },
  { name: 'Word to PDF', url: '/word-to-pdf', tag: 'PDF Tool' },
  { name: 'Edit PDF', url: '/edit-pdf', tag: 'PDF Tool' },
  { name: 'Video Watermark Remove', url: '/video-watermark', tag: 'Video Tool' },
  { name: 'Image Watermark Remove', url: '/image-watermark', tag: 'Image Tool' },
  { name: 'Flip Image', url: '/flip-image', tag: 'Image Tool' },
  { name: 'Black & White Image', url: '/black-white', tag: 'Image Tool' },
  { name: 'Add Text to Image', url: '/add-text-image', tag: 'Image Tool' },
  { name: 'Make Round Image', url: '/make-round-image', tag: 'Image Tool' },
  { name: 'Blur Background', url: '/blur-background', tag: 'AI Image' },
  { name: 'Photo Collage Maker', url: '/collage-maker', tag: 'Image Tool' },
  { name: 'Upscale Image', url: '/upscale-image', tag: 'AI Enhancer' },
  { name: 'PNG to JPG', url: '/png-to-jpg', tag: 'Format Convert' },
  { name: 'JPG to PNG', url: '/jpg-to-png', tag: 'Format Convert' },
  { name: 'WEBP to JPG', url: '/webp-to-jpg', tag: 'Format Convert' },
  { name: 'JPG to WEBP', url: '/jpg-to-webp', tag: 'Format Convert' },
  { name: 'PNG to SVG', url: '/png-to-svg', tag: 'Format Convert' },
  { name: 'QR Code Generator', url: '/qr-code', tag: 'Generator' },
  { name: 'Image to Text (OCR)', url: '/image-to-text', tag: 'OCR Tool' },
  { name: 'More Tools Hub', url: '/more-tools', tag: 'Navigation' },
];

function openSearchPalette() {
  const overlay = document.getElementById('searchPaletteOverlay');
  const input = document.getElementById('paletteSearchInput');
  if (overlay) {
    overlay.classList.add('active');
    if (input) {
      input.value = '';
      input.focus();
      filterSearchPalette('');
    }
  }
}

function closeSearchPalette() {
  const overlay = document.getElementById('searchPaletteOverlay');
  if (overlay) overlay.classList.remove('active');
}

function handleSearchOverlayClick(e) {
  if (e.target.id === 'searchPaletteOverlay') {
    closeSearchPalette();
  }
}

function filterSearchPalette(query) {
  const container = document.getElementById('paletteResults');
  if (!container) return;
  const q = query.trim().toLowerCase();
  const matched = REMOVIX_SEARCH_TOOLS.filter(t => 
    !q || t.name.toLowerCase().includes(q) || t.tag.toLowerCase().includes(q)
  );

  if (matched.length === 0) {
    container.innerHTML = '<p style="padding:16px; font-size:13.5px; color:var(--ink-muted); text-align:center;">No matching tools found.</p>';
    return;
  }

  container.innerHTML = matched.slice(0, 8).map(t => `
    <a href="${t.url}" class="palette-item">
      <span>${t.name}</span>
      <span class="palette-item-tag">${t.tag}</span>
    </a>
  `).join('');
}

function focusRecentFiles(e) {
  const el = document.getElementById('recent-files');
  if (el) {
    if (e) e.preventDefault();
    el.scrollIntoView({ behavior: 'smooth' });
  } else {
    window.location.href = '/#recent-files';
  }
}

// Keyboard shortcuts (Ctrl+K, Escape)
document.addEventListener('keydown', function(e) {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    openSearchPalette();
  } else if (e.key === 'Escape') {
    closeSearchPalette();
    closeLoginModal();
  }
});

// Run theme & Supabase auth init on page load
document.addEventListener('DOMContentLoaded', function() {
  initThemeMode();
  initSupabase();
});
if (document.readyState !== 'loading') {
  initThemeMode();
  initSupabase();
}
"""
