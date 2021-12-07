from flask import Flask, request
import telegram
import os


TOKEN = os.environ.get("TOKEN")
URL = os.environ.get("URL")

bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


@app.route("/{}".format(TOKEN), methods=["POST"])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode("utf-8").decode()
    print("got text message :", text)

    bot.sendMessage(chat_id=chat_id, text="oi eu sou um robô", reply_to_message_id=msg_id)

    return "ok"


@app.route("/setwebhook", methods=["GET", "POST"])
def set_webhook():
    print(URL)
    print(TOKEN)
    webhook = bot.setWebhook("{URL}{HOOK}".format(URL=URL, HOOK=TOKEN))
    if webhook:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route("/")
def index():
    return "."


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True, threaded=True)
