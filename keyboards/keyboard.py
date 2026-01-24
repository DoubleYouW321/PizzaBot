from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Menu"),
            KeyboardButton(text="About"),
        ],
        [
            KeyboardButton(text="Variants shipping"),
            KeyboardButton(text="Payment vars"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="What block are you interested in?"
)

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text="Menu"),
    KeyboardButton(text="About"),
    KeyboardButton(text="Variants shipping"),
    KeyboardButton(text="Payment vars"),
)
start_kb2.adjust(2, 2)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(
    KeyboardButton(text="feedback")
)

admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить товар"),
            KeyboardButton(text="Ассортимент"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбирите действие"
)

del_kb = ReplyKeyboardRemove()

