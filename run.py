import asyncio
import os
import logging as log
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.start_handlers import router

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')