from modular_app import oDb
from modular_app.auth import models

def getUserByUserName(username:str):
    user = models.User.query.filter_by(userName=username).first()
    return user

def createUser(username:str, password:str):
    newUser = models.User(userName=username, password=password)

    oDb.session.add(newUser)
    oDb.session.commit()

    return newUser