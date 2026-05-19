"""
AI Vision MultiTool Telegram Bot
Main entry point
"""

import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from config import BOT_TOKEN
from handlers.caption_handler import handle_caption
from handlers.ocr_handler import handle_ocr
from handlers.background_handler import handle_background
from handlers.face_handler import handle_face
from handlers.object_handler import handle_object
from handlers.emotion_handler import handle_emotion
from handlers.cartoon_handler import handle_cartoon
from handlers.enhance_handler import handle_enhance

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user selected mode
user_modes = {}

MENU_TEXT = """
🤖 *AI Vision MultiTool Bot*

Choose a feature below, then send me an image!

🖼️ *Available Features:*
• /caption — AI Image Caption
• /ocr — Extract Text from Image
• /removebg — Remove Background
• /detectface — Detect Faces
• /detectobjects — Detect Objects
• /emotion — Detect Emotions
• /cartoon — Cartoon Effect
• /enhance — Enhance Image Quality

📌 *How to use:*
1. Tap a button or send a command
2. Upload your image
3. Get results instantly!
"""

# ─── Conversation Responses ───────────────────────────────────────────────────

CONVERSATIONS = {
    "greetings": {
        "triggers": ["hi", "hello", "hey", "hii", "helo", "howdy", "sup", "what's up", "whats up", "yo"],
        "responses": [
            "👋 Hey there! Great to see you!\n\nSend me an image and I'll work my AI magic on it! 🪄",
            "Hello! 😊 I'm VisionLab Bot — your AI-powered image assistant!\n\nTap /start to see what I can do!",
            "Hi! 👋 Ready to do some cool AI stuff with your images?\n\nUse /start to pick a feature!",
            "Hey hey! 🤖 What can I help you with today?\n\nSend /start to explore all my features!",
        ]
    },
    "who_are_you": {
        "triggers": ["who are you", "who r you", "who r u", "who are u", "whats your name",
                     "what's your name", "your name", "ur name", "what do i call you", "introduce yourself"],
        "responses": [
            "🤖 I'm *VisionLab Bot* — your smart AI image assistant!\n\nI can caption images, read text, remove backgrounds, detect faces & objects, analyze emotions, cartoonify photos, and enhance image quality.\n\nTap /start to try me out! 🚀",
            "I'm *VisionLab Bot* 🧠 — an AI-powered Telegram bot built with Computer Vision and Deep Learning.\n\nThink of me as your personal image analyst! 📸",
        ]
    },
    "what_are_you": {
        "triggers": ["what are you", "what r you", "what r u", "what are u", "what kind of bot",
                     "are you a bot", "are you ai", "are you human", "are you real", "are you robot"],
        "responses": [
            "🤖 I'm an *AI-powered Telegram Bot* built with:\n\n• 🧠 Deep Learning (BLIP, YOLOv8, DeepFace)\n• 👁️ Computer Vision (OpenCV)\n• 📝 OCR (EasyOCR)\n• 🎨 Image Processing (Pillow)\n\nNot human — but pretty smart! 😄",
            "I'm a bot, but a very capable one! 😎\n\nI combine multiple AI models to analyze, transform, and understand your images.\n\nTry /start to see what I can do!",
        ]
    },
    "what_do_you_do": {
        "triggers": ["what do you do", "what can you do", "what are your features", "your features",
                     "help me", "how can you help", "what are your abilities", "capabilities",
                     "what do u do", "what r ur features"],
        "responses": [
            "🌟 *Here's what I can do with your images:*\n\n🖼️ /caption — Describe any image using AI\n📝 /ocr — Extract text from images\n✂️ /removebg — Remove backgrounds\n👤 /detectface — Detect & count faces\n🔍 /detectobjects — Identify objects\n😊 /emotion — Read facial emotions\n🎨 /cartoon — Turn photos into cartoons\n✨ /enhance — Boost image quality\n\nJust tap /start to begin! 🚀",
        ]
    },
    "why_are_you": {
        "triggers": ["why are you here", "why were you made", "what is your purpose", "your purpose",
                     "why do you exist", "reason for your existence", "why r u here"],
        "responses": [
            "🎯 My purpose is to make *AI image processing accessible to everyone* — right inside Telegram!\n\nNo coding needed. No apps to install. Just send an image and get instant AI results. 🪄",
            "I was created to bring the power of *Computer Vision & Deep Learning* to your fingertips!\n\nWhether you need text extracted, backgrounds removed, or emotions detected — I've got you covered. 📸",
        ]
    },
    "how_are_you": {
        "triggers": ["how are you", "how r you", "how r u", "how are u", "how do you feel",
                     "how's it going", "hows it going", "you okay", "you good", "u good"],
        "responses": [
            "I'm doing great, thanks for asking! 😊 All my AI models are loaded and ready to go!\n\nHow about you? Got any images for me to analyze? 📸",
            "Running at full power! ⚡ All systems operational!\n\nReady to process your images whenever you are! 🚀",
            "Fantastic! 🤖✨ I just love analyzing images — it's literally what I was built for!\n\nSend me a photo and let's have some fun!",
        ]
    },
    "thank_you": {
        "triggers": ["thank you", "thanks", "thankyou", "thank u", "thx", "ty", "thnx", "thnks",
                     "thanks a lot", "thank you so much", "many thanks", "appreciate it",
                     "great job", "nice", "good job", "well done", "awesome", "amazing",
                     "brilliant", "excellent", "fantastic", "superb", "perfect", "wonderful",
                     "impressive", "incredible", "cool", "great"],
        "responses": [
            "You're welcome! 😊 Happy to help!\n\nWant to try another feature? Tap a button below! 👇",
            "Glad I could help! 🙌 Come back anytime you have an image to process!",
            "Anytime! 🤖✨ That's what I'm here for!\n\nFeel free to send another image!",
            "Thanks for the kind words! 🌟 It means a lot to this little bot! 😄",
        ]
    },
    "bye": {
        "triggers": ["bye", "goodbye", "good bye", "see you", "see ya", "cya", "later",
                     "take care", "goodnight", "good night", "gn", "ttyl", "talk later", "gtg"],
        "responses": [
            "Goodbye! 👋 Come back anytime you need AI image magic!\n\nHave a great day! ☀️",
            "See you later! 🤖💫 I'll be here whenever you need me!\n\nBye bye! 👋",
            "Take care! 😊 Don't forget — I'm just a message away for all your image needs!",
        ]
    },
    "greetings_time": {
        "triggers": ["good morning", "good evening", "good afternoon", "gm", "good day"],
        "responses": [
            "Good day to you too! ☀️ Hope you're having a wonderful time!\n\nReady to do some AI image magic? Tap /start! 🚀",
            "Hello and good day! 😊🌟\n\nWhenever you're ready, I'm here to help with your images!",
        ]
    },
    "who_made_you": {
        "triggers": ["who made you", "who created you", "who built you", "who is your developer",
                     "who is your creator", "who programmed you", "your developer", "your creator"],
        "responses": [
            "🛠️ I was built by a talented developer using:\n\n• Python 🐍\n• Hugging Face AI Models 🤗\n• YOLOv8 by Ultralytics\n• DeepFace, OpenCV, EasyOCR\n• python-telegram-bot\n\nA true full-stack AI project! 💪",
        ]
    },
    "love": {
        "triggers": ["i love you", "i like you", "you're great", "you are great", "you're awesome",
                     "you are awesome", "you're the best", "best bot", "love you", "luv u"],
        "responses": [
            "Aww, that's so sweet! 🥰 I love helping you with your images!\n\nLet's keep the good vibes going — send me a photo! 📸",
            "💙 Thanks! You're pretty awesome yourself!\n\nNow let's make some AI magic together! ✨",
        ]
    },
    "joke": {
        "triggers": ["tell me a joke", "say something funny", "make me laugh", "joke", "funny"],
        "responses": [
            "Why did the AI refuse to look at the photo? 📸\n\n...Because it had too many *pixels* of doubt! 😄",
            "Why did the robot go to school? 🤖\n\n...To improve its *neural* network! 😂",
            "What did the computer say to the camera? 📷\n\n...'I see you've been *framing* things differently!' 😄",
        ]
    },
    "what_is_ai": {
        "triggers": ["what is ai", "what is artificial intelligence", "explain ai", "tell me about ai",
                     "what is machine learning", "what is deep learning", "what is computer vision"],
        "responses": [
            "🧠 *Artificial Intelligence (AI)* is the simulation of human intelligence in machines!\n\nI use several AI techniques:\n\n• *Deep Learning* — multi-layer neural networks\n• *Computer Vision* — machines that see & understand images\n• *NLP* — machines that understand language\n• *Machine Learning* — systems that learn from data\n\nPretty cool, right? 😎",
        ]
    },
    "fallback": {
        "triggers": [],
        "responses": [
            "Hmm, I'm not sure I understood that 🤔\n\nI'm best at processing images! Try sending one, or tap /start to explore my features! 🚀",
            "I'm still learning to chat 😄 but I'm *really* good at image processing!\n\nSend me a photo or use /start to get started!",
            "That's a bit beyond my chat skills! 🤖\n\nBut send me an image and I'll impress you with my AI abilities! 📸",
        ]
    }
}


