from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN", "Y7748358859:AAH9LY-1b7AwBKxOTocvvS9EYP3LApkG0Uo")
app = Flask(__name__)

# Telegram bot setup
bot_app = ApplicationBuilder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! 👋 This bot is running on Vercel!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/start - Greet\n/help - Show help")

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("help", help))

# Flask route for Telegram webhook
@app.route("/", methods=["GET"])
def home():
    return "✅ Telegram Bot Running on Vercel"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    asyncio.run(bot_app.process_update(update))
    return "ok"

# Set webhook automatically when deployed
async def set_webhook():
    url = os.getenv("VERCEL_URL", "")
    if url:
        webhook_url = f"https://{url}/{TOKEN}"
        await bot_app.bot.set_webhook(webhook_url)
        print("Webhook set to:", webhook_url)

asyncio.run(set_webhook())
