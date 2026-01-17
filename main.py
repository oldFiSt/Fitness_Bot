import asyncio
import logging
from aiogram import Bot, Dispatcher

from routers import router as main_router
import config


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(main_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
