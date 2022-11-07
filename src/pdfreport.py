from platform import python_branch
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def px2mm(px):
    return px * 0.2645833333 * mm

PDF_HEIGHT, PDF_WIDTH = px2mm(1080), px2mm(1920)
INDENTS = (px2mm(50), px2mm(50)) # indents by x and y

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

def add_image(canv, path_to_img: str, x: float, y: float):

    F_CONST = Formatter(114*mm, INDENTS[0], y)

    img = Image.open(path_to_img)
    img_f = image_formatter(img, int(F_CONST.width()))

    canv.drawImage(img_f, x=x, y=y - px2mm(img_f.getSize()[1]))

def first_slide(canv):
    add_image(canv, "../img/logo_klimatika.png", 13*mm, PDF_HEIGHT - 13*mm)
    canv.setFont('TTNormsProBold', 72)
    canv.drawString(INDENTS[0], px2mm(680), "Apartment")
    canv.drawString(INDENTS[0], px2mm(680 - 120), "VAC Cleaning Completion")
    canv.drawString(INDENTS[0], px2mm(680 - 2*120), "Report")
    canv.setFont('TTNormsPro', 36)
    canv.setFillColor("#E2000F")
    canv.drawString(INDENTS[0], px2mm(680 - 2*120 - 86), "Learn how we help you breathe.")

# set up fonts
pdfmetrics.registerFont(TTFont('TTNormsPro', '../fonts/TTNormsPro.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsProBold', '../fonts/TTNormsProB.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsItalics', '../fonts/TTNormsProI.ttf'))

canv = canvas.Canvas("report.pdf", pagesize=(PDF_WIDTH, PDF_HEIGHT))

first_slide(canv)
canv.showPage()
canv.save()


