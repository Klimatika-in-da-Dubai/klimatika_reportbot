from aiogram.filters.callback_data import CallbackData
from src.models import Report, Client, Room, CleaningNode


class ClientCB(CallbackData, prefix="client"):
    type: Client.Type


class ServiceCB(CallbackData, prefix="service"):
    service: Report.Service


class ExtraServiceCB(CallbackData, prefix="ex_service"):
    action: str
    service: Report.ExtraService


class OtherExtraServiceCB(CallbackData, prefix="oth_ex_service"):
    action: str
    id: int


class RoomTypeCB(CallbackData, prefix="room"):
    type: Room.Type


class CleaningNodeCB(CallbackData, prefix="cleaning_node"):
    action: str
    index: int
    type: CleaningNode.Type


class FactorCB(CallbackData, prefix="factor"):
    action: str
    factor: Report.Factor
    index: int
