import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove
import io

# Page config with custom theme
st.set_page_config(
    page_title="Element Prep Studio",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for aesthetic UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .title-container {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .title-text {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ffffff, #ffd1dc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .subtitle-text {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
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
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .footer-text {
        color: white;
        font-size: 1.2rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    .stCheckbox {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 8px;
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
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .stSlider {
        padding: 1rem 0;
    }
    
    .stSelectbox {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: rgba(255, 255, 255, 0.2);
    }
    
    .success-message {
        background: rgba(76, 175, 80, 0.2);
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    
    .info-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="title-container">
        <h1 class="title-text">✨ Element Prep Studio</h1>
        <p class="subtitle-text">Remove backgrounds, upscale, and enhance images in seconds</p>
    </div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Drop your image here or click to browse",
    type=["png", "jpg", "jpeg", "webp"],
    help="Supported formats: PNG, JPG, JPEG, WEBP"
)

if uploaded_file:
    # Load and display original image
    image = Image.open(uploaded_file)
    original_size = image.size
    
    st.markdown("### 📸 Original Image")
    st.image(image, use_container_width=True)
    
    st.markdown(f"""
        <div class="info-box">
            <strong>Image Info:</strong> {original_size[0]} × {original_size[1]} pixels
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features section
    st.markdown("### 🎨 Choose Your Enhancements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        remove_bg = st.checkbox("🎭 Remove Background", value=True, help="AI-powered background removal")
        enhance_quality = st.checkbox("✨ Enhance Quality", value=False, help="Improve sharpness and clarity")
    
    with col2:
        upscale = st.checkbox("📈 Upscale Image", value=True, help="Increase resolution 2x or 4x")
        adjust_colors = st.checkbox("🎨 Adjust Colors", value=False, help="Fine-tune brightness and contrast")
    
    # Advanced options
    if upscale:
        st.markdown("#### Upscale Options")
        upscale_factor = st.select_slider(
            "Upscale Factor",
            options=[2, 3, 4],
            value=2,
            help="How much to increase the image size"
        )
    
    if adjust_colors:
        st.markdown("#### Color Adjustments")
        col_a, col_b = st.columns(2)
        with col_a:
            brightness = st.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
        with col_b:
            contrast = st.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
    
    if enhance_quality:
        st.markdown("#### Quality Enhancement")
        sharpness = st.slider("Sharpness", 0.0, 3.0, 1.5, 0.1)
    
    st.markdown("---")
    
    # Process button
    if st.button("🚀 Process Image", type="primary", use_container_width=True):
        with st.spinner("✨ Working magic on your image..."):
            try:
                result_img = image.copy()
                steps_completed = []
                
                # Step 1: Remove background
                if remove_bg:
                    with st.spinner("🎭 Removing background..."):
                        uploaded_file.seek(0)
                        img_bytes = uploaded_file.read()
                        output = remove(img_bytes)
                        result_img = Image.open(io.BytesIO(output))
                        steps_completed.append("Background removed")
                
                # Step 2: Enhance quality
                if enhance_quality:
                    with st.spinner("✨ Enhancing quality..."):
                        enhancer = ImageEnhance.Sharpness(result_img)
                        result_img = enhancer.enhance(sharpness)
                        steps_completed.append("Quality enhanced")
                
                # Step 3: Color adjustments
                if adjust_colors:
                    with st.spinner("🎨 Adjusting colors..."):
                        # Brightness
                        enhancer = ImageEnhance.Brightness(result_img)
                        result_img = enhancer.enhance(brightness)
                        # Contrast
                        enhancer = ImageEnhance.Contrast(result_img)
                        result_img = enhancer.enhance(contrast)
                        steps_completed.append("Colors adjusted")
                
                # Step 4: Upscale
                if upscale:
                    with st.spinner("📈 Upscaling image..."):
                        new_size = (
                            original_size[0] * upscale_factor,
                            original_size[1] * upscale_factor
                        )
                        result_img = result_img.resize(new_size, Image.Resampling.LANCZOS)
                        steps_completed.append(f"Upscaled {upscale_factor}x")
                
                # Success message
                st.markdown(f"""
                    <div class="success-message">
                        <strong>✅ Success!</strong> Completed: {', '.join(steps_completed)}
                    </div>
                """, unsafe_allow_html=True)
                
                # Display result
                st.markdown("### 🎉 Processed Image")
                st.image(result_img, use_container_width=True)
                
                final_size = result_img.size
                st.markdown(f"""
                    <div class="info-box">
                        <strong>Final Size:</strong> {final_size[0]} × {final_size[1]} pixels 
                        ({final_size[0] * final_size[1] / (original_size[0] * original_size[1]):.1f}x original resolution)
                    </div>
                """, unsafe_allow_html=True)
                
                # Download options
                st.markdown("### 💾 Download Your Image")
                
                col_dl1, col_dl2 = st.columns(2)
                
                with col_dl1:
                    # PNG download
                    buf_png = io.BytesIO()
                    result_img.save(buf_png, format="PNG")
                    st.download_button(
                        "⬇️ Download PNG",
                        data=buf_png.getvalue(),
                        file_name="element_prep_result.png",
                        mime="image/png",
                        use_container_width=True
                    )
                
                with col_dl2:
                    # JPEG download (for smaller file size)
                    if result_img.mode in ('RGBA', 'LA', 'P'):
                        jpeg_img = Image.new('RGB', result_img.size, (255, 255, 255))
                        if result_img.mode == 'P':
                            result_img = result_img.convert('RGBA')
                        jpeg_img.paste(result_img, mask=result_img.split()[-1] if result_img.mode in ('RGBA', 'LA') else None)
                    else:
                        jpeg_img = result_img
                    
                    buf_jpg = io.BytesIO()
                    jpeg_img.save(buf_jpg, format="JPEG", quality=95)
                    st.download_button(
                        "⬇️ Download JPEG",
                        data=buf_jpg.getvalue(),
                        file_name="element_prep_result.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"❌ Oops! Something went wrong: {str(e)}")
                st.info("💡 Try uploading a different image or adjusting your settings.")

else:
    # Empty state with helpful info
    st.markdown("""
        <div class="info-box">
            <h3 style="margin-top: 0;">👋 Get Started</h3>
            <p>Upload an image above to begin transforming your creative elements!</p>
            <p><strong>Perfect for:</strong></p>
            <ul>
                <li>Poster design elements</li>
                <li>Social media content</li>
                <li>Product photography</li>
                <li>Digital art projects</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p class="footer-text">Made for han :)</p>
    </div>
""", unsafe_allow_html=True)
