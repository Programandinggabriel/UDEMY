"""Este arcivo 'models.py' funciona para registrar todos los modelos (tablas) de la bd, 
   que esten relacionados con las tareas o tasks, asi comunicarnos con la bd.

   FACILITA LA MIGRACION DE LA APP YA QUE NO SE NECESITA DE UN ARCHIVO EXTERNO
   POR EL CONTROL QUE SE REALIZA MEDIANTE SQLALCHEMY A LA RESPECTIVA BD"""

from modular_app import oDb

#Clase task (modelo base de datos). Tabla flask_tasks 
#Este se entiende como la clase task (tabla de la bd task)
class Task(oDb.Model):
    __tablename__ = 'flask_tasks'
    #Campos
    id = oDb.Column(oDb.Integer, primary_key=True)
    name = oDb.Column(oDb.String(255))
