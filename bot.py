from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
import os

from utils import read_concrete_deployment_schema, read_deployment_schemas_list

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise Exception("No token provided")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


SCHEMAS = read_deployment_schemas_list()


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message) -> None:
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        "Привет!\nЯ бот, который деплоит Feecc\nНапиши /deploy для получения списка доступных вам деплоев."
    )


@dp.message_handler(commands=["deploy"])
async def send_deploy_info(message: types.Message) -> None:
    """
    This handler will be called when user sends `/deploy` command
    """
    keyboard = types.InlineKeyboardMarkup()
    for schema in SCHEMAS:
        keyboard.add(types.InlineKeyboardButton(text=schema, callback_data=f"deploy_{schema}"))
    await message.answer("Доступные для деплоя схемы:", reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith="deploy_"))
async def sent_deployment_schema(call: types.CallbackQuery):
    """
    This handler will catch 'deploy_*' calls
    """
    schema = await read_concrete_deployment_schema(call.data.split("_")[1])
    await call.message.answer(
        f"Деплой схемы {schema.name} (Таргет: {schema.target or 'Неизвестно'})\nДетали: {schema.chain} "
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
