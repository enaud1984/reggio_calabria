from typing import List

from pydantic import BaseModel


class CodeInput(BaseModel):
    id_execute: int
    model_id: int
    shape_id: int
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
    srid: int = None
    df_out: bool = False

class MapTables(BaseModel):
    data: List[ColumnResponse]

    def to_dict(self):
        return {"data": [column_response.__dict__ for column_response in self.data]}
