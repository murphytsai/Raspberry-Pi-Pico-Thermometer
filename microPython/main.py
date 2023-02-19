from machine import Pin, I2C, RTC
from ssd1306 import SSD1306_I2C
import onewire
import ds18x20
import time
import utime
import binascii
from urtc import DS1307
r=machine.RTC()

# clock i2c
i2c_rtc = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
rtc = DS1307(i2c_rtc)
# lcd i2c
i2c_lcd = I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 32, i2c_lcd)
oled.text("Ready... ",12,8)
oled.show()

onboard_led = Pin(25, Pin.OUT)
onboard_led.on()

ds_pin = Pin(16)

ds18b20_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

sensors = ds18b20_sensor.scan()

print('Found DS18B20: ', sensors)

while True:
    onboard_led.on()
    oled.fill(0)
    ds18b20_sensor.convert_temp()
    time.sleep_ms(750)
    temp = ""
    cnt = 0
    temp = []
    if not sensors:
        sensors = ds18b20_sensor.scan()
        print('Found DS18B20: ', sensors)

    for device in sensors:
        cnt += 1
        if cnt > 3:
            cnt=0
        s = binascii.hexlify(device)
        readable_string = s.decode('ascii')
        temp.append(str(round(ds18b20_sensor.read_temp(device),1)))

    (year,month,date,day,hour,minute,second,p1)=rtc.datetime()
    time_str = "{}/{}/{} {:02}:{:02}".format(month, date, year, hour, minute)
    oled.text(time_str, 0,0)
    oled.text(" ".join(temp[:3]),10,10)
    oled.text(" ".join(temp[3:]),10,20)
    oled.show()
    print(time_str)
    print("%s" % temp) 
    onboard_led.off()
    print("======================\n")
    time.sleep_ms(2000)
