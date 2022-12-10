from PIL import Image

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .reporttools import *

 
class pdfGenerator():
    canv = canvas.Canvas("./report.pdf", pagesize=(PDF_WIDTH, PDF_HEIGHT))
    def __init__(self, report_name: str = "report"):
    # set up fonts
        self.canv = canvas.Canvas(f"./reports/{report_name}.pdf", pagesize=(PDF_WIDTH, PDF_HEIGHT))
        pdfmetrics.registerFont(TTFont('TTNormsPro', '../fonts/TTNormsPro.ttf'))
        pdfmetrics.registerFont(TTFont('TTNormsProBold', '../fonts/TTNormsProB.ttf'))
        pdfmetrics.registerFont(TTFont('TTNormsProItalics', '../fonts/TTNormsProI.ttf'))
        pdfmetrics.registerFont(TTFont('TTNormsProMedium', '../fonts/TTNormsProM.ttf'))
        pdfmetrics.registerFont(TTFont('TTNormsProLight', '../fonts/TTNormsProL.ttf'))

    def first_slide(self):
        canv = self.canv
        img = Image.open(KLIMATIKA_LOGO_PATH)
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
    
    
    def outline_slide(self, date: str, name: str, ph_number: str, address: str, helped: str, cleaned: str):
        canv = self.canv
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
        textobject.textOut('Performed services   ')
        textobject.setFillColor("#6F7378")
        textobject.setLeading(100)
        textobject.textLine(helped)
        
        if cleaned != "" :
            textobject.setFillColor("#E2000F")
            textobject.setFont('TTNormsProMedium', 37)
            textobject.setLeading(45)
            textobject.textLine(text='What we did extra:')
            textobject.setFont('TTNormsPro', 37)
            textobject.setFillColor("#6F7378")
            new_cleaned = divide_by_len(cleaned, 69)
            for i in new_cleaned:
                textobject.textLine(i)
        canv.drawText(textobject)
        canv.showPage()
    
    
    def room_slide(self, room: str, obj: str, before: BinaryIO, after: BinaryIO):
        canv = self.canv

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
    
    
    def last_slides(self):
        canv = self.canv

        canv.setFillColor("#E2000F")
        canv.rect(0, 0, PDF_WIDTH, PDF_HEIGHT, stroke=0, fill=1)
        img = Image.open(LOGO_PATH)
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
        textobject.textLine(text='and check if you need to swap for')
        textobject.textLine(text='new ones at the start of each')
        textobject.textLine(text='season.')
    
        canv.drawText(textobject)
        canv.showPage()
    
        img = Image.open(LETS_TALK_LOGO_PATH)
        add_image(canv, img, px2mm(600), INDENTS[0], INDENTS[1])

        textobject = canv.beginText()
        textobject.setTextOrigin(INDENTS[0], PDF_HEIGHT - px2mm(100))
    
        textobject.setFont('TTNormsProBold', 54)
        textobject.setFillColor("#E2000F")
        textobject.textLine(text='Let’s talk!')

        canv.drawText(textobject)
    
        textobject = canv.beginText()
        textobject.setTextOrigin(PDF_WIDTH / 2 + px2mm(100), PDF_HEIGHT - px2mm(100))

        textobject.setFont('TTNormsPro', 30)
        textobject.setCharSpace(-1)
        textobject.setLeading(35)
        textobject.textLine(text='Call or email us any time for any')
        textobject.setLeading(300)
        textobject.textLine(text='inquiries regarding our services')

        textobject.setFont('TTNormsProBold', 40)
        textobject.setLeading(45)
        textobject.textLine(text='Phone')

        textobject.setFont('TTNormsPro', 40)
        textobject.setLeading(85)
        textobject.textLine(text='+971 58 819 7173')

        textobject.setFont('TTNormsProBold', 40)
        textobject.setLeading(45)
        textobject.textLine(text='Email')

        textobject.setFont('TTNormsPro', 40)
        textobject.setLeading(85)
        textobject.textLine(text='info@klimatika.ae')

        textobject.setFont('TTNormsProBold', 40)
        textobject.setLeading(45)
        textobject.textLine(text='Website')

        textobject.setFont('TTNormsPro', 40)
        textobject.textLine(text='www.klimatika.ae')

        canv.drawText(textobject)
        canv.showPage()
    
    def generate(self, report: dict):
        self.first_slide()
        outline = report["Outline"]
        self.outline_slide(outline["date"].strftime("%m/%d/%Y"),
                           outline["name"],
                           outline["phone_number"],
                           outline["address"],
                           outline["helped_with"],
                           outline["cleaned"])
        rooms = report["Rooms"]
        for room in rooms["rooms_list"]:
            room_items = { 'vent' : room['vent'], 
                           'duct' : room['duct'],
                           'pallet' : room['pallet'],
                           'radiator' : room['radiator'], 
                           'filter' : room['filter'],
                           'impelers' : room['impelers'] }
            for item_name, item in room_items.items():
                self.room_slide(room['room'], f"{room['object']} ({item_name})", item['img_before'], item['img_after'])
        self.last_slides()

        self.canv.save()

