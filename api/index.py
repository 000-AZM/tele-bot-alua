from flask import Flask, request
import telegram
import os

# --- Telegram Setup ---
TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

# --- Flask App ---
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "✅ Bot is alive on Vercel!"

@app.route('/api/index', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return "Webhook running!"
    try:
        data = request.get_json(force=True)
        update = telegram.Update.de_json(data, bot)

        if update.message:
            chat_id = update.message.chat.id
            text = update.message.text
            bot.send_message(chat_id=chat_id, text=f"You said: {text}")
        return "ok"
    except Exception as e:
        print("Error:", e)
        return "error", 500

if __name__ == "__main__":
    app.run(debug=True)
