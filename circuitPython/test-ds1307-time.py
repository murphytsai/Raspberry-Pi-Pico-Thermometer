import time
from urtc import DS1307
import board
import busio
import adafruit_ds1307

i2c_rtc = busio.I2C (scl=board.GP3, sda=board.GP2)

rtc = adafruit_ds1307.DS1307(i2c_rtc)
help(rtc.datetime)

if False:
    # first time to set time
    year = int(input("Year : "))
    month = int(input("month (Jan --> 1 , Dec --> 12): "))
    date = int(input("date : "))
    day = int(input("day (1 --> monday , 2 --> Tuesday ... 0 --> Sunday): "))
    hour = int(input("hour (24 Hour format): "))
    minute = int(input("minute : "))
    second = int(input("second : "))
    now = (year,month,date,day,hour,minute,second,0)
    rtc.datetime(now)

while True:
    t = rtc.datetime
    print(
        "The date is {} {}/{}/{}".format(
           t.tm_wday, t.tm_mday, t.tm_mon, t.tm_year
        )
    )
    #print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))    
    time_str = "{}/{}/{} {:02}:{:02}".format(t.tm_mon, t.tm_mday, t.tm_year, t.tm_hour, t.tm_min)
    print(time_str)
    time.sleep(1)
    