"""
Handler: Emotion Detection using DeepFace
"""
from deepface import DeepFace
import cv2


EMOTION_EMOJIS = {
    "happy":    "😊",
    "sad":      "😢",
    "angry":    "😠",
    "fear":     "😨",
    "surprise": "😲",
    "disgust":  "🤢",
    "neutral":  "😐",
}


async def handle_emotion(update, image_path: str):
    try:
        result = DeepFace.analyze(
            img_path=image_path,
            actions=["emotion"],
            enforce_detection=True,
            silent=True
        )

        # DeepFace returns a list when multiple faces found
        if isinstance(result, list):
            faces = result
        else:
            faces = [result]

        response_lines = [f"😊 *Emotion Detection Result:*\n\n*{len(faces)} face(s) analyzed:*\n"]

        for i, face in enumerate(faces, 1):
            emotions = face["emotion"]
            dominant = face["dominant_emotion"]
            emoji = EMOTION_EMOJIS.get(dominant, "🙂")

            # Top 3 emotions
            top3 = sorted(emotions.items(), key=lambda x: -x[1])[:3]
            emotion_lines = "\n".join(
                [f"  • {e.title()}: {v:.1f}%" for e, v in top3]
            )

            response_lines.append(
                f"*Face {i}:*\n"
                f"{emoji} Dominant: *{dominant.title()}*\n"
                f"{emotion_lines}\n"
            )

        await update.message.reply_text(
            "\n".join(response_lines),
            parse_mode="Markdown"
        )

    except ValueError as e:
        if "Face could not be detected" in str(e):
            await update.message.reply_text(
                "😊 *Emotion Detection Result:*\n\n"
                "⚠️ No face detected. Please send a clear photo of a human face.",
                parse_mode="Markdown"
            )
        else:
            raise
