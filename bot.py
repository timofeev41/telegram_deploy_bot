from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
import os

from utils import build_actions_keyboard, read_concrete_deployment_schema, read_deployment_schemas_list

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
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    for schema in SCHEMAS:
        keyboard.add(types.InlineKeyboardButton(text=schema, callback_data=f"info_{schema}"))
    await message.answer("Доступные для деплоя схемы:", reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith="info_"))
async def send_deployment_info(call: types.CallbackQuery):
    """
    This handler will catch 'info_*' calls
    """
    try:
        schema = await read_concrete_deployment_schema(call.data[5:])
        await call.message.edit_text(
            f"Деплой схемы {schema.name} (Таргет: {schema.target or 'Неизвестно'})\nДетали: {schema.chain} ",
            reply_markup=await build_actions_keyboard(call.data[5:]),
        )
    except FileNotFoundError:
        await call.message.edit_text(f"Произошла ошибка в обработке схемы {call.data[5:]}")


@dp.callback_query_handler(Text(startswith="deploy_"))
async def send_deployment_schema(call: types.CallbackQuery):
    """
    This handler will catch 'deploy_*' calls
    """
    call_data = call.data[7:]
    if call_data.startswith("cancel"):
        await call.message.edit_text("Деплой схемы отменен")
    elif call_data.startswith("start"):
        await call.message.edit_text(f"Деплой схемы {call_data[6:]}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
