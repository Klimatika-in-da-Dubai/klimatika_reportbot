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


def divide_by_len(cleaned: str, line_len: int) -> list:
    cleaned = cleaned.replace("  ", " ")
    new_cleaned = []
    j = 1
    start = 0
    if line_len >= len(cleaned):
        new_cleaned.append(cleaned)
    else:
        while j <= 4 and start < len(cleaned):
            end_j = j * (line_len + 1)
            if end_j >= len(cleaned):
                end_j = len(cleaned) - 1
            for end in range(end_j, start, -1):
                if end + 1 == len(cleaned) or cleaned[end] == ' ':
                    end += 1
                    new_cleaned.append(cleaned[start:end])
                    start = end
                    j += 1
                    break
    return new_cleaned


def image_crop(path_to_img, w_size=4, h_size=3) -> Image.Image:
    img = Image.open(path_to_img)
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
    F_CONST = Formatter(img_width, INDENTS[0], y)

    img_f = image_formatter(img, int(F_CONST.width()))

    canv.drawImage(img_f, x=x, y=y, mask='auto')
    #  - px2mm(img_f.getSize()[1]

 
def first_slide(canv):
    img = Image.open("../img/logo_klimatika.png")
    add_image(canv, img, px2mm(430), INDENTS[0], PDF_HEIGHT - px2mm(215))

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


def outline_slide(canv, date: str, name: str, ph_number: str, address: str, helped: str, cleaned: str):
    textobject = canv.beginText()
    textobject.setTextOrigin(INDENTS[0], PDF_HEIGHT - px2mm(100))

    textobject.setFont('TTNormsProBold', 55)
    textobject.setCharSpace(-1)
    textobject.setFillColor("#E2000F")
    textobject.setLeading(100)
    textobject.textLine(text='Outline')

    textobject.setFont('TTNormsPro', 37)
    textobject.setFillColor("#000000")
    textobject.setLeading(55)
    textobject.textOut('Date   ')
    textobject.setFillColor("#6F7378")
    textobject.textLine(text=date)

    textobject.setFillColor("#000000")
    textobject.textOut('Name   ')
    textobject.setFillColor("#6F7378")
    textobject.textLine(text=name)

    textobject.setFillColor("#000000")
    textobject.textOut('Phone number   ')
    textobject.setFillColor("#6F7378")
    textobject.textLine(ph_number)

    textobject.setFillColor("#000000")
    textobject.textOut('Address   ')
    textobject.setFillColor("#6F7378")
    textobject.textLine(address)

    textobject.setFillColor("#000000")
    textobject.textOut('We help with   ')
    textobject.setFillColor("#6F7378")
    textobject.setLeading(100)
    textobject.textLine(helped)

    textobject.setFillColor("#E2000F")
    textobject.setFont('TTNormsProMedium', 37)
    textobject.setLeading(45)
    textobject.textLine(text='What we cleaned:')
    textobject.setFont('TTNormsPro', 37)
    textobject.setFillColor("#6F7378")
    new_cleaned = divide_by_len(cleaned, 69)
    for i in new_cleaned:
        textobject.textLine(i)
    canv.drawText(textobject)
    canv.showPage()


def room_slide(canv, room: str, obj: str, before: str, after: str):
    img_before = image_crop(before)
    img_after = image_crop(after)
    add_image(canv, img_before, px2mm(860), INDENTS[0], INDENTS[1])
    add_image(canv, img_after, px2mm(860), PDF_WIDTH - px2mm(860) - INDENTS[0], INDENTS[1])

    textobject = canv.beginText()
    textobject.setTextOrigin(INDENTS[0], PDF_HEIGHT - px2mm(100))

    textobject.setFont('TTNormsProBold', 54)
    textobject.setFillColor("#E2000F")
    textobject.setLeading(55)
    textobject.textLine(text=room)
    
    textobject.setFont('TTNormsPro', 37)
    textobject.setFillColor("#000000")
    textobject.textLine(text=obj)

    textobject.setFont('TTNormsProLight', 35)
    textobject.setTextOrigin(px2mm(400), PDF_HEIGHT - px2mm(330))
    textobject.textLine(text="before")
    textobject.setTextOrigin(PDF_WIDTH - px2mm((530)), PDF_HEIGHT - px2mm(330))
    textobject.setFillColor("#E2000F")
    textobject.textLine(text="after")
    canv.drawText(textobject)

    canv.showPage()


