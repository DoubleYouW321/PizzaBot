from aiogram.types import BotCommand

private = [
    BotCommand(command='start', description='запуск бота'),
    BotCommand(command='menu', description='меню'),
    BotCommand(command='about', description='описание бота'),
    BotCommand(command='payment', description='способы оплаты'),
    BotCommand(command='shipping', description='доставка'),
    BotCommand(command='admin', description='админка'),
]