def get_conversation_response(text: str) -> str:
    """Match user text to a conversation category and return a random response."""
    text_lower = text.lower().strip()
    for category, data in CONVERSATIONS.items():
        if category == "fallback":
            continue
        for trigger in data["triggers"]:
            if trigger in text_lower:
                return random.choice(data["responses"])
    return random.choice(CONVERSATIONS["fallback"]["responses"])


# ─── Menu Helpers ─────────────────────────────────────────────────────────────

def build_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🖼️ Caption",      callback_data="caption"),
            InlineKeyboardButton("📝 OCR",           callback_data="ocr"),
        ],
        [
            InlineKeyboardButton("✂️ Remove BG",     callback_data="removebg"),
            InlineKeyboardButton("👤 Face Detect",   callback_data="detectface"),
        ],
        [
            InlineKeyboardButton("🔍 Objects",       callback_data="detectobjects"),
            InlineKeyboardButton("😊 Emotion",       callback_data="emotion"),
        ],
        [
            InlineKeyboardButton("🎨 Cartoon",       callback_data="cartoon"),
            InlineKeyboardButton("✨ Enhance",        callback_data="enhance"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def send_menu(update: Update):
    """Send the feature menu after an operation completes."""
    await update.message.reply_text(
        "✅ *Done! What would you like to do next?*\n\nPick a feature or send another image:",
        parse_mode="Markdown",
        reply_markup=build_menu_keyboard()
    )


# ─── Core Command Handlers ────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        MENU_TEXT, parse_mode="Markdown", reply_markup=build_menu_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        MENU_TEXT, parse_mode="Markdown", reply_markup=build_menu_keyboard()
    )


async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE, mode: str):
    chat_id = update.effective_chat.id
    user_modes[chat_id] = mode
    mode_info = {
        "caption":       ("🖼️", "Image Caption",     "Send me any image and I'll describe what's in it!"),
        "ocr":           ("📝", "OCR",                "Send me an image with text and I'll extract it!"),
        "removebg":      ("✂️", "Background Removal", "Send me an image and I'll remove the background!"),
        "detectface":    ("👤", "Face Detection",     "Send me an image and I'll detect all faces!"),
        "detectobjects": ("🔍", "Object Detection",   "Send me an image and I'll identify all objects!"),
        "emotion":       ("😊", "Emotion Detection",  "Send me a face image and I'll detect emotions!"),
        "cartoon":       ("🎨", "Cartoon Effect",     "Send me an image and I'll cartoonify it!"),
        "enhance":       ("✨", "Image Enhancement",  "Send me a low-quality image and I'll enhance it!"),
    }
    return mode_info.get(mode, ("🤖", mode, "Send me an image!"))


