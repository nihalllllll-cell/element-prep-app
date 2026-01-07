import streamlit as st
from PIL import Image
from rembg import remove
import io
import requests

st.set_page_config(page_title="BG Remover & Upscaler", layout="centered")

st.title("🎨 Background Remover & Upscaler")
st.write("Remove backgrounds and upscale images in one go!")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display original image
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        remove_bg = st.checkbox("Remove Background", value=True)
    
    with col2:
        upscale = st.checkbox("Upscale Image (2x)", value=True)
    
    if st.button("Process Image", type="primary"):
        with st.spinner("Processing..."):
            result_img = image.copy()
            
            # Step 1: Remove background if selected
            if remove_bg:
                st.info("Removing background...")
                # Reset file pointer
                uploaded_file.seek(0)
                img_bytes = uploaded_file.read()
                output = remove(img_bytes)
                result_img = Image.open(io.BytesIO(output))
            
            # Step 2: Upscale if selected
            if upscale:
                st.info("Upscaling image...")
                original_size = result_img.size
                new_size = (original_size[0] * 2, original_size[1] * 2)
                result_img = result_img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Display result
            st.success("Done!")
            st.image(result_img, caption="Processed Image", use_container_width=True)
            
            # Download button
            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            st.download_button(
                "⬇️ Download Processed Image",
                data=buf.getvalue(),
                file_name="processed_image.png",
                mime="image/png"
            )

st.markdown("---")
st.caption("Made with ❤️ to save time on creative work")
