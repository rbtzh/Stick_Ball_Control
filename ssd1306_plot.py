from machine import Pin, SoftI2C, UART, ADC

from ssd1306_tools import SSD1306_I2C_MODIFIED
from bh1750 import BH1750

#init adc
switchbtn = ADC(Pin(12))
ADC_MAX = 4096

#init ssd1306 with i2c
oled_width = 128
oled_height = 64
i2c1 = SoftI2C(scl=Pin(10), sda=Pin(11))
oled = SSD1306_I2C_MODIFIED(oled_width, oled_height, i2c1)

#init bh1750 with i2c
i2c2 = SoftI2C(scl=Pin(1), sda=Pin(2))
s = BH1750(i2c2)

ADCtransfer = oled_height / ADC_MAX
BHtransfer = oled_height / 1024


oled.fill(0)
oled.pixel(64,32,5)
oled.show()

while True:
    #y = oled_height - round(switchbtn.read() * ADCtransfer)
    y = oled_height - round(s.luminance(BH1750.CONT_LOWRES) * BHtransfer)
    oled.pixel(127,y,5)
    #oled.pixel(127,y-1,5)
    #oled.pixel(127,y+1,5)
    oled.scroll(-1,0)
    oled.pixel(127,y,0)
    #oled.pixel(127,y-1,0)
    #oled.pixel(127,y+1,0)
    oled.show()
