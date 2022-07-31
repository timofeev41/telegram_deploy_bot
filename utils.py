import json
import os
from models import Schema
from pydantic import parse_obj_as
from aiogram import types


def read_deployment_schemas_list() -> list[str]:
    return os.listdir("deployment_schemas")


async def read_concrete_deployment_schema(schema_file: str) -> Schema:
    schema = open("deployment_schemas/" + schema_file, mode="r", encoding="utf-8")
    return parse_obj_as(Schema, json.load(schema))


async def build_actions_keyboard(schema_file: str) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(types.InlineKeyboardButton(text="Деплой", callback_data=f"deploy_start_{schema_file}"))
    keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data=f"deploy_cancel_{schema_file}"))
    return keyboard
