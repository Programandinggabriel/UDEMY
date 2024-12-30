from sqlalchemy.orm import relationship
from modular_app import oDb

#Clase Documents documentos de las apps
class Documents(oDb.Model):
    __tablename__ = 'tasks_documents'
    
    #Fields
    id = oDb.Column(oDb.Integer, primary_key=True)
    name = oDb.Column(oDb.String(255))
    extension = oDb.Column(oDb.String(10))