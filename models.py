import os
from pydantic import BaseModel


class SchemaTarget(BaseModel):
    description: str | None = None
    action: str

    async def execute(self) -> None:
        """Execute target command from config"""
        os.system(self.action)


class Schema(BaseModel):
    name: str
    target: str | None
    chain: list[SchemaTarget]
