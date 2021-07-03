import telebot
import time
from config import TOKEN, PROJECT
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
from datetime import datetime
import pandas as pd
from df2gspread import df2gspread as df2g
from utils import save_to_csv, save_to_sheet, extract_args


# authorize app to google app as web server
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
credentials = SAC.from_json_keyfile_name("./ggapi_key.json", scopes=SCOPES)
gc = gspread.authorize(credentials)  # create a gspread authorize
# identify spreadsheets
SPREADSHEET_ID = "1_UlAs1Ed6rxl1TNM8Vv2fnEsRT61BOWTVzCMtd1hwME"
INVENTORY_NAME = "KiemKho_bot"
ROTATION_NAME = "QuayDau_bot"
# initialize bot object
bot = telebot.TeleBot(TOKEN, threaded=False)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    """Send welcome when type /start."""

    bot.send_message(
        message.chat.id,
        "Xin chào. Mình là bot. Gõ /help để biết thêm chi tiết cách sử dụng. Happy working!",
    )


@bot.message_handler(commands=["about"])
def send_about(message):
    """Send about."""

    about = """
    Introduction myself
    Name: L. Baby bot
    Version: 2.0
    Platform: Telegram
    Author: Tran Viet Phuoc
    Email: phuoc.finn@gmail.com
    Github: https://github.com/tranvietphuoc
    """
    bot.send_message(message.chat.id, about)


@bot.message_handler(commands=["help"])
def send_help(message):
    """Send help message."""

    mess = """
    Actived commands để tương tác với bot:
    /start: Hello world
    /help: Hướng dẫn sử dụng bot.
    /about: Giới thiệu bot.
    /to_csv <YYYY-mm-dd>: Xuất file csv với ngày cụ thể theo định dạng trên.
    /to_sheet <YYYY-mm-dd>: Đẩy dữ liệu trong file csv đã lưu lên google sheets có sẵn.
    /backlog: Show link dẫn tới tool export backlog.
    """
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=["to_csv"])
def send_csv(message):
    """Send csv file to user."""
    
    args = extract_args(message.text)
    print(args)
    file_uri = f"./assets/csv/kiem_kho_{str(arg)}.csv"
    try:
        with open(file_uri, mode="r") as file_obj:
            bot.send_document(
                message.chat.id, file_obj, caption="Rất hân hạnh được phục vụ."
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id, f"File ngày {args} không tồn tại. Vui lòng thử lại"
        )


@bot.message_handler(commands=["to_sheet"])
def to_sheet(message):
    """Send data from csv at ./assets/csv/ folder to google sheets"""

    arg = extract_args(message.text)
    file_uri = f"./assets/csv/kiem_kho_{str(arg)}.csv"
    try:
        COLS = ["Date", "User", "OrderCodes"]
        df_csv = pd.read_csv(file_uri, names=COLS)
        print(df_csv)
        # then upload new data to sheets
        bot.send_message(message.chat.id, "Đang xử lý...")
        # update new data to sheets
        df2g.upload(
            df_csv,
            SPREADSHEET_ID,
            INVENTORY_NAME,
            credentials=credentials,
            row_names=False,
            col_names=True,
            clean=True,
        )
        bot.send_message(message.chat.id, "Đã push lên google sheets.")
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            f"File ngày {arg} không tồn tại trên hệ thống. Vui lòng thử lại",
        )


@bot.message_handler(commands=["backlog"])
def send_backlog(message):
    bot.send_message(
        message.chat.id,
        f"Tới trang https://ops-exporting.herokuapp.com để export file backlog.",
    )


@bot.message_handler(func=lambda m: True)
def collecting_handler(message):
    """Collect orders"""

    # open sheet
    sh = gc.open_by_key(SPREADSHEET_ID)
    if message.chat.type == "group" or message.chat.type == "private":
        print(message)
        # read each sheet
        wks_quay_dau = sh.worksheet(ROTATION_NAME)

        # read data from group and write to sheets
        if message.chat.title == "KIỂM KHO QUẬN 7" or message.chat.title == "test":
            file_uri = f"./assets/csv/kiem_kho_{datetime.fromtimestamp(message.date).strftime('%Y-%m-%d')}.csv"
            # save text to csv file
            save_to_csv(file_uri, message)
            bot.send_message(message.chat.id, "Đã lưu vào file csv.")
        elif message.chat.title == "Đơn Quay Đầu - Bắn Kiểm Thiếu":
            # save to Quaydau_bot sheet
            save_to_sheet(wks_quay_dau, message)
            bot.send_message(
                message.chat.id,
                "Mã đơn hàng đã được lưu vào google sheets. Các anh chị có tên vui lòng hoàn tất đơn quay đầu trong ngày. Thanks.",
            )
        else:
            bot.send_message(message.chat.id, "Nothing to do...")


bot.remove_webhook()
time.sleep(1)  # idling
# heroku server
bot.set_webhook(url=f"https://{PROJECT}.herokuapp.com/{bot.token}")
## test with local server
# bot.set_webhook(url=f"https://ce7a65ab604c.ngrok.io/{bot.token}")