def extra_slide(canv, text: str, picture: str):
    img = image_crop(picture)
    add_image(canv, img, px2mm(860), PDF_WIDTH - px2mm(860) - INDENTS[0], INDENTS[1])

    textobject = canv.beginText()
    textobject.setTextOrigin(INDENTS[0], PDF_HEIGHT - px2mm(100))

    textobject.setFont('TTNormsProBold', 54)
    textobject.setFillColor("#E2000F")
    textobject.setLeading(55)
    textobject.textLine(text="What we did extra")
    
    textobject.setFont('TTNormsPro', 45)
    textobject.setTextOrigin(INDENTS[0], PDF_HEIGHT/2)
    textobject.setFillColor("#6F7378")
    new_text = divide_by_len(text, 26)
    for i in new_text:
        textobject.textLine(i)
    canv.drawText(textobject)

    canv.showPage()


def last_slides(canv):
    canv.setFillColor("#E2000F")
    canv.rect(0, 0, PDF_WIDTH, PDF_HEIGHT, stroke=0, fill=1)
    img = Image.open("../img/logo_part.png")
    add_image(canv, img, px2mm(777), PDF_WIDTH - px2mm(777 + INDENTS[0]), INDENTS[1])

    textobject = canv.beginText()
    textobject.setTextOrigin(INDENTS[0], PDF_HEIGHT - px2mm(100))

    textobject.setFont('TTNormsProBold', 54)
    textobject.setCharSpace(-1)
    textobject.setFillColor("#FFFFFF")
    textobject.setLeading(55)
    textobject.textLine(text='Make Sure to Clean Your')
    textobject.setLeading(230)
    textobject.textLine(text='VAC Filters')

    textobject.setFillColor("#E6E6E6")
    textobject.setFont('TTNormsPro', 48)
    textobject.setLeading(45)
    textobject.textLine(text='Clean air filters can help you')
    textobject.textLine(text='save between 5% and 15% from')
    textobject.setLeading(70)
    textobject.textLine(text='your electricity bill!')

    textobject.setLeading(45)
    textobject.textLine(text='Clean your VAC filters quarterly')
    textobject.textLine(text='and checkfi you need toswap for')
    textobject.textLine(text='new ones at the start of each')
    textobject.textLine(text='season.')

    canv.drawText(textobject)
    canv.showPage()

    textobject = canv.beginText()
    textobject.setTextOrigin(INDENTS[0], PDF_HEIGHT - px2mm(100))

    textobject.setFont('TTNormsProBold', 54)
    textobject.setLeading(350)
    textobject.textLine(text='Let’s talk!')

    textobject.setFont('TTNormsPro', 48)
    textobject.setCharSpace(-1)
    textobject.setLeading(65)
    textobject.textLine(text='Phone: +971 58 819 7173')
    textobject.textLine(text='Email: info@klimatika.ae')
    textobject.textLine(text='Website: www.klimatika.ae')
    canv.drawText(textobject)

    canv.showPage()


# set up fonts
pdfmetrics.registerFont(TTFont('TTNormsPro', '../fonts/TTNormsPro.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsProBold', '../fonts/TTNormsProB.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsProItalics', '../fonts/TTNormsProI.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsProMedium', '../fonts/TTNormsProM.ttf'))
pdfmetrics.registerFont(TTFont('TTNormsProLight', '../fonts/TTNormsProL.ttf'))

canv = canvas.Canvas("report.pdf", pagesize=(PDF_WIDTH, PDF_HEIGHT))

first_slide(canv)
outline_slide(canv, "10 January 2022", "Edem", "+7 123 456 78 90",
              "Nizhny Novgorod, st. Kuznechihynskaya, 100",
              "Just test smth. And something else, to test how loo",
              "test    cleaned   24 teeeeeest test test ")
room_slide(canv, "Bedroom", "Fridge", "../static_slides/before.jpg", "../static_slides/after.jpg")
extra_slide(canv, "Test text text test. how many words in one lineeeeee. About 29 symbols", "../static_slides/extra.jpg")
last_slides(canv)

canv.save()


