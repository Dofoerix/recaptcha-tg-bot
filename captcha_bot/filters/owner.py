from aiogram.filters import BaseFilter
from aiogram.types import Message


class OwnerFilter(BaseFilter):
    async def __call__(self, message: Message, owner_id: int) -> bool:
        return message.from_user.id == owner_id