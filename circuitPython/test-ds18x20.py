import board
import time
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

ds_pin = board.GP16
ow_bus = OneWireBus(ds_pin)

while True:
    sensors = ow_bus.scan()
    for device in sensors: 
        ds18 = DS18X20(ow_bus, device)
        ds18.temperature
    print("-" * 20)
    time.sleep(1)