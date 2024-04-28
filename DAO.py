from pydantic import BaseModel


class CodeInput(BaseModel):
    id_model: str
    language: str
    params: dict
    data: dict  #json di oout di UPLOAD MODELLO PYTHON


map_temp={"filename": file,
          "schema": "",
          "table": table_name,
          "column": col,
          "tipo": tipo,
          "column_name": "",
          "import": True}
class ResponseUpload(BaseModel):
    filename:str,
    schema:str,
    table: str,
    column: col,
    tipo: tipo,
    column_name": "",
    import": True

