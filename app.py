from flask import Flask, request, abort
from werkzeug.exceptions import HTTPException
import json
from bot import bot
from telebot.types import Update
from config import SECRET_KEY
from datetime import datetime


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
        {"code": e.code, "name": e.name, "description": e.description}
    )
    response.content_type = "application/json"
    return response


@app.route(WEBHOOK_URL, methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        print(request.headers)
        print(datetime.now())
        # length = request.headers["content-length"]
        json_string = request.get_data().decode("utf-8")
        update = Update.de_json(json_string)
        print(update)
        bot.process_new_updates([update])
        return "OK", 200
    return abort(403)
