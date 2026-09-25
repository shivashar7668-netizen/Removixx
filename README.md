<div align="center">

# ⚡ Removix — AI Video & Image Watermark Remover

<p align="center">
  <strong>Next-Generation, Real-Time AI Watermark Removal Engine for Images & Videos</strong>
</p>

[![Live Demo](https://img.shields.io/badge/Live_Website-removix.sanvox.in-0284c7?style=for-the-badge&logo=google-chrome&logoColor=white)](https://removix.sanvox.in)
[![Developer Website](https://img.shields.io/badge/Developer-shivankthakur.com-6366f1?style=for-the-badge&logo=safari&logoColor=white)](https://shivankthakur.com/)
[![GitHub](https://img.shields.io/badge/GitHub-shivankthakurr%2FRemovix-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/shivankthakurr/Removix)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](LICENSE)

---

**Removix** is an intelligent, production-ready AI watermark remover built for creators, photographers, and video editors. Powered by deep learning (**LaMa — Large Mask Inpainting**) and multi-threaded CPU acceleration, Removix automatically detects and seamlessly erases visible AI watermarks, provenance tags, and corner logos while preserving 100% original texture, lighting, and pixel fidelity.

[🌐 Experience Removix Live](https://removix.sanvox.in) • [💻 Desktop App](#-native-windows-desktop-app) • [🚀 Quickstart](#-quickstart--local-setup)

---

</div>

## 🌟 Key Highlights

- **🎯 Universal Watermark Removal:** Erases Google Gemini sparkles, Midjourney, DALL-E, Stable Diffusion / SDXL, Adobe Firefly, TikTok, and custom corner watermarks.
- **🧠 SOTA Neural Inpainting:** Employs **big-LaMa ONNX** with multi-core parallelism and CPU memory arena optimization. Zero blur, zero smudge, and photorealistic context reconstruction.
- **🎬 Full Video Pipeline:** Frame-by-frame temporal consistency stabilization, lossless audio re-muxing, and variable frame rate (VFR) handling via PyAV and FFmpeg.
- **🖌️ Interactive Box Eraser:** Select any custom area on an image or video frame with a sleek, compact floating action bar (`[ ⚡ Erase with AI  ✕ ]`).
- **🛡️ C2PA & Metadata Stripping:** Automatically removes Content Credentials (C2PA manifests), SynthID provenance marks, EXIF tags, and AI generation fingerprints.
- **⚡ Real-Time Dynamic Progress:** Monotonic, non-blocking progress streaming (0% → 100%) with continuous sub-stage milestone reporting.
- **🔒 Production Ready:** 100% cloud-deployed on Oracle Cloud VPS with Nginx reverse proxy, automated Let's Encrypt HTTPS/SSL, and Systemd auto-healing.

---

## 📸 Before & After Interactive Preview

Removix isolates the watermark region with context-aware padding, runs neural matrix reconstruction, and performs soft feathered Gaussian boundary blending:

| Input (Original AI Image) | Removix Cleaned Output |
| :---: | :---: |
| Visible AI Sparkle / Corner Watermark | **Seamless AI Restoration (Zero Blur)** |
| Embedded C2PA / SynthID Metadata | **100% Cleaned & Anonymized** |
| Untouched Pixel Region | **Byte-Identical & Lossless** |

---

## 🛠️ System Architecture

```
                          ┌────────────────────────────────┐
                          │   Removix Web / Desktop UI     │
                          │   (HTML5, Glassmorphism, CSS)  │
                          └───────────────┬────────────────┘
                                          │
                                 POST /api/upload
                                          │
                                          ▼
                          ┌────────────────────────────────┐
                          │      Flask Async Server        │
                          │      (Reverse Proxy Nginx)     │
                          └───────────────┬────────────────┘
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   ▼                                             ▼
     ┌───────────────────────────┐                 ┌───────────────────────────┐
     │    Image Inpaint Worker   │                 │    Video Stream Worker    │
     │  - C2PA / EXIF Scanner    │                 │  - Frame Decomposition    │
     │  - Sparkle Engine         │                 │  - Temporal Stabilizer    │
     │  - Context Padder (512²)  │                 │  - PTS Lossless Remux     │
     └─────────────┬─────────────┘                 └─────────────┬─────────────┘
                   │                                             │
                   └──────────────────────┬──────────────────────┘
                                          │
                                          ▼
                          ┌────────────────────────────────┐
                          │    Multi-Threaded LaMa AI      │
                          │  (ONNX Runtime • AVX2 Parallel)│
                          └────────────────────────────────┘
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/shivankthakurr/Removix.git
cd Removix
```

### 2. Setup Virtual Environment (Recommended: `uv`)
```bash
# Using uv (lightning fast):
uv venv --python 3.12 venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies:
uv pip install -e ".[video,lama]" flask gunicorn
```

### 3. Run Removix Web Server
```bash
python app.py --server
```
Open **`http://localhost:7860`** in your browser.

---

## 💻 Native Windows Desktop App

Removix can also run as a native Windows standalone desktop application without needing any browser tabs or console windows.

### Run in Desktop Mode:
```bash
python app.py
```

### Build Windows Executable (.exe) & Installer:
```bash
# Build standalone windowed Removix.exe:
python build_exe.py

# Build professional Windows Setup Installer (Inno Setup):
python build_installer.py
```
Output installer will be generated in `dist/Removix-Setup-v1.0.exe`.

---

## 🌐 Production Cloud Deployment

Removix is designed for $0 / ₹0 Always Free cloud deployment on VPS environments (e.g., Oracle Cloud Always Free):

- **Web Server:** Nginx reverse proxy with `client_max_body_size 500M` and WebSocket stream headers.
- **SSL / TLS:** Universal RSA 2048-bit Let's Encrypt certificate managed by `certbot`.
- **Process Manager:** Systemd service (`removix.service`) with automatic boot recovery and memory watchdog.
- **Memory Scaling:** 8 GB NVMe SSD Swap configuration to handle 4K ultra-resolution images and long video streams without OOM.

---

## 👨‍💻 Developer & Author
 
**Removix** was designed, architected, and developed by:
 
<div align="center">
 
### **Shivank Thakur**
*Full-Stack & Machine Learning Software Engineer*
 
[![Portfolio Website](https://img.shields.io/badge/Portfolio-shivankthakur.com-6366f1?style=for-the-badge&logo=safari&logoColor=white)](https://shivankthakur.com/)
[![GitHub](https://img.shields.io/badge/GitHub-shivankthakurr-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/shivankthakurr)
[![Project Live](https://img.shields.io/badge/Removix_Live-removix.sanvox.in-0284c7?style=for-the-badge&logo=google-chrome&logoColor=white)](https://removix.sanvox.in)

🌐 **Official Portfolio:** [https://shivankthakur.com/](https://shivankthakur.com/)  
🐙 **GitHub:** [https://github.com/shivankthakurr](https://github.com/shivankthakurr)  
⚡ **Live Product:** [https://removix.sanvox.in](https://removix.sanvox.in)
 
</div>
 
---
 
## 📄 License
 
This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for complete details.
 
```
Copyright 2025-2026 Shivank Thakur (https://shivankthakur.com/)
 
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 
    http://www.apache.org/licenses/LICENSE-2.0
```
 
---
 
<div align="center">
  <sub>Built with ❤️ by <a href="https://shivankthakur.com/"><strong>Shivank Thakur</strong></a> • Powered by LaMa & ONNX Runtime</sub>
</div>
