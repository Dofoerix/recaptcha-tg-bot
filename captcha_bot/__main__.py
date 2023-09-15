import asyncio
from pathlib import Path
import os

from aiogram import Bot

from captcha_bot.config import parse_config


async def main():
    config = parse_config(os.path.join(Path(__file__).parents[1], 'settings.json'))

    bot = Bot(config['token'])

if __name__ == '__main__':
    asyncio.run(main())