import datetime
import pytz

def scanned_time():
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    today = now.strftime("%Y/%m/%d")
    return today