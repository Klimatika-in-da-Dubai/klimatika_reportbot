from platform import python_branch
from reportlab.pdfgen import canvas, textobject
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

def add_image(canv, path_to_img: str, img_width: float, x: float, y: float):
    F_CONST = Formatter(img_width, INDENTS[0], y)

    img = Image.open(path_to_img)
    img_f = image_formatter(img, int(F_CONST.width()))

    canv.drawImage(img_f, x=x, y=y - px2mm(img_f.getSize()[1]), mask='auto')

def first_slide(canv):
    add_image(canv, "../img/logo_klimatika.png", px2mm(430), INDENTS[0], PDF_HEIGHT - INDENTS[0])

    textobject = canv.beginText()
    textobject.setTextOrigin(INDENTS[0], px2mm(600))
    textobject.setFont('TTNormsProBold', 72)
    textobject.setLeading(90)
    textobject.textLine(text='Apartment')
    textobject.setLeading(75)
    textobject.textLine(text='VAC Cleaning Completion')
    textobject.textLine(text='Report')

    textobject.setFont('TTNormsPro', 36)
    textobject.setTextOrigin(INDENTS[0], px2mm(600 - 2*150))
    textobject.setFillColor("#E2000F")
    textobject.textLine(text='Learn how we help you breathe.')
    canv.drawText(textobject)

    canv.showPage()

def last_slides(canv):
    canv.setFillColor("#E2000F")
    canv.rect(0, 0, PDF_WIDTH, PDF_HEIGHT, stroke=0, fill=1)
    add_image(canv, "../img/logo_part.png", px2mm(777), PDF_WIDTH - px2mm(777 + INDENTS[0]), 481)

    canv.setFillColor("#FFFFFF")
    canv.setFont('TTNormsProBold', 54)
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(100), "Make Sure to Clean Your")
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(175), "VAC Filters")

    canv.setFont('TTNormsPro', 45)
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(460), "Clean air filters can help you")
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(460 + 65), "save between 5% and 15% from")
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(460 + 2*65), "your electricity bill!")

    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(480 + 3*65), "Clean your VAC filters quarterly")
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(480 + 4*65), "and checkfi you need toswap for")
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(480 + 5*65), "new ones at the start of each")
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(480 + 6*65), "season.")

    canv.showPage()

    canv.setFont('TTNormsProBold', 54)
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(100), "Let’s talk!")

    canv.setFont('TTNormsPro', 47)
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(600), "Phone: +971 58 819 7173")
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(600 + 78), "Email: info@klimatika.ae")
    canv.drawString(INDENTS[0], PDF_HEIGHT - px2mm(600 + 2*78), "Website: www.klimatika.ae")

    canv.showPage()


# set up fonts
pdfmetrics.registerFont(TTFont('TTNormsPro', '../fonts/TTNormsPro.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsProBold', '../fonts/TTNormsProB.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsItalics', '../fonts/TTNormsProI.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsProLight', '../fonts/TTNormsProL.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsProThin', '../fonts/TTNormsProT.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsProMedium', '../fonts/TTNormsProM.ttf'))

canv = canvas.Canvas("report.pdf", pagesize=(PDF_WIDTH, PDF_HEIGHT))

first_slide(canv)
last_slides(canv)

canv.save()


