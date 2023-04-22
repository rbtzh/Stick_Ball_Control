def lora_ssd1306():
    from machine import Pin, SoftI2C, UART, ADC

    from ssd1306_tools import SSD1306_I2C_MODIFIED

    #init ssd1306 with i2c
    oled_width = 128
    oled_height = 64
    i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
    oled = SSD1306_I2C_MODIFIED(oled_width, oled_height, i2c)

    #init ATK1218 GPS with UART
    uart1 = UART(1, baudrate=115200, rx=18, tx=17, bits=8, parity=None, stop=1)
    oled.fill(0)
    
    while True:
        uart_read = uart1.readline()

        if uart_read:
            #oled.fill(0)
            #print(GNGGA_list) 
            #try:
            uart_read = str(uart_read)
            oled.scroll(0, 10)
            oled.text(f"{uart_read}", 0, 10)
            #except IndexError:
                #pass
            #else:
            print(f"{uart_read}")
            oled.show()
lora_ssd1306()
