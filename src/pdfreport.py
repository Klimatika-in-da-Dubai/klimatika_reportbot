from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from PIL import Image

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class FormatConstants:
    IMAGE_WIDTH = 0
    X_POS = 0
    Y_POS = 0
    PDF_WIDTH, PDF_HEIGHT = A4

    def __init__(self, img_width, vert_pos):
        self.IMAGE_WIDTH = img_width * mm
        self.X_POS = img_width * mm
        self.Y_POS = vert_pos

    def width(self) -> float:
        return self.IMAGE_WIDTH

    def center(self) -> tuple[int, int]:
        return (int((self.PDF_WIDTH - self.X_POS) / 2), int(self.Y_POS))

    def left(self) -> tuple[int, int]:
        return (0, int(self.Y_POS))

    def right(self) -> tuple[int, int]:
        return (int(self.PDF_WIDTH - self.X_POS), int(self.Y_POS))


def image_formatter(img, exp_width: int) -> canvas.ImageReader:
    img_w, img_h = img.size
    size_rel = img_h / img_w
    exp_height = int(exp_width * size_rel)
    exp_size = tuple([exp_width, exp_height])
    return canvas.ImageReader(img.resize(exp_size))

def create_pdf(canv, img = 0, img_pos: tuple[int, int] = (0, 0)) -> None:
    x, y = img_pos
    canv.setFont('TTNormsPro', 15)
    canv.drawString(500, 80, "Hello World")
    canv.drawImage(img, x=x, y=y)

pdfmetrics.registerFont(TTFont('TTNormsPro', '../fonts/TTNormsPro.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsProBold', '../fonts/TTNormsProB.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsItalics', '../fonts/TTNormsProI.ttf'))

F_CONST = FormatConstants(100, 0)

img = Image.open("./test.jpg")
img_f = image_formatter(img, int(F_CONST.width()))

canv = canvas.Canvas("report.pdf", pagesize=(F_CONST.PDF_HEIGHT, F_CONST.PDF_WIDTH))
create_pdf(canv, img_f, F_CONST.center())
canv.showPage()
canv.save()


