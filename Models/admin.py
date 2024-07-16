from pydantic import BaseModel


class LoginSesion(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    password: str
    name_user: str
    acceso: bool
    activo: bool
    foto_perfil: str
    tipo: str
    token: str


class UserRegister(BaseModel):
    id: str
    email: str
    password: str
    name_user: str
    foto_perfil: str
    tipo: str
