from PIL import Image

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfdoc import Destination
from reportlab.pdfbase.ttfonts import TTFont, TTFontParser

from .reporttools import *


class pdfGenerator:
    canv = canvas.Canvas("./report.pdf", pagesize=(PDF_WIDTH, PDF_HEIGHT))

    def __init__(self, report_name: str = "report"):
        self.report_name = report_name
        self.canv = canvas.Canvas(
            f"{REPORTS_PATH}/{self.report_name}.pdf", pagesize=(PDF_WIDTH, PDF_HEIGHT)
        )
        # set up fonts
        pdfmetrics.registerFont(TTFont(Fonts.regular["name"], Fonts.regular["path"]))
        pdfmetrics.registerFont(TTFont(Fonts.bold["name"], Fonts.bold["path"]))
        pdfmetrics.registerFont(TTFont(Fonts.italics["name"], Fonts.italics["path"]))
        pdfmetrics.registerFont(TTFont(Fonts.medium["name"], Fonts.medium["path"]))
        pdfmetrics.registerFont(TTFont(Fonts.light["name"], Fonts.light["path"]))

    def first_slide(self):
        canv = self.canv
        img = Image.open(FIRST_SLIDE_TEMPLATE_PATH)
        add_image(canv, img, PDF_WIDTH, 0, 0)
        # img = Image.open(KLIMATIKA_LOGO_PATH)
        # add_image(canv, img, 430, Indent.get_x(), PDF_HEIGHT - 215)

        textobject = canv.beginText()
        textobject.setTextOrigin(Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 5)
        textobject.setFillColor("#FFFFFF")
        textobject.setFont(Fonts.bold["name"], 130)
        textobject.setLeading(140)

        textobject.textLine(text="Apartment")
        textobject.textLine(text="VAC Cleaning")
        textobject.textLine(text="Completion")
        textobject.textLine(text="Report")

        textobject.setFont(Fonts.regular["name"], 36)
        textobject.setTextOrigin(Indent.get_x(), Indent.get_y() * 2)
        textobject.textOut(text="Learn how we help ")
        textobject.setFont(Fonts.bold["name"], 36)
        textobject.textOut(text="you breathe.")

        longest_stroke_len = len("of Klimatika AC and Refridgerator")
        _frst_stroke_len = len("Presented by Aleksandr Orlov")
        thrd_stroke = "Maintenance LLC"
        _thrd_stroke_len = len(thrd_stroke)
        frth_stroke = "(License# 1113949)"
        _frth_stroke_len = len(frth_stroke)

        textobject.setFont(Fonts.regular["name"], 30)
        textobject.setTextOrigin(
            PDF_WIDTH - (PDF_WIDTH / 4) - Indent.get_x(), Indent.get_y() * 3
        )
        textobject.textOut(
            text=(" " * (longest_stroke_len - _frst_stroke_len) * 2) + "Presented by "
        )
        textobject.setFont(Fonts.bold["name"], 30)
        textobject.textLine(text="Aleksandr Orlov")

        textobject.setFont(Fonts.regular["name"], 30)
        textobject.textOut(text="of ")
        textobject.setFont(Fonts.bold["name"], 30)
        textobject.textLine(text="Klimatika AC and Refridgerator")

        textobject.textLine(
            text=(" " * (longest_stroke_len - _thrd_stroke_len) * 2) + thrd_stroke
        )
        textobject.setFont(Fonts.regular["name"], 30)

        textobject.textLine(
            text=(" " * (longest_stroke_len - _frth_stroke_len) * 2) + frth_stroke
        )

        canv.drawText(textobject)

        canv.showPage()

    def outline_slide(
        self,
        date: str,
        name: str,
        ph_number: str,
        address: str,
        helped: str,
        description: str,
        cleaned: str,
    ) -> None:
        canv = self.canv
        textobject = canv.beginText()

        textobject.setTextOrigin(Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 2)

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setCharSpace(-1)
        textobject.setFillColor("#E2000F")
        textobject.setLeading(HEDING_FONT_SIZE * 2)
        textobject.textLine(text="Outline")

        textobject.setFont(Fonts.regular["name"], 37)
        textobject.setFillColor("#000000")
        textobject.setLeading(70)
        textobject.textOut("Date   ")
        textobject.setFillColor("#6F7378")
        textobject.textLine(text=date)

        textobject.setFillColor("#000000")
        textobject.textOut("Name   ")
        textobject.setFillColor("#6F7378")
        textobject.textLine(text=name)

        textobject.setFillColor("#000000")
        textobject.textOut("Phone number   ")
        textobject.setFillColor("#6F7378")
        textobject.textLine(ph_number)

        textobject.setFillColor("#000000")
        textobject.textOut("Address   ")
        textobject.setFillColor("#6F7378")
        textobject.textLine(address)

        textobject.setFillColor("#000000")
        textobject.textOut("Performed services   ")
        textobject.setFillColor("#6F7378")
        textobject.textLine(helped)

        if description != "":
            textobject.setFillColor("#000000")
            textobject.setLeading(45)
            textobject.textLine("Description:")
            textobject.setFillColor("#6F7378")

            new_description = divide_by_len(description, 69)
            for i in range(len(new_description)):
                if i + 1 == len(new_description):
                    textobject.setLeading(70)
                textobject.textLine(new_description[i])

        if cleaned != "":
            textobject.setFillColor("#E2000F")
            textobject.setFont(Fonts.medium["name"], 37)
            textobject.setLeading(45)
            textobject.textLine(text="What we did extra:")
            textobject.setFont(Fonts.regular["name"], 37)
            textobject.setFillColor("#6F7378")
            new_cleaned = divide_by_len(cleaned, 69)
            for i in new_cleaned:
                textobject.textLine(i)
        canv.drawText(textobject)
        canv.showPage()

    def room_slide(self, obj: str, before: BinaryIO, after: BinaryIO):
        canv = self.canv

        img_before = image_crop(before)
        img_after = image_crop(after)
        add_image(canv, img_before, 860, Indent.get_x(), Indent.get_y() * 3)
        add_image(
            canv, img_after, 860, PDF_WIDTH - 860 - Indent.get_x(), Indent.get_y() * 3
        )

        textobject = canv.beginText()
        textobject.setTextOrigin(
            Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 2 - HEDING_FONT_SIZE
        )

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setFillColor("#E2000F")
        textobject.setLeading(HEDING_FONT_SIZE)
        textobject.textLine(text=f"BEFORE and AFTER {obj} cleaning")

        canv.drawText(textobject)

        canv.showPage()

    def repair_slide(self, before: BinaryIO, after: BinaryIO):
        canv = self.canv

        img_before = image_crop(before)
        img_after = image_crop(after)
        add_image(canv, img_before, 860, Indent.get_x(), Indent.get_y() * 3)
        add_image(
            canv, img_after, 860, PDF_WIDTH - 860 - Indent.get_x(), Indent.get_y() * 3
        )

        textobject = canv.beginText()
        textobject.setTextOrigin(
            Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 2 - HEDING_FONT_SIZE
        )

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setFillColor("#E2000F")
        textobject.setLeading(HEDING_FONT_SIZE)
        textobject.textLine(text=f"BEFORE and AFTER")

        canv.drawText(textobject)

        canv.showPage()

    def last_slides(self):
        canv = self.canv

        canv.setFillColor("#E2000F")
        canv.rect(0, 0, PDF_WIDTH, PDF_HEIGHT, stroke=0, fill=1)
        img = Image.open(PRE_LAST_SLIDE_TEMPLATE_PATH)
        add_image(canv, img, PDF_WIDTH, 0, 0)

        textobject = canv.beginText()
        textobject.setTextOrigin(
            Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 2 - HEDING_FONT_SIZE
        )

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setCharSpace(-1)
        textobject.setFillColor("#FFFFFF")
        textobject.setLeading(HEDING_FONT_SIZE)
        textobject.textLine(text="Make Sure to Clean Your")
        textobject.textLine(text="VAC Filters")

        textobject.setFillColor("#E6E6E6")
        textobject.setFont(Fonts.regular["name"], 48)

        textobject.setTextOrigin(Indent.get_x(), PDF_HEIGHT / 2 - Indent.get_y())
        textobject.setLeading(48)
        textobject.textLine(
            text="Clean air filters can help you save between 5% and 15% from"
        )
        textobject.textLine(text="your electricity bill!")

        textobject.setTextOrigin(Indent.get_x(), PDF_HEIGHT * 1 / 4)
        textobject.setLeading(48)
        textobject.textLine(
            text="Clean your VAC filters quarterly and check if you need to swap"
        )
        textobject.textLine(text="for new ones at the start of each season.")

        canv.drawText(textobject)
        canv.showPage()

        img = Image.open(LETS_TALK_LOGO_PATH)
        add_image(canv, img, 600, Indent.get_x(), Indent.get_y())

        textobject = canv.beginText()
        textobject.setTextOrigin(
            Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 2 - HEDING_FONT_SIZE
        )

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setFillColor("#E2000F")
        textobject.textLine(text="Let’s talk!")

        canv.drawText(textobject)

        textobject = canv.beginText()
        textobject.setTextOrigin(PDF_WIDTH / 2 + Indent.get_x(), PDF_HEIGHT - 100)

        textobject.setFont(Fonts.regular["name"], 30)
        textobject.setCharSpace(-1)
        textobject.setLeading(35)
        textobject.textLine(text="Call or email us any time for any")
        textobject.setLeading(300)
        textobject.textLine(text="inquiries regarding our services")

        textobject.setFont(Fonts.bold["name"], 40)
        textobject.setLeading(45)
        textobject.textLine(text="Phone")

        textobject.setFont(Fonts.regular["name"], 40)
        textobject.setLeading(85)
        textobject.textLine(text="+971 58 819 7173")

        textobject.setFont(Fonts.bold["name"], 40)
        textobject.setLeading(45)
        textobject.textLine(text="Email")

        textobject.setFont(Fonts.regular["name"], 40)
        textobject.setLeading(85)
        textobject.textLine(text="info@klimatika.ae")

        textobject.setFont(Fonts.bold["name"], 40)
        textobject.setLeading(45)
        textobject.textLine(text="Website")

        textobject.setFont(Fonts.regular["name"], 40)
        textobject.textLine(text="www.klimatika.ae")

        canv.drawText(textobject)
        canv.showPage()

    def generate(self, report: dict):
        self.first_slide()

        outline = report["Outline"]
        self.outline_slide(
            outline["date"].strftime("%m/%d/%Y"),
            outline["name"],
            outline["phone_number"],
            outline["address"],
            outline["helped_with"],
            outline["description"],
            outline["cleaned"],
        )
        rooms = report["Rooms"]
        for room in rooms["rooms_list"]:
            for _node, node in room["nodes"].items():
                if outline["helped_with"] == "Other Repair Services":
                    self.repair_slide(node["img_before"], node["img_after"])
                else:
                    self.room_slide(node["name"], node["img_before"], node["img_after"])

        self.last_slides()
        self.canv.save()

        pdf_compression(f"{self.report_name}.pdf")
