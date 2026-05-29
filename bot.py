import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "📥 Havola yuboring, video yuklab beraman!\n\n"
        "✅ YouTube\n"
        "✅ TikTok\n"
        "✅ Instagram"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not ("youtube.com" in url or "youtu.be" in url or "tiktok.com" in url or "instagram.com" in url):
        await update.message.reply_text("❌ YouTube, TikTok yoki Instagram havolasini yuboring!")
        return
    msg = await update.message.reply_text("⏳ Yuklanmoqda...")
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
        with open(file_path, 'rb') as f:
            await update.message.reply_video(video=f, caption=f"🎬 {info.get('title','Video')}")
        os.remove(file_path)
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ Xatolik: {str(e)[:200]}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    logger.info("Bot ishga tushdi!")
    app.run_polling()
