"""
Documentos relacionados con tasks
"""

#from sqlalchemy.orm import session as oDbSession
from modular_app.documents import models
from modular_app import oDb

#Obtener documento por el id
def getDocumentById(id:int):
    document = oDb.session.query(models.Documents).get(ident=id)
    return document

#Insertar nuevo documento
def createDocument(filename:str):
    #separa extension del filename
    extension = filename.lower().rsplit(sep='.', maxsplit=1)[1]
    newDocument = models.Documents(name=filename, extension=extension)
    
    oDb.session.add(newDocument)
    oDb.session.commit()
    oDb.session.refresh(newDocument)

    return newDocument

def deleteDocument(id:int):
    delDocument = getDocumentById(id)
    oDb.session.delete(delDocument)
    oDb.session.commit()
    
    return True
