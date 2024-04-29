
from sqlalchemy import Column, Integer, String,TIMESTAMP,Boolean,JSON

from config import Base
import logging

log=logging.getLogger(__name__)
class RequestEntity:

    __tablename__ = 'richieste'
    __table_args__ = {'schema': 'public'}

    ID = Column(Integer, primary_key=True)
    SHAPEFILE = Column(String, nullable=True) #nome zip file
    DATE_UPLOAD	= Column(TIMESTAMP, nullable=True) #data upload
    DATA_LOAD= Column(TIMESTAMP, nullable=False) #data inizio caricamento
    DATA_EXECUTION= Column(TIMESTAMP, nullable=True) #data_execution
    STATUS = Column(String, nullable=True) #status RUNNING/QUEUED/FINISHED
    GROUP_ID	= Column(String, nullable=False)	
    PATH_SHAPEFILE	= Column(String, nullable=True)
    MD5	= Column(String, nullable=True)	#md5 del file zip per verificare che non sia già caricato
    USERFILE	= Column(String, nullable=True) #elenco nome_file caricati
    LOAD_TYPE	= Column(String, nullable=True) #source_type, aggiungere anche la cartella oltre al file zip
    ESITO= Column(String, nullable=True) #ok|KO
    RESULTS = Column(String, nullable=True) # json con i campi dell'esito del pod, corrisponde a result in java

    def __str__(self):
        path=self.PATH_SHAPEFILE.replace("\\","/")
        return ("{"+'"Request":{'
                f'"ID"="{self.ID}",'     
                f'"SHAPEFILE"="{self.SHAPEFILE}",'
                f'"STATUS"="{self.STATUS}",'
                f'"GROUP_ID"="{self.GROUP_ID}",'
                f'"DATA_UPLOAD"="{self.DATA_UPLOAD}",'
                f'"DATA_LOAD"="{self.DATA_LOAD}",'
                f'"DATA_EXECUTION"="{self.DATA_EXECUTION}",'
                f'"PATH_SHAPEFILE"="{path}",'
                f'"MD5"="{self.MD5}",'
                f'"ESITO"="{self.ESITO}",'
                f'"RESULTS"="{self.RESULTS}"'
                "}}").replace('"None"',"null").replace("=",":")


    def to_json(self):
        path=self.PATH_SHAPEFILE.replace("\\","/")
        return {"Request":{
                "ID":{self.ID},     
                "SHAPEFILE":self.SHAPEFILE,
                "STATUS":self.STATUS,
                "GROUP_ID":self.GROUP_ID,
                "DATA_UPLOAD":self.DATA_UPLOAD,
                "DATA_LOAD":self.DATA_LOAD,
                "DATA_EXECUTION":self.DATA_EXECUTION,
                "PATH_SHAPEFILE":path,
                "MD5":self.MD5,
                "ESITO":self.ESITO,
                "RESULTS":self.RESULTS
            }
        }

    


