"""
Handler: OCR Text Extraction using EasyOCR
"""
import easyocr
import cv2
import numpy as np

_reader = None

def load_reader():
    global _reader
    if _reader is None:
        print("Loading EasyOCR model (downloads on first run)...")
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader


async def handle_ocr(update, image_path: str):
    reader = load_reader()

    # Preprocess for better accuracy
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Run OCR
    results = reader.readtext(thresh)

    if not results:
        await update.message.reply_text(
            "📝 *OCR Result:*\n\n⚠️ No text detected in this image.",
            parse_mode="Markdown"
        )
        return

    # Collect text with confidence
    lines = []
    for (_, text, confidence) in results:
        if confidence > 0.3:
            lines.append(text)

    extracted = "\n".join(lines) if lines else "No readable text found."

    # Telegram message limit guard
    if len(extracted) > 3500:
        extracted = extracted[:3500] + "\n\n... (text truncated)"

    await update.message.reply_text(
        f"📝 *Extracted Text:*\n\n```\n{extracted}\n```",
        parse_mode="Markdown"
    )
