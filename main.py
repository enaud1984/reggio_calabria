import logging
from logging.config import dictConfig

from fastapi import FastAPI
import uvicorn
from starlette.responses import JSONResponse
from config import *
from utility import shapeFile2Postgis
from logger_api import LogConfig
import traceback

app = FastAPI(summary= "Applicativo per la gestione di file shape",
    description="""
        """,
    version= "0.0.1")


logger = logging.getLogger(APP)
@app.post("/shape_file2postgis")
async def shape_file2postgis(file_zip:str, schema:str=None):
    conn_str_db = f"host='{POSTGRES_SERVER}' port='{POSTGRES_PORT}' dbname='{POSTGRES_DB}' user='{POSTGRES_USER}' password='{POSTGRES_PASSWORD}'"
    try:
        result=shapeFile2Postgis(file_zip,conn_str_db,schema)
        return JSONResponse(content={"result": result,"esito":"OK"}, status_code=201)
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        print(f"Error:{e}")
        traceback.print_exc()
        return JSONResponse(content={"esito":"KO","error": str(e)}, status_code=501)


if __name__ == "__main__":
    log = LogConfig().model_dump()
    if not os.path.isdir("log"):
        os.makedirs("log")
    dictConfig(log)
    print("started 127.0.0.1 port 5000")
    uvicorn.run(APP, host="127.0.0.1", port=5000)