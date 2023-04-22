from machine import Pin, I2C, SoftI2C 
from ssd1306 import SSD1306_I2C


oled_width = 128
oled_height = 64
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(oled_width, oled_height, i2c)

x_step = 10
y_step = 10

x_direction = 1 # >0 down
y_direction = -1 # >0 right

x_pos = 0
y_pos = 0

line_height = 7
text_width = 8

oled.fill(0)
#oled.text("Hello", 0, 0)

display_text = "."

ctrl_speed_pin = Pin(6, Pin.IN, Pin.PULL_UP)
ctrl_clear_pin = Pin(7, Pin.IN, Pin.PULL_UP)

while True:
    if ctrl_speed_pin.value() == 0:
        x_step = abs(round((oled_width / 2 - x_pos)/(oled_width / 20))+10)
        y_step = abs(round((oled_height / 2 - y_pos)/(oled_height / 10))+10)
    else:
        x_step = 3
        y_step = 3
    if ctrl_clear_pin.value() == 0:
        oled.fill(0)
    if (x_direction > 0 and x_pos + len(display_text) * text_width >= oled_width) or (x_direction < 0 and x_pos <= 0):
        x_direction *= -1
    if (y_direction > 0 and y_pos + line_height >= oled_height) or (y_direction < 0 and y_pos <= 0):
        y_direction *= -1
    
    #oled.fill(0)
    oled.text(display_text, x_pos, y_pos)
    oled.show()

    print(y_step)
    x_pos += x_step * x_direction
    y_pos += y_step * y_direction
    
