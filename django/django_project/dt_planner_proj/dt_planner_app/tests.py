import datetime

start_date_str = '12/23/2020 12:27'
start_date = datetime.datetime.strptime(start_date_str, '%m/%d/%Y %H:%M')

print(start_date)
