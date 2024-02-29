import json

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.methods.send_message import SendMessage
from aiogram.types import Message
from pymongo.collection import Collection

from src.calculation import calc
from src.config import conf

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> SendMessage:
    await message.answer(f'Hello, {message.from_user.full_name}!')


@dp.message()
async def calculation(message: Message, collection: Collection) -> SendMessage:
    input_data = json.loads(message.text)
    actual_result = await calc(collection, input_data)
    await message.answer(json.dumps(actual_result))


async def start(collection: Collection) -> None:
    bot = Bot(token=conf.telegram_token.get_secret_value(), parse_mode='HTML')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, collection=collection)
