from machine import Pin, I2C
import time
import utime
from urtc import DS1307
r=machine.RTC()

i2c_rtc = I2C(1, sda=Pin(2), scl=Pin(3), freq = 400000)
rtc = DS1307(i2c_rtc)
print(rtc.datetime())
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
    (year,month,date,day,hour,minute,second,p1)=rtc.datetime()
    utime.sleep(1)
    print(rtc.datetime())
    