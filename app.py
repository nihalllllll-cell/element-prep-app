import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont, ImageOps
from rembg import remove
import io
import numpy as np
from typing import Tuple
import gc

# Page config with custom theme
st.set_page_config(
    page_title="Hania, Don't Crash Out",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetic UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
    }
    
    .title-container {
        text-align: center;
        padding: 3rem 2rem 2rem 2rem;
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        margin-bottom: 2.5rem;
        border: 2px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .title-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .title-text {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #ffd1dc 50%, #fff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -2px;
        text-shadow: 0 2px 20px rgba(255, 255, 255, 0.3);
        animation: float 3s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .subtitle-text {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.15rem;
        margin-top: 0.8rem;
        font-weight: 300;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.15rem;
        font-weight: 600;
        border-radius: 15px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 35px rgba(102, 126, 234, 0.7),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.15rem;
        font-weight: 600;
        border-radius: 15px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 6px 25px rgba(245, 87, 108, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 35px rgba(245, 87, 108, 0.7),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '💜';
        position: absolute;
        font-size: 6rem;
        opacity: 0.05;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        animation: heartbeat 2s ease-in-out infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: translate(-50%, -50%) scale(1); }
        50% { transform: translate(-50%, -50%) scale(1.1); }
    }
    
    .footer-text {
        color: white;
        font-size: 1.3rem;
        font-weight: 500;
        letter-spacing: 1px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
    }
    
    .stCheckbox {
        background: rgba(255, 255, 255, 0.12);
        padding: 0.7rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .stCheckbox:hover {
        background: rgba(255, 255, 255, 0.18);
        transform: translateX(3px);
    }
    
    .stCheckbox label {
        color: white !important;
        font-weight: 500;
    }
    
    .uploadedFile {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    div[data-testid="stImage"] {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3),
                    0 0 0 1px rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stImage"]:hover {
        transform: scale(1.01);
        box-shadow: 0 16px 50px rgba(0, 0, 0, 0.4),
                    0 0 0 1px rgba(255, 255, 255, 0.2);
    }
    
    .stSlider {
        padding: 1.2rem 0;
    }
    
    .stSlider > label {
        color: white !important;
        font-weight: 500;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    .stSlider [data-baseweb="slider"] {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stSelectbox {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.98) 0%, rgba(118, 75, 162, 0.98) 100%);
        backdrop-filter: blur(20px);
        border-right: 2px solid rgba(255, 255, 255, 0.15);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        color: white;
        font-weight: 700;
        font-size: 1.4rem;
        margin-top: 1.5rem;
        margin-bottom: 1.2rem;
        padding-bottom: 0.7rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.35);
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
        font-weight: 600;
        font-size: 1rem;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] {
        gap: 0.7rem;
    }
    
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(10px);
        padding: 0.9rem 1.2rem;
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.25);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        color: white !important;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.28);
        transform: translateX(5px) scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    [data-testid="stSidebar"] .stSelectbox > label {
        color: white !important;
        font-weight: 600;
        font-size: 1rem;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.18);
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"]:hover {
        background: rgba(255, 255, 255, 0.25);
        border-color: rgba(255, 255, 255, 0.35);
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3);
        margin: 2rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: rgba(255, 255, 255, 0.2);
    }
    
    .success-message {
        background: rgba(76, 175, 80, 0.25);
        border-left: 5px solid #4CAF50;
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .info-box {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1.5rem 0;
        border: 2px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .preset-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid rgba(255, 255, 255, 0.3);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .preset-card:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def optimize_image_for_processing(image: Image.Image, max_dimension: int = 4096) -> Tuple[Image.Image, float]:
    """Optimize image size for processing if too large, return scale factor"""
    width, height = image.size
    max_current = max(width, height)
    
    if max_current > max_dimension:
        scale = max_dimension / max_current
        new_size = (int(width * scale), int(height * scale))
        return image.resize(new_size, Image.Resampling.LANCZOS), scale
    return image, 1.0

def restore_original_scale(image: Image.Image, original_size: Tuple[int, int]) -> Image.Image:
    """Restore image to original dimensions if it was scaled down"""
    if image.size != original_size:
        return image.resize(original_size, Image.Resampling.LANCZOS)
    return image

def add_shadow(image: Image.Image, offset: Tuple[int, int] = (5, 5), 
               blur: int = 10, opacity: int = 128) -> Image.Image:
    """Add drop shadow to image with transparency"""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Create shadow layer
    shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    
    # Get alpha channel
    alpha = image.split()[3]
    shadow.paste(Image.new('RGBA', image.size, (0, 0, 0, opacity)), mask=alpha)
    
    # Blur shadow
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    
    # Create new image with shadow
    total_size = (image.size[0] + abs(offset[0]) + blur * 2,
                  image.size[1] + abs(offset[1]) + blur * 2)
    result = Image.new('RGBA', total_size, (0, 0, 0, 0))
    
    shadow_pos = (blur + max(0, offset[0]), blur + max(0, offset[1]))
    image_pos = (blur + max(0, -offset[0]), blur + max(0, -offset[1]))
    
    result.paste(shadow, shadow_pos)
    result.paste(image, image_pos, image)
    
    return result

def add_padding(image: Image.Image, padding: int, color=(0, 0, 0, 0)) -> Image.Image:
    """Add padding around image"""
    new_size = (image.size[0] + 2 * padding, image.size[1] + 2 * padding)
    result = Image.new(image.mode, new_size, color)
    result.paste(image, (padding, padding))
    return result

def auto_crop_transparent(image: Image.Image, margin: int = 0) -> Image.Image:
    """Auto-crop image to content with optional margin"""
    if image.mode != 'RGBA':
        return image
    
    # Get bounding box of non-transparent pixels
    bbox = image.getbbox()
    if bbox:
        # Add margin
        bbox = (max(0, bbox[0] - margin),
                max(0, bbox[1] - margin),
                min(image.size[0], bbox[2] + margin),
                min(image.size[1], bbox[3] + margin))
        return image.crop(bbox)
    return image

def smart_upscale(image: Image.Image, factor: int, quality_mode: str = "balanced") -> Image.Image:
    """Ultra-advanced upscaling with multiple quality modes and AI-like techniques"""
    if factor == 1:
        return image
    
    # Check if image is too large for upscaling
    current_pixels = image.size[0] * image.size[1]
    target_pixels = current_pixels * (factor ** 2)
    max_pixels = 178_956_970  # PIL max pixel limit
    
    if target_pixels > max_pixels:
        safe_factor = int((max_pixels / current_pixels) ** 0.5)
        st.warning(f"⚠️ Image too large for {factor}x upscale. Using maximum safe factor: {safe_factor}x")
        factor = max(safe_factor, 1)
        if factor == 1:
            return image
    
    current_img = image.copy()
    remaining_factor = float(factor)
    
    # Quality mode settings
    if quality_mode == "maximum":
        sharpen_per_pass = 1.3
        final_sharpen = 1.8
        use_unsharp = True
        passes = 3 if factor > 2 else 2
    elif quality_mode == "balanced":
        sharpen_per_pass = 1.2
        final_sharpen = 1.4
        use_unsharp = True
        passes = 2
    else:  # fast
        sharpen_per_pass = 1.1
        final_sharpen = 1.2
        use_unsharp = False
        passes = 1
    
    pass_count = 0
    
    while remaining_factor > 1.01:
        # Calculate step factor
        if remaining_factor >= 4 and passes > 2:
            step_factor = 2.0
        elif remaining_factor >= 2:
            step_factor = 2.0
        else:
            step_factor = remaining_factor
        
        new_size = (
            int(current_img.size[0] * step_factor),
            int(current_img.size[1] * step_factor)
        )
        
        if new_size[0] * new_size[1] > max_pixels:
            st.warning("⚠️ Reached maximum image size limit")
            break
        
        # Pre-sharpening to preserve details before upscale
        if quality_mode in ["balanced", "maximum"] and pass_count > 0:
            current_img = advanced_sharpen(current_img, 1.1)
        
        # Upscale using LANCZOS
        current_img = current_img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Post-processing after upscale
        if remaining_factor > 1.5:
            # Apply sharpening
            current_img = advanced_sharpen(current_img, sharpen_per_pass)
            
            # Apply subtle edge enhancement for crispness
            if quality_mode == "maximum":
                enhanced = current_img.filter(ImageFilter.EDGE_ENHANCE)
                current_img = Image.blend(current_img, enhanced, 0.15)
        
        remaining_factor = remaining_factor / step_factor
        pass_count += 1
        gc.collect()
    
    # Final quality pass
    if use_unsharp and factor >= 2:
        # Create unsharp mask effect
        blurred = current_img.filter(ImageFilter.GaussianBlur(radius=2))
        
        if current_img.mode == 'RGBA':
            # Process RGB only, preserve alpha
            alpha = current_img.split()[3]
            rgb = Image.merge('RGB', current_img.split()[:3])
            rgb_blur = Image.merge('RGB', blurred.split()[:3])
            
            # Unsharp mask formula: original + (original - blurred) * amount
            rgb_array = np.array(rgb, dtype=np.float32)
            blur_array = np.array(rgb_blur, dtype=np.float32)
            
            sharpened = rgb_array + (rgb_array - blur_array) * 0.8
            sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
            
            rgb_result = Image.fromarray(sharpened, 'RGB')
            current_img = Image.merge('RGBA', (*rgb_result.split(), alpha))
        else:
            if current_img.mode == 'RGB':
                img_array = np.array(current_img, dtype=np.float32)
                blur_array = np.array(blurred, dtype=np.float32)
                
                sharpened = img_array + (img_array - blur_array) * 0.8
                sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
                
                current_img = Image.fromarray(sharpened, 'RGB')
            else:
                current_img = advanced_sharpen(current_img, final_sharpen)
    
    # Final subtle clarity boost
    if quality_mode == "maximum":
        enhancer = ImageEnhance.Contrast(current_img)
        current_img = enhancer.enhance(1.05)
    
    return current_img
    """Intelligent noise reduction"""
    return image.filter(ImageFilter.MedianFilter(size=strength * 2 + 1))

def edge_enhance(image: Image.Image, factor: float = 1.5) -> Image.Image:
    """Enhance edges for crisp elements with smart blending"""
    # Apply edge enhancement
    enhanced = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    
    # Blend more carefully to avoid over-enhancement
    blend_factor = min(factor / 10, 0.3)  # Cap at 30% blend
    return Image.blend(image, enhanced, blend_factor)

def color_pop(image: Image.Image, saturation: float = 1.5) -> Image.Image:
    """Boost color saturation intelligently"""
    if image.mode not in ['RGB', 'RGBA']:
        return image
    
    # Cap saturation to avoid oversaturation
    safe_saturation = min(saturation, 2.0)
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(safe_saturation)

def advanced_sharpen(image: Image.Image, amount: float = 1.5) -> Image.Image:
    """Advanced sharpening with unsharp mask technique"""
    # Create slightly blurred version
    blurred = image.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Calculate sharpening amount
    sharp_amount = min(amount, 3.0)  # Cap to prevent artifacts
    
    # Apply unsharp mask manually
    if image.mode == 'RGBA':
        # Process RGB channels only
        alpha = image.split()[3]
        rgb = Image.merge('RGB', image.split()[:3])
        rgb_blur = Image.merge('RGB', blurred.split()[:3])
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(rgb)
        rgb_sharp = enhancer.enhance(sharp_amount)
        
        result = Image.merge('RGBA', (*rgb_sharp.split(), alpha))
        return result
    else:
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(sharp_amount)

# Header
st.markdown("""
    <div class="title-container">
        <h1 class="title-text">✨ Hania, Don't Crash Out</h1>
        <p class="subtitle-text">All your design prep work in one place - remove backgrounds, enhance, and export perfectly</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with presets and batch options
with st.sidebar:
    st.markdown("### ⚡ Quick Presets")
    
    preset = st.radio(
        "Choose workflow",
        ["Custom", "Social Media", "Print Design", "Web Graphics", "Product Shot", "Max Quality"],
        help="Pre-configured settings"
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Export")
    
    output_format = st.selectbox(
        "Format",
        ["PNG (Transparent)", "PNG (White BG)", "JPEG", "WEBP"],
        help="Output format"
    )
    
    if "JPEG" not in output_format and "WEBP" not in output_format:
        export_size = st.radio(
            "Size",
            ["Original", "1080p", "2K", "4K", "Custom"],
            help="Export dimensions"
        )
        
        if export_size == "Custom":
            st.markdown("**Custom Dimensions**")
            custom_width = st.number_input("Width", min_value=100, max_value=16000, value=2000)
            custom_height = st.number_input("Height", min_value=100, max_value=16000, value=2000)

# Preset configurations
preset_configs = {
    "Social Media": {
        "remove_bg": True,
        "upscale_factor": 2,
        "upscale_quality": "Balanced",
        "enhance_quality": True,
        "sharpness": 1.5,
        "auto_crop": True,
        "add_shadow": True,
        "color_boost": True
    },
    "Print Design": {
        "remove_bg": True,
        "upscale_factor": 4,
        "upscale_quality": "Maximum Quality",
        "enhance_quality": True,
        "sharpness": 2.0,
        "denoise": True,
        "color_boost": True
    },
    "Web Graphics": {
        "remove_bg": True,
        "upscale_factor": 2,
        "upscale_quality": "Fast",
        "enhance_quality": True,
        "sharpness": 1.2,
        "auto_crop": True
    },
    "Product Shot": {
        "remove_bg": True,
        "upscale_factor": 3,
        "upscale_quality": "Maximum Quality",
        "enhance_quality": True,
        "sharpness": 2.0,
        "add_shadow": True,
        "add_padding": True,
        "denoise": True
    },
    "Max Quality": {
        "remove_bg": True,
        "upscale_factor": 4,
        "upscale_quality": "Maximum Quality",
        "enhance_quality": True,
        "sharpness": 2.5,
        "denoise": True,
        "color_boost": True,
        "edge_enhance": True
    }
}

# Main content
col_upload, col_info = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Drop your image here or click to browse",
        type=["png", "jpg", "jpeg", "webp"],
        help="Supported formats: PNG, JPG, JPEG, WEBP"
    )

with col_info:
    if preset != "Custom":
        st.markdown("### 📋 Active Features")
        config = preset_configs[preset]
        feature_list = []
        if config.get("remove_bg"): feature_list.append("✓ Background Removal")
        if config.get("upscale_factor", 1) > 1: feature_list.append(f"✓ {config['upscale_factor']}x Upscale")
        if config.get("enhance_quality"): feature_list.append("✓ Quality Boost")
        if config.get("auto_crop"): feature_list.append("✓ Auto Crop")
        if config.get("add_shadow"): feature_list.append("✓ Drop Shadow")
        if config.get("denoise"): feature_list.append("✓ Denoise")
        
        for feature in feature_list:
            st.markdown(f"{feature}")
    else:
        st.markdown("### 💡 Tips")
        st.markdown("Use presets for quick results or go custom for full control!")

if uploaded_file:
    # Load and display original image
    try:
        image = Image.open(uploaded_file)
        original_size = image.size
        
        # Validate image
        if image.size[0] * image.size[1] > 178_956_970:
            st.error("❌ Image is too large! Maximum supported size is ~178 megapixels.")
            st.stop()
        
        # Convert palette images to RGBA for better processing
        if image.mode == 'P':
            image = image.convert('RGBA')
        elif image.mode == 'L':
            image = image.convert('RGB')
            
    except Exception as e:
        st.error(f"❌ Error loading image: {str(e)}")
        st.stop()
    
    # Display original
    st.markdown("### 📸 Original Image")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, width="stretch")
    
    # Calculate file size
    file_size_kb = round(uploaded_file.size / 1024, 1)
    file_size_display = f"{file_size_kb} KB" if file_size_kb < 1024 else f"{round(file_size_kb/1024, 1)} MB"
    
    st.markdown(f"""
        <div class="info-box">
            <strong>Image Info:</strong> {original_size[0]} × {original_size[1]} pixels | 
            {image.mode} | {file_size_display}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features section
    st.markdown("### 🎨 Enhancement Options")
    
    # Apply preset or custom settings
    if preset != "Custom":
        config = preset_configs[preset]
        remove_bg = config.get("remove_bg", False)
        upscale = config.get("upscale_factor", 2) > 1
        upscale_factor = config.get("upscale_factor", 2)
        upscale_quality = config.get("upscale_quality", "Balanced")
        enhance_quality = config.get("enhance_quality", False)
        sharpness = config.get("sharpness", 1.5)
        adjust_colors = False
        brightness = 1.0
        contrast = 1.0
        saturation = 1.0
        auto_crop = config.get("auto_crop", False)
        add_shadow_effect = config.get("add_shadow", False)
        shadow_blur = 10
        shadow_opacity = 128
        denoise = config.get("denoise", False)
        color_boost = config.get("color_boost", False)
        edge_enhance_effect = config.get("edge_enhance", False)
        add_padding_effect = config.get("add_padding", False)
        padding_size = 50
        
        st.info(f"🎯 Using **{preset}** preset - all settings optimized!")
    else:
        # Custom controls
        tab1, tab2, tab3 = st.tabs(["🎭 Basic", "✨ Advanced", "🎨 Effects"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                remove_bg = st.checkbox("🎭 Remove Background", value=True, 
                                       help="AI-powered background removal")
                upscale = st.checkbox("📈 Upscale Image", value=True, 
                                     help="Increase resolution with advanced algorithm")
            with col2:
                enhance_quality = st.checkbox("✨ Enhance Quality", value=False, 
                                             help="Improve sharpness and clarity")
                adjust_colors = st.checkbox("🎨 Adjust Colors", value=False, 
                                           help="Fine-tune brightness and contrast")
            
            if upscale:
                st.markdown("**Upscale Settings**")
                upscale_factor = st.select_slider(
                    "Upscale Factor",
                    options=[2, 3, 4, 5, 6],
                    value=2,
                    help="Higher = larger output"
                )
                
                upscale_quality = st.radio(
                    "Quality Mode",
                    ["Fast", "Balanced", "Maximum Quality"],
                    index=1,
                    horizontal=True,
                    help="Maximum Quality: Best results but slower"
                )
            else:
                upscale_factor = 1
                upscale_quality = "Balanced"
            
            if enhance_quality:
                st.markdown("**Quality Enhancement**")
                sharpness = st.slider("Sharpness", 0.0, 3.0, 1.5, 0.1,
                                     help="Higher values = sharper (may show artifacts above 2.5)")
            else:
                sharpness = 1.0
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                auto_crop = st.checkbox("✂️ Auto-Crop to Content", value=False,
                                       help="Remove empty space around element")
                denoise = st.checkbox("🧹 Denoise", value=False,
                                     help="Reduce image noise and grain")
            with col2:
                edge_enhance_effect = st.checkbox("🔲 Edge Enhancement", value=False,
                                                 help="Make edges crisper")
                color_boost = st.checkbox("🌈 Color Boost", value=False,
                                         help="Increase color saturation")
            
            if adjust_colors:
                st.markdown("**Color Controls**")
                col_a, col_b = st.columns(2)
                with col_a:
                    brightness = st.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
                    saturation = st.slider("Saturation", 0.5, 2.0, 1.0, 0.1)
                with col_b:
                    contrast = st.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
            else:
                brightness = 1.0
                contrast = 1.0
                saturation = 1.0
        
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                add_shadow_effect = st.checkbox("🌑 Add Drop Shadow", value=False,
                                               help="Add professional shadow effect")
                if add_shadow_effect:
                    shadow_blur = st.slider("Shadow Blur", 5, 30, 10)
                    shadow_opacity = st.slider("Shadow Opacity", 50, 255, 128)
                else:
                    shadow_blur = 10
                    shadow_opacity = 128
            
            with col2:
                add_padding_effect = st.checkbox("📐 Add Padding", value=False,
                                                help="Add space around the element")
                if add_padding_effect:
                    padding_size = st.slider("Padding Size", 10, 200, 50)
                else:
                    padding_size = 50
    
    st.markdown("---")
    
    # Process button
    if st.button("🚀 Process Image", type="primary"):
        with st.spinner("✨ Working magic on your image..."):
            try:
                # Memory management
                result_img = image.copy()
                steps_completed = []
                processing_errors = []
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Optimize image size if needed for processing
                processing_img, scale_factor = optimize_image_for_processing(result_img)
                if scale_factor < 1.0:
                    st.info(f"ℹ️ Temporarily scaled image to {int(scale_factor * 100)}% for processing")
                    result_img = processing_img
                
                # Step 1: Remove background
                if remove_bg:
                    status_text.text("🎭 Removing background...")
                    progress_bar.progress(10)
                    try:
                        uploaded_file.seek(0)
                        img_bytes = uploaded_file.read()
                        
                        # Add timeout and error handling for rembg
                        try:
                            output = remove(img_bytes)
                            result_img = Image.open(io.BytesIO(output))
                            steps_completed.append("Background removed")
                        except Exception as rembg_error:
                            st.warning(f"⚠️ Background removal failed: {str(rembg_error)}")
                            st.info("💡 Continuing with original image...")
                            result_img = image.copy()
                            processing_errors.append(f"Background removal: {str(rembg_error)}")
                            
                    except Exception as e:
                        processing_errors.append(f"Background removal: {str(e)}")
                        st.warning("⚠️ Background removal failed, continuing with original image")
                        result_img = image.copy()
                    progress_bar.progress(25)
                    gc.collect()
                
                # Step 2: Auto-crop
                if auto_crop and result_img.mode == 'RGBA':
                    status_text.text("✂️ Auto-cropping...")
                    try:
                        result_img = auto_crop_transparent(result_img, margin=10)
                        steps_completed.append("Auto-cropped")
                    except Exception as e:
                        processing_errors.append(f"Auto-crop: {str(e)}")
                    progress_bar.progress(35)
                
                # Step 3: Denoise
                if denoise:
                    status_text.text("🧹 Denoising...")
                    try:
                        result_img = smart_denoise(result_img, strength=2)
                        steps_completed.append("Denoised")
                    except Exception as e:
                        processing_errors.append(f"Denoise: {str(e)}")
                    progress_bar.progress(45)
                
                # Step 4: Edge enhancement
                if edge_enhance_effect:
                    status_text.text("🔲 Enhancing edges...")
                    try:
                        result_img = edge_enhance(result_img, 1.5)
                        steps_completed.append("Edges enhanced")
                    except Exception as e:
                        processing_errors.append(f"Edge enhancement: {str(e)}")
                    progress_bar.progress(55)
                
                # Step 5: Enhance quality (Advanced sharpening)
                if enhance_quality:
                    status_text.text("✨ Enhancing quality...")
                    try:
                        result_img = advanced_sharpen(result_img, sharpness)
                        steps_completed.append("Quality enhanced")
                    except Exception as e:
                        processing_errors.append(f"Quality enhancement: {str(e)}")
                    progress_bar.progress(65)
                
                # Step 6: Color adjustments
                if adjust_colors or color_boost:
                    status_text.text("🎨 Adjusting colors...")
                    try:
                        if adjust_colors:
                            enhancer = ImageEnhance.Brightness(result_img)
                            result_img = enhancer.enhance(brightness)
                            enhancer = ImageEnhance.Contrast(result_img)
                            result_img = enhancer.enhance(contrast)
                        if color_boost:
                            result_img = color_pop(result_img, 1.3)
                        steps_completed.append("Colors adjusted")
                    except Exception as e:
                        processing_errors.append(f"Color adjustment: {str(e)}")
                    progress_bar.progress(75)
                
                # Step 7: Upscale
                if upscale and upscale_factor > 1:
                    status_text.text(f"📈 Upscaling {upscale_factor}x with {upscale_quality.lower()} mode...")
                    try:
                        quality_map = {
                            "Fast": "fast",
                            "Balanced": "balanced", 
                            "Maximum Quality": "maximum"
                        }
                        result_img = smart_upscale(result_img, upscale_factor, quality_map[upscale_quality])
                        steps_completed.append(f"Upscaled {upscale_factor}x ({upscale_quality})")
                    except Exception as e:
                        processing_errors.append(f"Upscaling: {str(e)}")
                        st.warning(f"⚠️ Upscaling failed: {str(e)}")
                    progress_bar.progress(85)
                    gc.collect()
                
                # Step 8: Add effects
                if add_shadow_effect and result_img.mode == 'RGBA':
                    status_text.text("🌑 Adding shadow...")
                    try:
                        result_img = add_shadow(result_img, offset=(5, 5), 
                                              blur=shadow_blur, opacity=shadow_opacity)
                        steps_completed.append("Shadow added")
                    except Exception as e:
                        processing_errors.append(f"Shadow: {str(e)}")
                    progress_bar.progress(92)
                
                if add_padding_effect:
                    status_text.text("📐 Adding padding...")
                    try:
                        result_img = add_padding(result_img, padding_size)
                        steps_completed.append("Padding added")
                    except Exception as e:
                        processing_errors.append(f"Padding: {str(e)}")
                    progress_bar.progress(96)
                
                progress_bar.progress(100)
                status_text.text("✅ Complete!")
                
                # Show warnings if any
                if processing_errors:
                    st.warning(f"⚠️ Some operations had issues: {', '.join(processing_errors)}")
                
                # Success message
                st.markdown(f"""
                    <div class="success-message">
                        <strong>✅ Success!</strong> Completed: {', '.join(steps_completed)}
                    </div>
                """, unsafe_allow_html=True)
                
                # Display result
                st.markdown("### 🎉 Processed Image")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(result_img, width="stretch")
                
                final_size = result_img.size
                size_increase = (final_size[0] * final_size[1]) / (original_size[0] * original_size[1])
                
                st.markdown(f"""
                    <div class="info-box">
                        <strong>Final Size:</strong> {final_size[0]} × {final_size[1]} pixels 
                        ({size_increase:.1f}x resolution increase)
                    </div>
                """, unsafe_allow_html=True)
                
                # Download options
                st.markdown("### 💾 Download Your Image")
                
                # Handle export sizing
                export_img = result_img.copy()
                if 'export_size' in locals() and export_size != "Original":
                    if export_size == "1080p":
                        target_size = (1080, 1080)
                    elif export_size == "2K":
                        target_size = (2048, 2048)
                    elif export_size == "4K":
                        target_size = (3840, 3840)
                    elif export_size == "Custom":
                        target_size = (custom_width, custom_height)
                    else:
                        target_size = export_img.size
                    
                    if target_size != export_img.size:
                        # Check if target size is valid
                        if target_size[0] * target_size[1] <= 178_956_970:
                            export_img = export_img.resize(target_size, Image.Resampling.LANCZOS)
                        else:
                            st.warning("⚠️ Target export size too large, using processed size instead")
                
                # Prepare download based on format
                try:
                    if output_format == "PNG (Transparent)":
                        buf = io.BytesIO()
                        export_img.save(buf, format="PNG", optimize=True)
                        mime_type = "image/png"
                        file_ext = "png"
                    elif output_format == "PNG (White BG)":
                        if export_img.mode == 'RGBA':
                            bg = Image.new('RGB', export_img.size, (255, 255, 255))
                            bg.paste(export_img, mask=export_img.split()[3])
                            export_img = bg
                        buf = io.BytesIO()
                        export_img.save(buf, format="PNG", optimize=True)
                        mime_type = "image/png"
                        file_ext = "png"
                    elif output_format == "JPEG":
                        if export_img.mode in ('RGBA', 'LA', 'P'):
                            bg = Image.new('RGB', export_img.size, (255, 255, 255))
                            if export_img.mode == 'P':
                                export_img = export_img.convert('RGBA')
                            if export_img.mode in ('RGBA', 'LA'):
                                bg.paste(export_img, mask=export_img.split()[3])
                            export_img = bg
                        buf = io.BytesIO()
                        export_img.save(buf, format="JPEG", quality=95, optimize=True)
                        mime_type = "image/jpeg"
                        file_ext = "jpg"
                    else:  # WEBP
                        buf = io.BytesIO()
                        export_img.save(buf, format="WEBP", quality=95, method=6)
                        mime_type = "image/webp"
                        file_ext = "webp"
                    
                    buf_size = len(buf.getvalue()) / 1024
                    size_display = f"{buf_size:.1f} KB" if buf_size < 1024 else f"{buf_size/1024:.1f} MB"
                    
                    col_dl1, col_dl2, col_dl3 = st.columns(3)
                    
                    with col_dl2:
                        st.download_button(
                            f"⬇️ Download {output_format.split()[0]} ({size_display})",
                            data=buf.getvalue(),
                            file_name=f"element_prep_result.{file_ext}",
                            mime=mime_type
                        )
                except Exception as e:
                    st.error(f"❌ Export error: {str(e)}")
                    st.info("💡 Try a different export format or reduce the image size")
                
                # Memory cleanup
                gc.collect()
                
            except Exception as e:
                st.error(f"❌ Processing error: {str(e)}")
                st.info("💡 Try with fewer enhancements enabled or a smaller image")
                
                # Show detailed error for debugging
                with st.expander("🔍 Error Details"):
                    st.code(str(e))
                    import traceback
                    st.code(traceback.format_exc())

else:
    # Empty state with helpful info
    st.markdown("""
        <div class="info-box">
            <h3 style="margin-top: 0;">👋 Get Started</h3>
            <p>Upload an image above to begin transforming your creative elements!</p>
            <p><strong>Perfect for:</strong></p>
            <ul>
                <li>🎨 Poster design elements</li>
                <li>📱 Social media content</li>
                <li>📦 Product photography</li>
                <li>🎭 Digital art projects</li>
                <li>🖼️ Print-ready graphics</li>
            </ul>
            <p><strong>Pro tip:</strong> Use the sidebar to choose quick presets for common workflows!</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p class="footer-text">Made for han :)</p>
    </div>
""", unsafe_allow_html=True)
