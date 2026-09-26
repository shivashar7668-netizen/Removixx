"""
Removix UI - Premium Banner Animated Laptop SVG Illustration Component
----------------------------------------------------------------------
Dedicated component for embedding and styling the self-animating SMIL SVG:
"laptop.svg".
Renders within the Premium banner illustration container, aligned with
the floating tool cards (Image, PDF, Video, AI/OCR).
"""

from pathlib import Path
import re

_COMPONENT_DIR = Path(__file__).parent
_SVG_FILE_PATH = _COMPONENT_DIR / "laptop.svg"

# Cached in-memory SVG string and inner markup
_CACHED_RAW_SVG = None
_CACHED_INNER_SVG = None


def get_laptop_svg_raw() -> str:
    """Reads and returns the complete laptop.svg XML string."""
    global _CACHED_RAW_SVG
    if _CACHED_RAW_SVG is None:
        try:
            if _SVG_FILE_PATH.exists():
                with open(_SVG_FILE_PATH, "r", encoding="utf-8", errors="ignore") as f:
                    _CACHED_RAW_SVG = f.read().strip()
            else:
                _CACHED_RAW_SVG = ""
        except Exception:
            _CACHED_RAW_SVG = ""
    return _CACHED_RAW_SVG


def get_laptop_svg_inner() -> str:
    """Extracts and returns the inner content of laptop.svg between <svg ...> and </svg>."""
    global _CACHED_INNER_SVG
    if _CACHED_INNER_SVG is None:
        raw = get_laptop_svg_raw()
        if raw:
            # Strip outer <svg ...> and </svg>
            inner = re.sub(r"^<svg[^>]*>", "", raw, flags=re.IGNORECASE)
            inner = re.sub(r"</svg>$", "", inner, flags=re.IGNORECASE).strip()
            _CACHED_INNER_SVG = inner
        else:
            _CACHED_INNER_SVG = ""
    return _CACHED_INNER_SVG


def render_premium_laptop_svg_node(x: int = 50, y: int = 95, width: int = 420, height: int = 244) -> str:
    """
    Renders the animated laptop as a nested SVG viewport node matching
    the Premium banner coordinate system (0 0 520 380).
    Trimmed viewBox (0 130 500 290) perfectly frames the animated laptop
    and its screen popup, sitting cleanly below the floating badges.
    """
    inner = get_laptop_svg_inner()
    return f"""<!-- Animated Laptop Illustration (SMIL Animated SVG) -->
<svg class="premium-laptop-animated-svg" x="{x}" y="{y}" width="{width}" height="{height}" viewBox="0 130 500 290" preserveAspectRatio="xMidYMid meet" filter="url(#premDropShadow)">
  {inner}
</svg>"""

