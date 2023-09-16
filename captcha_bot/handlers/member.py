import asyncio

from aiogram import Router, F
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated, BufferedInputFile, Message, Chat

from captcha_bot.image import ImageMaker
from captcha_bot.filters.newcomer import NewcomerFiter

router = Router()
router.chat_member.filter(F.chat.type.in_({'group', 'supergroup'}))
router.message.filter(F.chat.type.in_({'group', 'supergroup'}), NewcomerFiter())

async def _delay_kick(event: ChatMemberUpdated, newcomers: dict[int, tuple[list[int], asyncio.Task]], delay: int) -> None:
    user = event.new_chat_member.user
    print(f'{user.id} will be kicked after {delay} minutes')
    try:
        await asyncio.sleep(delay * 60)
        await event.chat.unban(user.id)
        await event.answer(f'{user.first_name} кикнут')
    except asyncio.CancelledError:
        await event.answer(f'{user.first_name} не будет кикнут')
    finally:
        del newcomers[user.id]


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def member_joined(
    event: ChatMemberUpdated,
    image_maker: ImageMaker,
    newcomers: dict[int, tuple[list[int], asyncio.Task]],
    kick_delay: int
):
    user = event.new_chat_member.user.id
    image, answers = image_maker.create_random()
    await event.answer_photo(
        BufferedInputFile(image, 'captcha.jpg'),
        caption=f'Привет, @{event.new_chat_member.user.username}! Реши капчу, пожалуйста\n'
        'В своём следующем сообщении напиши цифры от 1 до 9 соответствующие картинкам (отсчёт начинается слева сверху)\n'
        f'Вот ответы, кстати: {str(answers)}'
    )
    if kick_delay:
        kick_task = asyncio.create_task(_delay_kick(event, newcomers, kick_delay))
    else:
        kick_task = None
    newcomers[user] = (answers, kick_task)

@router.message()
async def solution(message: Message, newcomers: dict[int, tuple[list[int], asyncio.Task]]):
    user = message.from_user.id

    if message.text:
        text = message.text
    elif message.caption:
        text = message.caption
    else:
        text = None

    correct = 0
    if text:
        for answer in newcomers[user][0]:
            if str(answer) in text:
                correct += 1

        if not any(symbol.isdigit() for symbol in text):
            congrats = 'Ни одной цифры не написал...'
        elif correct == 0:
            congrats = 'Что-то грустно...'
        elif correct < 3:
            congrats = 'Ну хоть что-то...'
        elif correct == 3:
            congrats = 'Неплохо!'
        elif correct > 3:
            congrats = 'Поздравляю!'
    else:
        congrats = 'Это даже не текст...'

    await message.reply(f'Твой ответ содержит {correct} правильных ответов. {congrats}')

    kick_task = newcomers[user][1]
    if isinstance(kick_task, asyncio.Task):
        kick_task.cancel()
        print(f'{user} kick task is cancelled')
    else:
        del newcomers[user]