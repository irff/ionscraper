__author__ = 'Kandito Agung, Zaka Zaidan'
__version__ = 'v1.0.0'

import lxml.etree
import lxml.html
from lxml.html.clean import Cleaner
import re
from datetime import datetime

def html_to_string(string_data):
    string_data = clear_script(string_data)
    data = lxml.html.fromstring(string_data)
    data = lxml.html.tostring(data, method="text", encoding=unicode)
    return re.sub(' +',' ',data)
    
def clear_script(string_data):
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True

    data = lxml.html.fromstring(string_data)
    return lxml.html.tostring(cleaner.clean_html(data))

def item_merge(items):
    result = ""
    for i in items:
        result = result + html_to_string(i)
    return result

def clear_item(item):
    return item.encode('ascii','ignore').replace("\xe2","-").replace("\n","").replace("\t","").replace("\r","")

def tempo_komunika_date(plain_string):
    plain_string = clear_item(plain_string)
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

def formatted_date_with_second(year,month,day,hour,minute, second):
    datetime_string = ""
    datetime_string = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second + ".000"
    return datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S.%f")

def get_month(ms):
    if ms in ["Januari","Jan","January"]:
        return "01"
    elif ms in ["Februari","Feb","February"]:
        return "02"
    elif ms in ["Maret","Mar","March"]:
        return "03"
    elif ms in ["April","Apr"]:
        return "04"
    elif ms in ["Mei","May"]:
        return "05"
    elif ms in ["Juni","Jun","June"]:
        return "06"
    elif ms in ["Juli","Jul","July"]:
        return "07"
    elif ms in ["Agustus","Agt","Aug","August"]:
        return "08"
    elif ms in ["September","Sep","Sept"]:
        return "09"
    elif ms in ["Oktober","Okt","Oct","October"]:
        return "10"
    elif ms in ["November","Nov"]:
        return "11"
    elif ms in ["Desember","Des","Dec","December"]:
        return "12"