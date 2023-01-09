from aiogram.utils.i18n import gettext as _
from aiogram import types
from src.models import Room, Report, Client, CleaningNode
from .form import (
    get_client_type_keyboard,
    get_extra_service_keyboard,
    get_service_keyboard,
    get_yes_no_keyboard,
    get_room_type_keyboard,
    get_cleaning_node_keyboard,
)


async def send_room_type_keyboard(message: types.Message):
    await message.answer(
        _("Select room type:"),
        reply_markup=get_room_type_keyboard(
            message.chat.id,
            [
                Room.Type.KITCHEN.for_button(_("Kitchen")),
                Room.Type.BEDROOM.for_button(_("Bedroom")),
                Room.Type.LIVING_ROOM.for_button(_("Living Room")),
            ],
        ),
    )


async def send_service_keyboard(message: types.Message):
    await message.answer(
        _("Choose service:"),
        reply_markup=get_service_keyboard(
            message.chat.id,
            [
                Report.Service.PREMIUM.for_button(_("Premium")),
                Report.Service.PREMIUM_EXTRA.for_button(_("Premium + Extra")),
                Report.Service.OTHER_REPAIR_SERVICES.for_button(
                    _("Other Repair Services")
                ),
            ],
        ),
    )


async def send_extra_service_keyboard(message: types.Message):
    await message.answer(
        text=_("Choose extra services"),
        reply_markup=get_extra_service_keyboard(
            chat_id=message.chat.id,
            extra_services=[
                Report.ExtraService.COLD_FOG_MACHINE_DISINFECTIONS.for_button(
                    _("Cold Fog Machine Disinfections")
                ),
                Report.ExtraService.NEW_POLYESTER_FILTERS_INSTALLATION.for_button(
                    _("New Polyester Filters Installation")
                ),
                Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB.for_button(
                    _("Thermal Insulator Change Job")
                ),
                Report.ExtraService.REPAIR_WORKS.for_button(_("Repair Works")),
            ],
            other=_("Other"),
            enter=_("Enter"),
        ),
    )


async def send_client_type_keyboard(message: types.Message):
    await message.answer(
        _("Select client is an owner or a tenant"),
        reply_markup=get_client_type_keyboard(
            message.chat.id,
            [
                Client.Type.OWNER.for_button(
                    _("Owner"),
                ),
                Client.Type.TENANT.for_button(
                    _("Tenant"),
                ),
            ],
        ),
    )


async def send_yes_no_keboard(message: types.Message, text: str):
    await message.answer(
        text=text,
        reply_markup=get_yes_no_keyboard(message.chat.id, yes=_("Yes"), no=_("No")),
    )


async def edit_service_keyboard(message: types.Message):
    await message.edit_text(
        _("Choose service:"),
        reply_markup=get_service_keyboard(
            message.chat.id,
            [
                Report.Service.PREMIUM.for_button(_("Premium")),
                Report.Service.PREMIUM_EXTRA.for_button(_("Premium + Extra")),
                Report.Service.OTHER_REPAIR_SERVICES.for_button(
                    _("Other Repair Services")
                ),
            ],
        ),
    )


async def edit_extra_service_keyboard(message: types.Message):
    await message.edit_text(
        text=_("Choose extra services"),
        reply_markup=get_extra_service_keyboard(
            chat_id=message.chat.id,
            extra_services=[
                Report.ExtraService.COLD_FOG_MACHINE_DISINFECTIONS.for_button(
                    _("Cold Fog Machine Disinfections")
                ),
                Report.ExtraService.NEW_POLYESTER_FILTERS_INSTALLATION.for_button(
                    _("New Polyester Filters Installation")
                ),
                Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB.for_button(
                    _("Thermal Insulator Change Job")
                ),
                Report.ExtraService.REPAIR_WORKS.for_button(_("Repair Works")),
            ],
            other=_("Other"),
            enter=_("Enter"),
        ),
    )


async def edit_client_type_keyboard(message: types.Message):
    await message.edit_text(
        _("Select client is an owner or a tenant"),
        reply_markup=get_client_type_keyboard(
            message.chat.id,
            [
                Client.Type.OWNER.for_button(
                    _("Owner"),
                ),
                Client.Type.TENANT.for_button(
                    _("Tenant"),
                ),
            ],
        ),
    )


async def send_cleaning_node_keyboard(message: types.Message):
    await message.answer(
        _("Choose cleaning nodes"),
        reply_markup=get_cleaning_node_keyboard(
            message.chat.id,
            [
                CleaningNode("grills", type=CleaningNode.Type.DEFAULT).for_button(
                    _("grills")
                ),
                CleaningNode("duct", type=CleaningNode.Type.DEFAULT).for_button(
                    _("duct")
                ),
                CleaningNode("pan", type=CleaningNode.Type.DEFAULT).for_button(
                    _("pan")
                ),
                CleaningNode("radiator", type=CleaningNode.Type.DEFAULT).for_button(
                    _("radiator")
                ),
                CleaningNode("filter", type=CleaningNode.Type.DEFAULT).for_button(
                    _("filter")
                ),
                CleaningNode("blades", type=CleaningNode.Type.DEFAULT).for_button(
                    _("blades")
                ),
            ],
            other=_("Other"),
            enter=_("Enter"),
        ),
    )


async def edit_cleaning_node_keyboard(message: types.Message):
    await message.edit_text(
        _("Choose cleaning nodes"),
        reply_markup=get_cleaning_node_keyboard(
            message.chat.id,
            [
                CleaningNode("grills", type=CleaningNode.Type.DEFAULT).for_button(
                    _("grills")
                ),
                CleaningNode("duct", type=CleaningNode.Type.DEFAULT).for_button(
                    _("duct")
                ),
                CleaningNode("pan", type=CleaningNode.Type.DEFAULT).for_button(
                    _("pan")
                ),
                CleaningNode("radiator", type=CleaningNode.Type.DEFAULT).for_button(
                    _("radiator")
                ),
                CleaningNode("filter", type=CleaningNode.Type.DEFAULT).for_button(
                    _("filter")
                ),
                CleaningNode("blades", type=CleaningNode.Type.DEFAULT).for_button(
                    _("blades")
                ),
            ],
            other=_("Other"),
            enter=_("Enter"),
        ),
    )
