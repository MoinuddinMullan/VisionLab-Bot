# 🤖 AI Vision MultiTool Telegram Bot

A powerful Telegram bot that combines **8 AI/ML features** into a single image-processing assistant. Built with Python, OpenCV, Hugging Face, YOLOv8, DeepFace, and more.

---

## ✨ Features

| Command | Feature | Technology |
|---|---|---|
| `/caption` | AI Image Captioning | BLIP (Hugging Face) |
| `/ocr` | Text Extraction | EasyOCR |
| `/removebg` | Background Removal | rembg / U²-Net |
| `/detectface` | Face Detection | OpenCV Haar Cascade |
| `/detectobjects` | Object Detection | YOLOv8 |
| `/emotion` | Emotion Detection | DeepFace |
| `/cartoon` | Cartoon + Sketch Effect | OpenCV |
| `/enhance` | Image Enhancement | OpenCV + Pillow |

---

## 🚀 Quick Start

### Step 1 — Get a Telegram Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow prompts → choose a name and username for your bot
4. Copy the **token** BotFather gives you (looks like `123456:ABC-DEF...`)

---

### Step 2 — Clone & Setup

```bash
# Clone the repo (or download the ZIP)
git clone https://github.com/yourusername/AI_Vision_Bot.git
cd AI_Vision_Bot

# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

> ⚠️ **First install takes 5–15 minutes** — it downloads PyTorch, OpenCV, Hugging Face models, etc.

---

### Step 3 — Add Your Token

```bash
# Copy the example file
cp .env.example .env

# Open .env and paste your token:
# BOT_TOKEN=123456:YOUR_TOKEN_HERE
```

Or on Windows, just open `.env.example` in Notepad, add your token, and save it as `.env`.

---

### Step 4 — Run the Bot

```bash
python bot.py
```

You should see:
```
🤖 AI Vision MultiTool Bot is running...
```

Now open Telegram, find your bot by its username, and send `/start`!

---

## 📁 Project Structure

```
AI_Vision_Bot/
│
├── bot.py              ← Main bot (routing + commands)
├── config.py           ← Token & settings
├── requirements.txt    ← All dependencies
├── .env                ← Your secrets (NOT on GitHub)
├── .env.example        ← Template for .env
├── .gitignore
│
├── handlers/           ← One file per feature
│   ├── caption_handler.py
│   ├── ocr_handler.py
│   ├── background_handler.py
│   ├── face_handler.py
│   ├── object_handler.py
│   ├── emotion_handler.py
│   ├── cartoon_handler.py
│   └── enhance_handler.py
│
├── uploads/            ← Temp input images (auto-created)
└── outputs/            ← Processed output images (auto-created)
```

---

## 🔧 How to Use the Bot

1. Send `/start` → see the interactive menu
2. Tap a feature button **or** type a command like `/ocr`
3. Bot confirms: *"OCR mode activated! Send me an image."*
4. Upload any image
5. Get your result!

---

## 🖥️ System Requirements

| | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB |
| CPU | Intel i5 | Intel i7 / Ryzen 7 |
| GPU | Not required | NVIDIA (CUDA) |
| Python | 3.9+ | 3.10 |
| Storage | 5 GB free | 10 GB free |

> The bot runs fine on CPU. A GPU just makes AI inference faster.

---

## ☁️ Cloud Deployment (Free Tiers)

### Option A — Render (Recommended, free)
1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo
4. Set environment variable: `BOT_TOKEN = your_token`
5. Start command: `python bot.py`

### Option B — Railway
1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Add `BOT_TOKEN` in Variables tab

---

## 🛡️ Security Notes

- `.env` is in `.gitignore` — your token will **never** be pushed to GitHub
- Bot validates image files before processing
- Each user's files are stored with their `chat_id` to avoid collisions
- Uploaded files are temporary (you can add a cleanup cron if needed)

---

## 🐛 Common Issues

**`ModuleNotFoundError`** → Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`

**`Face could not be detected`** → The emotion detector needs a clear, forward-facing face photo

**Bot not responding** → Check that `python bot.py` is still running in your terminal

**Slow first response** → Models download on first use. BLIP is ~1GB, YOLOv8n is ~6MB — subsequent runs are instant

---

## 📄 License

MIT — free to use, modify, and include in your portfolio.

---

## 🙏 Technologies Used

- [python-telegram-bot](https://python-telegram-bot.org/)
- [Hugging Face BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [rembg](https://github.com/danielgatis/rembg)
- [YOLOv8 (Ultralytics)](https://github.com/ultralytics/ultralytics)
- [DeepFace](https://github.com/serengil/deepface)
- [OpenCV](https://opencv.org/)
