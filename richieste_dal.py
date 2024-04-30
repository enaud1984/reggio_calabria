from typing import List, Optional


from sqlalchemy import update, delete,asc
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from datetime import datetime
#from config import DEFAULT_LOAD_TYPE, DEFAULT_STATUS
from richieste_entity import RequestEntityUpload, RequestEntityLoad, RequestModel, RequestModelExecution


def sqlalchemy_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class RichiesteUpload:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.model = RequestEntityUpload

    async def create_request(self, ID_SHAPE: int, SHAPEFILE: str,DATE_UPLOAD:datetime,STATUS:str,
                             GROUP_ID: str, PATH_SHAPEFILE: str,MD5: str, USERFILE:list, SRID:int,RESPONSE:dict={}):

        new_request = self.model(ID_SHAPE=ID_SHAPE, SHAPEFILE=SHAPEFILE, DATE_UPLOAD=DATE_UPLOAD,STATUS=STATUS,
                                 GROUP_ID=GROUP_ID,SRID=SRID,PATH_SHAPEFILE=PATH_SHAPEFILE,MD5=MD5, USERFILE=USERFILE,
                                 RESPONSE=RESPONSE)

        self.db_session.add(new_request)
        await self.db_session.flush()
        return new_request

    async def get_all_requests(self, ID_SHAPE=None, GROUP_ID=None, skip: int = 0, limit: int = 100):
        stmt = select(self.model)
        if GROUP_ID is not None and ID_SHAPE is not None:
            q = await self.db_session.execute(
                stmt.where(self.model.ID_SHAPE == ID_SHAPE and self.model.GROUP_ID == GROUP_ID).offset(skip).limit(limit))
        elif ID_SHAPE is None and GROUP_ID is not None:
            q = await self.db_session.execute(stmt.where(self.model.GROUP_ID == GROUP_ID).offset(skip).limit(limit))
        elif GROUP_ID is None and ID_SHAPE is not None:
            q = await self.db_session.execute(stmt.where(self.model.ID_SHAPE == ID_SHAPE).offset(skip).limit(limit))
        return q.scalars().all()

    async def get_request(self, id=None):
        stmt = select(self.model)
        q = await self.db_session.execute(stmt.where(self.model.ID == int(id)))
        return q.first()


    async def del_request(self, ID_SHAPE: int):
        q = await self.db_session.execute(delete(self.model).where(self.model.ID_SHAPE == ID_SHAPE))
        return q

    async def update_requestValidator(self, ID: int, USER_ID: Optional[str] = None,
                                      GROUP_ID: Optional[str]= None, SHAPEFILE: Optional[str]= None,
                                      STATO: Optional[str]= None,
                                      STATUS: Optional[str]= None,  # status RUNNING/QUEUED/FINISHED
                                      DATA_CARICAMENTO: Optional[datetime]= None,  # data inizio caricamento
                                      LOAD_TYPE: Optional[str]= None,
                                      # source_type, aggiungere anche la cartella oltre al file zip
                                      HOST_WORKER: Optional[str]= None,  # host del worker
                                      RUNNING: Optional[bool]= None,  # running del processo
                                      QUEUED: Optional[int]= None,
                                      PATH_SHAPEFILE:Optional[str]= None
                                      # accodamenti in corso per lo stesso group-id (ad esempio 2 file tim-->2righe
                                      ):

        q = update(self.model).where(self.model.ID == ID)
        if SHAPEFILE:
            q = q.values(name=SHAPEFILE)
        if STATO:
            q = q.values(STATO=STATO)
        if USER_ID:
            q = q.values(USER_ID=USER_ID)
        if GROUP_ID:
            q = q.values(GROUP_ID=GROUP_ID)
        if STATUS:
            q = q.values(STATUS=STATUS)
        if DATA_CARICAMENTO:
            q = q.values(DATA_CARICAMENTO=DATA_CARICAMENTO)
        if LOAD_TYPE:
            q = q.values(LOAD_TYPE=LOAD_TYPE)
        if RUNNING:
            q = q.values(RUNNING=RUNNING)
        if QUEUED:
            q = q.values(QUEUED=QUEUED)
        if HOST_WORKER:
            q = q.values(HOST_WORKER=HOST_WORKER)
        if PATH_SHAPEFILE:
            q = q.values(PATH_SHAPEFILE=PATH_SHAPEFILE)
        q.execution_options(synchronize_session="fetch")
        ret= await self.db_session.execute(q)
        return ret

