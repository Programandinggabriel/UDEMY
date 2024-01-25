from flask import abort, request, jsonify

from flask_restful import Resource

from modular_app.tasks import sql_operations

#Clase con el recurso que se va a crear
class TaskAPI(Resource):
    #method http
    def get(self, id=None):
        if id:
            task = sql_operations.getTaskById(taskId=id)
           
            if task is None:
                abort(code=404)
            else:
                response = jsonify({
                    "id":task.id,
                    "name": task.name, 
                    "category": task.category.name,
                    "category_id": task.category_id})
        else:
            tasks = sql_operations.getAllTask()
            response = {}

            #Serializa respuesta alternativas (marshall_with o metodo de la clase)
            for task in tasks:
                #Cargo diccionario con la clave id task
                #valores (propiedades de el objeto actual task)
                response[task.id] = {"name": task.name, 
                                     "category": task.category.name,
                                     "category_id": task.category_id}
        
        return response
    
    def post(self):
        if validate_http_form():
            newTask = sql_operations.createTask(taskName=request.form['name'], 
                                                categoryType=request.form['category_id'])
            
            return jsonify({"name": newTask.name, 
                            "category": newTask.category.name,
                            "category_id": newTask.category_id})

    def put(self, id:int=None):
        if validate_http_form():
            if id is not None:
                taskUpdate = sql_operations.getTaskById(taskId=id)

                if not taskUpdate:
                    abort(code=404, description="Id de tarea no existe")
                
                taskUpdate = sql_operations.updateTask(taskId=taskUpdate.id, 
                                                       taskName=request.form['name'], 
                                                       categoryID=request.form['category_id'])
                
                return jsonify({"name": taskUpdate.name, 
                                "category": taskUpdate.category.name,
                                "category_id": taskUpdate.category_id})
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


#valida form metodo POST
def validate_http_form():
    if not request.form:
        abort(code=400, description="Falta el formulario")
    
    if not "name" in request.form:
        abort(code=400, description="name no encontrado")
    
    if not "category_id" in request.form:
        abort(code=400, description="category_id no encontrado")

    if len(request.form['name']) <= 3:
        abort(code=400, description="name es demasiado corto para ser asignado")

    if not request.form['category_id'].isnumeric():
        abort(code=400, description="category_id debe ser entero")

    return True