async def cmd_caption(update, context):
    e, n, p = await set_mode(update, context, "caption")
    await update.message.reply_text(f"{e} *{n} mode activated!*\n\n{p}", parse_mode="Markdown")

async def cmd_ocr(update, context):
    e, n, p = await set_mode(update, context, "ocr")
    await update.message.reply_text(f"{e} *{n} mode activated!*\n\n{p}", parse_mode="Markdown")

async def cmd_removebg(update, context):
    e, n, p = await set_mode(update, context, "removebg")
    await update.message.reply_text(f"{e} *{n} mode activated!*\n\n{p}", parse_mode="Markdown")

async def cmd_detectface(update, context):
    e, n, p = await set_mode(update, context, "detectface")
    await update.message.reply_text(f"{e} *{n} mode activated!*\n\n{p}", parse_mode="Markdown")

async def cmd_detectobjects(update, context):
    e, n, p = await set_mode(update, context, "detectobjects")
    await update.message.reply_text(f"{e} *{n} mode activated!*\n\n{p}", parse_mode="Markdown")

async def cmd_emotion(update, context):
    e, n, p = await set_mode(update, context, "emotion")
    await update.message.reply_text(f"{e} *{n} mode activated!*\n\n{p}", parse_mode="Markdown")

async def cmd_cartoon(update, context):
    e, n, p = await set_mode(update, context, "cartoon")
    await update.message.reply_text(f"{e} *{n} mode activated!*\n\n{p}", parse_mode="Markdown")

