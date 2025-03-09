from enum import IntEnum, auto
from typing import Any, BinaryIO
from PIL import Image

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import BytesIO, TTFont
from reportlab.pdfgen import canvas

from .reporttools import (
    FIRST_SLIDE,
    HEDING_FONT_SIZE,
    LAST_SLIDE,
    PDF_WIDTH,
    PDF_HEIGHT,
    PRE_LAST_SLIDE,
    REPORTS_PATH,
    Fonts,
    Indent,
    add_image,
    image_crop,
    pdf_compression,
)


PREMIUM_DESCRIPTION_POINTS = [
    "Deep cleaning of fan coil unit (VAV, blower fans, air-filter, evaporator coil, drain tray (if accessible))",
    "Check-up and adjustment of valves, fan belts, pulleys, coil, filter, strainer, pipe joints, insulation, bearings, drain trays, drain pipes and manometer tubes. VRV system errors\nand pressure check-up (as applicable to your type of property)",
    "Checking for noise, leaks, smell, vibration and general performance issues (for villas - refrigerant level check-up, board of roof-top AC unit control clean-up and check-up,\ncontrols calibrations checks)",
    "Check-up of thermostat (for villas – starters, relays and timers)",
    "Cleaning of above-ceiling areas (construction work left-overs clean-up, vacuum cleaning with special hose and brush, hand-washing with water)",
    "Disinfection with antibacterial detergent (ShieldMe)",
    "Using anti-dust protection curtains (Zipwall US)",
    "All works performed with german hand tools - DeWalt, Karcher.",
]


class WorkingFactors(IntEnum):
    CUMBERSOME_AND_DIFFICULT_ACCESS = auto()
    PROPERTY_ACCESS_PERMIT_NOT_APPLIED = auto()
    NOT_STANDART_SIZES_OR_DIFFICULTIES = auto()
    INSPECTION_ON_WEEKEND = auto()
    WORK_IN_OTHER_EMIRATE = auto()


WORKING_FACTORS_TEXT: dict[WorkingFactors, str] = {
    WorkingFactors.CUMBERSOME_AND_DIFFICULT_ACCESS: "Cumbersome and otherwise difficult access to units (ceiling access panels located far from AC units, access panels being less than\n60 cm and similar) which affected the overall time of works",
    WorkingFactors.PROPERTY_ACCESS_PERMIT_NOT_APPLIED: "Property access permit not applied for/provided/procured for by the Client in advance",
    WorkingFactors.NOT_STANDART_SIZES_OR_DIFFICULTIES: "Duct grills and/or diffusers are of the length more than 2 meters long and system has not been serviced for a long time",
    WorkingFactors.INSPECTION_ON_WEEKEND: "The inspection performed on a weekend or on a UAE National Holiday",
    WorkingFactors.WORK_IN_OTHER_EMIRATE: "The Client's premises are located outside Dubai, in other emirate",
}


