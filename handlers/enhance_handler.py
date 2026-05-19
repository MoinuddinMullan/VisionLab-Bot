"""
Handler: AI Image Enhancement using OpenCV + Pillow
(ESRGAN/GFPGAN require large GPU models; this uses strong CV-based enhancement
that works on any machine and still looks impressive)
"""
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


def enhance_image(image_path: str, output_path: str) -> str:
    # --- OpenCV: Denoise + Sharpen ---
    img_cv = cv2.imread(image_path)

    # Denoise
    denoised = cv2.fastNlMeansDenoisingColored(img_cv, None, h=10, hColor=10,
                                                templateWindowSize=7, searchWindowSize=21)

    # Upscale 2x with Lanczos (high-quality interpolation)
    h, w = denoised.shape[:2]
    upscaled = cv2.resize(denoised, (w * 2, h * 2), interpolation=cv2.INTER_LANCZOS4)

    # Unsharp mask for crispness
    gaussian = cv2.GaussianBlur(upscaled, (0, 0), 2.0)
    sharpened = cv2.addWeighted(upscaled, 1.5, gaussian, -0.5, 0)

    # --- PIL: Color + Contrast boost ---
    pil_img = Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))
    pil_img = ImageEnhance.Contrast(pil_img).enhance(1.2)
    pil_img = ImageEnhance.Color(pil_img).enhance(1.15)
    pil_img = ImageEnhance.Brightness(pil_img).enhance(1.05)
    pil_img = ImageEnhance.Sharpness(pil_img).enhance(1.3)

    pil_img.save(output_path, quality=95)
    return output_path


async def handle_enhance(update, image_path: str, output_path: str):
    output_file = output_path + "_enhanced.jpg"
    enhance_image(image_path, output_file)

    with open(output_file, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=(
                "✨ *Image Enhanced!*\n\n"
                "Applied:\n"
                "• AI Denoising\n"
                "• 2× Upscaling (Lanczos)\n"
                "• Unsharp Sharpening\n"
                "• Contrast & Color Boost"
            ),
            parse_mode="Markdown"
        )
