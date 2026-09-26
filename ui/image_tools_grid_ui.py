"""
Removix UI - Image Tools Grid Page
----------------------------------
Displays a modern, fully responsive card grid of all 29 Image tools:
- AI & Enhancement (Remove Background, Remove Watermark, Upscale Image, Blur Background)
- Creative & Editing (Resize, Crop, Compress, Flip, Black & White, Add Text, Make Round, Collage Maker)
- Format Converters (PNG, JPG, WEBP, SVG, GIF, TIFF bidirectional conversions)
Each card links directly to its specialized tool page.
"""

from ui.layout import render_layout


def render_image_tools_grid_page() -> str:
    """Renders the Image Tools hub grid with 29 tool cards."""

    tools = [
        # AI & Core Tools
        {
            "name": "Remove Background",
            "desc": "Instantly isolate portraits and objects with transparent PNG cutout.",
            "route": "/bg-remove",
            "icon_bg": "#e0f2fe",
            "icon_color": "#0284c7",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#0284c7" stroke-width="1.8"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12" stroke-linecap="round"/></svg>',
        },
        {
            "name": "Remove Watermark",
            "desc": "Erase logos, stamps, and watermarks with deep neural reconstruction.",
            "route": "/image-watermark",
            "icon_bg": "#fee2e2",
            "icon_color": "#dc2626",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#dc2626" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="3" stroke-linecap="round"/><circle cx="8.5" cy="8.5" r="1.5" fill="#dc2626" stroke="none"/><path d="M21 15l-5-5L5 21" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        },
        {
            "name": "Upscale Image",
            "desc": "Double image resolution (2x) with high-clarity edge enhancement.",
            "route": "/upscale-image",
            "icon_bg": "#fef9c3",
            "icon_color": "#ca8a04",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#ca8a04" stroke-width="1.8"><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/><path d="M21 14v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5"/></svg>',
        },
        {
            "name": "Blur Background",
            "desc": "Keep the subject razor-sharp while softly blurring the background.",
            "route": "/blur-background",
            "icon_bg": "#fae8ff",
            "icon_color": "#a855f7",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#a855f7" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2"/></svg>',
        },

        # Editing & Adjustments
        {
            "name": "Resize Image",
            "desc": "Change dimensions by exact pixels or percentage with aspect ratio lock.",
            "route": "/resize-image",
            "icon_bg": "#dbeafe",
            "icon_color": "#2563eb",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#2563eb" stroke-width="1.8"><polyline points="4 14 10 14 10 20"/><polyline points="20 10 14 10 14 4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/></svg>',
        },
        {
            "name": "Crop Image",
            "desc": "Trim unwanted edges or crop to popular social media aspect ratios.",
            "route": "/crop-image",
            "icon_bg": "#d1fae5",
            "icon_color": "#059669",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#059669" stroke-width="1.8"><path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/></svg>',
        },
        {
            "name": "Compress Image",
            "desc": "Dramatically shrink file size while preserving high visual quality.",
            "route": "/compress-image",
            "icon_bg": "#ffedd5",
            "icon_color": "#ea580c",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#ea580c" stroke-width="1.8"><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/></svg>',
        },
        {
            "name": "Flip Image",
            "desc": "Mirror pictures horizontally or invert them vertically with ease.",
            "route": "/flip-image",
            "icon_bg": "#f1f5f9",
            "icon_color": "#475569",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#475569" stroke-width="1.8"><path d="M12 2v20"/><polyline points="4 8 8 12 4 16"/><polyline points="20 8 16 12 20 16"/></svg>',
        },
        {
            "name": "Black & White",
            "desc": "Convert vibrant photos into timeless monochrome with deep contrast.",
            "route": "/black-white",
            "icon_bg": "#f3e8ff",
            "icon_color": "#7e22ce",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#7e22ce" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="#7e22ce"/></svg>',
        },
        {
            "name": "Add Text to Image",
            "desc": "Overlay custom captions, watermarks, and typography onto images.",
            "route": "/add-text-image",
            "icon_bg": "#e0e7ff",
            "icon_color": "#4338ca",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#4338ca" stroke-width="1.8"><path d="M4 7V4h16v3"/><line x1="12" y1="4" x2="12" y2="20"/><line x1="8" y1="20" x2="16" y2="20"/></svg>',
        },
        {
            "name": "Make Round Image",
            "desc": "Crop photos into perfect circles with transparent outer borders.",
            "route": "/make-round-image",
            "icon_bg": "#ccfbf1",
            "icon_color": "#0f766e",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#0f766e" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5" stroke-dasharray="2 2"/></svg>',
        },
        {
            "name": "Collage Maker",
            "desc": "Combine multiple photos into neat side-by-side or 2x2 grid collages.",
            "route": "/collage-maker",
            "icon_bg": "#fce7f3",
            "icon_color": "#be185d",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#be185d" stroke-width="1.8"><rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/></svg>',
        },

        # Popular Format Converters
        {
            "name": "PNG to JPG",
            "desc": "Convert transparent PNGs into optimized JPG photos with white fill.",
            "route": "/png-to-jpg",
            "icon_bg": "#fee2e2",
            "icon_color": "#ef4444",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#ef4444" stroke-width="1.8"><path d="M7 16l-4-4m0 0l4-4m-4 4h18"/><rect x="14" y="5" width="8" height="14" rx="2"/></svg>',
        },
        {
            "name": "JPG to PNG",
            "desc": "Transform JPG images into lossless PNG format with zero degradation.",
            "route": "/jpg-to-png",
            "icon_bg": "#dbeafe",
            "icon_color": "#3b82f6",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#3b82f6" stroke-width="1.8"><path d="M17 8l4 4m0 0l-4 4m4-4H3"/><rect x="2" y="5" width="8" height="14" rx="2"/></svg>',
        },
        {
            "name": "WEBP to JPG",
            "desc": "Convert modern WebP images to widely compatible JPG format.",
            "route": "/webp-to-jpg",
            "icon_bg": "#ffedd5",
            "icon_color": "#f97316",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#f97316" stroke-width="1.8"><path d="M7 16l-4-4m0 0l4-4m-4 4h18"/><circle cx="17" cy="12" r="4"/></svg>',
        },
        {
            "name": "JPG to WEBP",
            "desc": "Compress JPG photos into next-gen lightweight WebP files.",
            "route": "/jpg-to-webp",
            "icon_bg": "#d1fae5",
            "icon_color": "#10b981",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#10b981" stroke-width="1.8"><path d="M17 8l4 4m0 0l-4 4m4-4H3"/><circle cx="7" cy="12" r="4"/></svg>',
        },
        {
            "name": "PNG to WEBP",
            "desc": "Convert PNG to WebP while retaining full alpha transparency.",
            "route": "/png-to-webp",
            "icon_bg": "#e0f2fe",
            "icon_color": "#0ea5e9",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#0ea5e9" stroke-width="1.8"><path d="M17 8l4 4m0 0l-4 4m4-4H3"/><polygon points="6 6 10 12 6 18"/></svg>',
        },
        {
            "name": "WEBP to PNG",
            "desc": "Convert WebP graphics into standard PNGs with transparent layers.",
            "route": "/webp-to-png",
            "icon_bg": "#fae8ff",
            "icon_color": "#d946ef",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#d946ef" stroke-width="1.8"><path d="M7 16l-4-4m0 0l4-4m-4 4h18"/><polygon points="18 6 14 12 18 18"/></svg>',
        },
        {
            "name": "PNG to SVG",
            "desc": "Vectorize or embed PNG graphics into infinitely scalable SVG code.",
            "route": "/png-to-svg",
            "icon_bg": "#fef9c3",
            "icon_color": "#eab308",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#eab308" stroke-width="1.8"><path d="M4 12v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-6"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>',
        },
        {
            "name": "JPG to SVG",
            "desc": "Convert raster JPG pictures into resolution-independent SVG files.",
            "route": "/jpg-to-svg",
            "icon_bg": "#ffedd5",
            "icon_color": "#c2410c",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#c2410c" stroke-width="1.8"><polygon points="12 2 2 22 22 22"/></svg>',
        },
        {
            "name": "SVG to PNG",
            "desc": "Render crisp vector SVG graphics into high-resolution raster PNGs.",
            "route": "/svg-to-png",
            "icon_bg": "#dbeafe",
            "icon_color": "#1d4ed8",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#1d4ed8" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',
        },
        {
            "name": "JPG to GIF",
            "desc": "Convert JPG still pictures into compact GIF format.",
            "route": "/jpg-to-gif",
            "icon_bg": "#ccfbf1",
            "icon_color": "#14b8a6",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#14b8a6" stroke-width="1.8"><rect x="2" y="6" width="20" height="12" rx="2"/><line x1="6" y1="12" x2="6.01" y2="12"/><line x1="10" y1="12" x2="14" y2="12"/><line x1="18" y1="12" x2="18.01" y2="12"/></svg>',
        },
        {
            "name": "GIF to JPG",
            "desc": "Extract and save GIF animations or frames as clear JPG photos.",
            "route": "/gif-to-jpg",
            "icon_bg": "#fee2e2",
            "icon_color": "#b91c1c",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#b91c1c" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M10 9l5 3-5 3z" fill="#b91c1c"/></svg>',
        },
        {
            "name": "PNG to GIF",
            "desc": "Convert PNG designs into lightweight web-ready GIF files.",
            "route": "/png-to-gif",
            "icon_bg": "#fce7f3",
            "icon_color": "#db2777",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#db2777" stroke-width="1.8"><path d="M4 16l4-8 4 6 3-3 5 5"/><rect x="2" y="4" width="20" height="16" rx="2"/></svg>',
        },
        {
            "name": "GIF to PNG",
            "desc": "Convert GIF images to crisp lossless PNG format with transparent alpha.",
            "route": "/gif-to-png",
            "icon_bg": "#e0e7ff",
            "icon_color": "#6366f1",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#6366f1" stroke-width="1.8"><circle cx="8" cy="8" r="2"/><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M3 16l6-6 4 4 5-5 3 3"/></svg>',
        },
        {
            "name": "JPG to TIFF",
            "desc": "Convert JPG photographs to archival-grade uncompressed TIFF format.",
            "route": "/jpg-to-tiff",
            "icon_bg": "#fef3c7",
            "icon_color": "#d97706",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#d97706" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/></svg>',
        },
        {
            "name": "TIFF to JPG",
            "desc": "Convert massive TIFF camera scans into web-friendly JPG files.",
            "route": "/tiff-to-jpg",
            "icon_bg": "#e2e8f0",
            "icon_color": "#334155",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#334155" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 16l4-4 4 4"/></svg>',
        },
        {
            "name": "PNG to TIFF",
            "desc": "Export transparent PNG graphics to high-fidelity printing TIFFs.",
            "route": "/png-to-tiff",
            "icon_bg": "#ecfdf5",
            "icon_color": "#047857",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#047857" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><line x1="9" y1="15" x2="15" y2="15"/></svg>',
        },
        {
            "name": "TIFF to PNG",
            "desc": "Convert TIFF scans into high-compatibility PNG format.",
            "route": "/tiff-to-png",
            "icon_bg": "#e0f2fe",
            "icon_color": "#0369a1",
            "icon_svg": '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#0369a1" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8" cy="8" r="1.5"/></svg>',
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
        <a href="{tool['route']}" class="image-tool-card" style="text-decoration:none;">
          <div class="image-tool-icon" style="--icon-bg:{tool['icon_bg']}; --icon-dark-bg:{dark_bg};">
            {tool['icon_svg']}
          </div>
          <h3 class="image-tool-name">{tool['name']}</h3>
          <p class="image-tool-desc">{tool['desc']}</p>
          <div class="image-tool-arrow">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
            </svg>
          </div>
        </a>
        '''

    main_card_html = f'''
    <div class="image-tools-grid">
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
    .image-tools-grid {
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
      .image-tools-grid {
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
      }
    }

    /* Mobile (width < 768px) -> exactly 2 cards */
    @media (max-width: 767px) {
      .app-main-content-area {
        padding: 16px 12px 40px !important;
      }
      .image-tools-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
      }
    }

    .image-tool-card {
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

    .image-tool-card:hover {
      border-color: #bae6fd;
      transform: translateY(-3px);
      box-shadow: 0 10px 24px rgba(2, 132, 199, 0.12);
    }

    .image-tool-icon {
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

    html.dark-mode .image-tool-icon,
    body.dark-mode .image-tool-icon,
    [data-theme="dark"] .image-tool-icon {
      background: var(--icon-dark-bg) !important;
    }

    .image-tool-icon svg {
      width: 22px;
      height: 22px;
    }

    .image-tool-name {
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

    .image-tool-desc {
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

    .image-tool-arrow {
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

    .image-tool-card:hover .image-tool-arrow {
      background: #0284c7;
      border-color: #0284c7;
      color: #ffffff;
      transform: translateX(3px);
    }

    /* Dark Mode (Supports html.dark-mode, body.dark-mode, [data-theme="dark"]) */
    html.dark-mode .image-tool-card,
    body.dark-mode .image-tool-card,
    [data-theme="dark"] .image-tool-card {
      background: #1e293b !important;
      border-color: #334155 !important;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
    }
    html.dark-mode .image-tool-card:hover,
    body.dark-mode .image-tool-card:hover,
    [data-theme="dark"] .image-tool-card:hover {
      border-color: #38bdf8 !important;
      background: #1e293b !important;
      box-shadow: 0 10px 24px rgba(56, 189, 248, 0.15);
    }
    html.dark-mode .image-tool-name,
    body.dark-mode .image-tool-name,
    [data-theme="dark"] .image-tool-name {
      color: #f1f5f9 !important;
    }
    html.dark-mode .image-tool-desc,
    body.dark-mode .image-tool-desc,
    [data-theme="dark"] .image-tool-desc {
      color: #94a3b8 !important;
    }
    html.dark-mode .image-tool-arrow,
    body.dark-mode .image-tool-arrow,
    [data-theme="dark"] .image-tool-arrow {
      background: #0f172a !important;
      border-color: #334155 !important;
      color: #64748b !important;
    }
    """

    return render_layout(
        title="Image Tools",
        active_tool="image-tools",
        hero_title="Image Tools",
        hero_sub="All-in-one suite to convert, resize, crop, enhance, and edit images. <strong>Fast, private, and free</strong>.",
        main_card_html=main_card_html,
        extra_css=extra_css,
    )
