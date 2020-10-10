import numpy as np
import re
from datetime import datetime
import csv
from gspread.exceptions import APIError
import time


def convert_datetime_to_date(d):
    """Convert datetime to only date."""
    try:
        return d.strftime("%Y-%m-%d")
    except ValueError:
        return np.nan


def check_spreadsheets_type(message):
    try:
        return (
            message.document.mime_type
            == "application/vnd.openxmlformats-officedocument/spreadsheetml.sheet"
        )
    except AttributeError:
        return False


def extract_args(args):
    """Extract the argument of command."""
    try:
        return args.split()[1]
    except IndexError:
        print("Only has one argument. Check it again.")


def save_to_sheet(wks, message):
    """Write filtered data to sheet"""
    # orders matching pattern
    matching_pattern = (
        r"((^[A-Z]{2,}[A-Z0-9]{3,})|(^[0-9]{8,}[A-Z0-9]+)|(^[0-9]{1}[A-Z0-9]+))"
    )
    # read order column of google sheet
    elements_from_sheet = wks.col_values(3)
    # get list of orders from message
    orders_from_message = [
        element[0]
        for element in re.findall(matching_pattern, message.text, re.MULTILINE)
    ]

    # write to google sheet
    for i, order in enumerate(orders_from_message, 1):
        try:
            if order not in elements_from_sheet and len(order) > 7:
                wks.update_cell(
                    len(elements_from_sheet) + i,
                    1,
                    str(datetime.fromtimestamp(message.date).strftime("%Y-%m-%d")),
                )
                wks.update_cell(
                    len(elements_from_sheet) + i, 2, message.from_user.username
                )
                wks.update_cell(len(elements_from_sheet) + i, 3, order)
                # Google Sheets API has a limit 100 requests per 100 seconds per user.
                # Limits for reads and writes are tracked separately. There is no daily usage limit.
                time.sleep(1)
        except AttributeError as attr:
            print(attr)
            break
        except APIError:
            print("Limit write request per 100 seconds!")
            continue
    print("Done!")


def save_to_csv(file_uri, message):
    """export to csv file."""
    matching_pattern = (
        r"((^[A-Z]{2,}[A-Z0-9]{3,})|(^[0-9]{8,}[A-Z0-9]+)|(^[0-9]{1}[A-Z0-9]+))"
    )
    # make a list of order codes
    orders_of_message = [
        element[0]
        for element in re.findall(matching_pattern, message.text, re.MULTILINE)
    ]
    # write csv file and save to assets folder
    with open(file_uri, mode="a") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        for order in orders_of_message:
            csv_writer.writerow(
                [
                    datetime.fromtimestamp(message.date).strftime("%Y-%m-%d"),
                    message.from_user.username,
                    order,
                ]
            )
