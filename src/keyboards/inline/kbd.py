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
    get_factors_keyboard,
    get_skip_keyboard
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
                Room.Type.MASTER_ROOM.for_button(_("Master bedroom")),
                Room.Type.KIDS_ROOM.for_button(_("Kids bedroom")),
                Room.Type.GUEST_ROOM.for_button(_("Guest bedroom")),
                Room.Type.MAIDS_ROOM.for_button(_("Maids bedroom")),
                Room.Type.CABINET_ROOM.for_button(_("Cabinet room")),
                Room.Type.GYM.for_button(_("Gym"))
            ],
        other=_("Other"),
        ),
    )


async def send_service_keyboard(message: types.Message):
    await message.answer(
        _("Choose service:"),
        reply_markup=get_service_keyboard(
            message.chat.id,
            [
                Report.Service.SERVICE.for_button(_("Service")),
                Report.Service.MAINTENANCE.for_button(_("Maintenance")),
                Report.Service.CHECK_LIST.for_button(_("Check list")),

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
                # Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB.for_button(
                #     _("Thermal Insulator Change Job")
                # ),
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
                Report.Service.SERVICE.for_button(_("Service")),
                Report.Service.MAINTENANCE.for_button(_("Maintenance")),
                Report.Service.CHECK_LIST.for_button(_("Check list")),
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
                # Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB.for_button(
                #     _("Thermal Insulator Change Job")
                # ),
                Report.ExtraService.REPAIR_WORKS.for_button(_("Repair Works")),
            ],
            other=_("Other"),
            enter=_("Enter"),
        ),
    )

async def send_maintenance_node_keyboard(message: types.Message):
    await message.answer(
        _("Choose maintenance nodes"),
        reply_markup=get_cleaning_node_keyboard(
            message.chat.id,
            [
                CleaningNode(
                    "grills", button_text=_("grills"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "duct", button_text=_("duct"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "pan", button_text=_("pan"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "radiator",
                    button_text=_("radiator"),type=CleaningNode.Type.DEFAULT,
                ),
                CleaningNode(
                    "filter", button_text=_("filter"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "blades", button_text=_("blades"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "ceiling area",
                    button_text=_("ceiling area"),
                    type=CleaningNode.Type.DEFAULT,
                ),
            ],
            other=_("Other"),
            enter=_("Enter"),
        ),
    )



async def edit_maintenance_node_keyboard(message: types.Message):
    await message.edit_text(
        _("Choose maintenance nodes"),
        reply_markup=get_cleaning_node_keyboard(
            message.chat.id,
            [
                CleaningNode(
                    "grills", button_text=_("grills"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "duct", button_text=_("duct"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "pan", button_text=_("pan"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "radiator",
                    button_text=_("radiator"),type=CleaningNode.Type.DEFAULT,
                ),
                CleaningNode(
                    "filter", button_text=_("filter"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "blades", button_text=_("blades"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "ceiling area",
                    button_text=_("ceiling area"),
                    type=CleaningNode.Type.DEFAULT,
                ),
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


async def send_service_node_keyboard(message: types.Message):
    await message.answer(
        _("Choose cleaning nodes"),
        reply_markup=get_cleaning_node_keyboard(
            message.chat.id,
            [
                CleaningNode(
                    "аctuator", button_text=_("Actuator"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "motor", button_text=_("Motor"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "isolation", button_text=_("Isolation fixing"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "electronic fasteners tightening",
                    button_text=_("Electronic fasteners tightening"),
                    type=CleaningNode.Type.DEFAULT,
                ),
                CleaningNode(
                    "level fixing", button_text=_("Level fixing"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "compressor", button_text=_("Compressor"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "capacitor replacement(outside unit)",
                    button_text=_("Capacitor replacement(outside unit)"),
                    type=CleaningNode.Type.DEFAULT,
                ),
                CleaningNode(
                    "fan motor", button_text=_("Fan motor"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "fan impeller", button_text=_("Fan impeller"), type=CleaningNode.Type.DEFAULT
                ),
            ],
            other=_("Other"),
            enter=_("Enter"),
        ),
    )


async def edit_service_node_keyboard(message: types.Message):
    await message.edit_text(
        _("Choose service nodes"),
        reply_markup=get_cleaning_node_keyboard(
            message.chat.id,
            [
                CleaningNode(
                    "аctuator", button_text=_("Actuator"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "motor", button_text=_("Motor"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "isolation", button_text=_("Isolation fixing"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "electronic fasteners tightening",
                    button_text=_("Electronic fasteners tightening"),
                    type=CleaningNode.Type.DEFAULT,
                ),
                CleaningNode(
                    "level fixing", button_text=_("Level fixing"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "compressor", button_text=_("Compressor"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "capacitor replacement(outside unit)",
                    button_text=_("Capacitor replacement(outside unit)"),
                    type=CleaningNode.Type.DEFAULT,
                ),
                CleaningNode(
                    "fan motor", button_text=_("Fan motor"), type=CleaningNode.Type.DEFAULT
                ),
                CleaningNode(
                    "fan impeller", button_text=_("Fan impeller"), type=CleaningNode.Type.DEFAULT
                ),
            ],
            other=_("Other"),
            enter=_("Enter"),
        ),
    )


async def send_factors_keyboard(message: types.Message):
    await message.answer(
        _("What were the factors complicating the work?"),
        reply_markup=get_factors_keyboard(
            message.chat.id,
            [
                Report.Factor.DIFFICULT_ACCESS_TO_UNITS.for_button(
                    _("Difficult access")
                ),
                Report.Factor.NO_ACCESS_TO_OBJECT.for_button(_("No access to object")),
                Report.Factor.CUSTOM_SIZES.for_button(_("Custom sizes of vent")),
                Report.Factor.DAY_OFF_WORK.for_button(_("Day off work")),
                Report.Factor.WORKING_IN_ANOTHER_EMIRATE.for_button(
                    _("Working in another emirate")
                ),
            ],
            enter=_("Enter"),
        ),
    )


async def edit_factors_keyboard(message: types.Message):
    await message.edit_text(
        _("What were the factors complicating the work?"),
        reply_markup=get_factors_keyboard(
            message.chat.id,
            [
                Report.Factor.DIFFICULT_ACCESS_TO_UNITS.for_button(
                    _("Difficult access")
                ),
                Report.Factor.NO_ACCESS_TO_OBJECT.for_button(_("No access to object")),
                Report.Factor.CUSTOM_SIZES.for_button(_("Custom sizes of vent")),
                Report.Factor.DAY_OFF_WORK.for_button(_("Day off work")),
                Report.Factor.WORKING_IN_ANOTHER_EMIRATE.for_button(
                    _("Working in another emirate")
                ),
            ],
            enter=_("Enter"),
        ),
    )


# Функция для отправки сообщения с клавиатурой "Пропустить"
async def send_skip_keyboard(message: types.Message, text: str):
    await message.answer(
        text=text,
        reply_markup=get_skip_keyboard(),
    )