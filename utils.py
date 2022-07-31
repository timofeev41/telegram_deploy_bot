import json
import os
from models import Schema
from pydantic import parse_obj_as


def read_deployment_schemas_list() -> list[str]:
    return os.listdir("deployment_schemas")


async def read_concrete_deployment_schema(schema_file: str) -> Schema:
    schema = open("deployment_schemas/" + schema_file, mode="r", encoding="utf-8")
    return parse_obj_as(Schema, json.load(schema))
