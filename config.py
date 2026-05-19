"""
Configuration — put your secrets here (never commit this to GitHub!)
"""
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
HF_TOKEN = os.getenv("HF_TOKEN", "")
MAX_FILE_SIZE_MB = 10
UPLOAD_DIR  = "uploads"
OUTPUT_DIR  = "outputs"
