from typing import BinaryIO
from aiogram import types, Bot

from dataclasses import dataclass, field
from .cleaningnode import CleaningNode, DEFAULT_SERVICE_NODES,DEFAULT_MAINTENANCE_NODES

from enum import Enum


@dataclass
class Room:
    class Type(str, Enum):
        UNKNOWN = "Unknown"
        BEDROOM = "Bedroom"
        LIVING_ROOM = "Living Room"
        MASTER_ROOM = "Master bedroom"
        KIDS_ROOM = "Kids bedroom"
        GUEST_ROOM = "Guest bedroom"
        MAIDS_ROOM = "Maids bedroom"
        CABINET_ROOM = "Cabinet room"
        GYM = "Gym"
        KITCHEN = "Kitchen"


        def __str__(self) -> str:
            return str(self.value)

        def for_button(self, text: str) -> tuple[str, ...]:
            return (text, self)

    room_type: Type = Type.UNKNOWN
    room_object: str = ""
    room_comment: str = ""

    default_cleaning_nodes: list[list[CleaningNode, bool]] = field(default_factory=list)
    cleaning_nodes: list[CleaningNode] = field(default_factory=list)

    nodes_queue: list[CleaningNode] = field(default_factory=list)
    _index: int = 0

    def __post_init__(self):
        
        self.default_cleaning_nodes.extend(
            [[node, False] for node in DEFAULT_SERVICE_NODES]
        )

    @property
    def last_cleaning_node(self) -> CleaningNode | None:
        if self.cleaning_nodes_empty():
            return None
        return self.cleaning_nodes[-1]

    def pop_cleaning_node(self) -> None:
        if self.cleaning_nodes_empty():
            return
        self.cleaning_nodes.pop()

    def cleaning_nodes_empty(self) -> bool:
        return len(self.cleaning_nodes) == 0

    def clear_all_cleaning_nodes(self) -> None:
        for default_node in self.default_cleaning_nodes:
            default_node[1] = False

        self.cleaning_nodes.clear()

    def set_default_node(self, node: CleaningNode) -> None:
        pos = DEFAULT_SERVICE_NODES.index(node)
        self.default_cleaning_nodes[pos][0] = node
        self.default_cleaning_nodes[pos][1] = True



    def set_default2_node(self, node: CleaningNode) -> None:
        pos = DEFAULT_MAINTENANCE_NODES.index(node)
        self.default_cleaning_nodes[pos][0] = node
        self.default_cleaning_nodes[pos][1] = True

    def add_node(self, node: CleaningNode) -> None:
        if node.type == CleaningNode.Type.OTHER:
            self.cleaning_nodes.append(node)

    def add_default_node(self, index: int) -> None:
        self.default_cleaning_nodes[index][1] = True

    def delete_node(self, index: int, type: CleaningNode.Type) -> None:
        if type == CleaningNode.Type.DEFAULT:
            self.delete_default_node(index)
        elif type == CleaningNode.Type.OTHER:
            self.cleaning_nodes.pop(index)

    def delete_default_node(self, index: int):
        self.default_cleaning_nodes[index][1] = False

    def create_nodes_queue(self):
        self.nodes_queue.clear()
        self._index = 0
        for node, status in filter(lambda x: x[1], self.default_cleaning_nodes):
            self.nodes_queue.append(node)

        for node in self.cleaning_nodes:
            self.nodes_queue.append(node)

    @property
    def current_node(self) -> CleaningNode | None:
        if self.nodes_queue_empty():
            return None
        return self.nodes_queue[self._index]

    def next_cleaning_node(self):
        self._index += 1
        return self.current_node

    def nodes_queue_empty(self):
        return self._index == len(self.nodes_queue)

    def nodes_queue_back(self):
        if self._index == 0:
            raise Exception("_index is zero")
        self._index -= 1

    async def dict_with_binary(self, bot: Bot) -> dict:
        nodes = [
            node for node, status in self.default_cleaning_nodes if status
        ] + self.cleaning_nodes
        dictionary = {
            "room": self.room_type,
            "object": self.room_object,
            "room_comment": self.room_comment,
            "nodes": dict(
                [
                    (
                        index,
                        {
                            "name": node.name.lower(),
                            "img_before": await download_image(bot, node.photo_before),
                            "img_after": await download_image(bot, node.photo_after),
                            "comment": node.comment if hasattr(node, "comment") else None,  # Добавили комментарий
                        },
                    )
                    for index, node in enumerate(nodes)
                ]
            ),
        }
        print("dictionary:", dictionary )
        return dictionary


async def download_images(bot, photos: list[types.PhotoSize]) -> list[BinaryIO] | None:
    if len(photos) == 0:
        return
    return [await download_image(bot, image) for image in photos]


async def download_image(bot: Bot, photo: types.PhotoSize | None) -> BinaryIO:
    if photo is None:
        raise ValueError("Photo is None")
    return await bot.download(photo.file_id)
