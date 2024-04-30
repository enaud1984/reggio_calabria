import ast
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()
APP = os.getenv("APP","geo_labs:app")
ProgramFiles =os.getenv("ProgramFiles")
LOCALAPPDATA =os.getenv("LOCALAPPDATA")
R_VERSION = os.getenv("R_VERSION","R-4.3.3")#"R-4.4.0"
r_path = os.path.join(ProgramFiles,"R",R_VERSION)
real_path = r_path if os.path.isdir(r_path) else os.path.join(LOCALAPPDATA,"Programs","R",R_VERSION)
if os.path.isdir(r_path):
  R_HOME = os.getenv("R_HOME", real_path)
else:
  R_HOME = os.getenv("R_HOME")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "127.0.0.1")
POSTGRES_PORT= os.getenv("POSTGRES_PORT", "5444")
POSTGRES_DB= os.getenv("POSTGRES_DB","reggio_calabria")
SCHEMA = "geo_labs"
DB_BASE_URL=f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
DATABASE_URL_POSTGRES = os.getenv(
  "DATABASE_URL",f"postgresql+asyncpg://{DB_BASE_URL}"
)
connection_string = f"dbname='{POSTGRES_DB}' user='{POSTGRES_USER}' host='{POSTGRES_SERVER}' password='{POSTGRES_PASSWORD}'"
ENABLE_POOL_LOAD = os.getenv("ENABLE_POOL_LOAD","True")=="True"
if ENABLE_POOL_LOAD:
    engine_Db_no_async = create_engine(DATABASE_URL_POSTGRES.replace("+asyncpg",""),poolclass=NullPool)
else:
    engine_Db_no_async = create_engine(DATABASE_URL_POSTGRES.replace("+asyncpg",""))
engine_Db = create_async_engine(DATABASE_URL_POSTGRES)
async_session_Db= sessionmaker(engine_Db, expire_on_commit=False, class_=AsyncSession)

CHUNCKSIZE=eval(os.getenv("CHUNCKSIZE","30000"))
#parte di log usati in logger_api.py
LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")
HANDLERS=ast.literal_eval(os.getenv("LOG_HANDLER",'["default","file"]'))
PATH_TO_UPLOAD=os.path.join("to_upload")
LIST_SRID = ast.literal_eval(os.getenv("LIST_SRID","[3003,3004,23032,23033,23034,32632,32633,32634,32632,25832,25833,6707,6708,6709,6875,3857,7794,26591,26592,6705,102091,102092]"))
LIST_LANG = ["Python", "R"]
LIST_LOAD =["append","replace"]
#geoserver
GEOSERVER_LB_HOST_IP=os.getenv('GEOSERVER_LB_HOST_IP', '127.0.0.1')
GEOSERVER_LB_PORT=os.getenv('GEOSERVER_LB_PORT', '8080')
GEOSERVER_WEB_UI_LOCATION=os.getenv('GEOSERVER_LB_PORT', 'http://localhost/geoserver/')
GEOSERVER_PUBLIC_LOCATION=os.getenv('GEOSERVER_PUBLIC_LOCATION', 'http://localhost/geoserver/')
GEOSERVER_LOCATION=os.getenv('GEOSERVER_LOCATION', f'http://{GEOSERVER_LB_HOST_IP}:{GEOSERVER_LB_PORT}/geoserver/')
GEOSERVER_ADMIN_USER=os.getenv('GEOSERVER_ADMIN_USER', f'admin')
GEOSERVER_ADMIN_PASSWORD=os.getenv('GEOSERVER_ADMIN_PASSWORD', f'geoserver')
GEOSERVER_DB_SERVICES=os.getenv('GEOSERVER_DB_SERVICES', f'db')
GEOSERVER_DB_PORT=eval(os.getenv('GEOSERVER_DB_PORT', "5432"))

EVICTOR_RUN_PERIODICITY=eval(os.getenv('GS_EVICTOR_RUN_PERIODICITY','300'))
MAX_OPEN_PREPARED_STATEMENTS=eval(os.getenv('GS_MAX_OPEN_PREPARED_STATEMENTS','50'))
BATCH_INSERT_SIZE=eval(os.getenv('GS_BATCH_INSERT_SIZE','1'))
PREPAREDSTATEMENTS=os.getenv('GS_PREPAREDSTATEMENTS'	,"false")
LOOSE_BBOX=os.getenv('GS_LOOSE_BBOX',"true")
ESTIMATED_EXTENDS=os.getenv('GS_ESTIMATED_EXTENDS',"true")
FETCH_SIZE=eval(os.getenv('GS_FETCH_SIZE','1000'))
VALIDATE_CONNECTIONS=os.getenv('GS_VALIDATE_CONNECTIONS',"true")
SUPPORT_ON_THE_FLY_GEOMETRY_SIMPLIFICATION=os.getenv('GS_SUPPORT_ON_THE_FLY_GEOMETRY_SIMPLIFICATION',"true")
CONNECTION_TIMEOUT=eval(os.getenv('GS_CONNECTION_TIMEOUT','20'))
MIN_CONNECTIONS=eval(os.getenv('GS_MIN_CONNECTIONS','1'))
MAX_CONNECTIONS=eval(os.getenv('GS_MAX_CONNECTIONS','10'))
EVICTOR_TESTS_PER_RUN=eval(os.getenv('GS_EVICTOR_TESTS_PER_RUN','3'))
TEST_WHILE_IDLE=os.getenv('GS_TEST_WHILE_IDLE',"true")
MAX_CONNECTION_IDLE_TIME=eval(os.getenv('GS_MAX_CONNECTION_IDLE_TIME','300'))

ONSTART_DROP_CREATE= ast.eval(os.getenv('ONSTART_DROP_CREATE','False'))
