import asyncio
import logging

from aiogram import Router, F
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated, BufferedInputFile, Message

from captcha_bot.image import ImageMaker
from captcha_bot.filters.newcomer import NewcomerFiter
from captcha_bot.filters.chat import ChatFilter


router = Router()
router.chat_member.filter(F.chat.type.in_({'group', 'supergroup'}), ChatFilter())
router.message.filter(F.chat.type.in_({'group', 'supergroup'}), NewcomerFiter(), ChatFilter())

async def _delay_kick(event: ChatMemberUpdated, newcomers: dict[int, tuple[list[int], asyncio.Task]], delay: int) -> None:
    user = event.new_chat_member.user
    logging.info(f'{user.username} ({user.full_name}) will be kicked in {delay} minute(s)')
    try:
        await asyncio.sleep(delay * 60)
        await event.chat.unban(user.id)
        logging.info(f'{user.username} ({user.full_name}) was kicked')
    except asyncio.CancelledError:
        logging.info(f'{user.username} ({user.full_name}) won\'t be kicked')
    finally:
        del newcomers[user.id]


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def member_joined(
    event: ChatMemberUpdated,
    image_maker: ImageMaker,
    newcomers: dict[int, tuple[list[int], asyncio.Task]],
    kick_delay: int,
    messages_text: dict[str, str]
):
    user = event.new_chat_member.user
    image, answers = image_maker.create_random()
    text = messages_text['joined'].format(username=f'@{user.username}', first_name=user.first_name,
                                          full_name=user.full_name, answers=str(answers).strip('[]'))
    await event.answer_photo(
        BufferedInputFile(image, 'captcha.jpg'),
        caption=text
    )
    if kick_delay:
        kick_task = asyncio.create_task(_delay_kick(event, newcomers, kick_delay))
    else:
        kick_task = None
    newcomers[user.id] = (answers, kick_task)

@router.message()
async def solution(message: Message, newcomers: dict[int, tuple[list[int], asyncio.Task]],
                   messages_text: dict[str, str]):
    user = message.from_user

    if message.text:
        text = message.text
    elif message.caption:
        text = message.caption
    else:
        text = None

    answers = newcomers[user.id][0]
    correct = 0
    incorrect = 0
    user_answers = []

    if text:
        for symbol in text:
            if symbol.isnumeric():
                if int(symbol) in answers and symbol not in user_answers:
                    user_answers.append(symbol)
                    correct += 1
                elif int(symbol) not in answers:
                    incorrect += 1

        if not any(symbol.isdigit() for symbol in text):
            congrats = messages_text['no_nums']
        elif correct == 0:
            congrats = messages_text['0_correct']
        elif correct == 1:
            congrats = messages_text['1_correct']
        elif correct == 2:
            congrats = messages_text['2_correct']
        elif correct == 3:
            congrats = messages_text['3_correct']
        elif correct > 3 and incorrect > 2:
            congrats = messages_text['incorrect']
        elif correct > 3:
            congrats = messages_text['4_correct']
    else:
        congrats = messages_text['no_text']

    text = messages_text['answer'].format(username=f'@{user.username}', first_name=user.first_name,
                                          full_name=user.full_name, correct=correct, incorrect=incorrect,
                                          congrats=congrats, answers=str(answers).strip('[]'))

    await message.reply(text)

    kick_task = newcomers[user.id][1]
    if isinstance(kick_task, asyncio.Task):
        kick_task.cancel()
        logging.info(f'{user.username} ({user.full_name}) kick task was cancelled')
    else:
        del newcomers[user]