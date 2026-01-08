import asyncio
import logging
from aiogram import Router, Dispatcher, types, F, Bot

from routers import router as main_router
from routers.commands.base_commands import dp
import config

router = Router()
dp.include_router(main_router)

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.BOT_TOKEN    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

