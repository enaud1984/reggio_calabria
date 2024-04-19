import logging
from logging.config import dictConfig
from fastapi import FastAPI
import uvicorn
from starlette.responses import JSONResponse
from config import APP
import os
from utility import shapeFile2Postgis
from logger_api import LogConfig
import traceback

if __name__ == "__main__":
    log = LogConfig().model_dump()
    if not os.path.isdir("log"):
        os.makedirs("log")
    dictConfig(log)
    print("started 127.0.0.1 port 5000")
    uvicorn.run(APP, host="127.0.0.1", port=5000)