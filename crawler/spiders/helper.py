__author__ = 'Kandito Agung'

import lxml.etree
import lxml.html
from datetime import datetime

def html_to_string(string_data):
    data = lxml.html.fromstring(string_data)
    return lxml.html.tostring(data, method="text", encoding=unicode)


def kompas_date(plain_string):
    if plain_string == None:
        return None

    plain_string = html_to_string(plain_string)

    string_date = plain_string[plain_string.find(",") + 2 : plain_string.find("|") - 1]
    string_time = plain_string[plain_string.find("|") + 2 : len(plain_string)]

    date = string_date.split(" ")
    day = date[0]
    year = date[2]

    ms = date[1]
    month = ""
    if ms == "Januari":
        month = "01"
    elif ms == "Februari":
        month = "02"
    elif ms == "Maret":
        month = "03"
    elif ms == "April":
        month = "04"
    elif ms == "Mei":
        month = "05"
    elif ms == "Juni":
        month = "06"
    elif ms == "Juli":
        month = "07"
    elif ms == "Agustus":
        month = "08"
    elif ms == "September":
        month = "09"
    elif ms == "Oktober":
        month = "10"
    elif ms == "November":
        month = "11"
    elif ms == "Desember":
        month = "12"

    hour = string_time[0:2]
    minute = string_time[3:5]

    datetime_string = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":00.000"
    return datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S.%f")
