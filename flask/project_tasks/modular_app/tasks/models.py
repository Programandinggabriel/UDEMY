"""Este arcivo 'models.py' funciona para registrar todos los modelos (tablas) de la bd, 
   que esten relacionados con las tareas o tasks, asi comunicarnos con la bd.

   FACILITA LA MIGRACION DE LA APP YA QUE NO SE NECESITA DE UN ARCHIVO EXTERNO
   POR EL CONTROL QUE SE REALIZA MEDIANTE SQLALCHEMY A LA RESPECTIVA BD"""

from modular_app import oDb
from sqlalchemy.orm import relationship #relacion entre tablas de la BD

#Pivot tables
#Esta tabla mostrara los muchos ID de task asociados a lo muchos ID de tag
task_tags = oDb.Table('pivot_tasks_tags',
                      oDb.Column('task_id', oDb.Integer, oDb.ForeignKey('tasks.id')),
                      oDb.Column('tag_id', oDb.Integer, oDb.ForeignKey('tasks_tags.id'))
                     )




#Models
"""Clase task (modelo base de datos). Tabla flask_tasks 
   Este se entiende como la clase task (tabla de la bd task)"""
class Task(oDb.Model):
    __tablename__ = 'tasks'
    
    #Fields
    id = oDb.Column(oDb.Integer, primary_key=True)
    name = oDb.Column(oDb.String(255))
    document_id = oDb.Column(oDb.Integer, oDb.ForeignKey('tasks_documents.id'), nullable=True)
    category_id = oDb.Column(oDb.Integer, oDb.ForeignKey('tasks_categories.id'), nullable=True)

    #Relationship
    """Relacion entre task y document (1 tarea puede contener 1 documento)
    por lo que document tendra el documento relacionado con el ID de la task consultada
    esto es igual a: document = oDb.session.query(models.Documents).get(document_id) 
    esta funcion en la ruta de update en el modelo task"""

    document = relationship('Documents', lazy='joined')
    category = relationship('Category', lazy='joined')
    tags = relationship(argument='Tag', secondary=task_tags)

"""Clase Category (Categorias de las TASK)
    Como no se creara un modulo de CRUD para las categories por ello se crean en el mismo archivo
    de modelos (tablas de base de datos) de TASK"""
class Category(oDb.Model):
    #Una Categoria puede estar en MUCHAS tareas
    __tablename__ = "tasks_categories"

    #Fields
    id = oDb.Column(oDb.Integer, primary_key=True)
    name = oDb.Column(oDb.String(100))

"""Clase Tag(tags de las tareas)"""
class Tag(oDb.Model):
    #MUCHOS tag pueden estar en MUCHAS tareas
    __tablename__="tasks_tags"

    #Fields
    id = oDb.Column(oDb.Integer, primary_key=True)
    name = oDb.Column(oDb.String(100))