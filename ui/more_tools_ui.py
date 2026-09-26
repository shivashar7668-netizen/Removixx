"""
Removix UI - More Tools Hub View
--------------------------------
Hub page displaying a single unified grid of specialized tools:
- Image & PDF to Text (OCR)
- QR Code Generator
- Future specialized utilities

Uses the exact same card sizing, weights, hover interactions, grid layout,
and dark/light tokens as Image Tools and PDF Tools grids.
"""

from ui.layout import render_layout

MORE_TOOLS_CSS = r"""
.tool-container {
  max-width: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
  box-sizing: border-box !important;
}

.main-tool-card {
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}

.app-main-content-area {
  padding: 24px 32px 60px !important;
  box-sizing: border-box !important;
}

/* Unified Grid Layout: Desktop (width > 1200px) -> exactly 7 cards */
.more-tools-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
  width: 100%;
  box-sizing: border-box;
}

/* Tablet (768px - 1200px) -> exactly 4 cards */
@media (max-width: 1200px) {
  .app-main-content-area {
    padding: 20px 20px 48px !important;
  }
  .more-tools-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
  }
}

/* Mobile (width < 768px) -> exactly 2 cards */
@media (max-width: 767px) {
  .app-main-content-area {
    padding: 16px 12px 40px !important;
  }
  .more-tools-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
}

.more-tool-card {
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;
  padding: 16px 12px 14px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  text-decoration: none;
  color: inherit;
  position: relative;
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
  min-width: 0;
  width: 100%;
  min-height: 100%;
  box-sizing: border-box;
}

.more-tool-card:hover {
  border-color: #bae6fd;
  transform: translateY(-3px);
  box-shadow: 0 10px 24px rgba(2, 132, 199, 0.12);
}

.more-tool-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  flex-shrink: 0;
  background: var(--icon-bg);
  transition: background-color 0.2s ease;
}

html.dark-mode .more-tool-icon,
body.dark-mode .more-tool-icon,
[data-theme="dark"] .more-tool-icon {
  background: var(--icon-dark-bg) !important;
}

.more-tool-icon svg {
  width: 22px;
  height: 22px;
}

.more-tool-name {
  font-size: 13.5px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 6px 0;
  line-height: 1.25;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  white-space: normal;
  width: 100%;
  min-width: 0;
}

.more-tool-desc {
  font-size: 11.5px;
  color: #64748b;
  line-height: 1.45;
  margin: 0 0 12px 0;
  flex: 1;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  width: 100%;
  min-width: 0;
}

.more-tool-arrow {
  margin-top: auto;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  transition: all 0.25s ease;
  flex-shrink: 0;
}

.more-tool-card:hover .more-tool-arrow {
  background: #0284c7;
  border-color: #0284c7;
  color: #ffffff;
  transform: translateX(3px);
}

/* Dark Mode (Supports html.dark-mode, body.dark-mode, [data-theme="dark"]) */
html.dark-mode .more-tool-card,
body.dark-mode .more-tool-card,
[data-theme="dark"] .more-tool-card {
  background: #1e293b !important;
  border-color: #334155 !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
}

html.dark-mode .more-tool-card:hover,
body.dark-mode .more-tool-card:hover,
[data-theme="dark"] .more-tool-card:hover {
  border-color: #38bdf8 !important;
  background: #1e293b !important;
  box-shadow: 0 10px 24px rgba(56, 189, 248, 0.15);
}

html.dark-mode .more-tool-name,
body.dark-mode .more-tool-name,
[data-theme="dark"] .more-tool-name {
  color: #f1f5f9 !important;
}

html.dark-mode .more-tool-desc,
body.dark-mode .more-tool-desc,
[data-theme="dark"] .more-tool-desc {
  color: #94a3b8 !important;
}

html.dark-mode .more-tool-arrow,
body.dark-mode .more-tool-arrow,
[data-theme="dark"] .more-tool-arrow {
  background: #0f172a !important;
  border-color: #334155 !important;
  color: #64748b !important;
}
"""


def render_more_tools_page() -> str:
    """Renders the More Tools hub view with a single unified tool grid."""

    tools = [
        {
            "name": "Image & PDF to Text (OCR)",
            "desc": "Extract text from photos, scans, and documents with Hindi and English bilingual recognition.",
            "route": "/image-to-text",
            "icon_bg": "#e0f2fe",
            "icon_color": "#0284c7",
            "icon_svg": '''<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#0284c7" stroke-width="1.8">
                <path d="M4 7V4h16v3" stroke-linecap="round"/>
                <line x1="12" y1="4" x2="12" y2="20" stroke-linecap="round"/>
                <line x1="8" y1="20" x2="16" y2="20" stroke-linecap="round"/>
                <rect x="2" y="2" width="20" height="20" rx="3" stroke-dasharray="3 3"/>
              </svg>''',
        },
        {
            "name": "QR Code Generator",
            "desc": "Create custom styled QR codes for links, Wi-Fi, text, and contacts with color presets and instant export.",
            "route": "/qr-code",
            "icon_bg": "#fef3c7",
            "icon_color": "#d97706",
            "icon_svg": '''<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#d97706" stroke-width="1.8">
                <rect x="3" y="3" width="7" height="7" rx="1.5" stroke-linecap="round"/>
                <rect x="14" y="3" width="7" height="7" rx="1.5" stroke-linecap="round"/>
                <rect x="14" y="14" width="7" height="7" rx="1.5" stroke-linecap="round"/>
                <rect x="3" y="14" width="7" height="7" rx="1.5" stroke-linecap="round"/>
                <path d="M10 7h4M7 10v4M17 10v4M10 17h4"/>
              </svg>''',
        },
    ]

    def hex_to_rgba(hex_code: str, alpha: float = 0.18) -> str:
        h = hex_code.lstrip("#")
        if len(h) == 6:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            return f"rgba({r}, {g}, {b}, {alpha})"
        return hex_code

    cards_html = ""
    for tool in tools:
        dark_bg = hex_to_rgba(tool.get("icon_color", "#0284c7"), 0.18)
        cards_html += f'''
        <a href="{tool['route']}" class="more-tool-card" style="text-decoration:none;">
          <div class="more-tool-icon" style="--icon-bg:{tool['icon_bg']}; --icon-dark-bg:{dark_bg};">
            {tool['icon_svg']}
          </div>
          <h3 class="more-tool-name">{tool['name']}</h3>
          <p class="more-tool-desc">{tool['desc']}</p>
          <div class="more-tool-arrow">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
            </svg>
          </div>
        </a>
        '''

    main_card_html = f'''
    <div class="more-tools-grid">
      {cards_html}
    </div>
    '''

    return render_layout(
        title="More Tools",
        active_tool="more-tools",
        hero_title="More Tools",
        hero_sub="Discover specialized utilities for <strong>Text Extraction (OCR)</strong> and <strong>QR Code Generation</strong>.",
        main_card_html=main_card_html,
        extra_css=MORE_TOOLS_CSS,
    )
