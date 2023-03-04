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

    def summary_first(self,
            date: str,
            name: str,
            phone_number: str,
            address: str,
            description: dict,
            helped_with: str,
        ):
        canv = self.canv
        textobject = canv.beginText()
        
        textobject.setTextOrigin(Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 2)

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setCharSpace(-1)
        textobject.setFillColor("#E2000F")
        textobject.setLeading(HEDING_FONT_SIZE * 1.5)
        textobject.textLine(text="Summary (1 of 3)")

        textobject.setFillColor("#E2000F")
        textobject.setFont(Fonts.bold["name"], 35)
        textobject.textOut("Date:  ")
        textobject.setFont(Fonts.regular["name"], 35)
        textobject.setFillColor("#6F7378")
        textobject.setLeading(55)
        textobject.textLine(text=date)

        textobject.setFillColor("#E2000F")
        textobject.setFont(Fonts.bold["name"], 35)
        textobject.textOut("Name:  ")
        textobject.setFont(Fonts.regular["name"], 35)
        textobject.setFillColor("#6F7378")
        textobject.setLeading(55)
        textobject.textLine(text=name)

        textobject.setFillColor("#E2000F")
        textobject.setFont(Fonts.bold["name"], 35)
        textobject.textOut("Phone number:  ")
        textobject.setFont(Fonts.regular["name"], 35)
        textobject.setFillColor("#6F7378")
        textobject.setLeading(55)
        textobject.textLine(phone_number)

        textobject.setFillColor("#E2000F")
        textobject.setFont(Fonts.bold["name"], 35)
        textobject.textOut("Address:  ")
        textobject.setFont(Fonts.regular["name"], 35)
        textobject.setFillColor("#6F7378")
        textobject.setLeading(55)
        textobject.textLine(address)

        textobject.setFillColor("#E2000F")
        textobject.setFont(Fonts.bold["name"], 35)
        textobject.textOut("Performed serviced:  ")
        textobject.setFont(Fonts.regular["name"], 35)
        textobject.setFillColor("#6F7378")
        textobject.setLeading(70)
        textobject.textLine(helped_with)

        if description["text"] != "":
            textobject.setFillColor("#E2000F")
            textobject.setFont(Fonts.bold["name"], 33)
            textobject.setLeading(55)
            textobject.textLine("Description: ")
            textobject.setFont(Fonts.regular["name"], 31)

            textobject.setFillColor("#6F7378")
            textobject.setLeading(45)
            textobject.textLine(description["text"])

            textobject.setTextOrigin(Indent.get_x() * 2, PDF_HEIGHT // 2 - 80)
            for line in description["points"]:
                textobject.setLeading(45)
                textobject.setFillColor("#E2000F")
                textobject.textOut("• ")
                textobject.setFillColor("#6F7378")
                new_line = divide_by_len(line, 120)
                count = 0
                for i in new_line:
                    if count > 0:
                        textobject.textOut("   ")     
                    textobject.textLine(i)
                    count += 1
        canv.drawText(textobject)
        canv.showPage()

    def summary_second(self,
            extra_services: list,
            working_factors: list,
        ):
        canv = self.canv
        textobject = canv.beginText()
        
        textobject.setTextOrigin(Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 2)

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setCharSpace(-1)
        textobject.setFillColor("#E2000F")
        textobject.textLine(text="Summary (2 of 3)")

        textobject.setTextOrigin(Indent.get_x() * 2, PDF_HEIGHT - Indent.get_y() * 2 - HEDING_FONT_SIZE * 1.5)

        if extra_services != []:
            textobject.setFont(Fonts.bold["name"], 40)
            textobject.setFillColor("#E2000F")
            textobject.setLeading(60)
            textobject.textLine("What we did extra:")
            textobject.setFillColor("#6F7378")

            textobject.setFont(Fonts.regular["name"], 32)
            for i in range(len(extra_services)):
                textobject.setLeading(50)
                if i + 1 == len(extra_services):
                    textobject.setLeading(100)
                new_line = divide_by_len(extra_services[i], 110)
                if len(new_line) > 1:
                    textobject.setLeading(45)
                count = 0
                textobject.textOut("• ")
                for i in new_line:
                    if count > 0:
                        textobject.textOut("   ")     
                    textobject.textLine(i)
                    count += 1
                    if count == len(new_line) - 1:
                        textobject.setLeading(50)

        if working_factors != []:
            textobject.setFont(Fonts.bold["name"], 40)
            textobject.setFillColor("#E2000F")
            textobject.setLeading(60)
            textobject.textLine("Factors on your premises affecting the final price and length of our services:")
            textobject.setFont(Fonts.regular["name"], 32)
            textobject.setFillColor("#6F7378")
            for i in working_factors:
                textobject.setLeading(50)
                # textobject.textLine("• " + i)
                new_line = divide_by_len(i, 110)
                if len(new_line) > 1:
                    textobject.setLeading(45)
                count = 0
                textobject.textOut("• ")
                for i in new_line:
                    if count > 0:
                        textobject.textOut("   ")     
                    textobject.textLine(i)
                    count += 1
                    if count == len(new_line) - 1:
                        textobject.setLeading(50)
        canv.drawText(textobject)
        canv.showPage()


    def summary_third(self,):
        canv = self.canv
        textobject = canv.beginText()
        
        textobject.setTextOrigin(Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 2)

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setCharSpace(-1)
        textobject.setFillColor("#E2000F")
        textobject.setLeading(HEDING_FONT_SIZE * 2)
        textobject.textLine(text="Summary (3 of 3)")

        textobject.setFont(Fonts.bold["name"], 50)
        textobject.setFillColor("#E2000F")
        textobject.setLeading(HEDING_FONT_SIZE)
        textobject.textLine("Hereby we:")

        textobject.setTextOrigin(Indent.get_x() * 2, PDF_HEIGHT - Indent.get_y() * 2 - HEDING_FONT_SIZE * 3)
        textobject.setFont(Fonts.regular["name"], 31)
        textobject.setLeading(50)

        textobject.setFillColor("#E2000F")
        textobject.textOut("• ")
        textobject.setFillColor("#6F7378")
        textobject.textLine("represent the outline of what we actually did where " +
                            "photos evidence that our services had been performed as shown to the best extent")
        textobject.setLeading(60)
        textobject.textLine("   possible given the circumstances, access and work conditions;")

        textobject.setFillColor("#E2000F")
        textobject.textOut("• ")
        textobject.setFillColor("#6F7378")
        textobject.setLeading(60)
        textobject.textLine("gaurantee that photos are genuine and had not been used from other clients' premises;")

        textobject.setFillColor("#E2000F")
        textobject.textOut("• ")
        textobject.setFillColor("#6F7378")
        textobject.setLeading(50)
        textobject.textLine("kindly ask you to take into account that mild dust " +
                            "layer in the duct and some dirt in the trays/drain may add up very quickly (in 2-3 days")
        textobject.textLine("   after cleaning) in the GCC region due to cliamte " +
                            "conditions and AC system work, this is normal and does not indicate that our services")
        textobject.textLine("   have been performed loosely or unduly. " +
                            "Please provide evidence if you feel strong that it was our fault, otherwise we won't be able to")
        textobject.textLine("   process it in a proper way. For frivoulous " +
                            "claims not supported by convicing evidence we reserve the right to dispute such claims based")
        textobject.textLine("   on this report and solely on the fact that no objections " + 
                            "from your side were raised when you received this report and paid for our")
        textobject.setLeading(60)
        textobject.textLine("   services.")

        textobject.setFillColor("#E2000F")
        textobject.textOut("• ")
        textobject.setFillColor("#6F7378")
        textobject.setLeading(50)
        textobject.textLine("kindly inform you if you do not raise any objections " + 
                            "to what you see in this report or invoice within 24 hours after receiving this")
        textobject.setLeading(60)
        textobject.textLine("   report/invoice, we assume that you accept the works " +
                            "as they are depicted in photos in full and have no objections whatsoever.")

        textobject.setFillColor("#E2000F")
        textobject.textOut("• ")
        textobject.setLeading(50)
        textobject.textLine("highly recommend that you have your AC units and " + 
                            "Duct system serviced at least 3-4 times a year, so that you enjoy fresh air, system")
        textobject.textLine("   work properly and you pay less for electricity bills or AC repair.")
        
        canv.drawText(textobject)
        canv.showPage()


    def summary_slides(
        self,
        date: str,
        name: str,
        phone_number: str,
        address: str,
        description: dict,
        helped_with: str,
        extra_services: list,
        working_factors: list,
    ):
        self.summary_first(date, name, phone_number, address, description, helped_with)
        self.summary_second(extra_services, working_factors)
        self.summary_third()

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
        outline = report
        self.summary_slides(
            outline["date"].strftime("%m/%d/%Y"),
            outline["name"],
            outline["phone_number"],
            outline["address"],
            outline["description"],
            outline["helped_with"],
            outline["extra_services"],
            outline["working_factors"],
        )
        rooms = report["Rooms"]
        for room in rooms["rooms_list"]:
            for _, node in room["nodes"].items():
                self.room_slide(node["name"], node["img_before"], node["img_after"])

        self.last_slides()
        self.canv.save()

        pdf_compression(f"{self.report_name}.pdf")

