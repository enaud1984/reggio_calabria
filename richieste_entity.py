
from sqlalchemy import Column, Integer, String,TIMESTAMP,Boolean,JSON,ARRAY

from config import Base
import logging

log=logging.getLogger(__name__)
class RequestEntityUpload(Base):
    __tablename__ = 'richieste_upload'
    __table_args__ = {'schema': 'public'}

    ID_SHAPE = Column(Integer, primary_key=True)
    SHAPEFILE = Column(String, nullable=True) #nome zip file
    DATE_UPLOAD	= Column(TIMESTAMP, nullable=True) #data upload
    STATUS = Column(String, nullable=True) #status RUNNING/QUEUED/FINISHED
    GROUP_ID = Column(String, nullable=False)
    SRID=Column(Integer, nullable=False)
    PATH_SHAPEFILE	= Column(String, nullable=True)
    MD5	= Column(String, nullable=True) #md5 del file zip per verificare che non sia già caricato
    USERFILE = Column(ARRAY(String), nullable=True) #elenco nome_file caricati
    RESPONSE = Column(JSON, nullable=True)  #json della richiesta precedente

    def __str__(self):
        path=self.PATH_SHAPEFILE.replace("\\","/")
        return ("{"+'"Request":{'
                f'"ID_SHAPE"="{self.ID_SHAPE}",'     
                f'"SHAPEFILE"="{self.SHAPEFILE}",'
                f'"STATUS"="{self.STATUS}",'
                f'"GROUP_ID"="{self.GROUP_ID}",'
                f'"DATA_UPLOAD"="{self.DATE_UPLOAD}",'
                f'"PATH_SHAPEFILE"="{path}",'
                f'"MD5"="{self.MD5}",'
                f'"USERFILE"="{self.USERFILE}",'    
                f'"RESPONSE"="{self.RESPONSE}",'    
                "}}").replace('"None"',"null").replace("=",":")


    def to_json(self):
        path=self.PATH_SHAPEFILE.replace("\\","/")
        return {"Request":{
                "ID_SHAPE":{self.ID_SHAPE},
                "SHAPEFILE":self.SHAPEFILE,
                "STATUS":self.STATUS,
                "GROUP_ID":self.GROUP_ID,
                "DATA_UPLOAD":self.DATE_UPLOAD,
                "PATH_SHAPEFILE":path,
                "MD5":self.MD5,
                "USERFILE": self.USERFILE,
                "RESPONSE": self.RESPONSE,
            }
        }

class RequestEntityLoad(Base):
    __tablename__ = 'richieste_load'
    __table_args__ = {'schema': 'public'}

    ID_SHAPE = Column(Integer, primary_key=True)
    DATE_LOAD = Column(TIMESTAMP, nullable=True) #data upload
    STATUS = Column(String, nullable=True) #status RUNNING/QUEUED/FINISHED
    GROUP_ID = Column(String, nullable=False)
    REQUEST = Column(JSON, nullable=True)  #json della richiesta precedente editato



    def __str__(self):
        return ("{"+'"Request":{'
                    f'"ID_SHAPE"="{self.ID_SHAPE}",'
                    f'"STATUS"="{self.STATUS}",'
                    f'"GROUP_ID"="{self.GROUP_ID}",'
                    f'"DATE_LOAD"="{self.DATE_LOAD}",'
                    f'"REQUEST"="{self.REQUEST}",'
                    "}}").replace('"None"',"null").replace("=",":")


    def to_json(self):
        return {"Request":{
            "ID_SHAPE":{self.ID_SHAPE},
            "STATUS":self.STATUS,
            "GROUP_ID":self.GROUP_ID,
            "DATE_LOAD":self.DATE_LOAD,
            "REQUEST":self.REQUEST,
        }
        }

class RequestModel(Base):
    __tablename__ = 'models'
    __table_args__ = {'schema': 'public'}


    ID_MODEL = Column(Integer, primary_key=True)
    DATE_MODEL = Column(TIMESTAMP, nullable=True) #data upload
    STATUS = Column(String, nullable=True) #status RUNNING/QUEUED/FINISHED
    GROUP_ID = Column(String, nullable=False)
    CODE = Column(String, nullable=False)
    PARAMS = Column(JSON, nullable=True)  #json della richiesta precedente editato
    LIBRARY = Column(Boolean, nullable=False)  #flag library

    def __str__(self):
        return ("{"+'"Request":{'
                    f'"ID_MODEL"="{self.ID_MODEL}",'
                    f'"DATE_MODEL"="{self.DATE_MODEL}",'
                    f'"STATUS"="{self.STATUS}",'
                    f'"CODE"="{self.CODE}",'
                    f'"PARAMS"="{self.PARAMS}",'
                    "}}").replace('"None"',"null").replace("=",":")


    def to_json(self):
        return {"Request":{
            "ID_MODEL":{self.ID_MODEL},
            "DATE_MODEL":self.DATE_MODEL,
            "STATUS":self.STATUS,
            "CODE":self.CODE,
            "PARAMS":self.PARAMS,
        }
        }

class ModelExecution(Base):
    __tablename__ = 'model_execution'
    __table_args__ = {'schema': 'public'}


    ID_EXECUTION = Column(Integer, primary_key=True)
    DATE_EXECUTION = Column(TIMESTAMP, nullable=True) #data upload
    STATUS = Column(String, nullable=True) #status RUNNING/QUEUED/FINISHED
    GROUP_ID = Column(String, nullable=False) # group id
    FK_MODEL = Column(Integer, nullable=False) # fk ad un modello
    FK_SHAPE = Column(Integer, nullable=False) # fk ad un load su geoServer
    FK_SHAPE_ZIP = Column(Integer, nullable=False) # fk ad uno zip
    PARAMS = Column(JSON, nullable=True)  #json della richiesta precedente editato
    RESULTS = Column(JSON, nullable=True)  #json della richiesta precedente editato

    def __str__(self):
        return ("{"+'"Request":{'
                    f'"ID_EXECUTION"="{self.ID_EXECUTION}",'
                    f'"DATE_EXECUTION"="{self.DATE_EXECUTION}",'
                    f'"STATUS"="{self.STATUS}",'
                    f'"GROUP_ID"="{self.GROUP_ID}",'
                    f'"FK_MODEL"="{self.FK_MODEL}",'
                    f'"FK_SHAPE"="{self.FK_SHAPE}",'
                    f'"FK_SHAPE_ZIP"="{self.FK_SHAPE_ZIP}",'
                    f'"PARAMS"="{self.PARAMS}",'
                    f'"RESULTS"="{self.RESULTS}",'
                    "}}").replace('"None"',"null").replace("=",":")


    def to_json(self):
        return {"Request":{
            "ID_EXECUTION":{self.ID_EXECUTION},
            "DATE_EXECUTION":self.DATE_EXECUTION,
            "STATUS":self.STATUS,
            "FK_MODEL":self.FK_MODEL,
            "FK_SHAPE":self.FK_SHAPE,
            "FK_SHAPE_ZIP":self.FK_SHAPE_ZIP,
            "PARAMS":self.PARAMS,
            "RESULTS":self.RESULTS,
        }
        }