class RichiesteLoad:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.model = RequestEntityLoad

    async def create_request(self, ID_SHAPE: int, DATE_LOAD:datetime,STATUS:str,
                             GROUP_ID: str, REQUEST:dict={}):

        new_request = self.model(ID_SHAPE=ID_SHAPE, DATE_LOAD=DATE_LOAD,STATUS=STATUS, GROUP_ID=GROUP_ID, REQUEST=REQUEST)

        self.db_session.add(new_request)
        await self.db_session.flush()
        return new_request

    async def get_all_requests(self, ID_SHAPE=None, GROUP_ID=None, skip: int = 0, limit: int = 100):
        stmt = select(self.model)
        if GROUP_ID is not None and ID_SHAPE is not None:
            q = await self.db_session.execute(
                stmt.where(self.model.ID_SHAPE == ID_SHAPE and self.model.GROUP_ID == GROUP_ID).offset(skip).limit(limit))
        elif ID_SHAPE is None and GROUP_ID is not None:
            q = await self.db_session.execute(stmt.where(self.model.GROUP_ID == GROUP_ID).offset(skip).limit(limit))
        elif GROUP_ID is None and ID_SHAPE is not None:
            q = await self.db_session.execute(stmt.where(self.model.ID_SHAPE == ID_SHAPE).offset(skip).limit(limit))
        return q.scalars().all()

    async def get_request(self, ID_SHAPE=None):
        stmt = select(self.model)
        q = await self.db_session.execute(stmt.where(self.model.ID_SHAPE == int(ID_SHAPE)))
        return q.first()

    async def del_request(self, ID_SHAPE: int):
        q = await self.db_session.execute(delete(self.model).where(self.model.ID_SHAPE == ID_SHAPE))
        return q

class RichiesteModel:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.model = RequestModel

    async def create_request(self, ID_MODEL: int, DATE_MODEL:datetime,STATUS:str,
                             GROUP_ID: str, CODE:str,PARAMS:dict={},LIBRARY:bool=False):

        new_request = self.model(ID_MODEL = ID_MODEL,
                                 DATE_MODEL = DATE_MODEL,
                                 STATUS = STATUS,
                                 GROUP_ID = GROUP_ID,
                                 CODE = CODE,
                                 PARAMS = PARAMS,
                                 LIBRARY = LIBRARY)

        self.db_session.add(new_request)
        await self.db_session.flush()
        return new_request

    async def get_all_requests(self, ID_MODEL=None, GROUP_ID=None, skip: int = 0, limit: int = 100):
        stmt = select(self.model)
        if GROUP_ID is not None and ID_MODEL is not None:
            q = await self.db_session.execute(
                stmt.where(self.model.ID_MODEL == ID_MODEL and self.model.GROUP_ID == GROUP_ID).offset(skip).limit(limit))
        elif ID_MODEL is None and GROUP_ID is not None:
            q = await self.db_session.execute(stmt.where(self.model.GROUP_ID == GROUP_ID).offset(skip).limit(limit))
        elif GROUP_ID is None and ID_MODEL is not None:
            q = await self.db_session.execute(stmt.where(self.model.ID_MODEL == ID_MODEL).offset(skip).limit(limit))
        return q.scalars().all()

    async def get_request(self, ID_MODEL=None):
        stmt = select(self.model)
        q = await self.db_session.execute(stmt.where(self.model.ID_MODEL == int(ID_MODEL)))
        return q.first()

    async def del_request(self, ID_MODEL: int):
        q = await self.db_session.execute(delete(self.model).where(self.model.ID_MODEL == ID_MODEL))
        return q

class RichiesteExecution:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.model = RequestModelExecution

    async def create_request(self, ID_EXECUTION ,DATE_EXECUTION ,STATUS,GROUP_ID,FK_MODEL,FK_SHAPE,PARAMS,RESULTS,MAPPING_OUTPUT):

        new_request = self.model(ID_EXECUTION = ID_EXECUTION,
                                 DATE_EXECUTION = DATE_EXECUTION,
                                 STATUS = STATUS,
                                 GROUP_ID = GROUP_ID,
                                 FK_MODEL = FK_MODEL, #
                                 FK_SHAPE = FK_SHAPE,
                                 PARAMS = PARAMS,
                                 MAPPING_OUTPUT=MAPPING_OUTPUT,
                                 RESULTS = RESULTS)

        self.db_session.add(new_request)
        await self.db_session.flush()
        return new_request

    async def get_all_requests(self, ID_EXECUTION=None, GROUP_ID=None, skip: int = 0, limit: int = 100):
        stmt = select(self.model)
        if GROUP_ID is not None and ID_EXECUTION is not None:
            q = await self.db_session.execute(
                stmt.where(self.model.ID_EXECUTION == ID_EXECUTION and self.model.GROUP_ID == GROUP_ID).offset(skip).limit(limit))
        elif ID_EXECUTION is None and GROUP_ID is not None:
            q = await self.db_session.execute(stmt.where(self.model.GROUP_ID == GROUP_ID).offset(skip).limit(limit))
        elif GROUP_ID is None and ID_EXECUTION is not None:
            q = await self.db_session.execute(stmt.where(self.model.ID_EXECUTION == ID_EXECUTION).offset(skip).limit(limit))
        return q.scalars().all()

    async def get_request(self, ID_EXECUTION=None):
        stmt = select(self.model)
        q = await self.db_session.execute(stmt.where(self.model.ID_EXECUTION == int(ID_EXECUTION)))
        return q.first()

    async def del_request(self, ID_EXECUTION: int):
        q = await self.db_session.execute(delete(self.model).where(self.model.ID_EXECUTION == ID_EXECUTION))
        return q
