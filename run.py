import asyncio
import os
import logging as log
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from handlers.user_private import user_router
from common.bot_cmds_list import private

TOKEN = os.getenv("TOKEN")
ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(user_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')