import asyncio
from pathlib import Path
import os
import logging

from aiogram import Bot, Dispatcher

from captcha_bot.config import parse_config
from captcha_bot.handlers import member
from captcha_bot.image import ImageMaker


async def main():
    logging.basicConfig(level=logging.INFO)

    config = parse_config(os.path.join(Path(__file__).parents[1], 'settings.json'))

    image_creator = ImageMaker('images')

    bot = Bot(config['token'])
    dp = Dispatcher(image_creator=image_creator)
    dp.include_routers(member.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())