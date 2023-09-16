import asyncio

from aiogram.filters import BaseFilter
from aiogram.types import Message


class NewcomerFiter(BaseFilter):
    async def __call__(self, message: Message, newcomers: dict[int, tuple[list[int], asyncio.Task]]) -> bool:
        return message.from_user.id in newcomers