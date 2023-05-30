import datetime
import pytz
import pandas as pd

def get_time_now_with_zone(dateFormat,timeZone):
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    # Lấy giờ hiện tại theo giờ UTC+7
    utc_7 = pytz.timezone(timeZone)
    now_utc_7 = now_utc.astimezone(utc_7)
    return  datetime.datetime.strptime(now_utc_7.strftime(dateFormat),dateFormat)
    
def check_date_type(str_date):
        try:
            if (pd.isnull(str_date) or pd.isna(str_date) or str_date=='' ):
                return True
            date=pd.to_datetime(str_date)
            if (pd.isnull(date)):
                return False
            return True
        except:
            return False    
    
def is_valid_date(formate_date,date_string):
    date_string=date_string.strip()
    try:
        date_obj = datetime.datetime.strptime(date_string, formate_date)
        return True
    except ValueError:
        return False

def change_time_to_int(time):
    integer_value = int(time.strftime('%Y%m%d%H%M%S'))
    return integer_value

def change_int_to_time(value):
    return

#print(pytz.all_timezones)
print(get_time_now_with_zone('%d-%m-%Y %H:%M:%S','Europe/London'))