"""
Handler: Face Detection using OpenCV Haar Cascade + MediaPipe
"""
import cv2
import numpy as np


async def handle_face(update, image_path: str, output_path: str):
    output_file = output_path + "_faces.jpg"

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load Haar cascade (built into OpenCV — no download needed)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    face_count = len(faces)

    if face_count == 0:
        await update.message.reply_text(
            "👤 *Face Detection Result:*\n\n⚠️ No faces detected in this image.",
            parse_mode="Markdown"
        )
        return

    # Draw bounding boxes
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(img, "Face", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imwrite(output_file, img)

    with open(output_file, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=f"👤 *Face Detection Result:*\n\n✅ Detected *{face_count}* face(s) in the image.",
            parse_mode="Markdown"
        )
