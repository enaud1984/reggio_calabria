from pydantic import BaseModel


class CodeInput(BaseModel):
    code: str
    language: str
    params:dict
