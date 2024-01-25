from modular_app.auth.models import User

def authenticate(username:str, password:str):
    user = User.query.filter(User.userName == username).first()

    if not user: 
        return None
    
    if not user.validatePasword(password=password):
        return None
    
    return user
