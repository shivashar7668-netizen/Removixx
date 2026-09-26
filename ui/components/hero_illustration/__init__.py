"""
Removix Hero Illustration Component Package
-------------------------------------------
Dedicated package for the hero banner animated SVG illustration.
"""

from .hero_illustration import (
    render_hero_illustration,
    get_hero_svg_content,
    HERO_ILLUSTRATION_CSS,
)

__all__ = [
    "render_hero_illustration",
    "get_hero_svg_content",
    "HERO_ILLUSTRATION_CSS",
]
