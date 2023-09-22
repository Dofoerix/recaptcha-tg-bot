from typing import Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatFilter(BaseFilter):
    async def __call__(self, message: Message, chat_ids: list[Optional[int]]) -> bool:
        if chat_ids:
            return message.chat.id in chat_ids
        else:
            return True