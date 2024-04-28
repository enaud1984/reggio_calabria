import ast
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

APP = os.getenv("APP","geo_labs:app")
R_HOME = os.getenv("R_HOME", "C:\\Users\\gventura\\AppData\\Local\\Programs\\R\\R-4.3.3")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "127.0.0.1")
POSTGRES_PORT= os.getenv("POSTGRES_PORT", "5444")
POSTGRES_DB= os.getenv("POSTGRES_DB","reggio_calabria")
SCHEMA = "public"
DB_BASE_URL=f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
DATABASE_URL_POSTGRES = os.getenv(
  "DATABASE_URL",f"postgresql+asyncpg://{DB_BASE_URL}"
)
ENABLE_POOL_LOAD = os.getenv("ENABLE_POOL_LOAD","True")=="True"
if ENABLE_POOL_LOAD:
    engine_sinfiDb_no_async = create_engine(DATABASE_URL_POSTGRES.replace("+asyncpg",""),poolclass=NullPool)
else:
    engine_sinfiDb_no_async = create_engine(DATABASE_URL_POSTGRES.replace("+asyncpg",""))
CHUNCKSIZE=eval(os.getenv("CHUNCKSIZE","30000"))

#parte di log usati in logger_api.py
LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")
HANDLERS=ast.literal_eval(os.getenv("LOG_HANDLER",'["default","file"]'))

PATH_TO_UPLOAD=os.path.join("to_upload")

LIST_SRID = ast.literal_eval(os.getenv("LIST_SRID","[3003,3004,23032,23033,23034,32632,32633,32634,32632,25832,25833,6707,6708,6709,6875,3857,7794,26591,26592,6705,102091,102092]"))
