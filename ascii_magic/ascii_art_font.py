from PIL import ImageFont

import os


class AsciiArtFont():
    FONT_SIZE = 18

    def __init__(self, font: str):
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', font)
        if os.path.exists(font_path):
            self._font = ImageFont.truetype(font=font_path, size=self.FONT_SIZE)
        else:
            self._font = ImageFont.truetype(font=font, size=self.FONT_SIZE)

    def get_font(self) -> ImageFont.ImageFont:
        return self._font

    def get_char_size(self) -> tuple[int, int, int]:
        bbox = self._font.getbbox('M')
        char_width = int(bbox[2] - bbox[0])
        char_height = int(bbox[3] - bbox[1])
        line_height = int(char_height + self.FONT_SIZE / 4)
        return char_width, char_height, line_height

    def get_ratio(self) -> float:
        char_width, _, line_height = self.get_char_size()
        return line_height / char_width
