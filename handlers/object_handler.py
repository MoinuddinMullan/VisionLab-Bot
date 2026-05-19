"""
Handler: Object Detection using YOLOv8 (Ultralytics)
"""
from ultralytics import YOLO
import cv2

_model = None

def load_model():
    global _model
    if _model is None:
        print("Loading YOLOv8 model (downloads on first run)...")
        _model = YOLO("yolov8n.pt")   # nano = fast, good enough for bot use
    return _model


async def handle_object(update, image_path: str, output_path: str):
    output_file = output_path + "_objects.jpg"
    model = load_model()

    results = model(image_path, conf=0.35)
    result = results[0]

    # Save annotated image
    annotated = result.plot()
    cv2.imwrite(output_file, annotated)

    # Build label summary
    names = result.names
    boxes = result.boxes
    detected = {}

    for box in boxes:
        label = names[int(box.cls)]
        conf  = float(box.conf)
        if label not in detected or detected[label] < conf:
            detected[label] = conf

    if not detected:
        await update.message.reply_text(
            "🔍 *Object Detection Result:*\n\n⚠️ No objects detected with sufficient confidence.",
            parse_mode="Markdown"
        )
        return

    label_lines = "\n".join(
        [f"• {label.title()} ({conf*100:.0f}% confidence)"
         for label, conf in sorted(detected.items(), key=lambda x: -x[1])]
    )

    with open(output_file, "rb") as f:
        await update.message.reply_photo(
            photo=f,
            caption=(
                f"🔍 *Object Detection Result:*\n\n"
                f"Found *{len(detected)}* unique object(s):\n\n{label_lines}"
            ),
            parse_mode="Markdown"
        )
