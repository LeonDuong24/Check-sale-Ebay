import datetime
import pytz
import pandas as pd

def get_time_now_with_zone(timeZone):
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    # Lấy giờ hiện tại theo giờ UTC+7
    utc_7 = pytz.timezone(timeZone)
    now_utc_7 = now_utc.astimezone(utc_7)
    str_now_utc_7=now_utc_7.strftime("%Y%m%d%H%M%S")
    return  datetime.datetime.strptime(str_now_utc_7,"%Y%m%d%H%M%S")

def change_str_to_time(string, dateFormat):
    return  datetime.datetime.strptime(string,dateFormat)

def change_date_format(date,dateFormat):
    return date.strftime(dateFormat)
    
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

def change_time_to_int(time,formate_date):
    datetime_obj = datetime.datetime.strptime(time, formate_date)
    integer_value = int(datetime_obj.strftime('%Y%m%d%H%M%S'))
    return integer_value


#print(pytz.all_timezones)
# print(change_date_format(get_time_now_with_zone('America/New_York'),'%Y%m%d%H%M%S'))
# print(change_date_format(get_time_now_with_zone('America/New_York')+ datetime.timedelta(hours=24),'%Y%m%d%H%M%S'))
#print(get_time_now_with_zone("%Y%m%d%H%M%S",'America/New_York')+ datetime.timedelta(hours=2))
#print(change_time_to_int('2023 06 07 05-50-30','%Y %m %d %H-%M-%S'))