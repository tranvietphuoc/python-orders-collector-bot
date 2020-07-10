import telebot
import time
from config import TOKEN, PROJECT
import gspread
from gspread.exceptions import APIError
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


bot = telebot.TeleBot(TOKEN, threaded=False)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "welcome! i'm a bot")
    bot.send_message(message.chat.id, "my pleasure is reserving you <3")


@bot.message_handler(func=lambda m: True)
def order_handler(message):

    # open sheet
    sh = gc.open("Turning")
    if message.chat.type == "group" or message.chat.type == "private":
        print(message)
        print("-----")

        # read each sheet
        wks_quay_dau = sh.worksheet("quay_dau")
        wks_ra_kien = sh.worksheet("ra_kien")

        # read data from group and write to sheets
        if message.chat.title == "hang chieu ra kien":
            write_to_sheet(wks_ra_kien, message)
        else:
            write_to_sheet(wks_quay_dau, message)


def write_to_sheet(wks, message):
    """Write filtered data to sheet"""
    # orders matching pattern
    matching_pattern = (
        r"((^[A-Z]{2,}[A-Z0-9]+)|(^[0-9]{8,}[A-Z0-9]+)|(^[0-9]{1}[A-Z0-9]+))"
    )
    # read order column of google sheet
    list_orders = wks.col_values(3)
    # get list of orders from message
    list_of_orders = [
        element[0]
        for element in re.findall(matching_pattern, message.text, re.MULTILINE)
    ]

    # write to google sheet
    for i, element in enumerate(list_of_orders, 1):
        try:
            if element not in list_orders:
                wks.update_cell(
                    len(list_orders) + i, 1, str(datetime.fromtimestamp(message.date))
                )
                wks.update_cell(len(list_orders) + i, 2, message.from_user.username)
                wks.update_cell(len(list_orders) + i, 3, element)
        except AttributeError as attr:
            print(attr)
            break
        except APIError:
            print("Limit write request per 100 seconds!")
            time.sleep(100)
            continue
    print("Done!")


def check_state(message):
    """Check the state of orders."""
    pass


bot.remove_webhook()
time.sleep(1)  # idling
bot.set_webhook(url=f"https://{PROJECT}.herokuapp.com/{bot.token}")
# bot.set_webhook(url=f"https://c7fe0e43375b.ngrok.io/{bot.token}")
