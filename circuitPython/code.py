import time
import board
import busio
import digitalio
import binascii
import adafruit_ds1307
import adafruit_ssd1306
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20


# clock i2c
i2c_rtc = busio.I2C (scl=board.GP3, sda=board.GP2)
rtc = adafruit_ds1307.DS1307(i2c_rtc)

# lcd i2c
i2c_lcd = busio.I2C (scl=board.GP1, sda=board.GP0) # This RPi Pico way to call I2C
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c_lcd)
oled.text(' ^_^ Welcome ^_^ ', 12, 8, None)
oled.show()

# ds18x20
ds_pin = board.GP16
ow_bus = OneWireBus(ds_pin)
sensors = ow_bus.scan()
print('Found DS18B20: ', sensors)

# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.LED)
# For QT Py M0:
# led = digitalio.DigitalInOut(board.SCK)
led.switch_to_output()

my_id_dict = {"042449f6753c" : 1,
              "218f48f6c83c" : 2,
              "391a49f69f3c" : 3,
              "66d749f6903c" : 4,
              "846648f6923c" : 5}

WAIT_TO_LOG = (5 * 60)
g_time = ""

def get_current_time():
    t = rtc.datetime
    time_str = "{}/{}/{} {:02}:{:02}:{:02}".format(t.tm_mon, t.tm_mday, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec)
    return time_str

def update_lcd(curr_time, temp_list):
    #oled.show()
    temp_list.sort()
    # csv fmt : datetime, id, temperature
    oled.fill(0)
    oled.text(curr_time, 0, 0, None)
    oled.text(" ".join(temp_list[:3]),0,10, None)
    oled.text(" ".join(temp_list[3:]),0,20, None)
    oled.show()
    print(" ".join(temp_list[:3]))
    print(" ".join(temp_list[3:]))
    print("==============================")
    
try:
    #oled.fill(0)
    #oled.show()
    with open("/temperature.csv", "a") as fp:
        print("temperature.csv is created")
        time_bf = 0
        
        while True:
            led.value = not led.value
            time.sleep(1)

            cnt = 0
            temp_list = []
            if not sensors:
                sensors = ow_bus.scan()
                print('Found DS18B20: ', sensors)
            
            b_log_file = False
            if time.time() - time_bf > WAIT_TO_LOG:
                b_log_file = True
                time_bf = time.time()
                
            for device in sensors:
                led.value = 1
                csv_fmt=""
                cnt += 1
                if cnt > 3:
                    cnt=0
                s = binascii.hexlify(device.serial_number)
                my_id = s.decode('ascii')
                ds18 = DS18X20(ow_bus, device)
                my_temp = str(round(ds18.temperature,1))
                temp_list.append("{}}}{}".format(my_id_dict[my_id], my_temp))
                g_time = get_current_time()             
                csv_fmt='{},{},{}'.format(g_time, my_id_dict[my_id], my_temp)
                print(csv_fmt)

                if b_log_file:
                    print("==Start to write file : ", csv_fmt)
                    fp.write('{}\n'.format(csv_fmt))
                    fp.flush()

            update_lcd(g_time, temp_list)
            
            
except OSError as e:  # Typically when the filesystem isn't writeable...
    delay = 0.5  # ...blink the LED every half second.
    if e.args[0] == 28:  # If the file system is full...
        delay = 0.25  # ...blink the LED faster!
    while True:
        led.value = not led.value
        time.sleep(delay)
        print("filesystem is not writeable")
