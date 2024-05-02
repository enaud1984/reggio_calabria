from logging.config import dictConfig
import uvicorn
from config import APP
import os
from logger_api import LogConfig

from config import R_HOME
os.environ['R_HOME'] = R_HOME

if __name__ == "__main__":
    log = LogConfig().model_dump()
    if not os.path.isdir("log"):
        os.makedirs("log")
    if not os.path.isdir("to_upload"):
        os.makedirs("to_upload")
    if not os.path.isdir("data"):
        os.makedirs("data")
    dictConfig(log)
    print("started 127.0.0.1 port 5000")
    uvicorn.run(APP, host="127.0.0.1", port=5000)