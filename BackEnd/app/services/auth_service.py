from app.models.user import User
from app.db import db
from app.utils.jwt_helper import create_token

def register_user(email, password, role="student"):
    if User.query.filter_by(email=email).first():
        return {"error": "User already exists"}, 400
    user = User(email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {
"message": "User registered successfully"}, 201


def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"error": "Invalid credentials"}, 401
    
    token = create_token(user.id, user.email, user.role)
    return {"token": token}
