from typing import List, Optional


from sqlalchemy import update, delete,asc
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from datetime import datetime
#from config import DEFAULT_LOAD_TYPE, DEFAULT_STATUS
from richieste_entity import RequestEntityUpload


def sqlalchemy_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class RichiesteDAL:
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

    async def get_all_requests(self, id=None, group_id=None, skip: int = 0, limit: int = 100):
        stmt = select(self.model)
        if group_id is not None and id is not None:
            q = await self.db_session.execute(
                stmt.where(self.model.ID == id and self.model.GROUP_ID == group_id).offset(skip).limit(limit))
        elif id is None and group_id is not None:
            q = await self.db_session.execute(stmt.where(self.model.GROUP_ID == group_id).offset(skip).limit(limit))
        elif group_id is None and id is not None:
            q = await self.db_session.execute(stmt.where(self.model.ID == id).offset(skip).limit(limit))
        return q.scalars().all()

    async def get_request(self, id=None):
        stmt = select(self.model)
        q = await self.db_session.execute(stmt.where(self.model.ID == int(id)))
        return q.first()

    async def get_host_worker(self, group_id=None):
        stmt = select(self.model.HOST_WORKER)
        if group_id:
            result = await self.db_session.execute(stmt.where(self.model.GROUP_ID == group_id and self.model.HOST_WORKER is not None))
        else:
            result = await self.db_session.execute(stmt.where(self.model.HOST_WORKER is not None))
        host_workers = result.scalar()

        if host_workers is not None:
            return host_workers
        else:
            return []

    async def get_host_worker_not_completed(self):
        stmt = select(self.model.ID,self.model.HOST_WORKER,self.model.STATUS,self.model.QUEUED)

        result = await self.db_session.execute(stmt.where(self.model.RUNNING == True and self.model.HOST_WORKER is not None).order_by(self.model.QUEUED,asc(self.model.QUEUED)))
        host_worker_status_map = [{"ID": row[0],"HOST":row[1],"STATUS":row[2],"REQUEST_PARAMETER":row.REQUEST_PARAMETER,"QUEUED":row.QUEUED} for row in result]
        host_worker_status_map=sorted(host_worker_status_map, key=lambda x: x['QUEUED'])
        return host_worker_status_map

    async def del_request(self, id: int):
        q = await self.db_session.execute(delete(self.model).where(self.model.ID == id))
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

