import asyncio
import logging

from aiogram import Bot, Dispatcher

from captcha_bot.config import BotConfig
from captcha_bot.handlers import member, admin
from captcha_bot.image import ImageMaker


async def main():
    logging.basicConfig(format='%(levelname)s | %(message)s', level=logging.INFO)

    config = BotConfig()

    image_maker = ImageMaker('images', config.include_directories, config.exclude_directories,
                             config.no_caption_directories)

    newcomers = {}

    bot = Bot(config.token.get_secret_value())
    dp = Dispatcher(image_maker=image_maker, owner_id=config.owner_id, chat_ids=config.chat_ids,
                    newcomers=newcomers, kick_delay=config.kick_delay, messages_text=config.messages_text)
    dp.include_routers(member.router, admin.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())