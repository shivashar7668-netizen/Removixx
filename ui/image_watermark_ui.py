"""
Removix UI - Image Watermark Removal View
----------------------------------------
Contains UI template and client-side logic for AI Image Watermark removal.
"""

from modules.ui_template import PAGE as BASE_PAGE

def render_image_watermark_page() -> str:
    """Renders the Image Watermark Removal interface."""
    page = BASE_PAGE
    # Set active sidebar item to image-tools
    page = page.replace('class="sidebar-nav-link active" data-tool="video-tools"', 'class="sidebar-nav-link" data-tool="video-tools"')
    page = page.replace('class="sidebar-nav-link" data-tool="image-tools"', 'class="sidebar-nav-link active" data-tool="image-tools"')
    
    # Update Hero Text
    page = page.replace('<h1>Removix Watermark Remover</h1>', '<h1>Image Watermark Remover</h1>')
    page = page.replace('Drop any AI <strong>video or image</strong> and the watermark is gone in seconds — every frame, original quality, ready to post.',
                        'Drop any AI generated <strong>image</strong> and remove watermarks instantly with deep neural LaMa reconstruction.')
    
    # Update Dropzone Text
    page = page.replace('id="drop-primary-text">Drop your video or image here, or browse</p>',
                        'id="drop-primary-text">Drop your image here, or browse</p>')
    page = page.replace('id="drop-secondary-text">Supports MP4, MOV, WebM, MKV, PNG, JPG, WEBP • Max 4K resolution</p>',
                        'id="drop-secondary-text">Supports PNG, JPG, JPEG, WEBP • Lossless quality</p>')
    
    # Pre-select image mode on load
    page = page.replace("let currentMode = 'video';", "let currentMode = 'image';")
    page = page.replace("accept=\".mp4,.mov,.m4v,.webm,.mkv,.avi,.flv,.png,.jpg,.jpeg,.webp\"", "accept=\".png,.jpg,.jpeg,.webp\"")
    page = page.replace("Clean Another File", "Clean Another Image")
    
    return page
