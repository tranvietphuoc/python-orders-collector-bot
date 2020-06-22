from flask import Flask, request, abort
from werkzeug.exceptions import HTTPException
import json
from bot import bot
import telebot
from config import SECRET_KEY
import logging
from logging import Formatter, FileHandler


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
WEBHOOK_URL = f"/{bot.token}"


@app.errorhandler(HTTPException)
def handle_exception(e):
    """
    Generic exception handler.
    Return JSON data.
    """
    response = e.get_response()
    response.data = json.dumps(
        {"code": e.code, "name": e.name, "description": e.description,}
    )
    response.content_type = "application/json"
    return response


@app.route(WEBHOOK_URL, methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        # print(PROJECT)
        return "OK", 200
    return abort(403)


if __name__ == "__main__":
    file_handler = FileHandler("app.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s %(username)s: %(message)s")
    )
    app.logger.addHandler(file_handler)
    app.run(debug=True)
