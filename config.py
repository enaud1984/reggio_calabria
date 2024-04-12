import ast
import os
from sqlalchemy import create_engine, NullPool

APP = os.getenv("APP","Poc_RC")

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