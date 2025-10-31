from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    print(update)
    return {"ok": True}

@app.route("/", methods=["GET"])
def index():
    return "Bot is running"
