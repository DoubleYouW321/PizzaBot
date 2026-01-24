from aiogram import F, Router
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.requests import req_add_product, req_get_product, req_delete_product, req_get_products, req_update_product
import keyboards.keyboard as kb
from keyboards.inline_kbd import get_callback_btns, get_url_btns

admin_router = Router()

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        'AddProduct:name': 'Введите название товара',
        'AddProduct:description': 'Введите описание товара',
        'AddProduct:price': 'Введите стоимость товара',
        'AddProduct:image': 'Загрузите изображение товара',
    }

@admin_router.message(Command('admin'))
async def admin(message: Message):
    await message.answer('Что хотите сделать?', reply_markup=kb.admin)

@admin_router.message(F.text.lower() == 'ассортимент')
async def look(message: Message, session: AsyncSession):
    for product in await req_get_products(session):
        await message.answer_photo(
            product.image, 
            caption=f'''{product.name}\n{product.description}\nСтоимость: {product.price} рублей''',
            reply_markup=get_callback_btns(btns={
                'Удалить': f'delete_{product.id}',
                'Изменить': f'change_{product.id}',
            })
        )
    await message.answer('Список товаров', reply_markup=kb.del_kb)

@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: CallbackQuery, session):
    product_id = callback.data.split('_')[-1]
    await req_delete_product(session, int(product_id))
    await callback.answer('Товар удален')
    await callback.message.answer('Товар удален!')

@admin_router.callback_query(StateFilter(None), F.data.startswith('change_'))
async def change_product(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split('_')[-1]
    product_for_change = await req_get_product(session, int(product_id))

    AddProduct.product_for_change = product_for_change
    await callback.answer()
    await callback.message.answer('Введите название товара ', reply_markup=kb.del_kb)
    await state.set_state(AddProduct.name)


#FSM

@admin_router.message(StateFilter(None), F.text == 'Добавить товар')
async def add(message: Message, state: FSMContext):
    await message.answer('Введите название товара', reply_markup=kb.del_kb)
    await state.set_state(AddProduct.name)

@admin_router.message(StateFilter('*'), Command('отмена'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None
    await state.clear()
    await message.answer('Действия отменены', reply_markup=kb.admin)

@admin_router.message(StateFilter('*'), Command('назад'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def back(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('Предыдущего шага нет')
        return
    
    previous = None 
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}')
            return
        previous = step

@admin_router.message(AddProduct.name, or_f(F.text, '.'))
async def name(message: Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        await state.update_data(name=message.text)
    await message.answer('Введите описание товара', reply_markup=kb.del_kb)
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.description, F.text)
async def price(message: Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer('Введите стоимость товара', reply_markup=kb.del_kb)
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.price, F.text)
async def photo(message: Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        await state.update_data(price=message.text)
    await message.answer('Загрузите изображение товара', reply_markup=kb.del_kb)
    await state.set_state(AddProduct.image)

@admin_router.message(AddProduct.image, or_f(F.photo, F.text == '.')) 
async def add_prod(message: Message, state: FSMContext, session: AsyncSession):
    if message.text == '.':
        await state.update_data(image=AddProduct.product_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()

    if AddProduct.product_for_change:
        await req_update_product(session, AddProduct.product_for_change.id, data)
    else:
        await req_add_product(session, data)
    await message.answer('Товар добавлен', reply_markup=kb.admin)
    await state.clear()
    
    AddProduct.product_for_change = None

