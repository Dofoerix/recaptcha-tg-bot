from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import CommandObject
from aiogram.filters import Command, CommandStart

from captcha_bot.filters.owner import OwnerFilter
from captcha_bot.image import ImageMaker


router = Router()
router.message.filter(F.chat.type == 'private', OwnerFilter())

@router.message(CommandStart())
async def start(message: Message):
    await message.reply('Привет, вот мои команды:\n'
                        '/start - вывести этот текст\n'
                        '/create <подпись> - вывести капчу с заданной подписью\n'
                        '/create_random - вывести капчу со случайной подписью')

@router.message(Command('create'))
async def create(message: Message, command: CommandObject, image_maker: ImageMaker):
    if command.args:
        try:
            image, answers = image_maker.create(command.args)
        except KeyError:
            await message.reply('К сожалению, директории для этой подписи нет')
            return
        await message.reply_photo(BufferedInputFile(image, 'captcha.jpg'),
                                  caption=f'Ответы: {str(answers).strip("[]")}')
    else:
        await message.reply('Напишите подпись после команды')

@router.message(Command('create_random'))
async def create_random(message: Message, image_maker: ImageMaker):
    image, answers = image_maker.create_random()
    await message.reply_photo(BufferedInputFile(image, 'captcha.jpg'), caption=f'Ответы: {str(answers).strip("[]")}')