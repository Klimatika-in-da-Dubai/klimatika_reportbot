from typing import BinaryIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image

def px2mm(px):
    return px * 0.2645833333 * mm

PDF_HEIGHT, PDF_WIDTH = px2mm(1080), px2mm(1920)
INDENTS = (px2mm(50), px2mm(50)) # indents by x and y
KLIMATIKA_LOGO_PATH = "./img/logo_klimatika.png"
LOGO_PATH = "./img/logo_part.png"

class Formatter:
    IMAGE_WIDTH = 0
    X_POS = 0
    Y_POS = 0

    def __init__(self, img_width, hor_pos, vert_pos):
        self.IMAGE_WIDTH = img_width
        self.X_POS = hor_pos
        self.Y_POS = vert_pos

    def width(self) -> float:
        return self.IMAGE_WIDTH

    def center(self) -> tuple[int, int]:
        return (int((PDF_WIDTH - self.X_POS) / 2), int(self.Y_POS))

    def left(self) -> tuple[int, int]:
        return (0, int(self.Y_POS))

    def right(self) -> tuple[int, int]:
        return (int(PDF_WIDTH - self.X_POS), int(self.Y_POS))


def divide_by_len(text: str, line_len: int) -> list:
    text = text.replace("  ", " ")
    new_text = []
    j = 1
    start = 0
    if line_len >= len(text):
        new_text.append(text)
    else:
        while j <= 4 and start < len(text):
            end_j = j * (line_len + 1)
            if end_j >= len(text):
                end_j = len(text) - 1
            for end in range(end_j, start, -1):
                if end + 1 == len(text) or text[end] == ' ':
                    end += 1
                    new_text.append(text[start:end])
                    start = end
                    j += 1
                    break
    return new_text


def image_crop(img_bin: BinaryIO, w_size=4, h_size=3) -> Image.Image:
    img = Image.open(img_bin)
    width, height = img.size

    relation = width/height
    left = 0
    top = 0
    right = width
    bottom = height

    if relation > w_size/h_size:
        to_crop = (width - (height * w_size)/h_size) / 2
        left = to_crop
        top = 0
        right = width - to_crop
        bottom = height
    elif relation < w_size/h_size:
        to_crop = (height - (width * h_size)/w_size) / 2
        left = 0
        top = to_crop
        right = width
        bottom = height - to_crop
    return img.crop((left, top, right, bottom))


def image_formatter(img, exp_width: int) -> canvas.ImageReader:
    img_w, img_h = img.size
    size_rel = img_h / img_w
    exp_height = int(exp_width * size_rel)
    exp_size = tuple([exp_width, exp_height])
    return canvas.ImageReader(img.resize(exp_size))


def add_image(canv, img: Image.Image, img_width: float, x: float, y: float):
    format_const = Formatter(img_width, INDENTS[0], y)
    img_f = image_formatter(img, int(format_const.width()))
    canv.drawImage(img_f, x=x, y=y, mask='auto')
