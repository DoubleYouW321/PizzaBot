from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from sqlalchemy.ext.asyncio import AsyncSession

from database.requests import req_get_products
import keyboards.keyboard as kb

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Приветствуем вас в онлайн пиццерии W_Pizza", reply_markup=kb.start_kb3.as_markup(
        resize_keyboard=True,
        input_field_placeholder="What block are you interested in?"
    ))

@user_router.message(or_f(Command('menu'), (F.text.lower() == "menu")))
async def menu(message: Message, session: AsyncSession):
    for product in await req_get_products(session):
        await message.answer_photo(
            product.image, 
            caption=f'''{product.name} \n {product.description} \n  Стоимость: {product.price} рублей'''
        )
    await message.answer('Меню', reply_markup=kb.del_kb)

@user_router.message(or_f(Command('about'), (F.text.lower() == "about")))
async def about(message: Message):
    await message.answer('Описание бота в разработке...', reply_markup=kb.del_kb)

@user_router.message(or_f(Command('payment'), (F.text.lower() == "payment vars")))
async def payment(message: Message):
    text = as_marked_section(
        "Способы оплаты: ", 
        "By credit card",
        "By cache",
        "In the restaurant",
        marker='✅ '
    )
    await message.answer(text.as_html(), reply_markup=kb.del_kb)
    
@user_router.message(or_f(Command('shipping'), (F.text.lower() == "variants shipping")))
async def shipping(message: Message):
    text = as_list(
        as_marked_section(
            'Shipping vars:',
            'Курьер',
            'Самовывоз',
            'В ресторане поем',
            marker='✅ '
        ),
        as_marked_section(
            'Нельзя',
            'Почта',
            'Голуби',
            marker='❌ '
        ),
        sep='\n------------------\n'
    )
    await message.answer(text.as_html(), reply_markup=kb.del_kb)