import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("8501178349:AAGvRQWnWAYeDCtMghJNZiJMs5qcL-43ALk")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "📥 Video yuklab olish uchun havola yuboring:\n\n"
        "✅ YouTube\n"
        "✅ TikTok\n"
        "✅ Instagram\n\n"
        "Havolani yuboring, men yuklab beraman! 🚀"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not ("youtube.com" in url or "youtu.be" in url or "tiktok.com" in url or "instagram.com" in url):
        await update.message.reply_text("❌ Faqat YouTube, TikTok yoki Instagram havolasini yuboring!")
        return

    msg = await update.message.reply_text("⏳ Yuklanmoqda, kuting...")

    ydl_opts = {
        'format': 'best[filesize<50M]/best',
        'outtmpl': '/tmp/%(id)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await msg.edit_text("📤 Yuborilmoqda...")
        
        with open(file_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=f"🎬 {info.get('title', 'Video')}"
            )
        
        os.remove(file_path)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ Xatolik: {str(e)[:200]}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("Bot ishga tushdi ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
