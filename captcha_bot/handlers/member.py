from aiogram import Router, F
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated, BufferedInputFile

from captcha_bot.image import ImageMaker


router = Router()
router.chat_member.filter(F.chat.type.in_({'group', 'supergroup'}))

@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def member_joined(event: ChatMemberUpdated, image_maker: ImageMaker):
    image, answers = image_maker.create_random()
    await event.answer_photo(
        BufferedInputFile(image, 'captcha.jpg'),
        caption=f'Привет, @{event.new_chat_member.user.username}! Реши капчу пожалуйста\nВот ответы, кстати: {str(answers)}'
    )