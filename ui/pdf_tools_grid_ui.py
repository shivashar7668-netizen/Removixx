"""
Removix UI - PDF Tools Grid Page
---------------------------------
Displays a 5x2 card grid of all 10 PDF tools.
Each card links to its individual tool page.
Matches reference design: white rounded cards, colored icons, descriptions, arrow buttons.
"""

from ui.layout import render_layout


def render_pdf_tools_grid_page() -> str:
    """Renders the PDF Tools hub grid with 10 tool cards."""

    # Define all 10 tools with their icon SVGs, colors, names, descriptions, and routes
    tools = [
        {
            "name": "PDF to Image",
            "desc": "Convert PDF pages into high-quality images (PNG/JPG).",
            "route": "/pdf-to-image",
            "icon_bg": "#fee2e2",
            "icon_color": "#dc2626",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#dc2626" stroke-width="1.8"><rect x="3" y="3" width="14" height="14" rx="2" stroke-linecap="round"/><path d="M7 21h12a2 2 0 0 0 2-2V7" stroke-linecap="round"/><circle cx="8" cy="8" r="1.5" fill="#dc2626" stroke="none"/><path d="M17 13l-3.5-3.5L7 16" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        },
        {
            "name": "Image to PDF",
            "desc": "Convert multiple images into a single PDF file.",
            "route": "/image-to-pdf",
            "icon_bg": "#dbeafe",
            "icon_color": "#2563eb",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#2563eb" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke-linecap="round"/><polyline points="14 2 14 8 20 8"/><rect x="8" y="12" width="8" height="6" rx="1" stroke-linecap="round"/></svg>',
        },
        {
            "name": "Merge PDF",
            "desc": "Combine multiple PDF files into one document.",
            "route": "/merge-pdf",
            "icon_bg": "#d1fae5",
            "icon_color": "#059669",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#059669" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke-linecap="round"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>',
        },
        {
            "name": "Split PDF",
            "desc": "Split a PDF into multiple separate files.",
            "route": "/split-pdf",
            "icon_bg": "#e0f2fe",
            "icon_color": "#0284c7",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#0284c7" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke-linecap="round"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13" stroke-linecap="round"/></svg>',
        },
        {
            "name": "Rotate PDF",
            "desc": "Rotate PDF pages left or right with ease.",
            "route": "/rotate-pdf",
            "icon_bg": "#fae8ff",
            "icon_color": "#a855f7",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#a855f7" stroke-width="1.8"><path d="M1 4v6h6" stroke-linecap="round" stroke-linejoin="round"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        },
        {
            "name": "Delete Pages",
            "desc": "Remove unwanted pages from your PDF file.",
            "route": "/delete-pages",
            "icon_bg": "#fee2e2",
            "icon_color": "#dc2626",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#dc2626" stroke-width="1.8"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke-linecap="round" stroke-linejoin="round"/><line x1="10" y1="11" x2="10" y2="17" stroke-linecap="round"/><line x1="14" y1="11" x2="14" y2="17" stroke-linecap="round"/></svg>',
        },
        {
            "name": "Protect PDF",
            "desc": "Add password protection to secure your PDF file.",
            "route": "/protect-pdf",
            "icon_bg": "#fef9c3",
            "icon_color": "#ca8a04",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#ca8a04" stroke-width="1.8"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4" stroke-linecap="round"/></svg>',
        },
        {
            "name": "Unlock PDF",
            "desc": "Remove password protection from your PDF file.",
            "route": "/unlock-pdf",
            "icon_bg": "#d1fae5",
            "icon_color": "#059669",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#059669" stroke-width="1.8"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1" stroke-linecap="round"/></svg>',
        },
        {
            "name": "Word to PDF",
            "desc": "Convert Word documents (DOC/DOCX) to PDF.",
            "route": "/word-to-pdf",
            "icon_bg": "#dbeafe",
            "icon_color": "#2563eb",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none"><rect x="3" y="2" width="18" height="20" rx="2" stroke="#2563eb" stroke-width="1.8"/><text x="12" y="15" text-anchor="middle" font-size="8" font-weight="700" fill="#2563eb" font-family="Arial,sans-serif">W</text></svg>',
        },
        {
            "name": "Edit PDF",
            "desc": "Add text, images, shapes and annotations to your PDF.",
            "route": "/edit-pdf",
            "icon_bg": "#f0f9ff",
            "icon_color": "#0284c7",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#0284c7" stroke-width="1.8"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke-linecap="round" stroke-linejoin="round"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        },
    ]

    def hex_to_rgba(hex_code: str, alpha: float = 0.18) -> str:
        h = hex_code.lstrip("#")
        if len(h) == 6:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            return f"rgba({r}, {g}, {b}, {alpha})"
        return hex_code

    # Build cards HTML
    cards_html = ""
    for tool in tools:
        dark_bg = hex_to_rgba(tool.get("icon_color", "#0284c7"), 0.18)
        cards_html += f'''
        <a href="{tool['route']}" class="pdf-tool-card" style="text-decoration:none;">
          <div class="pdf-tool-icon" style="--icon-bg:{tool['icon_bg']}; --icon-dark-bg:{dark_bg};">
            {tool['icon_svg']}
          </div>
          <h3 class="pdf-tool-name">{tool['name']}</h3>
          <p class="pdf-tool-desc">{tool['desc']}</p>
          <div class="pdf-tool-arrow">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
            </svg>
          </div>
        </a>
        '''

    main_card_html = f'''
    <div class="pdf-tools-grid">
      {cards_html}
    </div>
    '''

    extra_css = r"""
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

    /* Grid Layout: Desktop (width > 1200px) -> exactly 7 cards */
    .pdf-tools-grid {
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
      .pdf-tools-grid {
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
      }
    }

    /* Mobile (width < 768px) -> exactly 2 cards */
    @media (max-width: 767px) {
      .app-main-content-area {
        padding: 16px 12px 40px !important;
      }
      .pdf-tools-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
      }
    }

    .pdf-tool-card {
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

    .pdf-tool-card:hover {
      border-color: #bae6fd;
      transform: translateY(-3px);
      box-shadow: 0 10px 24px rgba(2, 132, 199, 0.12);
    }

    .pdf-tool-icon {
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

    html.dark-mode .pdf-tool-icon,
    body.dark-mode .pdf-tool-icon,
    [data-theme="dark"] .pdf-tool-icon {
      background: var(--icon-dark-bg) !important;
    }

    .pdf-tool-icon svg {
      width: 22px;
      height: 22px;
    }

    .pdf-tool-name {
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

    .pdf-tool-desc {
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

    .pdf-tool-arrow {
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

    .pdf-tool-card:hover .pdf-tool-arrow {
      background: #0284c7;
      border-color: #0284c7;
      color: #ffffff;
      transform: translateX(3px);
    }

    /* Dark Mode (Supports html.dark-mode, body.dark-mode, [data-theme="dark"]) */
    html.dark-mode .pdf-tool-card,
    body.dark-mode .pdf-tool-card,
    [data-theme="dark"] .pdf-tool-card {
      background: #1e293b !important;
      border-color: #334155 !important;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
    }
    html.dark-mode .pdf-tool-card:hover,
    body.dark-mode .pdf-tool-card:hover,
    [data-theme="dark"] .pdf-tool-card:hover {
      border-color: #38bdf8 !important;
      background: #1e293b !important;
      box-shadow: 0 10px 24px rgba(56, 189, 248, 0.15);
    }
    html.dark-mode .pdf-tool-name,
    body.dark-mode .pdf-tool-name,
    [data-theme="dark"] .pdf-tool-name {
      color: #f1f5f9 !important;
    }
    html.dark-mode .pdf-tool-desc,
    body.dark-mode .pdf-tool-desc,
    [data-theme="dark"] .pdf-tool-desc {
      color: #94a3b8 !important;
    }
    html.dark-mode .pdf-tool-arrow,
    body.dark-mode .pdf-tool-arrow,
    [data-theme="dark"] .pdf-tool-arrow {
      background: #0f172a !important;
      border-color: #334155 !important;
      color: #64748b !important;
    }
    """

    return render_layout(
        title="PDF Tools",
        active_tool="pdf-tools",
        hero_title="PDF Tools",
        hero_sub="All-in-one PDF tools to convert, merge, split, edit and more. <strong>Fast, secure and free</strong> to use.",
        main_card_html=main_card_html,
        extra_css=extra_css,
    )
