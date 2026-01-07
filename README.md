---
title: BG Remover & Upscaler
emoji: 🎨
colorFrom: purple
colorTo: pink
sdk: docker
sdk_version: "latest"
app_file: app.py
pinned: false
---

# Background Remover & Upscaler

A Streamlit app that removes backgrounds and upscales images - all the boring prep work done in one click!

## Features
- 🖼️ Upload any image (PNG, JPG, JPEG)
- ✂️ Remove background using AI
- 📈 Upscale image 2x with high quality
- ⬇️ Download processed result as PNG
- ⚡ Do both at once or separately

## How to Use
1. Upload your image
2. Choose whether to remove background and/or upscale
3. Click "Process Image"
4. Download your result!

## Tech Stack
- Streamlit
- Pillow (image processing)
- rembg (AI background removal)
- ONNX Runtime

## Deployment
Deploy directly to Streamlit Cloud or Hugging Face Spaces using the provided Dockerfile.

Perfect for designers, content creators, and anyone tired of running images through multiple tools!
