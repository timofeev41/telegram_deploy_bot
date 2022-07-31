from pydantic import BaseModel


class Schema(BaseModel):
    name: str
    target: str | None
    chain: list[str]
