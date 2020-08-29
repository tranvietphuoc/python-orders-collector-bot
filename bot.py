import telebot
import time
from config import TOKEN, PROJECT, SPREADSHEETS_ID
import gspread
from gspread.exceptions import APIError
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import datetime
import csv


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


@bot.message_handler(commands=["start"])
def send_welcome(message):
    """send welcome when type /start."""
    bot.send_message(message.chat.id, "Tôi là bot. Tôi đang đợi lệnh từ bạn...")


@bot.message_handler(commands=['help'])
def send_help(message):
    mess = """
    /to_csv <YYYY-mm-dd> - Xuất file csv với ngày cụ thể theo định dạng trên.\n
    """
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['to_csv'])
def send_csv(message):
    arg = extract_arg(message.text)
    print(arg)
    try:
        file = open(f"./assets/csv/kiem_kho_{str(arg)}.csv", 'r')
        bot.send_document(message.chat.id, file)
        file.close()
    except FileNotFoundError:
        bot.send_message(message.chat.id, f'File ngày {arg} không tồn tại. Vui lòng thử lại')


@bot.message_handler(func=lambda m: True)
def order_handler(message):
    """Handle orders"""
    # open sheet
    sh = gc.open_by_key('16PAFFaZOTfHczYcpmU6uu7Gtq_iCb5MTgCnUKlK5pP8')
    if message.chat.type == "group" or message.chat.type == "private":
        print(message)
        print("-----")

        # read each sheet
        wks_quay_dau = sh.worksheet('quay_dau')

        # read data from group and write to sheets
        if message.chat.title == "KIỂM KHO QUẬN 7":
            # write_to_sheet(wks_kiem_kho, message)
            to_csv(message)
            bot.send_message(message.chat.id, "Đã lưu vào file csv.")
        elif message.chat.title == 'Đơn Quay Đầu - Bắn Kiểm Thiếu':
            to_sheets(wks_quay_dau, message)
            bot.send_message(message.chat.id, 'Lưu hoàn tất, vui lòng check google sheets mỗi ngày!')
        else:
            bot.send_message(message.chat.id, '^^')


def to_csv(message):
    """export to csv file."""
    matching_pattern = r'((^[A-Z]{2,}[A-Z0-9]{3,})|(^[0-9]{8,}[A-Z0-9]+)|(^[0-9]{1}[A-Z0-9]+))'
    list_orders_of_message = [
        element[0] for element in re.findall(matching_pattern, message.text, re.MULTILINE)
    ]

    with open(f"./assets/csv/kiem_kho_{datetime.fromtimestamp(message.date).strftime('%Y-%m-%d')}.csv", mode='a') as f:
        csv_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for e in list_orders_of_message:
            csv_writer.writerow(
                [datetime.fromtimestamp(message.date).strftime('%Y-%m-%d'), message.from_user.username, e]
            )


def to_sheets(wks, message):
    """Write filtered data to sheet"""
    # orders matching pattern
    matching_pattern = (
        r"((^[A-Z]{2,}[A-Z0-9]{3,})|(^[0-9]{8,}[A-Z0-9]+)|(^[0-9]{1}[A-Z0-9]+))"
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
                    len(list_orders) + i,
                    1,
                    str(datetime.fromtimestamp(message.date).strftime('%Y-%m-%d'))
                )
                wks.update_cell(len(list_orders) + i, 2, message.from_user.username)
                wks.update_cell(len(list_orders) + i, 3, element)
                # Google Sheets API has a limit 100 requests per 100 seconds per user. Limits for reads and writes are tracked separately. There is no daily usage limit.
                time.sleep(1)
        except AttributeError as attr:
            print(attr)
            break
        except APIError:
            print("Limit write request per 100 seconds!")
            continue
    print("Done!")


def extract_arg(arg):
    """Extract the argument of command."""
    try:
        return arg.split()[1]
    except IndexError:
        print('Only has one argument. Check it again.')


bot.remove_webhook()
time.sleep(1)  # idling
bot.set_webhook(url=f"https://{PROJECT}.herokuapp.com/{bot.token}")
# bot.set_webhook(url=f"https://3b80392e556e.ngrok.io/{bot.token}")