HEREBY_WE = [
    "represent the outline of what we actually did where photos evidence that our services had been performed as shown to the best extent\npossible given the circumstances, access and work conditions;",
    "gaurantee that photos are genuine and had not been used from other clients' premises;",
    "kindly ask you to take into account that mild dust layer in the duct and some dirt in the trays/drain may add up very quickly (in 2-3 days\nafter cleaning) in the GCC region due to cliamte conditions and AC system work, this is normal and does not indicate that our services\nhave been performed loosely or unduly. Please provide evidence if you feel strong that it was our fault, otherwise we won't be able to\nprocess it in a proper way. For frivoulous claims not supported by convicing evidence we reserve the right to dispute such claims based\non this report and solely on the fact that no objections from your side were raised when you received this report and paid for our\nservices.",
    "kindly inform you if you do not raise any objections to what you see in this report or invoice within 24 hours after receiving this\nreport/invoice, we assume that you accept the works as they are depicted in photos in full and have no objections whatsoever.",
]


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

    def bullet_list(
        self,
        textobject: canvas.PDFTextObject,
        str_list: list[str],
        bullet_color: str,
        bullet_font_args: dict[str, Any],
        text_color: str,
        text_font_args: dict[str, Any],
        leading: float,
    ):
        for line in str_list:
            textobject.setLeading(leading)
            textobject.setFillColor(bullet_color)
            textobject.setFont(**bullet_font_args)
            textobject.textOut("•  ")
            textobject.setFont(**text_font_args)
            textobject.setLeading(leading)
            textobject.setFillColor(text_color)
            new_line = line.split("\n")
            count = 0
            for i in new_line:
                if count > 0:
                    textobject.textOut("    ")
                textobject.textLine(i)
                count += 1

    def first_slide(self):
        canv = self.canv
        img = Image.open(FIRST_SLIDE)
        add_image(canv, img, PDF_WIDTH, 0, 0)
        # img = Image.open(KLIMATIKA_LOGO_PATH)
        # add_image(canv, img, 430, Indent.get_x(), PDF_HEIGHT - 215)

        textobject = canv.beginText()
        textobject.setTextOrigin(Indent.get_x(), 791)
        textobject.setFillColor("#FFFFFF")
        textobject.setFont(Fonts.bold["name"], 88)
        # textobject.setLeading(140)

        textobject.textLine(text="Maintenance")
        textobject.textLine(text="Service Completion")
        textobject.textLine(text="Report")

        textobject.setFont(Fonts.regular["name"], 30)
        textobject.setTextOrigin(Indent.get_x(), 467)
        textobject.textOut(text="Presented by ")
        textobject.setFont(Fonts.bold["name"], 30)
        textobject.textOut(text="Andrei Nosikov ")

        textobject.setFont(Fonts.regular["name"], 30)
        textobject.textLine(text="of")
        textobject.setFont(Fonts.bold["name"], 30)
        textobject.textLine(text="Klimatika AC and Refrigerator ")
        textobject.textOut(text="Maintenance LLC ")
        textobject.setFont(Fonts.regular["name"], 30)
        textobject.textLine(text=" (License# 1113949)")

        textobject.setFont(Fonts.regular["name"], 36)
        textobject.setTextOrigin(Indent.get_x(), 64)
        textobject.textOut(text="Learn how we help ")
        textobject.setFont(Fonts.bold["name"], 36)
        textobject.textOut(text="you breathe.")

        # longest_stroke_len = len("of Klimatika AC and Refridgerator")
        # _frst_stroke_len = len("Presented by Aleksandr Orlov")
        # thrd_stroke = "Maintenance LLC"
        # _thrd_stroke_len = len(thrd_stroke)
        # frth_stroke = "(License# 1113949)"
        # _frth_stroke_len = len(frth_stroke)

        canv.drawText(textobject)

        canv.showPage()

    def summary_first(
        self,
        date: str,
        name: str,
        phone_number: str,
        address: str,
        performed_service: str,
        summary_num: int,
    ):
        canv = self.canv
        textobject = canv.beginText()

        textobject.setTextOrigin(Indent.get_x(), 959)

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setCharSpace(-1)
        textobject.setFillColor("#2082EA")
        textobject.setLeading(HEDING_FONT_SIZE * 1.5)
        summary_text = "Summary (1 of 3)"
        if summary_num == 2:
            summary_text = "Summary (1 of 2)"
        textobject.textLine(summary_text)

        textobject.setTextOrigin(Indent.get_x(), 880)
        textobject.setFillColor("#2082EA")
        textobject.setFont(Fonts.bold["name"], 29)
        textobject.textOut("Date:  ")
        textobject.setFont(Fonts.regular["name"], 29)
        textobject.setFillColor("#6F7378")
        textobject.setLeading(55)
        textobject.textLine(text=date)

        textobject.setFillColor("#2082EA")
        textobject.setFont(Fonts.bold["name"], 29)
        textobject.textOut("Name:  ")
        textobject.setFont(Fonts.regular["name"], 29)
        textobject.setFillColor("#6F7378")
        textobject.setLeading(55)
        textobject.textLine(text=name)

        textobject.setFillColor("#2082EA")
        textobject.setFont(Fonts.bold["name"], 29)
        textobject.textOut("Phone number:  ")
        textobject.setFont(Fonts.regular["name"], 29)
        textobject.setFillColor("#6F7378")
        textobject.setLeading(55)
        textobject.textLine(phone_number)

        textobject.setFillColor("#2082EA")
        textobject.setFont(Fonts.bold["name"], 29)
        textobject.textOut("Address:  ")
        textobject.setFont(Fonts.regular["name"], 29)
        textobject.setFillColor("#6F7378")
        textobject.setLeading(55)
        textobject.textLine(address)

        textobject.setFillColor("#2082EA")
        textobject.setFont(Fonts.bold["name"], 29)
        textobject.textOut("Performed services:  ")
        textobject.setFont(Fonts.regular["name"], 29)
        textobject.setFillColor("#6F7378")
        textobject.setLeading(70)
        textobject.textLine(performed_service)

        textobject.setTextOrigin(Indent.get_x(), 588)
        textobject.setFillColor("#2082EA")
        textobject.setFont(Fonts.bold["name"], 23)
        textobject.textOut("Description:")
        textobject.setTextOrigin(Indent.get_x(), 533)

        textobject.setFont(Fonts.regular["name"], 23)
        textobject.setFillColor("#525252")

        if "Premium" in performed_service:
            textobject.textLine("Premium cleaning service included:")

            textobject.setTextOrigin(Indent.get_x() + 15, 489)
            textobject.setCharSpace(0.2)
            self.bullet_list(
                textobject,
                PREMIUM_DESCRIPTION_POINTS,
                "#2082EA",
                {"psfontname": Fonts.bold["name"], "size": 23},
                "#525252",
                {"psfontname": Fonts.regular["name"], "size": 23},
                43,
            )
        else:
            textobject.textLine(
                "Minor repairs around the house, not related to the repair of air conditioners and ventilation"
            )

        canv.drawText(textobject)
        canv.showPage()

    def summary_second(
        self,
        extra_services: list,
        working_factors: list[WorkingFactors],
    ):
        canv = self.canv
        textobject = canv.beginText()
        textobject.setTextOrigin(Indent.get_x(), 959)
        textobject.setCharSpace(0.3)

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setCharSpace(-1)
        textobject.setFillColor("#2082EA")
        textobject.setLeading(HEDING_FONT_SIZE * 1.5)
        textobject.textLine("Summary (2 of 3)")

        textobject.setTextOrigin(Indent.get_x(), 844)
        if extra_services:
            self.extra_services(textobject, extra_services)
            textobject.setTextOrigin(Indent.get_x(), 492)

        if working_factors:
            self.working_factors(textobject, working_factors)

        canv.drawText(textobject)
        canv.showPage()

    def extra_services(self, textobject: canvas.PDFTextObject, extra_services: list):
        textobject.setFillColor("#2082EA")
        textobject.setFont(Fonts.bold["name"], 28)
        textobject.setLeading(83)
        textobject.textLine("What we did extra:")
        textobject.setFont(Fonts.regular["name"], 28)
        textobject.setXPos(28)
        self.bullet_list(
            textobject,
            extra_services,
            "#6F7378",
            {"psfontname": Fonts.bold["name"], "size": 30},
            "#6F7378",
            {"psfontname": Fonts.regular["name"], "size": 30},
            54,
        )

    def working_factors(
        self, textobject: canvas.PDFTextObject, working_factors: list[str]
    ):
        textobject.setFillColor("#2082EA")
        textobject.setFont(Fonts.bold["name"], 28)
        textobject.setLeading(72)
        textobject.textLine(
            "Factors on your premises affecting the inspection time length and final price for our services:"
        )
        textobject.setFont(Fonts.regular["name"], 28)
        textobject.setXPos(28)
        self.bullet_list(
            textobject,
            working_factors,
            "#6F7378",
            {"psfontname": Fonts.bold["name"], "size": 30},
            "#6F7378",
            {"psfontname": Fonts.regular["name"], "size": 30},
            54,
        )

    def summary_third(self, summary_num: int):
        canv = self.canv
        textobject = canv.beginText()

        textobject.setTextOrigin(Indent.get_x(), 959)

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setCharSpace(0)
        textobject.setFillColor("#2082EA")
        textobject.setLeading(HEDING_FONT_SIZE * 2)
        summary_text = "Summary (3 of 3)"
        if summary_num == 2:
            summary_text = "Summary (2 of 2)"
        textobject.textLine(summary_text)

        textobject.setTextOrigin(Indent.get_x(), 833)
        textobject.setFont(Fonts.bold["name"], 50)
        textobject.setFillColor("#2082EA")
        textobject.textLine("Hereby we:")

        textobject.setTextOrigin(75, 755)
        textobject.setFont(Fonts.regular["name"], 29)

        self.bullet_list(
            textobject,
            HEREBY_WE,
            "#2082EA",
            {"psfontname": Fonts.bold["name"], "size": 29},
            "#525252",
            {"psfontname": Fonts.regular["name"], "size": 29},
            55,
        )

        textobject.setFont(Fonts.bold["name"], 29)
        textobject.setFillColor("#2082EA")
        textobject.textOut("• ")
        textobject.setLeading(55)
        textobject.textLine(
            "highly recommend that you have your AC units and Duct system serviced at least 3-4 times a year, so that you enjoy fresh air,"
        )
        textobject.textLine(
            "system work properly and you pay less for electricity bills or AC repair."
        )

        canv.drawText(textobject)
        canv.showPage()

    def summary_slides(
        self,
        date: str,
        name: str,
        phone_number: str,
        address: str,
        performed_service: str,
        extra_services: list,
        working_factors: list,
    ):
        if extra_services != [] or working_factors != []:
            self.summary_first(date, name, phone_number, address, performed_service, 1)
            self.summary_second(extra_services, working_factors)
            self.summary_third(3)
        else:
            self.summary_first(date, name, phone_number, address, performed_service, 2)
            self.summary_third(2)

    def room_slide(self, obj: str, before: BinaryIO, after: BinaryIO, room_name: str, comment: str):
        canv = self.canv

        img_before = image_crop(before)
        img_after = image_crop(after)
        add_image(canv, img_before, 860, Indent.get_x(), Indent.get_y() * 3)
        add_image(
            canv, img_after, 860, PDF_WIDTH - 860 - Indent.get_x(), Indent.get_y() * 3
        )

        # Размеры шрифтов
        room_name_size = HEDING_FONT_SIZE  # Размер заголовка (название комнаты)
        obj_text_size = 60  # Размер текста "BEFORE and AFTER {obj}"
        comment_size = 35  # Размер комментария

        # Устанавливаем цвет текста
        canv.setFillColor("#2082EA")

        # Центрирование названия комнаты
        canv.setFont(Fonts.bold["name"], room_name_size)
        room_name_width = canv.stringWidth(room_name, Fonts.bold["name"], room_name_size)
        canv.drawString((PDF_WIDTH - room_name_width) / 2, PDF_HEIGHT - Indent.get_y() * 2, room_name)

        # Увеличиваем межстрочное расстояние и размещаем "BEFORE and AFTER {obj}" слева
        canv.setFont(Fonts.bold["name"], obj_text_size)
        obj_text = f"BEFORE and AFTER {obj}"
        # Увеличиваем расстояние (например, добавляем 1.5 * obj_text_size)
        canv.drawString(Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 3 - obj_text_size, obj_text)

        # Комментарий слева, если есть
        if comment:
            comment_text = f"Comment: {comment}"
            canv.setFont(Fonts.regular["name"], comment_size)
            canv.drawString(Indent.get_x(), Indent.get_y() * 2, comment_text)

        canv.showPage()

    def room_comment_slide(self, rooms: list):
        canv = self.canv
        title_size = HEDING_FONT_SIZE  # Размер заголовка
        room_name_size = 50  # Размер названия комнаты
        comment_size = 35  # Размер комментария

        # Устанавливаем цвет текста
        canv.setFillColor("#2082EA")

        # Заголовок "Recommendations and Comments:" по центру
        canv.setFont(Fonts.bold["name"], title_size)
        title_text = "Recommendations and Comments:"
        title_width = canv.stringWidth(title_text, Fonts.bold["name"], title_size)  # Вычисляем ширину текста
        title_x = (PDF_WIDTH - title_width) / 2  # Вычисляем координату X для центрирования
        canv.drawString(title_x, PDF_HEIGHT - Indent.get_y() * 2, title_text)

        # Смещение по Y для вывода комментариев
        y_offset = PDF_HEIGHT - Indent.get_y() * 4

        for room in rooms:
            if room["room_comment"]:  # Проверяем, есть ли комментарий к комнате
                # Название комнаты
                canv.setFont(Fonts.bold["name"], room_name_size)
                canv.drawString(Indent.get_x(), y_offset, f"Room: {room['object']}")
                y_offset -= room_name_size * 1.5

                # Комментарий
                canv.setFont(Fonts.regular["name"], comment_size)
                canv.drawString(Indent.get_x(), y_offset, room["room_comment"])
                y_offset -= comment_size * 2

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
        textobject.setFillColor("#2082EA")
        textobject.setLeading(HEDING_FONT_SIZE)
        textobject.textLine(text="BEFORE and AFTER")

        canv.drawText(textobject)

        canv.showPage()

    def last_slides(self):
        canv = self.canv

        canv.setFillColor("#2082EA")
        canv.rect(0, 0, PDF_WIDTH, PDF_HEIGHT, stroke=0, fill=1)
        img = Image.open(PRE_LAST_SLIDE)
        add_image(canv, img, PDF_WIDTH, 0, 0)

        textobject = canv.beginText()
        textobject.setTextOrigin(Indent.get_x(), 879)

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setCharSpace(-1)
        textobject.setFillColor("#FFFFFF")
        textobject.setLeading(HEDING_FONT_SIZE)
        textobject.textLine(text="Make   Sure   to    get   Your    VAC")
        textobject.textLine(text="system  inspected  and  serviced")
        textobject.textLine(text="on a regular basis!")

        textobject.setFillColor("#E6E6E6")
        textobject.setTextOrigin(Indent.get_x(), 587)
        textobject.setFont(Fonts.regular["name"], 48)
        textobject.setLeading(82)
        textobject.textLine(text="Clean air system can help you save between 5% and")
        textobject.textLine(text="15% from your electricity bill!")

        textobject.setTextOrigin(Indent.get_x(), 372)
        textobject.setLeading(66)
        textobject.textLine(
            text="HAVE  your  AC  and  Duct  system  SERVICED  every  3-4"
        )
        textobject.textLine(
            text="months  to  prevent  the  system  from  faailing  when  you"
        )
        textobject.textLine(text="need it most.")

        canv.drawText(textobject)
        canv.showPage()

        img = Image.open(LAST_SLIDE)
        add_image(canv, img, PDF_WIDTH, Indent.get_x(), Indent.get_y())

        textobject = canv.beginText()
        textobject.setTextOrigin(108, 817)

        textobject.setFont(Fonts.bold["name"], HEDING_FONT_SIZE)
        textobject.setFillColor("#2082EA")
        textobject.textLine(text="Let’s talk!")

        canv.drawText(textobject)

        textobject = canv.beginText()
        textobject.setTextOrigin(108, 737)

        textobject.setFont(Fonts.regular["name"], 30)
        textobject.setCharSpace(-1)
        textobject.textLine(text="Call or email us any time for any inquiries")
        textobject.textLine(text="regarding our services")

        textobject.setTextOrigin(108, 591)
        textobject.setFont(Fonts.bold["name"], 40)
        textobject.textLine(text="Phone")
        textobject.setLeading(44)
        textobject.setFont(Fonts.regular["name"], 40)
        textobject.textLine(text="+971 58 819 7173")

        textobject.setTextOrigin(108, 475)
        textobject.setFont(Fonts.bold["name"], 40)
        textobject.textLine(text="Email")

        textobject.setTextOrigin(108, 415)
        textobject.setFont(Fonts.regular["name"], 40)
        textobject.textLine(text="info@klimatika.ae")

        textobject.setTextOrigin(108, 356)
        textobject.setFont(Fonts.bold["name"], 40)
        textobject.textLine(text="Website")
        textobject.setTextOrigin(108, 296)
        textobject.setFont(Fonts.regular["name"], 40)
        textobject.textLine(text="www.klimatika.ae")

        canv.drawText(textobject)
        canv.showPage()

    def generate(self, report: dict) -> str:
        self.first_slide()

        outline = report["Outline"]
        self.summary_slides(
            outline["date"].strftime("%m/%d/%Y"),
            outline["name"],
            outline["phone_number"],
            outline["address"],
            outline["performed_service"],
            outline["extra_services"],
            outline["work_factors"],
        )

        rooms = report["Rooms"]
        print("rooms:", rooms, 'rooms["rooms_list"]:', rooms["rooms_list"])
        
        for room in rooms["rooms_list"]:
            print("room:", room)
            for _, node in room["nodes"].items():
                print("room['nodes']:", room)
                print("node:", node)

                if outline["performed_service"] == "Other Repair Services":
                    self.repair_slide(node["img_before"], node["img_after"])
                else:
                    self.room_slide(
                        node["name"], 
                        node["img_before"], 
                        node["img_after"], 
                        room["object"], 
                        node.get("comment", "")  # Добавляем комментарий, если есть
                    )
        
        # Добавляем слайд с комментариями к комнатам, если есть
        print(rooms["rooms_list"][0]["room_comment"])
        if any(room.get("room_comment") for room in rooms["rooms_list"]):
            print("ok room comment")
            self.room_comment_slide(rooms["rooms_list"])
        
        self.last_slides()
        self.canv.save()

        return pdf_compression(f"{REPORTS_PATH / self.report_name}.pdf")





    def generate_first(self):
        self.first_slide()
        self.summary_first("date", "name", "89999", "add", "Premium + Extra", 3)
        self.summary_second(
            [],
            [
                WorkingFactors.CUMBERSOME_AND_DIFFICULT_ACCESS,
                WorkingFactors.PROPERTY_ACCESS_PERMIT_NOT_APPLIED,
                WorkingFactors.NOT_STANDART_SIZES_OR_DIFFICULTIES,
                WorkingFactors.INSPECTION_ON_WEEKEND,
                WorkingFactors.WORK_IN_OTHER_EMIRATE,
            ],
        )
        self.summary_third(3)
        with open("./test.jpg", "rb") as f:
            image1 = BytesIO(f.read())

        with open("./test.jpg", "rb") as f:
            image2 = BytesIO(f.read())
        self.room_slide("test", image1, image2)
        self.last_slides()
        self.canv.save()
