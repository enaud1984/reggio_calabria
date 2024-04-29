from pydantic import BaseModel
import os
from datetime import datetime

from config import APP,LOG_LEVEL,HANDLERS

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = APP
    LOG_FORMAT: str = '%(asctime)s\t%(name)s\t%(levelprefix)s\t%(message)s'#"%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = LOG_LEVEL

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }

    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file": {
           'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            "filename": os.path.join("log",f"{APP.split(':')[0]}_{datetime.strftime(datetime.now(),'%Y%m%d_%H%M')}.log"),
            'maxBytes': 10485760,
            'backupCount': 3
        }, "access": {
           'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            "filename": os.path.join("log",f"access_{APP.split(':')[0]}_{datetime.strftime(datetime.now(),'%Y%m%d')}.log"),
            'maxBytes': 10485760,
            'backupCount': 3
        }
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": HANDLERS, "level": LOG_LEVEL},
        "uvicorn":{
         "handlers":[
            "default"
         ],
         "level":"INFO"
        },
        "uvicorn.error":{
            "level":"INFO",
            "handlers":HANDLERS,
            "propagate":True
        },
        "uvicorn.access":{
            "handlers":[
                "access"
            ],
            "level":"INFO",
            "propagate":False
        }
    }