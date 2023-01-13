from typing import BinaryIO
from aiogram import types, Bot
from queue import Queue

from dataclasses import dataclass, field
from .cleaningnode import CleaningNode, DEFAULT_CLEANING_NODES

from enum import Enum, auto


@dataclass
class Room:
    class Type(str, Enum):
        UNKNOWN = ""
        BEDROOM = "Bedroom"
        LIVING_ROOM = "Living Room"
        KITCHEN = "Kitchen"

        def __str__(self) -> str:
            return str(self.value)

        def for_button(self, text: str) -> tuple[str, ...]:
            return (text, self)

    room_type: Type = Type.UNKNOWN
    room_object: str = ""

    default_cleaning_nodes: list[list[CleaningNode, bool]] = field(default_factory=list)
    cleaning_nodes: list[CleaningNode] = field(default_factory=list)

    nodes_queue: Queue[CleaningNode] = field(default_factory=Queue)

    current_node: CleaningNode | None = None

    def __post_init__(self):
        self.default_cleaning_nodes.extend(
            [[node, False] for node in DEFAULT_CLEANING_NODES]
        )

    def add_node(self, node: CleaningNode) -> None:
        if node.type == CleaningNode.Type.DEFAULT:
            self.add_default_node(node)
        elif node.type == CleaningNode.Type.OTHER:
            self.cleaning_nodes.append(node)

    def add_default_node(self, node: CleaningNode) -> None:
        pos = DEFAULT_CLEANING_NODES.index(node)
        self.default_cleaning_nodes[pos][0] = node
        self.default_cleaning_nodes[pos][1] = True

    def delete_node(self, node: CleaningNode) -> None:
        if node.type == CleaningNode.Type.DEFAULT:
            self.delete_default_node(node)
        elif node.type == CleaningNode.Type.OTHER:
            self.cleaning_nodes.remove(node)

    def delete_default_node(self, node: CleaningNode):
        pos = DEFAULT_CLEANING_NODES.index(node)
        self.default_cleaning_nodes[pos][1] = False

    def create_nodes_queue(self):
        for node, status in filter(lambda x: x[1], self.default_cleaning_nodes):
            self.nodes_queue.put(node)

        for node in self.cleaning_nodes:
            self.nodes_queue.put(node)

        self.current_node = self.nodes_queue.get()

    def next_cleaning_node(self):
        if self.nodes_queue.empty():
            self.current_node = None
            return

        self.current_node = self.nodes_queue.get()
        return self.current_node

    async def dict_with_binary(self, bot: Bot) -> dict:
        nodes = [
            node for node, status in self.default_cleaning_nodes if status
        ] + self.cleaning_nodes
        dictionary = {
            "room": self.room_type,
            "object": self.room_object,
            "nodes": dict(
                [
                    (
                        node.name,
                        {
                            "img_before": await download_image(bot, node.photo_before),
                            "img_after": await download_image(bot, node.photo_after),
                        },
                    )
                    for node in nodes
                ]
            ),
        }

        return dictionary


async def download_images(bot, photos: list[types.PhotoSize]) -> list[BinaryIO] | None:
    if len(photos) == 0:
        return
    return [await download_image(bot, image) for image in photos]


async def download_image(bot: Bot, photo: types.PhotoSize | None) -> BinaryIO | None:
    if photo is None:
        raise ValueError("Photo is None")
    return await bot.download(photo.file_id)
