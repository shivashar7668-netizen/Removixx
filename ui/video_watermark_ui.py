"""
Removix UI - Video Watermark Removal View
----------------------------------------
Contains UI template and client-side logic for AI Video Watermark removal.
"""

from modules.ui_template import PAGE as BASE_PAGE

def render_video_watermark_page() -> str:
    """Renders the Video Watermark Removal interface."""
    # Ensure sidebar active state is 'video-watermark'
    page = BASE_PAGE.replace('data-tool="video-watermark" class="sidebar-item"', 'data-tool="video-watermark" class="sidebar-item active"')
    return page
