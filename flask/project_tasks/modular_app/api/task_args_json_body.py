import os
from werkzeug.datastructures import FileStorage

from werkzeug.utils import secure_filename

from flask import abort, jsonify

from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required

from modular_app.tasks import sql_operations
from modular_app.documents import sql_operations as doc_sql_operations
from modular_app import app, config

#Configuro validacion de args
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='No existe el nombre de la tarea')
parser.add_argument('category_id', type=int, required=True, help='No existe el id de la categoria')

#Clase con el recurso que se va a crear
class TaskAPI(Resource):
    #method http
    @jwt_required()
    def get(self, id=None):
        if id:
            task = sql_operations.getTaskById(taskId=id)
           
            if task is None:
                abort(code=404, description="La tarea consultada no existe")
            else:
                #Extraigo los tags asignados a la tarea
                tagsList = []
                for tag in task.tags:
                    tagsList.append({"id":tag.id, "name":tag.name})

                response = {"id":task.id,
                            "name": task.name,
                            "category": task.category.name,
                            "tags": tagsList,
                            "document_id":task.document_id}
        else:
            response = {}
            tasks = sql_operations.getAllTask()

            #Serializa respuesta alternativas (marshall_with o metodo de la clase)
            for task in tasks:
                tagsList = []
                for tag in task.tags:
                    tagsList.append({"id":tag.id, "name":tag.name})
                
                #Cargo diccionario con la clave id task
                #valores (propiedades de el objeto actual task)
                response[task.id] = {"id":task.id,
                                     "name": task.name, 
                                     "category_id": task.category_id,
                                     "category": task.category.name,
                                     "tags": tagsList,
                                     "document_id":task.document_id}
        
        return jsonify(response)
    
    def post(self):
        args = parser.parse_args()

        if len(args['name']) <= 3:
            abort(code=400, description="name es demasiado corto para ser asignado")
        
        newTask = sql_operations.createTask(taskName=args['name'], 
                                            categoryType=args['category_id'])
            
        return jsonify({"id":newTask.id,
                        "name": newTask.name, 
                        "category": newTask.category.name,
                        "document_id":newTask.document_id})

    def put(self, id:int=None):
        args = parser.parse_args()

        if len(args['name']) <= 3:
            abort(code=400, description="name es demasiado corto para ser asignado")
        
        if id is not None:
            taskUpdate = sql_operations.getTaskById(taskId=id)

            if not taskUpdate:
                abort(code=404, description="Id de tarea no existe")
            
            taskUpdate = sql_operations.updateTask(taskId=taskUpdate.id, 
                                                    taskName=args['name'], 
                                                    categoryID=args['category_id'])

            return jsonify({"id":taskUpdate.id,
                            "name": taskUpdate.name, 
                            "category": taskUpdate.category.name,
                            "category_id": taskUpdate.category_id,
                            "document_id":taskUpdate.document_id})
        else:
            abort(code=400, description="Falta el ID de la tarea")

    def delete(self, id:int=None):
        if id is not None:
            taskDelete = sql_operations.getTaskById(taskId=id)

            if not taskDelete:
                abort(code=404, description="Id de tarea no existe")

            sql_operations.deleteTask(taskId=taskDelete.id)

            return jsonify({"msj":"Tarea eliminada correctamente"})
        else:
            abort(code=400, description="Falta el ID de la tarea")

#Creo otra clase que necesito para ADMINISTRAR EL RECURSO TASK
class TaskAPIPagination(Resource):
    @jwt_required()
    def get(self, page:int, count:int):
        tasks = sql_operations.pagination(page=page, count=count)
        response = {}

        #Serializa respuesta alternativas (marshall_with o metodo de la clase)
        for task in tasks:
            #Cargo diccionario con la clave id task
            #valores (propiedades de el objeto actual task)
            response[task.id] = {"name": task.name, 
                                 "category": task.category.name,
                                 "category_id": task.category_id,
                                 "document_id":task.document_id}
        
        return jsonify(response)
    
#Carga de archivos a las tareas
class TaskAPIUpload(Resource):
    def put(self, id:int=None):
        task = sql_operations.getTaskById(taskId=id)

        if not task:
            abort(code=404, description="No existe tarea con el id")

        parserUpload = reqparse.RequestParser()
        parserUpload.add_argument('file', type=FileStorage, required=True, location='files', help="Falta el documento a cargar")
        
        arg = parserUpload.parse_args()
        
        oFileStorage = arg['file']

        if oFileStorage and config.validate_ext_file(filename=oFileStorage.filename):
            fileName = secure_filename(oFileStorage.filename)
            oFileStorage.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
            oDocument = doc_sql_operations.createDocument(filename=fileName)
            
            #actualiza task con el respectivo id del document creado
            taskUpdate = sql_operations.updateTask(taskId=task.id, taskName=task.name, documentId=oDocument.id, categoryID=task.category_id)

        return jsonify({"id":taskUpdate.id,
                        "name": taskUpdate.name,
                        "category_id": taskUpdate.category_id, 
                        "document_id":taskUpdate.document_id})