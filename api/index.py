from flask import Flask, request
import os
import telegram

# --- Telegram Setup ---
TOKEN = os.environ.get("BOT_TOKEN") or "YOUR_BOT_TOKEN"
bot = telegram.Bot(token=TOKEN)

# --- Flask App ---
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is alive on Vercel!"

@app.route("/api/index", methods=["POST"])
def webhook():
    try:
        # Parse Telegram update
        data = request.get_json(force=True)
        update = telegram.Update.de_json(data, bot)

        # Handle normal messages
        if update.message and update.message.text:
            chat_id = update.message.chat.id
            text = update.message.text

            # Respond to /start
            if text == "/start":
                bot.send_message(chat_id=chat_id, text="👋 Hello! I'm running on Vercel.")
            else:
                bot.send_message(chat_id=chat_id, text=f"You said: {text}")

        # Always return ok to Telegram
        return "ok"
    except Exception as e:
        print("Error:", e)
        # Prevent Telegram from retrying endlessly
        return "ok"

if __name__ == "__main__":
    app.run(debug=True)