async def cmd_enhance(update, context):
    e, n, p = await set_mode(update, context, "enhance")
    await update.message.reply_text(f"{e} *{n} mode activated!*\n\n{p}", parse_mode="Markdown")


# ─── Inline Button Handler ────────────────────────────────────────────────────

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    mode = query.data
    user_modes[chat_id] = mode

    mode_info = {
        "caption":       ("🖼️", "Image Caption",     "Send me any image and I'll describe what's in it!"),
        "ocr":           ("📝", "OCR",                "Send me an image with text and I'll extract it!"),
        "removebg":      ("✂️", "Background Removal", "Send me an image and I'll remove the background!"),
        "detectface":    ("👤", "Face Detection",     "Send me an image and I'll detect all faces!"),
        "detectobjects": ("🔍", "Object Detection",   "Send me an image and I'll identify all objects!"),
        "emotion":       ("😊", "Emotion Detection",  "Send me a face image and I'll detect emotions!"),
        "cartoon":       ("🎨", "Cartoon Effect",     "Send me an image and I'll cartoonify it!"),
        "enhance":       ("✨", "Image Enhancement",  "Send me a low-quality image and I'll enhance it!"),
    }
    emoji, name, prompt = mode_info.get(mode, ("🤖", mode, "Send me an image!"))
    await query.edit_message_text(
        f"{emoji} *{name} mode activated!*\n\n{prompt}",
        parse_mode="Markdown"
    )


# ─── Text Conversation Handler ────────────────────────────────────────────────

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    response = get_conversation_response(text)
    await update.message.reply_text(
        response, parse_mode="Markdown", reply_markup=build_menu_keyboard()
    )


# ─── Image Router ─────────────────────────────────────────────────────────────

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    mode = user_modes.get(chat_id)

    if not mode:
        await update.message.reply_text(
            "⚠️ Please select a feature first!\n\nUse /start to see the menu.",
            reply_markup=build_menu_keyboard()
        )
        return

    await update.message.reply_text("⏳ Processing your image, please wait...")

    photo = update.message.photo[-1] if update.message.photo else update.message.document
    file = await context.bot.get_file(photo.file_id)

    import os
    input_path  = f"uploads/{chat_id}_input.jpg"
    output_path = f"outputs/{chat_id}_output"
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    await file.download_to_drive(input_path)

    try:
        if mode == "caption":
            await handle_caption(update, input_path)
        elif mode == "ocr":
            await handle_ocr(update, input_path)
        elif mode == "removebg":
            await handle_background(update, input_path, output_path)
        elif mode == "detectface":
            await handle_face(update, input_path, output_path)
        elif mode == "detectobjects":
            await handle_object(update, input_path, output_path)
        elif mode == "emotion":
            await handle_emotion(update, input_path)
        elif mode == "cartoon":
            await handle_cartoon(update, input_path, output_path)
        elif mode == "enhance":
            await handle_enhance(update, input_path, output_path)

        # ✅ Auto-show menu after every completed operation
        await send_menu(update)

    except Exception as e:
        logger.error(f"Error in mode {mode}: {e}")
        await update.message.reply_text(
            f"❌ Something went wrong: {str(e)}\n\nMake sure all dependencies are installed."
        )
        await send_menu(update)


# ─── App Entry Point ──────────────────────────────────────────────────────────

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",          start))
    app.add_handler(CommandHandler("help",           help_command))
    app.add_handler(CommandHandler("caption",        cmd_caption))
    app.add_handler(CommandHandler("ocr",            cmd_ocr))
    app.add_handler(CommandHandler("removebg",       cmd_removebg))
    app.add_handler(CommandHandler("detectface",     cmd_detectface))
    app.add_handler(CommandHandler("detectobjects",  cmd_detectobjects))
    app.add_handler(CommandHandler("emotion",        cmd_emotion))
    app.add_handler(CommandHandler("cartoon",        cmd_cartoon))
    app.add_handler(CommandHandler("enhance",        cmd_enhance))

    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_image))

    # Text handler must be LAST
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 AI Vision MultiTool Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()