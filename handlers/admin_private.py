from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keyboards.keyboard as kb

admin_router = Router()

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Введите название товара',
        'AddProduct:description': 'Введите описание товара',
        'AddProduct:price': 'Введите стоимость товара',
        'AddProduct:image': 'Загрузите изображение товара',
    }

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

@admin_router.message(AddProduct.name, F.text)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите описание товара', reply_markup=kb.del_kb)
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.description, F.text)
async def price(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введите стоимость товара', reply_markup=kb.del_kb)
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.price, F.text)
async def photo(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer('Загрузите изображение товара', reply_markup=kb.del_kb)
    await state.set_state(AddProduct.image)

@admin_router.message(AddProduct.image, F.photo) 
async def add_prod(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer('Товар добавлен', reply_markup=kb.admin)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()