"""En este archivo ira relacionado todo el CRUD, querys o acciones relacionadas con la tabla flask_task, osea 
   las tareas, la tabla flask task se encuentra en models, ya que es tratada como objeto gracias a sqlalchemy"""

#Lib para tratar el objeto relacional (base de datos a objeto)
#from sqlalchemy.orm import session
#importo tabla o modelo relacional respectivo a las tareas
from modular_app.tasks import models
#importo base de datos
from modular_app import oDb

#Obtener por id de task
def getTaskById(taskId:int):
    #Esto es traducido internamente a sql como SELECT * FROM flask_tasks WHERE id = x
    #task = oSessionDb.query(oTbTask).filter(oTbTask.id == idTask).first()
    
    #Get obedece a la PK
    task = oDb.session.query(models.Task).get(ident=taskId)
    
    #Obedece la PK
    #task = oTbTask.query.get_or_404(ident=idTask)

    return task

#listar todas las task
def getAllTask():
    #SELECT * FROM flask_tasks
    tasks = oDb.session.query(models.Task).all()
    
    return tasks

#Crear tarea
def createTask(taskName:str):
    #asigno argumentos a la clase iniciada del modelo (tabla) task
    #INSERT INTO flask_task (id, name) VALUES (x, x)
    newTask = models.Task(name=taskName)
    oDb.session.add(newTask)
    oDb.session.commit()
    oDb.session.refresh(newTask)

    return newTask

#Actualizar tarea
def updateTask(taskId:int, taskName:str):
    #obtengo tel obejto (registro) task que se actualizara
    updateTask = getTaskById(taskId)
    #Cambio nombre
    #UPDATE flask_task SET name = x WHERE id = x
    updateTask.name = taskName

    oDb.session.add(updateTask)
    oDb.session.commit()
    oDb.session.refresh(updateTask)

    return updateTask

#Elimina tarea
def deleteTask(taskId:int):
    #DELETE FROM flask_task WHERE id = x
    deleteTask = getTaskById(taskId)
    oDb.session.delete(deleteTask)
    oDb.session.commit()

#paginación
#SELECT * FROM flask_task LIMIT X OFFSET Y
def pagination(page:int, count:int):
    return models.Task.query.paginate(page=page, per_page=count)