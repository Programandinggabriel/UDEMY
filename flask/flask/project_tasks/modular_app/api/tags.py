from flask import jsonify, abort

from flask_restful import Resource, reqparse

from modular_app.tasks import models
from modular_app import oDb

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='No existe el nombre para el tag')

class TagAPI(Resource):
    def get(self, id:int=None):
        if id:
            tag = models.Tag.query.get(ident=id)

            if tag is None:
                abort(code=400, description="No existe un tag con el id")
            
            else:
                response = {"id":tag.id, 
                                    "name":tag.name}
        else:
            tags = models.Tag.query.all()
            response = {}

            #Serializa respuesta alternativas (marshall_with o metodo de la clase)
            for tag in tags:
                response[tag.id] = {"name": tag.name}
            
        return jsonify(response)
    
    def post(self):
        args = parser.parse_args()

        if len(args['name']) <= 3:
            abort(code=404, description="name es demasiado corto para ser asignado a el tag")

        newTag = models.Tag(name=args["name"])

        oDb.session.add(newTag)
        oDb.session.commit()
        oDb.session.refresh(newTag)

        
        return jsonify({"id":newTag.id, 
                        "name": newTag.name})
    
    def put(self, id:int=None):
        if id:
            args = parser.parse_args()
            tagUpdate = models.Tag.query.get(ident=id)
            
            if not tagUpdate:
                abort(code=404, description="No existe el tag por el id")

            tagUpdate.name = args["name"]

            oDb.session.add(tagUpdate)
            oDb.session.commit()
            oDb.session.refresh(tagUpdate)

            return jsonify({"id":tagUpdate.id,
                            "name":tagUpdate.name}) 

        else:
            abort(code=400, description="Falta el ID de el tag")

    def delete(self, id:int=None):
        if id:
            tagDelete = models.Tag.query.get(ident=id)

            if not tagDelete:
                abort(code=404, description="No existe el tag por el id")

            oDb.session.delete(tagDelete)
            oDb.session.commit()

            return jsonify({"msj":"Tag eliminado correctamente"})
        else:
            abort(code=400, description="Falta el ID de el tag")