from machine import Pin
import onewire
import ds18x20
import time
import binascii

onboard_led = Pin(25, Pin.OUT)
onboard_led.on()

ds_pin = Pin(16)

ds18b20_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

sensors = ds18b20_sensor.scan()

print('Found DS18B20: ', sensors)

while True:
    onboard_led.on()
    ds18b20_sensor.convert_temp()
    time.sleep_ms(750)
    for device in sensors:
        s = binascii.hexlify(device)
        readable_string = s.decode('ascii')
        print("Device: %s"% readable_string)
        print("Temperature: %s °C\n" % str(round(ds18b20_sensor.read_temp(device),2)))
    onboard_led.off()
    time.sleep(2)
