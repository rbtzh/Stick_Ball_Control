from machine import Pin, SoftI2C, UART, ADC

from ssd1306_tools import SSD1306_I2C_MODIFIED

switchbtn = ADC(Pin(12))

#init ssd1306 with i2c
oled_width = 128
oled_height = 64
i2c = SoftI2C(scl=Pin(10), sda=Pin(11))
oled = SSD1306_I2C_MODIFIED(oled_width, oled_height, i2c)

#init ATK1218 GPS with UART
uart1 = UART(1, baudrate=38400, rx=18, tx=17, bits=8, parity=None, stop=1)

while True:
    uart_read = str(uart1.readline())
    if switchbtn.read() <= 1000:
        if '$GNGGA' in uart_read:
            oled.fill(0)
            GNGGA_list = uart_read.split(',')
            #print(GNGGA_list) 
            try:    
                oled.text_center(f"{GNGGA_list[3]}: {GNGGA_list[2]}", 0)
                oled.text_center(f"{GNGGA_list[5]}: {GNGGA_list[4]}", 10)
                oled.text_center(f"GPS Status: {GNGGA_list[6]}", 30)
                oled.text_center(f"Satellite: {GNGGA_list[7]}", 40)
                oled.text_center(f"Page: 1", 54)
            except IndexError:
                pass
            else:
                oled.show()
    elif switchbtn.read() <= 2000:
        if '$GNGGA' in uart_read:
            oled.fill(0)
            GNGGA_list = uart_read.split(',')

            try:
                utctimestring = GNGGA_list[1]
                utctimestring_format = utctimestring[0:2]+":"+utctimestring[2:4]+":"+utctimestring[4:6]
                if int(utctimestring[0:2]) + 8 < 24:
                    utc8timestring_format = str(int(utctimestring[0:2]) + 8) +":"+utctimestring[2:4]+":"+utctimestring[4:6]
                else:
                    utc8timestring_format = str(int(utctimestring[0:2]) - 16) +":"+utctimestring[2:4]+":"+utctimestring[4:6]
                    
                oled.text_center(f"UTC", 0)
                oled.text_center(f"{utctimestring_format}", 10)
                oled.text_center(f"Local", 30)
                oled.text_center(f"{utc8timestring_format}", 40)
                oled.text_center(f"Page: 2", 54)
            except IndexError:
                pass
            else:
                oled.show()
    elif switchbtn.read() <= 3000:
        if '$GNGGA' in uart_read:
            oled.fill(0)
            GNGGA_list = uart_read.split(',')

            try:
                oled.text_center(f"Zhao Yanbo", 0)
                oled.text_center(f"Is", 10)
                oled.text_center(f"Handsome", 20)
                oled.text_center(f"Thanks", 30)
                oled.text_center(f"Page: 3", 54)
            except IndexError:
                pass
            else:
                oled.show()
    elif switchbtn.read() <= 4000:
        if '$GNGGA' in uart_read:
            oled.fill(0)
            GNGGA_list = uart_read.split(',')
            #print(GNGGA_list)
            try:
                utctimestring = GNGGA_list[1]
                utctimestring_format = utctimestring[0:2]+":"+utctimestring[2:4]+":"+utctimestring[4:6]
                oled.text_center(f"UTC: {utctimestring_format}", 0)
                oled.text_center(f"", 10)
                oled.text_center(f"", 40)
                oled.text_center(f"", 50)
                oled.text_center(f"Page: 4", 54)
            except IndexError:
                pass
            else:
                oled.show()
    elif switchbtn.read() > 4000:
        if '$GNGGA' in uart_read:
            oled.fill(0)
            GNGGA_list = uart_read.split(',')
            #print(GNGGA_list)
            try:
                utctimestring = GNGGA_list[1]
                utctimestring_format = utctimestring[0:2]+":"+utctimestring[2:4]+":"+utctimestring[4:6]
                oled.text_center(f"UTC: {utctimestring_format}", 0)
                oled.text_center(f"", 10)
                oled.text_center(f"", 40)
                oled.text_center(f"", 50)
                oled.text_center(f"Page: 5", 54)
            except IndexError:
                pass
            else:
                oled.show()

