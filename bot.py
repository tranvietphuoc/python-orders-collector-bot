import telebot
import time
from config import TOKEN, PROJECT
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import datetime


# authorize app to google app as web server
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "./ggapi_key.json", scope
)
gc = gspread.authorize(credentials)  # create a gspread authorize


bot = telebot.TeleBot(TOKEN, threaded=True)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "welcome!")
    bot.send_message(message.chat.id, "hi there!")


@bot.message_handler(func=lambda m: True)
def order_handler(message):
    if message.chat.type == "group" or message.chat.type == "private":
        print(message)

        matching_pattern = r"((^[A-Z]{2,}[A-Z0-9]+)|(^[0-9]{8,}[A-Z0-9]+))"
        wks = gc.open("Turning").sheet1
        # these column below must have the same len
        list_dates = wks.col_values(1)
        list_users = wks.col_values(2)
        list_orders = wks.col_values(3)

        # get list of orders from message.text
        list_of_orders = [
            element[0]
            for element in re.findall(matching_pattern, message.text, re.MULTILINE)
        ]
        print(list_of_orders)

        for i, order in enumerate(list_orders, 1):
            try:
                if order:  # string is not None
                    continue
                else:
                    for j, element in enumerate(list_of_orders):
                        wks.update_cell(i + j, 3, element)
                        wks.update_cell(
                            i + j, 1, str(datetime.fromtimestamp(message.date))
                        )
                        wks.update_cell(
                            i + j, 2, message.from_user.username,
                        )
            except AttributeError as e:
                print(e)

            break


bot.remove_webhook()
time.sleep(1)  # idling
bot.set_webhook(url=f"https://order-collector.herokuapp.com/{bot.token}")
# bot.set_webhook(url=f"https://60e3fd470038.ngrok.io/{bot.token}")
