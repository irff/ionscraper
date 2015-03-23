__author__ = 'Kandito Agung'

import lxml.etree
import lxml.html
from datetime import datetime

def html_to_string(string_data):
    data = lxml.html.fromstring(string_data)
    return lxml.html.tostring(data, method="text", encoding=unicode)

def item_merge(items):
    result = ""
    for i in items:
        result = result + html_to_string(i)
    return result

def last_item(items):
    result = ""
    for i in items:
        result = items
    return result

def tempo_komunika_date(plain_string):
    plain_string = plain_string.replace("\n","").replace("\t","")
    day = plain_string[:2]
    month = get_month(plain_string[2:-4])
    year =  plain_string[-4:]
    hour = "00"
    minute = "00"
    return formatted_date(year,month,day,hour,minute)

def formatted_date(year,month,day,hour,minute):
    datetime_string = ""
    datetime_string = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":00.000"
    return datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S.%f")

def get_month(ms):
    if ms == "Januari" or ms == "Jan":
        return "01"
    elif ms == "Februari" or ms == "Feb":
        return "02"
    elif ms == "Maret" or ms == "Mar":
        return "03"
    elif ms == "April" or ms == "Apr":
        return "04"
    elif ms == "Mei" or ms == "May":
        return "05"
    elif ms == "Juni" or ms == "Jun":
        return "06"
    elif ms == "Juli" or ms == "Jul":
        return "07"
    elif ms == "Agustus" or ms == "Agt":
        return "08"
    elif ms == "September" or ms == "Sep":
        return "09"
    elif ms == "Oktober" or ms =="Okt":
        return "10"
    elif ms == "November" or ms == "Nov":
        return "11"
    elif ms == "Desember" or ms == "Des":
        return "12"