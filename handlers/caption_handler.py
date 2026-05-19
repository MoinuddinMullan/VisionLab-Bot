"""
Handler: AI Image Captioning using BLIP (Hugging Face)
"""
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Load model once (cached after first run)
_processor = None
_model = None

def load_model():
    global _processor, _model
    if _processor is None:
        print("Loading BLIP captioning model...")
        _processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        _model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        _model.eval()
    return _processor, _model


async def handle_caption(update, image_path: str):
    processor, model = load_model()

    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=50)

    caption = processor.decode(output[0], skip_special_tokens=True)

    await update.message.reply_text(
        f"🖼️ *AI Image Caption:*\n\n_{caption}_",
        parse_mode="Markdown"
    )
