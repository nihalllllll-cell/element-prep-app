import streamlit as st
from rembg import remove
from PIL import Image
import torch
import io
from realesrgan import RealESRGANer
import numpy as np

st.title("One-Click Element Prep")

file = st.file_uploader("Upload image", ["png", "jpg", "jpeg"])
if file:
    img = Image.open(file).convert("RGB")
    st.image(img, caption="Original")

    remove_bg = st.checkbox("Remove background")
    upscale = st.checkbox("Upscale 4×")

    if st.button("Process"):
        result_img = img

        if remove_bg:
            result_img = Image.open(io.BytesIO(remove(result_img)))

        if upscale:
            st.info("Upscaling…")
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            upscaler = RealESRGANer(scale=4, model_path=None, device=device)
            result_np = np.array(result_img)
            result_np, _ = upscaler.enhance(result_np, outscale=4)
            result_img = Image.fromarray(result_np)

        buf = io.BytesIO()
        result_img.save(buf, "PNG")
        st.download_button("Download", buf.getvalue(), "element.png", "image/png")
