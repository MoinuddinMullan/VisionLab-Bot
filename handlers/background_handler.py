"""
Handler: Background Removal using rembg (U2-Net)
"""
from rembg import remove
from PIL import Image
import io


async def handle_background(update, image_path: str, output_path: str):
    output_file = output_path + "_nobg.png"

    with open(image_path, "rb") as f:
        input_data = f.read()

    output_data = remove(input_data)

    with open(output_file, "wb") as f:
        f.write(output_data)

    with open(output_file, "rb") as f:
        await update.message.reply_document(
            document=f,
            filename="background_removed.png",
            caption="✂️ *Background removed!*\n\nTransparent PNG is ready to use.",
            parse_mode="Markdown"
        )
