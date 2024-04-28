from typing import List

from pydantic import BaseModel


class CodeInput(BaseModel):
    id_model: str
    language: str
    params: dict
    data: dict  #json di oout di UPLOAD MODELLO PYTHON

class ColumnResponse(BaseModel):
    filename: str
    schema_name: str = "public"
    table: str
    column: str
    tipo: str
    column_name: str
    importing: bool = True
    isVariable: bool = False
    df_out: bool = False

class MapTables(BaseModel):
    data: List[ColumnResponse]