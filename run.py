import asyncio
import os
import logging as log
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from handlers.user_private import user_router
from handlers.admin_private import admin_router
from common.bot_cmds_list import private
from database.engine import create_db, drop_db, session_maker
from middlewares.mw import DataBaseSession

TOKEN = os.getenv("TOKEN")
ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()
    await create_db()

async def on_shutdown(bot):
    print('Бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.include_routers(user_router, admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')