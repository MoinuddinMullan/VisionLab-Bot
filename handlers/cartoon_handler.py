"""
Handler: Cartoon / Pencil Sketch Effect using OpenCV
(No heavy GAN model required — works instantly with CV techniques)
"""
import cv2
import numpy as np


def cartoonify(image_path: str, output_path: str) -> str:
    img = cv2.imread(image_path)
    img = cv2.resize(img, (600, int(img.shape[0] * 600 / img.shape[1])))

    # Step 1: Reduce noise
    smooth = cv2.bilateralFilter(img, d=9, sigmaColor=300, sigmaSpace=300)

    # Step 2: Edge detection
    gray = cv2.cvtColor(smooth, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        blockSize=9,
        C=2
    )

    # Step 3: Combine edges with color
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cartoon = cv2.bitwise_and(smooth, edges_colored)

    cv2.imwrite(output_path, cartoon)
    return output_path


def pencil_sketch(image_path: str, output_path: str) -> str:
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    inv = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    inv_blur = cv2.bitwise_not(blur)
    sketch = cv2.divide(gray, inv_blur, scale=256.0)

    cv2.imwrite(output_path, sketch)
    return output_path


async def handle_cartoon(update, image_path: str, output_path: str):
    cartoon_path = output_path + "_cartoon.jpg"
    sketch_path  = output_path + "_sketch.jpg"

    cartoonify(image_path, cartoon_path)
    pencil_sketch(image_path, sketch_path)

    media = []
    with open(cartoon_path, "rb") as f1, open(sketch_path, "rb") as f2:
        from telegram import InputMediaPhoto
        await update.message.reply_photo(
            photo=open(cartoon_path, "rb"),
            caption="🎨 *Cartoon Effect*",
            parse_mode="Markdown"
        )
        await update.message.reply_photo(
            photo=open(sketch_path, "rb"),
            caption="✏️ *Pencil Sketch Effect*",
            parse_mode="Markdown"
        )
