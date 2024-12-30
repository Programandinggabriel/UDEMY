from werkzeug.security import generate_password_hash, check_password_hash
 
from modular_app import oDb

class User(oDb.Model):
    __tablename__ = 'users'
    id = oDb.Column(oDb.Integer, primary_key=True)
    userName = oDb.Column(oDb.String(100))
    pwdHash = oDb.Column(oDb.String(500))
    email = oDb.Column(oDb.String(255), nullable=False, unique=True)
    emailConfirmedAt = oDb.Column(oDb.DateTime())
    
    firstName = oDb.Column(oDb.String(100), nullable=False)
    secondName = oDb.Column(oDb.String(100), nullable=False)

    def __init__(self, userName:str, password:str):
        self.userName = userName
        self.pwdHash = generate_password_hash(password)

    def validatePasword(self, password:str):
        return check_password_hash(self.pwdHash, password)
    
    def get_id(self):
        return str(self.id)
    
    #Propiedades de la clase usuario, se puede establecer la logica que sea necesaria
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymus(self):
        return False
    @property
    def serialize(self):
        return {"id":self.id, 
                "username": self.userName}