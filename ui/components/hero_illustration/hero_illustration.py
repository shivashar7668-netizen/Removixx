"""
Removix UI - Hero Banner Animated SVG Illustration Component
-----------------------------------------------------------
Dedicated component for embedding and responsively styling the self-animating SMIL SVG illustration:
"Young_man_with_red_shirt_at_a_computer.svg".
Requires zero external JS libraries (no lottie-web / lottie-react).
"""

from pathlib import Path

_COMPONENT_DIR = Path(__file__).parent
_SVG_FILE_PATH = _COMPONENT_DIR / "Young_man_with_red_shirt_at_a_computer.svg"

# Cached in-memory SVG string
_CACHED_SVG_CONTENT = None

def get_hero_svg_content() -> str:
    """Reads and returns the self-animating SVG XML string."""
    global _CACHED_SVG_CONTENT
    if _CACHED_SVG_CONTENT is None:
        try:
            if _SVG_FILE_PATH.exists():
                with open(_SVG_FILE_PATH, "r", encoding="utf-8", errors="ignore") as f:
                    _CACHED_SVG_CONTENT = f.read().strip()
            else:
                _CACHED_SVG_CONTENT = ""
        except Exception:
            _CACHED_SVG_CONTENT = ""
    return _CACHED_SVG_CONTENT

HERO_ILLUSTRATION_CSS = r"""
/* ========== HERO BANNER ANIMATED SVG ILLUSTRATION ========== */
.hero-svg-wrapper {
  flex: 1;
  max-width: 480px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  min-height: 220px;
}

.hero-svg-container {
  width: 100%;
  max-width: 460px;
  height: auto;
  aspect-ratio: 1330 / 920;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  filter: drop-shadow(0 14px 28px rgba(2, 132, 199, 0.14));
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), filter 0.3s ease;
}

.hero-svg-container:hover {
  transform: scale(1.02);
}

body.dark-mode .hero-svg-container,
[data-theme="dark"] .hero-svg-container {
  filter: drop-shadow(0 16px 34px rgba(14, 165, 233, 0.20));
}

.hero-svg-container svg {
  width: 100% !important;
  height: 100% !important;
  display: block;
  max-width: 100%;
  height: auto;
  overflow: visible;
}

/* Tablet (max-width: 1100px): Proportional scale */
@media (max-width: 1100px) {
  .hero-svg-wrapper {
    max-width: 380px;
    min-height: 190px;
  }
  .hero-svg-container {
    max-width: 350px;
  }
}

@media (max-width: 900px) {
  .hero-svg-wrapper {
    max-width: 320px;
    min-height: 170px;
  }
  .hero-svg-container {
    max-width: 290px;
  }
}

/* Mobile (max-width: 768px): Stack layout with centered animation */
@media (max-width: 768px) {
  .home-banner-card {
    flex-direction: column !important;
    padding: 28px 20px 24px !important;
    text-align: center;
    gap: 20px !important;
  }
  .banner-left {
    max-width: 100% !important;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .banner-heading {
    font-size: clamp(24px, 5.8vw, 32px) !important;
  }
  .banner-subtext {
    font-size: 13.5px !important;
    max-width: 480px;
    margin: 0 auto;
  }
  .hero-svg-wrapper {
    max-width: 320px;
    width: 100%;
    margin: 0 auto;
    min-height: 180px;
  }
  .hero-svg-container {
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .home-banner-card {
    padding: 22px 14px 20px !important;
    gap: 16px !important;
  }
  .hero-svg-wrapper {
    max-width: 270px;
    min-height: 150px;
  }
  .hero-svg-container {
    max-width: 250px;
  }
}
"""

def render_hero_illustration() -> dict:
    """
    Renders the hero animated SVG illustration component.
    Returns:
        dict: {
            "html": container HTML with embedded self-animating SVG,
            "css": responsive component CSS
        }
    """
    svg_markup = get_hero_svg_content()
    html = f"""<div class="hero-svg-wrapper" id="heroSvgWrapper">
  <div class="hero-svg-container" id="heroSvgContainer" aria-label="Animated illustration of young man at computer">
    {svg_markup}
  </div>
</div>"""
    return {
        "html": html,
        "css": HERO_ILLUSTRATION_CSS,
    }
