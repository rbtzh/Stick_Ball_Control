import ssd1306


class SSD1306_I2C_MODIFIED(ssd1306.SSD1306_I2C):
    
    def __init__(self, oled_width, oled_height, i2c, text_width=8, line_height=10, line_height_with_margin=12):
        self.tw = text_width
        self.lh = line_height
        self.lh_margin = line_height_with_margin
        super().__init__(oled_width, oled_height, i2c)
    
    def get_horizontal_align_center(self, textcount:int):
        return int((self.width - textcount * self.tw) / 2)
    
    def text_center(self, context:string, y_position:int):
        self.text(context, self.get_horizontal_align_center(len(context)), y_position)