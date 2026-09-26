"""
Removix UI Package
------------------
Clean modular frontend layouts, views, and components.
"""

from ui.layout import render_layout, render_processing_component
from ui.sidebar import render_top_bar_html, render_sidebar_html
from ui.home_ui import render_home_page
from ui.video_watermark_ui import render_video_watermark_page
from ui.image_watermark_ui import render_image_watermark_page
from ui.pdf_tools_ui import render_image_to_pdf_page, render_pdf_to_image_page
from ui.pdf_tools_grid_ui import render_pdf_tools_grid_page
from ui.merge_pdf_ui import render_merge_pdf_page
from ui.split_pdf_ui import render_split_pdf_page
from ui.rotate_pdf_ui import render_rotate_pdf_page
from ui.delete_pages_ui import render_delete_pages_page
from ui.protect_pdf_ui import render_protect_pdf_page
from ui.unlock_pdf_ui import render_unlock_pdf_page
from ui.word_to_pdf_ui import render_word_to_pdf_page
from ui.edit_pdf_ui import render_edit_pdf_page
from ui.converter_ui import render_converter_page
from ui.qr_ui import render_qr_page
from ui.ocr_ui import render_ocr_page
from ui.bg_remove_ui import render_bg_remove_page
from ui.more_tools_ui import render_more_tools_page

# Image Tools Hub & Views
from ui.image_tools_grid_ui import render_image_tools_grid_page
from ui.png_to_jpg_ui import render_png_to_jpg_page
from ui.jpg_to_png_ui import render_jpg_to_png_page
from ui.webp_to_jpg_ui import render_webp_to_jpg_page
from ui.jpg_to_webp_ui import render_jpg_to_webp_page
from ui.png_to_webp_ui import render_png_to_webp_page
from ui.webp_to_png_ui import render_webp_to_png_page
from ui.png_to_svg_ui import render_png_to_svg_page
from ui.jpg_to_svg_ui import render_jpg_to_svg_page
from ui.svg_to_png_ui import render_svg_to_png_page
from ui.jpg_to_gif_ui import render_jpg_to_gif_page
from ui.gif_to_jpg_ui import render_gif_to_jpg_page
from ui.png_to_gif_ui import render_png_to_gif_page
from ui.gif_to_png_ui import render_gif_to_png_page
from ui.jpg_to_tiff_ui import render_jpg_to_tiff_page
from ui.tiff_to_jpg_ui import render_tiff_to_jpg_page
from ui.png_to_tiff_ui import render_png_to_tiff_page
from ui.tiff_to_png_ui import render_tiff_to_png_page
from ui.resize_image_ui import render_resize_image_page
from ui.crop_image_ui import render_crop_image_page
from ui.compress_image_ui import render_compress_image_page
from ui.flip_image_ui import render_flip_image_page
from ui.black_white_ui import render_black_white_page
from ui.add_text_image_ui import render_add_text_image_page
from ui.make_round_image_ui import render_make_round_image_page
from ui.blur_background_ui import render_blur_background_page
from ui.collage_maker_ui import render_collage_maker_page
from ui.upscale_image_ui import render_upscale_image_page
from ui.profile_ui import render_profile_view
from ui.info_pages_ui import (
    render_privacy_page,
    render_faq_page,
    render_contact_page,
    render_about_page,
)
from ui.layout import FOOTER_HTML, FOOTER_CSS
