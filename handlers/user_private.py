from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Приветствуем вас в онлайн пиццерии W_Pizza")

@user_router.message(Command('menu'))
async def menu(message: Message):
    await message.answer('Меню')