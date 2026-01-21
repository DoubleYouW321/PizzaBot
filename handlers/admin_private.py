from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

import keyboards.keyboard as kb

admin_router = Router()

@admin_router.message(Command('admin'))
async def admin(message: Message):
    await message.answer('Что хотите сделать?', reply_markup=kb.admin)

@admin_router.message(F.text == 'Посмотреть товары')
async def look(message: Message):
    await message.answer('Список товаров', reply_markup=kb.del_kb)
    
@admin_router.message(F.text == 'Изменить товар')
async def edit(message: Message):
    await message.answer('Список товаров', reply_markup=kb.del_kb)

@admin_router.message(F.text == 'Удалить товар')
async def delete(message: Message):
    await message.answer('Выбирите товар для удаления', reply_markup=kb.del_kb)

@admin_router.message(F.text == 'Добавить товар')
async def add(message: Message):
    await message.answer('Введите название товара', reply_markup=kb.del_kb)

@admin_router.message(Command('отмена'))
@admin_router.message(F.text.casefold() == 'отмена')
async def cancel(message: Message):
    await message.answer('Действия отменены', reply_markup=kb.admin)

@admin_router.message(Command('назад'))
@admin_router.message(F.text.casefold() == 'назад')
async def back(message: Message):
    await message.answer('Ок, вы вернулись к прошлому шагу', reply_markup=kb.del_kb)

@admin_router.message(F.text)
async def name(message: Message):
    await message.answer('Введите описание товара', reply_markup=kb.del_kb)

@admin_router.message(F.text)
async def price(message: Message):
    await message.answer('Введите стоимость товара', reply_markup=kb.del_kb)

@admin_router.message(F.text)
async def photo(message: Message):
    await message.answer('Загрузите изображение товара', reply_markup=kb.del_kb)

@admin_router.message(F.text)
async def add_prod(message: Message):
    await message.answer('Товар добавлен', reply_markup=kb.del_kb)