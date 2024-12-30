from flask import abort, jsonify

from flask_restful import Resource, reqparse

from modular_app.tasks import models

from modular_app import oDb

#Configuro validacion de args
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='No existe el nombre de la categoria')

#Clase con el recurso que se va a crear
class CategoriesAPI(Resource):
    #method http
    def get(self, id=None):
        if id:
            category = models.Category.query.get(ident=id)
           
            if category is None:
                abort(code=404, description="La categoria buscada no existe")
            else:
                response = {"id":category.id, 
                            "name":category.name}
        else:
            categories = models.Category.query.all()
            response = {}

            #Serializa respuesta alternativas (marshall_with o metodo de la clase)
            for category in categories:
                response[category.id] = {"name": category.name}
        
        return jsonify(response)
    
    def post(self):
        args = parser.parse_args()

        if len(args['name']) <= 3:
            abort(code=400, description="name es demasiado corto para ser asignado a la categoria")
        
        newCategory = models.Category(name=args['name'])
        
        oDb.session.add(newCategory)
        oDb.session.commit()
        oDb.session.refresh(newCategory)

        return jsonify({"id":newCategory.id, 
                        "name": newCategory.name})

    def put(self, id:int=None):
        if id:
            args = parser.parse_args()

            if len(args['name']) <= 3:
                abort(code=400, description="name es demasiado corto para ser asignado a la categoria")
            
            categoryUpdate = models.Category.query.get(ident=id)

            if not categoryUpdate:
                abort(code=404, description="Id de category no existe")
            
            categoryUpdate.name = args["name"]
            
            oDb.session.add(categoryUpdate)
            oDb.session.commit()
            oDb.session.refresh(categoryUpdate)

            return jsonify({"id":categoryUpdate.id,
                            "name":categoryUpdate.name})
        else:
            abort(code=400, description="Falta el ID de la categoria")

    def delete(self, id:int=None):
        if id is not None:
            categoryDelete = models.Category.query.get(ident=id)

            if not categoryDelete:
                abort(code=404, description="Id de category no existe")

            oDb.session.delete(categoryDelete)
            oDb.session.commit()

            return jsonify({"msj":"Categoria eliminada correctamente"})
        else:
            abort(code=400, description="Falta el ID de la categoria")